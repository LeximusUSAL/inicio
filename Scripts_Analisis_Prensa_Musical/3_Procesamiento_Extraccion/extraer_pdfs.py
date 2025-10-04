#!/usr/bin/env python3
import os
import glob
from pdfminer.high_level import extract_text
from pathlib import Path

def extraer_texto_pdf(ruta_pdf):
    """Extrae texto de un archivo PDF"""
    try:
        texto = extract_text(ruta_pdf)
        return texto
    except Exception as e:
        print(f"Error procesando {ruta_pdf}: {e}")
        return None

def procesar_pdfs_directorio(directorio_origen, directorio_destino=None):
    """Procesa todos los PDFs de un directorio"""

    # Si no se especifica directorio destino, usar el mismo directorio
    if directorio_destino is None:
        directorio_destino = directorio_origen

    # Crear directorio destino si no existe
    Path(directorio_destino).mkdir(parents=True, exist_ok=True)

    # Buscar todos los PDFs
    patron_pdfs = os.path.join(directorio_origen, "*.pdf")
    archivos_pdf = glob.glob(patron_pdfs)

    if not archivos_pdf:
        print(f"No se encontraron PDFs en {directorio_origen}")
        return

    print(f"Encontrados {len(archivos_pdf)} archivos PDF")

    for archivo_pdf in archivos_pdf:
        print(f"Procesando: {os.path.basename(archivo_pdf)}")

        # Extraer texto
        texto = extraer_texto_pdf(archivo_pdf)

        if texto:
            # Crear nombre del archivo de texto
            nombre_base = Path(archivo_pdf).stem
            archivo_txt = os.path.join(directorio_destino, f"{nombre_base}.txt")

            # Guardar texto extraído
            try:
                with open(archivo_txt, 'w', encoding='utf-8') as f:
                    f.write(texto)
                print(f"  ✓ Guardado: {archivo_txt}")
            except Exception as e:
                print(f"  ✗ Error guardando {archivo_txt}: {e}")
        else:
            print(f"  ✗ No se pudo extraer texto de {archivo_pdf}")

def procesar_lista_pdfs(lista_archivos, directorio_destino="textos_extraidos"):
    """Procesa una lista específica de archivos PDF"""

    Path(directorio_destino).mkdir(parents=True, exist_ok=True)

    for archivo_pdf in lista_archivos:
        if not os.path.exists(archivo_pdf):
            print(f"Archivo no encontrado: {archivo_pdf}")
            continue

        print(f"Procesando: {archivo_pdf}")
        texto = extraer_texto_pdf(archivo_pdf)

        if texto:
            nombre_base = Path(archivo_pdf).stem
            archivo_txt = os.path.join(directorio_destino, f"{nombre_base}.txt")

            with open(archivo_txt, 'w', encoding='utf-8') as f:
                f.write(texto)
            print(f"  ✓ Guardado: {archivo_txt}")

if __name__ == "__main__":
    # Configuración para tu directorio específico
    directorio_pdfs = "/Users/maria/Downloads/BIBLIOGRAFÍA. Historiografía-20250929"
    directorio_salida = "/Users/maria/Downloads/textos_extraidos_bibliografia"

    print("=== Extractor de texto de PDFs ===")
    print(f"Directorio origen: {directorio_pdfs}")
    print(f"Directorio destino: {directorio_salida}")
    print()

    # Procesar todos los PDFs del directorio de bibliografía
    procesar_pdfs_directorio(directorio_pdfs, directorio_salida)

    print("\n¡Proceso completado!")