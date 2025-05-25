import os
import pandas as pd

# Carpeta que conté els CSV
carpeta = 'resum_final'  # Canvia-ho pel teu directori

# Recorrem tots els fitxers de la carpeta
for nom_fitxer in os.listdir(carpeta):
    if nom_fitxer.lower().endswith('.csv'):
        ruta = os.path.join(carpeta, nom_fitxer)
        try:
            # Llegim el CSV
            df = pd.read_csv(ruta)
            
            # Ens assegurem que 'Año' sigui numèrica (converteix a NaN els no numèrics)
            df['Año'] = pd.to_numeric(df['Año'], errors='coerce')
            
            # Filtrar: mantenim només els anys > 1998
            df_filtrat = df[df['Año'] > 1998].copy()
            
            # Guardem (sobre-escrivim) el CSV netejat
            df_filtrat.to_csv(ruta, index=False)
            
            n_orig = len(df)
            n_keep = len(df_filtrat)
            print(f"{nom_fitxer}: {n_orig - n_keep} files eliminades, queden {n_keep} files.")
        
        except Exception as e:
            print(f"Error processant {nom_fitxer}: {e}")
