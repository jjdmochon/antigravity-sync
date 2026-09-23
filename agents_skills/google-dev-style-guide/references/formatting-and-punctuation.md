# Formatting, Typography, and Punctuation Reference (Google Developer Docs Style Guide)

This guide provides comprehensive editorial standards for **Markdown formatting**, **typography**, and all **10 official Punctuation sections** from the [Google Developer Documentation Style Guide](https://developers.google.com/style/punctuation).

---

## Part 1: Official Punctuation Guide (10 Topics)

### 1. Colons
- **Introducing lists and code:** Use a colon at the end of a complete sentence that introduces a bulleted list, numbered procedure, or code snippet.
- **Capitalization after colons:**
  - If the text following the colon is a **complete, independent sentence**, capitalize the first letter.
  - If the text is a **fragment or continuing clause**, do not capitalize the first letter.
- **Avoid colon stacking:** Never place a colon after a heading or within introductory fragments that lack a complete clause.

---

### 2. Commas
- **Serial (Oxford) Comma:** Always use the serial comma before the coordinating conjunction (*and*, *or*) in lists of three or more items:
  - *Correct:* The API supports JSON, XML, and protocol buffers.
  - *Incorrect:* The API supports JSON, XML and protocol buffers.
- **Introductory Clauses:** Place a comma after introductory dependent clauses, prepositional phrases, and transition words (*However,*, *For example,*).
- **Compound Sentences:** Use a comma before a coordinating conjunction (*and*, *but*, *so*, *or*) when connecting two independent clauses.
- **Restrictive vs. Non-Restrictive (*that* vs. *which*):** Use *that* without commas for essential restrictive clauses; use *, which* with commas for non-essential descriptive clauses.

---

### 3. Dashes (Em Dashes & En Dashes)
- **Em Dash (`—`):** Use an em dash to indicate a significant break in thought or an emphatic parenthetical phrase.
  - **No spaces:** Do not put spaces before or after an em dash (`service—once initialized—listens on port 8080`).
- **En Dash (`–`):** Use an en dash to indicate ranges of numbers, dates, or pages (`pages 10–25`, `2024–2026`, `100–200 ms`).
- **Do not substitute hyphens for dashes:** Never use a single hyphen `-` or double hyphen `--` where an em dash `—` or en dash `–` is required in rendered documentation.

---

### 4. Ellipses
- **Omission in Quotes/Logs:** Use an ellipsis (`...` or `…`) with spaces around it to indicate omitted words or lines in code outputs or quotations.
- **Progress & Truncation:** In UI text, use an ellipsis only for in-progress operations (`Loading...`, `Saving...`).
- **Avoid in Prose:** Do not use ellipses to indicate trailing thoughts or conversational pauses in technical documentation.

---

### 5. Hyphens
- **Compound Modifiers:** Hyphenate compound adjectives when they precede the noun they modify, but not when they follow the noun:
  - *Preceding noun:* `open-source project`, `client-side rendering`, `read-only file`.
  - *Following noun:* `The project is open source`, `rendering occurs client side`.
- **No Hyphen with *-ly* Adverbs:** Never hyphenate adverbs ending in *-ly* with an adjective (`highly scalable architecture`, NOT `highly-scalable`).
- **Prefixes:** Most common technical prefixes are closed without hyphens (`multithreaded`, `microservice`, `reinstall`, `subquery`), unless needed to prevent misreading (`re-create` vs `recreate`, `pre-existing`).

---

### 6. Parentheses
- **Punctuation Placement:**
  - If the entire sentence is enclosed in parentheses, place the period **inside** the closing parenthesis: `(This feature requires administrator privileges.)`
  - If the parenthetical remark is part of a larger sentence, place the punctuation **outside** the closing parenthesis: `Configure your settings in the console (or CLI).`
- **Avoid Nested Parentheses:** Do not place parentheses inside parentheses; rewrite the sentence or use commas/em dashes.

---

### 7. Periods and End Punctuation
- **Complete Sentences:** Every complete sentence must end with a period.
- **List Items:**
  - End list items with a period if they are complete sentences or imperative commands.
  - Omit trailing periods if all list items are short sentence fragments or single words.
- **Headings & Tables:** Do **not** put periods at the end of headings, titles, subheadings, or table header cells.
- **Exclamation Marks:** Avoid exclamation marks in technical documentation (except in code syntax or warnings where critical for safety).

---

### 8. Quotation Marks
- **American English Placement:** Place periods and commas **inside** quotation marks:
  - *Correct:* The parameter is labeled "Optional."
- **Colons & Semicolons:** Place colons and semicolons **outside** quotation marks.
- **Double vs. Single:** Always use double quotation marks (`"text"`). Use single quotation marks (`'text'`) only for nested quotes within quotes.
- **UI Elements & Code Symbols:** Do **not** use quotation marks for UI elements (use **bold**) or code symbols/parameters (use `` `code font` ``).

---

### 9. Semicolons
- **Independent Clauses:** Use a semicolon sparingly to link two closely related independent clauses without a conjunction. Prefer splitting into two distinct sentences for maximum readability.
- **Complex Lists:** Use semicolons to separate items in a series when the items themselves contain internal commas:
  - *Example:* The committee included Alice Smith, Director; Bob Jones, Lead Architect; and Carol White, Lead Engineer.

---

### 10. Slashes
- **Avoid in Prose:** Do not use slashes (`/`) to represent alternatives (avoid `and/or`, `he/she`, `input/output`, `w/o`). Write out `and or or`, `input and output`, or `without`.
- **Acceptable Uses:** Slashes are reserved strictly for:
  - File paths and directories (`/usr/local/bin`, `src/index.ts`).
  - URLs (`https://developers.google.com/style`).
  - Mathematical fractions or division operations (`MB/s`).

---

## Part 2: Markdown & Text Formatting Reference

| Format | Markdown Syntax | Allowed Usage | Prohibited Usage |
| :--- | :--- | :--- | :--- |
| **Bold** | `**text**` | **UI elements** (buttons, menus, labels, key shortcuts) and run-in headings for notes/alerts. | Do **not** use for general emphasis or headings. |
| *Italics* | `_text_` | New terms on first mention, "words as words", titles of full works, math/version variables (*x*, *1.4.x*), and light semantic emphasis. | Do **not** over-use or use for UI elements. |
| `Code Font` | `` `code` `` | Inline code, function/class names, parameters, CLI flags, filenames, paths, IP addresses, ports, package names, HTTP status codes, user input. | Do **not** use proportional font for technical identifiers. |
| <u>Underline</u> | N/A | Reserved **strictly for hyperlinks**. | Do **not** manually underline any text. |

---

## Part 3: Headings, Lists & Structural Guidelines

- **Sentence Case Headings:** Capitalize only the first word of titles and headings, plus proper nouns and acronyms (`Setting up your development environment`).
- **Sequential Hierarchy:** Maintain strict sequential hierarchy (`#` -> `##` -> `###`).
- **Numbered vs. Bulleted Lists:**
  - Use numbered lists for sequential steps and workflows.
  - Use bulleted lists for non-sequential items and options.
- **Descriptive Link Text:** Always describe the destination link target (never write `click here` or paste bare URLs).
