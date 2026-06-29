# -*- coding: utf-8 -*-
"""Genera 2 articoli acquisizioni (residenziale + commerciale) — giugno 2026.
Esegui da repo root: python scripts/build_acquisizioni_giugno16.py
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

DATE_IT = "16 giugno 2026"
DATE_ISO = "2026-06-16"
TIME_TS = "2026-06-16T09:00:00+02:00"
DATA_PORTALE = "16 giugno 2026"
DATE_MOD_ISO = "2026-06-16"

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((Path(__file__).parent / "acquisizioni_giugno16_data.json").read_text(encoding="utf-8"))

STYLE_ACQ = r"""<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--nero:#152435;--bianco:#F7F5F1;--oro:#FF6B35;--grigio:#6B7A8D;--gc:#E1DBD1;--sfondo:#ECE7DF;--blu:#2C4A6E;--oro2:#FF8F5E}
body{font-family:'Montserrat',sans-serif;background:var(--bianco);color:var(--nero)}
header{background:var(--nero);position:sticky;top:0;z-index:100}
.hi{max-width:1380px;margin:0 auto;padding:0 1.5rem;height:74px;display:flex;align-items:center;gap:2rem}
.logo{font-family:'Cormorant Garamond',serif;color:#fff;font-size:1.28rem;font-weight:600}.logo span{color:var(--oro);font-style:italic}
nav{display:flex;flex:1;gap:.2rem}nav a{color:rgba(255,255,255,.72);font-size:.81rem;padding:.4rem .72rem}nav a.active{color:var(--oro)}
.h-btn{background:var(--oro);color:var(--nero);padding:.4rem .88rem;border-radius:6px;font-size:.76rem;font-weight:600}
.art-hero{position:relative}.art-hero-img{width:100%;height:420px;object-fit:cover;display:block}
.art-hero-overlay{position:absolute;inset:auto 0 0 0;padding:2.2rem 1.5rem;background:linear-gradient(transparent,rgba(21,36,53,.94))}
.art-hero-inner{max-width:820px;margin:0 auto}
.breadcrumb{font-size:.72rem;color:rgba(255,255,255,.45);margin-bottom:.86rem}.breadcrumb a{color:rgba(255,255,255,.55)}
.cat-badge{font-size:.57rem;letter-spacing:.12em;text-transform:uppercase;background:rgba(255,107,53,.2);color:var(--oro);padding:.24rem .68rem;font-weight:700;display:inline-block;margin-bottom:.72rem}
.art-hero h1{font-family:'Cormorant Garamond',serif;font-size:1.95rem;font-weight:300;color:#fff;line-height:1.2}.art-hero h1 strong{font-weight:600;font-style:italic}
.art-hero-meta{display:flex;gap:1rem;align-items:center;font-size:.8rem;color:rgba(255,255,255,.5);margin-top:.92rem;flex-wrap:wrap}
.av{width:36px;height:36px;border-radius:50%;background:var(--oro);display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--nero)}
.art-container{max-width:820px;margin:0 auto;padding:2.4rem 1.5rem 3.55rem}
.art-content{font-size:.91rem;line-height:1.88}
.art-content h2{font-family:'Cormorant Garamond',serif;font-size:1.68rem;margin:2.28rem 0 .68rem;border-bottom:2px solid var(--oro);padding-bottom:.34rem}
.art-content h3{font-size:1.1rem;color:var(--blu);margin:1.15rem 0 .35rem}
.art-content p{margin-bottom:1.04rem}.art-content ul,.art-content ol{margin:0 0 1rem 1.28rem}
.art-content a{color:var(--blu);text-decoration:underline}
.art-content table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.84rem}
.art-content th,.art-content td{border:1px solid var(--gc);padding:.55rem .65rem;text-align:left}
.art-content th{background:var(--sfondo)}
.aeo-box{border:2px solid var(--blu);border-radius:12px;padding:1.15rem 1.3rem;margin-bottom:1.65rem;background:linear-gradient(135deg,rgba(44,74,110,.07),rgba(255,107,53,.06))}
.aeo-box h2{font-family:'Montserrat',sans-serif;font-size:.95rem;text-transform:uppercase;letter-spacing:.06em;color:var(--blu);margin:0 0 .55rem;border:none;padding:0}
.acq-block{margin:2rem 0 2.5rem;padding-bottom:2rem;border-bottom:1px solid var(--gc)}
.acq-block:last-of-type{border-bottom:none}
.acq-preview{width:100%;max-height:340px;object-fit:cover;border-radius:12px;margin:.6rem 0 1rem;display:block}
.acq-meta{font-size:.82rem;color:var(--grigio);margin:.35rem 0 .85rem;line-height:1.6}
.acq-fatti{background:var(--sfondo);border:1px solid var(--gc);border-radius:10px;padding:.9rem 1.1rem;margin:1rem 0;font-size:.84rem}
.acq-fatti ul{margin:.4rem 0 0 1.1rem}
.acq-cta{display:inline-flex;margin-top:.65rem;font-weight:700;font-size:.8rem;background:var(--blu);color:#fff;padding:.55rem 1.1rem;border-radius:8px;text-decoration:none}
.acq-cta:hover{opacity:.92}
.tag-row{display:flex;flex-wrap:wrap;gap:.45rem;margin:1.5rem 0}
.tag-row span{font-size:.72rem;background:var(--sfondo);border:1px solid var(--gc);padding:.28rem .62rem;border-radius:999px;color:var(--blu);font-weight:600}
.cta-deep{display:inline-flex;background:linear-gradient(180deg,var(--oro2),var(--oro));color:var(--nero);font-weight:800;padding:.8rem 1.62rem;border-radius:10px;font-size:.8rem;margin:1rem .75rem 1rem 0}
.faq-item{border:1px solid var(--gc);border-radius:8px;margin-bottom:.5rem}
.faq-q{padding:.86rem .98rem;font-weight:600;font-size:.84rem;cursor:pointer}.faq-a{max-height:0;overflow:hidden;transition:max-height .35s;background:var(--sfondo)}
.faq-item.open .faq-a{max-height:420px}.faq-a-inner{padding:0 .98rem .86rem;font-size:.83rem;color:var(--grigio)}
.author-bio{display:flex;gap:1.08rem;padding:1.38rem;border:1px solid rgba(44,74,110,.12);border-radius:12px;margin:1.68rem 0}
.related{background:var(--sfondo);border:1px solid var(--gc);padding:1.32rem;border-radius:10px}
footer{background:linear-gradient(180deg,var(--nero),#0d1a2a);color:rgba(255,255,255,.65);padding:2.35rem 1.5rem;font-size:.75rem}
.skip-link{position:absolute;top:-100%;background:var(--oro);color:var(--nero);padding:.46rem .9rem;z-index:9999}.skip-link:focus{top:0}
.kpi-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:.55rem;margin:1.2rem 0 1.6rem}
.kpi-strip div{background:var(--sfondo);border:1px solid var(--gc);border-radius:10px;padding:.75rem .85rem;text-align:center}
.kpi-strip strong{display:block;font-family:'Cormorant Garamond',serif;font-size:1.35rem;color:var(--blu)}
.kpi-strip span{font-size:.62rem;letter-spacing:.06em;text-transform:uppercase;color:var(--grigio)}
.portale-nav{display:flex;flex-wrap:wrap;gap:.45rem;margin:1rem 0 1.8rem}
.portale-nav a{font-size:.72rem;font-weight:600;background:#fff;border:1px solid var(--gc);color:var(--blu);padding:.35rem .75rem;border-radius:999px;text-decoration:none}
.portale-nav a:hover{border-color:var(--oro);color:var(--nero)}
.sec-divider{display:flex;align-items:center;gap:.75rem;margin:2.4rem 0 1rem}
.sec-divider h2{margin:0;border:none;padding:0;font-size:1.45rem}
.sec-divider::after{content:'';flex:1;height:1px;background:var(--gc)}
.acq-card{border:1px solid var(--gc);border-radius:14px;padding:1.15rem 1.2rem 1.35rem;margin:1.35rem 0;background:#fff;box-shadow:0 8px 24px rgba(21,36,53,.05)}
.acq-card.is-spotlight{border-color:var(--oro);box-shadow:0 10px 28px rgba(255,107,53,.12)}
.acq-card-head{display:flex;flex-wrap:wrap;align-items:center;gap:.45rem;margin-bottom:.55rem}
.seg-chip{font-size:.58rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;padding:.2rem .55rem;border-radius:999px}
.seg-res{background:rgba(44,74,110,.12);color:var(--blu)}
.seg-com{background:rgba(255,107,53,.15);color:#9a3d12}
.seg-evi{background:var(--oro);color:var(--nero)}
.acq-card h3{font-family:'Cormorant Garamond',serif;font-size:1.22rem;margin:0;line-height:1.3;color:var(--nero)}
.acq-card .acq-preview{border-radius:10px;margin:.75rem 0 1rem}
@media(max-width:600px){.art-hero-img{height:260px}.kpi-strip{grid-template-columns:repeat(2,1fr)}}
</style>
<link rel="stylesheet" href="css/blog-lead-form.css?v=1">"""

FOOTER = """
</main>
<footer><div class="fi">&copy; 2026 Gruppo Immobiliare Righetto — P.IVA 05182390285 — Via Roma 96, Limena (PD)</div></footer>
<script>document.querySelectorAll('.faq-q').forEach(function(q){q.addEventListener('click',function(){var p=this.parentElement,o=p.classList.contains('open');document.querySelectorAll('.faq-item.open').forEach(function(x){x.classList.remove('open');});if(!o)p.classList.add('open');});});</script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="js/config.js?v=4"></script>
<script src="js/rig-lead-form.js?v=1"></script>
<script src="js/nav-mobile.js?v=3" defer></script>
<script src="js/cookie-consent.js?v=3" defer></script>
</body></html>
"""

RES_TOP5 = [p for p in DATA["res"] if p.get("codice")][:5]
COM_TOP5 = DATA["com"][:5]

RES_BY_CODE = {p["codice"]: p for p in DATA["res"] if p.get("codice")}
COM_BY_CODE = {p["codice"]: p for p in DATA["com"]}

# Mix portale v2: Grisignano in evidenza + 4 residenziali + 2 uffici affitto + 1 capannone (ordine acquisizione commerciale)
RES_MIX_ORDER = ["LP0285-V", "LP0286", "LA0317", "LP0283", "LP0281"]
COM_MIX_PICK = ["UFF2105a", "CAP1609a", "uff2189a"]
RES_MIX = [RES_BY_CODE[c] for c in RES_MIX_ORDER]
COM_MIX = [COM_BY_CODE[c] for c in COM_MIX_PICK]


def word_count(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split()) if text else 0


def fmt_eur(n: int | float | None, affitto: bool = False) -> str:
    if n is None:
        return "su richiesta"
    s = f"{int(n):,}".replace(",", ".")
    return f"€{s}/mese" if affitto else f"€{s}"


def fmt_stato(s: str | None) -> str:
    if not s:
        return "da verificare"
    return s.replace("_", " ")


def is_affitto(p: dict) -> bool:
    op = (p.get("tipo_operazione") or "").lower()
    return "affitto" in op or (p.get("prezzo") or 0) < 5000


def meta_line(p: dict) -> str:
    aff = is_affitto(p)
    parts = [f"<strong>{fmt_eur(p.get('prezzo'), aff)}</strong>"]
    if p.get("superficie"):
        parts.append(f"<strong>{p['superficie']} mq</strong>")
    if p.get("locali"):
        parts.append(f"{p['locali']} locali")
    if p.get("bagni"):
        parts.append(f"{p['bagni']} bagni")
    parts.append(p.get("tipologia") or "immobile")
    parts.append(f"stato <strong>{fmt_stato(p.get('stato'))}</strong>")
    if p.get("classe_energetica"):
        ce = f"classe <strong>{p['classe_energetica']}</strong>"
        if p.get("ipe_kwh"):
            ce += f" (IPE {p['ipe_kwh']} kWh/m²a)"
        parts.append(ce)
    if p.get("garage"):
        parts.append("<strong>garage</strong>")
    if p.get("giardino"):
        g = "<strong>giardino</strong>"
        if p.get("mq_giardino"):
            g += f" {p['mq_giardino']} mq"
        parts.append(g)
    if p.get("piano"):
        parts.append(str(p["piano"]))
    return " · ".join(parts)


def acq_block(idx: int, p: dict, paras: list[str], fatti: list[str], alt: str, segment: str = "res", spotlight: bool = False) -> str:
    cod = p["codice"]
    slug = p["slug"]
    tit = p["titolo"]
    seg_cls = "seg-res" if segment == "res" else "seg-com"
    seg_lbl = "Residenziale" if segment == "res" else "Commerciale"
    chips = f'<span class="seg-chip {seg_cls}">{seg_lbl}</span>'
    if spotlight:
        chips += '<span class="seg-chip seg-evi">In evidenza</span>'
    card_cls = "acq-card is-spotlight" if spotlight else "acq-card"
    body = "".join(f"<p>{t}</p>" for t in paras)
    fli = "".join(f"<li>{f}</li>" for f in fatti)
    img = p.get("foto0") or ""
    load = "eager" if idx == 1 else "lazy"
    cta_lbl = "Apri scheda" if segment == "res" else "Vedi scheda"
    return f"""<article class="{card_cls}" id="{cod.lower().replace(' ', '')}">
  <div class="acq-card-head">{chips}<span style="font-size:.68rem;color:var(--grigio);margin-left:auto">#{idx} · {escape(cod)}</span></div>
  <h3>{escape(tit)}</h3>
  <img class="acq-preview" src="{escape(img)}" alt="{escape(alt)}" width="820" height="340" loading="{load}">
  <p class="acq-meta">{meta_line(p)}</p>
  {body}
  <div class="acq-fatti"><strong>In sintesi operativa</strong><ul>{fli}</ul></div>
  <a class="acq-cta" href="immobile?s={escape(slug)}">{cta_lbl} {escape(cod)} — foto e planimetrie</a>
</article>"""


def faq_html(faqs: list[tuple[str, str]]) -> str:
    items = "".join(
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>'
        for q, a in faqs
    )
    return f'<div id="faq" style="margin-top:2rem"><h2 style="font-family:\'Cormorant Garamond\',serif;font-size:1.62rem;border-bottom:2px solid var(--oro);margin-bottom:.9rem">Domande frequenti</h2>{items}</div>'


def lead_form(slug: str, ids: tuple[str, str, str, str, str]) -> str:
    n, t, e, m, g = ids
    return f"""<section class="blog-lead-wrap" id="richiedi-consulenza" aria-labelledby="blog-lead-title">
  <h2 id="blog-lead-title">Richiedi informazioni su un immobile o una valutazione</h2>
  <form data-rig-lead-form data-provenienza="{slug}" data-pagina="{slug}" data-msg-prefix="[Blog]" novalidate>
    <div class="bl-fields">
      <label for="{n}">Nome e cognome *</label>
      <input type="text" id="{n}" required autocomplete="name" placeholder="Mario Rossi">
      <label for="{t}">Telefono *</label>
      <input type="tel" id="{t}" required autocomplete="tel" placeholder="333 123 4567">
      <label for="{e}">Email</label>
      <input type="email" id="{e}" autocomplete="email" placeholder="mario@email.it">
      <label for="{m}">Messaggio (opzionale)</label>
      <textarea id="{m}" placeholder="Immobile di interesse, comune, vendita o acquisto…"></textarea>
      <label class="bl-chk"><input type="checkbox" id="{g}" required> Acconsento al trattamento dei dati (GDPR). <a href="privacy-policy">Privacy</a></label>
      <button type="submit">Invia richiesta</button>
    </div>
    <div class="rig-lead-success">
      <h3>Messaggio inviato!</h3>
      <p>Grazie. Ti ricontattiamo entro pochi minuti negli orari di apertura.</p>
    </div>
  </form>
</section>"""


RES_NARRATIVES = {
    "LP0286": {
        "alt": "Casa singola ristrutturata Altichiero Padova LP0286 — anteprima portale Righetto",
        "paras": [
            "Pubblicata a fine maggio 2026, questa <strong>villetta indipendente</strong> ad <strong>Altichiero</strong> è il punto di riferimento per chi cerca metrature ampie senza cantieri: circa <strong>230 mq</strong> su un unico livello, con finiture aggiornate e impianti moderni.",
            "Via Beato Arnaldo da Limena collega il quartiere verde di Padova nord alla tangenziale e ai servizi quotidiani. Garage e giardino privato completano un profilo «pronto abitare» adatto a famiglie numerose o a chi vuole spazi hobby e lavoro da casa.",
            "In visita verifichiamo orientamento, spese e documentazione APE classe <strong>C</strong>: elementi che incidono su mutuo e tempi di rogito. Per il contesto di mercato del quartiere, utile incrociare con le <a href=\"https://www.agenziaentrate.gov.it\" target=\"_blank\" rel=\"noopener noreferrer\">quotazioni OMI</a> e la nostra guida <a href=\"blog-quartieri-padova-2026\">quartieri Padova 2026</a>.",
        ],
        "fatti": [
            "Tipologia: casa singola ristrutturata, 8 vani, 2 bagni.",
            "Quartiere: Altichiero (PD) — contesto residenziale verde.",
            "Pertinenze: garage e giardino circa 300 mq.",
            "Target: famiglia che vuole entrare senza ristrutturazione.",
        ],
    },
    "LP0285-V": {
        "alt": "Casa su due livelli con giardino Grisignano di Zocco LP0285 — anteprima Righetto",
        "paras": [
            "A <strong>Grisignano di Zocco</strong> proponiamo una <strong>casa singola su due livelli</strong> per circa <strong>140 mq</strong>, con <strong>sei locali</strong> e ampio scoperto recintato — ideale per chi cerca privacy a pochi minuti da Padova est.",
            "L'immobile è <strong>da ristrutturare</strong>: offre margine progettuale su distribuzione interna ed efficientamento energetico (oggi classe <strong>F</strong>). Il prezzo di <strong>€110.000</strong> colloca l'annuncio tra le opportunità più accessibili del portafoglio residenziale attuale.",
            "Fronte Viale Kennedy garantisce visibilità e accesso; in trattativa consigliamo sempre un preventivo lavori prima dell'offerta vincolante. Per chi confronta il comune, utile leggere anche le dinamiche di <a href=\"blog-compravendite-italia-q1-agenzia-entrate-2026-padova\">compravendite Q1 2026</a> sul territorio veneto.",
        ],
        "fatti": [
            "Layout: 6 locali su due piani — flessibilità per nuclei familiari.",
            "Giardino privato ampio — raro a questa fascia di prezzo.",
            "Stato: da ristrutturare — budget lavori da quantificare.",
            "Target: prima casa con progetto di personalizzazione.",
        ],
    },
    "LA0317": {
        "alt": "Quadrilocale ristrutturato Mandria Padova LA0317 — anteprima fotografica",
        "paras": [
            "In <strong>Mandria</strong>, zona residenziale tranquilla del comune di Padova, pubblichiamo un <strong>quadrilocale al secondo piano</strong> già <strong>ristrutturato</strong> per circa <strong>90 mq</strong>. Palazzina silenziosa, ambienti luminosi e finiture curate: profilo adatto a coppie e famiglie con tempi di ingresso brevi.",
            "Via Rovereto offre servizi di prossimità e collegamenti rapidi verso centro e tangenziale. Il prezzo di <strong>€200.000</strong> posiziona l'offerta nella fascia media del quartiere: in agenzia confrontiamo sempre spese condominiali, luce naturale e orientamento con altre proposte Mandria/Sacrocuore.",
            "Documentazione APE classe <strong>E</strong> in scheda. Per chi acquista con mutuo, incrociare rata aggiornata con <a href=\"blog-bce-tassi-mutui-giugno-2026-padova\">BCE e mutui giugno 2026</a> e simulazione in <a href=\"landing-mutuo\">landing mutuo</a>.",
        ],
        "fatti": [
            "Piano: secondo — verificare esigenze mobilità in famiglia.",
            "Stato: ristrutturato — impianti e finiture aggiornati.",
            "Uso ideale: prima casa o base familiare stabile.",
            "Quartiere: Mandria — contesto villette e servizi.",
        ],
    },
    "LP0283": {
        "alt": "Porzione bifamiliare Sacrocuore Padova LP0283 — anteprima portale",
        "paras": [
            "Nel quartiere <strong>Sacrocuore</strong> proponiamo una <strong>porzione di bifamiliare indipendente</strong> su un unico piano per circa <strong>100 mq</strong>, con <strong>doppi servizi</strong> e <strong>giardino</strong> riservato — combinazione richiesta da famiglie padovane che vogliono privacy senza gestire un'intera villa.",
            "L'unità è <strong>ristrutturata</strong> (classe energetica <strong>D</strong>), fattore che facilita perizia mutuo e rogito. Sacrocuore resta tra i rioni consolidati per domanda familiare, scuole e commercio di quartiere.",
            "Per approfondire prezzi e contesto locale: <a href=\"blog-mercato-sacrocuore-padova-omi-2026\">Sacrocuore e OMI 2026</a>. In visita valutiamo accessi indipendenti, spese e conformità urbanistica con la documentazione in scheda.",
        ],
        "fatti": [
            "Tipologia: porzione bifamiliare — ingresso indipendente.",
            "Bagni: 2 — comfort per famiglia o home office.",
            "Giardino privato circa 200 mq.",
            "Target: giardino in città con budget inferiore alla villetta intera.",
        ],
    },
    "LP0281": {
        "alt": "Porzione bifamiliare Montà Padova LP0281 con terrazza — anteprima Righetto",
        "paras": [
            "A <strong>Montà</strong>, quartiere residenziale di Padova, acquisiamo una <strong>porzione di bifamiliare</strong> su due livelli per circa <strong>160 mq</strong> con <strong>terrazza abitabile</strong>, garage e scoperto — soluzione per chi cerca spazi generosi con possibilità di personalizzazione.",
            "L'immobile è <strong>da ristrutturare</strong> (classe <strong>G</strong>): il prezzo di <strong>€145.000</strong> riflette lo stato grezzo e apre margine per efficientamento e redistribuzione interna. Via Magellano offre contesto tranquillo con collegamenti verso il centro.",
            "Montà si colloca tra le zone di cintura urbana richieste da famiglie che bilanciano prezzo e metrature. Prima dell'offerta consigliamo sopralluogo tecnico su copertura, terrazza e impianti: passo standard nelle trattative Righetto.",
        ],
        "fatti": [
            "Metrature: circa 160 mq su due livelli, 5 locali.",
            "Pertinenze: garage, giardino, terrazza abitabile.",
            "Stato: da ristrutturare — progetto su misura.",
            "Target: acquirente con visione di riqualificazione e ampliamento outdoor.",
        ],
    },
}

COM_NARRATIVES = {
    "UFF2105a": {
        "alt": "Ufficio in affitto Limena UFF2105a — anteprima Righetto Immobiliare",
        "paras": [
            "A <strong>Limena</strong>, sede di Righetto Immobiliare, proponiamo in <strong>affitto</strong> un <strong>ufficio di circa 90 mq</strong> in contesto direzionale, con soppalco e travatura a vista. Classe energetica <strong>B</strong> e spese condominiali contenute (circa €60/mese) rendono l'offerta interessante per studi professionali e piccole imprese.",
            "Canone richiesto: <strong>€800/mese + IVA</strong>. Parcheggio comodo nello stabile e posizione strategica tra Padova e provincia nord. Limena beneficia di ottimi collegamenti sulla viabilità principale verso il capoluogo.",
            "Per imprese che valutano location e costi fissi, confrontare sempre vincoli contrattuali, destinazione d'uso e oneri accessori prima della proposta. Il segmento uffici in affitto nel Padovano resta attivo su fasce 60–150 mq.",
        ],
        "fatti": [
            "Contratto: affitto commerciale, canone €800/mese + IVA.",
            "Superficie: circa 90 mq, 2 locali + servizio.",
            "Classe B — IPE 16,5 kWh/m²a.",
            "Target: professionisti, consulenti, PMI servizi.",
        ],
    },
    "CAP1609a": {
        "alt": "Capannone industriale Rubano CAP1609a — anteprima portale Righetto",
        "paras": [
            "A <strong>Rubano</strong> vendiamo un <strong>capannone di circa 550 mq</strong> con lotto indipendente aggiuntivo di <strong>3.500 mq</strong> (pavimentazione in ghiaia compattata, non cementificato). Uffici al primo piano; attualmente suddiviso in due unità con possibilità di reunificazione.",
            "Prezzo richiesto: <strong>€360.000</strong>. Stato <strong>da ristrutturare</strong>, classe <strong>G</strong> — adatto ad artigiani, logistica leggera o investitori che vogliono modulare gli spazi produttivi. Ingresso carraio indipendente sul lotto.",
            "Rubano è tra i comuni della cintura ovest con forte domanda artigianale e collegamento rapido verso Padova. Per due diligence: verificare destinazione urbanistica, accessi pesanti e conformità impianti con tecnico prima del compromesso.",
        ],
        "fatti": [
            "Superficie capannone: circa 550 mq + lotto 3.500 mq.",
            "Comune: Rubano — cintura ovest padovana.",
            "Layout: due unità reunibili, uffici al piano superiore.",
            "Target: attività produttive, deposito, investimento industriale leggero.",
        ],
    },
    "CAP1687": {
        "alt": "Capannone cemento armato Limena CAP1687 — anteprima fotografica",
        "paras": [
            "Nel comune di <strong>Limena</strong> proponiamo in <strong>vendita</strong> un <strong>capannone in cemento armato di circa 1.200 mq</strong> con uffici annessi, su due lotti per circa <strong>3.000 mq</strong> complessivi. Altezza media <strong>5 metri</strong>, <strong>doppio accesso carraio</strong>, immobile in buono stato di manutenzione strutturale.",
            "Prezzo richiesto: <strong>€730.000</strong>. Al momento <strong>locato a azienda referenziata</strong>: profilo adatto a investitori che cercano reddito da locazione industriale oltre alla rivalutazione del comparto. Posizione su area produttiva servita.",
            "Il segmento capannoni nel Padovano resta legato alla domanda manifatturiera veneta. Per valutazioni comparative usiamo transazioni verificabili e visite con accesso ai vani tecnici — non stime generiche da portali.",
        ],
        "fatti": [
            "Superficie: circa 1.200 mq capannone + uffici.",
            "Lotti: circa 3.000 mq complessivi.",
            "Stato locativo: affittato a società referenziata.",
            "Target: investitore income o operatore che rileva going concern.",
        ],
    },
    "uff2189a": {
        "alt": "Ufficio open space Limena uff2189a — secondo piano zona industriale",
        "paras": [
            "In <strong>Via dell'Industria</strong> a Limena affittiamo un <strong>ufficio di circa 140 mq</strong> al secondo piano, con <strong>quattro vani</strong> e servizio. Canone <strong>€1.100/mese</strong>, classe energetica <strong>F</strong> — tipologia adatta a team che necessitano open space modulabile.",
            "La zona industriale di Limena concentra studi tecnici, logistica di servizio e piccole imprese del Padovano nord. Parcheggi e accessi carrai nelle vicinanze facilitano operatività quotidiana.",
            "Prima della firma del contratto commerciale verificare destinazione d'uso, spese condominiali e vincoli di sublocazione. Righetto segue anche locazioni commerciali per proprietari e inquilini: <a href=\"servizio-locazioni\">servizio locazioni</a>.",
        ],
        "fatti": [
            "Affitto: €1.100/mese, circa 140 mq.",
            "Zona: Limena industriale — Via dell'Industria.",
            "4 locali + bagno — layout flessibile.",
            "Target: PMI, studi associati, back-office.",
        ],
    },
    "NEG2173a": {
        "alt": "Locale commerciale in affitto Limena NEG2173a — anteprima vetrina",
        "paras": [
            "Sempre nel comparto <strong>Via delle Industrie</strong> a Limena, proponiamo un <strong>locale commerciale</strong> di circa <strong>150 mq</strong> in <strong>affitto</strong> a <strong>€1.200/mese</strong>. Due vani principali e servizio, stato <strong>buono</strong>, classe <strong>F</strong>.",
            "Il negozio si presta a attività di vicinato, showroom leggero o servizi alla persona, con visibilità su area ad alto passaggio veicolare. Limena cresce come hub residenziale e commerciale a ridosso di Padova: domanda locale stabile.",
            "Per inquilini e investitori, il punto critico resta il <strong>contratto commerciale</strong> (durata, rinnovi, oneri). In agenzia affianchiamo la trattativa con documentazione ordine e verifica urbanistica — senza pubblicare tariffe di mediazione online.",
        ],
        "fatti": [
            "Canone: €1.200/mese, 150 mq circa.",
            "Tipologia: negozio / locale commerciale.",
            "Posizione: Limena, zona industriale e servizi.",
            "Target: retail, servizi, attività artigianali con vetrina.",
        ],
    },
}


def build_mix_body() -> str:
    res_blocks = []
    for i, p in enumerate(RES_MIX, 1):
        n = RES_NARRATIVES[p["codice"]]
        res_blocks.append(acq_block(i, p, n["paras"], n["fatti"], n["alt"], segment="res", spotlight=(p["codice"] == "LP0285-V")))
    res_html = "\n".join(res_blocks)

    com_blocks = []
    for j, p in enumerate(COM_MIX, len(RES_MIX) + 1):
        n = COM_NARRATIVES[p["codice"]]
        com_blocks.append(acq_block(j, p, n["paras"], n["fatti"], n["alt"], segment="com"))
    com_html = "\n".join(com_blocks)

    return f"""
<div class="aeo-box">
<h2>In sintesi</h2>
<p style="font-size:.84rem;margin:0 0 .6rem">Tour aggiornato del <strong>portale Righetto Immobiliare</strong> al <strong>{DATA_PORTALE}</strong>: <strong>5 proposte residenziali</strong> (con <strong>Grisignano di Zocco in apertura</strong>), più <strong>2 uffici in affitto</strong> a Limena e un <strong>capannone</strong> a Rubano — foto, prezzi e link scheda.</p>
<ul style="font-size:.84rem">
<li><strong>8 incarichi attivi</strong> in un unico articolo: vendita abitativa + commerciale</li>
<li>Residenziale: da <strong>€110.000</strong> (Grisignano) a <strong>€365.000</strong> (Altichiero)</li>
<li>Commerciale in ordine di acquisizione: UFF2105a → CAP1609a → uff2189a</li>
</ul>
</div>

<div class="kpi-strip" aria-label="Numeri selezione portale">
  <div><strong>8</strong><span>schede attive</span></div>
  <div><strong>5</strong><span>residenziali</span></div>
  <div><strong>3</strong><span>commerciali</span></div>
  <div><strong>101</strong><span>comuni serviti</span></div>
</div>

<nav class="portale-nav" aria-label="Salta alla sezione">
  <a href="#lp0285-v">Grisignano</a>
  <a href="#residenziale">Tutte le case</a>
  <a href="#commerciale">Uffici e capannone</a>
  <a href="#confronto">Tabella rapida</a>
  <a href="#faq">FAQ</a>
</nav>

<p>Questo formato <strong>portale mix</strong> sostituisce la versione solo residenziale: stesso URL, layout a card più leggibile su mobile e desktop, con segmentazione chiara tra abitazioni e spazi professionali. I dati provengono dal database portale (Supabase) — non sono stime di mercato inventate.</p>
<p>Il contesto macro resta quello del Q1 2026: compravendite nazionali <strong>+4,4%</strong> (Agenzia delle Entrate) e mutuo al <strong>47,8%</strong> delle operazioni — approfondimento in <a href="blog-compravendite-italia-q1-agenzia-entrate-2026-padova">compravendite Q1 2026</a>. Per il racconto agenzia: <a href="blog-righetto-storia-territorio-acquisizioni-2026">storia Righetto e acquisizioni</a>.</p>

<div class="sec-divider" id="residenziale"><h2>Residenziale — 5 case e appartamenti</h2></div>
<p>Apriamo con <strong>LP0285-V a Grisignano di Zocco</strong>: casa su due livelli con ampio scoperto a prezzo di ingresso, poi le altre quattro acquisizioni residenziali più recenti tra Padova città e provincia.</p>
{res_html}

<div class="sec-divider" id="commerciale"><h2>Commerciale — uffici in affitto e capannone</h2></div>
<p>Dopo il blocco residenziale, tre proposte <strong>commerciali</strong> in ordine di acquisizione sul portale: due <strong>uffici in affitto</strong> a Limena (zona direzionale e industriale) e un <strong>capannone in vendita</strong> a Rubano con lotto ampio. Per l'elenco completo solo commerciale vedi anche <a href="blog-ultime-acquisizioni-commerciali-padova-giugno-2026">articolo commerciali giugno 2026</a>.</p>
{com_html}

<h2 id="confronto">Confronto rapido — tutte le schede</h2>
<table>
<thead><tr><th>Codice</th><th>Segmento</th><th>Zona</th><th>Prezzo / canone</th><th>Nota</th></tr></thead>
<tbody>
<tr><td>LP0285-V</td><td>Residenziale</td><td>Grisignano di Zocco</td><td>€110.000</td><td>In evidenza — 6 locali, da ristrutturare</td></tr>
<tr><td>LP0286</td><td>Residenziale</td><td>Padova Altichiero</td><td>€365.000</td><td>Villetta ristrutturata 230 mq</td></tr>
<tr><td>LA0317</td><td>Residenziale</td><td>Padova Mandria</td><td>€200.000</td><td>Quadrilocale ristrutturato</td></tr>
<tr><td>LP0283</td><td>Residenziale</td><td>Padova Sacrocuore</td><td>€230.000</td><td>Bifamiliare con giardino</td></tr>
<tr><td>LP0281</td><td>Residenziale</td><td>Padova Montà</td><td>€145.000</td><td>Terrazza, da ristrutturare</td></tr>
<tr><td>UFF2105a</td><td>Commerciale</td><td>Limena</td><td>€800/mese + IVA</td><td>Ufficio ~90 mq, classe B</td></tr>
<tr><td>CAP1609a</td><td>Commerciale</td><td>Rubano</td><td>€360.000</td><td>Capannone ~550 mq + lotto</td></tr>
<tr><td>uff2189a</td><td>Commerciale</td><td>Limena</td><td>€1.100/mese</td><td>Ufficio ~140 mq, 4 vani</td></tr>
</tbody>
</table>

<h2>Come prenotare visita o richiedere documenti</h2>
<ol>
<li>Sfoglia <a href="immobili">tutto il portale</a> o apri la scheda dal codice incarico (es. LP0285-V).</li>
<li>Chiama <a href="tel:+390498843484">049.88.43.484</a> o usa il form in fondo pagina indicando codice e fascia oraria.</li>
<li>Per residenziale con mutuo: simulazione rata (<a href="landing-mutuo">landing mutuo</a>) e pre-approvazione banca.</li>
<li>Per uffici: verifica destinazione d'uso e spese prima della proposta locazione.</li>
<li>Per capannone: sopralluogo tecnico su accessi carrai e stato copertura.</li>
</ol>

<h2>Perché Grisignano apre la selezione</h2>
<p>LP0285-V concentra ciò che molti acquirenti cercano nel 2026: <strong>metrature generose</strong>, <strong>scoperto privato</strong> e prezzo sotto la soglia psicologica dei €150.000 nel Padovano. È da ristrutturare — quindi richiede budget lavori esplicito — ma offre margine progettuale raro a questa cifra. Per confronto con il capoluogo, le guide zona e OMI restano il riferimento istituzionale prima di formulare offerta.</p>

<h2>Acquirente residenziale: APE, mutuo e stato immobile</h2>
<p>Chi punta a LP0286 o LA0317 (già ristrutturati) ha percorso mutuo più lineare; chi valuta LP0285-V o LP0281 deve integrare preventivo impresa. La quota mutuo al <strong>47,8%</strong> nel Q1 2026 (ADE) conferma il ruolo del credito, senza sostituire due diligence su conformità e spese. Tassi aggiornati: <a href="blog-bce-tassi-mutui-giugno-2026-padova">BCE e mutui giugno 2026</a>. Per prima casa, incrociare requisiti con <a href="blog-agevolazioni-prima-casa-2026">agevolazioni prima casa 2026</a> e simulazione personalizzata in sede.</p>

<h2>Imprenditore e professionista: uffici Limena</h2>
<p>UFF2105a e uff2189a coprono fasce diverse (90 mq studio elegante vs 140 mq open space modulabile). Canoni €800 e €1.100/mese vanno letti con IVA, spese e durata contratto commerciale — tema affrontato in <a href="servizio-locazioni">servizio locazioni</a> Righetto. Limena resta hub tra Padova e cintura nord: parcheggi e viabilità sono variabili decisive in visita.</p>

<h2>Capannone Rubano: profilo operativo</h2>
<p>CAP1609a unisce capannone diviso in due unità reunibili, uffici al piano superiore e lotto esterno di circa 3.500 mq. Prezzo <strong>€360.000</strong> per ~550 mq coperti posiziona l'offerta nel segmento artigianale/logistica leggera della cintura ovest. Stato da ristrutturare e classe G impongono analisi impianti e destinazione urbanistica con tecnico prima del compromesso.</p>

<h2>Venditore: come entra un nuovo incarico</h2>
<p>Ogni scheda elencata nasce da mandato dopo <strong>valutazione comparativa</strong> e shooting professionale. Il compenso di mediazione si concorda <strong>nel mandato</strong> — non pubblichiamo listini online. Valutazione gratuita: <a href="landing-valutazione">landing valutazione</a>.</p>

<h2>Virtual tour e gallerie fotografiche</h2>
<p>Le schede portale includono gallerie navigabili (swipe su anteprima) e, dove disponibile, <a href="visite-virtuali">visite virtuali 360°</a>. L'articolo integra il racconto; i dati ufficiali restano sempre in scheda immobile.</p>

<h2>Microzone residenziali in sintesi</h2>
<p><strong>Altichiero (LP0286)</strong> — villetta ristrutturata su un livello, target famiglie che vogliono entrare senza cantiere. <strong>Mandria (LA0317)</strong> — quadrilocale silenzioso, prima casa con servizi di quartiere. <strong>Sacrocuore (LP0283)</strong> — porzione bifamiliare con doppi servizi e giardino in città. <strong>Montà (LP0281)</strong> — metrature ampie e terrazza, trade-off ristrutturazione. Incrociare sempre con <a href="blog-quartieri-padova-2026">guida quartieri Padova 2026</a> per contesto prezzi.</p>

<h2>Domande che riceviamo in agenzia</h2>
<p><strong>«Posso visitare Grisignano e Padova lo stesso giorno?»</strong> — Sì, se gli appuntamenti sono compatibili: segnala priorità e budget per un giro efficiente.</p>
<p><strong>«LP0284 è disponibile?»</strong> — LP0284-V non risulta attivo; in evidenza c'è LP0285-V, profilo analogo su due livelli.</p>
<p><strong>«Gli uffici sono arredati?»</strong> — Stato in scheda; in visita verifichiamo impianti, soppalco e spese condominiali.</p>
<p><strong>«Il capannone è divisibile?»</strong> — CAP1609a oggi in due unità con possibilità di reunificazione — da confermare in trattativa con progetto d'uso.</p>

<h2>Collegamenti utili sul sito</h2>
<p>Filtra <a href="immobili?op=vendita">vendita</a> o <a href="immobili?op=affitto">affitto</a> per tipologia; per capannoni e uffici usa i filtri avanzati in <a href="immobili">catalogo completo</a>. Servizi correlati: <a href="servizio-vendita">vendita</a>, <a href="servizio-locazioni">locazioni commerciali</a>, <a href="landing-valutazione">valutazione gratuita</a>. Checklist acquirente: <a href="blog-checklist-verifiche-prima-compromesso-padova-2026">verifiche pre-compromesso Padova</a>.</p>

<h2>Checklist rapida prima dell'offerta</h2>
<ul>
<li><strong>Residenziale:</strong> APE, planimetria, spese condominiali, agibilità.</li>
<li><strong>Ufficio:</strong> destinazione d'uso, contratto commerciale, spese e parcheggio.</li>
<li><strong>Capannone:</strong> accessi carrai, altezze, portate pavimento, vincoli urbanistici.</li>
</ul>
<p>Supporto documentale in trattativa riservata; acquirente libero di nominare tecnico e notaio di fiducia.</p>

<h2>Numeri Righetto (claim verificati)</h2>
<table>
<thead><tr><th>Indicatore</th><th>Valore</th></tr></thead>
<tbody>
<tr><td>Operatività</td><td>Dal <strong>2000</strong>, sede Limena (PD)</td></tr>
<tr><td>Portafoglio</td><td><strong>350+</strong> immobili gestiti</td></tr>
<tr><td>Territorio</td><td><strong>101</strong> comuni</td></tr>
<tr><td>Soddisfazione</td><td><strong>98%</strong></td></tr>
<tr><td>Recensioni Google</td><td><strong>127</strong> · media <strong>4,9/5</strong></td></tr>
</tbody>
</table>

<div class="tag-row" aria-label="Keyword social">
  <span>#RighettoImmobiliare</span><span>#CasePadova</span><span>#GrisignanoDiZocco</span>
  <span>#UfficioLimena</span><span>#CapannonePadova</span><span>#Acquisizioni2026</span><span>#Padova</span>
</div>
<p style="font-size:.8rem;color:var(--grigio)"><em>Ultimo aggiornamento: {DATE_IT}. Prezzi e disponibilità come da portale; verificare scheda immobile prima di visita o proposta.</em></p>
<a class="cta-deep" href="immobili">Sfoglia portale</a>
<a class="cta-deep" href="immobili?op=vendita" style="background:var(--blu);color:#fff">Solo vendita</a>
<a class="cta-deep" href="landing-valutazione" style="background:var(--nero);color:#fff">Valutazione gratuita</a>
"""


def build_res_body() -> str:
    blocks = []
    for i, p in enumerate(RES_TOP5, 1):
        n = RES_NARRATIVES[p["codice"]]
        blocks.append(acq_block(i, p, n["paras"], n["fatti"], n["alt"]))
    acq_html = "\n".join(blocks)
    return f"""
<div class="aeo-box">
<h2>In sintesi</h2>
<p style="font-size:.84rem;margin:0 0 .6rem">Selezione delle <strong>ultime 5 acquisizioni residenziali</strong> attive sul portale Righetto Immobiliare al <strong>{DATA_PORTALE}</strong>: villette, appartamenti e porzioni di bifamiliare tra Padova città e provincia, con anteprima fotografica e link alla scheda completa.</p>
<ul style="font-size:.84rem">
<li>Ordine per <strong>data di inserimento</strong> nel database portale (Supabase)</li>
<li>Mix <strong>ristrutturato</strong> e <strong>da ristrutturare</strong> — fasce da €110.000 a €365.000</li>
<li>Per il racconto agenzia completo: <a href="blog-righetto-storia-territorio-acquisizioni-2026">storia Righetto e acquisizioni 2026</a></li>
</ul>
</div>

<h2>Perché un focus solo residenziale</h2>
<p>Il portale Righetto pubblica <strong>vendita e locazione</strong> su <strong>101 comuni</strong> del Padovano. Questo articolo raccoglie le <strong>cinque proposte abitative più recenti</strong> ancora attive, distinte dall'articolo istituzionale che mescola storia agenzia e mix tipologie. Qui trovi solo <strong>case e appartamenti</strong> per famiglie, prima casa e investitori locativi residenziali.</p>
<p>Il mercato locale nel primo semestre 2026 mostra domanda sostenuta su abitazione principale: i dati ADE del Q1 segnano <strong>+4,4%</strong> di compravendite nazionali e quota mutuo al <strong>47,8%</strong> — contesto utile in <a href="blog-compravendite-italia-q1-agenzia-entrate-2026-padova">compravendite Q1 2026</a>. A Padova, cintura e quartieri consolidati (Altichiero, Mandria, Sacrocuore, Montà) restano tra le aree con maggiore richiesta di visite qualificate.</p>

<h2>Come leggere le schede: prezzo, stato e APE</h2>
<p>Ogni scheda riporta prezzo richiesto, metrature, numero locali, stato manutentivo e <strong>classe energetica</strong> quando disponibile. Non sono promesse di rendimento o tempi di vendita garantiti: sono dati dell'incarico alla data di pubblicazione. Prima di un'offerta vincolante consigliamo sempre seconda visita, verifica documenti e — per immobili da ristrutturare — preventivo lavori.</p>
<table>
<thead><tr><th>Segmento</th><th>Profilo acquirente</th><th>Attenzione in visita</th></tr></thead>
<tbody>
<tr><td>Ristrutturato</td><td>Chi vuole rogito rapido</td><td>APE, spese, conformità impianti</td></tr>
<tr><td>Da ristrutturare</td><td>Chi ha budget lavori</td><td>Struttura, tetto, umidità, preventivi</td></tr>
<tr><td>Villetta / bifamiliare</td><td>Famiglie con spazio outdoor</td><td>Scoperto, recinzioni, accessi carraio</td></tr>
<tr><td>Appartamento</td><td>Prima casa in città</td><td>Condominio, ascensore, rumore</td></tr>
</tbody>
</table>

<h2>Le ultime 5 acquisizioni residenziali: tour guidato</h2>
<p>Di seguito le proposte in ordine cronologico di caricamento sul portale. Clicca sulla scheda per galleria fotografica, planimetrie e contatto visita.</p>
{acq_html}

<h2>Zone e collegamenti nel Padovano</h2>
<p>Le acquisizioni coprono <strong>Padova città</strong> (Altichiero, Mandria, Sacrocuore, Montà) e <strong>Grisignano di Zocco</strong> in provincia est. Per ogni area pubblichiamo guide zona con prezzi orientativi OMI e FAQ locali: <a href="zona-limena">Limena</a>, <a href="zona-arcella-padova">Arcella</a>, <a href="zona-sacra-famiglia-padova">Sacra Famiglia</a>, <a href="zona-vigonza">Vigonza</a>.</p>
<p>Chi vende un immobile residenziale segue lo stesso percorso descritto in <a href="servizio-vendita">servizio vendita</a>: valutazione in sede, shooting professionale, pubblicazione multicanale e gestione trattativa. Il compenso di mediazione si concorda <strong>nel mandato</strong> — non pubblichiamo listini online.</p>

<h2>Acquirente: prossimi passi operativi</h2>
<ol>
<li>Filtrare su <a href="immobili?op=vendita">immobili in vendita</a> per comune, prezzo e tipologia.</li>
<li>Prenotare visita con riferimento al <strong>codice incarico</strong> (es. LP0286).</li>
<li>Per mutuo: pre-approvazione e simulazione rata aggiornata (<a href="landing-mutuo">landing mutuo</a>).</li>
<li>Per immobili da ristrutturare: preventivo tecnico prima dell'offerta.</li>
<li>Inviare richiesta tramite form in fondo pagina o <a href="tel:+390498843484">049.88.43.484</a>.</li>
</ol>

<h2>Confronto rapido delle cinque proposte</h2>
<p>Per orientarsi senza aprire subito tutte le schede, ecco una lettura comparativa basata sui dati portale — non su promesse di apprezzamento futuro.</p>
<table>
<thead><tr><th>Codice</th><th>Comune / zona</th><th>Prezzo</th><th>Profilo</th></tr></thead>
<tbody>
<tr><td>LP0286</td><td>Padova Altichiero</td><td>€365.000</td><td>Villetta ristrutturata, 230 mq — pronto abitare</td></tr>
<tr><td>LP0285-V</td><td>Grisignano di Zocco</td><td>€110.000</td><td>6 locali, da ristrutturare — prezzo ingresso</td></tr>
<tr><td>LA0317</td><td>Padova Mandria</td><td>€200.000</td><td>Quadrilocale ristrutturato, 90 mq</td></tr>
<tr><td>LP0283</td><td>Padova Sacrocuore</td><td>€230.000</td><td>Bifamiliare con giardino, 2 bagni</td></tr>
<tr><td>LP0281</td><td>Padova Montà</td><td>€145.000</td><td>Bifamiliare con terrazza, da ristrutturare</td></tr>
</tbody>
</table>
<p>La forbice di prezzo (da €110.000 a €365.000) riflette metrature, stato e pertinenze — non solo il comune. Un appartamento ristrutturato in Mandria compete con altre soluzioni semicentro solo se il budget e le esigenze di spazio outdoor coincidono.</p>

<h2>Mutuo, prima casa e tempi di decisione nel 2026</h2>
<p>Con i tassi aggiornati a giugno 2026 (vedi <a href="blog-bce-tassi-mutui-giugno-2026-padova">BCE e mutui</a>), la sensibilità alla rata resta elevata. Chi punta a LP0286 o LA0317 beneficia di perizie più lineari su immobili già ristrutturati; chi valuta LP0285-V o LP0281 deve integrare nel budget il costo lavori, spesso con preventivo vincolante di impresa prima dell'offerta.</p>
<p>La quota nazionale di operazioni con mutuo al <strong>47,8%</strong> nel Q1 2026 (dati ADE) conferma che il credito resta centrale, ma non sostituisce la due diligence sull'immobile: conformità urbanistica, APE e spese ricorrenti vanno letti insieme alla simulazione bancaria.</p>

<h2>Venditore residenziale: come entra un nuovo incarico</h2>
<p>Le acquisizioni elencate sono il risultato di mandati concordati con i proprietari dopo <strong>valutazione comparativa</strong> sul segmento (villetta, appartamento, porzione bifamiliare). Il flusso standard prevede sopralluogo, raccolta documenti, shooting fotografico professionale, pubblicazione su sito e portali, gestione visite e trattativa fino al rogito.</p>
<p>Non pubblichiamo tempi di vendita garantiti né prezzi «suggeriti» privi di comparabili verificati. Se vuoi affidarci un immobile residenziale, la <a href="landing-valutazione">valutazione gratuita</a> è il primo passo: in sede definiamo strategia di prezzo e piano di promozione coerente con OMI e stock locale.</p>

<h2>Virtual tour e materiale digitale</h2>
<p>Dove disponibile, integriamo schede con gallerie ad alta risoluzione e — per incarichi selezionati — <a href="visite-virtuali">visite virtuali</a> o video. L'obiettivo è ridurre visite non qualificate e offrire al compratore distante un primo livello di ispezione utile, senza sostituire il sopralluogo reale prima del compromesso.</p>

<h2>Microzone in dettaglio: dove sono le cinque proposte</h2>
<h3>Altichiero (LP0286)</h3>
<p>Quartiere residenziale a nord del capoluogo, con forte componente verde e villette. Altichiero attrae famiglie che vogliono indipendenza senza allontanarsi eccessivamente da Padova: collegamenti verso tangenziale e servizi di quartiere sono un punto di forza ricorrente nelle visite. La proposta LP0286 rappresenta il segmento alto di metratura «chiavi in mano».</p>
<h3>Grisignano di Zocco (LP0285-V)</h3>
<p>Comune della campagna orientale, a breve distanza da Padova est. Qui il mercato premia metri di scoperto a prezzi inferiori al capoluogo: LP0285-V punta su acquirenti con progetto di ristrutturazione e budget lavori esplicito. Confrontare sempre con OMI comunale prima di formulare offerta.</p>
<h3>Mandria (LA0317)</h3>
<p>Zona residenziale interna al comune di Padova, apprezzata per tranquillità e mix villette-condomini bassi. Il quadrilocale ristrutturato intercetta domanda di prima casa e famiglie che evitano cantieri: in visita è essenziale valutare ascensori, parcheggio e spese condominiali rispetto a Sacrocuore o Arcella.</p>
<h3>Sacrocuore (LP0283)</h3>
<p>Rione consolidato con domanda familiare stabile, vicino a scuole e commercio di prossimità. La porzione di bifamiliare con doppi servizi e giardino risponde a nicchia «privacy in città» a prezzo inferiore alla villetta intera. Approfondimento mercato: <a href="blog-mercato-sacrocuore-padova-omi-2026">Sacrocuore OMI 2026</a>.</p>
<h3>Montà (LP0281)</h3>
<p>Area residenziale di Padova con villette e porzioni di bifamiliare, collegamenti verso nord-est città. LP0281 offre terrazza abitabile e garage — elementi outdoor richiesti — con trade-off di ristrutturazione interna. Adatto a chi ha tempo e capitale per personalizzare gli ambienti.</p>

<h2>Domande che ci fanno in agenzia su queste proposte</h2>
<p><strong>«LP0284 è ancora disponibile?»</strong> — L'incarico LP0284-V a Grisignano risulta al momento non attivo sul portale; in questa selezione compare la proposta gemella LP0285-V, sempre a Grisignano, con profilo analogo su due livelli.</p>
<p><strong>«Posso visitare più immobili in un'unica uscita?»</strong> — Sì, se gli appuntamenti sono compatibili con disponibilità chiavi e percorsi: segnalaci priorità e budget per organizzare un giro efficiente.</p>
<p><strong>«Inviate documenti prima della visita?»</strong> — Ape e planimetria sono in scheda; visura e documenti proprietà vengono condivisi in fase di seria intenzione, nel rispetto privacy venditore.</p>
<p><strong>«Accettate proposte con mutuo al 100%?»</strong> — Dipende da banca, reddito e perizia: non è decisione dell'agenzia ma del creditore; consigliamo pre-approvazione.</p>

<h2>Checklist documenti per l'acquirente residenziale</h2>
<p>Prima del compromesso, oltre alla visita emotiva, conviene allineare un pacchetto minimo di verifiche — tema trattato anche in <a href="blog-checklist-verifiche-prima-compromesso-padova-2026">checklist pre-compromesso Padova</a>:</p>
<ol>
<li><strong>APE</strong> e classe energetica coerenti con scheda e impianti visibili.</li>
<li><strong>Planimetria catastale</strong> conforme allo stato di fatto.</li>
<li><strong>Spese condominiali</strong> e ultimo bilancio (per appartamenti).</li>
<li><strong>Agibilità / conformità</strong> urbanistica per ville e bifamiliari.</li>
<li><strong>Assenza vincoli</strong> ipotecari o trascrizioni pregiudizievoli — verifica notarile.</li>
</ol>
<p>In agenzia supportiamo la raccolta documentale lato venditore; l'acquirente resta libero di nominare tecnico e notaio di fiducia per pareri indipendenti.</p>

<h2>Numeri Righetto (claim verificati)</h2>
<table>
<thead><tr><th>Indicatore</th><th>Valore</th></tr></thead>
<tbody>
<tr><td>Operatività</td><td>Dal <strong>2000</strong>, sede Limena (PD)</td></tr>
<tr><td>Portafoglio</td><td><strong>350+</strong> immobili gestiti</td></tr>
<tr><td>Territorio</td><td><strong>101</strong> comuni</td></tr>
<tr><td>Soddisfazione</td><td><strong>98%</strong></td></tr>
<tr><td>Recensioni Google</td><td><strong>127</strong> · media <strong>4,9/5</strong></td></tr>
</tbody>
</table>

<div class="tag-row" aria-label="Keyword social">
  <span>#RighettoImmobiliare</span><span>#CasePadova</span><span>#AgenziaImmobiliarePadova</span>
  <span>#VenditaCasaPadova</span><span>#Acquisizioni2026</span><span>#ImmobiliResidenziali</span><span>#Padova</span>
</div>
<p style="font-size:.8rem;color:var(--grigio)"><em>Ultimo aggiornamento: {DATE_IT}. Prezzi e disponibilità come da portale alla data di pubblicazione; verificare sempre la scheda immobile prima di visita o proposta.</em></p>
<a class="cta-deep" href="immobili?op=vendita">Sfoglia residenziale</a>
<a class="cta-deep" href="landing-valutazione" style="background:var(--blu);color:#fff">Valutazione gratuita</a>
"""


def build_com_body() -> str:
    blocks = []
    for i, p in enumerate(COM_TOP5, 1):
        n = COM_NARRATIVES[p["codice"]]
        blocks.append(acq_block(i, p, n["paras"], n["fatti"], n["alt"]))
    acq_html = "\n".join(blocks)
    return f"""
<div class="aeo-box">
<h2>In sintesi</h2>
<p style="font-size:.84rem;margin:0 0 .6rem">Panoramica delle <strong>ultime 5 acquisizioni commerciali</strong> sul portale Righetto al <strong>{DATA_PORTALE}</strong>: <strong>uffici</strong>, <strong>capannoni</strong> e <strong>locali/negozi</strong> tra Limena e Rubano, con canoni, metrature e link alle schede.</p>
<ul style="font-size:.84rem">
<li>Mix <strong>affitto</strong> (uffici e negozio) e <strong>vendita</strong> (capannoni industriali)</li>
<li>Dati da database portale — non stime di mercato inventate</li>
<li>Approfondimento agenzia: <a href="blog-righetto-storia-territorio-acquisizioni-2026">storia e acquisizioni Righetto</a></li>
</ul>
</div>

<h2>Immobili commerciali nel Padovano: perché un articolo dedicato</h2>
<p>Righetto Immobiliare segue dal <strong>2000</strong> anche <strong>locazioni commerciali</strong> e <strong>capannoni</strong> oltre al residenziale. PMI, artigiani, studi professionali e investitori cercano spazi con criteri diversi dall'abitazione: accessi carrai, altezze industriali, canoni, destinazione d'uso e contratti commerci.</p>
<p>Questo articolo elenca le <strong>cinque proposte commerciali più recenti</strong> ancora attive, senza confondere prezzi residenziali con canoni mensili. Per il contesto economico veneto resta utile il legame con export e logistica — tema affrontato in altre analisi di mercato sul blog — ma qui restiamo sui <strong>dati delle singole schede</strong>.</p>

<h2>Tipologie: ufficio, capannone, negozio</h2>
<table>
<thead><tr><th>Tipologia</th><th>Uso tipico</th><th>Variabile chiave</th></tr></thead>
<tbody>
<tr><td><strong>Ufficio</strong></td><td>Studi, PMI servizi, back-office</td><td>Canone €/mq, spese, parcheggio</td></tr>
<tr><td><strong>Capannone</strong></td><td>Produzione, logistica, deposito</td><td>Altezza, accessi carrai, lotto</td></tr>
<tr><td><strong>Negozio / locale</strong></td><td>Retail, servizi alla persona</td><td>Vetrina, passaggio, contratto commerciale</td></tr>
</tbody>
</table>
<p>In ogni trattativa verifichiamo <strong>destinazione urbanistica</strong>, <strong>conformità impianti</strong> e — per capannoni — portate e pavimentazioni. Il compenso di mediazione si definisce <strong>in sede</strong> nel mandato.</p>

<h2>Le ultime 5 acquisizioni commerciali: dettaglio e foto</h2>
<p>Ordine per data di inserimento sul portale. Per visite e proposte: codice incarico e <a href="contatti">contatti</a> agenzia.</p>
{acq_html}

<h2>Limena e Rubano: due poli del comparto</h2>
<p><strong>Limena</strong> concentra uffici in affitto e capannoni su area produttiva, a pochi minuti da Padova — sede operativa Righetto in Via Roma 96. <strong>Rubano</strong>, sulla cintura ovest, offre capannoni con lotti ampi per attività che richiedono outdoor e manovra mezzi pesanti.</p>
<p>Per confronti di canone o prezzo al mq usiamo transazioni comparabili e visite, non tabelle generiche. Dove servono quotazioni istituzionali di contesto, rimandiamo a <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">OMI Agenzia delle Entrate</a> per il segmento pertinente.</p>

<h2>Proprietario commerciale: cosa facciamo in agenzia</h2>
<ul>
<li>Valutazione allineata al segmento (reddito da locazione o prezzo di vendita industriale).</li>
<li>Shooting fotografico e scheda completa su portale e portali partner.</li>
<li>Gestione visite con qualifica dell'interessato (attività, budget, tempi).</li>
<li>Assistenza su contratto commerciale e documenti urbanistici.</li>
</ul>
<p>Primo passo senza impegno: <a href="landing-valutazione">valutazione gratuita</a> o chiamata allo <a href="tel:+390498843484">049.88.43.484</a>.</p>

<h2>Investitore: capannone locato vs da riposizionare</h2>
<p>Nel portafoglio attuale coesistono capannoni <strong>da ristrutturare</strong> con prezzo di ingresso contenuto e strutture <strong>già locate</strong> a inquilini referenziati — profili opposti che richiedono analisi diversa (capex vs yield). Non pubblichiamo rendimenti percentuali non verificabili: ogni scenario va costruito su canone effettivo, spese e fiscalità con i propri consulenti.</p>

<h2>Tabella comparativa commerciali</h2>
<table>
<thead><tr><th>Codice</th><th>Tipologia</th><th>Comune</th><th>Canone / prezzo</th><th>Superficie</th></tr></thead>
<tbody>
<tr><td>UFF2105a</td><td>Ufficio affitto</td><td>Limena</td><td>€800/mese + IVA</td><td>~90 mq</td></tr>
<tr><td>CAP1609a</td><td>Capannone vendita</td><td>Rubano</td><td>€360.000</td><td>~550 mq + lotto</td></tr>
<tr><td>CAP1687</td><td>Capannone vendita</td><td>Limena</td><td>€730.000</td><td>~1.200 mq</td></tr>
<tr><td>uff2189a</td><td>Ufficio affitto</td><td>Limena</td><td>€1.100/mese</td><td>~140 mq</td></tr>
<tr><td>NEG2173a</td><td>Locale affitto</td><td>Limena</td><td>€1.200/mese</td><td>~150 mq</td></tr>
</tbody>
</table>

<h2>Contratto commerciale: cosa chiedere prima di firmare</h2>
<p>Per uffici e negozi in affitto, il <strong>contratto commerciale</strong> regola durata, rinnovi, oneri di fitto, deposito cauzionale e spese di registrazione. Consigliamo di verificare:</p>
<ul>
<li>Destinazione d'uso catastale e urbanistica coerente con l'attività prevista.</li>
<li>Spese condominiali o di gestione del complesso (dove applicabile).</li>
<li>Stato impianti elettrici e antincendio — obblighi a carico inquilino o locatore.</li>
<li>Possibilità di sublocazione o cessione del contratto.</li>
<li>Allineamento canone con comparabili della stessa microzona.</li>
</ul>
<p>Righetto affianca le parti nella fase di trattativa; per clausole fiscali e registrazione rimandiamo a commercialista o consulente del lavoro di fiducia.</p>

<h2>Capannoni: due diligence tecnica</h2>
<p>Per CAP1609a e CAP1687 la visita deve includere carportate, altezze libere, portate pavimento, copertura e impianti. Su CAP1687 il dato «locato a azienda referenziata» va letto con contratto di locazione in essere e tempi di eventuale rilascio — informazioni disponibili in trattativa riservata, non nel teaser pubblico.</p>
<p>Su CAP1609a il lotto aggiuntivo in ghiaia compattata offre flessibilità per manovra e stoccaggio outdoor, ma va verificata compatibilità con attività prevista e vincoli comunali a Rubano.</p>

<h2>Uffici Limena: domanda locale</h2>
<p>Limena funge da cerniera tra Padova e la cintura nord: uffici da 40 a 140 mq intercettano studi professionali, piccole imprese di servizi e back-office di aziende distribuite sul territorio. I canoni in tabella (€800–€1.100/mese per le proposte elencate) vanno incrociati con costi di fitto, IVA e oneri accessori — non solo con il residenziale per metro quadro.</p>
<p>Per chi cerca spazi più piccoli oltre a questa selezione, il portale include altre unità (es. studi sotto i 50 mq) filtrabili per tipologia <strong>ufficio</strong>.</p>

<h2>Imprenditore: dal locale alla apertura</h2>
<p>Il locale NEG2173a si presta a attività con vetrina su area ad alto passaggio. Prima dell'avvio commerciale verificare SCIA o pratiche comunali necessarie, insegna, carico elettrico e adempimenti ASL ove richiesti dal settore. L'agenzia non sostituisce pratiche amministrative, ma può coordinare tempistiche con il proprietario per consegna chiavi e stato luoghi.</p>

<h2>Affitto commerciale vs acquisto capannone</h2>
<p>La selezione mescola <strong>tre locazioni</strong> e <strong>due vendite industriali</strong>. Chi avvia attività spesso preferisce affitto per contenere capitale iniziale; chi ha cassa o accesso a credito industriale può valutare acquisto capannone per stabilità costi e patrimonializzazione. Non esiste scelta universale: dipende da settore, orizzonte anni e fiscalità — da discutere con commercialista.</p>
<p>Per le locazioni UFF2105a, uff2189a e NEG2173a i canoni indicati sono mensili; per CAP1609a e CAP1687 i prezzi sono di vendita intera proprietà. Non confondere €/mq residenziale con €/mq commerciale: segmenti e comparabili sono diversi.</p>

<h2>Settori che chiedono queste tipologie nel Padovano</h2>
<ul>
<li><strong>Studi professionali e consulenza</strong> → uffici Limena 90–140 mq, parcheggio e classe energetica.</li>
<li><strong>Artigianato leggero e deposito</strong> → capannone Rubano con lotto ampio.</li>
<li><strong>Logistica urbana e produzione</strong> → capannone Limena 1.200 mq con doppio accesso.</li>
<li><strong>Retail e servizi</strong> → locale vetrina Via delle Industrie.</li>
</ul>
<p>Il Veneto resta tra le regioni con tessuto PMI denso: domanda di metri commerciali segue cicli economici diversi dal residenziale. Per macro-dati usiamo fonti istituzionali (ISTAT, camera di commercio) in articoli di mercato; qui restiamo sulle singole schede attive.</p>

<h2>Collegamenti utili sul sito Righetto</h2>
<p>Oltre alle schede singole, puoi esplorare <a href="immobili">tutto il portale</a> filtrando per tipologia ufficio, capannone o negozio. Per il tour mix residenziale + commerciale vedi <a href="blog-ultime-acquisizioni-residenziali-padova-giugno-2026">acquisizioni portale giugno 2026</a> e <a href="blog-righetto-storia-territorio-acquisizioni-2026">storia e acquisizioni 2026</a>.</p>

<h2>Checklist visita capannone o ufficio</h2>
<ol>
<li>Altezza libera, lucernari e illuminazione naturale negli uffici sopraelevati.</li>
<li>Numero accessi carrai e raggio di manovra per mezzi propri.</li>
<li>Stato copertura, grondaie e infiltrazioni perimetrali.</li>
<li>Pavimentazioni industriali, portate e eventuali fessure.</li>
<li>Impianto elettrico, cabina e potenza disponibile per macchinari.</li>
<li>Destinazione urbanistica e eventuali vincoli paesaggistici o idrogeologici.</li>
<li>Per locazioni: stato manutentivo a carico locatore vs inquilino.</li>
</ol>

<h2>Mediazione e mandato commerciale</h2>
<p>Come per il residenziale, il compenso di mediazione su vendita capannone o locazione ufficio/negozio si concorda <strong>in sede</strong> e consta nel mandato prima dell'avvio promozione. Non pubblichiamo percentuali online. Proprietari che valutano di affidarci un immobile commerciale possono richiedere <a href="landing-valutazione">valutazione gratuita</a> con comparabili di segmento — non prezzi residenziali adattati a caso.</p>

<div class="tag-row" aria-label="Keyword social">
  <span>#RighettoImmobiliare</span><span>#ImmobiliCommerciali</span><span>#CapannonePadova</span>
  <span>#UfficioLimena</span><span>#NegozioPadova</span><span>#AgenziaImmobiliarePadova</span><span>#Acquisizioni2026</span>
</div>
<p style="font-size:.8rem;color:var(--grigio)"><em>Ultimo aggiornamento: {DATE_IT}. Canoni e prezzi come da portale; verificare disponibilità in scheda prima di visita.</em></p>
<a class="cta-deep" href="immobili">Sfoglia commerciale</a>
<a class="cta-deep" href="landing-valutazione" style="background:var(--blu);color:#fff">Valutazione gratuita</a>
"""


ARTICLES = [
    {
        "filename": "blog-ultime-acquisizioni-residenziali-padova-giugno-2026.html",
        "slug": "blog-ultime-acquisizioni-residenziali-padova-giugno-2026",
        "img": "img/blog/blog-ultime-acquisizioni-residenziali-padova-giugno-2026.webp",
        "hero_img": RES_MIX[0]["foto0"],
        "html_title": "Acquisizioni portale Righetto giugno 2026 | Case e commerciali",
        "og_title": "Portale Righetto: Grisignano in evidenza, case, uffici e capannone",
        "meta_desc": "Tour aggiornato portale Righetto: Grisignano LP0285-V in apertura, 4 case Padova, 2 uffici Limena in affitto e capannone Rubano. Foto e schede giugno 2026.",
        "schema_headline": "Acquisizioni portale Righetto giugno 2026: residenziale e commerciale in un tour",
        "section": "Vita d'Agenzia",
        "cat_badge": "Portale Righetto",
        "bread": "Acquisizioni portale 2026",
        "breadcrumb_tail": "Acquisizioni portale",
        "h1": "<strong>Nuove acquisizioni dal portale Righetto</strong> — 5 case, uffici in affitto e capannone",
        "hero_alt": "Casa Grisignano di Zocco LP0285-V — copertina tour portale Righetto giugno 2026",
        "body_fn": build_mix_body,
        "faqs": [
            ("Quali immobili sono nel tour aggiornato?", "8 schede: LP0285-V Grisignano (in evidenza), LP0286, LA0317, LP0283, LP0281 residenziali; UFF2105a e uff2189a uffici affitto Limena; CAP1609a capannone Rubano."),
            ("Perché Grisignano è per prima?", "LP0285-V è in evidenza editoriale per prezzo di ingresso e ampio scoperto; seguono le altre case per data acquisizione residenziale."),
            ("Come prenoto una visita?", "049.88.43.484, contatti o form in fondo articolo con codice incarico."),
            ("Ci sono solo case?", "No: l'articolo include anche due uffici in affitto e un capannone in vendita."),
            ("I prezzi sono negoziabili?", "Ogni trattativa è individuale; prezzo o canone come da scheda alla pubblicazione."),
            ("Questo articolo sostituisce la scheda?", "No: integra con racconto e link; dati ufficiali restano in scheda immobile."),
        ],
        "related": [
            ("Acquisizioni solo commerciali", "blog-ultime-acquisizioni-commerciali-padova-giugno-2026"),
            ("Storia Righetto e acquisizioni", "blog-righetto-storia-territorio-acquisizioni-2026"),
            ("Compravendite Q1 2026", "blog-compravendite-italia-q1-agenzia-entrate-2026-padova"),
        ],
        "lead_ids": ("bl-nome-res", "bl-tel-res", "bl-email-res", "bl-msg-res", "bl-gdpr-res"),
        "registry": {
            "titolo": "Acquisizioni portale Righetto giugno 2026: case, uffici e capannone",
            "categoria": "Vita d'Agenzia",
            "tempo": 12,
            "contenuto": "Grisignano LP0285-V in evidenza, 4 residenziali Padova, 2 uffici affitto Limena, capannone Rubano — tour mix portale.",
            "evidenza": True,
            "emoji": "🏠",
        },
    },
    {
        "filename": "blog-ultime-acquisizioni-commerciali-padova-giugno-2026.html",
        "slug": "blog-ultime-acquisizioni-commerciali-padova-giugno-2026",
        "img": "img/blog/blog-ultime-acquisizioni-commerciali-padova-giugno-2026.webp",
        "hero_img": COM_TOP5[2]["foto0"],
        "html_title": "Ultime 5 acquisizioni commerciali Padova 2026 | Righetto",
        "og_title": "Uffici, capannoni e negozi: ultime acquisizioni commerciali Righetto",
        "meta_desc": "Uffici in affitto Limena, capannoni Rubano e Limena, locale commerciale: ultime 5 proposte commerciali sul portale Righetto con foto e link scheda.",
        "schema_headline": "Ultime acquisizioni commerciali Padova 2026: uffici, capannoni e negozi dal portale",
        "section": "Vita d'Agenzia",
        "cat_badge": "Vita d'Agenzia",
        "bread": "Acquisizioni commerciali 2026",
        "breadcrumb_tail": "Acquisizioni commerciali",
        "h1": "<strong>Ultime 5 acquisizioni commerciali</strong>: uffici, capannoni e negozi nel Padovano",
        "hero_alt": "Ultime acquisizioni commerciali Padova — uffici capannoni negozi Righetto giugno 2026",
        "body_fn": build_com_body,
        "faqs": [
            ("Quali commerciali sono elencati?", "UFF2105a ufficio Limena, CAP1609a capannone Rubano, CAP1687 capannone Limena, uff2189a ufficio Limena, NEG2173a locale Limena — dati portale 16 giugno 2026."),
            ("Ci sono solo affitti?", "No: due capannoni in vendita e tre unità in affitto commerciale."),
            ("Seguite locazioni commerciali?", "Sì — servizio dedicato per proprietari e inquilini."),
            ("Posso proporre il mio capannone?", "Sì, con valutazione gratuita in sede."),
            ("Pubblicate percentuali di mediazione?", "No: condizioni concordate nel mandato."),
            ("Le foto sono quelle del portale?", "Sì, provengono dalle schede Supabase ufficiali."),
        ],
        "related": [
            ("Storia e acquisizioni Righetto", "blog-righetto-storia-territorio-acquisizioni-2026"),
            ("Acquisizioni portale mix", "blog-ultime-acquisizioni-residenziali-padova-giugno-2026"),
            ("Servizio locazioni", "servizio-locazioni"),
        ],
        "lead_ids": ("bl-nome-com", "bl-tel-com", "bl-email-com", "bl-msg-com", "bl-gdpr-com"),
        "registry": {
            "titolo": "Ultime 5 acquisizioni commerciali Padova 2026: uffici e capannoni",
            "categoria": "Vita d'Agenzia",
            "tempo": 10,
            "contenuto": "Uffici, capannoni Rubano/Limena e locale commerciale — ultime 5 proposte attive con schede.",
            "evidenza": False,
            "emoji": "🏢",
        },
    },
]


def build_html(cfg: dict, body: str, wc: int) -> str:
    slug = cfg["slug"]
    faq_obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in cfg["faqs"]
        ],
    }
    blog_obj = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": cfg["schema_headline"],
        "description": cfg["meta_desc"],
        "image": [f"https://righettoimmobiliare.it/{cfg['img']}"],
        "author": {"@type": "Person", "name": "Gino Capon"},
        "publisher": {"@type": "Organization", "name": "Righetto Immobiliare", "url": "https://righettoimmobiliare.it"},
        "datePublished": DATE_ISO,
        "dateModified": DATE_MOD_ISO,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://righettoimmobiliare.it/{slug}"},
        "articleSection": cfg["section"],
        "wordCount": wc,
        "inLanguage": "it-IT",
    }
    rel = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in cfg["related"])
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9MHDHHES26"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9MHDHHES26');</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#2C4A6E">
<title>{cfg["html_title"]}</title>
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="dns-prefetch" href="https://cdn.jsdelivr.net">
<link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="canonical" href="https://righettoimmobiliare.it/{slug}">
<meta property="og:type" content="article">
<meta property="og:title" content="{cfg["og_title"]}">
<meta property="og:description" content="{cfg["meta_desc"]}">
<meta property="og:url" content="https://righettoimmobiliare.it/{slug}">
<meta property="og:image" content="https://righettoimmobiliare.it/{cfg["img"]}">
<meta property="article:published_time" content="{TIME_TS}">
<meta property="article:author" content="Gino Capon">
<meta property="article:section" content="{cfg["section"]}">
<meta name="description" content="{cfg["meta_desc"]}">
<script type="application/ld+json">{json.dumps(blog_obj, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_obj, ensure_ascii=False)}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://righettoimmobiliare.it/"}},{{"@type":"ListItem","position":2,"name":"Blog","item":"https://righettoimmobiliare.it/blog"}},{{"@type":"ListItem","position":3,"name":"{cfg["bread"]}"}}]}}</script>
<link rel="stylesheet" href="css/fonts.css?v=3"><link rel="stylesheet" href="css/nav-mobile.css?v=4">
<link rel="stylesheet" href="css/scroll-reveal.css?v=3" media="print" onload="this.media='all'">
{STYLE_ACQ}
</head>
<body>
<a href="#main-content" class="skip-link">Contenuto principale</a>
<header><div class="hi">
  <a href="/" class="logo">Righetto <span>Immobiliare</span></a>
  <nav><a href="/">Home</a><a href="immobili">Immobili</a><a href="gino-capon">Profilo autore</a><a href="blog" class="active">Blog</a><a href="contatti">Contatti</a></nav>
  <a class="h-btn" href="landing-valutazione">Valutazione gratuita</a>
</div><button class="nav-burger" id="burgerBtn" aria-label="Menu"><span></span><span></span><span></span></button></header>
<div class="nav-mobile" id="navMobile"><a href="/">Home</a><a href="immobili">Immobili</a><a href="gino-capon">Profilo autore</a><a href="blog">Blog</a><a href="contatti">Contatti</a></div>
<main id="main-content">
<div class="art-hero">
  <img class="art-hero-img" src="{cfg["hero_img"]}" alt="{cfg["hero_alt"]}" width="1280" height="420" fetchpriority="high">
  <div class="art-hero-overlay"><div class="art-hero-inner">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="blog">Blog</a> / {cfg["breadcrumb_tail"]}</div>
    <span class="cat-badge">{cfg["cat_badge"]}</span>
    <h1>{cfg["h1"]}</h1>
    <div class="art-hero-meta"><div class="av">G</div><span>Gino Capon</span><span>{DATE_IT}</span><span>Aggiornato: {DATE_IT}</span></div>
  </div></div>
</div>
<div class="art-container"><div class="art-content">
{body}
{faq_html(cfg["faqs"])}
<div class="author-bio"><img src="img/team/titolari.webp" alt="Gino Capon Righetto Immobiliare" width="64" height="64" loading="lazy"><div><strong>Gino Capon</strong><p style="font-size:.8rem;color:#555">Titolare — Righetto Immobiliare, Limena (PD). Mediazione immobiliare su Padova e provincia dal 2000.</p><p style="font-size:.78rem;margin-top:.4rem"><a href="gino-capon">Profilo autore</a> · <a href="blog-righetto-storia-territorio-acquisizioni-2026">Storia e acquisizioni</a></p></div></div>
<div class="related"><h3 style="font-family:'Cormorant Garamond',serif">Articoli correlati</h3><ul style="margin-left:1.1rem;margin-top:.4rem">{rel}</ul></div>
</div></div>
{lead_form(slug, cfg["lead_ids"])}
{FOOTER}"""


def registry_entries(cfg: dict, wc: int) -> dict:
    reg = cfg["registry"]
    base = {
        "titolo": reg["titolo"],
        "categoria": reg["categoria"],
        "data": DATE_ISO,
        "stato": "pubblicato",
        "immagine_copertina": cfg["img"],
        "url_statico": cfg["slug"],
    }
    blog_html = {**base, "tempo": reg["tempo"], "autore": "Gino Capon", "contenuto": reg["contenuto"], "evidenza": reg["evidenza"]}
    admin = {**blog_html, "emoji": reg["emoji"], "contenuto": f"<p>{reg['contenuto']}</p>", "data_pubblicazione": DATE_ISO}
    return {"blog_html": blog_html, "admin": admin, "homepage": {k: v for k, v in base.items()}}


def main() -> None:
    registry = {
        "generated": DATE_ISO,
        "date_display": DATE_IT,
        "files": [],
        "blog_html_articoliStatici": [],
        "admin_blogSeedArticles": [],
        "homepage_js_articoliStatici": [],
    }
    for cfg in ARTICLES:
        body = cfg["body_fn"]()
        wc = word_count(body)
        html = build_html(cfg, body, wc)
        out = ROOT / cfg["filename"]
        out.write_text(html, encoding="utf-8")
        entries = registry_entries(cfg, wc)
        registry["files"].append({"filename": cfg["filename"], "slug": cfg["slug"], "wordCount_body": wc})
        registry["blog_html_articoliStatici"].append(entries["blog_html"])
        registry["admin_blogSeedArticles"].append(entries["admin"])
        registry["homepage_js_articoliStatici"].append(entries["homepage"])
        print(f"OK {cfg['filename']} — {wc} parole")
    reg_path = ROOT / "scripts" / "acquisizioni_giugno16_registry.json"
    reg_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Registry: {reg_path}")


if __name__ == "__main__":
    main()
