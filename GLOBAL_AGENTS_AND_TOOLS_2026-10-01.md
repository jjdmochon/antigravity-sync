# Global Master Catalog: Agents, Subagents, Skills & Tools

**Updated:** 2026-10-01 · supersedes `GLOBAL_AGENTS_AND_TOOLS.md`

> [!NOTE]
> Installed at `%USERPROFILE%\.gemini\GLOBAL_AGENTS_AND_TOOLS_2026-10-01.md` and linked from
> [GEMINI.md](GEMINI.md). Source of truth: `Antigravity-Sync` on Google Drive
> (git `jjdmochon/antigravity-sync`). Everything listed here works from **any folder or workspace**.

---

## 1. Architecture

| Layer | Path | Content | Loaded |
| :--- | :--- | :--- | :--- |
| Core | `~\.agents\skills` (also `~\.claude\skills`, `~\.gemini\config\skills` via junctions) | 43 skills: persona, Jev pipeline, writing, orchestration, routers | Always |
| Library | `~\.agents\skill-library` | 228 domain skills | On demand, via `skill-catalog` |
| Archive | `~\.agents\skill-archive` | Retired collections (ClaudeScientificSkills, legacy flat files) | Never |

- **Why two layers.** Loading every skill overflowed Antigravity's *Customization token budget* and
  skills were truncated at random. The core costs about 18 KB of descriptions; the library costs nothing
  until a skill is read.
- **Reaching a library skill.** Open `skill-catalog` (index at
  `~\.agents\skills\skill-catalog\references\index.md`), then read
  `~\.agents\skill-library\<name>\SKILL.md` and follow it. Never report a capability as missing
  without checking the catalog.
- **Workspace packs** (local folders only, never inside Google Drive): `skill-pack.ps1 enable <pack>`
  links a group of library skills into `<ws>\.agents\skills` and `<ws>\.claude\skills`.
  Packs: `biomed`, `tooluniverse`, `tooluniverse-dev`, `genomics`, `bionemo`, `sci-python`, `gcp-data`,
  `design`, `business`, `ugr`.
- **Drive workspaces** (`Developer`, `Developer UGR`) carry no skill copies since 2026-10-01.

---

## 2. Primary Persona: `juanjo-copilot`

- **Mode:** fast mode, autonomous execution, bilingual (Spanish / English).
- **Domains:** DestiNA Genomics (DCL, SMART probes, PCR-free detection, miR-122 / DILI, MALDI-TOF and
  LC-MS); UGR teaching (QFUNO, QFDOS, QO1/QO2, TRANSMED, interactive web apps, Genyo Fusion);
  PNA biophysics and geometric deep learning; KRT10; ISO 9001 / ISO 13485.
- **Where it lives:** core skill `juanjo-copilot`, Claude Code subagent
  `~\.claude\agents\juanjo-copilot.md`, Antigravity rule
  `config\plugins\juanjo-omni-agent\rules\agent_protocol.md`. The three copies carry the same pipeline.

### Mandatory document pipeline (Jev-gated)

| Stage | Tool | Rule |
| :--- | :--- | :--- |
| 0. Triage | `jev-system-one` → `py -3.13 "$HOME/.agents/skills/jev-system-one/scripts/jev_doc_gatekeeper.py" "<file>" --json` | Always first, on the file path. Run only the stages listed in `etapas_a_ejecutar`. |
| 1. Provenance | `remove-ai-marks` / `watermarks-remover` | Invisible Unicode, zero-width markers, homoglyphs, C2PA / EXIF / XMP. |
| 2. Anti-slop | `no-ai-slop` | AI clichés, robotic cadence, filler. |
| 3. Voice | `humanizer-juanjo` or `humanizer-juanjo-es` | Exactly the one Jev selects. |
| 4. Certification | Gatekeeper again | Sign-off requires `quality_gate_passed == true`; quote Jev's probabilities. |

> [!IMPORTANT]
> Jev needs Python 3.13 (`C:\Python313`, where `typesafe-sdk` 0.7.1 is installed) and
> `TYPESAFE_API_KEY` in `~\.env`. Plain `python` resolves to Anaconda and makes the engine fall back to
> `fallo-abierto (sin Jev)`, which never certifies.

---

## 3. Subagents

### Claude Code (`~\.claude\agents`, synced from `claude_agents\`)

| Subagent | Use it for | Tools |
| :--- | :--- | :--- |
| `juanjo-copilot` | Any task in Juanjo's domains with the persona and the Jev pipeline active. | All |
| `document-reviewer` | Running the Jev-gated review pipeline on a finished document; reports Jev probabilities. | Bash, Read, Edit, Write, Glob, Grep |
| `albatross-expert` | Albatross RNA language model, IRES structural logic, alternative RNA conformations, DMS-MaPseq (Sychla et al., Rouskin Lab, bioRxiv 2026). Pairs with the library skill `albatross-rna-paper`. | Bash, Read, Edit, Write, Glob, Grep |

Built-in Claude Code agent types (`Explore`, `Plan`, `general-purpose`) and the `Workflow` tool cover
read-only search, planning and multi-agent orchestration. Templates for both platforms:
[SUBAGENTS_TEMPLATES_2026-10-01.md](SUBAGENTS_TEMPLATES_2026-10-01.md).

### Antigravity

Subagents are created at run time with `define_subagent` / `invoke_subagent` (least privilege,
`Workspace: "branch"` for anything that writes) and governed with `send_message` / `manage_subagents`.
The `multi-agent-orchestrator` and `subagent-templates` core skills describe the patterns.

---

## 4. MCP Servers

| Platform | Server | Status | Notes |
| :--- | :--- | :--- | :--- |
| Claude Code (user scope) | `gemini-api-docs` | Connected | HTTP, `https://gemini-api-docs-mcp.dev` |
| Claude Code (user scope) | `chrome-devtools` | Connected | `npx -y chrome-devtools-mcp@latest` |
| Claude Code (claude.ai connectors) | PubMed, ChEMBL, Open Targets, Clinical Trials, Consensus, Wolfram, Inductive Bio, Gmail, Google Calendar, Google Drive, Google Docs, Google Sheets, Claude Docs, Spotify | Connected | Prefer PubMed / ChEMBL / Open Targets / Clinical Trials MCP over the equivalent library skills. |
| Claude Code (claude.ai connectors) | Slack, Microsoft 365, Notion, Atlassian, Linear, monday.com, Asana, Box, Canva, Figma, HubSpot, Intercom, Maven Bio, AdisInsight, Scholar Gateway | Needs authentication | Authenticate only when needed. |
| Antigravity | `gemini-api-docs` (plugin `gemini-api`) | Active | |
| Antigravity | `claude-skills` (`antigravity-ide\mcp_config.json`) | Disabled | Served the same skills a second time and inflated the budget. |
| — | `tooluniverse` | Removed (2026-10-01) | Exposed hundreds of tools; covered by the `tooluniverse` router skill and the library. |

`sync-pull` registers the two Claude Code user-scope servers on a new machine and reports any failure.

### Antigravity plugins (`~\.gemini\config\plugins`)

`android-cli-plugin`, `chrome-devtools-plugin`, `gemini-api`, `google-antigravity-sdk`,
`juanjo-omni-agent`, `modern-web-guidance-plugin`. Their bundled `SKILL.md` files are renamed
`SKILL.md.disabled`, because the same skills already live in the core.

---

## 5. Installed Scientific, AI & Provenance Stack

Versions verified on 2026-10-01 in `C:\Python313` (`py -3.13 -m pip list`). Other interpreters on
the machine (Anaconda, 3.12) carry different or older versions.

### Single-cell, omics & data

| Package | Version | Function |
| :--- | :--- | :--- |
| `drug2cell` | 0.1.2 | Single-cell drug-target mapping and per-cell activity scoring with ChEMBL (`d2c.score`, `d2c.gsea`). |
| `scanpy` | 1.12.3 | Single-cell RNA-seq: QC, normalisation, clustering, UMAP, markers. |
| `anndata` | 0.13.2 | Annotated matrices (`.h5ad`). |
| `blitzgsea` | 1.3.54 | Fast gene set enrichment. |
| `zarr` / `h5py` | 3.3.0 / 3.16.0 | Chunked N-D arrays and HDF5. |
| `pandas` / `numpy` / `scipy` / `sympy` | 3.0.0 / 2.4.2 / 1.17.1 / 1.14.0 | Tabular, numerical and symbolic computing. |

### Cheminformatics & chemical biology

| Package | Version | Function |
| :--- | :--- | :--- |
| `rdkit` | 2026.3.1 | 2D/3D structures, substructure search, descriptors. |
| `SmilesPE` | 0.0.3 | SMILES pair encoding for chemical language models. |
| `analytical-chemistry-qc` (library skill) | — | Raw ¹H/¹³C NMR and LC-MS processing: phasing, baseline, deconvolution, UV purity, MS adducts. |

### Geometric deep learning & models

| Package | Version | Function |
| :--- | :--- | :--- |
| `torch` | 2.13.0 | Tensors and neural networks. |
| `torch-geometric` | 2.7.0 | Graph neural networks for molecules and structural analogues. |
| `e3nn` | 0.6.0 | E(3)-equivariant networks for 3D conformers. |
| `transformers` / `peft` | 5.15.0 / 0.20.0 | Transformer architectures and parameter-efficient fine-tuning. |
| `umap-learn` | 0.5.12 | Manifold learning and visualisation. |

### Documents, audio & web

| Package | Version | Function |
| :--- | :--- | :--- |
| `PyMuPDF` / `pymupdf4llm` | 1.27.2.3 | PDF parsing and Markdown extraction. |
| `python-docx` | 1.2.0 | Word documents (also used by Jev's gatekeeper). |
| `openai-whisper` | 20250625 | Local transcription. |
| `python-fasthtml` / `starlette` / `uvicorn` | 0.14.11 / 1.6.0 / 0.52.2 | Async web apps. |
| `graphifyy` | 0.3.1 | Knowledge graphs from folders (`graphify` CLI). |
| `typesafe-sdk` | 0.7.1 | Jev System-1 engine (see section 2). |

### Declared but not verified in `C:\Python313` on 2026-10-01

`nmrglue`, `pyopenms`, `polars`, `magika` (Python package and CLI), R / Bioconductor qPCR suite,
MegaMolBART, `bionemo-agent-toolkit` (`Developer UGR\bionemo-agent-toolkit`), `assembly_go`,
`molecular_spaces`, `tabfm`. Check with `py -3.13 -m pip show <name>` before relying on them.

### Command-line tools

| Command | Status on this machine | Function |
| :--- | :--- | :--- |
| `sync-push` / `sync-pull` | On PATH (`%LOCALAPPDATA%\agy\bin`) | Drive synchronisation (section 7). |
| `graphify` | On PATH | Knowledge graph generation. |
| `uv` | On PATH | Python packages and environments. |
| `ffmpeg` / `ffprobe` | On PATH | Audio and video for `/brag` and media skills. |
| `wm-clean`, `wm-inspect`, `wm-text`, `wm-audit`, `wm-score`, `wm-serve`, `watermarks-remover` | Not on PATH | Installed by `setup-secondary-pc.ps1`. Until then use the `watermarks-remover` skill scripts. |
| `gh` | Not installed | `winget install GitHub.cli`; git pushes work through Git Credential Manager. |

---

## 6. Skills

Descriptions come from each `SKILL.md` and are shortened. Core skills load automatically; library
skills are read on demand.

### 6.1 Core (43 skills, always loaded)

#### Persona, Jev pipeline & writing

| Skill | Purpose |
| :--- | :--- |
| `juanjo-copilot` | Master personal agent for Juan José Díaz-Mochón (Juanjo): UGR academic teaching, DestiNA Genomics (PNA/DCL chemistry, miRNA biomarkers), KRT10 keratin biophysics, ISO... |
| `jev-system-one` | Ultrarrápido motor de decisiones "System 1" no autoregresivo (TypeSafe AI Jev) para enrutamiento de subagentes (<100ms), circuit breakers, filtrado de slop de IA y tri... |
| `humanizer-juanjo` | Rewrite English text in Juanjo's own voice — composed, quietly confident, technically specific, action-oriented — while stripping every AI writing tell. Use when the u... |
| `humanizer-juanjo-es` | Reescribir texto en español con la voz propia de Juanjo — serena, discretamente segura, técnicamente específica y orientada a la acción — eliminando toda señal de escr... |
| `humanizer` | Remove signs of AI-generated writing from text. Use when editing or reviewing text to make it sound more natural and human-written. Based on Wikipedia's comprehensive... |
| `humanizer-hugh` | Humanize text using Hugh's personal writing voice. Removes AI-generated patterns and rewrites in Hugh's warm, conversational, professional-personal style. Combines the... |
| `no-ai-slop` | Edit drafts into sharper, more human writing while preserving the writer's personal voice, or detect AI-slop patterns without rewriting. Use when the user wants a draf... |
| `remove-ai-marks` | Remove multi-vendor AI provenance marks: invisible Unicode (Layer A), statistical text watermarks via rewrite (Layer B, always offer), and C2PA/EXIF/XMP/container meta... |
| `watermarks-remover` | Remove multi-vendor AI provenance marks: invisible Unicode (Layer A), statistical text watermarks via rewrite (Layer B, always offer), and C2PA/EXIF/XMP/container meta... |
| `clean-user-facing-text` | Clean and finalize authorized natural-language text intended for readers by auditing suspicious invisible Unicode and rewriting prose while preserving facts and meanin... |
| `document-pipeline` | High-stakes document production orchestrating Builder -> Provenance -> Voice stages for zero AI provenance, calibrated voice, and clean metadata. |
| `scientific-writing` | Draft, write, or revise scientific manuscripts, technical reports, and IMRAD articles with domain notation standards and publication quality. |
| `scientific-manuscript-review` | Systematic review and editing of scientific manuscripts to improve clarity, structure, scientific rigor, and reader comprehension. |
| `literature-review` | Search, survey, and synthesize scientific literature across PubMed, bioRxiv, EuropePMC, arXiv, and USPTO with structured evidence and verified citations. |
| `google-dev-style-guide` | Use this skill when writing, editing, reviewing, or auditing technical documentation, developer guides, API references, READMEs, code comments, release notes, or tutor... |

#### Routers & discovery

| Skill | Purpose |
| :--- | :--- |
| `skill-catalog` | Index of 228 extra skills kept out of the context budget (ToolUniverse, AlphaGenome, Albatross, NVIDIA BioNeMo/NIM protein design, biomedical databases, literature sea... |
| `tooluniverse` | Router skill for ToolUniverse tasks. First checks if specialized tooluniverse skills (54 skills covering disease/drug/target research, clinical decision support, genom... |
| `find-skills-juanjo` | Find a skill: local core and skill-library first, npx skills / skills.sh as fallback; external skills reviewed and installed into skill-library only with approval. |

#### Documents, slides & media

| Skill | Purpose |
| :--- | :--- |
| `anydoc` | Convert Word (.doc, .docx), PowerPoint (.ppt, .pptx), Excel (.xls, .xlsx), OpenDocument (.odt, .ods, .odp), RTF, EPUB, CSV, and PDF files to GitHub-Flavored Markdown a... |
| `convert-documents-to-markdown` | Convert Word (.doc, .docx), PowerPoint (.ppt, .pptx), Excel (.xls, .xlsx), OpenDocument (.odt, .ods, .odp), RTF, EPUB, CSV, and PDF files to GitHub-Flavored Markdown a... |
| `markdown-presentation` | Create professional, presenter-friendly markdown presentations with timing guidance, expandable details, and clean visual hierarchy. |
| `markdown-slides` | Create presentation slides in Markdown format (Deckset/Marp compatible). Use when user requests to create slides, presentations, or convert documents to slide format.... |
| `magika` | Detect and determine file content types, MIME types, and binary file formats using Google's Magika deep-learning model. Use when identifying unknown files, verifying b... |
| `graphify` | any input (code, docs, papers, images) → knowledge graph → clustered communities → HTML + JSON + audit report |
| `brag` | Turn the current project website into a short, polished, shareable launch video using Hyperframes. Use when someone says "/brag", "let's brag about this", "make a laun... |
| `brag-slim` | Turn a project directory or a website URL into a short, shareable launch video with music, motion, and share copy. One file, no bundled assets — built entirely by the... |

#### Orchestration & agent engineering

| Skill | Purpose |
| :--- | :--- |
| `multi-agent-orchestrator` | Complete 5-Part Elevating Antigravity master engineering suite: interactive UI interviewing (ask_question + user_prefs.json), parameterized visual asset generation (ge... |
| `subagent-templates` | Library of copy-paste parallel-subagent task patterns for common research/dev workflows (multi-omics dossiers, biomarker validation, PNA probe design, single-cell drug... |
| `workflow-skill-creator` | Distills a completed user workflow or interaction into a reusable agent skill. Use when the user asks to turn their workflow, interaction, or multi-step process into a... |
| `skill-repair` | Use this to fix and re-install agent skills that have failed installation. This skill provides the necessary context and permissions to surgically update the `manifest... |
| `paper2agent` | Convert research papers and associated files, research code, or both into a reviewed paper skill and tested MCP server. Use for paper-only, code-only, or combined conv... |
| `smart-pna-probe-design` | Design DestiNA DGL / SMART PNA probe panels for Dynamic Chemical Labelling (DCL) PCR-free nucleic acid and microRNA detection, abasic monomer placement, and PNA.DNA duplex structural models. |
| `juanjo-ugr-dev-agent` | Specialized AI pair programmer, scientific researcher, and academic assistant for Dr. Juan José Díaz-Mochón (Juanjo). Integrates full domain context across Biotech/DES... |

#### Development, Python & safety

| Skill | Purpose |
| :--- | :--- |
| `uv` | Checks whether the uv Python package manager is installed and installs it if missing. Ensures uv is on PATH. Use when another skill requires uv as a prerequisite. |
| `managing-python-dependencies` | Ensures proper Python dependency management, avoiding global `pip install` and adhering to project-specific tooling. |
| `ml-best-practices` | CRITICAL RULE: You MUST use this skill whenever the task involves any machine learning tasks or data analysis. Use this skill if the user's prompt or requirements ment... |
| `credentials` | Instructions for handling API keys and credentials safely, verifying their presence, and prompting the user to add them if missing using a safe protocol. |
| `accidental-data-loss-prevention` | **STOP AND VERIFY**: Before running any command or tool that results in irreversible data loss, you MUST obtain explicit user consent. When in doubt, ask. It is better... |

#### Google, Gemini & Android

| Skill | Purpose |
| :--- | :--- |
| `gemini-api-dev` | Use this skill when writing code that calls the Gemini API for text generation, multi-turn chat, multimodal understanding, image generation, video generation, streamin... |
| `gemini-interactions-api` | Use this skill when writing code that calls the Gemini API for text generation, multi-turn chat, multimodal understanding, image generation, video generation, streamin... |
| `gemini-live-api-dev` | Use this skill when building real-time, bidirectional streaming applications with the Gemini Live API. Covers WebSocket-based audio/video/text streaming, voice activit... |
| `gemini-omni-flash-api` | Use this skill for generative video editing, text-to-video, image-referenced video generation, first-frame-to-video, first-and-last-frame transitions, and video extens... |
| `google-antigravity-sdk` | Design, implement, and debug autonomous AI agents and multi-agent systems using the Google Antigravity (AGY) SDK. ACTIVATE this skill when the user wants to create, co... |
| `android-cli` | Provides instructions for installing and using the `android` CLI. The `android` command-line tool is a critical tool for Android development and helps you create new A... |

### 6.2 Library (228 skills, on demand via `skill-catalog`)

#### Databases, literature & structure (52)

| Skill | Purpose |
| :--- | :--- |
| `alphafold-database-fetch-and-analyze` | Retrieve and analyze AlphaFold predicted structures for a protein. Use when the user provides a specific UniProt Accession ID and wants structural confidence metrics (... |
| `biorxiv-database` | Efficient database search tool for bioRxiv preprint server. Use this skill when searching for life sciences preprints by keywords, authors, date ranges, or categories,... |
| `brenda-database` | Access BRENDA enzyme database via SOAP API. Retrieve kinetic parameters (Km, kcat), reaction equations, organism data, and substrate-specific enzyme information for bi... |
| `chembl-database` | Query the ChEMBL database for bioactive molecules, drug targets, bioactivity data, approved drugs, and chemical structures. Use when the user asks about compounds, tar... |
| `clinical-trials-database` | Query ClinicalTrials.gov via APIv2. Use when you want to search for trials by condition, drug, location, status, or phase; retrieve trial details by NCT ID; check elig... |
| `clinpgx-database` | Access ClinPGx pharmacogenomics data (successor to PharmGKB). Query gene-drug interactions, CPIC guidelines, allele functions, for precision medicine and genotype-guid... |
| `clinvar-database` | Use when needing clinical significance, pathogenicity classifications (e.g., Pathogenic, Benign, VUS), clinical evidence rationales, or finding "hard positive" benchma... |
| `consensus-database` | Query the Consensus.app API to search over 220M+ peer-reviewed academic research papers, extract AI-synthesized takeaways, SJR quartile impact, and citation metrics. U... |
| `dbsnp-database` | Use when you want to look up, map, and search for short genetic variants (SNPs, indels) in NCBI's dbSNP database. Resolves between rsIDs, genomic coordinates in VCF fo... |
| `drugbank-database` | Access and analyze comprehensive drug information from the DrugBank database including drug properties, interactions, targets, pathways, chemical structures, and pharm... |
| `embl-ebi-ols` | Query and search the EMBL-EBI Ontology Lookup Service (OLS) for biomedical ontology terms, definitions, and hierarchies across 250+ ontologies (e.g., GO, DOID, HP). Us... |
| `ena-database` | Access European Nucleotide Archive via API/FTP. Retrieve DNA/RNA sequences, raw reads (FASTQ), genome assemblies by accession, for genomics and bioinformatics pipeline... |
| `encode-ccres-database` | Query the ENCODE Registry of cis-Regulatory Elements (cCREs) via the SCREEN GraphQL API, or make custom queries to the ENCODE Portal REST API for experiments and files... |
| `ensembl-database` | Query the Ensembl database to resolve gene, transcript, and protein IDs, fetch genomic or protein sequences, retrieve gene structures (exons), and get variant conseque... |
| `fda-database` | Query openFDA API for drugs, devices, adverse events, recalls, regulatory submissions (510k, PMA), substance identification (UNII), for FDA regulatory data analysis an... |
| `foldseek-structural-search` | Performs 3D structural searches of proteins against various databases (PDB, AlphaFold, CATH, MGnify, etc.) using the Foldseek API. Use ONLY when the user provides a ph... |
| `gene-database` | Query NCBI Gene via E-utilities/Datasets API. Search by symbol/ID, retrieve gene info (RefSeqs, GO, locations, phenotypes), batch lookups, for gene annotation and func... |
| `geo-database` | Access NCBI GEO for gene expression/genomics data. Search/download microarray and RNA-seq datasets (GSE, GSM, GPL), retrieve SOFT/Matrix files, for transcriptomics and... |
| `gnomad-database` | Query the Genome Aggregation Database (gnomAD). Use when determining the rarity or allele frequency of specific genetic variants, retrieving gene constraint metrics (p... |
| `gtex-database` | Use when you want to retrieve quantitative RNA expression data and variant eQTL information from the GTEx (Genotype-Tissue Expression) Project across 54 non-diseased t... |
| `gwas-database` | Query NHGRI-EBI GWAS Catalog for SNP-trait associations. Search variants by rs ID, disease/trait, gene, retrieve p-values and summary statistics, for genetic epidemiol... |
| `hmdb-database` | Access Human Metabolome Database (220K+ metabolites). Search by name/ID/structure, retrieve chemical properties, biomarker data, NMR/MS spectra, pathways, for metabolo... |
| `human-protein-atlas-database` | Use when you want to retrieve semi-quantitative protein expression and spatial localisation data from the Human Protein Atlas (HPA). |
| `interpro-database` | Identify domains, families, and sites in proteins; find all proteins in a family or sharing a domain; explore species distribution for a domain; annotate genomes with... |
| `jaspar-database` | Query the JASPAR database for Transcription Factor (TF) binding profiles. Use when retrieving Position Frequency Matrices (PFMs) or Position Weight Matrices (PWMs) for... |
| `kegg-database` | Direct REST API access to KEGG (academic use only). Pathway analysis, gene-pathway mapping, metabolic pathways, drug interactions, ID conversion. For Python workflows... |
| `literature-search-arxiv` | Search for scientific papers, preprints, and publications on arXiv. Extract metadata, abstracts, and download full-text PDFs or HTML versions of papers. Use when the u... |
| `literature-search-biorxiv` | Browse, filter, and download life sciences, biology, and medical preprints from bioRxiv and medRxiv. Supports fetching paper metadata by DOI, and browsing by date rang... |
| `literature-search-europepmc` | Search Europe PMC for scientific literature and download open-access full texts and PDFs. Retrieve full-text XML/plain text by PMCID, get citation lists and bibliography. |
| `literature-search-openalex` | Query the OpenAlex scholarly database for research papers, authors, institutions, topics, sources, publishers, funders, geo-locations, and keywords. Use when searching... |
| `metabolomics-workbench-database` | Access NIH Metabolomics Workbench via REST API (4,200+ studies). Query metabolites, RefMet nomenclature, MS/NMR data, m/z searches, study metadata, for metabolomics an... |
| `ncbi-sequence-fetch` | Retrieve protein and nucleotide sequences from NCBI databases using E-utilities. Supports direct accession lookup, CDS translation, gene+organism search, locus lookup,... |
| `openalex-database` | Query and analyze scholarly literature using the OpenAlex database. This skill should be used when searching for academic papers, analyzing research trends, finding wo... |
| `openfda-database` | Query, search, and download data from the openFDA API for drugs, devices, foods, tobacco, cosmetics, animal and veterinary products, substances, and transparency data.... |
| `opentargets-database` | Query Open Targets Platform for target-disease associations, drug target discovery, tractability/safety data, genetics/omics evidence, known drugs, for therapeutic tar... |
| `pdb-database` | Use when you want to search for or download experimentally-determined 3D structures for biomolecules (proteins, nucleic acids, bound ligands). Supports searching by se... |
| `predictingthepast` | Ancient text restoration, attribution, dating, contextualization, and embedding via Aeneas (Latin) / Ithaca (Ancient Greek). Use when asked to "restore", "attribute",... |
| `protein-interaction-network-analysis` | Analyze protein-protein interaction networks using STRING, BioGRID, and SASBDB databases. Maps protein identifiers, retrieves interaction networks with confidence scor... |
| `protein-sequence-msa` | Performs multiple sequence alignment of proteins with EBI Clustal Omega. Use when you need to align multiple sequences to assess similarity, domain conservation, or ke... |
| `protein-sequence-similarity-search` | Searches for homologous protein sequences using MMseqs2 (fast, default) or BLAST (comprehensive, fallback). Trigger this whenever the user provides a protein sequence... |
| `pubchem-database` | Query PubChem, search by name/CID/SMILES, retrieve properties, similarity/substructure searches, bioactivity, for cheminformatics. Use when a user asks about a specifi... |
| `pubmed-database` | Search PubMed for scientific literature, including published clinical trials. Fetch abstracts and full text. Link published research to biological databases (gene, pro... |
| `pymol` | Visualize, analyze, and render protein and molecular structures using PyMOL. Use when the user wants to create images of protein structures, perform structural alignme... |
| `quickgo-database` | Query the QuickGO and Evidence & Conclusion Ontology (ECO) REST API. Use this when you need to map genes to biological processes, molecular functions, or cellular comp... |
| `reactome-database` | Query the Reactome database (Analysis and Content Services). Use when the user asks about pathway analysis, gene list enrichment, retrieving results by token, finding... |
| `scienceskillscommon` | Shared Python package for Science Skills, currently containing http_client -- a unified HTTP client with rate limiting, retries, and exponential backoff. Not a standal... |
| `string-database` | Query the STRING database for protein-protein interactions (PPIs), functional enrichment, and homology. Use when the user asks about interactions between specific prot... |
| `ucsc-conservation-and-tfbs` | Fetch Evolutionary Conservation scores (phyloP, phastCons) and Transcription Factor Binding Sites (TFBS) from the UCSC Genome Browser. Use when analyzing whether genom... |
| `unibind-database` | Queries the UniBind database for experimentally validated transcription factor (TF) binding sites. Use when retrieving direct TF-DNA interaction datasets, downloading... |
| `uniprot-database` | Access protein metadata, function, taxonomy, and sequences across UniProtKB, UniParc, and UniRef. Use when searching for proteins, mapping identifiers, or retrieving f... |
| `uspto-database` | Access USPTO APIs for patent/trademark searches, examination history (PEDS), assignments, citations, office actions, TSDR, for IP analysis and prior art searches. |
| `zinc-database` | Access ZINC (230M+ purchasable compounds). Search by ZINC ID/SMILES, similarity searches, 3D-ready structures for docking, analog discovery, for virtual screening and... |

#### Quality & ISO (1)

| Skill | Purpose |
| :--- | :--- |
| `iso-13485-certification` | Comprehensive toolkit for preparing ISO 13485 certification documentation for medical device Quality Management Systems. Use when users need help with ISO 13485 QMS do... |

#### Design, communication & business (12)

| Skill | Purpose |
| :--- | :--- |
| `airtable-kanban-work-tracker` | Track your work as records on an Airtable Kanban board: one thread per record, flipping each record from an in-progress status to a ready-for-review status as you work... |
| `brand-book-generator` | Generates three radically distinct, on-trend brand concepts for a founder's app and ships them as a single NO-SCROLL hero webpage — a bento "brand book" (logo + taglin... |
| `briefing-trailer` | Turn a real day — a founder's, an operator's, anyone's — into a cinematic ~30s "coming soon" movie trailer where the trailer IS the day's briefing, told entirely in te... |
| `business-simulation-operator-method` | A battle-tested methodology for running ANY business in real-time simulation as an autonomous operator agent on Hyperagent. Pick a venture — a shop, restaurant, SaaS p... |
| `claymation-explainer` | End-to-end workflow for producing a playful claymation-style explainer/ad video: storyboard → character reference images → scene stills → Veo image-to-video clips → si... |
| `landscaping-design-and-quote` | Turns a customer's backyard photo + address into an interactive design-and-quote package: a clean "before", multiple AI design concepts rendered from the same photo, b... |
| `muller-brockmann-grid-systems` | Build editorial/magazine/report webpages on a GENUINE Müller-Brockmann modular grid (International Typographic Style) — not a decorative one. Encodes the discipline (c... |
| `nyc-subway-campaign` | End-to-end method to visualize a full NYC subway (MTA) out-of-home ad campaign for any brand: lock a vivid brand identity, create a canonical logo asset FIRST and reus... |
| `nyt-data-viz` | NYT-discipline data visualization. Applies the design rules of The New York Times graphics desk + Upshot — color, typography, annotation, chart-type selection — to mak... |
| `onetake` | Short product or skill motion films (10–30 s, narrated feature demos up to ~60 s) in one continuous take: measured moves, UI rebuilt from screenshots, shutter motion blur, 4K60 and a continuity oracle. Noncommercial licence: UGR only, never DestiNA. |
| `veo-hyperframes` | End-to-end production pipeline for creating polished launch videos using Veo 3.1 video generation and Hyperframes motion graphics overlays. Built around the Text Zone... |
| `vignelli-canon-design-system` | Massimo Vignelli's complete design discipline — distilled from The Vignelli Canon (his own book). Encodes the Intangibles (semantics, discipline, appropriateness, time... |

#### UGR teaching (2)

| Skill | Purpose |
| :--- | :--- |
| `qfdos-exam-generator` | Metodología oficial, pipeline de generación, calibración psicométrica y quimioinformática para la preparación de exámenes de Química Farmacéutica II (2627 QFDOS E · Gr... |
| `ugr-courseware` | Create or enhance teaching materials for UGR courses (QF1/QF2/Quimica Farmaceutica), including class notes, HTML5 simulators (Genyo Fusion), quizzes, and exam problems. |

#### Genomics & sequence models (AlphaGenome, Albatross) (6)

| Skill | Purpose |
| :--- | :--- |
| `albatross-rna-paper` | Read and answer questions about An RNA Language Model trained on sequence alone reveals the structural logic of Internal Ribosome Entry Sites, its supplementary inform... |
| `alphagenome` | Master skill for Google DeepMind AlphaGenome foundation model across Eulerna, single-variant impact scoring, locus saturation mutagenesis scanning, chromatin accessibi... |
| `alphagenome-atlas-website-links` | Constructs deep-links and URLs for the AlphaGenome Atlas website. Supports generating single-variant exploration links (1-based chr:pos:ref>alt), genomic locus views (... |
| `alphagenome-eulerna` | Integración de AlphaGenome (Google DeepMind) en la plataforma Eulerna. Permite escanear mutagénesis en loci de eRNAs, evaluar variantes reguladoras no codificantes, ca... |
| `alphagenome-single-variant-analysis` | Analyzes genetic variant effects on gene expression (RNA-seq), chromatin accessibility (DNASE), histone marks (ChIP), and transcription factors using the AlphaGenome A... |
| `alphagenome-variant-impact-score` | Score, annotate, and analyze the functional impact of genetic variants using AlphaGenome Variant Impact (AVI) scores. Query variants in chr:pos:ref>alt format, annotat... |

#### Google Cloud, BigQuery & data (31)

| Skill | Purpose |
| :--- | :--- |
| `bigquery-ai-ml` | Leverages BigQuery's built-in machine learning and GenAI capabilities |
| `bigquery-bigframes` | Generates Python code using BigQuery DataFrames (BigFrames), the pandas/scikit-learn-style\ |
| `bigquery-data-transfer-service` | Discovers and inspects BigQuery Data Transfer Service (DTS) configurations. |
| `bigquery-graph` | Provides guidelines and best practices for querying and defining property |
| `bigquery-sql` | Provides BigQuery SQL query optimization techniques, execution best practices, |
| `bigtable-basics` | Assists in provisioning instances/tables, designing performant schemas, |
| `building-data-apps` | Build modern data apps, dashboards, and interactive reports using either React + Vite or Streamlit. Includes optional Gemini Data Analytics chat integration for an AI... |
| `data-autocleaning` | Automated data quality and transformation capabilities for Dataform/dbt/BigQuery |
| `dataform-bigquery` | Expertise in generating clean, correct, and efficient Dataform pipeline |
| `dbt-bigquery` | Expert guidance for creating, modifying, and optimizing dbt pipelines |
| `developing-with-bigquery` | A repository of BigQuery-specific logic, knowledge, and specialized standards. Use this skill whenever you are doing anything with BigQuery, including: 1. BigQuery que... |
| `discovering-gcp-data-assets` | Finds and inspects data assets within Google Cloud. Relevant when any of the following conditions are true: 1. The user request involves finding, exploring, or inspect... |
| `enforcing-resource-attribution` | Enforces resource attribution for CLI commands. Use this skill whenever |
| `federate-lakehouse-catalog` | Sets up Google Cloud Lakehouse federated catalogs to remote Iceberg |
| `gcloud-auth-verification` | Guidelines for identifying and resolving missing Google Cloud authentication |
| `gcp-composer-troubleshooting` | Provides expert guidance for troubleshooting Cloud Composer (Apache |
| `gcp-data-pipelines` | Primary entry point for building, managing, and orchestrating data pipelines |
| `gcp-dataflow` | Guides writing, packaging, executing, and troubleshooting Apache Beam pipelines on Dataflow. Use when creating new pipelines, configuring Flex Templates, or analyzing... |
| `gcp-managed-airflow-dag-authoring` | Guides the authoring and validation of Apache Airflow DAGs for Managed |
| `gcp-managed-airflow-migrations` | Provides guidance for migrating Apache Airflow DAGs in Managed Service |
| `gcp-managed-airflow-recommendations` | Provides recommendations and best practices for creating, configuring, |
| `gcp-pipeline-orchestration` | This skill helps the agent generate or update orchestration pipeline |
| `gcp-pipeline-resource-provisioning` | Automates declarative resource creation and provisioning for data pipelines, supporting BigQuery, Dataform, Dataproc, BigQuery Data Transfer Service (DTS), and other r... |
| `gcp-spark` | Develops and executes Spark code on Managed Spark on Google Cloud (Dataproc Clusters and Serverless). Reads and writes data using BigLake Iceberg catalogs, BigQuery an... |
| `gcs-security-assessment` | Assesses the security posture of Google Cloud Storage (GCS) buckets\ |
| `google-cloud-auth-verification` | Mandatory Step 0 pre-flight execution order and authentication verification |
| `google-cloud-storage-basics` | Stores, retrieves, and manages data as objects in Cloud Storage (Google\ |
| `google-cloud-storage-bucket-architect` | Creates Cloud Storage (Google Cloud Storage, or GCS) buckets. Analyzes\ |
| `google-cloud-storage-fuse` | Mounts Cloud Storage buckets as a POSIX file system with Cloud Storage\ |
| `notebook-guidance` | This skill guides the use of Jupyter notebooks for data analysis, exploration, and visualization, particularly with BigQuery. It outlines best practices for notebook e... |
| `schema-mapping` | Guides the process of analyzing, mapping, and documenting transformations |

#### NVIDIA BioNeMo, NIM & protein design (30)

| Skill | Purpose |
| :--- | :--- |
| `boltz2-nim` | Use Boltz2 NIM for biomolecular structure prediction and binding affinity. Invoke for Boltz2, protein structures, protein-ligand/DNA/RNA complexes, SMILES or CCD ligan... |
| `complexa-design` | End-to-end Proteina-Complexa design pipeline driver. Reach for this skill whenever the user wants to "design a binder", "design binders for X", "run complexa design",... |
| `complexa-evaluate-pdbs` | Standalone evaluation of an existing PDB directory with Proteina-Complexa. Use this skill whenever the user wants to "evaluate PDB files", "re-fold these designs", "co... |
| `complexa-setup` | First-time setup, environment configuration, and model-weight installation for Proteina-Complexa. Reach for this skill whenever the user says "set up complexa", "insta... |
| `complexa-slurm` | Launch Proteina-Complexa pipelines on a remote SLURM cluster — binder search, LaProteina monomer design, or multi-node distributed training. Reach for this skill whene... |
| `complexa-sweep` | Use this skill whenever the user wants to run a parameter sweep over a Proteina-Complexa design pipeline — cartesian-product hyperparameter scans, Pareto search over g... |
| `complexa-target` | Use this skill whenever the user wants to add, register, edit, list, show, or validate a Proteina-Complexa design target for any pipeline — protein binder (default), l... |
| `cuequivariance` | Define custom groups (Irrep subclasses), build segmented tensor products with CG coefficients, create equivariant polynomials and IrDictPolynomials, and use built-in d... |
| `diffdock-nim` | Run DiffDock molecular docking via NVIDIA NIM to predict small-molecule binding poses against protein targets. Use for DiffDock, molecular docking, ligand docking, bli... |
| `drug-discovery-pipeline` | Run a complete computational drug discovery pipeline using NVIDIA BioNeMo NIMs: generate drug-like molecules with GenMol, dock them to a protein target with DiffDock,... |
| `evo2-nim` | Generate and analyze DNA sequences using NVIDIA's Evo 2 BioNeMo NIM microservice. Use for Evo2/Evo 2, DNA generation, genomic sequence generation, hosted generation, l... |
| `genmol-nim` | Generate novel drug-like molecules using the GenMol NIM microservice. Use for de novo generation, scaffold decoration, motif extension, lead optimization, SAFE notatio... |
| `genomics-workflow-acceleration` | Use when accelerating existing genomics workflows with NVIDIA Parabricks, improving runtime or price/performance, converting pipeline steps to GPUs, or comparing CPU a... |
| `kermt-add-cmim-pretrain` | Convert a grover_base checkpoint (encoder-only or encoder + vocab heads) into a hybrid checkpoint by adding a randomly-initialized cMIM decoder + latent_dist, then con... |
| `kermt-continue-pretrain` | Continue pretraining from an existing KERMT checkpoint. The skill validates the user's checkpoint and pretrain CSV, prepares the data into shard/vocab/features form, t... |
| `kermt-embed` | Extract per-molecule embeddings from any encoder-bearing KERMT checkpoint (grover_base / cmim / hybrid / finetuned). Writes one .npy per readout type (atom_from_atom,... |
| `kermt-finetune` | Finetune a pretrained KERMT encoder on a labeled CSV. The skill validates the input checkpoint (must be a pretrain ckpt — grover_base / cmim / hybrid), validates the l... |
| `kermt-infer` | Run predictions with a finetuned KERMT checkpoint on a SMILES-only CSV. The skill validates that the input ckpt has task FFN heads (refuses pretrain ckpts with a redir... |
| `kermt-monitor` | Check progress for a detached KERMT run (pretrain, finetune, or any kermt_run_detached invocation). Reads run.json, queries docker for container state, tails the pretr... |
| `kermt-pretrain-scratch` | Pretrain a fresh KERMT model from scratch on a user-provided corpus. Builds a new vocabulary from the corpus, instantiates the model architecture from defaults, and la... |
| `kermt-setup` | Bootstrap the KERMT agent environment — verify host docker + nvidia-container-toolkit, build the kermt:latest image from the repo's Dockerfile if it doesn't yet exist,... |
| `molmim-nim` | Use this skill for MolMIM, NVIDIA's BioNeMo NIM microservice for small-molecule latent-space generation and optimization. Invoke for MolMIM, molecular embeddings, hidd... |
| `msa-search-nim` | Generate multiple sequence alignments (MSAs) for protein sequences using the ColabFold MSA-Search NIM. Use for homolog search, UniRef30/ColabFold env searches, A3M or... |
| `msa-structure-prediction-pipeline` | Run a complete protein structure prediction pipeline using NVIDIA BioNeMo NIMs: search for MSA alignments with MSA-Search (ColabFold), then predict the structure with... |
| `nvmolkit-usage` | Write code that calls the installed nvMolKit Python API for GPU-accelerated, batched RDKit-style operations - Morgan fingerprints, Tanimoto/cosine similarity, ETKDG co... |
| `openfold2-nim` | Use this skill for OpenFold2, NVIDIA's BioNeMo NIM microservice for monomer protein structure prediction. Invoke whenever the user mentions OpenFold2, AlphaFold2-like... |
| `openfold3-nim` | Use this skill for OpenFold3, NVIDIA's BioNeMo NIM microservice for biomolecular structure prediction. Invoke whenever the user mentions OpenFold3 or needs protein, pr... |
| `parabricks` | Route NVIDIA Parabricks pbrun tools, assess GPU/runtime readiness, and provide version-aware command guidance for FASTQ/BAM processing, RNA-seq, variant calling, BAM Q... |
| `proteinmpnn-nim` | Run ProteinMPNN inverse folding via NVIDIA NIM to design protein sequences for a target backbone. Use for ProteinMPNN, inverse folding, sequence design, backbone redes... |
| `rfdiffusion-nim` | Run RFDiffusion protein backbone design via NVIDIA NIM. Use for de novo protein backbones, motif scaffolding, binder design, hotspot residues, contigs syntax, diffusio... |

#### Scientific Python, ML & other tools (29)

| Skill | Purpose |
| :--- | :--- |
| `adaptyv` | Cloud laboratory platform for automated protein testing and validation. Use when designing proteins and needing experimental validation including binding assays, expre... |
| `analytical-chemistry-qc` | Automated end-to-end processing and expert interpretation of raw 1H/13C NMR (Bruker/Varian FID, acqus) and LC-MS (Shimadzu .lcd OLE2, Waters/Thermo .raw, .mzML) datase... |
| `arboreto` | Infer gene regulatory networks (GRNs) from gene expression data using scalable algorithms (GRNBoost2, GENIE3). Use when analyzing transcriptomics data (bulk RNA-seq, s... |
| `bioservices` | Unified Python interface to 40+ bioinformatics services. Use when querying multiple databases (UniProt, KEGG, ChEMBL, Reactome) in a single workflow with consistent AP... |
| `cellxgene-census` | Query the CELLxGENE Census (61M+ cells) programmatically. Use when you need expression data across tissues, diseases, or cell types from the largest curated single-cel... |
| `cobrapy` | Constraint-based metabolic modeling (COBRA). FBA, FVA, gene knockouts, flux sampling, SBML models, for systems biology and metabolic engineering analysis. |
| `datacommons-client` | Work with Data Commons, a platform providing programmatic access to public statistical data from global sources. Use this skill when working with demographic data, eco... |
| `deeptools` | NGS analysis toolkit. BAM to bigWig conversion, QC (correlation, PCA, fingerprints), heatmaps/profiles (TSS, peaks), for ChIP-seq, RNA-seq, ATAC-seq visualization. |
| `diffdock` | Diffusion-based molecular docking. Predict protein-ligand binding poses from PDB/SMILES, confidence scores, virtual screening, for structure-based drug design. Not for... |
| `esm` | Comprehensive toolkit for protein language models including ESM3 (generative multimodal protein design across sequence, structure, and function) and ESM C (efficient p... |
| `etetoolkit` | Phylogenetic tree toolkit (ETE). Tree manipulation (Newick/NHX), evolutionary event detection, orthology/paralogy, NCBI taxonomy, visualization (PDF/SVG), for phylogen... |
| `geniml` | This skill should be used when working with genomic interval data (BED files) for machine learning tasks. Use for training region embeddings (Region2Vec, BEDspace), si... |
| `gget` | Fast CLI/Python queries to 20+ bioinformatics databases. Use for quick lookups: gene info, BLAST searches, AlphaFold structures, enrichment analysis. Best for interact... |
| `glyph` | Chemical structures, Unicode scientific typography, and visual glyph generator. Use for rendering SMILES to SVG/PNG (RDKit), converting formulas to clean Unicode glyph... |
| `gtars` | High-performance toolkit for genomic interval analysis in Rust with Python bindings. Use when working with genomic regions, BED files, coverage tracks, overlap detecti... |
| `hypogenic` | Automated LLM-driven hypothesis generation and testing on tabular datasets. Use when you want to systematically explore hypotheses about patterns in empirical data (e.... |
| `hypothesis-generation` | Structured hypothesis formulation from observations. Use when you have experimental observations or data and need to formulate testable hypotheses with predictions, pr... |
| `imaging-data-commons` | Query and download public cancer imaging data from NCI Imaging Data Commons using idc-index. Use for accessing large-scale radiology (CT, MR, PET) and pathology datase... |
| `lamindb` | This skill should be used when working with LaminDB, an open-source data framework for biology that makes data queryable, traceable, reproducible, and FAIR. Use when m... |
| `markitdown` | Convert files and office documents to Markdown. Supports PDF, DOCX, PPTX, XLSX, images (with OCR), audio (with transcription), HTML, CSV, JSON, XML, ZIP, YouTube URLs,... |
| `matchms` | Spectral similarity and compound identification for metabolomics. Use for comparing mass spectra, computing similarity scores (cosine, modified cosine), and identifyin... |
| `modal` | Run Python code in the cloud with serverless containers, GPUs, and autoscaling. Use when deploying ML models, running batch processing jobs, scheduling compute-intensi... |
| `neuropixels-analysis` | Neuropixels neural recording analysis. Load SpikeGLX/OpenEphys data, preprocess, motion correction, Kilosort4 spike sorting, quality metrics, Allen/IBL curation, AI-as... |
| `pathml` | Full-featured computational pathology toolkit. Use for advanced WSI analysis including multiplexed immunofluorescence (CODEX, Vectra), nucleus segmentation, tissue gra... |
| `pennylane` | Hardware-agnostic quantum ML framework with automatic differentiation. Use when training quantum circuits via gradients, building hybrid quantum-classical models, or n... |
| `pufferlib` | High-performance reinforcement learning framework optimized for speed and scale. Use when you need fast parallel training, vectorized environments, multi-agent systems... |
| `pyhealth` | Comprehensive healthcare AI toolkit for developing, testing, and deploying machine learning models with clinical data. This skill should be used when working with elec... |
| `pymoo` | Multi-objective optimization framework. NSGA-II, NSGA-III, MOEA/D, Pareto fronts, constraint handling, benchmarks (ZDT, DTLZ), for engineering design and optimization... |
| `research-lookup` | Look up current research information using Perplexity's Sonar Pro Search or Sonar Reasoning Pro models through OpenRouter. Automatically selects the best model based o... |

#### ToolUniverse (router in core: `tooluniverse`) (65)

| Skill | Purpose |
| :--- | :--- |
| `create-tooluniverse-skill` | Create high-quality ToolUniverse skills following test-driven, implementation-agnostic methodology. Integrates tools from ToolUniverse's 1,264+ tool library, creates m... |
| `devtu-auto-discover-apis` | Automatically discover life science APIs online, create ToolUniverse tools, validate them, and prepare integration PRs. Performs gap analysis to identify missing tool... |
| `devtu-create-tool` | Create new scientific tools for ToolUniverse framework with proper structure, validation, and testing. Use when users need to add tools to ToolUniverse, implement new... |
| `devtu-docs-quality` | Comprehensive documentation quality system combining automated validation with ToolUniverse-specific auditing. Detects outdated commands, circular navigation, inconsis... |
| `devtu-fix-tool` | Fix failing ToolUniverse tools by diagnosing test failures, identifying root causes, implementing fixes, and validating solutions. Use when ToolUniverse tools fail tes... |
| `devtu-github` | GitHub workflow for ToolUniverse - push code safely by moving temp files, activating pre-commit hooks, running tests, and cleaning staged files. Use when pushing to Gi... |
| `devtu-optimize-descriptions` | Optimize tool descriptions in ToolUniverse JSON configs for clarity and usability. Reviews descriptions for missing prerequisites, unexpanded abbreviations, unclear pa... |
| `devtu-optimize-skills` | Optimize ToolUniverse skills for better report quality, evidence handling, and user experience. Apply patterns like tool verification, foundation data layers, disambig... |
| `setup-tooluniverse` | Install and configure ToolUniverse with MCP integration for any AI coding client (Cursor, Codex Desktop, Windsurf, VS Code, Codex, Gemini CLI, Trae, Cline, Antigravity... |
| `tooluniverse-adverse-event-detection` | Detect and analyze adverse drug event signals using FDA FAERS data, drug labels, disproportionality analysis (PRR, ROR, IC), and biomedical evidence. Generates quantit... |
| `tooluniverse-antibody-engineering` | Comprehensive antibody engineering and optimization for therapeutic development. Covers humanization, affinity maturation, developability assessment, and immunogenicit... |
| `tooluniverse-binder-discovery` | Discover novel small molecule binders for protein targets using structure-based and ligand-based approaches. Creates actionable reports with candidate compounds, ADMET... |
| `tooluniverse-cancer-variant-interpretation` | Provide comprehensive clinical interpretation of somatic mutations in cancer. Given a gene symbol + variant (e.g., EGFR L858R, BRAF V600E) and optional cancer type, pe... |
| `tooluniverse-chemical-compound-retrieval` | Retrieves chemical compound information from PubChem and ChEMBL with disambiguation, cross-referencing, and quality assessment. Creates comprehensive compound profiles... |
| `tooluniverse-chemical-safety` | Comprehensive chemical safety and toxicology assessment integrating ADMET-AI predictions, CTD toxicogenomics, FDA label safety data, DrugBank safety profiles, and STIT... |
| `tooluniverse-clinical-guidelines` | Search and retrieve clinical practice guidelines across 12+ authoritative sources including NICE, WHO, ADA, AHA/ACC, NCCN, SIGN, CPIC, CMA, CTFPHC, GIN, MAGICapp, PubM... |
| `tooluniverse-clinical-trial-design` | Strategic clinical trial design feasibility assessment using ToolUniverse. Evaluates patient population sizing, biomarker prevalence, endpoint selection, comparator an... |
| `tooluniverse-clinical-trial-matching` | AI-driven patient-to-trial matching for precision medicine and oncology. Given a patient profile (disease, molecular alterations, stage, prior treatments), discovers a... |
| `tooluniverse-crispr-screen-analysis` | Comprehensive CRISPR screen analysis for functional genomics. Analyze pooled or arrayed CRISPR screens (knockout, activation, interference) to identify essential genes... |
| `tooluniverse-disease-research` | Generate comprehensive disease research reports using 100+ ToolUniverse tools. Creates a detailed markdown report file and progressively updates it with findings from... |
| `tooluniverse-drug-drug-interaction` | Comprehensive drug-drug interaction (DDI) prediction and risk assessment. Analyzes interaction mechanisms (CYP450, transporters, pharmacodynamic), severity classificat... |
| `tooluniverse-drug-repurposing` | Identify drug repurposing candidates using ToolUniverse for target-based, compound-based, and disease-driven strategies. Searches existing drugs for new therapeutic in... |
| `tooluniverse-drug-research` | Generates comprehensive drug research reports with compound disambiguation, evidence grading, and mandatory completeness sections. Covers identity, chemistry, pharmaco... |
| `tooluniverse-drug-target-validation` | Comprehensive computational validation of drug targets for early-stage drug discovery. Evaluates targets across 10 dimensions (disambiguation, disease association, dru... |
| `tooluniverse-epigenomics` | Production-ready genomics and epigenomics data processing for BixBench questions. Handles methylation array analysis (CpG filtering, differential methylation, age-rela... |
| `tooluniverse-expression-data-retrieval` | Retrieves gene expression and omics datasets from ArrayExpress and BioStudies with gene disambiguation, experiment quality assessment, and structured reports. Creates... |
| `tooluniverse-gene-enrichment` | Perform comprehensive gene enrichment and pathway analysis using gseapy (ORA and GSEA), PANTHER, STRING, Reactome, and 40+ ToolUniverse tools. Supports GO enrichment (... |
| `tooluniverse-gwas-drug-discovery` | Transform GWAS signals into actionable drug targets and repurposing opportunities. Performs locus-to-gene mapping, target druggability assessment, existing drug identi... |
| `tooluniverse-gwas-finemapping` | Identify and prioritize causal variants at GWAS loci using statistical fine-mapping and locus-to-gene predictions. Computes posterior probabilities for causal variants... |
| `tooluniverse-gwas-snp-interpretation` | Interpret genetic variants (SNPs) from GWAS studies by aggregating evidence from multiple databases (GWAS Catalog, Open Targets Genetics, ClinVar). Retrieves variant a... |
| `tooluniverse-gwas-study-explorer` | Compare GWAS studies, perform meta-analyses, and assess replication across cohorts. Integrates NHGRI-EBI GWAS Catalog and Open Targets Genetics to compare study design... |
| `tooluniverse-gwas-trait-to-gene` | Discover genes associated with diseases and traits using GWAS data from the GWAS Catalog (500,000+ associations) and Open Targets Genetics (L2G predictions). Identifie... |
| `tooluniverse-image-analysis` | Production-ready microscopy image analysis and quantitative imaging data skill for colony morphometry, cell counting, fluorescence quantification, and statistical anal... |
| `tooluniverse-immune-repertoire-analysis` | Comprehensive immune repertoire analysis for T-cell and B-cell receptor sequencing data. Analyze TCR/BCR repertoires to assess clonality, diversity, V(D)J gene usage,... |
| `tooluniverse-immunotherapy-response-prediction` | Predict patient response to immune checkpoint inhibitors (ICIs) using multi-biomarker integration. Given a cancer type, somatic mutations, and optional biomarkers (TMB... |
| `tooluniverse-infectious-disease` | Rapid pathogen characterization and drug repurposing analysis for infectious disease outbreaks. Identifies pathogen taxonomy, essential proteins, predicts structures,... |
| `tooluniverse-install-skills` | Detect and auto-install missing ToolUniverse research skills by checking common client skill directories and cloning from GitHub if absent. Use when ToolUniverse speci... |
| `tooluniverse-literature-deep-research` | Conduct comprehensive literature research with target disambiguation, evidence grading, and structured theme extraction. Creates a detailed report with mandatory compl... |
| `tooluniverse-metabolomics` | Comprehensive metabolomics research skill for identifying metabolites, analyzing studies, and searching metabolomics databases. Integrates HMDB (220k+ metabolites), Me... |
| `tooluniverse-metabolomics-analysis` | Analyze metabolomics data including metabolite identification, quantification, pathway analysis, and metabolic flux. Processes LC-MS, GC-MS, NMR data from targeted and... |
| `tooluniverse-multi-omics-integration` | Integrate and analyze multiple omics datasets (transcriptomics, proteomics, epigenomics, genomics, metabolomics) for systems biology and precision medicine. Performs c... |
| `tooluniverse-multiomic-disease-characterization` | Comprehensive multi-omics disease characterization integrating genomics, transcriptomics, proteomics, pathway, and therapeutic layers for systems-level understanding.... |
| `tooluniverse-network-pharmacology` | Construct and analyze compound-target-disease networks for drug repurposing, polypharmacology discovery, and systems pharmacology. Builds multi-layer networks from ChE... |
| `tooluniverse-pharmacovigilance` | Analyze drug safety signals from FDA adverse event reports, label warnings, and pharmacogenomic data. Calculates disproportionality measures (PRR, ROR), identifies ser... |
| `tooluniverse-phylogenetics` | Production-ready phylogenetics and sequence analysis skill for alignment processing, tree analysis, and evolutionary metrics. Computes treeness, RCV, treeness/RCV, par... |
| `tooluniverse-polygenic-risk-score` | Build and interpret polygenic risk scores (PRS) for complex diseases using GWAS summary statistics. Calculates genetic risk profiles, interprets PRS percentiles, and a... |
| `tooluniverse-precision-medicine-stratification` | Comprehensive patient stratification for precision medicine by integrating genomic, clinical, and therapeutic data. Given a disease/condition, genomic data (germline v... |
| `tooluniverse-precision-oncology` | Provide actionable treatment recommendations for cancer patients based on molecular profile. Interprets tumor mutations, identifies FDA-approved therapies, finds resis... |
| `tooluniverse-protein-interactions` | Analyze protein-protein interaction networks using STRING, BioGRID, and SASBDB databases. Maps protein identifiers, retrieves interaction networks with confidence scor... |
| `tooluniverse-protein-structure-retrieval` | Retrieves protein structure data from RCSB PDB, PDBe, and AlphaFold with protein disambiguation, quality assessment, and comprehensive structural profiles. Creates det... |
| `tooluniverse-protein-therapeutic-design` | Design novel protein therapeutics (binders, enzymes, scaffolds) using AI-guided de novo design. Uses RFdiffusion for backbone generation, ProteinMPNN for sequence desi... |
| `tooluniverse-proteomics-analysis` | Analyze mass spectrometry proteomics data including protein quantification, differential expression, post-translational modifications (PTMs), and protein-protein inter... |
| `tooluniverse-rare-disease-diagnosis` | Provide differential diagnosis for patients with suspected rare diseases based on phenotype and genetic data. Matches symptoms to HPO terms, identifies candidate disea... |
| `tooluniverse-rnaseq-deseq2` | Production-ready RNA-seq differential expression analysis using PyDESeq2. Performs DESeq2 normalization, dispersion estimation, Wald testing, LFC shrinkage, and result... |
| `tooluniverse-sdk` | Build AI scientist systems using ToolUniverse Python SDK for scientific research. Use when users need to access 1000++ scientific tools through Python code, create sci... |
| `tooluniverse-sequence-retrieval` | Retrieves biological sequences (DNA, RNA, protein) from NCBI and ENA with gene disambiguation, accession type handling, and comprehensive sequence profiles. Creates de... |
| `tooluniverse-single-cell` | Production-ready single-cell and expression matrix analysis using scanpy, anndata, and scipy. Performs scRNA-seq QC, normalization, PCA, UMAP, Leiden/Louvain clusterin... |
| `tooluniverse-spatial-omics-analysis` | Computational analysis framework for spatial multi-omics data integration. Given spatially variable genes (SVGs), spatial domain annotations, tissue type, and disease... |
| `tooluniverse-spatial-transcriptomics` | Analyze spatial transcriptomics data to map gene expression in tissue architecture. Supports 10x Visium, MERFISH, seqFISH, Slide-seq, and imaging-based platforms. Perf... |
| `tooluniverse-statistical-modeling` | Perform statistical modeling and regression analysis on biomedical datasets. Supports linear regression, logistic regression (binary/ordinal/multinomial), mixed-effect... |
| `tooluniverse-structural-variant-analysis` | Comprehensive structural variant (SV) analysis skill for clinical genomics. Classifies SVs (deletions, duplications, inversions, translocations), assesses pathogenicit... |
| `tooluniverse-systems-biology` | Comprehensive systems biology and pathway analysis using multiple pathway databases (Reactome, KEGG, WikiPathways, Pathway Commons, BioModels). Performs pathway enrich... |
| `tooluniverse-target-research` | Gather comprehensive biological target intelligence from 9 parallel research paths covering protein info, structure, interactions, pathways, expression, variants, drug... |
| `tooluniverse-variant-analysis` | Production-ready VCF processing, variant annotation, mutation analysis, and structural variant (SV/CNV) interpretation for bioinformatics questions. Parses VCF files (... |
| `tooluniverse-variant-interpretation` | Systematic clinical variant interpretation from raw variant calls to ACMG-classified recommendations with structural impact analysis. Aggregates evidence from ClinVar,... |

---

## 7. Commands & Triggers

| Command | Effect |
| :--- | :--- |
| `sync-pull` | Drive → this machine: master files, config, core, library (no deletions; moves demoted skills to the library), catalog rebuild, Claude Code MCP registration. |
| `sync-push` | This machine → Drive. Refuses to run if the core has more than 70 skills or if Drive holds library skills this machine lacks. |
| `build-skill-catalog.ps1` | Rebuilds `skill-catalog` from the local library. |
| `skill-pack.ps1 list \| status \| enable <pack> \| disable <pack>` | Workspace packs (section 1). |

**Natural-language triggering.** Describe the task (*"Evalúa la variante de KRT10 con AlphaGenome"*);
the agent finds the skill in the core or through `skill-catalog`. To force one, name it
(*"Usa `uniprot-database`"*). For long or parallel work, ask `juanjo-copilot` to delegate to
subagents ([SUBAGENTS_TEMPLATES_2026-10-01.md](SUBAGENTS_TEMPLATES_2026-10-01.md)).
