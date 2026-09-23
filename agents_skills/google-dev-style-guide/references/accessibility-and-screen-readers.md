# Google Developer Style Guide: Accessibility Guidelines

This reference provides technical documentation accessibility standards based on the **Google Developer Accessibility Guide**.

---

## 1. Directional & Spatial Language

Do **NOT** use directional terms to orient readers or point to document positions (e.g., *above*, *below*, *top-right*, *left-hand column*, *bottom of the page*).

- **Why:** Screen readers present content sequentially in an audio stream (visual position is irrelevant), and localization into Right-To-Left (RTL) languages flips visual layouts.
- **Rules & Replacements:**
  - Instead of *see above*, use *see preceding section* or *see earlier*.
  - Instead of *the form below*, use *the following form*.
  - Instead of *in the left sidebar*, use *in the navigation menu*.

---

## 2. Images, Diagrams, and Alt Text

- **Mandatory Alt Text:** Provide descriptive `alt` text for every image. Alt text must convey the intent and core information of the visual.
  - *Example:* `![Architecture diagram showing client request flow to the backend API](path/to/img.png)`
- **Decorative Images:** Use empty alt text (`alt=""`) ONLY for purely decorative dividers or background flourishes.
- **No Text in Images:** Never embed critical code samples, terminal logs, or procedural instructions inside images. Use real text and fenced code blocks.
- **Icons & UI Symbols:** Use `aria-label` or adjacent text labels for icons without visible text.

---

## 3. Accessible Data Tables

- **Preceding Intro:** Always introduce tables in the text preceding them.
- **Simple Grid Layout:** Do **NOT** merge cells or use `colspan` / `rowspan`. Screen readers struggle with complex merged cells.
- **Header Markup:** Use `<th>` tags for first-row column headers and include `scope="col"` or `scope="row"`.
- **No Layout Tables:** Never use tables for visual page layout; use tables strictly for tabular data.

---

## 4. Color, Contrast, and Visual Indicators

- **Secondary Indicators:** Never rely solely on color, shape, or position to communicate meaning or state. Pair color cues with explicit text labels or icons.
  - *Incorrect:* Green status indicates operational services; red status indicates outages.
  - *Correct:* Green checkmark icon (**Operational**) indicates active services; red warning icon (**Outage**) indicates an outage.
- **Contrast Ratios:** Ensure custom text styling meets WCAG AA contrast standards (minimum 4.5:1 for standard body text).
