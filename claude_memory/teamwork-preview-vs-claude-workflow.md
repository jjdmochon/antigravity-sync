---
name: teamwork-preview-vs-claude-workflow
description: "Resultados de comparar teamwork_preview (Antigravity) con Workflow de Claude en la revisión del manuscrito HyaloSpheres, y cuándo usar cada uno"
metadata:
  type: reference
---

Prueba realizada el 2026-10-16 sobre el manuscrito HyaloSpheres (texto convertido de .docx, sin figuras).

Qué es teamwork_preview: meta-orquestador de Antigravity (tool invoke_subagent, TypeName teamwork_preview). Se le da un contrato (requisitos R1.., Verification Resources, Acceptance Criteria con checkboxes, Working directory, integrity_mode development|demo|benchmark) y él elige la topología: Document Review, Proof Pipeline, Full Team (por defecto), Small Focused Team (frase "This is a single self-contained fix; keep it small and focused.") y Very Large Team ("Use a very large team of agents."). Estas frases son opt-in; no usarlas en comparaciones de revisión.

Resultados de la prueba:
- Claude Workflow (11 agentes): unos 6 min, 795k tokens de subagentes, 16 hallazgos mayores. Más fuerte en estadística, reporte animal (ARRIVE, ética), inconsistencias entre texto y figuras, dosis enzimática.
- Antigravity teamwork (47 carpetas de agente, `.agents/teamwork/`): unos 50 min, 12 mayores. Más fuerte en cálculo cuantitativo (balance de masas, límites geométricos, masa de Dox por bolita), purificación omitida, calibración Dorfman, DOI roto y referencia fantasma.
- Los dos coinciden en el núcleo (contradicción de grupos Tabla 1 vs Resultados, 420 nm vs <200 nm, plateau de eficacia, falta de PK).
- Antigravity es más duro ("bordering on reject") y mezcla conocimiento externo sin marcarlo.

**Why:** Juanjo quería decidir cuándo usar teamwork_preview frente a subagentes/Workflow de Claude y los agent teams experimentales (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1).

**How to apply:** Para revisión de manuscritos, empezar con el Workflow de Claude (rápido, barato) y usar teamwork_preview solo en manuscritos críticos o como segunda opinión cuantitativa; mejor aún, añadir al Workflow un agente de cálculo y verificación completa de referencias. Sustituir ficheros por su conversión a texto y avisar de que las figuras no se ven. El prompt de contrato (qué, no cómo; verificación objetiva; criterios booleanos) sirve para ambos. Archivos de la prueba: C:\Users\Juanjo\teamwork_projects\ (manuscript_review_test, claude_results, merged_review). Script del Workflow: C:\Users\Juanjo\teamwork_projects\claude_results\manuscript_review.js (se lanza con Workflow scriptPath y args {manuscript: ruta .md, outDir: carpeta de salida}). Ver también [[doc-gate-hook]].
