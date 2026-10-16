---
name: humanizers-fuera-de-claude-code
description: Las humanizer con los 8 registros llegan a claude.ai como zips y a gemini.google.com como Gem; ambos se generan con empaquetar_humanizers.py y no certifican con Jev
metadata:
  type: project
  modified: 2026-10-16
---

Las skills `humanizer-juanjo` y `humanizer-juanjo-es` viven en `agents_skills/` y leen la guía
de registros en `~/.agents/skills/jev-system-one/references/registros.md`. Claude Code y
Antigravity las ven tal cual (Antigravity por la junction `~\.gemini\config\skills`). Fuera de
esos dos entornos no existe `~/.agents` ni Jev, así que hay dos paquetes adaptados (2026-10-16):

- **claude.ai / app de Claude:** `claude_ai_upload/humanizer-juanjo.zip` y
  `humanizer-juanjo-es.zip`. Cada zip lleva `references/registros.md` dentro. La skill deduce el
  registro del destinatario y del formato, o usa el que indique el usuario. Sustituyen a las
  humanizer de la cuenta: hay que borrar las antiguas y subir estas.
- **gemini.google.com:** Gem "Voz de Juanjo". `gemini_gem/instrucciones_gem.md` va en el campo
  Instrucciones (unos 10 000 caracteres); `gemini_gem/conocimiento/` (las dos humanizer y
  `registros.md`) va en Conocimiento.

**Regenerar:** `py -3.13 claude_ai_upload/empaquetar_humanizers.py` produce a la vez los zips y
`gemini_gem/conocimiento/`. Cada sustitución se comprueba y el script falla si alguna línea de
origen cambió o si queda una ruta local, para no producir un paquete a medias.

**Why:** sin estos paquetes, claude.ai y la app seguían con el perfil único de CEO, el mismo
que causaba los falsos positivos que resolvieron los registros ([[jev-gatekeeper-pipeline-documental]]).

**How to apply:**
- Tras editar una humanizer o `registros.md`, ejecutar el script, hacer commit y volver a subir
  los zips y los ficheros de conocimiento.
- `instrucciones_gem.md` no se genera: si cambia un registro (`registros.md` o
  `scripts/jev_registros.py`), hay que editar su sección a mano y volver a pegarla en el Gem.
  Sus criterios para identificar el registro copian el orden de `INSTR_CHOICE`.
- Ninguno de los dos paquetes certifica con Jev. Un entregable certificado se hace en Claude
  Code o en Antigravity.
- No está verificado que el Gem acepte 10 000 caracteres de instrucciones. Si los rechaza, se
  quita la sección "# Registros", que ya está completa en `registros.md`.
