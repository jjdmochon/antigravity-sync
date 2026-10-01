#!/usr/bin/env python3
r"""
jev_doc_gatekeeper.py - Jev System-1 Gatekeeper para el Pipeline de Revision Documental.

Triaje no autoregresivo que decide QUE etapas del pipeline necesita realmente un
documento, y certifica el entregable al final (etapas 0 y 4 de CLAUDE.md seccion 3).

Reparto de responsabilidades:
  - Invisibles, homoglifos y metadatos -> deteccion DETERMINISTA local, sin API.
    Son preguntas mecanicas con respuesta exacta; no se delegan en un modelo.
  - Slop, voz y LaTeX                  -> Jev Noul con instrucciones especificadas.
  - Idioma                             -> Jev Choice (--lang lo sobreescribe).

Uso:
  python jev_doc_gatekeeper.py documento.md
  python jev_doc_gatekeeper.py informe.docx --json
  python jev_doc_gatekeeper.py tesis.pdf --lang es --json
  echo "texto" | python jev_doc_gatekeeper.py -
"""

import os
import re
import sys
import json
import time
import argparse
import unicodedata
from pathlib import Path

# Asegurar encoding UTF-8 en consola de Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

try:
    import dotenv
    dotenv.load_dotenv(Path.home() / ".env")
except ImportError:
    pass

UMBRAL = 0.50
MAX_CHARS = 9000  # ventana enviada a Jev; documentos largos se muestrean

# --------------------------------------------------------------------------
# Deteccion determinista (etapa 1 del pipeline)
# --------------------------------------------------------------------------

INVISIBLES = {
    "\u200b": "ZWSP (espacio de ancho cero)",
    "\u200c": "ZWNJ (no-unidor de ancho cero)",
    "\u200d": "ZWJ (unidor de ancho cero)",
    "\u2060": "WORD JOINER",
    "\ufeff": "BOM / ZWNBSP",
    "\u00ad": "SOFT HYPHEN",
    "\u180e": "MONGOLIAN VOWEL SEPARATOR",
    "\u2061": "FUNCTION APPLICATION",
    "\u2062": "INVISIBLE TIMES",
    "\u2063": "INVISIBLE SEPARATOR",
    "\u2064": "INVISIBLE PLUS",
}

HOMOGLIFOS = {
    "\u0430": "a", "\u0435": "e", "\u043e": "o", "\u0440": "p", "\u0441": "c",
    "\u0443": "y", "\u0445": "x", "\u0410": "A", "\u0412": "B", "\u0415": "E",
    "\u041a": "K", "\u041c": "M", "\u041d": "H", "\u041e": "O", "\u0420": "P",
    "\u0421": "C", "\u0422": "T", "\u0425": "X", "\u03bf": "o", "\u0391": "A",
    "\u0392": "B", "\u0395": "E", "\u0397": "H", "\u039f": "O", "\u03a1": "P",
}

METADATOS = {".docx", ".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".webp",
             ".pptx", ".xlsx", ".heic", ".mp4", ".mov"}

LATEX_PATTERNS = [
    r"\$[^$\n]+\$",
    r"\\\([^)]+\\\)",
    r"\\\[[^\]]+\\\]",
    r"\\text\{[^}]+\}",
    r"\\frac\{",
]


def escanear_marcas(texto, ruta):
    """Barrido determinista de marcas invisibles, homoglifos y metadatos."""
    hallazgos = []

    for ch, nombre in INVISIBLES.items():
        n = texto.count(ch)
        if n:
            hallazgos.append({"tipo": "invisible", "detalle": nombre,
                              "codepoint": "U+%04X" % ord(ch), "ocurrencias": n})

    vs = sum(1 for c in texto if "\ufe00" <= c <= "\ufe0f")
    if vs:
        hallazgos.append({"tipo": "invisible", "detalle": "VARIATION SELECTOR",
                          "codepoint": "U+FE00-FE0F", "ocurrencias": vs})
    tags = sum(1 for c in texto if "\U000e0000" <= c <= "\U000e007f")
    if tags:
        hallazgos.append({"tipo": "invisible",
                          "detalle": "TAG CHARS (watermark encubierto)",
                          "codepoint": "U+E0000-E007F", "ocurrencias": tags})

    # Homoglifos: solo se reportan si el texto es mayoritariamente latino
    intrusos = [(c, texto.count(c)) for c in HOMOGLIFOS if texto.count(c)]
    if intrusos:
        latinos = sum(1 for c in texto if "a" <= c.lower() <= "z")
        no_latinos = sum(1 for c in texto if c.isalpha()
                         and "CYRILLIC" in unicodedata.name(c, ""))
        if latinos > no_latinos * 10:
            for c, n in intrusos:
                hallazgos.append({
                    "tipo": "homoglifo",
                    "detalle": "%s se hace pasar por '%s'"
                               % (unicodedata.name(c, "?"), HOMOGLIFOS[c]),
                    "codepoint": "U+%04X" % ord(c), "ocurrencias": n})

    if ruta is not None and ruta.suffix.lower() in METADATOS:
        hallazgos.append({
            "tipo": "metadatos",
            "detalle": "formato %s puede portar C2PA/EXIF/XMP" % ruta.suffix.lower(),
            "codepoint": None, "ocurrencias": 1})

    return hallazgos


def latex_literal(texto):
    """LaTeX crudo detectado por regex sobre texto ya extraido correctamente."""
    return any(re.search(p, texto) for p in LATEX_PATTERNS)


# --------------------------------------------------------------------------
# Juicio -> Jev System-1
#
# Las instrucciones van deliberadamente especificadas al detalle. Medido:
# con instrucciones vagas el Noul se queda en 0.63 sobre slop evidente y no
# separa nada; con estas la separacion es 0.97 frente a 0.03.
# --------------------------------------------------------------------------

INSTR_SLOP = (
    "El texto muestra senales de redaccion generada por IA sin editar: muletillas "
    "(delve, tapestry, beacon, testament, pivotal, crucial, landscape, leverage, "
    "synergy, robust, seamless, unparalleled, transformative, revolutionize, "
    "profundizar, tapiz, faro, panorama, sin fisuras, papel crucial), transiciones "
    "formulaicas, construcciones 'no solo X sino tambien Y', cadencia de tres "
    "elementos repetida, clausulas -ing superficiales encadenadas, atribuciones vagas "
    "('los expertos coinciden'), y relleno corporativo sin contenido verificable. "
    "Responde verdadero solo si estas senales estan presentes de forma marcada."
)

INSTR_VOZ = (
    "El texto se DESVIA de la voz ejecutiva de Juanjo. Esa voz es: compuesta y "
    "tecnicamente precisa, con cifras y unidades concretas, plural natural en espanol "
    "('hemos cerrado', 'proponemos'), encabezados topicos ('En cuanto a...', "
    "'Respecto a...'), afirmaciones verificables y orientadas a la accion, calida pero "
    "controlada. Responde verdadero si el texto suena promocional, grandilocuente, "
    "impersonal, academicamente farragoso, o carece de concrecion tecnica; responde "
    "falso si ya cumple esa voz."
)

INSTR_LATEX = (
    "El texto contiene delimitadores LaTeX crudos que romperian una exportacion a Word "
    "o Google Docs: $...$, \\(...\\), \\[...\\], \\text{...}, \\frac, \\alpha y "
    "similares. Responde verdadero solo si aparecen delimitadores o macros LaTeX "
    "literales, no si simplemente hay simbolos matematicos Unicode."
)


def muestrear(texto):
    """Documentos largos: cabeza + centro + cola, para no perder slop enterrado."""
    if len(texto) <= MAX_CHARS:
        return texto
    t = MAX_CHARS // 3
    medio = (len(texto) - t) // 2
    return (texto[:t] + "\n\n[...]\n\n" + texto[medio:medio + t]
            + "\n\n[...]\n\n" + texto[-t:])


def consultar_jev(texto, lang=None):
    from typesafe_sdk import TypeSafeClient, Noul, Choice
    cliente = TypeSafeClient(api_key=os.getenv("TYPESAFE_API_KEY"))
    preguntas = {
        "slop": Noul(instructions=INSTR_SLOP),
        "voz": Noul(instructions=INSTR_VOZ),
        "latex": Noul(instructions=INSTR_LATEX),
    }
    if lang is None:
        preguntas["idioma"] = Choice(
            instructions="Idioma principal de redaccion del documento.",
            criteria={"es": "Espanol", "en": "Ingles"})

    a = cliente.system_one(state={"documento": muestrear(texto)},
                           questions=preguntas).answers
    return {
        "p_slop": round(float(a["slop"].noul), 3),
        "p_voz": round(float(a["voz"].noul), 3),
        "p_latex": round(float(a["latex"].noul), 3),
        "idioma": lang if lang else a["idioma"].choice,
    }


# --------------------------------------------------------------------------

def extraer_texto(ruta):
    """Extraccion real por formato. Leer un .docx o .pdf como texto plano
    devuelve binario comprimido: el veredicto saldria calculado sobre ruido."""
    ext = ruta.suffix.lower()
    if ext == ".docx":
        import docx
        d = docx.Document(str(ruta))
        partes = [p.text for p in d.paragraphs]
        for tabla in d.tables:
            for fila in tabla.rows:
                partes.extend(c.text for c in fila.cells)
        return "\n".join(partes)
    if ext == ".pdf":
        import fitz
        with fitz.open(str(ruta)) as doc:
            return "\n".join(pg.get_text() for pg in doc)
    t = ruta.read_text(encoding="utf-8", errors="replace")
    # Limpiar payloads base64 embebidos (data:image/...;base64,...) para evitar muestreo de ruido binario
    return re.sub(r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+', '[IMAGEN_BASE64]', t)


def auditar(texto, ruta, lang=None):
    t0 = time.perf_counter()
    marcas = escanear_marcas(texto, ruta)
    latex_local = latex_literal(texto)

    try:
        jev = consultar_jev(texto, lang)
        motor = "jev-native (typesafe-ai)"
        aviso = None
        degradado = False
    except Exception as e:
        # Sin veredicto de Jev no se descarta ninguna etapa NI se certifica nada.
        jev = {"p_slop": 1.0, "p_voz": 1.0, "p_latex": 1.0, "idioma": lang or "es"}
        motor = "fallo-abierto (sin Jev)"
        aviso = ("Jev no disponible (%s: %s). Se ejecutan todas las etapas y se "
                 "deniega la certificacion." % (type(e).__name__, e))
        degradado = True

    latex_final = bool(latex_local or jev["p_latex"] >= UMBRAL)
    humanizer = "humanizer-juanjo-es" if jev["idioma"] == "es" else "humanizer-juanjo"

    etapas = {
        "1_watermarks": {"ejecutar": bool(marcas), "motivo": "deteccion determinista",
                         "evidencia": marcas},
        "2_anti_slop": {"ejecutar": jev["p_slop"] >= UMBRAL,
                        "probabilidad": jev["p_slop"], "motivo": "Jev Noul"},
        "3_voz": {"ejecutar": jev["p_voz"] >= UMBRAL, "probabilidad": jev["p_voz"],
                  "motivo": "Jev Noul", "skill": humanizer},
        "4_latex": {"ejecutar": latex_final, "probabilidad": jev["p_latex"],
                    "motivo": "regex literal + Jev Noul"},
    }
    pendientes = [k for k, v in etapas.items() if v["ejecutar"]]

    # La certificacion exige veredicto real de Jev. Una caida de API nunca aprueba.
    aprobado = (not pendientes) and not degradado

    if degradado:
        dictamen = "Sin certificar: Jev inaccesible, ejecutar pipeline completo"
    elif aprobado:
        dictamen = "Certificado para entrega"
    else:
        dictamen = "Rechazado por Gatekeeper: ejecutar " + ", ".join(pendientes)

    res = {
        "status": "success",
        "engine": motor,
        "documento": str(ruta) if ruta else "<stdin>",
        "caracteres": len(texto),
        "muestreado": len(texto) > MAX_CHARS,
        "language": jev["idioma"],
        # --- claves de compatibilidad con CLAUDE.md seccion 3 ---
        "has_latex_violations": latex_final,
        "slop_probability": jev["p_slop"],
        "needs_humanizer_rewrite": jev["p_voz"] >= UMBRAL,
        "quality_gate_passed": aprobado,
        "recommendation": dictamen,
        # --- triaje por etapas ---
        "etapas": etapas,
        "etapas_a_ejecutar": pendientes,
        "humanizer_skill": humanizer,
        "latencia_ms": round((time.perf_counter() - t0) * 1000),
    }
    if aviso:
        res["warning"] = aviso
    return res


def main():
    global UMBRAL
    ap = argparse.ArgumentParser(description="Jev Document Pipeline Gatekeeper")
    ap.add_argument("target", help="Ruta del documento, o '-' para leer de stdin")
    ap.add_argument("--lang", choices=["es", "en"], default=None,
                    help="Forzar idioma (por defecto lo detecta Jev)")
    ap.add_argument("--json", action="store_true", help="Salida JSON")
    ap.add_argument("--umbral", type=float, default=UMBRAL,
                    help="Umbral de decision (def. 0.50)")
    args = ap.parse_args()
    UMBRAL = args.umbral

    if args.target == "-":
        texto, ruta = sys.stdin.read(), None
    else:
        ruta = Path(args.target)
        if not ruta.exists():
            print("ERROR: no existe %s" % ruta, file=sys.stderr)
            sys.exit(2)
        texto = extraer_texto(ruta)

    res = auditar(texto, ruta, args.lang)

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    def marca(b):
        return "EJECUTAR" if b else "  omitir"

    e = res["etapas"]
    print("\n=== JEV SYSTEM-1 DOCUMENT GATEKEEPER ===")
    print("Documento:     %s  (%d car.%s)"
          % (res["documento"], res["caracteres"],
             ", muestreado" if res["muestreado"] else ""))
    print("Idioma:        %s" % res["language"])
    print("Etapa 1:       %s  watermarks/metadatos  (%d hallazgos deterministas)"
          % (marca(e["1_watermarks"]["ejecutar"]), len(e["1_watermarks"]["evidencia"])))
    for h in e["1_watermarks"]["evidencia"]:
        cp = " " + h["codepoint"] if h["codepoint"] else ""
        print("                 - %s%s x%d" % (h["detalle"], cp, h["ocurrencias"]))
    print("Etapa 2:       %s  anti-slop  (p=%s)"
          % (marca(e["2_anti_slop"]["ejecutar"]), e["2_anti_slop"]["probabilidad"]))
    print("Etapa 3:       %s  voz -> %s  (p=%s)"
          % (marca(e["3_voz"]["ejecutar"]), e["3_voz"]["skill"],
             e["3_voz"]["probabilidad"]))
    print("LaTeX crudo:   %s  (p=%s)"
          % (marca(e["4_latex"]["ejecutar"]), e["4_latex"]["probabilidad"]))
    print("Quality Gate:  %s" % ("APROBADO" if res["quality_gate_passed"] else "RECHAZADO"))
    print("Dictamen:      %s" % res["recommendation"])
    print("Motor:         %s  (%d ms)\n" % (res["engine"], res["latencia_ms"]))
    if res.get("warning"):
        print("AVISO:         %s\n" % res["warning"])


if __name__ == "__main__":
    main()
