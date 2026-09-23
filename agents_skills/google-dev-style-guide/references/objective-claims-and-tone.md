# Google Developer Style Guide: Objective Writing & Avoiding Excessive Claims

This reference provides technical writing standards for maintaining an objective, verifiable, and fluff-free tone based on the **Google Developer Excessive Claims Guide**.

---

## 1. Eliminate Marketing Fluff & Superlatives

Developers read technical documentation to solve problems, not to be sold. Avoid subjective marketing hype and unprovable superlatives.

- **Prohibited Superlatives:** *best*, *fastest*, *simplest*, *most powerful*, *revolutionary*, *state-of-the-art*, *always*, *never*.
- **Rules & Replacements:**
  - *Incorrect:* BigQuery is the fastest and best data warehouse for analytics.
  - *Correct:* BigQuery is a cloud data warehouse designed for large-scale analytics.

---

## 2. Remove Subjective "Easy" and "Simple" Claims

Avoid patronizing phrases like *easily*, *simply*, *just*, *it is easy to*, or *straightforward*.

- **Why:** What is "simple" for an expert may be complex or frustrating for a beginner. Removing these words makes prose shorter, direct, and universally respectful.
- **Rules & Replacements:**
  - *Incorrect:* You can easily set up the database by simply running `npm start`.
  - *Correct:* To set up the database, run `npm start`.
  - *Incorrect:* Just click **Deploy**.
  - *Correct:* Click **Deploy**.

---

## 3. Design Intent vs. Guaranteed Absolutes

Software systems can experience outages, vulnerabilities, or edge-case failures. Frame security, reliability, and performance in terms of **design intent** rather than absolute guarantees.

| Claim Category | Excessive / Absolute Claim (Avoid) | Objective / Design-Focused (Preferred) |
| :--- | :--- | :--- |
| **Security** | *This architecture guarantees 100% security against attacks.* | *This architecture is designed to mitigate unauthorized access.* |
| **Reliability** | *Ensures zero downtime.* | *Helps minimize downtime using redundant clusters.* |
| **Performance** | *Delivers blazing fast response times.* | *Optimized for sub-50ms latency (see [Benchmark Report](...)).* |

---

## 4. Benchmark & Citation Requirements

- **Quantify Performance:** Replace vague adjectives (*blazing fast*, *ultra low-memory*) with concrete metrics (*response latency under 20ms*, *memory footprint below 128MB*).
- **Cite Sources:** Provide links to benchmark methodologies or test parameters when stating performance metrics.

---

## 5. Third-Party Neutrality

- **Objective Comparisons:** Never use disparaging, condescending, or hostile language when referencing open-source alternatives or third-party products.
- **Factual Distinctions:** Focus strictly on architectural differences, supported protocols, or compatibility features.
