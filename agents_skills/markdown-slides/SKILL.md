---
name: markdown-slides
description: Create presentation slides in Markdown format (Deckset/Marp compatible). Use when user requests to create slides, presentations, or convert documents to slide format. Handles image positioning, speaker notes, and proper formatting.
---

# Markdown Slides Skill
Convert content to presentation slides in Markdown format compatible with Deckset and Marp presentation tools.

## When to Use This Skill
Activate this skill when the user:
- Asks to create slides or a presentation
- Requests to convert a document to slide format
- Mentions Deckset or Marp
- Wants to generate speaker notes
- Needs to format images for presentations

## Input Requirements
- **Source content**: Markdown file, outline, or structured content
- **Images**: Files in _files_/ directory or paths to be resolved
- **Target platform**: Deckset (default) or Marp
- **Options**:
    - Speaker notes (enabled by default)
    - Slide numbering (optional frontmatter)
    - Emoji enhancement (enabled by default)

## Output Specifications
- **File location**: Same folder as source
- **File naming**: Original name with `- slides` suffix
- **Example**: `document.md` → `document - slides.md`
- **Format**: Deckset-compatible markdown
- **Structure**: Proper slide dividers, image tags, speaker notes
- **Enhancement**: Emojis added for visual appeal

## Main Process

### Step 1: Slide Structure Setup
**Objective**: Create logical slide divisions with proper hierarchy

**Actions**:
1. Read and analyze source content structure
2. Insert slide dividers (`---`) at logical breaks:
    - Between major sections
    - Between distinct topics
    - After section intro slides
    - Before/after major diagrams
3. Maintain content hierarchy:
    - H1 (`#`) for section titles
    - H2 (`##`) for main slide titles
    - H3 (`###`) for sub-topics
4. Preserve original organization and flow
5. Add optional frontmatter: `slidenumbers: true`

**Example**:
```markdown
slidenumbers: true
# 1. Section Title 🎯

![](section-background.png)

^ Introduction to this section.

---

## Main Topic 📊

Content here...

---

### Detailed Subtopic

More details...
```

### Step 2: Image Format Conversion
**Objective**: Convert images to Deckset format with proper positioning

**Critical Requirements**: 
⚠️ MUST resolve relative paths per-image basis 
⚠️ MUST URL-encode spaces and escape special characters 
⚠️ MUST verify image files exist

**Image Position Formats**:
| Format | Usage | Example |
| :--- | :--- | :--- |
| `![]()` | Section intro backgrounds | `![](background.png)` |
| `![inline]()` | Diagrams within text flow | `![inline](diagram.svg)` |
| `![right fit]()` | **PRIMARY**: Content slides | `![right fit](chart.png)` |
| `![right 80%]()` | Specific sizing needed | `![right 80%](image.png)` |
| `![inline fill]()` | Full-width inline | `![inline fill](wide.png)` |

**Actions**:
1. Identify all image references in source
2. For each image:
    a. Determine appropriate position format
    b. Resolve relative path from slide file location
    c. URL-encode spaces: `" "` → `"%20"`
    d. Escape parentheses: `"("` → `"%28"`, `")"` → `"%29"`
    e. Verify file exists at resolved path
    f. Use original images when available
    g. Copy missing images to `_files/` directory
3. Apply positioning based on context:
    - Section intros: Use `![]()` for full background
    - Diagrams in text: Use `![inline]()`
    - **Default for content slides**: Use `![right fit]()` ⭐
    - Custom sizing: Use `![right XX%]()` when needed
    - Full-width inline: Use `![inline fill]()` for wide images

### Step 3: Speaker Notes Conversion
**Objective**: Convert appropriate content to speaker notes

**Format**: Lines starting with `^ ` (caret + space)
**Placement**: At the end of each slide

**Convert to speaker notes**:
✅ Multi-sentence paragraphs
✅ Explanatory text
✅ Additional context
✅ Talking points

**DO NOT convert**:
❌ Single-sentence paragraphs
❌ Lists (bullet or numbered)
❌ Block quotes
❌ Sentences ending with colon (:)
❌ Headers (H1, H2, H3)
❌ Table content

**For Marp platform**: Use HTML comments instead `<!-- This is a speaker note for Marp -->`

### Step 4: Content Enhancement
**Objective**: Polish the presentation for maximum impact

**Actions**:
1. **Add emojis** to section and slide titles:
    - Use relevant emojis that enhance meaning
    - Don't overuse - keep it professional
    - Examples: 🎯📊🤖💡🚀📚🔧⚡
2. **Clean up comments**:
    - Remove markdown comments not meant for slides
    - Remove TODO items
    - Remove internal notes
3. **Ensure clean format**:
    - Consistent spacing
    - Proper header hierarchy
    - Clear slide breaks
4. **Add frontmatter** (if requested): `slidenumbers: true`
5. **Final review**:
    - Each slide has clear focus
    - Images positioned correctly
    - Speaker notes placed at end
    - No orphaned content

## Critical Guidelines

### Image Handling
⚠️ **CRITICAL RULES**:
1. **NEVER invent images** - Only reference images that exist in the source document or `_files/` folder.
2. Use original images from source when available
3. Resolve paths per-image - don't assume same directory
4. URL-encode spaces and escape special characters
5. **Verify existence before referencing** - run `ls` or `glob` to confirm file exists

### Speaker Notes Rules
**When to convert to speaker notes**:
- Multi-sentence explanatory paragraphs
- Contextual information not needed on slide
- Talking points for the speaker

**When NOT to convert**:
- Single-sentence paragraphs
- Bullet or numbered lists
- Block quotes
- Headers or table content

## Quality Checklist
- [ ] No invented images
- [ ] All images have valid, URL-encoded paths
- [ ] Image files exist at specified locations
- [ ] Speaker notes use `^ ` prefix
- [ ] Slide dividers (`---`) at logical breaks
- [ ] Consistent header hierarchy
- [ ] Emojis added appropriately
- [ ] File saved with `- slides` suffix
