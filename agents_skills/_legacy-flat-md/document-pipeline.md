# document-pipeline

**Trigger**: Use for any high-stakes document production that requires zero AI provenance, calibrated voice, and metadata-clean delivery. Orchestrates Builder → Provenance → Voice as three sequential stages. Triggered automatically by the CLAUDE.md pipeline rule or explicitly by the user.

---

## When to Apply This Pipeline

Apply to: scientific manuscripts, grant proposals, ISO documents, technical reports, course syllabi, web copy for UGR/DestiNA, any external-facing deliverable.

Skip for: quick inline answers, code, internal scratch notes, exploratory drafts explicitly marked "rough".

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────┐
│  INPUT: User request + source material + target format  │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  STAGE 1: BUILDER                                       │
│  Draft complete document following domain skill         │
│  (scientific-writing / ugr-courseware / etc.)           │
│  Output: raw_draft.md (or .docx, .pptx)                │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  STAGE 2: PROVENANCE HYGIENE                            │
│  Apply clean-user-facing-text pipeline:                 │
│  → Layer A: wm-text (invisible Unicode)                 │
│  → Layer B: no-ai-slop (stylometric cleaning)           │
│  → Layer M: wm-clean metadata strip (file outputs)     │
│  Output: provenance_clean.md                            │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  STAGE 3: VOICE CALIBRATION                             │
│  Apply humanizer-juanjo (EN) or humanizer-juanjo-es     │
│  Final check: word count, citation integrity, notation  │
│  Output: final_deliverable.[format]                     │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  DELIVERY: SendUserFile + device_commit_files           │
└─────────────────────────────────────────────────────────┘
```

---

## Execution Modes

### Mode A: Single-Agent Sequential (default, short documents < 2000 words)
Run all three stages in sequence within the same conversation turn. Fastest for typical documents.

### Mode B: Multi-Agent Parallel (long documents, manuscripts)
When using the `Agent` tool for complex documents:

```python
# Stage 1: Builder agent (with worktree isolation for file output)
Agent(
    description="Draft scientific manuscript section",
    prompt="[Complete self-contained prompt with all context]",
    isolation="worktree"  # if writing to files
)

# Stage 2: Provenance agent (read-only input, writes clean output)
Agent(
    description="Provenance hygiene pass",
    prompt="Apply clean-user-facing-text pipeline to: [draft content]"
)

# Stage 3: Voice agent (final calibration)
Agent(
    description="Voice calibration — humanizer-juanjo-es",
    prompt="Apply humanizer-juanjo-es to: [provenance-clean content]"
)
```

**Anti-patterns** (never do):
- Never give Builder agent write access to the final output path
- Never run Stage 2 and Stage 3 in parallel (3 depends on 2's output)
- Never skip Stage 2 for external deliverables, even "clean" drafts

---

## Stage 1 — Builder Protocol

1. Select the appropriate domain skill based on document type:
   - Scientific manuscript → `scientific-writing`
   - UGR teaching material → `ugr-courseware`
   - Literature survey → `literature-review`
   - General report → proceed with IMRAD-like structure

2. Draft the complete document:
   - All sections filled (no "TODO" placeholders in output)
   - All citations included (use WebSearch to verify DOIs)
   - All figures/tables referenced
   - Notation in Unicode, not LaTeX

3. Tag the raw output clearly:
   ```
   <!-- STAGE 1 RAW DRAFT — NOT FOR DELIVERY -->
   [document content]
   <!-- END STAGE 1 -->
   ```

---

## Stage 2 — Provenance Hygiene Protocol

### 2A. Unicode scrub (inline)
Scan for and remove:
- U+200B, U+200C, U+200D, U+2060, U+FEFF
- U+202A–U+202E bidi overrides
- Non-breaking spaces where regular spaces are appropriate

### 2B. Stylometric cleaning (no-ai-slop)
Run the full `no-ai-slop` protocol. Target score < 3/10.
Log: categories cleaned and count of changes.

### 2C. File metadata (when output is a file)
If the Stage 1 output is a .docx, .pdf, .html, or image file:
```bash
wm-clean "<draft_file>" -o "<clean_file>"
```

---

## Stage 3 — Voice Calibration Protocol

Determine language from content (not just instructions):
- Predominantly Spanish → `humanizer-juanjo-es`
- Predominantly English → `humanizer-juanjo`
- Mixed → apply appropriate protocol per section, mark transitions

Run the full voice calibration protocol.

**Final QA checklist**:
- [ ] Word count within target (if specified)
- [ ] All section headers present and descriptive
- [ ] All citations verified (at least title + author + year)
- [ ] No LaTeX delimiters in prose
- [ ] Chemical/physics notation in Unicode
- [ ] No slop patterns (spot-check: search for "furthermore", "it is worth", "in conclusion")
- [ ] Voice consistent throughout (no sudden register shifts)

---

## Delivery Protocol

```python
# 1. Send file to conversation
SendUserFile(files=["final_deliverable.docx"], status="normal")

# 2. Commit to user's connected folder
device_commit_files(
    files=[{"fileUuid": "<uuid>", "devicePath": "K:\\Mi unidad\\...\\<filename>"}]
)
```

Accompany with a single-sentence summary: what was produced, word count, and any decisions made during drafting that the user should know about.

---

## Escalation Rules

If the Builder stage produces content with factual uncertainty:
- Flag the uncertain claim explicitly: `[VERIFY: <claim>]`
- Do not fabricate citations — write `[CITATION NEEDED]` and use WebSearch to find one
- If a citation cannot be found, remove the claim or reframe as "to our knowledge"

If the Provenance stage scores > 7/10 on slop:
- Restart Stage 2 with targeted rewriting of the worst-scoring sections
- Do not pass to Stage 3 until score < 3/10
