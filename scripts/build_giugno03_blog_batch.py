# -*- coding: utf-8 -*-
"""Genera 6 articoli blog 3 giugno 2026 — Righetto. Esegui da repo root:
python scripts/build_giugno03_blog_batch.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from build_apr19_blog_batch import (  # noqa: E402
    DISCLAIMER_BODY,
    MAX_TEMPLATE_PARAGRAPHS,
    MEDIAZIONE,
    assert_body_paragraph_diversity,
    build_paragraphs,
    word_count,
)

DATE_IT = "3 giugno 2026"
DATE_ISO = "2026-06-03"
TIME_TS = "2026-06-03T09:00:00+02:00"
MIN_BODY_WORDS = 2400

STYLE_BLOCK = r"""<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--nero:#152435;--bianco:#F7F5F1;--oro:#FF6B35;--grigio:#6B7A8D;--gc:#E1DBD1;--sfondo:#ECE7DF;--blu:#2C4A6E;--oro2:#FF8F5E}
body{font-family:'Montserrat',sans-serif;background:var(--bianco);color:var(--nero)}
header{background:var(--nero);position:sticky;top:0;z-index:100}
.hi{max-width:1380px;margin:0 auto;padding:0 1.5rem;height:74px;display:flex;align-items:center;gap:2rem}
.logo{font-family:'Cormorant Garamond',serif;color:#fff;font-size:1.28rem;font-weight:600}.logo span{color:var(--oro);font-style:italic}
nav{display:flex;flex:1;gap:.2rem}nav a{color:rgba(255,255,255,.72);font-size:.81rem;padding:.4rem .72rem}nav a.active{color:var(--oro)}
.h-btn{background:var(--oro);color:var(--nero);padding:.4rem .88rem;border-radius:6px;font-size:.76rem;font-weight:600}
.art-hero{position:relative}.art-hero-img{width:100%;height:468px;object-fit:cover;filter:brightness(.48)}
.art-hero-overlay{position:absolute;inset:auto 0 0 0;padding:2.65rem 1.5rem;background:linear-gradient(transparent,rgba(21,36,53,.95))}
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
.warn{background:linear-gradient(135deg,rgba(44,74,110,.08),rgba(255,107,53,.08));border:1px solid var(--gc);border-radius:10px;padding:1rem 1.2rem;margin:1.2rem 0;font-size:.86rem}
.aeo-box{border:2px solid var(--blu);border-radius:12px;padding:1.15rem 1.3rem;margin-bottom:1.65rem;background:linear-gradient(135deg,rgba(44,74,110,.07),rgba(255,107,53,.06))}
.aeo-box h2{font-family:'Montserrat',sans-serif;font-size:.95rem;text-transform:uppercase;letter-spacing:.06em;color:var(--blu);margin:0 0 .55rem;border:none;padding:0}
.aeo-box ul{font-size:.84rem;margin:.3rem 0 0 1.15rem}
.cap-img{font-size:.72rem;color:var(--grigio);margin:.4rem 0 0}
.cta-deep{display:inline-flex;background:linear-gradient(180deg,var(--oro2),var(--oro));color:var(--nero);font-weight:800;padding:.8rem 1.62rem;border-radius:10px;font-size:.8rem;margin:1rem .75rem 1rem 0}
.faq-item{border:1px solid var(--gc);border-radius:8px;margin-bottom:.5rem}
.faq-q{padding:.86rem .98rem;font-weight:600;font-size:.84rem;cursor:pointer}.faq-a{max-height:0;overflow:hidden;transition:max-height .35s;background:var(--sfondo)}
.faq-item.open .faq-a{max-height:420px}.faq-a-inner{padding:0 .98rem .86rem;font-size:.83rem;color:var(--grigio)}
.author-bio{display:flex;gap:1.08rem;padding:1.38rem;border:1px solid rgba(44,74,110,.12);border-radius:12px;margin:1.68rem 0}
.related{background:var(--sfondo);border:1px solid var(--gc);padding:1.32rem;border-radius:10px}
footer{background:linear-gradient(180deg,var(--nero),#0d1a2a);color:rgba(255,255,255,.65);padding:2.35rem 1.5rem;font-size:.75rem}
.skip-link{position:absolute;top:-100%;background:var(--oro);color:var(--nero);padding:.46rem .9rem;z-index:9999}.skip-link:focus{top:0}
@media(max-width:700px){.art-hero-img{height:288px}}
</style>
  <link rel="stylesheet" href="css/blog-lead-form.css?v=1">"""

FOOTER = """
</main>
<footer><div class="fi">&copy; 2026 Gruppo Immobiliare Righetto — P.IVA 05182390285 — Via Roma 96, Limena (PD)</div></footer>
<script>document.querySelectorAll('.faq-q').forEach(function(q){q.addEventListener('click',function(){var p=this.parentElement,o=p.classList.contains('open');document.querySelectorAll('.faq-item.open').forEach(function(x){x.classList.remove('open');});if(!o)p.classList.add('open');});});</script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="js/config.js?v=4"></script>
<script src="js/rig-lead-form.js?v=3"></script>
<script src="js/nav-mobile.js?v=3" defer></script>
<script src="js/cookie-consent.js?v=3" defer></script>
</body></html>
"""


def aeo_box(per_chi: str, sintesi_items: list[str], non_e_items: list[str]) -> str:
    sintesi_li = "".join(f"<li>{s}</li>" for s in sintesi_items)
    non_e_li = "".join(f"<li>{s}</li>" for s in non_e_items)
    return f"""<div class="aeo-box">
<h2>Per chi è questo articolo</h2>
<p style="font-size:.84rem;margin:0">{per_chi}</p>
<h2 style="margin-top:.85rem">In sintesi</h2>
<ul>{sintesi_li}</ul>
<h2 style="margin-top:.85rem">Cosa NON è</h2>
<ul>{non_e_li}</ul>
</div>"""


def sources_table(rows: list[tuple[str, str, str]]) -> str:
    body = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
    return f"""<h2 id="tab-fonti">Tabella riepilogo fonti citate</h2>
<table>
<thead><tr><th>Indicatore / tema</th><th>Fonte primaria</th><th>Uso operativo</th></tr></thead>
<tbody>{body}</tbody>
</table>
<p style="font-size:.8rem;color:var(--grigio)"><em>Ultimo aggiornamento contenuti: {DATE_IT}. Verificare sempre comunicati e tabelle ufficiali aggiornate.</em></p>"""


def faq_html(faqs: list[tuple[str, str]]) -> str:
    items = ""
    for q, a in faqs:
        items += f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>'
    return f'<div id="faq" style="margin-top:2rem"><h2 style="font-family:\'Cormorant Garamond\',serif;font-size:1.62rem;border-bottom:2px solid var(--oro);margin-bottom:.9rem">Domande frequenti</h2>{items}</div>'


def build_body(cfg: dict) -> tuple[str, int]:
    body_n = int(cfg.get("body_n", 10))
    static_parts = [
        cfg["cap_img"],
        cfg["aeo"],
        cfg.get("body_extra", ""),
        cfg.get("body_mid", ""),
        cfg.get("body_tail", ""),
        cfg["sources"],
        DISCLAIMER_BODY,
        MEDIAZIONE,
    ]
    static_html = "\n".join(p for p in static_parts if p)
    template = build_paragraphs(cfg["topic"], cfg["anchors"], n=body_n) if body_n else ""
    body = "\n".join(p for p in [static_html, template] if p)
    while word_count(body) < MIN_BODY_WORDS and body_n < MAX_TEMPLATE_PARAGRAPHS:
        body_n += 4
        template = build_paragraphs(cfg["topic"], cfg["anchors"], n=body_n)
        body = "\n".join(p for p in [static_html, template] if p)
    if body_n > MAX_TEMPLATE_PARAGRAPHS:
        raise ValueError(
            f"body_n={body_n} supera MAX_TEMPLATE_PARAGRAPHS={MAX_TEMPLATE_PARAGRAPHS} "
            f"per {cfg['slug']}; aggiungere prosa unica."
        )
    assert_body_paragraph_diversity(body)
    wc = word_count(body)
    if wc < MIN_BODY_WORDS:
        raise ValueError(f"{cfg['slug']}: corpo {wc} parole < {MIN_BODY_WORDS}")
    return body, wc


def build_article(cfg: dict) -> tuple[str, int]:
    slug = cfg["slug"]
    img = cfg["img"]
    body, wc_body = build_body(cfg)

    blog_obj = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": cfg["schema_headline"],
        "description": cfg["meta_desc"],
        "image": [f"https://righettoimmobiliare.it/{img}"],
        "author": {"@type": "Person", "name": "Gino Capon"},
        "publisher": {"@type": "Organization", "name": "Righetto Immobiliare", "url": "https://righettoimmobiliare.it"},
        "datePublished": DATE_ISO,
        "dateModified": DATE_ISO,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://righettoimmobiliare.it/{slug}"},
        "articleSection": cfg["section"],
        "wordCount": wc_body,
        "inLanguage": "it-IT",
    }
    faq_obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in cfg["faqs"]
        ],
    }
    bread_obj = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://righettoimmobiliare.it/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://righettoimmobiliare.it/blog"},
            {"@type": "ListItem", "position": 3, "name": cfg["bread"]},
        ],
    }

    rel_html = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in cfg["related"])

    head = f"""<!DOCTYPE html>
<html lang="it">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PHEL8KXLBX"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-PHEL8KXLBX');</script>
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
<meta property="og:image" content="https://righettoimmobiliare.it/{img}">
<meta property="article:published_time" content="{TIME_TS}">
<meta property="article:author" content="Gino Capon">
<meta name="description" content="{cfg["meta_desc"]}">
<script type="application/ld+json">{json.dumps(blog_obj, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_obj, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(bread_obj, ensure_ascii=False)}</script>
<link rel="stylesheet" href="css/fonts.css?v=3"><link rel="stylesheet" href="css/nav-mobile.css?v=4">
<link rel="stylesheet" href="css/scroll-reveal.css?v=3" media="print" onload="this.media='all'">
{STYLE_BLOCK}
</head>
<body>
<a href="#main-content" class="skip-link">Contenuto principale</a>
<header><div class="hi">
  <a href="/" class="logo">Righetto <span>Immobiliare</span></a>
  <nav><a href="/">Home</a><a href="blog" class="active">Blog</a><a href="contatti">Contatti</a></nav>
  <a class="h-btn" href="landing-consulenza-immobiliare-gratuita">Consulenza gratuita</a>
</div><button class="nav-burger" id="burgerBtn" aria-label="Menu"><span></span><span></span><span></span></button></header>
<div class="nav-mobile" id="navMobile"><a href="/">Home</a><a href="blog">Blog</a><a href="contatti">Contatti</a></div>
<main id="main-content">
<div class="art-hero">
  <img class="art-hero-img" src="{img}" alt="{cfg["alt_img"]}" width="1200" height="630" fetchpriority="high">
  <div class="art-hero-overlay"><div class="art-hero-inner">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="blog">Blog</a> / {cfg["breadcrumb_tail"]}</div>
    <span class="cat-badge">{cfg["cat_badge"]}</span>
    <h1>{cfg["h1"]}</h1>
    <div class="art-hero-meta"><div class="av">G</div><span>Gino Capon</span><span>{DATE_IT}</span><span>Aggiornato: {DATE_IT}</span></div>
  </div></div>
</div>
<div class="art-container"><div class="art-content">
{body}
<a class="cta-deep" href="{cfg["cta_primary"][1]}">{cfg["cta_primary"][0]}</a>
<a class="cta-deep" href="{cfg["cta_secondary"][1]}" style="background:var(--blu);color:#fff">{cfg["cta_secondary"][0]}</a>
{faq_html(cfg["faqs"])}
<div class="author-bio"><img src="img/team/titolari.webp" alt="Gino Capon Righetto Immobiliare" width="64" height="64" loading="lazy"><div><strong>Gino Capon</strong><p style="font-size:.8rem;color:#555">Titolare — Righetto Immobiliare, Limena (PD). Analisi di mercato per famiglie e investitori nel territorio patavino.</p><p style="font-size:.78rem;margin-top:.4rem"><a href="gino-capon">Profilo autore</a></p></div></div>
<div class="related"><h3 style="font-family:'Cormorant Garamond',serif">Articoli correlati</h3><ul style="margin-left:1.1rem;margin-top:.4rem">{rel_html}</ul></div>
</div></div>
<section class="blog-lead-wrap" id="richiedi-consulenza" aria-labelledby="blog-lead-title">
  <h2 id="blog-lead-title">Richiedi una consulenza gratuita</h2>
  <form data-rig-lead-form data-provenienza="{slug}" data-pagina="{slug}" data-msg-prefix="[Blog]" novalidate>
    <div class="bl-fields">
      <label for="bl-nome-{slug}">Nome e cognome *</label>
      <input type="text" id="bl-nome-{slug}" required autocomplete="name" placeholder="Mario Rossi">
      <label for="bl-tel-{slug}">Telefono *</label>
      <input type="tel" id="bl-tel-{slug}" required autocomplete="tel" placeholder="333 123 4567">
      <label for="bl-email-{slug}">Email</label>
      <input type="email" id="bl-email-{slug}" autocomplete="email" placeholder="mario@email.it">
      <label for="bl-msg-{slug}">Messaggio (opzionale)</label>
      <textarea id="bl-msg-{slug}" placeholder="Comune, obiettivo vendita/acquisto…"></textarea>
      <label class="bl-chk"><input type="checkbox" id="bl-gdpr-{slug}" required> Acconsento al trattamento dei dati (GDPR). <a href="privacy-policy">Privacy</a></label>
      <button type="submit">Invia richiesta</button>
    </div>
    <div class="rig-lead-success">
      <h3>Messaggio inviato!</h3>
      <p>Grazie. Ti ricontattiamo entro pochi minuti negli orari di apertura.</p>
    </div>
  </form>
</section>
"""
    return head + FOOTER, wc_body


ARTICLES: list[dict] = [
    {
        "filename": "blog-gestione-spese-casa-risparmio-padova-2026.html",
        "slug": "blog-gestione-spese-casa-risparmio-padova-2026",
        "img": "img/blog/blog-gestione-spese-casa-padova-2026.webp",
        "bread": "Gestione spese casa Padova",
        "section": "Guida acquirenti",
        "html_title": "Gestione spese casa dopo l'acquisto a Padova 2026: energia, IMU, dispensa | Righetto",
        "og_title": "Economia domestica per proprietari padovani: risparmio senza perdere valore immobile",
        "schema_headline": "Gestione spese casa e risparmio per proprietari nel Padovano dopo la compravendita",
        "meta_desc": "Guida immobiliare alla gestione post-acquisto a Padova: dispensa, bollette, decluttering, IMU e manutenzione. Principi verificabili, non lifestyle blog.",
        "cat_badge": "Guida acquirenti",
        "alt_img": "Casa padovana e gestione domestica — illustrazione editoriale spese proprietà e risparmio energetico",
        "breadcrumb_tail": "Gestione spese casa",
        "h1": "<strong>Gestione spese casa</strong> dopo l'acquisto a Padova: risparmio, manutenzione e valore dell'immobile",
        "cap_img": '<p class="cap-img">Immagine <strong>illustrativa</strong> su gestione domestica — angolo immobiliare, non consigli lifestyle. Ispirazione editoriale da guide economia domestica; dati fiscali da <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a>.</p>',
        "aeo": aeo_box(
            "Per <strong>proprietari nel Padovano</strong> che hanno chiuso la compravendita e vogliono contenere costi fissi senza penalizzare manutenzione, APE e valore di rivendita.",
            [
                "Dopo il rogito, <strong>bollette, IMU, TARI e manutenzione</strong> incidono sul costo totale di proprietà oltre alla rata mutuo.",
                "Organizzare <strong>dispensa, spazi e consumi energetici</strong> riduce sprechi senza trascurare impianti e sicurezza.",
                "Il <strong>decluttering ordinato</strong> facilita ispezioni, perizie e home staging in caso di futura vendita.",
                "L'<a href=\"https://www.agenziaentrate.gov.it\" target=\"_blank\" rel=\"noopener noreferrer\">Agenzia delle Entrate</a> pubblica guide su IMU e agevolazioni: verificare sempre l'anno d'imposta vigente.",
            ],
            [
                "Non è un blog di ricette o decorazione d'interni.",
                "Non promette risparmi percentuali fissi su bollette senza audit energetico.",
                "Non sostituisce il commercialista per IMU e detrazioni.",
            ],
        ),
        "body_extra": """<h2>Perché parlarne in chiave immobiliare</h2>
<p>Dopo l'acquisto a <strong>Padova</strong> o in cintura — da <strong>Limena</strong> a <strong>Albignasego</strong> — molte famiglie concentrano l'attenzione su mutuo e rogito, sottovalutando il <strong>costo annuo di possesso</strong>. Gestire spesa alimentare, energia e spazi non è solo abitudine domestica: incide su liquidità per lavori straordinari, su classe energetica percepita e su tempi di vendita futura. Guide generaliste sull'economia domestica offrono spunti utili; qui li traduciamo per chi ha un capitale immobilizzato in un appartamento o in una villetta.</p>
<h2>Tabella voci ricorrenti post-acquisto</h2>
<table>
<thead><tr><th>Voce</th><th>Frequenza</th><th>Nota immobiliare Padovano</th></tr></thead>
<tbody>
<tr><td>Mutuo / spese bancarie</td><td>mensile</td><td>Già noto in fase acquisto — vedi <a href="blog-mutuo-prima-casa-padova">mutuo prima casa</a></td></tr>
<tr><td>Condominio (ordinarie + straordinarie)</td><td>trimestrale / straordinarie</td><td>Verificare fondo lavori e delibere pendenti</td></tr>
<tr><td>IMU</td><td>annuale</td><td>Calcolo su sito <a href="https://www.agenziaentrate.gov.it/portale/web/guest/schede/fabbricatiterreni/imu" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate — IMU</a></td></tr>
<tr><td>TARI</td><td>annuale</td><td>Comune di residenza dell'immobile</td></tr>
<tr><td>Energia e gas</td><td>mensile</td><td>Classe APE incide su bolletta e appeal in vendita</td></tr>
<tr><td>Manutenzione impianti</td><td>annuale / quinquennale</td><td>Certificazioni obbligatorie (es. caldaia) evitano contestazioni</td></tr>
</tbody>
</table>
<h2>Dispensa e spazi: ordine che protegge l'investimento</h2>
<p>Una dispensa gestita con rotazione scorte evita sprechi alimentari e umidità in ripostigli poco ventilati — problema frequente in bilocali del <strong>centro storico</strong> con murature spesse. In termini immobiliari, umidità e muffe danneggiano intonaci e pavimenti; un controllo periodico degli angoli ciechi (sotto lavelli, cassonetti) è manutenzione preventiva a costo zero. Il decluttering — liberare stanze da oggetti inutilizzati — migliora percezione metratura in visita e semplifica eventuale <a href="blog-home-staging-padova">home staging</a>.</p>
<h3>Energia: dove il risparmio incontra l'APE</h3>
<p>ISTAT monitora prezzi energia e costo della vita; le bollette dipendono da abitudini e da isolamento reale. Interventi mirati (serramenti, valvole termostatiche, manutenzione climatizzatore) hanno più senso se allineati a un piano di valorizzazione documentato. Non promettiamo percentuali di risparmio standard: servono audit e fatture storiche dell'immobile.</p>""",
        "body_mid": """<h2>IMU e fiscalità di possesso</h2>
<p>L'<strong>IMU</strong> si applica secondo normativa vigente e delibere comunali; l'<a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a> mette a disposizione schede, aliquote e calcolatori. Prima casa in uso proprio può beneficiare di esenzioni o riduzioni se rispettati i requisiti: verificare con commercialista, distinto dall'articolo sulle <a href="blog-agevolazioni-prima-casa-2026">agevolazioni acquisto</a>. Per chi acquista in <strong>seconda casa</strong> nel Padovano, IMU e TARI pesano sul rendimento locativo netto.</p>
<h2>Checklist trimestrale proprietario padovano</h2>
<ul>
<li>Controllare bollette vs consumi precedenti; segnalare anomalie a gestore o tecnico.</li>
<li>Verificare stato caldaia e climatizzazione; conservare libretti per futura due diligence.</li>
<li>Rivedere spese condominiali e avvisi di assemblea straordinaria.</li>
<li>Ispezionare cantina e garage per infiltrazioni — comuni in zone umide come <strong>Saonara</strong>.</li>
<li>Aggiornare inventario lavori fatti (fatture) per eventuale vendita.</li>
</ul>
<h3>Decluttering prima di una futura vendita</h3>
<p>Stanze ordinate e prive di accumulo accelerano perizia e shooting fotografico. Non serve ristrutturazione: serve percezione di spazio utile e impianti accessibili. Incrociare con <a href="blog-documenti-vendita-casa">documenti di vendita</a> e con <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a> se valutate di uscire dal mercato nei prossimi anni.</p>
<h2>Risparmio sì, ma senza trascurare il capitale immobile</h2>
<p>Rinviare manutenzione del tetto condominiale o della caldaia per risparmiare centinaia di euro può costare migliaia in danni o sconto in trattativa. Il bilancio familiare post-acquisto dovrebbe prevedere una <strong>riserva lavori</strong> — Banca d'Italia documenta regolarmente il peso delle spese obbligate sulle famiglie — separata dalla spesa corrente. In agenzia, vediamo acquirenti che sottostimano questo capitolo e slittano su riqualificazioni energetiche utili al mercato.</p>
<div class="warn"><strong>Nota:</strong> guide esterne sull'economia domestica (es. blog specializzati consumi) sono ispirazione editoriale; per imposte e detrazioni usare solo fonti istituzionali e pareri professionali.</div>""",
        "body_tail": """<h2>Condominio: spesa condivisa che influenza il valore</h2>
<p>In edifici padovani anni '70-'90, spese straordinarie per facciate e cappotto sono frequenti. Un proprietario attento partecipa alle assemblee, legge preventivi e evita sorprese che spaventano acquirenti futuri. Chiedere estratto conto spese e stato fondo lavori prima di mettere in vendita è coerente con <a href="blog-percorso-vendita-immobile-padova-2026">percorso di vendita</a> strutturato.</p>
<h3>Studenti e affitti brevi: gestione consumi</h3>
<p>Appartamenti vicino all'università subiscono rotazione inquilini e consumi elevati. Contratti chiari su utenze e manutenzione ordinaria proteggono il reddito netto. Per chi passa da locazione a vendita, documentare interventi su impianti rassicura acquirenti con mutuo.</p>
<h2>Integrazione con il piano mutuo</h2>
<p>La rata non è l'unico impegno mensile: includere condominio, IMU rateizzata dove previsto, assicurazione fabbricato e manutenzione nel budget evita tensioni familiari. Per chi ha appena acquistato, rivedere il piano dopo sei mesi di bollette reali è più utile di qualsiasi stima teorica. Righetto affianca famiglie del <strong>Padovano</strong> con orientamento su valore immobile e tempi di mercato, non con consulenza finanziaria domestica.</p>
<h2>Quando il risparmio conviene investirlo in casa</h2>
<p>Se il risparmio accumulato supera la soglia di emergenza familiare, valutare interventi con ROI difendibile: sostituzione infissi in appartamento classe G, adeguamento elettrico in immobili con impianto datato. Ogni scelta va incrociata con OMI e comparabili — non con trend lifestyle. Per mutuo e ristrutturazione, vedi <a href="blog-bonus-mobili-2026-massimizzare-ristrutturazioni">bonus e ristrutturazioni</a>.</p>""",
        "sources": sources_table([
            ("IMU e possesso", "Agenzia delle Entrate — schede IMU", "Aliquote, esenzioni, calcolo"),
            ("Costo vita famiglie", "ISTAT — indici prezzi", "Contesto inflazione spese correnti"),
            ("Credito e spese obbligate", "Banca d'Italia", "Sostenibilità budget familiare"),
            ("Economia domestica (ispirazione)", "Lucidellart — guide consumi", "Solo spunto editoriale, non fonte fiscale"),
        ]),
        "topic": "gestione spese casa proprietari Padova post acquisto",
        "anchors": [
            ("mutuo prima casa", "blog-mutuo-prima-casa-padova"),
            ("documenti vendita", "blog-documenti-vendita-casa"),
        ],
        "body_n": 22,
        "faqs": [
            ("La gestione dispensa influenza il valore casa?", "Indirettamente: meno umidità e migliore manutenzione preservano gli interni e la percezione in visita."),
            ("Dove calcolo l'IMU a Padova?", "Sul portale Agenzia delle Entrate e sul sito del Comune per aliquote locali."),
            ("Conviene rimandare manutenzione per risparmiare?", "Spesso no: rischi danni maggiori e sconti in vendita futura."),
            ("Questo articolo sostituisce un commercialista?", "No: per IMU e detrazioni servono pareri professionali aggiornati."),
            ("Come collegare risparmio e APE?", "Interventi energetici documentati migliorano classe e appeal — con preventivi tecnici."),
            ("Righetto gestisce utenze?", "No: supportiamo compravendita e valorizzazione immobiliare nel Padovano."),
        ],
        "related": [
            ("Mutuo prima casa Padova", "blog-mutuo-prima-casa-padova"),
            ("Documenti vendita casa", "blog-documenti-vendita-casa"),
            ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        ],
        "cta_primary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        "cta_secondary": ("Valutazione immobile", "landing-valutazione"),
        "registry": {
            "titolo": "Gestione spese casa dopo l'acquisto a Padova 2026: energia, IMU, dispensa",
            "categoria": "Guida acquirenti",
            "tempo": 12,
            "contenuto": "Economia domestica in chiave immobiliare: possesso, manutenzione e risparmio nel Padovano.",
            "evidenza": True,
            "emoji": "🏠",
        },
    },
    {
        "filename": "blog-scegliere-immobile-giusto-padova-2026.html",
        "slug": "blog-scegliere-immobile-giusto-padova-2026",
        "img": "img/blog/blog-scegliere-immobile-giusto-padova-2026.webp",
        "bread": "Scegliere immobile giusto Padova",
        "section": "Guida acquirenti",
        "html_title": "Come scegliere l'immobile giusto a Padova 2026: zona, luce, condominio, impianti | Righetto",
        "og_title": "Dieci criteri per la casa giusta nel Padovano: oltre il prezzo al mq",
        "schema_headline": "Criteri per scegliere l'immobile giusto a Padova: zona, luminosità, condominio e impianti",
        "meta_desc": "Guida per acquirenti padovani: zona, esposizione, rumore, condominio, impianti e conformità. Metodo Righetto, non lista generica portali.",
        "cat_badge": "Guida acquirenti",
        "alt_img": "Selezione appartamento Padova — illustrazione editoriale criteri acquisto casa luminosità e zona",
        "breadcrumb_tail": "Scegliere immobile giusto",
        "h1": "<strong>Scegliere l'immobile giusto</strong> a Padova: criteri oltre il prezzo al metro quadro",
        "cap_img": '<p class="cap-img">Immagine <strong>illustrativa</strong> su scelta immobile — metodo acquirente Padovano. Ispirazione editoriale da checklist portali; verifiche su OMI e normativa da fonti istituzionali.</p>',
        "aeo": aeo_box(
            "Per <strong>acquirenti nel territorio patavino</strong> che confrontano annunci e visite e vogliono una griglia di valutazione oggettiva prima dell'offerta.",
            [
                "<strong>Zona e microzona</strong> determinano servizi, rumore e liquidità futura — incrociare con OMI.",
                "<strong>Luminosità ed esposizione</strong> incidono su comfort, bollette e percezione in rivendita.",
                "<strong>Condominio e spese</strong> vanno letti con ultimo bilancio e delibere straordinarie.",
                "<strong>Impianti e conformità</strong> evitano costi nascosti post-compromesso.",
            ],
            [
                "Non è ranking soggettivo di quartieri «alla moda».",
                "Non garantisce plusvalenze.",
                "Non sostituisce sopralluogo tecnico e visura catastale.",
            ],
        ),
        "body_extra": """<h2>Oltre la «casa perfetta» dei portali</h2>
<p>Le checklist generiche — spesso ispirate da articoli tipo «dieci consigli per la casa perfetta» su portali nazionali — elencano desiderabilità estetica. Per chi compra a <strong>Padova</strong>, servono criteri verificabili: titoli edilizi, spese condominiali reali, esposizione solare misurabile in visita, distanza da servizi effettivamente usati. Il prezzo al metro quadro da OMI è un inizio, non una verdetto.</p>
<h2>Griglia di valutazione (tabella operativa)</h2>
<table>
<thead><tr><th>Criterio</th><th>Cosa verificare in visita</th><th>Rischio se ignorato</th></tr></thead>
<tbody>
<tr><td>Zona / microzona</td><td>OMI, pendolarismo, rumore notturno</td><td>Difficoltà rivendita o affitto</td></tr>
<tr><td>Luminosità</td><td>Esposizione, altezza piani, ostacoli</td><td>Costi energia, percezione «buia»</td></tr>
<tr><td>Condominio</td><td>Bilancio, lavori straordinari, regolamento</td><td>Spese impreviste migliaia di euro</td></tr>
<tr><td>Impianti</td><td>Età caldaia, certificazioni, quadro elettrico</td><td>Obbligo adeguamento post-acquisto</td></tr>
<tr><td>Struttura</td><td>Infiltrazioni, crepe, cantina</td><td>Contenzioso e sconto rogito</td></tr>
<tr><td>Documenti</td><td>APE, planimetria, conformità</td><td>Mutuo negato o clausole sospensive</td></tr>
</tbody>
</table>
<h2>Zona Padova: città, cintura e collina</h2>
<p>Il capoluogo offre semicentro storico, zone universitarie e periferie servite da tram e bus; la cintura (<strong>Limena, Vigodarzere, Cadoneghe</strong>) attrae famiglie per metrature e parcheggi. I <strong>Colli Euganei</strong> aggiungono turismo e stagionalità. Non esiste zona «giusta» in assoluto: esiste coerenza con budget, pendolarismo e orizzonte anni. Per quadro prezzi: <a href="blog-mercato-immobiliare-padova-2026">mercato Padova 2026</a>.</p>
<h3>Luminosità e orientamento</h3>
<p>In visita, osservare a diverse ore: sud e est regalano luce mattutina; nord può richiedere illuminazione artificiale costante. Balconi su cortili interni in condominio padovano spesso riducono ventilazione. Annotare con foto geotagged per confrontare più annunci senza affidarsi alla memoria.</p>""",
        "body_mid": """<h2>Condominio: il costo invisibile</h2>
<p>Chiedere ultimo bilancio consuntivo, preventivo corrente e elenco lavori straordinari approvati ma non ancora pagati. Un appartamento «economico» con straordinaria da 15.000 euro in arrivo non è un affare. Verificare regolamento su animali, affitti brevi e modifiche interne — rilevante se pensate a locazione studenti. Per debiti condominiali in vendita, vedi <a href="blog-documenti-compravendita-rogito-padova-2026">documenti al rogito</a>.</p>
<h2>Impianti: dove nascono i preventivi post-acquisto</h2>
<p>Caldaia oltre 15-20 anni, impianto elettrico senza certificazione, assenza di climatizzazione in piano alto: voci che comparabili moderni già includono. Un tecnico prima dell'offerta vincolante costa meno di una clausola sospensiva fallita. Incrociare con <a href="blog-ape-prestazione-energetica-acquisto-padova-2026">APE in acquisto</a>.</p>
<h2>Checklist pre-offerta (lista numerata)</h2>
<ol>
<li>Confrontare almeno tre microzone con bande OMI coerenti.</li>
<li>Seconda visita in orario diverso (rumore, luce).</li>
<li>Richiedere APE, planimetria catastale e ultimo bilancio condominiale.</li>
<li>Stimare costo impianti se datati (preventivo non vincolante).</li>
<li>Verificare parcheggio e ZTL se usate auto quotidianamente.</li>
<li>Allineare prezzo offerta a comparabili venduti, non solo in vendita.</li>
</ol>
<p>Prima di firmare, leggere <a href="blog-comprare-casa-padova-guida-2026">guida comprare casa Padova</a> e valutare <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a> per incrociare annuncio e realtà di mercato.</p>""",
        "body_tail": """<h2>Errore frequente: scegliere solo per metratura</h2>
<p>Due appartamenti da 85 mq possono avere distribuzione opposta: uno con cucina abitabile e due bagni attrae famiglie; l'altro con cameretta non conforme rischia sanatoria. La planimetria catastale va confrontata con stato di fatto — tema <a href="blog-planimetria-catastale-compravendita-padova-2026">planimetria e compravendita</a>.</p>
<h3>Acquirente con mutuo: coerenza perizia</h3>
<p>La banca perizia classe energetica, ubicazione e stato manutentivo. Un immobile «giusto» emotivamente ma con difformità può non finanziarsi. Anticipare verifica con <a href="blog-mutuo-prima-casa-padova">mutuo prima casa</a> e pre-approvazione.</p>
<h2>Venditore onesto vs annuncio ottimistico</h2>
<p>Foto wide-angle e filtri nascondono soffitti bassi o vicinanza ferrovia. Misurare con metro laser, ascoltare ambienti senza musica del venditore, chiedere storico spese condominiali per tre anni. Righetto condivide schede visita strutturate nelle trattative in <strong>101 comuni</strong> serviti da Limena.</p>
<h2>Sintesi: metodo prima dell'emozione</h2>
<p>La casa giusta a Padova è quella che regge due diligence tecnica, budget totale (acquisto + lavori + spese) e orizzonte familiare. Emozione conta, ma dopo i filtri oggettivi. Per il passo successivo — compromesso — preparate la <a href="blog-checklist-verifiche-prima-compromesso-padova-2026">checklist pre-compromesso</a> del nostro blog.</p>""",
        "sources": sources_table([
            ("Quotazioni microzona", "OMI — Agenzia delle Entrate", "Confronto prezzo richiesto"),
            ("Efficienza energetica", "APE / D.lgs. 192/2005", "Classe e obblighi"),
            ("Contesto demografico", "ISTAT", "Servizi e domanda abitativa"),
            ("Checklist scelta casa (ispirazione)", "Immobiliare.it — guide editoriali", "Solo struttura argomenti, non dati"),
        ]),
        "topic": "scegliere immobile giusto criteri Padova acquirenti",
        "anchors": [
            ("comprare casa guida", "blog-comprare-casa-padova-guida-2026"),
            ("APE acquisto", "blog-ape-prestazione-energetica-acquisto-padova-2026"),
        ],
        "body_n": 24,
        "faqs": [
            ("Quale zona conviene a Padova?", "Dipende da budget, lavoro e stile di vita; usare OMI e visite multiple, non ranking generici."),
            ("Come giudicare luminosità?", "Visite a orari diversi, esposizione e ostacoli esterni; foto per confronto."),
            ("Cosa chiedere al condominio?", "Bilancio, straordinarie deliberate, fondo lavori, regolamento."),
            ("Quando serve tecnico?", "Prima dell'offerta vincolante su immobili datati o con dubbi su impianti."),
            ("Il prezzo più basso è sempre meglio?", "No se nasconde lavori, debiti condominiali o difformità."),
            ("Righetto seleziona per me?", "Affianchiamo con comparabili e visite; la scelta finale resta dell'acquirente."),
        ],
        "related": [
            ("Comprare casa Padova", "blog-comprare-casa-padova-guida-2026"),
            ("Checklist pre-compromesso", "blog-checklist-verifiche-prima-compromesso-padova-2026"),
            ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        ],
        "cta_primary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        "cta_secondary": ("Calcolo mutuo", "landing-chat-calcolo-mutuo"),
        "registry": {
            "titolo": "Come scegliere l'immobile giusto a Padova 2026: zona, luce, condominio",
            "categoria": "Guida acquirenti",
            "tempo": 12,
            "contenuto": "Criteri verificabili per acquirenti: microzona, impianti, condominio e documenti.",
            "evidenza": True,
            "emoji": "🔍",
        },
    },
    {
        "filename": "blog-quattro-imposte-rogitio-prima-casa-padova-2026.html",
        "slug": "blog-quattro-imposte-rogitio-prima-casa-padova-2026",
        "img": "img/blog/blog-quattro-imposte-rogitio-prima-casa-padova-2026.webp",
        "bread": "Quattro imposte rogito prima casa",
        "section": "Fisco",
        "html_title": "Le quattro imposte al rogito prima casa a Padova 2026: IVA, registro, ipotecaria, catastale | Righetto",
        "og_title": "Calcolo imposte notarili prima casa: DPR 131/1986 e requisiti ISEE",
        "schema_headline": "IVA, imposta di registro, ipotecaria e catastale al rogito prima casa nel Padovano",
        "meta_desc": "Focus calcolo al notaio: le quattro imposte su acquisto prima casa (IVA o registro, ipotecaria, catastale). DPR 131/1986, ISEE under 36 e soglia 40.000 € — fonti Agenzia delle Entrate.",
        "cat_badge": "Fisco",
        "alt_img": "Rogito notarile e imposte — illustrazione editoriale tasse acquisto prima casa Padova",
        "breadcrumb_tail": "Quattro imposte rogito",
        "h1": "<strong>Le quattro imposte</strong> al rogito prima casa a Padova: calcolo e requisiti verificabili",
        "cap_img": '<p class="cap-img">Immagine <strong>illustrativa</strong> su rogito — non è prospetto notarile. Ispirazione editoriale da guide fintech; aliquote e requisiti da <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a> e <strong>DPR 131/1986</strong>.</p>',
        "aeo": aeo_box(
            "Per <strong>acquirenti prima casa nel Padovano</strong> che distinguono agevolazioni generali da calcolo effettivo delle quattro imposte in sede di stipula.",
            [
                "Su compravendite <strong>da privato</strong> si applicano imposta di <strong>registro</strong>, <strong>ipotecaria</strong> e <strong>catastale</strong> (DPR 131/1986).",
                "Da <strong>impresa costruttrice</strong> con IVA: imposta sostitutiva IVA con ipotecaria e catastale in misura ridotta.",
                "Requisiti <strong>prima casa</strong> e <strong>ISEE under 36</strong> (soglia reddito 40.000 €) vanno verificati su normativa AE aggiornata.",
                "Angolo diverso dall'articolo sulle <a href=\"blog-agevolazioni-prima-casa-2026\">agevolazioni</a>: qui il focus è il conteggio al rogito.",
            ],
            [
                "Non è parere fiscale personalizzato.",
                "Non sostituisce il preventivo del notaio.",
                "Non ripete l'articolo su registro e catasto in generale.",
            ],
        ),
        "body_extra": """<h2>Le «quattro imposte»: schema chiaro</h2>
<p>In sede di rogito, l'acquirente affronta un insieme di tributi che i media riassumono come «quattro imposte». La nomenclatura precisa dipende da <strong>soggetto venditore</strong> (privato o impresa) e da <strong>agevolazione prima casa</strong>. Il <strong>DPR 131/1986</strong> (TUIR imposte ipotecarie e catastali) e successive modifiche definiscono aliquote e basi imponibili; l'<a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a> pubblica schede operative e FAQ aggiornate.</p>
<h2>Tabella comparativa privato vs costruttore (prima casa)</h2>
<table>
<thead><tr><th>Tributo</th><th>Da privato (agevolato prima casa)</th><th>Da impresa con IVA (prima casa)</th></tr></thead>
<tbody>
<tr><td>Imposta di registro</td><td>Aliquota agevolata su valore catastale (verificare AE)</td><td>Non applicabile — sostituita da IVA</td></tr>
<tr><td>IVA</td><td>Non applicabile</td><td>Aliquota agevolata su prezzo (es. 4% prima casa — verificare AE)</td></tr>
<tr><td>Imposta ipotecaria</td><td>Aliquota ridotta prima casa</td><td>Aliquota ridotta prima casa</td></tr>
<tr><td>Imposta catastale</td><td>Aliquota ridotta prima casa</td><td>Aliquota ridotta prima casa</td></tr>
</tbody>
</table>
<p><em>Aliquote effettive: consultare Agenzia delle Entrate e notaio per l'anno d'imposta e il caso concreto.</em></p>
<h2>ISEE under 36 e soglia 40.000 euro</h2>
<p>Per i giovani under 36, l'Agenzia delle Entrate ha definito requisiti e benefici collegati all'<strong>ISEE</strong> e a una soglia di reddito (comunicazioni ufficiali citano il limite di <strong>40.000 euro</strong> per accedere a certe agevolazioni). Verificare idoneità prima del compromesso: attestazione ISEE, residenza, vincoli di utilizzo dell'immobile come abitazione principale. Dettaglio requisiti in <a href="blog-agevolazioni-prima-casa-2026">agevolazioni prima casa 2026</a>, senza duplicare quel testo.</p>
<h3>Base imponibile: valore catastale vs prezzo</h3>
<p>Per imposta di registro su compravendita da privato, la base è in genere il <strong>valore catastale</strong> (rendita rivalutata) se superiore al prezzo dichiarato — regola da confermare con notaio. Su nuovo da costruttore, base IVA segue prezzo contrattuale con aliquota dedicata.</p>""",
        "body_mid": """<h2>Calcolo pratico al notaio: cosa chiedere</h2>
<p>Richiedere <strong>preventivo scritto</strong> con voce per voce: registro o IVA, ipotecaria, catastale, onorario notarile, bolli, volture. A Padova, rogiti su immobili con rendite catastali non aggiornate possono generare sorprese se il valore catastale supera il prezzo concordato. Incrociare con <a href="blog-imposte-registro-catasto-compravendita-padova-2026">imposte registro e catasto</a> per il quadro generale compravendita.</p>
<h2>Errore da evitare: confondere esenzioni</h2>
<ul>
<li>Prima casa abituale non coincide automaticamente con ogni beneficio under 36.</li>
<li>Seconda casa nel Padovano perde aliquote agevolate su registro/IVA.</li>
<li>Locazione futura può far decadere benefici: leggere vincoli AE.</li>
<li>Acquisto in comune diverso da residenza: verificare requisiti prima casa.</li>
</ul>
<h2>Mutuo e imposte: liquidità complessiva</h2>
<p>Oltre alle imposte, servono fondi per caparra, onorario notaio, perizia, assicurazioni. La Banca d'Italia documenta il peso delle spese accessorie sulle famiglie acquirenti. Per finanziamento: <a href="blog-mutuo-prima-casa-padova">mutuo prima casa Padova</a> e <a href="landing-consulenza-immobiliare-gratuita">consulenza</a>.</p>
<div class="warn"><strong>Distinzione:</strong> guide Moneyfarm e simili offrono spunti divulgativi sulle quattro imposte; per importi vincolanti usare solo notaio e Agenzia delle Entrate.</div>""",
        "body_tail": """<h2>Padova: casi tipici in agenzia</h2>
<p>Trilocale da privato in cintura con agevolazione prima casa: triade registro-ipotecaria-catastale a aliquote ridotte. Appartamento nuovo a <strong>Limena</strong> da costruttore: IVA agevolata più ipotecaria e catastale. Attico con categoria catastale non residenziale: verificare classificazione prima di stimare imposte — può cambiare aliquota.</p>
<h3>Documenti per non perdere agevolazioni</h3>
<p>Dichiarazione sostitutiva prima casa, certificazione residenza, eventuale ISEE per under 36, attestazione stato di famiglia. Il notaio inserisce clausole su decadenza se non si trasferisce la residenza entro termini di legge.</p>
<h2>Collegamento rogito e post-rogito</h2>
<p>Le imposte di acquisto sono una tantum; IMU e TARI iniziano dal possesso. Pianificare flusso cassa oltre il giorno del rogito. Per vendita futura, plusvalenza e imposte diverse — <a href="blog-costi-proprieta-acquisto-possesso-vendita-padova-2026">ciclo costi proprietà</a>.</p>
<h2>Sintesi operativa</h2>
<p>Prima dell'offerta: simulazione notarile indicativa. Prima del compromesso: verifica requisiti prima casa e under 36. Prima del rogito: bonifico imposte e controllo valori catastali. Righetto coordina tempi con studi notarili partner nel Padovano senza sostituire pareri fiscali.</p>""",
        "sources": sources_table([
            ("Aliquote registro/ipotecaria/catastale", "DPR 131/1986 — TUIR", "Testo coordinato imposte"),
            ("Prima casa e under 36", "Agenzia delle Entrate — schede acquisto", "Requisiti, ISEE, soglie"),
            ("IVA immobili", "Agenzia delle Entrate — IVA", "Nuovo da impresa"),
            ("Guide imposte rogito (ispirazione)", "Moneyfarm — articoli divulgativi", "Solo struttura argomenti"),
        ]),
        "topic": "quattro imposte rogito prima casa IVA registro ipotecaria catastale",
        "anchors": [
            ("agevolazioni prima casa", "blog-agevolazioni-prima-casa-2026"),
            ("imposte registro catasto", "blog-imposte-registro-catasto-compravendita-padova-2026"),
        ],
        "body_n": 22,
        "faqs": [
            ("Quali sono le quattro imposte al rogito?", "Registro o IVA (a seconda del venditore), ipotecaria e catastale — con aliquote diverse per prima casa."),
            ("Cosa dice il DPR 131/1986?", "Disciplina imposte ipotecarie e catastali su atti tra vivi e successioni."),
            ("Under 36 e 40.000 euro di reddito?", "Requisiti per benefici under 36 secondo normativa AE — verificare ISEE e comunicazioni vigenti."),
            ("Da privato o da costruttore cambia tutto?", "Sì: da privato registro; da impresa con IVA aliquota sostitutiva."),
            ("Il notaio calcola da solo?", "Sì, ma conviene preventivo anticipato per liquidità."),
            ("Righetto calcola imposte?", "No: rimandiamo a notaio e Agenzia delle Entrate."),
        ],
        "related": [
            ("Agevolazioni prima casa", "blog-agevolazioni-prima-casa-2026"),
            ("Imposte registro e catasto", "blog-imposte-registro-catasto-compravendita-padova-2026"),
            ("Mutuo prima casa", "blog-mutuo-prima-casa-padova"),
        ],
        "cta_primary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        "cta_secondary": ("Documenti rogito", "blog-documenti-compravendita-rogito-padova-2026"),
        "registry": {
            "titolo": "Quattro imposte al rogito prima casa Padova 2026: IVA, registro, ipotecaria, catastale",
            "categoria": "Fisco",
            "tempo": 11,
            "contenuto": "Calcolo al notaio, DPR 131/1986, ISEE under 36 — angolo operativo distinto dalle agevolazioni.",
            "evidenza": False,
            "emoji": "📋",
        },
    },
    {
        "filename": "blog-costi-proprieta-acquisto-possesso-vendita-padova-2026.html",
        "slug": "blog-costi-proprieta-acquisto-possesso-vendita-padova-2026",
        "img": "img/blog/blog-costi-proprieta-acquisto-possesso-vendita-padova-2026.webp",
        "bread": "Costi proprietà ciclo completo",
        "section": "Fisco",
        "html_title": "Costi proprietà immobiliare Padova 2026: acquisto, possesso, vendita e plusvalenza | Righetto",
        "og_title": "Dal rogito alla plusvalenza: ciclo fiscale e pratico della proprietà nel Padovano",
        "schema_headline": "Costi di acquisto, possesso e vendita immobile a Padova: privato, costruttore, IMU, plusvalenza",
        "meta_desc": "Ciclo completo costi proprietà: acquisto da privato o costruttore, IMU/TARI annuali, plusvalenza 26%. Fonti Agenzia delle Entrate e Banca d'Italia — guida pratica Padova.",
        "cat_badge": "Fisco",
        "alt_img": "Ciclo vita immobile — illustrazione editoriale costi acquisto possesso vendita Padova",
        "breadcrumb_tail": "Costi proprietà ciclo",
        "h1": "<strong>Costi della proprietà</strong> a Padova: acquisto, possesso e vendita in un unico percorso",
        "cap_img": '<p class="cap-img">Immagine <strong>illustrativa</strong> sul ciclo di proprietà — ispirazione editoriale The Dream RE; dati fiscali da <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a>.</p>',
        "aeo": aeo_box(
            "Per <strong>proprietari e investitori nel Padovano</strong> che vogliono mappare costi dall'acquisto alla vendita, inclusi IMU, TARI e tassazione plusvalenze.",
            [
                "Fase <strong>acquisto</strong>: imposte rogito, notaio, mutuo — diversa da privato vs costruttore.",
                "Fase <strong>possesso</strong>: IMU, TARI, condominio, manutenzione, assicurazioni.",
                "Fase <strong>vendita</strong>: imposte, plusvalenza (aliquota ordinaria <strong>26%</strong> su redditi diversi — verificare normativa vigente).",
                "Visione a ciclo evita di valutare solo il prezzo di acquisto.",
            ],
            [
                "Non è consulenza fiscale personalizzata.",
                "Non promette rendimenti netti su locazione.",
                "Non elenca tariffe di mediazione online.",
            ],
        ),
        "body_extra": """<h2>Perché ragionare a ciclo</h2>
<p>Molte guide confrontano solo «privato vs costruttore» al momento dell'acquisto. La proprietà immobiliare a <strong>Padova</strong> si estende su anni: costi fissi annuali, lavori straordinari, eventuale locazione e infine vendita con possibile <strong>plusvalenza</strong>. Una lettura integrata — come quella proposta da blog immobiliari internazionali adattata al contesto italiano — aiuta a non sottovalutare il costo totale di detenzione.</p>
<h2>Tabella tre fasi</h2>
<table>
<thead><tr><th>Fase</th><th>Principali voci</th><th>Fonte / verifica</th></tr></thead>
<tbody>
<tr><td>Acquisto</td><td>Imposte, notaio, perizia, agenzia</td><td>AE, preventivo notaio</td></tr>
<tr><td>Possesso</td><td>IMU, TARI, condominio, utenze, manutenzione</td><td>AE, Comune, bilancio condominiale</td></tr>
<tr><td>Vendita</td><td>Imposte atti, plusvalenza, documenti</td><td>AE, commercialista</td></tr>
</tbody>
</table>
<h2>Acquisto: privato vs costruttore nel Padovano</h2>
<p>Da <strong>privato</strong> in semicentro: imposta di registro su base catastale, spese notarili proporzionali al valore. Da <strong>costruttore</strong> a <strong>Vigodarzere</strong> o <strong>Cadoneghe</strong>: IVA agevolata prima casa se requisiti, garanzie post-consegna da verificare nel contratto. Dettaglio imposte: <a href="blog-quattro-imposte-rogitio-prima-casa-padova-2026">quattro imposte al rogito</a>.</p>
<h3>Mutuo e costo del capitale</h3>
<p>La Banca d'Italia pubblica dati su spread e condizioni credito; il TAEG include spese accessorie. Il costo del denaro va sommato al costo di possesso per famiglie che non acquistano cash.</p>""",
        "body_mid": """<h2>Possesso: IMU, TARI e condominio</h2>
<p>L'<strong>IMU</strong> si calcola secondo aliquote comunali e detrazioni previste — schede su <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a>. La <strong>TARI</strong> dipende dal Comune dell'immobile. Il <strong>condominio</strong> può superare entrambe in edifici con straordinarie programmate. Per gestione quotidiana: <a href="blog-gestione-spese-casa-risparmio-padova-2026">gestione spese casa</a>.</p>
<h2>Investimento locativo: costo netto</h2>
<p>Canone lordo meno IMU (se dovuta), spese condominiali non recuperabili, manutenzione, vacanza locativa e tassazione reddito. ISTAT e Banca d'Italia offrono contesto inflazione e affitti nazionali; OMI locazione resta riferimento semestrale per il Padovano.</p>
<h2>Vendita e plusvalenza</h2>
<p>La plusvalenza da immobili per persone fisiche fuori attività d'impresa è assoggettata, in regime ordinario, ad aliquota del <strong>26%</strong> su redditi diversi (verificare normativa e scadenze dichiarative vigenti). Esclusioni e riteggo su prezzo di acquisto, imposte pagate e lavori documentati: tema per commercialista, non per agenzia. Incrociare con <a href="blog-documenti-vendita-casa">documenti vendita</a> e <a href="blog-tasse-vendita-casa">tasse vendita</a>.</p>
<ul>
<li>Conservare fatture lavori e copia atto acquisto.</li>
<li>Valutare timing vendita vs carico fiscale (senza ottimizzazione aggressiva non consigliata).</li>
<li>Allineare prezzo vendita a comparabili OMI.</li>
</ul>""",
        "body_tail": """<h2>Scenario famiglia padovana: esempio strutturale (senza cifre inventate)</h2>
<p>Famiglia acquista trilocale in cintura, detiene dieci anni, vende per upsizing. Costi: imposte acquisto, dieci anni di IMU/TARI/condominio, manutenzione straordinaria tetto, imposte e plusvalenza in vendita, mediazione da concordare in mandato. Il guadagno netto dipende da prezzo acquisto/vendita e da detrazioni ammesse — non da formule generiche web.</p>
<h3>Seconda casa vs prima casa</h3>
<p>Seconda casa nel Padovano o sui Colli Euganei cambia IMU e aliquote acquisto. Pianificare prima del compromesso.</p>
<h2>Checklist documentale per ciclo completo</h2>
<ol>
<li>Cartella acquisto: atto, imposte pagate, perizia mutuo.</li>
<li>Cartella possesso: IMU, TARI, fatture lavori, assemblee condominiali.</li>
<li>Cartella vendita: APE aggiornato, certificazioni impianti, storico utenze.</li>
</ol>
<p>Righetto supporta <a href="servizio-vendita">vendita</a> e <a href="landing-valutazione">valutazione</a> con comparabili verificati; per fiscalità rimandiamo a professionisti abilitati.</p>
<div class="warn"><strong>Ispirazione editoriale:</strong> The Dream RE e blog simili descrivono cicli ownership/lifecycle; in Italia numeri e aliquote vanno sempre da AE e commercialista.</div>""",
        "sources": sources_table([
            ("IMU e tributi locali", "Agenzia delle Entrate", "Possesso e aliquote"),
            ("Plusvalenza e redditi diversi", "Agenzia delle Entrate — IRPEF", "Aliquota 26% regime ordinario"),
            ("Credito e spese famiglie", "Banca d'Italia", "Contesto mutuo"),
            ("Ciclo costi proprietà (ispirazione)", "The Dream RE — articoli", "Solo modello narrativo"),
        ]),
        "topic": "costi proprietà acquisto possesso vendita plusvalenza Padova",
        "anchors": [
            ("quattro imposte rogito", "blog-quattro-imposte-rogitio-prima-casa-padova-2026"),
            ("gestione spese casa", "blog-gestione-spese-casa-risparmio-padova-2026"),
        ],
        "body_n": 20,
        "faqs": [
            ("Quali costi dopo il rogito?", "IMU, TARI, condominio, utenze, manutenzione, assicurazione."),
            ("Plusvalenza sempre al 26%?", "Regime ordinario persone fisiche: 26% su redditi diversi — verificare esclusioni con commercialista."),
            ("Privato vs costruttore al acquisto?", "Imposte diverse: registro vs IVA; impatto su costo iniziale."),
            ("Come stimare costo totale detenzione?", "Sommare fasi con preventivi reali, non solo prezzo acquisto."),
            ("Righetto fa piani fiscali?", "No: affianchiamo compravendita; fiscalità a commercialista/notaio."),
            ("Dove trovo aliquote IMU Padova?", "Agenzia delle Entrate e delibere Comune di Padova / comune dell'immobile."),
        ],
        "related": [
            ("Quattro imposte rogito", "blog-quattro-imposte-rogitio-prima-casa-padova-2026"),
            ("Gestione spese casa", "blog-gestione-spese-casa-risparmio-padova-2026"),
            ("Tasse vendita casa", "blog-tasse-vendita-casa"),
        ],
        "cta_primary": ("Valutazione immobile", "landing-valutazione"),
        "cta_secondary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        "registry": {
            "titolo": "Costi proprietà Padova 2026: acquisto, possesso, vendita e plusvalenza 26%",
            "categoria": "Fisco",
            "tempo": 12,
            "contenuto": "Ciclo completo privato/costruttore, IMU, TARI e plusvalenza — guida pratica Padovano.",
            "evidenza": False,
            "emoji": "💶",
        },
    },
    {
        "filename": "blog-dieci-errori-acquisto-casa-padova-2026.html",
        "slug": "blog-dieci-errori-acquisto-casa-padova-2026",
        "img": "img/blog/blog-dieci-errori-acquisto-casa-padova-2026.webp",
        "bread": "Dieci errori acquisto casa",
        "section": "Guida acquirenti",
        "html_title": "Dieci errori da evitare nell'acquisto casa a Padova 2026 | Righetto",
        "og_title": "Cosa non fare quando compri casa nel Padovano: mutuo, visite, condominio",
        "schema_headline": "Dieci errori comuni nell'acquisto casa a Padova: pre-approvazione, perizia, debiti condominiali",
        "meta_desc": "Errori frequenti acquirenti padovani: senza pre-approvazione mutuo, saltare sopralluogo tecnico, ignorare debiti condominiali, timing sbagliato. Contesto Padova 2026.",
        "cat_badge": "Guida acquirenti",
        "alt_img": "Acquirente casa Padova — illustrazione editoriale errori comuni compravendita",
        "breadcrumb_tail": "Errori acquisto casa",
        "h1": "<strong>Dieci errori</strong> da evitare quando compri casa a Padova nel 2026",
        "cap_img": '<p class="cap-img">Immagine <strong>illustrativa</strong> — ispirazione editoriale da guide «cosa non fare»; verifiche tecniche e credito da <a href="https://www.bancaditalia.it" target="_blank" rel="noopener noreferrer">Banca d\'Italia</a> e prassi notarile.</p>',
        "aeo": aeo_box(
            "Per <strong>acquirenti nel Padovano</strong> alla prima o seconda compravendita che vogliono evitare errori ricorrenti emersi in trattative reali.",
            [
                "Firmare offerte senza <strong>pre-approvazione mutuo</strong> o indicazione bancaria.",
                "Saltare <strong>seconda visita</strong> o sopralluogo tecnico su immobili datati.",
                "Ignorare <strong>debiti condominiali</strong> e straordinarie del venditore.",
                "Sottovalutare <strong>timing</strong> (delibera mutuo, rogito, clausole sospensive).",
            ],
            [
                "Non è lista moralistica: ogni errore ha conseguenza economica documentabile.",
                "Non copre tutte le casistiche giuridiche.",
                "Non sostituisce due diligence legale su casi complessi.",
            ],
        ),
        "body_extra": """<h2>Perché un elenco di errori (e non di consigli generici)</h2>
<p>Guide lifestyle tipo «dieci cose da non fare» in edilizia spesso mescolano gusto personale e sicurezza. Qui mappiamo <strong>errori con costo</strong> osservati nel mercato padovano: caparre perse, mutui negati, straordinarie condominiali scoperte al rogito, difformità che bloccano volture. I dati su credito dalla Banca d'Italia confermano selettività bancaria: preparazione non è optional.</p>
<h2>Tabella dieci errori e conseguenze</h2>
<table>
<thead><tr><th>#</th><th>Errore</th><th>Conseguenza tipica Padova</th></tr></thead>
<tbody>
<tr><td>1</td><td>Offerta senza pre-approvazione mutuo</td><td>Caparra a rischio, venditore preferisce altro acquirente</td></tr>
<tr><td>2</td><td>Una sola visita di giorno</td><td>Rumore notturno o buio non percepiti (es. vicino ferrovia)</td></tr>
<tr><td>3</td><td>Nessun tecnico su impianti datati</td><td>Preventivi post-rogito da migliaia di euro</td></tr>
<tr><td>4</td><td>Non chiedere bilancio condominiale</td><td>Spese straordinarie imminenti</td></tr>
<tr><td>5</td><td>Ignorare debiti venditore verso condominio</td><td>Art. 63 disp. att. c.c. — recupero da acquirente</td></tr>
<tr><td>6</td><td>Compromesso senza clausola sospensiva mutuo</td><td>Penali se finanziamento negato</td></tr>
<tr><td>7</td><td>Non verificare planimetria vs stato di fatto</td><td>Sanatoria e mutuo bloccato</td></tr>
<tr><td>8</td><td>Timing rogito vs scadenza delibera</td><td>Delibera mutuo scaduta, nuova perizia</td></tr>
<tr><td>9</td><td>Fidarsi solo del prezzo in annuncio</td><td>Offerta fuori mercato, mesi persi</td></tr>
<tr><td>10</td><td>Tralasciare APE e classe energetica</td><td>Costi energia e perizia bancaria severa</td></tr>
</tbody>
</table>""",
        "body_mid": """<h2>Errori 1-3: credito e percezione immobile</h2>
<p><strong>Pre-approvazione:</strong> nel Padovano, venditori in mercato con stock contenuto preferiscono acquirenti bancabili. CRIF segnala domanda mutui variabile — vedi barometro mutui sul blog. <strong>Visite:</strong> centro storico e ZTL hanno ritmi diversi da cintura; visitare sera e weekend. <strong>Tecnico:</strong> edifici anni '60 a <strong>Saonara</strong> e <strong>Maserà di Padova</strong> spesso hanno impianti non certificati.</p>
<h2>Errori 4-6: condominio e contratto</h2>
<p>Richiedere certificazione amministratore su assenza debiti del venditore e delibere straordinarie. Il compromesso deve prevedere <strong>clausola sospensiva</strong> mutuo e verifica titoli. Per caparra: <a href="blog-caparra-confirmatoria-padova">caparra confirmatoria Padova</a>.</p>
<h2>Errori 7-10: documenti, tempo, mercato</h2>
<p>Planimetria catastale e conformità urbanistica — <a href="blog-planimetria-catastale-compravendita-padova-2026">planimetria compravendita</a>. Allineare calendario rogito con banca. Confrontare prezzo con OMI e venduti, non solo con annunci aspirazionali. APE classe G in zone dove comparabili sono D: sconto o lavori.</p>
<p>Prima di procedere: <a href="blog-mutuo-prima-casa-padova">mutuo prima casa</a>, <a href="blog-scegliere-immobile-giusto-padova-2026">scegliere immobile</a>, <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a>.</p>""",
        "body_tail": """<h2>Contesto Padova 2026</h2>
<p>Mercato con trattative attive ma banche selettive: l'errore «offerta emozionale» costa più che in anni di credito largo. Università e sanità sostengono domanda su certi micro-segmenti; non giustifica prezzo fuori banda OMI.</p>
<h3>Errore bonus: sottovalutare la mediazione utile</h3>
<p>Rifiutare accompagnamento professionale per «risparmiare commissione» può significare perdere verifiche su titoli e negoziazione prezzo. I compensi di mediazione sono da concordare in mandato, non da listini web.</p>
<h2>Sequenza anti-errore consigliata</h2>
<ol>
<li>Pre-approvazione e budget totale (acquisto + lavori + imposte).</li>
<li>Selezione microzone e comparabili.</li>
<li>Visite ripetute + checklist tecnica.</li>
<li>Offerta con clausole sospensive corrette.</li>
<li>Due diligence documentale pre-rogito.</li>
</ol>
<p>Righetto affianca acquirenti nel <strong>Padovano</strong> con metodo documentato, senza promettere «casa perfetta».</p>
<div class="warn"><strong>Ispirazione:</strong> articoli tipo Casaegiardino «10 cose da non fare» — adattati al contesto fiscale e urbanistico padovano.</div>""",
        "sources": sources_table([
            ("Credito ipotecario", "Banca d'Italia — indagini mutui", "Selettività e LTV"),
            ("Debiti condominiali", "Codice Civile — disp. att.", "Trasferimento obblighi"),
            ("Quotazioni", "OMI — Agenzia delle Entrate", "Pricing realistico"),
            ("Errori comuni (ispirazione)", "Casaegiardino — guide editoriali", "Solo struttura elenco"),
        ]),
        "topic": "errori acquisto casa evitare Padova acquirenti",
        "anchors": [
            ("mutuo prima casa", "blog-mutuo-prima-casa-padova"),
            ("checklist compromesso", "blog-checklist-verifiche-prima-compromesso-padova-2026"),
        ],
        "body_n": 24,
        "faqs": [
            ("Qual è l'errore più costoso?", "Spesso compromesso senza clausola sospensiva mutuo o ignorare difformità urbanistiche."),
            ("Devo sempre fare seconda visita?", "Fortemente consigliato, a orari diversi, su immobili che vi piacciono."),
            ("Debiti condominiali del venditore?", "L'acquirente può essere chiamato a pagarli — verificare certificazione."),
            ("Pre-approvazione basta?", "È un passo; serve allineare perizia e tempi delibera."),
            ("Posso correggere dopo l'errore?", "A volte con penali o rinegoziazione; meglio prevenire in due diligence."),
            ("Righetto protegge da tutti gli errori?", "Riduciamo rischi operativi; decisioni e obblighi restano dell'acquirente."),
        ],
        "related": [
            ("Scegliere immobile giusto", "blog-scegliere-immobile-giusto-padova-2026"),
            ("Checklist pre-compromesso", "blog-checklist-verifiche-prima-compromesso-padova-2026"),
            ("Mutuo prima casa", "blog-mutuo-prima-casa-padova"),
        ],
        "cta_primary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        "cta_secondary": ("Calcolo mutuo", "landing-chat-calcolo-mutuo"),
        "registry": {
            "titolo": "Dieci errori da evitare nell'acquisto casa a Padova 2026",
            "categoria": "Guida acquirenti",
            "tempo": 11,
            "contenuto": "Pre-approvazione, visite, condominio, timing: errori con costo nel Padovano.",
            "evidenza": False,
            "emoji": "⚠️",
        },
    },
    {
        "filename": "blog-checklist-verifiche-prima-compromesso-padova-2026.html",
        "slug": "blog-checklist-verifiche-prima-compromesso-padova-2026",
        "img": "img/blog/blog-checklist-verifiche-prima-compromesso-padova-2026.webp",
        "bread": "Checklist prima del compromesso",
        "section": "Normativa",
        "html_title": "Checklist verifiche prima del compromesso a Padova 2026: documenti, impianti, mutuo | Righetto",
        "og_title": "Cosa verificare prima di firmare il preliminare nel Padovano",
        "schema_headline": "Checklist tecnica e documentale prima del compromesso di compravendita a Padova",
        "meta_desc": "Verifiche pre-offerta e pre-compromesso: documenti, impianti, struttura, mutuo, conformità catastale. Checklist tecnica per acquirenti padovani — normativa e prassi.",
        "cat_badge": "Normativa",
        "alt_img": "Checklist documenti compravendita — illustrazione editoriale verifiche pre-compromesso Padova",
        "breadcrumb_tail": "Checklist pre-compromesso",
        "h1": "<strong>Checklist verifiche</strong> prima del compromesso a Padova: documenti, impianti e mutuo",
        "cap_img": '<p class="cap-img">Immagine <strong>illustrativa</strong> su due diligence — ispirazione Immobiliare Cavallo; normativa da <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a> e prassi notarile.</p>',
        "aeo": aeo_box(
            "Per <strong>acquirenti e venditori nel Padovano</strong> che devono firmare un preliminare e vogliono una lista di verifiche tecniche e documentali ordinata.",
            [
                "<strong>Documenti:</strong> APE, planimetria, visure, certificazioni impianti.",
                "<strong>Struttura e impianti:</strong> infiltrazioni, conformità elettrico/idraulico.",
                "<strong>Mutuo:</strong> clausola sospensiva, perizia, scadenze delibera.",
                "<strong>Condominio:</strong> assenza debiti, regolamento, straordinarie.",
            ],
            [
                "Non è modello di contratto sostitutivo del notaio.",
                "Non copre compravendite con società e trust complessi.",
                "Non garantisce esito positivo mutuo.",
            ],
        ),
        "body_extra": """<h2>Perché verificare prima del compromesso</h2>
<p>Il <strong>compromesso</strong> (preliminare) vincola le parti su prezzo, caparra e tempi. Dopo la firma, uscire costa penali. Le checklist di studi tecnici — ispirate a modelli come quelli di Immobiliare Cavallo — vanno adattate al contesto padovano: condominio spesso con straordinarie, centro storico con vincoli, cintura con nuovo e seconda mano misti.</p>
<h2>Checklist documenti (tabella)</h2>
<table>
<thead><tr><th>Documento</th><th>Cosa controllare</th><th>Rischio</th></tr></thead>
<tbody>
<tr><td>APE</td><td>Validità, classe, dati coerenti con impianti</td><td>Perizia bancaria, obblighi futuri</td></tr>
<tr><td>Planimetria catastale</td><td>Corrispondenza con stato di fatto</td><td>Sanatoria, mutuo</td></tr>
<tr><td>Visura catastale</td><td>Intestatari, rendita, categorie</td><td>Contenzioso vendita</td></tr>
<tr><td>Titoli edilizi / agibilità</td><td>Permessi storici, CILA in corso</td><td>Difformità urbanistiche</td></tr>
<tr><td>Certificazioni impianti</td><td>Data, conformità DM 37/2008</td><td>Obbligo adeguamento</td></tr>
<tr><td>Condominio</td><td>Certificazione debiti, ultimo bilancio</td><td>Recupero crediti</td></tr>
</tbody>
</table>
<p>Dettaglio rogito: <a href="blog-documenti-compravendita-rogito-padova-2026">documenti compravendita</a> e <a href="blog-documenti-vendita-casa">documenti vendita</a>.</p>""",
        "body_mid": """<h2>Verifiche strutturali e impiantistiche</h2>
<p>Sopralluogo tecnico su: umidità cantina e facciate, funzionamento caldaia e climatizzazione, quadro elettrico, pressione idraulica, finestre e isolamento acustico verso vie trafficate (comune in <strong>corso Milano</strong> o <strong>via Venezia</strong>). A norma, impianti devono rispettare regolamenti vigenti; certificazioni rilasciate da professionisti abilitati.</p>
<h2>Mutuo: clausole del compromesso</h2>
<ul>
<li>Clausola sospensiva con importo minimo finanziamento e scadenza delibera.</li>
<li>Penale caparra limitata se mutuo negato per causa non imputabile all'acquirente.</li>
<li>Allineamento prezzo a valore perizia stimato.</li>
<li>Tempi rogito coerenti con validità delibera bancaria.</li>
</ul>
<p>Approfondimento: <a href="blog-mutuo-prima-casa-padova">mutuo prima casa Padova</a> e <a href="blog-mutuo-documenti-tempi-prima-casa-padova-2026">documenti e tempi mutuo</a>.</p>
<h2>Condominio e regolamento</h2>
<p>Leggere regolamento su modifiche interne, affitti brevi, animali. Verificare fondo lavori per straordinarie approvate. In edifici UNESCO o centro antico, vincoli aggiuntivi su facciate e infissi.</p>""",
        "body_tail": """<h2>Sequenza temporale consigliata</h2>
<ol>
<li>Prima visita e filtro prezzo/OMI.</li>
<li>Richiesta documenti base al venditore (APE, planimetria, condominio).</li>
<li>Seconda visita + eventuale tecnico.</li>
<li>Pre-approvazione bancaria indicativa.</li>
<li>Offerta o proposta con condizioni sospensive.</li>
<li>Compromesso redatto da notaio o avvocato.</li>
</ol>
<h3>Venditore: preparare il pacchetto</h3>
<p>Anticipare documenti riduce tempo e rafforza prezzo richiesto. Vedi <a href="blog-documenti-vendita-casa">checklist venditore</a> e <a href="servizio-preliminari">servizio preliminari</a> Righetto.</p>
<h2>Padova: attenzioni locali</h2>
<p><strong>Zone alluvionabili</strong> e <strong>vincoli paesaggistici</strong> in alcune aree della provincia richiedono verifiche idrauliche e autorizzazioni storiche. <strong>ZTL</strong> e parcheggio incidono su attrattiva ma non su legittimità titoli — distinguere marketing da normativa.</p>
<p>Per accompagnamento: <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a>. Evitare errori comuni: <a href="blog-dieci-errori-acquisto-casa-padova-2026">dieci errori acquisto</a>.</p>
<div class="warn"><strong>Nota:</strong> checklist Immobiliare Cavallo e simili sono ispirazione metodologica; ogni compravendita richiede adattamento e pareri professionali.</div>""",
        "sources": sources_table([
            ("Catasto e planimetrie", "Agenzia delle Entrate — catasto", "Visure e conformità"),
            ("Impianti termici/elettrici", "DM 37/2008 e norme tecniche", "Certificazioni"),
            ("Compromesso e caparra", "Codice Civile", "Obblighi parti"),
            ("Checklist tecnica (ispirazione)", "Immobiliare Cavallo — guide", "Solo modello operativo"),
        ]),
        "topic": "checklist verifiche documenti impianti prima compromesso Padova",
        "anchors": [
            ("documenti compravendita", "blog-documenti-compravendita-rogito-padova-2026"),
            ("dieci errori acquisto", "blog-dieci-errori-acquisto-casa-padova-2026"),
        ],
        "body_n": 22,
        "faqs": [
            ("Quando serve il tecnico?", "Prima del compromesso su immobili con impianti datati o dubbi strutturali."),
            ("Cosa deve dare il venditore?", "APE, planimetria, visura, certificazioni impianti, certificazione condominio."),
            ("Clausola sospensiva mutuo obbligatoria?", "Fortemente consigliata per acquirenti finanziati."),
            ("Planimetria non conforme: che fare?", "Valutare sanatoria, costi e clausola risolutiva prima di firmare."),
            ("Chi redige il compromesso?", "Notaio o avvocato; evitare modelli generici non adattati."),
            ("Righetto fa due diligence legale?", "Supportiamo raccolta documenti e coordinamento; pareri legali a specialisti."),
        ],
        "related": [
            ("Documenti al rogito", "blog-documenti-compravendita-rogito-padova-2026"),
            ("Dieci errori acquisto", "blog-dieci-errori-acquisto-casa-padova-2026"),
            ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        ],
        "cta_primary": ("Supporto preliminare", "servizio-preliminari"),
        "cta_secondary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        "registry": {
            "titolo": "Checklist verifiche prima del compromesso a Padova 2026",
            "categoria": "Normativa",
            "tempo": 12,
            "contenuto": "Documenti, impianti, struttura e mutuo: due diligence pre-preliminare nel Padovano.",
            "evidenza": False,
            "emoji": "✅",
        },
    },
]


def registry_entries(cfg: dict) -> dict:
    reg = cfg["registry"]
    img = cfg["img"]
    slug = cfg["slug"]
    base = {
        "titolo": reg["titolo"],
        "categoria": reg["categoria"],
        "data": DATE_ISO,
        "stato": "pubblicato",
        "immagine_copertina": img,
        "url_statico": slug,
    }
    blog_html = {
        **base,
        "tempo": reg["tempo"],
        "autore": "Gino Capon",
        "contenuto": reg["contenuto"],
        "evidenza": reg["evidenza"],
    }
    admin = {
        **blog_html,
        "emoji": reg["emoji"],
        "contenuto": f"<p>{reg['contenuto']}</p>",
        "data_pubblicazione": DATE_ISO,
    }
    homepage = {k: v for k, v in base.items()}
    return {"blog_html": blog_html, "admin": admin, "homepage": homepage}


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    results: list[dict] = []
    registry = {
        "generated": DATE_ISO,
        "date_display": DATE_IT,
        "files": [],
        "blog_html_articoliStatici": [],
        "admin_blogSeedArticles": [],
        "homepage_js_articoliStatici": [],
    }

    for cfg in ARTICLES:
        html, wc = build_article(cfg)
        out_path = root / cfg["filename"]
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        entries = registry_entries(cfg)
        registry["files"].append({"filename": cfg["filename"], "slug": cfg["slug"], "wordCount_body": wc})
        registry["blog_html_articoliStatici"].append(entries["blog_html"])
        registry["admin_blogSeedArticles"].append(entries["admin"])
        registry["homepage_js_articoliStatici"].append(entries["homepage"])
        results.append({"file": cfg["filename"], "slug": cfg["slug"], "words": wc})
        print(f"OK {cfg['filename']} — wordCount corpo: {wc}")

    reg_path = root / "scripts" / "giugno03_blog_registry.json"
    with open(reg_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("\n--- Registry JSON ---")
    try:
        print(json.dumps(registry, ensure_ascii=False, indent=2))
    except UnicodeEncodeError:
        print(json.dumps(registry, ensure_ascii=True, indent=2))
    print(f"\nScritti {len(results)} articoli + {reg_path.relative_to(root)}")


if __name__ == "__main__":
    main()
