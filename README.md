# 🔄 Antigravity Sync Hub (Google Drive)

Este directorio mantiene sincronizados todos tus agentes, reglas, configuraciones maestras y los 236 skills de **Google Antigravity** entre tus dos ordenadores.

---

## 💻 1. Configuración Inicial en el Equipo B (Segundo PC)

1. Asegúrate de tener **Google Drive para escritorio** activo en tu segundo equipo.
2. Abre **PowerShell** en tu segundo equipo.
3. Ejecuta el script de configuración automática:
   ```powershell
   powershell -ExecutionPolicy Bypass -File "K:\Mi unidad\Antigravity-Sync\setup-secondary-pc.ps1"
   ```
   *(Si en tu segundo PC la unidad de Google Drive es `G:` o `D:`, adapta la letra de la unidad)*.

**¿Qué hace este script en el segundo PC?**
- Instala `GEMINI.md`, `GLOBAL_AGENTS_AND_TOOLS.md` y `SUBAGENTS_TEMPLATES.md`.
- Sincroniza la carpeta global `config` con los **236 skills y plugins**.
- Clona y configura `watermarks-remover`.
- Habilita los comandos globales (`wm-clean`, `wm-inspect`, `wm-score`, `sync-push`, `sync-pull`).

---

## ⚡ 2. Comandos de Sincronización Rápida (Desde Cualquier Terminal)

Puedes ejecutar estos comandos desde la terminal de cualquier carpeta o workspace:

| Comando | Acción |
| :--- | :--- |
| **`sync-push`** | Sube tus skills/reglas creados o modificados localmente hacia Google Drive. |
| **`sync-pull`** | Descarga e incorpora de inmediato los cambios realizados desde el otro equipo. |

---

## 🌐 3. Alcance Global

Las configuraciones sincronizadas residen en el **Global Customizations Root** (`C:\Users\<user>\.gemini\config`), lo que significa que:
- **Se aplican a cualquier carpeta, disco o workspace** que abras en Antigravity.
- `juanjo-copilot` y los skills especializados están siempre activos en ambos equipos.

---

## 📁 4. Estructura de las skills (desde 2026-10-01: núcleo + biblioteca)

Cada skill tiene **una sola copia real** en cada equipo, en uno de dos niveles:

```
~\.agents\skills          <- NÚCLEO: se carga siempre (~44 skills, ~18 KB de descripciones)
~\.claude\skills          -> junction al núcleo
~\.gemini\config\skills   -> junction al núcleo
~\.agents\skill-library   <- BIBLIOTECA: ~227 skills que no se cargan solas
~\.agents\skill-archive   <- retiradas (ClaudeScientificSkills, _legacy-flat-md, rescates .bak)
```

| En Drive | Local | Qué es |
| :--- | :--- | :--- |
| `agents_skills\` | `~\.agents\skills` | Núcleo: juanjo-copilot, jev-system-one, humanizers, no-ai-slop, watermarks-remover, document-pipeline, `tooluniverse` (router)… |
| `skill_library\` | `~\.agents\skill-library` | ToolUniverse, AlphaGenome, Albatross, BioNeMo/NIM, bases de datos, literatura, Python científico, GCP/BigQuery, ISO, diseño, UGR |

**Por qué.** Con las 185 skills cargadas, Antigravity superaba el *Customization token budget*
y truncaba skills al azar. Con solo 42 globales y copias por workspace (30/09), las carpetas
que no eran esos workspaces se quedaban sin skills. Ahora:

- La skill **`skill-catalog`** (núcleo) indexa la biblioteca. En **cualquier carpeta**, el agente
  lee el índice y abre `~\.agents\skill-library\<nombre>\SKILL.md`. La generan `sync-pull` y
  `sync-push` con `build-skill-catalog.ps1`; no viaja por Drive porque lleva rutas locales.
- **Mover una skill entre niveles** = mover su carpeta entre `skills` y `skill-library` y hacer `sync-push`.
- **Packs por workspace** (opcional, solo en carpetas locales, no en Drive):
  `skill-pack.ps1 enable <pack>` crea junctions a la biblioteca en `<ws>\.agents\skills` y
  `<ws>\.claude\skills`. Packs en `skill-packs.json`: `biomed`, `tooluniverse`, `tooluniverse-dev`,
  `genomics`, `gcp-data`, `ugr`, `bionemo`, `sci-python`, `design`, `business`.
  `skill-pack.ps1 list | status | disable <pack>`.
- **Workspaces de Drive** (`Developer`, `Developer UGR`): desde 2026-10-01 no llevan copias de
  skills en `.agents\skills` ni `.claude\skills`. Sus 84 skills propias (BioNeMo/NIM, Complexa,
  KERMT, K-Dense, diseño…) pasaron a la biblioteca; las 143 copias antiguas se borraron
  (Drive las conserva 30 días en su papelera).

**Salvaguardas de los scripts.**
- `sync-pull` no borra skills: lo que deja de ser núcleo se mueve a la biblioteca; la biblioteca
  se copia sin purga y con `/XO` (no pisa ficheros locales más recientes).
- `sync-push` se niega a subir si el núcleo local tiene más de 70 skills (equipo sin migrar) o si
  Drive tiene skills de biblioteca que este equipo no tiene. En ambos casos: `sync-pull` primero.

Los SKILL.md duplicados dentro de `config\plugins\*` están desactivados (`SKILL.md.disabled`)
porque Antigravity los cargaba además de los del núcleo. El MCP `claude-skills` de
`~\.gemini\antigravity-ide\mcp_config.json` está en `"disabled": true` por el mismo motivo.

Antes de esa fecha las tres eran carpetas reales independientes y llevaban meses
divergiendo en silencio, porque los scripts solo creaban el junction si la ruta no
existía y nunca reparaban una carpeta real ya presente. Ahora `sync-push` y `sync-pull`
detectan ese caso, apartan la carpeta como `.bak-<fecha>` y rehacen el enlace.

`claude_skills\` es del esquema antiguo y ya no se actualiza. Puede moverse a `archive\`.

**No se sincronizan** (se excluyen en ambos scripts, y no sirven en otro equipo porque
llevan rutas absolutas del equipo origen): `.venv`, `.git`, `__pycache__`, `node_modules`,
`*.pyc`, `desktop.ini`.

### Después de un `sync-pull` en un equipo nuevo

Las claves de API no viajan por Drive. Hay que crear `~\.env` en el equipo destino con,
al menos, `TYPESAFE_API_KEY` (motor Jev) y `ALPHAGENOME_API_KEY`.

---

## 🤖 5. Claude Code (desde 2026-09-23)

Claude Code (`claude`, instalado en `~\.local\bin\claude.exe`) usa las mismas piezas:

| Pieza | Ruta en Claude | Origen |
| :--- | :--- | :--- |
| Skills de núcleo (~44) | `~\.claude\skills` → junction a `~\.agents\skills` | `agents_skills\` |
| Biblioteca (~227) | `~\.agents\skill-library`, vía `skill-catalog` | `skill_library\` |
| Subagentes | `~\.claude\agents\*.md` | `claude_agents\` |
| Instrucciones globales | `~\.claude\CLAUDE.md` | `CLAUDE.md` |

Skills incorporadas desde los plugins de Antigravity: `gemini-api-dev`, `gemini-interactions-api`,
`gemini-live-api-dev`, `gemini-omni-flash-api`, `android-cli`, `google-antigravity-sdk`,
`developing-with-bigquery`, `gcloud-auth-verification`.

MCP equivalentes a los de Antigravity (se registran una vez por equipo, ámbito usuario):

```powershell
claude mcp add --scope user --transport http gemini-api-docs https://gemini-api-docs-mcp.dev
claude mcp add --scope user chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

El MCP `tooluniverse` ya no se registra (2026-10-01): expone cientos de herramientas y su función
la cubren la skill router `tooluniverse` y las sub-skills de la biblioteca.

## 🐙 6. Repositorio GitHub

Esta carpeta es también un repositorio git (`jjdmochon/antigravity-sync`, **privado**).
`.gitignore` excluye secretos (`*.bak` de MCP con tokens, `.env`), datos locales
(`config/projects`, `sidecars`) y el esquema antiguo (`archive`, `claude_skills`).

```powershell
git add -A; git commit -m "sync"; git push
```

Haz `push` desde un solo equipo cada vez: Drive sincroniza también `.git`.
