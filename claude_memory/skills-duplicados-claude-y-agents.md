---
name: skills-duplicados-claude-y-agents
description: .agents\skills es la copia canonica; .claude\skills y .gemini\config\skills son junctions a ella desde el 2026-09-21
metadata: 
  node_type: memory
  type: project
  originSessionId: d2c2721d-e51d-4088-adc4-3f2b2d193ed5
  modified: 2026-10-05T13:40:40.972Z
---

`C:\Users\Juanjo\.agents\skills` es la **única copia canónica** de las skills globales.
`.claude\skills` y `.gemini\config\skills` son *junctions* a ella desde el 2026-09-21.
Editar en cualquiera de las tres rutas es equivalente: escriben en el mismo sitio.

Antes de esa fecha las tres eran directorios reales e independientes, y llevaban meses
divergiendo en silencio: `.claude` era una instantánea del 14-ago, `.agents` estaba al día.
Consecuencia concreta: `watermarks-remover` y `no-ai-slop`, que CLAUDE.md sección 3 declara
obligatorias, no eran invocables desde Claude Code porque solo existían en `.agents`. Y la
ruta de `.claude` seguía sirviendo la versión de `run_eulerna_enhancer_scan.py` que imprime
hotspots inventados (ver [[eulerna-alphagenome-mcp-returns-fake-data]]).

**Why:** el diseño con junctions ya estaba previsto en `sync-push.ps1`, pero la comprobación
era `if (-not (Test-Path $dir)) { mklink }`, que nunca repara un directorio real ya existente.
El junction no llegaba a crearse jamás y nadie se enteraba.

**How to apply:** no recrear nunca `.claude\skills` ni `.gemini\config\skills` como carpetas
reales. Si una herramienta lo hace, los `sync-push.ps1` / `sync-pull.ps1` de
`K:\Mi unidad\Antigravity-Sync` ya la apartan como `.bak-<fecha>` y rehacen el junction.
Comprobar el estado con `Get-Item <ruta> -Force | Select LinkType,Target`.

Las copias apartadas `~\.claude\skills.bak-20260921` (500 MB) y
`~\.gemini\config\skills.bak-20260921` ya no existen (comprobado el 2026-10-05). Los `.md` sueltos que solo vivían en `.claude` se rescataron en
`.agents\skills\_legacy-flat-md\`.

Relacionado: [[jev-gatekeeper-pipeline-documental]]
