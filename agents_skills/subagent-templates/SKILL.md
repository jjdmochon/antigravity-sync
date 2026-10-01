---
name: subagent-templates
description: >-
  Library of copy-paste parallel-subagent task patterns for common research/dev workflows
  (multi-omics dossiers, biomarker validation, PNA probe design, single-cell drug repurposing,
  UGR courseware, ISO audits, literature/patent surveys, builder+auditor loops, document
  provenance pipelines, AlphaGenome swarms, Albatross IRES analysis, BioNeMo NIM binder design).
  Mirrors SUBAGENTS_TEMPLATES_2026-10-01.md. Use when the
  user asks to "spawn subagents", "run this in parallel", or references one of these templates by
  name/number.
---

# Subagent Execution Templates

Mirrors `~/.gemini/SUBAGENTS_TEMPLATES_2026-10-01.md` (the full catalogue, 19 templates), adapted to Claude
Code's `Agent` tool. Where Gemini's prompt says "spawn subagents", issue multiple `Agent` tool
calls **in the same message** so they run in parallel, then synthesize the results yourself.

## How to use these templates
1. Fill in the bracketed placeholders.
2. Call `Agent` once per numbered subagent, all in one message block (parallel execution).
3. Consolidate the returned reports into the requested deliverable.
4. For domain lookups (ClinVar, gnomAD, AlphaFold, ChEMBL, PubChem, PubMed, etc.) prefer the
   connected MCP servers (PubMed, ChEMBL, Open Targets, Clinical Trials) or the matching skill over
   freehand web search. Most domain skills live in the library, not in the loaded core: write the
   path into the subagent prompt (`~/.agents/skill-library/<name>/SKILL.md`) or tell it to consult
   `skill-catalog`. A subagent never sees a library skill on its own.
5. Use the named subagents when they fit: `document-reviewer` (Jev-gated review),
   `albatross-expert` (Albatross / IRES), `juanjo-copilot` (persona + pipeline). Add
   `isolation: "worktree"` to any subagent that edits files.

---

## Template 1 — Multi-Omics Disease & Target Dossier
Target validation connecting clinical genetics, protein structure, and pharmacology.

```
Spawn 3 subagents in parallel for target [TARGET_GENE, e.g. KRT10 or EGFR]:
1. Genomics: pathogenic variants + population allele frequencies (ClinVar, gnomAD).
2. Structural Biology: AlphaFold model, pLDDT scores, ligand-binding pockets/interfaces.
3. Pharmacology: ChEMBL/PubChem small-molecule modulators, IC50/Ki, mechanism of action.
Consolidate into one Markdown target dossier.
```

## Template 2 — DCL Chemistry & miRNA Biomarker Validation
Validating a Dynamic Chemical Labeling assay for diagnostic microRNA detection.

```
Run the local DCL calibration analysis on data/, and in parallel spawn subagents to:
1. Biomarker Literature: PubMed search for clinical serum concentrations of [TARGET_miRNA] in
   [CONDITION, e.g. DILI] studies.
2. Sequence & Specificity: verify probe alignment against human miRNA isoforms (miRBase/NCBI) for
   zero off-target cross-hybridization.
Integrate clinical thresholds and specificity results into the final analytical chemistry report.
```

## Template 3 — PNA Probe Biophysics Campaign
Designing PNA/SMART probes to discriminate a specific point mutation.

```
Spawn 3 subagents in parallel to design a PNA targeting strategy for [MUTATION, e.g. KRT10 R156C]:
1. Thermodynamic Modeling: PNA:RNA / PNA:DNA duplex Tm and delta-Tm penalty for the mismatch.
2. Conformer Analysis: steric accessibility of the target sequence in transcript secondary
   structure (e3nn / PyG).
3. Prior Art: patented PNA modifications / oligonucleotide probes for this gene family.
Compile a probe candidate ranking table with predicted Tm and discrimination ratios.
```

## Template 4 — Single-Cell Drug Repurposing (drug2cell + ChEMBL)

```
Process the single-cell AnnData (.h5ad) with Scanpy, and in parallel spawn subagents to:
1. Drug Repurposing: run drug2cell (d2c.score / d2c.gsea) mapping ChEMBL clinical-stage drug
   targets against the identified marker gene clusters.
2. Pathway Enrichment: BlitzGSEA across Reactome/KEGG for top upregulated genes in the disease
   cluster.
Return an interactive UMAP colored by drug sensitivity score.
```

## Template 5 — Academic Courseware & Interactive Web Hub

```
For course [COURSE, e.g. Química Farmacéutica I - Tema 3], spawn 3 subagents in parallel:
1. Interactive Web App: standalone HTML5/CSS3 simulator for [TOPIC].
2. Self-Assessment Quiz: 10-question formative assessment with flashcard-style explanations.
3. Study Guide: key formulas/concepts extracted from the lecture draft.
Save all deliverables ready to embed into the course portal.
```

## Template 6 — ISO 9001 / ISO 13485 Compliance & Audit Checklist

```
Spawn 2 subagents in parallel for an ISO compliance readiness audit:
1. QMS Audit: validation protocols / risk-management docs against ISO 13485 clauses (IVD).
2. Metrics Dashboard: interactive HTML/JS dashboard tracking CAPA resolutions, checklist status,
   KPI metrics.
Provide a gap analysis table and prioritized action items.
```

## Template 7 — Multi-Database Literature & Patent Prior Art Survey

```
Spawn 3 subagents in parallel on [TOPIC]:
1. PubMed & EuropePMC: peer-reviewed studies (last 5 years) with DOI and key quantitative findings.
2. bioRxiv & arXiv: recent preprints, emerging methods, pre-publication benchmarks.
3. Patents: granted patents / published applications, key claims and assignees.
Synthesize into one executive literature matrix.
```

## Template 8 — Builder + Auditor Loop (adversarial verification)
High-stakes analysis/manuscript/validation work where an independent subagent stress-tests it.

```
Complete [BUILD_TASK]. Once built, spawn an independent Auditor subagent to:
1. Stress-test against edge cases (negative signals, zero concentrations, missing replicates,
   malformed input).
2. Validate mathematical/statistical rigor (LOD/LOQ, regression residuals, error propagation).
3. Check compliance against [STANDARDS, e.g. ISO 13485 / journal guidelines].
4. Output a signed audit_report.md with test coverage, edge cases tested, and certification.
Do not mark the task complete until the Auditor certifies a 100% pass rate.
```

Flow: Builder → initial output → spawn Auditor → adversarial audit suite → if findings, back to
Builder; if certified, produce `audit_report.md` + final deliverables.

## Template 9 — Document Production & Jev-Governed Review Pipeline
Publication-grade manuscripts/reports/courseware with a human voice, certified by Jev. Maps to
the pipeline in the [juanjo-copilot](../juanjo-copilot/SKILL.md) skill. Shortcut: delegate stages
0–4 to the `document-reviewer` subagent.

```
Draft [DOCUMENT] to disk. Then run the review pipeline via subagents:
0. Jev triage: py -3.13 "$HOME/.agents/skills/jev-system-one/scripts/jev_doc_gatekeeper.py" "<file>" --json
   Run only the stages in etapas_a_ejecutar.
1. Builder: draft the full text with exact data and structured formatting.
2. Provenance & Metadata: remove-ai-marks / watermarks-remover (invisible Unicode, container metadata).
3. Slop Purge & Voice: no-ai-slop, then the humanizer Jev selected (humanizer-juanjo or -es).
4. Certification: re-run the gatekeeper; sign-off requires quality_gate_passed == true.
If the engine reads "fallo-abierto (sin Jev)", run every stage and report the document as uncertified.
```

## Template 15 — AlphaGenome Variant Impact Swarm

```
Spawn 3 subagents in parallel for variant [chr:pos:ref>alt]:
1. AlphaGenome: read ~/.agents/skill-library/alphagenome-variant-impact-score and
   alphagenome-atlas-website-links; return AVI scores and Atlas links.
2. Clinical & population: clinvar-database, dbsnp-database, gnomad-database (library).
3. Structure: alphafold-database-fetch-and-analyze (library); residue pLDDT and local context.
Compile reports/variants/[VARIANT_ID].md.
```

## Template 18 — Albatross IRES & RNA Conformation Analysis

```
Delegate to the albatross-expert subagent: read ~/.agents/skill-library/albatross-rna-paper and
answer [QUESTION about an IRES / sequence / DMS-MaPseq result], citing figure and table numbers.
```

## Template 19 — BioNeMo NIM Protein Binder Design

```
Run subagents in order (each step feeds the next) for target [PDB / chain / hotspot]:
1. Structure: openfold3-nim or pdb-database. 2. Backbones: rfdiffusion-nim.
3. Sequences: proteinmpnn-nim. 4. Validation: boltz2-nim co-folding, rank by interface confidence.
Each reads its SKILL.md from ~/.agents/skill-library. Write reports/binders/[TARGET]_candidates.md.
```

Templates 10–14 and 16–17 (test remediation, telemetry, circuit breaker, interviewer, visual
studio, Aeneas/Ithaca, Magika) are in `~/.gemini/SUBAGENTS_TEMPLATES_2026-10-01.md`.

---

## General blueprint
```
Spawn subagents in parallel to:
1. Subagent 1 ([Role/Domain]): [query/action] -> return [format].
2. Subagent 2 ([Role/Domain]): [query/action] -> return [format].
3. Subagent 3 ([Role/Domain]): [query/action] -> return [format].
Consolidate results into [final deliverable].
```
