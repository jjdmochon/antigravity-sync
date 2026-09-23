# clean-user-facing-text

**Trigger**: Full provenance hygiene pipeline. Use when the user asks to "clean", "audit", "strip AI marks", "remove watermarks", or "finalize" a document for external delivery. Combines Layer A Unicode cleaning + Layer B stylometric rewriting + metadata stripping.

---

## Pipeline Overview

```
Input text/file
     │
     ▼
Layer A — Unicode & Invisible Character Cleaning
     │
     ▼
Layer B — Stylometric Rewriting (no-ai-slop)
     │
     ▼
Layer C — Voice Calibration (humanizer-juanjo / -es)
     │
     ▼
Layer M — Metadata Stripping (files only, via CLI)
     │
     ▼
Clean output ready for delivery
```

---

## Layer A — Invisible Unicode Cleaning

### If working with a local file (device_bash available):
```bash
# Quick text scrub (Markdown, TXT, HTML):
wm-text "<ruta_archivo>" -o "<ruta_limpia>" --stats

# Full clean including metadata (PDF, DOCX, ODT, images):
wm-clean "<ruta_archivo>" -o "<ruta_limpia>"

# Inspect before cleaning:
wm-inspect "<ruta_archivo>"
```

### If working with inline text only:
Scan for and remove these Unicode ranges:
- **Zero-width characters**: U+200B (ZWSP), U+200C (ZWNJ), U+200D (ZWJ), U+2060 (WJ), U+FEFF (BOM/ZWNBS)
- **Bidi overrides**: U+202A, U+202B, U+202C, U+202D, U+202E, U+2066–U+2069
- **Soft hyphen**: U+00AD (only if not semantically meaningful)
- **Space homoglyphs**: U+00A0 (NBSP) → replace with regular space unless intentional; U+2009 (thin space), U+202F (narrow NBSP)
- **Homoglyph letters**: Cyrillic а/е/о/р/с/х/у lookalikes substituted for Latin — flag but do not auto-replace

Report count of removed characters in a brief summary line.

---

## Layer B — Stylometric Cleaning

Apply the full `no-ai-slop` protocol:

**Priority targets for stylometric detection:**
1. Burstiness variance normalization (AI text has unusually uniform sentence length) → vary sentence rhythm
2. N-gram density of high-frequency AI phrases (the 10 categories in `no-ai-slop`)
3. Passive construction density > 30% → reduce
4. Hedge stacking → eliminate
5. Rule-of-three cadence → vary or collapse

**Do not rewrite** if the text was clearly human-authored (low slop score < 3/10). Report score and stop.

---

## Layer C — Voice Calibration

After Layer B, apply voice calibration:
- **English text** → apply `humanizer-juanjo` protocol
- **Spanish text** → apply `humanizer-juanjo-es` protocol
- **Mixed language** → apply appropriate protocol per section

---

## Layer M — Metadata Stripping (file deliverables)

For any output file that will leave the workspace:

```bash
# Images (PNG, JPEG, WebP, SVG):
wm-clean "<imagen>" -o "<imagen_limpia>"
# Strips: EXIF, XMP, IPTC, C2PA manifests

# Documents (PDF):
wm-clean "<doc.pdf>" -o "<doc_limpia.pdf>"
# Strips: XMP metadata, Creator tool, Producer, ModDate with AI signatures

# Word documents (DOCX, ODT):
wm-clean "<doc.docx>" -o "<doc_limpia.docx>"
# Strips: Author field, LastModifiedBy, revision history author names with AI signatures

# Markdown / HTML:
wm-text "<doc.md>" -o "<doc_limpia.md>"
# Strips: invisible Unicode, tracking comments in HTML
```

---

## Audit Mode

When the user asks to "audit" a folder or file without cleaning:
```bash
wm-audit "<directorio>" --check-stylometry
# Returns: file-by-file inventory of detected markers

wm-score "<archivo>" --explain
# Returns: stylometry score with per-category breakdown
```

Report findings in this format:
```
AUDIT REPORT — <filename>
━━━━━━━━━━━━━━━━━━━━━━━━
Unicode markers found: X characters (types: ZWSP ×N, BOM ×N)
Stylometry score: X/10
  - Rule-of-three: X instances
  - Hollow openers: X instances
  - Passive density: X%
C2PA manifest: [Present / Absent]
EXIF AI tags: [Present / Absent]

Recommendation: [Clean urgently / Minor cleanup / Acceptable]
```

---

## Delivery Checklist

Before returning the cleaned file:
- [ ] Layer A: no invisible Unicode remaining (`wm-inspect` returns 0 markers)
- [ ] Layer B: slop score < 3/10
- [ ] Layer C: voice calibrated to Juanjo profile
- [ ] Layer M: metadata stripped (if file)
- [ ] Facts and citations unchanged
- [ ] Unicode math/chemistry notation preserved
- [ ] No LaTeX delimiters introduced
