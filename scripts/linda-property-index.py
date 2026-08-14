#!/usr/bin/env python3
"""Indice immobili statico per Guardian freshness + Linda grounding."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OG = ROOT / "data/og-immobili.json"
OUT = ROOT / "data/linda-property-index-latest.json"


def main() -> int:
    og = json.loads(OG.read_text(encoding="utf-8")) if OG.exists() else {"bySlug": {}}
    by_slug = og.get("bySlug", {})
    items = []
    for slug, e in by_slug.items():
        items.append({
            "seo_slug": slug,
            "codice": e.get("codice"),
            "titolo": e.get("titolo"),
            "description": e.get("description"),
            "app_url": e.get("app_url"),
            "qr_url": f"https://righettoimmobiliare.it/qr-property?s={slug}",
        })

    out = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "count": len(items),
        "source": "data/og-immobili.json",
        "items": items,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK: property index {len(items)} immobili")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
