import os
import glob
import pandas as pd
import numpy as np

# ← AJUSTA estas rutas/nombre antes de lanzar
folder = "processedData"      # carpeta con .csv
output_folder = "processedData2"
date_column = "Año"           # e.g. "Año", "Fecha"; o None si no hay columna temporal

os.makedirs(output_folder, exist_ok=True)

for filepath in glob.glob(os.path.join(folder, "*.csv")):
    # 1) Carga y normaliza missings
    df = pd.read_csv(filepath)
    df.replace("n.d.", np.nan, inplace=True)

    # 2) Conversión correcta del año a datetime
    if date_column and date_column in df.columns:
        df[date_column] = df[date_column].astype(str)
        df[date_column] = pd.to_datetime(
            df[date_column],
            format="%Y",
            errors="coerce"
        )
        df.sort_values(by=date_column, inplace=True)
        df.set_index(date_column, inplace=True)

    # 3) Imputación por columna, ignorando "Empresa"
    for col in df.columns:
        if col == "Empresa":
            # la dejamos tal cual, no convertimos ni interpolamos
            continue

        # Convertimos a numérico (cualquier no-numérico a NaN)
        df[col] = pd.to_numeric(df[col], errors="coerce")
        miss_ratio = df[col].isna().mean()

        if miss_ratio > 0.5:
            df[col].fillna(0, inplace=True)
        else:
            df[col].interpolate(method="linear", inplace=True, limit_direction="both")
            df[col].fillna(0, inplace=True)

    # 4) Si habíamos puesto el índice, lo devolvemos a columna
    if date_column and date_column in df.index.names:
        df.reset_index(inplace=True)

    # 5) Guarda el CSV procesado
    fname = os.path.basename(filepath)
    out_path = os.path.join(output_folder, fname)
    df.to_csv(out_path, index=False)
    print(f"→ Procesado: {fname}  →  {out_path}")
