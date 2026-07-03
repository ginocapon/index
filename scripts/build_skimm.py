# -*- coding: utf-8 -*-
"""Genera TEST-SKILL/skimm.md e skimm.json — registro keyword/intent anti-doppioni blog."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_MD = ROOT / "TEST-SKILL" / "skimm.md"
OUT_JSON = ROOT / "TEST-SKILL" / "skimm.json"

# Angolo editoriale esplicito (evita cannibalizzazione SEO tra articoli vicini)
ANGLE_OVERRIDES: dict[str, dict] = {
    "blog-stanza-universitaria-padova-canoni-2026": {
        "kw_primaria": "canone-stanza-insights-490-padova",
        "angolo": "Dato Immobiliare.it Insights (+46% vs 2020) e periferie tram — non FIMAA Q1",
        "intent": "affitto-studenti-budget",
    },
    "blog-studentati-veneto-2026-posti-letto": {
        "kw_primaria": "posti-letto-esu-camplus-pnrr-veneto",
        "angolo": "Canali offerta regionale (ESU/privati/PNRR) — non singolo canone stanza",
        "intent": "housing-sistemico-veneto",
    },
    "blog-residenze-green-padova-tribloc-2026": {
        "kw_primaria": "tribloc-gozzi-nzeb-riuso-uffici",
        "angolo": "Progetto urbano Tribloc/Gozzi — non generico green building",
        "intent": "riuso-edilizio-studenti",
    },
    "blog-vicenza-residenze-universitarie-calmierate-2026": {
        "kw_primaria": "casa-querini-calmierati-vicenza",
        "angolo": "Vicenza PNRR Saudino — non Padova né Tribloc",
        "intent": "calmierati-vicenza",
    },
    "blog-housing-lavoratori-veneto-edilcassa-2026": {
        "kw_primaria": "edilcassa-fondo-garanzia-locazione-lavoratori",
        "angolo": "Fondo 250k€ garanzie affitto operai — non studenti né canoni",
        "intent": "corporate-housing-edile",
    },
    "blog-affitti-padova-canoni-2026": {
        "kw_primaria": "affitti-padova-canoni-trend-2026",
        "angolo": "Pillar canoni città +8% — non stanza singola Insights",
        "intent": "affitti-pillar",
    },
    "blog-affitto-studenti-padova": {
        "kw_primaria": "guida-affitto-studenti-padova",
        "angolo": "Guida evergreen zone/contratti — non dato anno",
        "intent": "affitto-studenti-guida",
    },
    "blog-affitti-canoni-fimaa-q1-2026-padova": {
        "kw_primaria": "fimaa-q1-2026-canoni-veneto",
        "angolo": "Rilevazione trimestrale FIMAA — non Insights 490€",
        "intent": "affitti-dato-trimestrale",
    },
    "blog-checklist-affitto-studenti-padova-2026": {
        "kw_primaria": "checklist-contratto-studenti-padova",
        "angolo": "Checklist operativa caparra/contratto — non mercato",
        "intent": "affitto-studenti-operativo",
    },
    "blog-contratto-affitto-padova": {
        "kw_primaria": "contratto-affitto-tipologie-padova",
        "angolo": "4+4, 3+2, transitorio, cedolare — normativa",
        "intent": "contratti-locazione",
    },
    "blog-rendimento-affitto-padova": {
        "kw_primaria": "rendimento-locativo-quartieri-padova",
        "angolo": "Yield % per quartiere investitori",
        "intent": "investimento-locativo",
    },
    "blog-bce-tassi-mutui-giugno-2026-padova": {
        "kw_primaria": "bce-giugno-2026-tassi-mutui",
        "angolo": "Decisione BCE giugno +25bp — evento datato",
        "intent": "mutui-evento-bce",
    },
    "blog-mutui-tasso-fisso-bancaitalia-padova-2026": {
        "kw_primaria": "mutui-tasso-fisso-bancaitalia",
        "angolo": "Preferenza fisso vs variabile BdI — non BCE singolo meeting",
        "intent": "mutui-scelta-tasso",
    },
    "blog-dazi-usa-ue-mercato-padova-2026": {
        "kw_primaria": "dazi-usa-ue-filiera-veneto-padova",
        "angolo": "Impatto occupazione/credito Padova — non cronaca Strasburgo",
        "intent": "macro-commercio-locale",
    },
    "blog-eurocamera-accordo-dazi-usa-2026": {
        "kw_primaria": "eurocamera-accordo-dazi-sunset-2029",
        "angolo": "Accordo istituzionale EU-USA — non filiera padovana",
        "intent": "macro-istituzionale",
    },
}

CLUSTER_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("Affitti e locazioni", ("affitto", "affitti", "stanza", "locaz", "housing", "studentati", "residenze-universitarie", "rendimento-affitto", "contratto-affitto", "canoni-fimaa", "emergenza-abitativa", "affitto-breve", "quotazioni-locazioni")),
    ("Mutui e credito", ("mutuo", "mutui", "tassi", "bce", "crif", "barometro-mutui", "surroga", "calcolo-mutuo", "documenti-tempi-mutuo", "selettivi-banche")),
    ("Acquisto e prima casa", ("comprare", "acquisto", "prima-casa", "agevolazioni-prima", "compromesso", "caparra", "scegliere-immobile", "errori-acquisto", "checklist-verifiche", "planimetria-catastale")),
    ("Vendita", ("vendere", "vendita", "costi-vendere", "tempi-vendita", "percorso-vendita", "documenti-vendita", "tasse-vendita", "home-staging", "vendibile")),
    ("Fisco e normativa", ("imposte", "tasse", "fisco", "bonus", "condono", "piano-casa", "decreto", "rogito", "costi-proprieta", "quattro-imposte")),
    ("Mercato e dati", ("mercato", "prezzi", "omi", "compravendite", "sondaggio-bancaditalia", "stock-vendita", "crisi-immobiliare", "bolla", "prospettive", "previsioni", "case-piu-vendute", "nuove-costruzioni", "costi-costruzione")),
    ("Territorio e zone", ("quartieri", "limena", "vigonza", "zona-", "sacrocuore", "piazzola", "centro-padova", "cintura", "servizi-infrastrutture", "trasporti", "scuole")),
    ("Sostenibilità e APE", ("green", "ape", "case-green", "direttiva-case-green", "nzbe", "tribloc")),
    ("Macro e geopolitica", ("geopolitica", "dazi", "eurocamera", "ucraina", "medio-oriente", "patrimonio-casa-resilienza", "tensioni")),
    ("Investimenti", ("investire", "investimenti", "trend-investimenti")),
    ("Vita d'agenzia", ("acquisizioni", "righetto-storia", "righetto-bilancio", "impegno-quotidiano", "agenzia-immobiliare-top", "ca-marcello")),
    ("Servizi e istituzionale", ("scegliere-agenzia", "permuta", "successione", "comprare-affittare")),
]

STOP_TOKENS = frozenset(
    "blog padova 2026 2025 veneto italia html il la le di del della per e in a al".split()
)


def extract_from_html(path: Path) -> dict | None:
    t = path.read_text(encoding="utf-8", errors="replace")
    slug = path.stem
    if slug == "blog-articolo":
        return None
    title_m = re.search(r"<title>([^<]+)</title>", t)
    title = title_m.group(1).strip() if title_m else slug
    title = re.sub(r"\s*\|\s*Righetto.*$", "", title, flags=re.I)
    canon_m = re.search(
        r'rel="canonical"\s+href="https://righettoimmobiliare\.it/([^"?]+)',
        t,
    )
    canon = canon_m.group(1).rstrip("/") if canon_m else slug
    h1_m = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S | re.I)
    h1 = re.sub(r"<[^>]+>", "", h1_m.group(1)).strip() if h1_m else ""
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', t, re.I)
    desc = desc_m.group(1) if desc_m else ""
    return {
        "slug": canon,
        "file": path.name,
        "title": title,
        "h1": h1[:120],
        "meta_desc": desc[:160],
    }


def extract_blog_html_entries() -> list[dict]:
    text = (ROOT / "blog.html").read_text(encoding="utf-8", errors="replace")
    entries: list[dict] = []
    blocks = re.findall(
        r'\{[^{}]*"url_statico"\s*:\s*"([^"]+)"[^{}]*\}',
        text,
        re.S,
    )
    # parse each articoliStatici object more reliably
    for m in re.finditer(
        r'"url_statico"\s*:\s*"([^"]+)"[^}]*?"titolo"\s*:\s*"([^"]+)"[^}]*?"categoria"\s*:\s*"([^"]+)"',
        text,
        re.S,
    ):
        entries.append(
            {"slug": m.group(1), "titolo": m.group(2), "categoria": m.group(3)}
        )
    # fallback: also single-quoted admin-style in same array
    for m in re.finditer(
        r"url_statico:\s*'([^']+)'[^}]*?titolo:\s*'([^']+)'[^}]*?categoria:\s*'([^']+)'",
        text,
        re.S,
    ):
        entries.append(
            {"slug": m.group(1), "titolo": m.group(2), "categoria": m.group(3)}
        )
    seen: set[str] = set()
    out: list[dict] = []
    for e in entries:
        if e["slug"] not in seen:
            seen.add(e["slug"])
            out.append(e)
    return out


def classify_cluster(slug: str, categoria: str = "") -> str:
    s = slug.lower()
    for name, keys in CLUSTER_RULES:
        if any(k in s for k in keys):
            return name
    cat = categoria.lower()
    if "affitt" in cat or "locaz" in cat:
        return "Affitti e locazioni"
    if "mutui" in cat or "finanz" in cat or "credito" in cat:
        return "Mutui e credito"
    if "fisco" in cat or "normativ" in cat:
        return "Fisco e normativa"
    if "mercato" in cat or "econom" in cat:
        return "Mercato e dati"
    if "guida" in cat or "acquist" in cat:
        return "Acquisto e prima casa"
    return "Altri / trasversali"


def slug_tokens(slug: str) -> list[str]:
    raw = slug.replace("blog-", "").replace("-", " ")
    return [w for w in raw.split() if w and w not in STOP_TOKENS and len(w) > 2]


def derive_kw(slug: str, override: dict | None) -> str:
    if override and override.get("kw_primaria"):
        return override["kw_primaria"]
    toks = slug_tokens(slug)
    return "-".join(toks[:5]) if toks else slug


def derive_angolo(slug: str, title: str, override: dict | None) -> str:
    if override and override.get("angolo"):
        return override["angolo"]
    return f"Angolo da definire — verificare overlap cluster ({title[:60]})"


def derive_intent(slug: str, cluster: str, override: dict | None) -> str:
    if override and override.get("intent"):
        return override["intent"]
    return cluster.lower().replace(" ", "-")[:40]


def build_catalog() -> list[dict]:
    bh_map = {e["slug"]: e for e in extract_blog_html_entries()}
    catalog: dict[str, dict] = {}
    for p in sorted(ROOT.glob("blog-*.html")):
        row = extract_from_html(p)
        if not row:
            continue
        slug = row["slug"]
        bh = bh_map.get(slug, {})
        ov = ANGLE_OVERRIDES.get(slug)
        cluster = classify_cluster(slug, bh.get("categoria", ""))
        catalog[slug] = {
            "slug": slug,
            "file": row["file"],
            "title": bh.get("titolo") or row["title"],
            "categoria": bh.get("categoria", ""),
            "cluster": cluster,
            "kw_primaria": derive_kw(slug, ov),
            "angolo": derive_angolo(slug, row["title"], ov),
            "intent": derive_intent(slug, cluster, ov),
            "h1": row["h1"],
        }
    return sorted(catalog.values(), key=lambda x: (x["cluster"], x["slug"]))


def find_risks(catalog: list[dict]) -> list[str]:
    risks: list[str] = []
    by_kw: dict[str, list[str]] = defaultdict(list)
    by_intent: dict[str, list[str]] = defaultdict(list)
    token_index: dict[str, list[str]] = defaultdict(list)

    for item in catalog:
        by_kw[item["kw_primaria"]].append(item["slug"])
        by_intent[item["intent"]].append(item["slug"])
        for tok in slug_tokens(item["slug"]):
            token_index[tok].append(item["slug"])

    for kw, slugs in by_kw.items():
        if len(slugs) > 1:
            risks.append(f"KW primaria duplicata `{kw}`: {', '.join(slugs)}")

    for intent, slugs in by_intent.items():
        if len(slugs) > 1 and intent not in ("affitti-pillar",):
            risks.append(f"Intent simile `{intent}`: {', '.join(slugs[:4])}{'…' if len(slugs)>4 else ''}")

    risky_tokens = ("padova", "2026", "mutui", "affitti", "mercato", "studenti", "residenze", "veneto", "green")
    for tok in risky_tokens:
        slugs = token_index.get(tok, [])
        if len(slugs) >= 8:
            risks.append(f"Token slug sovrausato `{tok}` ({len(slugs)} articoli) — variare radice nei prossimi batch")

    # Coppie affitti note
    pairs = [
        ("blog-stanza-universitaria-padova-canoni-2026", "blog-affitti-padova-canoni-2026", "Insights 490 vs pillar +8%"),
        ("blog-stanza-universitaria-padova-canoni-2026", "blog-affitti-canoni-fimaa-q1-2026-padova", "Insights vs FIMAA Q1"),
        ("blog-residenze-green-padova-tribloc-2026", "blog-domanda-case-green-certificazione-padova-2026", "Tribloc vs Case Green generico"),
        ("blog-bce-tassi-mutui-giugno-2026-padova", "blog-mutui-casa-padova-2026", "Evento BCE vs guida mutui"),
    ]
    slugs_set = {c["slug"] for c in catalog}
    for a, b, note in pairs:
        if a in slugs_set and b in slugs_set:
            risks.append(f"Coppia da non fondere ({note}): {a} ↔ {b}")

    return risks


def render_md(catalog: list[dict], risks: list[str]) -> str:
    today = date.today().isoformat()
    by_cluster: dict[str, list[dict]] = defaultdict(list)
    for c in catalog:
        by_cluster[c["cluster"]].append(c)

    lines: list[str] = [
        "# SKIMM — Blog Keyword & Intent Map (Righetto)",
        "",
        f"> **Generato:** {today} · Script: `python scripts/build_skimm.py`",
        "> **Uso:** prima di ogni nuovo articolo — anti-doppioni semantici + keyword per «bucare» Google senza cannibalizzare.",
        "> **Companion:** `check_doppioni_sito.py` (tecnico) + `skill-content.md` §2.0–2.2 + `SKILL-2.0.md` §8.1a.",
        "",
        "---",
        "",
        "## 1. Programma regole interne (anti-doppioni + SEO)",
        "",
        "### 1.1 Flusso obbligatorio nuovo articolo",
        "",
        "1. Leggere **§3 catalogo** e **§4 matrice rischi** di questo file.",
        "2. Eseguire `python scripts/check_doppioni_sito.py` (slug/titolo/canonical).",
        "3. Eseguire `python scripts/build_skimm.py --check \"slug-proposto\" \"kw-primaria\" \"cluster\"` (se implementato) o verificare manualmente §3.",
        "4. Se overlap → **STOP** → nuovo angolo + fonte istituzionale (OMI, BCE, ISTAT, FIMAA, ADE…).",
        "5. Pubblicare con: `kw_primaria` unica · H2 domanda diverse · sezione **Cosa può fare Righetto** · foto realistiche.",
        "",
        "### 1.2 Come «bucare» Google senza doppioni",
        "",
        "| Strategia | Cosa fare | Esempio buono | Esempio da evitare |",
        "|---|---|---|---|",
        "| **Long-tail datato** | Ancorare a evento/fonte con data | `bce-giugno-2026-tassi-mutui` | Secondo «mutui 2026» generico |",
        "| **Entità nominale** | Nome progetto/luogo univoco | `tribloc-gozzi-nzeb` | Altro «residenze green padova» |",
        "| **Intent diverso** | Stesso tema, pubblico diverso | Checklist contratto vs dato canoni | Due guide affitto studenti |",
        "| **Geografia variata** | Cambiare città o scala | `casa-querini-vicenza` | Terzo articolo solo «Padova studenti» |",
        "| **Dato vs normativa vs operativo** | Un solo tipo per URL | FIMAA Q1 (dato) / decreto 66 (norma) / checklist (azione) | FIMAA + Insights nello stesso pezzo come pillar |",
        "",
        "### 1.3 Regole slug (batch e singoli)",
        "",
        "- **Max 2 slug** nello stesso batch con la stessa radice (`padova`, `veneto`, `2026`, `studenti`, `residenze`).",
        "- **Keyword primaria** (colonna §3) **univoca** in tutto il catalogo.",
        "- Slug pattern: `blog-{entità-o-dato}-{località-opzionale}-{anno-opzionale}` — preferire **entità** (`tribloc-gozzi`, `casa-querini`, `edilcassa-garanzia`) a aggettivi generici (`housing`, `residenze-universitarie`).",
        "- **Anno nel slug** solo per articoli **legati a evento** (BCE meeting, bando, Q1 FIMAA). Guide evergreen **senza** anno in URL.",
        "- **Non** cambiare slug live senza 301 + sitemap.",
        "",
        "### 1.4 Keyword secondarie (title/H2/meta)",
        "",
        "- Title: 1 keyword primaria + localizzazione + **hook numerico** se c'è fonte.",
        "- H2: domande AEO **non copiate** da altri articoli dello stesso cluster.",
        "- Meta description: dato verificabile + beneficio + implicit CTA.",
        "- `article:tag`: 3–5 tag, **nessuno** già usato come `kw_primaria` di un altro articolo.",
        "",
        "### 1.5 Cluster COMPLETI — gap consentiti",
        "",
        "Cluster segnati COMPLETO in `skill-content.md` §1: nuovo articolo solo se:",
        "",
        "- nuova **fonte/dato** (trimestre OMI, comunicato BCE, bando ESU), oppure",
        "- nuova **entità** (progetto, norma, quartiere), oppure",
        "- nuovo **intent** (checklist, confronto, corporate B2B).",
        "",
        "### 1.6 Prossimi articoli — keyword ancora libere (opportunità)",
        "",
        "- `affitto-transitorio-padova-durata-massima` (normativa, non duplica contratto-affitto)",
        "- `imu-seconda-casa-padova-2026` (fisco possesso, distinto da costi-proprieta)",
        "- `studentato-esu-bando-2026-27` (evento bando, distinto da posti-letto sistemico)",
        "- `rubano-limena-affitto-lavoratori-cantiere` (B2B locale, distinto da edilcassa)",
        "- `mestre-affitti-studenti-ca-foscari` (geografia diversa da Padova)",
        "",
        "---",
        "",
        "## 2. Stato verifica automatica",
        "",
    ]
    if risks:
        lines.append(f"**{len(risks)} avvisi** al generazione {today}:")
        lines.append("")
        for r in risks:
            lines.append(f"- {r}")
    else:
        lines.append("Nessun conflitto `kw_primaria` duplicata. Controllare comunque angoli editoriali §4.")
    lines.extend(
        [
            "",
            f"**Articoli catalogati:** {len(catalog)}",
            "",
            "---",
            "",
            "## 3. Catalogo completo per cluster",
            "",
        ]
    )

    for cluster in sorted(by_cluster.keys()):
        lines.append(f"### {cluster} ({len(by_cluster[cluster])})")
        lines.append("")
        lines.append("| Slug | KW primaria | Angolo editoriale |")
        lines.append("|---|---|---|")
        for c in by_cluster[cluster]:
            ang = c["angolo"].replace("|", "/")
            lines.append(f"| `{c['slug']}` | `{c['kw_primaria']}` | {ang} |")
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## 4. Matrice rischi — cluster Affitti (non fondere)",
            "",
            "| Articolo A | Articolo B | Perché restano distinti |",
            "|---|---|---|",
            "| `blog-affitto-studenti-padova` | `blog-checklist-affitto-studenti-padova-2026` | Guida zone vs checklist operativa |",
            "| `blog-affitti-padova-canoni-2026` | `blog-stanza-universitaria-padova-canoni-2026` | Pillar città vs dato Insights stanza |",
            "| `blog-affitti-canoni-fimaa-q1-2026-padova` | `blog-stanza-universitaria-padova-canoni-2026` | FIMAA trimestre vs Insights |",
            "| `blog-studentati-veneto-2026-posti-letto` | `blog-stanza-universitaria-padova-canoni-2026` | Offerta sistemica vs prezzo stanza |",
            "| `blog-residenze-green-padova-tribloc-2026` | `blog-domanda-case-green-certificazione-padova-2026` | Progetto Tribloc vs domanda Case Green |",
            "| `blog-vicenza-residenze-universitarie-calmierate-2026` | `blog-studentati-veneto-2026-posti-letto` | Vicenza Querini vs panorama Veneto |",
            "| `blog-housing-lavoratori-veneto-edilcassa-2026` | `blog-contratto-affitto-padova` | B2B edile vs contratti residenziali |",
            "",
            "---",
            "",
            "## 5. Aggiornamento",
            "",
            "Dopo ogni batch blog:",
            "",
            "1. `python scripts/build_skimm.py`",
            "2. Aggiungere `ANGLE_OVERRIDES` in `scripts/build_skimm.py` per ogni articolo nuovo.",
            "3. `python scripts/check_doppioni_sito.py`",
            "4. Commit `skimm.md` + `skimm.json` insieme agli HTML.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    import sys

    catalog = build_catalog()
    risks = find_risks(catalog)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(render_md(catalog, risks), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "generated": date.today().isoformat(),
                "count": len(catalog),
                "risks": risks,
                "articles": catalog,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"OK skimm: {len(catalog)} articoli, {len(risks)} avvisi")
    print(f"  {OUT_MD}")
    print(f"  {OUT_JSON}")

    if len(sys.argv) >= 4 and sys.argv[1] == "--check":
        prop_slug = sys.argv[2]
        prop_kw = sys.argv[3]
        prop_cluster = sys.argv[4] if len(sys.argv) > 4 else ""
        conflicts = [
            c
            for c in catalog
            if c["kw_primaria"] == prop_kw or c["slug"] == prop_slug
        ]
        if conflicts:
            print("CONFLITTO:")
            for c in conflicts:
                print(f"  - {c['slug']} ({c['kw_primaria']})")
            return 1
        print(f"OK proposta: {prop_slug} / {prop_kw} / {prop_cluster}")
        return 0

    return 1 if any("duplicata" in r for r in risks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
