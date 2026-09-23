# Google Developer Style Guide: Word List & Terminology Reference

The **Google Developer Documentation Word List** provides explicit usage, spelling, and terminology rules for technical writing.

---

## 1. Dictionary & Search Hierarchy
1. **Google Word List:** Check the official [Google Developer Word List](https://developers.google.com/style/word-list).
2. **Merriam-Webster Default:** If a term is not on the list, use [Merriam-Webster.com](https://www.merriam-webster.com/). Always use the **first listed spelling variant** (e.g., *canceled*, NOT *cancelled*; *indexes*, NOT *indices*).
3. **Authoritative Tech Docs:** For specific protocol or library terms, follow the official primary documentation.

---

## 2. Usage Classifications

- ⚠️ **Use with Caution (Avoid):** Term is ambiguous, obscure, or jargon. Use alternatives or define on first mention.
- 🚫 **Don't Use:** Prohibited due to ambiguity, non-inclusive history, or redundancy. Write around or replace.
- 📱 **Android / ☁️ Google Cloud / 💼 Workspace:** Context-specific term rules.

---

## 3. High-Frequency Terms & Corrections

| Anti-Pattern / Term to Avoid | Preferred Alternative (Google Style) | Rule & Rationale |
| :--- | :--- | :--- |
| **`about` vs `on`** | *For more information **about** X, see...* | Use *about* for document cross-references (not *on*). |
| **`above`** | *earlier*, *preceding*, *later* | Don't use *above* for document positions (*preceding*) or version numbers (*version 2.0 and later*). |
| **`access` (verb)** | *see*, *view*, *edit*, *use*, *find* | Prefer direct, user-friendly action verbs. |
| **`account name`** | *username* | Use *username*. |
| **`agnostic`** | *platform-independent*, *vendor-neutral* | Be technically exact rather than figurative. |
| **`aka`** | *also known as*, or use parentheses `(X)` | Write out or rephrase. |
| **`allows you to`** | *lets you*, *enables* | Direct and concise phrasing. |
| **`allowlist` (verb)** | *add to the allowlist*, *grant access* | *Allowlist* is OK as a noun; avoid using as a verb (*allowlisting*). |
| **`abort`** | *stop*, *cancel*, *exit*, *end* | Avoid in general prose except for POSIX/Linux process signals. |
| **`admin`** | *administrator* | Write out *administrator* (OK to use *admin* in Android docs or direct UI label quotes). |
| **`action bar`** | *app bar* | `[Android]` Use *app bar* in Android documentation. |
| **`ad-tech` / `adtech`** | *advertising technology (ad tech)* | Write out on first mention, two words. |
| **`ampersand (&)`** | *and* | Don't use `&` in text/headings unless quoting UI labels or code. |
| **`canceled`** | *canceled* | First entry in Merriam-Webster (single 'l'). |
