---
name: anydoc
description: Convert Word (.doc, .docx), PowerPoint (.ppt, .pptx), Excel (.xls, .xlsx), OpenDocument (.odt, .ods, .odp), RTF, EPUB, CSV, and PDF files to GitHub-Flavored Markdown and extract embedded images/assets. Use when a task needs the contents of an office document, spreadsheet, presentation, ebook, or PDF.
license: MIT
metadata:
  author: firecrawl
---

# Convert documents to Markdown (with assets extraction)

Convert any document into Markdown and extract embedded images/assets automatically in one step:

```bash
python scripts/convert_anydoc.py <file>              # Convert to <file>.md and extract assets to <file>_assets/
python scripts/convert_anydoc.py <file> out.md       # Write to custom output file
npx -y @firecrawl/anydoc <file> -o out.md            # CLI mode (Markdown text only, without asset extraction)
```

Rules:

1. Supported inputs: `.doc`, `.docx`, `.docm`, `.odt`, `.rtf`, `.epub`, `.pdf`, `.ppt`, `.pps`, `.pot`, `.pptx`, `.pptm`, `.ppsx`, `.ppsm`, `.odp`, `.xls`, `.xlsx`, `.xlsm`, `.xlsb`, `.ods`, `.csv`.
2. Running `python scripts/convert_anydoc.py <file>` automatically extracts embedded images (PNG, JPEG, WMF, EMF, CDX ChemDraw drawings) into a `<file>_assets/` folder in a single step.
3. For text-only conversion without assets, use `npx -y @firecrawl/anydoc <file> -o out.md`.
