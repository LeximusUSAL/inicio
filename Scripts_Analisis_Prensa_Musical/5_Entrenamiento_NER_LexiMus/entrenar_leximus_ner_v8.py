#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
entrenar_leximus_ner_v8.py
──────────────────────────
Estrategia v8 — Dev set alineado con evaluación manual

  ENTRENAMIENTO:
    - train_v6.spacy                    (corpus base limpio, sin oversampling de v7)
    - negativos_ciclos_anteriores.json  (78 hard negatives de ciclos previos)

  DEV (early stopping) — 900 docs de la revisión manual de 1.200:
    - 75% de test_ampliado_positivos.json  (~792 docs)
    - 75% de test_ampliado_negativos.json  (~108 docs)

  TEST FINAL — 300 docs restantes de la revisión manual:
    - 25% de test_ampliado_positivos.json  (~264 docs)
    - 25% de test_ampliado_negativos.json  (~36 docs)

  Referencia comparativa: v7 evaluado manualmente (F1 global = 0.869)

  La partición 75/25 usa SEED=42 → reproducible.

Mantiene las 4 etiquetas: COMPOSITOR, INTERPRETE, CANTANTE, AGRUPACION.

Uso:
  cd "/Users/maria/Desktop/NER LEXIMUS/Listados_Herramientas"
  python3 entrenar_leximus_ner_v8.py
"""

import csv, json, math, random, re, shutil
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

# ─── RUTAS ───────────────────────────────────────────────────────────────────

DIR_BASE    = Path("/Users/maria/Desktop/NER LEXIMUS/Listados_Herramientas")
DIR_NEG     = Path("/Users/maria/Desktop/NEGATIVOS_ENTRENAMIENTO_NER")

MODELO_BASE = DIR_BASE / "leximus_ner_v7_trf" / "model-best"
CSV_RULER   = DIR_BASE / "entidades_ner_leximus.csv"
TRAIN_BASE  = DIR_BASE / "train_v6.spacy"       # corpus base, sin oversampling de v7
OUTPUT_DIR  = DIR_BASE / "leximus_ner_v8_trf"

# Hard negatives de ciclos anteriores → van al entrenamiento
JSON_NEG_ANT  = DIR_NEG / "negativos_ciclos_anteriores.json"

# Las 1.200 revisadas manualmente → se parten en dev (900) + test (300)
JSON_TEST_POS = DIR_NEG / "test_ampliado_positivos.json"
JSON_TEST_NEG = DIR_NEG / "test_ampliado_negativos.json"

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

OVERSAMPLE_FACTOR = 3       # oversampling AGRUPACION
DEV_RATIO         = 0.75    # 75% → dev, 25% → test

ETIQUETAS = ["COMPOSITOR", "INTERPRETE", "CANTANTE", "AGRUPACION"]

# Métricas v7 evaluadas manualmente sobre 1.200 entidades (referencia)
V7_MANUAL = {
    "global":     {"f1": 0.869, "p": 0.934, "r": 0.813},
    "COMPOSITOR": {"f1": 0.924, "p": 1.000, "r": 0.859},
    "INTERPRETE": {"f1": 0.839, "p": 0.867, "r": 0.812},
    "CANTANTE":   {"f1": 0.821, "p": 0.842, "r": 0.800},
    "AGRUPACION": {"f1": 0.741, "p": 0.909, "r": 0.625},
}

# ─── CARGA JSON ───────────────────────────────────────────────────────────────

def cargar_json_comentado(path: Path) -> list:
    texto = path.read_text(encoding="utf-8")
    texto = re.sub(r"^//.*\n", "", texto, flags=re.MULTILINE)
    return json.loads(texto)

# ─── CONVERSIÓN JSON → spaCy Docs ────────────────────────────────────────────

def json_a_docs(datos: list, nlp_blank, nombre: str) -> list[Doc]:
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

def partir_docs(docs: list[Doc], ratio: float, seed: int):
    """Partición estratificada positivos/negativos con seed fijo."""
    rng = random.Random(seed)
    positivos = [d for d in docs if d.ents]
    negativos = [d for d in docs if not d.ents]
    rng.shuffle(positivos)
    rng.shuffle(negativos)
    corte_pos = int(len(positivos) * ratio)
    corte_neg = int(len(negativos) * ratio)
    dev  = positivos[:corte_pos]  + negativos[:corte_neg]
    test = positivos[corte_pos:]  + negativos[corte_neg:]
    rng.shuffle(dev)
    rng.shuffle(test)
    return dev, test

# ─── FUNCIONES ────────────────────────────────────────────────────────────────

def detectar_inconsistencias(docs: list[Doc]) -> dict:
    conteo = defaultdict(lambda: defaultdict(int))
    for doc in docs:
        for ent in doc.ents:
            conteo[ent.text.strip().lower()][ent.label_] += 1
    return {t: dict(c) for t, c in conteo.items() if len(c) > 1}

def resolver_inconsistencias(docs: list[Doc], nlp_blank,
                              inconsistentes: dict) -> list[Doc]:
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
    con_label = [d for d in docs if any(e.label_ == label for e in d.ents)]
    extra = con_label * (factor - 1)
    combinado = docs + extra
    random.shuffle(combinado)
    return combinado

def cargar_patrones_csv(csv_path: Path) -> list[dict]:
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

    # Verificar entity_ruler y añadirlo desde CSV si se perdió al guardar
    nlp_check = spacy.load(ruta)
    if nlp_check.has_pipe("entity_ruler"):
        ruler = nlp_check.get_pipe("entity_ruler")
        print(f"  ✓ Entity Ruler verificado en {ruta.name}: {len(ruler)} patrones")
    else:
        # select_pipes elimina entity_ruler del config.cfg — lo restauramos
        patrones = cargar_patrones_csv(CSV_RULER)
        ruler = nlp_check.add_pipe("entity_ruler", last=True,
                                    config={"overwrite_ents": False})
        ruler.add_patterns(patrones)
        nlp_check.to_disk(ruta)
        print(f"  ✓ Entity Ruler restaurado en {ruta.name}: {len(ruler)} patrones")
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
    n_neg = 0
    for d in docs:
        if not d.ents:
            n_neg += 1
        for e in d.ents:
            c[e.label_] += 1
    total = sum(c.values())
    print(f"  {nombre}: {len(docs)} docs | {total} ents | "
          f"negativos={n_neg} | {dict(sorted(c.items()))}")

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

    ref_label = "v7 manual" if referencia else ""
    print(f"\n  Evaluación en {nombre}:")
    print(f"  {'':15}  {'F1':>7}  {'P':>7}  {'R':>7}  {'Δ F1 vs ' + ref_label:>14}")
    print(f"  {'─'*58}")
    ref_g = referencia.get("global") if referencia else None
    print(f"  {'GLOBAL':<15}  {f1:>7.3f}  {pre:>7.3f}  {rec:>7.3f}  {delta(f1, ref_g):>14}")
    for etq in ETIQUETAS:
        m     = per_type.get(etq, {})
        ef1   = m.get("f", 0.0)
        ep    = m.get("p", 0.0)
        er    = m.get("r", 0.0)
        ref_e = referencia.get(etq) if referencia else None
        print(f"  {etq:<15}  {ef1:>7.3f}  {ep:>7.3f}  {er:>7.3f}  {delta(ef1, ref_e):>14}")
    return f1

# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    random.seed(SEED)

    print("=" * 66)
    print("Fine-tuning NER LexiMus v8 — Dev alineado + Entity Ruler activo en evaluación")
    print("=" * 66)

    for ruta in [MODELO_BASE, CSV_RULER, TRAIN_BASE,
                 JSON_NEG_ANT, JSON_TEST_POS, JSON_TEST_NEG]:
        if not ruta.exists():
            raise FileNotFoundError(f"No encontrado: {ruta}")

    # ── 1. Cargar modelo base v7 ──────────────────────────────────────────────
    print(f"\n[1/8] Cargando modelo base: leximus_ner_v7_trf/model-best ...")
    nlp = spacy.load(MODELO_BASE)
    print(f"  Componentes: {nlp.pipe_names}")
    asegurar_entity_ruler(nlp, CSV_RULER)
    nlp_blank = spacy.blank("es")

    # ── 2. Partir las 1.200 revisadas en dev (900) + test (300) ──────────────
    print(f"\n[2/8] Partiendo 1.200 revisadas manualmente en dev/test ({DEV_RATIO:.0%}/{1-DEV_RATIO:.0%})...")
    datos_pos = cargar_json_comentado(JSON_TEST_POS)
    datos_neg = cargar_json_comentado(JSON_TEST_NEG)
    docs_pos  = json_a_docs(datos_pos, nlp_blank, "Positivos (1.056)")
    docs_neg  = json_a_docs(datos_neg, nlp_blank, "Negativos (144)")
    todos_1200 = docs_pos + docs_neg

    dev_docs, test_docs = partir_docs(todos_1200, DEV_RATIO, SEED)
    stats(dev_docs,  f"DEV  (early stopping, {len(dev_docs)} docs)")
    stats(test_docs, f"TEST (evaluación final, {len(test_docs)} docs)")

    # ── 3. Cargar corpus de entrenamiento ─────────────────────────────────────
    print(f"\n[3/8] Cargando corpus de entrenamiento...")
    train_docs = cargar_docs(TRAIN_BASE, nlp)
    stats(train_docs, "TRAIN base (v6)")

    datos_neg_ant = cargar_json_comentado(JSON_NEG_ANT)
    docs_neg_ant  = json_a_docs(datos_neg_ant, nlp_blank, "Negativos ciclos anteriores (78)")

    # ── 4. Fusionar corpus de entrenamiento ───────────────────────────────────
    print(f"\n[4/8] Fusionando corpus base + hard negatives anteriores...")
    train_docs = train_docs + docs_neg_ant
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

    guardar_docbin(train_docs, DIR_BASE / "train_v8.spacy")
    print("  Guardado: train_v8.spacy")

    # ── 7. Entrenamiento ──────────────────────────────────────────────────────
    print(f"\n[7/8] Preparando ejemplos y entrenando...")
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

    pipes_activos = ["transformer", "ner"]
    nlp.select_pipes(enable=pipes_activos)
    optimizer = nlp.resume_training()

    print(f"\n  LR: warmup {LR_MIN:.0e}→{LR_MAX:.0e} ({WARMUP_EPOCHS} épocas) "
          f"+ decay x{DECAY_FACTOR}/época")
    print(f"  Épocas={MAX_EPOCHS}  Patience={PATIENCE}  Batch={BATCH_SIZE}")
    print(f"  Train: {len(train_ejs)} ejs  Dev: {len(dev_ejs)} ejs  Test: {len(test_docs)} docs")
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
        # Evaluar con el pipeline completo (NER + Entity Ruler), igual que en producción
        nlp.enable_pipe("entity_ruler")
        sc  = nlp.evaluate(dev_ejs)
        nlp.disable_pipe("entity_ruler")
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

    # Guardar model-last
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
    print(f"\nMejor F1 en dev (900 revisadas): {mejor_f1:.3f}")

    if not mejor_dir.exists():
        print("\n  ⚠ No se guardó ningún model-best.")
        return

    print("\n[8/8] Evaluación detallada del model-best:")
    nlp_best = spacy.load(mejor_dir)

    if nlp_best.has_pipe("entity_ruler"):
        print(f"  Entity Ruler: {len(nlp_best.get_pipe('entity_ruler'))} patrones  ✓")
    else:
        print(f"  ⚠ Entity Ruler NO presente en model-best")

    # 8a. Dev (900)
    dev_ejs_best = [Example(nlp_best.make_doc(d.text), d) for d in dev_docs]
    evaluar(nlp_best, dev_ejs_best, nombre=f"dev_manual ({len(dev_docs)} docs)")

    # 8b. Test final (300) — comparado con v7
    print(f"\n  {'─'*58}")
    print(f"  TEST FINAL ({len(test_docs)} docs revisados manualmente) vs v7")
    print(f"  {'─'*58}")
    test_ejs_best = [Example(nlp_best.make_doc(d.text), d) for d in test_docs]
    evaluar(nlp_best, test_ejs_best,
            nombre=f"test_manual ({len(test_docs)} docs)", referencia=V7_MANUAL)

    print(f"\n  Δ F1 = diferencia respecto a v7 evaluado manualmente.")
    print(f"  Positivo = mejora. Negativo = regresión.")
    print(f"\nModelos guardados en:")
    print(f"  {mejor_dir}   ← usar este")
    print(f"  {ultimo_dir}")
    print(f"\nPara usar:")
    print(f"  nlp = spacy.load('{mejor_dir}')")
    print("─" * 66)


if __name__ == "__main__":
    main()
