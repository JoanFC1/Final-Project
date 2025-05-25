import os
import pandas as pd

# Carpeta d’entrada i carpeta de sortida
carpeta_entrada = 'resum_final'           # On tens els CSV originals
carpeta_sortida = 'processedData'     # Carpeta nova on guardarem els CSV modificats

# Creem la carpeta de sortida si no existeix
os.makedirs(carpeta_sortida, exist_ok=True)

# Recorrem tots els fitxers .csv de la carpeta d’entrada
for nom_fitxer in os.listdir(carpeta_entrada):
    if nom_fitxer.lower().endswith('.csv'):
        ruta_entrada = os.path.join(carpeta_entrada, nom_fitxer)
        ruta_sortida = os.path.join(carpeta_sortida, nom_fitxer)
        try:
            # Llegim el CSV
            df = pd.read_csv(ruta_entrada)
            
            # Obtenim el nom base sense extensió
            base_nom = os.path.splitext(nom_fitxer)[0]
            # Afegim la columna amb el nom del fitxer sense ".csv"
            df['Empresa'] = base_nom
            
            # Guardem el nou CSV a la carpeta de sortida
            df.to_csv(ruta_sortida, index=False)
            
            print(f"Procesat: \"{nom_fitxer}\" → guardat a \"{carpeta_sortida}\" amb Fitxer=\"{base_nom}\"")
        except Exception as e:
            print(f"Error amb \"{nom_fitxer}\": {e}")
