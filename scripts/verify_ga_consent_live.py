# -*- coding: utf-8 -*-
"""Verifica deploy GA4 + Consent Mode su righettoimmobiliare.it (post-push)."""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

SITE = "https://righettoimmobiliare.it"
GA_ID = "G-PHEL8KXLBX"
PAGES = [
    "/",
    "/index.html",
    "/agenzia-immobiliare-padova",
    "/zona-limena",
    "/blog-quotazioni-locazioni-omi-istat-padova-2026",
    "/contatti",
]
LLMS = ["/llms.txt", "/ai.json", "/robots.txt"]


def fetch(url: str, timeout: int = 25) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "RighettoGA4Verify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return e.code, body


def main() -> int:
    issues: list[str] = []
    ok: list[str] = []

    # 1) ga-consent.js live
    code, js = fetch(f"{SITE}/js/ga-consent.js?v=1")
    if code != 200:
        issues.append(f"ga-consent.js HTTP {code}")
    else:
        for needle in [
            GA_ID,
            "analytics_storage",
            "denied",
            "rigGaConsentUpdate",
            "gtag('consent', 'default'",
        ]:
            if needle not in js:
                issues.append(f"ga-consent.js manca: {needle}")
        if not issues:
            ok.append("ga-consent.js live OK (Consent Mode v2 + G-PHEL8KXLBX)")

    # 2) Pagine campione
    for path in PAGES:
        code, html = fetch(f"{SITE}{path}")
        if code != 200:
            issues.append(f"{path} HTTP {code}")
            continue
        if "googletagmanager.com/gtag/js?id=" + GA_ID in html:
            issues.append(f"{path}: gtag inline ancora presente (deploy non aggiornato?)")
        has_consent = "ga-consent.js" in html or (
            path in ("/", "/index.html") and "ga-consent.js" in html
        )
        if path in ("/", "/index.html"):
            if "ga-consent.js" not in html:
                issues.append(f"{path}: index senza ga-consent.js (idle loader)")
        elif "ga-consent.js" not in html:
            issues.append(f"{path}: ga-consent.js assente")
        else:
            ok.append(f"{path}: solo ga-consent.js")

    # 3) Catalogo AI
    code, llms = fetch(f"{SITE}/llms.txt")
    if code == 200:
        blog_links = len(re.findall(r"righettoimmobiliare\.it/blog-", llms))
        if blog_links < 100:
            issues.append(f"llms.txt live: solo {blog_links} link blog (attesi ~107)")
        else:
            ok.append(f"llms.txt live: {blog_links} link blog")

    code, ai_raw = fetch(f"{SITE}/ai.json")
    if code == 200:
        try:
            ai = json.loads(ai_raw)
            idx = ai.get("contentIndex", {})
            if idx.get("measurementId") != GA_ID:
                issues.append("ai.json live: measurementId errato")
            elif idx.get("consentMode") != "v2-custom-banner":
                issues.append("ai.json live: consentMode non documentato")
            else:
                ok.append("ai.json live: GA4 + Consent Mode documentati")
        except json.JSONDecodeError:
            issues.append("ai.json live: JSON invalido")

    code, robots = fetch(f"{SITE}/robots.txt")
    if code == 200:
        for bot in ("GPTBot", "ClaudeBot", "Google-Extended", "PerplexityBot"):
            if bot not in robots:
                issues.append(f"robots.txt: {bot} non citato")
        if "Allow" in robots or "allow" in robots.lower():
            ok.append("robots.txt: crawler AI presenti")

    # 4) Simulazione flusso consenso (logica statica)
    sim = {
        "step1_default": "analytics_storage=denied" in js if code == 200 else False,
        "step2_grant": "analytics_storage: prefs.analytics ? 'granted' : 'denied'" in js
        or "analytics ? 'granted'" in js,
        "step3_config": f"gtag('config', GA_ID" in js or f"'config', GA_ID" in js,
        "measurement_id": GA_ID,
        "note": "Eventi GA4 in Realtime richiedono browser con consenso analitici attivo",
    }
    if all([sim["step1_default"], sim["step2_grant"], sim["step3_config"]]):
        ok.append("Simulazione consenso: default denied → update on grant → config OK")
    else:
        issues.append(f"Simulazione consenso incompleta: {sim}")

    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "site": SITE,
        "ok": ok,
        "issues": issues,
        "simulation": sim,
        "pass": len(issues) == 0,
    }
    out = __file__.replace("verify_ga_consent_live.py", "..") + "/data/ga-consent-verify-latest.json"
    from pathlib import Path

    out_path = Path(__file__).resolve().parent.parent / "data" / "ga-consent-verify-latest.json"
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("=== Verifica GA4 + Consent Mode (live) ===\n")
    for line in ok:
        print("OK", line)
    for line in issues:
        print("ERR", line)
    print(f"\nReport: {out_path}")
    print("ESITO:", "PASS" if report["pass"] else "FAIL")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
