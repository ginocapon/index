"""
Verifica token Meta (.env): Facebook Page + Instagram Business rispondono.

Uso:
  python verifica_meta.py
  python verifica_meta.py --dry-run   # solo controlla variabili .env
"""

from __future__ import annotations

import argparse
import os
import sys

import requests
from dotenv import load_dotenv

ROOT = __import__("pathlib").Path(__file__).resolve().parent


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def req(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        print(f"Manca {name} in .env", file=sys.stderr)
        sys.exit(2)
    return v


def debug_token(token: str, graph_v: str) -> dict:
    r = requests.get(
        f"https://graph.facebook.com/{graph_v}/debug_token",
        params={"input_token": token, "access_token": token},
        timeout=30,
    )
    r.raise_for_status()
    return r.json().get("data") or {}


def test_page_publish(page_id: str, token: str, graph_v: str) -> str | None:
    """Prova post non pubblicato: fallisce se manca token pagina o permessi."""
    r = requests.post(
        f"https://graph.facebook.com/{graph_v}/{page_id}/feed",
        data={
            "message": "Test verifica Righetto (bozza, non visibile)",
            "published": "false",
            "access_token": token,
        },
        timeout=30,
    )
    data = r.json()
    if data.get("error"):
        return data["error"].get("message", str(data["error"]))
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Test connessione Graph API Meta")
    parser.add_argument("--dry-run", action="store_true", help="Solo presenza variabili .env")
    args = parser.parse_args()
    load_env()

    page_id = req("META_PAGE_ID")
    token = req("META_PAGE_ACCESS_TOKEN")
    ig_id = os.environ.get("META_IG_USER_ID", "").strip()
    graph_v = os.environ.get("META_GRAPH_VERSION", "v21.0").strip().strip("/")

    if args.dry_run:
        print("OK variabili .env presenti (META_PAGE_ID, META_PAGE_ACCESS_TOKEN)")
        if ig_id:
            print(f"OK META_IG_USER_ID={ig_id[:8]}…")
        else:
            print("Attenzione: META_IG_USER_ID vuoto (solo Facebook)")
        return 0

    ok = True
    try:
        info = debug_token(token, graph_v)
        ttype = (info.get("type") or "?").upper()
        scopes = info.get("scopes") or []
        print(f"Token tipo: {ttype} (scopes: {', '.join(scopes[:8])}{'…' if len(scopes) > 8 else ''})")
        if ttype == "USER":
            print(
                "ERRORE: in .env serve il token PAGINA, non quello utente.\n"
                "  Graph API Explorer → GET me/accounts?fields=name,id,access_token,"
                "instagram_business_account\n"
                "  Copia access_token della pagina Righetto in META_PAGE_ACCESS_TOKEN.",
                file=sys.stderr,
            )
            ok = False
            try:
                acc = requests.get(
                    f"https://graph.facebook.com/{graph_v}/me/accounts",
                    params={
                        "access_token": token,
                        "fields": "name,id,access_token,instagram_business_account",
                    },
                    timeout=30,
                ).json()
                for p in acc.get("data") or []:
                    ig = (p.get("instagram_business_account") or {}).get("id", "")
                    print(
                        f"  Pagina trovata: {p.get('name')} id={p.get('id')} "
                        f"ig={ig or '—'} (usa il suo access_token in .env)",
                        file=sys.stderr,
                    )
            except requests.RequestException:
                pass
        elif ttype != "PAGE":
            print(f"Attenzione: tipo token {ttype} — atteso PAGE", file=sys.stderr)
    except requests.RequestException as e:
        print(f"debug_token: {e}", file=sys.stderr)
        ok = False

    try:
        r = requests.get(
            f"https://graph.facebook.com/{graph_v}/{page_id}",
            params={"fields": "name,fan_count,instagram_business_account", "access_token": token},
            timeout=30,
        )
        data = r.json()
        if data.get("error"):
            print(f"Facebook ERRORE: {data['error'].get('message', data['error'])}", file=sys.stderr)
            ok = False
        else:
            print(f"Facebook OK: {data.get('name')} (fan: {data.get('fan_count', '?')})")
            ig_linked = (data.get("instagram_business_account") or {}).get("id")
            if ig_linked and ig_id and str(ig_linked) != str(ig_id):
                print(
                    f"Attenzione: META_IG_USER_ID={ig_id} ma la pagina ha ig={ig_linked}",
                    file=sys.stderr,
                )
            elif ig_linked and not ig_id:
                print(f"Suggerimento: META_IG_USER_ID={ig_linked}", file=sys.stderr)
            pub_err = test_page_publish(page_id, token, graph_v)
            if pub_err:
                print(f"Pubblicazione test ERRORE: {pub_err}", file=sys.stderr)
                ok = False
            else:
                print("Pubblicazione test OK (bozza non visibile su Facebook)")
    except requests.RequestException as e:
        print(f"Facebook rete: {e}", file=sys.stderr)
        ok = False

    if ig_id:
        try:
            r = requests.get(
                f"https://graph.facebook.com/{graph_v}/{ig_id}",
                params={"fields": "id", "access_token": token},
                timeout=30,
            )
            data = r.json()
            if data.get("error"):
                print(f"Instagram ERRORE: {data['error'].get('message', data['error'])}", file=sys.stderr)
                ok = False
            else:
                print(f"Instagram OK: account id {data.get('id', '?')}")
        except requests.RequestException as e:
            print(f"Instagram rete: {e}", file=sys.stderr)
            ok = False
    else:
        print("Instagram: saltato (META_IG_USER_ID assente)")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
