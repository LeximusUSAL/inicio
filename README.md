# LexiMus USAL - Prensa Musical e Inteligencia Artificial

[![Universidad de Salamanca](https://img.shields.io/badge/Universidad-Salamanca-003D5C?style=flat-square)](https://www.usal.es/)
[![Proyecto LexiMus](https://img.shields.io/badge/Proyecto-LexiMus-008a9b?style=flat-square)](https://leximus.es/)
[![License](https://img.shields.io/badge/License-CC_BY--NC--SA-blue?style=flat-square)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

> **Laboratorio Digital para la Historia Musical Española a través de la Prensa Histórica**

[![Visita la Web](https://img.shields.io/badge/🌐_Visita_la_Web-LeximusUSAL.github.io/inicio-007bff?style=for-the-badge)](https://LeximusUSAL.github.io/inicio)

---

## 📖 Sobre el Proyecto

**LexiMus USAL** aplica **Inteligencia Artificial** al análisis de prensa musical histórica española para recuperar, analizar y visualizar el patrimonio musical documentado en periódicos y revistas desde el siglo XVIII hasta la actualidad.

Este proyecto forma parte de **"LexiMus: Léxico y ontología de la música en español"** (PID2022-139589NB-C33), un proyecto coordinado entre:

- 🎓 **Universidad de Salamanca**
- 🎼 **Instituto Complutense de Ciencias Musicales** (Madrid)
- 📚 **Universidad de La Rioja**

### ¿Qué hace la IA en este proyecto?

La Inteligencia Artificial actúa como un **asistente de investigación incansable** capaz de:

- 📰 Leer y analizar millones de palabras de prensa histórica en horas
- 🎵 Identificar contenido musical: conciertos, críticas, compositores, obras
- 🔍 Reconocer patrones en el lenguaje musical a través del tiempo
- 📊 Extraer datos estadísticos y tendencias del discurso musical español
- 🗂️ Clasificar y estructurar información de textos no estructurados

## 🎯 Objetivos

1. **Recuperar el patrimonio musical español** documentado en la prensa histórica
2. **Analizar la evolución del léxico y discurso musical** español (1788-2024)
3. **Descubrir patrones y tendencias** en la cultura musical histórica
4. **Democratizar el acceso** a fuentes históricas mediante tecnología digital
5. **Proporcionar herramientas de investigación** para musicólogos e historiadores

## 🌐 Contenido de la Web

### 1. Buscador de Noticias Musicales

**Detección Automática de Contenido Musical**

Un repositorio en constante crecimiento con noticias, anuncios y artículos sobre música extraídos automáticamente de periódicos históricos españoles. El contenido es validado por musicólogos especializados en cada época histórica.

#### 📚 Corpus Disponibles

| Publicación | Periodo | Descripción |
|-------------|---------|-------------|
| **Diario de Madrid** | 1788-1823 | Noticias y anuncios de la vida musical madrileña |
| **El Debate** | 1881-1883 | Publicación liberal con contenido musical diverso |
| **España** | Semanario | Revista de la "edad de plata" intelectual española |
| **El Sol** | 1918-1932 | Con críticas musicales de Adolfo Salazar |

#### 🔧 Metodología de Extracción

El proceso utiliza **Claude Code**, una herramienta de IA especializada:

1. **Fuentes originales**: PDFs digitalizados de la Hemeroteca de la Biblioteca Nacional de España (BNE)
2. **Prompts especializados**: Instrucciones adaptadas al estilo de cada publicación histórica
3. **Detección automática**: Identificación de secciones musicales (conciertos, críticas, anuncios)
4. **Transcripción inteligente**: Conservación de fechas, nombres, lugares y contexto

**📂 [Ver Scripts de Análisis →](Scripts_Analisis_Prensa_Musical/)**

Todos los scripts Python utilizados están disponibles públicamente con 23 herramientas organizadas en 4 categorías.

### 2. Análisis Inicial

**Descubrimiento de Patrones en Textos No Estructurados**

Análisis computacionales que revelan tendencias, patrones y evolución del discurso musical español.

#### 🛠️ Herramientas Empleadas

1. **Claude AI**: Análisis cualitativo inicial
   - Temáticas principales (ópera, música religiosa, popular)
   - Compositores y obras más mencionados
   - Evolución del vocabulario musical
   - Tendencias temporales y geográficas

2. **Voyant Tools**: Precisión estadística
   - Frecuencia exacta de términos musicales
   - Visualizaciones (nubes de palabras, gráficos temporales)
   - Análisis de coocurrencias
   - Estadísticas de distribución textual

3. **Sketch Engine**: Análisis lingüístico avanzado
   - Análisis semántico del vocabulario musical
   - Identificación de colocaciones típicas
   - Comparaciones entre períodos históricos
   - Extracción de terminología especializada

#### 📊 Metodología

- ✅ **Enfoque no supervisado**: La IA encuentra patrones sin categorías predefinidas
- ✅ **Validación cruzada**: Resultados contrastados entre herramientas
- ✅ **Validación por expertos**: Revisión musicológica especializada
- ✅ **Contextualización histórica**: Situación en el contexto correspondiente

## 🚀 Estructura del Repositorio

```
inicio/
├── README.md                              # Este archivo
├── intro.html                             # Página principal del proyecto
├── index.html                             # Página de entrada
├── Scripts_Analisis_Prensa_Musical/       # 📂 Scripts Python de análisis
│   ├── 1_Analisis_Revistas_Musicales/     # 6 scripts para revistas
│   ├── 2_Analisis_Prensa/                 # 5 scripts para periódicos
│   ├── 3_Procesamiento_Extraccion/        # 9 scripts de procesamiento
│   ├── 4_Generadores_Web/                 # 2 generadores de interfaces
│   └── README.md                          # Documentación técnica detallada
├── noticiasmusicales/                     # Buscador de noticias
├── principal/                             # Análisis principales
└── [recursos adicionales]
```

## 💡 Resultados y Hallazgos

Este proyecto representa una **nueva forma de investigar en musicología**, donde la IA actúa como una lupa digital que permite:

- 🔍 Ver patrones difíciles de detectar manualmente
- 📈 Descubrir **qué** se escribió sobre música en cada época
- 🎭 Entender **cómo** evolucionó el discurso musical español
- 🎼 Identificar qué obras y compositores dominaron cada período
- 📝 Analizar la transformación del vocabulario musical

### Impacto para la Investigación

Los datos extraídos permiten a los investigadores:

- Interpretar el patrimonio musical con mayor precisión
- Detectar tendencias longitudinales (1788-2024)
- Comparar períodos históricos con datos cuantificables
- Acceder a fuentes previamente inaccesibles por su volumen

## 🔄 Actualizaciones

La web está en **constante actualización**, incorporando:

- ✨ Nuevos corpus de prensa histórica
- 🔧 Refinamiento de análisis existentes
- 📊 Nuevas visualizaciones interactivas
- 🎯 Mejoras en la precisión de extracción

## 🤝 Colaboradores

### Instituciones Participantes

- **Universidad de Salamanca** (Coordinación)
- **Instituto Complutense de Ciencias Musicales** (Madrid)
- **Universidad de La Rioja**

### Equipo

👥 [Ver Equipo Universidad de Salamanca →](https://leximus.es/equipo/#usal)

## 📚 Cómo Citar

Si utilizas las fuentes de este espacio en tu investigación, por favor cita:

> **Prensa musical e Inteligencia Artificial**. Proyecto LexiMus: Léxico y ontología de la música en español (PID2022-139589NB-C33), Universidad de Salamanca. Disponible en: https://LeximusUSAL.github.io/inicio

## 📄 Licencia y Financiación

Financiado por el **Ministerio de Ciencia e Innovación (MICIU/AEI)** y **Fondos FEDER**.

**© 2025 Universidad de Salamanca**

**Proyecto LexiMus | EQUIPO Universidad de Salamanca**

---

## 🔗 Enlaces Útiles

- 🌐 **Web del Proyecto**: https://LeximusUSAL.github.io/inicio
- 📂 **Scripts de Análisis**: [Scripts_Analisis_Prensa_Musical/](Scripts_Analisis_Prensa_Musical/)
- 🎼 **Proyecto LexiMus Nacional**: https://leximus.es/
- 🏛️ **Universidad de Salamanca**: https://www.usal.es/

---

<div align="center">

**Explorando el patrimonio musical español con Inteligencia Artificial**

[![GitHub](https://img.shields.io/badge/GitHub-LeximusUSAL-181717?style=flat-square&logo=github)](https://github.com/LeximusUSAL)
[![Web](https://img.shields.io/badge/Web-inicio-008a9b?style=flat-square&logo=google-chrome&logoColor=white)](https://LeximusUSAL.github.io/inicio)

</div>
