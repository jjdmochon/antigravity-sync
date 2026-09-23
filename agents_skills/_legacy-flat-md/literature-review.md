# literature-review

**Trigger**: Use when the user asks to search, survey, or review the scientific literature on any topic. Runs structured parallel searches across PubMed, bioRxiv, EuropePMC, arXiv, and USPTO patents. Returns a synthesis with citations, not a list of abstracts.

---

## Pre-Search Protocol

Before launching searches, identify:
1. **Topic**: extract 3-5 key search terms from the user's request
2. **Scope**: clinical / basic research / methods / patents / all?
3. **Depth**: quick survey (top 10 papers) / systematic (exhaustive) / focused (last 3 years)
4. **Output format**: summary paragraph / evidence table / annotated bibliography / full review section

Default: multi-database search, last 5 years, synthesis format.

---

## Search Execution (Parallel Agents when available)

When using the `Agent` tool for parallel execution:

```
Agent 1: PubMed + EuropePMC (peer-reviewed, clinical)
Agent 2: bioRxiv + medRxiv (preprints, latest methods)
Agent 3: arXiv (computational, physics, ML methods)
Agent 4: Google Scholar via WebSearch (broad coverage + citations)
Agent 5: USPTO/Espacenet (patents, if technology-focused)
```

Each agent returns: title, authors, year, journal/source, DOI, key quantitative finding (1 sentence).

### Search Query Construction

**PubMed / EuropePMC query syntax**:
```
("<term1>"[Title/Abstract] OR "<term2>"[Title/Abstract]) AND ("<term3>"[Title/Abstract])
Filters: Publication Date: last 5 years, Humans, English/Spanish
```

**WebSearch queries** (run 3 complementary formulations):
```
site:pubmed.ncbi.nlm.nih.gov "<exact phrase>" <year range>
"<term1>" "<term2>" review OR meta-analysis site:ncbi.nlm.nih.gov
<topic> preprint 2023 OR 2024 OR 2025 site:biorxiv.org
```

---

## Result Synthesis Protocol

Do NOT return a list of abstracts. Synthesize into:

### Structure: Evidence-Based Narrative

**1. State of the Field (1-2 paragraphs)**
What do we know? What is the consensus? Cite 3-5 landmark papers.

**2. Key Findings by Subtopic**
For each major subtopic, 1 paragraph:
- Quantitative finding with citation
- Methodological approach used
- Confidence level (n, study design, replication)

**3. Contradictions and Open Questions**
Where do studies disagree? What sample sizes are too small? What populations are understudied?

**4. Recent Developments (last 18 months)**
Preprints, emerging methods, breaking results — flagged as "not yet peer-reviewed" where applicable.

**5. Patent Landscape** (if technology-focused)
Key assignees, filing dates, claim coverage, freedom to operate signals.

---

## Citation Format

**In-text**: Author et al., Year — e.g., "López et al., 2024"
**Reference list** (Vancouver / ICMJE style):
```
1. Author AB, Author CD. Title of article. Journal. Year;Volume(Issue):Pages. doi:10.XXXX/XXXXX
```
Always include DOI. Flag if DOI could not be verified (preprint, conference abstract).

---

## Domain-Specific Search Templates

### miRNA / DCL / DestiNA
```
("miR-122" OR "miRNA-122") AND ("liver toxicity" OR "DILI" OR "hepatotoxicity") AND ("biomarker" OR "detection")
("dynamic chemical labeling" OR "aldehyde probe") AND ("nucleic acid" OR "miRNA")
("PCR-free" OR "amplification-free") AND ("nucleic acid detection") AND ("point-of-care" OR "diagnostic")
```

### PNA / Nucleic Acid Analogs
```
("peptide nucleic acid" OR "PNA") AND ("thermal denaturation" OR "melting temperature") AND ("discrimination" OR "mismatch")
("SMART probe" OR "γ-modified PNA") AND ("single nucleotide")
```

### KRT10 / Keratin / Epidermolytic Ichthyosis
```
("KRT10" OR "keratin 10") AND ("epidermolytic ichthyosis" OR "EI" OR "bullous ichthyosiform erythroderma")
("R156" OR "R162" OR "keratin mutation") AND ("filament" OR "structural")
```

### Química Física / Physical Chemistry Education
```
("physical chemistry" OR "química física") AND ("simulation" OR "interactive") AND ("undergraduate" OR "teaching")
("thermodynamics teaching" OR "kinetics simulation") AND ("web" OR "HTML5" OR "applet")
```

---

## Quality Gates Before Returning Results

- [ ] All DOIs verified (WebSearch to confirm publication exists)
- [ ] No hallucinated papers — if a paper cannot be confirmed, flag it
- [ ] Synthesis, not list — prose paragraphs with integrated citations
- [ ] Statistical claims include n and p-values from original source
- [ ] Preprints clearly labeled as "not peer-reviewed"
- [ ] Year range matches user's request
