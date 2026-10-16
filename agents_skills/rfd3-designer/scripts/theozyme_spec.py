"""Theozyme specification and constraint generator for RFdiffusion3 / Foundry.

Generates unindexed catalytic motif and atomic constraint JSON definitions
as described in Butcher et al., Science 2026.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional


def create_theozyme_spec(
    name: str,
    catalytic_atoms: List[Dict[str, Any]],
    substrate_file: Optional[str] = None,
    symmetry: str = "C1",
    scaffold_length_range: tuple[int, int] = (100, 160),
    rasa_constraints: Optional[List[Dict[str, Any]]] = None,
    hb_constraints: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Build an unindexed theozyme specification for RFD3."""
    spec = {
        "theozyme_name": name,
        "format_version": "rfd3-atomworks-v1",
        "symmetry": symmetry,
        "scaffold_length": {
            "min": scaffold_length_range[0],
            "max": scaffold_length_range[1],
        },
        "catalytic_motif": {
            "unindexed": True,
            "atoms": catalytic_atoms,
        },
        "substrate": {
            "path": substrate_file if substrate_file else None,
            "fixed": True,
        },
        "atomic_conditioning": {
            "rasa": rasa_constraints or [],
            "hydrogen_bonds": hb_constraints or [],
        },
    }
    return spec


def parse_pdb_motif_atoms(
    pdb_path: Path, atom_selections: List[str]
) -> List[Dict[str, Any]]:
    """Extract coordinates of selected catalytic atoms from a PDB file.

    atom_selections format: 'CHAIN:RESNUM:ATOMNAME:RESTYPE',
    e.g. 'A:89:NE2:HIS' or 'A:200:ZN:ZN'
    """
    selected_atoms = []
    lookup = set(atom_selections)

    with open(pdb_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(("ATOM  ", "HETATM")):
                chain = line[21:22].strip()
                res_num = line[22:26].strip()
                atom_name = line[12:16].strip()
                res_type = line[17:20].strip()
                element = line[76:78].strip() or atom_name[0]

                key = f"{chain}:{res_num}:{atom_name}:{res_type}"
                loose_key = f"{chain}:{res_num}:{atom_name}"

                if key in lookup or loose_key in lookup:
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    selected_atoms.append(
                        {
                            "residue_name": res_type,
                            "atom_name": atom_name,
                            "element": element,
                            "coords": [x, y, z],
                            "role": "catalytic",
                        }
                    )
    return selected_atoms


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build RFD3 theozyme specification for unindexed motif scaffolding."
    )
    parser.add_argument("--name", required=True, help="Name of theozyme (e.g. ZAPP_phosphotriesterase)")
    parser.add_argument("--pdb", type=Path, help="Reference PDB containing catalytic coordinates")
    parser.add_argument(
        "--select",
        nargs="+",
        help="Atom selections: CHAIN:RESNUM:ATOM (e.g. A:57:NE2 A:102:OD1 A:195:OG A:300:ZN)",
    )
    parser.add_argument("--substrate", type=str, help="Path to substrate SDF/PDB file")
    parser.add_argument("--symmetry", default="C1", choices=["C1", "C2", "C3", "D2"], help="Point group symmetry")
    parser.add_argument("--min-len", type=int, default=110, help="Minimum scaffold length")
    parser.add_argument("--max-len", type=int, default=160, help="Maximum scaffold length")
    parser.add_argument("--output", "-o", type=Path, required=True, help="Output JSON spec path")

    args = parser.parse_args()

    catalytic_atoms = []
    if args.pdb and args.select:
        catalytic_atoms = parse_pdb_motif_atoms(args.pdb, args.select)
    elif not args.pdb:
        # Default placeholder demonstration theozyme
        catalytic_atoms = [
            {"residue_name": "HIS", "atom_name": "NE2", "element": "N", "coords": [0.0, 0.0, 0.0], "role": "coordination"},
            {"residue_name": "HIS", "atom_name": "NE2", "element": "N", "coords": [2.5, 1.2, 0.0], "role": "coordination"},
            {"residue_name": "GLU", "atom_name": "OE1", "element": "O", "coords": [1.2, -2.1, 0.5], "role": "general_base"},
            {"residue_name": "ZN", "atom_name": "ZN", "element": "ZN", "coords": [1.1, 0.2, 0.0], "role": "catalytic_metal"},
        ]

    spec = create_theozyme_spec(
        name=args.name,
        catalytic_atoms=catalytic_atoms,
        substrate_file=args.substrate,
        symmetry=args.symmetry,
        scaffold_length_range=(args.min_len, args.max_len),
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2)

    print(f"Generated RFD3 theozyme spec with {len(catalytic_atoms)} motif atoms: {args.output}")


if __name__ == "__main__":
    main()
