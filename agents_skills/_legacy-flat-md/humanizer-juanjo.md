# humanizer-juanjo

**Trigger**: Rewrite into Juanjo's executive English voice. Use when the user asks to humanize, rewrite, polish, or calibrate tone of any English text produced for professional, academic, or scientific communication.

---

## Voice Profile: Juanjo — Executive English

**Character**: Composed, technically precise, authoritative, action-oriented. The voice of a PI who also ships code and writes grants.

**Registers served**: Scientific manuscripts, grant proposals, ISO documentation, biotech reports, investor decks, DestiNA/UGR communications.

---

## Step-by-Step Rewrite Protocol

### Step 1 — Structural triage
Read the full text before touching a word. Identify:
- The central claim or deliverable of each paragraph
- Any paragraph that exists only to soften, qualify, or pad
- Any list that should be prose and any prose that should be a list

### Step 2 — Cut ruthlessly, then rebuild
Delete the following on sight — do not replace, just delete:
- Opening filler: "It is worth noting that", "It is important to understand", "In today's fast-paced world", "Certainly", "Of course", "Absolutely"
- Closing filler: "In conclusion", "In summary", "Overall", "To summarize", "It is clear that"
- Passive padding: "It can be seen that", "It should be noted that", "There are several reasons why"
- Hollow intensifiers: "very", "quite", "really", "extremely", "highly" (unless quantified: "3.2× higher")
- Em-dash overuse: keep em-dashes only for genuine parenthetical emphasis, max 1 per paragraph
- Rule-of-three cadence: if three parallel items exist only for rhythm, collapse to two or one

### Step 3 — Active voice, concrete subjects
Every sentence should have a human or system as its grammatical subject performing an action.

| Before | After |
|---|---|
| "Validation was performed using..." | "We validated using..." |
| "Results were obtained that suggest..." | "Results suggest..." |
| "It was found that the probe..." | "The probe..." |
| "Improvement can be achieved by..." | "To improve X, do Y." |

### Step 4 — Quantify vague claims
Replace qualitative hedges with numbers where the data exists, or remove the hedge entirely.

| Before | After |
|---|---|
| "significantly improved" | "improved by 40% (p < 0.01)" |
| "a large number of samples" | "1,847 samples" |
| "several studies have shown" | "Three independent cohorts (refs) show" |

### Step 5 — Terminology precision (domain-specific)
- Genomics: use standard gene/protein nomenclature (italicized genes: *KRT10*, *EGFR*)
- Chemistry: Unicode directly — ¹H NMR, ¹³C NMR, [M+H]⁺, KD, δ, ν, Δ, ×
- Never LaTeX delimiters in prose or Markdown: no `$...$`, `\(...\)`, `\text{...}`
- Assay data: always state n, units, and statistical test

### Step 6 — Paragraph architecture
Each paragraph: one claim → one or two pieces of evidence → one implication. Never more than 5 sentences. If a paragraph has two claims, split it.

### Step 7 — Final voice check
Read the output aloud (mentally). Flag any sentence that sounds like it was written by a committee. Rewrite it as if explaining to a sharp colleague over coffee.

---

## Tone Calibration by Document Type

| Type | Tone | Key markers |
|---|---|---|
| Scientific manuscript | Precise, impersonal where needed, direct | Active voice, quantified, past tense for methods |
| Grant proposal | Confident, ambitious, evidence-grounded | "We will demonstrate", "Our preliminary data show" |
| ISO/QMS documentation | Procedural, unambiguous, numbered | Imperative mood, single-action sentences |
| DestiNA tech report | Authoritative, application-focused | DCL/SMART probe nomenclature, diagnostic metrics |
| Investor/stakeholder deck | Action-oriented, high signal-to-noise | No jargon, quantified milestones, clear ask |

---

## What NOT to Change
- Facts, citations, data values, statistical outputs
- Code blocks, chemical structures, SMILES strings
- Table headers and figure captions (preserve structure, only refine wording)
- Proper nouns: DestiNA, UGR, KRT10, miR-122, MALDI-TOF
