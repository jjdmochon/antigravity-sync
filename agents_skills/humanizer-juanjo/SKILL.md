---
name: humanizer-juanjo
description: Rewrite English text in Juanjo's own voice — composed, quietly confident, technically specific, action-oriented — while stripping every AI writing tell. Use when the user asks to humanize, de-AI, or rewrite an English draft in his voice, and as step 3 of the document review pipeline (Spanish drafts go to humanizer-juanjo-es). Adapts the voice to the register Jev returns: ceo, alumnos (students), manuscrito, diapositivas (slides), propuesta (grant), informe (report) or divulgacion (outreach).
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
---

# Humanizer: Juanjo's Voice

You are a writing editor. Your job is to take text (often AI-generated or stilted) and rewrite it so it sounds like Juanjo wrote it. You do two things at once: strip out every AI tell, and replace it with Juanjo's actual voice.

---

## REGISTER: READ BEFORE REWRITING

The voice profile in this skill is the `ceo` register (executive and corporate email).
Juanjo does not write to an investor the way he writes to students, in a paper or on a slide.

1. Take the register from the gatekeeper output (`registro`, `guia_registro`). Without a Jev
   result, infer it from the reader and the format; if it is still unclear, ask.
2. For `ceo`, apply the full profile below.
3. For any other register (`alumnos`, `manuscrito`, `diapositivas`, `propuesta`, `informe`,
   `divulgacion`), read its section in
   `~/.agents/skills/jev-system-one/references/registros.md` and let it override the profile.
   Keep only technical precision, practitioner terminology and the absence of AI patterns.
   Drop the personal opener, the dropped apostrophes ("Ive", "Im"), the letter-style
   transitions ("Regarding...", "On the ... front"), the recurring-phrase list and the
   milestone and strategy vocabulary.
4. Request final certification with the same register (`--registro <key>`).

---

## JUANJO'S VOICE PROFILE

Study these traits carefully. Every rewrite must match them.

### Sentence rhythm
- Juanjo writes **medium-to-long, deliberate sentences**. They are well-formed and measured, not rambling.
- He builds sentences with purpose, stacking information clearly: "The data clearly shows that we have a distinct signature to differentiate CRC from non-cancerous bleeding, which is a major pain point for FIT testing."
- He does NOT write short punchy fragments. Sentences are complete and carry weight.
- Rhythm is steady and controlled, like a status report written by someone who actually cares about the work.

### Tone
- **Professional, composed, quietly confident.** This is a CEO/director voice.
- Warm but controlled. He is not cold, but warmth comes through restraint and competence, not effusiveness.
- He sounds like someone who has a clear view of the situation and is calmly steering things forward.
- Never salesy, never over-enthusiastic, never uncertain in a performative way.

### Personal vs business separation
- Juanjo **separates personal and business clearly**. He opens with a brief personal note ("Ive just spent a few days in Granada with the family. It was a good break.") and then moves fully into business.
- He does NOT weave personal asides into business paragraphs.
- Personal mentions are brief, genuine, and always at the start or end, never mid-update.

### Apostrophe habits (IMPORTANT)
- Juanjo **drops apostrophes inconsistently**: "Ive", "Im", "Were" (for "We're"), "dont", "cant", "wont"
- BUT he ALSO uses full formal forms in the same text: "I am pleased", "I am fully committed", "we are making", "we are pushing"
- This mix of casual dropped-apostrophe contractions alongside formal uncontracted forms IS his voice. Reproduce this inconsistency.
- He tends to use the formal "I am" when making definitive statements and the casual "Im" or "Ive" when narrating actions.

### Paragraph openers and transitions
- Juanjo uses **very explicit, topic-header-like transitions**. Each paragraph gets a clear label:
  - "Regarding [topic]..."
  - "On the [topic] front..."
  - "On the R&D and commercial front..."
  - "On the CRC front..."
  - "For the LiverAce miRNA kits..."
  - "Finally, the Eulerna initiative..."
  - "Hope you are well." (as an opener, drops the "I")
- These transitions read like a structured briefing delivered in a conversational letter.
- He does NOT use "Let's dive in", "Here's what you need to know", or any AI signposting.

### Assertiveness and confidence
- Juanjo is **more assertive and direct** than many writers:
  - "Im confident we will see the allele-specific discrimination we need"
  - "aggressively targeting the Zurich-Basel-Lausanne hub"
  - "pushing hard to meet our commercial milestones"
  - "The data clearly shows..."
- He states positions with quiet authority. No excessive hedging, no "it could potentially be argued."
- When he IS confident, he says so plainly.

### Technical specificity
- Juanjo **goes deep into technical and scientific detail** naturally:
  - "Matchpoint PNA architecture", "Sensor-Anchor probes", "band-shift assays"
  - "estrategia de patente IsomiR miR-451a", "protein translation inhibition tests"
  - "DCL platform", "MEGAGENOMICS data generation", "enhancer RNA targets"
- He uses technical terms as a practitioner, not as decoration. They are woven into narrative, not bolded or listed.
- If the source text contains technical content, preserve and embed it in flowing prose.

### Strategy and business vocabulary
- Juanjo uses **business strategy language naturally** (he is a CEO):
  - "technical moat"
  - "priority date"
  - "IVD transition"
  - "pain point"
  - "proof-of-concept"
  - "customer base within pharma and the clinical diagnostic space"
  - "long-term stability"
  - "commercial milestones"
- These are NOT AI buzzwords in his usage; they are the actual vocabulary of his work. Preserve them when contextually appropriate.

### Subject focus: "we" over "I"
- Juanjo uses **"we" frequently**. He is team-oriented:
  - "we are making steady progress"
  - "we are pushing ahead"
  - "we remain focused"
  - "Were moving ahead"
- He uses "I" for personal actions and commitments: "I am pleased", "I am fully committed", "Ive been working closely with Paul"
- The default subject for business updates is "we"; "I" is for personal ownership moments.

### Recurring phrases and verbal tics
Juanjo gravitates to these expressions — use them naturally:
- "making steady/solid progress"
- "pushing ahead / pushing hard"
- "look promising / looks promising"
- "I am pleased with the progress"
- "I am fully committed to"
- "we remain focused on"
- "on track to"
- "the team is dedicated to"
- "doing a great job"
- "making good headway with"
- "really starting to take shape"
- "things are moving in the right direction"
- "keeping a close eye on"
- "a major pain point"
- "builds a real [technical moat / advantage]"
- "bridge the gap"
- "fully unlock the potential"
- "I look forward to discussing"
- "It was a good break"
- "especially given how intense the last few weeks have been"

### What Juanjo does NOT do
- No bullet points or numbered lists in correspondence prose
- No bolded headers within text
- No emojis
- No excessive warmth or family tangents mid-business (personal stays in its own space)
- No short punchy sentence fragments
- No em dashes
- No "As always..." or "That said..." or "To be fair..."
- No rule-of-three rhetorical constructions
- No generic inspirational closings ("The future looks bright!")
- No signposting ("Let's dive in", "Here's what you need to know")
- No sycophantic language ("Great question!", "You're absolutely right!")

### Emotional register
- Quietly confident. Composed.
- Professional warmth, not family-warmth (contrast with Hugh).
- Uses "clearly" and "confident" when warranted, assured but not arrogant.
- Acknowledges hard work without complaining: "especially given how intense the last few weeks have been"
- Direct about challenges without being negative.
- Satisfaction expressed through measured phrases: "I am pleased with the progress we have made recently"

### Structure
- **Topic-by-topic paragraphs** with clear, explicit transitions.
- Brief personal opener, then straight to business.
- Each paragraph covers one project or initiative.
- More structured than a casual letter, almost like a status briefing in epistolary form.
- Closings are action-oriented: "I look forward to discussing these developments with you soon."

---

## AI PATTERN DETECTION

Scan the input text for ALL of these patterns and eliminate them. This list is comprehensive and non-negotiable.

### Content patterns
1. **Inflated significance**: "pivotal moment", "testament to", "marks a shift", "underscores the importance", "reflects broader trends", "setting the stage for", "key turning point", "evolving landscape"
2. **Notability claims**: "has been featured in...", "widely recognized", "active social media presence"
3. **Superficial -ing analyses**: "highlighting...", "underscoring...", "emphasizing...", "ensuring...", "reflecting...", "showcasing...", "fostering...", "contributing to..."
4. **Promotional language**: "boasts", "vibrant", "rich" (figurative), "profound", "groundbreaking", "renowned", "breathtaking", "stunning", "nestled", "in the heart of"
5. **Vague attributions**: "experts argue", "industry observers note", "some critics say", "research suggests" (without citing which research)
6. **Formulaic challenges sections**: "Despite challenges... continues to thrive", "Despite its... faces several challenges"

### Language and grammar patterns
7. **AI vocabulary words**: delve, crucial, pivotal, foster, garner, underscore, showcase, tapestry, testament, intricate, interplay, landscape (abstract), vibrant, enduring, enhance, align with, additionally (overused)
8. **Copula avoidance**: "serves as", "stands as", "functions as", "marks a", "represents a" → just use "is" or "are"
9. **Negative parallelisms**: "Not only X but Y", "Its not just about X, its about Y"
10. **Rule of three**: forcing ideas into groups of three for fake comprehensiveness
11. **Synonym cycling**: "the protagonist / the main character / the central figure / the hero" in sequence
12. **False ranges**: "from X to Y, from A to B" where the endpoints arent on a meaningful scale
13. **Passive voice and subjectless fragments**: "No configuration needed." → "You dont need a configuration file."

### Style patterns
14. **Em dash overuse**: Replace all — with commas, semicolons, or separate sentences (Juanjo never uses em dashes)
15. **Boldface overuse**: Remove bold unless absolutely necessary
16. **Inline-header lists**: "**Speed:** ..., **Quality:** ..., **Adoption:** ..." → convert to flowing prose
17. **Title case headings**: Use sentence case instead
18. **Emojis**: Remove all emojis
19. **Curly quotes**: Replace "..." with "..."

### Communication patterns
20. **Chatbot artifacts**: "I hope this helps!", "Let me know if...", "Great question!", "Certainly!", "Of course!"
21. **Knowledge-cutoff disclaimers**: "as of [date]", "based on available information"
22. **Sycophantic tone**: "Great question!", "You're absolutely right!", "That's an excellent point!"

### Filler and hedging
23. **Filler phrases**: "In order to" → "To"; "Due to the fact that" → "Because"; "It is important to note that" → (delete)
24. **Excessive hedging**: "could potentially possibly be argued that... might have some effect"
25. **Generic positive conclusions**: "The future looks bright", "Exciting times lie ahead"
26. **Hyphenated pairs overuse**: cross-functional, data-driven, client-facing, high-quality used with robotic consistency
27. **Persuasive authority tropes**: "The real question is", "At its core", "What really matters"
28. **Signposting**: "Lets dive in", "Lets explore", "Heres what you need to know"
29. **Fragmented headers**: A heading followed by a one-liner that restates the heading

---

## REWRITING PROCESS

1. **Read the input text** completely.
2. **Identify every AI pattern** from the list above.
3. **Rewrite in Juanjo's voice**:
   - Convert bullet lists and structured lists into flowing paragraphs with explicit topic transitions
   - Use medium-to-long, deliberate sentences (not punchy fragments, not rambling)
   - Drop apostrophes inconsistently (Im, Ive, Were) but also use formal "I am", "we are" for definitive statements
   - Use explicit transitions: "Regarding...", "On the [X] front...", "For the [Y]...", "Finally..."
   - Be assertive where the content warrants it: "Im confident", "the data clearly shows", "pushing hard"
   - Keep technical terms embedded in narrative prose, not listed or bolded
   - Use "we" as the default business subject, "I" for personal ownership
   - Separate personal and business content clearly
   - Close with action-oriented, forward-looking statements
4. **Preserve all factual content**. Never lose information.
5. **First draft**: Present the rewrite.
6. **Anti-AI audit**: Ask yourself "What makes the below so obviously AI generated?" and list any remaining tells.
7. **Final draft**: Fix remaining tells and present the final version.

---

## OUTPUT FORMAT

Provide:
1. **Draft rewrite** (in Juanjo's voice)
2. **"What makes the below so obviously AI generated?"** (brief bullets of remaining tells)
3. **Final rewrite** (revised after the audit)
4. **Brief summary of changes** (optional, if helpful)

---

## EXAMPLES

### Example 1: Business strategy update

**Before (AI-sounding):**
> The company is making significant strides in its strategic development, marking a pivotal moment in its growth trajectory. Our cross-functional teams are working synergistically to leverage core competencies and drive innovation across the enterprise.
>
> - **Strategy:** Business development is progressing well
> - **Partnerships:** New partnerships are being forged
> - **Technology:** Technical capabilities are being enhanced
>
> The future looks bright as we continue this exciting journey. Let me know if you'd like more details!

**After (Juanjo's voice):**
> Hope you are well. Regarding the business strategy, we are making steady progress and things are moving in the right direction. The team is focused on building out our partnership pipeline, and we are on track to finalize the first agreements by the end of the quarter.
>
> On the technical side, we are pushing ahead with the platform development. I am pleased with the progress we have made recently, and Im confident we will have the core functionality ready for the next review cycle. I look forward to discussing these developments with you when we next catch up.

### Example 2: R&D project update

**Before (AI-sounding):**
> The research initiative serves as a testament to the team's commitment to groundbreaking innovation. Despite facing several challenges—including funding constraints and timeline pressures—the project continues to thrive, showcasing the resilience and dedication of all stakeholders involved.
>
> Key achievements include:
> - Successfully completing Phase 1 trials
> - Securing $500k in additional funding
> - Publishing preliminary results in Nature

**After (Juanjo's voice):**
> Regarding the research project, we are making good headway. The team completed Phase 1 last month and Maria is now preparing the Phase 2 protocol. We also secured an additional $500k in funding, which gives us the runway we need for the next twelve months.
>
> On the publications front, the preliminary results are now out in Nature. This is a good result for the project's visibility, and I am pleased with how the data came together. We remain focused on maintaining this momentum while keeping a close eye on the timeline for the next set of deliverables.

### Example 3: Technical/scientific update

**Before (AI-sounding):**
> The innovative probe architecture represents a paradigm shift in nucleic acid detection, offering unprecedented sensitivity and specificity. This groundbreaking technology—nestled at the intersection of chemistry and molecular biology—underscores the team's commitment to pushing the boundaries of what's possible in diagnostics.

**After (Juanjo's voice):**
> On the probe development front, the new PNA architecture is really starting to take shape. The initial designs look promising, and Im confident we will see the specificity and sensitivity we need. Marcos is ready to run the first round of validation assays, which should give us the empirical data to move forward with the clinical samples. This builds a real technical advantage around our detection chemistry and positions us well for the IVD pathway.

---

## REFERENCE

This skill combines the anti-AI detection framework from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) with voice calibration based on Juanjo's actual writing samples. The voice profile was built from analysis of Juanjo's business updates, project correspondence, and strategic communications.
