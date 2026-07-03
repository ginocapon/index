#!/usr/bin/env python3
"""Inietta sezione «Cosa può fare Righetto» (righetto-sol) nei blog che ne sono privi."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIMM = ROOT / "TEST-SKILL" / "skimm.json"

# ~20 slug ad alto traffico atteso (pillar + guide + mercato)
PRIORITY_SLUGS = {
    "blog-comprare-casa-padova-guida-2026",
    "blog-mutui-casa-padova-2026",
    "blog-case-vendita-padova",
    "blog-affitti-padova-canoni-2026",
    "blog-mercato-immobiliare-padova-2026",
    "blog-costi-vendere-casa-padova-2026",
    "blog-tempi-vendita-casa-padova",
    "blog-prezzi-case-padova-zona-2026",
    "blog-affitto-studenti-padova",
    "blog-mutuo-prima-casa-padova",
    "blog-comprare-affittare-padova",
    "blog-percorso-vendita-immobile-padova-2026",
    "blog-vendita-immobiliare-padova-strategie-2026",
    "blog-scegliere-agenzia-immobiliare-padova-2026",
    "blog-documenti-vendita-casa",
    "blog-quartieri-padova-2026",
    "blog-mutuo-fisso-variabile-padova-2026",
    "blog-home-staging-padova",
    "blog-investire-immobiliare-padova",
    "blog-righetto-storia-territorio-acquisizioni-2026",
}

FOOT = (
    '<p class="righetto-sol-foot"><em>Mediazione e compenso concordati in sede nel mandato'
    " — nessun listino percentuale online. Tel. 049.8843484 · "
    '<a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a>.</em></p>'
)

LINK_LABEL = {
    "immobili": "catalogo immobili",
    "servizio-locazioni": "servizio locazioni",
    "servizio-gestione": "servizio gestione",
    "servizio-valutazioni": "servizio valutazioni",
    "servizio-vendita": "servizio vendita",
    "servizi": "servizi",
    "chi-siamo": "chi siamo",
    "contatti": "contatti",
    "blog": "blog",
    "visite-virtuali": "visite virtuali",
    "landing-consulenza-immobiliare-gratuita": "consulenza gratuita",
}


def link_label(href: str) -> str:
    if href.startswith("blog-"):
        return "articolo correlato"
    return LINK_LABEL.get(href, href.replace("-", " "))

# (titolo soluzione, descrizione, href)
CLUSTER_SOLUTIONS: dict[str, list[tuple[str, str, str]]] = {
    "Acquisto e prima casa": [
        ("Ricerca mirata sul territorio", "Shortlist su Padova e 101 comuni con filtri, foto e tour 360° dove disponibili", "immobili"),
        ("Due diligence pre-compromesso", "Verifica documenti, APE, planimetrie e coerenza prezzo/OMI prima della caparra", "servizio-valutazioni"),
        ("Affiancamento al mutuo", "Coordinamento con banca e notaio su tempi, delibera e rogito senza sorprese", "landing-consulenza-immobiliare-gratuita"),
        ("Visita a distanza", "Tour virtuale e galleria scheda per chi arriva da fuori regione", "visite-virtuali"),
    ],
    "Affitti e locazioni": [
        ("Ricerca locazione personalizzata", "Selezione annunci allineati a budget, zona e tipologia contrattuale", "servizio-locazioni"),
        ("Contratto e registrazione", "Redazione, caparra documentata e consegna chiavi in sicurezza", "servizio-locazioni"),
        ("Qualifica inquilino", "Screening referenze e allineamento canone al mercato FIMAA/OMI", "servizio-gestione"),
        ("Alert nuovi annunci", "Iscrizione alert su catalogo per ricevere proposte in zona", "immobili"),
    ],
    "Vendita": [
        ("Valutazione comparativa", "Stima su comparabili OMI e stock locale — senza listini online", "servizio-valutazioni"),
        ("Piano commercializzazione", "Foto professionali, portali, open house e report settimanale", "servizio-vendita"),
        ("Preparazione immobile", "Home staging leggero e check documenti per accelerare il rogito", "servizio-vendita"),
        ("Gestione trattativa", "Mediazione tra parti su prezzo, tempi e condizioni sospensive", "landing-consulenza-immobiliare-gratuita"),
    ],
    "Mutui e credito": [
        ("Budget e capacità di spesa", "Allineamento rata, spese accessorie e prezzo massimo sostenibile", "landing-consulenza-immobiliare-gratuita"),
        ("Scelta immobile bankable", "Selezione annunci compatibili con perizia e LTV della banca", "immobili"),
        ("Coordinamento rogito", "Timeline compromesso → delibera → atto con notaio e agenzia", "servizio-valutazioni"),
        ("Surroga e rinegoziazione", "Supporto su passaggio tasso fisso/variabile quando previsto dal contratto", "blog-surroga-mutuo-padova-2026"),
    ],
    "Mercato e dati": [
        ("Lettura dati sul tuo caso", "Incrocio articolo con microzona OMI e stock attuale in agenzia", "immobili"),
        ("Consulenza senza impegno", "30 minuti in sede o video per tradurre i numeri in decisione", "landing-consulenza-immobiliare-gratuita"),
        ("Report zona personalizzato", "Prezzi, tempi di vendita e domanda per il tuo comune", "servizio-valutazioni"),
        ("Aggiornamenti periodici", "Alert email su nuovi annunci in linea con i trend del mercato", "immobili"),
    ],
    "Territorio e zone": [
        ("Tour del quartiere", "Visite mirate su zone collegate all'articolo con agente locale", "immobili"),
        ("Scheda zona approfondita", "Collegamenti alle pagine zona OMI con Pro/Contro e FAQ", "blog"),
        ("Valutazione microzona", "Stima €/mq rispetto alla media del quartiere", "servizio-valutazioni"),
        ("Consulenza acquirenti", "Confronto tra due o più zone della provincia sul tuo budget", "landing-consulenza-immobiliare-gratuita"),
    ],
    "Fisco e normativa": [
        ("Checklist documenti", "Elenco operativo per rogito, imposte e conformità catastale", "blog-documenti-compravendita-rogito-padova-2026"),
        ("Supporto preliminare", "Verifica clausole e caparra prima della firma", "servizio-valutazioni"),
        ("Collegamenti istituzionali", "Orientamento su ADE/OMI — senza consulenza fiscale sostitutiva", "landing-consulenza-immobiliare-gratuita"),
        ("Gestione locazione conforme", "Contratti registrati e prassi FIMAA per proprietari", "servizio-locazioni"),
    ],
    "Sostenibilità e APE": [
        ("Due diligence energetica", "Lettura APE, spese future e impatto su mutuo/valore", "servizio-valutazioni"),
        ("Selezione immobili efficienti", "Filtro annunci per classe energetica e interventi possibili", "immobili"),
        ("Vendita case green", "Posizionamento immobile Classe A/B sul mercato padovano", "servizio-vendita"),
        ("Consulenza riqualificazione", "Priorità interventi prima del rogito o dell'affitto", "landing-consulenza-immobiliare-gratuita"),
    ],
    "Investimenti": [
        ("Analisi rendimento locativo", "Confronto canone, spese e imposte su microzona", "blog-rendimento-affitto-padova"),
        ("Selezione asset", "Shortlist box, ville o locali commerciali in provincia", "immobili"),
        ("Gestione locazione", "Inquilino, riscossione e manutenzione ordinaria", "servizio-gestione"),
        ("Due diligence acquisto", "Verifica redditività e stato legale pre-acquisto", "servizio-valutazioni"),
    ],
    "Macro e geopolitica": [
        ("Scenario sul tuo timing", "Acquistare, vendere o attendere — in base al tuo orizzonte", "landing-consulenza-immobiliare-gratuita"),
        ("Protezione patrimonio", "Diversificazione tra prima casa e investimento in provincia", "servizio-valutazioni"),
        ("Monitoraggio tassi", "Aggiornamento su mutuo e capacità d'acquisto reale", "blog-mutui-casa-padova-2026"),
        ("Stock locale aggiornato", "Annunci attivi su Padova e 101 comuni", "immobili"),
    ],
    "Servizi e istituzionale": [
        ("Permuta e timing", "Valutazione simultanea vendita + acquisto", "servizio-vendita"),
        ("Scelta agenzia trasparente", "Mandato scritto, report e canali comunicazione chiari", "chi-siamo"),
        ("Successione immobiliare", "Coordinamento eredi, perizia e messa in vendita", "servizio-vendita"),
        ("Contatto diretto", "WhatsApp e telefono per urgenze operative", "contatti"),
    ],
    "Vita d'agenzia": [
        ("Conoscere il team", "Gino Capon e Linda Righetto — 350+ immobili dal 2000", "chi-siamo"),
        ("Servizi completi", "Vendita, locazione, gestione, valutazioni, virtual tour", "servizi"),
        ("Ultimi ingressi portale", "Annunci residenziali e commerciali appena acquisiti", "immobili"),
        ("Consulenza gratuita", "Primo incontro senza impegno in sede Limena", "landing-consulenza-immobiliare-gratuita"),
    ],
    "Altri / trasversali": [
        ("Orientamento personalizzato", "Capire quale servizio Righetto risponde al tuo quesito", "servizi"),
        ("Catalogo aggiornato", "350+ immobili in vendita e affitto in provincia", "immobili"),
        ("Blog e guide correlate", "Approfondimenti su acquisto, vendita e locazione", "blog"),
        ("Contatto rapido", "Telefono 049.8843484 e form con risposta in giornata", "contatti"),
    ],
}

INTENT_OVERRIDES: dict[str, list[tuple[str, str, str]]] = {
    "affitto-studenti-operativo": [
        ("Checklist affitto studenti", "Contratto transitorio, caparra e registrazione passo passo", "blog-checklist-affitto-studenti-padova-2026"),
        ("Ricerca periferie tram", "Arcella, Guizza, Ponte di Brenta con canoni sotto la media centro", "servizio-locazioni"),
        ("Visita per genitori fuori sede", "Tour 360° prima del contratto", "visite-virtuali"),
        ("Supporto proprietari", "Posizionamento canone e qualifica inquilino", "servizio-locazioni"),
    ],
    "vendita-pillar": [
        ("Valutazione gratuita", "Stima comparativa OMI senza percentuali online", "servizio-valutazioni"),
        ("Piano vendita 90 giorni", "Foto, portali, open house e report", "servizio-vendita"),
        ("Documenti in ordine", "Checklist venditore pre-compromesso", "blog-documenti-vendita-casa"),
        ("Tempi medi zona", "Allineamento aspettative su durata e prezzo", "blog-tempi-vendita-casa-padova"),
    ],
    "acquisto-pillar": [
        ("Guida passo passo", "Dalla pre-delibera al rogito con timeline reale", "blog-comprare-casa-padova-guida-2026"),
        ("Ricerca immobili", "Filtri avanzati e alert nuovi annunci", "immobili"),
        ("Verifiche pre-compromesso", "Impianti, catastale e mutuo", "blog-checklist-verifiche-prima-compromesso-padova-2026"),
        ("Consulenza gratuita", "Primo incontro in agenzia Limena", "landing-consulenza-immobiliare-gratuita"),
    ],
}


def load_skimm() -> dict[str, dict]:
    data = json.loads(SKIMM.read_text(encoding="utf-8"))
    return {a["file"]: a for a in data.get("articles", [])}


def quesito(article: dict) -> str:
    angolo = (article.get("angolo") or "").strip()
    if angolo:
        return f"{angolo} — quali passi concreti con un'agenzia locale?"
    title = (article.get("title") or "").strip()
    return f"{title}: come muoversi in sicurezza nel Padovano?"


def pick_solutions(article: dict) -> list[tuple[str, str, str]]:
    intent = article.get("intent") or ""
    if intent in INTENT_OVERRIDES:
        return INTENT_OVERRIDES[intent]
    cluster = article.get("cluster") or "Altri / trasversali"
    return CLUSTER_SOLUTIONS.get(cluster, CLUSTER_SOLUTIONS["Altri / trasversali"])


def build_block(article: dict) -> str:
    q = quesito(article)
    items = pick_solutions(article)
    lis = "".join(
        f'<li><strong>{t}</strong> — {d} (<a href="{href}">{link_label(href)}</a>)</li>'
        for t, d, href in items[:4]
    )
    return (
        "\n<div class=\"righetto-sol\">\n"
        "<h2>Cosa può fare Righetto</h2>\n"
        f"<p class=\"righetto-sol-quesito\"><strong>Il quesito:</strong> {q}</p>\n"
        f"<ul>{lis}</ul>\n"
        f"{FOOT}\n"
        "</div>\n"
    )


def find_insert_pos(content: str) -> int | None:
    patterns_after = (
        r'<div\s+class="stats-grid"[^>]*>.*?</div>\s*',
        r'<div\s+class="blog-rich-stats"[^>]*>.*?</div>\s*',
        r'<div\s+class="highlight-box"[^>]*>.*?</div>\s*',
        r'<div\s+class="blog-rich-callout"[^>]*>.*?</div>\s*',
        r'<div\s+class="intro-box"[^>]*>.*?</div>\s*',
        r'<div\s+class="toc"[^>]*>.*?</div>\s*',
    )

    for opener, start in (
        (r'<div\s+class="art-content"[^>]*>', None),
        (r"<article[^>]*>", None),
    ):
        m = re.search(opener, content, re.I)
        if not m:
            continue
        base = m.end()
        chunk = content[base:]
        for pattern in patterns_after:
            hit = re.search(pattern, chunk, re.I | re.DOTALL)
            if hit:
                return base + hit.end()
        h2 = re.search(r"<h2[\s>]", chunk, re.I)
        if h2:
            return base + h2.start()
        return base

    m = re.search(r'<main\s+id="main-content"[^>]*>', content, re.I)
    if m:
        chunk = content[m.end() :]
        chat = re.search(r'<div\s+id="chatFlow"', chunk, re.I)
        if chat:
            return m.end() + chat.start()
    return None


def bump_blog_css(content: str) -> str:
    return re.sub(
        r'href="css/blog-rich\.css\?v=\d+"',
        'href="css/blog-rich.css?v=3"',
        content,
    )


def patch_file(path: Path, article: dict) -> bool:
    raw = path.read_text(encoding="utf-8")
    if "righetto-sol" in raw or "Cosa può fare Righetto" in raw:
        return False
    pos = find_insert_pos(raw)
    if pos is None:
        print(f"  SKIP (no art-content): {path.name}", file=sys.stderr)
        return False
    block = build_block(article)
    new_raw = raw[:pos] + block + raw[pos:]
    new_raw = bump_blog_css(new_raw)
    path.write_text(new_raw, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    skimm = load_skimm()
    missing = []
    for f in sorted(ROOT.glob("blog-*.html")):
        t = f.read_text(encoding="utf-8")
        if "righetto-sol" not in t and "Cosa può fare Righetto" not in t:
            missing.append(f)

    priority = [f for f in missing if f.stem in PRIORITY_SLUGS]
    rest = [f for f in missing if f.stem not in PRIORITY_SLUGS]
    order = priority + rest

    patched = 0
    for f in order:
        article = skimm.get(f.name, {
            "file": f.name,
            "title": f.stem.replace("blog-", "").replace("-", " ").title(),
            "angolo": "",
            "cluster": "Altri / trasversali",
            "intent": "",
        })
        if patch_file(f, article):
            tag = "PRIORITY" if f.stem in PRIORITY_SLUGS else "batch"
            print(f"  OK [{tag}] {f.name}")
            patched += 1

    print(f"\nPatch completato: {patched}/{len(missing)} articoli")
    return 0 if patched else 1


if __name__ == "__main__":
    raise SystemExit(main())
