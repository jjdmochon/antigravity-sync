#!/usr/bin/env python3
"""
render_glyph.py — Utilidad para renderizado de glifos químicos y moleculares (RDKit)
Parte de la skill 'glyph' para el workspace QFDOS (2026/2027).
"""

import os
import sys
import argparse
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

UNICODE_REPLACEMENTS = [
    (r"\Delta G^\circ", "ΔG°"),
    (r"\Delta G", "ΔG"),
    (r"\Delta H", "ΔH"),
    (r"\Delta S", "ΔS"),
    (r"\pm", "±"),
    (r"\approx", "≈"),
    (r"\mu M", "µM"),
    (r"uM", "µM"),
    (r"\AA", "Å"),
    (r"Angstrom", "Å"),
    (r"K_D", "KD"),
    (r"K_a", "Ka"),
    (r"K_b", "Kb"),
    (r"^1H", "¹H"),
    (r"^13C", "¹³C"),
    (r"[M+H]+", "[M+H]⁺"),
    (r"[M-H]-", "[M-H]⁻"),
]

def clean_unicode(text: str) -> str:
    res = text
    for old, new in UNICODE_REPLACEMENTS:
        res = res.replace(old, new)
    return res

def render_structure(smiles: str, output_path: str, name: str = "", width: int = 500, height: int = 400):
    mol = Chem.MolFromSmiles(smiles)
    if not mol:
        print(f"Error: SMILES no válido '{smiles}'", file=sys.stderr)
        sys.exit(1)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    ext = os.path.splitext(output_path)[1].lower()
    
    if ext == ".svg":
        drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
        opts = drawer.drawOptions()
        opts.clearBackground = True
        opts.bondLineWidth = 2.2
        opts.padding = 0.08
        rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol, legend=name)
        drawer.FinishDrawing()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(drawer.GetDrawingText())
    else:
        # Default to PNG
        img = Draw.MolToImage(mol, size=(width, height), legend=name)
        img.save(output_path)
    
    print(f"✓ Glifo químico generado exitosamente en: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Renderizador de Glifos Moleculares y Tipografía Química")
    parser.add_argument("--smiles", "-s", type=str, help="Cadena SMILES de la molécula")
    parser.add_argument("--out", "-o", type=str, default="glyph_molecule.svg", help="Ruta del archivo de salida (.svg o .png)")
    parser.add_argument("--name", "-n", type=str, default="", help="Nombre o leyenda de la molécula")
    parser.add_argument("--clean-text", "-t", type=str, help="Cadena de texto con LaTeX a convertir en glifos Unicode")
    parser.add_argument("--width", type=int, default=500, help="Ancho de la imagen (px)")
    parser.add_argument("--height", type=int, default=400, help="Alto de la imagen (px)")

    args = parser.parse_args()

    if args.clean_text:
        print(clean_unicode(args.clean_text))
        return

    if args.smiles:
        render_structure(args.smiles, args.out, args.name, args.width, args.height)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
