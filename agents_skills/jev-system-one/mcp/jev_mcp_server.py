#!/usr/bin/env python3
r"""
jev_mcp_server.py - Jev System-1 como servidor MCP (stdio) para la app de escritorio de Claude.

La app no ejecuta los scripts de una skill en este equipo, pero si llama a servidores MCP
locales. Este servidor expone el gatekeeper y el router de Jev sin duplicar su logica: importa
jev_doc_gatekeeper.py y jev_router.py de ../scripts.

Requisitos: Python 3.13 (py -3.13) con typesafe-sdk, mcp>=2, python-dotenv, python-docx y
pymupdf; TYPESAFE_API_KEY en ~/.env. Registro en %APPDATA%\Claude\claude_desktop_config.json:

    "jev": {"command": "py", "args": ["-3.13", "<ruta>\\jev_mcp_server.py"]}

Prueba sin la app:  py -3.13 jev_mcp_server.py --selftest
"""

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import jev_doc_gatekeeper as gk  # noqa: E402  (carga ~/.env al importarse)
import jev_router  # noqa: E402

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402  (mensaje visible para el modelo)

INSTRUCCIONES = """\
Jev System-1 gobierna el pipeline de revision documental de Juanjo.
Etapa 0: llama a jev_gate_text (texto del chat o adjunto) o jev_gate_file (ruta en disco) y
ejecuta SOLO las etapas de 'etapas_a_ejecutar': 1_watermarks -> remove-ai-marks;
2_anti_slop -> no-ai-slop; 3_voz -> la skill de 'humanizer_skill' (nunca las dos);
4_latex -> sustituir LaTeX crudo por Unicode.
Etapa 4: vuelve a llamar a la herramienta con el texto final. Solo se entrega como
certificado si quality_gate_passed es true; cita slop_probability y las probabilidades.
Si engine es 'fallo-abierto (sin Jev)', ejecuta todas las etapas y di que no hay certificacion.
"""

servidor = MCPServer(name="jev", title="Jev System-1", version="1.0.0",
                     instructions=INSTRUCCIONES)

FORMATOS = {".md", ".txt", ".docx", ".pdf", ".html", ".htm", ".tex", ".rst"}


def _lang(lang):
    if lang in (None, "", "auto"):
        return None
    if lang not in ("es", "en"):
        raise ToolError("lang debe ser 'es', 'en' o vacio (deteccion automatica)")
    return lang


@servidor.tool(
    name="jev_gate_text",
    description=(
        "Gatekeeper Jev (etapas 0 y 4 del pipeline) sobre un texto: detecta marcas invisibles "
        "y homoglifos, y estima con Jev la probabilidad de slop, voz no calibrada y LaTeX crudo. "
        "Devuelve etapas_a_ejecutar, humanizer_skill y quality_gate_passed. Usalo con el texto "
        "pegado o adjunto en el chat; para ficheros de disco usa jev_gate_file."))
def jev_gate_text(texto: str, lang: str | None = None) -> dict:
    if not texto or not texto.strip():
        raise ToolError("texto vacio")
    return gk.auditar(texto, None, _lang(lang))


@servidor.tool(
    name="jev_gate_file",
    description=(
        "Gatekeeper Jev sobre un fichero local (.md, .txt, .docx, .pdf, .html, .tex). Extrae el "
        "texto real (python-docx, PyMuPDF), muestrea inicio/medio/final en documentos largos y "
        "marca los formatos que pueden llevar metadatos C2PA/EXIF/XMP. Ruta absoluta."))
def jev_gate_file(ruta: str, lang: str | None = None) -> dict:
    p = Path(ruta).expanduser()
    if not p.is_absolute():
        raise ToolError("usa una ruta absoluta")
    if not p.is_file():
        raise ToolError("no existe el fichero: %s" % p)
    if p.suffix.lower() not in FORMATOS:
        raise ToolError("formato no soportado %s (admite %s)" % (p.suffix, ", ".join(sorted(FORMATOS))))
    return gk.auditar(gk.extraer_texto(p), p, _lang(lang))


@servidor.tool(
    name="jev_route",
    description=(
        "Router Jev System-1: clasifica una tarea en el dominio de Juanjo (destina_biotech, "
        "ugr_teaching, biophysics_pna, keratin_krt10, compliance_iso, review_provenance, "
        "scientific_tools, general_dev) y estima si requiere subagentes o ejecutar codigo."))
def jev_route(tarea: str) -> dict:
    if not tarea or not tarea.strip():
        raise ToolError("tarea vacia")
    return jev_router.route_task(tarea)


def _selftest():
    import json
    r = jev_gate_text("Estamos avanzando con la validacion del panel de miR-122.", "es")
    print(json.dumps({k: r[k] for k in ("engine", "slop_probability", "quality_gate_passed",
                                        "etapas_a_ejecutar")}, ensure_ascii=False))
    print(json.dumps({k: v for k, v in jev_route("Prepara el examen de QFDOS tema 4").items()
                      if k in ("domain", "engine")}, ensure_ascii=False))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        servidor.run("stdio")
