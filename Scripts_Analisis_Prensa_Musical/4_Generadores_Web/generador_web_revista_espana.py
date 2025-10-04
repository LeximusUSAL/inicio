#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generador de interfaz web para Revista ESPAÑA
Similar al diseño de El Sol con datos embebidos

Proyecto LexiMus: Léxico y ontología de la música en español (PID2022-139589NB-C33)
Universidad de Salamanca
"""

import json
import os
from datetime import datetime

def generar_web_revista_espana():
    # Cargar datos del análisis
    with open('/Users/maria/datos_revista_espana_musical.json', 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    # Preparar datos para JavaScript embebido
    articulos_js = []
    for articulo in datos['articulos']:
        articulo_web = {
            'id': articulo['numero'],
            'numero': articulo['numero'],
            'titulo': articulo['titulo'][:100] + '...' if len(articulo['titulo']) > 100 else articulo['titulo'],
            'fecha': articulo['fecha'],
            'autores': ', '.join(articulo['autores']) if articulo['autores'] else 'Autor no identificado',
            'periodo': articulo['periodo'],
            'num_palabras': articulo['num_palabras'],
            'total_menciones_musicales': articulo['total_menciones_musicales'],
            'contenido': articulo['contenido']
        }
        articulos_js.append(articulo_web)
    
    # Estadísticas para la página
    estadisticas = datos['estadisticas']['resumen_general']
    
    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Revista ESPAÑA (1915-1924) - Análisis Musical</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 20px;
            min-height: 100vh;
        }}

        .sidebar {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            height: fit-content;
            position: sticky;
            top: 20px;
        }}

        .main-content {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}


        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: #310000;
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}

        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            display: block;
        }}

        .stat-label {{
            font-size: 0.9rem;
            opacity: 0.9;
            margin-top: 5px;
        }}

        .search-section {{
            margin-bottom: 25px;
        }}

        .search-input {{
            width: 100%;
            padding: 15px;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }}

        .search-input:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .filter-section {{
            margin-bottom: 25px;
        }}

        .filter-title {{
            font-weight: 600;
            margin-bottom: 15px;
            color: #4a5568;
            font-size: 1.1rem;
        }}

        .period-filters {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .period-btn {{
            background: #f7fafc;
            border: 2px solid #e2e8f0;
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: left;
            font-size: 0.9rem;
        }}

        .period-btn:hover,
        .period-btn.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }}

        .results-section {{
            margin-top: 20px;
        }}

        .results-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e2e8f0;
        }}

        .results-count {{
            font-weight: 600;
            color: #4a5568;
        }}

        .sort-select {{
            padding: 8px 12px;
            border: 2px solid #e2e8f0;
            border-radius: 6px;
            font-size: 0.9rem;
            background: white;
        }}

        .article-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .article-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            border-color: #667eea;
        }}

        .article-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }}

        .article-number {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }}

        .article-date {{
            color: #666;
            font-size: 0.9rem;
        }}

        .article-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
            line-height: 1.4;
        }}

        .article-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            font-size: 0.85rem;
            color: #666;
            margin-bottom: 10px;
        }}

        .article-preview {{
            color: #4a5568;
            font-size: 0.9rem;
            line-height: 1.5;
            margin-top: 10px;
        }}

        .highlight {{
            background: #fef9c3;
            padding: 2px 4px;
            border-radius: 3px;
        }}

        .pagination {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-top: 30px;
        }}

        .page-btn {{
            padding: 10px 15px;
            border: 2px solid #e2e8f0;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .page-btn:hover,
        .page-btn.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }}

        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(5px);
        }}

        .modal-content {{
            background: white;
            margin: 2% auto;
            padding: 30px;
            border-radius: 15px;
            width: 90%;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}

        .modal-header {{
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }}

        .close {{
            position: absolute;
            right: 20px;
            top: 20px;
            font-size: 2rem;
            cursor: pointer;
            color: #666;
            transition: color 0.3s ease;
        }}

        .close:hover {{
            color: #f56565;
        }}

        .modal-body {{
            line-height: 1.6;
            color: #4a5568;
        }}

        .notice {{
            background: #fef7e0;
            border: 1px solid #f6d55c;
            color: #744210;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 0.9rem;
        }}

        .header-sidebar {{
            text-align: center;
            margin-bottom: 25px;
            padding: 20px;
            background: linear-gradient(135deg, #e8f4fd 0%, #f8f0ff 100%);
            border-radius: 15px;
        }}

        .header-sidebar h1 {{
            font-size: 1.8rem;
            color: #4a5568;
            margin-bottom: 8px;
            font-weight: 700;
        }}

        .header-sidebar .subtitle {{
            color: #666;
            font-size: 1rem;
            margin-bottom: 10px;
            font-weight: 500;
        }}

        .project-code {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 5px;
        }}

        .institution {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }}

        .bne-link {{
            font-size: 0.8rem;
            padding-top: 10px;
            border-top: 1px solid rgba(0,0,0,0.1);
        }}

        .bne-link a {{
            color: #ff6b35;
            text-decoration: none;
        }}

        .bne-link a:hover {{
            text-decoration: underline;
        }}

        .header {{
            margin-bottom: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5rem;
            color: #4a5568;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header .subtitle {{
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 20px;
        }}

        @media (max-width: 768px) {{
            .container {{
                grid-template-columns: 1fr;
                padding: 15px;
            }}
            
            .sidebar {{
                position: static;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <div class="header-sidebar">
                <h1>Proyecto <span style="color: #ff6b35;">LexiMus</span></h1>
                <div class="subtitle">Léxico y ontología de la música en español</div>
                <div class="project-code">PID2022-139589NB-C33</div>
                <div class="institution">Universidad de Salamanca</div>
                <div class="bne-link">
                    Todos los números España disponibles en la <a href="https://hemerotecadigital.bne.es/hd/es/card?sid=3274681" target="_blank">Hemeroteca de la BNE</a>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-number">{estadisticas['total_numeros']}</span>
                    <span class="stat-label">Números de revista con referencias musicales</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{estadisticas['total_palabras']:,}</span>
                    <span class="stat-label">Total de palabras</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">{estadisticas['palabras_unicas']:,}</span>
                    <span class="stat-label">Palabras únicas</span>
                </div>
            </div>
            
            <div class="filter-section">
                <div class="filter-title">Búsqueda</div>
                <input type="text" id="searchInput" class="search-input" placeholder="Buscar en contenido...">
            </div>
            
            <div class="filter-section">
                <div class="filter-title">Filtrar por Año</div>
                <div class="period-filters">
                    <button class="period-btn active" data-year="all">
                        Todos los años
                    </button>
                    <button class="period-btn" data-year="1915">1915</button>
                    <button class="period-btn" data-year="1916">1916</button>
                    <button class="period-btn" data-year="1917">1917</button>
                    <button class="period-btn" data-year="1918">1918</button>
                    <button class="period-btn" data-year="1919">1919</button>
                    <button class="period-btn" data-year="1920">1920</button>
                    <button class="period-btn" data-year="1921">1921</button>
                    <button class="period-btn" data-year="1922">1922</button>
                    <button class="period-btn" data-year="1923">1923</button>
                    <button class="period-btn" data-year="1924">1924</button>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="header">
                <h1>Revista ESPAÑA</h1>
                <div class="subtitle">
                    Búsqueda de referencias y noticias sobre música (1915-1924)
                </div>
            </div>
            
            <div class="results-section">
                <div class="results-header">
                    <div class="results-count" id="resultsCount">
                        Mostrando {len(articulos_js)} artículos
                    </div>
                    <select id="sortSelect" class="sort-select">
                        <option value="numero">Ordenar por número</option>
                        <option value="fecha">Ordenar por fecha</option>
                        <option value="palabras">Ordenar por palabras</option>
                    </select>
                </div>
                
                <div id="articlesList">
                    <!-- Los artículos se cargarán aquí -->
                </div>
                
                <div class="pagination" id="pagination">
                    <!-- La paginación se cargará aquí -->
                </div>
            </div>
        </div>
    </div>
    
    <!-- Modal para mostrar artículos completos -->
    <div id="articleModal" class="modal">
        <div class="modal-content">
            <span class="close">&times;</span>
            <div class="modal-header">
                <h2 id="modalTitle"></h2>
                <div id="modalMeta"></div>
            </div>
            <div class="modal-body" id="modalBody">
            </div>
        </div>
    </div>

    <script>
        // Datos embebidos
        const articulos = {json.dumps(articulos_js, ensure_ascii=False, indent=2)};
        
        let filteredArticles = [...articulos];
        let currentPage = 1;
        const articlesPerPage = 10;
        
        // Referencias a elementos DOM
        const searchInput = document.getElementById('searchInput');
        const periodBtns = document.querySelectorAll('.period-btn');
        const sortSelect = document.getElementById('sortSelect');
        const articlesList = document.getElementById('articlesList');
        const resultsCount = document.getElementById('resultsCount');
        const pagination = document.getElementById('pagination');
        const modal = document.getElementById('articleModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalMeta = document.getElementById('modalMeta');
        const modalBody = document.getElementById('modalBody');
        const closeBtn = document.querySelector('.close');
        
        // Event listeners
        searchInput.addEventListener('input', handleSearch);
        periodBtns.forEach(btn => btn.addEventListener('click', handleYearFilter));
        sortSelect.addEventListener('change', handleSort);
        closeBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => {{
            if (e.target === modal) closeModal();
        }});
        
        // Funciones de filtrado y búsqueda
        function handleSearch() {{
            const searchTerm = searchInput.value.toLowerCase();
            filteredArticles = articulos.filter(article =>
                article.titulo.toLowerCase().includes(searchTerm) ||
                article.contenido.toLowerCase().includes(searchTerm) ||
                article.autores.toLowerCase().includes(searchTerm)
            );
            currentPage = 1;
            updateDisplay();
        }}
        
        function handleYearFilter(e) {{
            periodBtns.forEach(btn => btn.classList.remove('active'));
            e.target.classList.add('active');
            
            const selectedYear = e.target.dataset.year;
            if (selectedYear === 'all') {{
                filteredArticles = [...articulos];
            }} else {{
                filteredArticles = articulos.filter(article => {{
                    const articleYear = article.fecha.match(/\\d{{4}}/)
                    return articleYear && articleYear[0] === selectedYear;
                }});
            }}
            
            // Aplicar búsqueda actual si existe
            const searchTerm = searchInput.value.toLowerCase();
            if (searchTerm) {{
                filteredArticles = filteredArticles.filter(article =>
                    article.titulo.toLowerCase().includes(searchTerm) ||
                    article.contenido.toLowerCase().includes(searchTerm) ||
                    article.autores.toLowerCase().includes(searchTerm)
                );
            }}
            
            currentPage = 1;
            updateDisplay();
        }}
        
        function handleSort() {{
            const sortBy = sortSelect.value;
            filteredArticles.sort((a, b) => {{
                switch(sortBy) {{
                    case 'numero':
                        return a.numero - b.numero;
                    case 'fecha':
                        return new Date(a.fecha) - new Date(b.fecha);
                    case 'palabras':
                        return b.num_palabras - a.num_palabras;
                    default:
                        return 0;
                }}
            }});
            currentPage = 1;
            updateDisplay();
        }}
        
        function updateDisplay() {{
            displayArticles();
            updatePagination();
            updateResultsCount();
        }}
        
        function displayArticles() {{
            const startIndex = (currentPage - 1) * articlesPerPage;
            const endIndex = startIndex + articlesPerPage;
            const pageArticles = filteredArticles.slice(startIndex, endIndex);
            
            articlesList.innerHTML = pageArticles.map(article => {{
                const preview = article.contenido.substring(0, 200).replace(/\\d+→/g, '') + '...';
                const searchTerm = searchInput.value.toLowerCase();
                const highlightedTitle = searchTerm ? 
                    highlightText(article.titulo, searchTerm) : article.titulo;
                const highlightedPreview = searchTerm ? 
                    highlightText(preview, searchTerm) : preview;
                
                return `
                    <div class="article-card" onclick="openModal(${{article.numero}})">
                        <div class="article-header">
                            <span class="article-number">N° ${{article.numero}}</span>
                            <span class="article-date">${{article.fecha}}</span>
                        </div>
                        <div class="article-title">${{highlightedTitle}}</div>
                        <div class="article-meta">
                            <span>📝 ${{article.autores}}</span>
                            <span>📅 ${{article.periodo}}</span>
                            <span>📊 ${{article.num_palabras}} palabras</span>
                        </div>
                        <div class="article-preview">${{highlightedPreview}}</div>
                    </div>
                `;
            }}).join('');
        }}
        
        function updatePagination() {{
            const totalPages = Math.ceil(filteredArticles.length / articlesPerPage);
            
            if (totalPages <= 1) {{
                pagination.innerHTML = '';
                return;
            }}
            
            let paginationHTML = '';
            
            // Botón anterior
            if (currentPage > 1) {{
                paginationHTML += `<button class="page-btn" onclick="changePage(${{currentPage - 1}})">‹ Anterior</button>`;
            }}
            
            // Números de página
            const startPage = Math.max(1, currentPage - 2);
            const endPage = Math.min(totalPages, currentPage + 2);
            
            for (let i = startPage; i <= endPage; i++) {{
                paginationHTML += `<button class="page-btn ${{i === currentPage ? 'active' : ''}}" onclick="changePage(${{i}})">${{i}}</button>`;
            }}
            
            // Botón siguiente
            if (currentPage < totalPages) {{
                paginationHTML += `<button class="page-btn" onclick="changePage(${{currentPage + 1}})">Siguiente ›</button>`;
            }}
            
            pagination.innerHTML = paginationHTML;
        }}
        
        function updateResultsCount() {{
            resultsCount.textContent = `Mostrando ${{filteredArticles.length}} artículos`;
        }}
        
        function changePage(page) {{
            currentPage = page;
            displayArticles();
            updatePagination();
            
            // Scroll to top
            document.querySelector('.main-content').scrollTo({{
                top: 0,
                behavior: 'smooth'
            }});
        }}
        
        function highlightText(text, searchTerm) {{
            if (!searchTerm) return text;
            const regex = new RegExp(`(${{searchTerm.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&')}})`, 'gi');
            return text.replace(regex, '<span class="highlight">$1</span>');
        }}
        
        function openModal(articleId) {{
            const article = articulos.find(a => a.numero === articleId);
            if (!article) return;
            
            modalTitle.textContent = article.titulo;
            modalMeta.innerHTML = `
                <div style="margin-bottom: 10px;">
                    <strong>Número:</strong> ${{article.numero}} | 
                    <strong>Fecha:</strong> ${{article.fecha}} | 
                    <strong>Período:</strong> ${{article.periodo}}
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Autor(es):</strong> ${{article.autores}} | 
                    <strong>Palabras:</strong> ${{article.num_palabras}}
                </div>
            `;
            
            // Formatear contenido eliminando números de línea y mejorando presentación
            const formattedContent = article.contenido
                .replace(/^\\s*\\d+→/gm, '')
                .replace(/\\n\\s*\\n/g, '</p><p>')
                .replace(/^/, '<p>')
                .replace(/$/, '</p>');
            
            modalBody.innerHTML = formattedContent;
            modal.style.display = 'block';
            document.body.style.overflow = 'hidden';
        }}
        
        function closeModal() {{
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }}
        
        // Inicialización
        document.addEventListener('DOMContentLoaded', function() {{
            updateDisplay();
        }});
        
        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape' && modal.style.display === 'block') {{
                closeModal();
            }}
        }});
    </script>
</body>
</html>'''
    
    # Guardar el archivo HTML
    with open('/Users/maria/revista_espana_musical.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Interfaz web generada: /Users/maria/revista_espana_musical.html")
    print(f"Datos procesados: {len(articulos_js)} artículos")
    print("La interfaz incluye:")
    print("- Búsqueda en tiempo real")
    print("- Filtros por período histórico")
    print("- Ordenación múltiple")
    print("- Visualización modal de artículos completos")
    print("- Diseño responsivo similar a El Sol")


if __name__ == "__main__":
    generar_web_revista_espana()