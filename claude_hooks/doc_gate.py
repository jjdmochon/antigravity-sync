#!/usr/bin/env python3
r"""
doc_gate.py - PostToolUse hook (Write|Edit) que aplica CLAUDE.md seccion 3 a entregables.

Modos:
  latex  Sincrono, determinista, <50 ms. Bloquea (decision: block) si el fichero
         contiene delimitadores LaTeX crudos. El motivo vuelve a Claude.
  jev    Asincrono (asyncRewake). Ejecuta jev_doc_gatekeeper.py y sale con codigo 2
         solo si hay LaTeX, marcas invisibles/metadatos o slop; eso despierta a Claude
         con el informe. La etapa de voz NO bloquea: el Noul de voz da falsos
         positivos sobre texto ya calibrado.

Solo actua sobre .md / .html / .htm / .txt fuera de directorios de configuracion,
dependencias y temporales, y nunca sobre README/CLAUDE/SKILL/MEMORY/AGENTS.
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

EXTS = {".md", ".html", ".htm", ".txt"}
SKIP_DIRS = ("/.claude/", "/.agents/", "/.gemini/", "/node_modules/", "/.git/",
             "/appdata/local/temp/", "/.venv/", "/venv/", "/dist/", "/build/",
             "/.next/", "/site-packages/", "/.claude-worktrees/")
SKIP_NAMES = {"readme.md", "claude.md", "skill.md", "memory.md", "agents.md",
              "gemini.md", "changelog.md", "license.md", "contributing.md"}

GATEKEEPER = Path.home() / ".agents/skills/jev-system-one/scripts/jev_doc_gatekeeper.py"
LAST_RESULT = Path.home() / ".claude/state/jev-last.json"

LATEX_PATTERNS = [
    (re.compile(r"\\\(.+?\\\)"), r"\( ... \)"),
    (re.compile(r"\\\[.+?\\\]", re.S), r"\[ ... \]"),
    (re.compile(r"\\(?:text|mathrm|mathbf|frac|sqrt|alpha|beta|gamma|delta|Delta|mu|nu|cdot|times|rightarrow|to)\b"), r"comando \texto"),
    (re.compile(r"\$\$.+?\$\$", re.S), r"$$ ... $$"),
    # $...$ en linea con contenido matematico (^, _, \ o {) para no confundir precios
    (re.compile(r"(?<![\w$])\$(?=[^$\n]{1,120}\$)[^$\n]*[\\^_{][^$\n]*\$(?![\w$])"), r"$ ... $"),
]


def target_path(payload):
    ti = payload.get("tool_input") or {}
    tr = payload.get("tool_response") or {}
    p = ti.get("file_path") or (tr.get("filePath") if isinstance(tr, dict) else None)
    return Path(p) if p else None


def in_scope(path):
    if path is None or path.suffix.lower() not in EXTS or not path.is_file():
        return False
    norm = "/" + str(path.resolve()).replace("\\", "/").lower() + "/"
    if any(d in norm for d in SKIP_DIRS):
        return False
    return path.name.lower() not in SKIP_NAMES


def strip_code(text, suffix):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    if suffix in (".html", ".htm"):
        text = re.sub(r"<(script|style|code|pre)\b.*?</\1>", "", text, flags=re.S | re.I)
    return text


def mode_latex(path):
    text = strip_code(path.read_text(encoding="utf-8", errors="replace"), path.suffix.lower())
    hits = []
    for rx, label in LATEX_PATTERNS:
        m = rx.search(text)
        if m:
            hits.append("%s -> %r" % (label, m.group(0)[:60]))
    if hits:
        print(json.dumps({
            "decision": "block",
            "reason": ("LaTeX crudo en %s (CLAUDE.md: Zero Raw LaTeX). Sustituir por Unicode "
                       "nativo (1H RMN, DMSO-d6, Zn2+, Δ, ×, →). Encontrado: %s"
                       % (path.name, "; ".join(hits))),
        }, ensure_ascii=False))
    return 0


def mode_jev(path):
    if not GATEKEEPER.is_file():
        return 0
    try:
        out = subprocess.run([sys.executable, str(GATEKEEPER), str(path), "--json"],
                             capture_output=True, text=True, encoding="utf-8", timeout=90)
        res = json.loads(out.stdout)
    except Exception:
        return 0  # el gate nunca debe romper una edicion por un fallo de red/API
    etapas = res.get("etapas", {})
    fallos = []
    if res.get("has_latex_violations"):
        fallos.append("LaTeX crudo")
    if etapas.get("1_watermarks", {}).get("ejecutar"):
        fallos.append("marcas invisibles/metadatos %s -> watermarks-remover"
                      % etapas["1_watermarks"].get("evidencia", []))
    if etapas.get("2_anti_slop", {}).get("ejecutar"):
        fallos.append("slop p=%.2f -> no-ai-slop" % etapas["2_anti_slop"].get("probabilidad", 0))
    save_last(path, res, fallos)
    if fallos:
        sys.stderr.write("Jev gate RECHAZA %s: %s\n" % (path.name, "; ".join(fallos)))
        return 2
    return 0


def save_last(path, res, fallos):
    """Deja el ultimo veredicto en LAST_RESULT para el mod jev-status de Claude Code."""
    etapas = res.get("etapas", {})
    try:
        LAST_RESULT.parent.mkdir(parents=True, exist_ok=True)
        LAST_RESULT.write_text(json.dumps({
            "file": str(path),
            "time": int(time.time() * 1000),
            "gate_ok": not fallos,
            "quality_gate_passed": bool(res.get("quality_gate_passed")),
            "p_slop": etapas.get("2_anti_slop", {}).get("probabilidad"),
            "p_voz": etapas.get("3_voz", {}).get("probabilidad"),
            "fallos": fallos,
        }, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "latex"
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    path = target_path(payload)
    if not in_scope(path):
        return 0
    return mode_jev(path) if mode == "jev" else mode_latex(path)


if __name__ == "__main__":
    sys.exit(main())
