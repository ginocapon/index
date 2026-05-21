"""
Legge dalla Pagina Facebook gli ultimi post pubblicati (Graph: published_posts)
e li salva in Supabase (tabella facebook_feed_cache) per l'agenda admin.

Prima crea la tabella: sql/facebook-feed-cache.sql

.env: META_PAGE_ID, META_PAGE_ACCESS_TOKEN, META_GRAPH_VERSION (opzionale),
      SUPABASE_URL, SUPABASE_KEY (service_role consigliato per upsert)

Permessi token utili: pages_read_engagement (oltre a quelli per pubblicare).

Nota: l'agenda/programmazione nativa in Meta Business Suite non è sempre esposta
via Graph come elenco unificato; questo script copre i post già pubblicati.
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


def graph_get_published_posts(
    version: str,
    page_id: str,
    token: str,
    limit: int,
) -> list[dict]:
    url = f"https://graph.facebook.com/{version.strip('/')}/{page_id}/published_posts"
    params = {
        "access_token": token,
        "limit": min(max(limit, 1), 100),
        "fields": "id,message,created_time,permalink_url,full_picture,status_type",
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
                + " — verifica permessi (es. pages_read_engagement) e token Pagina."
            )
        batch = data.get("data") or []
        rows.extend(batch)
        next_url = (data.get("paging") or {}).get("next")
        url = next_url if next_url and len(rows) < limit else None
        params = None  # next URL already has cursor
    return rows[:limit]


def parse_fb_time(s: str | None):
    if not s:
        return None
    # Es. 2024-05-16T12:00:00+0000
    try:
        if s.endswith("+0000"):
            s = s[:-5] + "+00:00"
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def main() -> int:
    load_env()
    ap = argparse.ArgumentParser(description="Sync Facebook Page posts → Supabase cache")
    ap.add_argument("--limit", type=int, default=40, help="Numero massimo post da scaricare")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo stampa JSON, non scrive su Supabase",
    )
    args = ap.parse_args()

    graph_v = os.environ.get("META_GRAPH_VERSION", "v21.0").strip().strip("/")
    page_id = req_env("META_PAGE_ID")
    token = req_env("META_PAGE_ACCESS_TOKEN")

    posts = graph_get_published_posts(graph_v, page_id, token, args.limit)
    print(f"Graph: ricevuti {len(posts)} post da published_posts.")

    if args.dry_run:
        print(json.dumps(posts, indent=2, ensure_ascii=False)[:8000])
        return 0

    sb = sb_client()
    now = datetime.now(timezone.utc).isoformat()
    batch: list[dict] = []
    for p in posts:
        pid = p.get("id")
        if not pid:
            continue
        batch.append(
            {
                "post_id": pid,
                "message": p.get("message"),
                "permalink_url": p.get("permalink_url"),
                "picture_url": p.get("full_picture"),
                "created_time": (
                    parse_fb_time(p.get("created_time")) or datetime.now(timezone.utc)
                ).isoformat(),
                "status_type": p.get("status_type"),
                "synced_at": now,
                "raw": p,
            }
        )

    if batch:
        sb.table("facebook_feed_cache").upsert(batch, on_conflict="post_id").execute()

    print(f"Supabase: upsert {len(batch)} righe in facebook_feed_cache.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
