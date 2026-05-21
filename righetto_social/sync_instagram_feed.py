"""
Legge gli ultimi media pubblicati dell'account Instagram Business collegato alla Pagina
(Graph: GET /{ig-user-id}/media) e salva in Supabase (instagram_feed_cache).

Prima crea la tabella: sql/instagram-feed-cache.sql

.env:
  META_IG_USER_ID        — ID Instagram Business (obbligatorio per questo script)
  META_PAGE_ACCESS_TOKEN — token Pagina collegato all'IG (stesso di publish_from_agenda)
  META_GRAPH_VERSION     — opzionale
  SUPABASE_URL, SUPABASE_KEY — service_role consigliato per upsert

Permessi token utili: instagram_basic (lettura profilo/media).

Nota: i contenuti programmati nell'app Instagram/Meta non sono elencati qui finché non sono pubblicati.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv
from supabase import Client, create_client

ROOT = Path(__file__).resolve().parent


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def req_env(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        print(f"Manca variabile d'ambiente {name}", file=sys.stderr)
        sys.exit(2)
    return v


def sb_client() -> Client:
    url = (req_env("SUPABASE_URL")).strip().rstrip("/")
    for suf in ("/rest/v1", "/graphql/v1"):
        if url.endswith(suf):
            url = url[: -len(suf)].rstrip("/")
    low = url.lower()
    if "app.supabase.com" in low or "/dashboard" in low:
        print(
            "ERRORE: SUPABASE_URL deve essere Project URL (xxx.supabase.co), non la dashboard.",
            file=sys.stderr,
        )
        sys.exit(2)
    key = req_env("SUPABASE_KEY")
    return create_client(url, key)


def graph_get_ig_media(version: str, ig_user_id: str, token: str, limit: int) -> list[dict]:
    url = f"https://graph.facebook.com/{version.strip('/')}/{ig_user_id}/media"
    params = {
        "access_token": token,
        "limit": min(max(limit, 1), 100),
        "fields": "id,caption,media_type,media_url,thumbnail_url,permalink,timestamp",
    }
    rows: list[dict] = []
    while url:
        r = requests.get(url, params=params, timeout=45)
        try:
            data = r.json()
        except Exception:
            print(r.text[:500], file=sys.stderr)
            r.raise_for_status()
            raise
        if r.status_code >= 400:
            err = data.get("error", {})
            raise RuntimeError(
                err.get("message", r.text[:300])
                + " — verifica META_IG_USER_ID, token Pagina e permesso instagram_basic."
            )
        batch = data.get("data") or []
        rows.extend(batch)
        next_url = (data.get("paging") or {}).get("next")
        url = next_url if next_url and len(rows) < limit else None
        params = None
    return rows[:limit]


def parse_ig_timestamp(s: str | None):
    if not s:
        return None
    try:
        # Es. 2024-05-16T12:00:00+0000 oppure ISO con Z
        if s.endswith("+0000"):
            s = s[:-5] + "+00:00"
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def main() -> int:
    load_env()
    ap = argparse.ArgumentParser(description="Sync Instagram Business media → Supabase cache")
    ap.add_argument("--limit", type=int, default=40, help="Numero massimo media da scaricare")
    ap.add_argument("--dry-run", action="store_true", help="Solo stampa JSON, non scrive su Supabase")
    args = ap.parse_args()

    graph_v = os.environ.get("META_GRAPH_VERSION", "v21.0").strip().strip("/")
    ig_id = req_env("META_IG_USER_ID")
    token = req_env("META_PAGE_ACCESS_TOKEN")

    media = graph_get_ig_media(graph_v, ig_id, token, args.limit)
    print(f"Graph: ricevuti {len(media)} elementi da IG media.")

    if args.dry_run:
        print(json.dumps(media, indent=2, ensure_ascii=False)[:8000])
        return 0

    sb = sb_client()
    now = datetime.now(timezone.utc).isoformat()
    batch: list[dict] = []
    for m in media:
        mid = m.get("id")
        if not mid:
            continue
        ts = parse_ig_timestamp(m.get("timestamp")) or datetime.now(timezone.utc)
        batch.append(
            {
                "media_id": mid,
                "caption": m.get("caption"),
                "permalink": m.get("permalink"),
                "media_url": m.get("media_url"),
                "thumbnail_url": m.get("thumbnail_url"),
                "media_type": m.get("media_type"),
                "timestamp": ts.isoformat(),
                "synced_at": now,
                "raw": m,
            }
        )

    if batch:
        sb.table("instagram_feed_cache").upsert(batch, on_conflict="media_id").execute()

    print(f"Supabase: upsert {len(batch)} righe in instagram_feed_cache.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
