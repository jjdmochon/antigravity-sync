---
name: doc-gate-hook
description: ~/.claude/hooks/doc_gate.py enforces CLAUDE.md §3 (zero raw LaTeX + Jev gate) on .md/.html/.txt deliverables via a PostToolUse Write|Edit hook
metadata:
  type: project
---

`~/.claude/hooks/doc_gate.py` has two modes: `latex` (sync, deterministic, blocks with a reason on raw `$…$`, `\(…\)`, `\text{…}`) and `jev` (async rewake; runs `jev_doc_gatekeeper.py` and wakes Claude only on LaTeX, invisible marks/metadata or slop). It skips ~/.claude, ~/.agents, node_modules, temp dirs and README/CLAUDE/SKILL/MEMORY files. Created 2026-10-05.

**Update 2026-10-16:** the voice stage now blocks again (commit b185a39) and is judged per register; the gatekeeper reads the register from a `<!-- registro: X -->` marker, a `.jev-registro` file in the folder, or Jev's Choice. See [[jev-gatekeeper-pipeline-documental]].

**Why (original):** the voice stage was deliberately non-blocking — on 2026-10-05 the voice Noul scored 0.81 "needs rewrite" on a sentence already written in Juanjo's voice, so blocking on it would nag on every save. Same fragility as [[jev-gatekeeper-pipeline-documental]].

**How to apply:** if the hook misfires on a file type or path, adjust EXTS/SKIP_DIRS in the script rather than disabling it. Wiring lives in ~/.claude/settings.json under hooks.PostToolUse.
