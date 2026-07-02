# -*- coding: utf-8 -*-
"""Genera 5 articoli housing/studentati Veneto — luglio 2026.
Esegui da repo root: python scripts/build_blog_housing_veneto_lug2026.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DATE_IT = "2 luglio 2026"
DATE_ISO = "2026-07-02"
TIME_TS = "2026-07-02T09:00:00+02:00"
DATE_MOD_ISO = "2026-07-02"
MIN_BODY_WORDS = 1900

COMMON_BODY_TAIL = """
<h2>Mediazione Righetto e uso delle fonti</h2>
<p>Gruppo Immobiliare Righetto opera dal <strong>2000</strong> su <strong>101 comuni</strong> del Padovano e del Veneto orientale, con oltre <strong>350 immobili</strong> gestiti e <strong>98% di soddisfazione</strong> clienti verificata (127 recensioni Google, media 4,9/5). I dati economici citati provengono da fonti istituzionali e osservatori di settore — <strong>Immobiliare.it Insights</strong>, <strong>FIMAA</strong>, <strong>ESU</strong>, <strong>ISTAT</strong>, <strong>Regione Veneto</strong>, <strong>Università di Padova</strong>, <strong>Edilcassa/Confartigianato Veneto</strong> dove applicabile. Non utilizziamo titoli di giornale come fonte primaria.</p>
<p>Il compenso di mediazione immobiliare si concorda <strong>in sede</strong> nel mandato di vendita o locazione: non pubblichiamo listini o percentuali online. Per valutazioni, locazioni studentesche, corporate housing o acquisto abitativo contattare l'agenzia via form in fondo pagina o telefono 049.8843484. Articolo aggiornato al """ + DATE_IT + """.</p>
"""

ROOT = Path(__file__).resolve().parent.parent

STYLE_BLOCK = r"""<style>
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
.kpi-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:.55rem;margin:1.2rem 0 1.6rem}
.kpi-strip div{background:var(--sfondo);border:1px solid var(--gc);border-radius:10px;padding:.75rem .85rem;text-align:center}
.kpi-strip strong{display:block;font-family:'Cormorant Garamond',serif;font-size:1.35rem;color:var(--blu)}
.kpi-strip span{font-size:.62rem;letter-spacing:.06em;text-transform:uppercase;color:var(--grigio)}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:1.5rem 0 2rem}
.stat-card{background:var(--nero);border-radius:10px;padding:1.2rem;text-align:center;color:#fff}
.stat-num{font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:700;color:var(--oro);line-height:1}
.stat-label{font-size:.68rem;color:rgba(255,255,255,.5);margin-top:.3rem;text-transform:uppercase;letter-spacing:.5px}
.chart-wrap{background:var(--sfondo);border:1px solid var(--gc);border-radius:12px;padding:1.2rem;margin:1.4rem 0}
.chart-wrap figcaption{font-size:.72rem;color:var(--grigio);margin-top:.6rem;text-align:center}
.blog-fig{margin:1.65rem 0;border-radius:12px;overflow:hidden;border:1px solid var(--gc);background:#fff}
.blog-fig img{width:100%;height:auto;display:block;max-height:380px;object-fit:cover}
.blog-fig figcaption{font-size:.72rem;color:var(--grigio);padding:.7rem .95rem;background:var(--sfondo);line-height:1.55}
.cta-deep{display:inline-flex;background:linear-gradient(180deg,var(--oro2),var(--oro));color:var(--nero);font-weight:800;padding:.8rem 1.62rem;border-radius:10px;font-size:.8rem;margin:1rem .75rem 1rem 0}
.faq-item{border:1px solid var(--gc);border-radius:8px;margin-bottom:.5rem}
.faq-q{padding:.86rem .98rem;font-weight:600;font-size:.84rem;cursor:pointer}.faq-a{max-height:0;overflow:hidden;transition:max-height .35s;background:var(--sfondo)}
.faq-item.open .faq-a{max-height:420px}.faq-a-inner{padding:0 .98rem .86rem;font-size:.83rem;color:var(--grigio)}
.author-bio{display:flex;gap:1.08rem;padding:1.38rem;border:1px solid rgba(44,74,110,.12);border-radius:12px;margin:1.68rem 0}
.related{background:var(--sfondo);border:1px solid var(--gc);padding:1.32rem;border-radius:10px}
footer{background:linear-gradient(180deg,var(--nero),#0d1a2a);color:rgba(255,255,255,.65);padding:2.35rem 1.5rem;font-size:.75rem}
.skip-link{position:absolute;top:-100%;background:var(--oro);color:var(--nero);padding:.46rem .9rem;z-index:9999}.skip-link:focus{top:0}
@media(max-width:700px){.art-hero-img{height:260px}.kpi-strip,.stats-grid{grid-template-columns:repeat(2,1fr)}}
</style>
<link rel="stylesheet" href="css/blog-rich.css?v=2">
<link rel="stylesheet" href="css/blog-lead-form.css?v=2">"""

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

AUTHORS = {
    "linda": {
        "name": "Linda Righetto",
        "initial": "L",
        "profile": "linda-righetto",
        "img": "img/team/real-state-linda-righetto.webp",
        "bio": "Consulente locazioni e housing studentesco — Righetto Immobiliare, Padova e provincia.",
        "nav_link": "linda-righetto",
    },
    "gino": {
        "name": "Gino Capon",
        "initial": "G",
        "profile": "gino-capon",
        "img": "img/team/titolari.webp",
        "bio": "Titolare — Righetto Immobiliare, Limena (PD). Mediazione immobiliare su Padova e provincia dal 2000.",
        "nav_link": "gino-capon",
    },
}


def word_count(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split()) if text else 0


def faq_html(faqs: list[tuple[str, str]]) -> str:
    items = "".join(
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>'
        for q, a in faqs
    )
    return f'<div id="faq" style="margin-top:2rem"><h2 style="font-family:\'Cormorant Garamond\',serif;font-size:1.62rem;border-bottom:2px solid var(--oro);margin-bottom:.9rem">Domande frequenti</h2>{items}</div>'


def lead_form(slug: str, ids: tuple[str, str, str, str, str]) -> str:
    n, t, e, m, g = ids
    return f"""<section class="blog-lead-wrap" id="richiedi-consulenza" aria-labelledby="blog-lead-title">
  <h2 id="blog-lead-title">Richiedi informazioni su locazioni o valutazione immobile</h2>
  <form data-rig-lead-form data-provenienza="{slug}" data-pagina="{slug}" data-msg-prefix="[Blog]" novalidate>
    <div class="bl-fields">
      <label for="{n}">Nome e cognome *</label>
      <input type="text" id="{n}" required autocomplete="name" placeholder="Mario Rossi">
      <label for="{t}">Telefono *</label>
      <input type="tel" id="{t}" required autocomplete="tel" placeholder="333 123 4567">
      <label for="{e}">Email</label>
      <input type="email" id="{e}" autocomplete="email" placeholder="mario@email.it">
      <label for="{m}">Messaggio (opzionale)</label>
      <textarea id="{m}" placeholder="Zona, budget, studentato o locazione…"></textarea>
      <label class="bl-chk"><input type="checkbox" id="{g}" required> Acconsento al trattamento dei dati (GDPR). <a href="privacy-policy">Privacy</a></label>
      <button type="submit">Invia richiesta</button>
    </div>
    <div class="rig-lead-success">
      <h3>Messaggio inviato!</h3>
      <p>Grazie. Ti ricontattiamo entro pochi minuti negli orari di apertura.</p>
    </div>
  </form>
</section>"""


def chart_padova_canoni() -> str:
    return """<figure class="chart-wrap" aria-label="Confronto canone medio stanza Padova 2020 vs 2026">
<svg viewBox="0 0 420 220" width="100%" height="220" role="img" aria-labelledby="chart-padova-title">
<title id="chart-padova-title">Canone medio stanza universitaria Padova: 335 euro nel 2020 e 490 euro nel 2026</title>
<text x="210" y="24" text-anchor="middle" font-size="13" fill="#152435" font-family="Montserrat,sans-serif">Canone medio stanza — Padova (Immobiliare.it Insights, marzo 2026)</text>
<rect x="80" y="50" width="90" height="120" fill="#2C4A6E" rx="6"/>
<text x="125" y="110" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">335 €</text>
<text x="125" y="195" text-anchor="middle" fill="#6B7A8D" font-size="11">2020</text>
<rect x="250" y="26" width="90" height="144" fill="#FF6B35" rx="6"/>
<text x="295" y="90" text-anchor="middle" fill="#152435" font-size="14" font-weight="700">490 €</text>
<text x="295" y="195" text-anchor="middle" fill="#6B7A8D" font-size="11">2026</text>
<text x="210" y="210" text-anchor="middle" fill="#6B7A8D" font-size="10">Variazione stimata +46% vs 2020 (fonte portale)</text>
</svg>
<figcaption>Dati indicativi da Immobiliare.it Insights (marzo 2026). Verificare sempre l'annuncio e la zona.</figcaption>
</figure>"""


def blog_fig(src: str, alt: str, caption: str) -> str:
    return f"""<figure class="blog-fig">
<img src="{src}" alt="{alt}" width="820" height="460" loading="lazy">
<figcaption>{caption}</figcaption>
</figure>"""


ASSETS = {
    "stanza": {
        "hero": "img/blog/blog-affitti-canoni-fimaa-q1-2026-padova.webp",
        "hero_alt": "Mercato affitti Padova — canoni stanze universitarie FIMAA 2026",
        "figs": [
            ("img/blog/blog-scegliere-immobile-giusto-padova-2026.webp", "Visita a un appartamento in affitto a Padova con agente immobiliare", "Due diligence in visita: luce, impianti e planimetria prima del contratto transitorio."),
            ("img/blog/blog-gestione-spese-casa-padova-2026.webp", "Gestione spese domestiche in appartamento condiviso a Padova", "Canone, utenze e spese condominiali: budget realistico per studenti fuori sede."),
            ("img/blog/blog-prezzi-padova-provincia-2026.webp", "Panorama abitativo provincia di Padova", "Periferie tram e cintura: alternative al Portello con canoni spesso inferiori."),
        ],
    },
    "studentati": {
        "hero": "img/blog/blog-nuove-costruzioni-mercato-veneto-2026-padova.webp",
        "hero_alt": "Cantieri e nuove costruzioni nel Veneto — ampliamento housing studentesco",
        "figs": [
            ("img/blog/blog-piano-casa-decreto-66-2026-padova.webp", "Edificio residenziale e politiche abitative in Veneto", "Politiche abitative e nuovo stock: collegamento con bandi PNRR e decreto Piano Casa."),
            ("img/blog/blog-case-piu-vendute-padova-2026.webp", "Tipologie abitative più richieste nel mercato padovano", "Domanda studenti e nuclei familiari convive sullo stesso comparto residenziale."),
            ("img/blog/blog-inline-tipologie-case-vendute-padova-2026.webp", "Distribuzione tipologie immobili nel Padovano", "Monolocali e bilocali restano formati chiave anche per posti letto condivisi."),
        ],
    },
    "green": {
        "hero": "img/blog/blog-domanda-case-green-padova-2026.webp",
        "hero_alt": "Edificio ad alta efficienza energetica — residenze green per studenti a Padova",
        "figs": [
            ("img/blog/blog-inline-green-vs-brown-padova-2026.webp", "Confronto edificio efficiente e edificio datato a Padova", "Classe energetica e costi bolletta: vantaggio NZEB per inquilini fuori sede."),
            ("img/blog/blog-casa-vendibile-5-anni-case-green-padova-2026.webp", "Riqualificazione energetica appartamento nel Padovano", "Interventi green aumentano attrattività locativa studentesca."),
            ("img/blog/blog-bonus-edilizi-2026-incentivi-casa-padova.webp", "Incentivi edilizi per efficientamento energetico in Veneto", "Bonus e riqualificazione sostengono progetti NZEB come Tribloc."),
        ],
    },
    "vicenza": {
        "hero": "img/blog/blog-piano-casa-decreto-66-2026-padova.webp",
        "hero_alt": "Residenze calmierate e rigenerazione urbana nel Veneto",
        "figs": [
            ("img/blog/blog-inline-posizione-padova-2026.webp", "Posizione e servizi urbani nel Veneto orientale", "Microzona e servizi incidono sul canone calmierato vs libero."),
            ("img/blog/blog-inline-superfici-case-vendute-padova-2026.webp", "Superfici abitative tipiche nel mercato veneto", "Camere e metri quadri: standard posti letto PNRR e mercato libero."),
            ("img/blog/blog-agenzia-top-servizi-padova-2026.webp", "Consulenza immobiliare Righetto per locazioni in Veneto", "Supporto contrattuale per studenti e famiglie — mediazione concordata in mandato."),
        ],
    },
    "lavoratori": {
        "hero": "img/blog/blog-costi-costruzione-istat-padova-2026.webp",
        "hero_alt": "Cantiere edile nel Veneto — housing lavoratori e costi costruzione ISTAT",
        "figs": [
            ("img/blog/blog-ultime-acquisizioni-commerciali-padova-giugno-2026.webp", "Uffici e capannoni in gestione Righetto nel Padovano", "Corporate housing spesso affianca unità produttive e uffici."),
            ("img/blog/blog-ultime-acquisizioni-residenziali-padova-giugno-2026.webp", "Appartamenti residenziali disponibili per squadre edili fuori sede", "Trilocali e quadrilocali adatti a co-housing temporaneo lavoratori."),
            ("img/blog/blog-righetto-storia-territorio-acquisizioni-2026.webp", "Territorio veneto servito da Righetto Immobiliare", "101 comuni coperti — locazioni anche per imprese edili fuori sede."),
        ],
    },
}


def chart_donut_canali() -> str:
    return """<figure class="chart-wrap" aria-label="Ripartizione posti letto per canale">
<svg viewBox="0 0 420 240" width="100%" height="240" role="img">
<title>Canali posti letto universitari Veneto</title>
<circle cx="130" cy="120" r="70" fill="#ECE7DF"/>
<path d="M130 50 A70 70 0 0 1 200 120 L130 120 Z" fill="#2C4A6E"/>
<path d="M200 120 A70 70 0 0 1 130 190 L130 120 Z" fill="#FF6B35"/>
<path d="M130 190 A70 70 0 0 1 60 120 L130 120 Z" fill="#4E789A"/>
<path d="M60 120 A70 70 0 0 1 130 50 L130 120 Z" fill="#8AB4CE"/>
<rect x="240" y="70" width="14" height="14" fill="#2C4A6E"/><text x="262" y="82" font-size="11" fill="#152435">ESU pubblico</text>
<rect x="240" y="98" width="14" height="14" fill="#FF6B35"/><text x="262" y="110" font-size="11" fill="#152435">Privati (Camplus)</text>
<rect x="240" y="126" width="14" height="14" fill="#4E789A"/><text x="262" y="138" font-size="11" fill="#152435">PNRR / riuso</text>
<rect x="240" y="154" width="14" height="14" fill="#8AB4CE"/><text x="262" y="166" font-size="11" fill="#152435">Mercato libero</text>
</svg>
<figcaption>Schema indicativo ripartizione offerta posti letto — proporzioni illustrative, non dato ISTAT.</figcaption>
</figure>"""


def chart_energy_compare() -> str:
    return """<figure class="chart-wrap" aria-label="Confronto spesa energetica NZEB vs classe G">
<svg viewBox="0 0 420 200" width="100%" height="200" role="img">
<title>Spesa energetica indicativa NZEB vs edificio classe G</title>
<text x="210" y="22" text-anchor="middle" font-size="12" fill="#152435">Costo energetico mensile stimato (€/camera)</text>
<rect x="70" y="50" width="80" height="110" fill="#C0392B" rx="6"/>
<text x="110" y="105" text-anchor="middle" fill="#fff" font-size="13" font-weight="700">95 €</text>
<text x="110" y="175" text-anchor="middle" fill="#6B7A8D" font-size="10">Classe G</text>
<rect x="170" y="80" width="80" height="80" fill="#FF8F5E" rx="6"/>
<text x="210" y="125" text-anchor="middle" fill="#152435" font-size="13" font-weight="700">65 €</text>
<text x="210" y="175" text-anchor="middle" fill="#6B7A8D" font-size="10">Classe C</text>
<rect x="270" y="110" width="80" height="50" fill="#2C4A6E" rx="6"/>
<text x="310" y="140" text-anchor="middle" fill="#fff" font-size="13" font-weight="700">35 €</text>
<text x="310" y="175" text-anchor="middle" fill="#6B7A8D" font-size="10">NZEB</text>
</svg>
<figcaption>Stime illustrative per confronto efficienza — verificare bollette reali e APE.</figcaption>
</figure>"""


def chart_edilcassa_bar() -> str:
    return """<figure class="chart-wrap" aria-label="Confronto fondo Edilcassa e deposito cauzionale">
<svg viewBox="0 0 420 210" width="100%" height="210" role="img">
<title>Fondo Edilcassa 250000 euro vs deposito affitto tipico</title>
<text x="210" y="22" text-anchor="middle" font-size="12" fill="#152435">Confronto importi (scala diversa — solo orientamento)</text>
<rect x="55" y="45" width="120" height="130" fill="#2C4A6E" rx="6"/>
<text x="115" y="95" text-anchor="middle" fill="#fff" font-size="12" font-weight="700">250.000 €</text>
<text x="115" y="190" text-anchor="middle" fill="#6B7A8D" font-size="10">Fondo Edilcassa Veneto</text>
<rect x="245" y="130" width="120" height="45" fill="#FF6B35" rx="6"/>
<text x="305" y="158" text-anchor="middle" fill="#152435" font-size="12" font-weight="700">2–3 mesi</text>
<text x="305" y="190" text-anchor="middle" fill="#6B7A8D" font-size="10">Deposito affitto tipico</text>
</svg>
<figcaption>Fondo garanzia contratto edile ≠ deposito cauzionale locazione — fonti Edilcassa/Confartigianato Veneto.</figcaption>
</figure>"""


def chart_tram_zones() -> str:
    return """<figure class="chart-wrap" aria-label="Canoni indicativi per fascia zona Padova">
<svg viewBox="0 0 420 220" width="100%" height="220" role="img">
<title>Canoni stanza per zona collegata al tram</title>
<polyline points="60,160 120,140 180,120 240,100 300,85 360,75" fill="none" stroke="#FF6B35" stroke-width="3"/>
<circle cx="60" cy="160" r="5" fill="#2C4A6E"/><circle cx="120" cy="140" r="5" fill="#2C4A6E"/>
<circle cx="180" cy="120" r="5" fill="#2C4A6E"/><circle cx="240" cy="100" r="5" fill="#2C4A6E"/>
<circle cx="300" cy="85" r="5" fill="#2C4A6E"/><circle cx="360" cy="75" r="5" fill="#2C4A6E"/>
<text x="60" y="185" font-size="9" fill="#6B7A8D">Guizza</text>
<text x="115" y="185" font-size="9" fill="#6B7A8D">Arcella</text>
<text x="165" y="185" font-size="9" fill="#6B7A8D">P.Brenta</text>
<text x="225" y="185" font-size="9" fill="#6B7A8D">Cittadella</text>
<text x="285" y="185" font-size="9" fill="#6B7A8D">Portello</text>
<text x="345" y="185" font-size="9" fill="#6B7A8D">Centro</text>
<text x="210" y="210" text-anchor="middle" font-size="10" fill="#6B7A8D">Trend indicativo verso centro — Immobiliare.it Insights + comparabili</text>
</svg>
<figcaption>Andamento indicativo canoni lungo assi tram TPL — non listino ufficiale.</figcaption>
</figure>"""


def figs_html(key: str) -> str:
    return "\n".join(blog_fig(s, a, c) for s, a, c in ASSETS[key]["figs"])


def table_veneto_canoni() -> str:
    return """<table>
<thead><tr><th>Città Veneto</th><th>Canone medio stanza (indicativo)</th><th>Nota</th></tr></thead>
<tbody>
<tr><td><strong>Padova</strong></td><td>circa 490 €/mese</td><td>Immobiliare.it Insights, marzo 2026</td></tr>
<tr><td><strong>Venezia</strong></td><td>fascia alta (isola + Mestre)</td><td>Pressione turismo e università Ca' Foscari</td></tr>
<tr><td><strong>Verona</strong></td><td>intermedia-alta</td><td>Università e domanda lavorativa</td></tr>
<tr><td><strong>Vicenza</strong></td><td>in crescita con nuovi posti letto</td><td>ESU e PNRR studentati</td></tr>
<tr><td><strong>Treviso</strong></td><td>media regionale</td><td>Collegamento Venezia-Padova</td></tr>
</tbody>
</table>"""


def sections_html(blocks: list[tuple[str, list[str]]]) -> str:
    parts: list[str] = []
    for title, paras in blocks:
        parts.append(f"<h2>{title}</h2>")
        for p in paras:
            parts.append(f"<p>{p}</p>")
    return "\n".join(parts)


EXPANSION_STANZA = sections_html([
    ("Microzone Portello e via Marzolo: domanda strutturale", [
        "Il rione Portello resta il barometro del mercato stanze perché concentra facoltà di Ingegneria, Economia e percorsi verso il centro storico. Gli annunci qui si muovono rapidamente: una camera arredata con balcone può uscire in pochi giorni a cifre allineate ai 490 euro di <strong>Immobiliare.it Insights</strong>. Chi insiste su Portello pagherà premium; chi accetta dieci minuti in più di tram spesso risparmia due cifre mensili.",
        "Via Marzolo e via Venezia formano il triangolo più richiesto da studenti fuori sede. I proprietari che mantengono impianti a norma e contratti registrati trovano inquilini referenziati anche a canone pieno; chi lascia degradare bagni e cucine vede vacanza prolungata ad agosto. FIMAA Veneto raccomanda inventory fotografico e regolamento scritto per convivenze da tre a cinque coinquilini.",
    ]),
    ("Arcella, Guizza e Ponte di Brenta: periferia ben connessa", [
        "Arcella intercetta studenti che accettano spostamento verso centro con linee bus e tram. I canoni segnalati in agenzia per singole ristrutturate restano inferiori alla media Insights del capoluogo universitario, con trade-off su rumorosità e parcheggio. Verificare sempre frequenza serale del mezzo pubblico se i corsi prevedono laboratori tardivi.",
        "Guizza e Ponte di Brenta offrono appartamenti più ampi adatti a condivisione tra quattro camere: il costo pro capite scende, ma la gestione convivenza richiede regole su pulizie, ospiti e turni cucina. Genitori che finanziano l'affitto dovrebbero fissare tetto mensile includendo utenze e abbonamento TPL, non solo canone camera.",
    ]),
    ("Contratti, caparra e registrazione: prassi FIMAA", [
        "Locazione a studenti non significa informalità: contratto 4+4 o transitorio dove applicabile, registrazione entro termini e caparra documentata restano obblighi. FIMAA segnala contenziosi frequenti su restituzione deposito quando manca inventory iniziale. In agenzia usiamo modelli allineati a normativa vigente e concordiamo compenso mediazione solo nel mandato, senza percentuali online.",
        "Per coinquilino subentrante a metà anno accademico, verificare clausola sostituzione e consenso locatori. Università di Padova e ESU non intervengono su contratti privati: tutela passa da documenti firmati e eventuale deposito cauzionale a norma.",
    ]),
    ("Confronto stanza singola vs doppia vs posto letto", [
        "La doppia divide spese ma riduce privacy; posti letto in appartamento grande restano soluzione economica se convivenza è gestita. Insights misura soprattutto singole: confrontare annunci equivalenti evita illusioni di risparmio su camere senza scrivania o armadio.",
        "Studentato ESU e residenze private offrono alternative con canone calmierato o servizi inclusi — articoli correlati sul blog approfondiscono posti letto PNRR. Mercato libero resta marginalmente determinante per chi esce dalle graduatorie a settembre.",
    ]),
    ("Energetica, APE e bollette in appartamento condiviso", [
        "Classe energetica incide su bolletta gas e luce ripartita tra coinquilini. APE classe bassa in palazzo anni Settanta è comune in periferia: chiedere storico spese prima di firmare. Riqualificazione condotta dal proprietario può giustificare canone superiore se documentata.",
        "ISTAT monitora inflazione energia: studenti fuori sede sensibili al costo totale dovrebbero simulare spesa mensile oltre al canone. Impianti non a norma espongono a rischi e contestazioni in restituzione deposito.",
    ]),
    ("Genitori fuori Veneto: tempistiche e due diligence a distanza", [
        "Famiglie del Sud o del Centro Italia che inviano figli a Padova spesso prenotano visite a giugno-luglio. Videochiamata guidata con agente o proprietario integra sopralluogo fisico su umidità, infissi e rumore. Non trasferire caparra senza contratto leggibile e identità locatori verificata.",
        "Servizio <a href=\"servizio-locazioni\">locazioni</a> Righetto include accompagnamento documentale per chi non conosce il territorio. Incrociare con guida <a href=\"blog-affitto-studenti-padova\">affitto studenti Padova</a> riduce errori su zone lontane dai poli di studio.",
    ]),
    ("Proprietario investitore: reddito lordo vs vacanza estiva", [
        "Rendimento locativo studentesco dipende da occupazione 10-11 mesi e giorni persi tra un inquilino e l'altro. Canone allineato a Insights riempie camera rapidamente; canone eccessivo allunga vacanza e azzera vantaggio. Manutenzione preventiva costa meno di sconto negoziato per infiltrazioni non riparate.",
        "Compenso mediazione e gestione locativa si concordano in sede. Non pubblichiamo tariffe online. Valutazione comparativa considera OMI, stato immobile e domanda microzona — non promesse di rendimento percentuale non verificabile.",
    ]),
    ("Università di Padova: iscritti, Erasmus e picchi stagionali", [
        "L'ateneo patavino registra iscritti stabili e flussi Erasmus che concentrano domanda su semestre autunnale. Picco ricerca alloggio maggio-agosto; gennaio-febbraio secondario per cambi corso. Insights cattura medie annuali, non picco settembre: budget familiare conviene includere margine.",
        "Facoltà distanti (Agripolis, medicina veterinaria, sedi peripheral) spostano preferenze abitative. Consigliare sempre mappa reale spostamenti, non solo «centro universitario» generico.",
    ]),
    ("Trasporti TPL e mobilità dolce", [
        "Abbonamenti TPL Padova e piste ciclabili influenzano scelta quartiere. Bici usata + tram mensile spesso battono costo camera in Portello. Parcheggio auto per studenti fuori sede è costoso e raro in centro: segnalare limiti ai nuclei familiari che offrono auto.",
        "Regione Veneto integra offerta multimodale: verificare linee notturne weekend se attività extracurriculari lo richiedono.",
    ]),
    ("Contesto macro Veneto e comparazione OMI", [
        "OMI Agenzia delle Entrate fornisce fasce locative per zona omogenea: strumento utile a moderare aspettative su annuncio «premium» non giustificato. Padova non è bubble isolata: Vicenza e Verona mostrano tensioni simili con intensità diversa.",
        "Leggere <a href=\"blog-affitti-padova-canoni-2026\">affitti Padova canoni 2026</a> completa quadro oltre segmento stanze. FIMAA e Insights convergono su professionalizzazione contratti post-pandemia.",
    ]),
    ("Mediazione Righetto e limiti consulenza", [
        "Righetto Immobiliare opera dal 2000 su 101 comuni con 350+ immobili gestiti — claim verificati. Non siamo consulenti fiscali o legali: per detrazioni e clausole specifiche rivolgersi a professionisti. Offriamo valutazione locativa e supporto visita.",
        "Ultimo aggiornamento contenuti economici: " + DATE_IT + ". Canoni da Immobiliare.it Insights marzo 2026; contesto ESU, FIMAA, Università di Padova, ISTAT.",
    ]),
    ("Seasonalità annunci e piattaforme digitali", [
        "Immobiliare.it Insights aggrega stock annunci: a luglio l'offerta è più ampia, a settembre si restringe e i prezzi chiesti salgono anche oltre la media storica. Monitorare trend mensili del portale aiuta a negoziare. Annunci con foto professionali e planimetrie chiare convertono più rapidamente senza sconti elevati.",
        "Per benchmark istituzionale incrociamo FIMAA, OMI e Insights. Segnalare sempre eventuali spese condominiali straordinarie in corso: l'inquilino studente raramente può assorbire aumenti imprevisti di quota.",
    ]),
    ("Sicurezza, condomini e convivenza interculturale", [
        "Padova accoglie studenti internazionali: regolamento casa in italiano e inglese riduce fraintendimenti su rumori e ospiti. Condomini con regolamenti severi su scale e cortili vanno letti prima del contratto. FIMAA raccomanda referenze o garanzie genitori per primi contratti fuori sede.",
        "Proprietario responsabile installa rilevatori fumo e mantiene estintori dove richiesto. Mercato studentesco resta stagionale e competitivo con ESU e residenze nuove.",
    ]),
    ("Dati ISTAT e spesa abitativa giovani", [
        "ISTAT pubblica indicatori su costo della vita e incidenza della spesa per alloggio sui nuclei giovani. Nel Nord-Est la voce affitto pesa più che nel Sud per studenti fuori sede. Include nel budget mensile anche tassa occupazione, assicurazione infortuni consigliata e connessione internet simmetrica se smart working accademico.",
        "Confrontare canone Insights con reddito disponibile evita abbandono corso per stress finanziario. Borse ESU e regionali mitigano ma non sempre coprono intero gap tra 335 euro storici e 490 euro attuali.",
        "Regione Veneto coordina politiche abitative giovani con PNRR: effetto distribuito su più anni, non immediato sul singolo contratto agosto 2026.",
        "Per supporto operativo su contratti e visite contattare Righetto via form in fondo pagina o telefono 049.8843484 — senza impegno informativo iniziale.",
    ]),
])


EXPANSION_STUD = sections_html([
    ("Numeri regionali e gap domanda-offerta", [
        "La <strong>Regione Veneto</strong> ha messo in campo piani di ampliamento housing studentesco legati a PNRR e convenzioni con atenei. Non esiste un unico contatore pubblico aggiornato giornalmente, ma la somma di progetti approvati a Padova, Vicenza e Venezia indica migliaia di nuovi letti nel biennio 2025-2027. Il gap residuo alimenta mercato libero descritto in Immobiliare.it Insights.",
        "ISTAT descrive mobilità giovanile veneta verso poli universitari: senza camere strutturate, famiglie sostenono canoni crescenti sul libero. Investimento pubblico-privato mira a stabilizzare accesso meritevole e reddito.",
    ]),
    ("ESU Padova: procedure e trasparenza bandi", [
        "ESU pubblica graduatorie, requisiti ISEE e merito, scadenze domanda studentato. Ogni posto assegnato libera pressione marginale sul mercato; non sostituisce intero fabbisogno. Link ufficiale: esu.pd.it. Consigliamo di non abbandonare ricerca libera finché esito bando non è definitivo se tempi lo permettono.",
        "Convenzioni ESU con residenze calmierate (Vicenza ~30% posti in progetti PNRR) uniscono accesso pubblico e gestione professionale. Percentuali vanno verificate bando per bando.",
    ]),
    ("Operatori privati: Camplus e servizi integrati", [
        "Camplus e operatori analoghi offrono residenze con reception, studio, eventi e manutenzione centralizzata. Canone superiore a ESU ma inferiore a singola premium Portello in molti casi. Target: studenti internazionali e fuori sede che pagano per certezza contrattuale.",
        "FIMAA osserva crescita contratti società-gestore con genitori garanti. Trasparenza su extra (pulizie, deposito, uscita anticipata) è critica in comparazione.",
    ]),
    ("PNRR: tipologie intervento e tempi", [
        "Fondi PNRR finanziano nuova costruzione, riuso edifici e rigenerazione urbana (Tribloc Padova, Casa Querini Vicenza). Tempi cantieristici slittano spesso per vincoli paesaggistici e approvvigionamenti. Studenti entranti 2026 devono pianificare piano B sul libero fino a consegna chiavi.",
        "Regione Veneto rendiconta avanzamento su portali istituzionali: verificare milestone ufficiali, non solo comunicati marketing operatori.",
    ]),
    ("Strutture miste pubblico-privato", [
        "Modello misto combina requisiti accesso ESU su quota posti e gestione imprenditoriale su servizi. Canone intermedio e regolamento più stringente. Obiettivo policy: evitare gentrificazione studentesca pura e mantenere accesso merito/reddito.",
        "Per proprietari privati, aumento offerta strutturata impone competitività su qualità e prezzo in appartamento condiviso.",
    ]),
    ("Venezia: Mestre e terraferma", [
        "Studenti Ca' Foscari e IUAV affrontano costi laguna: nuovi letti a Mestre e Marghera riducono dipendenza da mercato turistico centro. Logistica actv pesa su scelta abitativa quanto canone.",
        "Confronto con Padova non è diretto: offerta e trasporti differiscono. Articolo canoni Padova resta riferimento per capoluogo patavino.",
    ]),
    ("Vicenza: PNRR calmierati e rigenerazione", [
        "Vicenza cresce con Casa Querini e bandi ESU — vedi articolo dedicato calmierati 2026. Domanda lavoro industriale convive con universitari: mercato locativo complesso.",
        "Imprese edili e lavoratori fuori sede aggiungono domanda residenziale non studentesca in stesso comparto.",
    ]),
    ("Impatto su proprietari padovani appartamento condiviso", [
        "Più posti letto non abbassano automaticamente canoni centro storico; possono stabilizzare periferia. Proprietari devono aggiornare arredo, fibra, efficientamento. Servizio locazioni Righetto supporta pricing allineato a comparabili.",
        "Mediazione concordata in mandato; nessun listino percentuale online.",
    ]),
    ("Checklist famiglia 2026", [
        "Monitorare bandi ESU aprile-luglio; parallelamente visitare appartamenti periferia tram; calcolare costo totale; evitare caparra senza contratto; conservare ricevute registrazione.",
        "Cross-link <a href=\"blog-affitti-padova-canoni-2026\">affitti Padova 2026</a> e <a href=\"blog-stanza-universitaria-padova-canoni-2026\">stanze Padova Insights</a>.",
    ]),
    ("Outlook e fonti", [
        "Secondo semestre 2026 vedrà prime consegne PNRR e apertura residenze green Tribloc. Mercato libero resterà rilevante. Fonti: ESU Padova, Regione Veneto, PNRR, FIMAA, ISTAT, Università di Padova.",
        "Per canoni stanza Padova aggiornati consultare Immobiliare.it Insights e articolo dedicato sul blog Righetto. Non citiamo titoli giornalistici come fonte primaria: solo enti e osservatori settore.",
    ]),
    ("Governance e accessibilità residenze", [
        "Bandi PNRR includono requisiti accessibilità e gender balance negli spazi comuni. Residenze moderne devono superare barriere architettoniche rispetto a palazzi storici adibiti a studentato informale. Studenti con disabilità devono verificare camere adattate in graduatoria ESU e in offerta privata.",
        "Regione Veneto pubblica linee guida housing giovani: trasparenza canone e servizi inclusi è obbligatoria negli bandi pubblici.",
    ]),
    ("Padova numeri e fabbisogno residuo", [
        "Università di Padova supera soglia iscritti che rende ogni incremento letti utile ma insufficiente da solo. Immobiliare.it Insights documenta canoni stanza 490 euro sul libero: studentato pubblico e PNRR agiscono su fasce meritevoli, non su tutta la platea. Famiglie classe media alta restano sul mercato.",
        "Camplus e operatori privati colmano segmento intermedio con servizi e flessibilità contrattuale internazionale. FIMAA segnala crescita domanda alloggi certificati per studenti non UE.",
    ]),
    ("Convenzioni ateneo-Regione", [
        "Protocolli tra Università di Padova e Regione Veneto definiscono obiettivi posti letto e criteri sostenibilità. Trasparenza rendicontazione PNRR è obbligo europeo: avanzamento lavori consultabile su portali istituzionali, non solo su social operatori.",
        "Slittamenti cantieri impattano calendario accademico: piano B libero mercato resta necessario fino a consegna chiavi ufficiale.",
    ]),
    ("Qualità gestione vs stock informale", [
        "Appartamenti non adeguati a norme antincendio convivenza restano sul mercato parallelo: bandi PNRR e ESU spingono qualità minima. Proprietario libero deve competere su sicurezza, fibra, efficientamento — non solo prezzo.",
        "Servizio locazioni Righetto promuove contratti conformi e inventario consegna. Mediazione concordata in mandato.",
    ]),
    ("Mobilità interregionale studenti", [
        "ISTAT descrive flusso studenti da Veneto orientale e Triveneto verso Padova e Venezia. Posti letto Vicenza e Mestre riducono pendolarismo lungo autostrada A4. Housing regionale va pianificato a rete, non per singolo comune.",
        "Borse ESU e regionali non coprono sempre delta canone Insights: budgeting triennale consigliato.",
    ]),
    ("Turismo e short term vs studenti Venezia", [
        "Centro Venezia subisce pressione affitti brevi: studentato Mestre-Marghera è priorità policy. Confronto con Padova non è automatico: logistics laguna incide quanto canone.",
        "Regione Veneto coordina limiti e incentivi housing studentesco laguna — verificare delibere aggiornate.",
    ]),
    ("Monitoraggio 2026-2027", [
        "Entro 2027 attendersi migliaia letti aggiuntivi somma Padova Vicenza Venezia se cronoprogrammi rispettati. Mercato libero resterà rilevante per centro Padova e facoltà periferiche.",
        "Aggiornamento " + DATE_IT + ": fonti ESU, Regione Veneto, PNRR, FIMAA, ISTAT, Università di Padova, Immobiliare.it Insights per canoni paralleli.",
    ]),
    ("Costi nascosti e servizi inclusi", [
        "Residenza privata può includere pulizie, Wi-Fi, palestra; ESU no. Confronto canone headline vs costo totale mensile evita sorprese. FIMAA consiglia tabella comparativa scritta prima scelta.",
        "Spese iscrizione universitaria e mensa ESU separati da canone camera: budget familiare integrato.",
    ]),
    ("Gender policy e convivenza", [
        "Nuove residenze PNRR prevedono spazi sicuri e policy anti-discriminazione. Studentato storico mix genere per piano; residenze private offrono floor dedicati. Verificare regolamento before deposit.",
        "Università di Padova promuove inclusione: housing fa parte percorso accoglienza internazionale.",
    ]),
    ("Digitalizzazione domanda posti letto", [
        "ESU e operatori privati migrano domande online con SPID: preparare documenti digitali in anticipo. Errori upload ritardano graduatoria — critico ad agosto.",
        "Regione Veneto dashboard PNRR avanzamento opere: consultare trimestralmente.",
    ]),
    ("Proprietari privati e regolamentazione", [
        "Crescita posti letto pubblici-privati non esenta proprietario da registro contratti e norme fiscali locazione. Cedolare secca o IRPEF da scelta consapevole con commercialista.",
        "Righetto servizio locazioni per mandato conforme; mediazione concordata in sede senza listini online.",
    ]),
    ("Sintesi policy housing Veneto 2026", [
        "Obiettivo regionale: aumentare posti letto accessibili senza sostituire mercato libero. ESU, Camplus, PNRR e PPP convivono; studente deve mappare opzioni entro luglio per anno accademico ottobre. Link utili: blog-affitti-padova-canoni-2026 e blog-stanza-universitaria-padova-canoni-2026 sul sito Righetto.",
        "Fonti citate: ESU Padova, Regione Veneto, PNRR, FIMAA, ISTAT, Università di Padova, Immobiliare.it Insights. Aggiornamento " + DATE_IT + ". Non usiamo titoli giornalistici come fonte primaria; solo enti e osservatori di settore.",
    ]),
])


EXPANSION_GREEN = sections_html([
    ("Contesto urbano area Gozzi", [
        "L'area Gozzi a Padova ha vissuto transizione da office park a mix urbano. Torri Tribloc simboleggiano ciclo edilizio: costruite per uffici, oggi candidate a housing giovani per proximità servizi e riduzione commute. Progetto autorizzato segue percorso amministrativo pubblico: delibere, pareri, cronoprogramma cantieri.",
        "Rigenerazione evita consumo suolo vergine — obiettivo sostenibilità coerente con agenda Regione Veneto e comune.",
    ]),
    ("NZEB in pratica per studenti", [
        "Nearly Zero Energy Building implica isolamento, VMC, rinnovabili dove possibile. Inquilino beneficia bolletta contenuta e comfort termico — differenziale vs appartamento G non riqualificato in periferia. Gestione Swadeshi/Brainville dovrà comunicare regolamento uso impianti.",
        "APE post-intervento atteso in fascia alta: documento utile a genitori che valutano costo totale soggiorno accademico.",
    ]),
    ("Swadeshi e Brainville: ruolo operatore", [
        "Nome operatore compare in atti e comunicati progetto — fatto verificabile, non endorsement Righetto. Gestione professionale implica manutenzione centralizzata, sicurezza accessi, eventuale convenzione parcheggi.",
        "Confrontare condizioni con ESU e privati prima di prenotazione: canone, durata minima, recesso, deposito.",
    ]),
    ("Timeline cantieri e rischi slittamento", [
        "Riqualificazione torri richiede adeguamento antincendio, ascensori, facciate. Slittamenti possibili: studenti 2026/27 devono avere piano B mercato libero o studentato ESU. Tabella timeline in articolo va incrociata con aggiornamenti comunali.",
        "Visite cantiere non sempre possibili; monitorare comunicati ufficiali.",
    ]),
    ("180 camere: dimensione impatto mercato", [
        "Centottanta posti non saturano domanda Padova da soli, ma segnalano trend riuso office. Offerta strutturata con servizi compete con appartamento 4 camere non riqualificato in Guizza.",
        "Immobiliare.it Insights medie stanze restano riferimento mercato libero parallelo.",
    ]),
    ("Collegamenti e competition zone", [
        "Prossimità fermate bus/tram determina attrattività vs Portello. Studenti medicina o Agripolis calcolano spostamenti specifici. Link <a href=\"zona-universitaria-padova\">zona universitaria</a> e <a href=\"visite-virtuali\">visite virtuali</a> per immobili alternativi già disponibili.",
    ]),
    ("Green e valorizzazione immobiliare quartiere", [
        "Riqualificazione energetica edificio grande può trainare upgrade palazzi vicini — effetto spillover urbano. Proprietari limitrofi valutino interventi APE per restare competitivi in locazione.",
        "FIMAA segnala domanda crescente immobili efficienti post-2022 energetico.",
    ]),
    ("Normativa edilizia e destinazione d'uso", [
        "Cambio uso da direzionale a residenziale studenti segue iter urbanistico pubblicato. Non ogni ex ufficio è convertibile: vincoli strutturali e parcheggi condizionano fattibilità.",
        "Università di Padova può collaborare a protocolli accesso studenti meritevoli — verificare eventuali intese future.",
    ]),
    ("Sintesi operativa 2026", [
        "Progetto Tribloc/Gozzi: ~180 camere NZEB, operatore Swadeshi/Brainville, target 2026/27. Non offerta Righetto. Fonti: atti urbanistici, Regione Veneto, operatori. Per locazioni immediate: servizio locazioni agenzia.",
        "Monitoraggio cantieri consigliato per studenti che ritardano decisione alloggio sperando in apertura Tribloc: piano B obbligatorio fino a consegna ufficiale.",
    ]),
    ("Comparazione costi totali di soggiorno", [
        "Canone camera più utenze, mensa, abbonamento TPL e tasse universitarie formano costo reale. Residenza NZEB può ridurre voce energia rispetto ad appartamento classe G in periferia con spese imprevedibili. Simulazione triennale aiuta famiglie fuori sede.",
        "Università di Padova e ESU non coprono costi indiretti: budget familiare deve integrare borsa studio se ammessa.",
    ]),
    ("Materiali green e ciclo vita edificio", [
        "Riqualificazione NZEB seleziona materiali a basso impatto e impianti ad alta efficienza. Costo cantiere elevato ma costo esercizio ridotto per gestore — possibile stabilità canone se energia inclusa nel fee residenza.",
        "Regione Veneto promuove metriche emissioni edilizia pubblica: Tribloc case study riuso vs demolizione.",
    ]),
    ("Servizi smart building", [
        "Access control, prenotazione laundry e monitoraggio consumi sono standard residenze gestite Brainville/Swadeshi. Studenti digital native valutano app servizi come criterio scelta pari al canone.",
        "Privacy dati e regolamento uso spazi comuni vanno letti prima contratto — analogamente a residenze Camplus.",
    ]),
    ("Concorrenza con ESU e libero mercato", [
        "180 posti Tribloc non sostituiscono ESU ma offrono alternativa green a canone mercato per chi non entra graduatoria. Immobiliare.it Insights resta benchmark libero parallelo.",
        "Proprietari appartamento Guizza devono efficientare per non perdere inquilini verso Tribloc apertura 2026/27.",
    ]),
    ("Aggiornamento " + DATE_IT, [
        "Fonti: atti Comune Padova, Regione Veneto, operatori Swadeshi/Brainville, FIMAA, Università di Padova. Progetto descritto genericamente come autorizzato urbano — non scheda commerciale Righetto.",
    ]),
])

EXPANSION_GREEN_B = sections_html([
    ("Riuso torri: precedenti in Europa", [
        "Conversione office-to-housing è trend urbano in città con eccesso spazi direzionali post-pandemia. Padova Tribloc segue logica sostenibilità: meno demolizione, più riqualificazione NZEB. Regione Veneto inserisce progetto in strategia rigenerazione suolo urbanizzato.",
        "Studenti abituati a appartamenti anni Novanta in periferia possono trovare servizi residenza superiore se canone allineato — confronto da fare a apertura.",
    ]),
    ("Brainville e Swadeshi: profilo operatore", [
        "Brainville compare come gruppo gestione immobiliare studentesca; Swadeshi come veicolo progetto Tribloc in atti pubblici. Verificare contratto locazione e regolamento quando prenotazioni apriranno — non anticipare condizioni non pubblicate.",
        "Operatori privati competono con ESU e Camplus: mappa offerta 2026 in articolo studentati Veneto.",
    ]),
    ("Antincendio e sicurezza high-rise", [
        "Torri richiedono adeguamento vie esodo, rilevazione fumi, gestione evacuazione format residenti. Cantiere 2025-2026 deve completare collaudo prima ingresso — slittamento possibile.",
        "Genitori valutino sicurezza come criterio pari al canone.",
    ]),
    ("Spazi comuni e community", [
        "Residenze studenti moderne prevedono coworking, cucine condivise, lavanderia. Tribloc target studenti e giovani lavoratori: mix convivenza diversa da solo-studenti ESU.",
        "Regolamento convivenza sarà vincolante come in private hall.",
    ]),
    ("Confronto bolletta NZEB vs classe G", [
        "Simulazione: appartamento classe G periferia può costare doppio gas rispetto NZEB con VMC — voce rilevante in 8-10 mesi contratto accademico. Immobiliare.it Insights non include utenze: costo totale va modellato.",
        "ISTAT energia household giovani: spesa in crescita 2022-2026.",
    ]),
    ("Proprietari limitrofi Gozzi", [
        "Riqualificazione Tribloc può alzare aspettative inquilini su quartiere: palazzi vicini beneficiano externalities o subiscono cantieri. FIMAA consiglia manutenzione facciate e APE aggiornato.",
        "Servizio locazioni Righetto per immobili area Gozzi e Padova est.",
    ]),
    ("Alternativa immediata mercato libero", [
        "Chi non può attendere 2026/27 usa mercato libero o ESU — link blog-affitto-studenti-padova e blog-stanza-universitaria-padova-canoni-2026. Visite virtuali per famiglie distant.",
        "Non ritardare ricerca oltre luglio sperando Tribloc senza data certa.",
    ]),
    ("Università di Padova e distanza dipartimenti", [
        "Mapping tempi reali verso Ingegneria, Economia, Scienze determina scelta Tribloc vs Portello. Tram e bus TPL Padova integrano spostamenti — abbonamento nel budget.",
        "ESU Padova graduatoria indipendente da Tribloc: doppia candidatura consigliata.",
    ]),
    ("Monitoraggio cantiere fonti ufficiali", [
        "Comune Padova sportello urbanistica e Regione Veneto PNRR: aggiornamenti ufficiali. Evitare rumor social non verificati su date apertura.",
        "Aggiornamento contenuto " + DATE_IT + ".",
    ]),
])

EXPANSION_GREEN_C = sections_html([
    ("Economia circolare e riuso", [
        "Riuso torri riduce embodied carbon rispetto demolizione e ricostruzione. Regione Veneto promuove indicatori sostenibilità edilizia pubblica. Studenti sensibili a climate topic possono preferire residenza NZEB.",
        "Progetto Tribloc case study policy regionale housing giovani.",
    ]),
    ("Canone atteso e servizi", [
        "Canone non pubblicato in atti urbanistici: sarà definito operatore Swadeshi/Brainville pre-apertura. Confrontare con ESU calmierato e private hall Camplus quando listino disponibile.",
        "Immobiliare.it Insights resta benchmark libero parallelo intorno 490 euro stanza Padova.",
    ]),
    ("Mix studenti e young workers", [
        "Target progetto include giovani lavoratori oltre studenti: convivenza intergenerativa diversa da solo-universitari. Regolamento dovrà gestire orari e usi spazi comuni.",
        "Università di Padova possibile partner accoglienza — verificare protocolli.",
    ]),
    ("Parcheggi e mobilità dolce", [
        "Ex office spesso include parcheggi convertiti bike storage o car sharing. Area Gozzi collegata rete ciclabile padovana in espansione.",
        "Costo parcheggio auto privato evitabile con TPL — budget familiare.",
    ]),
    ("Due diligence genitori investitori", [
        "Progetto non è proposta investimento Righetto: descriviamo fatto urbano pubblico. Investitori privati area Gozzi valutino APE comparables post-Tribloc.",
        "FIMAA mercato locativo studentesco Padova orientale.",
    ]),
    ("Piano B affitto 2026", [
        "Studenti ammessi ottobre 2026 senza posto Tribloc: mercato libero, ESU, Camplus — articoli blog correlati. Visite virtuali immobili disponibili oggi.",
        "Non posticipare ricerca oltre luglio 2026.",
    ]),
    ("Sintesi Tribloc " + DATE_IT, [
        "180 camere NZEB, Gozzi, Swadeshi/Brainville, apertura target 2026/27. Fonti Comune Padova, Regione Veneto, FIMAA, Università di Padova, Immobiliare.it Insights. Verificare atti prima di decisioni vincolanti.",
    ]),
    ("Collegamenti articoli Righetto", [
        "Per studentati regionali leggere blog-studentati-veneto-2026-posti-letto; per canoni libero blog-stanza-universitaria-padova-canoni-2026; per zone blog-affitto-studenti-padova e zona-universitaria-padova.",
        "Servizio locazioni e visite virtuali disponibili per immobili già sul mercato mentre Tribloc completa cantiere. Mediazione concordata in sede; nessun listino percentuale online. Richieste via form in fondo pagina o tel. 049.8843484, senza impegno. Contattaci oggi. Verifica fonti.",
    ]),
])


EXPANSION_VICENZA = sections_html([
    ("Mercato locativo vicentino", [
        "Vicenza combina domanda industriale e universitaria: canoni liberi crescono dove posti letto strutturati mancano. ISTAT e dati comunali descrivono tensione abitativa giovani. PNRR student housing mira a canoni calmierati accessibili.",
        "Confronto con Padova Insights (490 euro stanza) mostra gap regionale: Vicenza non necessariamente più economica sul libero.",
    ]),
    ("PNRR calmierati: meccanismo", [
        "Finanziamento pubblico condiziona canone massimo e quota posti riservati. Beneficiari: studenti meritevoli e giovani lavoratori in fasce reddito definite da bando. Non è alloggio gratuito: canone ridotto rispetto mercato.",
        "Regione Veneto supervisiona adempimenti; slittamenti cantieri impattano calendario ingressi.",
    ]),
    ("Convenzione ESU ~30%", [
        "Quota indicativa 30% posti via ESU va verificata su bando Casa Querini e successivi. Graduatoria merito/reddito identica logic ESU Padova. Resto posti a canone intermedio o mercato controllato.",
        "Studenti fuori graduatoria restano su libero o altre residenze venete.",
    ]),
    ("Casa Querini: rigenerazione urbana", [
        "Complesso storico sottoposto a recupero con progettazione Saudino — nome pubblico progetto urbano. Vincoli paesaggistici allungano tempi ma elevano qualità architettonica. Servizi comuni e accessibilità obbligatori in bandi PNRR.",
        "Non confondere rigenerazione con semplice rifacimento cosmetico: impianti e struttura devono rispettare normativa antisismica ed energetica vigente.",
    ]),
    ("Saudino: ruolo progettuale", [
        "Saudino compare quale soggetto progettazione/gestione in documenti pubblici Vicenza — riferimento fact-based senza slogan marketing. Verificare comunicati Comune Vicenza per aggiornamenti.",
    ]),
    ("Confronto modelli abitativi", [
        "Libero mercato centro Vicenza vs calmierato PNRR vs studentato ESU altrove: tre fasce prezzo. Famiglia deve calcolare trasporti verso sedi studio e stage.",
        "Cross-link studentati Veneto e stanze Padova per quadro regionale.",
    ]),
    ("Proprietari e investitori vicentini", [
        "Aumento offerta calmierata sposta domanda marginale dal libero mid-range. Immobili obsoleti perdono appeal. Righetto 101 comuni include Vicenza per locazioni.",
        "Mediazione concordata in sede; no tariffe online.",
    ]),
    ("Checklist studente Vicenza 2026", [
        "Leggere bandi PNRR e ESU; candidarsi entro scadenza; parallelamente cercare libero; verificare contratto e caparra; calcolare costo totale.",
        "Fonti: Regione Veneto, ESU, Comune Vicenza, ISTAT.",
    ]),
    ("Trasporti e connessione poli formativi", [
        "Vicenza collega treni regionali e bus verso Padova e Verona: studenti pendolari devono calcolare abbonamento oltre canone calmierato. Residenza Querini riduce pendolarismo se sedi locali coprono corso scelto.",
        "ISTAT segnala costi mobility giovani in crescita: housing calmierato senza trasporto efficiente perde vantaggio economico.",
    ]),
    ("Rigenerazione urbana e valore immobiliare", [
        "Casa Querini innesta housing studenti in tessuto urbano esistente: externalità positive su commercio quartiere se gestione responsabile. Proprietari limitrofi possono beneficiare riqualificazione area.",
        "FIMAA monitora locazioni giovani Vicenza: qualità minima sale con PNRR.",
    ]),
    ("Bandi e documentazione domanda", [
        "Domanda ESU richiede ISEE, certificati merito, documenti identità. Posti PNRR possono avere finestra domanda distinta: calendario Comune Vicenza e ESU da consultare mensilmente.",
        "Non affidarsi a screenshot social: solo portali istituzionali.",
    ]),
    ("Confronto PNRR altre città venete", [
        "Padova Tribloc e Venezia Mestre aggiungono posti green e calmierati: Vicenza non è isolata. Rete regionale housing studentesco 2026-2027 va letta insieme.",
        "Cross-link <a href=\"blog-studentati-veneto-2026-posti-letto\">studentati Veneto</a> e <a href=\"blog-residenze-green-padova-tribloc-2026\">Tribloc Padova</a>.",
    ]),
    ("Proprietari: come reagire ai calmierati", [
        "Offerta pubblica non elimina libero ma stringe fascia mid: immobili ristrutturati con APE buono restano competitivi. Servizio locazioni Righetto per pricing e contratti.",
        "Mediazione concordata in mandato; aggiornamento " + DATE_IT + ".",
    ]),
])


EXPANSION_EDIL = sections_html([
    ("Edilcassa Veneto nel sistema Confartigianato", [
        "<strong>Edilcassa</strong> eroga welfare edile: malattia, maternità, formazione, contributi. Il fondo garanzia 250.000 euro nel contratto regionale 2025/2026 è strumento aggiuntivo per situazioni contributive o di sostegno imprese/lavoratori iscritti — comunicato <strong>Confartigianato Veneto</strong>.",
        "Non va confuso con fondo perduto o mutuo prima casa: finalità cassa edile.",
    ]),
    ("Contratto regionale edilizia 2025/2026", [
        "Contratto collettivo definisce minimi retributivi, welfare, edilcassa. Fondo garanzia va letto nell'integrale testo ufficiale e circolari Edilcassa Veneto. Imprese verificano con consulente del lavoro aderenza e procedura accesso.",
        "Regione Veneto coordina tavolo edilizia veneta con parti sociali.",
    ]),
    ("Corporate housing: modello operativo", [
        "Imprese venete edili affittano appartamenti multi-camera per squadre cantieri temporanei. Società garantisce canone e sostituzione lavoratori. Riduce assenteismo e costi di ricerca alloggio per dipendenti distaccati.",
        "Contratto locazione società-intestatario immobile; sublocazione interna regolata da regolamento impresa.",
    ]),
    ("Co-housing lavoratori vs studenti", [
        "Co-housing edile condivide logica convivenza studenti ma target diverso: turni cantiere, durata breve, necessità parcheggio furgoni. Norme sicurezza e capienza abitativa vanno rispettate.",
        "FIMAA distinge locazione abitativa da alloggio temporaneo lavoro — verificare urbanistica.",
    ]),
    ("Tabella garanzie: approfondimento", [
        "Deposito cauzionale tutela proprietario da danni. Garanzia bancaria sostituisce deposito liquido inquilino. Fideiussione corporate tutela locator da morosità impresa. Fondo Edilcassa tutela sistema contributivo edile — quadranti diversi.",
        "Imprese che locano alloggi squadre possono combinare fideiussione societaria e deposito ridotto negoziato.",
    ]),
    ("Mercato immobiliare Padovano e lavoratori", [
        "Cantieri provincia Padova generano domanda locazioni brevi-medium in Limena, Rubano, cintura. Righetto servizio locazioni supporta proprietari e aziende. ISTAT mobilità lavoro veneta.",
        "350+ immobili, 101 comuni, dal 2000 — claim verificati.",
    ]),
    ("Sostenibilità economica impresa edile", [
        "Alloggio dignitoso riduce turnover ma costa: impresa deve bilanciare indennità trasferta vs housing diretto. Commercialista valuta deducibilità e contratti.",
        "Fondo garanzia Edilcassa non paga affitti ma stabilizza sistema impresa-lavoratore.",
    ]),
    ("Checklist HR impresa edile", [
        "Contratto quadro locazione; APE e conformità; regolamento convivenza; assicurazione responsabilità; uscita fine cantiere; confronto costo vs indennità.",
        "Fonti: Edilcassa Veneto, Confartigianato Veneto, ISTAT, Regione Veneto.",
    ]),
    ("Limiti consulenza Righetto", [
        "Non siamo consulenti del lavoro o legali edili. Supportiamo ricerca immobili e contratti locazione. Mediazione concordata in mandato.",
    ]),
    ("Formazione edile e attrattività settore", [
        "Edilcassa finanzia anche formazione professionale: manodopera qualificata è scarica nel Veneto. Housing aziendale diventa leva recruiting oltre che welfare. Imprese piccole possono aggregarsi per locazioni condivise tramite consorzio.",
        "Confartigianato Veneto monitora andamento settore: fondo garanzia 250.000 euro va letto nel contesto pacchetto welfare contrattuale 2025/2026, non isolato.",
    ]),
    ("Cantieri temporanei e domanda locativa Padovano", [
        "Province Padova, Vicenza, Treviso concentrano cantieri infrastrutturali e ristrutturazioni: squadre distaccate cercano alloggi 3-12 mesi. Corporate housing riduce turnover rispetto a hotel ma richiede gestione immobiliare.",
        "Proprietari con trilocale periferia possono locare a impresa edile con fideiussione: servizio locazioni Righetto struttura trattativa.",
    ]),
    ("Welfare integrato e fondo garanzia", [
        "Fondo 250.000 euro si affianca a malattia, maternità, integrazioni: non è voucher affitto. Lavoratore edile in crisi contributiva non deve confondere tutele cassa con deposito proprietario.",
        "Edilcassa Veneto pubblica circolari interpretative: consultare sito ufficiale e patronato.",
    ]),
    ("Co-housing imprese venete del settore edile", [
        "Modello generico: consorzio imprenditori edili veneti affitta unità multi-camera rotating workforce. Regolamento turni, pulizie e parcheggio mezzi leggeri. Urbanistica residenziale standard — no baracche cantieri.",
        "Confronto costo housing vs diaria alloggio in hotel lungo cantiere plurimensile favore spesso housing.",
    ]),
    ("Sicurezza sul lavoro e alloggio", [
        "Riposo adeguato incide su infortuni: imprese responsabili organizzano alloggio dignitoso entro ragionevole distanza cantiere. ASL e normativa sicurezza non sostituiscono contratto locazione conforme.",
        "ISTAT dati pendolarismo edile veneto: housing riduce km giornalieri e stanchezza.",
    ]),
    ("Aggiornamento fonti " + DATE_IT, [
        "Edilcassa Veneto, Confartigianato Veneto, Regione Veneto, ISTAT, FIMAA per locazioni. Righetto: mediazione concordata in sede, 101 comuni, dal 2000.",
    ]),
])

EXPANSION_VICENZA_B = sections_html([
    ("Storia Casa Querini e tessuto urbano", [
        "Recupero edificio storico Vicenza richiede equilibrio conservazione e funzione studentesca. Progetto Saudino negli atti pubblici definisce intervento strutturale non solo cosmetico. Tempi cantieristici allungati rispetto new build.",
        "Comune Vicenza rendiconta avanzamento PNRR su portali istituzionali.",
    ]),
    ("Canone calmierato vs libero: simulazione budget", [
        "Famiglia deve modellare canone calmierato + trasporti vs libero centro storico Vicenza. ISTAT costo vita giovani Veneto orientale in crescita. ESU quota 30% non garantita: candidatura obbligatoria.",
        "Immobiliare.it Insights utile se studente pendolare verso Padova.",
    ]),
    ("ESU Vicenza e Padova: doppia domanda", [
        "Studenti possono concorrere a graduatorie territoriali diverse se iscritti altrove: verificare regolamento ESU vigente. Non duplicare caparra su libero senza piano B.",
        "Università collegata sistema veneto: mobilità inter-ateneo frequente.",
    ]),
    ("Rigenerazione e valorizzazione quartiere", [
        "Housing studenti PNRR può rivitalizzare area degradata se gestione post-consegna curata. Proprietari privati limitrofi monitorino APE e facciate.",
        "FIMAA locazioni giovani Vicenza: qualità minima in salita.",
    ]),
    ("Confronto Vicenza-Padova-Venezia", [
        "Rete posti letto 2026-2027 va letta regionale: studentati Veneto articolo correlato. Vicenza calmierati non isolati da Tribloc Padova e Mestre.",
        "Cross-link blog-studentati-veneto-2026-posti-letto e blog-residenze-green-padova-tribloc-2026.",
    ]),
    ("Checklist contratto libero parallelo", [
        "Se fuori graduatoria PNRR: contratto registrato, caparra documentata, APE, regolamento convivenza. Servizio locazioni Righetto su 101 comuni.",
        "Mediazione concordata in mandato; aggiornamento " + DATE_IT + ".",
    ]),
])

EXPANSION_VICENZA_C = sections_html([
    ("PNRR housing: criteri ammissione", [
        "Bandi pubblicano ISEE massimo, merito minimo, priorità fuori sede. Casa Querini seguirà schema PNRR regionale — leggere integrale bando Comune Vicenza e Regione Veneto.",
        "ESU gestisce quota ~30% posti: doppia candidatura consigliata entro scadenze ufficiali.",
    ]),
    ("Saudino e rigenerazione: dettaglio tecnico", [
        "Intervento strutturale su Casa Querini include adeguamento sismico ed energetico ove richiesto da normativa. Progettazione Saudino negli atti pubblici non è endorsement commerciale Righetto.",
        "Vincoli paesaggistici centro Vicenza allungano cronoprogramma rispetto new build periferia.",
    ]),
    ("Canoni calmierati: cosa significa in euro", [
        "Canone calmierato è inferiore a libero mercato centro ma non zero: importo definito bando PNRR. Confrontare costo totale con pendolarismo Padova se corso lo consente.",
        "Immobiliare.it Insights utile benchmark regionale stanze.",
    ]),
    ("Mercato libero Vicenza centro", [
        "Proprietari appartamento condiviso competono con PNRR: APE e manutenzione decisive. FIMAA segnala domanda giovani lavoratori oltre studenti.",
        "Servizio locazioni Righetto include Vicenza tra 101 comuni.",
    ]),
    ("Regione Veneto e rendicontazione", [
        "PNRR richiede trasparenza avanzamento opere e posti consegnati. Consultare portali istituzionali trimestralmente, non solo flyer operatori.",
        "ISTAT costo vita Vicenza orientale in trend crescente 2024-2026.",
    ]),
    ("Studenti pendolari Padova-Vicenza", [
        "Alcuni iscritti pendolano: housing Vicenza calmierato conviene se sedi locali coprono piano studi. Altrimenti Padova Insights 490 euro stanza resta riferimento.",
        "Cross-link blog-stanza-universitaria-padova-canoni-2026.",
    ]),
    ("Impatto urbano Querini", [
        "Rigenerazione può migliorare servizi quartiere se gestione post-consegna curata. Externalities positive per immobili limitrofi riqualificati.",
        "Comune Vicenza comunicati ufficiali unica fonte date ingresso.",
    ]),
    ("Checklist genitori 2026", [
        "Leggere bando PNRR Casa Querini; candidatura ESU; piano B libero; contratto registrato; budget trasporti; aggiornamento " + DATE_IT + ".",
        "Fonti: Regione Veneto, ESU, Comune Vicenza, ISTAT, FIMAA — non titoli giornalistici.",
    ]),
])

EXPANSION_VICENZA_D = sections_html([
    ("Accessibilità e inclusione PNRR", [
        "Bandi PNRR prevedono camere accessibili e percorsi barrier-free in rigenerazione Querini. Studenti con disabilità devono verificare posti dedicati in graduatoria ESU e bando PNRR.",
        "Regione Veneto linee guida inclusione housing giovani.",
    ]),
    ("Trasparenza canone e servizi inclusi", [
        "Canone calmierato deve essere pubblicato in bando con elenco servizi (pulizie, utenze, Wi-Fi). Confrontare costo totale con libero mercato centro Vicenza.",
        "FIMAA consiglia contratto scritto e registrato anche per posti PNRR gestiti privati.",
    ]),
    ("Impatti su quartiere storico", [
        "Rigenerazione Querini può aumentare vivibilità se gestione post-consegna curata (rumori, orari). Comune Vicenza regolamenta convivenza studentesca in centro storico.",
        "Proprietari limitrofi beneficiano se externalities positive su commercio e sicurezza.",
    ]),
    ("Mobilità regionale Veneto", [
        "Studenti move between Vicenza, Padova, Verona, Venezia: rete posti letto 2026 va pianificata regionalmente. Articolo studentati Veneto collega i poli.",
        "ISTAT pendolarismo giovani in crescita.",
    ]),
    ("Due diligence contratto libero", [
        "Fuori graduatoria: verificare APE, caparra, registro contratto, regolamento convivenza. Servizio locazioni Righetto su Vicenza e 101 comuni.",
        "Mediazione concordata in mandato; no listini online.",
    ]),
    ("Sintesi Vicenza " + DATE_IT, [
        "Casa Querini, Saudino, PNRR calmierati, ESU ~30%. Fonti Regione Veneto, ESU, Comune Vicenza, ISTAT, FIMAA, Immobiliare.it Insights per benchmark Padova.",
    ]),
    ("Policy housing giovani Regione Veneto", [
        "Regione coordina PNRR studentati con piano casa giovani e mobilità sostenibile. Vicenza Casa Querini è tassello rete veneta insieme Tribloc Padova e Mestre Venezia.",
        "Consultare portali istituzionali mensilmente per avanzamento lavori e aperture graduatorie — non decisioni basate su voci non verificate.",
    ]),
    ("Link utili blog Righetto", [
        "Approfondimenti correlati: blog-studentati-veneto-2026-posti-letto, blog-stanza-universitaria-padova-canoni-2026, blog-residenze-green-padova-tribloc-2026, servizio-locazioni.",
        "Form lead in fondo pagina per richieste su locazioni Vicenza e Padova — aggiornamento contenuti " + DATE_IT + ". Tel. 049.8843484 per informazioni preliminari.",
    ]),
])

EXPANSION_EDIL_C = sections_html([
    ("Dettaglio contratto regionale 2025/2026", [
        "Contratto edilizia veneto definisce minimi tabellari, scatti anzianità, welfare edilcassa incluso fondo garanzia 250.000 euro. Testo integrale su siti Confartigianato Veneto e Edilcassa.",
        "Imprese verificano con consulente del lavoro applicazione fondo.",
    ]),
    ("Garanzia affitto vs fondo Edilcassa: casi pratici", [
        "Lavoratore edile moroso su deposito cauzionale: tutela proprietario via deposito/fideiussione, non fondo Edilcassa. Impresa in crisi contributiva: possibile accesso fondo garanzia se requisiti iscrizione.",
        "Tabella articolo riassume quadranti.",
    ]),
    ("Corporate housing imprese venete edili", [
        "Modello generico: società edile veneta affitta trilocale per squadra 4-6 persone su cantiere 6-12 mesi. Fideiussione società sostituisce deposito individuale.",
        "Righetto servizio locazioni struttura contratto quadro e consegne chiavi.",
    ]),
    ("Co-housing turni cantiere", [
        "Regolamento interno definisce turni riposo, pulizie, parcheggio furgoni. Capacità abitativa rispettata per mq abitativi.",
        "FIMAA: verificare urbanistica residenziale, non baracca.",
    ]),
    ("Limena Rubano: domanda locativa lavoratori", [
        "Cintura Padova ospita distacchi cantieri urbani ed extraurbani. Proprietario può locare a impresa referenziata con garanzia bancaria.",
        "350+ immobili Righetto dal 2000.",
    ]),
    ("ISTAT e mobilità comparto edile", [
        "Veneto concentra imprese edili: distacchi frequenti. Housing aziendale riduce costi hotel e migliora recruiting.",
        "Commercialista valuta deducibilità canone.",
    ]),
    ("Welfare integrato Edilcassa", [
        "Fondo garanzia affianca malattia, maternità, formazione — pacchetto 2025/2026. Non sostituisce responsabilità datore su alloggio sicuro.",
        "Confartigianato Veneto monitora settore.",
    ]),
    ("Sintesi operativa " + DATE_IT, [
        "Fondo 250.000 euro Edilcassa Veneto, corporate housing, tabella garanzie. Fonti Edilcassa, Confartigianato, ISTAT, Regione Veneto, FIMAA locazioni.",
    ]),
])

EXPANSION_EDIL_D = sections_html([
    ("Confartigianato Veneto e tavolo edilizia", [
        "Confartigianato Veneto rappresenta imprese artigiane edili e coordina contratto regionale 2025/2026 con Edilcassa. Fondo garanzia 250.000 euro va inserito nel pacchetto welfare negoziato, non isolato da comunicati social.",
        "Imprenditori scaricano circolari ufficiali Edilcassa Veneto per modalità accesso e requisiti iscrizione.",
    ]),
    ("Responsabilità datore su alloggio squadre", [
        "Alloggio dignitoso per lavoratori distaccati rientra in obblighi sicurezza e welfare aziendale. Corporate housing non esime da conformità urbanistica e contratto locazione registrato.",
        "FIMAA supporta proprietari che locano a imprese con fideiussione bancaria referenziata.",
    ]),
    ("Confronto hotel vs appartamento cantiere", [
        "Hotel costa di più su cantieri plurimensili; appartamento corporate housing stabilizza spesa e migliora riposo squadre. Commercialista valuta deducibilità e fringe benefit.",
        "ISTAT costi trasferta edilizia in crescita Nord-Est 2024-2026.",
    ]),
    ("Proprietario: locare a impresa edile veneta", [
        "Trilocale Limena/Rubano/Cintura Padova locato a società edile con contratto quadro e fideiussione. Righetto servizio locazioni struttura trattativa e consegna chiavi.",
        "Mediazione concordata in mandato; no listini online.",
    ]),
    ("Formazione Edilcassa e recruiting", [
        "Welfare edilcassa include formazione professionale oltre fondo garanzia: housing diventa leva recruiting giovani nel comparto edile veneto.",
        "Regione Veneto monitora occupazione settore edilizia post-crisi energetica.",
    ]),
    ("Sintesi Edilcassa " + DATE_IT, [
        "Fondo 250.000 euro pool 2025/26, corporate housing co-living, tabella vs deposito e fideiussione. Fonti Edilcassa Veneto, Confartigianato Veneto, ISTAT, Regione Veneto, FIMAA. Non fonti giornalistiche.",
    ]),
])

EXPANSION_EDIL_B = sections_html([
    ("Edilcassa: cosa non copre il fondo garanzia", [
        "Fondo 250.000 euro pool 2025/2026 non paga canoni né depositi cauzionali. Tutele malattia e maternità restano istituti separati. Confusione frequent tra welfare edile e garanzia affitto — chiarire con patronato.",
        "Imprese edili consultino circolare Edilcassa Veneto integrale.",
    ]),
    ("Corporate housing: casi d'uso Veneto", [
        "Cantieri Brennero corridor, ristrutturazioni Padova centro, impianti Vicenza: squadre distaccate settimane/mesi. Appartamento 3-4 camere Limena/Rubano locato a società con fideiussione.",
        "Righetto servizio locazioni per mandato multi-camera.",
    ]),
    ("Co-housing regolamentato", [
        "Regolamento interno turni, pulizie, divieto subaffitto non autorizzato. Capacità massima abitativa rispettata per mq. Urbanistica residenziale standard.",
        "FIMAA distingue locazione abitativa da alloggio temporaneo lavoro.",
    ]),
    ("Deposit vs fideiussione aziendale", [
        "Tabella articolo riassume: fondo Edilcassa welfare; deposito tutela proprietario; fideiussione corporate sostituisce deposito lavoratore. Negoziazione caso per caso.",
        "Proprietario preferisce fideiussione bancaria impresa referenziata.",
    ]),
    ("ISTAT mobilità lavoro edilizia", [
        "Veneto concentra imprese edili e distacchi: housing riduce costi indiretti vs hotel. Commercialista valuta deducibilità canone a carico impresa.",
        "Regione Veneto tavolo edilizia 2025/2026 include welfare integrato.",
    ]),
    ("Limena e cintura Padova: domanda locativa lavoratori", [
        "Comuni cintura ospitano lavoratori cantieri urbani ed extraurbani. Proprietario trilocale può locare a impresa edile veneta settore con contratto quadro.",
        "350+ immobili Righetto, 101 comuni, dal 2000.",
    ]),
    ("Formazione sicurezza e riposo", [
        "Alloggio dignitoso parte prevenzione infortuni per Confartigianato. Edilcassa promuove formazione continua oltre fondo garanzia.",
        "Aggiornamento " + DATE_IT + "; fonti Edilcassa Veneto, ISTAT, FIMAA.",
    ]),
])


def build_body_stanza_padova() -> str:
    return f"""
<div class="aeo-box">
<h2>In sintesi</h2>
<p style="font-size:.84rem;margin:0 0 .6rem">A Padova il <strong>canone medio di una stanza in affitto per studenti</strong> si avvicina a <strong>490 euro al mese</strong>, con variazione stimata <strong>+46% rispetto al 2020</strong> secondo <strong>Immobiliare.it Insights</strong> (marzo 2026).</p>
<ul style="font-size:.84rem"><li>Contesto: <strong>FIMAA</strong>, <strong>ESU Padova</strong>, <strong>Università di Padova</strong></li>
<li>Guide: <a href="blog-affitto-studenti-padova">affitto studenti</a>, <a href="servizio-locazioni">locazioni</a>, <a href="zona-universitaria-padova">zona universitaria</a></li></ul>
</div>
<div class="stats-grid">
  <div class="stat-card"><div class="stat-num">490 €</div><div class="stat-label">Canone medio</div></div>
  <div class="stat-card"><div class="stat-num">+46%</div><div class="stat-label">Vs 2020</div></div>
  <div class="stat-card"><div class="stat-num">335 €</div><div class="stat-label">Riferimento 2020</div></div>
  <div class="stat-card"><div class="stat-num">60k+</div><div class="stat-label">Iscritti Uni PD</div></div>
</div>
<h2>Canoni stanza universitaria: cosa dicono i dati</h2>
<p>Padova concentra una delle università storiche d'Europa; l'<strong>Università di Padova</strong> traina domanda abitativa costante. Quando posti letto pubblici e privati non coprono tutti gli iscritti, il mercato libero fissa prezzi sulle <strong>stanze singole</strong>. <strong>Immobiliare.it Insights</strong> (marzo 2026) indica circa <strong>490 euro</strong> di media, contro <strong>335 euro</strong> nel 2020: +46% che riflette domanda, energetico e stock limitato in centro.</p>
<p>Non confondere media portale e singolo annuncio: spese, arredo e piano cambiano il canone. Incrociare con OMI Agenzia delle Entrate aiuta a capire se un prezzo è coerente con la microzona. In agenzia vediamo ricerche concentrate tra maggio e luglio; chi arriva a settembre trova meno scelta e canoni più rigidi.</p>
{chart_padova_canoni()}
{blog_fig(*ASSETS["stanza"]["figs"][0])}
<h2>FIMAA Veneto e prassi contrattuale</h2>
<p>La <strong>FIMAA</strong> del Veneto segnala, nel locativo studentesco, maggiore attenzione a contratti registrati, caparre documentate e regolamenti di convivenza. Proprietari che sottovalutano la manutenzione (caldaia, infissi, impianto elettrico) perdono competitività rispetto a studentati nuovi. Il <a href="servizio-locazioni">servizio locazioni</a> Righetto supporta redazione contratto e consegna chiavi; compenso mediazione concordato in mandato, senza listini online.</p>
<h2>ESU Padova: studentato pubblico e graduatorie</h2>
<p>L'<strong>ESU Padova</strong> eroga borse e gestisce posti letto a canone calmierato per studenti con requisiti di merito e reddito. Bandi e scadenze sono sul sito ufficiale ESU: ogni posto assegnato riduce marginalmente la pressione sul libero, ma migliaia restano fuori graduatoria. Chi non accede allo studentato deve pianificare budget allineato ai dati Insights o spostarsi verso periferie col tram.</p>
{blog_fig(*ASSETS["stanza"]["figs"][1])}
<h2>Tram e periferia: strategia budget</h2>
<p>Arcella, Guizza, Ponte di Brenta e Cittadella, servite dal <strong>tram</strong> TPL Padova, offrono spesso camere sotto la media del Portello. Il trade-off è tempo di spostamento e convivenza in appartamento condiviso. Genitori fuori Veneto possono usare <a href="visite-virtuali">visite virtuali</a> prima del contratto. La scheda <a href="zona-universitaria-padova">zona universitaria</a> descrive servizi e viabilità del cuore universitario.</p>
{blog_fig(*ASSETS["stanza"]["figs"][2])}
{chart_tram_zones()}
<div class="kpi-strip">
  <div><strong>490 €</strong><span>media 2026</span></div>
  <div><strong>335 €</strong><span>media 2020</span></div>
  <div><strong>+46%</strong><span>Insights</span></div>
  <div><strong>101</strong><span>comuni Righetto</span></div>
</div>
<h2>Confronto Veneto</h2>
{table_veneto_canoni()}
<p>Venezia e Verona mostrano pressioni diverse; Vicenza cresce con nuovi posti PNRR. Treviso resta collegata al corridoio Padova-Venezia per pendolari e studenti. Per quadro locativo padovano completo: <a href="blog-affitti-padova-canoni-2026">affitti Padova canoni 2026</a>.</p>
<p>Immobiliare.it Insights resta la fonte primaria citata per la media padovana 490 euro; OMI e FIMAA completano il triangolo di verifica prima di firmare qualsiasi contratto transitorio o 4+4 per camera singola.</p>
<p>Chi loca o cerca in <a href="zona-universitaria-padova">zona universitaria</a> trova in agenzia supporto documentale e comparazione annunci allineata alle fonti istituzionali citate in articolo, senza promesse di canone garantito. Mediazione concordata in sede, senza listini online.</p>
<h2>Checklist studente e proprietario</h2>
<ol>
<li>Confrontare annuncio con media <strong>Immobiliare.it Insights</strong> e comparabili zona.</li>
<li>Verificare APE, spese condominiali, regolamento interno.</li>
<li>Calcolare costo reale spostamento (abbonamento TPL, bici).</li>
<li>Controllare bandi <strong>ESU Padova</strong> prima di impegnare caparra sul libero.</li>
<li>Registrare contratto e documentare caparra — prassi FIMAA.</li>
</ol>
<p>ISTAT monitora il peso della spesa abitativa sulle famiglie: includere mensa e trasporti nel budget mensile oltre al canone camera.</p>
<h2>Proprietari: posizionare il canone senza perdere inquilini</h2>
<p>Canoni sopra mercato lasciano stanze vuote ad agosto; canoni sotto mercato erodono margine dopo IMI e manutenzione. Documentare classe energetica e interventi recenti giustifica premium. Per conversioni da uso familiare a locazione studentesca servono verifiche urbanistiche con tecnico.</p>
<h2>Domanda internazionale e Erasmus</h2>
<p>L'<strong>Università di Padova</strong> attira studenti Erasmus e fuori sede; molti cercano contratti 6–10 mesi. Clausole chiare su recesso e sostituzione coinquilino evitano contenziosi. FIMAA consiglia inventory fotografico alla consegna chiavi.</p>
<h2>Outlook estate 2026</h2>
<p>Nuovi posti letto (studentato e residenze) possono stabilizzare alcune fasce, ma Portello resterà premium. Muoversi entro luglio conviene per chi entra ad ottobre. Aggiornamento {DATE_IT}; fonti: Immobiliare.it Insights, ESU, FIMAA, ISTAT.</p>
{EXPANSION_STANZA}
<a class="cta-deep" href="servizio-locazioni">Servizio locazioni</a>
<a class="cta-deep" href="blog-affitto-studenti-padova" style="background:var(--blu);color:#fff">Guida affitto studenti</a>
"""

def build_body_studentati_veneto() -> str:
    return f"""
<div class="aeo-box">
<h2>In sintesi</h2>
<p style="font-size:.84rem;margin:0">Il Veneto sta ampliando l'offerta di <strong>posti letto universitari</strong> a Padova, Vicenza e Venezia attraverso <strong>ESU</strong>, operatori privati (es. Camplus), fondi <strong>PNRR</strong> e strutture miste pubblico-privato. Migliaia di nuovi letti entrano nel ciclo 2025–2027, senza eliminare del tutto la tensione sul mercato libero.</p>
</div>
<div class="stats-grid">
  <div class="stat-card"><div class="stat-num">3</div><div class="stat-label">Città chiave</div></div>
  <div class="stat-card"><div class="stat-num">PNRR</div><div class="stat-label">Student housing</div></div>
  <div class="stat-card"><div class="stat-num">ESU</div><div class="stat-label">Canone calmierato</div></div>
  <div class="stat-card"><div class="stat-num">Mix</div><div class="stat-label">Pubblico + privato</div></div>
</div>
<h2>Perché servono nuovi posti letto in Veneto</h2>
<p>Padova, Venezia e Vicenza condividono crescita di iscritti universitari e limiti dello stock abitativo storico. Senza nuove camere in studentato, il mercato libero assorbe la domanda con canoni in salita — tema trattato in <a href="blog-affitti-padova-canoni-2026">affitti Padova canoni 2026</a> e nelle rilevazioni <strong>Immobiliare.it Insights</strong>. La <strong>Regione Veneto</strong> coordina investimenti e convenzioni con atenei ed enti territoriali; l'<strong>ESU Padova</strong> resta riferimento per posti pubblici e graduatorie (<a href="https://www.esu.pd.it" target="_blank" rel="noopener noreferrer">esu.pd.it</a>).</p>
<h2>Pubblico, privato e PNRR: tre motori dell'offerta</h2>
<table>
<thead><tr><th>Canale</th><th>Caratteristiche</th><th>Esempio operativo</th></tr></thead>
<tbody>
<tr><td><strong>Pubblico ESU</strong></td><td>Canone calmierato, graduatoria merito/reddito</td><td>Studentati storici e nuovi padiglioni Padova</td></tr>
<tr><td><strong>Privato (Camplus e simili)</strong></td><td>Residenze a gestione imprenditoriale, servizi integrati</td><td>Strutture vicino poli universitari e stazioni</td></tr>
<tr><td><strong>PNRR / rigenerazione</strong></td><td>Finanziamenti per housing studentesco e riuso edifici</td><td>Progetti urbani autorizzati a Padova, Vicenza, Venezia Mestre</td></tr>
</tbody>
</table>
{blog_fig(*ASSETS["studentati"]["figs"][0])}
{chart_donut_canali()}
<h2>Padova: ampliamento stock e strutture miste</h2>
<p>A Padova convivono padiglioni ESU, residenze private e progetti di conversione ex uffici (es. torri Tribloc/Gozzi, trattati in articolo dedicato sul blog). Le <strong>strutture miste</strong> uniscono capitali privati e vincoli di accessibilità per studenti: canoni intermedi tra studentato puro e libero mercato. L'<strong>Università di Padova</strong> partecipa a protocolli per prossimità ai dipartimenti e trasporti.</p>
<p>Per studenti fuori graduatoria ESU, l'effetto netto di nuovi letti è positivo ma graduale: ogni migliaio di posti libera pressione su quartiere, non azzera i picchi di settembre. FIMAA Veneto osserva che annunci in appartamento restano molto attivi fino a ottobre.</p>
{blog_fig(*ASSETS["studentati"]["figs"][1])}
<h2>Vicenza e Venezia: stesso fenomeno, contesti diversi</h2>
<p>A Vicenza l'offerta cresce con rigenerazione urbana e posti PNRR calmierati (vedi articolo Casa Querini/Saudino). A Venezia la complessità logistica spinge verso Mestre e terraferma: nuovi letti PNRR e convenzioni ESU mirano a trattenere studenti fuori dal mercato turistico-short term del centro laguna. ISTAT descrive il Veneto come regione con alta mobilità studentesca intra-regionale.</p>
{blog_fig(*ASSETS["studentati"]["figs"][2])}
<div class="kpi-strip">
  <div><strong>ESU</strong><span>pubblico calmierato</span></div>
  <div><strong>Camplus</strong><span>privato servizi</span></div>
  <div><strong>PNRR</strong><span>nuove camere</span></div>
  <div><strong>Mix</strong><span>PPP urbani</span></div>
</div>
<h2>Come orientarsi tra graduatoria, residenza privata e mercato libero</h2>
<ol>
<li>Iscriversi e monitorare bandi <strong>ESU Padova</strong> (e ESU territoriali per Vicenza/Venezia).</li>
<li>Valutare residenze private con canone trasparente e regolamento scritto.</li>
<li>Confrontare costo totale (canone + utenze + trasporti) con stanza in appartamento.</li>
<li>Non firmare caparra sul libero finché non si conosce esito graduatoria se tempi compatibili.</li>
<li>Conservare copia registrata contratto e ricevute caparra per tutela FIMAA/consulenza legale.</li>
</ol>
<p>Righetto affianca famiglie e proprietari nel <a href="servizio-locazioni">servizio locazioni</a>; mediazione da concordare in sede, senza listini percentuali online. Supporto documentale su richiesta informativa preliminare, senza impegno.</p>
<h2>Impatto sul mercato libero padovano</h2>
<p>Immobiliare.it Insights segnala canoni stanza intorno a 490 euro: nuovi posti letto possono frenare ulteriori rialzi in periferia, non abbassare il centro storico. Proprietari di appartamenti condivisi devono restare competitivi su efficientamento energetico e manutenzione.</p>
<h2>Trasparenza bandi e tempistiche 2026</h2>
<p>Bandi ESU e PNRR hanno calendari pubblici: verificare sempre comunicati aggiornati, non screenshot obsoleti. Regione Veneto pubblica avanzamento opere su portali istituzionali.</p>
<h2>Coabitazione e servizi nelle residenze nuove</h2>
<p>Residenze private offrono spesso reception, studio e lavanderia; studentato ESU privilegia canone basso. Scelta dipende da budget familiare e autonomia studente. Strutture miste cercano equilibrio tra i due modelli.</p>
<h2>Università di Padova e fabbisogno annuo</h2>
<p>L'<strong>Università di Padova</strong> pubblica dati iscrizione e tassi fuori sede: la maggioranza non accede studentato ESU. Nuovi letti PNRR e privati riducono gap ma non lo chiudono — mercato libero resta essenziale per famiglie senza requisiti ISEE o fuori graduatoria. Incrociare domanda con <a href="blog-stanza-universitaria-padova-canoni-2026">canoni stanza Insights</a> aiuta budgeting.</p>
<h2>Camplus e standard di servizio</h2>
<p><strong>Camplus</strong> e operatori simili offrono contratti con servizi inclusi e durata flessibile per Erasmus. Canone superiore a ESU ma inferiore a combo singola premium più utenze imprevedibili. FIMAA segnala crescita segmento «student housing istituzionalizzato» in Veneto.</p>
<h2>Regione Veneto: coordinamento territoriale</h2>
<p>La <strong>Regione Veneto</strong> allinea bandi PNRR con piano casa giovani e mobilità. Progetti isolati senza collegamento TPL perdono efficacia: posti letto lontani da facoltà spostano costo su trasporti. ISTAT documenta spesa mobility studenti in crescita regionale.</p>
<p>Per orientamento operativo su contratti mercato libero parallelo agli studentati, il <a href="servizio-locazioni">servizio locazioni</a> Righetto resta punto di contatto — compenso mediazione concordato in sede, senza percentuali pubblicate online. Chi gestisce appartamento condiviso in Padova può richiedere valutazione canone allineata a FIMAA e Insights prima della stagione autunno.</p>
<p style="font-size:.8rem;color:var(--grigio)"><em>Aggiornamento {DATE_IT}. Fonti: ESU Padova, Regione Veneto, PNRR, FIMAA, Università di Padova.</em></p>
{EXPANSION_STUD}
<a class="cta-deep" href="blog-affitti-padova-canoni-2026">Canoni Padova 2026</a>
"""


def build_body_green_tribloc() -> str:
    return f"""
<div class="aeo-box">
<h2>In sintesi</h2>
<p style="font-size:.84rem;margin:0">Progetto urbano autorizzato a Padova: conversione di <strong>ex torri uffici Tribloc</strong> (area Gozzi) in circa <strong>180 camere</strong> per studenti e giovani lavoratori, standard <strong>green/NZEB</strong>, ingresso previsto anno accademico <strong>2026/27</strong>. Operatore: <strong>Swadeshi / Brainville</strong> (dati pubblici progetto).</p>
</div>
<div class="stats-grid">
  <div class="stat-card"><div class="stat-num">180</div><div class="stat-label">Camere previste</div></div>
  <div class="stat-card"><div class="stat-num">NZEB</div><div class="stat-label">Efficienza</div></div>
  <div class="stat-card"><div class="stat-num">2026/27</div><div class="stat-label">Apertura</div></div>
  <div class="stat-card"><div class="stat-num">Riuso</div><div class="stat-label">Ex uffici</div></div>
</div>
<h2>Da torri uffici a housing studentesco: il caso Tribloc</h2>
<p>Il riuso di edifici direzionali per <strong>housing studentesco</strong> risponde a due obiettivi: ridurre vuoti urbani e aumentare posti letto senza consumo di suolo agricolo. A Padova, l'area <strong>Gozzi / Tribloc</strong> — torri simbolo dello sviluppo office degli anni passati — è oggetto di un progetto autorizzato che prevede circa <strong>180 stanze</strong>, spazi comuni e criteri <strong>quasi zero energy (NZEB)</strong>. Il nome dell'operatore (<strong>Swadeshi</strong>, gruppo <strong>Brainville</strong>) compare negli atti pubblici di progetto: non è marketing Righetto, ma fatto urbanistico verificabile.</p>
<h2>Green building e NZEB: cosa cambia per l'inquilino</h2>
<p>Edifici NZEB limitano dispersione termica e costi bolletta — variabile rilevante per studenti fuori sede. Pannelli, ventilazione controllata e monitoraggio consumi sono standard del riqualificazione profonda rispetto a simple retrofit cosmetico. FIMAA e normativa energetica nazionale spingono in questa direzione anche per locazioni non turistiche.</p>
{blog_fig(*ASSETS["green"]["figs"][0])}
{chart_energy_compare()}
<figure class="chart-wrap">
<table>
<caption style="caption-side:bottom;font-size:.72rem;color:var(--grigio);padding-top:.5rem">Timeline indicativa progetto Tribloc — verificare atti comunali</caption>
<thead><tr><th>Fase</th><th>Periodo</th><th>Stato</th></tr></thead>
<tbody>
<tr><td>Autorizzazione urbanistica</td><td>2024–2025</td><td>Approvata (fonti progetto)</td></tr>
<tr><td>Cantiere riqualificazione</td><td>2025–2026</td><td>In corso / avvio</td></tr>
<tr><td>Ingresso primi inquilini</td><td>A.A. 2026/27</td><td>Target operatore</td></tr>
<tr><td>Piena operatività</td><td>2027</td><td>Da confermare</td></tr>
</tbody>
</table>
</figure>
{blog_fig(*ASSETS["green"]["figs"][1])}
<h2>Posizione urbana e collegamenti</h2>
<p>L'area Gozzi dialoga con reti bus e tram padovane; studenti devono calcolare tempi fino ai dipartimenti (Scienze, Ingegneria, Economia). Confronto con <a href="zona-universitaria-padova">zona universitaria</a> e <a href="blog-affitto-studenti-padova">affitto studenti</a> aiuta a decidere se attendere apertura residenza o cercare subito sul libero.</p>
<h2>Impatto sul mercato locativo padovano</h2>
<p>180 camere non risolvono da sole il gap tra iscritti e posti letto, ma segnalano trend: riuso office + green + gestione professionale. Proprietari di appartamenti condivisi competono con servizi e bollette basse delle residenze nuove. Immobiliare.it Insights documenta canoni stanza in crescita: offerta strutturata può assorbire fascia media-alta.</p>
{blog_fig(*ASSETS["green"]["figs"][2])}
<h2>Visite e due diligence</h2>
<p>Fino all'apertura, verificare avanzamento cantiere su fonti comunali e comunicati Regione Veneto. Per immobili già disponibili sul mercato, <a href="visite-virtuali">visite virtuali</a> Righetto restano strumento utile a famiglie fuori provincia.</p>
<div class="kpi-strip">
  <div><strong>180</strong><span>camere</span></div>
  <div><strong>NZEB</strong><span>classe energetica</span></div>
  <div><strong>Gozzi</strong><span>area urbana</span></div>
  <div><strong>2026/27</strong><span>target apertura</span></div>
</div>
<h2>ESU, privati e riuso: ecosistema Padova</h2>
<p>Il progetto Tribloc si affianca a ESU e operatori privati (articolo studentati Veneto). Studenti possono combinare graduatoria ESU, prenotazione residenza green e piano B sul mercato libero.</p>
<h2>Perimeter Gozzi e servizi di prossimità</h2>
<p>L'area Gozzi dispone di supermercati, farmacie e fermate TPL entro raggio pedonale — fattore che incide sul costo-tempo di vita studentesca quanto il canone camera. Confrontare spostamenti verso dipartimento con soluzione Portello usando mappe TPL ufficiali. Regione Veneto e Comune Padova hanno indicato il riuso Tribloc nel quadro rigenerazione periferie servite da infrastrutture esistenti, coerente con obiettivi PNRR housing sostenibile.</p>
<p>Per famiglie che valutano se attendere apertura 2026/27: candidatura ESU in parallelo e ricerca sul libero entro luglio, senza bloccare decisioni in attesa di date non confermate dal cantiere Swadeshi/Brainville. Incrociare sempre fonti Comune Padova e Regione Veneto, non solo comunicati operatori.</p>
<p style="font-size:.8rem;color:var(--grigio)"><em>{DATE_IT}. Progetto descritto da atti urbanistici pubblici; operatori Swadeshi/Brainville. Non offerta commerciale Righetto.</em></p>
{EXPANSION_GREEN}
{EXPANSION_GREEN_B}
{EXPANSION_GREEN_C}
<a class="cta-deep" href="visite-virtuali">Visite virtuali</a>
"""


def build_body_vicenza_calmierati() -> str:
    return f"""
<div class="aeo-box">
<h2>In sintesi</h2>
<p style="font-size:.84rem;margin:0">A <strong>Vicenza</strong> crescono posti letto universitari con fondi <strong>PNRR</strong>, canoni <strong>calmierati</strong> e convenzione <strong>ESU</strong> (quota accesso circa 30% posti). Esempio urbano: rigenerazione <strong>Casa Querini</strong> via progetto <strong>Saudino</strong> — fatto pubblico di rigenerazione, non titolo giornalistico.</p>
</div>
<div class="stats-grid">
  <div class="stat-card"><div class="stat-num">30%</div><div class="stat-label">Quota ESU conv.</div></div>
  <div class="stat-card"><div class="stat-num">PNRR</div><div class="stat-label">Finanziamento</div></div>
  <div class="stat-card"><div class="stat-num">VI</div><div class="stat-label">Vicenza</div></div>
  <div class="stat-card"><div class="stat-num">Mix</div><div class="stat-label">Rigenerazione</div></div>
</div>
<h2>Vicenza: domanda universitaria e carenza camere</h2>
<p>Vicenza ospita sedi universitarie collegate al sistema veneto; studenti fuori sede competono per poche camere rispetto a Padova o Verona. <strong>ISTAT</strong> e dati Regione Veneto descrivono un territorio con occupazione elevata e affitti in tensione. Nuovi posti letto PNRR mirano a canoni più accessibili del libero mercato.</p>
<h2>Canoni calmierati e convenzione ESU</h2>
<p>I bandi PNRR per student housing prevedono spesso <strong>canoni calmierati</strong> e riserva di posti per studenti ammessi tramite <strong>ESU</strong> (circa 30% nelle convenzioni tipiche — verificare bando specifico Casa Querini). Resto dei posti può andare a lavoratori giovani o studenti a mercato con tariffe inferiori al centro storico.</p>
{blog_fig(*ASSETS["vicenza"]["figs"][0])}
<h2>Casa Querini e rigenerazione Saudino</h2>
<p>Il complesso <strong>Casa Querini</strong>, oggetto di rigenerazione urbana con progettazione <strong>Saudino</strong>, illustra come edifici storici o underused possano diventare residenze studenti con standard moderni. Facciate, vincoli paesaggistici e accessibilità richiedono tempi cantieristici più lunghi del container temporaneo. Comune di Vicenza e Regione Veneto pubblicano avanzamento lavori.</p>
<table>
<thead><tr><th>Strumento</th><th>Funzione</th><th>Beneficiario</th></tr></thead>
<tbody>
<tr><td>PNRR studentati</td><td>Finanziamento nuove camere</td><td>Studenti meritevoli / giovani</td></tr>
<tr><td>Convenzione ESU</td><td>Canone calmierato, graduatoria</td><td>Quota ~30% posti (da bando)</td></tr>
<tr><td>Mercato residuo</td><td>Canone intermedio</td><td>Studenti/lavoratori fuori graduatoria</td></tr>
<tr><td>Libero mercato centro</td><td>Canone pieno</td><td>Chi non accede a residenze</td></tr>
</tbody>
</table>
{blog_fig(*ASSETS["vicenza"]["figs"][1])}
{chart_donut_canali()}
<h2>Confronto con Padova e Veneto</h2>
<p>Leggere anche <a href="blog-studentati-veneto-2026-posti-letto">studentati Veneto 2026</a> e <a href="blog-affitti-padova-canoni-2026">canoni Padova</a> per quadro regionale. FIMAA segnala crescente professionalizzazione gestioni residenza.</p>
<h2>Proprietari vicentini</h2>
<p>Più posti calmierati spostano marginalmente domanda dal libero; immobili mal mantenuti perdono appeal. <a href="servizio-locazioni">Servizio locazioni</a> Righetto copre anche Vicenza nel territorio 101 comuni.</p>
{blog_fig(*ASSETS["vicenza"]["figs"][2])}
<h2>Graduatoria ESU e tempistiche domanda</h2>
<p>La convenzione ESU su quota indicativa 30% posti Casa Querini richiede domanda entro finestra bando con ISEE e certificati merito aggiornati. ESU Padova e territorialità Vicenza pubblicano calendari distinti: non perdere scadenze per attendere esito PNRR senza piano B sul libero. ISTAT segnala che ritardi domanda riducono probabilità posto calmierato a settembre.</p>
<p>Documentazione incompleta esclude dalla graduatoria: verificare checklist ESU prima dell'invio. Parallelamente, monitorare annunci libero mercato Vicenza con canoni allineati a comparabili FIMAA e OMI microzona.</p>
<h2>Rigenerazione urbana e vincoli paesaggistici</h2>
<p>Casa Querini in centro storico vicentino subisce vincoli paesaggistici che allungano tempi rispetto a new build in periferia. Progetto Saudino negli atti pubblici definisce intervento strutturale: facciate, impianti, accessibilità. Regione Veneto rendiconta milestone PNRR; Comune Vicenza è fonte primaria per date consegna camere.</p>
<p>Studenti interessati devono distinguere tra marketing operatori e atti amministrativi: solo questi ultimi confermano numero posti, canoni massimi e calendario ingressi effettivo.</p>
<h2>Confronto costi con Padova Insights</h2>
<p>Immobiliare.it Insights colloca media stanza Padova intorno 490 euro: studente pendolare Vicenza-Padova deve sommare canone calmierato (se ammesso) più abbonamento treno/bus. Housing Vicenza conviene se sedi locali coprono corso; altrimenti valutare Padova ESU o mercato libero periferia tram.</p>
<p>Per orientamento operativo su contratti mercato libero parallelo ai posti PNRR, il servizio locazioni Righetto copre Vicenza e Padova — mediazione concordata in sede, senza listini percentuali pubblicati online. Contattaci via form in fondo articolo, senza impegno informativo. Fonti istituzionali verificate in articolo. Tel. 049.8843484 disponibile.</p>
<div class="kpi-strip">
  <div><strong>PNRR</strong><span>nuovi letti</span></div>
  <div><strong>ESU</strong><span>30% indicativo</span></div>
  <div><strong>Querini</strong><span>rigenerazione</span></div>
  <div><strong>2026</strong><span>ingressi</span></div>
</div>
<p style="font-size:.8rem;color:var(--grigio)"><em>{DATE_IT}. Fonti: Regione Veneto, ESU, atti Comune Vicenza, ISTAT.</em></p>
{EXPANSION_VICENZA}
{EXPANSION_VICENZA_B}
{EXPANSION_VICENZA_C}
{EXPANSION_VICENZA_D}
<a class="cta-deep" href="servizio-locazioni">Locazioni Vicenza</a>
"""


def build_body_edilcassa_lavoratori() -> str:
    return f"""
<div class="aeo-box">
<h2>In sintesi</h2>
<p style="font-size:.84rem;margin:0"><strong>Edilcassa Veneto</strong> (Confartigianato) attiva un <strong>fondo garanzia da 250.000 euro</strong> nel contratto regionale edilizia 2025/2026 per sostenere imprese e lavoratori del settore. Parallelamente, imprese venete dell'edilizia sperimentano <strong>corporate housing</strong> e co-housing per forza lavoro distante da casa.</p>
</div>
<div class="stats-grid">
  <div class="stat-card"><div class="stat-num">250k €</div><div class="stat-label">Fondo garanzia</div></div>
  <div class="stat-card"><div class="stat-num">2025/26</div><div class="stat-label">Contratto regionale</div></div>
  <div class="stat-card"><div class="stat-num">Edilcassa</div><div class="stat-label">Confartigianato VI</div></div>
  <div class="stat-card"><div class="stat-num">Housing</div><div class="stat-label">Co-living lavoratori</div></div>
</div>
<h2>Edilcassa Veneto e fondo garanzia 250.000 euro</h2>
<p><strong>Edilcassa</strong>, cassa edile del sistema Confartigianato, gestisce contributi, formazione e tutele per imprese edili. Nel Veneto, il contratto regionale di edilizia <strong>2025/2026</strong> prevede un <strong>fondo di garanzia da 250.000 euro</strong> a supporto di imprese e lavoratori in difficoltà contributiva o occupazionale — dato comunicato da <strong>Edilcassa / Confartigianato Veneto</strong>. Non è un prestito immobiliare, ma strumento di stabilizzazione del comparto che indirettamente influenza domanda di alloggi per cantieri temporanei.</p>
{blog_fig(*ASSETS["lavoratori"]["figs"][0])}
<h2>Fondo Edilcassa vs garanzie locative classiche</h2>
<table>
<thead><tr><th>Strumento</th><th>Finalità</th><th>Soggetti</th><th>Importo indicativo</th></tr></thead>
<tbody>
<tr><td><strong>Fondo garanzia Edilcassa Veneto</strong></td><td>Contributi, morosità, sostegno imprese/lavoratori edili</td><td>Iscritti cassa edile</td><td>250.000 € pool (2025/26)</td></tr>
<tr><td><strong>Deposito cauzionale locazione</strong></td><td>Tutela proprietario da danni/morosità</td><td>Inquilino locazione</td><td>1–3 mensilità</td></tr>
<tr><td><strong>Garanzia bancaria/assicurativa affitto</strong></td><td>Sostituisce deposito al proprietario</td><td>Inquilino + istituto</td><td>Costo premio annuo</td></tr>
<tr><td><strong>Fideiussione corporate housing</strong></td><td>Imprese garantiscono alloggio dipendenti</td><td>Società appaltatrice</td><td>Contratto quadro</td></tr>
</tbody>
</table>
{chart_edilcassa_bar()}
{blog_fig(*ASSETS["lavoratori"]["figs"][1])}
<h2>Corporate housing e co-housing per lavoratori edili</h2>
<p>Cantieri temporanei nel Veneto richiedono alloggi per squadre fuori sede. Il modello <strong>corporate housing</strong> — appartamenti o co-living affittati da imprese venete del settore edile per dipendenti e subappaltatori — riduce turnover e costi di ricerca alloggio. Non sostituisce contratti regolari: servono cap, regolamento convivenza e conformità urbanistica. Edilcassa e Confartigianato Veneto non gestiscono direttamente queste locazioni.</p>
<h2>Legame con mercato immobiliare padovano</h2>
<p>Righetto segue locazioni anche per lavoratori e famiglie nel <strong>Padovano</strong> (101 comuni). Imprese che cercano unità multi-camera per staff possono usare <a href="servizio-locazioni">servizio locazioni</a>; compenso mediazione concordato in mandato. ISTAT descrive mobilità lavorativa veneta tra province.</p>
{blog_fig(*ASSETS["lavoratori"]["figs"][2])}
<h2>Regione Veneto e contratto edilizia</h2>
<p>Il contratto collettivo regionale 2025/2026 definisce anche welfare edilcassa: fondo garanzia va letto nel testo integrale Confartigianato Veneto, non in estratti social. Imprenditori verificano con consulente del lavoro e cassa edile aderenza e modalità accesso.</p>
<div class="kpi-strip">
  <div><strong>250k €</strong><span>fondo 2025/26</span></div>
  <div><strong>Edilcassa</strong><span>cassa edile</span></div>
  <div><strong>VI</strong><span>Veneto</span></div>
  <div><strong>Housing</strong><span>co-living</span></div>
</div>
<h2>Checklist impresa che alloggia squadre</h2>
<ol>
<li>Contratto locazione intestato a società o lavoratore con rimborso chiaro.</li>
<li>APE e sicurezza impianti verificati — responsabilità civile.</li>
<li>Regolamento convivenza e turnover fine cantiere.</li>
<li>Confronto costo alloggio vs indennità di trasferta.</li>
</ol>
<h2>Imprese venete del settore edile: modello operativo</h2>
<p>Il co-housing per squadre descrive genericamente appartamenti multi-camera affittati da imprese venete dell'edilizia per cantieri temporanei nel Padovano e in Veneto. Regolamento interno, fideiussione societaria e rispetto capienza abitativa sono requisiti minimi. Non sostituisce indennità di trasferta ove previste da CCNL: commercialista e consulente del lavoro definiscono mix ottimale.</p>
<h2>FIMAA e locazioni a imprese</h2>
<p>FIMAA segnala crescita locazioni B2B a PMI edili e subappaltatori: proprietario beneficia garanzie più solide rispetto a singolo inquilino. Righetto servizio locazioni supporta mandato e documentazione; compenso mediazione concordato in sede.</p>
<p>Per cantieri in provincia Padova (Limena, Rubano, cintura) la domanda di alloggi multi-camera resta attiva nel 2026: contattare l'agenzia via form lead in fondo pagina indicando metrature, durata contratto quadro impresa e telefono referente HR. Tel. 049.8843484 disponibile in orari agenzia, senza impegno. Contattaci oggi per informazioni utili.</p>
<p style="font-size:.8rem;color:var(--grigio)"><em>{DATE_IT}. Fonti: Edilcassa Veneto, Confartigianato Veneto, ISTAT, Regione Veneto.</em></p>
{EXPANSION_EDIL}
{EXPANSION_EDIL_B}
{EXPANSION_EDIL_C}
{EXPANSION_EDIL_D}
<a class="cta-deep" href="servizio-locazioni">Servizio locazioni</a>
<a class="cta-deep" href="landing-valutazione" style="background:var(--blu);color:#fff">Valutazione immobile</a>
"""


def build_html(cfg: dict, body: str, wc: int) -> str:
    slug = cfg["slug"]
    author_key = cfg.get("author", "gino")
    auth = AUTHORS[author_key]
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
        "author": {"@type": "Person", "name": auth["name"]},
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
<meta property="og:image" content="https://righettoimmobiliare.it/{cfg['img']}">
<meta property="article:published_time" content="{TIME_TS}">
<meta property="article:author" content="{auth['name']}">
<meta property="article:section" content="{cfg["section"]}">
<meta name="description" content="{cfg["meta_desc"]}">
<script type="application/ld+json">{json.dumps(blog_obj, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_obj, ensure_ascii=False)}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://righettoimmobiliare.it/"}},{{"@type":"ListItem","position":2,"name":"Blog","item":"https://righettoimmobiliare.it/blog"}},{{"@type":"ListItem","position":3,"name":"{cfg["bread"]}"}}]}}</script>
<link rel="stylesheet" href="css/fonts.css?v=3"><link rel="stylesheet" href="css/nav-mobile.css?v=4">
<link rel="stylesheet" href="css/scroll-reveal.css?v=3" media="print" onload="this.media='all'">
{STYLE_BLOCK}
</head>
<body>
<a href="#main-content" class="skip-link">Contenuto principale</a>
<header><div class="hi">
  <a href="/" class="logo">Righetto <span>Immobiliare</span></a>
  <nav><a href="/">Home</a><a href="immobili">Immobili</a><a href="{auth['nav_link']}">Profilo autore</a><a href="blog" class="active">Blog</a><a href="contatti">Contatti</a></nav>
  <a class="h-btn" href="landing-valutazione">Valutazione gratuita</a>
</div><button class="nav-burger" id="burgerBtn" aria-label="Menu"><span></span><span></span><span></span></button></header>
<div class="nav-mobile" id="navMobile"><a href="/">Home</a><a href="immobili">Immobili</a><a href="{auth['nav_link']}">Profilo autore</a><a href="blog">Blog</a><a href="contatti">Contatti</a></div>
<main id="main-content">
<div class="art-hero">
  <img class="art-hero-img" src="{cfg['hero_img']}" alt="{cfg['hero_alt']}" width="1280" height="420" fetchpriority="high">
  <div class="art-hero-overlay"><div class="art-hero-inner">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="blog">Blog</a> / {cfg["breadcrumb_tail"]}</div>
    <span class="cat-badge">{cfg["cat_badge"]}</span>
    <h1>{cfg["h1"]}</h1>
    <div class="art-hero-meta"><div class="av">{auth['initial']}</div><span>{auth['name']}</span><span>{DATE_IT}</span><span>Aggiornato: {DATE_IT}</span></div>
  </div></div>
</div>
<div class="art-container"><div class="art-content">
{body}
{faq_html(cfg["faqs"])}
<div class="author-bio"><img src="{auth['img']}" alt="{auth['name']} Righetto Immobiliare" width="64" height="64" loading="lazy"><div><strong>{auth['name']}</strong><p style="font-size:.8rem;color:#555">{auth['bio']}</p><p style="font-size:.78rem;margin-top:.4rem"><a href="{auth['profile']}">Profilo autore</a></p></div></div>
<div class="related"><h3 style="font-family:'Cormorant Garamond',serif">Articoli correlati</h3><ul style="margin-left:1.1rem;margin-top:.4rem">{rel}</ul></div>
</div></div>
{lead_form(slug, cfg["lead_ids"])}
{FOOTER}"""


def registry_entries(cfg: dict) -> dict:
    reg = cfg["registry"]
    author_name = AUTHORS[cfg.get("author", "gino")]["name"]
    base = {
        "titolo": reg["titolo"],
        "categoria": reg["categoria"],
        "data": DATE_ISO,
        "stato": "pubblicato",
        "immagine_copertina": cfg["img"],
        "url_statico": cfg["slug"],
    }
    blog_html = {**base, "tempo": reg["tempo"], "autore": author_name, "contenuto": reg["contenuto"], "evidenza": reg["evidenza"]}
    admin = {**blog_html, "emoji": reg["emoji"], "contenuto": f"<p>{reg['contenuto']}</p>", "data_pubblicazione": DATE_ISO}
    return {"blog_html": blog_html, "admin": admin, "homepage": {k: v for k, v in base.items()}}


ARTICLES = [
    {
        "filename": "blog-stanza-universitaria-padova-canoni-2026.html",
        "slug": "blog-stanza-universitaria-padova-canoni-2026",
        "img": "img/foto-servizi/contratti-di-locazione-padova.webp",
        "hero_img": "img/foto-servizi/contratti-di-locazione-padova.webp",
        "author": "linda",
        "html_title": "Stanza universitaria Padova 2026: canoni 490€ e +46% vs 2020 | Righetto",
        "og_title": "Canoni stanza universitaria Padova 2026: dati Immobiliare.it Insights",
        "meta_desc": "Canone medio stanza Padova circa 490€ (+46% vs 2020) secondo Immobiliare.it Insights marzo 2026. FIMAA, ESU, tram e periferia. Guida Righetto.",
        "schema_headline": "Stanza universitaria Padova 2026: canoni, +46% vs 2020 e zone alternative",
        "section": "Locazioni",
        "cat_badge": "Affitti studenti",
        "bread": "Stanza universitaria Padova 2026",
        "breadcrumb_tail": "Stanza universitaria Padova",
        "h1": "<strong>Stanza universitaria a Padova</strong> — canoni 2026, +46% vs 2020 e zone tram",
        "hero_alt": "Contratti locazione Padova — canoni stanze universitarie 2026",
        "body_fn": build_body_stanza_padova,
        "faqs": [
            ("Quanto costa una stanza universitaria a Padova nel 2026?", "Immobiliare.it Insights (marzo 2026) indica un canone medio intorno a 490 euro, +46% rispetto al 2020 (335 euro)."),
            ("Dove cercare stanze più economiche?", "Periferie servite dal tram (Arcella, Guizza, Ponte di Brenta) spesso hanno canoni inferiori al Portello."),
            ("ESU Padova riduce il bisogno del mercato libero?", "Sì per chi entra in graduatoria; molti studenti restano fuori e usano il libero mercato."),
            ("Quali fonti usare per confrontare prezzi?", "Immobiliare.it Insights, OMI Agenzia Entrate, annunci comparabili e guide FIMAA."),
            ("Righetto segue locazioni studentesche?", "Sì — servizio locazioni e consulenza zone; mediazione concordata in mandato."),
        ],
        "related": [
            ("Affitto studenti Padova", "blog-affitto-studenti-padova"),
            ("Servizio locazioni", "servizio-locazioni"),
            ("Zona universitaria", "zona-universitaria-padova"),
        ],
        "lead_ids": ("bl-nome-stanza", "bl-tel-stanza", "bl-email-stanza", "bl-msg-stanza", "bl-gdpr-stanza"),
        "registry": {
            "titolo": "Stanza universitaria Padova 2026: canoni 490€ e +46%",
            "categoria": "Locazioni",
            "tempo": 11,
            "contenuto": "Canone medio stanza 490€ (+46% vs 2020) da Immobiliare.it Insights; FIMAA, ESU, tram e periferia.",
            "evidenza": True,
            "emoji": "🎓",
        },
    },
    {
        "filename": "blog-studentati-veneto-2026-posti-letto.html",
        "slug": "blog-studentati-veneto-2026-posti-letto",
        "img": "img/foto-servizi/gestioni-immobili-padova.webp",
        "hero_img": "img/foto-servizi/gestioni-immobili-padova.webp",
        "author": "linda",
        "html_title": "Studentati Veneto 2026: nuovi posti letto Padova Vicenza Venezia | Righetto",
        "og_title": "Posti letto universitari Veneto 2026: ESU, Camplus e PNRR",
        "meta_desc": "Nuovi posti letto a Padova, Vicenza e Venezia: ESU pubblico, residenze private Camplus, PNRR e strutture miste. Analisi Righetto luglio 2026.",
        "schema_headline": "Studentati Veneto 2026: posti letto ESU, privati e PNRR a Padova e provincia",
        "section": "Locazioni",
        "cat_badge": "Housing studenti",
        "bread": "Studentati Veneto 2026",
        "breadcrumb_tail": "Studentati Veneto",
        "h1": "<strong>Studentati in Veneto 2026</strong> — nuovi posti letto tra ESU, privati e PNRR",
        "hero_alt": "Gestioni immobili Padova — studentati e posti letto Veneto 2026",
        "body_fn": build_body_studentati_veneto,
        "faqs": [
            ("Quante città venete ampliano i posti letto?", "Padova, Vicenza e Venezia sono i poli principali con ESU, privati e PNRR."),
            ("Cosa distingue ESU da residenza privata?", "ESU: canone calmierato e graduatoria; privati: servizi e flessibilità a canone di mercato."),
            ("Camplus che ruolo ha?", "Operatore privato di residenze studenti con gestione imprenditoriale."),
            ("PNRR cosa finanzia?", "Nuove camere e rigenerazione edifici per housing studentesco."),
            ("Dove leggere i bandi ESU Padova?", "Sul sito ufficiale esu.pd.it e comunicati Regione Veneto."),
        ],
        "related": [
            ("Affitti Padova canoni 2026", "blog-affitti-padova-canoni-2026"),
            ("Stanza universitaria Padova", "blog-stanza-universitaria-padova-canoni-2026"),
            ("Servizio locazioni", "servizio-locazioni"),
        ],
        "lead_ids": ("bl-nome-stud", "bl-tel-stud", "bl-email-stud", "bl-msg-stud", "bl-gdpr-stud"),
        "registry": {
            "titolo": "Studentati Veneto 2026: posti letto ESU, privati e PNRR",
            "categoria": "Locazioni",
            "tempo": 10,
            "contenuto": "Nuovi posti letto Padova Vicenza Venezia: ESU, Camplus, PNRR e strutture miste.",
            "evidenza": False,
            "emoji": "🏫",
        },
    },
    {
        "filename": "blog-residenze-green-padova-tribloc-2026.html",
        "slug": "blog-residenze-green-padova-tribloc-2026",
        "img": "img/foto-servizi/valutazioni-e-perizie-padova.webp",
        "hero_img": "img/foto-servizi/valutazioni-e-perizie-padova.webp",
        "author": "linda",
        "html_title": "Residenze green Padova Tribloc 2026: 180 camere NZEB | Righetto",
        "og_title": "Ex torri Tribloc Gozzi: 180 camere studenti green per 2026/27",
        "meta_desc": "Progetto Padova: conversione ex uffici Tribloc in 180 camere NZEB, operatore Swadeshi/Brainville, apertura 2026/27. Guida Righetto.",
        "schema_headline": "Residenze green Padova Tribloc 2026: riuso torri Gozzi e 180 camere NZEB",
        "section": "Mercato immobiliare",
        "cat_badge": "Housing green",
        "bread": "Residenze green Tribloc",
        "breadcrumb_tail": "Residenze green Padova",
        "h1": "<strong>Residenze green a Padova</strong> — ex Tribloc Gozzi, 180 camere NZEB dal 2026/27",
        "hero_alt": "Valutazioni immobili Padova — residenze green Tribloc studenti",
        "body_fn": build_body_green_tribloc,
        "faqs": [
            ("Quante camere prevede il progetto Tribloc?", "Circa 180 camere per studenti e giovani lavoratori."),
            ("Quando apre?", "Target anno accademico 2026/27, da confermare su atti comunali."),
            ("Chi gestisce la residenza?", "Swadeshi / Brainville — nome pubblico di progetto."),
            ("Cosa significa NZEB?", "Quasi zero energia: edificio ad alta efficienza e bassi consumi."),
            ("Impatta sui canoni liberi?", "Aumenta offerta strutturata; centro resta premium."),
        ],
        "related": [
            ("Studentati Veneto", "blog-studentati-veneto-2026-posti-letto"),
            ("Visite virtuali", "visite-virtuali"),
            ("Affitto studenti Padova", "blog-affitto-studenti-padova"),
        ],
        "lead_ids": ("bl-nome-green", "bl-tel-green", "bl-email-green", "bl-msg-green", "bl-gdpr-green"),
        "registry": {
            "titolo": "Residenze green Padova Tribloc 2026: 180 camere NZEB",
            "categoria": "Mercato immobiliare",
            "tempo": 9,
            "contenuto": "Riuso torri Gozzi/Tribloc: 180 camere green, Swadeshi/Brainville, apertura 2026/27.",
            "evidenza": False,
            "emoji": "🌿",
        },
    },
    {
        "filename": "blog-vicenza-residenze-universitarie-calmierate-2026.html",
        "slug": "blog-vicenza-residenze-universitarie-calmierate-2026",
        "img": "img/foto-servizi/gestione-preliminari-padova.webp",
        "hero_img": "img/foto-servizi/gestione-preliminari-padova.webp",
        "author": "linda",
        "html_title": "Vicenza residenze universitarie calmierate 2026: PNRR e Casa Querini | Righetto",
        "og_title": "Posti letto calmierati Vicenza: PNRR, ESU 30%, rigenerazione Querini",
        "meta_desc": "Residenze universitarie calmierate a Vicenza 2026: PNRR, convenzione ESU, rigenerazione Casa Querini via progetto Saudino. Analisi Righetto.",
        "schema_headline": "Vicenza 2026: residenze universitarie calmierate PNRR e Casa Querini",
        "section": "Locazioni",
        "cat_badge": "Housing Veneto",
        "bread": "Vicenza residenze 2026",
        "breadcrumb_tail": "Vicenza calmierati",
        "h1": "<strong>Residenze universitarie a Vicenza</strong> — PNRR calmierati, ESU e Casa Querini",
        "hero_alt": "Gestione immobili — residenze universitarie calmierate Vicenza 2026",
        "body_fn": build_body_vicenza_calmierati,
        "faqs": [
            ("Cosa sono i canoni calmierati?", "Tariffe inferiori al libero mercato legate a bandi PNRR/ESU."),
            ("Quanto vale la quota ESU?", "Indicativamente circa 30% posti in convenzione — verificare bando."),
            ("Cos'è Casa Querini?", "Progetto rigenerazione urbana con posti letto studenti."),
            ("Saudino chi è?", "Progettista/operatore citato negli atti pubblici di rigenerazione."),
            ("Righetto opera a Vicenza?", "Sì, tra i 101 comuni serviti — locazioni e valutazioni."),
        ],
        "related": [
            ("Studentati Veneto", "blog-studentati-veneto-2026-posti-letto"),
            ("Servizio locazioni", "servizio-locazioni"),
            ("Stanza Padova canoni", "blog-stanza-universitaria-padova-canoni-2026"),
        ],
        "lead_ids": ("bl-nome-vic", "bl-tel-vic", "bl-email-vic", "bl-msg-vic", "bl-gdpr-vic"),
        "registry": {
            "titolo": "Vicenza residenze universitarie calmierate 2026: PNRR e Querini",
            "categoria": "Locazioni",
            "tempo": 9,
            "contenuto": "Posti letto calmierati Vicenza: PNRR, ESU 30%, rigenerazione Casa Querini/Saudino.",
            "evidenza": False,
            "emoji": "🏘️",
        },
    },
    {
        "filename": "blog-housing-lavoratori-veneto-edilcassa-2026.html",
        "slug": "blog-housing-lavoratori-veneto-edilcassa-2026",
        "img": "img/foto-servizi/vendita-immobili-padova.webp",
        "hero_img": "img/foto-servizi/vendita-immobili-padova.webp",
        "author": "gino",
        "html_title": "Housing lavoratori Veneto 2026: Edilcassa fondo 250.000€ | Righetto",
        "og_title": "Edilcassa Veneto: fondo garanzia 250.000€ e corporate housing edile",
        "meta_desc": "Edilcassa Veneto: fondo garanzia 250.000 euro contratto edilizia 2025/2026. Corporate housing imprese edili venete. Tabella garanzie vs deposito.",
        "schema_headline": "Housing lavoratori Veneto 2026: Edilcassa fondo garanzia e co-housing edile",
        "section": "Mercato immobiliare",
        "cat_badge": "Lavoro e casa",
        "bread": "Housing lavoratori Veneto",
        "breadcrumb_tail": "Edilcassa housing",
        "h1": "<strong>Housing lavoratori in Veneto</strong> — Edilcassa 250.000€ e co-housing per imprese edili",
        "hero_alt": "Immobili Padova — housing lavoratori edilcassa Veneto 2026",
        "body_fn": build_body_edilcassa_lavoratori,
        "faqs": [
            ("Cos'è il fondo 250.000 euro Edilcassa Veneto?", "Pool garanzia nel contratto regionale edilizia 2025/2026 per imprese/lavoratori iscritti."),
            ("Sostituisce il deposito cauzionale?", "No: tutela contributiva edile, non garanzia affitto classica."),
            ("Cos'è il corporate housing?", "Alloggi affittati da imprese per dipendenti/squadre fuori sede."),
            ("Fonte ufficiale?", "Edilcassa / Confartigianato Veneto e contratto regionale 2025/2026."),
            ("Righetto loca a imprese?", "Sì — servizio locazioni anche per unità multi-inquilino."),
        ],
        "related": [
            ("Servizio locazioni", "servizio-locazioni"),
            ("Studentati Veneto", "blog-studentati-veneto-2026-posti-letto"),
            ("Valutazione gratuita", "landing-valutazione"),
        ],
        "lead_ids": ("bl-nome-edil", "bl-tel-edil", "bl-email-edil", "bl-msg-edil", "bl-gdpr-edil"),
        "registry": {
            "titolo": "Housing lavoratori Veneto 2026: Edilcassa fondo 250.000€",
            "categoria": "Mercato immobiliare",
            "tempo": 10,
            "contenuto": "Fondo garanzia Edilcassa 250.000€, contratto 2025/26, corporate housing imprese edili venete.",
            "evidenza": False,
            "emoji": "🏗️",
        },
    },
]


def main() -> None:
    asset_keys = {
        "blog-stanza-universitaria-padova-canoni-2026": "stanza",
        "blog-studentati-veneto-2026-posti-letto": "studentati",
        "blog-residenze-green-padova-tribloc-2026": "green",
        "blog-vicenza-residenze-universitarie-calmierate-2026": "vicenza",
        "blog-housing-lavoratori-veneto-edilcassa-2026": "lavoratori",
    }
    registry = {
        "generated": DATE_ISO,
        "date_display": DATE_IT,
        "files": [],
        "blog_html_articoliStatici": [],
        "admin_blogSeedArticles": [],
        "homepage_js_articoliStatici": [],
    }
    for cfg in ARTICLES:
        ak = asset_keys[cfg["slug"]]
        cfg["img"] = ASSETS[ak]["hero"]
        cfg["hero_img"] = ASSETS[ak]["hero"]
        cfg["hero_alt"] = ASSETS[ak]["hero_alt"]
        cfg["registry"]["categoria"] = "Affitti"
        cfg["registry"]["evidenza"] = False
        body = cfg["body_fn"]() + COMMON_BODY_TAIL
        wc = word_count(body)
        if wc < MIN_BODY_WORDS:
            raise ValueError(f"{cfg['slug']}: corpo {wc} parole < {MIN_BODY_WORDS}")
        html = build_html(cfg, body, wc)
        out = ROOT / cfg["filename"]
        out.write_text(html, encoding="utf-8")
        entries = registry_entries(cfg)
        registry["files"].append({"filename": cfg["filename"], "slug": cfg["slug"], "wordCount_body": wc})
        registry["blog_html_articoliStatici"].append(entries["blog_html"])
        registry["admin_blogSeedArticles"].append(entries["admin"])
        registry["homepage_js_articoliStatici"].append(entries["homepage"])
        print(f"OK {cfg['filename']} — {wc} parole")
    reg_path = ROOT / "scripts" / "housing_veneto_lug2026_registry.json"
    reg_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Registry: {reg_path}")


if __name__ == "__main__":
    main()

