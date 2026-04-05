#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entrenar_leximus_ner_v8.py
──────────────────────────
Script de fine-tuning del modelo LexiMus-NER (spaCy + BETO) para
reconocimiento de personas y agrupaciones musicales en prensa histórica
española (COMPOSITOR, INTERPRETE, CANTANTE, AGRUPACION).

Mejoras respecto a v7:

  G) Ejemplos negativos (hard negatives): documentos donde el modelo
     confundió spans como entidades. Se añaden con entidades=[] para
     que el modelo aprenda a NO etiquetar esos contextos.
     Fuentes:
       - test_ampliado_negativos.json     (144 FP de la revisión actual)
       - negativos_ciclos_anteriores.json (78 FP de ciclos anteriores)

  H) Corpus positivo ampliado: 1.056 nuevas entidades validadas
     manualmente tras pre-revisión con Gemini 3 Flash.
     Fuente: test_ampliado_positivos.json

  Test set actualizado: test_reannotado.spacy (60 docs, 139 entidades)
  en lugar del test original incompleto (80 entidades).

Mantiene las 4 etiquetas: COMPOSITOR, INTERPRETE, CANTANTE, AGRUPACION.

Arquitectura:
  - Modelo base: es_dep_news_trf (spaCy español con BETO)
  - Fine-tuning: transformer + capa NER (resto del pipeline congelado)
  - Entity Ruler: gazetteer de entidades conocidas (entidades_ner_leximus.csv)

Uso básico (archivos en el mismo directorio que el script):
  python3 entrenar_leximus_ner_v8.py

Uso con rutas personalizadas:
  python3 entrenar_leximus_ner_v8.py \\
      --base-dir /ruta/a/datos \\
      --neg-dir  /ruta/a/negativos \\
      --modelo-base leximus_ner_v7_trf/model-best \\
      --output-dir leximus_ner_v8_trf

Dataset publicado en Zenodo:
  https://doi.org/10.5281/zenodo.19429405

Proyecto LexiMus — Universidad de Salamanca
PID2022-139589NB-C33 — MCIN/AEI
"""

import argparse
import csv
import json
import math
import random
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from thinc.api import set_gpu_allocator, prefer_gpu
set_gpu_allocator("pytorch")
gpu_activo = prefer_gpu()

import spacy
from spacy.tokens import DocBin, Doc, Span
from spacy.training import Example

print(f"  MPS/GPU activo: {gpu_activo}")


# ─── ARGUMENTOS ──────────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Fine-tuning LexiMus-NER v8 (spaCy + BETO)"
    )
    parser.add_argument(
        "--base-dir", type=Path,
        default=Path(__file__).parent,
        help="Directorio con los archivos .spacy y el CSV del gazetteer "
             "(por defecto: directorio del script)"
    )
    parser.add_argument(
        "--neg-dir", type=Path,
        default=None,
        help="Directorio con los JSON de negativos y positivos ampliados "
             "(por defecto: subdirectorio 'negativos' dentro de --base-dir)"
    )
    parser.add_argument(
        "--modelo-base", type=str,
        default="leximus_ner_v7_trf/model-best",
        help="Ruta al modelo base (relativa a --base-dir o absoluta)"
    )
    parser.add_argument(
        "--output-dir", type=str,
        default="leximus_ner_v8_trf",
        help="Directorio de salida para el modelo entrenado "
             "(relativo a --base-dir o absoluto)"
    )
    return parser.parse_args()


# ─── HIPERPARÁMETROS ─────────────────────────────────────────────────────────

MAX_EPOCHS        = 40
PATIENCE          = 12
DROPOUT           = 0.1
BATCH_SIZE        = 8
SEED              = 42

LR_MAX            = 5e-5
LR_MIN            = 5e-6
WARMUP_EPOCHS     = 3
DECAY_FACTOR      = 0.95

OVERSAMPLE_FACTOR = 3   # oversampling AGRUPACION (clase minoritaria)

ETIQUETAS = ["COMPOSITOR", "INTERPRETE", "CANTANTE", "AGRUPACION"]

# Métricas v7 en test_reannotado (referencia comparativa)
V7_TEST = {
    "global":     {"f1": 0.869, "p": 0.934, "r": 0.813},
    "COMPOSITOR": {"f1": 0.924, "p": 1.000, "r": 0.859},
    "INTERPRETE": {"f1": 0.839, "p": 0.867, "r": 0.812},
    "CANTANTE":   {"f1": 0.821, "p": 0.842, "r": 0.800},
    "AGRUPACION": {"f1": 0.741, "p": 0.909, "r": 0.625},
}


# ─── CARGA JSON ───────────────────────────────────────────────────────────────

def cargar_json_comentado(path: Path) -> list:
    """Carga JSON con líneas de comentario // al inicio."""
    texto = path.read_text(encoding="utf-8")
    texto = re.sub(r"^//.*\n", "", texto, flags=re.MULTILINE)
    return json.loads(texto)


# ─── CONVERSIÓN JSON → spaCy Docs ────────────────────────────────────────────

def json_a_docs(datos: list, nlp_blank, nombre: str) -> list[Doc]:
    """
    Convierte lista de ejemplos JSON a spaCy Docs.
    Cada item: {texto, entidades: [{inicio, fin, etiqueta, texto}], ...}
    Los negativos tienen entidades=[] → doc sin entidades (hard negative).
    """
    docs = []
    errores = 0
    for item in datos:
        texto = item.get("texto", "").strip()
        if not texto:
            continue
        doc = nlp_blank.make_doc(texto)
        spans = []
        for ent in item.get("entidades", []):
            ini = ent.get("inicio")
            fin = ent.get("fin")
            etq = ent.get("etiqueta", "")
            if ini is None or fin is None or etq not in ETIQUETAS:
                continue
            span = doc.char_span(ini, fin, label=etq, alignment_mode="expand")
            if span is not None:
                spans.append(span)
        try:
            doc.ents = spans
            docs.append(doc)
        except Exception:
            errores += 1
    print(f"  {nombre}: {len(docs)} docs cargados ({errores} errores de span)")
    return docs


# ─── UTILIDADES ──────────────────────────────────────────────────────────────

def detectar_inconsistencias(docs: list[Doc]) -> dict:
    conteo = defaultdict(lambda: defaultdict(int))
    for doc in docs:
        for ent in doc.ents:
            conteo[ent.text.strip().lower()][ent.label_] += 1
    return {t: dict(c) for t, c in conteo.items() if len(c) > 1}


def resolver_inconsistencias(docs: list[Doc], nlp_blank,
                              inconsistentes: dict) -> list[Doc]:
    """Resuelve spans con etiquetas inconsistentes eligiendo la mayoritaria."""
    resolucion = {
        texto: max(conteos, key=conteos.get)
        for texto, conteos in inconsistentes.items()
    }
    resultado = []
    for doc in docs:
        if not any(e.text.strip().lower() in resolucion for e in doc.ents):
            resultado.append(doc)
            continue
        doc_nuevo = nlp_blank.make_doc(doc.text)
        spans = []
        for ent in doc.ents:
            clave = ent.text.strip().lower()
            nueva = resolucion.get(clave, ent.label_)
            span  = doc_nuevo.char_span(ent.start_char, ent.end_char,
                                         label=nueva, alignment_mode="expand")
            if span:
                spans.append(span)
        try:
            doc_nuevo.ents = spans
            resultado.append(doc_nuevo)
        except Exception:
            resultado.append(doc)
    return resultado


def oversample_label(docs: list[Doc], label: str, factor: int) -> list[Doc]:
    """Oversampling de documentos con una etiqueta específica."""
    con_label = [d for d in docs if any(e.label_ == label for e in d.ents)]
    extra = con_label * (factor - 1)
    combinado = docs + extra
    random.shuffle(combinado)
    return combinado


def cargar_patrones_csv(csv_path: Path) -> list[dict]:
    """Carga patrones del gazetteer CSV para el Entity Ruler."""
    patrones = []
    vistos   = set()
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            etiqueta = fila["etiqueta"]
            if etiqueta not in ETIQUETAS:
                continue
            textos = {fila["texto"].strip()}
            if fila.get("variante_limpia", "").strip():
                textos.add(fila["variante_limpia"].strip())
            notas = fila.get("notas", "")
            if "Apodo:" in notas:
                apodo = notas.split("Apodo:")[-1].split("|")[0].strip()
                if apodo:
                    textos.add(apodo)
            for texto in textos:
                if not texto or len(texto) < 2:
                    continue
                clave = (texto.lower(), etiqueta)
                if clave in vistos:
                    continue
                vistos.add(clave)
                patrones.append({"label": etiqueta, "pattern": texto})
    return patrones


def asegurar_entity_ruler(nlp, csv_path: Path):
    if nlp.has_pipe("entity_ruler"):
        ruler = nlp.get_pipe("entity_ruler")
        print(f"  Entity Ruler ya presente: {len(ruler)} patrones")
        return
    patrones = cargar_patrones_csv(csv_path)
    ruler = nlp.add_pipe("entity_ruler", last=True,
                          config={"overwrite_ents": False})
    ruler.add_patterns(patrones)
    print(f"  Entity Ruler añadido: {len(ruler)} patrones")


def guardar_modelo(nlp, ruta: Path, pipes_activos: list):
    pipes_congelados = [p for p in nlp.component_names if p not in pipes_activos]
    for p in pipes_congelados:
        if nlp.has_pipe(p):
            nlp.enable_pipe(p)
    if ruta.exists():
        shutil.rmtree(ruta)
    nlp.to_disk(ruta)
    nlp_check = spacy.load(ruta)
    if nlp_check.has_pipe("entity_ruler"):
        ruler = nlp_check.get_pipe("entity_ruler")
        print(f"  ✓ Entity Ruler verificado en {ruta.name}: {len(ruler)} patrones")
    else:
        print(f"  ⚠ Entity Ruler NO encontrado en {ruta.name}")
    del nlp_check
    nlp.select_pipes(enable=pipes_activos)


def lr_para_epoca(epoca: int) -> float:
    if epoca <= WARMUP_EPOCHS:
        return LR_MIN + (LR_MAX - LR_MIN) * (epoca / WARMUP_EPOCHS)
    else:
        return LR_MAX * (DECAY_FACTOR ** (epoca - WARMUP_EPOCHS))


def cargar_docs(ruta: Path, nlp) -> list[Doc]:
    db = DocBin().from_disk(ruta)
    return list(db.get_docs(nlp.vocab))


def guardar_docbin(docs: list[Doc], ruta: Path):
    DocBin(docs=docs).to_disk(ruta)


def stats(docs: list[Doc], nombre: str):
    c = defaultdict(int)
    n_negativos = 0
    for d in docs:
        if not d.ents:
            n_negativos += 1
        for e in d.ents:
            c[e.label_] += 1
    total = sum(c.values())
    print(f"  {nombre}: {len(docs)} docs | {total} ents | "
          f"negativos={n_negativos} | {dict(sorted(c.items()))}")


def evaluar(nlp, ejemplos: list, nombre: str, referencia: dict | None = None):
    sc       = nlp.evaluate(ejemplos)
    f1       = sc.get("ents_f", 0.0)
    pre      = sc.get("ents_p", 0.0)
    rec      = sc.get("ents_r", 0.0)
    per_type = sc.get("ents_per_type", {})

    def delta(nuevo, ref_dict, key="f1"):
        if ref_dict is None:
            return ""
        d = nuevo - ref_dict.get(key, 0.0)
        return f"{d:+.3f}"

    print(f"\n  Evaluación en {nombre}:")
    print(f"  {'':15}  {'F1':>7}  {'P':>7}  {'R':>7}  {'Δ F1 vs v7':>11}")
    print(f"  {'─'*55}")
    ref_g = referencia.get("global") if referencia else None
    print(f"  {'GLOBAL':<15}  {f1:>7.3f}  {pre:>7.3f}  {rec:>7.3f}  {delta(f1, ref_g):>11}")
    for etq in ETIQUETAS:
        m    = per_type.get(etq, {})
        ef1  = m.get("f", 0.0)
        ep   = m.get("p", 0.0)
        er   = m.get("r", 0.0)
        ref_e = referencia.get(etq) if referencia else None
        print(f"  {etq:<15}  {ef1:>7.3f}  {ep:>7.3f}  {er:>7.3f}  {delta(ef1, ref_e):>11}")
    return f1


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    random.seed(SEED)

    # Resolver rutas
    BASE_DIR   = args.base_dir.resolve()
    NEG_DIR    = (args.neg_dir or BASE_DIR / "negativos").resolve()
    MODELO_BASE = (BASE_DIR / args.modelo_base).resolve() \
                  if not Path(args.modelo_base).is_absolute() \
                  else Path(args.modelo_base)
    OUTPUT_DIR  = (BASE_DIR / args.output_dir).resolve() \
                  if not Path(args.output_dir).is_absolute() \
                  else Path(args.output_dir)

    CSV_RULER      = BASE_DIR / "entidades_ner_leximus.csv"
    TRAIN_V7       = BASE_DIR / "train_v7.spacy"
    DEV_IN         = BASE_DIR / "dev_v6.spacy"
    TEST_REAN      = BASE_DIR / "test_reannotado.spacy"
    JSON_POSITIVOS = NEG_DIR  / "test_ampliado_positivos.json"
    JSON_NEG_NUEVO = NEG_DIR  / "test_ampliado_negativos.json"
    JSON_NEG_ANT   = NEG_DIR  / "negativos_ciclos_anteriores.json"

    print("=" * 66)
    print("Fine-tuning NER LexiMus v8 — Mejoras G+H (negativos + corpus ampliado)")
    print("=" * 66)
    print(f"  base-dir:    {BASE_DIR}")
    print(f"  neg-dir:     {NEG_DIR}")
    print(f"  modelo-base: {MODELO_BASE}")
    print(f"  output-dir:  {OUTPUT_DIR}")

    for ruta in [MODELO_BASE, CSV_RULER, TRAIN_V7, DEV_IN, TEST_REAN,
                 JSON_POSITIVOS, JSON_NEG_NUEVO, JSON_NEG_ANT]:
        if not ruta.exists():
            raise FileNotFoundError(f"No encontrado: {ruta}")

    # ── 1. Cargar modelo base ─────────────────────────────────────────────────
    print(f"\n[1/8] Cargando modelo base: {MODELO_BASE.name} ...")
    nlp = spacy.load(MODELO_BASE)
    print(f"  Componentes: {nlp.pipe_names}")
    asegurar_entity_ruler(nlp, CSV_RULER)
    nlp_blank = spacy.blank("es")

    # ── 2. Cargar corpus v7 existente ─────────────────────────────────────────
    print(f"\n[2/8] Cargando corpus v7...")
    train_docs = cargar_docs(TRAIN_V7, nlp)
    dev_docs   = cargar_docs(DEV_IN,   nlp)
    test_docs  = cargar_docs(TEST_REAN, nlp)
    stats(train_docs, "TRAIN v7 (base)")
    stats(dev_docs,   "DEV")
    stats(test_docs,  "TEST reannotado")

    # ── 3. Cargar y convertir nuevos datos (G+H) ──────────────────────────────
    print(f"\n[3/8] Cargando nuevos datos (positivos + negativos)...")
    datos_pos   = cargar_json_comentado(JSON_POSITIVOS)
    datos_neg_n = cargar_json_comentado(JSON_NEG_NUEVO)
    datos_neg_a = cargar_json_comentado(JSON_NEG_ANT)

    docs_pos   = json_a_docs(datos_pos,   nlp_blank, "Positivos nuevos (H)")
    docs_neg_n = json_a_docs(datos_neg_n, nlp_blank, "Negativos revisión actual (G)")
    docs_neg_a = json_a_docs(datos_neg_a, nlp_blank, "Negativos ciclos anteriores (G)")

    n_nuevos_pos = sum(len(d.ents) for d in docs_pos)
    n_nuevos_neg = len(docs_neg_n) + len(docs_neg_a)
    print(f"\n  Resumen nuevos datos:")
    print(f"    Positivos: {len(docs_pos)} docs, {n_nuevos_pos} entidades")
    print(f"    Negativos: {n_nuevos_neg} docs (hard negatives)")

    # ── 4. Fusionar corpus ────────────────────────────────────────────────────
    print(f"\n[4/8] Fusionando corpus v7 + nuevos datos...")
    train_docs = train_docs + docs_pos + docs_neg_n + docs_neg_a
    random.shuffle(train_docs)
    stats(train_docs, "TRAIN v8 (fusionado)")

    # ── 5. Resolver inconsistencias ───────────────────────────────────────────
    print(f"\n[5/8] Detectando y resolviendo inconsistencias...")
    docs_con_ents = [d for d in train_docs if d.ents]
    docs_sin_ents = [d for d in train_docs if not d.ents]

    inconsis = detectar_inconsistencias(docs_con_ents)
    print(f"  Spans inconsistentes: {len(inconsis)}")
    for texto, counts in sorted(inconsis.items(), key=lambda x: -sum(x[1].values()))[:10]:
        mayoritaria = max(counts, key=counts.get)
        print(f"    {repr(texto):40s}  {counts}  → {mayoritaria}")
    if len(inconsis) > 10:
        print(f"    ... (y {len(inconsis)-10} más)")

    docs_con_ents = resolver_inconsistencias(docs_con_ents, nlp_blank, inconsis)
    train_docs = docs_con_ents + docs_sin_ents
    random.shuffle(train_docs)

    # ── 6. Oversampling AGRUPACION ────────────────────────────────────────────
    print(f"\n[6/8] Oversampling AGRUPACION x{OVERSAMPLE_FACTOR}...")
    antes = sum(1 for d in train_docs if any(e.label_ == "AGRUPACION" for e in d.ents))
    train_docs = oversample_label(train_docs, "AGRUPACION", OVERSAMPLE_FACTOR)
    despues = sum(1 for d in train_docs if any(e.label_ == "AGRUPACION" for e in d.ents))
    stats(train_docs, "TRAIN v8 tras oversampling")
    print(f"  Docs AGRUPACION: {antes} → {despues}")

    guardar_docbin(train_docs, BASE_DIR / "train_v8.spacy")
    print("  Guardado: train_v8.spacy")

    # ── 7. Entrenamiento ──────────────────────────────────────────────────────
    print(f"\n[7/8] Preparando ejemplos...")
    train_ejs = [Example(nlp.make_doc(d.text), d) for d in train_docs]
    dev_ejs   = [Example(nlp.make_doc(d.text), d) for d in dev_docs]

    ner = nlp.get_pipe("ner")
    for etq in ETIQUETAS:
        ner.add_label(etq)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    mejor_dir  = OUTPUT_DIR / "model-best"
    ultimo_dir = OUTPUT_DIR / "model-last"

    if mejor_dir.exists():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copytree(mejor_dir, OUTPUT_DIR / f"model-best_backup_{ts}")
        print(f"  Backup del model-best anterior guardado.")

    # Re-entrenar transformer + NER; el resto del pipeline se congela
    pipes_activos = ["transformer", "ner"]
    nlp.select_pipes(enable=pipes_activos)
    optimizer = nlp.resume_training()

    print(f"\n  LR: warmup {LR_MIN:.0e}→{LR_MAX:.0e} ({WARMUP_EPOCHS} épocas) "
          f"+ decay x{DECAY_FACTOR}/época")
    print(f"  Épocas={MAX_EPOCHS}  Patience={PATIENCE}  Batch={BATCH_SIZE}")
    print(f"  Train: {len(train_ejs)} ejs  Dev: {len(dev_ejs)} ejs")
    print("─" * 66)
    print(f"{'Época':>5}  {'LR':>8}  {'Loss':>10}  {'F1 Dev':>8}  {'P':>7}  {'R':>7}")
    print("─" * 66)

    mejor_f1   = 0.0
    sin_mejora = 0

    for epoca in range(1, MAX_EPOCHS + 1):
        lr_actual = lr_para_epoca(epoca)
        optimizer.learn_rate = lr_actual

        random.shuffle(train_ejs)
        losses = {}
        for i in range(0, len(train_ejs), BATCH_SIZE):
            lote = train_ejs[i:i + BATCH_SIZE]
            nlp.update(lote, drop=DROPOUT, losses=losses, sgd=optimizer)

        loss_ner = losses.get("ner", 0.0)
        sc  = nlp.evaluate(dev_ejs)
        f1  = sc.get("ents_f", 0.0)
        pre = sc.get("ents_p", 0.0)
        rec = sc.get("ents_r", 0.0)

        print(f"{epoca:>5}  {lr_actual:>8.2e}  {loss_ner:>10.2f}  {f1:>8.3f}  "
              f"{pre:>7.3f}  {rec:>7.3f}", end="")

        if f1 > mejor_f1:
            mejor_f1   = f1
            sin_mejora = 0
            guardar_modelo(nlp, mejor_dir, pipes_activos)
            print("  ← mejor")
        else:
            sin_mejora += 1
            print(f"  ({sin_mejora}/{PATIENCE})")
            if sin_mejora >= PATIENCE:
                print(f"\n  Early stopping en época {epoca}.")
                break

    # Guardar model-last con pipeline completo
    pipes_congelados = [p for p in nlp.component_names if p not in pipes_activos]
    for p in pipes_congelados:
        if nlp.has_pipe(p):
            nlp.enable_pipe(p)
    if ultimo_dir.exists():
        shutil.rmtree(ultimo_dir)
    nlp.to_disk(ultimo_dir)

    # ── 8. Evaluación final ───────────────────────────────────────────────────
    print("\n" + "─" * 66)
    print("RESULTADOS FINALES")
    print("─" * 66)
    print(f"\nMejor F1 en dev: {mejor_f1:.3f}")

    if not mejor_dir.exists():
        print("\n  ⚠ No se guardó ningún model-best.")
        return

    print("\n[8/8] Evaluación detallada del model-best:")
    nlp_best = spacy.load(mejor_dir)

    if nlp_best.has_pipe("entity_ruler"):
        print(f"  Entity Ruler: {len(nlp_best.get_pipe('entity_ruler'))} patrones  ✓")
    else:
        print(f"  ⚠ Entity Ruler NO presente en model-best")

    dev_ejs_best  = [Example(nlp_best.make_doc(d.text), d) for d in dev_docs]
    evaluar(nlp_best, dev_ejs_best, nombre="dev")

    print(f"\n  {'─'*55}")
    print(f"  TEST SET REANNOTADO — test_reannotado.spacy (60 docs, 139 ents)")
    print(f"  {'─'*55}")

    test_ejs_best = [Example(nlp_best.make_doc(d.text), d) for d in test_docs]
    evaluar(nlp_best, test_ejs_best,
            nombre="test_reannotado.spacy", referencia=V7_TEST)

    print(f"\n  Δ F1 = diferencia respecto a v7 en el mismo test reannotado.")
    print(f"  Positivo = mejora. Negativo = regresión.")
    print(f"\nModelos guardados en:")
    print(f"  {mejor_dir}   ← usar este")
    print(f"  {ultimo_dir}")
    print(f"\nPara usar el modelo:")
    print(f"  import spacy")
    print(f"  nlp = spacy.load('{mejor_dir}')")
    print("─" * 66)


if __name__ == "__main__":
    main()
