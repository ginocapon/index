# -*- coding: utf-8 -*-
"""Genera 5 articoli blog 27 maggio 2026 — Righetto. Esegui da repo root:
python scripts/build_may27_blog_batch.py
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

DATE_IT = "27 maggio 2026"
DATE_ISO = "2026-05-27"
TIME_TS = "2026-05-27T10:00:00+02:00"
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
<script src="js/rig-lead-form.js?v=1"></script>
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
        "filename": "blog-sondaggio-bancaditalia-q1-2026-padova.html",
        "slug": "blog-sondaggio-bancaditalia-q1-2026-padova",
        "img": "img/blog/blog-sondaggio-bancaditalia-q1-2026.webp",
        "bread": "Sondaggio Banca d'Italia Q1 2026",
        "section": "Mercato immobiliare",
        "html_title": "Sondaggio abitativo Banca d'Italia Q1 2026: LTV 77,2% e mutuo al 64,5% | Padova",
        "og_title": "Sondaggio abitativo Q1 2026: mutui, tempi di vendita e sconti",
        "schema_headline": "Sondaggio abitativo Banca d'Italia Q1 2026: lettura per acquirenti e venditori nel Padovano",
        "meta_desc": "Comunicato Banca d'Italia maggio 2026: LTV 77,2%, 64,5% acquisti con mutuo, 5,2 mesi vendita, 7,3% sconto. Applicazione al territorio patavino.",
        "cat_badge": "Mercato immobiliare",
        "alt_img": "Grafici e dati abitativi — illustrazione editoriale sondaggio credito e mercato casa Italia",
        "breadcrumb_tail": "Sondaggio Banca d'Italia",
        "h1": "<strong>Sondaggio abitativo</strong> Q1 2026: mutui, tempi di vendita e affitti nel contesto padovano",
        "cap_img": '<p class="cap-img">Immagine <strong>illustrativa</strong> su dati e mercato abitativo — non riproduce tabelle ufficiali della Banca d\'Italia. I numeri citati provengono dal comunicato stampa di maggio 2026.</p>',
        "aeo": aeo_box(
            "Per famiglie e investitori del <strong>Padovano</strong> che vogliono tradurre il <a href=\"https://www.bancaditalia.it/media/comunicati-stampa/2026/index.html\" target=\"_blank\" rel=\"noopener noreferrer\">sondaggio abitativo</a> del primo trimestre 2026 in scelte concrete su mutuo, prezzo richiesto e tempi di vendita.",
            [
                "Nel Q1 2026 il <strong>loan-to-value (LTV) medio</strong> sui mutui per acquisto abitativo è <strong>77,2%</strong> (Banca d'Italia, maggio 2026).",
                "Circa il <strong>64,5%</strong> degli acquisti di abitazioni usa il mutuo ipotecario.",
                "Il tempo medio di vendita è <strong>5,2 mesi</strong>; lo sconto medio sulla richiesta iniziale è <strong>7,3%</strong>.",
                "Gli <strong>affitti</strong> crescono, ma con ritmo più contenuto rispetto ai prezzi di vendita.",
            ],
            [
                "Non è una perizia bancaria né una stima del valore del singolo immobile.",
                "Non sostituisce l'offerta mutuo firmata in filiale.",
                "Non promette tempi o sconti identici al dato nazionale sul micro-mercato padovano.",
            ],
        ),
        "body_extra": """<h2>Cosa misura il sondaggio abitativo</h2>
<p>La <a href="https://www.bancaditalia.it" target="_blank" rel="noopener noreferrer">Banca d'Italia</a> pubblica periodicamente un sondaggio sul mercato delle abitazioni che interroga banche, costruttori, agenzie immobiliari e famiglie. Il questionario del <strong>primo trimestre 2026</strong>, diffuso con comunicato stampa a <strong>maggio 2026</strong>, offre una fotografia aggregata su credito, transazioni e aspettative. È un termometro nazionale: va incrociato con OMI, osservatori locali e comparabili reali prima di fissare prezzo o budget.</p>
<p>In agenzia, usiamo questi indicatori come <em>contesto</em>, non come promessa. Un LTV medio del 77,2% segnala che le banche finanziano in media una quota elevata del valore di perizia, ma la singola pratica può chiudersi molto più bassa se reddito, classe energetica o difformità urbanistiche aumentano il rischio percepito.</p>
<h2>Tabella sintetica Q1 2026 (fonte Banca d'Italia)</h2>
<table>
<thead><tr><th>Indicatore</th><th>Valore Q1 2026</th><th>Lettura per il Padovano</th></tr></thead>
<tbody>
<tr><td>LTV medio mutui acquisto abitativo</td><td><strong>77,2%</strong></td><td>Anticipo tipico intorno al 23% del valore periziato — verificare caso per caso</td></tr>
<tr><td>Acquisti con mutuo</td><td><strong>64,5%</strong></td><td>Due compratori su tre usano credito: istruttoria tempestiva è strategica</td></tr>
<tr><td>Tempo medio di vendita</td><td><strong>5,2 mesi</strong></td><td>Benchmark nazionale; trilocali ristrutturati in cintura possono essere più rapidi</td></tr>
<tr><td>Sconto medio su prezzo richiesto</td><td><strong>7,3%</strong></td><td>Trattativa frequente: prezzo iniziale realistico riduce stress</td></tr>
<tr><td>Affitti vs vendita</td><td>affitti in crescita più lenta</td><td>Utile per investitori locativi nel campus e in cintura</td></tr>
</tbody>
</table>
<p><em>Fonte: comunicato stampa Banca d'Italia, maggio 2026, sondaggio abitativo Q1 2026.</em></p>
<h2>Mutuo al 64,5%: implicazioni pratiche</h2>
<p>Quando quasi due terzi degli acquisti passa dal mutuo, la qualità della <strong>documentazione</strong> e l'allineamento tra prezzo concordato e perizia diventano centrali. Nel territorio patavino — da <strong>Limena</strong> al centro storico di Padova — osserviamo acquirenti che arrivano con pre-approvazione ma slittano per difformità catastali o APE non aggiornati. Per orientarsi sui documenti, rimandiamo a <a href="blog-mutuo-documenti-tempi-prima-casa-padova-2026">documenti mutuo prima casa</a> e alla <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a>.</p>
<h3>LTV e anticipo: cosa chiedere in banca</h3>
<p>Un LTV medio del 77,2% non garantisce lo stesso rapporto su ogni immobile. Chiedere esplicitamente: massimale finanziabile sulla perizia, eventuali polizze obbligatorie, impatto del TAEG sulla rata. Incrociare con <a href="blog-barometro-mutui-crif-padova-2026">domanda mutui CRIF</a> e con l'articolo sui <a href="blog-mutui-selettivi-banche-padova-2026">mutui selettivi</a> completa il quadro senza promesse.</p>""",
        "body_mid": """<h2>Tempi di vendita: 5,2 mesi come riferimento</h2>
<p>Cinque mesi e poco più di due settimane è la media nazionale citata dal sondaggio. A Padova, la dispersione è ampia: monolocali da riqualificare in periferia possono superare la media, mentre trilocali energetici in <strong>Albignasego</strong> o <strong>Cadoneghe</strong> possono chiudersi più rapidamente se il prezzo è allineato a comparabili venduti. Il venditore dovrebbe monitorare giorni online, numero visite qualificate e feedback scritti, non solo il dato macro.</p>
<h3>Sconto medio 7,3%: trattativa o debolezza?</h3>
<p>Lo sconto medio non è una regola automatica: indica che molte trattative partono da prezzi richiesti superiori al valore percepito dal mercato. In pratica, un venditore che posiziona l'immobile +10% sopra i comparabili reali spesso converge verso quella forbice. Meglio uscire credibili e negoziare su dettagli (mobili, data rogito) piuttosto che subire un taglio tardivo quando l'acquirente ha alternative limitate ma budget teso.</p>
<h2>Affitti in crescita più lenta: effetto su investimento</h2>
<p>Il comunicato segnala che gli affitti continuano a salire, ma con ritmo inferiore ai prezzi di vendita. Per chi valuta buy-to-let nel Padovano — vicinanza università, ospedali, Mestre-Venezia — conviene calcolare rendimento netto realistico: IMU dove dovuta, spese condominiali, vacanza locativa, manutenzione. Le OMI locazione restano il riferimento semestrale; per un incrocio metodologico vedi <a href="blog-quotazioni-locazioni-omi-istat-padova-2026">OMI e ISTAT nel Padovano</a>.</p>
<h2>Micro-mercato padovano: tre domande da porsi</h2>
<ul>
<li>Il mio segmento (centro, cintura, collina) ha stock e domanda coerenti con la media nazionale su mutuo e tempi?</li>
<li>La mia banca applica LTV simile al 77,2% o policy più prudente su classe energetica G/F?</li>
<li>Ho comparabili venduti negli ultimi sei mesi per giustificare prezzo richiesto e sconto atteso?</li>
</ul>
<p>In conclusione, il sondaggio Banca d'Italia Q1 2026 conferma un mercato ancora sostenuto dal credito, con trattative che lasciano spazio allo sconto e tempi di vendita non immediati. Chi opera nel Padovano beneficia di tradurre questi numeri in checklist documentale e pricing, non in slogan. Righetto affianca venditori e acquirenti con <a href="servizio-vendita">vendita</a>, <a href="landing-valutazione">valutazioni</a> e report comparabili verificati sul campo.</p>
<div class="warn"><strong>Nota metodologica:</strong> il sondaggio aggrega risposte nazionali; non sostituisce osservazioni FIMAP/FIAIP o transazioni locali.</div>""",
        "sources": sources_table([
            ("LTV e mutui abitativi", "Banca d'Italia — sondaggio Q1 2026", "Contesto finanziamento, non offerta singola"),
            ("Tempi vendita e sconti", "Banca d'Italia — comunicato maggio 2026", "Benchmark trattativa"),
            ("Quotazioni microzona", "OMI — Agenzia delle Entrate", "Bande semestrali per comune/quartiere"),
            ("Affitti e contesto famiglie", "ISTAT", "Inflazione e costo della vita"),
        ]),
        "topic": "sondaggio abitativo Banca d'Italia Q1 2026",
        "anchors": [
            ("mutui selettivi Padova", "blog-mutui-selettivi-banche-padova-2026"),
            ("prezzi città vs provincia", "blog-prezzi-padova-provincia-fiaip-2026"),
        ],
        "body_tail": """<h2>Segmenti del mercato padovano: chi sente di più il dato Banca d'Italia</h2>
<p>La prima casa nel <strong>semicentro</strong> resta il segmento dove mutuo e tempi di vendita incidono con forza: famiglie giovani con anticipo limitato sfruttano LTV elevati solo se perizia e reddito reggono verifica. In <strong>seconda casa</strong> o investimento locativo studenti, la quota cash è spesso superiore alla media del 64,5%: meno dipendenza dal credito, più sensibilità a rendimento netto e regime fiscale. I venditori di ville in <strong>Colli Euganei</strong> o Abano Terme devono invece considerare acquirenti misti (residenti e fuori regione) con profili bancari diversi: un unico prezzo richiesto non cattura tutte le fasce.</p>
<h3>Domanda universitaria e locazione breve</h3>
<p>Padova traina flussi di affitto legati all'università. Il segnale «affitti in crescita più lenta» non significa mercato debole: può indicare allineamento dopo anni di forte run-up. Chi compra per locare deve incrociare canoni osservati, spese e vacanza con OMI locazione, non solo il titolo del comunicato Banca d'Italia. Per vendita post-locazione, tempi di 5,2 mesi restano riferimento utile se l'immobile è libero e documentato.</p>
<h2>Scenario acquirente: sequenza consigliata</h2>
<p>In primo luogo, definire budget massimo e ottenere indicazione bancaria non vincolante. Successivamente, selezionare due o tre comuni target (es. Limena, Saonara, Ponte San Nicolò) e comparabili reali. Parallelamente, verificare stato impianti e APE prima dell'offerta vincolante. D'altra parte, il venditore dovrebbe allineare prezzo richiesto tenendo conto dello sconto medio osservato a livello nazionale, senza assumere che ogni trattativa debba chiudersi esattamente al -7,3%. In agenzia, accompagniamo entrambe le parti con report settimanali e checklist condivise con notaio quando serve.</p>
<h2>Domande da porre in consulenza (senza numeri inventati)</h2>
<p>Quanti comparabili venduti negli ultimi sei mesi giustificano il mio prezzo? La banca finanzia il mio LTV target su questa classe energetica? Quale margine di sconto è realistico senza perdere acquirenti qualificati? Risposte dipendono da microzona, non da medie nazionali. Per approfondire il contesto prezzi locale, rimandiamo a <a href="blog-prezzi-padova-provincia-fiaip-2026">FIAIP Padova</a> e a <a href="blog-offerta-stock-vendita-italia-2026">stock annunci 2026</a>.</p>""",
        "body_n": 24,
        "faqs": [
            ("Cosa significa LTV 77,2%?", "Indica che il mutuo medio copre circa il 77% del valore periziato; l'anticipo effettivo dipende da banca, reddito e immobile."),
            ("Il 64,5% con mutuo vale anche a Padova?", "È una media nazionale del sondaggio: nel Padovano la quota può variare per segmento e prezzo."),
            ("5,2 mesi garantiscono la vendita?", "No: è una media; qualità energetica, prezzo e documentazione cambiano i tempi."),
            ("Perché lo sconto medio è 7,3%?", "Molte trattative partono da prezzi richiesti sopra il valore percepito; uno sconto in linea è frequente."),
            ("Dove trovo il comunicato ufficiale?", "Sul sito Banca d'Italia, sezione comunicati stampa maggio 2026 sul sondaggio abitativo Q1."),
            ("Righetto eroga mutui?", "No: supportiamo la parte immobiliare; per prodotti creditizi rivolgersi a banche autorizzate."),
        ],
        "related": [
            ("Barometro mutui CRIF 2026", "blog-barometro-mutui-crif-padova-2026"),
            ("Mutui selettivi Padova", "blog-mutui-selettivi-banche-padova-2026"),
            ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        ],
        "cta_primary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        "cta_secondary": ("Valutazione immobile", "landing-valutazione"),
        "registry": {
            "titolo": "Sondaggio abitativo Banca d'Italia Q1 2026: LTV 77,2% e mutuo al 64,5%",
            "categoria": "Mercato immobiliare",
            "tempo": 12,
            "contenuto": "Comunicato maggio 2026: tempi vendita 5,2 mesi, sconto 7,3%, affitti in crescita più lenta.",
            "evidenza": True,
            "emoji": "🏦",
        },
    },
    {
        "filename": "blog-costi-costruzione-istat-padova-2026.html",
        "slug": "blog-costi-costruzione-istat-padova-2026",
        "img": "img/blog/blog-costi-costruzione-istat-padova-2026.webp",
        "bread": "Costi costruzione ISTAT 2026",
        "section": "Mercato immobiliare",
        "html_title": "Costi costruzione ISTAT marzo 2026: +0,8% mensile, indice 117,2 | Padova",
        "og_title": "Costi costruzione in aumento: lettura ISTAT per il Padovano",
        "schema_headline": "Costi di costruzione ISTAT marzo 2026: impatto su ristrutturazioni e nuovo nel Padovano",
        "meta_desc": "ISTAT marzo 2026: costi costruzione +0,8% mensile, +1,6% annuo; Q1 edilizia residenziale +0,7%; indice 117,2 febbraio 2026. Lettura per ristrutturazioni a Padova.",
        "cat_badge": "Mercato immobiliare",
        "alt_img": "Cantiere edile e materiali — illustrazione editoriale costi costruzione e indice ISTAT",
        "breadcrumb_tail": "Costi costruzione ISTAT",
        "h1": "<strong>Costi di costruzione</strong> in risalita: cosa significa per chi ristruttura o compra nuovo a Padova",
        "cap_img": '<p class="cap-img">Foto <strong>illustrativa</strong> di cantiere — non documenta un progetto Righetto. Dati da <a href="https://www.istat.it" target="_blank" rel="noopener noreferrer">ISTAT</a>, comunicato costi costruzione marzo 2026.</p>',
        "aeo": aeo_box(
            "Per proprietari nel <strong>Padovano</strong> che stanno budgettando ristrutturazioni, ampliamenti o acquisto in nuova costruzione e vogliono ancorare i preventivi ai dati ufficiali.",
            [
                "A <strong>marzo 2026</strong> i costi di costruzione crescono del <strong>+0,8%</strong> su base mensile e del <strong>+1,6%</strong> su base annua (ISTAT).",
                "Nel <strong>Q1 2026</strong> l'edilizia residenziale registra <strong>+0,7%</strong> su base trimestrale.",
                "L'indice per l'edilizia residenziale era <strong>117,2</strong> a febbraio 2026 (base 2015=100).",
            ],
            [
                "Non è un preventivo di impresa per il singolo appartamento.",
                "Non indica automaticamente quanto salirà il prezzo di vendita del vostro immobile.",
                "Non sostituisce computi metrici e capitolati firmati con imprese qualificate.",
            ],
        ),
        "body_extra": """<h2>Perché monitorare l'indice ISTAT</h2>
<p>L'<a href="https://www.istat.it/it/archivio/costi-di-costruzione" target="_blank" rel="noopener noreferrer">indice dei costi di costruzione</a> misura l'evoluzione di materiali, manodopera e oneri per opere edili. A <strong>marzo 2026</strong> la variazione mensile è <strong>+0,8%</strong> e quella tendenziale annua <strong>+1,6%</strong>. Nel primo trimestre, il comparto <strong>edilizia residenziale</strong> avanza del <strong>+0,7%</strong>. L'indice per le abitazioni era a <strong>117,2</strong> a febbraio 2026 (base 2015=100): significa che i costi sono circa il 17% superiori rispetto alla base decennale, prima di ulteriori incrementi 2026.</p>
<h2>Tabella indicatori ISTAT (estratto marzo 2026)</h2>
<table>
<thead><tr><th>Indicatore</th><th>Variazione</th><th>Riferimento temporale</th></tr></thead>
<tbody>
<tr><td>Costi costruzione (generale)</td><td><strong>+0,8%</strong> m/m</td><td>Marzo 2026</td></tr>
<tr><td>Costi costruzione (generale)</td><td><strong>+1,6%</strong> a/a</td><td>Marzo 2026</td></tr>
<tr><td>Edilizia residenziale</td><td><strong>+0,7%</strong> trimestrale</td><td>Q1 2026</td></tr>
<tr><td>Indice edilizia residenziale</td><td><strong>117,2</strong></td><td>Febbraio 2026 (2015=100)</td></tr>
</tbody>
</table>
<p><em>Fonte: ISTAT, nota costi di costruzione, marzo 2026.</em></p>
<h2>Ristrutturazione vs nuovo: due budget diversi</h2>
<p>Chi ristruttura un appartamento in condominio a <strong>Padova centro</strong> affronta voci diverse da chi compra una unità in nuova costruzione a <strong>Vigodarzere</strong> o in collina. L'indice ISTAT cattura pressioni su acciaio, isolamento, impianti e manodopera specializzata. In pratica, preventivi del 2024 potrebbero essere sottostimati se non aggiornati. Prima di firmare un <a href="servizio-preliminari">preliminare</a> con clausole su lavori, verificare capitolato, tempi e penali.</p>
<h3>Impatto su APE e valorizzazione</h3>
<p>Interventi che migliorano classe energetica hanno costi sensibili all'indice materiali. Tuttavia, un APE migliore può accelerare vendita e ridurre sconto in trattativa — tema collegato a <a href="blog-domanda-case-green-certificazione-padova-2026">domanda case green</a>. Non esiste percentuale fissa di plusvalore: servono comparabili.</p>""",
        "body_mid": """<h2>Nuove costruzioni nel Padovano: domanda e offerta</h2>
<p>La cintura padovana ha visto cantieri residenziali anche in anni di tassi elevati. Quando i costi di costruzione salgono, i promotori possono ritardare nuovi lanci o rivedere listini: effetto indiretto su stock disponibile e prezzi richiesti. L'acquirente deve chiedere: data consegna certificata, capitolato impianti, garanzie post-consegna, conformità urbanistica. Per chi vende immobile datato, la concorrenza del nuovo cresce se i listini restano competitivi nonostante l'indice ISTAT.</p>
<h2>Checklist budget ristrutturazione 2026</h2>
<ul>
<li>Richiedere almeno tre preventivi comparabili su stesso capitolato.</li>
<li>Separare voci strutturali, impianti, finiture: facilita priorità se il budget stringe.</li>
<li>Verificare bonus e detrazioni vigenti con commercialista — vedi <a href="blog-bonus-mobili-2026-massimizzare-ristrutturazioni">bonus mobili</a>.</li>
<li>Aggiornare APE e planimetrie post-intervento prima della messa in vendita.</li>
<li>Incrociare costi con valutazione di mercato: evitare over-investimento rispetto al quartiere.</li>
</ul>
<h3>Manodopera e tempi cantiere nel Veneto</h3>
<p>Il Nord-Est ha densità imprese edili elevata, ma cantieri possono subire ritardi per approvvigionamenti o permessi condominiali. Un costo ISTAT in crescita spesso coincide con listini imprese aggiornati: negoziare solo sul prezzo senza specifiche tecniche genera dispute. In agenzia preferiamo venditori che documentano lavori con fatture e collaudi: riduce sconti tardivi in due diligence.</p>
<h2>Collegamento con mutuo e perizia</h2>
<p>Se finanziate ristrutturazione con mutuo, la banca valuta costi e incremento valore atteso. L'indice ISTAT aiuta a giustificare preventivi, non a garantire erogazione. Per il credito abitativo rimandiamo a <a href="blog-mutui-tasso-fisso-bancaitalia-padova-2026">mutui Banca d'Italia</a> e alla <a href="landing-consulenza-immobiliare-gratuita">consulenza</a> per allineare tempi cantiere e rogito.</p>
<p>In sintesi, la dinamica ISTAT marzo 2026 conferma pressione moderata ma persistente sui costi edili. Nel Padovano conviene tradurla in preventivi aggiornati, capitolati chiari e valutazioni di mercato sobrie prima di investire in ristrutturazioni aggressive.</p>""",
        "body_tail": """<h2>Materiali e supply chain: perché l'indice sale anche con domanda moderata</h2>
<p>Non sempre un indice ISTAT in crescita coincide con cantieri pieni: può riflettere costo energetico per produzione cemento, acciaio e isolanti, oltre a stipendi settore edile. Nel Veneto, imprese medie e piccole negoziano listini trimestrali con fornitori; un +0,8% mensile segnala che preventivi firmati a gennaio potrebbero essere già datati a maggio. Per chi vende dopo ristrutturazione, documentare fatture e data lavori aiuta a giustificare prezzo richiesto senza promesse di plusvalore automatico.</p>
<h3>Confronto con inflazione generale</h3>
<p>ISTAT pubblica anche indici prezzi al consumo: incrociare costo costruzione con inflazione familiare aiuta a capire se ristrutturare ora o scalare interventi. Non esiste regola universale: dipende da urgenza impiantistica, obblighi locativi e obiettivo vendita. In <strong>centro storico padovano</strong>, vincoli architettonici possono amplificare costi unitari rispetto all'indice nazionale.</p>
<h2>Nuovo vs riqualificazione: decisione per famiglie della cintura</h2>
<p>Albignasego, Cadoneghe e Vigodarzere offrono mix di nuovo e seconda mano. Se listini nuovo salgono per costi costruzione, il secondo mano ristrutturato può diventare alternativa competitiva — a patto di APE e impianti certificati. Valutare sempre costo totale: prezzo acquisto + lavori + tempi vs nuovo con garanzie d'impresa. Righetto supporta <a href="servizio-valutazioni">stime</a> pre e post intervento con comparabili OMI.</p>
<h2>Errori da evitare nel budgeting 2026</h2>
<ul>
<li>Sottostimare voci impiantistiche (elettrico, idraulico, climatizzazione).</li>
<li>Non includere IVA, oneri comunali e eventuali contributi.</li>
<li>Assumere che bonus fiscali coprano sempre il delta ISTAT — verificare con commercialista.</li>
<li>Vendere senza aggiornare planimetrie dopo modifiche interne.</li>
</ul>
<p>Per completezza, chi compra deve chiedere capitolato lavori dell'ultimo triennio se il venditore ha ristrutturato: qualità reale e non solo APE di facciata.</p>""",
        "sources": sources_table([
            ("Indice costi costruzione", "ISTAT — marzo 2026", "Trend materiali e manodopera"),
            ("Edilizia residenziale Q1", "ISTAT", "Segmento abitazioni"),
            ("Quotazioni zona", "OMI — Agenzia delle Entrate", "Confronto post-intervento"),
            ("Contesto inflazione", "ISTAT — IPC", "Lettura reale vs nominale"),
        ]),
        "topic": "costi costruzione ISTAT edilizia residenziale",
        "anchors": [
            ("bonus ristrutturazioni", "blog-bonus-mobili-2026-massimizzare-ristrutturazioni"),
            ("case green Padova", "blog-domanda-case-green-certificazione-padova-2026"),
        ],
        "body_n": 24,
        "faqs": [
            ("Cosa misura l'indice 117,2?", "Indice ISTAT edilizia residenziale con base 2015=100; febbraio 2026 segnala costi superiori alla base decennale."),
            ("+0,8% mensile impatta subito i preventivi?", "Le imprese possono aggiornare listini con ritardo; usare l'indice come riferimento di trend."),
            ("Ristrutturare conviene comunque?", "Dipende da stato immobile, obiettivo vendita/locazione e comparabili di zona."),
            ("Il nuovo costa sempre di più?", "Pressioni su costi possono spostare listini; confrontare capitolati e consegne."),
            ("Dove scarico i dati ISTAT?", "Portale ISTAT, sezione costi di costruzione, aggiornamento marzo 2026."),
            ("Righetto fa computi metrici?", "No: supportiamo valutazione e vendita; per quantitativi tecnici servono professionisti abilitati."),
        ],
        "related": [
            ("Bonus mobili 2026", "blog-bonus-mobili-2026-massimizzare-ristrutturazioni"),
            ("Case green Padova", "blog-domanda-case-green-certificazione-padova-2026"),
            ("Valutazione", "landing-valutazione"),
        ],
        "cta_primary": ("Valutazione post-lavori", "landing-valutazione"),
        "cta_secondary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        "registry": {
            "titolo": "Costi costruzione ISTAT marzo 2026: +0,8% mensile, indice 117,2",
            "categoria": "Mercato immobiliare",
            "tempo": 12,
            "contenuto": "Pressione su materiali e manodopera: budget ristrutturazioni e nuovo nel Padovano.",
            "evidenza": True,
            "emoji": "🏗️",
        },
    },
    {
        "filename": "blog-barometro-mutui-crif-padova-2026.html",
        "slug": "blog-barometro-mutui-crif-padova-2026",
        "img": "img/blog/blog-barometro-mutui-crif-padova-2026.webp",
        "bread": "Barometro mutui CRIF 2026",
        "section": "Finanziamenti",
        "html_title": "Barometro mutui CRIF Q1 2026: domanda -12,4%, importo medio 161.059 € | Padova",
        "og_title": "Domanda mutui in calo: dati CRIF e lettura per il Padovano",
        "schema_headline": "Barometro CRIF mutui Q1 2026: domanda in calo e scelte di durata nel contesto padovano",
        "meta_desc": "CRIF Q1 2026: domanda mutui -12,4% vs 2025, importo medio 161.059 euro, 43,5% sceglie durata 25-30 anni. Applicazione territorio patavino.",
        "cat_badge": "Finanziamenti",
        "alt_img": "Grafico domanda credito — illustrazione editoriale barometro mutui ipotecari",
        "breadcrumb_tail": "Barometro CRIF mutui",
        "h1": "<strong>Domanda mutui</strong> in calo nel Q1 2026: cosa segnala il barometro CRIF per chi compra a Padova",
        "cap_img": '<p class="cap-img">Immagine <strong>simbolica</strong> sulla domanda di credito — dati da pubblicazioni <a href="https://www.crif.com" target="_blank" rel="noopener noreferrer">CRIF</a> barometro mutui Q1 2026, non offerta bancaria Righetto.</p>',
        "aeo": aeo_box(
            "Per acquirenti nel <strong>territorio patavino</strong> che interpretano il calo della domanda mutui come segnale di mercato e vogliono capire importi medi e durate più scelte.",
            [
                "Nel Q1 2026 la <strong>domanda di mutui</strong> cala del <strong>-12,4%</strong> rispetto al Q1 2025 (CRIF).",
                "L'<strong>importo medio</strong> richiesto è <strong>161.059 euro</strong>.",
                "Il <strong>43,5%</strong> dei mutui ipotecari ha durata tra <strong>25 e 30 anni</strong>.",
            ],
            [
                "Non è un rifiuto sistematico del credito da parte delle banche.",
                "Non indica il tasso o la rata del vostro contratto.",
                "Non sostituisce pre-approvazione o delibera in filiale.",
            ],
        ),
        "body_extra": """<h2>Barometro CRIF: cosa monitora</h2>
<p><a href="https://www.crif.com" target="_blank" rel="noopener noreferrer">CRIF</a> pubblica periodicamente un barometro sulla domanda di mutui ipotecari in Italia, incrociando richieste e dinamiche di mercato. Nel <strong>primo trimestre 2026</strong> la domanda registra un calo del <strong>12,4%</strong> rispetto allo stesso trimestre 2025. L'importo medio richiesto è <strong>161.059 euro</strong> e quasi metà dei contratti (43,5%) si concentra su durate tra 25 e 30 anni: segnale di ricerca di rate più sostenibili allungando l'orizzonte.</p>
<h2>Tabella sintetica CRIF Q1 2026</h2>
<table>
<thead><tr><th>Indicatore</th><th>Valore</th><th>Nota</th></tr></thead>
<tbody>
<tr><td>Variazione domanda mutui</td><td><strong>-12,4%</strong> a/a</td><td>Q1 2026 vs Q1 2025</td></tr>
<tr><td>Importo medio</td><td><strong>161.059 €</strong></td><td>Media nazionale richieste</td></tr>
<tr><td>Durata 25-30 anni</td><td><strong>43,5%</strong></td><td>Quota prevalente</td></tr>
</tbody>
</table>
<p><em>Fonte: CRIF, barometro mutui ipotecari, Q1 2026.</em></p>
<h2>Calo domanda: cause possibili (senza semplificare)</h2>
<p>Un -12,4% può riflettere combinazione di tassi ancora sensibili, prezzi richiesti elevati in alcune zone, incertezza macro e maggiore selettività bancaria. Non significa automaticamente crollo delle compravendite: parte delle transazioni resta cash o con anticipi elevati. Nel Padovano, FIAIP segnala dinamiche differenziate città-provincia — vedi <a href="blog-prezzi-padova-provincia-fiaip-2026">prezzi Padova 2026</a>.</p>
<h3>Importo medio 161.059 euro e Padova</h3>
<p>La media nazionale aiuta a dimensionare budget, ma a Padova un trilocale in cintura può superare ampiamente la soglia mentre un monolocale per studenti resta sotto. Confrontare sempre con perizia e comparabili, non con la media CRIF da sola. Per simulazioni orientative: <a href="landing-chat-calcolo-mutuo">calcolo mutuo</a>.</p>""",
        "body_mid": """<h2>Durata 25-30 anni: trade-off consapevole</h2>
<p>Scegliere il massimo orizzonte riduce la rata mensile ma aumenta interessi complessivi e sensibilità a eventuali penali. Chiedere in banca: costo totale del credito, possibilità di rinegoziazione, impatto di estinzione parziale. Incrociare con <a href="blog-mutuo-fisso-variabile-padova-2026">fisso vs variabile</a> e con il sondaggio Banca d'Italia su LTV in <a href="blog-sondaggio-bancaditalia-q1-2026-padova">sondaggio abitativo Q1</a>.</p>
<h2>Implicazioni per venditori nel Padovano</h2>
<p>Meno domanda di mutui può tradursi in acquirenti più selezionati e trattative più lunghe su immobili fuori mercato. Documentazione ordinata, APE favorevole e prezzo credibile restano leve principali. Stock in calo — tema <a href="blog-offerta-stock-vendita-italia-2026">offerta stock 2026</a> — può compensare parzialmente se il prodotto è competitivo.</p>
<h2>Checklist acquirente con mutuo nel 2026</h2>
<ul>
<li>Pre-approvazione prima di offerte vincolanti.</li>
<li>Verificare gap tra prezzo e perizia bancaria.</li>
<li>Confrontare almeno due intermediari creditizi autorizzati.</li>
<li>Stress-test rata (+1-2 punti tasso) per sostenibilità familiare.</li>
<li>Allineare tempi rogito con scadenze delibera mutuo.</li>
</ul>
<p>In conclusione, il barometro CRIF descrive un credito abitativo meno intenso rispetto al 2025, con importi medi significativi e durate lunghe. Nel Padovano la traduzione operativa è preparazione documentale e pricing realistico, non allarmismo. Righetto supporta trattative e tempi con <a href="servizio-preliminari">preliminari</a> strutturati.</p>""",
        "body_tail": """<h2>Interpretare il -12,4% senza panico</h2>
<p>Un calo della domanda mutui può coesistere con mercato residenziale attivo su segmenti cash-heavy: eredità, permute, acquirenti che vendono altrove. Nel Padovano, la provincia ha registrato dinamiche di valore transato più vivaci della città in osservazioni FIAIP 2025-2026. CRIF misura richieste finanziamento, non tutte le compravendite. Evitare di inferire «mercato fermo» da un solo indicatore.</p>
<h3>Giovani e durata 25-30 anni</h3>
<p>Allungare durata per sostenere rata è scelta frequente quando prezzi e tassi comprimono budget. Tuttavia, costo totale interessi cresce: simulare estinzione parziale e scenari di reddito futuro. Per prima casa, verificare requisiti e agevolazioni fiscali in <a href="blog-mutuo-prima-casa-padova">mutuo prima casa Padova</a>.</p>
<h2>Venditori: come reagire a credito più selettivo</h2>
<p>Se meno famiglie ottengono mutuo al primo tentativo, aumenta l'importanza di acquirenti pre-qualificati e di prezzo allineato a perizia. Offerte con caparra confirmatoria da acquirente senza delibera sono rischiose: rimandiamo a <a href="blog-caparra-confirmatoria-padova">caparra e garanzie</a>. In esclusiva, condividiamo feedback post-visita per correggere prezzo o presentazione.</p>
<h2>Quadro complessivo Q1 2026</h2>
<p>Incrociare CRIF con sondaggio Banca d'Italia (LTV 77,2%, tempi 5,2 mesi) offre vista più completa: credito ancora rilevante ma meno intenso, trattative con sconto medio significativo. Strategia vincente nel Padovano resta prodotto competitivo (energia, documenti, prezzo) più che timing macro perfetto.</p>""",
        "sources": sources_table([
            ("Domanda mutui Q1", "CRIF — barometro mutui", "Trend richieste nazionali"),
            ("LTV e condizioni", "Banca d'Italia — indagine mutui", "Contesto bancario"),
            ("Prezzi locali", "FIAIP / OMI", "Micro-mercato Padova"),
            ("Tassi di riferimento", "BCE", "Policy monetaria"),
        ]),
        "topic": "barometro CRIF mutui ipotecari Q1 2026",
        "anchors": [
            ("sondaggio Banca d'Italia", "blog-sondaggio-bancaditalia-q1-2026-padova"),
            ("mutui selettivi", "blog-mutui-selettivi-banche-padova-2026"),
        ],
        "body_n": 24,
        "faqs": [
            ("Perché la domanda mutui cala del 12,4%?", "CRIF segnala minor intensità di richieste Q1 2026 vs 2025; causale multipla (tassi, prezzi, fiducia)."),
            ("161.059 euro è il prezzo medio casa?", "No: è l'importo medio richiesto a mutuo, non il prezzo di vendita."),
            ("Conviene sempre 25-30 anni?", "Dipende da reddito, età e costo totale; valutare con consulente creditizio."),
            ("Il calo CRIF ferma le compravendite?", "Non necessariamente: transazioni cash e segmenti resilienti continuano."),
            ("Dove trovo il report CRIF?", "Pubblicazioni CRIF sul barometro mutui ipotecari, Q1 2026."),
            ("Righetto vende prodotti mutuo?", "No: assistenza immobiliare; per credito rivolgersi a banche e broker autorizzati."),
        ],
        "related": [
            ("Sondaggio Banca d'Italia Q1", "blog-sondaggio-bancaditalia-q1-2026-padova"),
            ("Mutui selettivi Padova", "blog-mutui-selettivi-banche-padova-2026"),
            ("Calcolo mutuo", "landing-chat-calcolo-mutuo"),
        ],
        "cta_primary": ("Simulazione mutuo", "landing-chat-calcolo-mutuo"),
        "cta_secondary": ("Supporto trattativa", "contatti"),
        "registry": {
            "titolo": "Barometro mutui CRIF Q1 2026: domanda -12,4%, importo medio 161.059 €",
            "categoria": "Finanziamenti",
            "tempo": 11,
            "contenuto": "Durata 25-30 anni al 43,5%: lettura per acquirenti nel Padovano.",
            "evidenza": True,
            "emoji": "📊",
        },
    },
    {
        "filename": "blog-dazi-usa-ue-mercato-padova-2026.html",
        "slug": "blog-dazi-usa-ue-mercato-padova-2026",
        "img": "img/blog/blog-dazi-usa-ue-mercato-padova-2026.webp",
        "bread": "Dazi USA-UE e mercato Padova",
        "section": "Economia",
        "html_title": "Dazi USA-UE e mercato padovano 2026: Turnberry 15%, minaccia auto 25% | Canali verso casa",
        "og_title": "Accordo commerciale USA-UE e filiera Veneto: effetti indiretti sul mattone",
        "schema_headline": "Dazi USA-UE maggio 2026: impatto su export veneto, occupazione e fiducia nel mercato abitativo padovano",
        "meta_desc": "Patto Turnberry 15% dazi USA-UE, minaccia Trump 25% auto maggio 2026. Canali verso occupazione, credito e immobiliare nel Veneto — non cronaca Medio Oriente.",
        "cat_badge": "Economia",
        "alt_img": "Container e commercio internazionale — illustrazione editoriale dazi USA-UE e filiera industriale",
        "breadcrumb_tail": "Dazi USA-UE",
        "h1": "<strong>Dazi USA-UE</strong> e filiera veneta: dal patto Turnberry alla fiducia di chi compra casa a Padova",
        "cap_img": '<p class="cap-img">Immagine <strong>illustrativa</strong> su commercio internazionale — non riproduce testi dell\'accordo. Focus su <em>canali economici</em> verso occupazione e credito, distinto da <a href="blog-mercato-italiano-tensioni-medio-oriente-2026">tensioni Medio Oriente</a>.</p>',
        "aeo": aeo_box(
            "Per famiglie e imprenditori del <strong>Veneto orientale</strong> che collegano notizie su <strong>dazi USA-UE</strong> (patto Turnberry, minacce su auto) alle proprie scelte su mutuo, lavoro e immobile.",
            [
                "A maggio 2026 si discute di un <strong>accordo con dazio base 15%</strong> nel quadro Turnberry tra USA e UE.",
                "Resta la <strong>minaccia di dazi al 25% sui veicoli</strong> annunciata da Trump a maggio 2026.",
                "Il Veneto export-oriented può sentire effetti su <strong>occupazione e fiducia</strong>, con riflessi indiretti su mutui e compravendite.",
            ],
            [
                "Non è analisi geopolitica mediorientale (argomento trattato altrove sul blog).",
                "Non prevede crolli o boom automatici dei prezzi casa a Padova.",
                "Non è consulenza doganale o commerciale.",
            ],
        ),
        "body_extra": """<h2>Turnberry e dazio 15%: cosa cambia nel dibattito</h2>
<p>Le trattative tra Unione europea e Stati Uniti a maggio 2026 ruotano attorno a un <strong>accordo quadro</strong> che fissa un dazio base intorno al <strong>15%</strong> nel cosiddetto percorso Turnberry, con settori sensibili (acciaio, alluminio, auto) oggetto di clausole e negoziati paralleli. Per l'Italia, filiera manifatturiera e export verso gli USA restano rilevanti: il Veneto, con distretti meccanica, componentistica e moda, è esposto a shock di domanda e incertezza contrattuale.</p>
<h2>Minaccia 25% su auto: perché interessa anche chi compra casa</h2>
<p>L'annuncio di una possibile <strong>tariffa del 25% sui veicoli</strong> (maggio 2026) alimenta volatilità su filiere automotive e fornitori. Nel Padovano e in provincia operano imprese subfornitrici: effetti possibili su turni, cassa integrazione, reddito disponibile. Il canale verso l'immobiliare è indiretto ma reale: famiglie con reddito legato all'export possono ritardare acquisto, stringere budget mutuo o evitare upsizing. Non è legge del mercato, è scenario da monitorare.</p>
<h3>Tabella canali di trasmissione verso il mattone</h3>
<table>
<thead><tr><th>Canale</th><th>Meccanismo</th><th>Effetto possibile Padovano</th></tr></thead>
<tbody>
<tr><td>Occupazione industriale</td><td>Ordini export USA in calo</td><td>Maggiore prudenza su rata mutuo</td></tr>
<tr><td>Fiducia famiglie</td><td>Titoli e incertezza commerciale</td><td>Ritardo decisioni compravendita</td></tr>
<tr><td>Costo del denaro</td><td>Risposta BCE a inflazione/import</td><td>Condizioni mutuo variabili nel tempo</td></tr>
<tr><td>Investimenti impresa</td><td>CapEx ridotto in filiera</td><td>Minore domanda locazioni industriali</td></tr>
</tbody>
</table>
<h2>Distinction: non è l'articolo sul Medio Oriente</h2>
<p>Questo testo affronta <strong>commercial policy USA-UE</strong> e filiera veneta. Per energia e tensioni mediorientali rimandiamo a <a href="blog-mercato-italiano-tensioni-medio-oriente-2026">Medio Oriente e mercato</a> e a <a href="blog-previsioni-immobiliari-scenari-geopolitica-2026">previsioni e scenari</a>. Evitare di mescolare shock diversi in un unico titolo allarmistico.</p>""",
        "body_mid": """<h2>Padova e cintura: domanda residenziale e lavoro</h2>
<p>Il capoluogo euganeo combina università, sanità e pendolarismo verso Mestre-Venezia. Un rallentamento export non colpisce uniformemente: servizi e pubblico impiego possono restare stabili mentre manifattura subfornitura oscilla. Chi compra in <strong>Limena, Vigodarzere, Rubano</strong> dovrebbe mappare quanto il reddito familiare dipende da settori esposti ai dazi USA. Stress-test del mutuo resta la pratica più utile.</p>
<h2>Cosa fare (e cosa evitare) se segui le notizie sui dazi</h2>
<ul>
<li><strong>Fare:</strong> mantenere documenti mutuo pronti se la trattativa è avanzata; incertezza macro non annulla bisogni abitativi strutturali.</li>
<li><strong>Fare:</strong> diversificare fonti — comunicati UE, ICE, associazioni di categoria.</li>
<li><strong>Evitare:</strong> posticipare indefinitamente per titoli giornalistici senza impatto sul proprio reddito.</li>
<li><strong>Evitare:</strong> generalizzare da export veneto a prezzo del singolo appartamento in centro Padova.</li>
</ul>
<h3>Collegamento con Eurocamera</h3>
<p>Il voto e il compromesso del Parlamento europeo (Strasburgo, maggio 2026) su clausole di salvaguardia e sunset 2029 incidono sulla durata dell'incertezza. Approfondimento dedicato in <a href="blog-eurocamera-accordo-dazi-usa-2026">Eurocamera e accordo dazi USA</a>.</p>
<p>In conclusione, dazi USA-UE e minacce settoriali si traducono per il Padovano soprattutto in <strong>occupazione, fiducia e costo del denaro</strong>, non in quote automatiche sul metro quadro. Righetto affianca decisioni immobiliari con comparabili locali e <a href="landing-consulenza-immobiliare-gratuita">consulenza</a>, senza promettere scenari macro.</p>""",
        "body_tail": """<h2>Veneto orientale: filiere a rischio e filiere resilienti</h2>
<p>Meccatronica, occhialeria, calzature e componentistica auto convivono nel Nord-Est. Un dazio USA al 15% con escalation sui veicoli può colpire in modo asimmetrico: fornitore tier-2 subisce prima del brand finale. Famiglie con reddito duale (industria + servizi) hanno margine maggiore rispetto a nuclei mono-reddito esposti. Prima di comprare casa, mappare settore datore e orizzonte contrattuale collettivo aiuta stress-test rata.</p>
<h3>Domanda immobiliare da trasferimenti</h3>
<p>Non tutto passa da export: sanità, università e pendolarismo verso Venezia sostengono domanda residenziale padovana. Shock commerciali USA-UE non annullano bisogni abitativi strutturali (famiglia, studio, prossimità servizi). Tuttavia, ritardi su acquisto per incertezza possono accumularsi: quando fiducia riparte, segmenti pronti (APE buona, prezzo credibile) assorbono per primi.</p>
<h2>Politica commerciale e BCE: catena indiretta</h2>
<p>Tariffe e risposte europee possono alimentare dibattito su inflazione importata e reazione di politica monetaria. Per mutuo, significa monitorare BCE e spread bancari, non solo titoli sui dazi. Articolo gemello su voto parlamentare: <a href="blog-eurocamera-accordo-dazi-usa-2026">Eurocamera e accordo</a>. Per resilienza patrimoniale: <a href="blog-patrimonio-casa-resilienza-mercati-globali-2026">patrimonio casa</a>.</p>
<h2>Operatività Righetto in fase di incertezza</h2>
<p>Continuiamo a pubblicare comparabili verificati, accompagnare preliminari con clausole sospensive mutuo chiare e segnalare documenti urbanistici critici prima dell'offerta. Non vendiamo prodotti finanziari né facciamo previsioni macro: riduciamo attrito operativo sul singolo immobile in <strong>101 comuni</strong> serviti da Limena.</p>""",
        "sources": sources_table([
            ("Accordo USA-UE / Turnberry", "Comunicati UE e stampa istituzionale maggio 2026", "Quadro dazi 15%"),
            ("Minaccia dazi auto", "Dichiarazioni politiche USA maggio 2026", "Rischio settoriale"),
            ("Export Veneto", "ICE / dati camera commercio", "Esposizione filiera"),
            ("Mutui e fiducia", "Banca d'Italia / CRIF", "Contesto credito"),
        ]),
        "topic": "dazi USA-UE export Veneto mercato abitativo",
        "anchors": [
            ("Eurocamera accordo dazi", "blog-eurocamera-accordo-dazi-usa-2026"),
            ("geopolitica energia tassi", "blog-immobiliare-geopolitica-energia-tassi-2026"),
        ],
        "body_n": 24,
        "faqs": [
            ("I dazi USA-UE abbassano i prezzi casa a Padova?", "Non in modo automatico: effetti indiretti via lavoro, fiducia e credito."),
            ("Cosa significa dazio 15% Turnberry?", "Accordo quadro discusso maggio 2026 con tariffa base indicativa; settori possono avere regole diverse."),
            ("Perché distinto dall'articolo Medio Oriente?", "Shock diversi: qui commercio USA-UE e filiera veneta, lì energia e area mediterranea."),
            ("Devo rimandare l'acquisto?", "Dipende da situazione lavorativa e mutuo; valutare caso per caso."),
            ("Dove seguire negoziato ufficiale?", "Siti istituzionali UE e comunicati europei aggiornati."),
            ("Righetto fa previsioni macro?", "No: supporto immobiliare locale con dati verificabili."),
        ],
        "related": [
            ("Eurocamera accordo dazi", "blog-eurocamera-accordo-dazi-usa-2026"),
            ("Medio Oriente (canali distinti)", "blog-mercato-italiano-tensioni-medio-oriente-2026"),
            ("Patrimonio e resilienza", "blog-patrimonio-casa-resilienza-mercati-globali-2026"),
        ],
        "cta_primary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        "cta_secondary": ("Mercato Padova", "blog-mercato-immobiliare-padova-2026"),
        "registry": {
            "titolo": "Dazi USA-UE e mercato padovano 2026: Turnberry 15%, filiera Veneto",
            "categoria": "Economia",
            "tempo": 12,
            "contenuto": "Canali occupazione e credito verso mutui e compravendite — non cronaca Medio Oriente.",
            "evidenza": False,
            "emoji": "🌐",
        },
    },
    {
        "filename": "blog-eurocamera-accordo-dazi-usa-2026.html",
        "slug": "blog-eurocamera-accordo-dazi-usa-2026",
        "img": "img/blog/blog-eurocamera-accordo-dazi-usa-2026.webp",
        "bread": "Eurocamera accordo dazi USA",
        "section": "Economia",
        "html_title": "Eurocamera e accordo dazi USA 2026: compromesso Strasburgo, sunset 2029 | Italia",
        "og_title": "Parlamento UE su accordo commerciale USA: clausole e impatti indiretti",
        "schema_headline": "Parlamento europeo maggio 2026: compromesso su accordo commerciale USA, sunset 2029 e salvaguardie acciaio",
        "meta_desc": "Strasburgo maggio 2026: compromesso Eurocamera su accordo commerciale USA, clausola sunset 2029, salvaguardie acciaio e alluminio. Lettura per famiglie e imprese padovane.",
        "cat_badge": "Economia",
        "alt_img": "Aula parlamentare europea — illustrazione editoriale voto accordo commerciale USA-UE",
        "breadcrumb_tail": "Eurocamera dazi USA",
        "h1": "<strong>Eurocamera</strong> e accordo USA: clausola 2029, acciaio e riflessi sul mercato casa in Italia",
        "cap_img": '<p class="cap-img">Immagine <strong>illustrativa</strong> del contesto parlamentare europeo — non documenta un voto specifico. Sintesi da lavori di Strasburgo, maggio 2026.</p>',
        "aeo": aeo_box(
            "Per cittadini e imprenditori in <strong>Italia</strong> che seguono il voto del <strong>Parlamento europeo</strong> su trade USA e vogliono capire durata dell'accordo e settori protetti.",
            [
                "A <strong>Strasburgo, maggio 2026</strong>, emerge un <strong>compromesso</strong> parlamentare sull'accordo commerciale con gli USA.",
                "Compare una <strong>clausola sunset 2029</strong> per revisione o fine del quadro.",
                "Restano <strong>salvaguardie su acciaio e alluminio</strong> per tutelare filiere europee.",
            ],
            [
                "Non è testo legislativo vincolante da consultare al posto del Gazzettino Ufficiale UE.",
                "Non indica variazioni immediate del prezzo degli immobili.",
                "Non sostituisce consulenza legale o doganale per export.",
            ],
        ),
        "body_extra": """<h2>Cosa decide (o orienta) il Parlamento europeo</h2>
<p>Il <strong>Parlamento europeo</strong>, riunito a <strong>Strasburgo</strong> a maggio 2026, lavora su un compromesso che consente all'UE di procedere nell'implementazione dell'accordo commerciale con gli Stati Uniti discusso nel quadro Turnberry. Il ruolo parlamentare include controllo democratico, clausole di salvaguardia e limiti temporali: elementi che riducono (senza eliminare) l'incertezza per imprese export-oriented.</p>
<h2>Sunset clause 2029: perché conta</h2>
<p>La <strong>clausola di scadenza 2029</strong> implica che il quadro negociato dovrà essere rinnovato o rinegoziato entro quella data. Per pianificazione industriale — e indirettamente per famiglie dipendenti da settori esposti — significa orizzonte medio definito: utile per investimenti, meno utile se cercate certezze oltre cinque anni. Sul mattone, l'effetto è mediato: fiducia e occupazione pluriennali influenzano domanda di mutui e locazioni.</p>
<h3>Salvaguardie acciaio e alluminio</h3>
<p>Le <strong>salvaguardie</strong> su acciaio e alluminio mirano a evitare danni concentrati su siderurgia europea. Il Veneto ospita catene di fornitura metalmeccanica: tutela settoriale può limitare shock occupazionali locali. Non confondere protezione commerciale con boom edilizio: nuovi cantieri dipendono anche da tassi, permessi e domanda demografica.</p>
<table>
<thead><tr><th>Elemento compromesso</th><th>Contenuto sintetico</th><th>Lettura immobiliare indiretta</th></tr></thead>
<tbody>
<tr><td>Accordo commerciale USA</td><td>Implementazione con condizioni PE</td><td>Minor volatilità attesa su export</td></tr>
<tr><td>Sunset 2029</td><td>Revisione obbligata</td><td>Orizzonte medio per lavoro e credito</td></tr>
<tr><td>Acciaio / alluminio</td><td>Salvaguardie settoriali</td><td>Protezione occupazione industriale locale</td></tr>
</tbody>
</table>""",
        "body_mid": """<h2>Italia e Padova: posizione nella filiera</h2>
<p>L'Italia resta tra i paesi con forte integrazione commerciale transatlantica. Nel Padovano, PMI fornitrici possono beneficiare di regole più prevedibili, pur restando esposte a shock settoriali (auto, componentistica). Chi valuta acquisto casa con reddito da lavoro industriale dovrebbe mantenere margine sulla rata anche in scenari di rallentamento ordini.</p>
<h2>Collegamento con dazi e mercato locale</h2>
<p>Per il quadro dazi 15% e minacce auto rimandiamo a <a href="blog-dazi-usa-ue-mercato-padova-2026">dazi USA-UE e Padova</a>. Qui l'angolo è istituzionale europeo: cosa ha chiesto l'Eurocamera prima di dare via libera politico. Due livelli di lettura — negoziato e voto parlamentare — aiutano a non reagire a singoli titoli.</p>
<h2>Checklist prudente per famiglie e investitori</h2>
<ul>
<li>Separare cronaca politica da impatto sul proprio reddito.</li>
<li>Monitorare fonti UE ufficiali oltre ai social.</li>
<li>Mantenere documenti compravendita pronti: incertezza macro non sospende rogiti necessari.</li>
<li>Per mutuo, stress-test come in <a href="blog-barometro-mutui-crif-padova-2026">barometro CRIF</a>.</li>
</ul>
<p>In conclusione, il compromesso di Strasburgo maggio 2026 introduce limiti temporali e salvaguardie settoriali utili a imprese e lavoratori, con riflessi indiretti su fiducia e credito abitativo. Righetto resta focalizzata sul micro-mercato padovano con <a href="servizio-vendita">vendita</a> e <a href="landing-valutazione">valutazioni</a> ancorate a comparabili verificati.</p>""",
        "body_tail": """<h2>Trattato vs regolamento provvisorio: perché il PE conta</h2>
<p>Il Parlamento europeo non negozia tariffe, ma può condizionare consenso democratico e trasparenza. Clausole su acciaio e alluminio rispondono a pressioni di aree industriali europee; in Italia, filiere metalmeccaniche del Nord-Est seguono da vicino. Per l'immobiliare, effetto è mediato da occupazione e investimenti impresa, non da prezzo mq immediato.</p>
<h3>Orizzonte 2029 e mutui a lungo termine</h3>
<p>Chi prende mutuo 25-30 anni affronta orizzonte simile alla sunset clause: non significa scadenza mutuo, ma possibile rinnovo tensioni commerciali entro ciclo vita del debito. Stress-test resta best practice — vedi <a href="blog-mutui-tasso-fisso-bancaitalia-padova-2026">mutui Banca d'Italia</a>.</p>
<h2>Italia export e famiglie padovane</h2>
<p>Medicale, macchinari, design alimentare e moda convivono nel panorama export italiano. Padova e provincia beneficiano di diversificazione rispetto a mono-settore auto, pur restando esposti. Acquisto casa dovrebbe considerare stabilità reddituale pluriennale, fondi emergenza e costi fissi, indipendentemente da titoli Strasburgo.</p>
<h2>Sintesi operativa per lettori del blog</h2>
<p>Seguire negoziato USA-UE su due binari — esecutivo e parlamentare — riduce sorprese. Per decisioni immobiliari concrete: comparabili locali, documenti in ordine, consulenza <a href="landing-consulenza-immobiliare-gratuita">gratuita</a> se in dubbio su timing vendita o acquisto. Non sostituiamo analisti macro né consulenti export.</p>""",
        "sources": sources_table([
            ("Voto / compromesso PE", "Parlamento europeo — Strasburgo maggio 2026", "Condizioni accordo USA"),
            ("Accordo commerciale", "Commissione europea — comunicati", "Quadro negoziale"),
            ("Salvaguardie siderurgia", "Testi compromesso PE", "Acciaio e alluminio"),
            ("Contesto credito IT", "Banca d'Italia", "Fiducia e mutui"),
        ]),
        "topic": "Parlamento europeo accordo commerciale USA sunset 2029",
        "anchors": [
            ("dazi USA-UE Padova", "blog-dazi-usa-ue-mercato-padova-2026"),
            ("prospettive mercato", "blog-prospettive-mercato-residenziale-italia-2026"),
        ],
        "body_n": 24,
        "faqs": [
            ("Cosa significa sunset clause 2029?", "L'accordo sarebbe soggetto a revisione o fine entro il 2029 salvo rinnovo."),
            ("Il voto Eurocamera cambia i prezzi casa?", "No direttamente: effetti mediati su economia reale e fiducia."),
            ("Perché salvaguardie su acciaio?", "Tutela filiere europee esposte a import competitivi."),
            ("Dove leggo il testo ufficiale?", "Siti Parlamento europeo e Gazzetta Ufficiale UE quando pubblicato."),
            ("Collegamento con articolo dazi Padova?", "Sì: negoziato commerciale vs implementazione parlamentare."),
            ("Righetto commenta politica commerciale?", "No: traduciamo solo canali rilevanti per decisioni immobiliari locali."),
        ],
        "related": [
            ("Dazi USA-UE e Padova", "blog-dazi-usa-ue-mercato-padova-2026"),
            ("Prospettive mercato 2026", "blog-prospettive-mercato-residenziale-italia-2026"),
            ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        ],
        "cta_primary": ("Parla con noi", "contatti"),
        "cta_secondary": ("Valutazione immobile", "landing-valutazione"),
        "registry": {
            "titolo": "Eurocamera e accordo dazi USA 2026: compromesso Strasburgo, sunset 2029",
            "categoria": "Economia",
            "tempo": 11,
            "contenuto": "Salvaguardie acciaio/alluminio e orizzonte 2029: lettura per imprese e famiglie padovane.",
            "evidenza": False,
            "emoji": "🇪🇺",
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

    reg_path = root / "scripts" / "may27_blog_registry.json"
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
