#!/usr/bin/env python3
"""
Extractor de datos completo para la web mejorada
"""

import json
import re
from collections import defaultdict, Counter
from pathlib import Path

class ExtractorDatosCompleto:
    def __init__(self, directorio_textos):
        self.directorio = Path(directorio_textos)
        self.datos_base = self.cargar_datos_base()
        
    def cargar_datos_base(self):
        """Carga los datos del análisis base"""
        try:
            with open('resultados_el_sol.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def extraer_mujeres_top(self):
        """Extrae top 10 de mujeres mencionadas"""
        mujeres_data = self.datos_base.get('analisis_genero', {}).get('mujeres', {})
        
        # Contar menciones por mujer
        mujeres_contador = {}
        for nombre, menciones in mujeres_data.items():
            mujeres_contador[nombre] = len(menciones)
        
        # Top 10
        top_mujeres = sorted(mujeres_contador.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Agregar contexto para cada mujer
        mujeres_completo = []
        for nombre, count in top_mujeres:
            contextos = mujeres_data.get(nombre, [])
            primer_contexto = contextos[0].get('contexto', '') if contextos else ''
            
            mujeres_completo.append({
                'nombre': nombre,
                'menciones': count,
                'contexto': primer_contexto[:150] + '...' if len(primer_contexto) > 150 else primer_contexto
            })
        
        return mujeres_completo
    
    def extraer_evolucion_temporal(self):
        """Extrae evolución temporal año por año"""
        evolucion = defaultdict(lambda: defaultdict(int))
        
        # Procesar compositores por año
        compositores = self.datos_base.get('compositores', {})
        for compositor, menciones in compositores.items():
            for mencion in menciones:
                archivo = mencion.get('archivo', {})
                año = archivo.get('año') if isinstance(archivo, dict) else self.extraer_año_archivo(str(archivo))
                if año and 1918 <= año <= 1935:
                    evolucion[año]['compositores'] += 1
        
        # Procesar intérpretes por año
        interpretes = self.datos_base.get('interpretes', {})
        for interprete, menciones in interpretes.items():
            for mencion in menciones:
                archivo = mencion.get('archivo', {})
                año = archivo.get('año') if isinstance(archivo, dict) else self.extraer_año_archivo(str(archivo))
                if año and 1918 <= año <= 1935:
                    evolucion[año]['interpretes'] += 1
        
        # Convertir a lista ordenada
        años_ordenados = []
        for año in range(1918, 1936):
            años_ordenados.append({
                'año': año,
                'compositores': evolucion[año]['compositores'],
                'interpretes': evolucion[año]['interpretes'],
                'total': evolucion[año]['compositores'] + evolucion[año]['interpretes']
            })
        
        return años_ordenados
    
    def extraer_teatros_salas(self):
        """Extrae teatros y salas mencionados"""
        teatros = defaultdict(int)
        
        # Patrones para detectar teatros y salas
        patrones_teatros = [
            r'\b(?:teatro|sala)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+)',
            r'\b(Real|Español|Comedia|Zarzuela|Eslava|Principal|Recoletos)\b',
            r'\b(?:en\s+el\s+)([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+)(?:\s+se\s+celebr)',
        ]
        
        archivos_txt = list(self.directorio.rglob("*.txt"))
        
        for archivo in archivos_txt[:100]:  # Muestra para optimizar
            try:
                with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                    texto = f.read()
                
                for patron in patrones_teatros:
                    matches = re.finditer(patron, texto, re.IGNORECASE)
                    for match in matches:
                        teatro = match.group(1).strip() if match.lastindex >= 1 else match.group(0)
                        if len(teatro) > 3 and len(teatro) < 30:
                            teatros[teatro.title()] += 1
                            
            except Exception:
                continue
        
        # Top 15 teatros
        top_teatros = sorted(teatros.items(), key=lambda x: x[1], reverse=True)[:15]
        return [{'nombre': nombre, 'menciones': count} for nombre, count in top_teatros]
    
    def extraer_criticos_autores(self):
        """Extrae críticos y autores de artículos"""
        criticos = defaultdict(int)
        
        # Patrones para detectar firmas y autores
        patrones_criticos = [
            r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s*\.',
            r'Por\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'Firma:\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
        ]
        
        archivos_txt = list(self.directorio.rglob("*.txt"))
        
        for archivo in archivos_txt[:200]:  # Muestra optimizada
            try:
                with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                    texto = f.read()
                
                # Buscar en las últimas líneas donde suelen ir las firmas
                lineas = texto.split('\n')[-5:]
                texto_firmas = '\n'.join(lineas)
                
                for patron in patrones_criticos:
                    matches = re.finditer(patron, texto_firmas)
                    for match in matches:
                        critico = match.group(1).strip()
                        if len(critico.split()) <= 3 and len(critico) > 5:
                            criticos[critico] += 1
                            
            except Exception:
                continue
        
        # Top 10 críticos
        top_criticos = sorted(criticos.items(), key=lambda x: x[1], reverse=True)[:10]
        return [{'nombre': nombre, 'articulos': count} for nombre, count in top_criticos]
    
    def extraer_obras_musicales(self):
        """Extrae obras musicales específicas mencionadas"""
        obras = defaultdict(int)
        
        # Patrones para detectar títulos de obras
        patrones_obras = [
            r'\"([^\"]+)\"',  # Entre comillas
            r'_([^_]+)_',     # Entre guiones bajos (cursiva)
            r'\b(Sinfonía\s+\w+)',
            r'\b(Concierto\s+\w+)',
            r'\b(Sonata\s+\w+)',
        ]
        
        archivos_txt = list(self.directorio.rglob("*.txt"))
        
        for archivo in archivos_txt[:150]:  # Muestra optimizada
            try:
                with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                    texto = f.read()
                
                for patron in patrones_obras:
                    matches = re.finditer(patron, texto)
                    for match in matches:
                        obra = match.group(1).strip()
                        if len(obra) > 5 and len(obra) < 50:
                            # Filtrar obras que parecen reales
                            if any(word in obra.lower() for word in ['sinfonía', 'concierto', 'sonata', 'ópera', 'música']):
                                obras[obra.title()] += 1
                            elif '"' in match.group(0) and len(obra.split()) >= 2:
                                obras[obra.title()] += 1
                                
            except Exception:
                continue
        
        # Top 15 obras
        top_obras = sorted(obras.items(), key=lambda x: x[1], reverse=True)[:15]
        return [{'titulo': titulo, 'menciones': count} for titulo, count in top_obras]
    
    def extraer_año_archivo(self, nombre_archivo):
        """Extrae año del nombre de archivo"""
        match = re.search(r'(\d{4})', str(nombre_archivo))
        return int(match.group(1)) if match else None
    
    def generar_datos_completos(self):
        """Genera todos los datos adicionales"""
        print("Extrayendo datos completos...")
        
        datos_adicionales = {
            'mujeres_top': self.extraer_mujeres_top(),
            'evolucion_temporal': self.extraer_evolucion_temporal(),
            'teatros_salas': self.extraer_teatros_salas(),
            'criticos_autores': self.extraer_criticos_autores(),
            'obras_musicales': self.extraer_obras_musicales()
        }
        
        # Combinar con datos base
        datos_completos = {**self.datos_base, **datos_adicionales}
        
        # Guardar datos completos
        with open('datos_completos_el_sol.json', 'w', encoding='utf-8') as f:
            json.dump(datos_completos, f, ensure_ascii=False, indent=2)
        
        print("✅ Datos completos generados en: datos_completos_el_sol.json")
        return datos_completos

def main():
    directorio_textos = "/Users/maria/Desktop/txt- el sol (con vertex)"
    
    extractor = ExtractorDatosCompleto(directorio_textos)
    datos = extractor.generar_datos_completos()
    
    print(f"\n📊 Datos extraídos:")
    print(f"• Top mujeres: {len(datos['mujeres_top'])}")
    print(f"• Evolución temporal: {len(datos['evolucion_temporal'])} años")
    print(f"• Teatros/salas: {len(datos['teatros_salas'])}")
    print(f"• Críticos: {len(datos['criticos_autores'])}")
    print(f"• Obras musicales: {len(datos['obras_musicales'])}")

if __name__ == "__main__":
    main()