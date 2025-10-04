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

## 🛠️ Tecnologías Utilizadas

- **Python 3**: Lenguaje principal de análisis
- **Procesamiento NLP**: Reconocimiento de entidades basado en patrones (no ML)
- **Análisis estadístico**: Cálculo de frecuencias, distribuciones y métricas
- **Visualización web**: HTML5, CSS3, JavaScript ES6, Chart.js
- **Almacenamiento**: Archivos JSON para resultados de análisis

Los datos estadísticos posteriormente fueron revisados con otras dos herramientas: Voyant Tools y Skecht Engine

## 📊 Principales Hallazgos de Investigación

### Análisis de Género
- **Disparidad extrema**: Ratio de 17.8:1 en tratamientos formales masculinos vs. femeninos
- **Menciones profesionales**: Dominancia masculina de 166.8:1
- **Evidencia de sesgo institucional** en la cultura musical española

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
