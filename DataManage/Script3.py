import os
import pandas as pd

# Carpeta que contiene los archivos Excel
carpeta = 'rawData'  # Cámbialo si es otro directorio

# Extensiones válidas
extensiones = ('.xls', '.xlsx')

for nombre_archivo in os.listdir(carpeta):
    nombre_lower = nombre_archivo.lower()
    # Procesamos solo archivos .xls/.xlsx
    if nombre_lower.endswith(extensiones):
        ruta_antigua = os.path.join(carpeta, nombre_archivo)
        try:
            # Leemos la primera hoja, sin filas de cabecera para que B1 sea df.iloc[0,1]
            df = pd.read_excel(ruta_antigua, sheet_name=0, header=None, engine=None)
            valor_b1 = df.iloc[0, 1]  # fila 0, columna 1 -> celda B1
            # Nos aseguramos de que sea texto y no contenga saltos ni espacios extremos
            nuevo_nombre_base = str(valor_b1).strip()
            # Recuperamos la extensión original (incluye el punto)
            _, extension = os.path.splitext(nombre_archivo)
            # Construimos el nuevo nombre
            nuevo_nombre = f"{nuevo_nombre_base}{extension}"
            ruta_nueva = os.path.join(carpeta, nuevo_nombre)

            if not os.path.exists(ruta_nueva):
                os.rename(ruta_antigua, ruta_nueva)
                print(f"Renombrado: {nombre_archivo} → {nuevo_nombre}")
            else:
                print(f"Omitido (ya existe): {nuevo_nombre}")
        except Exception as e:
            print(f"Error al procesar '{nombre_archivo}': {e}")
