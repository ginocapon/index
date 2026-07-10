# -*- coding: utf-8 -*-
"""
Automazione sync foto Supabase -> GitHub Pages + purge Storage.

Usato da GitHub Actions (.github/workflows/sync-media-github.yml).
In locale: python scripts/sync_media_automation.py

Richiede SUPABASE_KEY (service_role).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUPABASE_URL = "https://qwkwkemuabfwvwuqrxlu.supabase.co"
BUCKET = "foto-immobili"


def load_key() -> str:
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if key:
        return key
    env = ROOT / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("SUPABASE_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SUPABASE_KEY mancante")


def sb_get(path: str, key: str) -> list:
    req = urllib.request.Request(
        f"{SUPABASE_URL}{path}",
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def storage_count(key: str) -> int:
    body = json.dumps({"prefix": "", "limit": 1}).encode()
    req = urllib.request.Request(
        f"{SUPABASE_URL}/storage/v1/object/list/{BUCKET}",
        data=body,
        method="POST",
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            items = json.loads(r.read().decode("utf-8"))
        return len(items or [])
    except Exception:
        return 0


def pending_in_db(key: str) -> int:
    rows = sb_get("/rest/v1/immobili?select=codice,foto", key)
    n = 0
    for row in rows:
        foto = row.get("foto") or []
        if not isinstance(foto, list):
            continue
        for u in foto:
            if "supabase.co/storage" in str(u):
                n += 1
                break
    return n


def run(cmd: list[str]) -> int:
    print("+", " ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=str(ROOT))


def main() -> int:
    key = load_key()
    db_pending = pending_in_db(key)
    storage_files = storage_count(key)

    print(f"Immobili con foto ancora su Supabase (DB): {db_pending}")
    print(f"Oggetti in bucket {BUCKET}: {storage_files}")

    if db_pending == 0 and storage_files == 0:
        print("OK: niente da sincronizzare.")
        return 0

    py = sys.executable
    steps = [
        [py, "scripts/migrate_supabase_media.py", "--photos", "--update-db", "--sync-og", "--visite"],
    ]
    if storage_files > 0 or db_pending > 0:
        steps.append([py, "scripts/purge_supabase_foto_immobili.py", "--execute", "--batch", "50", "--pause", "0.5"])

    for cmd in steps:
        rc = run(cmd)
        if rc != 0:
            print(f"ERRORE: comando fallito (exit {rc})", file=sys.stderr)
            return rc

    print("OK: automazione sync media completata.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
