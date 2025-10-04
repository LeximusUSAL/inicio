#!/usr/bin/env python3
"""
Analizador Musical del Periódico "El Sol" (1918-1935)
Extrae información sobre compositores, intérpretes, géneros y análisis de género
"""

import os
import re
import json
import glob
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import unicodedata

class AnalizadorElSol:
    def __init__(self, directorio_textos):
        self.directorio = Path(directorio_textos)
        self.resultados = {
            'compositores': defaultdict(list),
            'interpretes': defaultdict(list),
            'obras': defaultdict(list),
            'generos_musicales': defaultdict(int),
            'analisis_genero': {
                'hombres': defaultdict(list),
                'mujeres': defaultdict(list),
                'terminos_masculinos': defaultdict(int),
                'terminos_femeninos': defaultdict(int)
            },
            'diversidad_racial': defaultdict(list),
            'teatros_salas': defaultdict(list),
            'fechas_eventos': defaultdict(list),
            'criticos_autores': defaultdict(list),
            'estadisticas': {}
        }
        
        # Listas de compositores conocidos (expandible)
        self.compositores_conocidos = {
            'beethoven', 'mozart', 'bach', 'chopin', 'liszt', 'wagner', 'verdi',
            'puccini', 'bizet', 'debussy', 'ravel', 'stravinsky', 'strawinsky', 
            'falla', 'albéniz', 'granados', 'turina', 'rodrigo', 'bretón',
            'chapí', 'vives', 'serrano', 'luna', 'guerrero', 'alonso',
            'tchaikovsky', 'brahms', 'schumann', 'schubert', 'mendelssohn',
            'rossini', 'donizetti', 'bellini', 'massenet', 'gounod',
            'saint-saëns', 'franck', 'fauré', 'satie', 'milhaud'
        }
        
        # Instrumentos y géneros musicales
        self.instrumentos = {
            'piano', 'violín', 'viola', 'violoncello', 'contrabajo', 'flauta',
            'oboe', 'clarinete', 'fagot', 'trompa', 'trompeta', 'trombón',
            'tuba', 'arpa', 'guitarra', 'órgano', 'clave'
        }
        
        self.generos = {
            'ópera', 'zarzuela', 'opereta', 'sinfonía', 'concierto', 'sonata',
            'cuarteto', 'quinteto', 'trío', 'dúo', 'solo', 'recital',
            'oratorio', 'misa', 'réquiem', 'lied', 'canción', 'romanza',
            'vals', 'mazurca', 'polonesa', 'nocturno', 'estudio', 'preludio',
            'fuga', 'toccata', 'fantasía', 'rapsodia', 'serenata', 'divertimento'
        }
        
        # Términos para análisis de género
        self.terminos_masculinos = {
            'maestro', 'profesor', 'director', 'compositor', 'pianista',
            'violinista', 'tenor', 'barítono', 'bajo', 'artista', 'músico',
            'intérprete', 'virtuoso', 'genio', 'talento'
        }
        
        self.terminos_femeninos = {
            'maestra', 'profesora', 'directora', 'compositora', 'pianista',
            'violinista', 'soprano', 'mezzosoprano', 'contralto', 'artista',
            'música', 'intérprete', 'virtuosa', 'talento', 'diva', 'prima donna'
        }
        
        # Términos para detectar diversidad racial/étnica
        self.terminos_diversidad = {
            'negro', 'negra', 'afroamericano', 'africano', 'mulato', 'mulata',
            'gitano', 'gitana', 'flamenco', 'árabe', 'moro', 'judío', 'judía',
            'oriental', 'chino', 'japonés', 'indio', 'americano', 'argentino',
            'cubano', 'brasileño', 'mexicano', 'ruso', 'polaco', 'húngaro'
        }
    
    def limpiar_texto(self, texto):
        """Limpia y normaliza el texto"""
        # Normalizar caracteres unicode
        texto = unicodedata.normalize('NFKD', texto)
        # Convertir a minúsculas para análisis
        return texto.lower()
    
    def extraer_nombres_propios(self, texto):
        """Extrae nombres propios del texto"""
        # Patrón para nombres (mayúscula seguida de minúsculas)
        patron_nombres = r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*\b'
        nombres = re.findall(patron_nombres, texto)
        return [nombre for nombre in nombres if len(nombre.split()) <= 3]
    
    def analizar_compositores(self, texto, archivo):
        """Analiza compositores mencionados"""
        texto_limpio = self.limpiar_texto(texto)
        
        for compositor in self.compositores_conocidos:
            if compositor in texto_limpio:
                # Buscar el contexto original con mayúsculas
                patron = re.compile(rf'\b{re.escape(compositor)}\b', re.IGNORECASE)
                matches = patron.findall(texto)
                for match in matches:
                    self.resultados['compositores'][match.title()].append({
                        'archivo': archivo,
                        'contexto': self.extraer_contexto(texto, match, 100)
                    })
    
    def analizar_interpretes(self, texto, archivo):
        """Analiza intérpretes y músicos mencionados"""
        # Buscar patrones como "el pianista X", "la soprano Y", etc.
        patrones_interpretes = [
            r'(?:el|la)\s+(pianista|violinista|soprano|tenor|barítono|bajo|directora?)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*),\s+(pianista|violinista|soprano|tenor|barítono|bajo)',
            r'(?:Sra?\.|Srta?\.|D\.?|Dña\.?)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)'
        ]
        
        for patron in patrones_interpretes:
            matches = re.finditer(patron, texto)
            for match in matches:
                if len(match.groups()) >= 2:
                    nombre = match.group(2) if patron == patrones_interpretes[0] else match.group(1)
                    tipo = match.group(1) if patron == patrones_interpretes[0] else match.group(2) if len(match.groups()) >= 2 else 'artista'
                else:
                    nombre = match.group(1)
                    tipo = 'artista'
                
                self.resultados['interpretes'][nombre].append({
                    'tipo': tipo,
                    'archivo': archivo,
                    'contexto': self.extraer_contexto(texto, match.group(0), 150)
                })
    
    def analizar_generos_musicales(self, texto, archivo):
        """Analiza géneros musicales mencionados"""
        texto_limpio = self.limpiar_texto(texto)
        
        for genero in self.generos:
            if genero in texto_limpio:
                self.resultados['generos_musicales'][genero] += texto_limpio.count(genero)
    
    def analizar_genero_social(self, texto, archivo):
        """Analiza representación de género en el texto"""
        texto_limpio = self.limpiar_texto(texto)
        
        # Contar términos masculinos y femeninos
        for termino in self.terminos_masculinos:
            count = texto_limpio.count(termino)
            if count > 0:
                self.resultados['analisis_genero']['terminos_masculinos'][termino] += count
        
        for termino in self.terminos_femeninos:
            count = texto_limpio.count(termino)
            if count > 0:
                self.resultados['analisis_genero']['terminos_femeninos'][termino] += count
        
        # Detectar nombres con títulos de género
        patrones_hombres = [
            r'\b(?:Sr\.|Don|D\.)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'\b(maestro|profesor|director)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
            r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+),\s+(?:tenor|barítono|bajo)'
        ]
        
        patrones_mujeres = [
            r'\b(?:Sra?\.|Srta?\.|Dña?\.|Doña)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'\b(maestra|profesora|directora)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
            r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+),\s+(?:soprano|mezzosoprano|contralto)'
        ]
        
        for patron in patrones_hombres:
            matches = re.finditer(patron, texto)
            for match in matches:
                nombre = match.group(1) if match.lastindex == 1 else match.group(2)
                self.resultados['analisis_genero']['hombres'][nombre].append({
                    'archivo': archivo,
                    'contexto': self.extraer_contexto(texto, match.group(0), 100)
                })
        
        for patron in patrones_mujeres:
            matches = re.finditer(patron, texto)
            for match in matches:
                nombre = match.group(1) if match.lastindex == 1 else match.group(2)
                self.resultados['analisis_genero']['mujeres'][nombre].append({
                    'archivo': archivo,
                    'contexto': self.extraer_contexto(texto, match.group(0), 100)
                })
    
    def analizar_diversidad_racial(self, texto, archivo):
        """Analiza menciones de diversidad racial/étnica"""
        texto_limpio = self.limpiar_texto(texto)
        
        for termino in self.terminos_diversidad:
            if termino in texto_limpio:
                matches = re.finditer(rf'\b{re.escape(termino)}\b', texto, re.IGNORECASE)
                for match in matches:
                    self.resultados['diversidad_racial'][termino].append({
                        'archivo': archivo,
                        'contexto': self.extraer_contexto(texto, match.group(0), 200)
                    })
    
    def extraer_contexto(self, texto, termino, longitud=100):
        """Extrae contexto alrededor de un término"""
        pos = texto.lower().find(termino.lower())
        if pos == -1:
            return ""
        
        inicio = max(0, pos - longitud//2)
        fin = min(len(texto), pos + len(termino) + longitud//2)
        
        contexto = texto[inicio:fin]
        if inicio > 0:
            contexto = "..." + contexto
        if fin < len(texto):
            contexto = contexto + "..."
        
        return contexto.strip()
    
    def procesar_archivo(self, ruta_archivo):
        """Procesa un archivo individual"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
            
            archivo_info = {
                'nombre': ruta_archivo.name,
                'ruta': str(ruta_archivo),
                'año': self.extraer_año(ruta_archivo.name)
            }
            
            # Realizar todos los análisis
            self.analizar_compositores(contenido, archivo_info)
            self.analizar_interpretes(contenido, archivo_info)
            self.analizar_generos_musicales(contenido, archivo_info)
            self.analizar_genero_social(contenido, archivo_info)
            self.analizar_diversidad_racial(contenido, archivo_info)
            
            return True
            
        except Exception as e:
            print(f"Error procesando {ruta_archivo}: {e}")
            return False
    
    def extraer_año(self, nombre_archivo):
        """Extrae el año del nombre del archivo"""
        match = re.search(r'(\d{4})', nombre_archivo)
        return int(match.group(1)) if match else None
    
    def procesar_todos_los_archivos(self):
        """Procesa todos los archivos TXT en el directorio"""
        archivos_txt = list(self.directorio.rglob("*.txt"))
        total_archivos = len(archivos_txt)
        procesados = 0
        
        print(f"Procesando {total_archivos} archivos...")
        
        for archivo in archivos_txt:
            if self.procesar_archivo(archivo):
                procesados += 1
            
            if procesados % 50 == 0:
                print(f"Procesados: {procesados}/{total_archivos}")
        
        self.calcular_estadisticas()
        print(f"Procesamiento completado: {procesados}/{total_archivos} archivos")
        
        return procesados
    
    def calcular_estadisticas(self):
        """Calcula estadísticas generales"""
        self.resultados['estadisticas'] = {
            'total_compositores': len(self.resultados['compositores']),
            'total_interpretes': len(self.resultados['interpretes']),
            'total_hombres_identificados': len(self.resultados['analisis_genero']['hombres']),
            'total_mujeres_identificadas': len(self.resultados['analisis_genero']['mujeres']),
            'genero_mas_mencionado': max(self.resultados['generos_musicales'].items(), key=lambda x: x[1])[0] if self.resultados['generos_musicales'] else None,
            'compositor_mas_mencionado': max(self.resultados['compositores'].items(), key=lambda x: len(x[1]))[0] if self.resultados['compositores'] else None,
            'ratio_genero': {
                'hombres': len(self.resultados['analisis_genero']['hombres']),
                'mujeres': len(self.resultados['analisis_genero']['mujeres'])
            },
            'diversidad_detectada': len(self.resultados['diversidad_racial'])
        }
    
    def guardar_resultados(self, archivo_salida="resultados_el_sol.json"):
        """Guarda los resultados en un archivo JSON"""
        # Convertir defaultdict a dict para serialización
        resultados_serializables = {}
        for clave, valor in self.resultados.items():
            if isinstance(valor, defaultdict):
                resultados_serializables[clave] = dict(valor)
            else:
                resultados_serializables[clave] = valor
        
        # Manejar analisis_genero que tiene defaultdicts anidados
        if 'analisis_genero' in resultados_serializables:
            for subclave, subvalor in resultados_serializables['analisis_genero'].items():
                if isinstance(subvalor, defaultdict):
                    resultados_serializables['analisis_genero'][subclave] = dict(subvalor)
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(resultados_serializables, f, ensure_ascii=False, indent=2)
        
        print(f"Resultados guardados en: {archivo_salida}")
    
    def generar_reporte_texto(self):
        """Genera un reporte en texto plano"""
        reporte = []
        reporte.append("="*60)
        reporte.append("ANÁLISIS MUSICAL DEL PERIÓDICO 'EL SOL' (1918-1935)")
        reporte.append("="*60)
        reporte.append("")
        
        # Estadísticas generales
        stats = self.resultados['estadisticas']
        reporte.append("ESTADÍSTICAS GENERALES:")
        reporte.append(f"• Total de compositores identificados: {stats['total_compositores']}")
        reporte.append(f"• Total de intérpretes identificados: {stats['total_interpretes']}")
        reporte.append(f"• Compositor más mencionado: {stats['compositor_mas_mencionado']}")
        reporte.append(f"• Género musical más mencionado: {stats['genero_mas_mencionado']}")
        reporte.append("")
        
        # Análisis de género
        reporte.append("ANÁLISIS DE REPRESENTACIÓN DE GÉNERO:")
        reporte.append(f"• Hombres identificados: {stats['ratio_genero']['hombres']}")
        reporte.append(f"• Mujeres identificadas: {stats['ratio_genero']['mujeres']}")
        
        if stats['ratio_genero']['hombres'] > 0 and stats['ratio_genero']['mujeres'] > 0:
            ratio = stats['ratio_genero']['hombres'] / stats['ratio_genero']['mujeres']
            reporte.append(f"• Ratio hombres/mujeres: {ratio:.2f}:1")
        reporte.append("")
        
        # Diversidad racial/étnica
        reporte.append("DIVERSIDAD RACIAL/ÉTNICA:")
        reporte.append(f"• Términos de diversidad detectados: {stats['diversidad_detectada']}")
        
        if self.resultados['diversidad_racial']:
            reporte.append("• Términos encontrados:")
            for termino, ocurrencias in self.resultados['diversidad_racial'].items():
                reporte.append(f"  - {termino}: {len(ocurrencias)} menciones")
        reporte.append("")
        
        # Top compositores
        reporte.append("TOP 10 COMPOSITORES MÁS MENCIONADOS:")
        compositores_ordenados = sorted(self.resultados['compositores'].items(), 
                                      key=lambda x: len(x[1]), reverse=True)[:10]
        for i, (compositor, menciones) in enumerate(compositores_ordenados, 1):
            reporte.append(f"{i:2d}. {compositor}: {len(menciones)} menciones")
        reporte.append("")
        
        # Top géneros musicales
        reporte.append("TOP 10 GÉNEROS MUSICALES:")
        generos_ordenados = sorted(self.resultados['generos_musicales'].items(), 
                                 key=lambda x: x[1], reverse=True)[:10]
        for i, (genero, count) in enumerate(generos_ordenados, 1):
            reporte.append(f"{i:2d}. {genero}: {count} menciones")
        
        return "\n".join(reporte)

def main():
    """Función principal"""
    directorio_textos = "/Users/maria/Desktop/txt- el sol (con vertex)"
    
    print("Iniciando análisis del periódico 'El Sol'...")
    print(f"Directorio: {directorio_textos}")
    
    analizador = AnalizadorElSol(directorio_textos)
    archivos_procesados = analizador.procesar_todos_los_archivos()
    
    if archivos_procesados > 0:
        # Guardar resultados
        analizador.guardar_resultados("resultados_el_sol.json")
        
        # Generar reporte
        reporte = analizador.generar_reporte_texto()
        with open("reporte_el_sol.txt", "w", encoding="utf-8") as f:
            f.write(reporte)
        
        print("\n" + "="*60)
        print(reporte)
        print("\n" + "="*60)
        print("Archivos generados:")
        print("• resultados_el_sol.json - Datos completos en JSON")
        print("• reporte_el_sol.txt - Reporte en texto")
        print("\nPróximo paso: Crear la página web interactiva")
    else:
        print("No se pudieron procesar archivos. Verifica la ruta del directorio.")

if __name__ == "__main__":
    main()