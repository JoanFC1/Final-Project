#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

def eliminar_csv_liquidacion_o_extinguidos():
    """
    Recorre la carpeta 'resum_final' y elimina todos los archivos .csv
    cuyo nombre contenga "(EN LIQUIDACION)" o "(EXTINGUIDA)".
    """
    carpeta = Path("resum_final")
    if not carpeta.is_dir():
        print(f"Error: {carpeta!r} no és una carpeta vàlida.")
        return

    patrones = ["(EN LIQUIDACION)", "(EXTINGUIDA)"]
    eliminados = []

    for archivo in carpeta.glob("*.csv"):
        nombre = archivo.name.upper()  # Comparació insensible a majúscules
        if any(p in nombre for p in patrones):
            try:
                archivo.unlink()
                eliminados.append(archivo.name)
            except Exception as e:
                print(f"No s'ha pogut eliminar {archivo.name}: {e}")

    if eliminados:
        print("Arxius eliminats:")
        for nom in eliminados:
            print("  -", nom)
    else:
        print("No s'han trobat arxius per eliminar.")

if __name__ == "__main__":
    eliminar_csv_liquidacion_o_extinguidos()
