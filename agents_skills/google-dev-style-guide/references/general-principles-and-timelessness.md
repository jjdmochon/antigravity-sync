# Google Developer Style Guide: General Principles & Timeless Documentation

This reference details core guidelines for timeless documentation, prescriptive recommendations, avoiding jargon, future feature handling, and third-party content.

---

## 1. Timeless Documentation (Avoid Temporal Words)

Documentation should remain accurate over long periods without requiring frequent edits to remove stale time references.

- **Avoid Time-Anchored Words:** Do not use *now*, *currently*, *recently*, *new*, *in the future*, *soon*, or *version 3 coming later*.
  - *Incorrect:* Currently, BigQuery supports JSON data types.
  - *Correct:* BigQuery supports JSON data types.
  - *Incorrect:* Next month, the endpoint will require OAuth.
  - *Correct:* In API v2.0, the endpoint requires OAuth.
- **Exceptions:** Temporal words are acceptable only in inherently time-sensitive materials like release notes, changelogs, or blog posts.

---

## 2. Prescriptive Documentation & Modal Verbs

Prescriptive (opinionated) guidance recommends the single best path to achieve a goal rather than overwhelming readers with every possible alternative.

- **Must (Mandatory):** Use **must** (or direct imperative verbs) for required steps.
- **We Recommend (Suggested):** Use **We recommend** or **[Product] recommends** for best practices.
- **Avoid *Should* (Ambiguous):** Do **NOT** use *should*. *Should* leaves ambiguity about whether an action is mandatory or optional.
  - *Incorrect:* You should set the authorization header.
  - *Correct (Mandatory):* You **must** set the authorization header. / Set the authorization header.
  - *Correct (Best Practice):* **We recommend** setting a 30-second timeout.

---

## 3. Future Features & Unreleased Tech

- **Do NOT Document Speculative Features:** Never document unreleased, beta, or roadmap features in standard technical guides unless specifically creating preview/beta documentation.
- **Unreleased APIS:** If referencing preview/alpha features, explicitly tag them (`[Alpha]` or `[Beta]`) and state their preview status.

---

## 4. Jargon & Clear Terminology

- **Avoid Unnecessary Jargon:** Replace obscure internal jargon with plain, universally understood developer terms.
- **Define Essential Jargon:** If specialized domain jargon is unavoidable, define the term on first use or link to a glossary entry.

---

## 5. Third-Party Content & Attribution

- **Distinguish External Tools:** Clearly separate primary product instructions from third-party tools, libraries, or dependencies.
- **Maintain Neutrality:** Describe third-party integrations factually without making disparaging claims or unverified performance guarantees.
