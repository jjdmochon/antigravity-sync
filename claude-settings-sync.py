#!/usr/bin/env python3
"""
claude-settings-sync.py - Comparte entre equipos solo la parte comun de ~/.claude/settings.json.

settings.json no viaja entero: lleva estado propio de cada equipo (plugins, tema, permisos,
migraciones). Viajan tres claves:
  autoMode     contexto del clasificador del modo auto (se sustituye entera)
  skillOverrides  skills desactivadas u ocultas (Drive gana en conflicto, lo local se conserva)
  hooks        se fusionan por comando: un grupo de Drive sustituye al grupo local que comparta
               alguno de sus comandos; los hooks que solo existan en este equipo se conservan

Uso:
  py -3 claude-settings-sync.py export <settings.json> <shared.json>   (lo llama sync-push)
  py -3 claude-settings-sync.py merge  <shared.json> <settings.json>   (lo llama sync-pull)
"""

import copy
import json
import shutil
import sys
import time
from pathlib import Path

SHARED_KEYS = ("autoMode", "skillOverrides", "hooks")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def dump(obj, path):
    Path(path).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def commands(group):
    return {h.get("command") or h.get("prompt") or h.get("url") for h in group.get("hooks", [])} - {None}


def export(settings_path, shared_path):
    s = load(settings_path)
    shared = {k: s[k] for k in SHARED_KEYS if k in s}
    dump(shared, shared_path)
    print("  [+] settings compartidos exportados: %s" % (", ".join(shared) or "(ninguno)"))


def merge(shared_path, settings_path):
    shared = load(shared_path)
    p = Path(settings_path)
    s = load(p) if p.exists() else {}
    new = copy.deepcopy(s)

    if "autoMode" in shared:
        new["autoMode"] = shared["autoMode"]
    if "skillOverrides" in shared:
        new.setdefault("skillOverrides", {}).update(shared["skillOverrides"])
    for event, groups in shared.get("hooks", {}).items():
        local = new.setdefault("hooks", {}).setdefault(event, [])
        for g in groups:
            if g in local:
                continue
            cmds = commands(g)
            local[:] = [lg for lg in local if not (commands(lg) & cmds)]
            local.append(g)

    if new == s:
        print("  [=] settings.json ya tiene la parte compartida.")
        return
    if p.exists():
        shutil.copy2(p, p.with_name("settings.json.bak-" + time.strftime("%Y%m%d-%H%M%S")))
    dump(new, p)
    load(p)  # validar antes de dar por buena la escritura
    print("  [+] settings.json actualizado con autoMode, skillOverrides y hooks de Drive (copia .bak creada).")


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ("export", "merge"):
        sys.exit(__doc__)
    (export if sys.argv[1] == "export" else merge)(sys.argv[2], sys.argv[3])
