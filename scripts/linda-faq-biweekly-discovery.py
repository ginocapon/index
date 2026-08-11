#!/usr/bin/env python3
"""
Discovery bi-quindicinale FAQ Linda — nuovi articoli blog + immobili catalogo.

Analizza contenuti pubblicati dall'ultima run, estrae domande da FAQ schema / H2/H3
e genera proposte FAQ_DATA (≥20 per ciclo) senza modificare js/chatbot.js (policy YELLOW).

Output:
  - data/linda-faq-proposals-latest.json
  - data/linda-faq-archive.jsonl (cumulativo)
  - data/linda-faq-discovery-state.json
  - linda-faq-biweekly-report.md

Cron: venerdì 07:00 CEST (workflow venerdi-contenuti-freschezza) con gate 14 giorni.

Uso:
  python scripts/linda-faq-biweekly-discovery.py
  python scripts/linda-faq-biweekly-discovery.py --force   # bypass gate 14 giorni
  python scripts/linda-faq-biweekly-discovery.py --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIMM_JSON = ROOT / "TEST-SKILL/skimm.json"
CHATBOT_JS = ROOT / "js/chatbot.js"
OG_IMMOBILI = ROOT / "data/og-immobili.json"
EDITORIAL_QUEUE = ROOT / "data/editorial-queue.json"
STATE_JSON = ROOT / "data/linda-faq-discovery-state.json"
ARCHIVE_JSONL = ROOT / "data/linda-faq-archive.jsonl"
OUT_JSON = ROOT / "data/linda-faq-proposals-latest.json"
REPORT_MD = ROOT / "linda-faq-biweekly-report.md"

MIN_INTERVAL_DAYS = 14
MIN_PROPOSALS = 20
PHONE = "049.8843484"

QUESTION_STARTERS = (
    "quanto", "come", "qual", "quale", "quando", "dove", "perché", "perche",
    "cosa", "chi", "è possibile", "e possibile", "serve", "posso", "devo",
)

COMMISSION_REPLY = (
    "L'importo e le condizioni economiche **non sono pubblicati online**: "
    "vengono concordate **in sede** al momento del mandato."
)


def load_json(path: Path, default=None):
    if not path.exists():
        return default if default is not None else {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def proposal_id(source: str, question: str, slug: str = "") -> str:
    raw = f"{source}|{slug}|{question}".lower().strip()
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def parse_existing_keywords() -> set[str]:
    if not CHATBOT_JS.exists():
        return set()
    text = CHATBOT_JS.read_text(encoding="utf-8")
    if "const FAQ_DATA" not in text:
        return set()
    block = text.split("const FAQ_DATA")[1].split("];")[0]
    return set(re.findall(r"'([^']+)'", block))


def parse_existing_blog_refs() -> set[str]:
    if not CHATBOT_JS.exists():
        return set()
    text = CHATBOT_JS.read_text(encoding="utf-8")
    return set(re.findall(r"blog:\s*'([^']+)'", text))


def extract_faq_ld(html: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for m in re.finditer(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.DOTALL | re.IGNORECASE,
    ):
        raw = m.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            if item.get("@type") != "FAQPage":
                continue
            for ent in item.get("mainEntity", []) or []:
                if not isinstance(ent, dict):
                    continue
                q = (ent.get("name") or "").strip()
                ans = ent.get("acceptedAnswer") or {}
                a = (ans.get("text") or "").strip()
                if q and a and len(a) > 20:
                    out.append((q, a))
    return out


def extract_heading_questions(html: str) -> list[str]:
    questions: list[str] = []
    for m in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", html, re.DOTALL | re.IGNORECASE):
        txt = re.sub(r"<[^>]+>", "", m.group(1))
        txt = re.sub(r"\s+", " ", txt).strip()
        if not txt or len(txt) < 12:
            continue
        low = txt.lower()
        if "?" in txt or low.startswith(QUESTION_STARTERS):
            questions.append(txt)
    return questions


def keywords_from_question(q: str, extra: list[str] = []) -> list[str]:
    q_clean = re.sub(r"[^\w\sàèéìòù']", " ", q.lower())
    words = [w for w in q_clean.split() if len(w) > 2 and w not in ("che", "del", "della", "dei", "nel", "nella")]
    keys: list[str] = []
    if extra:
        keys.extend(extra[:2])
    if len(q) <= 48:
        keys.append(q.lower().strip())
    for w in words[:4]:
        if w not in keys:
            keys.append(w)
    phrase = " ".join(words[:5])
    if phrase and phrase not in keys:
        keys.append(phrase)
    return keys[:6]


def tone_linda(answer: str, blog_slug: str | None = None, blog_title: str | None = None) -> str:
    a = answer.strip()
    if "concordare" not in a.lower() and any(x in a.lower() for x in ("mediazione", "commissione", "provvigione", "agenzia")):
        a = f"{a}\n\n💰 Compenso mediazione: {COMMISSION_REPLY}"
    if not a.startswith(("🏠", "📋", "💶", "📍", "🕐", "📊", "🏦", "📝", "🏛️", "🏡", "📸", "🏷️", "⏱️", "🧾", "📈", "✅", "💡")):
        a = f"💡 {a}"
    if blog_slug and blog_title:
        a += f"\n\n📖 Approfondimento: *{blog_title}* sul nostro blog."
    a += f"\n\n📞 Per un orientamento personalizzato: **{PHONE}** o passa in Via Roma 96, Limena."
    return a


def immobile_questions(entry: dict, slug: str) -> list[dict]:
    codice = (entry.get("codice") or slug.split("-")[-1] or "rif").strip()
    if not codice:
        return []
    titolo = entry.get("titolo", "")
    desc = entry.get("description", "")
    seo_slug = entry.get("seo_slug", slug)

    tipologia = "immobile"
    operazione = "vendita"
    comune = ""
    if desc:
        parts = desc.split("·")
        if parts:
            tipologia = parts[0].strip().lower()
        for p in parts:
            if "affitto" in p.lower():
                operazione = "affitto"
            if "€" in p:
                prezzo = p.strip()
            m_com = re.search(r"Rif\.\s*([A-Z0-9-]+)", p)
            if m_com and not codice:
                codice = m_com.group(1)

    comune_m = re.search(r"(?:a|in)\s+([A-Za-zÀ-ÿ' ]+?)(?:\s*—|\s*·|$)", entry.get("title", ""))
    if comune_m:
        comune = comune_m.group(1).strip()

    proposals = []

    q1 = f"Informazioni sull'immobile rif. {codice}"
    r1 = (
        f"🏠 **{titolo}**\n\n{desc}\n\n"
        f"Puoi vedere foto, planimetria e virtual tour nella scheda del catalogo. "
        f"Per visita o dettagli aggiuntivi contattaci con il codice **{codice}**."
    )
    proposals.append({
        "question": q1,
        "k": keywords_from_question(q1, [codice.lower(), f"rif {codice.lower()}", seo_slug.split("-")[-1].lower()]),
        "r": tone_linda(r1),
        "immobile_slug": seo_slug,
        "immobile_codice": codice,
        "source": "immobile_catalog",
    })

    if comune:
        q2 = f"C'è un {tipologia} in {operazione} a {comune} rif {codice}?"
        r2 = (
            f"Sì, al momento abbiamo **{titolo}** ({desc}). "
            f"Codice incarico: **{codice}**. Possiamo organizzare una visita su appuntamento."
        )
        proposals.append({
            "question": q2,
            "k": keywords_from_question(q2, [comune.lower(), operazione, codice.lower()]),
            "r": tone_linda(r2),
            "immobile_slug": seo_slug,
            "immobile_codice": codice,
            "source": "immobile_catalog",
        })

    q3 = f"Come prenotare visita per {codice}"
    r3 = (
        f"Per visitare l'immobile **{codice}** ({titolo}) chiama **{PHONE}**, "
        f"usa il form contatti o chiedi qui in chat indicando il codice."
    )
    proposals.append({
        "question": q3,
        "k": [f"visita {codice.lower()}", f"prenota {codice.lower()}", "visita immobile", codice.lower()],
        "r": tone_linda(r3),
        "immobile_slug": seo_slug,
        "immobile_codice": codice,
        "source": "immobile_catalog",
    })

    return proposals


def gap_fill_from_skimm(missing_slugs: list[str], articles: list[dict], limit: int) -> list[dict]:
    out: list[dict] = []
    by_slug = {a["slug"]: a for a in articles}
    templates = [
        ("Cosa dice il blog su {topic}?", "Nel nostro articolo trattiamo {topic} con dati verificabili e contesto Padova/hinterland."),
        ("Guida {topic} a Padova", "Abbiamo una guida dedicata a {topic} sul blog Righetto — utile prima di decidere tempi e budget."),
        ("Domande su {topic}", "Per {topic} conviene leggere la guida aggiornata e poi valutare il caso con un consulente in sede."),
    ]
    for slug in missing_slugs[:limit]:
        art = by_slug.get(slug, {})
        title = art.get("title", slug.replace("blog-", "").replace("-", " "))
        topic = title[:60]
        tpl = templates[len(out) % len(templates)]
        q = tpl[0].format(topic=topic)
        r = tpl[1].format(topic=topic)
        out.append({
            "question": q,
            "k": keywords_from_question(q, [art.get("kw_primaria", ""), slug.replace("blog-", "")[:30]]),
            "r": tone_linda(r, slug, title),
            "blog": slug,
            "blogTitle": title,
            "source": "skimm_gap",
        })
    return out


def should_run(state: dict, force: bool) -> tuple[bool, str]:
    if force:
        return True, "force"
    last = state.get("last_run_at")
    if not last:
        return True, "first_run"
    try:
        last_dt = datetime.fromisoformat(last)
    except ValueError:
        return True, "invalid_last_run"
    elapsed = datetime.now() - last_dt
    if elapsed.days < MIN_INTERVAL_DAYS:
        return False, f"gate: {elapsed.days} giorni < {MIN_INTERVAL_DAYS}"
    return True, f"due: {elapsed.days} giorni"


def collect_new_blog_slugs(since: datetime | None) -> list[str]:
    slugs: list[str] = []
    skimm = load_json(SKIMM_JSON, {"articles": []})
    for art in skimm.get("articles", []):
        slug = art.get("slug", "")
        fpath = ROOT / art.get("file", f"{slug}.html")
        if not fpath.exists():
            fpath = ROOT / f"{slug}.html"
        if not fpath.exists():
            continue
        if since is None:
            slugs.append(slug)
            continue
        mtime = datetime.fromtimestamp(fpath.stat().st_mtime)
        if mtime >= since:
            slugs.append(slug)

    eq = load_json(EDITORIAL_QUEUE, {})
    items = eq.get("items", eq.get("queue", []))
    if isinstance(items, list):
        for it in items:
            if it.get("status") in ("published", "live", "done"):
                pub = it.get("published_at") or it.get("updated_at") or ""
                slug = it.get("slug", "")
                if slug and slug.startswith("blog-"):
                    if since is None or (pub and pub >= since.isoformat()[:10]):
                        if slug not in slugs:
                            slugs.append(slug)
    return slugs


def collect_new_immobili(since: datetime | None) -> list[str]:
    og = load_json(OG_IMMOBILI, {"bySlug": {}})
    by_slug = og.get("bySlug", {})
    out: list[str] = []
    for slug, entry in by_slug.items():
        codice = entry.get("codice") or ""
        if not codice:
            out.append(slug)
            continue
        img_dir = ROOT / "img/immobili" / codice
        changed = False
        if img_dir.exists():
            mtime = datetime.fromtimestamp(img_dir.stat().st_mtime)
            if since is None or mtime >= since:
                changed = True
        og_mtime = OG_IMMOBILI.stat().st_mtime
        if since is None or datetime.fromtimestamp(og_mtime) >= since:
            changed = True
        if changed:
            out.append(slug)
    return out


def build_proposals(
    blog_slugs: list[str],
    immobile_slugs: list[str],
    existing_kw: set[str],
    seen_ids: set[str],
    articles: list[dict],
    missing_blog_refs: list[str],
) -> list[dict]:
    proposals: list[dict] = []
    by_slug = {a["slug"]: a for a in articles}

    def accept(p: dict) -> bool:
        pid = proposal_id(p.get("source", ""), p.get("question", ""), p.get("blog", p.get("immobile_slug", "")))
        if pid in seen_ids:
            return False
        for k in p.get("k", []):
            if k in existing_kw:
                return False
        p["id"] = pid
        p["status"] = "proposed"
        p["policy"] = "yellow"
        p["merge_hint"] = "Revisione umana → FAQ_DATA in js/chatbot.js + bump chatbot.js?v=N"
        return True

    for slug in blog_slugs:
        art = by_slug.get(slug, {})
        fpath = ROOT / art.get("file", f"{slug}.html")
        if not fpath.exists():
            fpath = ROOT / f"{slug}.html"
        if not fpath.exists():
            continue
        html = fpath.read_text(encoding="utf-8", errors="replace")
        title = art.get("title", slug)

        for q, a in extract_faq_ld(html):
            p = {
                "question": q,
                "k": keywords_from_question(q, [art.get("kw_primaria", "")]),
                "r": tone_linda(a, slug, title),
                "blog": slug,
                "blogTitle": title,
                "source": "blog_faq_schema",
            }
            if accept(p):
                proposals.append(p)
                for k in p["k"]:
                    existing_kw.add(k)

        for hq in extract_heading_questions(html):
            p = {
                "question": hq,
                "k": keywords_from_question(hq, [art.get("kw_primaria", "")]),
                "r": tone_linda(
                    f"Per «{hq}» abbiamo trattato l'argomento nell'articolo *{title}* con focus su Padova e provincia.",
                    slug,
                    title,
                ),
                "blog": slug,
                "blogTitle": title,
                "source": "blog_heading",
            }
            if accept(p):
                proposals.append(p)
                for k in p["k"]:
                    existing_kw.add(k)

    for slug in immobile_slugs:
        og = load_json(OG_IMMOBILI, {"bySlug": {}})
        entry = og.get("bySlug", {}).get(slug, {})
        if not entry:
            continue
        for p in immobile_questions(entry, slug):
            if accept(p):
                proposals.append(p)
                for k in p["k"]:
                    existing_kw.add(k)

    if len(proposals) < MIN_PROPOSALS:
        need = MIN_PROPOSALS - len(proposals)
        for p in gap_fill_from_skimm(missing_blog_refs, articles, need + 10):
            if accept(p):
                proposals.append(p)
                for k in p["k"]:
                    existing_kw.add(k)
            if len(proposals) >= MIN_PROPOSALS:
                break

    return proposals[:max(MIN_PROPOSALS, len(proposals))]


def write_report(run: dict, skipped: bool, reason: str) -> None:
    lines = [
        "# Linda FAQ — discovery bi-quindicinale",
        "",
        f"**Generato:** {run.get('generated_at', now_iso())}",
        f"**Stato:** {'SKIP' if skipped else 'OK'} — {reason}",
        "",
    ]
    if skipped:
        lines.append("Prossima esecuzione quando il gate 14 giorni scade o con `--force`.")
    else:
        lines.extend([
            f"- Articoli blog analizzati: **{run.get('blog_slugs_scanned', 0)}**",
            f"- Immobili analizzati: **{run.get('immobile_slugs_scanned', 0)}**",
            f"- Proposte nuove questo ciclo: **{run.get('proposals_count', 0)}** (target ≥{MIN_PROPOSALS})",
            f"- Archivio cumulativo: **{run.get('archive_total', 0)}** voci",
            "",
            "## Policy",
            "",
            "Le proposte sono **YELLOW** — non vengono mergeate in `js/chatbot.js` dal cron.",
            "Dopo revisione: integrare in `FAQ_DATA`, `python scripts/audit_chatbot_faq.py`, bump `chatbot.js?v=N`.",
            "",
            "## Proposte (estratto)",
            "",
        ])
        for i, p in enumerate(run.get("proposals", [])[:30], 1):
            lines.append(f"### {i}. {p.get('question', '')[:80]}")
            lines.append(f"- **Source:** {p.get('source')}")
            lines.append(f"- **Keywords:** {', '.join(p.get('k', [])[:5])}")
            if p.get("blog"):
                lines.append(f"- **Blog:** `{p.get('blog')}`")
            if p.get("immobile_codice"):
                lines.append(f"- **Immobile:** {p.get('immobile_codice')}")
            lines.append("")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Bypass gate 14 giorni")
    parser.add_argument("--dry-run", action="store_true", help="Non salva file")
    args = parser.parse_args()

    state = load_json(STATE_JSON, {
        "version": 1,
        "last_run_at": None,
        "archive_ids": [],
        "total_archived": 0,
    })
    seen_ids = set(state.get("archive_ids", []))

    ok, reason = should_run(state, args.force)
    if not ok:
        run = {"generated_at": now_iso(), "skipped": True, "reason": reason}
        if not args.dry_run:
            write_report(run, True, reason)
            save_json(OUT_JSON, run)
        print(f"SKIP: {reason}")
        return 0

    since: datetime | None = None
    if state.get("last_run_at"):
        try:
            since = datetime.fromisoformat(state["last_run_at"]) - timedelta(days=1)
        except ValueError:
            since = None

    skimm = load_json(SKIMM_JSON, {"articles": []})
    articles = skimm.get("articles", [])
    all_slugs = {a["slug"] for a in articles}
    existing_blog_refs = parse_existing_blog_refs()
    missing_blog_refs = sorted(all_slugs - existing_blog_refs - {"blog"})
    existing_kw = parse_existing_keywords()

    blog_slugs = collect_new_blog_slugs(since)
    if not blog_slugs and since:
        blog_slugs = collect_new_blog_slugs(None)[:15]

    immobile_slugs = collect_new_immobili(since)
    if not immobile_slugs:
        og = load_json(OG_IMMOBILI, {"bySlug": {}})
        immobile_slugs = list(og.get("bySlug", {}).keys())[:12]

    proposals = build_proposals(
        blog_slugs,
        immobile_slugs,
        existing_kw,
        seen_ids,
        articles,
        missing_blog_refs,
    )

    run_id = datetime.now().strftime("%Y%m%d-%H%M")
    generated_at = now_iso()

    for p in proposals:
        p["run_id"] = run_id
        p["generated_at"] = generated_at

    archive_total = state.get("total_archived", 0)
    if not args.dry_run:
        with ARCHIVE_JSONL.open("a", encoding="utf-8") as f:
            for p in proposals:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
                seen_ids.add(p["id"])
                archive_total += 1

        state["last_run_at"] = generated_at
        state["last_run_reason"] = reason
        state["archive_ids"] = list(seen_ids)[-5000:]
        state["total_archived"] = archive_total
        save_json(STATE_JSON, state)

    run = {
        "generated_at": generated_at,
        "run_id": run_id,
        "skipped": False,
        "reason": reason,
        "blog_slugs_scanned": len(blog_slugs),
        "immobile_slugs_scanned": len(immobile_slugs),
        "proposals_count": len(proposals),
        "archive_total": archive_total,
        "min_target": MIN_PROPOSALS,
        "policy": "yellow",
        "proposals": proposals,
    }

    if not args.dry_run:
        save_json(OUT_JSON, run)
        write_report(run, False, reason)

    print(f"OK: {len(proposals)} proposte FAQ (target ≥{MIN_PROPOSALS})")
    print(f"Blog: {len(blog_slugs)} | Immobili: {len(immobile_slugs)} | Archivio: {archive_total}")
    if len(proposals) < MIN_PROPOSALS:
        print(f"WARN: sotto target {MIN_PROPOSALS}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
