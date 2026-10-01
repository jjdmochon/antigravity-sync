#!/usr/bin/env python3
"""
run_eulerna_enhancer_scan.py - Escaneo de loci reguladores de Eulerna
Requiere autenticación válida de AlphaGenome (ALPHAGENOME_API_KEY).
"""

import os
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Eulerna Enhancer / eRNA Locus Scanner")
    parser.add_argument("locus", help="Coordenadas genómicas chr:start-end (ej: chr6:31230000-31232000)")
    parser.add_argument("--gene", required=True, help="Gen diana regulado (ej: RORC, PAM, TNF)")
    parser.add_argument("--cell-type", default="synovial_fibroblast", help="Tipo celular de Eulerna")
    args = parser.parse_args()

    api_key = os.getenv("ALPHAGENOME_API_KEY")
    if not api_key:
        print("[BLOQUEO DE SEGURIDAD] ALPHAGENOME_API_KEY no detectada.")
        print("Para evitar datos sintéticos o simulados, no se genera ninguna predicción hasta contar con la clave oficial de Google DeepMind.")
        print(f"Puedes consultar el locus directamente en el Atlas web: https://alphagenome.deepmind.google/")
        sys.exit(1)

    print(f"Conectando con AlphaGenome API para escanear {args.locus}...")

if __name__ == "__main__":
    main()
