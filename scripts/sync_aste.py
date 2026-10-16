#!/usr/bin/env python3
"""Sync aste immobiliari residenziali Veneto -> Supabase tabella aste_immobili.

Fonti (solo lettura, anonime):
  - Portale Vendite Pubbliche (Ministero): ricerca + dettaglio + link documenti
  - astegiudiziarie.it: solo per la foto principale (PVP non espone foto)

Gli hash dei microservizi PVP cambiano a ogni deploy: vengono risolti a runtime
dalla pagina dettaglio + endpoint fe-config (vedi resolve_pvp_endpoints).

Richiede SUPABASE_KEY (service_role) in env o in .env (root o righetto_social/.env).
Uso: python3 scripts/sync_aste.py [--dry-run] [--limit N]
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUPABASE_URL = "https://qwkwkemuabfwvwuqrxlu.supabase.co"
PVP_HOST = "https://pvp.giustizia.it"
PVP_DETAIL_PAGE = PVP_HOST + "/pvp/it/detail_annuncio.page?idAnnuncio=1"
AGI_API = "https://webapi.astegiudiziarie.it"
AGI_SITE = "https://www.astegiudiziarie.it"
REGIONE = "Veneto"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"}
PAUSE = 0.25  # pausa educata tra le chiamate dettaglio


def http_json(url: str, body=None, headers=None, timeout=40):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
    if body is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def http_text(url: str, timeout=40) -> str:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def load_key() -> str:
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if key:
        return key
    for env_path in (ROOT / ".env", ROOT / "righetto_social" / ".env"):
        if env_path.is_file():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("SUPABASE_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SUPABASE_KEY mancante (.env root o righetto_social/.env)")


def to_iso_dt(date_str, time_str=None):
    """Normalizza 'yyyy-mm-dd' o 'dd/mm/yyyy' + opz. 'HH:MM' in ISO 'yyyy-mm-ddTHH:MM'."""
    if not date_str:
        return None
    d = str(date_str).strip()[:10]
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", d)
    if m:
        d = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", d):
        return None
    t = (str(time_str).strip()[:5] if time_str else "") or ""
    return d + ("T" + t if re.match(r"^\d{2}:\d{2}$", t) else "")


# ---------------------------------------------------------------- PVP endpoints
def resolve_pvp_endpoints() -> dict:
    """Risolve gli URL correnti dei microservizi PVP (cambiano a ogni deploy)."""
    page = http_text(PVP_DETAIL_PAGE)
    m = re.search(r'config="({&quot;systemParams&quot;.*?})"', page)
    if not m:
        raise SystemExit("PVP: config bo-ms non trovato nella pagina dettaglio")
    cfg = json.loads(html.unescape(m.group(1)))
    bo = cfg["systemParams"]["api"]["bo-ms"]["url"]  # /bo-<hash>/bo-ms
    fe = http_json(f"{PVP_HOST}{bo}/fe-config/dettaglio-annunci")
    ms = fe.get("msUrl") or {}
    return {
        "host": fe.get("host") or PVP_HOST,
        "ricerca": f"{fe.get('host') or PVP_HOST}/{ms['ricerca']}",
        "vendite": f"{fe.get('host') or PVP_HOST}/{ms['vendite']}",
        "buckets": fe.get("bucketsHost") or "https://resource-pvp.giustizia.it",
    }


# ---------------------------------------------------------------- PVP search
def pvp_search_all(ricerca_url: str) -> list:
    """Tutti gli annunci IMMOBILI in scadenza in Veneto (paginato)."""
    out, page = [], 0
    while True:
        q = urllib.parse.urlencode({"language": "it", "page": page, "size": 100,
                                    "sort": "dataOraVendita,asc"})
        d = http_json(f"{ricerca_url}/ricerca/vendite?{q}", body={
            "tipoLotto": "IMMOBILI", "flagRicerca": 1,
            "regione": REGIONE, "filtroAnnunci": "1"})
        body = d.get("body") or {}
        content = body.get("content") or []
        out.extend(content)
        total_pages = body.get("totalPages") or 1
        page += 1
        if page >= total_pages or not content:
            break
        time.sleep(PAUSE)
    return out


def pvp_detail(vendite_url: str, buckets: str, annuncio_id: int) -> dict:
    d = http_json(f"{vendite_url}/vendite/{annuncio_id}/restricted?language=it")
    b = d.get("body") or {}
    docs = []
    for a in (b.get("allegati") or []):
        link = a.get("linkAllegato") or ""
        if not link:
            continue
        docs.append({
            "nome": a.get("nomeFile") or "",
            "tipo": a.get("descrizione") or a.get("codiceTipoAllegato") or "",
            "url": buckets + urllib.parse.quote(link, safe="/?=&"),
            "dimensione": a.get("dimensioneAllegato"),
        })
    proc = b.get("procedura") or {}
    beni = b.get("beni") or []
    indirizzo_bene = ""
    if beni:
        ind = beni[0].get("indirizzo") or {}
        indirizzo_bene = " ".join(x for x in [ind.get("via"), ind.get("cap"),
                                              ind.get("citta"), ind.get("provincia")] if x)
    data_term = b.get("dataTermPresOff")
    ora_term = b.get("oraTermPresOff")
    return {
        "documenti": docs,
        "modalita_vendita": b.get("descModVendita") or "",
        "termine_offerte": to_iso_dt(data_term, ora_term),
        "proc_num": proc.get("numeRg"),
        "proc_anno": proc.get("numeAnnoRg"),
        "indirizzo_bene": indirizzo_bene,
        "data_term_raw": data_term,
        "ora_term_raw": ora_term,
    }




# ------------------------------------------------------------- tipologia bene
# La categoria catastale PVP e' troppo generica ("Abitazione di tipo civile"):
# la tipologia utile si ricava dalla descrizione del lotto. Se nessuna regola
# combacia -> "altro" (mai inventare).
TIPOLOGIA_RULES = [
    ("bifamiliare/villa", r"villetta|villino|\bvilla\b|bifamiliare|trifamiliare|quadrifamiliare|a schiera"),
    ("rustico/casale", r"rustic|casolare|casale|colonica|fienile"),
    ("appartamento", r"appartament|\battico\b|mansarda|monolocale|bilocale|trilocale|quadrilocale|\bloft\b"),
    ("casa", r"\bcasa\b|\bcasetta\b|unifamiliare"),
    ("box/garage", r"\bbox\b|garage|autorimessa|posto auto|posti auto"),
    ("ufficio", r"uffici"),
    ("negozio", r"negozi"),
    ("capannone", r"capannon"),
    ("magazzino", r"magazzin"),
    ("laboratorio", r"laboratori"),
    ("terreno", r"terren[oi]|edificabil"),
]


def classify_tipologia(desc: str) -> str:
    t = (desc or "").lower()
    for label, rx in TIPOLOGIA_RULES:
        if re.search(rx, t):
            return label
    return "altro"

# ------------------------------------------------------- foto da astegiudiziarie
def agi_foto_index() -> dict:
    """Mappa (tribunale_lower, num_procedura, anno) -> url foto, per il Veneto residenziale."""
    body = {"tipoRicerca": 0, "indirizzo": None, "latitudine": None, "longitudine": None,
            "latitudineNW": None, "longitudineNW": None, "latitudineSE": None,
            "longitudineSE": None, "noGeo": False, "idEsperimentoVendita": None,
            "idTipologie": [1], "tipologia": None, "idCategorie": [], "categoria": None,
            "descrizione": None, "comune": None, "provincia": None, "regione": REGIONE,
            "cap": None, "ricercaCap": None, "prezzoDa": None, "prezzoA": None,
            "priceMax": 0, "priceSteps": None, "tipologie": None, "idTribunale": None,
            "tribunale": None, "numeroProcedura": None, "annoProcedura": None,
            "ruolo": None, "idTipologiaProcedura": None, "giudice": None,
            "professionista": None, "idTipologiaVendita": None, "idModalitaVendita": None,
            "idPubblicazione": None, "dataVenditaDa": None, "dataVenditaA": None,
            "codiceAsta": None, "hasFoto": True, "hasPlanimetrie": None,
            "hasVirtualTour": None, "hasVideo": None, "bandita": None, "telematica": None,
            "inScadenza": None, "lottoUnico": None, "venditeAGI": None, "storica": False,
            "vetrina": False, "sezione": None, "searchOnMap": False, "tribunali": None,
            "tipologieProcedura": None, "tipologieVendita": None, "modalitaVendita": None,
            "numeroPubblicazioni": None, "listaIdLotto": None, "idProcedura": None,
            "orderBy": 6}
    headers = {"Origin": AGI_SITE, "Referer": AGI_SITE + "/"}
    lots = http_json(f"{AGI_API}/api/Search/Map", body=body, headers=headers)
    ids = [x["idLotto"] for x in lots if x.get("idLotto")]
    index = {}
    for i in range(0, len(ids), 20):
        time.sleep(PAUSE)
        for it in http_json(f"{AGI_API}/api/Search/Data", body=ids[i:i + 20], headers=headers):
            foto = it.get("urlPhoto")
            trib = (it.get("tribunale") or "").strip().lower()
            num = str(it.get("numeroProcedura") or "").strip()
            anno = it.get("annoProcedura")
            if foto and trib and num:
                index[(trib, num, anno)] = AGI_SITE + foto
    return index


# ---------------------------------------------------------------- Supabase
def sb_upsert(rows: list, key: str):
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/aste_immobili?on_conflict=id_pvp",
        data=json.dumps(rows).encode(), method="POST",
        headers={"apikey": key, "Authorization": f"Bearer {key}",
                 "Content-Type": "application/json",
                 "Prefer": "resolution=merge-duplicates,return=minimal"})
    with urllib.request.urlopen(req, timeout=120) as r:
        r.read()


def sb_get_existing(key: str) -> list:
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/aste_immobili?select=id_pvp,hash_cambio,attivo",
        headers={"apikey": key, "Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def sb_deactivate(ids: list, key: str):
    if not ids:
        return
    flt = ",".join(str(i) for i in ids)
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/aste_immobili?id_pvp=in.({flt})",
        data=json.dumps({"attivo": False, "updated_at": "now()"}).encode(), method="PATCH",
        headers={"apikey": key, "Authorization": f"Bearer {key}",
                 "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req, timeout=120) as r:
        r.read()


# ---------------------------------------------------------------- main
def main():
    dry = "--dry-run" in sys.argv
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    print("[1/5] Risoluzione endpoint PVP…")
    ep = resolve_pvp_endpoints()
    print("  ricerca:", ep["ricerca"])

    print("[2/5] Ricerca annunci Veneto in scadenza…")
    found = pvp_search_all(ep["ricerca"])
    resid = [x for x in found if x.get("categoriaLotto") == "IMMOBILE_RESIDENZIALE"]
    print(f"  trovati {len(found)} immobili, residenziali {len(resid)}")
    if limit:
        resid = resid[:limit]

    key = "" if dry else load_key()
    existing = {} if dry else {r["id_pvp"]: r for r in sb_get_existing(key)}

    print("[3/5] Indice foto da astegiudiziarie…")
    try:
        foto_idx = agi_foto_index()
        print(f"  {len(foto_idx)} procedure con foto")
    except Exception as e:
        print(f"  foto non disponibili ({e}); continuo senza")
        foto_idx = {}

    print("[4/5] Dettagli e upsert…")
    rows, seen_ids, n_new, n_skip = [], set(), 0, 0
    for x in resid:
        aid = x["id"]
        seen_ids.add(aid)
        ind = x.get("indirizzo") or {}
        dt = x.get("dataOraVendita")
        hash_src = json.dumps(["v2", x.get("prezzoBaseAsta"), dt, x.get("offertaMinima"),
                               x.get("descLotto"), x.get("disponibilita")], sort_keys=True)
        h = hashlib.sha1(hash_src.encode()).hexdigest()[:12]
        old = existing.get(aid)
        if old and old.get("hash_cambio") == h and old.get("attivo"):
            n_skip += 1
            continue
        try:
            det = pvp_detail(ep["vendite"], ep["buckets"], aid)
        except Exception as e:
            print(f"  dettaglio {aid} fallito: {e}")
            det = {"documenti": [], "modalita_vendita": "", "termine_offerte": None,
                   "proc_num": None, "proc_anno": None, "indirizzo_bene": ""}
        time.sleep(PAUSE)
        trib_city = re.sub(r"^tribunale di\s+", "", (x.get("tribunale") or "").lower())
        proc_num = det.get("proc_num") or x.get("procedura")
        foto = foto_idx.get((trib_city, str(proc_num or ""), det.get("proc_anno")))
        rows.append({
            "id_pvp": aid,
            "prezzo_base": x.get("prezzoBaseAsta"),
            "offerta_minima": x.get("offertaMinima"),
            "rialzo_minimo": x.get("rialzoMinimo"),
            "data_asta": dt,
            "termine_offerte": det.get("termine_offerte"),
            "data_pubblicazione": x.get("dataPubblicazione"),
            "comune": ind.get("citta") or "",
            "provincia": ind.get("provincia") or "",
            "indirizzo": det.get("indirizzo_bene") or ind.get("via") or "",
            "latitudine": (ind.get("coordinate") or {}).get("latitudine"),
            "longitudine": (ind.get("coordinate") or {}).get("longitudine"),
            "descrizione": (x.get("descLotto") or "")[:4000],
            "tipologia": classify_tipologia(x.get("descLotto") or ""),
            "tipologia_bene": ", ".join(x.get("categoriaBene") or []),
            "disponibilita": ", ".join(x.get("disponibilita") or []),
            "tribunale": x.get("tribunale") or "",
            "procedura": f"{proc_num}/{det.get('proc_anno')}" if proc_num else "",
            "modalita_vendita": det.get("modalita_vendita") or "",
            "link_dettaglio": f"{PVP_HOST}/pvp/it/detail_annuncio.page?idAnnuncio={aid}",
            "documenti": det.get("documenti") or [],
            "foto_url": foto or "",
            "foto_fonte": "astegiudiziarie.it" if foto else "",
            "attivo": True,
            "hash_cambio": h,
            "updated_at": "now()",
        })
        n_new += 1
        if len(rows) >= 50:
            if not dry:
                sb_upsert(rows, key)
            print(f"  upsert blocco da {len(rows)} (nuovi/aggiornati: {n_new})")
            rows = []
    if rows and not dry:
        sb_upsert(rows, key)

    print("[5/5] Disattivo annunci non più in scadenza…")
    stale = [i for i, r in existing.items() if r.get("attivo") and i not in seen_ids]
    if stale and not dry:
        sb_deactivate(stale, key)

    print(f"FINE: {len(found)} totali Veneto, {len(resid)} residenziali, "
          f"{n_new} upsert, {n_skip} invariati, {len(stale)} disattivati"
          + (" [DRY-RUN]" if dry else ""))


if __name__ == "__main__":
    main()
