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
import jev_registros  # noqa: E402

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402  (mensaje visible para el modelo)

INSTRUCCIONES = """\
Jev System-1 gobierna el pipeline de revision documental de Juanjo.
Etapa 0: llama a jev_gate_text (texto del chat o adjunto) o jev_gate_file (ruta en disco) y
ejecuta SOLO las etapas de 'etapas_a_ejecutar': 1_watermarks -> remove-ai-marks;
2_anti_slop -> no-ai-slop; 3_voz -> la skill de 'humanizer_skill' (nunca las dos) aplicando
la seccion del registro devuelto en 'registro' (guia en 'guia_registro');
4_latex -> sustituir LaTeX crudo por Unicode.
Registro de voz: si sabes que tipo de texto es (aviso a alumnos, manuscrito, diapositivas,
email de CEO, propuesta, informe ISO, divulgacion), pasalo en 'registro'; si no, Jev lo
detecta. Usa el mismo registro en todas las rondas de un texto. Lista: jev_registros.
Etapa 4: vuelve a llamar a la herramienta con el texto final. Solo se entrega como
certificado si quality_gate_passed es true; cita slop_probability y las probabilidades.
Si engine es 'fallo-abierto (sin Jev)', ejecuta todas las etapas y di que no hay certificacion.
"""

servidor = MCPServer(name="jev", title="Jev System-1", version="1.0.0",
                     instructions=INSTRUCCIONES)

FORMATOS = {".md", ".txt", ".docx", ".pdf", ".pptx", ".html", ".htm", ".tex", ".rst"}


MAX_RONDAS = 3


def _con_siguiente_paso(res: dict, ronda: int) -> dict:
    """Anade la instruccion operativa al resultado. Las instrucciones del servidor no siempre
    llegan al modelo; un campo en cada respuesta si (el 2026-10-02 la app se salto la etapa 4)."""
    res["ronda"] = ronda
    if res.get("quality_gate_passed"):
        res["siguiente_paso"] = ("CERTIFICADO. Presenta el texto como certificado por Jev y cita "
                                 "slop_probability y las probabilidades de etapas.")
    elif res.get("engine", "").startswith("fallo-abierto"):
        res["siguiente_paso"] = ("Jev no disponible: aplica todas las etapas y entrega el texto "
                                 "indicando expresamente que NO esta certificado.")
    elif ronda >= MAX_RONDAS:
        res["siguiente_paso"] = ("Tope de %d rondas alcanzado sin certificar. Entrega la mejor version "
                                 "indicando expresamente que NO esta certificada, con las "
                                 "probabilidades de esta ronda, y pide datos concretos al usuario "
                                 "si la voz sigue fallando." % MAX_RONDAS)
    else:
        res["siguiente_paso"] = (
            "NO CERTIFICADO. Aplica solo estas etapas: %s (voz -> %s con el registro '%s', guia %s). "
            "Despues vuelve a llamar a esta misma herramienta con el texto final completo, "
            "registro='%s' y ronda=%d (etapa 4). No presentes ninguna version como final ni "
            "certificada hasta que quality_gate_passed sea true."
            % (", ".join(res.get("etapas_a_ejecutar", [])), res.get("humanizer_skill"),
               res.get("registro"), res.get("guia_registro"), res.get("registro"), ronda + 1))
    return res


def _registro(registro):
    if registro in (None, "", "auto"):
        return None
    if jev_registros.normalizar(registro) is None:
        raise ToolError("registro desconocido '%s' (validos: %s, o vacio para detectarlo)"
                        % (registro, ", ".join(jev_registros.REGISTROS)))
    return registro


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
        "La voz se juzga segun el registro: ceo, alumnos, manuscrito, diapositivas, propuesta, "
        "informe o divulgacion; pasalo en 'registro' si lo conoces, o dejalo vacio y Jev lo "
        "detecta. Devuelve etapas_a_ejecutar, humanizer_skill, registro, guia_registro, "
        "quality_gate_passed y siguiente_paso. "
        "OBLIGATORIO: tras editar el texto, vuelve a llamarla con la version final y ronda+1; "
        "nunca entregues un texto como final sin una llamada que devuelva quality_gate_passed=true "
        "o sin decir que no esta certificado. Para ficheros de disco usa jev_gate_file."))
def jev_gate_text(texto: str, lang: str | None = None, registro: str | None = None,
                  ronda: int = 1) -> dict:
    if not texto or not texto.strip():
        raise ToolError("texto vacio")
    return _con_siguiente_paso(gk.auditar(texto, None, _lang(lang), _registro(registro)), ronda)


@servidor.tool(
    name="jev_gate_file",
    description=(
        "Gatekeeper Jev sobre un fichero local (.md, .txt, .docx, .pdf, .pptx, .html, .tex). Extrae el "
        "texto real (python-docx, PyMuPDF), muestrea inicio/medio/final en documentos largos y "
        "marca los formatos que pueden llevar metadatos C2PA/EXIF/XMP. Ruta absoluta. Igual que "
        "jev_gate_text: tras editar, vuelve a llamarla (o jev_gate_text con el texto) con ronda+1. "
        "Admite 'registro'; tambien lo leen del fichero un marcador '<!-- registro: X -->' o un "
        "fichero .jev-registro en su carpeta."))
def jev_gate_file(ruta: str, lang: str | None = None, registro: str | None = None,
                  ronda: int = 1) -> dict:
    p = Path(ruta).expanduser()
    if not p.is_absolute():
        raise ToolError("usa una ruta absoluta")
    if not p.is_file():
        raise ToolError("no existe el fichero: %s" % p)
    if p.suffix.lower() not in FORMATOS:
        raise ToolError("formato no soportado %s (admite %s)" % (p.suffix, ", ".join(sorted(FORMATOS))))
    return _con_siguiente_paso(gk.auditar(gk.extraer_texto(p), p, _lang(lang), _registro(registro)),
                               ronda)


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


@servidor.tool(
    name="jev_registros",
    description=("Lista los registros de voz que entiende el gatekeeper (clave, nombre y que "
                 "textos cubre) para elegir el parametro 'registro' de jev_gate_text/jev_gate_file."))
def jev_registros_tool() -> list:
    return jev_registros.listar()


def _selftest():
    import json
    r = jev_gate_text("Estamos avanzando con la validacion del panel de miR-122.", "es")
    print(json.dumps({k: r[k] for k in ("engine", "slop_probability", "quality_gate_passed",
                                        "etapas_a_ejecutar", "registro")}, ensure_ascii=False))
    r = jev_gate_text("Os recuerdo que el examen parcial es el 14 de enero a las 9:00 en el "
                      "aula B2 y cuenta un 30 % de la nota final.", "es", "alumnos")
    print(json.dumps({k: r[k] for k in ("registro", "quality_gate_passed", "etapas_a_ejecutar")},
                     ensure_ascii=False))
    print(json.dumps({k: v for k, v in jev_route("Prepara el examen de QFDOS tema 4").items()
                      if k in ("domain", "engine")}, ensure_ascii=False))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        servidor.run("stdio")
