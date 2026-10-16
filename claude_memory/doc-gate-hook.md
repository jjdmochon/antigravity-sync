---
name: doc-gate-hook
description: ~/.claude/hooks/doc_gate.py enforces CLAUDE.md §3 (zero raw LaTeX + Jev gate) on .md/.html/.txt deliverables via a PostToolUse Write|Edit hook
metadata:
  type: project
---

`~/.claude/hooks/doc_gate.py` has two modes: `latex` (sync, deterministic, blocks with a reason on raw `$…$`, `\(…\)`, `\text{…}`) and `jev` (async rewake; runs `jev_doc_gatekeeper.py` and wakes Claude only on LaTeX, invisible marks/metadata or slop). It skips ~/.claude, ~/.agents, node_modules, temp dirs and README/CLAUDE/SKILL/MEMORY files. Created 2026-10-05.

**Update 2026-10-16:** the voice stage now blocks again (commit b185a39) and is judged per register; the gatekeeper reads the register from a `<!-- registro: X -->` marker, a `.jev-registro` file in the folder, or Jev's Choice. See [[jev-gatekeeper-pipeline-documental]].

**Why (original):** the voice stage was deliberately non-blocking — on 2026-10-05 the voice Noul scored 0.81 "needs rewrite" on a sentence already written in Juanjo's voice, so blocking on it would nag on every save. Same fragility as [[jev-gatekeeper-pipeline-documental]].

**Superseded by the register-aware update above (this machine's local fix was dropped on merge; the manuscrito register should cover technical reports).** Earlier 2026-10-16 note: the code did NOT match that intent: `mode_jev` still appended "voz p=..." to `fallos` and exited 2, so a peer-review report was rejected twice (p=0.85, then 0.73) because the voice classifier is calibrated for correspondence, not technical reports. The voice rejection was removed from `mode_jev` (p_voz is still saved in `~/.claude/state/jev-last.json`); backup at `doc_gate.py.bak-20261015-195359`. Do not rewrite technical reports to force Juanjo's voice; apply humanizer-juanjo only to correspondence or on request.

**How to apply:** if the hook misfires on a file type or path, adjust EXTS/SKIP_DIRS in the script rather than disabling it. Wiring lives in ~/.claude/settings.json under hooks.PostToolUse.
