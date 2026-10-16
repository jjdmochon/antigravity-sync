# RFdiffusion3 Theozyme Configurations & Case Studies

This reference compiles experimental parameters and theozyme geometries from Butcher et al. (*Science*, 2026).

---

## 1. Phosphotriesterase Campaign (ZAPP-1 to ZAPP-5)

### Target Reaction
Hydrolysis of paraoxon (organophosphate ester) generating diethyl hydrogen phosphate and 4-nitrophenol (monitored at 405 nm).

### Theozyme Composition (6 Catalytic Residues + 2 Metal Ions)
- **Metals**: 2 × Zn(II) cofactors bridging the active center.
- **Bridging PTM**: 1 × Lysine carbamylate (Lys-CO2 / KCX). Reversibly assembled via CO2 equilibrium, driven by NaHCO3 supplementation.
- **Coordinating Residues**: 4 × Histidines (sampled across diverse tautomers and coordination modes).
- **General Base**: Sampled as Asp or Glu.
- **Nucleophile**: Coordinated hydroxide attacking the phosphorus atom in an SN2-like transition state.

### Conditioning Directives
- **RASA**: Buried hydrophobic ethyl groups of paraoxon; solvent-exposed nitrophenol leaving group.
- **Topology**: Helical bundle with active-site loop lid.
- **Kinetics**:
  - ZAPP-1: kcat = 0.015 s−1, kcat/KM = 2.0 M−1 s−1.
  - ZAPP-2: kcat = 0.023 s−1, kcat/KM = 4 M−1 s−1 (rate enhancement kcat/kuncat = (5 ± 2) × 10^5).

---

## 2. Amyloid Fibril-Cleaving Metalloprotease (TTRg11)

### Target Epitope
Human transthyretin (TTR, UniProt P02766) amyloid core longest β-strand:
`PAINVAVHVF` (cleavage directed between positions P1 and P1′: `PAINVA / VHVF`).

### Theozyme Composition
- **Active Center**: Catalytic Zn(II) ion with Astacin/Aminopeptidase N geometry (PDB 4QHP).
- **Consensus Motif**: `HEXXH + E` coordination shell.
- **Substrate Backbone**: P1 and P1′ fixed coordinates embedded into the diffusion cloud, allowing RFD3 to shape the S1-S4 specificity pockets dynamically.

### Experimental Screening Strategy
- **Cis Screen**: Protease fused to substrate peptide followed by mScarlet. 56 out of 96 designs exhibited >10% cleavage after 18 hours at 37 °C.
- **Trans Assay**: sfGFP-PAINVAVHVF-mScarlet FRET reporter construct.
- **Kinetics of TTRg11**: kcat = 0.072 s−1, KM = 70 μM, kcat/KM = 1100 M−1 s−1. Highly selective over alternative amyloidogenic sequences (Tau, α-synuclein, TDP-43, SAA).

---

## 3. Ribonucleoprotein Hybrid Catalyst (RNase P)

### Active Site Scaffolding
- **Input Constraints**: 4 catalytic ribonucleotides (PDB 3Q1Q chain A 49-52), 1 supporting ribonucleotide (A321), and 3 supporting protein residues (chain B 56-58).
- **Substrate Coordinates**: 12 RNA substrate residues kept as fixed atom context.
- **Generation Output**: RNA chain sampled between 50-80 nt and protein chain sampled between 100-120 aa. Motif scaffolding RMSD = 0.36 Å.
