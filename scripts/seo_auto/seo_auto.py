#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO automatico settimanale — Righetto Immobiliare.
Skill: TEST-SKILL/skill-seo-auto-weekly.md · Cron: .github/workflows/seo-auto-settimanale.yml

Comandi:
  python3 scripts/seo_auto/seo_auto.py weekly            # ingest → audit → evaluate → select → dashboard → report
  python3 scripts/seo_auto/seo_auto.py ingest|audit|select|evaluate|dashboard|report
  python3 scripts/seo_auto/seo_auto.py apply [--id SEO-...] # applica SOLO interventi approvati in approvals.json
  python3 scripts/seo_auto/seo_auto.py verify             # verifica online gli interventi pubblicati
  python3 scripts/seo_auto/seo_auto.py rollback --id SEO-...

Fonti dati (in ordine): API GSC (secret GSC_SERVICE_ACCOUNT_JSON) → CSV in data/seo-auto/inbox/ →
JSON repo (marcati stale). Nessun dato viene stimato e presentato come reale.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import html as htmllib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEO = ROOT / "data" / "seo-auto"
SNAP_DIR = SEO / "snapshots"
INBOX = SEO / "inbox"
PROPOSALS = SEO / "proposals"
BACKUPS = SEO / "backups"
REPORTS = SEO / "reports"
REGISTRY = SEO / "registry.jsonl"
APPROVALS = SEO / "approvals.json"
CONFIG = SEO / "config.json"
AUDIT_OUT = SEO / "audit-latest.json"
SELECTION_OUT = SEO / "selection-latest.json"
DASHBOARD = SEO / "dashboard.html"
EMAIL_HTML = ROOT / "seo-auto-email.html"
EMAIL_SUBJECT = ROOT / "seo-auto-subject.txt"
SITE = "https://righettoimmobiliare.it"

BRAND_RE = re.compile(r"righetto", re.I)


# ---------------------------------------------------------------- utilità

def load_json(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def save_json(p: Path, data) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cfg() -> dict:
    return load_json(CONFIG, {}) or {}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def cycle_id(d: date | None = None) -> str:
    d = d or date.today()
    y, w, _ = d.isocalendar()
    return f"{y}W{w:02d}"


def log_event(event: dict) -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    rows = read_registry()
    event = {"event_id": f"EV-{len(rows) + 1:05d}", "ts": now_iso(), **event}
    with REGISTRY.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def read_registry() -> list[dict]:
    if not REGISTRY.exists():
        return []
    out = []
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def path_from_url(u: str) -> str:
    u = re.sub(r"^https?://(www\.)?righettoimmobiliare\.it", "", u.strip())
    u = u.split("#")[0].split("?")[0]
    u = re.sub(r"/{2,}", "/", u)
    if u.endswith(".html"):
        u = u[:-5]
    if u in ("", "/index"):
        return "/"
    return u if u.startswith("/") else "/" + u


def file_for_path(p: str) -> Path | None:
    f = ROOT / ("index.html" if p == "/" else p.lstrip("/") + ".html")
    return f if f.exists() else None


def git_last_modified(f: Path) -> str | None:
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(f.relative_to(ROOT))],
                           cwd=ROOT, capture_output=True, text=True, timeout=20)
        return r.stdout.strip() or None
    except Exception:
        return None


def m(clicks, impr, pos=None) -> dict:
    clicks, impr = float(clicks or 0), float(impr or 0)
    return {"clicks": clicks, "impressions": impr,
            "ctr": round(clicks / impr, 4) if impr else 0.0,
            "position": round(float(pos), 2) if pos not in (None, "") else None}


# ---------------------------------------------------------------- INGEST

def _gsc_service():
    raw = os.environ.get("GSC_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        return None, "Secret GSC_SERVICE_ACCOUNT_JSON assente"
    try:
        from google.oauth2 import service_account  # type: ignore
        from google.auth.transport.requests import AuthorizedSession  # type: ignore
    except ImportError:
        return None, "Libreria google-auth non installata (pip install google-auth requests)"
    try:
        info = json.loads(raw)
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
        return AuthorizedSession(creds), None
    except Exception as e:  # credenziali malformate
        return None, f"Credenziali GSC non valide: {e}"


def _gsc_query(sess, site: str, start: str, end: str, dims: list[str], limit=25000) -> list[dict]:
    url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{urllib.request.quote(site, safe='')}/searchAnalytics/query"
    rows, start_row = [], 0
    while True:
        body = {"startDate": start, "endDate": end, "dimensions": dims,
                "rowLimit": limit, "startRow": start_row, "dataState": "final"}
        r = sess.post(url, json=body, timeout=60)
        if r.status_code != 200:
            raise RuntimeError(f"GSC API {r.status_code}: {r.text[:300]}")
        batch = r.json().get("rows", [])
        rows.extend(batch)
        if len(batch) < limit:
            return rows
        start_row += limit


def _gsc_inspect(sess, site: str, urls: list[str], max_n: int) -> dict:
    out = {}
    api = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
    for u in urls[:max_n]:
        try:
            r = sess.post(api, json={"inspectionUrl": u, "siteUrl": site, "languageCode": "it-IT"}, timeout=60)
            if r.status_code != 200:
                out[path_from_url(u)] = {"error": r.status_code}
                continue
            res = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
            out[path_from_url(u)] = {k: res.get(k) for k in ("verdict", "coverageState", "lastCrawlTime", "googleCanonical", "robotsTxtState")}
        except Exception as e:
            out[path_from_url(u)] = {"error": str(e)[:120]}
    return out


def ingest_api(sess, conf: dict) -> dict:
    site = conf.get("gsc_site", "sc-domain:righettoimmobiliare.it")
    lag = int(conf.get("gsc_lag_days", 3))
    end = date.today() - timedelta(days=lag)
    cur_s, prev_e = end - timedelta(days=27), end - timedelta(days=28)
    prev_s = prev_e - timedelta(days=27)
    period = {"current": [cur_s.isoformat(), end.isoformat()], "previous": [prev_s.isoformat(), prev_e.isoformat()]}

    def agg(rows):
        c = sum(r["clicks"] for r in rows)
        i = sum(r["impressions"] for r in rows)
        p = sum(r["position"] * r["impressions"] for r in rows) / i if i else None
        return m(c, i, p)

    pages: dict[str, dict] = {}
    for label, (s, e) in period.items():
        for r in _gsc_query(sess, site, s, e, ["page"]):
            p = path_from_url(r["keys"][0])
            pages.setdefault(p, {})[label] = m(r["clicks"], r["impressions"], r["position"])
        qrows = _gsc_query(sess, site, s, e, ["page", "query"])
        by_page: dict[str, list] = {}
        for r in qrows:
            by_page.setdefault(path_from_url(r["keys"][0]), []).append(r)
        for p, rows in by_page.items():
            nb = [r for r in rows if not BRAND_RE.search(r["keys"][1])]
            pages.setdefault(p, {})[f"nonbrand_{label}"] = agg(nb)
            if label == "current":
                top = sorted(rows, key=lambda r: -r["impressions"])[:8]
                pages[p]["top_queries"] = [{"q": r["keys"][1], **m(r["clicks"], r["impressions"], r["position"])} for r in top]
    daily = [{"date": r["keys"][0], **m(r["clicks"], r["impressions"], r["position"])}
             for r in _gsc_query(sess, site, prev_s.isoformat(), end.isoformat(), ["date"])]
    site_tot = {k: agg([{"clicks": d["clicks"], "impressions": d["impressions"], "position": d["position"] or 0}
                        for d in daily if period[k][0] <= d["date"] <= period[k][1]]) for k in period}
    sitemap_urls = re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
    inspect = _gsc_inspect(sess, site, sitemap_urls, int(conf.get("url_inspection_max", 60)))
    return {"source": "gsc_api", "stale": False, "data_end_date": end.isoformat(), "period": period,
            "site": site_tot, "pages": pages, "daily": daily, "index_status": inspect, "limitations": [
                "GSC anonimizza query rare: somma query < totale pagina.",
                "Posizione media pesata per impressioni; non è un ranking puntuale."]}


def _num(v: str) -> float:
    v = (v or "").strip().replace("%", "").replace("\u00a0", "")
    if not v:
        return 0.0
    if "," in v and "." in v:
        v = v.replace(".", "").replace(",", ".")
    else:
        v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return 0.0


def ingest_csv() -> dict | None:
    """Export GSC UI: Prestazioni → (Confronta 28 gg) → Esporta → CSV «Pagine». File in data/seo-auto/inbox/."""
    files = sorted(INBOX.glob("*.csv"), key=lambda f: f.stat().st_mtime, reverse=True)
    page_file = next((f for f in files if re.search(r"pagin|page", f.name, re.I)), None)
    if not page_file:
        return None
    with page_file.open(encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    if len(rows) < 2:
        return None
    head = [h.lower() for h in rows[0]]
    idx = {k: [i for i, h in enumerate(head) if re.search(pat, h)] for k, pat in
           {"clicks": r"clic", "impr": r"impression", "pos": r"posizion|position"}.items()}
    pages = {}
    for r in rows[1:]:
        if not r or not r[0].startswith("http"):
            continue
        p = path_from_url(r[0])
        get = lambda k, n: _num(r[idx[k][n]]) if len(idx[k]) > n else None
        entry = {"current": m(get("clicks", 0), get("impr", 0), get("pos", 0))}
        if len(idx["clicks"]) > 1:
            entry["previous"] = m(get("clicks", 1), get("impr", 1), get("pos", 1))
        pages[p] = entry
    mtime = date.fromtimestamp(page_file.stat().st_mtime).isoformat()
    tot = lambda k: m(sum(v[k]["clicks"] for v in pages.values() if k in v),
                      sum(v[k]["impressions"] for v in pages.values() if k in v))
    return {"source": "gsc_csv", "stale": False, "source_file": page_file.name, "data_end_date": mtime,
            "period": {"current": None, "previous": None}, "site": {"current": tot("current"),
            "previous": tot("previous") if any("previous" in v for v in pages.values()) else None},
            "pages": pages, "daily": [], "index_status": {},
            "limitations": ["Export manuale: niente query per pagina né dati giornalieri, niente brand/non-brand."]}


def ingest_repo_fallback() -> dict:
    kp = load_json(ROOT / "data" / "gsc-keywords-priority.json", {}) or {}
    s = kp.get("summary_28d", {})
    pages = {}
    for key in ("pages_winners", "pages_refresh_priority"):
        for p in kp.get(key, []):
            pages[path_from_url(p["url"])] = {"current": m(p.get("clicks"), p.get("impressions"))}
    return {"source": "repo_json_stale", "stale": True,
            "data_end_date": s.get("period_end"), "period": {"current": [s.get("period_start"), s.get("period_end")], "previous": None},
            "site": {"current": m(s.get("clicks"), s.get("impressions"), s.get("avg_position")), "previous": None},
            "pages": pages, "daily": [], "index_status": {},
            "limitations": [
                f"Dati pagina fermi al {s.get('period_end')}: nessun accesso API né export CSV recente.",
                "Solo 7 URL con metriche: impossibile un ranking affidabile su tutto il sito.",
                "Senza periodo precedente non si misurano cali né effetti degli interventi."]}


def cmd_ingest() -> dict:
    conf = cfg()
    errors = []
    snap = None
    sess, err = _gsc_service()
    if sess:
        try:
            snap = ingest_api(sess, conf)
        except Exception as e:
            errors.append(f"API GSC fallita: {e}")
    elif err:
        errors.append(err)
    if snap is None:
        snap = ingest_csv()
        if snap is None:
            errors.append("Nessun CSV in data/seo-auto/inbox/")
            snap = ingest_repo_fallback()
    ga4_id = os.environ.get("GA4_PROPERTY_ID", "").strip()
    snap["ga4"] = {"status": "non_configurato" if not ga4_id else "configurato_non_implementato",
                   "note": "GA4 Data API: aggiungere service account come Visualizzatore sulla proprietà."}
    snap["snapshot_date"] = date.today().isoformat()
    snap["ingest_errors"] = errors
    save_json(SNAP_DIR / f"{snap['snapshot_date']}.json", snap)
    print(f"ingest: fonte={snap['source']} stale={snap['stale']} pagine={len(snap['pages'])}")
    for e in errors:
        print(f"  ! {e}")
    return snap


def latest_snapshot() -> dict:
    snaps = sorted(SNAP_DIR.glob("*.json"))
    return load_json(snaps[-1]) if snaps else cmd_ingest()


# ---------------------------------------------------------------- AUDIT ON-PAGE (dato reale dal codice)

def _attr(tag_html: str, name: str) -> str | None:
    mm = re.search(rf'{name}\s*=\s*"([^"]*)"', tag_html, re.I) or re.search(rf"{name}\s*=\s*'([^']*)'", tag_html, re.I)
    return htmllib.unescape(mm.group(1)).strip() if mm else None


def page_facts(f: Path) -> dict:
    t = f.read_text(encoding="utf-8", errors="ignore")
    title_m = re.search(r"<title[^>]*>(.*?)</title>", t, re.S | re.I)
    meta_tag = next((x for x in re.findall(r"<meta[^>]+>", t, re.I) if re.search(r'name\s*=\s*["\']description["\']', x, re.I)), "")
    canon_tag = next((x for x in re.findall(r"<link[^>]+>", t, re.I) if re.search(r'rel\s*=\s*["\']canonical["\']', x, re.I)), "")
    robots_tag = next((x for x in re.findall(r"<meta[^>]+>", t, re.I) if re.search(r'name\s*=\s*["\']robots["\']', x, re.I)), "")
    body = re.sub(r"<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", t, flags=re.S | re.I)
    text = re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", body))).strip()
    return {
        "title": htmllib.unescape(re.sub(r"\s+", " ", title_m.group(1))).strip() if title_m else None,
        "meta": _attr(meta_tag, "content"),
        "canonical": _attr(canon_tag, "href"),
        "noindex": bool(robots_tag and "noindex" in robots_tag.lower()),
        "h1": len(re.findall(r"<h1[\s>]", t, re.I)),
        "h2": len(re.findall(r"<h2[\s>]", t, re.I)),
        "words": len(text.split()),
        "faq_schema": '"FAQPage"' in t,
        "forms": len(re.findall(r"<form[\s>]", t, re.I)),
        "jsonld": len(re.findall(r'application/ld\+json', t, re.I)),
        "links_out": sorted({path_from_url(h) for h in re.findall(r'href="([^"#:]+?)"', t)
                             if not h.startswith(("http", "mailto", "tel", "javascript", "css/", "js/", "img/", "data/", "fonts/", "#"))}),
    }


def classify(p: str) -> str:
    c = cfg().get("business_tiers", {})
    for tier, pats in c.items():
        if any(re.search(pt, p) for pt in pats):
            return tier
    return "contenuto"


def cmd_audit() -> dict:
    locs = [path_from_url(u) for u in re.findall(r"<loc>([^<]+)</loc>", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))]
    all_html = [f for f in ROOT.glob("*.html") if not f.name.startswith(("admin", "google"))]
    facts = {}
    for f in all_html:
        facts[path_from_url("/" + f.name)] = page_facts(f)
    inbound: dict[str, set] = {}
    for src, fx in facts.items():
        for dst in fx["links_out"]:
            if dst != src:
                inbound.setdefault(dst, set()).add(src)
    pages = {}
    for p in locs:
        f = file_for_path(p)
        if not f:
            pages[p] = {"missing_file": True}
            continue
        fx = facts.get(p) or page_facts(f)
        issues = []
        tl = len(fx["title"] or "")
        ml = len(fx["meta"] or "")
        notes = []
        if not fx["title"]:
            issues.append("title_mancante")
        elif tl > 70:
            issues.append(f"title_lungo_{tl}")
        elif tl > 60:
            notes.append(f"title_61_70_{tl}")
        elif tl < 25:
            issues.append(f"title_corto_{tl}")
        if fx["title"] and re.search(r"…|\.\.\.$", fx["title"]):
            issues.append("title_troncato")
        if not fx["meta"]:
            issues.append("meta_mancante")
        elif ml > 160:
            issues.append(f"meta_lunga_{ml}")
        elif ml < 70:
            issues.append(f"meta_corta_{ml}")
        if fx["h1"] != 1:
            issues.append(f"h1_{fx['h1']}")
        exp_canon = SITE + ("/" if p == "/" else p)
        if fx["canonical"] and fx["canonical"].rstrip("/") != exp_canon.rstrip("/"):
            issues.append("sitemap_canonical_altrove")
        if not fx["canonical"]:
            issues.append("canonical_mancante")
        if fx["noindex"]:
            issues.append("sitemap_noindex")
        if p in cfg().get("template_paths", []):
            issues.append("sitemap_template_senza_contenuto")
        pages[p] = {**{k: v for k, v in fx.items() if k != "links_out"},
                    "tier": classify(p), "inbound": len(inbound.get(p, ())),
                    "last_modified": git_last_modified(f), "issues": issues, "notes": notes}
    titles: dict[str, list] = {}
    for p, v in pages.items():
        if v.get("title"):
            titles.setdefault(v["title"].lower(), []).append(p)
    for t, ps in titles.items():
        if len(ps) > 1:
            for p in ps:
                pages[p]["issues"].append("title_duplicato")
    out = {"date": date.today().isoformat(), "pages_in_sitemap": len(locs), "pages": pages}
    save_json(AUDIT_OUT, out)
    n_iss = sum(1 for v in pages.values() if v.get("issues"))
    print(f"audit: {len(locs)} URL sitemap, {n_iss} con almeno un problema on-page")
    return out


# ---------------------------------------------------------------- SELEZIONE (punteggio trasparente)

BENCH_CTR = {1: .28, 2: .15, 3: .10, 4: .07, 5: .05, 6: .04, 7: .03, 8: .025, 9: .02, 10: .018}


def expected_ctr(pos: float | None) -> float | None:
    if not pos:
        return None
    if pos <= 10:
        return BENCH_CTR[max(1, int(round(pos)))]
    return .01 if pos <= 20 else .003


def last_content_refresh(p: str) -> str | None:
    dates = [e["ts"][:10] for e in read_registry() if e.get("url") == p and e.get("type") == "published"]
    kp = load_json(ROOT / "data" / "gsc-keywords-priority.json", {}) or {}
    dates += [r["date"] for r in kp.get("refreshed_this_week", []) if path_from_url(r["url"]) == p and r.get("date")]
    return max(dates) if dates else None


def cooldown_active(p: str, snap: dict, conf: dict) -> bool:
    """Blocca un nuovo intervento di contenuto se l'ultimo refresh non ha ancora 28 gg di dati GSC dopo di sé."""
    ref = last_content_refresh(p)
    if not ref:
        return False
    if (date.today() - date.fromisoformat(ref)).days < int(conf.get("cooldown_days", 28)):
        return True
    end = snap.get("data_end_date")
    return bool(snap.get("stale")) or not end or end < (date.fromisoformat(ref) + timedelta(days=28)).isoformat()


def score_page(p: str, a: dict, g: dict | None, stale: bool, conf: dict) -> tuple[float, list[str], dict]:
    w = conf.get("weights", {})
    reasons, parts = [], {}
    tier_mult = conf.get("tier_multiplier", {}).get(a.get("tier", "contenuto"), 1.0)
    if g and "current" in g:
        cur = g.get("nonbrand_current") or g["current"]
        imp, ctr, pos = cur["impressions"], cur["ctr"], cur.get("position")
        min_imp = int(conf.get("min_impressions_ctr", 100))
        exp = expected_ctr(pos)
        if imp >= min_imp and exp and ctr < exp * .7:
            missed = (exp - ctr) * imp
            parts["ctr_gap"] = round(min(missed, 60) * w.get("ctr_gap", 1.0), 1)
            reasons.append(f"CTR {ctr:.1%} vs atteso ~{exp:.0%} a pos. {pos:.1f} (benchmark stima) su {int(imp)} impr.: ~{missed:.0f} clic mancati")
        elif imp >= 30 and pos is None and ctr == 0:
            parts["zero_click"] = round(min(imp / 10, 20) * w.get("zero_click", 1.0), 1)
            reasons.append(f"{int(imp)} impressioni e 0 clic (posizione non disponibile)")
        if pos and 4 <= pos <= 15 and imp >= 30:
            parts["striking"] = round(10 * w.get("striking_distance", 1.0), 1)
            reasons.append(f"posizione media {pos:.1f}: margine verso top 3")
        prev = g.get("previous")
        if prev and prev["clicks"] >= 5:
            d = g["current"]["clicks"] - prev["clicks"]
            if d <= -max(5, prev["clicks"] * .2):
                parts["decline"] = round(min(-d, 40) * w.get("decline", 1.0), 1)
                reasons.append(f"clic {int(prev['clicks'])}→{int(g['current']['clicks'])} vs 28 gg precedenti")
        if stale and parts:
            for k in parts:
                parts[k] = round(parts[k] * .5, 1)
            reasons.append("dato GSC non aggiornato: peso dimezzato")
    sitemap_iss = [i for i in a.get("issues", []) if i.startswith("sitemap_")]
    tech = [i for i in a.get("issues", []) if not i.startswith(("meta_corta", "sitemap_"))]
    if sitemap_iss:
        parts["sitemap"] = round(12 * w.get("sitemap", 1.0), 1)
        reasons.append("sitemap incoerente: " + ", ".join(sitemap_iss) + " (Google riceve segnali contraddittori)")
    if tech:
        parts["tecnico"] = round(min(len(tech) * 5, 15) * w.get("technical", 1.0), 1)
        reasons.append("on-page: " + ", ".join(tech))
    under = int(conf.get("underlinked_threshold", 10))
    if a.get("tier") in ("owner_conversione", "pillar") and a.get("inbound", 99) < under:
        parts["underlinked"] = round((under - a["inbound"]) * 1.5 * w.get("internal_links", 1.0), 1)
        reasons.append(f"solo {a['inbound']} pagine interne linkano questa URL (soglia {under})")
    base = sum(parts.values())
    return round(base * tier_mult, 1), reasons, {**parts, "tier_mult": tier_mult}


def cmd_select() -> dict:
    conf = cfg()
    snap = latest_snapshot()
    audit = load_json(AUDIT_OUT) or cmd_audit()
    cands = []
    for p, a in audit["pages"].items():
        if a.get("missing_file"):
            continue
        g = snap["pages"].get(p)
        score, reasons, parts = score_page(p, a, g, snap.get("stale", True), conf)
        if score <= 0:
            continue
        only_technical = set(parts) <= {"sitemap", "tecnico", "tier_mult"}
        cd = cooldown_active(p, snap, conf) and not only_technical
        if cd:
            reasons.append(f"cooldown: ultimo refresh {last_content_refresh(p)} senza 28 gg di dati GSC successivi")
        cands.append({"url": p, "file": file_for_path(p).name, "tier": a["tier"], "score": score,
                      "score_parts": parts, "reasons": reasons, "gsc": g, "cooldown": cd,
                      "last_modified": a.get("last_modified"), "inbound": a.get("inbound"),
                      "title": a.get("title"), "meta": a.get("meta"), "issues": a.get("issues")})
    cands.sort(key=lambda c: -c["score"])
    min_score = float(conf.get("min_score", 8))
    picked = [c for c in cands if c["score"] >= min_score and not c["cooldown"]][: int(conf.get("max_pages", 10))]
    cyc = cycle_id()
    for c in picked:
        slug = "home" if c["url"] == "/" else c["url"].strip("/")
        c["intervention_id"] = f"SEO-{cyc}-{slug}"
    out = {"cycle": cyc, "date": date.today().isoformat(), "data_source": snap["source"], "stale": snap.get("stale"),
           "limitations": snap.get("limitations", []), "candidates_total": len(cands),
           "selected": picked,
           "excluded_cooldown": [{"url": c["url"], "score": c["score"], "reasons": c["reasons"]} for c in cands if c["cooldown"]][:20],
           "below_threshold": [{"url": c["url"], "score": c["score"]} for c in cands if c["score"] < min_score][:15]}
    save_json(SELECTION_OUT, out)
    save_json(PROPOSALS / f"{cyc}-selection.json", out)
    already = {e.get("intervention_id") for e in read_registry() if e.get("type") == "selected"}
    for c in picked:
        if c["intervention_id"] not in already:
            log_event({"type": "selected", "intervention_id": c["intervention_id"], "url": c["url"], "cycle": cyc,
                       "score": c["score"], "reasons": c["reasons"], "metrics_before": c["gsc"], "data_source": snap["source"]})
    print(f"select: {len(picked)} pagine selezionate su {len(cands)} candidate (soglia {min_score})")
    return out


# ---------------------------------------------------------------- APPLY / VERIFY / ROLLBACK

def _apply_ops(t: str, ops: list[dict]) -> str:
    for op in ops:
        kind = op["op"]
        if kind == "set_title":
            new, n = re.subn(r"<title[^>]*>.*?</title>", f"<title>{htmllib.escape(op['value'], quote=False)}</title>", t, count=1, flags=re.S | re.I)
            if n != 1:
                raise ValueError("title non trovato")
            t = new
            if op.get("sync_social", True):
                for prop in ("og:title", "twitter:title"):
                    t = re.sub(rf'(<meta[^>]+(?:property|name)="{prop}"[^>]+content=")[^"]*(")',
                               lambda mm: mm.group(1) + htmllib.escape(op["value"]) + mm.group(2), t, count=1)
        elif kind == "set_meta":
            pat = r'(<meta[^>]+name="description"[^>]+content=")[^"]*(")'
            if not re.search(pat, t):
                raise ValueError("meta description non trovata")
            t = re.sub(pat, lambda mm: mm.group(1) + htmllib.escape(op["value"]) + mm.group(2), t, count=1)
            if op.get("sync_social", True):
                for prop in ("og:description", "twitter:description"):
                    t = re.sub(rf'(<meta[^>]+(?:property|name)="{prop}"[^>]+content=")[^"]*(")',
                               lambda mm: mm.group(1) + htmllib.escape(op["value"]) + mm.group(2), t, count=1)
        elif kind in ("replace", "insert_before", "insert_after"):
            find = op["find"]
            if t.count(find) != 1:
                raise ValueError(f"ancora non univoca ({t.count(find)}x): {find[:60]}")
            rep = {"replace": op.get("html", ""), "insert_before": op["html"] + find, "insert_after": find + op["html"]}[kind]
            t = t.replace(find, rep, 1)
        else:
            raise ValueError(f"op sconosciuta {kind}")
    return t


def _invariants(before: str, after: str) -> list[str]:
    errs = []
    fb, fa = page_facts_text(before), page_facts_text(after)
    for k in ("canonical", "forms", "jsonld", "h1"):
        if fb[k] != fa[k]:
            errs.append(f"{k} cambiato: {fb[k]} → {fa[k]}")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', after, re.S):
        try:
            json.loads(block)
        except json.JSONDecodeError:
            errs.append("JSON-LD non valido dopo la modifica")
    return errs


def page_facts_text(t: str) -> dict:
    tmp = SEO / ".tmp.html"
    tmp.write_text(t, encoding="utf-8")
    fx = page_facts(tmp)
    tmp.unlink()
    return fx


def cmd_apply(only_id: str | None = None) -> list[str]:
    approvals = load_json(APPROVALS, {}) or {}
    published = {e["intervention_id"] for e in read_registry() if e.get("type") == "published"}
    done = []
    for iid, ap in approvals.items():
        if only_id and iid != only_id:
            continue
        if not ap.get("approved") or iid in published or not ap.get("ops"):
            continue
        f = ROOT / ap["file"]
        is_xml = f.suffix == ".xml"
        before = f.read_text(encoding="utf-8")
        try:
            after = _apply_ops(before, ap["ops"])
        except ValueError as e:
            log_event({"type": "apply_failed", "intervention_id": iid, "url": ap["url"], "error": str(e)})
            print(f"  ✗ {iid}: {e}")
            continue
        if is_xml:
            import xml.etree.ElementTree as ET
            try:
                ET.fromstring(after.encode("utf-8"))
                errs = []
            except ET.ParseError as e:
                errs = [f"XML non valido: {e}"]
        else:
            errs = _invariants(before, after)
        if errs:
            log_event({"type": "apply_blocked", "intervention_id": iid, "url": ap["url"], "error": errs})
            print(f"  ✗ {iid} bloccato: {errs}")
            continue
        bdir = BACKUPS / iid
        bdir.mkdir(parents=True, exist_ok=True)
        (bdir / f"{f.name}.before").write_text(before, encoding="utf-8")
        (bdir / f"{f.name}.after").write_text(after, encoding="utf-8")
        diff = "".join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), f"a/{f.name}", f"b/{f.name}"))
        (bdir / "diff.patch").write_text(diff, encoding="utf-8")
        f.write_text(after, encoding="utf-8")
        if not is_xml:
            val = subprocess.run(["node", "scripts/validate-page.js", "--file", f.name], cwd=ROOT, capture_output=True, text=True)
            if not ("Tutto OK" in val.stdout or val.returncode == 0):
                shutil.copy2(bdir / f"{f.name}.before", f)
                log_event({"type": "apply_reverted", "intervention_id": iid, "url": ap["url"], "error": val.stdout[-600:]})
                print(f"  ✗ {iid}: validate-page KO — ripristinato")
                continue
        fx = page_facts(f) if not is_xml else {"title": None, "meta": None}
        log_event({"type": "published", "intervention_id": iid, "url": ap["url"], "file": f.name,
                   "live_path": "/sitemap.xml" if is_xml else path_from_url("/" + f.name),
                   "verify_absent": ap.get("verify_absent", []), "verify_present": ap.get("verify_present", []),
                   "approved_by": ap.get("approved_by"), "approved_on": ap.get("approved_on"),
                   "summary": ap.get("summary"), "rationale": ap.get("rationale"),
                   "title_after": fx["title"], "meta_after": fx["meta"],
                   "backup": str(bdir.relative_to(ROOT)), "note": "pubblicato nel repo — verifica online con «verify» dopo deploy Pages"})
        done.append(iid)
        print(f"  ✓ {iid} applicato su {f.name}")
    return done


def _fetch(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "RighettoSEOAuto/1.0", "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


def cmd_verify() -> None:
    reg = read_registry()
    verified = {e["intervention_id"] for e in reg if e.get("type") == "live_verified"}
    last_fail = {x["intervention_id"]: x.get("checks") for x in reg if x.get("type") == "live_check_failed"}
    for e in [x for x in reg if x.get("type") == "published" and x["intervention_id"] not in verified]:
        dirty = subprocess.run(["git", "status", "--porcelain", "--", e["file"]], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if dirty:
            print(f"  … {e['intervention_id']} {e['file']} non ancora committato — verifica dopo il deploy")
            continue
        lp = e.get("live_path") or e["url"]
        url = SITE + ("/" if lp == "/" else lp)
        code, body = _fetch(url + f"?v={int(datetime.now().timestamp())}")
        checks = []
        if e.get("title_after"):
            tm = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
            checks.append(("title", bool(tm) and htmllib.unescape(tm.group(1)).strip() == e["title_after"]))
        if e.get("meta_after"):
            checks.append(("meta", htmllib.escape(e["meta_after"]) in body or e["meta_after"] in body))
        checks += [(f"assente:{s[:40]}", s not in body) for s in e.get("verify_absent", [])]
        checks += [(f"presente:{s[:40]}", s in body) for s in e.get("verify_present", [])]
        ok = code == 200 and all(c[1] for c in checks)
        if not ok and last_fail.get(e["intervention_id"]) == [list(c) for c in checks]:
            continue
        log_event({"type": "live_verified" if ok else "live_check_failed", "intervention_id": e["intervention_id"],
                   "url": e["url"], "live_path": lp, "http": code, "checks": checks})
        print(f"  {'✓' if ok else '…'} {e['intervention_id']} {lp} HTTP {code} {'OK' if ok else [c[0] for c in checks if not c[1]]}")


def _carry_external_edits(base_after: str, current: str, rebuilt: str) -> str | None:
    """Riporta su `rebuilt` le modifiche fatte al file dopo l'ultimo intervento SEO (es. nuovi blog in sitemap)."""
    if base_after == current:
        return rebuilt
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        (tdp / "a").write_text(base_after, encoding="utf-8")
        (tdp / "b").write_text(current, encoding="utf-8")
        (tdp / "r").write_text(rebuilt, encoding="utf-8")
        diff = subprocess.run(["diff", "-u", "a", "b"], cwd=td, capture_output=True, text=True).stdout
        (tdp / "d.patch").write_text(diff, encoding="utf-8")
        res = subprocess.run(["patch", "-s", "--no-backup-if-mismatch", "-r", "-", "r", "d.patch"], cwd=td, capture_output=True, text=True)
        return (tdp / "r").read_text(encoding="utf-8") if res.returncode == 0 else None


def cmd_rollback(iid: str) -> None:
    bdir = BACKUPS / iid
    befores = list(bdir.glob("*.before"))
    if not befores:
        sys.exit(f"Nessun backup per {iid}")
    target = ROOT / befores[0].name.replace(".before", "")
    reg = read_registry()
    rolled = {e["intervention_id"] for e in reg if e.get("type") == "rollback"}
    ids = [e["intervention_id"] for e in reg if e.get("type") == "published"
           and e.get("file") == target.name and e["intervention_id"] not in rolled]
    if iid not in ids:
        sys.exit(f"{iid} non risulta pubblicato (o già annullato) su {target.name}")
    approvals = load_json(APPROVALS, {}) or {}
    later = ids[ids.index(iid) + 1:]
    try:
        rebuilt = befores[0].read_text(encoding="utf-8")
        for lid in later:
            rebuilt = _apply_ops(rebuilt, approvals[lid]["ops"])
    except (KeyError, ValueError) as e:
        sys.exit(f"Rollback {iid} non ricostruibile ({e}): file invariato. Copia di riferimento: {befores[0]}")
    last_after = next((BACKUPS / ids[-1]).glob("*.after")).read_text(encoding="utf-8")
    final = _carry_external_edits(last_after, target.read_text(encoding="utf-8"), rebuilt)
    if final is None:
        sys.exit(f"Rollback {iid}: modifiche successive al file in conflitto — file invariato, intervenire a mano.")
    target.write_text(final, encoding="utf-8")
    log_event({"type": "rollback", "intervention_id": iid, "file": target.name, "reapplied": later})
    print(f"Ripristinato {target.name} da {iid} (riapplicati: {later or 'nessuno'})")


# ---------------------------------------------------------------- VALUTAZIONE

def cmd_evaluate() -> list[dict]:
    reg = read_registry()
    snaps = [load_json(f) for f in sorted(SNAP_DIR.glob("*.json"))]
    real = [s for s in snaps if s and not s.get("stale") and s.get("period", {}).get("current")]
    results = []
    evaluated_final = {e["intervention_id"] for e in reg if e.get("type") == "evaluated" and e.get("final")}
    for e in [x for x in reg if x.get("type") == "published" and x["intervention_id"] not in evaluated_final]:
        pub = date.fromisoformat(e["ts"][:10])
        before = next((s for s in reversed(real) if s["period"]["current"][1] < pub.isoformat()), None)
        after = next((s for s in real if s["period"]["current"][0] > (pub + timedelta(days=3)).isoformat()), None)
        if not before or not after:
            verdict, detail = "dati_insufficienti", "Servono snapshot API reali prima e ≥28 gg dopo la pubblicazione."
            final = False
        else:
            b = before["pages"].get(e["url"], {}).get("current")
            a = after["pages"].get(e["url"], {}).get("current")
            sb, sa = before["site"]["current"], after["site"]["current"]
            if not b or not a or max(b["impressions"], a["impressions"]) < 100:
                verdict, detail, final = "dati_insufficienti", "Meno di 100 impressioni nelle finestre confrontate.", True
            else:
                site_ratio = (sa["clicks"] / sb["clicks"]) if sb["clicks"] else 1
                page_ratio = (a["clicks"] / b["clicks"]) if b["clicks"] else (2 if a["clicks"] else 1)
                rel = page_ratio / site_ratio if site_ratio else page_ratio
                ctr_d = a["ctr"] - b["ctr"]
                if rel >= 1.2 and ctr_d >= 0:
                    verdict = "miglioramento_osservato"
                elif rel <= 0.8 and ctr_d < 0:
                    verdict = "peggioramento_osservato"
                else:
                    verdict = "stabile"
                detail = (f"clic {b['clicks']:.0f}→{a['clicks']:.0f}, CTR {b['ctr']:.1%}→{a['ctr']:.1%}, "
                          f"pos {b.get('position')}→{a.get('position')}; sito ×{site_ratio:.2f}, pagina relativa ×{rel:.2f}")
                final = True
        r = {"intervention_id": e["intervention_id"], "url": e["url"], "verdict": verdict, "detail": detail, "final": final}
        results.append(r)
        last = [x for x in reg if x.get("type") == "evaluated" and x["intervention_id"] == e["intervention_id"]]
        if not last or last[-1].get("verdict") != verdict or last[-1].get("detail") != detail:
            log_event({"type": "evaluated", **r})
    print(f"evaluate: {len(results)} interventi valutati")
    return results


# ---------------------------------------------------------------- DASHBOARD + REPORT

def _svg_line(points: list[tuple[str, float, bool]], annotations: list[tuple[str, str]], title: str, w=640, h=220) -> str:
    if not points:
        return f'<figure><figcaption>{htmllib.escape(title)} — nessun dato reale disponibile</figcaption></figure>'
    xs = sorted({p[0] for p in points} | {a[0] for a in annotations})
    maxv = max(p[1] for p in points) or 1
    px = lambda d: 40 + (xs.index(d) / max(1, len(xs) - 1)) * (w - 60)
    py = lambda v: h - 30 - (v / maxv) * (h - 60)
    path = " ".join(f"{'M' if i == 0 else 'L'}{px(d):.1f},{py(v):.1f}" for i, (d, v, _) in enumerate(points))
    dots = "".join(f'<circle cx="{px(d):.1f}" cy="{py(v):.1f}" r="4" fill="{"#9aa5b1" if stale else "#2C4A6E"}"><title>{d}: {v:.0f}{" (dato non aggiornato)" if stale else ""}</title></circle>' for d, v, stale in points)
    ann = "".join(f'<line x1="{px(d):.1f}" y1="20" x2="{px(d):.1f}" y2="{h - 30}" stroke="#C65A1E" stroke-dasharray="4 3"/><text x="{px(d) + 3:.1f}" y="30" font-size="9" fill="#C65A1E">{htmllib.escape(lbl)}</text>' for d, lbl in annotations)
    labels = "".join(f'<text x="{px(d):.1f}" y="{h - 12}" font-size="9" text-anchor="middle" fill="#6B7A8D">{d[5:]}</text>' for d in xs)
    return (f'<figure><svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{htmllib.escape(title)}">'
            f'<text x="40" y="14" font-size="11" font-weight="700" fill="#152435">{htmllib.escape(title)} (max {maxv:.0f})</text>'
            f'<path d="{path}" fill="none" stroke="#2C4A6E" stroke-width="2"/>{dots}{ann}{labels}</svg>'
            f'<figcaption>Punti grigi = dato non aggiornato/manuale · linee arancioni = interventi pubblicati</figcaption></figure>')


def _series() -> tuple[list, list, list]:
    clicks, impr = [], []
    seen = set()
    for f in sorted(SNAP_DIR.glob("*.json")):
        s = load_json(f)
        end = s.get("data_end_date")
        if not end or end in seen or not s.get("site", {}).get("current"):
            continue
        seen.add(end)
        clicks.append((end, s["site"]["current"]["clicks"], bool(s.get("stale"))))
        impr.append((end, s["site"]["current"]["impressions"], bool(s.get("stale"))))
    ann = [(e["ts"][:10], e["intervention_id"][-2:]) for e in read_registry() if e.get("type") == "published"]
    return clicks, impr, ann


def _interventions_table() -> str:
    reg = read_registry()
    ids = []
    for e in reg:
        if e.get("intervention_id") and e["intervention_id"] not in ids:
            ids.append(e["intervention_id"])
    rows = []
    for iid in ids:
        ev = [e for e in reg if e.get("intervention_id") == iid]
        state = ev[-1]["type"]
        pub = next((e["ts"][:10] for e in ev if e["type"] == "published"), "—")
        verdict = next((e["verdict"] for e in reversed(ev) if e["type"] == "evaluated"), "—")
        summ = next((e.get("summary") for e in ev if e.get("summary")), "") or "; ".join(ev[0].get("reasons", [])[:2])
        rows.append(f"<tr><td>{iid}</td><td>{htmllib.escape(ev[0]['url'])}</td><td>{state}</td><td>{pub}</td><td>{verdict}</td><td>{htmllib.escape(summ)}</td></tr>")
    return ("<table><thead><tr><th>ID</th><th>URL</th><th>Stato</th><th>Pubblicato</th><th>Esito</th><th>Intervento</th></tr></thead><tbody>"
            + "".join(rows) + "</tbody></table>") if rows else "<p>Nessun intervento registrato.</p>"


def cmd_dashboard() -> None:
    sel = load_json(SELECTION_OUT, {}) or {}
    clicks, impr, ann = _series()
    snap = latest_snapshot()
    warn = ""
    if snap.get("stale"):
        warn = ('<p class="warn"><strong>Attenzione:</strong> dati Search Console non aggiornati (fonte: '
                f'{snap["source"]}, fine periodo {snap.get("data_end_date")}). I grafici non mostrano l’andamento reale recente.</p>')
    html_out = f"""<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">
<meta name="robots" content="noindex, nofollow"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard SEO automatico — Righetto</title>
<style>body{{font-family:Arial,sans-serif;color:#152435;max-width:960px;margin:0 auto;padding:16px;line-height:1.5}}
table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{border:1px solid #d8dee6;padding:6px;text-align:left;vertical-align:top}}
th{{background:#eef2f6}}.warn{{background:#fff4e5;border-left:4px solid #C65A1E;padding:8px}}figure{{margin:16px 0}}figcaption{{font-size:12px;color:#6B7A8D}}</style>
</head><body><h1>SEO automatico — ciclo {sel.get('cycle', '—')}</h1>
<p>Aggiornato: {now_iso()} · Fonte dati: <strong>{snap['source']}</strong></p>{warn}
<h2>Andamento sito (28 gg per snapshot)</h2>{_svg_line(clicks, ann, 'Clic organici')}{_svg_line(impr, ann, 'Impressioni')}
<h2>Pagine selezionate</h2><table><thead><tr><th>ID</th><th>URL</th><th>Punteggio</th><th>Motivi</th></tr></thead><tbody>
{''.join(f"<tr><td>{c['intervention_id']}</td><td>{c['url']}</td><td>{c['score']}</td><td>{htmllib.escape('; '.join(c['reasons']))}</td></tr>" for c in sel.get('selected', []))}
</tbody></table><h2>Registro interventi</h2>{_interventions_table()}
<h2>Limiti dei dati</h2><ul>{''.join(f'<li>{htmllib.escape(x)}</li>' for x in snap.get('limitations', []) + snap.get('ingest_errors', []))}</ul>
</body></html>"""
    DASHBOARD.write_text(html_out, encoding="utf-8")
    print(f"dashboard: {DASHBOARD.relative_to(ROOT)}")


def cmd_report(evals: list[dict] | None = None) -> None:
    sel = load_json(SELECTION_OUT, {}) or {}
    snap = latest_snapshot()
    audit = load_json(AUDIT_OUT, {}) or {}
    approvals = load_json(APPROVALS, {}) or {}
    reg = read_registry()
    evals = evals if evals is not None else []
    s = snap.get("site", {})
    cur, prev = s.get("current") or {}, s.get("previous")
    stale = snap.get("stale")
    lines = [f"# Report SEO automatico — ciclo {sel.get('cycle')} ({date.today().isoformat()})", "",
             "## A. Fonte e qualità dei dati",
             f"- Fonte: **{snap['source']}**{' — DATI NON AGGIORNATI' if stale else ''} (fine periodo {snap.get('data_end_date')})"]
    lines += [f"- Limite: {x}" for x in snap.get("limitations", []) + snap.get("ingest_errors", [])]
    lines += ["", "## B. Stato del sito",
              f"- 28 gg: {cur.get('clicks', 0):.0f} clic · {cur.get('impressions', 0):.0f} impr. · CTR {cur.get('ctr', 0):.1%} · pos. {cur.get('position')}"]
    if prev:
        lines.append(f"- 28 gg precedenti: {prev['clicks']:.0f} clic · {prev['impressions']:.0f} impr. · CTR {prev['ctr']:.1%}")
    else:
        lines.append("- Periodo precedente: non disponibile → nessun confronto possibile.")
    nb = [v["nonbrand_current"] for v in snap.get("pages", {}).values() if v.get("nonbrand_current")]
    if nb:
        lines.append(f"- Non-brand (somma query per pagina): {sum(x['clicks'] for x in nb):.0f} clic · {sum(x['impressions'] for x in nb):.0f} impr.")
    else:
        lines.append("- Brand/non-brand: non separabile senza API.")
    ix = snap.get("index_status") or {}
    if ix:
        ok = sum(1 for v in ix.values() if (v or {}).get("verdict") == "PASS")
        lines.append(f"- URL Inspection: {ok}/{len(ix)} URL della sitemap indicizzate nel campione.")
    else:
        lines.append("- Indicizzazione: nessun dato URL Inspection in questo ciclo.")
    lines += ["", f"## C. Pagine selezionate: {len(sel.get('selected', []))} (su {sel.get('candidates_total')} candidate)", ""]
    for c in sel.get("selected", []):
        g = (c.get("gsc") or {}).get("current")
        met = f"{g['clicks']:.0f} clic / {g['impressions']:.0f} impr." if g else "nessuna metrica GSC per questa URL"
        lines += [f"### {c['intervention_id']} — {c['url']}", f"- Tier: {c['tier']} · punteggio {c['score']} · {met}",
                  "- Motivi: " + "; ".join(c["reasons"]), f"- Title attuale ({len(c.get('title') or '')}): {c.get('title')}", ""]
    if sel.get("excluded_cooldown"):
        lines.append("- In cooldown: " + ", ".join(x.get("url", "") for x in sel["excluded_cooldown"]))
    pub = [e for e in reg if e.get("type") == "published"]
    live = {e["intervention_id"]: e["type"] for e in reg if e.get("type") in ("live_verified", "live_check_failed")}
    lines += ["", f"## D. Interventi pubblicati ({len(pub)} totali)", ""]
    lines += [f"- {e['ts'][:10]} {e['intervention_id']} ({e['file']}): {e.get('summary')} — online: "
              f"{'verificato' if live.get(e['intervention_id']) == 'live_verified' else 'da verificare' if e['intervention_id'] not in live else 'controllo fallito'}"
              for e in pub[-20:]] or ["- Nessuno."]
    lines += ["", "## E. Esiti degli interventi precedenti (correlazione, non causalità)", ""]
    lines += [f"- {e['intervention_id']} {e['url']}: **{e['verdict']}** — {e['detail']}" for e in evals] or ["- Nessun intervento da valutare."]
    published_ids = {e["intervention_id"] for e in pub}
    pending = [(k, v) for k, v in approvals.items() if not v.get("approved") and k not in published_ids]
    pending_sel = [c for c in sel.get("selected", []) if c["intervention_id"] not in approvals]
    lines += ["", "## F. Proposte in attesa di approvazione", ""]
    lines += [f"- {k}: {v.get('summary')} — {v.get('rationale')}" for k, v in pending]
    lines += [f"- {c['intervention_id']}: proposta da redigere ({'; '.join(c['reasons'])})" for c in pending_sel]
    if not pending and not pending_sel:
        lines.append("- Nessuna.")
    issues = [(p, v["issues"]) for p, v in audit.get("pages", {}).items() if v.get("issues")]
    lines += ["", "## G. Limiti, rischi e problemi tecnici", ""]
    lines += [f"- Claim da verificare: {x}" for x in (load_json(CONFIG, {}) or {}).get("claims_to_verify", [])]
    lines += [f"- {p}: {', '.join(i)}" for p, i in issues[:40]]
    lines += ["", "## H. Prossime azioni", "",
              "1. " + ("Configurare il secret GSC_SERVICE_ACCOUNT_JSON (skill §9) — senza dati freschi non si misura nulla."
                       if stale else "Approvare le proposte della sezione F."),
              "2. Verificare online gli interventi «da verificare» con `seo_auto.py verify` dopo il deploy.",
              "3. Valutazione definitiva a ≥28 giorni di dati reali dalla pubblicazione.",
              "", f"Dashboard: `data/seo-auto/dashboard.html` · Registro: `data/seo-auto/registry.jsonl`"]
    md = "\n".join(lines) + "\n"
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / f"{date.today().isoformat()}.md").write_text(md, encoding="utf-8")
    body = "".join(f"<p>{htmllib.escape(l)}</p>" if not l.startswith("#") else f"<h3>{htmllib.escape(l.lstrip('# '))}</h3>" for l in lines if l)
    EMAIL_HTML.write_text(f'<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"></head><body style="font-family:Arial,sans-serif;max-width:680px;margin:auto;color:#152435">{body}</body></html>', encoding="utf-8")
    EMAIL_SUBJECT.write_text(f"[SEO AUTO] Ciclo {sel.get('cycle')} — {len(sel.get('selected', []))} pagine{' — DATI GSC DA AGGIORNARE' if snap.get('stale') else ''}", encoding="utf-8")
    print(f"report: data/seo-auto/reports/{date.today().isoformat()}.md")


def cmd_weekly() -> None:
    cmd_ingest()
    cmd_audit()
    cmd_verify()
    evals = cmd_evaluate()
    cmd_select()
    cmd_dashboard()
    cmd_report(evals)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["weekly", "ingest", "audit", "select", "evaluate", "apply", "verify", "rollback", "dashboard", "report"])
    ap.add_argument("--id")
    a = ap.parse_args()
    {"weekly": cmd_weekly, "ingest": cmd_ingest, "audit": cmd_audit, "select": cmd_select, "evaluate": cmd_evaluate,
     "apply": lambda: cmd_apply(a.id), "verify": cmd_verify, "rollback": lambda: cmd_rollback(a.id),
     "dashboard": cmd_dashboard, "report": lambda: cmd_report(None)}[a.cmd]()


if __name__ == "__main__":
    main()
