#!/usr/bin/env python3
"""
Genera domande IPOTETICHE per la base di conoscenza di Linda — senza AI, senza costi.

1) Articoli (blog-*.html del sito): per ogni H2/H3 crea una domanda e una risposta
   ESTRATTIVA (primo paragrafo sotto il titolo, testo originale) con link all'articolo.
   Domande molto simili vengono raggruppate (le varianti finiscono nella colonna varianti).
2) Annunci (Supabase, solo colonne pubbliche): rapporto delle informazioni MANCANTI
   nelle schede (cosa Linda non potrebbe dire e quindi rimanderebbe all'agenzia).

Uso:
  python scripts/linda_genera_domande.py --max-per-article 3
Output:
  data/linda-domande-ipotetiche.csv   (importabile da admin-kb.html, arrivano "Da verificare")
  data/linda-lacune-annunci.csv       (campi mancanti per annuncio)
Nessuna scrittura su Supabase. Solo lettura con chiave anon pubblica.
"""
import argparse, csv, difflib, html, io, json, re, sys, urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://righettoimmobiliare.it/"
SB_URL = "https://qwkwkemuabfwvwuqrxlu.supabase.co/rest/v1/"
COLONNE = "codice,tipologia,comune,prezzo,superficie,locali,bagni,piano,anno_costruzione,classe_energetica,spese_condominio,descrizione,attivo,venduto,affittato"


class Sezioni(HTMLParser):
    """Raccoglie title, canonical e coppie (heading, primo paragrafo) dal <main>/<article>/<body>."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""; self.canonical = ""; self.sezioni = []
        self._in_title = False; self._head = None; self._buf = []; self._tag = None
        self._skip = 0; self._cur_head = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "nav", "header", "footer", "form", "noscript"): self._skip += 1
        if tag == "title": self._in_title = True
        if tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href", "")
        if self._skip: return
        if tag in ("h2", "h3", "p"): self._tag = tag; self._buf = []

    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "header", "footer", "form", "noscript") and self._skip: self._skip -= 1
        if tag == "title": self._in_title = False
        if self._skip or tag != self._tag: return
        txt = re.sub(r"\s+", " ", "".join(self._buf)).strip()
        if tag in ("h2", "h3"):
            self._cur_head = txt if txt else None
        elif tag == "p" and self._cur_head and len(txt) >= 80:
            self.sezioni.append((self._cur_head, txt)); self._cur_head = None
        self._tag = None

    def handle_data(self, d):
        if self._in_title: self.title += d
        elif self._tag and not self._skip: self._buf.append(d)


def norm(s):
    s = re.sub(r"[^a-z0-9 ]", "", s.lower().replace("à", "a").replace("è", "e").replace("é", "e").replace("ì", "i").replace("ò", "o").replace("ù", "u"))
    return re.sub(r"\s+", " ", s).strip()


GENERICI = re.compile(r"(?i)^(in sintesi|riepilogo|introduzione|premessa|conclusion|per riassumere|in breve|checklist|fonti|note|prossimi passi)|righetto|condivid|pronto|contattaci|chiamaci|prenota|richied|perch[eé] (leggere|scegliere)|cosa (deve|pu[oò]) fare")


def domanda_da_titolo(h, tutte=False):
    """Ritorna una domanda, oppure None se il titolo non e' una domanda (salvo --tutte)."""
    h = re.sub(r"^\d+[\).\s-]+", "", h).strip().rstrip(":")
    if len(h) < 18 or GENERICI.search(h): return None
    if h.endswith("?"): return h
    if re.match(r"(?i)^(come|cosa|quando|quanto|quali|quale|perch|chi|dove|che |si pu|posso|devo|conviene|serve)", h): return h + "?"
    if not tutte: return None
    return "Cosa devo sapere su: " + h[0].lower() + h[1:] + "?"


def categoria(t):
    t = t.lower()
    for pat, c in [(r"mutu|tass[oi]|surroga", "mutui"), (r"imu|tasse|cedolare|bonus|detrazion|fiscal", "fiscale"),
                   (r"rogito|document|catast|visura|planimetri|ape\b", "documenti"), (r"affitt|locazion|inquilin|contratto", "affitto"),
                   (r"vender|vendita", "vendita"), (r"acquist|compr", "acquisto"), (r"zona|quartier|limena|padova|mercato|omi", "territorio")]:
        if re.search(pat, t): return c
    return "blog"


def articoli(max_per, tutte=False):
    candidati = []
    for p in sorted(ROOT.glob("blog-*.html")):
        if p.name == "blog-articolo.html": continue
        raw = p.read_bytes().decode("utf-8", "ignore")
        s = Sezioni(); s.feed(raw)
        url = s.canonical or (SITE + p.stem)
        url = re.sub(r"\.html$", "", url)
        if not url.startswith("https://righettoimmobiliare.it/"): url = SITE + p.stem
        titolo = re.sub(r"\s*[|—-]\s*Righetto.*$", "", html.unescape(s.title)).strip() or p.stem
        n = 0
        for head, par in s.sezioni:
            if n >= max_per: break
            if re.search(r"(?i)conclusion|faq|domande frequenti|indice|sommario|contatt", head): continue
            dom = domanda_da_titolo(head, tutte)
            if not dom: continue
            n += 1
            candidati.append({"domanda": dom, "risposta": par[:700].rsplit(" ", 1)[0] + ("…" if len(par) > 700 else ""),
                              "categoria": categoria(titolo + " " + head), "fonte_titolo": titolo[:100], "fonte_url": url})
    return candidati


def raggruppa(c):
    gruppi = []
    visti = set()
    for x in c:
        nx = norm(x["domanda"])
        if nx in visti: continue      # stessa domanda in piu' articoli: tieni la prima, evita risposte ambigue
        visti.add(nx)
        for g in gruppi:
            if x["categoria"] == g["categoria"] and difflib.SequenceMatcher(None, nx, norm(g["domanda"])).ratio() >= 0.82:
                if x["domanda"] != g["domanda"] and x["domanda"] not in g["varianti"]: g["varianti"].append(x["domanda"])
                break
        else:
            gruppi.append(dict(x, varianti=[]))
    return gruppi


def lacune_annunci():
    req = urllib.request.Request(SB_URL + "immobili?select=" + COLONNE + "&attivo=eq.true&venduto=eq.false&affittato=eq.false",
                                 headers={"apikey": SB_ANON, "Authorization": "Bearer " + SB_ANON})
    righe = json.load(urllib.request.urlopen(req, timeout=30))
    ok = lambda v: v not in (None, "", 0, "0")
    chiavi = [("prezzo", "prezzo"), ("superficie", "superficie"), ("locali", "locali"), ("bagni", "bagni"), ("piano", "piano"),
              ("anno_costruzione", "anno costruzione"), ("classe_energetica", "classe energetica"), ("spese_condominio", "spese condominiali")]
    out = []
    for r in righe:
        manc = [lab for k, lab in chiavi if not ok(r.get(k))]
        if len(str(r.get("descrizione") or "")) < 200: manc.append("descrizione breve (<200 caratteri)")
        out.append({"codice": r.get("codice"), "comune": r.get("comune"), "tipologia": r.get("tipologia"), "n_mancanti": len(manc), "mancanti": "; ".join(manc)})
    return sorted(out, key=lambda x: -x["n_mancanti"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-per-article", type=int, default=3)
    ap.add_argument("--tutte", action="store_true", help="includi anche titoli non interrogativi (qualita' inferiore)")
    ap.add_argument("--no-annunci", action="store_true", help="salta la lettura di Supabase")
    a = ap.parse_args()
    (ROOT / "data").mkdir(exist_ok=True)

    g = raggruppa(articoli(a.max_per_article, a.tutte))
    with open(ROOT / "data" / "linda-domande-ipotetiche.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        w.writerow(["domanda", "varianti", "risposta", "categoria", "fonte_titolo", "fonte_url", "scade_il"])
        for x in g:
            w.writerow([x["domanda"][:300], "|".join(x["varianti"]), x["risposta"], x["categoria"], x["fonte_titolo"], x["fonte_url"], ""])
    print(f"Domande ipotetiche da articoli: {len(g)} gruppi (varianti raggruppate: {sum(len(x['varianti']) for x in g)})")

    if not a.no_annunci:
        m = re.search(r"SB_ANON\s*=\s*\n?\s*'([^']+)'", (ROOT / "js" / "rig-lead-form.js").read_text(encoding="utf-8"))
        SB_ANON = m.group(1)
        l = lacune_annunci()
        with open(ROOT / "data" / "linda-lacune-annunci.csv", "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["codice", "comune", "tipologia", "n_mancanti", "mancanti"], delimiter=";")
            w.writeheader(); w.writerows(l)
        print(f"Annunci attivi analizzati: {len(l)} — con almeno 1 campo mancante: {sum(1 for x in l if x['n_mancanti'])}")
