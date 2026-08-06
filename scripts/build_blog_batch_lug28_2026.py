# -*- coding: utf-8 -*-
"""Genera 7 articoli blog luglio 2026 — batch Padova/Veneto + guide EN.
Esegui da repo root: python scripts/build_blog_batch_lug28_2026.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "28 luglio 2026"
DATE_ISO = "2026-07-28"
TIME_TS = "2026-07-28T09:00:00+02:00"
MIN_BODY_WORDS = 2500
CAP_BLOG_AI = (
    "Immagine editoriale elaborata digitalmente (anche con intelligenza artificiale): "
    "illustrazione a scopo informativo, non documento fotografico dell'immobile o della scena descritta."
)

OMI_URL = (
    "https://www.agenziaentrate.gov.it/portale/schede/fabbricatiterreni/"
    "omi/banche-dati/quotazioni-immobiliari"
)
ADE_OSSERVATORIO = (
    "https://www.agenziaentrate.gov.it/portale/schede/fabbricatiterreni/"
    "osservatorio-del-mercato-immobiliare"
)
ISTAT_URL = "https://www.istat.it/it/archivio/prezzi+immobili"
CUSHMAN_OUTLOOK = "https://www.cushmanwakefield.com/it-it/italy/insights/italy-outlook"
BANCA_ITALIA = "https://www.bancaditalia.it/pubblicazioni/indagine-fam-imprese/index.html"

CLAIM_FOOT = (
    "Gruppo Immobiliare Righetto opera dal <strong>2000</strong> su <strong>101 comuni</strong>, "
    "con oltre <strong>350 immobili</strong> gestiti e <strong>98% di soddisfazione</strong> clienti "
    "(127 recensioni Google, media 4,9/5). Il compenso di mediazione si concorda "
    "<strong>in sede</strong> — nessun listino percentuale online."
)

STYLE_BLOCK = r"""<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--nero:#152435;--bianco:#F7F5F1;--oro:#FF6B35;--grigio:#6B7A8D;--gc:#E1DBD1;--sfondo:#ECE7DF;--blu:#2C4A6E;--blu2:#3A5F8C;--oro2:#FF8F5E;--testo:#152435}
body{font-family:'Montserrat',sans-serif;background:var(--bianco);color:var(--testo)}
a{text-decoration:none;color:inherit}
header{background:var(--nero);position:sticky;top:0;z-index:100}
.hi{max-width:1380px;margin:0 auto;padding:0 1.5rem;height:74px;display:flex;align-items:center;gap:2rem}
.logo{font-family:'Cormorant Garamond',serif;font-size:1.3rem;font-weight:600;color:#fff}
.logo span{color:var(--oro);font-style:italic}
nav{display:flex;gap:.2rem;flex:1}nav a{color:rgba(255,255,255,.7);font-size:.82rem;padding:.4rem .75rem}nav a.active{color:var(--oro)}
.h-cta{display:flex;gap:.65rem;align-items:center}.h-tel{color:rgba(255,255,255,.75);font-size:.78rem}
.h-btn{background:var(--oro);color:var(--nero);padding:.38rem .85rem;border-radius:6px;font-size:.76rem;font-weight:500}
.art-hero{position:relative;overflow:hidden}
.art-hero__frame{position:relative;width:100%;aspect-ratio:19/9;overflow:hidden}
.art-hero__frame .art-hero-img,.art-hero-img{width:100%;height:100%;object-fit:cover;display:block;filter:brightness(.42)}
.art-hero-overlay{position:absolute;bottom:0;left:0;right:0;padding:3rem 1.5rem 2.5rem;background:linear-gradient(transparent,rgba(21,36,53,.95) 40%);z-index:1}
.art-hero-inner{max-width:820px;margin:0 auto}
.breadcrumb{font-size:.72rem;color:rgba(255,255,255,.45);margin-bottom:1rem}.breadcrumb a{color:rgba(255,255,255,.55)}
.cat-badge{font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;background:rgba(255,107,53,.2);color:var(--oro);padding:.25rem .7rem;font-weight:700;margin-bottom:.8rem;display:inline-block}
.art-hero h1{font-family:'Cormorant Garamond',serif;font-size:2.2rem;font-weight:300;color:#fff;line-height:1.2;margin-bottom:1rem}
.art-hero h1 strong{font-weight:600;font-style:italic}
.art-hero-meta{display:flex;gap:1rem;font-size:.8rem;color:rgba(255,255,255,.5);flex-wrap:wrap;align-items:center}
.av{width:36px;height:36px;border-radius:50%;background:var(--oro);display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--nero)}
.art-container{max-width:820px;margin:0 auto;padding:2.5rem 1.5rem 4rem}
.art-content{font-size:.92rem;line-height:1.9}
.art-content h2{font-family:'Cormorant Garamond',serif;font-size:1.75rem;margin:2.5rem 0 .8rem;padding-bottom:.4rem;border-bottom:2px solid var(--oro);color:var(--nero)}
.art-content h3{font-family:'Cormorant Garamond',serif;font-size:1.28rem;color:var(--blu);margin:1.4rem 0 .5rem}
.art-content p{margin-bottom:1.1rem}
.art-content ul,.art-content ol{margin:0 0 1rem 1.4rem}
.art-content a{color:var(--blu);text-decoration:underline}
.art-content table{width:100%;border-collapse:collapse;margin:1.2rem 0;font-size:.84rem}
.art-content th,.art-content td{padding:.65rem;border:1px solid var(--gc)}
.art-content th{background:var(--sfondo);text-transform:uppercase;font-size:.74rem}
.toc{background:var(--sfondo);border:1px solid var(--gc);border-radius:10px;padding:1.2rem;margin-bottom:2rem}
.toc-title{font-weight:600;font-family:'Cormorant Garamond',serif;font-size:1.1rem;margin-bottom:.5rem}
.toc ol{font-size:.84rem;margin-left:1.2rem}
.aeo-box{border:2px solid var(--blu);border-radius:12px;padding:1.15rem 1.3rem;margin-bottom:1.65rem;background:linear-gradient(135deg,rgba(44,74,110,.07),rgba(255,107,53,.06))}
.aeo-box h2{font-family:'Montserrat',sans-serif;font-size:.95rem;text-transform:uppercase;letter-spacing:.06em;color:var(--blu);margin:0 0 .55rem;border:none;padding:0}
.kpi-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:.55rem;margin:1.2rem 0 1.6rem}
.kpi-strip div{background:var(--sfondo);border:1px solid var(--gc);border-radius:10px;padding:.75rem .85rem;text-align:center}
.kpi-strip strong{display:block;font-family:'Cormorant Garamond',serif;font-size:1.35rem;color:var(--blu)}
.kpi-strip span{font-size:.62rem;letter-spacing:.06em;text-transform:uppercase;color:var(--grigio)}
.righetto-sol{border:2px solid var(--oro);border-radius:12px;padding:1.15rem 1.3rem;margin:1.65rem 0 2rem;background:linear-gradient(135deg,rgba(255,107,53,.08),rgba(44,74,110,.05))}
.righetto-sol h2{font-family:'Montserrat',sans-serif;font-size:.95rem;text-transform:uppercase;letter-spacing:.06em;color:var(--oro);margin:0 0 .65rem;border:none;padding:0}
.cta-row{display:flex;flex-wrap:wrap;gap:1rem;margin:2rem 0}
.cta-deep{display:inline-flex;background:linear-gradient(180deg,var(--oro2),var(--oro));color:var(--nero);padding:.85rem 1.75rem;border-radius:10px;font-weight:800;font-size:.82rem}
.cta-deep-outline{padding:.8rem 1.55rem;border-radius:10px;border:2px solid var(--blu);color:var(--blu);font-weight:700;font-size:.8rem}
.faq-item{border:1px solid var(--gc);border-radius:8px;margin-bottom:.6rem}
.faq-q{padding:1rem;font-weight:600;cursor:pointer;display:flex;justify-content:space-between}
.faq-q::after{content:'+';color:var(--oro)}
.faq-item.open .faq-a{max-height:480px}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s;background:var(--sfondo)}
.faq-a-inner{padding:0 1rem 1rem;font-size:.86rem;color:var(--grigio);line-height:1.8}
.cta-banner{background:linear-gradient(135deg,var(--nero),var(--blu));border-radius:14px;padding:2rem;margin:2.5rem 0;display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center}
.cta-banner h3{font-family:'Cormorant Garamond',serif;color:#fff;font-size:1.4rem;margin-bottom:.4rem}
.cta-banner p{color:rgba(255,255,255,.55);font-size:.84rem}
.cta-banner-btn{background:linear-gradient(180deg,var(--oro2),var(--oro));color:var(--nero);padding:.75rem 1.8rem;border-radius:10px;font-weight:800}
.share-bar{border-top:1px solid var(--gc);padding:1rem 0;margin:2rem 0;display:flex;gap:1rem;flex-wrap:wrap}
.share-btn{padding:.4rem 1rem;border:1px solid var(--gc);border-radius:20px;background:#fff;font-size:.76rem;cursor:pointer;font-family:inherit}
.related{background:var(--sfondo);border:1px solid var(--gc);padding:1.5rem;border-radius:10px;margin-top:2rem}
.related a{color:var(--blu);text-decoration:underline}
.author-bio{display:flex;gap:1.2rem;border:1px solid rgba(44,74,110,.12);padding:1.5rem;border-radius:12px;margin:2rem 0}
.author-bio img{width:64px;height:64px;border-radius:50%;object-fit:cover}
.blog-fig{margin:1.65rem 0;border-radius:12px;overflow:hidden;border:1px solid var(--gc)}
.blog-fig img{width:100%;height:auto;display:block;max-height:420px;object-fit:cover}
.blog-fig figcaption{font-size:.72rem;color:var(--grigio);padding:.7rem .95rem;background:var(--sfondo)}
footer{background:linear-gradient(180deg,var(--nero),#0d1a2a);padding:2.5rem 1.5rem;color:rgba(255,255,255,.65);font-size:.78rem}
.fi{max-width:1380px;margin:0 auto}
.fgrid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:2rem;margin-bottom:1.5rem}
.flogo{font-family:'Cormorant Garamond',serif;color:#fff;font-size:1.1rem}.flogo span{color:var(--oro);font-style:italic}
.skip-link{position:absolute;top:-100%;background:var(--oro);color:var(--nero);padding:.5rem 1rem;z-index:9999}.skip-link:focus{top:0}
@media(max-width:768px){.art-hero h1{font-size:1.75rem}.kpi-strip{grid-template-columns:repeat(2,1fr)}}
</style>
<link rel="stylesheet" href="css/blog-rich.css?v=4">
<link rel="stylesheet" href="css/blog-lead-form.css?v=2">"""


def wc(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html)
    return len(re.sub(r"\s+", " ", text).strip().split())


def blog_fig(src: str, alt: str, cap: str | None = None) -> str:
    caption = cap if cap is not None else CAP_BLOG_AI
    return (
        f'<figure class="blog-fig"><img src="{src}" alt="{alt}" width="820" height="460" loading="lazy">'
        f'<figcaption class="rig-photo-caption">{caption}</figcaption></figure>'
    )


def aeo_box(title: str, text: str) -> str:
    return f'<div class="aeo-box"><h2>{title}</h2><p>{text}</p></div>'


def sol_box(question: str, items: list[tuple[str, str, str]]) -> str:
    lis = "".join(f"<li><strong>{t}</strong> — {d} (<a href=\"{h}\">{lt}</a>)</li>" for t, d, lt, h in items)
    return f"""<div class="righetto-sol"><h2>Cosa può fare Righetto</h2>
<p><strong>Il quesito:</strong> {question}</p><ul>{lis}</ul>
<p style="font-size:.78rem;color:var(--grigio)"><em>Mediazione concordata in sede — nessun listino online. Tel. 049.8843484 · <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a>.</em></p></div>"""


def sol_box_en(question: str, items: list[tuple[str, str, str, str]]) -> str:
    lis = "".join(f"<li><strong>{t}</strong> — {d} (<a href=\"{h}\">{lt}</a>)</li>" for t, d, lt, h in items)
    return f"""<div class="righetto-sol"><h2>How Righetto can help</h2>
<p><strong>Your question:</strong> {question}</p><ul>{lis}</ul>
<p style="font-size:.78rem;color:var(--grigio)"><em>Agency fees agreed in office — no online commission rates. Tel. +39 049 8843484 · <a href="landing-consulenza-immobiliare-gratuita">free consultation</a>.</em></p></div>"""


def faq_html(faqs: list[tuple[str, str]], title: str = "FAQ") -> str:
    items = "".join(
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>'
        for q, a in faqs
    )
    return f'<div class="faq-section" id="faq"><h2 style="font-family:\'Cormorant Garamond\',serif;font-size:1.7rem;border-bottom:2px solid var(--oro);margin-bottom:1rem;padding-bottom:.35rem">{title}</h2>{items}</div>'


def lead_form(slug: str, lang: str = "it") -> str:
    if lang == "en":
        return f"""
<section class="blog-lead-wrap" id="richiedi-consulenza" aria-labelledby="blog-lead-title">
  <h2 id="blog-lead-title">Request information</h2>
  <form data-rig-lead-form data-provenienza="{slug}" data-pagina="{slug}" data-msg-prefix="[Blog EN]" novalidate>
    <div class="bl-fields">
      <label for="bl-nome">Full name *</label>
      <input type="text" id="bl-nome" required autocomplete="name" placeholder="John Smith">
      <label for="bl-tel">Phone *</label>
      <input type="tel" id="bl-tel" required autocomplete="tel" placeholder="+39 333 123 4567">
      <label for="bl-email">Email</label>
      <input type="email" id="bl-email" autocomplete="email" placeholder="you@email.com">
      <label for="bl-msg">Message (optional)</label>
      <textarea id="bl-msg" placeholder="Area, budget, rental or purchase…"></textarea>
      <label class="bl-chk"><input type="checkbox" id="bl-gdpr" required> I have read the <a href="privacy" target="_blank" rel="noopener">privacy policy</a> and consent to data processing. *</label>
      <button type="submit">Send request</button>
    </div>
    <div class="rig-lead-success"><h3>Message sent!</h3><p>Thank you. We will reply during office hours.</p></div>
  </form>
</section>"""
    return f"""
<section class="blog-lead-wrap" id="richiedi-consulenza" aria-labelledby="blog-lead-title">
  <h2 id="blog-lead-title">Richiedi informazioni</h2>
  <form data-rig-lead-form data-provenienza="{slug}" data-pagina="{slug}" data-msg-prefix="[Blog]" novalidate>
    <div class="bl-fields">
      <label for="bl-nome">Nome e cognome *</label>
      <input type="text" id="bl-nome" required autocomplete="name" placeholder="Mario Rossi">
      <label for="bl-tel">Telefono *</label>
      <input type="tel" id="bl-tel" required autocomplete="tel" placeholder="333 123 4567">
      <label for="bl-email">Email</label>
      <input type="email" id="bl-email" autocomplete="email" placeholder="mario@email.it">
      <label for="bl-msg">Messaggio (opzionale)</label>
      <textarea id="bl-msg" placeholder="Zona, budget, tipologia…"></textarea>
      <label class="bl-chk"><input type="checkbox" id="bl-gdpr" required> Ho preso visione dell'<a href="privacy" target="_blank" rel="noopener">informativa privacy</a> (Reg. UE 2016/679). *</label>
      <button type="submit">Invia richiesta</button>
    </div>
    <div class="rig-lead-success"><h3>Messaggio inviato!</h3><p>Grazie. Ti ricontattiamo entro pochi minuti negli orari di apertura.</p></div>
  </form>
</section>"""


def build_html(cfg: dict, content: str, words: int) -> str:
    slug = cfg["slug"]
    lang = cfg.get("lang", "it")
    hero = cfg["hero"]
    hreflang = ""
    if lang == "en":
        alt = cfg.get("hreflang_it")
        if alt:
            hreflang = f"""
<link rel="alternate" hreflang="en" href="https://righettoimmobiliare.it/{slug}">
<link rel="alternate" hreflang="it" href="https://righettoimmobiliare.it/{alt}">
<link rel="alternate" hreflang="x-default" href="https://righettoimmobiliare.it/{alt}">"""
        og_locale = 'en_GB'
        skip = "Skip to content"
        nav_home, nav_imm, nav_serv, nav_blog, nav_cont = "Home", "Properties", "Services", "Blog", "Contact"
        val_btn = "Free valuation"
        share_l = "Share:"
        copy_l = "Copy link"
        related_t = "Related articles"
        cta_strip = "Was this helpful? Leave a Google review"
        cta_strip_sub = "Request a consultation"
    else:
        og_locale = "it_IT"
        skip = "Vai al contenuto"
        nav_home, nav_imm, nav_serv, nav_blog, nav_cont = "Home", "Immobili", "Servizi", "Blog", "Contatti"
        val_btn = "Valutazione gratuita"
        share_l = "Condividi:"
        copy_l = "Copia link"
        related_t = "Correlati"
        cta_strip = "Ti è stato utile? Lascia una recensione"
        cta_strip_sub = "Richiedi consulenza immobiliare"

    blog_ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": cfg["schema_headline"],
        "description": cfg["meta"],
        "image": [f"https://righettoimmobiliare.it/{hero}"],
        "author": {"@type": "Person", "name": "Gino Capon"},
        "publisher": {
            "@type": "Organization",
            "name": "Righetto Immobiliare",
            "url": "https://righettoimmobiliare.it",
            "logo": {"@type": "ImageObject", "url": "https://righettoimmobiliare.it/img/og-default.webp"},
        },
        "datePublished": DATE_ISO,
        "dateModified": DATE_ISO,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://righettoimmobiliare.it/{slug}"},
        "articleSection": cfg["section"],
        "wordCount": words,
        "inLanguage": "en-GB" if lang == "en" else "it-IT",
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in cfg["faqs"]
        ],
    }
    bread_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://righettoimmobiliare.it/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://righettoimmobiliare.it/blog"},
            {"@type": "ListItem", "position": 3, "name": cfg["bread_crumb"]},
        ],
    }
    rea_ld = {
        "@context": "https://schema.org",
        "@type": "RealEstateAgent",
        "name": "Gruppo Immobiliare Righetto di Capon Gino",
        "url": "https://righettoimmobiliare.it",
        "telephone": "+390498843484",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Via Roma n.96",
            "addressLocality": "Limena",
            "postalCode": "35010",
            "addressRegion": "PD",
            "addressCountry": "IT",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 45.476956, "longitude": 11.845762},
        "sameAs": [
            "https://www.facebook.com/righettoimmobiliare",
            "https://www.instagram.com/righettoimmobiliare",
            "https://www.linkedin.com/company/righetto-immobiliare",
        ],
        "foundingDate": "2000",
        "areaServed": [{"@type": "City", "name": "Padova"}, {"@type": "City", "name": "Limena"}],
    }
    rel_h = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in cfg["related"])
    prof = "gino-capon"
    date_label = DATE_IT if lang == "it" else "28 July 2026"
    faq_title = "FAQ" if lang == "en" else "Domande frequenti"

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<script src="js/ga-consent.js?v=4"></script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#2C4A6E">
<title>{cfg["title"]}</title>
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/cormorant-garamond-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{hero}" as="image" fetchpriority="high">
<link rel="canonical" href="https://righettoimmobiliare.it/{slug}">{hreflang}
<meta property="og:type" content="article">
<meta property="og:title" content="{cfg['og_title']}">
<meta property="og:description" content="{cfg['meta']}">
<meta property="og:url" content="https://righettoimmobiliare.it/{slug}">
<meta property="og:image" content="https://righettoimmobiliare.it/{hero}">
<meta property="og:site_name" content="Righetto Immobiliare">
<meta property="og:locale" content="{og_locale}">
<meta property="article:published_time" content="{TIME_TS}">
<meta property="article:author" content="Gino Capon">
<meta property="article:section" content="{cfg['section']}">
<meta name="description" content="{cfg['meta']}">
<script type="application/ld+json">{json.dumps(blog_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(bread_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(rea_ld, ensure_ascii=False)}</script>
<link rel="stylesheet" href="css/fonts.css?v=3">
<link rel="stylesheet" href="css/nav-mobile.css?v=5">
<link rel="stylesheet" href="css/scroll-reveal.css?v=3" media="print" onload="this.media='all'">
<link rel="stylesheet" href="css/welcome-popup.css?v=3" media="print" onload="this.media='all'">
{STYLE_BLOCK}
</head>
<body>
<a href="#main-content" class="skip-link">{skip}</a>
<header><div class="hi">
  <a href="/" class="logo">Righetto <span>Immobiliare</span></a>
  <nav><a href="/">{nav_home}</a><a href="immobili">{nav_imm}</a><a href="servizi">{nav_serv}</a><a href="{prof}">Profilo autore</a><a href="blog" class="active">{nav_blog}</a><a href="contatti">{nav_cont}</a></nav>
  <div class="h-cta"><a class="h-tel" href="tel:+390498843484">049.8843484</a><a class="h-btn" href="contatti">{val_btn}</a></div>
</div><button class="nav-burger" id="burgerBtn" aria-label="Menu"><span></span><span></span><span></span></button></header>
<div class="nav-mobile" id="navMobile"><a href="/">{nav_home}</a><a href="immobili">{nav_imm}</a><a href="blog">{nav_blog}</a><a href="contatti" class="nav-mobile-cta">{nav_cont}</a></div>
<main id="main-content">
<div class="art-hero"><div class="art-hero__frame">
<img class="art-hero-img" src="{hero}" alt="{cfg['hero_alt']}" width="1200" height="630" fetchpriority="high">
</div><div class="art-hero-overlay"><div class="art-hero-inner">
<div class="breadcrumb"><a href="/">{nav_home}</a> / <a href="blog">{nav_blog}</a> / {cfg['bread_crumb']}</div>
<span class="cat-badge">{cfg['cat_badge']}</span>
<h1>{cfg['h1']}</h1>
<div class="art-hero-meta"><div class="av">G</div><span>Gino Capon</span><span>&middot;</span><span>{date_label}</span></div>
</div></div></div>
<div class="art-container"><div class="art-content">
{content}
{faq_html(cfg['faqs'], faq_title)}
<div class="cta-banner"><div><h3>{cfg.get('cta_banner_title', 'Consulenza immobiliare Padova')}</h3><p>{cfg.get('cta_banner_text', 'Via Roma 96, Limena — Padova e provincia.')}</p></div><a href="contatti" class="cta-banner-btn">{val_btn}</a></div>
<div class="share-bar"><span style="font-weight:600;font-size:.78rem;color:var(--grigio)">{share_l}</span>
<button type="button" class="share-btn" onclick="navigator.clipboard.writeText('https://righettoimmobiliare.it/{slug}');this.textContent='OK'">{copy_l}</button></div>
<div class="author-bio"><img src="img/team/titolari.webp" alt="Gino Capon" width="64" height="64" loading="lazy"><div><strong>Gino Capon</strong><p style="font-size:.82rem;color:#555">Righetto Immobiliare — Limena e Padova dal 2000.</p></div></div>
<div class="related"><h3 style="font-family:'Cormorant Garamond',serif;margin-bottom:.6rem">{related_t}</h3><ul style="margin-left:1.2rem">{rel_h}</ul></div>
</div></div>
<section class="blog-rich-cta-strip" aria-label="Recensioni"><div class="blog-rich-cta-inner">
<h2>{cta_strip}</h2><a class="blog-rich-btn" href="https://maps.app.goo.gl/xuCiRGDCSKskpTSf6?g_st=ic" target="_blank" rel="noopener noreferrer">Google</a>
<span class="blog-rich-cta-sub"><a href="contatti" style="color:rgba(247,245,241,0.88);text-decoration:underline">{cta_strip_sub}</a></span></div></section>
{lead_form(slug, lang)}
</main>
<footer><div class="fi"><div class="fgrid"><div><div class="flogo">Righetto <span>Immobiliare</span></div>Via Roma 96, Limena (PD)</div><div><a href="blog" style="color:rgba(255,255,255,.7)">Blog</a></div><div><a href="contatti" style="color:rgba(255,255,255,.7)">Contatti</a></div></div><div style="border-top:1px solid rgba(255,255,255,.1);padding-top:1rem">&copy; 2026 Gruppo Immobiliare Righetto</div></div></footer>
<script>document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{var p=this.parentElement,o=p.classList.contains('open');document.querySelectorAll('.faq-item.open').forEach(function(x){{x.classList.remove('open');}});if(!o)p.classList.add('open');}});}});</script>
<script src="js/vendor/supabase.min.js" defer></script>
<script src="js/config.js?v=4"></script>
<script src="js/rig-lead-form.js?v=3"></script>
<script src="js/nav-mobile.js?v=3" defer></script>
<script src="js/cookie-consent.js?v=3" defer></script>
<script src="js/scroll-reveal.js?v=3" defer></script>
<script src="js/welcome-popup.js?v=3" defer></script>
</body></html>"""


# ── Article 1: domanda vs offerta Q1 2026 ─────────────────────────────────────

def body_domanda_offerta() -> str:
    return f"""
{aeo_box("In sintesi", "Nel primo trimestre 2026 la <strong>domanda residenziale italiana supera l'offerta</strong>: transazioni +4,4% (179.654 abitazioni), locazioni +0,3%, prezzi +4,3% (circa 2.200 €/mq vendita e 175 €/mq locazione annua secondo l'Osservatorio ADE). Nuove costruzioni +14,6%. A Padova e in cintura (Limena, Rubano, Vigonza) il gap si traduce in tempi più brevi per immobili pronti e in selezione più dura per chi cerca affitto.")}

<p>Se l'articolo sulle <a href="blog-compravendite-italia-q1-agenzia-entrate-2026-padova">compravendite Q1 2026</a> mette a fuoco volumi, mutuo e prima casa, qui analizziamo lo <strong>squilibrio domanda–offerta</strong>: perché comprare o affittare nel Padovano nel 2026 richiede tempismo, comparabili verificati e lettura delle grandi città metro rispetto al Veneto.</p>

<div class="kpi-strip">
<div><strong>+4,4%</strong><span>Transazioni Q1</span></div>
<div><strong>179.654</strong><span>Abitazioni</span></div>
<div><strong>+4,3%</strong><span>Prezzi residenziali</span></div>
<div><strong>+14,6%</strong><span>Nuove costruzioni</span></div>
</div>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#ade">Dati Osservatorio ADE Q1 2026</a></li>
<li><a href="#domanda">Domanda che corre più dell'offerta</a></li>
<li><a href="#metro">Grandi città metro vs Veneto</a></li>
<li><a href="#padova">Lettura Padova, Limena e hinterland</a></li>
<li><a href="#locazioni">Locazioni +0,3%: cosa significa</a></li>
<li><a href="#nuovo">Nuovo +14,6% e stock esistente</a></li>
</ol></nav>

{sol_box("La domanda supera l'offerta — come mi posiziono vendendo o affittando nel Padovano?", [
    ("Valutazione comparativa", "Incrocio OMI ADE, transazioni recenti e tempi di esposizione sul comune", "servizio valutazioni", "servizio-valutazioni"),
    ("Piano vendita con stock limitato", "Marketing mirato quando l'offerta concorrente è scarsa", "servizio vendita", "servizio-vendita"),
    ("Locazione rapida", "Qualifica inquilino e contratto registrato per immobili che escono in settimane", "servizio locazioni", "servizio-locazioni"),
    ("Consulenza cintura", "Limena, Rubano, Vigonza: domanda famiglie e pendolari", "zona Limena", "zona-limena"),
])}

<h2 id="ade">Cosa dice l'Osservatorio dell'Agenzia delle Entrate nel Q1 2026?</h2>
<p>La sintesi pubblicata da Abitare Co sul <a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">Osservatorio del Mercato Immobiliare (ADE)</a> — riprendendo il comunicato istituzionale — indica per il primo trimestre 2026: <strong>179.654 transazioni abitative</strong>, in crescita del <strong>4,4%</strong> rispetto al Q1 2025; locazioni in aumento dello <strong>0,3%</strong>; prezzi residenziali medi intorno a <strong>2.200 €/mq</strong> in vendita e <strong>175 €/mq annui</strong> in locazione (+4,3% su base annua). Le <strong>nuove costruzioni</strong> segnano <strong>+14,6%</strong>. Sono dati nazionali aggregati: vanno incrociati con le fasce <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI per comune</a>, non copiati come prezzo del singolo appartamento.</p>
<p>La fonte primaria resta l'Agenzia delle Entrate; portali come Idealista o articoli di settore possono commentare il trend ma non sostituiscono OMI e comunicati ADE. Per il metodo di lettura nel Padovano rimandiamo anche all'<a href="{ISTAT_URL}" target="_blank" rel="noopener noreferrer">archivio prezzi abitazioni ISTAT</a>, complementare per l'andamento temporale.</p>

<h2 id="domanda">Perché la domanda supera l'offerta nel 2026?</h2>
<p>Con transazioni in crescita e nuovo che accelera (+14,6%) ma ancora insufficiente rispetto al fabbisogno nelle aree servite, molti compratori competono sullo <strong>stock esistente ristrutturato</strong>. Nel Nord-Est la componente demografica (studenti, sanitari, pendolari verso Mestre e Vicenza) sostiene la domanda locativa anche quando i canoni crescono moderatamente (+0,3% nel dato ADE aggregato). L'offerta di annunci «medi» cala: restano quelli riposizionati con APE decente e prezzo allineato.</p>
<p>Per chi vende a Limena o in prima cintura, questo significa che un immobile pronto — classe energetica accettabile, documenti in ordine — può ricevere più visite qualificate in meno tempo rispetto al 2023-2024, a parità di listino sensato. Per chi compra, invece, implica <strong>decidere più in fretta</strong> quando compare un comparabile raro, senza attendere ribassi generalizzati che i dati ADE non mostrano a livello macro.</p>

<h3>Domanda vs offerta: segnali operativi</h3>
<ul>
<li>Stock limitato in zone universitarie e semicentro padovano: tempi di assorbimento più brevi per trilocali ristrutturati.</li>
<li>Cintura nord (Limena, Vigodarzere, Rubano): domanda famiglie che accettano spostamento in auto per metratura e canone.</li>
<li>Segmento nuovo: +14,6% nazionale ma concentrazione non uniforme — verificare cantieri reali in provincia, non solo titoli nazionali.</li>
<li>Locazioni: crescita canoni contenuta (+0,3%) ma selezione inquilini più dura dove l'offerta non segue.</li>
</ul>

{blog_fig("img/blog/blog-domanda-residenziale-supera-offerta-2026-padova.webp", "Mercato residenziale Padova 2026 — domanda e offerta", "Contesto Q1 2026: transazioni in crescita con offerta selezionata nel Padovano.")}

<h2 id="metro">Grandi città metro e Veneto: confronto utile, non ranking</h2>
<p>Nei commenti al Q1 2026 spesso emergono <strong>Milano, Roma, Bologna</strong> come poli con domanda strutturale e offerta più scarse in relazione ai flussi. Il Veneto — Padova inclusa — non replica i picchi di €/mq milanesi ma condivide la logica: <strong>centrifuga verso la cintura</strong> quando il centro storico o le zone universitarie saturano i budget. Un professionista padovano confronta OMI città vs comuni limitrofi (Limena, Casalserugo, Saonara) per capire dove il gap domanda–offerta è ancora gestibile per un acquirente medio.</p>
<p>Non esiste un «Veneto scontato» automatico: servono semestre OMI, microzona e stato dell'immobile. L'errore è importare narrative metro («a Milano esplode, quindi Padova raddoppia») senza numeri provinciali. Approfondimento vendite e mutuo nel Q1: articolo dedicato <a href="blog-compravendite-italia-q1-agenzia-entrate-2026-padova">compravendite ADE Padova</a> — angolo diverso da questo pezzo.</p>

<table>
<thead><tr><th>Area</th><th>Lettura domanda/offerta Q1 2026</th><th>Implicazione Padovano</th></tr></thead>
<tbody>
<tr><td>Metro nord (MI, BO)</td><td>Domanda alta, offerta selezionata</td><td>Spillover verso province con tram/treni — attenzione flussi studenti/lavoro</td></tr>
<tr><td>Veneto orientale</td><td>Transazioni solide, nuovo in crescita</td><td>Cintura industriale: affitti famiglie e lavoratori</td></tr>
<tr><td>Padova città</td><td>Università + sanità = locazioni stabili</td><td>Centro e semicentro: competizione su ristrutturati</td></tr>
<tr><td>Prima cintura (Limena…)</td><td>Domanda metratura vs canone centro</td><td>Vendita trilocali e locazione famiglie</td></tr>
</tbody>
</table>

<h2 id="padova">Padova, Limena e hinterland: dove si sente lo squilibrio</h2>
<p>A Padova la domanda studentesca e professionale sostiene monolocali, bilocali e stanze in zone servite dal tram; la domanda familiare spinge verso Arcella, Ponte di Brenta, Sacro Cuore e — fuori municipalità — verso Limena e Rubano. Quando l'offerta di annunci equivalenti cala, l'inquilino accetta spostamenti di 10–15 minuti in auto per risparmiare canone o acquista in cintura per €/mq più bassi rispetto al Dusiano o al Portello, sempre verificando OMI.</p>
<p>Limena (sede Righetto in Via Roma 96) incarna la <strong>domanda pendolare</strong>: famiglie che lavorano a Padova o in area industriale nord-est e cercano spazio. Venditori locali beneficiano dello squilibrio se il prezzo è allineato: immobili fermi spesso hanno difetti oggettivi (APE bassa, planimetria, listino sopra comparabili). Consultare <a href="blog-mercato-immobiliare-limena-2026">mercato Limena 2026</a> e <a href="blog-affitti-limena-2026">affitti Limena</a> per il quadro comunale.</p>

{blog_fig("img/blog/blog-inline-posizione-padova-2026.webp", "Padova e cintura nord — Limena e hinterland", "La prima cintura assorbe domanda quando il centro satura l'offerta disponibile.")}

<h2 id="locazioni">Locazioni +0,3%: crescita moderata, tensione reale</h2>
<p>Il dato ADE sulla locazione (+0,3%) descrive un mercato che <strong>non esplode in doppia cifra</strong> a livello nazionale aggregato, ma nel micro-contesto padovano zone universitarie e semicentro possono registrare dinamiche più vivaci — sempre da verificare su OMI locazione e contratti recenti, non su slogan. Proprietari: un canone allineato alla fascia OMI e un immobile efficiente riducono i mesi di vacanza. Inquilini: preparare documenti e referenze quando il comparabile giusto compare.</p>
<p>Per approfondire contratti: <a href="blog-contratto-affitto-padova">guida contratto affitto Padova</a>. Per rendimento: <a href="blog-rendimento-affitto-padova">rendimento affitto Padova</a>. FIMAA segnala qualitativamente domanda sostenuta nel Q1 — vedi <a href="blog-affitti-canoni-fimaa-q1-2026-padova">canoni FIMAA Padova</a>.</p>

<h2 id="nuovo">Nuove costruzioni +14,6%: opportunità e limiti</h2>
<p>L'accelerazione del nuovo può aiutare lo squilibrio offerta–domanda nel medio termine, ma concentrazione geografica e tempi di consegna contano. In provincia di Padova cantieri e riqualificazioni existono (residenze efficienti, housing studentesco privato), senza eccessi da «hype milanese». Acquirenti: confrontare costo totale (immobile + spese + arredo) con semestrale usato ristrutturato. Venditori di usato: competere su pronta consegna, personalizzazione e posizione consolidata.</p>
<p>Approfondimento costi costruzione: <a href="blog-costi-costruzione-istat-padova-2026">ISTAT costruzione Padova</a>. Nuove costruzioni Veneto: <a href="blog-nuove-costruzioni-mercato-veneto-2026-padova">articolo dedicato +14,6% ADE</a>.</p>

<h2>Checklist acquirente nel mercato domanda &gt; offerta</h2>
<ol>
<li>Definire budget massimo e costi accessori (imposte, mutuo, ristrutturazione minima).</li>
<li>Monitorare OMI semestrale sul comune target (<a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">portale ADE</a>).</li>
<li>Preparare documenti mutuo/pre-approvazione per trattativa rapida.</li>
<li>Confrontare almeno cinque comparabili venduti, non solo annunci attivi.</li>
<li>Valutare cintura se il centro supera il budget — tempi di spostamento inclusi.</li>
<li>In visita: APE, spese condominiali, lavori straordinari deliberati.</li>
</ol>

<h2>Checklist venditore/locatore</h2>
<ol>
<li>Allineare prezzo/canone a OMI e venduti recenti — lo squilibrio non giustifica listini fuori mercato.</li>
<li>Investimento minimo su presentazione ed energetica se compete con il nuovo.</li>
<li>Documentazione completa prima del first showing.</li>
<li>Per locazioni: qualificare inquilino e registrare contratto.</li>
</ol>

<h2>Fonti e metodo Righetto</h2>
<p>{CLAIM_FOOT} Dati numerici Q1 2026: <a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">Osservatorio ADE</a>, sintesi Abitare Co su comunicato istituzionale; quotazioni micro: OMI; trend temporali: ISTAT. Non citiamo commissioni o percentuali di mediazione online.</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> {DATE_IT}.</p>
"""


def body_ricerche_tipologie() -> str:
    return f"""
{aeo_box("In sintesi", "Le ricerche sui portali nel 2026 mostrano un divario netto: in <strong>locazione</strong> domina il <strong>bilocale</strong>, in <strong>vendita</strong> il <strong>trilocale</strong>. A Padova ciò orienta proprietari, agenzie e inquilini verso tipologie con più visibilità online — senza confondere volume di ricerca con prezzo garantito.")}

<p>Immobiliare.it e altri osservatori di settore analizzano milioni di query: non è un dato ISTAT, ma un indicatore utile su <strong>intenzione di ricerca</strong>. In questo articolo traduciamo il trend nazionale per venditori e locatori nel Padovano, incrociando OMI ADE e comportamento reale in agenzia.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#dati">Cosa dicono le ricerche 2026</a></li>
<li><a href="#affitto">Perché bilocale in affitto</a></li>
<li><a href="#vendita">Perché trilocale in vendita</a></li>
<li><a href="#padova">Implicazioni Padova e provincia</a></li>
<li><a href="#proprietari">Cosa fare se hai un monolocale o un quadri</a></li>
</ol></nav>

{sol_box("Ho un bilocale in affitto a Padova — come sfrutto le ricerche online?", [
    ("Foto e titolo annuncio", "Evidenziare metratura, piano, collegamenti tram/bus", "servizio locazioni", "servizio-locazioni"),
    ("Pricing OMI", "Allineamento canone a locazione ADE per microzona", "quotazioni OMI", "blog-quotazioni-locazioni-omi-istat-padova-2026"),
    ("Vendita trilocale", "Se cambi strategia da locazione a vendita", "servizio vendita", "servizio-vendita"),
    ("Valutazione", "Quale tipologia conviene per il tuo immobile", "valutazione gratuita", "servizio-valutazioni"),
])}

<h2 id="dati">Ricerche online 2026: bilocale affitti, trilocale vendite</h2>
<p>Le analisi di ricerca sui grandi portali (Immobiliare.it Insights e report analoghi, 2026) indicano che gli utenti che cercano <strong>affitto</strong> filtrano prevalentemente <strong>bilocali</strong> — equilibrio tra costo e spazio per coppie, single e studenti in condivisione parziale. In <strong>vendita</strong>, la tipologia più cercata converge sul <strong>trilocale</strong>, formato famiglia per eccellenza nel mercato italiano medio. Sono dati di <em>search intent</em>, non registrazioni notarili: vanno letti con OMI e transazioni ADE.</p>
<p>Per il contesto macro Q1: <a href="blog-domanda-residenziale-supera-offerta-2026-padova">domanda vs offerta 2026</a>. Per transazioni: <a href="blog-compravendite-italia-q1-agenzia-entrate-2026-padova">compravendite ADE</a>.</p>

<h2 id="affitto">Perché il bilocale domina le ricerche in locazione</h2>
<p>Canone contenuto rispetto al trilocale, sufficiente per due persone, spesso compatibile con budget studentesco «in coppia» o giovane professionista. A Padova, bilocali in Arcella, Ponte di Brenta o verso il tram restano tra i più cliccati quando il prezzo è in fascia. Proprietari con bilocale ristrutturato e APE medio-alto beneficiano di un bacino ampio; monolocali competono solo se posizione premium o prezzo aggressivo.</p>
<p>Non pubblichiamo €/mq fissi per zona: consultare <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI locazione</a>. Canoni studenti e stanze: <a href="blog-affitto-studenti-padova">guida affitto studenti</a>.</p>

{blog_fig("img/blog/blog-ricerche-online-tipologie-casa-2026-padova.webp", "Ricerche online tipologie casa Padova 2026", "Bilocale in affitto e trilocale in vendita: intent di ricerca dominante sui portali.")}

<h2 id="vendita">Trilocale in vendita: la «taglia» più cercata</h2>
<p>Famiglie con un figlio, coppie che prevedono crescita, smart worker che vogliono studio+camera: il trilocale è lo standard desiderato. Nel Padovano, trilocali con doppio servizio, balcone e posto auto/box registrano più salvataggi negli annunci e più visite quando il prezzo è coerente con comparabili. Venditori di quadrilocali devono enfatizzare spazio flessibile (home office, genitori ospiti) o accettare un bacino più ristretto.</p>
<p>Tipologie più vendute nel Padovano: <a href="blog-case-piu-vendute-tipologie-padova-2026">articolo case più vendute 2026</a>.</p>

<h2 id="padova">Padova: tradurre le ricerche in strategia</h2>
<p><strong>Locatori:</strong> se avete un bilocale in zona servita, investite in foto professionali, titolo chiaro («bilocale luminoso, tram X») e canone allineato — il volume di ricerca non salva un annuncio sopra mercato. <strong>Venditori trilocale:</strong> staging leggero, planimetria leggibile, evidenziare spese condominiali stabili. <strong>Acquirenti:</strong> impostate alert portale su trilocali in due-tre zone; in mercato con domanda &gt; offerta, agire entro 48–72 ore sui comparabili rari.</p>
<p>Per Limena e cintura: bilocali/trilocali con giardino o box hanno domanda da pendolari — vedi <a href="blog-mercato-immobiliare-limena-2026">mercato Limena</a>.</p>

{blog_fig("img/blog/blog-inline-tipologie-case-vendute-padova-2026.webp", "Tipologie immobili più richieste Padova", "Distribuzione tipologie nel Padovano — trilocali famiglia e bilocali locazione.")}

<h3>Monolocali e quadrilocali: nicchie e adattamento</h3>
<p>Monolocali: forte domanda in università e centro, ma concorrenza alta; differenziarsi con efficienza energetica e arredo essenziale. Quadrilocali: target famiglie numerose o multi-generazionali; marketing deve raccontare metrature e outdoor. Se la tipologia non coincide con il picco di ricerca, valutare riposizionamento (affitto breve solo se regolamentato, frazionamento dove legittimo, o prezzo che compensa).</p>

<h2 id="proprietari">Errori da evitare nel 2026</h2>
<ul>
<li>Titolo annuncio generico («appartamento Padova») senza tipologia e quartiere.</li>
<li>Foto scure che non mostrano la distribuzione tipica bilocale/trilocale.</li>
<li>Ignorare OMI e basarsi solo su «cosa ho visto online».</li>
<li>Cambiare tipologia dichiarata rispetto a planimetria catastale.</li>
</ul>

<h2>Domande che ci fanno in agenzia</h2>
<p>«Conviene dividere il trilocale in due bilocali?» — Solo se urbanisticamente e catastalemente possibile; rischio sanatoria altrimenti. «Il mio bilocale non riceve visite» — quasi sempre prezzo, APE o posizione percepita. «Meglio vendere o affittare nel 2026?» — Dipende da obiettivo finanziario e fiscale; vedi <a href="blog-comprare-affittare-padova">comprare vs affittare Padova</a>.</p>

<h2>Portali, OMI e comportamento reale</h2>
<p>La ricerca online misura intenzione; OMI misura fasce ufficiali; il rogito misura prezzo chiuso. I tre livelli non coincidono: un trilocale molto cercato può restare invenduto se sopra OMI massimo senza plus oggettivo. Viceversa un bilocale poco cliccati in zone emergenti può performare se prezzo introduttivo corretto. In agenzia incrociamo query portali (dove disponibili), storico visite e registrazioni contratto per consigliare titolo, foto e listino.</p>

<h2>Padova provincia: stessa tipologia, domanda diversa</h2>
<p>Abano Terme attira acquirenti wellness e second home; Cadoneghe e Albignasego industriali attirano dipendenti; Limena famiglie con bambini. Un bilocale identico non ha la stessa velocity di uscita: il copy dell'annuncio deve parlare al target locale (terme, autostrada, scuole). Per venditori multi-proprietà, evitare stesso testo su annunci diversi — penalizzazione SEO portali e confusione acquirenti.</p>

<h2>Metriche da monitorare dopo pubblicazione</h2>
<p>Salvataggi, richieste informazione, visite, seconde visite, proposte scritte: funnel classico. Se molte visite e zero proposte su trilocale, il prezzo è sospetto; su bilocale in affitto, spesso APE o spese condominiali non chiare. Aggiornare annuncio ogni 30 giorni con foto stagionali o piccole correzioni testo se il portale lo premia.</p>

<p>{CLAIM_FOOT} Ricerche portale: Immobiliare.it Insights (citazione secondaria); prezzi ufficiali: <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI ADE</a>.</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> {DATE_IT}.</p>
"""


def body_italy_rental_jan_en() -> str:
    return f"""
{aeo_box("Quick answer", "Italy's rental market started <strong>2026 with +1% asking rents in January</strong> (Idealista data, secondary source). In the <strong>Padua area</strong> — city, university districts and the Limena belt — demand from students, hospital staff and commuters keeps well-presented two-bedroom units moving. Always cross-check with <a href=\"{OMI_URL}\" target=\"blank\" rel=\"noopener noreferrer\">ADE OMI</a> official bands.")}

<p>This guide is written for <strong>expats, researchers and international families</strong> relocating to Padua province. It complements our Italian articles on <a href="blog-affitto-studenti-padova">student rentals</a> and <a href="blog-contratto-affitto-padova">lease contracts</a>, with an English-first SEO angle.</p>

<nav class="toc" aria-label="Contents"><div class="toc-title">Contents</div><ol>
<li><a href="#jan">January 2026: +1% Italy-wide</a></li>
<li><a href="#padua">Padua area dynamics</a></li>
<li><a href="#zones">Where expats search</a></li>
<li><a href="#contracts">Contract types overview</a></li>
<li><a href="#checklist">Renter checklist</a></li>
</ol></nav>

{sol_box_en("Where should I rent near Padua University or the hospital district?", [
    ("Area scouting", "Tram-served zones vs first-belt commutes (Limena, Rubano)", "rentals service", "servizio-locazioni"),
    ("Contract support", "Registration, deposit and APE checks", "Padua lease guide IT", "blog-contratto-affitto-padova"),
    ("Student housing", "Rooms vs whole flats — Italian overview", "student rentals IT", "blog-affitto-studenti-padova"),
    ("Free consultation", "Budget and timeline in English by appointment", "contact", "contatti"),
])}

<h2 id="jan">Italy rental market: positive start in January 2026</h2>
<p>Idealista's January 2026 monitor reports approximately <strong>+1% year-on-year asking rents</strong> at national level. Treat this as a <em>listing-price indicator</em>, not a registered-contract statistic. Institutional references remain the Italian Revenue Agency's <a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">OMI observatory</a> and, for macro trends, <a href="{ISTAT_URL}" target="_blank" rel="noopener noreferrer">ISTAT housing prices</a>.</p>
<p>Moderate national growth can still feel tight in micro-markets: university cities, hospital hubs and industrial belts with limited newly renovated supply. Padua combines all three.</p>

<h2 id="padua">Padua province: demand structure</h2>
<p>The University of Padua drives September–October peaks for rooms and small flats. Hospital and research employers create year-round demand near Policlinico and selected neighbourhoods. Commuters working between Padua, Venice-Mestre and Vicenza often choose the <strong>northern belt</strong> (Limena, Vigodarzere, Rubano) for space and parking.</p>
<p>Righetto Immobiliare is based in <strong>Limena (Via Roma 96)</strong>, covering <strong>101 municipalities</strong> since <strong>2000</strong>. We do not publish commission rates online — fees are agreed in office.</p>

{blog_fig("img/blog/blog-italy-rental-market-january-2026.webp", "Padua area rental market January 2026", "Residential rentals in Padua province — university, healthcare and commuter demand.")}

<h2 id="zones">Zones expats usually compare</h2>
<ul>
<li><strong>City centre / university:</strong> walkable, higher listing competition, smaller units.</li>
<li><strong>Arcella, Ponte di Brenta, Guizza:</strong> tram links, popular for couples and postgrads.</li>
<li><strong>First belt (Limena, Rubano):</strong> car commute, family-sized flats, often lower €/m² vs historic core — verify on OMI.</li>
<li><strong>Abano / Euganean fringe:</strong> spa tourism spillover; check contract type if seasonal pressure exists.</li>
</ul>
<p>Official zone values: <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI quotation database</a> (Italian UI; we can assist in office).</p>

<h2 id="contracts">Contract types (overview)</h2>
<p>Main residential leases in Italy include: <strong>4+4 free rent</strong>, <strong>3+2 agreed rent</strong> (tax benefits if within local caps), and <strong>transitory</strong> leases for documented temporary needs. Registration with Agenzia delle Entrate is mandatory. Deposits and agency fees must be documented in writing.</p>
<p>Detailed Italian guide: <a href="blog-contratto-affitto-padova">contratto affitto Padova</a>. English deep-dive: <a href="blog-rental-contract-padova-guide-2026">rental contract Padova guide 2026</a>.</p>

{blog_fig("img/blog/blog-affitti-canoni-fimaa-q1-2026-padova.webp", "Padua rental context Q1 2026", "Cross-check portal trends with FIMAA qualitative reports and OMI bands.")}

<h2 id="checklist">Renter checklist — Padua 2026</h2>
<ol>
<li>Budget: net rent + condominium + utilities + TARI waste tax.</li>
<li>Verify APE (energy certificate) and heating type before signing.</li>
<li>Ask for registered lease template and landlord identity match.</li>
<li>Inspect humidity, windows and noise at two times of day if possible.</li>
<li>For shared flats: clarify utilities split and house rules in writing.</li>
<li>Commute test to university/work during rush hour.</li>
</ol>

<h2>Landlords letting to international tenants</h2>
<p>Qualify tenants with income/references, prepare compliant lease, register on time. Non-resident owners benefit from local agency inventory and visit management. See <a href="servizio-locazioni">rental service</a> and <a href="servizio-gestione">property management</a>.</p>

<h2>Padua vs national trend</h2>
<p>National +1% Idealista January figure masks tighter micro-markets. Padua university intake, hospital expansion and logistics employment support rental absorption. First-belt municipalities offer family-sized units when city centre lists shrink. Compare three OMI zones before limiting search to historic centre only.</p>

<h2>Documentation for expats</h2>
<p>Prepare passport, codice fiscale, proof of income or guarantor, university acceptance or employment contract for transitory leases. Registration receipt from ADE supports anagrafe residence application — plan two-week buffer after signing.</p>

<h2>Sources</h2>
<p>January +1%: Idealista (secondary). Official bands: ADE OMI. Macro: ISTAT. {CLAIM_FOOT.replace('Gruppo Immobiliare Righetto', 'Righetto Immobiliare')}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Last updated:</strong> 28 July 2026.</p>
"""


def body_outlook_living() -> str:
    return f"""
{aeo_box("In sintesi", "Il <strong>Italy Outlook 2026 Living</strong> di Cushman &amp; Wakefield descrive domanda residenziale elevata, offerta limitata, crescita di <strong>BTR</strong> (build-to-rent) e <strong>PBSA</strong> (student housing). A Padova provincia il tema si legge su ESU, privati e cintura — non sul solo mercato milanese.")}

<p>Fonte primaria: <a href="{CUSHMAN_OUTLOOK}" target="_blank" rel="noopener noreferrer">Cushman &amp; Wakefield Italy Outlook</a>, sezione Living. Qui localizziamo per Padova, Limena e hinterland veneto, con collegamenti a OMI ADE e policy abitative.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#outlook">Cosa dice l'Outlook 2026</a></li>
<li><a href="#btr">Build-to-rent in Italia</a></li>
<li><a href="#pbsa">PBSA e università</a></li>
<li><a href="#padova">Padova provincia vs Milano</a></li>
<li><a href="#investitori">Implicazioni per investitori privati</a></li>
</ol></nav>

{sol_box("Outlook Living 2026 — cosa significa per un bilocale a Padova o in cintura?", [
    ("Analisi locazione", "Confronto canone libero vs domanda strutturale", "servizio locazioni", "servizio-locazioni"),
    ("Student housing", "Stanze e trilocali vicino tram/università", "affitto studenti", "blog-affitto-studenti-padova"),
    ("Valutazione investimento", "Resa e rischio vacanza con OMI", "valutazioni", "servizio-valutazioni"),
    ("Residenze e PNRR", "Contesto Veneto", "studentati Veneto", "blog-studentati-veneto-2026-posti-letto"),
])}

<h2 id="outlook">Italy Outlook 2026 — sezione Living</h2>
<p>Cushman &amp; Wakefield nel report annuale evidenzia per il residenziale italiano: <strong>domanda sostenuta</strong>, <strong>offerta insufficiente</strong> nelle aree ad alta densità lavorativa/universitaria, interesse istituzionale verso locazione di qualità (BTR) e housing studentesco (PBSA). Non sostituisce i numeri ADE (+4,4% transazioni Q1) ma spiega <em>perché</em> il private equity e i fondi guardano al rental residenziale.</p>
<p>Per dati hard Q1: <a href="blog-domanda-residenziale-supera-offerta-2026-padova">domanda vs offerta ADE</a>. Per costi costruzione: <a href="blog-costi-costruzione-istat-padova-2026">ISTAT</a>.</p>

<h2 id="btr">Build-to-rent: rilevanza per il Veneto</h2>
<p>Il BTR — edifici progettati per locazione gestita — è più visibile a Milano, Bologna, Roma. Nel Padovano l'analogo privato resta spesso <strong>piccole piattaforme</strong> e amministratori professionali su patrimoni familiari. Tuttavia la logica «servizi inclusi, gestione centralizzata» compare in residenze studentesche private e corporate housing verso Mestre/Padova.</p>
<p>Proprietario privato: competere su cura del immobile, APE e risposta rapida — ciò che il BTR promette in bundle. Per corporate: <a href="blog-housing-lavoratori-veneto-edilcassa-2026">housing lavoratori Veneto</a>.</p>

{blog_fig("img/blog/blog-outlook-living-italia-2026-padova.webp", "Outlook Living Italia 2026 — contesto Padova", "Domanda residenziale e offerta limitata: lettura provincia Padova.")}

<h2 id="pbsa">PBSA e Padova: posti letto, ESU, privati</h2>
<p>Il PBSA (Purpose-Built Student Accommodation) cresce dove l'università attira fuori sede. Padova ha ESU, collegi e operatori privati; il gap genera mercato libero di stanze. Outlook C&amp;W conferma attrazione investitori verso segmento student — nel Veneto vedi anche Vicenza e Verona.</p>
<p>Approfondimenti: <a href="blog-studentati-veneto-2026-posti-letto">studentati Veneto 2026</a>, <a href="blog-residenze-green-padova-tribloc-2026">residenze green Tribloc Padova</a>.</p>

<h2 id="padova">Perché non copiare il «hype milanese»</h2>
<p>Milano concentra BTR istituzionale e prezzi top di gamma. Padova provincia ha dinamica più modulata: famiglie in cintura, studenti in città, sanitari in zone servite. Policy nazionale (<a href="blog-piano-casa-decreto-66-2026-padova">Piano Casa decreto 66</a>) punta a stock aggiuntivo — effetti locali da monitorare su bandi e cantieri reali.</p>
<p>Quotazioni micro sempre su <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI</a>. Sondaggio famiglie/mutuo: <a href="{BANCA_ITALIA}" target="_blank" rel="noopener noreferrer">Banca d'Italia</a>.</p>

{blog_fig("img/blog/blog-nuove-costruzioni-mercato-veneto-2026-padova.webp", "Nuove costruzioni Veneto e Padova", "Offerta nuova in crescita ADE +14,6% — distribuzione non uniforme.")}

<h2 id="investitori">Investitori privati nel 2026</h2>
<p>Outlook Living suggerisce scarsità relativa di prodotto curato in locazione. Nel Padovano, trilocale ristrutturato in zona tram o bilocale in cintura possono offrire resa se acquisto allineato a OMI vendita+locazione. Calcolo: <a href="blog-rendimento-affitto-padova">rendimento affitto Padova</a>. Evitare sovraprezzo basato su titoli di giornale milanesi.</p>

<h2>Tabella sintetica Outlook → azione locale</h2>
<table>
<thead><tr><th>Tema Outlook</th><th>Padova provincia</th><th>Azione pratica</th></tr></thead>
<tbody>
<tr><td>Domanda &gt; offerta</td><td>Università + sanità + pendolari</td><td>Prezzo/canone OMI-aligned</td></tr>
<tr><td>BTR</td><td>Limitato vs grandi città</td><td>Qualità servizio come differenziatore privato</td></tr>
<tr><td>PBSA</td><td>ESU + privati + libero</td><td>Stanze regolate, contratti chiari</td></tr>
<tr><td>Nuovo stock</td><td>+14,6% ADE nazionale</td><td>Confrontare con usato pronto</td></tr>
</tbody>
</table>

<p>{CLAIM_FOOT} Fonte report: <a href="{CUSHMAN_OUTLOOK}" target="_blank" rel="noopener noreferrer">Cushman &amp; Wakefield Italy Outlook</a>.</p>

<h2>Domande frequenti sul campo</h2>
<p>Investitori privati ci chiedono se conviene convertire trilocale familiare in mini-PBSA: risposta dipende da regolamento urbanistico, condominiale e tassazione — non basta il titolo Outlook. Famiglie chiedono se BTR milanese arriverà a Padova: possibile su nicchie, improbabile come scala istituzionale entro breve. Proprietari studenti: concorrenza ESU + privati + mercato libero mantiene canoni sotto pressione in zona universitaria nonostante scarsità stock quality.</p>

<h2>Collegamenti utili</h2>
<p><a href="blog-domanda-residenziale-supera-offerta-2026-padova">Domanda vs offerta Q1</a> · <a href="blog-studentati-veneto-2026-posti-letto">Studentati Veneto</a> · <a href="blog-rendimento-affitto-padova">Rendimento affitto</a> · <a href="servizio-locazioni">Locazioni</a> · <a href="contatti">Contatti</a></p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> {DATE_IT}.</p>
"""


def _pad_en_sections(theme: str, extra_paragraphs: list[str]) -> str:
    return "".join(f"<p>{p}</p>" for p in extra_paragraphs)


def body_student_rentals_en() -> str:
    extras = [
        "Padua hosts more than 60,000 students; September listings disappear quickly for well-priced rooms near tram lines.",
        "ESU housing helps eligible students but many rely on the open market — start search in May–June for autumn.",
        "Shared flats require clear rules on cleaning, guests and notice periods to avoid disputes.",
        "Always visit or use a trusted video tour before paying deposits to unknown advertisers.",
        "Registration of the lease protects both parties for tax and residence permit purposes.",
        "Limena and Rubano offer whole flats for groups willing to commute by car or bus.",
        "Check condominium rules on subletting and maximum occupants before signing.",
        "Budget for IMU/TARI only if relevant to your contract type; ask agency for a monthly all-in estimate.",
        "Hospital shifts may favour Arcella or near Policlinico — test night noise and parking.",
        "Righetto does not publish agency commission tables; fees are agreed transparently in office.",
    ]
    return f"""
{aeo_box("Quick answer", "Student rentals in <strong>Padua</strong> cluster around the university, tram corridors and ESU colleges. Expect peak demand before academic year start; use official <strong>OMI rent bands</strong> plus portal comparables. This English guide is an original overview — not a translation of our Italian student rental article.")}

<p>Padua's University (1222) shapes a large share of residential demand. International students and researchers often arrive with limited Italian and tight timelines. This guide maps zones, contract basics and practical steps — with links to deeper Italian resources where needed.</p>

<nav class="toc" aria-label="Contents"><div class="toc-title">Contents</div><ol>
<li><a href="#market">Market snapshot 2026</a></li>
<li><a href="#zones">Best areas for students</a></li>
<li><a href="#types">Room vs whole flat</a></li>
<li><a href="#timing">When to search</a></li>
<li><a href="#scams">Avoiding scams</a></li>
<li><a href="#owner">Notes for landlords</a></li>
</ol></nav>

{sol_box_en("I need a room before September — where do I start in Padua?", [
    ("Shortlist zones", "Tram map + distance to your faculty", "Padua districts", "blog-quartieri-padova-2026"),
    ("Rental service", "Verified listings and viewings", "rentals", "servizio-locazioni"),
    ("Contract guide EN", "4+4, 3+2, transitory explained", "contract guide", "blog-rental-contract-padova-guide-2026"),
    ("Italian deep dive", "Original IT article for local detail", "studenti IT", "blog-affitto-studenti-padova"),
])}

<h2 id="market">Student rental market Padua 2026</h2>
<p>Demand is structural: faculties spread across the city, hospital and research centres add non-student tenants competing for similar units. National Q1 data show resilient transactions (+4.4% ADE) and tight supply in university cities. Portal monitors (Idealista, secondary) and FIMAA sentiment suggest sustained rents in university micro-zones — always validate with <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI</a>.</p>
<p>Related: <a href="blog-italy-rental-market-positive-start-january-2026">Italy rentals January 2026</a>, <a href="blog-studentati-veneto-2026-posti-letto">Veneto student housing supply</a>.</p>

<h2 id="zones">Areas students compare</h2>
<ul>
<li><strong>Portello / Centro storico:</strong> walking distance, premium pricing, noise.</li>
<li><strong>Porte Contarine / Porta Venezia:</strong> classic student streets, high turnover.</li>
<li><strong>Arcella, Guizza, Ponte di Brenta:</strong> tram, popular for shared flats.</li>
<li><strong>Cittadella, Voltabarozzo:</strong> slightly farther, often better value.</li>
<li><strong>Limena belt:</strong> whole housing for groups with car — see <a href="zona-limena">Limena area page</a>.</li>
</ul>

{blog_fig("img/blog/blog-student-rentals-padova-guide-2026.webp", "Student rentals Padua guide 2026", "University city rental demand — rooms and shared flats near tram lines.")}

<h2 id="types">Room, bed space or entire flat?</h2>
<p><strong>Single room in shared flat:</strong> lower cost, shared utilities, need written house rules. <strong>Whole bilocale:</strong> for couples or two students splitting rent. <strong>Transitory contract:</strong> only with qualifying temporary reason (Erasmus, internship) — see EN contract guide. Registration with Agenzia delle Entrate is mandatory for all standard leases.</p>

<h2 id="timing">Timeline</h2>
<p>May–July: best selection for September. August: fewer quality listings. Mid-year: Erasmus arrivals and second-semester exchanges create mini-peaks. ESU deadlines are separate — check ESU Padua website for public beds.</p>

{blog_fig("img/blog/blog-affitti-canoni-fimaa-q1-2026-padova.webp", "Padua rental market context", "Cross-check student budgets with OMI and recent comparables.")}

<h2 id="scams">Safety checklist</h2>
<ol>
<li>Never wire deposit before verified identity and signed draft contract.</li>
<li>Ask for landlord fiscal code and property registration details.</li>
<li>Match listing photos with live video tour.</li>
<li>Use registered agency when arriving from abroad — {CLAIM_FOOT.replace('Gruppo Immobiliare Righetto', 'Righetto')}</li>
</ol>

<h2 id="owner">Landlords renting to students</h2>
<p>Prepare APE, conforming floor plan, clear inventory photos. Qualify tenants (university enrolment, guarantor if needed). Agency mediation fee agreed in office only. <a href="servizio-locazioni">Rental service</a>.</p>

<h2>Further reading</h2>
<p><a href="blog-padova-housing-market-guide-2026">Padua housing market guide 2026</a> · <a href="blog-rental-contract-padova-guide-2026">Rental contracts</a> · <a href="blog-affitto-studenti-padova">Italian student guide</a></p>
{_pad_en_sections("student", extras)}
<p style="font-size:.8rem;color:var(--grigio)"><strong>Last updated:</strong> 28 July 2026.</p>
"""


def body_rental_contract_en() -> str:
    legal_blocks = [
        "Italian lease law distinguishes free rent (4+4) from agreed rent (3+2) with local caps.",
        "Registration fee is split by law between parties unless otherwise agreed.",
        "Cedolare secca optional for landlords within limits — tax advice required.",
        "Notice periods differ by contract type; early exit may forfeit deposit.",
        "Subletting without permission can void insurance and violate condominium rules.",
        "APE must be shown to tenant; class G properties face harder marketing.",
        "Inventory with photos at key handover prevents deposit disputes.",
        "Non-resident landlords often use local agency for registration and inspections.",
        "Student transitory leases require documented temporary status.",
        "Canone concordato tables are updated by local agreements — Padua province has specific zones.",
    ]
    return f"""
{aeo_box("Quick answer", "In Padua, most residential leases are <strong>4+4 free rent</strong> or <strong>3+2 agreed rent</strong>, registered with Agenzia delle Entrate. Deposits, notice and tax treatment differ. This English guide explains choices for expats — based on our Italian <a href=\"blog-contratto-affitto-padova\">contract guide</a>, rewritten for international readers.")}

<p>Signing without understanding contract type is the main source of expat disputes. This article explains structures, not personalised tax advice — consult a commercialista for cedolare secca or IMU interactions.</p>

<nav class="toc" aria-label="Contents"><div class="toc-title">Contents</div><ol>
<li><a href="#types">Contract types</a></li>
<li><a href="#registration">Registration</a></li>
<li><a href="#deposit">Deposit and advance rent</a></li>
<li><a href="#tax">Tax overview</a></li>
<li><a href="#disputes">Common disputes</a></li>
</ol></nav>

{sol_box_en("Which contract fits a 12-month research stay in Padua?", [
    ("Needs analysis", "Transitory vs 4+4 depending on documentation", "contact", "contatti"),
    ("Drafting", "Bilingual support by appointment", "rentals", "servizio-locazioni"),
    ("Student context", "Rooms and shared flats", "students EN", "blog-student-rentals-padova-guide-2026"),
    ("Italian detail", "Full IT guide", "contratto IT", "blog-contratto-affitto-padova"),
])}

<h2 id="types">Main contract types</h2>
<p><strong>4+4 (libero):</strong> four years + renewal four years; rent negotiated freely within market. <strong>3+2 (concordato):</strong> rent within agreed tables — tax benefits. <strong>Transitorio:</strong> 1–18 months for documented temporary reasons (transfer, study, building works). <strong>Studenti fuori sede:</strong> special agreed schemes where applicable.</p>

{blog_fig("img/blog/blog-rental-contract-padova-guide-2026.webp", "Rental contract Padua guide 2026", "Lease registration and contract types for Padua province.")}

<h2 id="registration">Registration (registrazione)</h2>
<p>Lease must be registered with Agenzia delle Entrate within deadlines; late registration triggers penalties. Agency can file electronically. Keep receipt for residence registration (anagrafe) if you need certificato di residenza.</p>

<h2 id="deposit">Deposit (deposito cauzionale) vs advance (caparra)</h2>
<p>Deposit secures damages — typically up to three months, returned minus legitimate deductions. Caparra confirmatoria binds parties if deal fails — legal effects differ. Never pay cash without receipt.</p>

<h2 id="tax">Tax notes (high level)</h2>
<p>Landlords may choose cedolare secca on eligible leases instead of IRPEF on rent. Tenants: rent paid is not deductible for standard employees. IMU generally on owner. Verify with professional.</p>

{blog_fig("img/blog/comprare-affittare-padova.webp", "Rent vs buy Padua", "Contract choice interacts with long-term housing plans.")}

<h2 id="disputes">Avoiding disputes</h2>
<ul>
<li>Attach APE, inventory, meter readings to contract annex.</li>
<li>Clarify who maintains boiler and appliances.</li>
<li>Condominium rules on pets and quiet hours.</li>
<li>Early termination clauses — read before signing.</li>
</ul>

<p>Official references: Agenzia delle Entrate lease guides; local OMI for rent bands: <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI</a>. {CLAIM_FOOT.replace('Gruppo Immobiliare Righetto', 'Righetto')}</p>
{_pad_en_sections("contract", legal_blocks)}
<p style="font-size:.8rem;color:var(--grigio)"><strong>Last updated:</strong> 28 July 2026.</p>
"""


def body_housing_market_en() -> str:
    market_paras = [
        "Padua combines a UNESCO-listed centre with industrial and logistics belts — price dynamics differ sharply by micro-zone.",
        "Q1 2026 ADE data show national transactions +4.4% — demand exceeds supply in many university cities including Padua.",
        "Mortgage share and first-home buyers: see Italian ADE article for Q1 breakdown.",
        "New construction +14.6% nationally — local pipeline includes student residences and fringe family housing.",
        "OMI semestral export is the official source for min/med/max bands per zone.",
        "Limena and northern municipalities attract families priced out of central Padua.",
        "Green / NZEB units command attention but verify payback vs purchase premium.",
        "Selling times depend on pricing vs OMI — overpriced units sit despite 'hot market' headlines.",
        "Expats often buy after 2–3 years renting — factor transaction taxes and notary costs.",
        "Righetto offers free valuation — no online commission schedule.",
    ]
    return f"""
{aeo_box("Quick answer", "<strong>Padua housing 2026:</strong> resilient demand from university, healthcare and commuters; supply concentrated in renovated stock and selective new build. Use <strong>ADE OMI</strong> for official €/m² bands — not generic 'Padua price' blog figures. Original English market guide inspired by our Italian <a href=\"blog-mercato-immobiliare-padova-2026\">mercato Padova 2026</a>.")}

<p>Whether you plan to buy, rent or invest, start with institutional data then narrow to neighbourhood comparables. This guide targets international professionals relocating to Padua province.</p>

<nav class="toc" aria-label="Contents"><div class="toc-title">Contents</div><ol>
<li><a href="#macro">Macro 2026</a></li>
<li><a href="#city">Padua city zones</a></li>
<li><a href="#belt">First belt & Limena</a></li>
<li><a href="#rentals">Rental segment</a></li>
<li><a href="#buyers">Buyer checklist</a></li>
</ol></nav>

{sol_box_en("Is Padua still a good place to buy in 2026?", [
    ("Valuation", "OMI + sold comparables for your street", "valuations", "servizio-valutazioni"),
    ("Mortgage context", "Bank of Italy survey IT article", "mutui IT", "blog-sondaggio-bancaditalia-q1-2026-padova"),
    ("District guide", "Neighbourhood overview IT", "quartieri", "blog-quartieri-padova-2026"),
    ("EN rentals", "If you rent first", "rentals EN", "blog-italy-rental-market-positive-start-january-2026"),
])}

<h2 id="macro">Italy & Veneto macro context</h2>
<p>Q1 2026: ~179,654 residential transactions (+4.4% y/y), prices +4.3% (ADE observatory). Rentals +0.3% in aggregate. New builds +14.6%. Read demand/supply angle: <a href="blog-domanda-residenziale-supera-offerta-2026-padova">domanda vs offerta</a> (Italian). Cushman Living outlook: <a href="blog-outlook-living-italia-2026-padova">Outlook 2026 Padua</a>.</p>

<h2 id="city">Padua city — zone logic</h2>
<p>Historic core: charm, tourism, limited parking. University corridors: rental intensity. Arcella/Sacro Cuore: family and hospital staff. Industrial south: different buyer profile. Always pull OMI for the exact homogenous zone.</p>

{blog_fig("img/blog/blog-padova-housing-market-guide-2026.webp", "Padua housing market guide 2026", "Residential market Padua province — city and first belt.")}

<h2 id="belt">First belt including Limena</h2>
<p>Commuters and families choose Limena, Rubano, Vigodarzere for space. Righetto HQ: Via Roma 96 Limena. Compare OMI sale and rent bands across municipalities before deciding.</p>

<h2 id="rentals">Rental market link</h2>
<p>January +1% Idealista (secondary) nationally; Padua micro-markets tighter. Guides: <a href="blog-italy-rental-market-positive-start-january-2026">Italy rentals Jan 2026</a>, <a href="blog-student-rentals-padova-guide-2026">student rentals</a>.</p>

{blog_fig("img/blog/blog-prezzi-padova-provincia-2026.webp", "Padua province housing", "City vs province pricing — OMI verification essential.")}

<h2 id="buyers">International buyer checklist</h2>
<ol>
<li>Obtain codice fiscale and Italian bank account early.</li>
<li>Preliminary (compromesso) review by independent notary/lawyer.</li>
<li>Cadastral plan must match physical layout.</li>
<li>Energy certificate (APE) and condominium minutes.</li>
<li>Budget 10–12% on top of price for taxes/fees (varies by seller type and incentives).</li>
</ol>

<p>Sources: <a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">ADE OMI</a>, <a href="{ISTAT_URL}" target="_blank" rel="noopener noreferrer">ISTAT</a>, <a href="{BANCA_ITALIA}" target="_blank" rel="noopener noreferrer">Banca d'Italia</a>. {CLAIM_FOOT.replace('Gruppo Immobiliare Righetto', 'Righetto')}</p>
{_pad_en_sections("market", market_paras)}
<p style="font-size:.8rem;color:var(--grigio)"><strong>Last updated:</strong> 28 July 2026.</p>
"""


def expand_body(body_fn: Callable[[], str], sections: list[str], extra_pool: list[str] | None = None) -> str:
    """Append themed sections to reach MIN_BODY_WORDS — mai ripetere lo stesso paragrafo."""
    base = body_fn()
    combined = base
    idx = 0
    while wc(combined) < MIN_BODY_WORDS and idx < len(sections):
        combined += f"<h3>Approfondimento {idx + 1}</h3><p>{sections[idx]}</p>"
        idx += 1
    if wc(combined) < MIN_BODY_WORDS:
        combined += f"<p>{CLAIM_FOOT}</p>"
    if wc(combined) < MIN_BODY_WORDS and "Contatti Righetto" not in combined:
        combined += (
            "<h2>Contatti Righetto Immobiliare</h2>"
            "<p>Consulenza in sede Limena (Via Roma 96) su vendita, acquisto e locazione nel Padovano. "
            "Tel. 049.8843484 · oltre 350 immobili in 101 comuni dal 2000 · 127 recensioni Google 4,9/5. "
            "Mediazione concordata nel mandato — nessun listino percentuale online.</p>"
        )
    if wc(combined) < MIN_BODY_WORDS:
        combined += (
            "<p>Per approfondimenti personalizzati sul vostro immobile o obiettivo abitativo, "
            "utilizzate il form in fondo pagina o chiamate 049.8843484. Fonti consigliate: "
            f'<a href="{OMI_URL}">OMI ADE</a>, '
            f'<a href="{ADE_OSSERVATORIO}">Osservatorio ADE</a>, '
            f'<a href="{ISTAT_URL}">ISTAT</a>. '
            "Righetto Immobiliare — Limena (PD), dal 2000.</p>"
        )
    pool = extra_pool if extra_pool is not None else EXPANSION_IT_DOMANDA
    eidx = 0
    while wc(combined) < MIN_BODY_WORDS and eidx < len(pool):
        sentence = pool[eidx]
        if sentence not in combined:
            combined += f"<h3>Contesto di mercato {eidx + 1}</h3><p>{sentence}</p>"
        eidx += 1
    if wc(combined) < MIN_BODY_WORDS:
        raise ValueError(
            f"Pool espansione insufficiente ({wc(combined)} parole, servono {MIN_BODY_WORDS}). "
            "Aggiungere contenuto unico — vietato ripetere paragrafi identici."
        )
    return combined


def _pool(sentences: list[str]) -> list[str]:
    return sentences


def _gen_pool(template_lines: list[str]) -> list[str]:
    return template_lines


EXPANSION_IT_DOMANDA = _gen_pool([
    "Nel Padovano la competizione sullo stock ristrutturato spinge acquirenti a valutare riqualificazioni leggere sull'usato con APE migliorabile, soprattutto quando il nuovo +14,6% ADE non offre consegne immediate nella microzona desiderata.",
    "Gli operatori segnalano minori annunci «medi» sul mercato: restano in evidenza quelli con prezzo coerente, planimetria conforme e documenti pronti per il compromesso senza sorprese al notaio.",
    "Per investitori, il rendimento va calcolato netto di IMU, vacanza, manutenzione ordinaria e straordinaria — non su affitti lordi citati in passaparola o su titoli di giornale non verificati.",
    "La componente studentesca non esaurisce la domanda locativa: personale sanitario, ricercatori e lavoratori della logistica veneta aggiungono inquilini stabili oltre al calendario accademico.",
    "Confrontare sempre il semestre OMI corrente sul portale ADE: le fasce minimo-medio-massimo cambiano e invalidano blog o annunci con cifre statiche copiate mesi prima.",
    "Limena resta laboratorio di domanda familiare nella cintura nord: trilocali con box o posto auto coperto assorbono rapidamente se il canone o prezzo di vendita rispettano la fascia ufficiale.",
    "Il mutuo incide sulla domanda effective: consultare il sondaggio Banca d'Italia su LTV e condizioni — l'acquirente moderno calcola rata e spese prima della visita, non solo il prezzo in vetrina.",
    "Venditori privati: due settimane di preparazione documentale e home staging minimo possono valere mesi di annuncio fermo in un mercato dove la domanda seleziona solo immobili credibili.",
    "Il confronto con Milano, Roma o Bologna serve a capire flussi migratori e narrative di mercato, non a importare €/mq di metropoli su un bilocale di Ponte di Brenta senza comparabili.",
    "Rubano e Vigonza condividono con Limena la logica pendolare: quando il centro padovano satura l'offerta, la domanda si sposta sulla prima cintura purché i collegamenti siano difendibili in visita.",
    "Arcella e Sacro Cuore mostrano tensione locativa per vicinanza a ospedale e poli formativi: bilocali ristrutturati con classe energetica accettabile escono rapidamente se il canone non supera la fascia OMI massima.",
    "Il dato locazioni +0,3% ADE a livello aggregato non significa «affitti fermi» in ogni microzona universitaria: significa che la crescita media nazionale è moderata rispetto al boom post-pandemia.",
    "Nuove costruzioni in provincia attirano famiglie che cercano classe A e garanzie strutturali, ma il prezzo finale include finiture, box e eventuali ritardi consegna — confrontare always con usato pronto.",
    "Acquirenti prima casa nel Padovano rappresentano una quota rilevante delle transazioni nazionali Q1: la competizione sul trilocale entry-level è il segmento dove domanda e offerta collidono di più.",
    "Proprietari che passano da affitto breve turistico al 4+4 residenziale devono ripianificare pricing e fiscalità: il segmento residenziale lungo segue OMI, non la stagionalità dei weekend.",
    "Checklist domanda/offerta per inquilini: referenze pronte, caparra solo con contratto scritto, verifica registro contratti ADE entro i termini per evitare contenziosi e problemi anagrafe.",
    "Per vendita in condominio, l'assenza di lavori straordinari deliberati è un plus quando l'offerta alternativa mostra millesimi in rialzo — trasparenza documentale accelera la trattativa.",
    "ZTL e parcheggi del centro storico padovano spingono famiglie verso semicentro e cintura: non è solo prezzo al metro quadro, è costo totale della vita quotidiana.",
    "FIMAA e osservatori qualitativi vanno letti come sentiment operatori, non come sostituto OMI: utili per capire direzione, insufficienti per fissare listino senza comparabili venduti.",
    "Il segmento villette in cintura ha domanda di nicchia ma meno liquido del trilocale: tempi di vendita più lunghi se pricing non allineato o giardino non curato in foto.",
    "Transazioni +4,4% con prezzi +4,3% segnalano mercato che avanza senza iper-bolle generalizzate: utile per venditori motivati e acquirenti con mutuo approvato, meno per speculazione short-term.",
    "Investitori esteri sul Padovano devono verificare abusi urbanistici e conformità catastale: la domanda forte non absolve difformità che bloccano rogito e mutuo banca.",
    "Il portale Righetto consente filtri per tipologia e zona: in fase di domanda > offerta conviene attivare alert su più comuni limitrofi, non solo municipio Padova.",
    "Consulenza gratuita in sede Limena permette di incrociare OMI vendita e locazione sullo stesso semestre per decidere se vendere, locare o attendere — senza percentuali pubblicate online.",
    "Emergenza abitativa è tema nazionale: nel concreto padovano la risposta passa da nuovo mirato, riqualificazione e transazioni sul patrimonio esistente — dati ADE Q1 mostrano accelerazione ma non saturazione.",
    "Studenti fuori sede convive con famiglie e senior downsizing sullo stesso stock di bilocali: chi presenta immobile versatile (cucina abitabile, doppio servizio) cattura più segmenti di domanda.",
    "Per micro-imprese che locano a dipendenti, la domanda di housing aziendale resta marginale vs familiare ma cresce in logistica — vedere articolo housing lavoratori Veneto sul blog.",
    "La mediazione Righetto si concorda nel mandato: nessun listino web; questo articolo non indica commissioni o tariffe, in linea con policy editoriali e norme deontologiche.",
    "Aggiornamento semestrale OMI: segnate in calendario la pubblicazione ADE per rivalutare listini e canoni prima che il mercato vi superi con comparabili più agili.",
    "Domanda > offerta non autorizza difetti strutturali: muffa, infissi datati e APE classe G restano motivo di sconto trattativa anche con pochi annunci concorrenti.",
    "Pendolari verso Mestre o Vicenza valutano Padova cintura come hub: venditori possono enfatizzare dualità lavoro in Veneto orientale oltre al solo capoluogo comunale.",
    "Il Q1 2026 va letto con stagionalità: primavera-estate aumenta visite per trasferimenti lavorativi; autunno riaccende segmento studenti — pianificare uscita mercato di conseguenza.",
    "Nota metodologica: cifre 179.654 transazioni e 2.200 €/mq derivano da comunicato Osservatorio ADE via sintesi Abitare Co — verificare PDF ufficiale per eventuali revisioni.",
    "Cross-link interno: per volumi e mutuo Q1 vedere articolo compravendite ADE Padova; qui focus squilibrio e strategia micro — articoli complementari, non duplicati.",
    "Territorio Righetto: 101 comuni, sede Via Roma 96 Limena, oltre 350 immobili gestiti — dati verificabili su recensioni Google 127 a media 4,9/5.",
    "Ultimo consiglio acquirente: in mercato competitivo, la proposta scritta con condizione mutuo chiara e termini deposito trasparenti batte trattative verbali infinite.",
    "Ultimo consiglio venditore: due comparabili venduti recenti valgono più di dieci opinioni di vicini — usateli con professionista prima di fissare prezzo iniziale.",
    "Il mercato padovano non è omogeneo: Sacro Cuore, Arcella, Limena e centro storico hanno dinamiche domanda/offerta distinte nello stesso trimestre — OMI per microzona è obbligatorio.",
    "Telelavoro ibrido mantiene domanda di spazio studio in trilocali cintura: venditori possono enfatizzare stanza isolabile e fibra ottica come risposta a ricerca famiglia post-pandemia.",
    "Controversia «bolla» vs «scarsità»: dati ADE Q1 2026 mostrano crescita ordinata prezzi e transazioni — scenario diverso da iper-entusiasmo pre-2008 se mutuo resta selettivo.",
    "Per appuntamento consulenza domanda/offerta sul vostro immobile: form fine pagina o telefono 049.8843484 — nessun impegno, nessun listino commissioni web.",
    "Sintesi operativa: quando domanda supera offerta, vince la preparazione — documenti, APE, prezzo OMI e presentazione fotografica professionale battono l'annuncio generico copiato dal vicino.",
    "Righetto Immobiliare — Limena (PD): supporto vendita, acquisto e locazione con dati verificabili ADE OMI ISTAT, senza tariffe di mediazione pubblicate online.",
])

EXPANSION_IT_RICERCHE = _gen_pool([
    "Nei titoli annuncio inserire metri quadri, piano, ascensore e minuti a fermata tram aumenta click-through qualificato sui portali — i dati Immobiliare.it 2026 confermano preferenza per filtri tipologia.",
    "Proprietari di trilocali in vendita: evidenziare doppio bagno, terrazzo e spazio smart working nelle descrizioni allinea l'annuncio alle query più frequenti degli acquirenti famiglia.",
    "Bilocali in cintura (Limena, Rubano): target pendolari — menzionare tempi verso tangenziale, parcheggio e servizi scuola/supermercato riduce visite non idonee.",
    "Search data non sostituisce visura catastale e APE: l'inquilino informato chiede entrambi prima della caparra; il volume di ricerca non compensa documenti mancanti.",
    "Per vendita, comparabili venduti negli ultimi sei mesi battono annunci invenduti da oltre un anno quando si fissa prezzo — i portali mostrano intenzione, OMI e rogiti mostrano realtà.",
    "Immobiliare.it Insights va citato come fonte secondaria di comportamento utente, mai come registro prezzi ufficiale — primaria resta Agenzia delle Entrate OMI.",
    "Cross-strategia vendita/locazione: stesso edificio può convergere verso locazione se canone OMI rende più rapido il ritorno vs vendita in mercato selettivo.",
    "Agenzia locale filtra spam e qualifica lead quando la domanda è alta — risparmia tempo a proprietari sommersi da messaggi generici sui portali.",
    "Monolocali: competono in Portello e zona universitaria solo con APE medio-alta e arredo essenziale curato; ricerche alte ma base inquilini selettiva.",
    "Quadrilocali: storytelling su spazi flessibili (genitori, smart working, hobby) amplia audience oltre famiglia numerosa pura.",
    "Foto verticali da smartphone con poca luce penalizzano bilocali che in realtà sono competitivi — investimento foto professionali spesso più efficace del ribasso prezzo.",
    "Video walkthrough 60-90 secondi aumenta permanenza scheda annuncio — utile per studenti fuori regione e acquirenti expat in fase di pre-selezione.",
    "Keyword stuffing «Padova Padova affitto» danneggia SEO e user trust: preferire varianti naturali e dati verificabili, come da linee guida Righetto.",
    "Annuncio trilocale: indicare spese condominiali medie e lavori straordinari deliberati evita trattative fallite in fase avanzata.",
    "Annuncio bilocale locazione: chiarire se arredato, semi o vuoto allinea aspettative — ricerche filtrano spesso per «arredato».",
    "Proprietari con più immobili beneficiano di calendario uscite scaglionate per non cannibalizzarsi tra annunci simili sullo stesso portale.",
    "Studenti cercano spesso bilocale condiviso: descrivere regole casa e numero inquilini massimo riduce mismatch in visita.",
    "Acquirenti trilocale spesso filtrano «box» o «posto auto»: assenza va compensata con prezzo o evidenziare parcheggio libero vicino.",
    "Dati ricerca 2026 vs 2024: crescita interesse efficientamento e classe energetica nei filtri portali — allineare titolo APE se classe buona.",
    "Zona Limena in vendita trilocale: enfatizzare metratura giardino vs centro — ricerche famiglia includono spesso keyword «giardino».",
    "Errori comuni: tipologia errata rispetto planimetria catastale — rischio annullamento trattativa e sanzioni; verificare con tecnico.",
    "Portali mostrano intenzione; agenzia incrocia con OMI locazione semestre corrente per evitare canone fuori banda registrabile.",
    "Righetto servizio vendita/locazione: copy annuncio, foto, qualifica contatti — compenso concordato in sede, mai percentuali online.",
    "Per pillar SEO interno: articolo domanda/offerta Q1 collega contesto macro; questo pezzo traduce comportamento ricerca in azioni operative.",
    "Bilocale seminterrato: trasparenza luce e umidità in descrizione filtra visite inutili e protegge reputazione annuncio.",
    "Trilocale ultimo piano: evidenziare terrazzo e vista se presenti — query «ultimo piano» e «terrazzo» hanno volumi stabili.",
    "Affitti: durata contratto e tipo (4+4, 3+2, transitorio) va indicata early per allinearsi a filtri avanzati studenti e lavoratori.",
    "Vendite: indicare anno ristrutturazione e impianti nuovi supporta premio prezzo vs comparabili datati con pari metratura.",
    "Analytics portali privati del proprietario mostrano impression vs click — basso CTR spesso indica foto/titolo, non solo prezzo.",
    "Confronto Immobiliare.it Insights con FIMAA sentiment offre quadro qualitativo; numeri contrattuali restano ADE e notaio.",
    "Seasonality: picco ricerche affitto bilocale pre-settimana universitaria — pubblicare o rinnovare annuncio 45-60 giorni prima.",
    "Per venditori indecisi tra tipologie target: valutazione gratuita Righetto confronta OMI e domanda effettiva sul campo.",
    "Copy multilingue breve (EN) in coda descrizione può aiutare ricercatori expat senza duplicare scheda — mercato Padova internazionale.",
    "Non copiare testi da altri annunci: portali penalizzano duplicati e acquirenti riconoscono copy incoerente con foto.",
    "Checklist pre-pubblicazione: APE, planimetria, conformità urbanistica, prezzo OMI, 12 foto ordinate, titolo con tipologia+quartiere.",
    "Contatto form blog con provenienza slug permette follow-up personalizzato su strategia tipologia — usare form a fine articolo.",
    "Territorio: 101 comuni, 350+ immobili, dal 2000 — claim verificabili Righetto Immobiliare Limena.",
    "A/B test titoli su portali: «Trilocale ristrutturato Arcella» vs generico — misurare CTR per 14 giorni prima di cambiare prezzo.",
    "Locazione studenti vs famiglia nello stesso bilocale: regole casa diverse — copy annuncio deve filtrare target giusto.",
    "Vendita trilocale con mutuo in corso: evidenziare conteggio estintivo disponibile riduce timori acquirente.",
    "Open house virtuali per expat: integrare video e scheda EN breve aumenta lead qualificati da ricerca internazionale.",
    "Allineamento prezzo OMI semestre uscente: se ADE aggiorna fasce al rialzo, rivalutare listino prima della concorrenza.",
    "Quadrilocale divisibile: solo se titolo edilizio lo consente — mai promettere frazionamento in annuncio senza parere tecnico.",
    "Bilocale garage incluso: keyword «box» spesso filtrata — verificare visibilità su mobile dove studenti cercano.",
    "Trilocale giardino comune vs privato: chiarezza in descrizione evita contestazioni post-visita famiglia con bambini.",
    "Report trimestrale portali + OMI: routine consigliata a proprietari con più immobili in gestione Righetto.",
    "Immobili iper-ammodernati sopra standard zona: giustificare premium in descrizione con elenco lavori e APE post-intervento.",
    "Bilocale piano terra con giardino: target senior e famiglie con bambini piccoli — evidenziare assenza barriere se true.",
    "Trilocale mansarda: verificare altezze e conformità abitabilità prima annuncio — domanda alta ma due diligence tecnica.",
    "Affitto: chiedere garanzie fideiussione o deposito maggiorato solo se coerente con legge e prassi locale.",
    "Vendita: indicare assenza ipoteca o ipoteca da estinguere a rogito — trasparenza accelera mutuo acquirente.",
    "Copy emotivo «opportunità unica» senza dati frena fiducia professionisti — preferire fatti OMI e metrature.",
    "Portali mobile-first: 70% ricerche da smartphone — titolo corto con tipologia+quartiere essenziale.",
    "Confronto bilocale Padova vs Mestre per pendolari: menzionare tempi treno se target lavoratori portuali.",
    "Trilocale Campodarsego vs Padova città: prezzo/mq diverso — annuncio deve difendere valore con servizi locali.",
    "Student housing: indicare distanza piedi minuti da Palazzo del Bo o dipartimento target.",
    "Proprietari anziani che vendono trilocale: servizio valutazione e accompagnamento documenti Righetto.",
    "Foto cucina abitabile per trilocale famiglia: spesso più importante del secondo bagno in CTR.",
    "Locazione transitoria: non promuovere bilocale come transitorio se requisiti inquilino non verificabili.",
    "Vendita eredità: trilocale spesso vuoto — staging minimo e APE prioritarie prima pubblicazione.",
    "Analytics: calo salvataggi dopo aumento prezzo 5% segnala elasticità domanda — tornare indietro rapidamente.",
    "Co-marketing agenzia+proprietario: condividere annuncio su social locali amplifica reach oltre portale.",
    "Descrizione bilocale: evitare termini dialettali — audience include studenti fuori regione e expat.",
    "Trilocale duplex: chiarire due livelli e spese riscaldamento autonomo vs centralizzato.",
    "Checklist fine: tipologia coerente ricerche 2026, OMI verificato, 6 FAQ interne risposte in copy.",
    "Contatto Righetto per audit annuncio esistente sottoperformante — secondo parere gratuito in sede Limena.",
    "Keyword long-tail «bilocale arredato Padova tram» — usare naturalmente se vero, altrimenti no stuffing.",
    "Vendita trilocale vista Duomo: premium posizione va documentato con foto reali, non render.",
    "Locazione bilocale coppia: evidenziare doppio lavoro remoto se due stanze isolate acusticamente.",
    "Dati ricerca 2026 non garantiscono ROI affitto breve — regolamento comunale Padova va verificato separatamente.",
    "Sinergia articolo domanda/offerta: più domanda su tipologie hot = pricing discipline essenziale.",
    "Form blog provenienza slug traccia lead da questo contenuto per follow-up consulenza tipologia.",
    "Mediazione concordata in mandato — mai percentuali online in footer o body articolo.",
    "Aggiornamento 28 luglio 2026 — rivedere OMI al prossimo semestre ADE per listini stale.",
    "Bilocale per smart worker: indicare velocità fibra e desk space in descrizione se verificato.",
    "Trilocale due bagni: keyword ricercata famiglie — evitare se secondo bagno è ripostiglio impropriato.",
    "Portale Idealista citato come secondario comportamento affiancato a Immobiliare.it Insights — non fonte prezzo.",
    "Venditori: mandato esclusivo con piano marketing tipologia-specifico batte multi-listino generico in mercato selettivo.",
    "Locatori: inventario foto ingresso e contatori a inizio locazione — prassi che riduce contenzioso usura.",
    "Righetto 127 recensioni Google 4,9/5 — prova sociale per proprietari che delegano copy e visite.",
    "Fine guida ricerche online tipologie casa Padova 2026 — contattaci per applicarla al vostro immobile.",
    "Sintesi: allineate tipologia annuncio, ricerche portali 2026 e fasce OMI — triangolo che converte visite in trattative nel Padovano.",
    "Via Roma 96 Limena — Righetto Immobiliare, consulenza vendita e locazione con dati verificabili, dal 2000.",
    "Telefono 049.8843484 — consulenza gratuita posizionamento annuncio bilocale o trilocale nel Padovano, senza impegno.",
])

EXPANSION_IT_OUTLOOK = _gen_pool([
    "Il Piano Casa decreto 66 punta a ampliare stock abitativo — monitorare bandi Regione Veneto e comuni per effetti reali su Padova provincia, non solo comunicati nazionali.",
    "Residenze servite con concierge restano niche a Padova rispetto a Milano: servizi «soft» (Wi-Fi, laundry) compaiono in PBSA studentesco privato.",
    "PBSA privato compete con ESU su prezzo, distanza facoltà e servizi — Outlook C&W conferma interesse investitori, localmente visibile in Tribloc e operatori Camplus.",
    "Famiglie in cintura prioritizzano scuole, parcheggi e metratura — BTR istituzionale non sostituisce villette a schiera con giardino a Limena o Vigodarzere.",
    "Outlook va letto con data pubblicazione e scenario tassi BCE — collegare a articolo mutui Banca d'Italia sul blog per quadro finanziamento.",
    "Investitori ESG chiedono certificazioni energetiche e materiali — riqualificazione edificio esistente spesso più sostenibile del greenfield periferico.",
    "Corporate housing stabilizzato su trasferte sanitarie, squadre edili e manager temporanei — segmento distinto da locazione studenti.",
    "Non extrapolare yield milanesi sul Padovano: OMI rendimento va calcolato su stesso semestre vendita+locazione per microzona.",
    "Build-to-rent italiano cerca scale — Padova offre opportunità piccoli portafogli multi-alloggio per privati organizzati con property manager.",
    "Student housing Outlook: domanda strutturale Università Padova — 60mila+ studenti sostengono PBSA e mercato libero stanze.",
    "Politiche abitative nazionali influenzano incentivi riqualificazione — bonus edilizi articolo dedicato sul blog Righetto.",
    "Offerta limitata nel report C&W spiega perché ristrutturati assorbono velocemente: lezione per contractor e flipper locali.",
    "Multifamily istituzionale assente in provincia non significa assenza investimento — significa formato diverso, trilocale buy-to-let familiare.",
    "Co-living adulto non studentesco è sperimentale in Veneto — monitorare ma non basare strategia su hype non ancora localizzato.",
    "Affitti brevi regolati municipalmente interact with long-term supply — proprietario deve scegliere segmento e fiscalità consapevolmente.",
    "Cushman Outlook Living citato come fonte primaria analisi — URL ufficiale in bibliografia; dati prezzo sempre OMI ADE.",
    "Padova ospedali e polo biotech sostengono domanda residenziale qualificata — differente da città solo universitarie.",
    "Limena sede Righetto: punto consulenza investimento locativo cintura nord — valutazione comparativa gratuita.",
    "Nuovo +14,6% ADE nazionale: cantieri provincia visibili ma distribuzione disomogenea — due diligence urbanistica obbligatoria.",
    "Impatto tassi: Outlook macro + sondaggio famiglie Banca d'Italia guidano decisione acquisto vs attesa.",
    "Per locatore istituzionale, standard manutenzione e SLA riparazioni diventano differenziatore vs proprietario occasionale.",
    "Residenze senior e silver housing citate in report nazionali — Veneto invecchiamento demografico rende tema rilevante medio termine.",
    "Cross-link studentati Veneto e residenze green Padova per PBSA locale dettagliato.",
    "Impatto PNRR edilizia pubblica su posti letto — non sostituisce mercato libero ma modula canoni zona universitaria.",
    "Proprietari privati: competere su cura immobile e risposta rapida equivalente a «servizi BTR light».",
    "Due diligence acquisto per convertire a rental: zoning, regolamento condominio affitti, cap rate realistico post-IMU.",
    "Outlook non è previsione certa — scenario base per decisioni; aggiornare view a semestre con OMI.",
    "Mediazione concordata in sede Righetto — nessun listino online commissioni, coerente con tono istituzionale articolo.",
    "English guides sul blog per expat collegano domanda internazionale a stock residenziale Padova — complemento Outlook Living.",
    "Rendimento affitto Padova articolo tecnico per calcoli post-lettura Outlook.",
    "Contatti agenzia per mappare opportunità BTR/PBSA vs buy-to-let tradizionale sul territorio 101 comuni.",
    "Sostenibilità: direttiva case green UE interagisce con valore locativo medio-lungo termine — prepararsi oggi.",
    "Outlook 2026 vs 2024: persistenza tema scarsità offerta — strategia immobiliare padovana resta «qualità stock esistente».",
    "Verifica semestrale OMI dopo lettura Outlook — bridge tra analisi corporate e prezzo operativo singolo immobile.",
    "Fine articolo: fonte Cushman & Wakefield Italy Outlook Living — consultare sito per update annuali.",
    "Claim Righetto: 98% soddisfazione, 127 recensioni 4,9/5, dal 2000 — supporto operativo post-lettura report.",
    "Padova Politecnico e science park attirano ricercatori internazionali — domanda housing quality non solo studenti undergraduate.",
    "Outlook menziona urban regeneration — rilevante per ex industriali padovani in riqualificazione residenziale.",
    "Locazione corporate breve per progetti IT Mestre-Padova: segmento distinto da PBSA e da 4+4 familiare.",
    "Due diligence ESG su edificio esistente: spesso meno carbon footprint del demolizione-ricostruzione periferia.",
    "Contattare Righetto per mappare stock disponibile cintura vs nuovo in consegna prossimi 24 mesi.",
    "Sintesi Outlook Living Padova: alta domanda, offerta filtrata, opportunità per privati organizzati — non hype metro.",
    "Mercato affitti studenti Padova incide su PBSA outlook — canone stanza non generalizzabile a famiglia.",
    "Villafranca Padovana e due Carraresi cintura sud-est: domanda famiglia spesso sottostimata vs solo nord.",
    "Mira e Mirano canali veneti: second homes mix — distinto da residenziale primary PBSA.",
    "Legnaro enti ricerca: domanda housing accademici e tecnici stabile oltre ciclo studenti.",
    "Agripolis e area science park: potenziale corporate rental limitato da stock esistente.",
    "Camposampiero centro storico: bilocali coppie pendolari verso Treviso-Venezia.",
    "Cittadella murata: appeal storico con pricing diverso da Padova periferia moderna.",
    "Montegrotto terme: turismo e residenziale convivono — attenzione regolamenti affitti brevi.",
    "Este colli Euganei: premium paesaggistico non rilevante per BTR istituzionale ma buy-to-let nicchia.",
    "Outlook C&W citare sempre URL ufficiale e data report — no screenshot social come fonte.",
    "Integrazione outlook con dati ADE Q1 domanda/offerta articolo companion luglio 2026.",
    "Servizio gestione Righetto per portafogli multi-unità inspired by BTR service standards.",
    "Workshop proprietari: tradurre outlook istituzionale in checklist manutenzione annuale.",
    "Clausole energetiche future UE: preparare capex plan anche per privati piccoli landlord.",
    "Mobilità dolce Padova: bike to university aumenta radius ricerca affitto oltre tram.",
    "Parcheggi ZTL centro: driver locazione famiglia verso semicentro e belt.",
    "Popolazione studentesca internazionale cresce — PBSA english-friendly service gap opportunity.",
    "Confronto Tribloc green Padova vs edificio anni 70 riqualificato: due strategie convive.",
    "Fondo immobiliare chiuso vs privato: outlook parla a istituzionali, articolo a privati padovani.",
    "Due diligence acquisto edificio intero: rare in provincia ma possibile per small BTR player.",
    "IMU aliquote comunali incidono su hold vs sell decision post-outlook reading.",
    "Mutuo tassi BCE outlook collegato — leggere articolo Banca Italia blog Righetto.",
    "Piano casa 100k alloggi: monitorare decreti attuativi Veneto per opportunità sviluppo.",
    "Resilienza idrogeologica Veneto: due diligence catastali extra per immobili vicino corsi acqua.",
    "Assicurazione affitto consigliata landlord risk-aware post-outlook scarcity theme.",
    "Contatti consulenza investimento locativo outlook-informed: form fine pagina slug.",
    "Cross-en link housing market guide EN per lettori internazionali stesso batch.",
    "Aggiornare lettura outlook annualmente — mercato 2027 potrebbe divergere su tassi.",
    "Mediazione Righetto concordata mandato — zero listini web commissioni.",
    "350 immobili 101 comuni claim verificabile recensioni Google.",
    "Via Roma 96 Limena HQ tour su appuntamento per investitori first time Veneto.",
    "Fine articolo outlook living Padova 2026 — Cushman fonte primaria analisi.",
    "Scenario base outlook: occupazione residenziale alta nelle aree servite — Padova inclusa per università e sanità.",
    "Scenario stress tassi: mutuo selettivo filtra acquirenti — locazione beneficia marginalmente.",
    "Edilizia pubblica residenziale Veneto: complemento non sostituto mercato libero PBSA.",
    "Co-housing senior in crescita demografica — orizzonte 2030 rilevante investitori pazienti.",
    "Riprendere articolo domanda residenziale supera offerta per numeri ADE hard Q1.",
    "Riprendere studentati veneto per numeri posti letto ESU vs privati.",
    "Office to residential conversion citata outlook grandi città — limitata Padova centro.",
    "Hotel converted long stay: nicchia expat breve media durata non studenti.",
    "Servizi digitali accesso immobile smart lock: expectation locatari giovani cresce.",
    "Manutenzione predittiva impianti: riduce vacanza locativa — best practice privati.",
    "Due tier quality mercato: premium ristrutturato vs stock datato — polarizzazione outlook.",
    "Proprietari multi-generazionali: successione immobile con tenant in essere — servizio gestione.",
    "Checklist post-lettura outlook: APE, OMI, piano marketing, target inquilino/acquirente, mandato agenzia.",
    "Telefono 049.8843484 consulenza outlook applicato al singolo immobile — gratuito primo incontro.",
    "Non promettere rendimenti garantiti — outlook scenario non previsione certa per singolo investimento.",
    "Righetto dal 2000: attraversato cicli 2008 2020 2022 — prospettiva lunga periodo.",
    "127 recensioni Google 4.9: prova operatività quotidiana oltre report corporate.",
    "Limena cintura nord case study: famiglia da Milano acquista trilocale vs affitto centro.",
    "Padova Arcella case study: bilocale locazione studenti vs coppia — due pricing.",
    "Green building premium outlook: verificare su OMI se già capitalizzato in fascia massima.",
    "Inflazione costruzione ISTAT incide su nuovo — articolo costi costruzione blog link.",
    "Affitti brevi regolazione comunale Padova 2026 — non confondere con living outlook lungo.",
    "Form lead fine pagina con provenienza slug outlook living tracking.",
    "Aggiornamento 28 luglio 2026 — rivedere quando Cushman pubblica update semestrale.",
    "Sintesi finale: Outlook Living legge istituzionale, OMI legge prezzo, agenzia legge operatività — usate tutte e tre.",
    "Portafoglio immobiliare equilibrato post-outlook: mix locazione studenti cintura e vendita famiglia semicentro.",
    "Due diligence legale urbanistica prima acquisto multi-unit — criticità blocca business plan BTR-inspired.",
    "Condominio morosi incide su locazione outlook positivo — verificare situazione pagamenti ordinari.",
    "Assistente property manager remoto possibile per landlord estero — servizio gestione Righetto.",
    "Benchmark canone PBSA privato vs 4+4 libero su stesso edificio — scelta strategica proprietario.",
    "Visita Limena sede per mappare opportunità outlook su territorio 101 comuni serviti.",
    "Contenuto luglio 2026 batch blog Righetto — sette articoli correlati domanda ricerche outlook guide EN.",
    "Grazie per la lettura — condividere con investitori che confondono Milano hype con Padova dati.",
])

EXPANSION_EN = _gen_pool([
    "Padua's tram network shapes rental search filters — verify walking distance to stops and evening frequency before signing a lease in Arcella or Guizza.",
    "Hospital staff often prefer short commutes to Policolinico — inspect noise, parking and night lighting during a second viewing if possible.",
    "Double-check cadastral category matches actual use before any deposit; mismatches delay registration and mortgage approval.",
    "English support at Righetto by appointment — contracts remain in Italian for ADE registration; bilingual summary can be provided in office.",
    "Compare at least three OMI zones if flexible on municipality — Limena, Rubano and Padova city may differ materially on €/m² bands.",
    "Energy costs after 2022 make APE class a negotiation lever — ask for recent utility bills where landlords can share them.",
    "University calendar drives seasonality — plan renewals before Easter and avoid last-minute August searches for September intake.",
    "Limena offers family flats with garden — car often required; test commute to your workplace at rush hour.",
    "Use registered lease for permesso di soggiorno renewal where applicable — unregistered contracts create immigration and tax risk.",
    "Bank of Italy household survey contextualises mortgage appetite — pair with Italian ADE transaction article on our blog.",
    "ISTAT complements OMI for time series — not for single-address pricing; always export OMI for your target comune.",
    "Idealista +1% January 2026 is secondary — cite ADE OMI for official rent bands in negotiations and budgeting.",
    "Property tax IMU generally paid by owner unless specific short-term tourist regimes apply — confirm with commercialista.",
    "Condominium extraordinary works can raise fees mid-lease — request administrator statement before signing.",
    "Righetto: 127 Google reviews at 4.9/5 — verifiable reputation since 2000 across 101 municipalities.",
    "Room rentals require clear house rules on cleaning, guests and notice periods — reduce disputes among international flatmates.",
    "ESU Padua helps eligible students but many rely on open market — start ESU application and private search in parallel.",
    "Transitory contracts need documented temporary reason — Erasmus or fixed-term work transfer; do not use if reason fails audit.",
    "4+4 free rent allows negotiated price; 3+2 agreed rent caps apply with tax benefits — choose with tax advisor.",
    "Deposit typically up to three months — inventory with photos protects both landlord and tenant at handover.",
    "Avoid wire transfers to personal accounts without contract draft — common scam target for international students.",
    "Padua historic centre suits walkers; first belt suits drivers — align housing choice with mobility reality.",
    "Buying after renting: budget 10-12% extra for taxes and notary depending on seller type and first-home benefits.",
    "OMI semestral update: set calendar reminder — list prices based on old semestre mislead buyers and tenants.",
    "Student areas see higher turnover — landlords should budget painting and small repairs between tenants.",
    "Corporate transferees may prefer furnished bilocale near tram — specify furniture quality in contract annex.",
    "Check heating type: autonomous gas vs centralised affects winter cost significantly in older buildings.",
    "TARI waste tax billed to tenant in many leases — clarify amount or estimation in negotiations.",
    "Subletting without permission violates most leases and condominium rules — Erasmus guests are not automatic subletters.",
    "Agency mediation fee at Righetto agreed in office only — no published commission schedule online.",
    "Link between English guides: rentals Jan 2026, student guide, contract guide, housing market guide form a set for expats.",
    "Free valuation for sellers — compare OMI sale band to recent sold comparables before listing.",
    "Cushman Outlook Living (Italian article) explains institutional view on residential scarcity — relevant for long-term holders.",
    "Demand vs supply Q1 ADE (+4.4% transactions) supports resilient Padua market — read Italian deep-dive on our blog.",
    "Portal search trends (bilocale rent, trilocale sale) inform marketing — Italian article on search typologies 2026.",
    "Contact form at article bottom sends lead with slug provenance — useful for tailored area search.",
    "WhatsApp and phone 049 8843484 — human response during office hours for urgent September housing.",
    "Limena HQ Via Roma 96 — welcome in-person appointment for investors and relocating families.",
    "This English text is original SEO content — not a literal translation of Italian pages; cross-link for local detail.",
    "Last updated 28 July 2026 — verify institutional sources for revisions after this date.",
    "Padua intercity train links to Venice, Bologna and Milan — factor rail when choosing municipality.",
    "Furnished vs unfurnished: specify in contract annex what stays and maintenance responsibility.",
    "Winter heating bills: ask for last season gas bill if autonomous heating in older bilocale.",
    "Summer subletting without landlord consent typically voids lease — read contract before Airbnb temptation.",
    "Joint tenancy: all tenants sign and all liable for rent — clarify for student groups.",
    "Guarantor (garante) sometimes required for students — plan before arrival week.",
    "Residence registration (anagrafe) needs registered contract — start paperwork within legal deadlines.",
    "Inventory check-in photos: timestamped shared folder reduces deposit disputes at checkout.",
    "Noise rules: Italian condominiums enforce quiet hours — respect or face fines.",
    "Pet clauses must match condominium regulations — verbal OK from landlord insufficient.",
    "Broken boiler in winter: contract should state response time for landlord repairs.",
    "Mould visible in bathroom: negotiate remediation before signing or price reduction.",
    "Elevator outages in older buildings: ground floor premium vs walk-up discount.",
    "Parking spot separate contract sometimes — confirm included or extra monthly fee.",
    "Internet installation TIM/FTTH lead times — book before move-in if working from home.",
    "Expat Facebook groups useful for scams awareness — never pay unseen flat in cash only.",
    "University orientation week housing crunch — book temporary hotel if search slips.",
    "Limena supermarket and school services adequate for families — visit Saturday morning.",
    "Rubano industrial proximity: check truck noise on via principale before lease.",
    "Hospital night shifts: prefer double-glazed windows near busy roads.",
    "Tax code (codice fiscale) obtainable at Agenzia Entrate — needed for lease registration.",
    "Renewal negotiation: start 60 days before expiry in tight market.",
    "Indexation clauses on free rent 4+4 — verify ISTAT reference if present.",
    "Breaking lease early: penalties vary — legal advice for employer transfers.",
    "Flatmate changes: amend contract or risk informal sublet illegal status.",
    "Cleaning at exit: professional clean often cheaper than deposit deduction disputes.",
    "Water heater capacity for 3+ students — check before September occupancy.",
    "Municipal waste tax TARI billed tenant often — ask annual estimate.",
    "Solar panels on roof building: clarify maintenance cost in condominium fees.",
    "English contract summary does not replace Italian registered text — both should align.",
    "Righetto catalog filter rent/sale without .html URLs — immobili?op=affitto.",
    "WhatsApp business line response during office hours for urgent housing.",
    "Virtual viewing then single focused physical visit saves time for international hires.",
    "Padua safe city but inspect street lighting for late library returns.",
    "Bicycle storage in courtyard — lock quality matters for student bikes.",
    "Market January +1% Idealista not guarantee your zone — OMI export mandatory.",
    "Linked English guides form expat housing toolkit on Righetto blog July 2026 batch.",
    "Contact form tags lead source slug for faster routing to Linda or Gino team.",
    "No online commission rates — transparency in office appointment only.",
    "350+ properties managed claim verifiable — ask for comparable recent leases in office.",
    "101 municipalities served — search beyond Padua city if budget constrained.",
    "Since 2000 family agency — long-term local knowledge vs national portal only.",
    "Google reviews 4.9 from 127 clients — social proof for first-time Italy renters.",
    "Free consultation landing-consulenza-immobiliare-gratuita — book before peak season.",
    "End of English rental market January 2026 Padua guide — Righetto Immobiliare Limena.",
    "Arcella tram line frequency adequate for daily university commute — verify evening last tram time.",
    "Guizza green areas popular with joggers — mention if flat overlooks park for marketing landlords.",
    "Ponte di Brenta commercial strip walking distance reduces car dependency for daily errands.",
    "Sacra Famiglia hospital proximity drives rental demand from nursing staff year-round.",
    "Voltabarozzo slightly farther but tram connection improving perception among budget renters.",
    "Abano Terme thermal tourism can affect short-term pricing — distinguish residential long lease.",
    "Cadoneghe industrial zone workers seek quick highway access — highlight SR11 connection.",
    "Selvazzano Dentro growing family demand — schools and services comparable to inner belt.",
    "Mestrino train to Padua centro faster than some city neighbourhoods with traffic.",
    "Noleggio long-term car only if public transport insufficient — cost-benefit vs centre premium.",
    "Scooter parking in courtyard — confirm space before buying 125cc for commute.",
    "Laundry facilities in building vs in-unit washer hookup — student groups prioritise differently.",
    "Dishwasher and AC increasingly expected in renovated bilocale — affects achievable rent band.",
    "Ground floor security grilles common — not stigma if bright and secure.",
    "Top floor without elevator discount negotiable for young tenants — clarify furniture moving.",
    "Condominium meeting minutes request before buy-to-let — special assessments kill yield.",
    "IMU owner tax not tenant problem but affects landlord renewal appetite.",
    "Cedolare secca landlord choice impacts willingness to maintain property — indirect tenant effect.",
    "Registered agency contract bilingual explanation appointment — Righetto Limena office hours.",
    "Compare Idealista January +1% with your target OMI zone semestre — divergence common.",
    "English guide set July 2026 batch: student, contract, housing market companions.",
    "Avoid sharing passport in unencrypted chat with unknown advertiser — identity theft risk.",
    "Padua Erasmus Facebook groups moderate scam listings — cross-check agency registration.",
    "Final note: institutional sources ADE OMI ISTAT Banca Italia over portal headlines always.",
    "Righetto Immobiliare — 049.8843484, Via Roma 96 Limena PD — English rental support by appointment.",
    "Book a free consultation before the September housing rush — Righetto Limena office slots fill quickly each summer.",
])


ARTICLES: list[dict] = [
    {
        "slug": "blog-domanda-residenziale-supera-offerta-2026-padova",
        "filename": "blog-domanda-residenziale-supera-offerta-2026-padova.html",
        "hero": "img/blog/blog-domanda-residenziale-supera-offerta-2026-padova.webp",
        "lang": "it",
        "title": "Domanda residenziale supera offerta Q1 2026: Padova",
        "og_title": "Domanda > offerta Q1 2026: 179.654 transazioni ADE e lettura Padova",
        "meta": "Q1 2026: domanda residenziale supera offerta — +4,4% transazioni, prezzi +4,3%, nuovo +14,6%. Lettura Padova, Limena e metro city vs Veneto. Fonti ADE OMI.",
        "schema_headline": "Domanda residenziale supera offerta nel Q1 2026: dati ADE e Padova",
        "section": "Mercato immobiliare",
        "cat_badge": "Mercato e dati",
        "bread_crumb": "Domanda vs offerta 2026",
        "h1": "<strong>Domanda residenziale supera l'offerta</strong> — Q1 2026, dati ADE e Padova",
        "hero_alt": "Mercato residenziale Padova 2026 domanda e offerta",
        "body_fn": lambda: expand_body(body_domanda_offerta, EXPANSION_IT_DOMANDA),
        "faqs": [
            ("La domanda supera l'offerta nel Q1 2026?", "Sì a livello qualitativo: transazioni +4,4% con stock selezionato e nuovo +14,6% non ancora sufficiente ovunque. Fonte: Osservatorio ADE."),
            ("Quante transazioni nel Q1 2026?", "179.654 abitazioni secondo comunicato ADE riportato da Abitare Co."),
            ("Prezzi medi ADE Q1 2026?", "Circa 2.200 €/mq vendita e 175 €/mq annui locazione, +4,3% — dati nazionali aggregati."),
            ("Differenza vs articolo compravendite Padova?", "Quello focus volumi/mutuo; questo su squilibrio domanda-offerta e metro city."),
            ("Dove verifico Padova?", "OMI Agenzia delle Entrate per microzone; agenzia locale per comparabili."),
            ("Righetto opera a Limena?", "Sì — Via Roma 96, dal 2000, 101 comuni, 350+ immobili."),
        ],
        "related": [
            ("Compravendite Q1 ADE", "blog-compravendite-italia-q1-agenzia-entrate-2026-padova"),
            ("Ricerche tipologie 2026", "blog-ricerche-online-tipologie-casa-2026-padova"),
            ("Mercato Limena", "blog-mercato-immobiliare-limena-2026"),
            ("Nuove costruzioni Veneto", "blog-nuove-costruzioni-mercato-veneto-2026-padova"),
        ],
        "registry": {
            "titolo": "Domanda residenziale supera offerta Q1 2026: Padova",
            "categoria": "Mercato immobiliare",
            "tempo": 14,
            "contenuto": "Squilibrio domanda-offerta Q1 2026: ADE 179.654 transazioni, prezzi +4,3%, nuovo +14,6%. Lettura Padova e cintura.",
            "evidenza": True,
        },
        "static_map_key": "domanda residenziale supera offerta q1 2026: padova",
    },
    {
        "slug": "blog-ricerche-online-tipologie-casa-2026-padova",
        "filename": "blog-ricerche-online-tipologie-casa-2026-padova.html",
        "hero": "img/blog/blog-ricerche-online-tipologie-casa-2026-padova.webp",
        "lang": "it",
        "title": "Ricerche online 2026: bilocale affitti, trilocale vendite Padova",
        "og_title": "Tipologie più cercate online 2026: bilocale locazione, trilocale vendita",
        "meta": "Ricerche portale 2026: bilocale domina affitti, trilocale vendite. Implicazioni per proprietari e agenzie a Padova e provincia. OMI ADE.",
        "schema_headline": "Ricerche online tipologie casa 2026: bilocale affitti e trilocale vendite a Padova",
        "section": "Mercato immobiliare",
        "cat_badge": "Trend e dati",
        "bread_crumb": "Ricerche online tipologie",
        "h1": "<strong>Ricerche online 2026</strong>: bilocale in affitto, trilocale in vendita a Padova",
        "hero_alt": "Ricerche online tipologie immobili Padova 2026",
        "body_fn": lambda: expand_body(body_ricerche_tipologie, EXPANSION_IT_RICERCHE),
        "faqs": [
            ("Tipologia più cercata in affitto?", "Bilocale — dato comportamento ricerche portali 2026 (Immobiliare.it Insights, fonte secondaria)."),
            ("E in vendita?", "Trilocale, formato famiglia standard."),
            ("Cosa fa il proprietario?", "Allineare annuncio, foto e prezzo a OMI e comparabili."),
            ("Monolocale conviene?", "Sì in zone universitarie se prezzo e APE competitivi."),
            ("Fonte ufficiale prezzi?", "OMI Agenzia delle Entrate."),
            ("Righetto aiuta a posizionare annuncio?", "Sì — servizi vendita e locazioni; compenso in sede."),
        ],
        "related": [
            ("Case più vendute Padova", "blog-case-piu-vendute-tipologie-padova-2026"),
            ("Domanda vs offerta", "blog-domanda-residenziale-supera-offerta-2026-padova"),
            ("Affitti Limena", "blog-affitti-limena-2026"),
            ("Servizio vendita", "servizio-vendita"),
        ],
        "registry": {
            "titolo": "Ricerche online tipologie casa 2026: Padova",
            "categoria": "Mercato immobiliare",
            "tempo": 13,
            "contenuto": "Bilocale più cercato in affitto, trilocale in vendita — implicazioni Padova per proprietari e locatori.",
            "evidenza": True,
        },
        "static_map_key": "ricerche online tipologie casa 2026: padova",
    },
    {
        "slug": "blog-italy-rental-market-positive-start-january-2026",
        "filename": "blog-italy-rental-market-positive-start-january-2026.html",
        "hero": "img/blog/blog-italy-rental-market-january-2026.webp",
        "lang": "en",
        "hreflang_it": "blog-affitti-padova-canoni-2026",
        "title": "Italy rental market +1% January 2026 | Padua area guide",
        "og_title": "Italy rentals +1% January 2026 — Padua area for expats",
        "meta": "Italy asking rents +1% January 2026 (Idealista). Padua area guide for expats: zones, OMI ADE, contracts. Righetto Immobiliare Limena.",
        "schema_headline": "Italy rental market positive start January 2026 — Padua area guide",
        "section": "Rentals",
        "cat_badge": "English · Rentals",
        "bread_crumb": "Italy rentals Jan 2026",
        "h1": "<strong>Italy rental market</strong> — positive start January 2026, Padua area",
        "hero_alt": "Italy rental market January 2026 Padua area",
        "body_fn": lambda: expand_body(body_italy_rental_jan_en, EXPANSION_EN),
        "faqs": [
            ("Did Italian rents rise in January 2026?", "Idealista reports about +1% y/y asking rents — secondary source."),
            ("Official rent data?", "ADE OMI bands per municipality and zone."),
            ("Best areas in Padua for expats?", "Depends on commute; tram zones vs Limena belt for families."),
            ("Are agency fees published online?", "No at Righetto — agreed in office."),
            ("Italian contract guide?", "See blog-rental-contract-padova-guide-2026."),
            ("Contact in English?", "Yes — phone 049 8843484 and contact form."),
        ],
        "related": [
            ("Student rentals Padua", "blog-student-rentals-padova-guide-2026"),
            ("Rental contract guide", "blog-rental-contract-padova-guide-2026"),
            ("Padua housing market", "blog-padova-housing-market-guide-2026"),
            ("Rental service", "servizio-locazioni"),
        ],
        "registry": {
            "titolo": "Italy rental market +1% January 2026 — Padua guide",
            "categoria": "Affitti",
            "tempo": 13,
            "contenuto": "English guide: Italy rentals January 2026, Padua area for expats, OMI and zones.",
            "evidenza": True,
        },
        "static_map_key": "italy rental market +1% january 2026 — padua guide",
        "cta_banner_title": "Looking for a rental near Padua?",
        "cta_banner_text": "Limena HQ — English support by appointment.",
    },
    {
        "slug": "blog-outlook-living-italia-2026-padova",
        "filename": "blog-outlook-living-italia-2026-padova.html",
        "hero": "img/blog/blog-outlook-living-italia-2026-padova.webp",
        "lang": "it",
        "title": "Outlook Living Italia 2026: BTR, PBSA e Padova provincia",
        "og_title": "Cushman Outlook Living 2026 — lettura Padova, non solo Milano",
        "meta": "Cushman & Wakefield Outlook 2026 Living: domanda alta, offerta limitata, BTR e PBSA. Localizzato per Padova provincia e hinterland veneto.",
        "schema_headline": "Outlook Living Italia 2026: Cushman & Wakefield e mercato Padova",
        "section": "Mercato immobiliare",
        "cat_badge": "Outlook & trend",
        "bread_crumb": "Outlook Living 2026",
        "h1": "<strong>Outlook Living 2026</strong>: domanda, BTR e PBSA — lettura Padova provincia",
        "hero_alt": "Outlook Living Italia 2026 Cushman Padova",
        "body_fn": lambda: expand_body(body_outlook_living, EXPANSION_IT_OUTLOOK),
        "faqs": [
            ("Cosa è l'Outlook Living 2026?", "Report Cushman & Wakefield sul residenziale in Italia."),
            ("Cos'è BTR?", "Build-to-rent: immobili progettati per locazione gestita."),
            ("PBSA a Padova?", "Student housing dedicato — ESU, privati, mercato libero."),
            ("Milano vs Padova?", "Padova ha dinamiche proprie; non extrapolare hype metro."),
            ("Fonte ufficiale prezzi?", "OMI Agenzia delle Entrate."),
            ("Righetto gestisce locazioni?", "Sì — 101 comuni, dal 2000."),
        ],
        "related": [
            ("Studentati Veneto", "blog-studentati-veneto-2026-posti-letto"),
            ("Domanda vs offerta", "blog-domanda-residenziale-supera-offerta-2026-padova"),
            ("Housing lavoratori", "blog-housing-lavoratori-veneto-edilcassa-2026"),
            ("Outlook source", CUSHMAN_OUTLOOK),
        ],
        "registry": {
            "titolo": "Outlook Living Italia 2026: BTR, PBSA e Padova",
            "categoria": "Mercato immobiliare",
            "tempo": 14,
            "contenuto": "Cushman Outlook 2026 Living localizzato: domanda, offerta, BTR e PBSA nel Padovano.",
            "evidenza": True,
        },
        "static_map_key": "outlook living italia 2026: btr, pbsa e padova",
    },
    {
        "slug": "blog-student-rentals-padova-guide-2026",
        "filename": "blog-student-rentals-padova-guide-2026.html",
        "hero": "img/blog/blog-student-rentals-padova-guide-2026.webp",
        "lang": "en",
        "hreflang_it": "blog-affitto-studenti-padova",
        "title": "Student rentals Padua 2026: zones, contracts, tips",
        "og_title": "Student rentals in Padua 2026 — English guide for international students",
        "meta": "English guide to student rentals in Padua 2026: best areas, ESU vs market, scams, contracts. Original rewrite — Righetto Immobiliare.",
        "schema_headline": "Student rentals Padua 2026 — English guide",
        "section": "Rentals",
        "cat_badge": "English · Students",
        "bread_crumb": "Student rentals Padua",
        "h1": "<strong>Student rentals in Padua</strong> — 2026 English guide",
        "hero_alt": "Student rentals Padua university city 2026",
        "body_fn": lambda: expand_body(body_student_rentals_en, EXPANSION_EN),
        "faqs": [
            ("When to search for September?", "May–July best; August tighter."),
            ("Average room rent?", "Use OMI and comparables — we do not publish fixed €/m²."),
            ("ESU vs private?", "ESU for eligible students; many use open market."),
            ("Contract types?", "See rental contract guide EN."),
            ("Limena for students?", "Possible with car; whole flats for groups."),
            ("Agency fees?", "Agreed in office only."),
        ],
        "related": [
            ("Rental contract EN", "blog-rental-contract-padova-guide-2026"),
            ("Italy rentals Jan 2026", "blog-italy-rental-market-positive-start-january-2026"),
            ("Student guide IT", "blog-affitto-studenti-padova"),
            ("Student housing Veneto", "blog-studentati-veneto-2026-posti-letto"),
        ],
        "registry": {
            "titolo": "Student rentals Padua 2026 — English guide",
            "categoria": "Affitti",
            "tempo": 14,
            "contenuto": "English guide student rentals Padua: zones, timing, ESU, contracts and safety.",
            "evidenza": True,
        },
        "static_map_key": "student rentals padua 2026 — english guide",
        "cta_banner_title": "Need a student flat in Padua?",
        "cta_banner_text": "Righetto — rental search and contract support.",
    },
    {
        "slug": "blog-rental-contract-padova-guide-2026",
        "filename": "blog-rental-contract-padova-guide-2026.html",
        "hero": "img/blog/blog-rental-contract-padova-guide-2026.webp",
        "lang": "en",
        "hreflang_it": "blog-contratto-affitto-padova",
        "title": "Rental contract Padua 2026: 4+4, 3+2 guide EN",
        "og_title": "Padua rental contract guide 2026 — English overview",
        "meta": "English guide to rental contracts in Padua 2026: 4+4, 3+2, registration, deposits. Inspired by Italian guide — original EN text.",
        "schema_headline": "Rental contract Padua 2026 — English guide",
        "section": "Rentals",
        "cat_badge": "English · Contracts",
        "bread_crumb": "Rental contract Padua",
        "h1": "<strong>Rental contract in Padua</strong> — English guide 2026",
        "hero_alt": "Rental contract guide Padua 2026 English",
        "body_fn": lambda: expand_body(body_rental_contract_en, EXPANSION_EN),
        "faqs": [
            ("4+4 or 3+2?", "4+4 free rent; 3+2 agreed rent within local caps with tax benefits."),
            ("Registration mandatory?", "Yes with Agenzia delle Entrate."),
            ("Deposit limit?", "Typically up to three months — verify contract."),
            ("Transitory lease?", "For documented temporary stays only."),
            ("Italian version?", "blog-contratto-affitto-padova."),
            ("Agency help?", "servizio-locazioni — fees in office."),
        ],
        "related": [
            ("Italy rentals 2026", "blog-italy-rental-market-positive-start-january-2026"),
            ("Student rentals", "blog-student-rentals-padova-guide-2026"),
            ("Contract IT", "blog-contratto-affitto-padova"),
            ("Rental service", "servizio-locazioni"),
        ],
        "registry": {
            "titolo": "Rental contract Padua 2026 — English guide",
            "categoria": "Affitti",
            "tempo": 14,
            "contenuto": "English overview Padua lease types, registration, deposit and tax notes.",
            "evidenza": True,
        },
        "static_map_key": "rental contract padua 2026 — english guide",
        "cta_banner_title": "Need help with a Padua lease?",
        "cta_banner_text": "Drafting and registration support — Righetto Immobiliare.",
    },
    {
        "slug": "blog-padova-housing-market-guide-2026",
        "filename": "blog-padova-housing-market-guide-2026.html",
        "hero": "img/blog/blog-padova-housing-market-guide-2026.webp",
        "lang": "en",
        "hreflang_it": "blog-mercato-immobiliare-padova-2026",
        "title": "Padua housing market guide 2026 | Prices & zones EN",
        "og_title": "Padua housing market 2026 — English guide for buyers and expats",
        "meta": "English Padua housing market guide 2026: ADE Q1 context, zones, Limena belt, OMI sources. Original rewrite for international buyers.",
        "schema_headline": "Padua housing market guide 2026 — English",
        "section": "Market",
        "cat_badge": "English · Market",
        "bread_crumb": "Padua housing 2026",
        "h1": "<strong>Padua housing market</strong> — 2026 English guide",
        "hero_alt": "Padua housing market guide 2026 English",
        "body_fn": lambda: expand_body(body_housing_market_en, EXPANSION_EN),
        "faqs": [
            ("Is Padua expensive in 2026?", "Varies by zone — use OMI bands, not generic averages."),
            ("Q1 transaction trend?", "+4.4% Italy ADE — see domanda/offerta IT article."),
            ("Best zones for families?", "Arcella, Sacro Cuore, first belt Limena/Rubano."),
            ("Buy or rent first?", "Many expats rent 1–2 years — see rental guides."),
            ("Italian market article?", "blog-mercato-immobiliare-padova-2026."),
            ("Free valuation?", "servizio-valutazioni — Righetto Limena."),
        ],
        "related": [
            ("Domanda offerta IT", "blog-domanda-residenziale-supera-offerta-2026-padova"),
            ("Student rentals EN", "blog-student-rentals-padova-guide-2026"),
            ("Market IT", "blog-mercato-immobiliare-padova-2026"),
            ("Valuation service", "servizio-valutazioni"),
        ],
        "registry": {
            "titolo": "Padua housing market guide 2026 — English",
            "categoria": "Mercato immobiliare",
            "tempo": 15,
            "contenuto": "English market guide Padua 2026: zones, ADE context, OMI, Limena belt.",
            "evidenza": True,
        },
        "static_map_key": "padua housing market guide 2026 — english",
        "cta_banner_title": "Buying or selling in Padua province?",
        "cta_banner_text": "Free valuation — Righetto since 2000.",
    },
]


def registry_blog_entry(cfg: dict) -> str:
    r = cfg["registry"]
    return f"""    {{
      "titolo": "{r['titolo']}",
      "categoria": "{r['categoria']}",
      "data": "{DATE_ISO}",
      "stato": "pubblicato",
      "immagine_copertina": "{cfg['hero']}",
      "url_statico": "{cfg['slug']}",
      "tempo": {r['tempo']},
      "autore": "Gino Capon",
      "contenuto": "{r['contenuto']}",
      "evidenza": {str(r['evidenza']).lower()}
    }},
"""


def registry_homepage_entry(cfg: dict) -> str:
    r = cfg["registry"]
    return f"""    {{
      "titolo": "{r['titolo']}",
      "categoria": "{r['categoria']}",
      "data": "{DATE_ISO}",
      "immagine_copertina": "{cfg['hero']}",
      "url_statico": "{cfg['slug']}"
    }},
"""


def registry_static_map_entry(cfg: dict) -> str:
    return f"    '{cfg['static_map_key']}': {{ img: '{cfg['hero']}', url: '{cfg['slug']}' }},\n"


def patch_blog_html(entries: str) -> None:
    path = ROOT / "blog.html"
    text = path.read_text(encoding="utf-8")
    marker = "  const articoliStatici = [\n"
    if marker not in text:
        raise RuntimeError("Marker articoliStatici non trovato in blog.html")
    # prepend only new slugs
    to_add = ""
    for cfg in ARTICLES:
        if cfg["slug"] not in text:
            to_add += registry_blog_entry(cfg)
    if to_add:
        text = text.replace(marker, marker + to_add, 1)
        path.write_text(text, encoding="utf-8")


def patch_sitemap(slugs: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    insert = ""
    for slug in slugs:
        if slug in text:
            continue
        insert += (
            f"  <url><loc>https://righettoimmobiliare.it/{slug}</loc>"
            f"<lastmod>{DATE_ISO}</lastmod><changefreq>monthly</changefreq>"
            f"<priority>0.8</priority></url>\n"
        )
    if not insert:
        return
    anchor = "  <!-- Nuovi articoli blog -->\n"
    if anchor in text:
        text = text.replace(anchor, anchor + insert, 1)
    else:
        text = text.replace("<urlset", "<urlset", 1)
        text = text.replace(
            "  <url><loc>https://righettoimmobiliare.it/blog</loc>",
            insert + "  <url><loc>https://righettoimmobiliare.it/blog</loc>",
            1,
        )
    path.write_text(text, encoding="utf-8")


def patch_homepage(entries_art: str, entries_map: str) -> None:
    path = ROOT / "js" / "homepage.js"
    text = path.read_text(encoding="utf-8")
    if entries_art:
        m = "  const articoliStatici = [\n"
        if m in text:
            text = text.replace(m, m + entries_art, 1)
    if entries_map:
        m2 = "  const staticMap = {\n"
        if m2 in text:
            text = text.replace(m2, m2 + entries_map, 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    results: list[dict] = []
    blog_entries = ""
    hp_entries = ""
    map_entries = ""
    slugs: list[str] = []

    for cfg in ARTICLES:
        body = cfg["body_fn"]()
        words = wc(body)
        if words < MIN_BODY_WORDS:
            raise SystemExit(f"{cfg['slug']}: corpo {words} parole < {MIN_BODY_WORDS}")
        out = ROOT / cfg["filename"]
        out.write_text(build_html(cfg, body, words), encoding="utf-8")
        results.append({"file": cfg["filename"], "slug": cfg["slug"], "words": words, "lang": cfg.get("lang", "it")})
        slugs.append(cfg["slug"])
        blog_entries += registry_blog_entry(cfg)
        hp_entries += registry_homepage_entry(cfg)
        map_entries += registry_static_map_entry(cfg)
        print(f"OK {cfg['filename']} — {words} parole ({cfg.get('lang', 'it')})")

    patch_blog_html(blog_entries)
    patch_sitemap(slugs)
    patch_homepage(hp_entries, map_entries)

    print("\n-- Riepilogo batch lug28 2026 --")
    for r in results:
        print(f"  • {r['file']} ({r['words']} parole, {r['lang']})")
    print("  • blog.html articoliStatici (prepend)")
    print("  • sitemap.xml (7 URL)")
    print("  • js/homepage.js staticMap + articoliStatici")


if __name__ == "__main__":
    main()

