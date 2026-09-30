# 🌐 Global Master Catalog: Agents, Skills & Installed Open-Source Tools

> [!NOTE]
> **Global Access**: This master reference is stored globally at `C:\Users\Juanjo\.gemini\GLOBAL_AGENTS_AND_TOOLS.md` and registered in [GEMINI.md](file:///C:/Users/Juanjo/.gemini/GEMINI.md). You can reference and execute any tool or agent listed here from **any folder or workspace** on your machine.

---

## ⚡ 1. Primary Global Persona: `juanjo-copilot`

- **Execution Mode**: **Fast Mode / Allow Always** — Direct, autonomous code execution and problem-solving without interactive fluff.
- **Bilingual**: English and Spanish with high technical precision.
- **Integrated Knowledge Bases**:
  1. **DestiNA Genomics & Chemical Biology**: Dynamic Chemical Labeling (DCL), SMART Probes, PCR-free nucleic acid detection, miRNA biomarkers (miR-122 for liver toxicity / DILI), mass spec (MALDI-TOF / LC-MS).
  2. **Academic & Teaching (UGR - Química Física)**: Course administration (QF1 / QF2), lecture notes, interactive educational web applications, Google Sites continuous assessment hubs ("Evaluación Continua"), Genyo Fusion design system.
  3. **Biophysical Modeling & GDL-PNA**: Peptide Nucleic Acids (PNA) thermodynamics, duplex/triplex binding, Geometric Deep Learning (PyG) for nucleic acid analog design.
  4. **Genomics & Keratin Research (KRT10)**: Epidermolytic ichthyosis variants, filament mechanics, structural biology.
  5. **Quality & Compliance**: ISO 9001 and ISO 13485 metrics dashboards, validation checklists.
  6. **AI Provenance Hygiene & Watermark Stripping (`watermarks-remover`)**: Deterministic Layer A Unicode cleaning, Layer B stylometric rewriting and tone humanization, multi-format C2PA/EXIF/XMP metadata stripping for images, PDFs, Word docs, HTML, and Markdown.

---

## 📦 2. Installed Open-Source Scientific, AI & Provenance Stack

### Single-Cell Genomics & Transcriptomics

| Open-Source Package / Tool | Primary Function & Capabilities |
| :--- | :--- |
| **`drug2cell (v0.1.2)`** | Single-cell drug target mapping and per-cell drug activity scoring (d2c.score, d2c.gsea) with ChEMBL. |
| **`scanpy (v1.12.3)`** | Single-cell RNA-seq end-to-end analysis: QC, normalization, clustering, UMAP, marker identification. |
| **`anndata (v0.13.2)`** | Core annotated count matrix data structure (.h5ad) for single-cell data. |
| **`blitzgsea (v1.3.54)`** | High-speed Gene Set Enrichment Analysis (GSEA) and pathway ranking. |
| **`zarr (v3.3.0) & h5py (v3.16.0)`** | Chunked N-D array storage and HDF5 interfaces for large-scale multi-omics. |

### Cheminformatics & Chemical Biology

| Open-Source Package / Tool | Primary Function & Capabilities |
| :--- | :--- |
| **`analytical-chemistry-qc`** | Automated end-to-end processing and expert interpretation of raw ¹H/¹³C NMR (Bruker/Varian FID) and LC-MS (Shimadzu .lcd OLE2, .raw, .mzML) datasets. Executes group delay removal, FFT, phase optimization (ph0/ph1), AsLS baseline correction, pseudo-Voigt multiplet deconvolution, exchangeable proton detection (D2O shake comparison), UV purity integration (MaxPlot), and MS adduct deconvolutions (ES+/ES-). |
| **`nmrglue & pyopenms`** | Low-level NMR processing and LC-MS mass spectrometry feature extraction engines. |
| **`rdkit (v2026.3.1)`** | Comprehensive cheminformatics: 2D/3D structure generation, substructure searching, molecular descriptors. |
| **`SmilesPE (v0.0.3)`** | SMILES Pair Encoding tokenizer for chemical language models and representations. |
| **`R / Bioconductor qPCR Suite`** | Applied Biosystems QuantStudio .eds melt curve raw data extraction, Tm calculation, and derivative plotting. |

### Generative Molecular AI, OCSR & BioNeMo

| Open-Source Package / Tool | Primary Function & Capabilities |
| :--- | :--- |
| **`glyph (OCSRGlyph & MarkushGlyph)`** | State-of-the-art Optical Chemical Structure Recognition (OCSR). Translates molecular structure drawings from images into canonical SMILES (`OCSRGlyph`, Swin-B vision transformer) and patent Markush structures into CXSMILES with R-groups, positional attachments, and repeat units (`MarkushGlyph`, Qwen-based VLM). Local workspace at `K:\Mi unidad\Developer UGR\glyph`. |
| **`MegaMolBART / MolBART (Chemformer)`** | NVIDIA/AstraZeneca bidirectional chemical Seq2Seq BART transformer pre-trained on 1.4B SMILES strings. Used for *de novo* molecular generation, latent space optimization, retrosynthesis, and reaction outcome prediction. |
| **`bionemo-agent-toolkit`** | NVIDIA BioNeMo LLM agent tool calling layer for drug discovery microservices (ESM, AlphaFold, DiffDock). |
| **`assembly_go (Assembly-GO)`** | Assembly Theory molecular complexity quantification mapped to Gene Ontology biological pathways. |
| **`molecular_spaces`** | Chemical space cartography, latent space embeddings, and compound library diversity mapping. |
| **`tabfm`** | Tabular Foundation Models for zero-shot inference on clinical and assay spreadsheets. |

### Geometric Deep Learning & Neural Architectures

| Open-Source Package / Tool | Primary Function & Capabilities |
| :--- | :--- |
| **`torch (v2.13.0)`** | Core PyTorch tensor computation and deep neural network framework. |
| **`torch-geometric / PyG (v2.7.0)`** | Graph Neural Networks for molecular graphs, protein interfaces, and structural analogs. |
| **`e3nn (v0.6.0)`** | Euclidean E(3) equivariant steerable neural networks for 3D molecular symmetry and conformer modeling. |
| **`transformers (v5.15.0) & peft (v0.20.0)`** | Hugging Face transformer architectures and parameter-efficient fine-tuning. |
| **`umap-learn (v0.5.12)`** | Non-linear manifold learning for high-dimensional dimensionality reduction and visualization. |

### AI Provenance Hygiene, Watermark Removal & Document Cleaning (`watermarks-remover`)

| Tool / CLI Command | Scope & Capabilities |
| :--- | :--- |
| **`watermarks-remover`** | Master CLI entrypoint for all provenance and hygiene subcommands (`clean`, `inspect`, `text`, `audit`, `score`, `serve`). |
| **`wm-clean` / `clean_file.py`** | Unified multi-format metadata and watermark cleaner. Strips C2PA manifests, EXIF, XMP, and tracking metadata from images (`PNG`, `JPEG`, `WebP`, `SVG`), document containers (`PDF`, `DOCX`, `ODT`), HTML, and Markdown. |
| **`wm-inspect` / `inspect_file.py`** | Inspects files for provenance markers, C2PA Content Credentials, zero-width Unicode tracking characters, and AI metadata. |
| **`wm-text` / `clean_text.py`** | High-performance deterministic Layer A text hygiene: scrubs zero-width spaces, invisible tags, bidi overrides, and space homoglyphs while preserving semantic layouts. |
| **`wm-audit` / `audit_dir.py`** | Recursively scans directory trees to detect and report AI provenance signals across text, images, and documents. |
| **`wm-score` / `score_stylometry.py`** | Zero-LLM statistical & stylometric detector: scores burstiness variance, sentence cadence, and AI n-gram density. |
| **`wm-serve` / `server.py`** | Local HTTP microservice (`http://127.0.0.1:8765`) providing REST API endpoints (`/health`, `/capabilities`, `/inspect`, `/clean`, `/openapi.json`). |

### Data Science, Math & Systems

| Open-Source Package / Tool | Primary Function & Capabilities |
| :--- | :--- |
| **`polars & pandas (v3.0.0)`** | High-performance Arrow-native multithreaded and relational tabular processing. |
| **`scipy, numpy, sympy`** | Advanced scientific computing, numerical analysis, and symbolic mathematics. |

### Document Processing, Audio & Web

| Open-Source Package / Tool | Primary Function & Capabilities |
| :--- | :--- |
| **`magika (v1.0.3)`** | Google's deep learning file content-type and MIME detection engine (<5ms per file, ONNX runtime, 100+ binary and text formats). |
| **`PyMuPDF / pymupdf4llm (v1.27.2.3)`** | PDF parsing and structured Markdown extraction for scientific papers and lecture notes. |
| **`openai-whisper`** | Local audio transcription for lectures, meetings, and voice notes. |
| **`python-fasthtml, starlette, uvicorn`** | Modern Python asynchronous web application development. |
| **`graphifyy (v0.3.1)`** | Knowledge graph generation and community clustering from unstructured folders. |

---

## 🤖 3. Specialized Domain Agent Skills (239 Global Skills)

### 🧬 Genomics, Bioinformatics & Molecular Biology (49 Skills)

| Agent Skill Name | Purpose & Workflow Description |
| :--- | :--- |
| **`alphafold-database`** | Access AlphaFold 200M+ AI-predicted protein structures. Retrieve structures by UniProt ID, download PDB/mmCIF files, analyze confidence metrics (pLDDT, PAE), for drug discovery and structural biology. |
| **`alphafold-database-fetch-and-analyze`** | Retrieve and analyze AlphaFold predicted structures for a protein with pLDDT metrics. |
| **`alphagenome-atlas-website-links`** | Constructs deep-links and URLs for AlphaGenome Atlas (single-variant exploration 1-based chr:pos:ref>alt, locus views chr:start-end, reference vs alternate predictions). |
| **`alphagenome-single-variant-analysis`** | Analyzes genetic variant effects on gene expression, chromatin accessibility, and transcription factor binding. |
| **`alphagenome-variant-impact-score`** | Score, annotate, and analyze functional impact of genetic variants using AlphaGenome Variant Impact (AVI) scores and saturation mutagenesis window scans. |
| **`anndata`** | Data structure for annotated matrices in single-cell analysis (.h5ad). |
| **`arboreto`** | Infer gene regulatory networks (GRNs) from gene expression data using scalable algorithms (GRNBoost2, GENIE3). |
| **`biopython`** | Comprehensive molecular biology toolkit: sequences, alignments, BLAST automation, Entrez queries. |
| **`bioservices`** | Unified Python interface to 40+ bioinformatics services (UniProt, KEGG, ChEMBL, Reactome). |
| **`cellxgene-census`** | Query the CELLxGENE Census (61M+ cells) programmatically across tissues and cell types. |
| **`clinvar-database`** | Query NCBI ClinVar for variant clinical significance and pathogenicity classifications. |
| **`dbsnp-database`** | Look up, map, and search short genetic variants (SNPs, indels) in NCBI dbSNP. |
| **`deeptools`** | NGS analysis toolkit: BAM to bigWig conversion, QC, heatmaps/profiles for ChIP-seq, RNA-seq, ATAC-seq. |
| **`dnanexus-integration`** | DNAnexus cloud genomics platform SDK for pipeline execution. |
| **`embl-ebi-ols`** | Query EMBL-EBI Ontology Lookup Service for biomedical ontology terms across 250+ ontologies. |
| **`ena-database`** | Access European Nucleotide Archive via API/FTP for raw FASTQ and genome assemblies. |
| **`encode-ccres-database`** | Query ENCODE Registry of cis-Regulatory Elements (cCREs) via SCREEN GraphQL API. |
| **`ensembl-database`** | Query Ensembl genome database REST API for gene lookups, sequence retrieval, and VEP variant effect predictions. |
| **`etetoolkit`** | Phylogenetic tree toolkit for Newick manipulation, evolutionary events, and phylogenomics. |
| **`gene-database`** | Query NCBI Gene via E-utilities for RefSeqs, GO terms, chromosomal locations, and phenotypes. |
| **`geniml`** | Machine learning on genomic interval data (BED files, Region2Vec, BEDspace). |
| **`geo-database`** | Access NCBI GEO for gene expression microarray and RNA-seq datasets. |
| **`gget`** | Fast CLI/Python queries to 20+ bioinformatics databases. |
| **`gnomad-database`** | Query Genome Aggregation Database for allele frequencies and loss-of-function intolerance (pLI, LOEUF). |
| **`gtars`** | High-performance genomic interval analysis in Rust/Python. |
| **`gtex-database`** | Quantitative RNA expression data and variant eQTL information from GTEx Project across 54 tissue sites. |
| **`gwas-database`** | Query NHGRI-EBI GWAS Catalog for SNP-trait associations, p-values, and summary statistics. |
| **`human-protein-atlas-database`** | Semi-quantitative protein expression and spatial localization data from Human Protein Atlas (HPA). |
| **`interpro-database`** | Identify domains, families, and functional sites across 14 protein databases. |
| **`jaspar-database`** | Query JASPAR database for Transcription Factor (TF) binding profiles (PFMs/PWMs). |
| **`kegg-database`** | Direct REST API access to KEGG pathways, enzyme reactions, and metabolic networks. |
| **`ncbi-sequence-fetch`** | Retrieve protein and nucleotide sequences from NCBI databases using E-utilities. |
| **`pdb-database`** | Access RCSB PDB for experimentally determined 3D biomolecular structures and ligand complexes. |
| **`Protein Interaction Network Analysis`** | Analyze PPI networks using STRING, BioGRID, and SASBDB with confidence scores and functional enrichment. |
| **`protein-sequence-msa`** | Multiple sequence alignment of proteins using EBI Clustal Omega. |
| **`protein-sequence-similarity-search`** | Homologous protein sequence search via MMseqs2 or BLAST. |
| **`pydeseq2`** | Differential gene expression analysis (Python DESeq2) for bulk RNA-seq count matrices. |
| **`pymol`** | Molecular visualization, structural alignment, and publication-quality rendering with PyMOL. |
| **`pysam`** | SAM/BAM/CRAM alignments, VCF variants, and NGS coverage calculation. |
| **`quickgo-database`** | Query QuickGO and Evidence & Conclusion Ontology (ECO) REST API. |
| **`reactome-database`** | Query Reactome for biological pathways, enrichment, and reaction hierarchies. |
| **`scanpy`** | Single-cell RNA-seq analysis pipeline (QC, PCA, UMAP, Leiden clustering, marker genes). |
| **`scikit-bio`** | Biological data toolkit for alignments, phylogenetics, and microbiome diversity metrics (UniFrac, PCoA). |
| **`scvi-tools`** | Deep generative models for single-cell omics (scVI batch correction, differential expression). |
| **`string-database`** | Query STRING database for protein-protein interaction networks and pathway enrichment. |
| **`ucsc-conservation-and-tfbs`** | Fetch Evolutionary Conservation scores (phyloP, phastCons) and TFBS from UCSC Genome Browser. |
| **`unibind-database`** | Direct TF-DNA experimentally validated binding sites from UniBind. |
| **`uniprot-database`** | Query UniProtKB, Swiss-Prot, and TrEMBL for protein sequences, annotations, and functional features. |

### 🧪 Chemistry, Cheminformatics & Drug Discovery (19 Skills)

| Agent Skill Name | Purpose & Workflow Description |
| :--- | :--- |
| **`brenda-database`** | BRENDA enzyme database access: Km, kcat, reaction equations, and substrate kinetics. |
| **`chembl-database`** | Query ChEMBL bioactive molecules, drug targets, IC50/Ki bioactivities, and SAR data. |
| **`cobrapy`** | Constraint-based metabolic modeling (FBA, FVA, gene knockouts, SBML models). |
| **`datamol`** | Pythonic RDKit wrapper for molecular standardization, fingerprints, descriptors, and conformers. |
| **`deepchem`** | Molecular machine learning for ADMET, toxicity, and property prediction. |
| **`diffdock`** | Diffusion-based molecular docking for protein-ligand binding pose prediction. |
| **`drugbank-database`** | Comprehensive drug properties, mechanism of action, pharmacology, targets, and DDIs. |
| **`hmdb-database`** | Human Metabolome Database (220K+ metabolites) chemical properties, NMR/MS spectra, and pathways. |
| **`matchms`** | Mass spectrometry spectral similarity and unknown compound identification for metabolomics. |
| **`medchem`** | Medicinal chemistry filters: Lipinski Rule of 5, Veber, PAINS alerts, lead-likeness. |
| **`metabolomics-workbench-database`** | Access NIH Metabolomics Workbench for MS/NMR studies, metabolites, and biomarker discovery. |
| **`molfeat`** | Molecular featurization for ML (ECFP, MACCS, ChemBERTa embeddings). |
| **`opentargets-database`** | Query Open Targets Platform for target-disease associations, tractability, and drug validation. |
| **`pubchem-database`** | Query PubChem (110M+ compounds) by name, CID, SMILES, substructure, and bioassays. |
| **`pyopenms`** | Mass spectrometry analysis platform for LC-MS/MS proteomics and metabolomics pipelines. |
| **`pytdc`** | Therapeutics Data Commons datasets for ADME, toxicity, and drug-target interactions. |
| **`rdkit`** | Core cheminformatics toolkit for fine-grained 2D/3D molecular structure manipulation. |
| **`rowan`** | Cloud quantum chemistry: pKa prediction, conformer search, AutoDock Vina, and Boltz co-folding. |
| **`zinc-database`** | Access ZINC (230M+ purchasable compounds) for virtual screening and analog discovery. |

### 🏥 Clinical Research, Medical Data & Diagnostics (17 Skills)

| Agent Skill Name | Purpose & Workflow Description |
| :--- | :--- |
| **`clinical-decision-support`** | Clinical Decision Support reports, biomarker stratification, and GRADE evidence grading. |
| **`clinical-reports`** | Structured clinical reports (CARE case reports, ICH-E3 clinical trial reports, SOAP notes). |
| **`clinical-trials-database`** | Query ClinicalTrials.gov API v2 for trial eligibility, sponsors, conditions, and phases. |
| **`clinicaltrials-database`** | Structured ClinicalTrials.gov search and export workflows. |
| **`clinpgx-database`** | Pharmacogenomics gene-drug interactions, CPIC dosing guidelines, and allele function. |
| **`cosmic-database`** | Somatic mutations, Cancer Gene Census, and mutational signatures in oncology. |
| **`fda-database` / `openfda-database`** | OpenFDA API for adverse events (FAERS), recalls, 510(k), and drug labels. |
| **`imaging-data-commons`** | Query and download public cancer imaging data (DICOM CT, MR, PET, pathology WSIs). |
| **`iso-13485-certification`** | Medical device QMS documentation, gap analysis, and Quality Manual preparation. |
| **`neurokit2`** | Biosignal processing for ECG, EEG, EDA, RSP, PPG, EMG, and heart rate variability (HRV). |
| **`neuropixels-analysis`** | Neuropixels extracellular electrophysiology, spike sorting (Kilosort4), and unit curation. |
| **`pydicom`** | Medical imaging DICOM parsing, pixel extraction, anonymization, and format conversion. |
| **`pyhealth`** | Healthcare AI toolkit for EHR modeling, clinical prediction, and ICD/NDC coding. |
| **`treatment-plans`** | Concise, focused medical treatment plans with SMART goals and evidence-based regimens. |

### 🔬 Lab Automation & Cloud Biotech Platforms (10 Skills)

| Agent Skill Name | Purpose & Workflow Description |
| :--- | :--- |
| **`adaptyv`** | Automated wet-lab protein testing: binding assays, stability, expression optimization. |
| **`benchling-integration`** | Benchling ELN, registry, inventory, and API workflow automation. |
| **`flowio`** | Flow cytometry FCS file parsing, channel extraction, and event processing. |
| **`histolab`** | WSI tile extraction, tissue detection, and stain normalization for pathology slides. |
| **`labarchive-integration`** | Electronic Lab Notebook API integration for programmatic documentation and backups. |
| **`lamindb`** | FAIR data lakehouse framework for biological datasets, ontologies, and workflow lineage. |
| **`latchbio-integration`** | Latch platform serverless bioinformatics workflows and Nextflow integration. |
| **`omero-integration`** | Microscopy image management, ROI annotations, and high-content screening. |
| **`opentrons-integration`** | Official Opentrons Protocol API v2 for OT-2 and Flex liquid handlers. |
| **`pylabrobot`** | Vendor-agnostic lab automation framework for Hamilton, Tecan, and Opentrons robots. |

### 🤖 Machine Learning, Deep Learning & Optimization (14 Skills)

| Agent Skill Name | Purpose & Workflow Description |
| :--- | :--- |
| **`aeon`** | Time series machine learning: classification, forecasting, anomaly detection. |
| **`dask`** | Distributed computing for out-of-core pandas/NumPy pipelines across clusters. |
| **`esm`** | Meta protein language models (ESM3, ESM C) for embeddings, generative design, and inverse folding. |
| **`modal`** | Cloud serverless containers, GPUs, and autoscaling for scientific ML models. |
| **`polars`** | Blazing-fast in-memory DataFrame library with lazy evaluation and Apache Arrow backend. |
| **`pufferlib`** | High-performance reinforcement learning framework with vectorized environments. |
| **`pymoo`** | Multi-objective optimization framework (NSGA-II, NSGA-III, Pareto fronts). |
| **`pytorch-lightning`** | Scalable PyTorch engineering with LightningModules, multi-GPU training, and callbacks. |
| **`scikit-learn`** | Core Python machine learning: classification, regression, clustering, preprocessing. |
| **`scikit-survival`** | Survival analysis and time-to-event modeling (Cox models, Survival Forests). |
| **`shap`** | Model interpretability, SHAP values, feature importance, and explainable AI plots. |
| **`stable-baselines3`** | Production-ready RL algorithms (PPO, SAC, DQN, TD3) with Gymnasium environments. |
| **`torch-geometric`** | PyG Graph Neural Networks for node/graph classification and molecular graphs. |
| **`transformers`** | Hugging Face Transformers for text, vision, audio, and multimodal foundation models. |

### 📊 Scientific Computing, Math & Simulations (25 Skills)

| Agent Skill Name | Purpose & Workflow Description |
| :--- | :--- |
| **`astropy`** | Celestial coordinates, FITS file manipulation, and astrophysical calculations. |
| **`cirq`** | Google Quantum AI framework for noise-aware quantum circuits and NISQ experiments. |
| **`datacommons-client`** | Query public demographic, economic, and environmental statistics from Data Commons. |
| **`fluidsim`** | Computational fluid dynamics (Navier-Stokes, turbulence, spectral methods). |
| **`fred-economic-data`** | Access 800,000+ macroeconomic time series from the Federal Reserve Economic Data API. |
| **`geopandas`** | Geospatial vector data processing, spatial joins, and coordinate transformations. |
| **`matlab`** | MATLAB / GNU Octave numerical computing, matrix calculations, and algorithm migration. |
| **`matplotlib`** | Fine-grained scientific plotting and publication-ready vector graphic generation. |
| **`networkx`** | Complex graph algorithms, centrality metrics, and network topology analysis. |
| **`pennylane`** | Hardware-agnostic quantum ML with automatic differentiation (PyTorch/JAX). |
| **`plotly`** | Interactive web visualizations, dashboards, and responsive charts. |
| **`pymatgen`** | Materials science crystallography, phase diagrams, and Materials Project integration. |
| **`pymc-bayesian-modeling`** | Probabilistic programming, MCMC (NUTS), and hierarchical Bayesian models. |
| **`qiskit`** | IBM Quantum computing framework for circuit design and quantum error mitigation. |
| **`qutip`** | Open quantum system dynamics, Lindblad master equations, and cavity QED simulations. |
| **`seaborn`** | Statistical data visualization with attractive default distributions and heatmaps. |
| **`simpy`** | Process-based discrete-event simulation for queues, operations, and logistics. |
| **`statistical-analysis`** | Guided statistical test selection, assumption checks, and APA reporting. |
| **`statsmodels`** | Econometrics and statistical models: OLS, GLM, mixed models, ARIMA. |
| **`sympy`** | Symbolic algebra, calculus, exact solutions, and mathematical code generation. |
| **`vaex`** | Out-of-core DataFrame analytics for billion-row datasets exceeding RAM. |
| **`zarr-python`** | Chunked, compressed N-dimensional array storage for cloud and local scientific arrays. |

### 📑 Literature Research, Writing, Slides & Publications (34 Skills)

| Agent Skill Name | Purpose & Workflow Description |
| :--- | :--- |
| **`anydoc`** | Convert Word, PowerPoint, Excel, ODT, EPUB, RTF, and PDF documents to GitHub-flavored Markdown. |
| **`biorxiv-database` / `literature-search-biorxiv`** | Query bioRxiv and medRxiv preprint servers by DOI, keywords, and dates. |
| **`citation-management`** | Google Scholar / PubMed search, DOI validation, and BibTeX entry formatting. |
| **`denario`** | Multiagent AI workflow from scientific hypothesis generation to LaTeX publication. |
| **`infographics`** | Professional scientific infographics and visual summaries. |
| **`latex-posters` / `pptx-posters`** | Conference research posters in LaTeX (beamerposter) or web-native HTML/PPTX. |
| **`literature-review`** | Systematic literature reviews across PubMed, arXiv, and Semantic Scholar with citations. |
| **`literature-search-arxiv`** | Query arXiv for physics, math, and AI preprints and download full-text PDFs. |
| **`literature-search-europepmc`** | Europe PMC full-text scientific literature access and citation graph exploration. |
| **`literature-search-openalex` / `openalex-database`** | Query 240M+ scholarly works, h-index, and author bibliometrics in OpenAlex. |
| **`markdown-presentation` / `markdown-slides`** | Presenter-friendly Markdown slide decks compatible with Marp and Deckset. |
| **`markitdown`** | Multi-format file conversion to Markdown (PDF, DOCX, XLSX, audio, images). |
| **`paper-2-web`** | Convert scientific papers to interactive websites, video abstracts, and posters. |
| **`peer-review` / `scientific-manuscript-review`** | Structured peer reviews assessing methodology, statistical validity, and clarity. |
| **`predictingthepast`** | Ancient epigraphic text restoration and contextualization via Ithaca / Aeneas. |
| **`pubmed-database`** | Direct NCBI PubMed queries, MeSH term searching, and citation linking. |
| **`research-grants`** | Competitive grant proposal writing for NIH, NSF, ISCIII, and EU Horizon frameworks. |
| **`research-lookup` / `perplexity-search`** | Grounded real-time academic search with citations via Sonar models. |
| **`scholar-evaluation`** | Quantitative ScholarEval framework for research paper quality scoring. |
| **`scientific-brainstorming` / `hypothesis-generation`** | Creative scientific ideation and testable hypothesis formulation. |
| **`scientific-critical-thinking`** | GRADE evidence quality assessment and experimental bias detection. |
| **`scientific-schematics`** | Publication-quality biological pathways, neural architectures, and system flowcharts. |
| **`scientific-slides`** | PowerPoint and LaTeX Beamer slides for academic and research conferences. |
| **`scientific-visualization`** | Multi-panel, colorblind-safe publication figures (Nature/Science/Cell style). |
| **`scientific-writing`** | Deep research prose manuscript drafting following IMRAD guidelines. |
| **`uspto-database`** | USPTO patent examination history, assignments, and prior art searches. |
| **`venue-templates`** | Formatting templates for Nature, Science, IEEE, ACM, NeurIPS, and NIH grants. |

### ✍️ Content Refinement, Voice Personas & Provenance Hygiene (7 Skills)

| Agent Skill Name | Purpose & Workflow Description |
| :--- | :--- |
| **`clean-user-facing-text`** | Clean and finalize authorized prose by auditing suspicious invisible Unicode, zero-width tracking markers, and homoglyphs, and rewriting formulaic AI cadence while preserving claims, facts, code, and citations. |
| **`remove-ai-marks`** | Full provenance hygiene suite for multi-vendor AI marks: invisible Unicode (Layer A), statistical text watermarks via rewrite (Layer B), and C2PA / EXIF / XMP metadata stripping on PNG, JPEG, WebP, SVG, PDF, DOCX, ODT, HTML, MD. |
| **`humanizer`** | General AI writing removal: eliminates passive filler, em dash overuse, rule-of-three formulas, and robotic cadence. |
| **`humanizer-juanjo`** | Juanjo's executive English voice: composed, technically specific, authoritative, action-oriented. |
| **`humanizer-juanjo-es`** | Juanjo's executive Spanish voice: natural plural, structured headers, high domain precision. |
| **`humanizer-hugh`** | Warm, conversational, professional-personal writing style calibration. |
| **`no-ai-slop`** | Sharpen drafts into direct, human prose or detect AI writing patterns without rewriting. |

### 🛠️ Developer Tools, System & Customization (23 Skills)

| Agent Skill Name | Purpose & Workflow Description |
| :--- | :--- |
| **`agy-customizations`** | Comprehensive reference for Antigravity skills, rules, plugins, hooks, and MCP servers. |
| **`antigravity-guide`** | Sitemap, CLI commands, and customization guide for Google Antigravity. |
| **`create-tooluniverse-skill`** | Create new ToolUniverse skills following test-driven methodologies. |
| **`credentials`** | Secure handling and validation of API keys and credentials. |
| **`devtu-auto-discover-apis`** | Systematic life science API discovery and integration wrapper generation. |
| **`devtu-create-tool`** | Implement and test new ToolUniverse tool classes. |
| **`devtu-docs-quality`** | Automated documentation quality auditing and link verification. |
| **`devtu-fix-tool`** | Diagnose and fix failing ToolUniverse tools. |
| **`devtu-github`** | Safe git workflows, pre-commit validation, and test runs. |
| **`devtu-optimize-descriptions`** | Enhance tool descriptions and API usability in ToolUniverse. |
| **`devtu-optimize-skills`** | Optimize skills for report quality, evidence grading, and completeness. |
| **`gemini-interactions-api`** | Interactions API SDK for text, multimodal, function calling, and structured outputs. |
| **`gemini-live-api-dev`** | Bidirectional real-time streaming with Gemini Live WebSocket API. |
| **`get-available-resources`** | System resource detection (CPU, GPU, RAM, disk) to optimize parallel compute strategies. |
| **`graphify`** | Transform folders, codebases, or papers into clustered interactive knowledge graphs. |
| **`magika`** | AI file content-type and MIME identification using Google's ONNX deep-learning model (<5ms/file). |
| **`multi-agent-orchestrator`** | Orchestrates high-throughput parallel subagent workflows (`define_subagent` + `invoke_subagent`), isolated workspace branching (`Workspace: "branch"`), zero-polling reactive wakeup, and autonomous auto-fix remediation loops. |
| **`offer-k-dense-web`** | K-Dense Web integration for complex scientific workflows. |
| **`permissioned-github`** | Safe GitHub operations with permission gating. |
| **`setup-tooluniverse`** | MCP server configuration and ToolUniverse environment management. |
| **`uv`** | Fast Python package management and virtual environment management via `uv`. |
| **`workflow-skill-creator`** | Distill completed user workflows into reusable agent skills. |

### 🌐 ToolUniverse Specialized Multi-Agent Skills (52 Domain Agents)

| Agent Skill Name | Purpose & Workflow Description |
| :--- | :--- |
| **`tooluniverse`** | Master router skill dispatching across 1,400+ scientific database and analytics tools. |
| **`tooluniverse-adverse-event-detection`** | Pharmacovigilance safety signal detection via FDA FAERS, PRR, ROR, and IC scores. |
| **`tooluniverse-antibody-engineering`** | Humanization, affinity maturation, and developability assessment for therapeutic antibodies. |
| **`tooluniverse-binder-discovery`** | Structure- and ligand-based virtual screening for novel small-molecule protein binders. |
| **`tooluniverse-cancer-variant-interpretation`** | Somatic cancer mutation interpretation via CIViC, cBioPortal, and clinical trials. |
| **`tooluniverse-chemical-compound-retrieval`** | PubChem / ChEMBL compound profiling, SMILES disambiguation, and bioactivity data. |
| **`tooluniverse-chemical-safety`** | Toxicogenomics, ADMET-AI predictions, Ames mutagenicity, and DILI risk scoring. |
| **`tooluniverse-clinical-guidelines`** | Evidence-based clinical guidelines synthesis and therapeutic algorithms. |
| **`tooluniverse-clinical-trial-design`** | Biomarker-driven trial feasibility, patient cohort sizing, and endpoint selection. |
| **`tooluniverse-clinical-trial-matching`** | Precision patient-to-trial matching based on molecular alterations and stage. |
| **`tooluniverse-crispr-screen-analysis`** | Pooled/arrayed CRISPR screen processing (MAGeCK, BAGEL) for essential gene identification. |
| **`tooluniverse-disease-research`** | 10-dimensional systematic disease characterization reports. |
| **`tooluniverse-drug-drug-interaction`** | CYP450, transporter, and pharmacodynamic DDI risk evaluation and polypharmacy management. |
| **`tooluniverse-drug-repurposing`** | Systematic indication expansion for approved drugs via targets and safety data. |
| **`tooluniverse-drug-research`** | Comprehensive drug profiles: chemistry, targets, pharmacology, ADMET, and clinical trials. |
| **`tooluniverse-drug-target-validation`** | 10-dimension computational target validation and druggability scoring (0-100). |
| **`tooluniverse-epigenomics`** | DNA methylation array processing (CpG filtering), ChIP-seq peak calling, and ATAC-seq. |
| **`tooluniverse-expression-data-retrieval`** | ArrayExpress and BioStudies dataset profiling and expression matrix downloads. |
| **`tooluniverse-gene-enrichment`** | GO (BP/MF/CC), KEGG, Reactome, and Enrichr pathway over-representation analysis. |
| **`tooluniverse-gwas-drug-discovery`** | Translate GWAS risk signals into druggable therapeutic targets and repurposing leads. |
| **`tooluniverse-gwas-finemapping`** | Statistical fine-mapping and locus-to-gene (L2G) causal variant prioritization. |
| **`tooluniverse-gwas-snp-interpretation`** | Interpret GWAS variants (rsIDs) with ClinVar, GWAS Catalog, and Open Targets. |
| **`tooluniverse-gwas-study-explorer`** | Multi-cohort GWAS meta-analysis and genetic architecture comparison. |
| **`tooluniverse-gwas-trait-to-gene`** | Trait-to-gene discovery mapping phenotypic risk to causal genes. |
| **`tooluniverse-image-analysis`** | Quantitative microscopy morphometry, colony counting, and statistical testing. |
| **`tooluniverse-immune-repertoire-analysis`** | TCR/BCR clonality, V(D)J gene usage, CDR3 diversity, and epitope specificity. |
| **`tooluniverse-immunotherapy-response-prediction`** | Multi-biomarker ICI response scoring (TMB, MSI, PD-L1, immune microenvironment). |
| **`tooluniverse-infectious-disease`** | Pathogen genomics, essential target identification, and rapid antiviral screening. |
| **`tooluniverse-install-skills`** | Auto-detection and installation of missing ToolUniverse domain skills. |
| **`tooluniverse-literature-deep-research`** | Collision-aware literature deep research with evidence grading and synthesis. |
| **`tooluniverse-metabolomics`** | HMDB and MetaboLights metabolite profiling and study searches. |
| **`tooluniverse-metabolomics-analysis`** | Differential metabolite discovery, LC-MS/GC-MS quantification, and flux balance analysis. |
| **`tooluniverse-multi-omics-integration`** | Cross-omics integration (RNA-seq, proteomics, epigenomics, metabolomics) via MOFA+. |
| **`tooluniverse-multiomic-disease-characterization`** | 8-layer multi-omics disease profiling and mechanistic hypothesis generation. |
| **`tooluniverse-network-pharmacology`** | Compound-target-disease network topology, polypharmacology, and synergy prediction. |
| **`tooluniverse-pharmacovigilance`** | FDA FAERS disproportionality metrics and post-market safety signal surveillance. |
| **`tooluniverse-phylogenetics`** | Phylogenetic tree construction (NJ/UPGMA), bootstrap support, and evolutionary rates. |
| **`tooluniverse-polygenic-risk-score`** | PRS calculation and genetic predisposition profiling for complex diseases. |
| **`tooluniverse-precision-medicine-stratification`** | 9-phase patient risk tier assignment and targeted therapy selection. |
| **`tooluniverse-precision-oncology`** | Actionable tumor mutation interpretation, FDA therapy matching, and resistance analysis. |
| **`tooluniverse-protein-structure-retrieval`** | PDB, PDBe, and AlphaFold 3D structure retrieval and quality assessment. |
| **`tooluniverse-protein-therapeutic-design`** | AI-guided de novo protein design using RFdiffusion and ProteinMPNN. |
| **`tooluniverse-proteomics-analysis`** | MaxQuant/DIA-NN proteomics data processing, PTM analysis, and differential expression. |
| **`tooluniverse-rare-disease-diagnosis`** | HPO phenotype matching, Orphanet/OMIM differential diagnosis, and VUS interpretation. |
| **`tooluniverse-rnaseq-deseq2`** | Production-ready RNA-seq differential expression analysis with PyDESeq2. |
| **`tooluniverse-sdk`** | Python SDK programmatic orchestration of 1,000+ scientific tools. |
| **`tooluniverse-sequence-retrieval`** | NCBI/ENA biological sequence retrieval (DNA, RNA, proteins, assemblies). |
| **`tooluniverse-spatial-omics-analysis`** | Spatial transcriptomics (Visium, MERFISH) domain characterization and cell-cell interaction. |
| **`tooluniverse-spatial-transcriptomics`** | Spatial gene expression mapping, clustering, and tumor microenvironment architecture. |
| **`tooluniverse-statistical-modeling`** | Linear, logistic, and Cox regression modeling for biomedical datasets. |
| **`tooluniverse-structural-variant-analysis`** | Clinical structural variant (SV/CNV) classification and dosage sensitivity interpretation. |
| **`tooluniverse-systems-biology`** | Multi-database pathway analysis (Reactome, KEGG, WikiPathways, BioModels). |
| **`tooluniverse-target-research`** | 9-pathway comprehensive drug target intelligence and druggability profiling. |
| **`tooluniverse-variant-analysis`** | High-throughput VCF parsing, variant annotation, and clinical filtering. |
| **`tooluniverse-variant-interpretation`** | ACMG-guided clinical variant interpretation and pathogenicity scoring. |
| **`paper2agent`** | Convert scientific papers (PDF, spreadsheets, figures) and code into reviewed agent skills and MCP servers. |
| **`albatross-rna-paper`** | Structured reading package, figures, and datasets for Albatross RNA Language Model & IRES structural biology (Sychla et al., bioRxiv 2026). |

---

## 🚀 4. How to Trigger from Any Workspace

### Direct CLI Commands (Available Globally in Any Terminal)
- `watermarks-remover --help` — Master CLI for all provenance hygiene tools.
- `wm-clean <file> [-o <output>]` — Strip C2PA/EXIF/XMP metadata and invisible marks from images, PDFs, Word docs, Markdown, and text.
- `wm-inspect <file>` — Inspect files for provenance signals, C2PA Content Credentials, and hidden Unicode.
- `wm-text <file> [-o <output>] [--stats]` — Fast deterministic Layer A text scrubbing.
- `wm-audit <directory> [--check-stylometry]` — Audit an entire folder or repository for AI watermarks and metadata.
- `wm-score <file> [--explain]` — Score text stylometry, cadence, burstiness, and AI cadence markers.
- `wm-serve [--port 8765]` — Run the local background REST microservice.

### Natural Language Agent Triggering
1. **Automatic Detection**: Describe your task naturally (*"Clean this manuscript of AI tracking markers and metadata"*, *"Audit the current directory for AI provenance"*, or *"Evaluate KRT10 variant pLDDT with AlphaFold"*).
2. **Explicit Skill Activation**: State the skill directly (*"Use `remove-ai-marks` on this PDF"* or *"Use `clean-user-facing-text` on my course syllabus"*).
3. **Parallel Background Subagents**: Ask `juanjo-copilot` to spawn subagents for multi-database research pipelines or bulk provenance audits.
