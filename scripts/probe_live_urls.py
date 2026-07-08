#!/usr/bin/env python3
"""Probe live URLs for HTTP status (audit 404/5xx)."""
from __future__ import annotations

import json
import re
import ssl
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.righettoimmobiliare.it"
TIMEOUT = 12


def probe(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "RighettoSEOProbe/1.0"})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception as e:
        return -1, str(e)


def collect_candidates() -> list[str]:
    paths = {"/", "/immobili", "/blog", "/servizi", "/sitemap.xml", "/api/send-mail.php", "/scraping.html"}
    for p in ROOT.glob("*.html"):
        name = p.stem
        if name in ("404",):
            continue
        paths.add(f"/{name}")
        paths.add(f"/{name}.html")
    # blog-articolo slugs
    blog_html = (ROOT / "blog.html").read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r'"url_statico":\s*"([^"]+)"', blog_html):
        slug = m.group(1).strip()
        paths.add(f"/blog-articolo?s={slug}")
        paths.add(f"/{slug}")
    return sorted(paths)


def main() -> None:
    results = []
    for path in collect_candidates():
        url = BASE + path
        code, final = probe(url)
        results.append({"path": path, "status": code, "final": final})
        print(f"{code:>4} {path}")

    out = ROOT / "data" / "url-probe-latest.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    bad = [r for r in results if r["status"] >= 400 or r["status"] < 0]
    print(f"\nProbed {len(results)} URLs — issues: {len(bad)}")
    for r in bad:
        print(f"  {r['status']} {r['path']}")


if __name__ == "__main__":
    main()
