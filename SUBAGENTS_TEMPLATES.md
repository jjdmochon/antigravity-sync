# 🚀 Global Subagent Orchestration, Interactive UI & Process Governance Templates

> [!NOTE]
> **Global Reference**: This template guide is stored globally at `C:\Users\Juanjo\.gemini\SUBAGENTS_TEMPLATES.md` and registered in [GEMINI.md](file:///C:/Users/Juanjo/.gemini/GEMINI.md). You can reference, customize, or trigger any of these subagent patterns from **any folder or workspace** on your machine.

---

## 🏗️ 1. The Complete 5-Tool Antigravity Architecture

```mermaid
flowchart TD
    User["Developer / User Input"] --> Parent["1. Parent Orchestrator (Conversation ID: parent-id)
Main Context Clean & Sharp"]
    
    subgraph HITL["Human-in-the-Loop & Visual Studio (Parts 1 & 2)"]
        Parent -->|1. Hydrate user_prefs.json| State["Workspace State Hydration"]
        State -->|2. ask_question| UI["Interactive UI Modals"]
        Parent -->|3. generate_image| VisualStudio["Visual Asset Studio (SCENE + CAMERA + LIGHTING)"]
        VisualStudio -->|4. ask_question| Review{"Keep / Regenerate?"}
        Review -->|Keep| SaveAsset["Persist to public/images/"]
    end
    
    subgraph Execution["Parallel Swarm Execution & Governance (Parts 3, 4 & 5)"]
        Parent -->|define_subagent| Reg["Persona Registry (Least Privilege)"]
        Parent -->|invoke_subagent (Workspace: 'branch')| Swarm["Parallel Subagent Swarm"]
        Swarm --> W1["Worker 1 (Milestones 1-4)"]
        Swarm --> W2["Worker 2 (Milestones 1-4)"]
        W1 -.->|send_message (JSON Telemetry)| Parent
        W2 -.->|send_message (Fatal Alarm)| Parent
        Parent -->|manage_subagents: list| Audit["Fleet Auditing"]
        Parent -->|manage_subagents: kill_all| Kill["Hard Circuit Breaker (SIGKILL)"]
    end
```

---

## 🛡️ 2. The Complete 14 Anti-Patterns to Prevent

### Interactive UI Anti-Patterns (`ask_question`):
1. **Never Cause Option-Fatigue:** Keep option arrays strictly under 5–7 items; use pre-filtering for large datasets.
2. **Never Add Explicit "Other" / "Custom" Options:** Antigravity provides a default write-in text field automatically.
3. **Never Use Flat Root Keys in Configs:** Always namespace keys under a domain block (`"FORMS"`, `"TESTING"`, `"BIOCHEM"`) in `user_prefs.json`.
4. **Never Use Third-Person Phrasing:** Format options as direct user responses (*"Client-side validation"*), not imperative commands.

### Visual Asset Anti-Patterns (`generate_image`):
5. **Never Use Raw Prompt Injection:** Always parameterize prompts using structured tokens (`[SCENE]`, `[CAMERA]`, `[LIGHTING]`, `[STYLE]`).
6. **Never Store Assets in Volatile `/tmp`:** Always copy approved images to permanent project directories (`public/images/`) with absolute paths.
7. **Never Make Redundant Generation Calls:** Verify whether the target asset already exists on disk before triggering `generate_image`.

### Orchestration Anti-Patterns (`define_subagent` / `invoke_subagent`):
8. **Never Over-Permission Workers:** Practice least privilege (`enable_write_tools: false` if read-only; `enable_subagent_tools: false`).
9. **Never Tight-Loop Poll:** Never call `manage_task(Action='status')` or sleep in loops. Antigravity handles reactive wakeup automatically.
10. **Never Use Un-Scoped Prompts:** Provide 100% self-contained prompts with explicit paths, commands, and parent IDs.
11. **Always Isolate Modifying Tasks:** Use `Workspace: "branch"` for builds, tests, or file edits.

### Messaging & Governance Anti-Patterns (`send_message` / `manage_subagents`):
12. **Never Allow Unbounded Ping-Pong Loops:** Always require an explicit `STATUS: COMPLETE` or `TERMINATE` flag.
13. **Never Send Un-Grounded Messages:** Explicitly inject the parent `Conversation ID` in launch prompts.
14. **Never Send Free-Form Text Dumps:** Transmit structured JSON strings or strict prefix tags (`[PROGRESS]`, `[ERROR]`, `[ABORT]`).

---

## 📑 3. Master Template Catalog

1. [Template 1: Multi-Omics Disease & Target Dossier](#template-1-multi-omics-disease--target-dossier)
2. [Template 2: DestiNA DCL Chemistry & miRNA Biomarker Validation](#template-2-destina-dcl-chemistry--mirna-biomarker-validation)
3. [Template 3: KRT10 Variant & PNA Probe Biophysics Campaign](#template-3-krt10-variant--pna-probe-biophysics-campaign)
4. [Template 4: Single-Cell Drug Repurposing (drug2cell + ChEMBL)](#template-4-single-cell-drug-repurposing-drug2cell--chembl)
5. [Template 5: UGR Academic Courseware & Interactive Web Hub](#template-5-ugr-academic-courseware--interactive-web-hub)
6. [Template 6: ISO 9001 / ISO 13485 Compliance & Audit Checklist](#template-6-iso-9001--iso-13485-compliance--audit-checklist)
7. [Template 7: Rapid Multi-Database Literature & Patent Prior Art Survey](#template-7-rapid-multi-database-literature--patent-prior-art-survey)
8. [Template 8: Autonomous Dual 'Builder + Auditor' Loop (/goal Pattern)](#template-8-autonomous-dual-builder--auditor-loop-goal-pattern)
9. [Template 9: Autonomous Document Production & 3-Stage Provenance Review Pipeline](#template-9-autonomous-document-production--3-stage-provenance-review-pipeline)
10. [Template 10: Batch Test Execution & Autonomous Auto-Remediation Loop](#template-10-batch-test-execution--autonomous-auto-remediation-loop)
11. [Template 11: Multi-Step Telemetry Pipeline with Live Dashboard](#template-11-multi-step-telemetry-pipeline-with-live-dashboard)
12. [Template 12: Automated Hard Circuit Breaker & Fleet Governance](#template-12-automated-hard-circuit-breaker--fleet-governance)
13. [Template 13: Interactive Technical Interviewer & Round-Trip State Hydration](#template-13-interactive-technical-interviewer--round-trip-state-hydration)
14. [Template 14: Visual Asset Generation & Composition Studio](#template-14-visual-asset-generation--composition-studio)
15. [Template 15: DeepMind AlphaGenome & Variant Impact Discovery Swarm](#template-15-deepmind-alphagenome--variant-impact-discovery-swarm)
16. [Template 16: Ancient Epigraphic Restoration & Contextualization Campaign (Aeneas & Ithaca)](#template-16-ancient-epigraphic-restoration--contextualization-campaign-aeneas--ithaca)
17. [Template 17: High-Throughput Deep Learning File Ingestion & Security Audit (Magika)](#template-17-high-throughput-deep-learning-file-ingestion--security-audit-magika)

---

## Template 1: Multi-Omics Disease & Target Dossier
**Use Case**: Comprehensive target validation connecting clinical genetics, protein structures, and pharmacology without context flooding.

### 📋 Natural Language Trigger:
```text
In parallel, dispatch dedicated subagents to generate a target dossier for [TARGET_GENE, e.g., KRT10 or EGFR] across isolated branches. Register specialized worker personas and return a unified dossier.
```

---

## Template 2: DestiNA DCL Chemistry & miRNA Biomarker Validation
**Use Case**: Validating a Dynamic Chemical Labeling (DCL) assay for diagnostic microRNA detection.

### 📋 Natural Language Trigger:
```text
Run the local DCL calibration analysis on my CSV data in data/, and simultaneously spawn parallel subagents across isolated branches to evaluate clinical biomarker literature and probe sequence specificity.
```

---

## Template 3: KRT10 Variant & PNA Probe Biophysics Campaign
**Use Case**: Designing Peptide Nucleic Acid (PNA) or SMART probes to discriminate specific epidermal mutations.

### 📋 Natural Language Trigger:
```text
In parallel, launch subagents across isolated branches to design a PNA targeting strategy for [MUTATION, e.g., KRT10 R156C]:
1. Subagent 1: Model PNA:RNA duplex melting temperatures (Tm) and delta-Tm discrimination penalty.
2. Subagent 2: Evaluate steric accessibility using 3D conformers.
3. Subagent 3: Search USPTO for patented PNA modifications targeting keratin genes.
Compile candidate ranking table to reports/pna/candidates.md.
```

---

## Template 4: Single-Cell Drug Repurposing (drug2cell + ChEMBL)
**Use Case**: Mapping drug targets and identifying therapeutic candidates across single-cell clusters.

### 📋 Natural Language Trigger:
```text
Process the single-cell AnnData (.h5ad) object using Scanpy, and simultaneously dispatch parallel subagents in isolated branches to:
1. Subagent A: Run drug2cell (d2c.score and d2c.gsea) against ChEMBL clinical-stage compounds.
2. Subagent B: Run BlitzGSEA across Reactome and KEGG pathways for top cluster markers.
Synthesize findings into an interactive UMAP visualization.
```

---

## Template 5: UGR Academic Courseware & Interactive Web Hub
**Use Case**: Rapidly building teaching materials and interactive single-page educational tools for Química Física.

### 📋 Natural Language Trigger:
```text
For UGR [COURSE, e.g., Química Farmacéutica I - Tema 3], launch parallel subagents in isolated workspace branches:
1. Subagent 1 (Web App): Build a standalone HTML5/CSS3 simulator using the Genyo Fusion design system.
2. Subagent 2 (Quiz): Generate a 10-question formative assessment with interactive flashcard reveals.
3. Subagent 3 (Summary): Extract key formulas and concepts into a concise study guide.
```

---

## Template 6: ISO 9001 / ISO 13485 Compliance & Audit Checklist
**Use Case**: Preparing technical documentation, CAPA tracking, and audit metrics dashboards.

### 📋 Natural Language Trigger:
```text
Spawn parallel subagents across isolated branches to perform an ISO compliance readiness audit:
1. Subagent 1: Audit validation protocols and risk management documentation against ISO 13485 clauses.
2. Subagent 2: Build an interactive HTML/JS dashboard tracking CAPA resolutions, audit checklist statuses, and KPI metrics.
Output gap analysis matrix to reports/iso/gap_analysis.md.
```

---

## Template 7: Rapid Multi-Database Literature & Patent Prior Art Survey
**Use Case**: Deep research across preprint servers, peer-reviewed journals, and patent offices simultaneously.

### 📋 Natural Language Trigger:
```text
In parallel, conduct a comprehensive scientific and patent landscape search on [TOPIC]:
1. Subagent 1 (PubMed & EuropePMC): Extract peer-reviewed clinical studies with DOIs and key quantitative findings.
2. Subagent 2 (BioRxiv & ArXiv): Search recent preprints for emerging methodologies and pre-publication benchmarks.
3. Subagent 3 (USPTO Patents): Identify granted patents and published applications with key claims.
Consolidate results into reports/landscape/prior_art_matrix.md.
```

---

## Template 8: Autonomous Dual 'Builder + Auditor' Loop (/goal Pattern)
**Use Case**: High-stakes data analysis, manuscript preparation, or ISO validation where an independent adversarial subagent stress-tests the work before final delivery.

### 📋 Natural Language Trigger:
```text
Use /goal to develop [DELIVERABLE]. Once constructed, spawn an independent Auditor Subagent with least privilege (read-only) to:
1. Stress-test the codebase against edge cases.
2. Validate mathematical and statistical rigor.
3. Check compliance against [STANDARDS].
4. Output a certified validation report 'reports/audits/certification.md'.
```

---

## Template 9: Autonomous Document Production & Jev-Governed Review Pipeline
**Use Case**: Producing publication-grade manuscripts, technical reports, course syllabi, or educational web copy with zero AI provenance, zero robotic slop, and calibrated human voice governed by Jev System-1.

### 📋 Natural Language Trigger:
```text
Draft the requested document [DOCUMENT_NAME] and execute the Jev-governed review pipeline via subagents:
0. Subagent 0 (Jev Gatekeeper Triage): Run `jev_doc_gatekeeper.py` to evaluate initial text complexity, LaTeX syntax, and slop density.
1. Subagent 1 (Builder): Draft the complete technical text with structured formatting.
2. Subagent 2 (Provenance & Watermarks): Run `watermarks-remover` / `wm-text` to scrub zero-width Unicode tracking markers (Layer A) and strip metadata.
3. Subagent 3 (Slop Purge & Voice Humanizer): Apply `no-ai-slop` and `humanizer-juanjo` (or `humanizer-juanjo-es`) to calibrate tone and domain authority.
4. Subagent 4 (Jev Quality Gate): Run `jev_doc_gatekeeper.py` for final non-autoregressive sign-off (`quality_gate_passed == True`).
```

---

## Template 10: Batch Test Execution & Autonomous Auto-Remediation Loop
**Use Case**: Executing multiple test suites concurrently across isolated workspace branches, diagnosing failures, applying surgical fixes, and re-verifying until 100% pass.

### 📋 Natural Language Trigger:
```text
Execute all test suites in parallel across isolated branches. If any failures are detected, dispatch code_fixer to patch the issues and re-verify until all suites pass green.
```

---

## Template 11: Multi-Step Telemetry Pipeline with Live Dashboard
**Use Case**: Long-running multi-stage data processing where subagents stream live JSON milestone progress back to the parent for live dashboarding.

### 📋 Natural Language Trigger:
```text
Dispatch multi-stage workers in parallel across isolated branches with live telemetry reporting via send_message. Render a live dashboard as milestones complete.
```

---

## Template 12: Automated Hard Circuit Breaker & Fleet Governance
**Use Case**: Mission-critical distributed processing where any fatal subagent failure immediately halts the entire swarm via `manage_subagents(Action='kill_all')`, cleans up branched workspaces, and reports forensic diagnostics.

### 📋 Natural Language Trigger:
```text
Dispatch parallel subagents across isolated branches with error callbacks. If any subagent reports a FATAL_ERROR, execute a hard circuit breaker via manage_subagents (kill_all), purge temporary workspaces, and synthesize a post-mortem incident report.
```

---

## Template 13: Interactive Technical Interviewer & Round-Trip State Hydration
**Use Case**: Conducting structured domain-specific interactive interviews via `ask_question`, hydrating defaults from `user_prefs.json`, and persisting choices for subagents.

### 📋 Natural Language Trigger:
```text
Interview me for [FEATURE_NAME, e.g. web form / cloud deployment / dataset ETL pipeline]. Hydrate current preferences from user_prefs.json, render interactive UI selection modals, and persist my updated choices under the '[DOMAIN_NAMESPACE]' block.
```

---

## Template 14: Visual Asset Generation & Composition Studio
**Use Case**: Generating parameterized, production-ready visual assets (product cards, hero banners, diagrams) via `generate_image`, conducting an interactive review loop, and persisting to permanent workspace paths.

### 📋 Natural Language Trigger:
```text
Generate a mock visual asset for [SUBJECT, e.g., SMART PNA Probe diagnostic chip / UGR educational simulator UI mockup]. Apply structured photography/design token prompt synthesis, present the generated image for review via ask_question, and save the approved asset to public/images/.
```

### ⚙️ Orchestration Blueprint:
```json
// Step 1: Issue Parameterized generate_image tool call
{
  "Prompt": "Professional studio product photograph of [SUBJECT]. SCENE: smooth matte light gray surface, seamless background curve with soft infinite horizon. CAMERA: macro lens photography, sharp focus from front to back, f/11 aperture, crisp details, zero digital noise. LIGHTING: three-point soft-diffuse lighting, 48-inch octagonal softbox key light at 45 degrees, gentle fill light, backlit soft ambient glow, premium catalog style.",
  "ImageName": "diagnostic_chip_hero",
  "AspectRatio": "16:9",
  "ImagePaths": []
}

// Step 2: Interactive Review Loop via ask_question
{
  "questions": [
    {
      "question": "What would you like to do with this generated visual asset?",
      "is_multi_select": false,
      "options": [
        "(Recommended) Keep and save to public/images/",
        "Regenerate with updated prompt tokens",
        "Exit without saving"
      ]
    }
  ]
}

// Step 3: Persistence
// On approval, copy asset from brain storage to <workspace>/public/images/diagnostic_chip_hero.png
```

---

## Template 15: DeepMind AlphaGenome & Variant Impact Discovery Swarm
**Use Case**: Multiplexed non-coding and coding variant interpretation combining AlphaGenome Variant Impact (AVI) scores, saturation mutagenesis scans, AlphaGenome Atlas deep-links, and ClinVar/Ensembl validation.

### 📋 Natural Language Trigger:
```text
In parallel, launch a variant impact evaluation swarm for [VARIANT, e.g., chr12:52763294:C>T or KRT10 mutation]:
1. Subagent 1 (AlphaGenome AVI & Atlas): Query AlphaGenome Variant Impact scores, predict chromatin accessibility/splicing disruption, and generate clickable AlphaGenome Atlas deep-links.
2. Subagent 2 (Population & Clinical Genetics): Query gnomAD allele frequencies, ClinVar classifications, and dbSNP rsIDs.
3. Subagent 3 (Structural Impact): Fetch AlphaFold structure, assess residue pLDDT, and evaluate local structural perturbation.
Compile a comprehensive variant characterization dossier to reports/variants/[VARIANT_ID].md.
```

### ⚙️ Orchestration Blueprint:
```json
// Subagent 1: AlphaGenome AVI Analysis & Deep-Linking
{
  "TypeName": "research",
  "Role": "AlphaGenome Variant Specialist",
  "Workspace": "branch",
  "Prompt": "Using the alphagenome-variant-impact-score and alphagenome-atlas-website-links skills, analyze variant [VARIANT_STRING]. Check credentials protocol, extract AVI scores across regulatory/splicing tracks, and generate full AlphaGenome Atlas URLs. Return results via send_message to [PARENT_CONVERSATION_ID]."
}

// Subagent 2: Clinical & Population Verification
{
  "TypeName": "research",
  "Role": "Genomic Evidence Auditor",
  "Workspace": "branch",
  "Prompt": "Using clinvar-database, dbsnp-database, and gnomad-database skills, query clinical evidence and allele frequencies for variant [VARIANT_STRING]. Transmit structured findings back to [PARENT_CONVERSATION_ID]."
}
```

---

## Template 16: Ancient Epigraphic Restoration & Contextualization Campaign (Aeneas & Ithaca)
**Use Case**: Restoring damaged ancient texts, predicting geographical/chronological origins, generating semantic text embeddings, and retrieving parallel epigraphic inscriptions via DeepMind's Aeneas (Latin) and Ithaca (Ancient Greek).

### 📋 Natural Language Trigger:
```text
Dispatch an ancient text epigraphic analysis across isolated branches for [TEXT_FRAGMENT, Latin or Greek]:
1. Subagent 1 (Text Restoration): Run beam search restoration for damaged regions indicated by '?' or '#' characters.
2. Subagent 2 (Origin Attribution & Parallels): Infer geographical region, date distribution (BCE/CE), and top parallel inscriptions from EDR/EDH/PHI databases.
3. Subagent 3 (Visual Dashboard): Run visualize_results.py and serve the interactive HTML dashboard on a persistent background port.
```

### ⚙️ Orchestration Blueprint:
```json
// Subagent 1: Aeneas/Ithaca Epigraphic Worker
{
  "TypeName": "self",
  "Role": "Epigraphic AI Researcher",
  "Workspace": "branch",
  "Prompt": "Using the predictingthepast skill, check .licenses/predictingthepast_LICENSE.txt terms. Execute preprocess.py on the input fragment, run run_inference.py with --attribute, --restore, and --contextualize, and compile results.json. Transmit the top beam predictions and parallel inscription IDs back to [PARENT_CONVERSATION_ID]."
}
```

---

## Template 17: High-Throughput Deep Learning File Ingestion & Security Audit (Magika)
**Use Case**: Deep-learning verification of incoming binary assets, experimental data files, or documents using Google's Magika model to detect deceptive file extensions, inspect MIME types, and route files to specialized parsers.

### 📋 Natural Language Trigger:
```text
Dispatch a parallel file ingestion and verification swarm for directory [INPUT_DIR]:
1. Subagent 1 (Magika Deep Inspection): Run magika --jsonl -r across all files to detect true MIME types, predict content-type labels, and flag deceptive extension mismatches.
2. Subagent 2 (Metadata & Provenance Hygiene): For all detected documents or images, run wm-inspect and clean tracking metadata.
3. Subagent 3 (Structured Ingestion Router): Route verified PDFs to pymupdf4llm, tabular files to Polars, and chemical files to RDKit.
Compile an audit manifest to reports/ingestion/manifest.json.
```

### ⚙️ Orchestration Blueprint:
```json
// Subagent 1: Magika Deep Type Inspector
{
  "TypeName": "research",
  "Role": "Binary Content-Type Auditor",
  "Workspace": "branch",
  "Prompt": "Using the magika CLI tool, execute 'magika --jsonl -r [INPUT_DIR]'. Identify all files where the predicted extension diverges from the actual file extension. Transmit the anomaly report and JSONL stream back to [PARENT_CONVERSATION_ID]."
}
```


