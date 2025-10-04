#!/usr/bin/env python3

import fitz
import os

# Rutas
pdf_path = "/Users/maria/Desktop/1914 Nº 1/Revista-musical-hispano-americana-1-1914-n-o-1.pdf"
output_dir = "/Users/maria/Desktop/1914 Nº 1"

# Abrir PDF
doc = fitz.open(pdf_path)
base_name = "Revista-musical-hispano-americana-1-1914-n-o-1"

print(f"Procesando: {os.path.basename(pdf_path)}")
print(f"Páginas: {len(doc)}")

# Convertir páginas
for i in range(len(doc)):
    page = doc.load_page(i)
    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat)
    output_file = f"{base_name}_pagina_{i+1:03d}.jpg"
    output_path = os.path.join(output_dir, output_file)
    pix.save(output_path)
    print(f"Página {i+1} → {output_file}")

doc.close()
print(f"Completado: {len(doc)} páginas convertidas")