#!/usr/bin/env python3
import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

def extraer_con_ocr(ruta_pdf, idioma='spa+eng'):
    """Extrae texto de PDF usando OCR"""
    print(f"Procesando con OCR: {os.path.basename(ruta_pdf)}")

    try:
        # Convertir PDF a imágenes
        print("  - Convirtiendo PDF a imágenes...")
        imagenes = convert_from_path(ruta_pdf, dpi=300)

        texto_completo = ""

        # Procesar cada página
        for i, imagen in enumerate(imagenes):
            print(f"  - Procesando página {i+1}/{len(imagenes)}...")

            # Aplicar OCR a la imagen
            texto_pagina = pytesseract.image_to_string(imagen, lang=idioma)

            if texto_pagina.strip():
                texto_completo += f"\n\n--- PÁGINA {i+1} ---\n\n"
                texto_completo += texto_pagina

        return texto_completo

    except Exception as e:
        print(f"  ❌ Error en OCR: {e}")
        return None

def procesar_archivos_con_ocr():
    """Procesa archivos problemáticos con OCR"""
    directorio_pdfs = "/Users/maria/Downloads/BIBLIOGRAFÍA. Historiografía-20250929"
    directorio_salida = "/Users/maria/Downloads/textos_extraidos_bibliografia"

    archivos_problematicos = [
        "BRITO_1989._Musicologia_e_Historiografia_portuguesa.pdf",
        "CARRERAS_1994._Historiografia_musical.pdf",
        "RIEGER_1986._Dolce_semplice._El_papel_de_las_mujeres_en_la_musica.pdf",
        "STROHM_1999._Postmodern_thought_and_the_History_of_Music.pdf",
        "Weber 1999. The History of Musical Canon.pdf"
    ]

    print("=== Extracción con OCR ===\n")

    for nombre_archivo in archivos_problematicos:
        ruta_pdf = os.path.join(directorio_pdfs, nombre_archivo)

        if not os.path.exists(ruta_pdf):
            print(f"❌ No encontrado: {nombre_archivo}")
            continue

        # Extraer con OCR
        texto = extraer_con_ocr(ruta_pdf)

        if texto and len(texto.strip()) > 100:
            # Guardar resultado
            nombre_base = os.path.splitext(nombre_archivo)[0]
            archivo_txt = os.path.join(directorio_salida, f"{nombre_base}_OCR.txt")

            try:
                with open(archivo_txt, 'w', encoding='utf-8') as f:
                    f.write(texto)
                print(f"  ✅ Guardado: {len(texto)} caracteres")
                print(f"     {archivo_txt}")
            except Exception as e:
                print(f"  ❌ Error guardando: {e}")
        else:
            print(f"  ❌ OCR no extrajo contenido útil de {nombre_archivo}")

        print()  # Línea en blanco

if __name__ == "__main__":
    procesar_archivos_con_ocr()
    print("¡Extracción con OCR completada!")