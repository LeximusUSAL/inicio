#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de "La Iberia Musical" (1842-1855)
Análisis estadístico y lingüístico de 187 archivos de texto
Enfocado en 6 temas musicales específicos
"""

import os
import re
import json
from collections import defaultdict, Counter
from datetime import datetime
import glob

class AnalizadorIberiaMusical:
    def __init__(self, directorio_base):
        self.directorio_base = directorio_base
        self.temas_musicales = {
            'cuarteto': {
                'patrones': [r'\bcuartet[ot]\b', r'\bquartet[ot]\b', r'\bcuartett[ot]\b'],
                'menciones': [],
                'contextos': [],
                'vocabulario_asociado': Counter(),
                'archivos_con_menciones': [],
                'total_menciones': 0
            },
            'musica_camara': {
                'patrones': [r'\bmúsica\s+de\s+cámara\b', r'\bmusica\s+de\s+camara\b',
                           r'\bmúsica\s+di\s+camera\b', r'\bmusica\s+di\s+camera\b'],
                'menciones': [],
                'contextos': [],
                'vocabulario_asociado': Counter(),
                'archivos_con_menciones': [],
                'total_menciones': 0
            },
            'musica_instrumental': {
                'patrones': [r'\bmúsica\s+instrumental\b', r'\bmusica\s+instrumental\b',
                           r'\binstrumental\b'],
                'menciones': [],
                'contextos': [],
                'vocabulario_asociado': Counter(),
                'archivos_con_menciones': [],
                'total_menciones': 0
            },
            'sonata': {
                'patrones': [r'\bsonata\b', r'\bsonatas\b'],
                'menciones': [],
                'contextos': [],
                'vocabulario_asociado': Counter(),
                'archivos_con_menciones': [],
                'total_menciones': 0
            },
            'musica_sabia': {
                'patrones': [r'\bmúsica\s+sabia\b', r'\bmusica\s+sabia\b'],
                'menciones': [],
                'contextos': [],
                'vocabulario_asociado': Counter(),
                'archivos_con_menciones': [],
                'total_menciones': 0
            },
            'musica_clasica': {
                'patrones': [r'\bmúsica\s+clásica\b', r'\bmusica\s+clasica\b',
                           r'\bmúsica\s+clásica\b', r'\bmusica\s+clásica\b'],
                'menciones': [],
                'contextos': [],
                'vocabulario_asociado': Counter(),
                'archivos_con_menciones': [],
                'total_menciones': 0
            }
        }

        self.vocabulario_musical_general = [
            'piano', 'violín', 'viola', 'violoncello', 'contrabajo', 'flauta', 'oboe', 'clarinete',
            'fagot', 'trompa', 'trompeta', 'trombón', 'timbales', 'arpa', 'guitarra',
            'orquesta', 'sinfonía', 'concierto', 'cámara', 'solista', 'ensemble',
            'compositor', 'maestro', 'artista', 'músico', 'virtuoso',
            'teatro', 'academia', 'liceo', 'conservatorio', 'salón',
            'opera', 'zarzuela', 'ballet', 'vals', 'minuet', 'polonesa',
            'allegro', 'andante', 'adagio', 'presto', 'moderato',
            'mayor', 'menor', 'bemol', 'sostenido', 'tono', 'tonalidad',
            'melodía', 'armonía', 'ritmo', 'compás', 'movimiento'
        ]

        self.estadisticas_generales = {
            'total_archivos': 0,
            'total_palabras': 0,
            'archivos_procesados': 0,
            'archivos_con_contenido_musical': 0,
            'fechas_cubiertas': [],
            'distribucion_por_año': defaultdict(int)
        }

    def extraer_fecha_archivo(self, nombre_archivo):
        """Extrae la fecha del nombre del archivo"""
        match = re.search(r'(\d{4})_(\d{2})_(\d{2})', nombre_archivo)
        if match:
            año, mes, dia = match.groups()
            return f"{dia}/{mes}/{año}", int(año)
        return None, None

    def extraer_contexto(self, texto, posicion, ventana=150):
        """Extrae contexto alrededor de una mención"""
        inicio = max(0, posicion - ventana)
        fin = min(len(texto), posicion + ventana)
        return texto[inicio:fin].strip()

    def analizar_vocabulario_asociado(self, contexto, tema):
        """Analiza vocabulario musical asociado en el contexto"""
        contexto_lower = contexto.lower()
        for palabra in self.vocabulario_musical_general:
            if palabra.lower() in contexto_lower:
                self.temas_musicales[tema]['vocabulario_asociado'][palabra] += 1

    def procesar_archivo(self, ruta_archivo):
        """Procesa un archivo individual"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()

            nombre_archivo = os.path.basename(ruta_archivo)
            fecha_str, año = self.extraer_fecha_archivo(nombre_archivo)

            if año:
                self.estadisticas_generales['distribucion_por_año'][año] += 1
                if fecha_str:
                    self.estadisticas_generales['fechas_cubiertas'].append(fecha_str)

            # Contar palabras totales
            palabras = len(contenido.split())
            self.estadisticas_generales['total_palabras'] += palabras

            archivo_tiene_menciones = False

            # Buscar cada tema musical
            for tema, datos in self.temas_musicales.items():
                for patron in datos['patrones']:
                    matches = list(re.finditer(patron, contenido, re.IGNORECASE))

                    if matches:
                        archivo_tiene_menciones = True
                        datos['total_menciones'] += len(matches)

                        if nombre_archivo not in datos['archivos_con_menciones']:
                            datos['archivos_con_menciones'].append(nombre_archivo)

                        for match in matches:
                            contexto = self.extraer_contexto(contenido, match.start())
                            datos['contextos'].append({
                                'archivo': nombre_archivo,
                                'fecha': fecha_str or 'Sin fecha',
                                'contexto': contexto,
                                'posicion': match.start()
                            })

                            datos['menciones'].append({
                                'texto': match.group(),
                                'archivo': nombre_archivo,
                                'fecha': fecha_str or 'Sin fecha',
                                'contexto_previo': contenido[max(0, match.start()-50):match.start()],
                                'contexto_posterior': contenido[match.end():match.end()+50]
                            })

                            # Analizar vocabulario asociado
                            self.analizar_vocabulario_asociado(contexto, tema)

            if archivo_tiene_menciones:
                self.estadisticas_generales['archivos_con_contenido_musical'] += 1

            self.estadisticas_generales['archivos_procesados'] += 1

            return True

        except Exception as e:
            print(f"Error procesando {ruta_archivo}: {e}")
            return False

    def calcular_estadisticas(self):
        """Calcula estadísticas finales"""
        for tema, datos in self.temas_musicales.items():
            if self.estadisticas_generales['total_palabras'] > 0:
                datos['porcentaje_menciones'] = (datos['total_menciones'] / self.estadisticas_generales['total_palabras']) * 100
                datos['porcentaje_archivos'] = (len(datos['archivos_con_menciones']) / self.estadisticas_generales['total_archivos']) * 100
            else:
                datos['porcentaje_menciones'] = 0
                datos['porcentaje_archivos'] = 0

            # Top 10 vocabulario asociado
            datos['top_vocabulario_asociado'] = datos['vocabulario_asociado'].most_common(10)

    def procesar_todos_archivos(self):
        """Procesa todos los archivos en el directorio"""
        patron_archivos = os.path.join(self.directorio_base, "*.txt")
        archivos = glob.glob(patron_archivos)

        self.estadisticas_generales['total_archivos'] = len(archivos)

        print(f"Procesando {len(archivos)} archivos de La Iberia Musical...")

        for i, archivo in enumerate(archivos, 1):
            if self.procesar_archivo(archivo):
                if i % 20 == 0:
                    print(f"Procesados {i}/{len(archivos)} archivos...")

        self.calcular_estadisticas()
        print(f"Análisis completado: {self.estadisticas_generales['archivos_procesados']} archivos procesados")

    def generar_informe_json(self):
        """Genera informe completo en formato JSON"""
        informe = {
            'metadatos': {
                'titulo': 'Análisis de La Iberia Musical (1842-1855)',
                'descripcion': 'Análisis estadístico y lingüístico de 6 temas musicales específicos',
                'fecha_analisis': datetime.now().isoformat(),
                'archivos_analizados': self.estadisticas_generales['total_archivos'],
                'total_palabras': self.estadisticas_generales['total_palabras']
            },
            'estadisticas_generales': self.estadisticas_generales,
            'analisis_temas': {}
        }

        # Preparar datos de cada tema para JSON
        for tema, datos in self.temas_musicales.items():
            informe['analisis_temas'][tema] = {
                'nombre_tema': tema.replace('_', ' ').title(),
                'total_menciones': datos['total_menciones'],
                'porcentaje_menciones': round(datos['porcentaje_menciones'], 4),
                'archivos_con_menciones': len(datos['archivos_con_menciones']),
                'porcentaje_archivos': round(datos['porcentaje_archivos'], 2),
                'lista_archivos': datos['archivos_con_menciones'],
                'vocabulario_asociado': dict(datos['top_vocabulario_asociado']),
                'ejemplos_contextos': datos['contextos'][:5]  # Primeros 5 contextos
            }

        return informe

    def guardar_resultados(self, nombre_archivo='analisis_iberia_musical.json'):
        """Guarda los resultados en archivo JSON"""
        informe = self.generar_informe_json()

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(informe, f, ensure_ascii=False, indent=2)

        print(f"Resultados guardados en: {nombre_archivo}")
        return nombre_archivo

def main():
    # Ruta al directorio de archivos
    directorio = "/Users/maria/Desktop/FUENTES PARA CAROLINA/IBERIA/RESULTADOS La Iberia Musical TXT"

    if not os.path.exists(directorio):
        print(f"Error: No se encuentra el directorio {directorio}")
        return

    # Crear analizador y procesar archivos
    analizador = AnalizadorIberiaMusical(directorio)
    analizador.procesar_todos_archivos()

    # Guardar resultados
    archivo_resultados = analizador.guardar_resultados()

    # Mostrar resumen
    print("\n" + "="*60)
    print("RESUMEN DEL ANÁLISIS DE LA IBERIA MUSICAL")
    print("="*60)
    print(f"Total de archivos procesados: {analizador.estadisticas_generales['archivos_procesados']}")
    print(f"Total de palabras analizadas: {analizador.estadisticas_generales['total_palabras']:,}")
    print(f"Archivos con contenido musical: {analizador.estadisticas_generales['archivos_con_contenido_musical']}")

    print("\nMENCIONES POR TEMA:")
    for tema, datos in analizador.temas_musicales.items():
        print(f"- {tema.replace('_', ' ').title()}: {datos['total_menciones']} menciones "
              f"({datos['porcentaje_menciones']:.4f}% del total)")
        print(f"  En {len(datos['archivos_con_menciones'])} archivos ({datos['porcentaje_archivos']:.1f}%)")

    print(f"\nResultados detallados guardados en: {archivo_resultados}")

if __name__ == "__main__":
    main()