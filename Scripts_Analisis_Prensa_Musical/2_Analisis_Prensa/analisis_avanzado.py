#!/usr/bin/env python3
"""
Análisis avanzado para detectar patrones específicos en El Sol
Enfoque en género, raza y tratamiento diferencial
"""

import json
import re
from collections import defaultdict, Counter
from pathlib import Path

class AnalisisAvanzado:
    def __init__(self, directorio_textos):
        self.directorio = Path(directorio_textos)
        self.datos_base = self.cargar_datos_base()
        
        # Patrones específicos para análisis de género
        self.patrones_tratamiento_masculino = [
            r'\b(?:el\s+(?:gran|ilustre|eminente|destacado|notable|brillante))\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
            r'\b(?:maestro|profesor|director)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
            r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+),?\s+(?:el\s+)?(?:virtuoso|genio|talento)',
            r'\bDon\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)'
        ]
        
        self.patrones_tratamiento_femenino = [
            r'\b(?:la\s+(?:gran|ilustre|eminente|destacada|notable|brillante))\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
            r'\b(?:maestra|profesora|directora)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
            r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+),?\s+(?:la\s+)?(?:virtuosa|diva|prima\s+donna)',
            r'\b(?:Doña|Señora|Señorita)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)'
        ]
        
        # Términos que indican origen racial/étnico
        self.indicadores_raciales = {
            'africanx': ['negro', 'negra', 'africano', 'africana', 'etíope'],
            'gitanx': ['gitano', 'gitana', 'calé', 'flamenco'],
            'judíx': ['judío', 'judía', 'hebreo', 'hebrea'],
            'oriental': ['chino', 'china', 'japonés', 'japonesa', 'oriental'],
            'árabe': ['árabe', 'moro', 'mora', 'musulmán', 'musulmana'],
            'eslavo': ['ruso', 'rusa', 'polaco', 'polaca', 'húngaro', 'húngara'],
            'americano': ['americano', 'americana', 'indio', 'india', 'nativo']
        }
        
        # Palabras que indican calidad/valoración
        self.adjetivos_positivos = [
            'excelente', 'brillante', 'magistral', 'extraordinario', 'soberbio',
            'admirable', 'perfecto', 'sublime', 'genial', 'virtuoso', 'notable',
            'destacado', 'ilustre', 'eminente', 'prestigioso', 'reconocido'
        ]
        
        self.adjetivos_negativos = [
            'mediocre', 'deficiente', 'pobre', 'insuficiente', 'flojo',
            'irregular', 'discutible', 'criticable', 'deplorable'
        ]
    
    def cargar_datos_base(self):
        """Carga los datos del análisis base"""
        try:
            with open('resultados_el_sol.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def analizar_tratamiento_genero(self):
        """Analiza diferencias en el tratamiento por género"""
        resultados = {
            'adjetivos_masculinos': defaultdict(int),
            'adjetivos_femeninos': defaultdict(int),
            'tratamientos_formales': {
                'masculinos': defaultdict(int),
                'femeninos': defaultdict(int)
            },
            'contextos_profesionales': {
                'hombres': [],
                'mujeres': []
            }
        }
        
        archivos_txt = list(self.directorio.rglob("*.txt"))
        
        for archivo in archivos_txt:
            try:
                with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                    texto = f.read()
                
                # Analizar adjetivos asociados con hombres vs mujeres
                self._analizar_adjetivos_genero(texto, resultados, archivo.name)
                
                # Analizar tratamientos formales
                self._analizar_tratamientos_formales(texto, resultados)
                
                # Analizar contextos profesionales
                self._analizar_contextos_profesionales(texto, resultados, archivo.name)
                
            except Exception as e:
                continue
        
        return resultados
    
    def _analizar_adjetivos_genero(self, texto, resultados, archivo):
        """Analiza adjetivos asociados con menciones de género"""
        # Buscar adjetivos cerca de términos masculinos
        patrones_masc = [r'(?:maestro|profesor|director|pianista|violinista|tenor|barítono)\s+(\w+)', 
                        r'(\w+)\s+(?:maestro|profesor|director|pianista|violinista|tenor|barítono)']
        
        for patron in patrones_masc:
            matches = re.finditer(patron, texto.lower())
            for match in matches:
                adj = match.group(1)
                if adj in [a.lower() for a in self.adjetivos_positivos + self.adjetivos_negativos]:
                    resultados['adjetivos_masculinos'][adj] += 1
        
        # Buscar adjetivos cerca de términos femeninos
        patrones_fem = [r'(?:maestra|profesora|directora|pianista|violinista|soprano|mezzosoprano|contralto)\s+(\w+)',
                       r'(\w+)\s+(?:maestra|profesora|directora|pianista|violinista|soprano|mezzosoprano|contralto)']
        
        for patron in patrones_fem:
            matches = re.finditer(patron, texto.lower())
            for match in matches:
                adj = match.group(1)
                if adj in [a.lower() for a in self.adjetivos_positivos + self.adjetivos_negativos]:
                    resultados['adjetivos_femeninos'][adj] += 1
    
    def _analizar_tratamientos_formales(self, texto, resultados):
        """Analiza el uso de tratamientos formales"""
        # Tratamientos masculinos
        tratamientos_masc = ['Don', 'Sr.', 'Señor', 'Maestro', 'Profesor', 'Director']
        for tratamiento in tratamientos_masc:
            count = len(re.findall(rf'\b{tratamiento}\s+[A-ZÁÉÍÓÚÑ]', texto))
            resultados['tratamientos_formales']['masculinos'][tratamiento] += count
        
        # Tratamientos femeninos
        tratamientos_fem = ['Doña', 'Sra.', 'Srta.', 'Señora', 'Señorita', 'Maestra', 'Profesora', 'Directora']
        for tratamiento in tratamientos_fem:
            count = len(re.findall(rf'\b{tratamiento}\s+[A-ZÁÉÍÓÚÑ]', texto))
            resultados['tratamientos_formales']['femeninos'][tratamiento] += count
    
    def _analizar_contextos_profesionales(self, texto, resultados, archivo):
        """Analiza contextos profesionales por género"""
        # Contextos masculinos
        patrones_prof_masc = [
            r'(?:el|un)\s+(?:director|maestro|profesor|compositor)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
            r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+),\s+(?:director|maestro|profesor|compositor)'
        ]
        
        for patron in patrones_prof_masc:
            matches = re.finditer(patron, texto)
            for match in matches:
                contexto = self._extraer_contexto(texto, match.start(), 150)
                resultados['contextos_profesionales']['hombres'].append({
                    'nombre': match.group(1),
                    'contexto': contexto,
                    'archivo': archivo
                })
        
        # Contextos femeninos
        patrones_prof_fem = [
            r'(?:la|una)\s+(?:directora|maestra|profesora|compositora)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)',
            r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+),\s+(?:directora|maestra|profesora|compositora)'
        ]
        
        for patron in patrones_prof_fem:
            matches = re.finditer(patron, texto)
            for match in matches:
                contexto = self._extraer_contexto(texto, match.start(), 150)
                resultados['contextos_profesionales']['mujeres'].append({
                    'nombre': match.group(1),
                    'contexto': contexto,
                    'archivo': archivo
                })
    
    def analizar_diversidad_racial(self):
        """Análisis profundo de diversidad racial"""
        resultados = {
            'por_categoria': defaultdict(list),
            'contextos_valorativos': defaultdict(list),
            'terminos_asociados': defaultdict(Counter),
            'evolucion_temporal': defaultdict(lambda: defaultdict(int))
        }
        
        archivos_txt = list(self.directorio.rglob("*.txt"))
        
        for archivo in archivos_txt:
            try:
                año = self._extraer_año(archivo.name)
                
                with open(archivo, 'r', encoding='utf-8', errors='ignore') as f:
                    texto = f.read()
                
                for categoria, terminos in self.indicadores_raciales.items():
                    for termino in terminos:
                        matches = re.finditer(rf'\b{re.escape(termino)}\b', texto, re.IGNORECASE)
                        for match in matches:
                            contexto = self._extraer_contexto(texto, match.start(), 200)
                            
                            resultados['por_categoria'][categoria].append({
                                'termino': termino,
                                'contexto': contexto,
                                'archivo': archivo.name,
                                'año': año
                            })
                            
                            # Analizar valoración
                            valoracion = self._analizar_valoracion_contexto(contexto)
                            if valoracion:
                                resultados['contextos_valorativos'][categoria].append({
                                    'termino': termino,
                                    'valoracion': valoracion,
                                    'contexto': contexto
                                })
                            
                            # Evolución temporal
                            if año:
                                resultados['evolucion_temporal'][categoria][año] += 1
                            
                            # Términos asociados
                            palabras_contexto = re.findall(r'\b[a-záéíóúñ]+\b', contexto.lower())
                            for palabra in palabras_contexto:
                                if len(palabra) > 3:  # Evitar palabras muy cortas
                                    resultados['terminos_asociados'][categoria][palabra] += 1
                
            except Exception as e:
                continue
        
        return resultados
    
    def _analizar_valoracion_contexto(self, contexto):
        """Analiza la valoración (positiva/negativa) del contexto"""
        contexto_lower = contexto.lower()
        
        positivos = sum(1 for adj in self.adjetivos_positivos if adj.lower() in contexto_lower)
        negativos = sum(1 for adj in self.adjetivos_negativos if adj.lower() in contexto_lower)
        
        if positivos > negativos:
            return 'positiva'
        elif negativos > positivos:
            return 'negativa'
        else:
            return 'neutra'
    
    def _extraer_contexto(self, texto, posicion, longitud=100):
        """Extrae contexto alrededor de una posición"""
        inicio = max(0, posicion - longitud//2)
        fin = min(len(texto), posicion + longitud//2)
        
        contexto = texto[inicio:fin]
        if inicio > 0:
            contexto = "..." + contexto
        if fin < len(texto):
            contexto = contexto + "..."
        
        return contexto.strip()
    
    def _extraer_año(self, nombre_archivo):
        """Extrae el año del nombre del archivo"""
        match = re.search(r'(\d{4})', nombre_archivo)
        return int(match.group(1)) if match else None
    
    def generar_reporte_avanzado(self):
        """Genera un reporte completo del análisis avanzado"""
        print("Realizando análisis avanzado de género y diversidad...")
        
        # Análisis de género
        analisis_genero = self.analizar_tratamiento_genero()
        
        # Análisis de diversidad racial
        analisis_diversidad = self.analizar_diversidad_racial()
        
        reporte = []
        reporte.append("="*80)
        reporte.append("ANÁLISIS AVANZADO - GÉNERO Y DIVERSIDAD EN 'EL SOL' (1918-1935)")
        reporte.append("="*80)
        reporte.append("")
        
        # Sección de género
        reporte.append("🚻 ANÁLISIS DE TRATAMIENTO POR GÉNERO")
        reporte.append("-" * 50)
        
        # Tratamientos formales
        total_masc = sum(analisis_genero['tratamientos_formales']['masculinos'].values())
        total_fem = sum(analisis_genero['tratamientos_formales']['femeninos'].values())
        
        reporte.append(f"Tratamientos formales masculinos: {total_masc}")
        reporte.append(f"Tratamientos formales femeninos: {total_fem}")
        reporte.append(f"Ratio de formalidad: {total_masc/total_fem if total_fem > 0 else 'N/A'}:1")
        reporte.append("")
        
        # Top tratamientos
        if analisis_genero['tratamientos_formales']['masculinos']:
            top_masc = max(analisis_genero['tratamientos_formales']['masculinos'].items(), key=lambda x: x[1])
            reporte.append(f"Tratamiento masculino más usado: {top_masc[0]} ({top_masc[1]} veces)")
        
        if analisis_genero['tratamientos_formales']['femeninos']:
            top_fem = max(analisis_genero['tratamientos_formales']['femeninos'].items(), key=lambda x: x[1])
            reporte.append(f"Tratamiento femenino más usado: {top_fem[0]} ({top_fem[1]} veces)")
        
        reporte.append("")
        
        # Contextos profesionales
        contextos_hombres = len(analisis_genero['contextos_profesionales']['hombres'])
        contextos_mujeres = len(analisis_genero['contextos_profesionales']['mujeres'])
        
        reporte.append(f"Menciones profesionales masculinas: {contextos_hombres}")
        reporte.append(f"Menciones profesionales femeninas: {contextos_mujeres}")
        reporte.append(f"Diferencia profesional: {(contextos_hombres/contextos_mujeres if contextos_mujeres > 0 else 'N/A')}:1")
        reporte.append("")
        
        # Sección de diversidad racial
        reporte.append("🌍 ANÁLISIS DE DIVERSIDAD RACIAL Y ÉTNICA")
        reporte.append("-" * 50)
        
        for categoria, menciones in analisis_diversidad['por_categoria'].items():
            if menciones:
                reporte.append(f"{categoria.upper()}: {len(menciones)} menciones")
                
                # Valoración de contextos
                valoraciones = [m.get('valoracion') for m in analisis_diversidad['contextos_valorativos'].get(categoria, [])]
                if valoraciones:
                    positivas = valoraciones.count('positiva')
                    negativas = valoraciones.count('negativa')
                    neutras = valoraciones.count('neutra')
                    
                    reporte.append(f"  - Contextos positivos: {positivas}")
                    reporte.append(f"  - Contextos negativos: {negativas}")
                    reporte.append(f"  - Contextos neutros: {neutras}")
                
                # Evolución temporal
                evolucion = analisis_diversidad['evolucion_temporal'].get(categoria, {})
                if evolucion:
                    años_ordenados = sorted(evolucion.items())
                    periodo_inicial = sum(count for año, count in años_ordenados[:5])  # Primeros 5 años
                    periodo_final = sum(count for año, count in años_ordenados[-5:])   # Últimos 5 años
                    
                    if periodo_inicial > 0 and periodo_final > 0:
                        cambio = ((periodo_final - periodo_inicial) / periodo_inicial) * 100
                        reporte.append(f"  - Cambio temporal: {cambio:+.1f}% (inicio vs final)")
                
                reporte.append("")
        
        # Conclusiones
        reporte.append("🔍 PRINCIPALES HALLAZGOS")
        reporte.append("-" * 30)
        
        # Hallazgo sobre género
        if total_masc > 0 and total_fem > 0:
            ratio_formal = total_masc / total_fem
            if ratio_formal > 2:
                reporte.append("• SESGO DE FORMALIDAD: Los hombres reciben tratamientos formales")
                reporte.append(f"  significativamente más frecuentes ({ratio_formal:.1f}:1)")
            else:
                reporte.append("• EQUILIBRIO RELATIVO: El tratamiento formal por género")
                reporte.append("  muestra diferencias moderadas")
        
        # Hallazgo sobre diversidad
        total_diversidad = sum(len(menciones) for menciones in analisis_diversidad['por_categoria'].values())
        if total_diversidad > 0:
            categoria_principal = max(analisis_diversidad['por_categoria'].items(), key=lambda x: len(x[1]))
            reporte.append(f"• DIVERSIDAD PRESENTE: Se detectaron {total_diversidad} menciones")
            reporte.append(f"  de diversidad, predominando '{categoria_principal[0]}' ({len(categoria_principal[1])} menciones)")
        
        # Guardar reporte
        with open("analisis_avanzado_el_sol.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(reporte))
        
        return "\n".join(reporte), analisis_genero, analisis_diversidad

def main():
    """Función principal"""
    directorio_textos = "/Users/maria/Desktop/txt- el sol (con vertex)"
    
    analizador = AnalisisAvanzado(directorio_textos)
    reporte, datos_genero, datos_diversidad = analizador.generar_reporte_avanzado()
    
    print(reporte)
    print("\n" + "="*80)
    print("📁 Reporte guardado en: analisis_avanzado_el_sol.txt")
    print("🔬 Este análisis profundiza en:")
    print("  • Diferencias en tratamientos formales por género")
    print("  • Contextos profesionales masculinos vs femeninos")
    print("  • Valoración de menciones de diversidad racial")
    print("  • Evolución temporal de la representación")

if __name__ == "__main__":
    main()