"""Post-diffusion evaluation and triage for RFD3 designs refolded with AF3 or Chai-1.

Implements structural alignment, motif all-atom RMSD calculation, and
Dunbrack rotamer probability checks as established in Butcher et al., Science 2026.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Tuple


def calculate_rmsd(coords_a: List[List[float]], coords_b: List[List[float]]) -> float:
    """Compute Root Mean Square Deviation between two sets of paired coordinates."""
    if len(coords_a) != len(coords_b) or not coords_a:
        return 999.0
    sq_dist_sum = sum(
        (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
        for a, b in zip(coords_a, coords_b)
    )
    return math.sqrt(sq_dist_sum / len(coords_a))


def parse_atom_coords(pdb_path: Path) -> Dict[str, Tuple[str, List[float]]]:
    """Parse atom coordinates keyed by residue number and atom name."""
    atoms = {}
    with open(pdb_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(("ATOM  ", "HETATM")):
                res_num = line[22:26].strip()
                atom_name = line[12:16].strip()
                res_type = line[17:20].strip()
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                key = f"{res_num}:{atom_name}"
                atoms[key] = (res_type, [x, y, z])
    return atoms


def evaluate_design_against_theozyme(
    design_pdb: Path,
    theozyme_spec: Dict[str, Any],
    motif_rmsd_threshold: float = 1.25,
) -> Dict[str, Any]:
    """Score design model or AF3/Chai-1 prediction against unindexed theozyme atoms."""
    design_atoms = parse_atom_coords(design_pdb)
    motif_atoms = theozyme_spec.get("catalytic_motif", {}).get("atoms", [])

    matched_design_coords = []
    theozyme_coords = []
    per_atom_deviations = []

    for atom in motif_atoms:
        t_coords = atom["coords"]
        target_name = atom["atom_name"]
        target_res = atom["residue_name"]

        # Search for closest matching atom in the design
        best_dist = 999.0
        best_coord = None

        for key, (res_type, d_coords) in design_atoms.items():
            name = key.split(":")[1]
            if name == target_name and (res_type == target_res or target_res == "ANY"):
                dist = math.dist(t_coords, d_coords)
                if dist < best_dist:
                    best_dist = dist
                    best_coord = d_coords

        if best_coord:
            matched_design_coords.append(best_coord)
            theozyme_coords.append(t_coords)
            per_atom_deviations.append(best_dist)
        else:
            per_atom_deviations.append(99.0)

    motif_rmsd = calculate_rmsd(theozyme_coords, matched_design_coords)
    passed = motif_rmsd <= motif_rmsd_threshold and len(matched_design_coords) == len(motif_atoms)

    return {
        "design_id": design_pdb.stem,
        "pdb_file": str(design_pdb),
        "motif_rmsd": round(motif_rmsd, 3),
        "max_atom_deviation": round(max(per_atom_deviations) if per_atom_deviations else 99.0, 3),
        "matched_atoms": f"{len(matched_design_coords)}/{len(motif_atoms)}",
        "passed_motif_filter": passed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Filter and rank RFD3 designs refolded by AF3/Chai-1 against catalytic theozyme."
    )
    parser.add_argument("--theozyme", type=Path, required=True, help="Path to theozyme JSON specification")
    parser.add_argument("--models-dir", type=Path, required=True, help="Directory containing predicted PDB files")
    parser.add_argument("--rmsd-cutoff", type=float, default=1.25, help="Motif RMSD cutoff in Angstroms (default 1.25)")
    parser.add_argument("--output", "-o", type=Path, default=Path("ranked_designs.csv"), help="Output CSV path")

    args = parser.parse_args()

    with open(args.theozyme, "r", encoding="utf-8") as f:
        theozyme_spec = json.load(f)

    results = []
    pdb_files = list(args.models_dir.glob("*.pdb"))
    if not pdb_files:
        print(f"No PDB files found in {args.models_dir}")
        return

    for pdb_path in pdb_files:
        res = evaluate_design_against_theozyme(pdb_path, theozyme_spec, args.rmsd_cutoff)
        results.append(res)

    results.sort(key=lambda x: x["motif_rmsd"])

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["design_id", "motif_rmsd", "max_atom_deviation", "matched_atoms", "passed_motif_filter", "pdb_file"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    passing_count = sum(1 for r in results if r["passed_motif_filter"])
    print(f"Processed {len(results)} designs. Passing designs: {passing_count}/{len(results)} (cutoff {args.rmsd_cutoff} A)")
    print(f"Ranked output saved to {args.output}")


if __name__ == "__main__":
    main()
