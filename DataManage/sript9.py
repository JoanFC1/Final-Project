import os
import glob
import pandas as pd

# ← AJUSTA esta ruta a la carpeta donde están tus CSV
input_folder = "processedData2"
# Carpeta donde se guardará el concatenado
output_folder = os.path.join(input_folder, "./final_data")
output_file = os.path.join(output_folder, "all_data.csv")

# 1) Asegurarse de que exista la carpeta destino
os.makedirs(output_folder, exist_ok=True)

# 2) Listar todos los CSV en la carpeta origen
csv_paths = glob.glob(os.path.join(input_folder, "*.csv"))

# 3) Leer y concatenar
dfs = []
for path in csv_paths:
    try:
        df = pd.read_csv(path)
        dfs.append(df)
        print(f"Leído: {os.path.basename(path)}  ({len(df)} filas)")
    except Exception as e:
        print(f"Error al leer {path}: {e}")

if not dfs:
    raise ValueError("No se encontró ningún CSV en la carpeta especificada.")

combined = pd.concat(dfs, ignore_index=True)
print(f"\nTotal concatenado: {combined.shape[0]} filas, {combined.shape[1]} columnas.")

# 4) Guardar resultado
combined.to_csv(output_file, index=False)
print(f"→ Guardado el concatenado en: {output_file}")
