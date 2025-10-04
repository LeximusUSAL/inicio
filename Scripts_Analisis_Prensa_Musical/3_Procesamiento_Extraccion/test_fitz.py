#!/usr/bin/env python3

try:
    import fitz
    print("✅ PyMuPDF está disponible")
    
    # Intentar abrir el PDF
    pdf_path = "/Users/maria/Desktop/1914 Nº 1/Revista-musical-hispano-americana-1-1914-n-o-1.pdf"
    
    print(f"Intentando abrir: {pdf_path}")
    doc = fitz.open(pdf_path)
    print(f"✅ PDF abierto exitosamente")
    print(f"📄 Número de páginas: {len(doc)}")
    
    # Convertir solo la primera página como prueba
    page = doc.load_page(0)
    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat)
    
    output_path = "/Users/maria/Desktop/1914 Nº 1/test_pagina_001.jpg"
    pix.save(output_path)
    print(f"✅ Página de prueba guardada: test_pagina_001.jpg")
    
    doc.close()
    
except ImportError:
    print("❌ PyMuPDF no está disponible")
except Exception as e:
    print(f"❌ Error: {e}")