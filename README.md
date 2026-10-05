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
- Instala `GEMINI.md` y los catálogos fechados `GLOBAL_AGENTS_AND_TOOLS_<fecha>.md` y
  `SUBAGENTS_TEMPLATES_<fecha>.md` (vigentes: `_2026-10-01`). Al publicar una versión nueva,
  mueve la anterior a `archive\` y actualiza los enlaces de `GEMINI.md`.
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
~\.agents\skill-library   <- BIBLIOTECA: ~228 skills que no se cargan solas
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
- `sync-pull` tampoco pisa la configuración local (desde 2026-10-01). `config\` y `claude_agents\`
  se traen sin purga y con `/XO`. Nunca se traen `config\projects`, `config\sidecars` ni `.migrated`,
  porque llevan rutas y letras de unidad de cada equipo. `CLAUDE.md`, `GEMINI.md` y los catálogos
  fechados siguen la misma regla. Si la copia local es más reciente, se queda y el script avisa. Si
  Drive la sustituye, la local se guarda antes como `<fichero>.bak-<fecha>`.
- `sync-push` es el espejo: `config\` sube sin purga y con `/XO`, sin `projects`, `sidecars` ni
  `.migrated`. `CLAUDE.md`, `GEMINI.md` y los catálogos no suben si la versión de Drive es más
  reciente, que es un cambio del otro equipo que aún no ha llegado; en ese caso avisa: `sync-pull` y repite.
  El núcleo y la biblioteca suben con `/MIR /XO`: se propagan los borrados y los cambios de nivel,
  pero un fichero local más antiguo no sustituye al de Drive. Consecuencia: si restauras a mano una
  versión antigua de un fichero conservando su fecha, `sync-push` no la sube; tócala antes
  (`(Get-Item <fichero>).LastWriteTime = Get-Date`).
- `sync-push` se niega a subir si el núcleo local tiene más de 70 skills (equipo sin migrar) o si
  Drive tiene skills de biblioteca que este equipo no tiene. En ambos casos: `sync-pull` primero.
- **Registro de la última sincronización** (`~\.agents\sync-manifest.txt`, de `sync-manifest.ps1`).
  `sync-pull` y `sync-push` guardan la lista de ficheros de núcleo y biblioteca que este equipo
  conoce en Drive. `sync-push` solo borra en Drive lo que está en esa lista, es decir, lo que
  borraste aquí. Si Drive tiene ficheros que llegaron después (el otro equipo los subió y aún no
  hiciste `sync-pull`), aborta y los enumera. No compara fechas, porque robocopy conserva la original
  y una skill descomprimida de un zip llega con fechas antiguas. Un equipo sin registro debe hacer
  `sync-pull` una vez antes de su primer `sync-push`.
- **Retirar un plugin de `config\`:** como nada purga, bórralo en los dos equipos y en
  `config\plugins` de Drive. **Retirar un subagente:** bórralo en los dos equipos; `sync-push` lo
  quita de Drive.

Los SKILL.md duplicados dentro de `config\plugins\*` están desactivados (`SKILL.md.disabled`)
porque Antigravity los cargaba además de los del núcleo. El MCP `claude-skills` de
`~\.gemini\antigravity-ide\mcp_config.json` está en `"disabled": true` por el mismo motivo.

Antes de esa fecha las tres eran carpetas reales independientes y llevaban meses
divergiendo en silencio, porque los scripts solo creaban el junction si la ruta no
existía y nunca reparaban una carpeta real ya presente. Ahora `sync-push` y `sync-pull`
detectan ese caso, apartan la carpeta como `.bak-<fecha>` y rehacen el enlace.

`claude_skills\` era del esquema antiguo; desde 2026-10-01 está en `archive\claude_skills\`.

**No se sincronizan** (se excluyen en ambos scripts, y no sirven en otro equipo porque
llevan rutas absolutas del equipo origen): `.venv`, `.git`, `__pycache__`, `node_modules`,
`*.pyc`, `desktop.ini`.

### Después de un `sync-pull` en un equipo nuevo

Las claves de API no viajan por Drive. Copia `.env.example` a `~\.env` en el equipo destino y
rellena los valores (`TYPESAFE_API_KEY`, `ALPHAGENOME_API_KEY`, `GOOGLE_API_KEY`; la plantilla
dice de dónde sale cada una). `sync-pull` compara `~\.env` con la plantilla y avisa de las que
falten o estén vacías, sin mostrar nunca los valores.

Las skills de Jev se ejecutan con `py -3.13` (`typesafe-sdk`, `python-dotenv`, `python-docx`,
`pymupdf`). `sync-pull` avisa si falta Python 3.13 o alguno de esos paquetes.

---

## 🤖 5. Claude Code (desde 2026-09-23)

Claude Code (`claude`, instalado en `~\.local\bin\claude.exe`) usa las mismas piezas:

| Pieza | Ruta en Claude | Origen |
| :--- | :--- | :--- |
| Skills de núcleo (~44) | `~\.claude\skills` → junction a `~\.agents\skills` | `agents_skills\` |
| Biblioteca (~228) | `~\.agents\skill-library`, vía `skill-catalog` | `skill_library\` |
| Subagentes | `~\.claude\agents\*.md` | `claude_agents\` |
| Instrucciones globales | `~\.claude\CLAUDE.md` | `CLAUDE.md` |
| Hooks (`doc_gate.py`: Zero-LaTeX + Jev gate) | `~\.claude\hooks` | `claude_hooks\` |
| Comandos (`/albatross`) | `~\.claude\commands` | `claude_commands\` |
| Memoria global | `~\.claude\projects\C--Users-<usuario>\memory` | `claude_memory\` |
| Parte común de `settings.json` | `autoMode`, `skillOverrides`, `hooks` | `claude_settings_shared.json` |

Hooks, comandos y memoria viajan sin purga en los dos sentidos (desde 2026-10-05): lo que solo
exista en un equipo se conserva, y para retirar algo hay que borrarlo en los dos equipos y en Drive.
`settings.json` **no** viaja entero, porque plugins, tema y permisos son de cada equipo:
`sync-push` exporta las tres claves comunes con `claude-settings-sync.py export` y `sync-pull`
las fusiona con `merge` (copia `settings.json.bak-<fecha>` antes de escribir; los hooks se
fusionan por comando y los que solo existan en ese equipo se conservan).

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

### App de escritorio de Claude: Jev como MCP local (desde 2026-10-02)

La app de escritorio no ejecuta los scripts de las skills, así que `sync-pull` (paso 14) registra
en `%APPDATA%\Claude\claude_desktop_config.json` el servidor `jev`
(`agents_skills\jev-system-one\mcp\jev_mcp_server.py`, con `py -3.13`). Expone
`jev_gate_text`, `jev_gate_file` y `jev_route`, de modo que la app puede ejecutar las etapas 0 y 4
del pipeline con las skills de la cuenta (`remove-ai-marks`, `no-ai-slop`, `humanizer-juanjo(-es)`).
Requiere `mcp>=2` en Python 3.13 y reiniciar la app. Solo afecta a la app de escritorio de cada
equipo; claude.ai web y el móvil no ven MCP locales. Las skills subidas a la cuenta están en
`claude_ai_upload\`.

## 🐙 6. Repositorio GitHub

Esta carpeta es también un repositorio git (`jjdmochon/antigravity-sync`, **privado**).
`.gitignore` excluye secretos (`*.bak` de MCP con tokens, `.env`), datos locales
(`config/projects`, `sidecars`) el esquema antiguo (`archive`, `claude_skills`) y los accesos `*.gdoc` que crea Drive.

```powershell
git add -A; git commit -m "sync"; git push
```

Haz `push` desde un solo equipo cada vez: Drive sincroniza también `.git`.
