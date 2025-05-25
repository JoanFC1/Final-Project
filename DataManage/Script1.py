import pandas as pd
import os

# Carpeta amb tots els fitxers .xls
carpeta = 'rawData'
sortida = 'resum_final'
os.makedirs(sortida, exist_ok=True)

# Camps a extreure
camps_objetiu = [
    # Balance de situación
    'Inmovilizado', 'Inmovilizado inmaterial', 'Inmovilizado material', 'Otros activos fijos',
    'Activo circulante', 'Existencias', 'Deudores', 'Otros activos líquidos', 'Tesorería',
    'Total activo', 'Fondos propios', 'Capital suscrito', 'Otros fondos propios',
    'Pasivo fijo', 'Acreedores a L. P.', 'Otros pasivos fijos', 'Provisiones',
    'Pasivo líquido', 'Deudas financieras', 'Acreedores comerciales', 'Otros pasivos líquidos',
    'Total pasivo y capital propio', 'Fondo de maniobra', 'Número empleados',
    # Pérdidas y ganancias
    'Ingresos de explotación', 'Importe neto Cifra de Ventas', 'Consumo de mercaderías y de materias',
    'Resultado bruto', 'Otros gastos de explotación', 'Resultado Explotación',
    'Ingresos financieros', 'Gastos financieros', 'Resultado financiero',
    'Result. ordinarios antes Impuestos', 'Impuestos sobre sociedades',
    'Resultado Actividades Ordinarias', 'Ingresos extraordinarios', 'Gastos extraordinarios',
    'Resultados actividades extraordinarias', 'Resultado del Ejercicio',
    'Materiales', 'Gastos de personal', 'Dotaciones para amortiz. de inmovil.',
    'Otros Conceptos de Explotación', 'Gastos financieros y gastos asimilados',
    'Cash flow', 'Valor agregado', 'EBIT', 'EBITDA'
]

# Recorre tots els arxius
for fitxer in os.listdir(carpeta):
    if fitxer.endswith('.xls'):
        ruta = os.path.join(carpeta, fitxer)
        print(f"📂 Processant: {fitxer}")

        try:
            df = pd.read_excel(ruta, header=None)

            fila_anys = df.iloc[10]
            columnes_anys = fila_anys.dropna().astype(str)
            columnes_utilitzables = columnes_anys[columnes_anys.str.contains(r"\d{2}/\d{2}/\d{4}")].index
            df_dades = df.iloc[14:, :]

            resultats = []
            for _, fila in df_dades.iterrows():
                camp = fila[1]
                if isinstance(camp, str) and camp.strip() in camps_objetiu:
                    for col in columnes_utilitzables:
                        any_complet = df.iloc[10, col]
                        any_net = any_complet.split()[0]  # treu EUR
                        valor = fila[col]
                        resultats.append({'Campo': camp.strip(), 'Año': any_net, 'Valor': valor})

            # Crear DataFrame i pivotar
            df_resultat = pd.DataFrame(resultats)
            df_resultat['Año'] = pd.to_datetime(df_resultat['Año'], format='%d/%m/%Y').dt.year
            df_pivot = df_resultat.pivot_table(index='Año', columns='Campo', values='Valor', aggfunc='first')

            # Reindexar per assegurar anys 2023 a 1900
            anys_complets = list(range(2023, 1899, -1))
            df_pivot = df_pivot.reindex(index=anys_complets)

            # Convertim l'índex a columna
            df_pivot.reset_index(inplace=True)
            df_pivot.rename(columns={'index': 'Año'}, inplace=True)

            # Guarda el CSV
            nom_sortida = os.path.splitext(fitxer)[0] + '_resum.csv'
            ruta_sortida = os.path.join(sortida, nom_sortida)
            df_pivot.to_csv(ruta_sortida, index=False, encoding='utf-8-sig')
            print(f"✅ Guardat: {ruta_sortida}")

        except Exception as e:
            print(f"❌ Error amb {fitxer}: {e}")
