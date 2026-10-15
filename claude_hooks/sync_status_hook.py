#!/usr/bin/env python3
"""SessionStart: avisa si toca sync-pull o sync-push (llama a sync-status.ps1 en Drive).
Silencioso si todo esta al dia o si no encuentra Drive. Nunca bloquea el arranque."""
import json
import subprocess
import sys
from pathlib import Path

CANDIDATES = [r"%s:\Mi unidad\Antigravity-Sync" % d for d in "KIG"]
CANDIDATES.append(str(Path.home() / "Google Drive" / "Antigravity-Sync"))


def main():
    script = next((Path(c) / "sync-status.ps1" for c in CANDIDATES if (Path(c) / "sync-status.ps1").exists()), None)
    if not script:
        return
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), "-Silencioso", "-SinGit"],
            capture_output=True, text=True, encoding="utf-8", timeout=45,
        )
    except Exception:
        return
    msg = (r.stdout or "").strip()
    if msg:
        print(json.dumps({"systemMessage": msg}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
