# Chemical Biology & Medicinal Chemistry Toolkit

**Updated:** 2026-10-01 · companion to [GLOBAL_AGENTS_AND_TOOLS_2026-10-01.md](GLOBAL_AGENTS_AND_TOOLS_2026-10-01.md)

This guide collects the tools I rely on as a chemical biologist and professor of medicinal chemistry, and every name in it was checked against the installation on 2026-10-01. Core skills load automatically in every folder, while library skills live in `~\.agents\skill-library` and are available anywhere as soon as we name them.

## How to call things

The way we call a tool depends on where we are working, so the table below covers each case before the domain sections.

| Where you are | How to call it |
|---|---|
| **Claude Code, any folder** | Core skill: `/name` (e.g. `/literature-review`) or describe the task. Library skill: name it, e.g. *"usa la skill `chembl-database` de la biblioteca"*, or *"consulta skill-catalog"*. |
| **Antigravity (Gemini), any workspace** | Describe the task or name the skill; `GEMINI.md` already sends the agent to `skill-catalog`. |
| **Drive workspaces** (`J:\…\Developer`, `I:\…\Developer UGR`) | Same as above. Do not install skills there (packs refuse to run inside Drive). |
| **A local project you use constantly** | Load a pack permanently: `& 'I:\Mi unidad\Antigravity-Sync\skill-pack.ps1' enable biomed -Workspace .` Useful packs: `biomed`, `tooluniverse`, `bionemo`, `genomics`, `ugr`. |
| **Subagents (Claude Code)** | *"Delega en `document-reviewer`"*, *"pregunta a `albatross-expert`"*, *"usa `juanjo-copilot`"*. |
| **MCP connectors** | Just ask (*"busca en PubMed…"*, *"ADMET de este compuesto en ChEMBL"*); no skill needed. |
| **Python** (RDKit, scanpy, drug2cell, torch-geometric) | Always `py -3.13 script.py`. Plain `python` is Anaconda, with older or missing packages. |

## 1. Compounds, SAR & cheminformatics

| Tool | Where | Use it for |
|---|---|---|
| ChEMBL (MCP) | Connector | Compound search, IC50/Ki/EC50, mechanism, `get_admet`. Fastest route for SAR questions. |
| Inductive Bio (MCP) | Connector | ADMET and property prediction from SMILES. |
| `pubchem-database` | Library | Compound lookup by name, CID, SMILES or substructure; bioassays. |
| `tooluniverse-chemical-compound-retrieval` | Library | Full compound profile, disambiguation of names and SMILES, bioactivity. |
| `zinc-database` | Library | Purchasable analogues for virtual screening. |
| `drugbank-database` | Library | Drug pharmacology, targets, drug–drug interactions. |
| `glyph` | Library | SMILES to SVG/PNG and chemical typography for slides and exams. It does not read structures from images. |
| RDKit 2026.3.1 | `py -3.13` | Descriptors, fingerprints, substructures, conformers. |
| `nvmolkit-usage` | Library | GPU-batched fingerprints and similarity for large libraries. |
| Wolfram (MCP) | Connector | Physical-chemistry calculations, unit conversion, equilibria. |

In practice, a request such as *"Usa ChEMBL para el SAR de inhibidores de [diana] con IC50 < 100 nM"* goes straight to the connector, and *"Dame análogos comprables de este SMILES con zinc-database"* pulls the library skill without any further setup.

## 2. Targets, mechanism, safety & pharmacology

| Tool | Where | Use it for |
|---|---|---|
| `tooluniverse` (router) | Core | Entry point; picks the right ToolUniverse sub-skill. |
| `tooluniverse-target-research` / `-drug-target-validation` | Library | Target dossier and a 0–100 druggability score. |
| `tooluniverse-drug-research` | Library | Complete drug profile: chemistry, pharmacology, ADMET, trials. |
| `tooluniverse-chemical-safety` | Library | Toxicity: ADMET-AI, Ames mutagenicity, drug-induced liver injury (DILI) risk. Relevant to LiverAce. |
| `tooluniverse-drug-drug-interaction` | Library | CYP450 and transporter interactions. |
| `tooluniverse-network-pharmacology` / `-drug-repurposing` | Library | Polypharmacology and new indications. |
| `tooluniverse-adverse-event-detection` / `openfda-database` | Library | FAERS adverse events and safety signals. |
| `clinpgx-database` | Library | Pharmacogenomics and CPIC dosing guidelines. |
| Open Targets / Clinical Trials (MCP) | Connector | Target–disease evidence, clinical pipelines. |

For the LiverAce work, *"Usa tooluniverse para validar [diana] en hepatotoxicidad y resume el riesgo de DILI"* lets the router choose the safety and target sub-skills for us.

## 3. Structure, docking & design

| Tool | Where | Use it for |
|---|---|---|
| `pdb-database`, `alphafold-database-fetch-and-analyze` | Library | Experimental structures and AlphaFold models with per-residue confidence (pLDDT). |
| `pymol`, `foldseek-structural-search` | Library | Figures and visualisation; structural similarity search. |
| `diffdock` / `diffdock-nim` | Library | Protein–ligand docking. |
| `boltz2-nim` | Library | Co-folding of a protein with a ligand or binder. |
| `molmim-nim`, `genmol-nim` | Library | Generative small-molecule design (NVIDIA BioNeMo). |
| `kermt-finetune` / `kermt-infer` | Library | Train a KERMT molecular property model on your SMILES/assay CSV, then predict. |
| `rfdiffusion-nim` → `proteinmpnn-nim` → `boltz2-nim` | Library (`bionemo` pack) | De novo binder design; template 19 runs the chain. |
| `rfd3-designer`, `rfd3-paper` + `rfd3-expert` subagent | Core / Library + subagent | De novo all-atom biopolymer scaffolding (RFdiffusion3), unindexed catalytic theozymes, metalloenzymes (Zn2+, carbamylated Lys), targeted amyloid proteases, RNA codesign and hybrid ribonucleoprotein catalysts. |
| `esm` | Library | Protein language models (ESM3 / ESM C). |

## 4. Nucleic acids, PNA, miRNA & variants (DestiNA, KRT10)

| Tool | Where | Use it for |
|---|---|---|
| `ncbi-sequence-fetch`, `ensembl-database`, `gene-database` | Library | Sequences and gene structure for probe design. |
| `alphagenome-single-variant-analysis` and the other `alphagenome-*` skills | Library | Regulatory effect of a variant (KRT10). Needs `ALPHAGENOME_API_KEY`. |
| `clinvar-database`, `gnomad-database` | Library | Clinical classification and allele frequency. |
| `albatross-rna-paper` + `albatross-expert` subagent | Library + subagent | IRES and alternative RNA conformations, DMS-MaPseq. |
| `string-database`, `reactome-database`, `kegg-database` | Library | Interactions and pathways around a target or miRNA. |
| `analytical-chemistry-qc` | Library | Raw ¹H/¹³C NMR and LC-MS processing for PNA syntheses: phasing, deconvolution, UV purity, MS adducts. |
| `matchms`, `hmdb-database` | Library | MS spectral matching and metabolite identification. |

On the synthesis side, *"Usa analytical-chemistry-qc sobre la carpeta del FID de Bruker y dame la pureza y los aductos [M+H]+"* takes a raw NMR or LC-MS folder through to a purity figure we can report.

## 5. Literature, patents & grants

| Tool | Where | Use it for |
|---|---|---|
| PubMed, Consensus (MCP) | Connector | Fast literature search; Consensus summarises what the evidence agrees on. |
| `literature-review` | Core | Systematic review with citations. |
| `literature-search-europepmc` / `-openalex` / `-biorxiv` / `-arxiv` | Library | Full text, bibliometrics, preprints. |
| `uspto-database` | Library | Patents and prior art (PNA modifications, isomiRs). |
| `hypothesis-generation` | Library | Testable hypotheses from observations. |
| `scientific-writing`, `scientific-manuscript-review` | Core | IMRAD manuscripts; peer-review-style critique. |

For a prior-art question, *"Ejecuta la plantilla 7 sobre sondas PNA para miR-122"* runs PubMed, the preprint servers and USPTO in parallel and returns a single matrix.

## 6. Teaching (QFUNO, QFDOS, QO, TRANSMED)

| Tool | Where | Use it for |
|---|---|---|
| `ugr-courseware` | Library | Course materials and single-file interactive web apps (Genyo Fusion). |
| `qfdos-exam-generator` | Library | QFDOS exams. |
| `juanjo-ugr-dev-agent` | Core | UGR web development: Vercel, Google Apps Script, course portals. |
| `markdown-slides`, `anydoc` | Core | Lecture slides; Word, PowerPoint or PDF to Markdown. |
| `graphify` | Core | Knowledge graph from a folder of notes or papers. |

When preparing a unit, *"Plantilla 5 para QF1 Tema 3"* builds the simulator, the quiz and the study guide in parallel.

## 7. Documents, quality & ISO

| Tool | Where | Use it for |
|---|---|---|
| `document-reviewer` subagent | Subagent | Full Jev-gated review of any deliverable: *"Delega en document-reviewer el informe X.docx"*. |
| `jev-system-one`, `humanizer-juanjo(-es)`, `no-ai-slop`, `watermarks-remover` | Core | The individual stages of that pipeline. |
| `iso-13485-certification` | Library | QMS documentation and gap analysis for the IVD transition. |

## Shortcuts

Finally, when it is not clear which tool fits, *"Consulta skill-catalog y dime qué skill sirve para…"* is the quickest way in. The full catalogue of 228 library skills is in `~\.gemini\GLOBAL_AGENTS_AND_TOOLS_2026-10-01.md`, and the 19 subagent templates are in `~\.gemini\SUBAGENTS_TEMPLATES_2026-10-01.md`.
