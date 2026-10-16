# Gem de Gemini: editor con la voz de Juanjo

Equivalente, en gemini.google.com, a las skills `humanizer-juanjo` y `humanizer-juanjo-es` con
los ocho registros de voz. Antigravity no lo necesita: lee las skills de `~\.agents\skills`.

## Crear el Gem

1. gemini.google.com → Gems → Nuevo Gem.
2. Nombre: `Voz de Juanjo`.
3. Instrucciones: pega el contenido completo de `instrucciones_gem.md`.
4. Conocimiento: sube los tres ficheros de `conocimiento/`
   (`humanizer-juanjo-es.md`, `humanizer-juanjo.md`, `registros.md`). Las instrucciones
   funcionan sin ellos; con ellos el Gem dispone de los perfiles completos y de los ejemplos
   de antes y después.
5. Guarda y prueba con un borrador de cada tipo, por ejemplo un aviso de examen y un párrafo
   de resultados. La última línea de la respuesta debe decir el registro aplicado.

Uso: pega el borrador y, si quieres fijar el registro, indícalo ("como manuscrito",
"es para alumnos", "carta de recomendación").

## Mantenimiento

`conocimiento/` se regenera junto con los zips de claude.ai:

```powershell
py -3.13 "K:\Mi unidad\Antigravity-Sync\claude_ai_upload\empaquetar_humanizers.py"
```

`instrucciones_gem.md` se mantiene a mano. Si cambia un registro en
`agents_skills/jev-system-one/references/registros.md` o en `scripts/jev_registros.py`, hay que
actualizar su sección aquí y volver a pegarla en el Gem.

El Gem no certifica con Jev. Para un documento certificado, usa Claude Code o Antigravity.
