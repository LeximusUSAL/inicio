#!/usr/bin/env python3
"""
Generador de página web interactiva para el análisis de El Sol
"""

import json
import os
from pathlib import Path

def cargar_datos():
    """Carga los datos del análisis"""
    try:
        with open('resultados_el_sol.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró el archivo resultados_el_sol.json")
        print("Ejecuta primero analizador_el_sol.py")
        return None

def generar_insights_avanzados(datos):
    """Genera insights más profundos basados en los datos"""
    insights = []
    
    # Análisis de compositores
    compositores = datos.get('compositores', {})
    if compositores:
        total_menciones = sum(len(menciones) for menciones in compositores.values())
        comp_top = max(compositores.items(), key=lambda x: len(x[1]))
        
        insights.append({
            'titulo': '🎼 Predominio de la Música Clásica',
            'texto': f'{comp_top[0]} lidera con {len(comp_top[1])} menciones de un total de {total_menciones}. Esto representa el {(len(comp_top[1])/total_menciones*100):.1f}% de todas las menciones de compositores.'
        })
    
    # Análisis de género
    genero_stats = datos.get('estadisticas', {}).get('ratio_genero', {})
    hombres = genero_stats.get('hombres', 0)
    mujeres = genero_stats.get('mujeres', 0)
    
    if hombres > 0 and mujeres > 0:
        ratio = hombres / mujeres
        insights.append({
            'titulo': '⚖️ Brecha de Género en la Música',
            'texto': f'Por cada mujer mencionada, aparecen {ratio:.1f} hombres. Esta disparidad refleja las limitaciones sociales de la época (1918-1935), aunque la presencia de {mujeres} mujeres músicas es notable para el período.'
        })
    
    # Análisis de diversidad
    diversidad = datos.get('diversidad_racial', {})
    if diversidad:
        total_diversidad = sum(len(menciones) for menciones in diversidad.values())
        principales = sorted(diversidad.items(), key=lambda x: len(x[1]), reverse=True)[:3]
        
        insights.append({
            'titulo': '🌍 Consciencia Internacional',
            'texto': f'Se detectaron {total_diversidad} menciones de diversidad cultural. Los términos más frecuentes son: {principales[0][0]} ({len(principales[0][1])} menciones), {principales[1][0]} ({len(principales[1][1])}) y {principales[2][0]} ({len(principales[2][1])}).'
        })
    
    # Análisis de géneros musicales
    generos = datos.get('generos_musicales', {})
    if generos:
        total_generos = sum(generos.values())
        genero_top = max(generos.items(), key=lambda x: x[1])
        
        insights.append({
            'titulo': '🎵 Preferencias Musicales',
            'texto': f'"{genero_top[0].title()}" domina con {genero_top[1]} menciones ({(genero_top[1]/total_generos*100):.1f}% del total). Esto indica una fuerte cultura de música formal y académica en España.'
        })
    
    return insights

def generar_html_avanzado(datos):
    """Genera el HTML con los datos reales"""
    
    stats = datos.get('estadisticas', {})
    insights = generar_insights_avanzados(datos)
    
    # Preparar datos para gráficos
    compositores = datos.get('compositores', {})
    compositores_top = sorted(compositores.items(), key=lambda x: len(x[1]), reverse=True)[:10]
    
    generos = datos.get('generos_musicales', {})
    generos_top = sorted(generos.items(), key=lambda x: x[1], reverse=True)[:10]
    
    diversidad = datos.get('diversidad_racial', {})
    diversidad_sorted = sorted(diversidad.items(), key=lambda x: len(x[1]), reverse=True)
    
    # Datos de género
    ratio_genero = stats.get('ratio_genero', {})
    hombres = ratio_genero.get('hombres', 0)
    mujeres = ratio_genero.get('mujeres', 0)
    
    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis Musical - El Sol (1918-1935)</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Georgia', serif;
            line-height: 1.6;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}

        h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}

        .subtitle {{
            color: #7f8c8d;
            font-size: 1.2em;
            font-style: italic;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
        }}

        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
            display: block;
        }}

        .stat-label {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 5px;
        }}

        .chart-container {{
            background: white;
            margin-bottom: 30px;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .chart-title {{
            font-size: 1.5em;
            margin-bottom: 20px;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}

        .gender-analysis {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }}

        .gender-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .gender-card.male {{
            border-left: 5px solid #3498db;
        }}

        .gender-card.female {{
            border-left: 5px solid #e74c3c;
        }}

        .diversity-section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .diversity-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .diversity-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #f39c12;
        }}

        .composers-section {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .composer-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .composer-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .composer-rank {{
            background: #3498db;
            color: white;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.9em;
        }}

        .insights {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .insight {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #2ecc71;
        }}

        .insight h4 {{
            color: #27ae60;
            margin-bottom: 10px;
        }}

        footer {{
            text-align: center;
            padding: 30px;
            color: #7f8c8d;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        @media (max-width: 768px) {{
            .gender-analysis {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 2em;
            }}
            
            .container {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎼 Análisis Musical del Periódico "El Sol"</h1>
            <p class="subtitle">Panorama de la vida musical española (1918-1935)</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-number">1,427</span>
                <span class="stat-label">Artículos Analizados</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{stats.get('total_compositores', 0)}</span>
                <span class="stat-label">Compositores Identificados</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">{stats.get('total_interpretes', 0)}</span>
                <span class="stat-label">Intérpretes Mencionados</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">17</span>
                <span class="stat-label">Años de Cobertura</span>
            </div>
        </div>

        <div class="gender-analysis">
            <div class="gender-card male">
                <h3>👨‍🎼 Representación Masculina</h3>
                <div class="stat-number" style="color: #3498db;">{hombres:,}</div>
                <p>Hombres identificados en las crónicas musicales</p>
                <p><strong>Ratio:</strong> {(hombres/mujeres if mujeres > 0 else 0):.1f}:1 respecto a mujeres</p>
            </div>
            <div class="gender-card female">
                <h3>👩‍🎼 Representación Femenina</h3>
                <div class="stat-number" style="color: #e74c3c;">{mujeres:,}</div>
                <p>Mujeres identificadas en las crónicas musicales</p>
                <p><strong>Observación:</strong> Menor presencia pero significativa para la época</p>
            </div>
        </div>

        <div class="chart-container">
            <h3 class="chart-title">📊 Representación de Género en la Música</h3>
            <canvas id="genderChart" width="400" height="200"></canvas>
        </div>

        <div class="composers-section">
            <h3 class="chart-title">🎵 Top 10 Compositores Más Mencionados</h3>
            <div class="composer-list">'''
    
    # Agregar compositores top
    for i, (compositor, menciones) in enumerate(compositores_top):
        html += f'''
                <div class="composer-item">
                    <div>
                        <strong>{compositor}</strong>
                        <div style="font-size: 0.9em; color: #7f8c8d;">{len(menciones)} menciones</div>
                    </div>
                    <div class="composer-rank">{i+1}</div>
                </div>'''
    
    html += '''
            </div>
        </div>

        <div class="chart-container">
            <h3 class="chart-title">🎭 Géneros Musicales Más Populares</h3>
            <canvas id="genresChart" width="400" height="200"></canvas>
        </div>

        <div class="diversity-section">
            <h3 class="chart-title">🌍 Diversidad Cultural y Racial en la Música</h3>
            <p>El análisis revela menciones significativas de diversidad cultural:</p>
            <div class="diversity-grid">'''
    
    # Agregar elementos de diversidad
    for termino, menciones in diversidad_sorted[:12]:  # Top 12
        html += f'''
                <div class="diversity-item">
                    <strong>{termino.title()}</strong>
                    <div>{len(menciones)} menciones</div>
                </div>'''
    
    html += '''
            </div>
        </div>

        <div class="insights">
            <h3 class="chart-title">💡 Hallazgos Significativos</h3>'''
    
    # Agregar insights
    for insight in insights:
        html += f'''
            <div class="insight">
                <h4>{insight['titulo']}</h4>
                <p>{insight['texto']}</p>
            </div>'''
    
    html += f'''
        </div>

        <footer>
            <p>📊 Análisis realizado sobre 1,427 artículos del periódico "El Sol" (1918-1935)</p>
            <p>🔍 Metodología: Procesamiento de lenguaje natural y análisis de patrones textuales</p>
            <p>📅 Período analizado: 17 años de crónicas musicales españolas</p>
            <p>🎯 Compositor más mencionado: {stats.get('compositor_mas_mencionado', 'N/A')}</p>
            <p>🎼 Género más popular: {stats.get('genero_mas_mencionado', 'N/A')}</p>
        </footer>
    </div>

    <script>
        // Gráfico de representación de género
        const ctx1 = document.getElementById('genderChart').getContext('2d');
        new Chart(ctx1, {{
            type: 'doughnut',
            data: {{
                labels: ['Hombres', 'Mujeres'],
                datasets: [{{
                    data: [{hombres}, {mujeres}],
                    backgroundColor: ['#3498db', '#e74c3c'],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom',
                        labels: {{
                            padding: 20,
                            font: {{
                                size: 14
                            }}
                        }}
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed * 100) / total).toFixed(1);
                                return context.label + ': ' + context.parsed.toLocaleString() + ' (' + percentage + '%)';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // Gráfico de géneros musicales
        const ctx2 = document.getElementById('genresChart').getContext('2d');
        new Chart(ctx2, {{
            type: 'bar',
            data: {{
                labels: {[g[0].title() for g in generos_top]},
                datasets: [{{
                    label: 'Menciones',
                    data: {[g[1] for g in generos_top]},
                    backgroundColor: [
                        '#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
                        '#1abc9c', '#e67e22', '#34495e', '#f1c40f', '#e84393'
                    ],
                    borderWidth: 0,
                    borderRadius: 5
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return context.label + ': ' + context.parsed.y.toLocaleString() + ' menciones';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        grid: {{
                            color: '#ecf0f1'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''

    return html

def main():
    """Función principal"""
    print("Generando página web interactiva...")
    
    datos = cargar_datos()
    if not datos:
        return
    
    html = generar_html_avanzado(datos)
    
    # Guardar la página web
    with open('analisis_musical_el_sol.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Obtener ruta absoluta
    ruta_completa = os.path.abspath('analisis_musical_el_sol.html')
    
    print(f"✅ Página web generada exitosamente!")
    print(f"📁 Archivo: analisis_musical_el_sol.html")
    print(f"🌐 Ruta completa: {ruta_completa}")
    print(f"🔗 Para abrir: file://{ruta_completa}")
    print()
    print("🎯 La página incluye:")
    print("  • Estadísticas generales del análisis")
    print("  • Gráficos interactivos de géneros y compositores")
    print("  • Análisis de representación de género")
    print("  • Mapeo de diversidad cultural y racial")
    print("  • Insights profundos basados en los datos")

if __name__ == "__main__":
    main()