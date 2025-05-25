#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path

def eliminar_empreses_sense_dades():
    """
    Recorre la carpeta 'resum_final' i elimina tots els arxius .csv
    que, per a qualsevol any de 2000 a 2023, tinguin la fila buida
    (totes les columnes, excepte 'Año', són NaN o 'n.d.').
    """
    carpeta = Path("resum_final")
    if not carpeta.is_dir():
        print(f"Error: {carpeta!r} no és una carpeta vàlida.")
        return

    required_years = list(range(2000, 2024))
    eliminats = []

    for fitxer in carpeta.glob("*.csv"):
        try:
            # Tractem 'n.d.' i cadenes buides com NaN
            df = pd.read_csv(fitxer, na_values=['n.d.', ''], keep_default_na=True)
        except Exception as e:
            print(f"No s'ha pogut llegir {fitxer.name}: {e}")
            continue

        if 'Año' not in df.columns:
            print(f"{fitxer.name} no té la columna 'Año', es manté.")
            continue

        # Assegurem que 'Año' sigui numèrica
        df['Año'] = pd.to_numeric(df['Año'], errors='coerce')

        faltants = []
        for anyo in required_years:
            fila = df[df['Año'] == anyo]
            # si no existeix la fila o bé totes les dades són NaN → marca com a faltant
            if fila.empty or fila.drop(columns=['Año']).iloc[0].isna().all():
                faltants.append(anyo)

        if faltants:
            try:
                fitxer.unlink()
                eliminats.append((fitxer.name, faltants))
                print(f"Eliminat {fitxer.name}: falten dades pels anys {faltants}")
            except Exception as e:
                print(f"No s'ha pogut eliminar {fitxer.name}: {e}")

    if eliminats:
        print("\nResum d'eliminacions:")
        for nom, anys in eliminats:
            print(f" - {nom}: anys sense dades → {anys}")
    else:
        print("Tots els fitxers tenen alguna dada per a cada any de 2000 a 2023.")

if __name__ == "__main__":
    eliminar_empreses_sense_dades()
