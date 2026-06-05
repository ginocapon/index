#!/usr/bin/env python3
"""Verifica se tabelle sensibili sono leggibili con chiave anon (RLS assente o policy aperte)."""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ANON = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0."
    "JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc"
)
TABLES = [
    "richieste",
    "clienti",
    "smtp_config",
    "campagne_email",
    "pianificazioni",
    "bozze_social",
    "newsletter_subscribers",
]


def load_supabase_url() -> str:
    env_path = Path(__file__).resolve().parents[1] / "righetto_social" / ".env"
    if not env_path.is_file():
        raise SystemExit(f"Manca {env_path}")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("SUPABASE_URL="):
            return line.split("=", 1)[1].strip().strip('"').strip("'").rstrip("/")
    raise SystemExit("SUPABASE_URL non trovato in .env")


def probe(base: str, table: str) -> tuple[str, str, bool]:
    req = urllib.request.Request(
        f"{base}/rest/v1/{table}?select=*&limit=1",
        headers={"apikey": ANON, "Authorization": f"Bearer {ANON}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read(500).decode("utf-8", errors="replace")
            exposed = False
            if resp.status == 200 and body.strip().startswith("["):
                try:
                    rows = json.loads(body)
                    exposed = isinstance(rows, list) and len(rows) > 0
                except json.JSONDecodeError:
                    exposed = True
            return str(resp.status), body[:160], exposed
    except urllib.error.HTTPError as exc:
        body = exc.read(300).decode("utf-8", errors="replace")
        return f"HTTP {exc.code}", body[:160], False
    except Exception as exc:  # noqa: BLE001
        return "ERR", str(exc)[:160], False


def main() -> None:
    base = load_supabase_url()
    print(f"Progetto: {base}\n")
    exposed_tables: list[str] = []
    for table in TABLES:
        status, detail, is_exposed = probe(base, table)
        marker = "ESPOSTA" if is_exposed else "ok/bloccata"
        print(f"  {table:24} {marker:12} {status} {detail[:100]}")
        if is_exposed:
            exposed_tables.append(table)
    print()
    if exposed_tables:
        print("ATTENZIONE: tabelle leggibili con anon:", ", ".join(exposed_tables))
        sys.exit(1)
    print("Nessuna tabella sensibile leggibile con anon.")


if __name__ == "__main__":
    main()
