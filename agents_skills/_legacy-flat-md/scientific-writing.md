# scientific-writing

**Trigger**: Use when the user asks to draft, write, or complete a scientific manuscript, research article, technical report, or any structured scientific document following IMRAD or similar conventions. Covers full manuscripts, individual sections, abstracts, cover letters, and responses to reviewers.

---

## Pre-flight: Gather Context First

Before writing, confirm or infer:
1. **Target journal / venue**: Nature Methods? ACS Nano? PLOS ONE? Analytical Chemistry?
2. **Document type**: Full manuscript / Short communication / Review / Technical note
3. **Stage**: First draft / Revision / Response to reviewers
4. **Language**: English (→ `humanizer-juanjo`) / Spanish (→ `humanizer-juanjo-es`)
5. **Available material**: Abstract only? Data already in results? Full outline?

Use `AskUserQuestion` only if none of these can be inferred from context.

---

## IMRAD Structure (full manuscript)

### Title
- Informative, specific, ≤ 15 words
- Contains: system/method, what was done, key result or application
- No abbreviations except universally known ones (DNA, PCR, NMR)
- Avoid: "A study of...", "Investigation into...", "Novel..."

### Abstract (structured or unstructured)
Structured (Nature family, clinical journals):
- **Background** (1-2 sentences): what problem and why it matters
- **Methods** (2-3 sentences): what was done and key experimental design
- **Results** (2-3 sentences): top quantitative finding with n and p-values
- **Conclusions** (1-2 sentences): implication and generalizability

Unstructured: same content, no subheadings, ≤ 250 words.

### Introduction (3-4 paragraphs)
1. **Clinical/technological problem**: what is unmet and why it matters (cite reviews)
2. **State of the art**: what exists and why it falls short (cite specific papers)
3. **Gap statement**: the precise gap this work fills
4. **This work**: "Here we report..." — what was done, how, and key result. End with a 1-sentence preview of the main finding.

No: "In recent years...", "With the advent of...", "It is well known that..."

### Materials and Methods
- Past tense, passive or active (match journal style)
- Enough detail for reproduction: quantities, instruments (model + manufacturer), software (version + DOI or URL), statistical tests (with α level)
- Subsections: Materials | Synthesis/Preparation | Assay Protocol | Instrumentation | Data Analysis | Statistics
- Ethics statement if human/animal samples

### Results
- Present results in order of logic, not chronological order of experiments
- Every figure/table cited in text before appearing
- Each result paragraph: what was measured → what was found (with n, units, ± SD or CI, p-value) → what it means mechanistically
- No interpretation beyond the data in this section (save for Discussion)

### Discussion
- Open with the main finding restated in one sentence (not "In this study, we found that...")
- Compare to prior art: what agrees, what differs, why
- Mechanistic interpretation of key results
- Limitations: be honest, propose how to address
- Broad implications: who benefits, what does this enable
- Do NOT just list results again

### Conclusion
- 1-3 sentences max
- Restate the core advance and its significance
- No new information, no "future work" lists (put those in Discussion)

### References
- Format per target journal (DOI always)
- Cite primary sources, not reviews, for specific claims
- Limit self-citation to directly relevant prior work

---

## Chemistry & Biology Notation Standards

**NMR**: ¹H NMR (400 MHz, DMSO-d6): δ 7.52 (d, J = 8.2 Hz, 2H)
**MS**: HRMS (ESI): m/z calcd for C₁₂H₁₅N₂O [M+H]⁺ 203.1184, found 203.1181
**Units**: µM, nM, pM, mg mL⁻¹, mol L⁻¹, kDa, Da, nm, µm, Å, °C, min, h
**Statistics**: mean ± SD (n = X), Student's t-test, p < 0.05 (or exact p)
**Gene/protein**: *KRT10* gene (italic), KRT10 protein (regular)
**Sequences**: 5′-ATCGATCG-3′

Never LaTeX in prose. Never `$K_D$` → write KD.

---

## Specific Section Templates

### DCL / DestiNA / SMART Probe Papers
Key terms to use precisely:
- Dynamic Chemical Labeling (DCL) — capitalize as proper noun after first use
- SMART probe — always caps
- Aldehyde-tag recognition / amine-functionalized nucleotide
- miR-122 (not miRNA-122) — MIMAT0000422
- Limit of detection (LOD), not "detection limit" or "sensitivity" alone
- MALDI-TOF MS: matrix used, mass range, instrument model

### PNA / Biophysical Papers
- Peptide nucleic acid (PNA) — expand first use
- Tm (melting temperature, °C) — not T_m with subscript
- ΔTm — discrimination penalty
- KD (dissociation constant, nM) — not K_D
- Thermal denaturation: absorbance at 260 nm vs temperature

---

## Post-Draft: Mandatory Pipeline

After completing the draft, apply in order:
1. `no-ai-slop` — remove AI patterns
2. `humanizer-juanjo` (EN) or `humanizer-juanjo-es` (ES) — voice calibration
3. Check all numeric values match input data
4. Verify all citations are real (use WebSearch to confirm DOIs if needed)
5. Count words and flag if over journal limit
