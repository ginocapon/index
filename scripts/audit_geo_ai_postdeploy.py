# -*- coding: utf-8 -*-
"""Audit rapido post-deploy: piano GEO/AI 6 punti."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://righettoimmobiliare.it"


def fetch(path: str) -> str:
    with urllib.request.urlopen(SITE + path, timeout=25) as r:
        return r.read().decode("utf-8", errors="replace")


def main() -> int:
    results = {}

    # 1 llms
    llms = fetch("/llms.txt")
    blog_live = len(set(re.findall(r"righettoimmobiliare\.it/(blog-[^)\s]+)", llms)))
    results["1_llms_blog"] = {"count": blog_live, "ok": blog_live >= 107}

    ai = json.loads(fetch("/ai.json"))
    results["1_ai_json"] = {
        "blogArticles": ai.get("contentIndex", {}).get("blogArticles"),
        "measurementId": ai.get("contentIndex", {}).get("measurementId"),
        "consentMode": ai.get("contentIndex", {}).get("consentMode"),
        "ok": ai.get("contentIndex", {}).get("blogArticles", 0) >= 107,
    }

    # 2 GA consent live pages
    pages = ["/contatti", "/zona-limena", "/agenzia-immobiliare-padova"]
    ga_ok = True
    for p in pages:
        h = fetch(p)
        if "googletagmanager.com/gtag/js?id=G-PHEL8KXLBX" in h or "ga-consent.js" not in h:
            ga_ok = False
    home = fetch("/")
    ga_ok = ga_ok and "ga-consent.js" in home
    results["2_ga_consent"] = {"ok": ga_ok}

    # 4 SOSTENERE meta live
    z = fetch("/zona-limena")
    results["4_zona_limena_title"] = re.search(r"<title>([^<]+)", z).group(1) if re.search(r"<title>", z) else ""
    r = fetch("/blog-rendimento-affitto-padova")
    results["4_rendimento_meta"] = (
        re.search(r'name="description" content="([^"]+)"', r).group(1)[:90] if re.search(r'name="description"', r) else ""
    )

    # robots AI
    robots = fetch("/robots.txt")
    results["robots_ai_bots"] = all(b in robots for b in ("GPTBot", "ClaudeBot", "Google-Extended", "PerplexityBot"))

    out = ROOT / "data" / "geo-ai-audit-latest.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=== Audit GEO/AI post-deploy ===")
    for k, v in results.items():
        status = "OK" if (v.get("ok") if isinstance(v, dict) else v) else "CHECK"
        if isinstance(v, dict) and "ok" in v:
            print(f"{status} {k}: {v}")
        else:
            print(f"    {k}: {v}")

    all_ok = results["1_llms_blog"]["ok"] and results["1_ai_json"]["ok"] and results["2_ga_consent"]["ok"] and results["robots_ai_bots"]
    print("\nESITO GLOBALE:", "IN REGOLA" if all_ok else "DA RIVEDERE")
    print("Report:", out)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
