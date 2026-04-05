# Scripts de Análisis de Prensa Musical Española

Colección de 23 scripts Python para el análisis computacional de corpus de prensa y revistas musicales españolas (1788-2024).

## 📋 Descripción del Proyecto

Este repositorio contiene las principales herramientas de procesamiento de lenguaje natural y análisis estadístico desarrolladas para el proyecto **LexiMus** (Léxico y ontología de la música en español) desde la Universidad de Salamanca. Los scripts han procesado 25.8 millones de palabras distribuidas en 3,238 archivos de texto digitalizados de 19 revistas musicales españolas, abarcando más de dos siglos de periodismo musical. Los datos actualmente son provisionales porque las revistas tienen todavía bastante "ruido OCR". No obstante, se trata de una aproximación fundamental al análisis computacional de este tipo de fuentes, mostrando las posibilidades futuras una vez que las fuentes estén más limpias.

### Objetivos del Análisis

- **Análisis léxico musical**: Identificación y categorización de 150+ términos musicales (géneros, instrumentos, términos técnicos)
- **Estudio de sesgo de género**: Análisis sistemático de representación y tratamiento diferencial por género
- **Periodización histórica**: Análisis de 6 épocas desde el siglo XVIII, pasando por el periodo Romántico (1842-1900) hasta la era Democrática (1990-2024)
- **Distribución geográfica**: Estudio de cobertura Madrid/Barcelona/otras ciudades españolas

## 📂 Estructura del Repositorio

Además de los scripts específcos para revistas y prensa también hemos utilizado un script básico para buscar palabras clave en cualquier corpus de textos txt. Este recurso lo puedes encontrar aquí.  [**Búsquedas por palabras clave**](https://github.com/LeximusUSAL/buscador-palabras-corpus/blob/main/README.md) 🎵 disponible en GitHub.


### 1️⃣ Análisis de Revistas Musicales (6 scripts)

Scripts especializados para el procesamiento de revistas musicales especializadas:

- **`comprehensive_musical_magazines_analyzer.py`**: Motor principal de análisis para las 19 revistas completas (1842-2024)
- **`spanish_magazines_analyzer.py`**: Procesador especializado para colecciones específicas de revistas
- **`analizador_revistas_musicales.py`**: Analizador general de revistas musicales con extracción de entidades
- **`boletin_musical_analysis.py`**: Análisis específico del Boletín Musical
- **`analisis_revista_espana_completo.py`**: Ejemplo de Análisis completo para una sola pulicación, la Revista España
- **`analizador_revista_espana.py`**: Ejemplo de procesador para una Revista España

### 2️⃣ Análisis de Prensa (5 scripts)

Ejemplos de Scripts para el procesamiento de periódicos y prensa generalista con secciones musicales:

- **`analizador_el_sol.py`**: Análisis del diario El Sol (1918-1936)
- **`analizador_el_artista.py`**: Procesamiento de la revista El Artista
- **`analizador_iberia_musical.py`**: Análisis de Iberia Musical
- **`procesador_el_debate.py`**: Procesador del diario El Debate
- **`analisis_avanzado.py`**: Herramientas de análisis avanzado con métricas complejas

**Periodos cubiertos**: Desde el Diario de Madrid (1788-1800) hasta prensa contemporánea (2024).

### 3️⃣ Procesamiento y Extracción (9 scripts)

Herramientas de conversión, extracción OCR y procesamiento de datos:

- **`extractor_datos_completo.py`**: Extractor completo de datos de archivos de texto
- **`extract_transcriptions.py`**: Extracción de transcripciones musicales
- **`extraer_con_ocr.py`**: Procesamiento con OCR de documentos digitalizados
- **`extraer_pdfs.py`**: Extracción de texto desde archivos PDF
- **`reprocesar_pdfs_problematicos.py`**: Reprocesamiento de PDFs con errores de extracción
- **`renombrar_revistas.py`**: Utilidad de renombrado masivo de archivos
- **`convertir_hispanoamericana_simple.py`**: Convertidor para la Revista Musical Hispanoamericana
- **`convertir_con_sistema.py`**: Convertidor sistemático de formatos
- **`test_fitz.py`**: Script de prueba para la biblioteca PyMuPDF/Fitz

### 4️⃣ Generadores Web (2 scripts)

Generadores de interfaces web interactivas para visualización de resultados:

- **`generador_web.py`**: Generador principal de interfaces web con Chart.js
- **`generador_web_revista_espana.py`**: Generador especializado para la Revista España

**Características**: Visualizaciones interactivas, gráficos estadísticos, diseño responsive HTML5/CSS3/JavaScript ES6.

### 5️⃣ Entrenamiento del Modelo LexiMus-NER — Fine-tuning BETO

Sistema completo de reconocimiento de entidades musicales en prensa histórica española, compuesto por dos herramientas complementarias: un extractor basado en gazetteer (sin ML) y un script de entrenamiento mediante fine-tuning de BETO.

---

#### 5a. Extractor basado en gazetteer (sin dependencias ML)

Extractor de personas y agrupaciones musicales basado en un listado curado de 1.035 entidades (compositores, intérpretes, cantantes, agrupaciones). Busca todas las entidades en cualquier corpus de archivos `.txt` usando expresiones regulares.

- **1.035 entidades curadas** a partir del corpus ONDAS (1925–1935) y otras publicaciones
- **Sin dependencias**: solo Python 3.7+ estándar
- **Tres salidas**: listado `.txt`, datos completos `.json` e interfaz web interactiva de revisión `.html`
- **Extensible**: añade nuevas entidades al CSV y el script las detecta automáticamente

→ [**LexiMus NER**](https://github.com/LeximusUSAL/leximus-ner) · [Guía de uso y descarga](https://leximususal.github.io/leximus-ner) disponible en GitHub.

---

#### 5b. Script de entrenamiento — Fine-tuning BETO con spaCy

→ [**`entrenar_leximus_ner_v8.py`**](5_Entrenamiento_NER_LexiMus/entrenar_leximus_ner_v8.py)

Script de fine-tuning del modelo NER especializado en música histórica española. A diferencia del extractor por gazetteer, este modelo **generaliza** a entidades no catalogadas previamente.

**Arquitectura del modelo**:

| Capa | Componente | Estado |
|------|-----------|--------|
| Base | `es_dep_news_trf` (spaCy + BETO) | Congelada |
| Fine-tuning | Transformer BETO + capa NER | Re-entrenada |
| Gazetteer | Entity Ruler con 1.035 entidades | Congelado |

El pipeline completo (parser, POS tagger, morfologizador, lematizador) se congela durante el entrenamiento. Solo se re-entrenan el transformer y la capa NER.

**Etiquetas**:

| Etiqueta | Descripción | Ejemplo |
|----------|-------------|---------|
| `COMPOSITOR` | Compositor de obras musicales | *Manuel de Falla*, *Saco del Valle* |
| `INTERPRETE` | Intérprete instrumental o director | *Ricardo Villa*, *Eugenio Goossens* |
| `CANTANTE` | Cantante (ópera, zarzuela, popular) | *Hipólito Lázaro*, *Pepita Embil* |
| `AGRUPACION` | Conjunto musical con nombre propio | *Orquesta Filarmónica*, *Banda Municipal* |

**Corpus de entrenamiento (v8)**:

| Fuente | Tipo | Docs | Entidades |
|--------|------|------|-----------|
| `train_v7.spacy` | Corpus base acumulado | 2.733 | 8.536 |
| `test_ampliado_positivos.json` | Positivos nuevos validados (H) | 1.056 | 1.056 |
| `test_ampliado_negativos.json` | Hard negatives revisión actual (G) | 144 | 0 |
| `negativos_ciclos_anteriores.json` | Hard negatives ciclos anteriores (G) | 78 | 0 |
| `dev_v6.spacy` | Validación | 394 | 1.003 |
| `test_reannotado.spacy` | Test (evaluación final) | 60 | 139 |

**Pipeline de preparación de datos** (8 pasos):
1. Carga del modelo base v7
2. Carga del corpus existente (`.spacy`)
3. Conversión de nuevos datos JSON → spaCy Docs
4. Fusión de corpus (positivos + hard negatives)
5. Detección y resolución automática de inconsistencias de etiquetas
6. Oversampling de AGRUPACION (×3) por ser clase minoritaria
7. Entrenamiento con early stopping (`patience=12`, hasta 40 épocas)
8. Evaluación final del `model-best` en dev y test

**Hiperparámetros**:

```python
MAX_EPOCHS    = 40
PATIENCE      = 12       # early stopping
DROPOUT       = 0.1
BATCH_SIZE    = 8
LR_MAX        = 5e-5     # learning rate máximo (tras warmup)
LR_MIN        = 5e-6     # learning rate inicial (warmup)
WARMUP_EPOCHS = 3        # épocas de warmup lineal
DECAY_FACTOR  = 0.95     # decay por época tras warmup
OVERSAMPLE_FACTOR = 3    # oversampling AGRUPACION
SEED          = 42
```

**Resultados v7** (referencia para comparar con v8):

| Clase | F1 | Precisión | Recall |
|-------|----|-----------|--------|
| GLOBAL | **0.869** | 0.934 | 0.813 |
| COMPOSITOR | 0.924 | 1.000 | 0.859 |
| INTERPRETE | 0.839 | 0.867 | 0.812 |
| CANTANTE | 0.821 | 0.842 | 0.800 |
| AGRUPACION | 0.741 | 0.909 | 0.625 |

**Dataset publicado**: [https://doi.org/10.5281/zenodo.19429405](https://doi.org/10.5281/zenodo.19429405) — formato CoNLL TSV (IOB2), licencia CC BY 4.0.

**Guía de anotación**: [https://leximususal.github.io/leximus-ner-guia-anotacion/](https://leximususal.github.io/leximus-ner-guia-anotacion/)

**Dependencias**:
```bash
pip install spacy thinc torch
python3 -m spacy download es_dep_news_trf
```

**Uso**:
```bash
# Con archivos en el mismo directorio que el script
python3 entrenar_leximus_ner_v8.py

# Con rutas personalizadas
python3 entrenar_leximus_ner_v8.py \
    --base-dir /ruta/a/datos \
    --neg-dir  /ruta/a/negativos \
    --modelo-base leximus_ner_v7_trf/model-best \
    --output-dir leximus_ner_v8_trf
```

**Estructura de directorios esperada**:
```
base-dir/
├── entrenar_leximus_ner_v8.py
├── entidades_ner_leximus.csv      ← gazetteer
├── train_v7.spacy
├── dev_v6.spacy
├── test_reannotado.spacy
├── leximus_ner_v7_trf/model-best/ ← modelo base
└── leximus_ner_v8_trf/            ← salida (se crea automáticamente)

neg-dir/  (por defecto: base-dir/negativos/)
├── test_ampliado_positivos.json
├── test_ampliado_negativos.json
└── negativos_ciclos_anteriores.json
```

## 🛠️ Tecnologías Utilizadas

- **Python 3**: Lenguaje principal de análisis
- **Procesamiento NLP**: Reconocimiento de entidades basado en patrones (no ML)
- **Análisis estadístico**: Cálculo de frecuencias, distribuciones y métricas
- **Visualización web**: HTML5, CSS3, JavaScript ES6, Chart.js
- **Almacenamiento**: Archivos JSON para resultados de análisis

Los datos estadísticos posteriormente fueron revisados con otras dos herramientas: Voyant Tools y Skecht Engine

### 📦 Librerías y Dependencias Python

**IMPORTANTE**: Este proyecto **NO utiliza ML/NLP avanzado** (como spaCy, NLTK, transformers o modelos de lenguaje). En su lugar, emplea **análisis basado en expresiones regulares y patrones** para extracción de entidades musicales, haciendo el proyecto más ligero, reproducible y transparente académicamente.

#### Librerías Estándar de Python (incluidas por defecto)
- `os` - Operaciones del sistema de archivos y navegación de directorios
- `re` - Expresiones regulares para análisis de texto y extracción de patrones
- `json` - Serialización y deserialización de datos JSON
- `glob` - Búsqueda de archivos mediante patrones de nombres
- `collections` (Counter, defaultdict) - Estructuras de datos para conteos y agrupaciones
- `datetime` - Manejo de fechas y marcas temporales
- `pathlib.Path` - Manipulación de rutas de archivos orientada a objetos
- `unicodedata` - Normalización de caracteres Unicode y diacríticos
- `subprocess` - Ejecución de comandos externos del sistema
- `io.StringIO` - Operaciones de entrada/salida en memoria
- `typing` (List, Dict, Any) - Anotaciones de tipos para código más robusto

#### Librerías Externas (requieren instalación)

**Procesamiento de PDFs**:
- **PyMuPDF (fitz)** - Extracción eficiente de texto desde archivos PDF
- **pdfminer.six** - Análisis detallado de estructura y layout de PDFs
  - `pdfminer.high_level.extract_text` - Extracción de texto de alto nivel
  - `pdfminer.converter.TextConverter` - Conversión de PDF a texto plano
  - `pdfminer.layout.LAParams` - Parámetros de análisis de diseño
  - `pdfminer.pdfinterp` (PDFResourceManager, PDFPageInterpreter) - Interpretación de contenido PDF
  - `pdfminer.pdfpage.PDFPage` - Manejo de páginas individuales

**OCR (Reconocimiento Óptico de Caracteres)**:
- **pytesseract** - Interfaz Python para Tesseract OCR Engine
- **pdf2image** - Conversión de páginas PDF a imágenes para procesamiento OCR
- **Pillow (PIL)** - Procesamiento y manipulación de imágenes

#### Instalación de Dependencias

```bash
# Instalar todas las librerías externas necesarias
pip install PyMuPDF pdfminer.six pytesseract pdf2image Pillow

# Para usar Tesseract OCR, también necesitas instalarlo en el sistema:
# macOS:
brew install tesseract tesseract-lang

# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-spa

# Windows:
# Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
```

#### Archivo requirements.txt

```txt
PyMuPDF>=1.23.0
pdfminer.six>=20221105
pytesseract>=0.3.10
pdf2image>=1.16.3
Pillow>=10.0.0
```

## 📊 Principales Hallazgos de Investigación

### Análisis de Género
- **Disparidad extrema**: Ratio de 17.8:1 en tratamientos formales masculinos vs. femeninos
- **Menciones profesionales**: Dominancia masculina de 166.8:1
- **Evidencia de sesgo institucional** en la cultura musical española
- Mejorado en nuestro [**Detector de Género 
  Musical**](https://github.com/LeximusUSAL/detector-genero-musical) 🎵 disponible
  en GitHub.
  
### Vocabulario Musical
- **Géneros**: Ópera, jazz, rock, flamenco, zarzuela (30+ términos)
- **Instrumentos**: Piano, guitarra, violín, saxofón (40+ términos)
- **Términos técnicos**: Armonía, ritmo, melodía, tonalidad (50+ términos)
- **Espacios**: Teatro, conservatorio, casino, ateneo (20+ términos)

## 📈 Datos Procesados en septiembre 2025 (creciendo)

- **25.8 millones de palabras** analizadas
- **3,238 archivos de texto** procesados
- **19 revistas musicales** completas
- **182 años de cobertura** (1842-2024)

## 🚀 Uso de los Scripts

### Requisitos
- Python 3.x
- Dependencias del sistema (sin requirements.txt formal)
- Rutas de datos configuradas en cada script

### Ejecución Básica

```bash
# Análisis completo de las 19 revistas
python3 comprehensive_musical_magazines_analyzer.py

# Análisis de El Sol
python3 analizador_el_sol.py

# Generar interfaz web
python3 generador_web.py
```

### Rutas de Datos

Los scripts esperan encontrar datos en:
```
/Users/maria/Desktop/REVISTAS TXT PARA WEBS ESTADÍSTICAS/
```

**Nota**: Las rutas están hardcoded en los scripts y deben ajustarse según tu entorno.

## 📁 Archivos de Salida

### JSON Generados
- `comprehensive_musical_magazines_analysis.json`: Análisis completo de revistas
- `resultados_revistas_musicales.json`: Datos específicos por revista
- `datos_completos_el_sol.json`: Análisis de El Sol
- `analisis_iberia_musical.json`: Datos de Iberia Musical

### Interfaces Web
- `web_revistas_musicales.html`: Dashboard completo de revistas
- `analisis_musical_el_sol.html`: Interfaz de análisis de El Sol
- `boletin_musical_estadisticas.html`: Análisis del Boletín Musical

## 📖 Metodología

1. **Extracción de texto**: Conversión desde PDFs mediante OCR cuando necesario
2. **Procesamiento NLP**: Reconocimiento de patrones y extracción de entidades musicales
3. **Categorización manual**: Vocabulario y periodos históricos definidos académicamente
4. **Análisis estadístico**: Cálculo de frecuencias, distribuciones temporales y correlaciones
5. **Verificación manual**: Validación de resultados con rigor académico
6. **Visualización**: Generación de interfaces web interactivas

## 🔬 Contexto Académico

Parte del proyecto **"LexiMus: Léxico y ontología de la música en español"** (PID2022-139589NB-C33) desarrollado por:

- **Universidad de Salamanca**
- **Instituto Complutense de Ciencias Musicales**
- **Universidad de La Rioja**

## 📄 Licencia y Citación

Financiado por el **Ministerio de Ciencia e Innovación (MICIU/AEI)** y **Fondos FEDER**.

Si utilizas las fuentes de este espacio en tu investigación, por favor cita:

> Prensa musical e Inteligencia Artificial. Proyecto LexiMus: Léxico y ontología de la música en español (PID2022-139589NB-C33), Universidad de Salamanca. Disponible en: https://LeximusUSAL.github.io/inicio

**© 2025 Universidad de Salamanca**

**Proyecto LexiMus | EQUIPO Universidad de Salamanca**

---

## 📧 Contacto

Para más información sobre el proyecto LexiMus, visita: https://LeximusUSAL.github.io/inicio
