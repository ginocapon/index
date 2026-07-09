# -*- coding: utf-8 -*-
"""Verifica post-migrazione media Supabase -> GitHub Pages."""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUPABASE_URL = "https://qwkwkemuabfwvwuqrxlu.supabase.co"
SITE = "https://righettoimmobiliare.it"


def load_key() -> str:
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if key:
        return key
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("SUPABASE_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SUPABASE_KEY mancante")


def fetch_immobili(key: str) -> list[dict]:
    url = f"{SUPABASE_URL}/rest/v1/immobili?select=id,codice,attivo,foto&order=codice"
    req = urllib.request.Request(
        url, headers={"apikey": key, "Authorization": f"Bearer {key}"}
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def main() -> int:
    key = load_key()
    rows = fetch_immobili(key)
    active = [r for r in rows if r.get("attivo") and not r.get("venduto", False)]

    err = 0
    warn = 0
    ok_files = 0
    supabase_left = 0
    local_paths = 0

    print("=== Verifica migrazione media ===\n")

    for row in active:
        cod = (row.get("codice") or "?").strip()
        foto = row.get("foto") or []
        if not isinstance(foto, list) or not foto:
            print(f"WARN {cod}: nessuna foto")
            warn += 1
            continue
        for i, u in enumerate(foto):
            u = str(u).strip()
            if "supabase.co/storage" in u:
                print(f"ERR {cod} foto[{i}]: ancora Supabase")
                err += 1
                supabase_left += 1
                continue
            if u.startswith("img/immobili/"):
                local_paths += 1
                p = ROOT / u.replace("/", os.sep)
                if not p.is_file():
                    print(f"ERR {cod}: file mancante {u}")
                    err += 1
                else:
                    ok_files += 1
            else:
                print(f"WARN {cod} foto[{i}]: path non standard {u[:60]}")
                warn += 1

    share_files = list(ROOT.glob("share-immobile-*.html"))
    share_supabase = 0
    share_local = 0
    for sf in share_files:
        html = sf.read_text(encoding="utf-8", errors="replace")
        m = re.search(r'property="og:image"\s+content="([^"]+)"', html)
        if not m:
            continue
        og = m.group(1)
        if "supabase.co" in og:
            share_supabase += 1
            if share_supabase <= 5:
                print(f"ERR share {sf.name}: OG ancora Supabase")
                err += 1
        elif f"{SITE}/img/immobili/" in og:
            share_local += 1

    manifest_path = ROOT / "data" / "media-manifest.json"
    manifest_count = 0
    if manifest_path.is_file():
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_count = len([k for k in raw if not str(k).startswith("_")])

    img_count = len(list((ROOT / "img" / "immobili").rglob("*.webp")))
    reel_count = len(list((ROOT / "img" / "video" / "reels").glob("*.mp4")))

    print(f"\n--- Riepilogo ---")
    print(f"Immobili attivi: {len(active)}")
    print(f"Foto DB locali (img/immobili): {local_paths}")
    print(f"Foto ancora Supabase in DB: {supabase_left}")
    print(f"File WebP su disco: {img_count}")
    print(f"File verificati esistenti: {ok_files}")
    print(f"Share pages OG -> img/immobili: {share_local}/{len(share_files)}")
    print(f"Share pages OG ancora Supabase: {share_supabase}")
    print(f"Reel MP4 locali: {reel_count}")
    print(f"Manifest voci: {manifest_count}")

    if err:
        print(f"\nESITO: FALLITO ({err} errori, {warn} warning)")
        return 1
    print(f"\nESITO: OK — pronto per push GitHub Pages (non cancellare ancora Supabase)")
    if warn:
        print(f"({warn} warning non bloccanti)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
