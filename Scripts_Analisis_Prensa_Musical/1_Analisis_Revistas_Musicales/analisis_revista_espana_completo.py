#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ANÁLISIS EXHAUSTIVO DE LA REVISTA ESPAÑA
Análisis palabra por palabra de 392 archivos TXT para identificar contenido musical

Metodología:
- Clasificación exacta: A) Contenido musical SIGNIFICATIVO, B) Referencias musicales MENORES, C) SIN contenido musical
- Conteo preciso de compositores, géneros, instrumentos, instituciones, intérpretes
- Temas no musicales principales de cada archivo
"""

import os
import re
from pathlib import Path
from collections import defaultdict

class AnalizadorRevistaEspana:
    def __init__(self):
        self.directorio = "/Users/maria/Desktop/Música en la revista ESPAÑA/REVISTA ESPAÑA en TXT/"
        
        # Diccionarios para conteo exacto
        self.compositores = defaultdict(int)
        self.generos_musicales = defaultdict(int)
        self.instrumentos = defaultdict(int)
        self.instituciones_musicales = defaultdict(int)
        self.interpretes = defaultdict(int)
        
        # Contadores por clasificación
        self.categoria_A = []  # Contenido musical SIGNIFICATIVO
        self.categoria_B = []  # Referencias musicales MENORES
        self.categoria_C = []  # SIN contenido musical
        
        # Términos de búsqueda musical (exhaustivos)
        self.compositores_dict = {
            'manuel falla': 'Manuel de Falla',
            'falla': 'Manuel de Falla',
            'j. turina': 'Joaquín Turina',
            'turina': 'Joaquín Turina',
            'rogelio villar': 'Rogelio Villar',
            'amadeo vives': 'Amadeo Vives',
            'vives': 'Amadeo Vives',
            'wagner': 'Richard Wagner',
            'wágner': 'Richard Wagner',
            'beethoven': 'Ludwig van Beethoven',
            'mozart': 'Wolfgang Amadeus Mozart',
            'chopin': 'Frédéric Chopin',
            'bach': 'Johann Sebastian Bach',
            'liszt': 'Franz Liszt',
            'schumann': 'Robert Schumann',
            'brahms': 'Johannes Brahms',
            'verdi': 'Giuseppe Verdi',
            'puccini': 'Giacomo Puccini',
            'ramos carrión': 'Miguel Ramos Carrión',
            'miguel ramos carrión': 'Miguel Ramos Carrión',
            'barbieri': 'Francisco Asenjo Barbieri',
            'chapí': 'Ruperto Chapí',
            'bretón': 'Tomás Bretón',
            'granados': 'Enrique Granados',
            'albéniz': 'Isaac Albéniz',
            'serrano': 'José Serrano',
            'guerrero': 'Jacinto Guerrero',
            'moreno torroba': 'Federico Moreno Torroba',
            'edward elgar': 'Edward Elgar',
            'elgar': 'Edward Elgar'
        }
        
        self.generos_dict = {
            'ópera': 'Ópera',
            'opera': 'Ópera', 
            'zarzuela': 'Zarzuela',
            'opereta': 'Opereta',
            'concierto': 'Concierto',
            'sinfonía': 'Sinfonía',
            'sinfonia': 'Sinfonía',
            'vals': 'Vals',
            'valses': 'Vals',
            'polka': 'Polka',
            'polkas': 'Polka',
            'galop': 'Galop',
            'galops': 'Galop',
            'tango': 'Tango',
            'tangos': 'Tango',
            'flamenco': 'Flamenco',
            'jota': 'Jota',
            'fandango': 'Fandango',
            'bolero': 'Bolero',
            'seguidilla': 'Seguidilla',
            'sardana': 'Sardana',
            'marcha': 'Marcha',
            'marchas': 'Marcha',
            'himno': 'Himno',
            'himnos': 'Himno',
            'cuplé': 'Cuplé',
            'cuplés': 'Cuplé',
            'tonadilla': 'Tonadilla',
            'tonadilleras': 'Tonadilla',
            'género chico': 'Género chico',
            'música de cámara': 'Música de cámara',
            'música sacra': 'Música sacra',
            'música religiosa': 'Música religiosa',
            'varietés': 'Varietés',
            'variedades': 'Varietés',
            'revista musical': 'Revista musical'
        }
        
        self.instrumentos_dict = {
            'piano': 'Piano',
            'guitarra': 'Guitarra',
            'violín': 'Violín',
            'violin': 'Violín',
            'violonchelo': 'Violonchelo',
            'violoncelo': 'Violonchelo',
            'viola': 'Viola',
            'flauta': 'Flauta',
            'oboe': 'Oboe',
            'clarinete': 'Clarinete',
            'fagot': 'Fagot',
            'trompa': 'Trompa',
            'trompeta': 'Trompeta',
            'trombón': 'Trombón',
            'tuba': 'Tuba',
            'saxofón': 'Saxofón',
            'arpa': 'Arpa',
            'órgano': 'Órgano',
            'organo': 'Órgano',
            'armonio': 'Armonio',
            'acordeón': 'Acordeón',
            'bandurria': 'Bandurria',
            'laúd': 'Laúd',
            'tambor': 'Tambor',
            'timbal': 'Timbal',
            'timbales': 'Timbal',
            'castañuelas': 'Castañuelas',
            'pandereta': 'Pandereta',
            'organillo': 'Organillo',
            'organillos': 'Organillo'
        }
        
        self.instituciones_dict = {
            'teatro real': 'Teatro Real',
            'teatro español': 'Teatro Español', 
            'teatro de la zarzuela': 'Teatro de la Zarzuela',
            'teatro apolo': 'Teatro Apolo',
            'teatro eslava': 'Teatro Eslava',
            'teatro novedades': 'Teatro Novedades',
            'teatro lara': 'Teatro Lara',
            'teatro price': 'Teatro de Price',
            'kursaal': 'Kursaal',
            'conservatorio': 'Conservatorio',
            'orquesta sinfónica': 'Orquesta Sinfónica',
            'orquesta sinfonica madrid': 'Orquesta Sinfónica de Madrid',
            'banda de música': 'Banda de música',
            'banda municipal': 'Banda Municipal',
            'sociedad filarmónica': 'Sociedad Filarmónica',
            'ateneo': 'Ateneo',
            'liceo': 'Liceo',
            'casino': 'Casino',
            'círculo de bellas artes': 'Círculo de Bellas Artes',
            'academia de bellas artes': 'Academia de Bellas Artes'
        }
        
        self.interpretes_dict = {
            'pastora imperio': 'Pastora Imperio',
            'rafaelita espejo': 'Rafaelita Espejo',
            'consuelo la fornarina': 'Consuelo la Fornarina',
            'consuelito la fornarina': 'Consuelo la Fornarina',
            'la caramba': 'La Caramba',
            'celinda': 'Celinda',
            'almanzora': 'Almanzora',
            'maría de las nieves': 'María de las Nieves',
            'la perla': 'La Perla',
            'maestro lassalle': 'Maestro Lassalle',
            'maestro tortosa': 'Maestro Tortosa'
        }
        
        # Términos para determinar si es contenido significativo
        self.terminos_significativos = [
            'artículo musical', 'crónica musical', 'crítica musical', 'reseña musical',
            'concierto', 'representación', 'estreno', 'función', 'espectáculo musical',
            'ópera', 'zarzuela', 'opereta', 'recital', 'audición'
        ]
        
        self.resultados_detallados = []
    
    def leer_archivo(self, ruta_archivo):
        """Lee un archivo y devuelve su contenido en minúsculas para análisis"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                return file.read().lower()
        except Exception as e:
            print(f"Error leyendo {ruta_archivo}: {e}")
            return ""
    
    def extraer_numero_archivo(self, nombre_archivo):
        """Extrae el número del archivo del nombre"""
        match = re.search(r'(\d+)', nombre_archivo)
        return int(match.group(1)) if match else 0
    
    def contar_referencias(self, contenido, diccionario):
        """Cuenta las referencias de un diccionario específico en el contenido"""
        conteos = {}
        for termino, nombre_canonical in diccionario.items():
            # Buscar el término como palabra completa
            patron = r'\b' + re.escape(termino) + r'\b'
            coincidencias = len(re.findall(patron, contenido, re.IGNORECASE))
            if coincidencias > 0:
                if nombre_canonical in conteos:
                    conteos[nombre_canonical] += coincidencias
                else:
                    conteos[nombre_canonical] = coincidencias
        return conteos
    
    def clasificar_contenido(self, contenido, referencias_totales):
        """Clasifica el contenido como A, B o C según su contenido musical"""
        # Buscar términos que indiquen contenido musical significativo
        es_significativo = any(termino in contenido for termino in self.terminos_significativos)
        
        # Si tiene más de 5 referencias musicales O contiene términos significativos
        if referencias_totales > 5 or es_significativo:
            return 'A'
        elif referencias_totales > 0:
            return 'B'
        else:
            return 'C'
    
    def extraer_temas_principales(self, contenido):
        """Extrae los temas principales no musicales del contenido"""
        temas = []
        
        # Patrones comunes de temas en la revista España
        patrones_temas = {
            'política': r'(polític[ao]|gobierno|ministro|parlamento|congreso|diputados)',
            'guerra': r'(guerra|bélico|militar|soldado|batalla|conflicto)',
            'literatura': r'(literari[ao]|escritor|novela|poesía|poeta|libro)',
            'educación': r'(educación|enseñanza|escuela|universidad|estudiante)',
            'economía': r'(económic[ao]|comercio|industria|dinero|precio)',
            'sociedad': r'(social|sociedad|costumbres|pueblo|cultura)',
            'arte': r'(arte|pintura|pintor|escultura|artista)',
            'filosofía': r'(filosofía|filosófico|pensamiento|idea)',
            'religión': r'(religioso|iglesia|católico|fe|dios)',
            'internacional': r'(internacional|europa|francia|alemania|extranjero)'
        }
        
        for tema, patron in patrones_temas.items():
            if re.search(patron, contenido, re.IGNORECASE):
                temas.append(tema)
        
        return temas if temas else ['general']
    
    def analizar_archivo(self, ruta_archivo):
        """Analiza un archivo individual y devuelve los resultados"""
        contenido = self.leer_archivo(ruta_archivo)
        nombre_archivo = os.path.basename(ruta_archivo)
        numero_archivo = self.extraer_numero_archivo(nombre_archivo)
        
        # Contear todas las referencias musicales
        compositores_encontrados = self.contar_referencias(contenido, self.compositores_dict)
        generos_encontrados = self.contar_referencias(contenido, self.generos_dict)
        instrumentos_encontrados = self.contar_referencias(contenido, self.instrumentos_dict)
        instituciones_encontradas = self.contar_referencias(contenido, self.instituciones_dict)
        interpretes_encontrados = self.contar_referencias(contenido, self.interpretes_dict)
        
        # Calcular total de referencias
        total_referencias = (
            sum(compositores_encontrados.values()) +
            sum(generos_encontrados.values()) +
            sum(instrumentos_encontrados.values()) +
            sum(instituciones_encontradas.values()) +
            sum(interpretes_encontrados.values())
        )
        
        # Clasificar el contenido
        clasificacion = self.clasificar_contenido(contenido, total_referencias)
        
        # Extraer temas principales
        temas_principales = self.extraer_temas_principales(contenido)
        
        # Actualizar contadores globales
        for comp, count in compositores_encontrados.items():
            self.compositores[comp] += count
        for gen, count in generos_encontrados.items():
            self.generos_musicales[gen] += count
        for inst, count in instrumentos_encontrados.items():
            self.instrumentos[inst] += count
        for instit, count in instituciones_encontradas.items():
            self.instituciones_musicales[instit] += count
        for interp, count in interpretes_encontrados.items():
            self.interpretes[interp] += count
        
        resultado = {
            'numero': numero_archivo,
            'archivo': nombre_archivo,
            'clasificacion': clasificacion,
            'total_referencias': total_referencias,
            'compositores': compositores_encontrados,
            'generos': generos_encontrados,
            'instrumentos': instrumentos_encontrados,
            'instituciones': instituciones_encontradas,
            'interpretes': interpretes_encontrados,
            'temas_principales': temas_principales
        }
        
        # Clasificar en categorías
        if clasificacion == 'A':
            self.categoria_A.append(resultado)
        elif clasificacion == 'B':
            self.categoria_B.append(resultado)
        else:
            self.categoria_C.append(resultado)
        
        return resultado
    
    def procesar_todos_los_archivos(self):
        """Procesa todos los archivos del directorio"""
        print("🎵 INICIANDO ANÁLISIS EXHAUSTIVO DE LA REVISTA ESPAÑA")
        print("=" * 60)
        
        archivos = [f for f in os.listdir(self.directorio) if f.endswith('.txt')]
        archivos.sort(key=self.extraer_numero_archivo)
        
        print(f"📁 Total de archivos encontrados: {len(archivos)}")
        print()
        
        for i, archivo in enumerate(archivos, 1):
            ruta_completa = os.path.join(self.directorio, archivo)
            resultado = self.analizar_archivo(ruta_completa)
            self.resultados_detallados.append(resultado)
            
            # Mostrar progreso
            if i % 50 == 0:
                print(f"📊 Procesados {i}/{len(archivos)} archivos...")
        
        print(f"✅ Análisis completado: {len(archivos)} archivos procesados")
        print()
    
    def generar_reporte_individual(self):
        """Genera el reporte línea por línea para cada archivo"""
        print("📋 REPORTE INDIVIDUAL POR ARCHIVO")
        print("=" * 80)
        print()
        
        for resultado in sorted(self.resultados_detallados, key=lambda x: x['numero']):
            numero = resultado['numero']
            clasificacion = resultado['clasificacion']
            total = resultado['total_referencias']
            
            # Crear línea de referencias específicas
            referencias = []
            
            if resultado['compositores']:
                for comp, count in resultado['compositores'].items():
                    referencias.append(f"{comp}({count})")
            
            if resultado['generos']:
                for gen, count in resultado['generos'].items():
                    referencias.append(f"{gen}({count})")
            
            if resultado['instrumentos']:
                for inst, count in resultado['instrumentos'].items():
                    referencias.append(f"{inst}({count})")
            
            if resultado['instituciones']:
                for instit, count in resultado['instituciones'].items():
                    referencias.append(f"{instit}({count})")
            
            if resultado['interpretes']:
                for interp, count in resultado['interpretes'].items():
                    referencias.append(f"{interp}({count})")
            
            ref_str = ", ".join(referencias) if referencias else "Sin referencias"
            temas_str = ", ".join(resultado['temas_principales'])
            
            print(f"{numero:03d} | {clasificacion} | {total:2d} refs | {ref_str} | Temas: {temas_str}")
    
    def generar_resumen_estadistico(self):
        """Genera el resumen estadístico final"""
        print("\n" + "=" * 80)
        print("📊 RESUMEN ESTADÍSTICO FINAL")
        print("=" * 80)
        
        total_archivos = len(self.resultados_detallados)
        
        print(f"\n🗂️  CLASIFICACIÓN GENERAL:")
        print(f"   • Categoría A (Contenido musical SIGNIFICATIVO): {len(self.categoria_A)} archivos")
        print(f"   • Categoría B (Referencias musicales MENORES): {len(self.categoria_B)} archivos")
        print(f"   • Categoría C (SIN contenido musical): {len(self.categoria_C)} archivos")
        print(f"   • TOTAL DE ARCHIVOS PROCESADOS: {total_archivos}")
        
        print(f"\n🎼 COMPOSITORES MENCIONADOS ({len(self.compositores)} únicos):")
        for comp, count in sorted(self.compositores.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {comp}: {count} menciones")
        
        print(f"\n🎵 GÉNEROS MUSICALES ({len(self.generos_musicales)} únicos):")
        for gen, count in sorted(self.generos_musicales.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {gen}: {count} menciones")
        
        print(f"\n🎺 INSTRUMENTOS ({len(self.instrumentos)} únicos):")
        for inst, count in sorted(self.instrumentos.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {inst}: {count} menciones")
        
        print(f"\n🏛️  INSTITUCIONES MUSICALES ({len(self.instituciones_musicales)} únicas):")
        for instit, count in sorted(self.instituciones_musicales.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {instit}: {count} menciones")
        
        print(f"\n🎭 INTÉRPRETES/CANTANTES ({len(self.interpretes)} únicos):")
        for interp, count in sorted(self.interpretes.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {interp}: {count} menciones")
        
        # Estadísticas adicionales
        total_referencias = sum(self.compositores.values()) + sum(self.generos_musicales.values()) + sum(self.instrumentos.values()) + sum(self.instituciones_musicales.values()) + sum(self.interpretes.values())
        
        print(f"\n📈 ESTADÍSTICAS GENERALES:")
        print(f"   • Total de referencias musicales encontradas: {total_referencias}")
        print(f"   • Promedio de referencias por archivo: {total_referencias/total_archivos:.2f}")
        print(f"   • Archivos con contenido musical (A+B): {len(self.categoria_A) + len(self.categoria_B)} ({((len(self.categoria_A) + len(self.categoria_B))/total_archivos*100):.1f}%)")
        print(f"   • Archivos sin contenido musical (C): {len(self.categoria_C)} ({(len(self.categoria_C)/total_archivos*100):.1f}%)")

# Ejecutar el análisis
if __name__ == "__main__":
    analizador = AnalizadorRevistaEspana()
    analizador.procesar_todos_los_archivos()
    analizador.generar_reporte_individual()
    analizador.generar_resumen_estadistico()