# Google Developer Style Guide: Product Names Guidelines

This reference covers the official rules for writing, capitalizing, and formatting product, brand, service, and feature names.

---

## 1. Official Casing & Trademarking
- **Follow Official Branding:** Always use the official capitalization, spacing, and spelling established by the product owner or documentation.
  - *Examples:* `GitHub`, `Kubernetes`, `LaTeX`, `iOS`, `PyTorch`, `Google Cloud`.
- **Lowercase Initial Product Names:** If an official product name begins with a lowercase letter (e.g., `iOS`, `eBay`), preserve the lowercase letter even at the beginning of a sentence.
  - *Better:* Rephrase the sentence so the lowercase product name does not start the sentence.
  - *Incorrect:* Ios supports background tasks.
  - *Correct:* The iOS operating system supports background tasks.

---

## 2. Product Names vs. Feature Names
- **Product Names (Title Case):** Capitalize official product names and service titles (*Google Cloud Storage*, *BigQuery*, *Firebase Realtime Database*).
- **Feature Names (Lowercase):** Use lowercase for general product features unless they are officially trademarked or capitalized by the product team.
  - *Incorrect:* Use the Database Backup Feature.
  - *Correct:* Use the database backup feature.
- **UI Labels:** Match the exact capitalization used in the product user interface (*Click **Create Service Account***).

---

## 3. Grammatical Rules for Product Names

### Do NOT Use Product Names as Verbs
Never turn a product name into a verb. Instead, use a standard verb paired with the product name as a noun.
- *Incorrect:* Google the error log to find solutions.
- *Correct:* Search for the error log using Google to find solutions.
- *Incorrect:* Dockerize your application.
- *Correct:* Containerize your application using Docker.

### Avoid Possessives
Avoid forming possessives with product names. Use the product name as a proper adjective or noun modifier instead.
- *Incorrect:* BigQuery's performance is optimized for large datasets.
- *Correct:* BigQuery performance is optimized for large datasets.

### Pluralization & Generic Descriptors
Never pluralize a product name directly. Append a generic plural noun descriptor instead.
- *Incorrect:* Deploy multiple Cloud Runs.
- *Correct:* Deploy multiple Cloud Run services.

---

## 4. Shortening Product Names
- On first mention in a document, use the full official product name (e.g., *Google Cloud BigQuery*).
- On subsequent mentions, you may use an approved shortened form (e.g., *BigQuery*), provided it remains unambiguous.
- Never invent unauthorized abbreviations or acronyms for product names.
