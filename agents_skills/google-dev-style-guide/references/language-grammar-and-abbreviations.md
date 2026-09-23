# Google Developer Style Guide: Language and Grammar Reference

This reference provides exhaustive guidelines for all **14 core areas** of the **[Language and grammar](https://developers.google.com/style)** section of the Google Developer Documentation Style Guide.

---

## 1. Abbreviations & Acronyms
- **Spell out on first mention:** Provide the full term followed by the abbreviation in parentheses: `Application Programming Interface (API)`.
- **Known acronym exceptions:** Do not spell out universally recognized terms (`API`, `URL`, `HTML`, `JSON`, `HTTP`, `CLI`, `SDK`).
- **No Latin abbreviations:**
  - Avoid `i.e.` &rarr; use **"that is"** or **"namely"**.
  - Avoid `e.g.` &rarr; use **"for example"** or **"such as"**.
  - Avoid `etc.` &rarr; specify complete lists or use "including...".
- **No periods in acronyms:** Write `API`, `URL`, `IP` (never `A.P.I.`, `U.R.L.`).
- **Never use acronyms or initialisms as verbs:**
  - *Incorrect:* SSH into the remote machine.
  - *Correct:* Use SSH to log in to the remote machine.

---

## 2. Active Voice
- **Subject performs the action:** Always prefer active voice over passive voice for directness and conciseness.
  - *Passive (avoid):* The configuration is loaded by the application at startup.
  - *Active (preferred):* The application loads the configuration at startup.
- **When passive voice is acceptable:** Use passive voice only when the actor is completely unknown, irrelevant, or when emphasizing the object/recipient is critical for user safety.

---

## 3. Anthropomorphism (Avoid Human Attributes)
- **Software and hardware do not have feelings, thoughts, desires, or personal agency:**
  - *Incorrect:* The server thinks the token is expired.
  - *Correct:* The server determines that the token is expired.
  - *Incorrect:* The API wants you to specify an environment.
  - *Correct:* The API requires an environment parameter.
  - *Incorrect:* The program refuses to start.
  - *Correct:* The program fails to start.

---

## 4. Articles (*a*, *an*, *the*)
- **Sound-based rule for *a* vs *an*:** Base the article on the **phonetic sound** of the following word or acronym when spoken aloud:
  - Use **`an`** before vowel sounds: `an API` (*an ey-pee-eye*), `an HTTP request` (*an aytch-tee-tee-pee*), `an RPC`, `an SSH key`, `an SQL query` (*an ess-cue-el*).
  - Use **`a`** before consonant sounds: `a URL` (*a you-are-el*), `a database`, `a JSON object`, `a unique ID`.
- **Do not omit articles:** Avoid "telegraphic" or robotic headlinese in body copy or steps (e.g., write *Click the button*, not *Click button*).

---

## 5. Capitalization
- **Headings and page titles:** Use **Sentence case** for all headings (capitalize only the first word, proper nouns, and acronyms).
  - *Incorrect:* Configuring Your Authentication Credentials
  - *Correct:* Configuring your authentication credentials
- **Code symbols and product names:** Respect original case sensitivity (`JavaScript`, `GitHub`, `OAuth`, `Node.js`, `camelCase`).
- **UI Elements:** Match the exact capitalization shown in the product UI.

---

## 6. Contractions
- **Encouraged in technical prose:** Use common two-word contractions (*you're*, *it's*, *don't*, *can't*, *isn't*, *there's*) for an approachable, natural tone.
- **Favor negative contractions:** Use *don't* or *can't* rather than *do not* or *cannot*.
  - *Rationale:* Quick-scanning readers frequently miss standalone negation words ("not"). Contractions weld the negation directly to the auxiliary verb.
- **Avoid ambiguous or complex contractions:** Avoid *should've*, *could've*, *it'd*, or *who'll*.

---

## 7. Pluralization
- **Acronym plurals:** Add a lowercase `s` without an apostrophe (`APIs`, `URLs`, `SDKs`, `IPs` &mdash; never `API's`).
- **Latin and Greek plurals:** Use standard English plurals rather than classical forms (e.g., *indexes* not *indices*, *appendixes* not *appendices*, *schemas* not *schemata*).
- **Product names:** Never pluralize product names directly. Add a plural generic noun:
  - *Incorrect:* Deploy multiple Cloud Functions.
  - *Correct:* Deploy multiple Cloud Functions instances (or *functions*).

---

## 8. Possessives
- **Singular/Plural nouns:** Use standard `'s` for singular possessives (`the user's account`) and `s'` for plural possessives (`the users' accounts`).
- **No possessives for acronyms, code elements, or product names:**
  - *Incorrect:* The API's response payload / BigQuery's syntax.
  - *Correct:* The API response payload / BigQuery syntax.
- **Its vs. It's:** *Its* is possessive; *It's* is the contraction for *it is*.

---

## 9. Prepositions
- **Ending sentences with prepositions:** Completely acceptable if natural and readable (*The directory you want to save to* is better than *The directory to which you want to save*).
- **Correct preposition usage:**
  - Use **"on"** for platforms, devices, operating systems, and topics (*on Android*, *on macOS*).
  - Use **"in"** for languages, directories, or containers (*in Python*, *in `/var/log`*).
  - Use **"to"** vs **"with"** appropriately (*connect to*, *compatible with*).
  - Avoid using "about" where "for" or "on" is more precise.

---

## 10. Present Tense
- **Describe state and behavior in present tense:** Describe software as it operates currently, not as future events.
  - *Incorrect:* Calling `connect()` will establish a TCP connection.
  - *Correct:* Calling `connect()` establishes a TCP connection.
- **Avoid modal "will":** Eliminate predictive "will" when explaining execution or workflows.

---

## 11. Pronouns & Clear Antecedents
- **Second person default:** Use *you* and *your*.
- **Gender-neutral third-person:** Use singular *they*, *them*, *their* when third person is unavoidable, or rewrite into imperative mood / second person.
- **Unambiguous reference (avoid vague "this" or "it"):** Always clarify the antecedent noun after demonstrative pronouns:
  - *Vague:* This occurs when the timeout expires.
  - *Clear:* This error occurs when the timeout expires.

---

## 12. Second Person (*You*)
- **Direct address:** Address the developer directly as *you* and *your*.
- **Avoid first-person plural (*we*, *our*, *us*):** Technical documentation is about the user's task, not the authors'.
  - *Incorrect:* In this tutorial, we will create a Dockerfile.
  - *Correct:* In this tutorial, you create a Dockerfile (or imperative: *Create a Dockerfile*).
- **Exception for "We":** Reserve *we* solely for organizational stances or formal recommendations (*We recommend using TLS 1.3*).

---

## 13. Sentence Structure & Readability
- **Optimal sentence length:** Keep sentences focused and concise (aim for under 25 words).
- **Lead with context/condition before action:**
  - *Incorrect:* Click **Submit** to send your registration form.
  - *Correct:* To send your registration form, click **Submit**.
- **Parallel grammatical structure:** Ensure items in lists, bullet points, and tables share identical grammatical forms (e.g., all imperative verbs or all noun phrases).

---

## 14. Verbs in Reference Documents
- **Third-person singular present tense:** For API reference descriptions, method summaries, and field definitions, use third-person singular active verbs.
  - *Method summary:* `Returns the active user profile.` (NOT `Return the...` or `Will return the...`).
  - *Parameter description:* `Specifies the maximum number of items to retrieve.`
  - *Property description:* `Contains the HTTP response status code.`
