#!/usr/bin/env python3
"""
Analizador de Revistas Musicales - Bilbao e Hispanoamericana
Análisis de contenido musical de revistas especializadas (1909-1917)
"""

import json
import re
import os
from collections import defaultdict, Counter
from pathlib import Path

class AnalizadorRevistasMusicales:
    def __init__(self):
        self.bilbao_dir = "/Users/maria/Desktop/REVISTAS TXT PARA WEBS ESTADÍSTICAS/TXT - Revista Musical de Bilbao"
        self.hispano_dir = "/Users/maria/Desktop/REVISTAS TXT PARA WEBS ESTADÍSTICAS/TXT - Revista Musical Hispanoamericana"
        
        # Patrones para análisis
        self.patrones_compositores = [
            r'\b(Bach|Beethoven|Mozart|Chopin|Wagner|Schubert|Brahms|Liszt|Schumann|Haydn)\b',
            r'\b(Falla|Albéniz|Granados|Turina|Bretón|Chapí|Barbieri|Arrieta|Pedrell)\b',
            r'\b(Debussy|Ravel|Franck|Saint-Saëns|Massenet|Berlioz|Gounod|Bizet)\b',
            r'\b(Verdi|Puccini|Rossini|Donizetti|Bellini|Mascagni|Leoncavallo)\b',
            r'\b(Tchaikovsky|Rimsky|Korsakov|Mussorgsky|Borodin|Rachmaninoff)\b'
        ]
        
        self.patrones_interpretes = [
            r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\s+(?:cantó|interpretó|ejecutó|tocó)\b',
            r'\b(?:la|el)\s+(?:soprano|tenor|barítono|bajo|pianista|violinista)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\b',
            r'\b(?:señora|señorita|maestro)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\b'
        ]
        
        self.patrones_generos = [
            r'\b(ópera|zarzuela|opereta|comedia|drama)\s+musical\b',
            r'\b(concierto|recital|sinfonía|cuarteto|quinteto|trío)\b',
            r'\b(vals|mazurca|polca|tango|serenata|nocturno|preludio)\b',
            r'\b(fuga|sonata|rondó|tema|variaciones|fantasía|rapsodia)\b'
        ]
        
        self.patrones_instrumentos = [
            r'\b(piano|violín|viola|violonchelo|contrabajo|arpa|flauta|oboe|clarinete|fagot)\b',
            r'\b(trompeta|trompa|trombón|tuba|percusión|timbal|órgano|armonio)\b',
            r'\b(guitarra|bandurria|mandolina|canto|voz|coro|orquesta|banda)\b'
        ]
        
        self.patrones_genero = {
            'masculino': [
                r'\b(?:el|don|señor|maestro|profesor)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\b',
                r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s+(?:compositor|director|pianista|violinista|tenor|barítono|bajo)\b'
            ],
            'femenino': [
                r'\b(?:la|doña|señora|señorita|maestra|profesora)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\b',
                r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s+(?:soprano|mezzosoprano|contralto|pianista|violinista|cantante)\b'
            ]
        }
        
        self.patrones_lugares = [
            r'\b(Madrid|Barcelona|Bilbao|Sevilla|Valencia|Granada|Cádiz|Málaga)\b',
            r'\b(París|Londres|Berlín|Viena|Roma|Milán|Nueva\s+York|Buenos\s+Aires)\b',
            r'\b(?:Teatro|Sala|Conservatorio|Sociedad)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+)\b'
        ]

    def extraer_año_archivo(self, nombre_archivo):
        """Extrae el año del nombre del archivo"""
        match = re.search(r'(\d{4})', nombre_archivo)
        return int(match.group(1)) if match else None

    def procesar_archivo(self, archivo_path):
        """Procesa un archivo individual y extrae información"""
        try:
            with open(archivo_path, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
        except Exception as e:
            print(f"Error leyendo {archivo_path}: {e}")
            return {}
        
        nombre_archivo = os.path.basename(archivo_path)
        año = self.extraer_año_archivo(nombre_archivo)
        
        resultado = {
            'archivo': {
                'nombre': nombre_archivo,
                'ruta': str(archivo_path),
                'año': año
            },
            'compositores': [],
            'interpretes': [],
            'generos': [],
            'instrumentos': [],
            'genero_personas': {'masculino': [], 'femenino': []},
            'lugares': [],
            'estadisticas': {
                'palabras_total': len(contenido.split()),
                'caracteres': len(contenido)
            }
        }
        
        # Extraer compositores
        for patron in self.patrones_compositores:
            matches = re.finditer(patron, contenido, re.IGNORECASE)
            for match in matches:
                compositor = match.group(1).title()
                contexto = contenido[max(0, match.start()-50):match.end()+50]
                resultado['compositores'].append({
                    'nombre': compositor,
                    'contexto': contexto.strip()
                })
        
        # Extraer intérpretes
        for patron in self.patrones_interpretes:
            matches = re.finditer(patron, contenido, re.IGNORECASE)
            for match in matches:
                interprete = match.group(1).title()
                contexto = contenido[max(0, match.start()-50):match.end()+50]
                resultado['interpretes'].append({
                    'nombre': interprete,
                    'contexto': contexto.strip()
                })
        
        # Extraer géneros musicales
        for patron in self.patrones_generos:
            matches = re.finditer(patron, contenido, re.IGNORECASE)
            for match in matches:
                genero = match.group(0).lower()
                resultado['generos'].append(genero)
        
        # Extraer instrumentos
        for patron in self.patrones_instrumentos:
            matches = re.finditer(patron, contenido, re.IGNORECASE)
            for match in matches:
                instrumento = match.group(0).lower()
                resultado['instrumentos'].append(instrumento)
        
        # Análisis de género
        for genero, patrones in self.patrones_genero.items():
            for patron in patrones:
                matches = re.finditer(patron, contenido, re.IGNORECASE)
                for match in matches:
                    persona = match.group(1).title()
                    contexto = contenido[max(0, match.start()-30):match.end()+30]
                    resultado['genero_personas'][genero].append({
                        'nombre': persona,
                        'contexto': contexto.strip()
                    })
        
        # Extraer lugares
        for patron in self.patrones_lugares:
            matches = re.finditer(patron, contenido, re.IGNORECASE)
            for match in matches:
                lugar = match.group(1) if match.lastindex and match.lastindex >= 1 else match.group(0)
                resultado['lugares'].append(lugar.title())
        
        return resultado

    def procesar_directorio(self, directorio, revista_nombre):
        """Procesa todos los archivos de un directorio"""
        print(f"\n🔍 Procesando {revista_nombre}...")
        
        directorio_path = Path(directorio)
        archivos = list(directorio_path.glob("*.txt"))
        
        resultados = []
        for i, archivo in enumerate(archivos, 1):
            print(f"  📄 {i}/{len(archivos)}: {archivo.name}")
            resultado = self.procesar_archivo(archivo)
            if resultado:
                resultados.append(resultado)
        
        print(f"✅ {revista_nombre}: {len(resultados)} archivos procesados")
        return resultados

    def consolidar_datos(self, datos_bilbao, datos_hispano):
        """Consolida y analiza todos los datos"""
        print("\n📊 Consolidando datos...")
        
        # Contadores globales
        compositores_total = defaultdict(list)
        interpretes_total = defaultdict(list)
        generos_counter = Counter()
        instrumentos_counter = Counter()
        personas_genero = {'masculino': defaultdict(list), 'femenino': defaultdict(list)}
        lugares_counter = Counter()
        evolucion_temporal = defaultdict(lambda: defaultdict(int))
        
        # Procesar ambas revistas
        for datos, revista in [(datos_bilbao, 'Bilbao'), (datos_hispano, 'Hispanoamericana')]:
            for archivo_data in datos:
                año = archivo_data['archivo']['año']
                
                # Compositores
                for comp in archivo_data['compositores']:
                    compositores_total[comp['nombre']].append({
                        'revista': revista,
                        'archivo': archivo_data['archivo'],
                        'contexto': comp['contexto']
                    })
                    if año:
                        evolucion_temporal[año]['compositores'] += 1
                
                # Intérpretes
                for interp in archivo_data['interpretes']:
                    interpretes_total[interp['nombre']].append({
                        'revista': revista,
                        'archivo': archivo_data['archivo'],
                        'contexto': interp['contexto']
                    })
                    if año:
                        evolucion_temporal[año]['interpretes'] += 1
                
                # Géneros
                for genero in archivo_data['generos']:
                    generos_counter[genero] += 1
                
                # Instrumentos
                for instrumento in archivo_data['instrumentos']:
                    instrumentos_counter[instrumento] += 1
                
                # Análisis de género
                for genero in ['masculino', 'femenino']:
                    for persona in archivo_data['genero_personas'][genero]:
                        personas_genero[genero][persona['nombre']].append({
                            'revista': revista,
                            'archivo': archivo_data['archivo'],
                            'contexto': persona['contexto']
                        })
                
                # Lugares
                for lugar in archivo_data['lugares']:
                    lugares_counter[lugar] += 1
                
                if año:
                    evolucion_temporal[año]['total'] += 1
        
        # Crear estructura final
        resultado_final = {
            'metadatos': {
                'revistas_analizadas': ['Revista Musical de Bilbao', 'Revista Musical Hispanoamericana'],
                'periodo': '1909-1917',
                'total_archivos': len(datos_bilbao) + len(datos_hispano),
                'archivos_bilbao': len(datos_bilbao),
                'archivos_hispano': len(datos_hispano)
            },
            'compositores': dict(compositores_total),
            'interpretes': dict(interpretes_total),
            'generos_musicales': dict(generos_counter.most_common(20)),
            'instrumentos': dict(instrumentos_counter.most_common(20)),
            'analisis_genero': {
                'hombres': dict(personas_genero['masculino']),
                'mujeres': dict(personas_genero['femenino'])
            },
            'lugares': dict(lugares_counter.most_common(15)),
            'evolucion_temporal': dict(evolucion_temporal),
            'estadisticas_generales': {
                'compositores_unicos': len(compositores_total),
                'interpretes_unicos': len(interpretes_total),
                'generos_diferentes': len(generos_counter),
                'instrumentos_diferentes': len(instrumentos_counter),
                'personas_masculinas': len(personas_genero['masculino']),
                'personas_femeninas': len(personas_genero['femenino']),
                'lugares_mencionados': len(lugares_counter)
            }
        }
        
        return resultado_final

    def generar_estadisticas_resumidas(self, datos):
        """Genera estadísticas resumidas para la web"""
        stats = {
            'compositores_top': [],
            'interpretes_top': [],
            'generos_top': [],
            'instrumentos_top': [],
            'evolucion_anual': [],
            'ratio_genero': {},
            'lugares_principales': []
        }
        
        # Top compositores
        comp_counts = {nombre: len(menciones) for nombre, menciones in datos['compositores'].items()}
        stats['compositores_top'] = sorted(comp_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Top intérpretes
        interp_counts = {nombre: len(menciones) for nombre, menciones in datos['interpretes'].items()}
        stats['interpretes_top'] = sorted(interp_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Top géneros
        stats['generos_top'] = list(datos['generos_musicales'].items())[:10]
        
        # Top instrumentos
        stats['instrumentos_top'] = list(datos['instrumentos'].items())[:10]
        
        # Evolución anual
        for año in sorted(datos['evolucion_temporal'].keys()):
            stats['evolucion_anual'].append({
                'año': año,
                'menciones': datos['evolucion_temporal'][año]['total'],
                'compositores': datos['evolucion_temporal'][año]['compositores'],
                'interpretes': datos['evolucion_temporal'][año]['interpretes']
            })
        
        # Ratio de género
        total_hombres = sum(len(menciones) for menciones in datos['analisis_genero']['hombres'].values())
        total_mujeres = sum(len(menciones) for menciones in datos['analisis_genero']['mujeres'].values())
        
        stats['ratio_genero'] = {
            'hombres': total_hombres,
            'mujeres': total_mujeres,
            'ratio': round(total_hombres / total_mujeres, 2) if total_mujeres > 0 else 0
        }
        
        # Lugares principales
        stats['lugares_principales'] = list(datos['lugares'].items())[:10]
        
        return stats

    def ejecutar_analisis_completo(self):
        """Ejecuta el análisis completo de ambas revistas"""
        print("🎼 INICIANDO ANÁLISIS DE REVISTAS MUSICALES")
        print("=" * 50)
        
        # Procesar Revista Musical de Bilbao
        datos_bilbao = self.procesar_directorio(self.bilbao_dir, "Revista Musical de Bilbao")
        
        # Procesar Revista Musical Hispanoamericana
        datos_hispano = self.procesar_directorio(self.hispano_dir, "Revista Musical Hispanoamericana")
        
        # Consolidar datos
        datos_consolidados = self.consolidar_datos(datos_bilbao, datos_hispano)
        
        # Generar estadísticas resumidas
        estadisticas = self.generar_estadisticas_resumidas(datos_consolidados)
        
        # Guardar resultados
        with open('resultados_revistas_musicales.json', 'w', encoding='utf-8') as f:
            json.dump(datos_consolidados, f, ensure_ascii=False, indent=2)
        
        with open('estadisticas_revistas_musicales.json', 'w', encoding='utf-8') as f:
            json.dump(estadisticas, f, ensure_ascii=False, indent=2)
        
        # Mostrar resumen
        print("\n📈 RESUMEN DEL ANÁLISIS")
        print("=" * 30)
        print(f"📚 Total archivos procesados: {datos_consolidados['metadatos']['total_archivos']}")
        print(f"🎼 Compositores únicos: {datos_consolidados['estadisticas_generales']['compositores_unicos']}")
        print(f"🎭 Intérpretes únicos: {datos_consolidados['estadisticas_generales']['interpretes_unicos']}")
        print(f"🎵 Géneros musicales: {datos_consolidados['estadisticas_generales']['generos_diferentes']}")
        print(f"🎺 Instrumentos: {datos_consolidados['estadisticas_generales']['instrumentos_diferentes']}")
        print(f"👨 Personas masculinas: {datos_consolidados['estadisticas_generales']['personas_masculinas']}")
        print(f"👩 Personas femeninas: {datos_consolidados['estadisticas_generales']['personas_femeninas']}")
        print(f"🌍 Lugares mencionados: {datos_consolidados['estadisticas_generales']['lugares_mencionados']}")
        print(f"⚖️ Ratio de género: {estadisticas['ratio_genero']['ratio']}:1 (H:M)")
        
        print(f"\n✅ Resultados guardados en:")
        print(f"   📄 resultados_revistas_musicales.json")
        print(f"   📊 estadisticas_revistas_musicales.json")
        
        return datos_consolidados, estadisticas

def main():
    analizador = AnalizadorRevistasMusicales()
    datos, stats = analizador.ejecutar_analisis_completo()
    
    print("\n🎯 Top 5 Compositores:")
    for i, (nombre, count) in enumerate(stats['compositores_top'][:5], 1):
        print(f"   {i}. {nombre}: {count} menciones")
    
    print("\n🎭 Top 5 Géneros Musicales:")
    for i, (genero, count) in enumerate(stats['generos_top'][:5], 1):
        print(f"   {i}. {genero}: {count} menciones")

if __name__ == "__main__":
    main()