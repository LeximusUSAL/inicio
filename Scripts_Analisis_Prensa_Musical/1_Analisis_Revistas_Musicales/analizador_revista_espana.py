#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analizador de la Revista ESPAÑA (1915-1924)
Análisis de contenido musical y generación de interfaz web

Proyecto LexiMus: Léxico y ontología de la música en español (PID2022-139589NB-C33)
Universidad de Salamanca
"""

import os
import json
import re
from collections import defaultdict, Counter
from datetime import datetime
import glob


class AnalizadorRevistaEspana:
    def __init__(self, directorio_textos):
        self.directorio_textos = directorio_textos
        self.datos_completos = []
        self.estadisticas = {
            'total_numeros': 310,  # Dato proporcionado por el usuario
            'total_palabras': 132182,  # Dato proporcionado por el usuario
            'palabras_unicas': 19297,  # Dato proporcionado por el usuario
            'numero_articulos': 0,
            'fechas': [],
            'autores': set(),
            'temas_musicales': defaultdict(int),
            'periodos': defaultdict(int)
        }
        
        # Vocabulario musical especializado (adaptado del proyecto LexiMus)
        self.vocabulario_musical = {
            'instrumentos': [
                'guitarra', 'piano', 'violin', 'violonchelo', 'flauta', 'clarinete', 
                'trompeta', 'trombon', 'arpa', 'organo', 'orquesta', 'banda',
                'coro', 'orfeón', 'tambor', 'saxofon', 'oboe', 'fagot', 'tuba',
                'mandolina', 'bandurria', 'castañuelas', 'pandereta'
            ],
            'generos': [
                'opera', 'opereta', 'zarzuela', 'sinfonia', 'concierto', 'sonata',
                'vals', 'mazurka', 'polonesa', 'marcha', 'himno', 'cancion',
                'bolero', 'jota', 'flamenco', 'saeta', 'copla', 'fandango'
            ],
            'elementos_tecnicos': [
                'melodia', 'armonia', 'ritmo', 'compás', 'tonalidad', 'acorde',
                'nota', 'escala', 'tempo', 'allegro', 'andante', 'adagio',
                'fortissimo', 'pianissimo', 'crescendo', 'diminuendo'
            ],
            'espacios': [
                'teatro', 'conservatorio', 'auditorio', 'salon', 'ateneo',
                'casino', 'lyceum', 'coliseo', 'liceo'
            ],
            'personas': [
                'compositor', 'musico', 'pianista', 'violinista', 'cantante',
                'director', 'maestro', 'concertista', 'virtuoso', 'tenor',
                'soprano', 'baritono', 'mezzosoprano', 'bajo'
            ]
        }
        
        # Períodos históricos
        self.periodos = {
            (1915, 1918): "Primera Guerra Mundial",
            (1919, 1923): "Crisis de posguerra", 
            (1924, 1924): "Dictadura de Primo de Rivera"
        }
        
    
    def extraer_numero_archivo(self, archivo):
        """Extrae el número de la revista del nombre del archivo"""
        match = re.search(r'transcripcion_musical_espana_(\d+)', archivo)
        if match:
            return int(match.group(1))
        return 0
    
    def extraer_fecha_contenido(self, contenido):
        """Extrae la fecha del contenido del archivo"""
        # Buscar patrones de fecha en el contenido
        patrones_fecha = [
            r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
            r'(\d{1,2})\s+(\w+)\s+(\d{4})',  # Para formato "8 DICIEMBRE 1923"
            r'(\d{1,2})-(\d{1,2})-(\d{4})',
            r'(\d{4})',  # Solo año
            r'AÑO\s+[IVX]+,?\s*N[UÚ]M?\.\s*(\d+)'
        ]
        
        meses = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
            'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
            'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        
        for patron in patrones_fecha:
            match = re.search(patron, contenido, re.IGNORECASE)
            if match:
                if len(match.groups()) == 3 and match.group(2).lower() in meses:
                    # Formato: día de mes de año O día mes año
                    return f"{match.group(1)} de {match.group(2).lower()} de {match.group(3)}"
                elif len(match.groups()) == 1:
                    return match.group(1)
        
        return "Fecha no disponible"
    
    def crear_titulo_unificado(self, numero, fecha_str):
        """Crea un título unificado en el formato: España, número XXX - Fecha día, mes año"""
        # Extraer y formatear la fecha
        fecha_formateada = "Fecha no disponible"
        
        # Buscar patrón de fecha completa (con "de" o sin "de")
        match_fecha = re.search(r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', fecha_str, re.IGNORECASE)
        if not match_fecha:
            match_fecha = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', fecha_str, re.IGNORECASE)
        
        if match_fecha:
            dia = match_fecha.group(1)
            mes = match_fecha.group(2).lower()
            año = match_fecha.group(3)
            fecha_formateada = f"{dia} {mes} {año}"
        else:
            # Si no hay fecha completa, buscar solo año
            match_año = re.search(r'(\d{4})', fecha_str)
            if match_año:
                fecha_formateada = match_año.group(1)
        
        return f"España, número {numero} - {fecha_formateada}"
    
    def analizar_contenido_musical(self, texto):
        """Analiza el contenido musical del texto"""
        texto_lower = texto.lower()
        menciones_musicales = defaultdict(int)
        
        for categoria, terminos in self.vocabulario_musical.items():
            for termino in terminos:
                # Buscar el término y sus variaciones
                patron = rf'\b{re.escape(termino)}\w*\b'
                matches = re.findall(patron, texto_lower)
                if matches:
                    menciones_musicales[categoria] += len(matches)
                    # Contar cada término específico
                    for match in matches:
                        menciones_musicales[f"{categoria}_{match}"] += 1
        
        return dict(menciones_musicales)
    
    def extraer_autores(self, texto):
        """Extrae posibles autores del texto"""
        autores = set()
        
        # Patrones para detectar autores
        patrones_autor = [
            r'POR\s+([A-ZÁÉÍÓÚ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚ][a-záéíóúñ]+)*)',
            r'([A-ZÁÉÍÓÚ][A-ZÁÉÍÓÚ\s\.]+)$',  # Líneas con nombres en mayúsculas
            r'Firmado[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        ]
        
        for patron in patrones_autor:
            matches = re.findall(patron, texto, re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if len(match.strip()) > 3 and len(match.strip()) < 50:
                    autores.add(match.strip())
        
        return list(autores)
    
    def determinar_periodo(self, fecha_str):
        """Determina el período histórico basado en la fecha"""
        # Extraer año de la fecha
        match = re.search(r'(\d{4})', fecha_str)
        if match:
            año = int(match.group(1))
            for (inicio, fin), periodo in self.periodos.items():
                if inicio <= año <= fin:
                    return periodo
        return "Sin clasificar"
    
    def contar_palabras(self, texto):
        """Cuenta las palabras en el texto"""
        # Eliminar números de línea y caracteres especiales
        texto_limpio = re.sub(r'^\s*\d+→', '', texto, flags=re.MULTILINE)
        palabras = re.findall(r'\b[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]+\b', texto_limpio)
        return len(palabras)
    
    def procesar_archivo(self, ruta_archivo):
        """Procesa un archivo individual"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            if not contenido.strip():
                return None
            
            numero = self.extraer_numero_archivo(os.path.basename(ruta_archivo))
            fecha = self.extraer_fecha_contenido(contenido)
            autores = self.extraer_autores(contenido)
            menciones_musicales = self.analizar_contenido_musical(contenido)
            periodo = self.determinar_periodo(fecha)
            num_palabras = self.contar_palabras(contenido)
            
            # Crear título unificado
            titulo = self.crear_titulo_unificado(numero, fecha)
            
            articulo = {
                'numero': numero,
                'archivo': os.path.basename(ruta_archivo),
                'titulo': titulo,
                'fecha': fecha,
                'autores': autores,
                'periodo': periodo,
                'contenido': contenido,
                'num_palabras': num_palabras,
                'menciones_musicales': menciones_musicales,
                'total_menciones_musicales': sum(menciones_musicales.values())
            }
            
            return articulo
            
        except Exception as e:
            print(f"Error procesando {ruta_archivo}: {str(e)}")
            return None
    
    def analizar_corpus(self):
        """Analiza todo el corpus de textos"""
        print(f"Analizando corpus en: {self.directorio_textos}")
        
        archivos = glob.glob(os.path.join(self.directorio_textos, "*.txt"))
        archivos.sort()
        
        print(f"Encontrados {len(archivos)} archivos")
        
        for ruta_archivo in archivos:
            print(f"Procesando: {os.path.basename(ruta_archivo)}")
            articulo = self.procesar_archivo(ruta_archivo)
            
            if articulo:
                self.datos_completos.append(articulo)
                
                # Actualizar estadísticas
                self.estadisticas['numero_articulos'] += 1
                self.estadisticas['fechas'].append(articulo['fecha'])
                self.estadisticas['autores'].update(articulo['autores'])
                self.estadisticas['periodos'][articulo['periodo']] += 1
                
                # Actualizar temas musicales
                for tema, frecuencia in articulo['menciones_musicales'].items():
                    self.estadisticas['temas_musicales'][tema] += frecuencia
        
        print(f"Análisis completado: {len(self.datos_completos)} artículos procesados")
    
    def generar_estadisticas_resumen(self):
        """Genera estadísticas de resumen"""
        if not self.datos_completos:
            return {}
        
        # Top autores
        contador_autores = Counter()
        for articulo in self.datos_completos:
            for autor in articulo['autores']:
                contador_autores[autor] += 1
        
        # Top temas musicales por categoría
        temas_por_categoria = defaultdict(Counter)
        for tema, freq in self.estadisticas['temas_musicales'].items():
            if '_' in tema:
                categoria, termino = tema.split('_', 1)
                temas_por_categoria[categoria][termino] += freq
        
        # Evolución temporal
        articulos_por_año = defaultdict(int)
        for articulo in self.datos_completos:
            match = re.search(r'(\d{4})', articulo['fecha'])
            if match:
                año = match.group(1)
                articulos_por_año[año] += 1
        
        return {
            'resumen_general': {
                'total_numeros': self.estadisticas['total_numeros'],
                'total_articulos_musicales': len(self.datos_completos),
                'total_palabras': self.estadisticas['total_palabras'],
                'palabras_unicas': self.estadisticas['palabras_unicas'],
                'total_autores': len(self.estadisticas['autores']),
                'periodo_analizado': '1915-1924'
            },
            'autores_principales': dict(contador_autores.most_common(10)),
            'temas_musicales': {k: dict(v.most_common(10)) for k, v in temas_por_categoria.items()},
            'distribucion_temporal': dict(articulos_por_año),
            'periodos_historicos': dict(self.estadisticas['periodos'])
        }
    
    def guardar_datos(self, archivo_salida):
        """Guarda los datos analizados en formato JSON"""
        estadisticas_resumen = self.generar_estadisticas_resumen()
        
        datos_exportar = {
            'metadatos': {
                'proyecto': 'LexiMus: Léxico y ontología de la música en español',
                'codigo_proyecto': 'PID2022-139589NB-C33',
                'institucion': 'Universidad de Salamanca',
                'revista': 'ESPAÑA',
                'periodo': '1915-1924',
                'fecha_analisis': datetime.now().isoformat(),
                'total_archivos_procesados': len(self.datos_completos)
            },
            'estadisticas': estadisticas_resumen,
            'articulos': self.datos_completos
        }
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos_exportar, f, ensure_ascii=False, indent=2)
        
        print(f"Datos guardados en: {archivo_salida}")


def main():
    # Configuración
    directorio_textos = "/Users/maria/Desktop/Música en la revista ESPAÑA/REVISTA ESPAÑA en TXT SOLO MÚSICA"
    archivo_salida = "/Users/maria/datos_revista_espana_musical.json"
    
    # Crear analizador y procesar
    analizador = AnalizadorRevistaEspana(directorio_textos)
    analizador.analizar_corpus()
    analizador.guardar_datos(archivo_salida)
    
    print("\n=== RESUMEN DEL ANÁLISIS ===")
    estadisticas = analizador.generar_estadisticas_resumen()
    
    print(f"Números de revista analizados: {estadisticas['resumen_general']['total_numeros']}")
    print(f"Artículos con contenido musical: {estadisticas['resumen_general']['total_articulos_musicales']}")
    print(f"Total de palabras en corpus: {estadisticas['resumen_general']['total_palabras']:,}")
    print(f"Palabras únicas: {estadisticas['resumen_general']['palabras_unicas']:,}")
    print(f"Autores identificados: {estadisticas['resumen_general']['total_autores']}")
    print(f"Período analizado: {estadisticas['resumen_general']['periodo_analizado']}")


if __name__ == "__main__":
    main()