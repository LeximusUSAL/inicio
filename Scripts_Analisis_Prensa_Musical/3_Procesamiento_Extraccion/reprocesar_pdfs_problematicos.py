#!/usr/bin/env python3
import os
from pdfminer.high_level import extract_text
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO

def extraer_con_metodo_alternativo(ruta_pdf):
    """Método alternativo para PDFs problemáticos"""
    try:
        output_string = StringIO()
        with open(ruta_pdf, 'rb') as file:
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for page in PDFPage.get_pages(file, check_extractable=False):
                interpreter.process_page(page)

            device.close()
            texto = output_string.getvalue()
            output_string.close()

        return texto
    except Exception as e:
        print(f"Error con método alternativo: {e}")
        return None

def extraer_texto_robusto(ruta_pdf):
    """Extracción robusta con múltiples métodos"""
    print(f"Intentando extraer: {os.path.basename(ruta_pdf)}")

    # Método 1: extract_text básico
    try:
        texto = extract_text(ruta_pdf, check_extractable=False)
        if texto and len(texto.strip()) > 100:  # Verificar que hay contenido sustancial
            print("  ✓ Método básico exitoso")
            return texto
        else:
            print("  ⚠ Método básico: poco contenido")
    except Exception as e:
        print(f"  ✗ Método básico falló: {e}")

    # Método 2: Con parámetros específicos
    try:
        texto = extract_text(ruta_pdf,
                           check_extractable=False,
                           password='',
                           maxpages=0,
                           caching=True)
        if texto and len(texto.strip()) > 100:
            print("  ✓ Método con parámetros exitoso")
            return texto
        else:
            print("  ⚠ Método con parámetros: poco contenido")
    except Exception as e:
        print(f"  ✗ Método con parámetros falló: {e}")

    # Método 3: Alternativo manual
    texto = extraer_con_metodo_alternativo(ruta_pdf)
    if texto and len(texto.strip()) > 100:
        print("  ✓ Método alternativo exitoso")
        return texto
    else:
        print("  ✗ Método alternativo: poco o ningún contenido")

    return None

def reprocesar_archivos_problematicos():
    """Reprocesa archivos que fallaron"""
    directorio_pdfs = "/Users/maria/Downloads/BIBLIOGRAFÍA. Historiografía-20250929"
    directorio_salida = "/Users/maria/Downloads/textos_extraidos_bibliografia"

    archivos_problematicos = [
        "BRITO_1989._Musicologia_e_Historiografia_portuguesa.pdf",
        "CARRERAS_1994._Historiografia_musical.pdf",
        "FERREIRA_1992._Historiografia_Portugal_XIX.pdf",
        "RIEGER_1986._Dolce_semplice._El_papel_de_las_mujeres_en_la_musica.pdf",
        "STROHM_1999._Postmodern_thought_and_the_History_of_Music.pdf",
        "VIRGILI_BLANQUET_2004._La_musica_religiosa_en_el_siglo_XIX_espanol.pdf",
        "Weber 1999. The History of Musical Canon.pdf"
    ]

    print("=== Reprocesando archivos problemáticos ===\n")

    for nombre_archivo in archivos_problematicos:
        ruta_pdf = os.path.join(directorio_pdfs, nombre_archivo)

        if not os.path.exists(ruta_pdf):
            print(f"❌ No encontrado: {nombre_archivo}")
            continue

        # Extraer texto con métodos robustos
        texto = extraer_texto_robusto(ruta_pdf)

        if texto:
            # Guardar resultado
            nombre_base = os.path.splitext(nombre_archivo)[0]
            archivo_txt = os.path.join(directorio_salida, f"{nombre_base}.txt")

            try:
                with open(archivo_txt, 'w', encoding='utf-8') as f:
                    f.write(texto)
                print(f"  💾 Guardado: {len(texto)} caracteres")
                print(f"     {archivo_txt}")
            except Exception as e:
                print(f"  ❌ Error guardando: {e}")
        else:
            print(f"  ❌ No se pudo extraer texto de {nombre_archivo}")

        print()  # Línea en blanco

if __name__ == "__main__":
    reprocesar_archivos_problematicos()
    print("¡Reprocesamiento completado!")