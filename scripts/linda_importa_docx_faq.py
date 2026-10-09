#!/usr/bin/env python3
"""
Importa il documento di lavoro "Chatbot_Righetto_Prompt_300_FAQ.docx" nella base di conoscenza di Linda.

Produce (tutto in data/, nessuna rete, nessuna scrittura su Supabase):
  linda-kb-seed-300.csv          300 FAQ pronte per admin-kb.html (arrivano "Da verificare")
  linda-prompt-regole.md         Parte 1 (regole anti-errore) conservata integralmente
  linda-fonti-gerarchia.json     Parte 2 (gerarchia delle fonti)
  linda-linee-guida-redazione.md note INTERNE per chi cura la KB (mai mostrate ai clienti)

Uso:  python scripts/linda_importa_docx_faq.py "C:\\Users\\Utente\\Downloads\\Chatbot_Righetto_Prompt_300_FAQ.docx"
"""
import csv, html, json, re, sys, zipfile
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# categoria del documento -> categoria ammessa dalla KB
CAT = {
    "Vendita e incarico": "vendita",
    "Acquisto e visite": "acquisto",
    "Locazioni e contratti": "affitto",
    "Risoluzione, rinnovi e problemi locativi": "affitto",
    "Preliminare, proposta e caparra": "procedure",
    "Valutazioni, prezzi e mercato": "territorio",
    "Documenti, catasto e conformità": "documenti",
    "Mutui, costi e fiscalità": "mutui",
    "Investimenti e immobili non residenziali": "acquisto",
    "Servizio clienti, privacy e appuntamenti": "azienda",
    "FAQ aggiuntive": "procedure",
}
FONTI = {
    "ade": ("Agenzia delle Entrate", "https://www.agenziaentrate.gov.it/"),
    "omi": ("Osservatorio del Mercato Immobiliare (Agenzia delle Entrate)", "https://www.agenziaentrate.gov.it/portale/web/guest/schede/fabbricatiterreni/omi"),
    "not": ("Consiglio Nazionale del Notariato", "https://www.notariato.it/"),
    "bdi": ("Banca d'Italia", "https://www.bancaditalia.it/"),
    "l431": ("Legge 431/1998 (Normattiva)", "https://www.normattiva.it/atto/caricaDettaglioAtto?atto.codiceRedazionale=098G0483"),
}
RE_FISC = re.compile(r"cedolare|registr|imposta|\bIMU\b|plusvalenz|prima casa|agevolaz|bonus|detrazion|\bIVA\b|RLI", re.I)
RE_LOC = re.compile(r"locazion|affitt|inquilin|canone|transitor|4\+4|3\+2|studenti|sfratt|disdetta|conduttor|locator", re.I)


def fonte_per(q, a, cat):
    t = q + " " + a
    if re.search(r"\bOMI\b|quotazion", t): return "omi"
    if RE_FISC.search(t): return "ade"
    if RE_LOC.search(t) and cat == "affitto": return "l431"
    if cat in ("mutui",) or re.search(r"mutuo|finanzi", t, re.I): return "bdi"
    if cat in ("procedure", "documenti") or re.search(r"rogito|preliminare|notaio|caparra|catast|conformit", t, re.I): return "not"
    return None


# Sinonimi d'uso comune. NON includere termini giuridicamente distinti (es. caparra/acconto, disdetta/recesso).
SINONIMI = [
    ("casa", "appartamento", "immobile", "abitazione"), ("comprare", "acquistare"), ("affittare", "locare", "dare in affitto"),
    ("affitto", "locazione"), ("inquilino", "conduttore"), ("proprietario", "locatore"), ("mutuo", "finanziamento"),
    ("rogito", "atto notarile"), ("APE", "attestato di prestazione energetica", "certificato energetico"),
    ("provvigione", "commissione", "compenso"), ("canone", "affitto mensile"), ("preliminare", "compromesso"),
    ("proposta", "offerta"), ("catasto", "catastale"), ("agenzia", "agenzia immobiliare"),
]
APERTURE = re.compile(r"^(come (posso|si|faccio a|funziona|funzionano)|che cos['’]è|cos['’]è|cosa (significa|sono|succede se|devo|posso)|qual è|quali sono|quali|quanto (costa|devo|può)|posso|devo|è possibile|è obbligatorio|è meglio|chi|quando|dove|perché|cosa)\s+", re.I)


def varianti_per(q):
    """Varianti deterministiche (nessun LLM): forma a parole chiave + sostituzioni di sinonimi. Da rivedere nel pannello."""
    base = q.strip().rstrip("?").strip()
    out = []
    kw = re.sub(r"^(il|lo|la|l['’]|i|gli|le|un|uno|una|un['’])\s*", "", APERTURE.sub("", base).strip(), flags=re.I)
    if 8 <= len(kw) < len(base): out.append(kw)
    for grp in SINONIMI:
        for w in grp:
            m = re.search(r"\b" + re.escape(w) + r"\b", base, re.I)
            if not m: continue
            # con articolo/possessivo davanti il genere potrebbe non concordare: nessuna sostituzione
            if re.search(r"(il|lo|la|l['’]|i|gli|le|un|uno|una|mio|mia|miei|mie|del|della|dello|dei|delle|al|alla|nel|nella|sul|sulla)\s+$", base[:m.start()], re.I): break
            for alt in grp:
                if alt.lower() != w.lower():
                    out.append(base[:m.start()] + alt + base[m.end():])
            break
    seen, res = {q.lower().rstrip("?")}, []
    for v in out:
        k = v.lower().rstrip("?").strip()
        if k not in seen and len(v) <= 140:
            seen.add(k); res.append(v.rstrip("?").strip() + "?" if v is not kw else v)
    return res[:4]


def leggi(docx):
    x = zipfile.ZipFile(docx).read("word/document.xml").decode("utf8")
    x = re.sub(r"<w:br[^>]*/>", "\n", x)
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", x, flags=re.S):
        t = html.unescape("".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, flags=re.S)))
        st = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        out.append((st.group(1) if st else "", t))
    return out


def main(docx):
    righe = leggi(docx)
    # --- Parte 1: prompt ---
    i1 = next(i for i, (s, t) in enumerate(righe) if s == "Heading1" and t.startswith("PARTE 1"))
    i2 = next(i for i, (s, t) in enumerate(righe) if s == "Heading1" and t.startswith("PARTE 2"))
    i3 = next(i for i, (s, t) in enumerate(righe) if s == "Heading1" and t.startswith("PARTE 3"))
    prompt = "\n\n".join(t.strip() for s, t in righe[i1 + 1:i2] if t.strip())
    DATA.mkdir(exist_ok=True)
    (DATA / "linda-prompt-regole.md").write_text(
        "# Regole anti-errore e gestione richiesta — documento del titolare (9 ott 2026)\n\n"
        "> Fonte: Chatbot_Righetto_Prompt_300_FAQ.docx, Parte 1. Conservato integralmente.\n"
        "> Linda NON usa un modello generativo: queste regole sono applicate dal codice (js/linda-kb.js) e dal processo\n"
        "> di approvazione di admin-kb.html. Vedi TEST-SKILL/skill-linda-collega-virtuale.md §9.\n\n" + prompt + "\n", encoding="utf-8")

    # --- Parte 2: fonti ---
    fonti = []
    for s, t in righe[i2 + 1:i3]:
        m = re.match(r"(.+?)\s+[–-]\s+(.+?)\s+(https?://\S+)$", t.strip())
        if m: fonti.append({"fonte": m.group(1), "uso": m.group(2), "url": m.group(3)})
    (DATA / "linda-fonti-gerarchia.json").write_text(json.dumps({"ordine": "dal più autorevole al meno", "fonti": fonti}, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- Parte 3: FAQ ---
    items, cat, cur = [], None, None
    for s, t in righe[i3 + 1:]:
        t = t.strip()
        if s == "Heading2": cat = re.sub(r"\s*[–-].*$", "", t).strip(); continue
        m = re.match(r"(\d+)\.\s*Domanda:\s*(.+)", t)
        if m: cur = {"n": int(m.group(1)), "cat": cat, "q": m.group(2).strip(), "a": ""}; items.append(cur); continue
        if cur and t.startswith("Risposta:") and not cur["a"]: cur["a"] = t[9:].strip(); continue
        if cur and cur["a"] and t and s in ("", "ListBullet"): cur["a"] += " " + t
    assert len(items) == 300, f"attese 300 FAQ, trovate {len(items)}"

    # La FAQ 294 contiene istruzioni interne per chi cura la KB: NON va mostrata ai clienti.
    interno = ""
    for it in items:
        if it["n"] == 294:
            frasi = re.split(r"(?<=\.)\s+", it["a"])
            pubblica = " ".join(frasi[:2])
            interno = it["a"][len(pubblica):].strip()
            it["a"] = pubblica
    (DATA / "linda-linee-guida-redazione.md").write_text(
        "# Linee guida di redazione KB — USO INTERNO (non mostrare ai clienti)\n\n"
        "> Estratto dalla FAQ n. 294 del documento di lavoro: sono istruzioni per chi cura la base di conoscenza.\n\n"
        + "\n\n".join("- " + f for f in re.split(r"(?<=\.)\s+(?=[A-ZÈ])", interno) if f.strip()) + "\n", encoding="utf-8")

    # --- CSV importabile ---
    RE_NUM = re.compile(r"\d+[.,]?\d*\s*(%|€|euro|giorni|mesi|anni)")
    sc = Counter(); senza_fonte_con_numeri = []; nvar = 0
    with open(DATA / "linda-kb-seed-300.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        w.writerow(["domanda", "varianti", "risposta", "categoria", "fonte_titolo", "fonte_url", "scade_il"])
        for it in items:
            c = CAT.get(it["cat"], "procedure")
            if RE_FISC.search(it["q"] + it["a"]) and c not in ("affitto",): c = "fiscale" if c in ("mutui", "procedure", "vendita", "acquisto") and re.search(r"cedolare|imposta|IMU|plusvalenz|prima casa|bonus|detrazion", it["q"] + it["a"], re.I) else c
            k = fonte_per(it["q"], it["a"], c)
            ft, fu = FONTI[k] if k else ("", "")
            if RE_NUM.search(it["q"] + it["a"]) and not k: senza_fonte_con_numeri.append(it["n"])
            sc[c] += 1
            v = varianti_per(it["q"]); nvar += len(v)
            w.writerow([it["q"], "|".join(v), it["a"], c, ft, fu, ""])
    print(f"FAQ importate: {len(items)} | fonti di Parte 2: {len(fonti)}")
    print(f"Varianti generate: {nvar} (media {nvar / len(items):.1f} per voce)")
    print("Per categoria KB:", dict(sc))
    print("Numeri senza fonte:", senza_fonte_con_numeri or "nessuno")


if __name__ == "__main__":
    if len(sys.argv) < 2: sys.exit(__doc__)
    main(sys.argv[1])
