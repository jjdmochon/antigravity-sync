# Inclusive Language and Global Accessibility (Google Developer Docs Style Guide)

## 1. Gender-Neutral Language
- Use gender-neutral pronouns (**they/them/their**).
- Avoid assuming gender or using "he/she" or "(s)he".
- Better yet, rewrite sentences using second person ("you") or imperative mood to eliminate pronouns altogether.
  - *Incorrect:* A developer must register his application first.
  - *Correct:* Register your application first.

## 2. Inclusive Technical Terminology
- Avoid terms rooted in racial, historical, or ableist biases. Use technical equivalents:
  - `primary` / `main` / `replica` instead of `master` / `slave`
  - `allowlist` / `denylist` instead of `whitelist` / `blacklist`
  - `stop` / `terminate` / `end` instead of `abort` / `kill` (when referring to processes/threads in general prose, though command names like `kill` remain unchanged)
  - `placeholder` / `sample` instead of `dummy`
  - `sanity check` → `preliminary check` / `verification` / `smoke test`

## 3. Global & Cultural Accessibility
- **Avoid Idioms and Colloquialisms:** Phrases like "hit two birds with one stone", "under the hood", "piece of cake", or "ballpark estimate" do not translate well for non-native English speakers.
  - *Incorrect:* Under the hood, the SDK caches token requests.
  - *Correct:* Internally, the SDK caches token requests.
- **Avoid Ambiguous Time References:** Words like "currently", "now", "recently", "in the future", or "version 3 is coming soon" quickly become outdated. Specify version numbers or explicit dates instead.
  - *Incorrect:* Currently, this endpoint only supports JSON.
  - *Correct:* In API v1.2, this endpoint only supports JSON.

## 4. Accessibility for Screen Readers
- Provide descriptive alt text for all images and diagrams (`![Architecture diagram showing client request flow to backend service](path/to/img.png)`).
- Ensure visual tables have clear row and column headers.
- Do not rely solely on color to convey information (e.g., green vs red indicators). Use text labels or icons in addition to color.
