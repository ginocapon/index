# -*- coding: utf-8 -*-
"""Verifica indicizzazione pubblica (site: + pagina live + sitemap lastmod)."""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://righettoimmobiliare.it"
PAGES = [
    "/zona-limena",
    "/agenzia-immobiliare-padova",
    "/blog-rendimento-affitto-padova",
    "/blog-affitto-breve-padova-2026",
    "/blog-quotazioni-locazioni-omi-istat-padova-2026",
]
UA = "RighettoIndexCheck/1.0"


def fetch(url: str, timeout: int = 25) -> tuple[int, str, dict]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace"), dict(resp.headers)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, body, dict(e.headers) if e.headers else {}


def google_site_query(path: str) -> str:
    q = urllib.parse.quote(f"site:righettoimmobiliare.it{path}")
    return f"https://www.google.com/search?q={q}&num=5"


def check_google_index(path: str) -> dict:
    """Euristica: pagina SERP Google contiene URL canonico."""
    code, html, _ = fetch(google_site_query(path))
    if code != 200:
        return {"indexed_signal": "unknown", "note": f"Google HTTP {code}"}
    slug = path.lstrip("/")
    found = (
        f"righettoimmobiliare.it/{slug}" in html
        or f"www.righettoimmobiliare.it/{slug}" in html
    )
    if found:
        return {"indexed_signal": "likely_yes", "note": "URL compare in site: Google"}
    if "did not match any documents" in html.lower() or "nessun documento" in html.lower():
        return {"indexed_signal": "likely_no", "note": "site: Google — nessun risultato"}
    return {"indexed_signal": "unclear", "note": "SERP non interpretabile (captcha/blocco bot)"}


def main() -> int:
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    results = []

    for path in PAGES:
        url = SITE + path
        code, body, headers = fetch(url)
        title_m = re.search(r"<title>([^<]+)</title>", body, re.I)
        desc_m = re.search(r'name="description" content="([^"]*)"', body, re.I)
        canon_m = re.search(r'<link rel="canonical" href="([^"]+)"', body, re.I)
        lastmod_m = re.search(
            rf"<loc>{re.escape(url)}</loc><lastmod>([^<]+)</lastmod>", sitemap
        )
        idx = check_google_index(path)
        results.append({
            "path": path,
            "live_status": code,
            "title": title_m.group(1).strip() if title_m else "",
            "meta_len": len(desc_m.group(1)) if desc_m else 0,
            "canonical": canon_m.group(1) if canon_m else "",
            "sitemap_lastmod": lastmod_m.group(1) if lastmod_m else "missing",
            "google_index": idx,
        })

    out = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "pages": results,
        "gsc_note": "Conferma definitiva solo in GSC → Ispezione URL (non in Sitemap inviate)",
    }
    out_path = ROOT / "data" / "index-check-sostenere-latest.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=== Verifica pagine SOSTENERE ===\n")
    for r in results:
        sig = r["google_index"]["indexed_signal"]
        icon = {"likely_yes": "OK", "likely_no": "NO", "unclear": "?", "unknown": "?"}.get(sig, "?")
        print(f"[{icon}] {r['path']}")
        print(f"     Live: HTTP {r['live_status']} | lastmod sitemap: {r['sitemap_lastmod']}")
        print(f"     Title: {r['title'][:70]}")
        print(f"     Google site:: {r['google_index']['note']}")
        print()
    print(f"Report: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
