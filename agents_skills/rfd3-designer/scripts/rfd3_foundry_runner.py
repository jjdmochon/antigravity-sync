"""Foundry / RFdiffusion3 execution wrapper and manifest generator.

Prepares Foundry-compatible run configurations for RFD3 diffusion campaigns
supporting unindexed motif scaffolding, symmetry, and RASA conditioning.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


def generate_foundry_config(
    theozyme_spec_path: Path,
    output_dir: Path,
    num_designs: int = 100,
    diffusion_steps: int = 100,
    step_scale: float = 1.0,
    anti_loop_penalty: bool = True,
    cfg_scale: float = 2.0,
    symmetry: str = "C1",
) -> Dict[str, Any]:
    """Generate Foundry run configuration dict for RFD3."""
    config = {
        "model": "rfdiffusion3",
        "checkpoint": "rfd3_allatom_base",
        "inference": {
            "num_samples": num_designs,
            "steps": diffusion_steps,
            "step_scale": step_scale,
            "anti_loop_flag": anti_loop_penalty,
            "classifier_free_guidance_scale": cfg_scale,
            "symmetry_group": symmetry,
        },
        "conditioning": {
            "unindexed_theozyme_file": str(theozyme_spec_path.resolve()),
            "all_atom_mode": True,
        },
        "output": {
            "destination": str(output_dir.resolve()),
            "save_trajectories": False,
            "export_formats": ["cif", "pdb"],
        },
    }
    return config


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Foundry configuration and runner script for RFdiffusion3."
    )
    parser.add_argument("--theozyme", type=Path, required=True, help="Path to theozyme JSON specification")
    parser.add_argument("--outdir", "-o", type=Path, default=Path("rfd3_outputs"), help="Target output directory")
    parser.add_argument("--num-designs", "-n", type=int, default=96, help="Number of designs to generate (default 96)")
    parser.add_argument("--steps", type=int, default=100, help="Number of diffusion denoising steps (default 100)")
    parser.add_argument("--step-scale", type=float, default=1.0, help="Step scale for sampling temperature (default 1.0)")
    parser.add_argument("--cfg-scale", type=float, default=2.0, help="Classifier-Free Guidance scale (default 2.0)")
    parser.add_argument("--symmetry", default="C1", choices=["C1", "C2", "C3", "D2"], help="Point group symmetry")
    parser.add_argument("--anti-loop", action="store_true", default=True, help="Enable anti-loop penalty")

    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    config = generate_foundry_config(
        theozyme_spec_path=args.theozyme,
        output_dir=args.outdir,
        num_designs=args.num_designs,
        diffusion_steps=args.steps,
        step_scale=args.step_scale,
        anti_loop_penalty=args.anti_loop,
        cfg_scale=args.cfg_scale,
        symmetry=args.symmetry,
    )

    config_path = args.outdir / "foundry_rfd3_config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    # Shell script generator
    sh_path = args.outdir / "run_foundry_rfd3.ps1"
    powershell_cmd = f"""# Foundry RFdiffusion3 Execution Script
# Ensure Foundry virtualenv is activated: conda activate foundry OR uv run foundry
Write-Host "Launching Foundry RFD3 campaign: {args.theozyme.stem} ({args.num_designs} designs)..."
foundry run --config "{config_path.resolve()}"
Write-Host "RFD3 generation complete. Outputs saved in {args.outdir.resolve()}"
"""
    with open(sh_path, "w", encoding="utf-8") as f:
        f.write(powershell_cmd)

    print(f"Generated Foundry config: {config_path}")
    print(f"Generated PowerShell launcher: {sh_path}")


if __name__ == "__main__":
    main()
