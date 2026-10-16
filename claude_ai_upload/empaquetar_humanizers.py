#!/usr/bin/env python3
r"""
empaquetar_humanizers.py - Genera humanizer-juanjo.zip y humanizer-juanjo-es.zip para claude.ai.

La app de Claude y claude.ai no ven ~/.agents ni ejecutan el gatekeeper Jev. Este script toma
las skills de agents_skills/, mete dentro de cada una la guia de registros
(jev-system-one/references/registros.md) y reescribe las lineas que dependen de Jev o de rutas
locales para que la skill deduzca el registro por si misma.

Uso (desde cualquier carpeta):
  py -3.13 empaquetar_humanizers.py
Cada sustitucion se comprueba: si una skill cambia y una linea ya no aparece, el script falla
en vez de producir un zip a medias.
"""

import sys
import zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
SKILLS = RAIZ / "agents_skills"
GUIA = SKILLS / "jev-system-one" / "references" / "registros.md"

RUTA_LOCAL = "`~/.agents/skills/jev-system-one/references/registros.md`"

SUSTITUCIONES = {
    "humanizer-juanjo-es": [
        ("Adapta la voz al registro que devuelve Jev:",
         "Adapta la voz al registro del texto, que deduce del destinatario y del formato:"),
        ("""1. Toma el registro de la salida del gatekeeper (`registro`, `guia_registro`). Si no hay
   salida de Jev, dedúcelo del destinatario y del formato; si sigue sin estar claro, pregunta.""",
         """1. Si el usuario indica el registro, usa ese. Si no, dedúcelo del destinatario y del
   formato: cada sección de `references/registros.md` dice qué textos cubre. Si sigue sin
   estar claro, pregunta."""),
        (RUTA_LOCAL, "`references/registros.md` (incluido en esta skill)"),
        ("4. La certificación final se pide con el mismo registro (`--registro <clave>`).",
         "4. Al entregar, indica en una línea el registro aplicado. En esta app no hay "
         "certificación Jev;\n   si el usuario la pide, dile que se hace en Claude Code o Antigravity."),
    ],
    "humanizer-juanjo": [
        ("Adapts the voice to the register Jev returns:",
         "Adapts the voice to the register of the text, inferred from the reader and the format:"),
        ("""1. Take the register from the gatekeeper output (`registro`, `guia_registro`). Without a Jev
   result, infer it from the reader and the format; if it is still unclear, ask.""",
         """1. If the user names the register, use it. Otherwise infer it from the reader and the
   format: each section of `references/registros.md` says which texts it covers. If it is
   still unclear, ask."""),
        (RUTA_LOCAL, "`references/registros.md` (bundled with this skill)"),
        ("4. Request final certification with the same register (`--registro <key>`).",
         "4. When delivering, state the register applied in one line. There is no Jev "
         "certification in\n   this app; if the user asks for it, say it runs in Claude Code or Antigravity."),
    ],
}

SUSTITUCIONES_GUIA = [
    ("""Guía de reescritura para la etapa 3 del pipeline. El gatekeeper devuelve `registro` y
`guia_registro` (esta página con el ancla del registro); el humanizador del idioma
(`humanizer-juanjo-es` o `humanizer-juanjo`) aplica la sección correspondiente.""",
     """Guía de reescritura por registro. El humanizador del idioma (`humanizer-juanjo-es` o
`humanizer-juanjo`) identifica el registro del texto y aplica la sección correspondiente."""),
    ("""Las instrucciones que usa Jev para puntuar cada registro están en
`scripts/jev_registros.py`. Si se cambia aquí un rasgo, hay que cambiarlo también allí
y recalibrar con `scripts/calibrar_registros.py`.

""", ""),
]


def sustituir(texto, pares, origen):
    for viejo, nuevo in pares:
        n = texto.count(viejo)
        if n != 1:
            sys.exit("ERROR en %s: se esperaba 1 aparicion y hay %d de:\n%s" % (origen, n, viejo[:120]))
        texto = texto.replace(viejo, nuevo)
    return texto


def main():
    guia = sustituir(GUIA.read_text(encoding="utf-8"), SUSTITUCIONES_GUIA, GUIA.name)
    for skill, pares in SUSTITUCIONES.items():
        fuente = SKILLS / skill / "SKILL.md"
        texto = sustituir(fuente.read_text(encoding="utf-8"), pares, "%s/SKILL.md" % skill)
        if "~/.agents" in texto or "gatekeeper" in texto:
            sys.exit("ERROR: %s conserva referencias locales tras empaquetar" % skill)
        destino = AQUI / ("%s.zip" % skill)
        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("%s/SKILL.md" % skill, texto)
            z.writestr("%s/references/registros.md" % skill, guia)
        print("[+] %s  (%d bytes)" % (destino.name, destino.stat().st_size))


if __name__ == "__main__":
    main()
