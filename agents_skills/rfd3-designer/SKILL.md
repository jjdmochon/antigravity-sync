---
name: rfd3-designer
description: De novo all-atom biopolymer design, unindexed catalytic motif scaffolding, metalloenzyme engineering, protease design, and RNA codesign using RFdiffusion3, RosettaCommons Foundry, and LigandMPNN.
---

# RFdiffusion3 Biopolymer & De Novo Enzyme Designer

This skill operationalizes **RFdiffusion3 (RFD3)** (Butcher et al., *Science* 2026) for de novo biomolecular design across proteins, nucleic acids, and hybrid ribonucleoprotein assemblies.

## When to Use This Skill
Activate this skill when:
- Designing de novo enzymes (hydrolases, proteases, transferases) from quantum-chemical or transition-state theozymes.
- Scaffolding complex atomic functional motifs without specifying backbone sequence indices.
- Generating binders or biocatalysts with metal cofactors (Zn2+, Mg2+, Fe2+/3+), non-protein cofactors, or post-translational modifications (e.g. carbamylated lysine).
- Reprogramming protease substrate specificity against pathological peptide epitopes (amyloid fibrils, viral cleavage sites, neoepitopes).
- Designing folded structural RNA, small-molecule RNA aptamers, or hybrid protein-RNA catalytic complexes.

## Theoretical Foundations & Architectural Paradigm

### 1. Free-Atom All-Atom Diffusion
- **Native Atom Granularity**: Rather than operating on Cα or rigid residue frames, RFD3 diffuses all 14 protein atoms (4 backbone + 10 sidechain, padded with virtual atoms on Cβ for smaller canonical residues) and up to 23 atoms for nucleic acid/protein mixtures (12 backbone for RNA / 11 for DNA, plus up to 11 base atoms).
- **Unindexed Scaffolding**: Catalytic residues are provided as coordinate-fixed atomic tokens within the initial noise cloud. The network places and denoises the backbone around them, discovering sequence positions and rotamers jointly.
- **Compute Efficiency**: Features a condensed 2-layer Pairformer (168M parameters vs. 350M in AF3) without triangle updates, yielding inference speeds over an order of magnitude faster than RFD1/RFD2.

### 2. Conditioning Primitives
- **RASA (Relative Atomic Solvent Accessibility)**: Specifies buried hydrophobic contacts vs. solvent-exposed active-site clefts.
- **Hydrogen Bonding Status**: Directs donor and acceptor satisfaction for ligands and catalytic residues.
- **Point-Group Symmetry**: Enforces multimeric symmetries (C2, C3, etc.) during diffusion for oligomeric enzymes.
- **Token-Level Base Pairing**: Constrains paired and unpaired regions for RNA folding.
- **Classifier-Free Guidance (CFG)**: Amplifies adherence to secondary structure and active-site constraints.

---

## Standard End-to-End Design Workflow

```
[Reaction Mechanism / Transition State]
               │
               ▼
   1. Theozyme Construction (DFT / MACE / PDB)
   - Minimal catalytic atoms (His, Asp/Glu, Lys-CO2, Zn2+)
   - Substrate backbone & scissile bond coordinates
   - RASA burial masks
               │
               ▼
   2. All-Atom Backbone & Cavity Generation (RFD3 via Foundry)
   - Input: unindexed_motif.json + ligand.sdf
   - Step scale / temperature sampling
   - Anti-loop flags & length bounds (e.g. 100-160 residues)
               │
               ▼
   3. Sequence Optimization (LigandMPNN / ProteinMPNN)
   - Core hydrophobic packing
   - Sub-pocket complementarity (S1-S4)
   - 8-16 sequences per backbone
               │
               ▼
   4. Orthogonal Cross-Validation (AlphaFold3 / Chai-1 / RF3)
   - Motif all-atom RMSD < 1.25 Å
   - Cα RMSD < 1.0 Å
   - Dunbrack rotamer loss < 1.0
   - Ligand / substrate RMSD < 2.0 Å
               │
               ▼
   5. Hit Selection & Experimental Synthesis
   - Rank top 96-192 designs for zero-shot wet-lab screening
```

---

## Design Protocols

### Protocol A: De Novo Metalloenzyme & Hydrolase Design (e.g. Phosphotriesterases)
1. **Transition-State Modeling**: Define nucleophilic attack geometry (e.g. hydroxide attack on organophosphate ester) using quantum mechanics or machine-learning force fields (MACE).
2. **Cofactor Coordination**: Specify metal atoms (e.g. binuclear Zn2+ center) and coordinating residues (His, Asp, carbamylated Lys).
3. **RASA Conditioning**: Set high burial for hydrophobic substrate moieties and solvent exposure for the leaving group.
4. **Post-Purification Assembly**: If carbamylated lysine is used, express with Strep-tag II, supplement with ZnSO4, and add NaHCO3 to drive CO2 equilibrium toward carbamylation.

### Protocol B: Targeted Protease Design for Amyloid Epitopes (e.g. TTRg11)
1. **Epitope Selection**: Select the amyloid-forming beta-strand core (e.g. PAINVAVHVF from TTR, PDB 8GBR).
2. **Theozyme Configuration**: Merge catalytic zinc coordination (His3-Glu from astacin/aminopeptidase N) with substrate backbone atoms at P1 and P1′.
3. **Cavity Sculpting**: Use RFD3 to simultaneously scaffold catalytic residues, determine substrate curvature, and build a binding cleft accommodating flanking residues.
4. **Validation Screening**: Screen in cis by fusing the protease to substrate-mScarlet, then characterize top hits in trans using sfGFP-peptide-mScarlet FRET assays.

### Protocol C: Structural RNA & Ribonucleoprotein Scaffolding
1. **Secondary Structure Conditioning**: Provide dot-bracket notation (paired/unpaired base tokens).
2. **Non-Canonical Pairs**: Allow RFD3 to sample Leontis-Westhof non-canonical geometries.
3. **Aptamer / Hybrid Scaffolding**: For RNA-protein active sites (e.g. RNase P), input both catalytic ribonucleotides and protein sidechain constraints in a unified track.

---

## Included Helper Scripts

The skill provides production utilities located in `scripts/`:

1. `theozyme_spec.py`: Builds and validates unindexed catalytic motif JSON specifications from PDB or coordinate files.
2. `rfd3_foundry_runner.py`: Formats configuration parameters and generates execution manifests for RosettaCommons Foundry.
3. `filter_designs.py`: Analyzes AlphaFold3 / Chai-1 prediction CIF/PDB files, calculating motif RMSD and rotamer satisfaction.

## References & Companions
- Full paper and figures: consult the reading package in `~/.agents/skill-library/rfd3-paper/`.
- Interactive Claude Code subagent: `albatross-expert`-equivalent agent `rfd3-expert`.
- RosettaCommons Foundry: https://github.com/RosettaCommons/foundry
- Metallohydrolase Design: https://github.com/baker-laboratory/Metallohydrolase_Enzyme_Design
