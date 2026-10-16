# Skills para subir a claude.ai / app de Claude

Preparadas el 2026-10-01. La app de Claude y claude.ai solo ven las skills subidas a la cuenta;
no leen `~\.agents\skills` ni la biblioteca local.

Subida: claude.ai → Ajustes → Capacidades → Skills → subir el `.zip` (uno por skill).

| Zip | Qué hace en la cuenta |
|---|---|
| `no-ai-slop.zip` | Nueva: auditoría anti-slop (etapa 2 del pipeline). |
| `remove-ai-marks.zip` | **Sustituye** a la `remove-ai-marks` actual, que solo tiene `SKILL.md`; esta incluye los 6 ficheros de `references/`. Es la misma skill que la carpeta local `watermarks-remover`. Borra la antigua antes de subirla si la app no deja reemplazarla. |
| `glyph.zip` | Nueva: SMILES a SVG/PNG y tipografía química. El script necesita RDKit (`pip install rdkit` en el entorno de ejecución). |
| `ugr-courseware.zip` | Nueva: materiales docentes UGR. |
| `humanizer-juanjo.zip` / `humanizer-juanjo-es.zip` | **Sustituyen** a las dos humanizer de la cuenta (2026-10-16): añaden los ocho registros de voz (ceo, alumnos, manuscrito, diapositivas, propuesta, informe, divulgacion, recomendacion) con la guía `references/registros.md` dentro de la skill. En la app no hay Jev: la skill deduce el registro del destinatario y del formato, o usa el que le indiques ("humaniza esto como manuscrito"). Se regeneran con `py -3.13 empaquetar_humanizers.py` cada vez que cambien las humanizer o la guía; el mismo script actualiza `gemini_gem/conocimiento/`. |
| `agent-graph.zip` | **Sustituye** a la `agent-graph` subida el 2026-10-09: misma skill con el hook `scope-guard.py` en Python (en lugar de bash) y activación condicionada a `graph.md` / `AGENT_GRAPH_SCOPE` / `AGENT_GRAPH_ENFORCE=1`. En la app el hook no se ejecuta; la sustitución es solo por coherencia con `agents_skills/agent-graph`. |

`jev-system-one` no se incluye: necesita `py -3.13` con `typesafe-sdk`, la clave `TYPESAFE_API_KEY`
de `~\.env` y acceso a la API de TypeSafe, que solo existen en tus equipos. En la app el pipeline
funciona sin las etapas 0 y 4; para un documento certificado, usa Claude Code o Antigravity.
