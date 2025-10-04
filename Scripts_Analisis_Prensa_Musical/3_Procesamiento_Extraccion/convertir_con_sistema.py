#!/usr/bin/env python3
import subprocess
import os

def convertir_pdf_con_sistema():
    pdf_path = "/Users/maria/Desktop/1914 Nº 1/Revista-musical-hispano-americana-1-1914-n-o-1.pdf"
    output_dir = "/Users/maria/Desktop/1914 Nº 1"
    
    # Verificar que el PDF existe
    if not os.path.exists(pdf_path):
        print(f"Error: No se encuentra el PDF en {pdf_path}")
        return
    
    print(f"Convirtiendo PDF: {os.path.basename(pdf_path)}")
    
    # Usar osascript para convertir (AppleScript)
    script = f'''
    tell application "Preview"
        open POSIX file "{pdf_path}"
        delay 2
        tell document 1
            set pageCount to count of pages
            repeat with i from 1 to pageCount
                export pages i to POSIX file "{output_dir}/Revista-musical-hispano-americana-1-1914-n-o-1_pagina_" & (text -3 thru -1 of ("000" & i)) & ".jpg" as JPEG with resolution 300
            end repeat
        end tell
        close document 1
    end tell
    '''
    
    try:
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ Conversión completada usando Preview")
        else:
            print(f"Error en AppleScript: {result.stderr}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    convertir_pdf_con_sistema()