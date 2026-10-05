#!/usr/bin/env python3
"""Status line de Claude Code: modelo · % de contexto · coste de la sesion · carpeta actual.

Lee el JSON que Claude Code pasa por stdin. Los campos que falten se omiten en vez de fallar,
porque el esquema cambia entre versiones.
"""

import json
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


def main():
    try:
        d = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        d = {}
    parts = []

    model = (d.get("model") or {}).get("display_name")
    if model:
        parts.append(model)

    ctx = d.get("context_window") or {}
    pct = ctx.get("used_percentage")
    if pct is None and ctx.get("total_input_tokens") and ctx.get("context_window_size"):
        pct = 100.0 * ctx["total_input_tokens"] / ctx["context_window_size"]
    if pct is not None:
        parts.append("ctx %d%%" % round(pct))

    cost = (d.get("cost") or {}).get("total_cost_usd")
    if cost is not None:
        parts.append("$%.2f" % cost)

    cwd = (d.get("workspace") or {}).get("current_dir") or d.get("cwd")
    if cwd:
        p = Path(cwd)
        # En Drive interesa la carpeta del curso o proyecto, no "Mi unidad".
        parts.append(p.name or str(p))

    print(" · ".join(parts))


if __name__ == "__main__":
    main()
