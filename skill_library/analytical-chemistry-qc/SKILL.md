---
name: analytical-chemistry-qc
description: "Automated end-to-end processing and expert interpretation of raw 1H/13C NMR (Bruker/Varian FID, acqus) and LC-MS (Shimadzu .lcd OLE2, Waters/Thermo .raw, .mzML) datasets. Executes group delay removal, FFT, phase optimization (ph0/ph1), AsLS baseline correction, pseudo-Voigt multiplet deconvolution, exchangeable proton detection (D2O shake comparison), UV purity integration (MaxPlot), and MS adduct deconvolutions (ES+/ES-)."
---

# Analytical Chemistry & QC Autonomous Agent

This skill equips the assistant to act as an autonomous analytical chemist, emulating the multi-step NMR and LC-MS pipeline demonstrated in Claude Science (David Kamber, 2026).

## Core Workflows

### 1. ¹H / ¹³C NMR Raw FID Processing
- **Input**: Raw `fid` / `ser` binary + `acqus` / `procpar` acquisition metadata.
- **Pipeline**:
  1. DSP digital filter removal (Group Delay compensation from `GRPDLY`).
  2. Apodization windowing (exponential $LB \approx 0.3\text{ Hz}$) & zero filling ($2\times\text{ TD}$).
  3. Fast Fourier Transform (FFT).
  4. Automatic phase optimization ($\text{ph}_0, \text{ph}_1$) minimizing negative dispersion area.
  5. Asymmetric Least Squares (AsLS) / PLS baseline flattening ($\sigma < 0.15$ on blank regions).
  6. Chemical shift referencing ($\text{DMSO-d}_5$ at $2.500\text{ ppm}$, $\text{CDCl}_3$ at $7.260\text{ ppm}$).
  7. Pseudo-Voigt line fitting, coupling constant $J\text{ (Hz)}$ calculation, multiplet classification.
  8. Identification of broad exchangeable singlets ($\Delta \nu_{1/2} > 12\text{ Hz}$, $-\text{NH}/-\text{OH}$).
  9. Differential analysis against $\text{D}_2\text{O}$ exchange FID (cleared regions & uncovered multiplets).

### 2. LC-MS Raw Binary Processing & Purity Deconvolution
- **Input**: Vendor binaries (`.lcd` OLE2, `.raw`, `.d`) or open standards (`.mzML`, `.cdf`).
- **Pipeline**:
  1. Binary stream parsing (MS scans & PDA 3D matrix).
  2. UV Chromatogram generation (MaxPlot, $214\text{ nm}, 254\text{ nm}, 280\text{ nm}$).
  3. Chromatographic integration & UV area purity calculation ($\%\text{ Area}$).
  4. MS spectrum extraction across chromatographic peaks.
  5. Adduct assignment in $\text{ES}^+$ ($[M+H]^+$, $[M+\text{Na}]^+$, $[2M+H]^+$) and $\text{ES}^-$ ($[M-H]^-$, $[M+\text{AcO}]^-$).
  6. Instrumental plumbing delay calibration ($\Delta t \approx 2\text{--}3\text{ s}$ from UV cell to MS ion source).

### 3. Reporting & Visual Inspection
- Multi-panel publication-grade figures (NMR with integrals + LC-MS UV/TIC + Mass Spectra).
- Exact quantitative report tables with verification metrics.
