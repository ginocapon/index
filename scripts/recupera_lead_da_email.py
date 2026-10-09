#!/usr/bin/env python3
"""Recupera dalle email i contatti arrivati solo via email e li reinserisce in `richieste`.

Sorgente: cartella con file .eml (o file .mbox) esportati dalla casella info@.
Riconosce gli oggetti "Nuovo contatto dal sito:", "Richiesta immobile:", "Nuovo contatto dal chatbot:"
e gli avvisi "[ATTENZIONE] Lead NON salvato nel CRM:" (stesso lead -> deduplicato).

DEFAULT = DRY-RUN: non scrive nulla, produce solo il report CSV.
Scrittura reale solo con --apply E variabile d'ambiente SUPABASE_SERVICE_KEY (mai nel repo, mai in chat).

Deduplica: (1) nel file sorgente per telefono+email normalizzati, (2) contro il DB (se c'e' la chiave)
per telefono/email gia' presenti. Esclude i contatti di test (nome con TEST / email .invalid).

Uso:
  python scripts/recupera_lead_da_email.py --src C:/export/email            # prova, nessuna scrittura
  set SUPABASE_SERVICE_KEY=...   (PowerShell: $env:SUPABASE_SERVICE_KEY='...')
  python scripts/recupera_lead_da_email.py --src C:/export/email --apply
"""
import argparse, csv, email, html, json, mailbox, os, re, sys, urllib.request, urllib.error, urllib.parse
from datetime import datetime
from email import policy
from email.utils import parsedate_to_datetime
from pathlib import Path

SB_URL = "https://qwkwkemuabfwvwuqrxlu.supabase.co"
SUBJ = re.compile(r"(Nuovo contatto dal (sito|chatbot)|Richiesta immobile|\[ATTENZIONE\] Lead NON salvato)", re.I)
FIELDS = {"nome": "Nome", "telefono": "Telefono", "email": "Email", "messaggio": "Messaggio", "pagina": "Pagina"}


def norm_tel(t):
    d = re.sub(r"\D", "", t or "")
    return d[-10:] if len(d) >= 10 else d


def body_text(msg):
    part = msg.get_body(preferencelist=("html", "plain"))
    raw = part.get_content() if part else ""
    raw = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
    raw = re.sub(r"</?(b|strong|p|div)[^>]*>", "", raw, flags=re.I)
    return html.unescape(re.sub(r"<[^>]+>", "", raw))


def parse_fields(text):
    out = {}
    for key, label in FIELDS.items():
        m = re.search(rf"{label}:\s*(.*?)(?=\n\s*(?:Nome|Telefono|Email|Messaggio|Pagina|Errore DB|Consenso marketing|Sorgente|Interesse|Immobile):|\Z)", text, re.S | re.I)
        if m:
            out[key] = re.sub(r"\s+", " ", m.group(1)).strip(" -")
    return out


def iter_messages(src):
    p = Path(src)
    if p.is_file() and p.suffix.lower() == ".mbox":
        for m in mailbox.mbox(str(p)):
            yield email.message_from_bytes(m.as_bytes(), policy=policy.default)
    else:
        for f in sorted(p.rglob("*.eml")):
            yield email.message_from_bytes(f.read_bytes(), policy=policy.default)


def db_existing(key):
    """Telefoni/email gia' in richieste (richiede service key: l'anon non puo' leggere per RLS)."""
    tel, mail = set(), set()
    h = {"apikey": key, "Authorization": f"Bearer {key}"}
    start = 0
    while True:
        req = urllib.request.Request(f"{SB_URL}/rest/v1/richieste?select=telefono,email&limit=1000&offset={start}", headers=h)
        rows = json.load(urllib.request.urlopen(req, timeout=30))
        for r in rows:
            if r.get("telefono"): tel.add(norm_tel(r["telefono"]))
            if r.get("email"): mail.add(r["email"].strip().lower())
        if len(rows) < 1000: break
        start += 1000
    return tel, mail


def insert(key, row):
    req = urllib.request.Request(f"{SB_URL}/rest/v1/richieste", data=json.dumps([row]).encode(), method="POST",
                                 headers={"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json", "Prefer": "return=minimal"})
    try:
        urllib.request.urlopen(req, timeout=30)
        return "inserito", ""
    except urllib.error.HTTPError as e:
        return "errore", e.read().decode()[:200]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="cartella .eml oppure file .mbox")
    ap.add_argument("--apply", action="store_true", help="scrive davvero in richieste (default: dry-run)")
    ap.add_argument("--report", default=f"report-recupero-lead-{datetime.now():%Y%m%d-%H%M}.csv")
    a = ap.parse_args()

    key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if a.apply and not key:
        sys.exit("ERRORE: --apply richiede SUPABASE_SERVICE_KEY nell'ambiente. Nessuna scrittura eseguita.")
    ex_tel, ex_mail = db_existing(key) if key else (set(), set())
    if not key:
        print("NOTA: senza SUPABASE_SERVICE_KEY il controllo duplicati contro il DB e' saltato (solo dedup nel file).")

    seen, report = set(), []
    for msg in iter_messages(a.src):
        subj = str(msg.get("subject", ""))
        if not SUBJ.search(subj):
            continue
        f = parse_fields(body_text(msg))
        if not f.get("nome") or not (f.get("telefono") or f.get("email")):
            report.append({"data": "", "nome": f.get("nome", ""), "telefono": "", "email": "", "esito": "non-interpretabile", "dettaglio": subj[:80]})
            continue
        try:
            dt = parsedate_to_datetime(str(msg.get("date"))).isoformat()
        except Exception:
            dt = ""
        tel, mail = norm_tel(f.get("telefono")), (f.get("email") or "").strip().lower()
        k = tel or mail
        if re.search(r"\bTEST\b", f["nome"], re.I) or mail.endswith(".invalid"):
            esito = "test-escluso"
        elif k in seen:
            esito = "duplicato-file"
        elif (tel and tel in ex_tel) or (mail and mail in ex_mail):
            esito = "duplicato-db"
        else:
            esito = "da-inserire"
        seen.add(k)
        detail = ""
        if esito == "da-inserire" and a.apply:
            fonte = f.get("pagina") or "sconosciuta"
            row = {"nome": f["nome"], "telefono": f.get("telefono") or None, "email": f.get("email") or None,
                   "messaggio": f"[fonte: recupero-email {fonte}] " + (f.get("messaggio") or ""),
                   "provenienza": "form", "newsletter": False, "letto": False}
            if dt: row["created_at"] = dt
            esito, detail = insert(key, row)
        report.append({"data": dt, "nome": f["nome"], "telefono": f.get("telefono", ""), "email": f.get("email", ""), "esito": esito, "dettaglio": detail})

    with open(a.report, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=["data", "nome", "telefono", "email", "esito", "dettaglio"], delimiter=";")
        w.writeheader(); w.writerows(report)
    tot = {}
    for r in report: tot[r["esito"]] = tot.get(r["esito"], 0) + 1
    print(("APPLICATO" if a.apply else "DRY-RUN (nessuna scrittura)") + " -> " + ", ".join(f"{k}: {v}" for k, v in sorted(tot.items())))
    print("Report:", a.report)


if __name__ == "__main__":
    main()
