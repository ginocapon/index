"""
Converte il token utente in .env nel token PAGINA Righetto Immobiliare.

Dopo OAuth in Graph API Explorer (pagine autorizzate), il .env puo' ancora
contenere il token utente. Questo script chiama:
  GET /{META_PAGE_ID}?fields=access_token,instagram_business_account

Uso:
  python estrai_token_pagina.py
  python estrai_token_pagina.py --scrivi-env
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scrivi-env",
        action="store_true",
        help="Sostituisce META_PAGE_ACCESS_TOKEN nel file .env",
    )
    args = parser.parse_args()
    load_dotenv(ENV_PATH)

    user_token = os.environ.get("META_PAGE_ACCESS_TOKEN", "").strip()
    page_id = os.environ.get("META_PAGE_ID", "").strip()
    graph_v = os.environ.get("META_GRAPH_VERSION", "v21.0").strip().strip("/")

    if not user_token or not page_id:
        print("Manca META_PAGE_ACCESS_TOKEN o META_PAGE_ID in .env", file=sys.stderr)
        return 2

    r = requests.get(
        f"https://graph.facebook.com/{graph_v}/{page_id}",
        params={
            "fields": "access_token,instagram_business_account,name",
            "access_token": user_token,
        },
        timeout=30,
    )
    data = r.json()
    if data.get("error"):
        print(f"Errore Graph: {data['error'].get('message', data['error'])}", file=sys.stderr)
        return 1

    page_token = (data.get("access_token") or "").strip()
    if not page_token:
        print("Nessun access_token pagina nella risposta.", file=sys.stderr)
        return 1

    ig = (data.get("instagram_business_account") or {}).get("id", "")
    dbg = requests.get(
        f"https://graph.facebook.com/{graph_v}/debug_token",
        params={"input_token": page_token, "access_token": page_token},
        timeout=30,
    ).json().get("data", {})
    print(f"Pagina: {data.get('name')} (id {page_id})")
    print(f"Token pagina tipo: {dbg.get('type', '?')}")
    print(f"Token pagina (inizio): {page_token[:24]}…")
    if ig:
        print(f"Instagram collegato: {ig}")

    if args.scrivi_env:
        if not ENV_PATH.exists():
            print(f"File assente: {ENV_PATH}", file=sys.stderr)
            return 1
        text = ENV_PATH.read_text(encoding="utf-8")
        if re.search(r"^META_PAGE_ACCESS_TOKEN=", text, re.M):
            text = re.sub(
                r"^META_PAGE_ACCESS_TOKEN=.*$",
                f"META_PAGE_ACCESS_TOKEN={page_token}",
                text,
                count=1,
                flags=re.M,
            )
        else:
            text += f"\nMETA_PAGE_ACCESS_TOKEN={page_token}\n"
        if ig and re.search(r"^META_IG_USER_ID=", text, re.M):
            text = re.sub(
                r"^META_IG_USER_ID=.*$",
                f"META_IG_USER_ID={ig}",
                text,
                count=1,
                flags=re.M,
            )
        elif ig:
            text += f"META_IG_USER_ID={ig}\n"
        ENV_PATH.write_text(text, encoding="utf-8")
        print(f"OK: aggiornato {ENV_PATH}")
        print("Rilancia: python verifica_meta.py")
    else:
        print("\nAnteprima OK. Per salvare nel .env:")
        print("  python estrai_token_pagina.py --scrivi-env")

    return 0


if __name__ == "__main__":
    sys.exit(main())
