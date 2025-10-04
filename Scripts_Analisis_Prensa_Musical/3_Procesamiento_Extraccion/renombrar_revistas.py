#!/usr/bin/env python3
import os
import re

directorio = "/Users/maria/Desktop/Revista Musical de Bilbao"

# Mapeo de archivos con sus nuevos nombres
renombrados = {
    "Revista-musical-Bilbao-1-1910-n-o-13.pdf": "1910_13_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-1-1912-n-o-1.pdf": "1912_01_Revista-Musical-Bilbao.pdf", 
    "Revista-musical-Bilbao-1-1913-n-o-1.pdf": "1913_01_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-10-1911-n-o-10.pdf": "1911_10_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-10-1912-n-o-10.pdf": "1912_10_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-10-1913-n-o-10.pdf": "1913_10_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-11-1911-n-o-11.pdf": "1911_11_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-11-1912-n-o-11.pdf": "1912_11_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-11-1913-n-o-11.pdf": "1913_11_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-12-1911-n-o-12.pdf": "1911_12_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-12-1912-n-o-12.pdf": "1912_12_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-12-1913-n-o-12.pdf": "1913_12_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-2-1909-n-o-2.pdf": "1909_02_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-2-1911-n-o-2.pdf": "1911_02_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-2-1912-n-o-2.pdf": "1912_02_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-2-1913-n-o-2.pdf": "1913_02_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-3-1911-n-o-3.pdf": "1911_03_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-3-1912-n-o-3.pdf": "1912_03_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-3-1913-n-o-3.pdf": "1913_03_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-4-1909-n-o-4.pdf": "1909_04_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-4-1911-n-o-4.pdf": "1911_04_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-4-1912-n-o-4.pdf": "1912_04_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-4-1913-n-o-4.pdf": "1913_04_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-5-1911-n-o-5.pdf": "1911_05_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-5-1912-n-o-5.pdf": "1912_05_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-5-1913-n-o-5.pdf": "1913_05_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-6-1911-n-o-6.pdf": "1911_06_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-6-1912-n-o-6.pdf": "1912_06_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-6-1913-n-o-6.pdf": "1913_06_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-7-1911-n-o-7.pdf": "1911_07_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-7-1912-n-o-7.pdf": "1912_07_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-7-8-1913-n-o-7.pdf": "1913_07-08_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-8-1911-n-o-8.pdf": "1911_08_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-8-1912-n-o-8.pdf": "1912_08_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-9-1911-n-o-9.pdf": "1911_09_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-9-1912-n-o-9.pdf": "1912_09_Revista-Musical-Bilbao.pdf",
    "Revista-musical-Bilbao-9-1913-n-o-9.pdf": "1913_09_Revista-Musical-Bilbao.pdf"
}

print("🔄 Iniciando renombrado de archivos...")
exitosos = 0
errores = 0

for nombre_actual, nombre_nuevo in renombrados.items():
    ruta_actual = os.path.join(directorio, nombre_actual)
    ruta_nueva = os.path.join(directorio, nombre_nuevo)
    
    if os.path.exists(ruta_actual):
        try:
            os.rename(ruta_actual, ruta_nueva)
            print(f"✅ {nombre_actual} → {nombre_nuevo}")
            exitosos += 1
        except Exception as e:
            print(f"❌ Error: {nombre_actual} - {e}")
            errores += 1
    else:
        print(f"⚠️  No encontrado: {nombre_actual}")

print(f"\n📊 Resumen: {exitosos} archivos renombrados, {errores} errores")