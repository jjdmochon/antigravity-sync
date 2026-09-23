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

## 📁 4. Estructura de las skills (desde 2026-09-21)

Hay **una sola copia canónica** de las skills en cada equipo:

```
~\.agents\skills          <- copia real, canónica (139 skills)
~\.claude\skills          -> junction a la anterior
~\.gemini\config\skills   -> junction a la anterior
```

Editar en cualquiera de las tres rutas es equivalente: escriben en el mismo sitio. En
Drive las skills viajan **solo** en `agents_skills\`.

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
| Skills (180) | `~\.claude\skills` → junction a `~\.agents\skills` | `agents_skills\` |
| Subagentes | `~\.claude\agents\*.md` | `claude_agents\` |
| Instrucciones globales | `~\.claude\CLAUDE.md` | `CLAUDE.md` |

Skills incorporadas desde los plugins de Antigravity: `gemini-api-dev`, `gemini-interactions-api`,
`gemini-live-api-dev`, `gemini-omni-flash-api`, `android-cli`, `google-antigravity-sdk`,
`developing-with-bigquery`, `gcloud-auth-verification`.

MCP equivalentes a los de Antigravity (se registran una vez por equipo, ámbito usuario):

```powershell
claude mcp add --scope user --transport http gemini-api-docs https://gemini-api-docs-mcp.dev
claude mcp add --scope user chrome-devtools -- npx -y chrome-devtools-mcp@latest
claude mcp add --scope user tooluniverse -- uvx --from tooluniverse tooluniverse-smcp-stdio
```

## 🐙 6. Repositorio GitHub

Esta carpeta es también un repositorio git (`jjdmochon/antigravity-sync`, **privado**).
`.gitignore` excluye secretos (`*.bak` de MCP con tokens, `.env`), datos locales
(`config/projects`, `sidecars`) y el esquema antiguo (`archive`, `claude_skills`).

```powershell
git add -A; git commit -m "sync"; git push
```

Haz `push` desde un solo equipo cada vez: Drive sincroniza también `.git`.
