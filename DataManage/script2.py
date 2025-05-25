import pandas as pd

# Llegeix el CSV que ja tens
df = pd.read_csv("resultat_B17582495.csv")

# Convertim 'Año' a datetime per extreure només l'any com enter
df['Año'] = pd.to_datetime(df['Año'], format='%d/%m/%Y').dt.year

# Pivota el DataFrame: anys com índex, camps com columnes
df_pivot = df.pivot_table(index='Año', columns='Campo', values='Valor', aggfunc='first')

# Reindexa per incloure tots els anys des de 2023 fins a 1900
index_complet = list(range(2023, 1899, -1))
df_pivot = df_pivot.reindex(index=index_complet)

# Posa 'Año' com a columna (no com a índex)
df_pivot.reset_index(inplace=True)
df_pivot.rename(columns={'index': 'Año'}, inplace=True)

# Guarda resultat
df_pivot.to_csv("resultat_pivotat_B17582495.csv", index=False, encoding="utf-8-sig")
print("✅ Fitxer final creat: resultat_pivotat_B17582495.csv")
