---
name: google-dev-style-guide
description: >-
  Use this skill when writing, editing, reviewing, or auditing technical documentation, developer guides,
  API references, READMEs, code comments, release notes, or tutorials to ensure alignment with the Google
  Developer Docs Style Guide. Applies comprehensive standards for voice, tone, second person ("you"), active voice,
  sentence case headings, clean code samples, accessibility, objective writing, abbreviations (no i.e./e.g., no acronym verbs),
  contractions, timeless documentation (no "currently/now"), prescriptive guidelines (avoid "should"),
  Google Word List, Product Names rules, and clear technical communication.
---

# Google Developer Docs Style Guide

This skill provides comprehensive editorial and technical writing guidelines based on the **Google Developer Documentation Style Guide**. Use these principles to write, edit, and review clear, consistent, accessible, and user-focused developer documentation.

---

## Reference Hierarchy

When resolving editorial or stylistic questions, apply references in the following strict order:

1. **Project-Specific Style:** Follow style guidance, product glossaries, or explicit exceptions specific to your repository or product.
2. **This Google Developer Style Guide, Word List, Product Names, & Core Standards:** Follow the guidelines defined in this skill, the official [Google Developer Word List](https://developers.google.com/style/word-list), [Product Names Rules](https://developers.google.com/style/product-names), [Text-Formatting Summary](https://developers.google.com/style/text-formatting), [Accessibility Guidelines](https://developers.google.com/style/accessibility), and [Avoiding Excessive Claims](https://developers.google.com/style/excessive-claims).
3. **Third-Party References:** If neither project-specific rules nor this guide provide explicit answers, consult:
   * **Spelling:** [Merriam-Webster.com](https://www.merriam-webster.com/) (American English standard; use first listed form, e.g. *canceled*, *indexes*).
   * **Nontechnical Style & Grammar:** [*The Chicago Manual of Style*, 17th edition](https://www.chicagomanualofstyle.org/).
   * **Technical Style:** [Microsoft Writing Style Guide](https://docs.microsoft.com/style-guide/welcome/) (verify that guidance is general and not Microsoft-product-specific).
   * **Established Corpus Usage:** Check existing organizational documentation or broader corpora via [Google Ngram Viewer](https://books.google.com/ngrams/).

### Other Community Style Resources
* [Apple Style Guide](https://help.apple.com/applestyleguide/)
* [Red Hat Supplementary Style Guide for Product Documentation](https://redhat-documentation.github.io/supplementary-style-guide/)

---

## Core Editorial Principles

### 1. Voice, Tone, and Person
* **Address the Developer ("You"):** Use second person (`you`, `your`). Avoid first-person plural (`we`, `our`, `us`) unless referring explicitly to Google/the core engineering team.
* **Active Voice:** Keep sentences direct and clear (`The server processes the request` instead of `The request is processed by the server`).
* **Present Tense:** Describe software behavior as it happens now (`The function returns a string` instead of `The function will return a string`).
* **Imperative Mood & Prescriptive Verbs:** Start procedural steps with direct action verbs (`Configure`, `Install`, `Click`). Use **must** for mandatory actions and **We recommend** for suggestions. **Avoid *should*** because it creates ambiguity.

### 2. Language, Grammar, and Abbreviations
* **No `i.e.` or `e.g.`:** Use **"that is"** (for *i.e.*) and **"for example"** (for *e.g.*).
* **Introducing Acronyms:** Spell out on first mention followed by acronym in parentheses `Application Programming Interface (API)`. Exceptions: universally known developer terms (`API`, `URL`, `HTML`, `JSON`, `HTTP`). No periods in acronyms (`API`, NOT `A.P.I.`).
* **No Acronym Verbs:** Never use acronyms as verbs (*use SSH to log in*, NOT *ssh into*).
* **Contractions:** Use standard two-word contractions (*you're*, *don't*, *can't*, *isn't*)—especially negative contractions (*don't* instead of *do not*), which prevent readers from missing standalone negation words when scanning.
* **No Anthropomorphism:** Software/hardware does not think or feel (*The server determines*, NOT *The server thinks*).
* **Articles (`a` vs `an`):** Use `an` before vowel sounds (`an API`, `an RPC`), `a` before consonant sounds (`a URL`, `a database`).

### 3. Timeless Documentation
* **Avoid Temporal Anchors:** Do **not** use *now*, *currently*, *recently*, *new*, *in the future*, or *soon*. Describe software as it operates today.
* **No Speculative Future Features:** Do not document unreleased roadmap features in standard technical guides.

### 4. Objective Tone & Avoiding Excessive Claims
* **No Superlatives:** Avoid unprovable fluff (*best*, *fastest*, *simplest*, *most powerful*, *revolutionary*).
* **Remove "Easily" and "Simply":** Delete condescending filler (*you can easily*, *simply click*, *just run*). Start directly with the action verb (*To set up X, run Y*).
* **Design Intent vs. Absolutes:** Frame security and uptime around design intent (*designed to mitigate access*), never absolute guarantees (*guarantees 100% security*).
* **Quantify Performance:** Replace vague adjectives (*blazing fast*) with explicit benchmark metrics (*sub-50ms latency*).

### 5. Headings and Structure
* **Sentence Case:** Capitalize only the first word, proper nouns, and acronyms in titles and headings (`Setting up your environment`, NOT `Setting Up Your Environment`).
* **Task-Oriented & Descriptive:** Make procedure headings action-oriented (`Create an API key`) and conceptual headings clear (`Authentication overview`).
* **Sequential Hierarchy:** Never skip heading levels (`#` -> `##` -> `###`).

### 6. Text Formatting & Syntax
* **Bold (`**text**`):** Use **bold** ONLY for UI elements (buttons, menus, field labels, key shortcuts) and run-in lead-in headings for notes/alerts. Do NOT use bold for emphasis.
* **Italics (`_text_`):** Use single underscores `_text_` sparingly for defining new terms, "words as words", titles of full works, math/version variables (*x*, *1.4.x*), and light semantic emphasis.
* **Code Font (`` `code` ``):** Wrap filenames, directories, parameters, classes, methods, status codes, IP addresses, ports, and CLI flags in single backticks.
* **Underline:** Reserved **strictly for hyperlinks** (never manually underline text).

### 7. Accessibility & Screen Readers
* **No Directional Language:** Do **not** use spatial orientation words (*above*, *below*, *left-hand sidebar*, *bottom of the page*). Use *preceding*, *earlier*, *following*, or specific component names.
* **Descriptive Alt Text:** Provide intent-focused `alt` text for all images. Never embed critical text, code, or logs in images.
* **Simple Tables:** Avoid merged cells (`colspan`/`rowspan`). Introduce tables in preceding prose and use `<th>` tags with `scope`.
* **Multi-Cue State Indicators:** Never rely solely on color or shape to convey status (pair color dots with text labels or icons).

### 8. Product Names & Branding
* **Official Branding:** Preserve exact official capitalization, spacing, and casing (`GitHub`, `iOS`, `PyTorch`).
* **Never Use Product Names as Verbs:** Use standard verbs (*search using Google*, NOT *Google the error*; *containerize with Docker*, NOT *Dockerize*).
* **No Direct Pluralization:** Add generic noun descriptors (*Cloud Run services*, NOT *Cloud Runs*).
* **Avoid Possessives:** Use proper noun modifiers (*BigQuery performance*, NOT *BigQuery's performance*).

---

## Overriding Principle: Guidelines, Not Rigid Rules

> *"This guide contains guidelines, not rules. Depart from it when doing so improves your content... Break any of these rules sooner than say anything outright barbarous."*

Style guidelines provide consistency, but domain appropriateness and clarity always take precedence:
* **Domain Adaptation:** Depart from general guide recommendations if your domain or audience uses established competing terminology.
* **Internal Consistency:** **When you depart from this guide, be consistent throughout your document.**
* **Pragmatic Flexibility:** Always prioritize reader comprehension over blind adherence to stylistic conventions.

---

## 7-Step Editorial Audit Pipeline

When asked to review, edit, or write documentation using this style guide, execute the following audit steps:

1. **Voice, Person & Objectivity Check:** Convert "we/our" to "you/your" or direct imperatives. Strip marketing superlatives (*best*, *fastest*) and patronizing fluff (*easily*, *simply*, *just*). Remove modal *should* (use *must* or *we recommend*).
2. **Heading & Title Case Check:** Convert Title Case headings to Sentence case. Ensure headings are task-focused.
3. **Language, Grammar & Abbreviations Check:** Replace `i.e.` and `e.g.`, remove periods in acronyms (`API`), fix acronym verbs (*SSH into* -> *use SSH to log in*), add negative contractions (*don't*), remove anthropomorphism (*server thinks*), and strip temporal words (*currently*, *now*).
4. **Text Formatting Check:** Ensure **bold** is used ONLY for UI elements and alert headings (`**`), _italics_ uses underscores `_text_` for new terms/variables, backticks for code font, and underline reserved for links.
5. **Accessibility Check:** Eliminate directional language (*above*, *below*), verify image `alt` text, check table cell structure (no `colspan`/`rowspan`), and ensure color states have text labels.
6. **Code Block Sanitation:** Verify language tags, remove unnecessary `$` prompt symbols from terminal blocks, and sanitize credentials.
7. **Word List, Product Names & Consistency Audit:** Check terms against Google Word List (*about* vs *on*, *username*, *lets you*), enforce product name rules (no verbs, no possessives, generic plurals), replace biased terminology, and verify document-wide consistency.

---

## Quick Reference Table (Before vs. After)

| Pattern | Anti-Pattern (Avoid) | Preferred (Google Style) |
| :--- | :--- | :--- |
| **Latin Abbr.** | *i.e. / e.g.* | *that is / for example* |
| **Acronym Verbs** | *SSH into the server* | *Use SSH to log in to the server* |
| **Temporal Words** | *Currently, the API supports X* | *The API supports X* |
| **Modal Verbs** | *You should set the header* | *You must set the header / We recommend setting...* |
| **Fluff & "Easily"** | *You can easily set up X by simply...* | *To set up X, run...* |
| **Superlatives** | *The fastest and best database engine* | *A low-latency relational database engine* |
| **Spatial Direction** | *As shown in the table below...* | *As shown in the following table...* |
| **Person & Voice** | *We will now update the database...* | *Next, update the database...* |
| **Product Verbs** | *Google the log / Dockerize the app.* | *Search with Google / Containerize with Docker.* |
| **Terms** | *account name*, *allows you to*, *agnostic* | *username*, *lets you*, *platform-independent* |

---

## Comprehensive Reference Guides Directory

For detailed rules and specific edge cases across all Google Style subpages, refer to the following guide modules in `references/`:

* [Language, Grammar & Abbreviations Reference](./references/language-grammar-and-abbreviations.md)
* [General Principles & Timeless Documentation](./references/general-principles-and-timelessness.md)
* [Objective Writing & Avoiding Excessive Claims](./references/objective-claims-and-tone.md)
* [Accessibility & Screen Readers Guide](./references/accessibility-and-screen-readers.md)
* [Text Formatting & Typography Summary Guide](./references/formatting-and-punctuation.md)
* [Product Names Guidelines Reference](./references/product-names.md)
* [Google Developer Word List & Terminology Reference](./references/word-list-and-terms.md)
* [Tone, Voice, and Person Guidelines](./references/tone-and-voice.md)
* [Code Samples, Technical Elements, and API References](./references/code-and-api-docs.md)
* [Inclusive Language and Global Accessibility](./references/inclusive-and-global.md)
