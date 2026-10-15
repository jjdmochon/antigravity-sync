# Global Subagent Orchestration, Interactive UI & Process Governance Templates

**Updated:** 2026-10-01 · supersedes `SUBAGENTS_TEMPLATES.md`

> [!NOTE]
> Installed at `%USERPROFILE%\.gemini\SUBAGENTS_TEMPLATES_2026-10-01.md` and linked from
> [GEMINI.md](GEMINI.md). Companion catalog: [GLOBAL_AGENTS_AND_TOOLS_2026-10-01.md](GLOBAL_AGENTS_AND_TOOLS_2026-10-01.md).
> The core skill `subagent-templates` adapts these patterns to Claude Code.

### What changed on 2026-10-01

Regarding skills, we now split them into a core that every subagent sees automatically and a library that it does not. When a template relies on a library skill (AlphaGenome, the ToolUniverse sub-skills, the biomedical databases, BioNeMo/NIM, Albatross or the UGR material), the launch prompt has to name the path, `~/.agents/skill-library/<name>/SKILL.md`, or tell the worker to consult `skill-catalog`. The Drive workspaces no longer carry their own copies, so this is the only way a worker reaches those skills.

On the Jev front, the engine runs on Python 3.13, and every gatekeeper call in this document uses `py -3.13 "$HOME/.agents/skills/jev-system-one/scripts/jev_doc_gatekeeper.py" "<file>" --json`. Plain `python` resolves to Anaconda, which lacks `typesafe-sdk` and returns `fallo-abierto (sin Jev)`, so we never use it for the gate.

Finally, Claude Code now has three named subagents, `juanjo-copilot`, `document-reviewer` and `albatross-expert` (section 2), and templates 18 and 19 are new.

---

## 1. The 5-Tool Antigravity Architecture

```mermaid
flowchart TD
    User["Developer / User Input"] --> Parent["1. Parent Orchestrator (Conversation ID: parent-id)
Main Context Clean & Sharp"]

    subgraph HITL["Human-in-the-Loop & Visual Studio"]
        Parent -->|1. Hydrate user_prefs.json| State["Workspace State Hydration"]
        State -->|2. ask_question| UI["Interactive UI Modals"]
        Parent -->|3. generate_image| VisualStudio["Visual Asset Studio (SCENE + CAMERA + LIGHTING)"]
        VisualStudio -->|4. ask_question| Review{"Keep / Regenerate?"}
        Review -->|Keep| SaveAsset["Persist to public/images/"]
    end

    subgraph Execution["Parallel Swarm Execution & Governance"]
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

## 2. Claude Code Equivalents

| Antigravity | Claude Code | Notes |
| :--- | :--- | :--- |
| `define_subagent` + `invoke_subagent` | `Agent` tool with `subagent_type` | Named types: `juanjo-copilot`, `document-reviewer`, `albatross-expert`, plus built-ins `Explore` (read-only search), `Plan`, `general-purpose`. |
| `Workspace: "branch"` | `isolation: "worktree"` on the `Agent` call | Isolated git worktree for anything that edits files. |
| Parallel swarm | Several `Agent` calls in one message, or the `Workflow` tool | `Workflow` only when the user asks for multi-agent orchestration. |
| `send_message` | `SendMessage` | Continue a running subagent with its context. |
| `manage_subagents: list / kill_all` | `ListAgents` / `TaskStop` | |
| `ask_question` | `AskUserQuestion` | Same anti-patterns apply (section 3). |
| Reactive wakeup | Background task notifications | Never poll. |

### Claude Code subagents

| Subagent | Use it for |
| :--- | :--- |
| `juanjo-copilot` | Domain work with the persona and the Jev-gated pipeline active. |
| `document-reviewer` | Stages 0–4 of the review pipeline on a finished file; quotes Jev's probabilities. |
| `albatross-expert` | Albatross RNA language model, IRES structure, DMS-MaPseq (Sychla et al., bioRxiv 2026). |

---

## 3. The 15 Anti-Patterns to Prevent

### Interactive UI (`ask_question` / `AskUserQuestion`)
1. Never cause option fatigue: keep option arrays under 5–7 items; pre-filter large datasets.
2. Never add explicit "Other" / "Custom" options: both platforms add a free-text field automatically.
3. Never use flat root keys in configs: namespace keys under a domain block (`"FORMS"`, `"TESTING"`, `"BIOCHEM"`) in `user_prefs.json`.
4. Never use third-person phrasing: write options as direct user answers (*"Client-side validation"*), not commands.

### Visual assets (`generate_image`)
5. Never inject raw prompts: parameterise with structured tokens (`[SCENE]`, `[CAMERA]`, `[LIGHTING]`, `[STYLE]`).
6. Never store assets in volatile `/tmp`: copy approved images to permanent project paths (`public/images/`).
7. Never make redundant generation calls: check whether the asset already exists on disk first.

### Orchestration (`define_subagent` / `invoke_subagent` / `Agent`)
8. Never over-permission workers: least privilege (`enable_write_tools: false` when read-only; no subagent tools unless needed).
9. Never tight-loop poll: no `manage_task(Action='status')` loops or sleeps; both platforms wake the parent.
10. Never send unscoped prompts: prompts are self-contained, with explicit paths, commands and parent IDs.
11. Always isolate modifying tasks: `Workspace: "branch"` (Antigravity) or `isolation: "worktree"` (Claude Code).
12. Never assume a library skill is loaded: name its path (`~/.agents/skill-library/<name>/SKILL.md`) or tell the worker to consult `skill-catalog`.

### Messaging & governance (`send_message` / `manage_subagents`)
13. Never allow unbounded ping-pong loops: require an explicit `STATUS: COMPLETE` or `TERMINATE` flag.
14. Never send ungrounded messages: inject the parent `Conversation ID` in launch prompts.
15. Never send free-form text dumps: use structured JSON or strict prefix tags (`[PROGRESS]`, `[ERROR]`, `[ABORT]`).

---

## 4. Master Template Catalog

1. [Template 1: Multi-Omics Disease & Target Dossier](#template-1-multi-omics-disease--target-dossier)
2. [Template 2: DestiNA DCL Chemistry & miRNA Biomarker Validation](#template-2-destina-dcl-chemistry--mirna-biomarker-validation)
3. [Template 3: KRT10 Variant & PNA Probe Biophysics Campaign](#template-3-krt10-variant--pna-probe-biophysics-campaign)
4. [Template 4: Single-Cell Drug Repurposing (drug2cell + ChEMBL)](#template-4-single-cell-drug-repurposing-drug2cell--chembl)
5. [Template 5: UGR Academic Courseware & Interactive Web Hub](#template-5-ugr-academic-courseware--interactive-web-hub)
6. [Template 6: ISO 9001 / ISO 13485 Compliance & Audit Checklist](#template-6-iso-9001--iso-13485-compliance--audit-checklist)
7. [Template 7: Rapid Multi-Database Literature & Patent Prior Art Survey](#template-7-rapid-multi-database-literature--patent-prior-art-survey)
8. [Template 8: Autonomous Dual 'Builder + Auditor' Loop (/goal Pattern)](#template-8-autonomous-dual-builder--auditor-loop-goal-pattern)
9. [Template 9: Autonomous Document Production & Jev-Governed Review Pipeline](#template-9-autonomous-document-production--jev-governed-review-pipeline)
10. [Template 10: Batch Test Execution & Autonomous Auto-Remediation Loop](#template-10-batch-test-execution--autonomous-auto-remediation-loop)
11. [Template 11: Multi-Step Telemetry Pipeline with Live Dashboard](#template-11-multi-step-telemetry-pipeline-with-live-dashboard)
12. [Template 12: Automated Hard Circuit Breaker & Fleet Governance](#template-12-automated-hard-circuit-breaker--fleet-governance)
13. [Template 13: Interactive Technical Interviewer & Round-Trip State Hydration](#template-13-interactive-technical-interviewer--round-trip-state-hydration)
14. [Template 14: Visual Asset Generation & Composition Studio](#template-14-visual-asset-generation--composition-studio)
15. [Template 15: DeepMind AlphaGenome & Variant Impact Discovery Swarm](#template-15-deepmind-alphagenome--variant-impact-discovery-swarm)
16. [Template 16: Ancient Epigraphic Restoration & Contextualization Campaign (Aeneas & Ithaca)](#template-16-ancient-epigraphic-restoration--contextualization-campaign-aeneas--ithaca)
17. [Template 17: High-Throughput Deep Learning File Ingestion & Security Audit (Magika)](#template-17-high-throughput-deep-learning-file-ingestion--security-audit-magika)
18. [Template 18: Albatross IRES & RNA Conformation Analysis](#template-18-albatross-ires--rna-conformation-analysis)
19. [Template 19: BioNeMo NIM Protein Binder Design Campaign](#template-19-bionemo-nim-protein-binder-design-campaign)

---

## Template 1: Multi-Omics Disease & Target Dossier
We use this template for target validation, connecting clinical genetics, protein structures and pharmacology while keeping the parent context clean. It starts from the `tooluniverse` router in the core, which hands off to `tooluniverse-target-research` and `tooluniverse-drug-target-validation` in the library.

### Natural-language trigger
```text
In parallel, dispatch dedicated subagents to generate a target dossier for [TARGET_GENE, e.g., KRT10 or EGFR] across isolated branches. Each worker reads its ToolUniverse sub-skill from ~/.agents/skill-library. Return a unified dossier.
```

---

## Template 2: DestiNA DCL Chemistry & miRNA Biomarker Validation
We use this template when we validate a Dynamic Chemical Labeling (DCL) assay for diagnostic microRNA detection, utilizing the core skill `smart-pna-probe-design`.

### Natural-language trigger
```text
Run the local DCL calibration analysis on my CSV data in data/, and simultaneously spawn parallel subagents across isolated branches to evaluate clinical biomarker literature (PubMed MCP) and probe sequence specificity using smart-pna-probe-design:
1. Subagent A: Run smart-pna-probe-design to scan the miRNA target, place abasic blanks (*GL* / *L-Ser*), compute SMART adduct masses and duplex Tm.
2. Subagent B: Query PubMed and GEO databases for clinical validation cohorts and expression ranges.
3. Subagent C: Evaluate cross-hybridization penalties against closely related isoforms.
```

---

## Template 3: KRT10 Variant & PNA Probe Biophysics Campaign
We use this template to design PNA or SMART probes that discriminate specific epidermal mutations using `smart-pna-probe-design` alongside biophysical modeling.

### Natural-language trigger
```text
In parallel, launch subagents across isolated branches to design a PNA targeting strategy for [MUTATION, e.g., KRT10 R156C]:
1. Subagent 1: Model PNA:RNA duplex melting temperatures (Tm) and the ΔTm discrimination penalty via smart-pna-probe-design.
2. Subagent 2: Evaluate steric accessibility using 3D conformers (pna_struct).
3. Subagent 3: Search USPTO (library skill uspto-database) for patented PNA modifications targeting keratin genes.
Compile a candidate ranking table to reports/pna/candidates.md.
```

---

## Template 4: Single-Cell Drug Repurposing (drug2cell + ChEMBL)
We use this template to map drug targets and identify therapeutic candidates across single-cell clusters. The Python steps run with `py -3.13`, where drug2cell 0.1.2 and scanpy 1.12.3 are installed.

### Natural-language trigger
```text
Process the single-cell AnnData (.h5ad) object using Scanpy, and simultaneously dispatch parallel subagents in isolated branches to:
1. Subagent A: Run drug2cell (d2c.score and d2c.gsea) against ChEMBL clinical-stage compounds.
2. Subagent B: Run blitzgsea across Reactome and KEGG pathways for top cluster markers.
Synthesize findings into an interactive UMAP visualization.
```

---

## Template 5: UGR Academic Courseware & Interactive Web Hub
We use this template for teaching materials and single-page educational tools, drawing on `ugr-courseware` and `qfdos-exam-generator` from the library.

### Natural-language trigger
```text
For UGR [COURSE, e.g., Química Farmacéutica I - Tema 3], launch parallel subagents in isolated workspace branches:
1. Subagent 1 (Web App): Build a standalone HTML5/CSS3 simulator using the Genyo Fusion design system.
2. Subagent 2 (Quiz): Generate a 10-question formative assessment with interactive flashcard reveals.
3. Subagent 3 (Summary): Extract key formulas and concepts into a concise study guide.
Run the Jev-gated review (Template 9) on the study guide before delivery.
```

---

## Template 6: ISO 9001 / ISO 13485 Compliance & Audit Checklist
We use this template for technical documentation, CAPA tracking and audit dashboards, with `iso-13485-certification` from the library as the reference for the standard.

### Natural-language trigger
```text
Spawn parallel subagents across isolated branches to perform an ISO compliance readiness audit:
1. Subagent 1: Audit validation protocols and risk management documentation against ISO 13485 clauses.
2. Subagent 2: Build an interactive HTML/JS dashboard tracking CAPA resolutions, audit checklist statuses, and KPI metrics.
Output the gap analysis matrix to reports/iso/gap_analysis.md.
```

---

## Template 7: Rapid Multi-Database Literature & Patent Prior Art Survey
We use this template when we need preprint servers, peer-reviewed journals and patent offices covered at the same time.

### Natural-language trigger
```text
In parallel, conduct a comprehensive scientific and patent landscape search on [TOPIC]:
1. Subagent 1 (PubMed & Europe PMC): Extract peer-reviewed clinical studies with DOIs and key quantitative findings.
2. Subagent 2 (bioRxiv & arXiv): Search recent preprints for emerging methods and benchmarks.
3. Subagent 3 (USPTO): Identify granted patents and published applications with key claims.
Consolidate results into reports/landscape/prior_art_matrix.md.
```

---

## Template 8: Autonomous Dual 'Builder + Auditor' Loop (/goal Pattern)
We use this template for high-stakes analysis, manuscripts or ISO validation, where an independent read-only auditor has to stress-test the work before it leaves our hands.

### Natural-language trigger
```text
Use /goal to develop [DELIVERABLE]. Once constructed, spawn an independent Auditor Subagent with least privilege (read-only) to:
1. Stress-test the codebase against edge cases.
2. Validate mathematical and statistical rigor.
3. Check compliance against [STANDARDS].
4. Output a certified validation report to reports/audits/certification.md.
```

---

## Template 9: Autonomous Document Production & Jev-Governed Review Pipeline
We use this template for manuscripts, reports, syllabi and web copy that must leave without provenance markers, read in Juanjo's own voice and carry Jev's certification. In Claude Code the quickest route is to delegate stages 0 to 4 to the `document-reviewer` subagent.

### Natural-language trigger
```text
Draft the requested document [DOCUMENT_NAME] and execute the Jev-governed review pipeline via subagents:
0. Subagent 0 (Jev triage): py -3.13 "$HOME/.agents/skills/jev-system-one/scripts/jev_doc_gatekeeper.py" "<file>" --json. Run only the stages in etapas_a_ejecutar.
1. Subagent 1 (Builder): Draft the complete technical text with structured formatting.
2. Subagent 2 (Provenance): remove-ai-marks / watermarks-remover to scrub zero-width Unicode (Layer A) and strip metadata.
3. Subagent 3 (Slop purge & voice): no-ai-slop, then the humanizer Jev selected (humanizer-juanjo or humanizer-juanjo-es).
4. Subagent 4 (Jev certification): re-run the gatekeeper; sign-off requires quality_gate_passed == true. Quote the probabilities.
If the engine reports "fallo-abierto (sin Jev)", run every stage and state that the document is not certified.
```

---

## Template 10: Batch Test Execution & Autonomous Auto-Remediation Loop
We use this template to run test suites concurrently in isolated branches and keep patching and re-verifying until every suite is green.

### Natural-language trigger
```text
Execute all test suites in parallel across isolated branches. If any failures are detected, dispatch code_fixer to patch the issues and re-verify until all suites pass green.
```

---

## Template 11: Multi-Step Telemetry Pipeline with Live Dashboard
We use this template for long multi-stage processing in which the workers stream JSON milestones back to the parent.

### Natural-language trigger
```text
Dispatch multi-stage workers in parallel across isolated branches with live telemetry reporting via send_message. Render a live dashboard as milestones complete.
```

---

## Template 12: Automated Hard Circuit Breaker & Fleet Governance
We use this template for distributed processing in which a single fatal failure must halt the swarm (`manage_subagents(Action='kill_all')` in Antigravity, `TaskStop` in Claude Code), clean the branched workspaces and report diagnostics. Jev's `jev_router.py` can take the circuit-breaker decision in under 100 ms.

### Natural-language trigger
```text
Dispatch parallel subagents across isolated branches with error callbacks. If any subagent reports a FATAL_ERROR, execute a hard circuit breaker (kill_all), purge temporary workspaces, and synthesize a post-mortem incident report.
```

---

## Template 13: Interactive Technical Interviewer & Round-Trip State Hydration
We use this template for structured interviews through `ask_question`, with defaults read from `user_prefs.json` and the answers saved back for the subagents that follow.

### Natural-language trigger
```text
Interview me for [FEATURE_NAME, e.g. web form / cloud deployment / dataset ETL pipeline]. Hydrate current preferences from user_prefs.json, render interactive selection modals, and persist my updated choices under the '[DOMAIN_NAMESPACE]' block.
```

---

## Template 14: Visual Asset Generation & Composition Studio
We use this template to produce parameterised visual assets such as product cards, hero banners and diagrams through `generate_image`, review them interactively and store the approved ones permanently.

### Natural-language trigger
```text
Generate a mock visual asset for [SUBJECT, e.g., SMART PNA Probe diagnostic chip / UGR educational simulator UI mockup]. Apply structured design-token prompt synthesis, present the image for review via ask_question, and save the approved asset to public/images/.
```

### Orchestration blueprint
```json
// Step 1: Parameterised generate_image call
{
  "Prompt": "Professional studio product photograph of [SUBJECT]. SCENE: smooth matte light gray surface, seamless background curve with soft infinite horizon. CAMERA: macro lens photography, sharp focus from front to back, f/11 aperture, crisp details, zero digital noise. LIGHTING: three-point soft-diffuse lighting, 48-inch octagonal softbox key light at 45 degrees, gentle fill light, backlit soft ambient glow, premium catalog style.",
  "ImageName": "diagnostic_chip_hero",
  "AspectRatio": "16:9",
  "ImagePaths": []
}

// Step 2: Review loop via ask_question
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
// On approval, copy the asset from brain storage to <workspace>/public/images/diagnostic_chip_hero.png
```

---

## Template 15: DeepMind AlphaGenome & Variant Impact Discovery Swarm
We use this template to interpret coding and non-coding variants, combining AlphaGenome Variant Impact (AVI) scores and saturation mutagenesis with Atlas deep-links and ClinVar or Ensembl validation. It reads `alphagenome-variant-impact-score`, `alphagenome-atlas-website-links`, `clinvar-database`, `dbsnp-database`, `gnomad-database` and `alphafold-database-fetch-and-analyze` from the library, and it needs `ALPHAGENOME_API_KEY` in `~\.env`.

### Natural-language trigger
```text
In parallel, launch a variant impact evaluation swarm for [VARIANT, e.g., chr12:52763294:C>T or a KRT10 mutation]:
1. Subagent 1 (AlphaGenome AVI & Atlas): Query AVI scores, predict chromatin accessibility/splicing disruption, and generate AlphaGenome Atlas deep-links.
2. Subagent 2 (Population & clinical genetics): Query gnomAD allele frequencies, ClinVar classifications and dbSNP rsIDs.
3. Subagent 3 (Structural impact): Fetch the AlphaFold structure, assess residue pLDDT and local structural perturbation.
Compile a variant dossier to reports/variants/[VARIANT_ID].md.
```

### Orchestration blueprint
```json
// Subagent 1: AlphaGenome AVI analysis & deep-linking
{
  "TypeName": "research",
  "Role": "AlphaGenome Variant Specialist",
  "Workspace": "branch",
  "Prompt": "Read ~/.agents/skill-library/alphagenome-variant-impact-score/SKILL.md and ~/.agents/skill-library/alphagenome-atlas-website-links/SKILL.md and follow them to analyze variant [VARIANT_STRING]. Check the credentials protocol, extract AVI scores across regulatory/splicing tracks, and generate full AlphaGenome Atlas URLs. Return results via send_message to [PARENT_CONVERSATION_ID]."
}

// Subagent 2: Clinical & population verification
{
  "TypeName": "research",
  "Role": "Genomic Evidence Auditor",
  "Workspace": "branch",
  "Prompt": "Read the clinvar-database, dbsnp-database and gnomad-database skills from ~/.agents/skill-library and query clinical evidence and allele frequencies for variant [VARIANT_STRING]. Transmit structured findings back to [PARENT_CONVERSATION_ID]."
}
```

---

## Template 16: Ancient Epigraphic Restoration & Contextualization Campaign (Aeneas & Ithaca)
We use this template to restore damaged ancient texts, estimate their origin and date and retrieve parallel inscriptions with DeepMind's Aeneas for Latin and Ithaca for Ancient Greek, through the `predictingthepast` library skill.

### Natural-language trigger
```text
Dispatch an ancient text epigraphic analysis across isolated branches for [TEXT_FRAGMENT, Latin or Greek]:
1. Subagent 1 (Text restoration): Run beam search restoration for damaged regions marked with '?' or '#'.
2. Subagent 2 (Origin attribution & parallels): Infer region, date distribution (BCE/CE) and top parallel inscriptions from EDR/EDH/PHI.
3. Subagent 3 (Visual dashboard): Run visualize_results.py and serve the interactive HTML dashboard on a persistent background port.
```

### Orchestration blueprint
```json
// Subagent 1: Aeneas/Ithaca epigraphic worker
{
  "TypeName": "self",
  "Role": "Epigraphic AI Researcher",
  "Workspace": "branch",
  "Prompt": "Read ~/.agents/skill-library/predictingthepast/SKILL.md, check .licenses/predictingthepast_LICENSE.txt terms, run preprocess.py on the input fragment, run run_inference.py with --attribute, --restore and --contextualize, and compile results.json. Transmit the top beam predictions and parallel inscription IDs back to [PARENT_CONVERSATION_ID]."
}
```

---

## Template 17: High-Throughput Deep Learning File Ingestion & Security Audit (Magika)
We use this template to verify incoming binaries, data files and documents with Google's Magika, which catches deceptive extensions and lets us route each file to the right parser. The `magika` skill is in the core, but the CLI was not on PATH on 2026-10-01, so check `Get-Command magika` before launching the swarm.

### Natural-language trigger
```text
Dispatch a parallel file ingestion and verification swarm for directory [INPUT_DIR]:
1. Subagent 1 (Magika deep inspection): Run magika --jsonl -r across all files to detect true MIME types and flag extension mismatches.
2. Subagent 2 (Metadata & provenance hygiene): For detected documents or images, inspect and clean tracking metadata with the watermarks-remover skill.
3. Subagent 3 (Structured ingestion router): Route verified PDFs to pymupdf4llm, tabular files to pandas, and chemical files to RDKit.
Compile an audit manifest to reports/ingestion/manifest.json.
```

### Orchestration blueprint
```json
// Subagent 1: Magika deep type inspector
{
  "TypeName": "research",
  "Role": "Binary Content-Type Auditor",
  "Workspace": "branch",
  "Prompt": "Using the magika CLI tool, execute 'magika --jsonl -r [INPUT_DIR]'. Identify all files where the predicted extension diverges from the actual file extension. Transmit the anomaly report and JSONL stream back to [PARENT_CONVERSATION_ID]."
}
```

---

## Template 18: Albatross IRES & RNA Conformation Analysis
We use this template for questions about Internal Ribosome Entry Sites, alternative RNA conformations or DMS-MaPseq data that must be answered against the Albatross paper (Sychla et al., Rouskin Lab, bioRxiv 2026). The work goes to the `albatross-expert` subagent in Claude Code, which reads the paper, supplement, figures and tables from the `albatross-rna-paper` library skill.

### Natural-language trigger
```text
Delegate to albatross-expert: using ~/.agents/skill-library/albatross-rna-paper (references/paper.md, references/supplement.md, assets/), explain how Albatross scores [IRES_OR_SEQUENCE], which structural features drive the prediction, and how the DMS-MaPseq evidence supports it. Cite figure and table numbers from the paper.
```

### Orchestration blueprint (Claude Code)
```json
{
  "subagent_type": "albatross-expert",
  "description": "Albatross IRES analysis",
  "prompt": "Read ~/.agents/skill-library/albatross-rna-paper/SKILL.md and its references index. Answer: [QUESTION]. Quote the supporting section, figure or table for every claim and flag anything the paper does not establish."
}
```

---

## Template 19: BioNeMo NIM Protein Binder Design Campaign
We use this template for de novo binder design against a target protein with NVIDIA BioNeMo NIMs, taking the campaign from structure to a ranked list of candidates. It draws on the `bionemo` pack in the library: `openfold3-nim` or `openfold2-nim` for the structure, `rfdiffusion-nim` for backbones, `proteinmpnn-nim` for sequences, `boltz2-nim` for complex co-folding, with `msa-search-nim`, `diffdock-nim` and the `complexa-*` workflows available when the design calls for them. Each skill's `SKILL.md` explains the NVIDIA API credentials it needs.

### Natural-language trigger
```text
Run a binder design campaign for [TARGET, e.g., PDB 7XYZ chain A, hotspot residues 45-60] across isolated branches:
1. Subagent 1 (Structure): Predict or fetch the target structure (openfold3-nim / pdb-database) and define the hotspot.
2. Subagent 2 (Backbones): Generate N binder backbones with rfdiffusion-nim against the hotspot.
3. Subagent 3 (Sequences): Design sequences for each backbone with proteinmpnn-nim.
4. Subagent 4 (Validation): Co-fold target + binder with boltz2-nim and rank by interface confidence.
Each worker reads its skill from ~/.agents/skill-library/<name>/SKILL.md. Write the ranked table to reports/binders/[TARGET]_candidates.md.
```

### Orchestration blueprint
```json
// Subagent 2: Backbone generation
{
  "TypeName": "research",
  "Role": "RFdiffusion Backbone Designer",
  "Workspace": "branch",
  "Prompt": "Read ~/.agents/skill-library/rfdiffusion-nim/SKILL.md and follow it to generate [N] binder backbones for [TARGET_PDB] with hotspot [RESIDUES]. Save PDBs under designs/backbones/ and send a JSON summary (paths, contig strings, runtimes) to [PARENT_CONVERSATION_ID]."
}
```
