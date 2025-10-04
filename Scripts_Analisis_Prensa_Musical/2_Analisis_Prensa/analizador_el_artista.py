#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador de El Artista (1866-1867) - 6 Temas Musicales
Proyecto LexiMus - Universidad de Salamanca
"""

import os
import re
import json
from collections import defaultdict

class AnalizadorElArtista:
    def __init__(self, directorio_base):
        self.directorio_base = directorio_base

        # Definición de los 6 temas musicales con sus términos
        self.temas_musicales = {
            'cuarteto': {
                'terminos': [
                    r'\bcuarteto\b', r'\bcuartetos\b',
                    r'\bquarteto\b', r'\bquartetos\b',
                    r'\bcuartetto\b', r'\bquartett\b'
                ],
                'nombre': 'Cuarteto'
            },
            'musica_camara': {
                'terminos': [
                    r'\bmúsica de cámara\b', r'\bmusica de camara\b',
                    r'\bmúsica de camara\b', r'\bmusica de cámara\b',
                    r'\bcámara\b', r'\bcamara\b',
                    r'\bensemble\b', r'\bensembles\b',
                    r'\btrío\b', r'\btríos\b', r'\btrio\b', r'\btrios\b',
                    r'\bquinteto\b', r'\bquintetos\b',
                    r'\bsexteto\b', r'\bsextetos\b'
                ],
                'nombre': 'Música de Cámara'
            },
            'musica_instrumental': {
                'terminos': [
                    r'\bmúsica instrumental\b', r'\bmusica instrumental\b',
                    r'\binstrumental\b', r'\binstrumentales\b',
                    r'\bconcierto instrumental\b', r'\bconciertos instrumentales\b',
                    r'\bpieza instrumental\b', r'\bpiezas instrumentales\b',
                    r'\bobra instrumental\b', r'\bobras instrumentales\b'
                ],
                'nombre': 'Música Instrumental'
            },
            'sonata': {
                'terminos': [
                    r'\bsonata\b', r'\bsonatas\b',
                    r'\bsonatina\b', r'\bsonatinas\b',
                    r'\bsonaten\b'
                ],
                'nombre': 'Sonata'
            },
            'musica_sabia': {
                'terminos': [
                    r'\bmúsica sabia\b', r'\bmusica sabia\b',
                    r'\bmúsica docta\b', r'\bmusica docta\b',
                    r'\bmúsica culta\b', r'\bmusica culta\b',
                    r'\bmúsica seria\b', r'\bmusica seria\b',
                    r'\bmúsica elevada\b', r'\bmusica elevada\b',
                    r'\bmúsica clásica\b', r'\bmusica clasica\b',
                    r'\balta música\b', r'\balta musica\b'
                ],
                'nombre': 'Música Sabia'
            },
            'musica_clasica': {
                'terminos': [
                    r'\bmúsica clásica\b', r'\bmusica clasica\b',
                    r'\bmúsica clásica\b', r'\bmusica clásica\b',
                    r'\bclásica\b', r'\bclasica\b',
                    r'\bclásico\b', r'\bclasico\b',
                    r'\bclásicos\b', r'\bclasicos\b',
                    r'\bestilo clásico\b', r'\bestilo clasico\b',
                    r'\bcompositor clásico\b', r'\bcompositores clásicos\b'
                ],
                'nombre': 'Música Clásica'
            }
        }

    def analizar_archivo(self, ruta_archivo):
        """Analiza un archivo individual y cuenta menciones de cada tema"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read().lower()

            resultados = {}
            for tema_id, tema_data in self.temas_musicales.items():
                menciones = 0
                vocabulario = []

                for patron in tema_data['terminos']:
                    matches = re.finditer(patron, contenido, re.IGNORECASE)
                    for match in matches:
                        menciones += 1
                        vocabulario.append(match.group())

                if menciones > 0:
                    resultados[tema_id] = {
                        'menciones': menciones,
                        'vocabulario': vocabulario
                    }

            return resultados, contenido

        except Exception as e:
            print(f"Error procesando {ruta_archivo}: {e}")
            return {}, ""

    def analizar_corpus_completo(self):
        """Analiza todos los archivos de El Artista"""
        print("Iniciando análisis de El Artista...")

        # Obtener lista de archivos
        archivos_txt = []
        for archivo in os.listdir(self.directorio_base):
            if archivo.endswith('.txt') and not archivo.startswith('.'):
                archivos_txt.append(os.path.join(self.directorio_base, archivo))

        archivos_txt.sort()
        total_archivos = len(archivos_txt)
        print(f"Total de archivos a procesar: {total_archivos}")

        # Inicializar contadores
        estadisticas_globales = {
            tema_id: {
                'total_menciones': 0,
                'archivos_con_mencion': 0,
                'vocabulario_conjunto': []
            }
            for tema_id in self.temas_musicales.keys()
        }

        archivos_procesados = []
        total_palabras = 0

        # Procesar cada archivo
        for idx, ruta_archivo in enumerate(archivos_txt, 1):
            nombre_archivo = os.path.basename(ruta_archivo)
            print(f"[{idx}/{total_archivos}] Procesando: {nombre_archivo}")

            resultados_archivo, contenido = self.analizar_archivo(ruta_archivo)
            palabras_archivo = len(contenido.split())
            total_palabras += palabras_archivo

            # Actualizar estadísticas globales
            archivo_info = {
                'nombre': nombre_archivo,
                'palabras': palabras_archivo,
                'temas': {}
            }

            for tema_id in self.temas_musicales.keys():
                if tema_id in resultados_archivo:
                    estadisticas_globales[tema_id]['total_menciones'] += resultados_archivo[tema_id]['menciones']
                    estadisticas_globales[tema_id]['archivos_con_mencion'] += 1
                    estadisticas_globales[tema_id]['vocabulario_conjunto'].extend(
                        resultados_archivo[tema_id]['vocabulario']
                    )

                    archivo_info['temas'][tema_id] = {
                        'menciones': resultados_archivo[tema_id]['menciones']
                    }

            if archivo_info['temas']:
                archivos_procesados.append(archivo_info)

        # Calcular porcentajes y estadísticas finales
        resultados_finales = {
            'metadata': {
                'revista': 'El Artista',
                'periodo': '1866-1867',
                'total_archivos': total_archivos,
                'total_palabras': total_palabras,
                'archivos_con_temas_musicales': len(archivos_procesados),
                'porcentaje_archivos_con_temas': round((len(archivos_procesados) / total_archivos) * 100, 2)
            },
            'temas': {},
            'archivos_detallados': archivos_procesados
        }

        total_menciones_todas = sum(
            estadisticas_globales[tema_id]['total_menciones']
            for tema_id in self.temas_musicales.keys()
        )

        for tema_id, tema_data in self.temas_musicales.items():
            menciones = estadisticas_globales[tema_id]['total_menciones']
            archivos_con_tema = estadisticas_globales[tema_id]['archivos_con_mencion']

            resultados_finales['temas'][tema_id] = {
                'nombre': tema_data['nombre'],
                'total_menciones': menciones,
                'porcentaje_menciones': round((menciones / total_menciones_todas * 100) if total_menciones_todas > 0 else 0, 2),
                'archivos_con_mencion': archivos_con_tema,
                'porcentaje_archivos': round((archivos_con_tema / total_archivos) * 100, 2),
                'vocabulario_frecuencias': self._contar_frecuencias(
                    estadisticas_globales[tema_id]['vocabulario_conjunto']
                )
            }

        return resultados_finales

    def _contar_frecuencias(self, lista_palabras):
        """Cuenta frecuencias de términos encontrados"""
        frecuencias = defaultdict(int)
        for palabra in lista_palabras:
            frecuencias[palabra.lower()] += 1
        return dict(sorted(frecuencias.items(), key=lambda x: x[1], reverse=True))

    def guardar_json(self, resultados, ruta_salida):
        """Guarda los resultados en formato JSON"""
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Resultados guardados en: {ruta_salida}")

def main():
    directorio_base = "/Users/maria/Desktop/FUENTES CAROLINA/ARTISTA/El Artista txt resultados"
    archivo_salida = "/Users/maria/el_artista_analisis_temas_musicales.json"

    analizador = AnalizadorElArtista(directorio_base)
    resultados = analizador.analizar_corpus_completo()

    # Mostrar resumen
    print("\n" + "="*60)
    print("RESUMEN DEL ANÁLISIS - EL ARTISTA")
    print("="*60)
    print(f"Total de archivos analizados: {resultados['metadata']['total_archivos']}")
    print(f"Total de palabras: {resultados['metadata']['total_palabras']:,}")
    print(f"Archivos con temas musicales: {resultados['metadata']['archivos_con_temas_musicales']}")
    print(f"Porcentaje archivos con temas: {resultados['metadata']['porcentaje_archivos_con_temas']}%")
    print("\nMenciones por tema:")
    for tema_id, tema_stats in resultados['temas'].items():
        print(f"  - {tema_stats['nombre']}: {tema_stats['total_menciones']} menciones ({tema_stats['porcentaje_menciones']}%)")
        print(f"    Archivos: {tema_stats['archivos_con_mencion']} ({tema_stats['porcentaje_archivos']}%)")

    analizador.guardar_json(resultados, archivo_salida)

if __name__ == "__main__":
    main()
