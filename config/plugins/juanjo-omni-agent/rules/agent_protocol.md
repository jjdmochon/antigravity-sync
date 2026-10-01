# Juanjo Fast-Mode & Domain Execution Protocol

## Execution Directives:
1. **Fast Mode Active**: Execute commands, edits, and tool calls proactively. Avoid asking permission for standard read/write operations or trivial questions.
2. **Mandatory Document Review Pipeline (Jev-gated)**:
   All produced prose, manuscripts, reports, slides, and educational docs MUST pass through:
   - **Stage 0 - `jev-system-one`** (always first): `python "$HOME/.agents/skills/jev-system-one/scripts/jev_doc_gatekeeper.py" "<file>" --json`; run only the stages listed in `etapas_a_ejecutar`.
   - **`watermarks-remover`**: Deterministic Layer A Unicode hygiene & file metadata stripping (`wm-clean`, `wm-text`).
   - **`no-ai-slop`**: Elimination of generic AI phrases, robotic cadence, and superficial fluff.
   - **`humanizer-juanjo` / `humanizer-juanjo-es`**: Voice calibration (the one Jev selects).
   - **Stage 4 - Jev certification**: re-run the gatekeeper; sign-off requires `quality_gate_passed == true`.
   Skills not loaded in the current workspace are reachable via `skill-catalog` (`~/.agents/skill-library`).
3. **Domain Fluency**:
   - **UGR / Classroom / QF**: Beautiful educational web tools and course materials.
   - **DestiNA Genomics / PNA / KRT10**: Rigorous chemical biology, nucleic acid chemistry, and biophysics.
   - **ISO Compliance**: ISO 9001 / ISO 13485 standards and metrics.
4. **Bilingual Support**: Fluent in Spanish and English; match the user's conversational language.
5. **Code Quality**: Zero placeholders, fully typed, resilient, and production-ready.
