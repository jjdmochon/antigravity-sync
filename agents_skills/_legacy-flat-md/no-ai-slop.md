# no-ai-slop

**Trigger**: Use when the user asks to detect, remove, or score AI writing patterns in any text. Also use automatically as Step B of the document production pipeline before any `humanizer-juanjo` pass.

---

## What This Skill Does

Detects and eliminates the stylistic fingerprints that mark text as AI-generated, without rewriting facts, claims, or technical content. Operates as a surgical cleaner, not a full rewrite.

**Two modes:**
- **Detect mode**: Score the text and report which patterns were found (no rewriting)
- **Clean mode**: Remove patterns in place (default)

---

## The AI Slop Taxonomy (remove on sight)

### Category 1 — Hollow Openers
These add zero information. Delete, do not replace:
```
"It's worth noting that..."
"It's important to understand that..."
"It's crucial to recognize..."
"One key thing to consider is..."
"Before we dive in..."
"Let's explore..."
"In today's world..." / "In today's fast-paced..."
"As we navigate..."
"This is a complex topic..."
```

### Category 2 — Hollow Closers
Delete entirely or rewrite the paragraph's actual conclusion:
```
"In conclusion..." / "In summary..." / "To summarize..."
"Overall, it can be said that..."
"It is clear that..." / "Clearly..."
"Ultimately..."
"As we can see..."
"I hope this helps!"
```

### Category 3 — Rule-of-Three Cadence
AI loves exactly three parallel items for rhythm. If the items are genuine, keep them. If they exist only for cadence:
```
"X, Y, and Z" where any of the three is redundant → collapse to two or eliminate one
"First... Second... Third... Finally..." with hollow content → restructure as prose
"not only X but also Y and moreover Z" → pick the strongest claim
```

### Category 4 — Superficial -ing Clauses
"By doing X, we can achieve Y" → "X achieves Y" or "Do X to achieve Y"
"By leveraging..." → "Using..." or just the verb directly
"By harnessing..." → (delete, replace with specific mechanism)
"By utilizing..." → "Using..."

### Category 5 — Corporate Padding Transitions
Used as filler between paragraphs. Replace with substantive connective tissue or delete:
```
"Moreover," "Furthermore," "Additionally," → use only if the logical connection isn't implicit
"However, it is important to note that..." → "However, [the actual point]"
"That being said," → delete
"With that in mind," → delete
"It goes without saying that..." → delete (if it goes without saying, don't say it)
"Needless to say," → delete
```

### Category 6 — Hollow Intensifiers
Delete or replace with quantification:
```
"very", "quite", "really", "truly", "highly", "extremely", "incredibly"
"significantly" without a p-value → replace with the actual number or delete
"dramatically" → replace with percentage or delete
"revolutionary", "groundbreaking", "game-changing" → replace with specific impact claim
```

### Category 7 — Faux Empathy and Acknowledgment Phrases
```
"That's a great question!"
"Certainly!" / "Absolutely!" / "Of course!"
"I understand your concern..."
"I'd be happy to help with that!"
"Great choice!"
```
Delete all. Respond to the actual content.

### Category 8 — Excessive Bold Emphasis
AI over-bolds. Keep bold only for:
- First use of a defined term
- A single key metric or finding per section
- Genuine warnings (CAUTION, NOTE)

Remove bold from: transitional phrases, every item in a list, adjectives used for enthusiasm.

### Category 9 — Unnecessary Bullet Fragmentation
Convert bullets to prose when:
- Each bullet is a complete sentence that flows logically to the next
- There are fewer than 4 items
- The items have an inherent order or causality

Keep bullets for: genuinely parallel, enumerable items (a checklist, a feature list, ingredients).

### Category 10 — Hedge Stacking
```
"may potentially suggest that it is possible that..."
"could perhaps indicate..."
"it seems that it might be..."
```
Pick one hedge or eliminate all of them. Never stack more than one.

---

## Detect Mode Output Format

When asked to score/detect only (not clean), report:
```
SLOP SCORE: X/10

Patterns detected:
- [Category name]: [count] instances → [brief example]
- ...

Recommendation: [Clean / Minor cleanup / Acceptable]
```

---

## Clean Mode Rules

1. Never change: facts, data, citations, proper nouns, code, formulas
2. Never introduce new content — only remove or tighten
3. If removing a phrase leaves a grammatical fragment, fix the sentence structure
4. If an entire paragraph is slop with no factual content, flag it for deletion rather than silently removing it
5. After cleaning, the text should be shorter, not longer
