# -*- coding: utf-8 -*-
"""Genera 5 articoli blog aprile 2026 — Righetto. Esegui da repo root: python3 scripts/build_apr19_blog_batch.py"""
from __future__ import annotations

import json
import textwrap

DATE_IT = "19 aprile 2026"
DATE_ISO = "2026-04-19"
TIME_TS = "2026-04-19T09:00:00+02:00"

HEAD_TOP = """<!DOCTYPE html>
<html lang="it">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9MHDHHES26"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-9MHDHHES26');
</script>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#2C4A6E">
  <title>{html_title}</title>
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="dns-prefetch" href="https://cdn.jsdelivr.net">
  <link rel="dns-prefetch" href="https://qwkwkemuabfwvwuqrxlu.supabase.co">
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/cormorant-garamond-700.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="canonical" href="https://righettoimmobiliare.it/{slug}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html_title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:url" content="https://righettoimmobiliare.it/{slug}">
  <meta property="og:image" content="https://righettoimmobiliare.it/{img_path}">
  <meta property="og:site_name" content="Righetto Immobiliare">
  <meta property="og:locale" content="it_IT">
  <meta property="article:published_time" content="{time_ts}">
  <meta property="article:author" content="Gino Capon">
  <meta property="article:section" content="{section}">
  <meta name="description" content="{meta_desc}">
  <link rel="stylesheet" href="css/fonts.css?v=3">
  <link rel="stylesheet" href="css/nav-mobile.css?v=4">
  <link rel="stylesheet" href="css/scroll-reveal.css?v=3" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="css/welcome-popup.css?v=3" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="css/blog-rich.css?v=2">
  <script type="application/ld+json">{blog_json}</script>
  <script type="application/ld+json">{faq_json}</script>
  <script type="application/ld+json">{bread_json}</script>
"""

STYLE_BLOCK = r"""  <style>
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    :root{--nero:#152435;--bianco:#F7F5F1;--oro:#FF6B35;--grigio:#6B7A8D;--gc:#E1DBD1;--sfondo:#ECE7DF;--blu:#2C4A6E;--blu2:#3A5F8C;--oro2:#FF8F5E;--testo:#152435;--carta:#F2EDE7}
    body{font-family:'Montserrat',sans-serif;background:var(--bianco);color:var(--testo)}
    a{text-decoration:none;color:inherit}
    header{background:var(--nero);position:sticky;top:0;z-index:100}
    .hi{max-width:1380px;margin:0 auto;padding:0 1.5rem;height:74px;display:flex;align-items:center;gap:2rem}
    .logo{font-family:'Cormorant Garamond',serif;font-size:1.3rem;font-weight:600;color:#fff}
    .logo span{color:var(--oro);font-style:italic}
    nav{display:flex;gap:.2rem;flex:1}
    nav a{color:rgba(255,255,255,.7);font-size:.82rem;padding:.4rem .75rem;border-radius:4px;transition:color .2s}
    nav a:hover{color:#fff} nav a.active{color:var(--oro)}
    .h-cta{display:flex;gap:.65rem;align-items:center}
    .h-tel{color:rgba(255,255,255,.75);font-size:.78rem}
    .h-btn{background:var(--oro);color:var(--nero);padding:.38rem .85rem;border-radius:6px;font-size:.76rem;font-weight:500;transition:all .2s}
    .h-btn:hover{background:var(--oro2);transform:translateY(-1px)}
    .art-hero{position:relative;overflow:hidden}
    .art-hero-img{width:100%;height:480px;object-fit:cover;display:block;filter:brightness(.42)}
    .art-hero-overlay{position:absolute;bottom:0;left:0;right:0;padding:3rem 1.5rem 2.5rem;background:linear-gradient(transparent,rgba(21,36,53,.95) 40%)}
    .art-hero-inner{max-width:820px;margin:0 auto}
    .breadcrumb{font-size:.72rem;color:rgba(255,255,255,.45);margin-bottom:1rem}
    .breadcrumb a{color:rgba(255,255,255,.55);transition:color .2s}
    .breadcrumb a:hover{color:var(--oro)}
    .cat-badge{display:inline-block;font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;background:rgba(255,107,53,.2);color:var(--oro);padding:.25rem .7rem;border-radius:2px;font-weight:700;margin-bottom:.8rem}
    .art-hero h1{font-family:'Cormorant Garamond',serif;font-size:2.35rem;font-weight:300;color:#fff;line-height:1.2;margin-bottom:1rem}
    .art-hero h1 strong{font-weight:600;font-style:italic}
    .art-hero-meta{display:flex;align-items:center;gap:1.2rem;font-size:.8rem;color:rgba(255,255,255,.5);flex-wrap:wrap}
    .av{width:36px;height:36px;border-radius:50%;background:var(--oro);display:flex;align-items:center;justify-content:center;font-size:.9rem;font-weight:700;color:var(--nero)}
    .art-container{max-width:820px;margin:0 auto;padding:2.5rem 1.5rem 4rem}
    .art-content{font-size:.92rem;line-height:1.9;color:var(--testo)}
    .art-content h2{font-family:'Cormorant Garamond',serif;font-size:1.75rem;font-weight:600;color:var(--nero);margin:2.5rem 0 .8rem;padding-bottom:.4rem;border-bottom:2px solid var(--oro)}
    .art-content h3{font-family:'Cormorant Garamond',serif;font-size:1.3rem;font-weight:600;color:var(--blu);margin:1.5rem 0 .6rem}
    .art-content p{margin-bottom:1.1rem}
    .art-content ul,.art-content ol{margin:0 0 1.1rem 1.5rem}
    .art-content li{margin-bottom:.4rem}
    .art-content a{color:var(--blu);text-decoration:underline}
    .art-content table{width:100%;border-collapse:collapse;margin:1.2rem 0;font-size:.84rem}
    .art-content th,.art-content td{padding:.65rem .9rem;border:1px solid var(--gc);text-align:left}
    .art-content th{background:var(--sfondo);font-weight:600;font-size:.76rem;text-transform:uppercase}
    .cta-row{display:flex;flex-wrap:wrap;gap:1rem;margin:2rem 0;align-items:center}
    .cta-deep{display:inline-flex;align-items:center;justify-content:center;background:linear-gradient(180deg,var(--oro2),var(--oro));color:var(--nero);padding:.85rem 1.75rem;border-radius:10px;font-weight:800;font-size:.82rem;letter-spacing:.02em;box-shadow:0 4px 0 rgba(153,65,20,.45),0 10px 28px rgba(255,107,53,.28);transition:transform .2s,box-shadow .2s}
    .cta-deep:hover{transform:translateY(-2px);box-shadow:0 6px 0 rgba(153,65,20,.45),0 14px 36px rgba(255,107,53,.38)}
    .cta-deep-outline{display:inline-flex;align-items:center;justify-content:center;background:var(--carta);color:var(--blu);padding:.8rem 1.55rem;border-radius:10px;font-weight:700;font-size:.8rem;border:2px solid var(--blu);box-shadow:0 3px 0 var(--blu2);transition:transform .2s,box-shadow .2s}
    .cta-deep-outline:hover{transform:translateY(-2px);box-shadow:0 5px 0 var(--blu2)}
    .faq-section{margin-top:2.5rem}
    .faq-item{border:1px solid var(--gc);border-radius:8px;margin-bottom:.6rem;overflow:hidden}
    .faq-q{padding:1rem 1.2rem;font-weight:600;font-size:.88rem;cursor:pointer;display:flex;justify-content:space-between;background:#fff}
    .faq-q::after{content:'+';font-size:1.3rem;color:var(--oro);flex-shrink:0}
    .faq-item.open .faq-q::after{transform:rotate(45deg)}
    .faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease;background:var(--sfondo)}
    .faq-a-inner{padding:0 1.2rem 1rem;font-size:.86rem;line-height:1.8;color:var(--grigio)}
    .faq-item.open .faq-a{max-height:520px}
    .cta-banner{background:linear-gradient(135deg,var(--nero) 0%,var(--blu) 100%);border-radius:14px;padding:2rem 2.5rem;margin:2.5rem 0;display:flex;align-items:center;gap:2rem;flex-wrap:wrap}
    .cta-banner-text{flex:1;min-width:260px}
    .cta-banner h3{font-family:'Cormorant Garamond',serif;font-size:1.45rem;color:#fff;margin-bottom:.5rem}
    .cta-banner p{font-size:.84rem;color:rgba(255,255,255,.55);line-height:1.7}
    .cta-banner-btn{background:linear-gradient(180deg,var(--oro2),var(--oro));color:var(--nero);padding:.75rem 1.85rem;border-radius:10px;font-size:.85rem;font-weight:800;box-shadow:0 4px 0 rgba(153,65,20,.45),0 8px 24px rgba(255,107,53,.3);transition:transform .2s,box-shadow .2s}
    .cta-banner-btn:hover{transform:translateY(-2px);box-shadow:0 6px 0 rgba(153,65,20,.45),0 12px 32px rgba(255,107,53,.4)}
    .share-bar{border-top:1px solid var(--gc);padding:1rem 0;margin:2rem 0;display:flex;gap:1rem;flex-wrap:wrap;align-items:center}
    .share-btn{padding:.4rem 1rem;border:1px solid var(--gc);border-radius:20px;font-size:.76rem;cursor:pointer;background:#fff;font-family:inherit}
    .related{margin-top:2rem;padding:1.5rem;background:var(--sfondo);border-radius:10px;border:1px solid var(--gc)}
    .related h3{font-family:'Cormorant Garamond',serif;font-size:1.15rem;margin-bottom:.8rem}
    .author-bio{display:flex;gap:1.2rem;align-items:flex-start;border:1px solid rgba(44,74,110,.12);border-radius:12px;padding:1.5rem;margin:2rem 0}
    .author-bio img{width:64px;height:64px;border-radius:50%;object-fit:cover;flex-shrink:0}
    .author-bio-text p{font-size:.82rem;line-height:1.55;color:#555;margin:0}
    footer{background:linear-gradient(180deg,var(--nero) 0%,#0d1a2a 100%);padding:3rem 1.5rem 1.5rem;color:#fff}
    .fi{max-width:1380px;margin:0 auto}
    .fgrid{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:2rem;margin-bottom:2rem}
    @media(max-width:900px){.fgrid{grid-template-columns:1fr 1fr}}
    .flogo{font-family:'Cormorant Garamond',serif;font-size:1.15rem;margin-bottom:.5rem}
    .flogo span{color:var(--oro);font-style:italic}
    .finfo{font-size:.76rem;color:rgba(255,255,255,.6);line-height:1.85}
    .fh{font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,.55);margin-bottom:.6rem}
    .fcol a{display:block;font-size:.78rem;color:rgba(255,255,255,.6);margin-bottom:.25rem}
    .fbot{border-top:1px solid rgba(255,255,255,.08);padding-top:1rem;font-size:.72rem;color:rgba(255,255,255,.5);display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem}
    @media(max-width:768px){.art-hero-img{height:320px}.art-hero h1{font-size:1.85rem}.cta-banner{flex-direction:column;text-align:center}}
    .skip-link{position:absolute;top:-100%;left:50%;transform:translateX(-50%);background:var(--oro);color:var(--nero);padding:.55rem 1rem;border-radius:0 0 8px 8px;z-index:9999}.skip-link:focus{top:0}
  </style>
</head>"""

FOOTER_TMPL = r"""
<footer>
  <div class="fi">
    <div class="fgrid">
      <div><div class="flogo">Righetto <span>Immobiliare</span></div><div class="finfo">Via Roma n.96 — 35010 Limena (PD)<br>Tel 049.88.43.484</div></div>
      <div class="fcol"><div class="fh">Servizi</div><a href="servizio-vendita">Vendita</a><a href="servizio-valutazioni">Valutazioni</a></div>
      <div class="fcol"><div class="fh">Blog</div><a href="blog">Tutti gli articoli</a></div>
      <div class="fcol"><div class="fh">Info</div><a href="contatti">Contatti</a><a href="privacy">Privacy</a></div>
    </div>
    <div class="fbot"><span>&copy; 2026 Gruppo Immobiliare Righetto</span><span>P.IVA 05182390285</span></div>
  </div>
</footer>
<script>
document.querySelectorAll('.faq-q').forEach(function(q) {
  q.addEventListener('click', function() {
    var item = this.parentElement;
    var o = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(function(i) { i.classList.remove('open'); });
    if (!o) item.classList.add('open');
  });
});
</script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2" defer></script>
<script src="js/nav-mobile.js?v=3" defer></script>
<script src="js/config.js?v=3"></script>
<script>(function(){var d=false;function l(){if(d)return;d=true;var s=document.createElement('script');s.src='js/chatbot.js?v=4';document.body.appendChild(s);}
setTimeout(l,3000);['scroll','touchstart','keydown','click'].forEach(function(e){window.addEventListener(e,l,{once:true,passive:true});});})();</script>
<script src="js/cookie-consent.js?v=3" defer></script>
<script src="js/scroll-reveal.js?v=3" defer></script>
<script src="js/welcome-popup.js?v=3" defer></script>
</body>
</html>
"""

MEDIAZIONE = (
    "<p><strong>Nota sulla mediazione:</strong> i compensi di intermediazione "
    "vendita e locazione sono definiti in sede nel mandato, in conformità alla prassi: "
    "per la vendita, 3% + IVA per parte con minimo 2.500 euro per lotti di vendita; "
    "per l'affitto, una mensilità del canone + IVA. Questa pagina non sostituisce il mandato firmato.</p>"
)

DISCLAIMER_BODY = (
    "<p><em>Disclaimer:</em> l'articolo ha finalità informative; non costituisce consulenza fiscale, "
    "legale o finanziaria. Per il mutuo rivolgersi a intermediari creditizi autorizzati; per imposte e "
    "notaio consultare normativa vigente e pareri specialistici.</p>"
)


def word_count(html: str) -> int:
    import re
    text = re.sub(r"<[^>]+>", " ", html)
    return len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))


# Limite massimo paragrafi da template (build_paragraphs) — allineato a TEST-SKILL/SKILL-2.0.md sezione 8.1c
MAX_TEMPLATE_PARAGRAPHS = 50


def assert_body_paragraph_diversity(html: str, max_identical: int = 2) -> None:
    """Fallisce se troppi <p> hanno lo stesso testo (normalizzato). Cfr. skill 8.1c."""
    import re
    from collections import Counter

    paras = re.findall(r"<p[^>]*>(.*?)</p>", html, flags=re.IGNORECASE | re.DOTALL)
    texts: list[str] = []
    for raw in paras:
        t = re.sub(r"<[^>]+>", " ", raw)
        t = re.sub(r"\s+", " ", t).strip().lower()
        if len(t) < 48:
            continue
        texts.append(t)
    if not texts:
        return
    top = Counter(texts).most_common(1)[0]
    if top[1] > max_identical:
        raise ValueError(
            f"Corpo blog: {top[1]} paragrafi quasi identici (max {max_identical}). "
            "Ridurre template o aggiungere prosa unica (SKILL 8.1c)."
        )


def build_paragraphs(topic: str, anchors: list[tuple[str, str]], n: int = 14) -> str:
    """Paragrafi con transizioni e fonti istituzionali, senza ripetizione meccanica."""
    links = " ".join(f'<a href="{u}">{t}</a>' for t, u in anchors)
    opens = [
        "In primo luogo,", "Successivamente,", "Parallelamente,", "D'altra parte,", "Inoltre,", "Per converso,",
        "Dal punto di vista operativo,", "In termini pratici,", "Nello specifico,", "Sul piano normativo,",
        "Per quanto riguarda il Veneto,", "Nel Padovano,", "In agenzia osserviamo che,", "Dalla parte dell'acquirente,",
        "Dal lato del venditore,", "Per completezza,", "Sul versante fiscale,", "Per chi deve finanziare l'acquisto,",
        "Sul mercato secondario,", "Per le nuove costruzioni,", "In fase di perizia,", "All'atto del rogito,",
        "Prima del compromesso,", "Durante la trattativa,", "Sul fronte documentale,", "In sintesi,", "Infine,",
    ]
    cores = [
        f"i dati dell'<a href='https://www.istat.it' target='_blank' rel='noopener noreferrer'>ISTAT</a> descrivono pressioni su prezzi e consumi delle famiglie: contesto macro, non quotazione del singolo caso legato a «{topic}».",
        f"le pubblicazioni della <a href='https://www.bancaditalia.it' target='_blank' rel='noopener noreferrer'>Banca d'Italia</a> sul credito ipotecario chiariscono spread e istruttoria, senza sostituire il contratto firmato in banca.",
        f"l'<a href='https://www.agenziaentrate.gov.it' target='_blank' rel='noopener noreferrer'>Agenzia delle Entrate</a> offre OMI semestrali e strumenti sui trasferimenti: il confronto su microzona resta il passaggio obbligato.",
        f"la <a href='https://www.ecb.europa.eu' target='_blank' rel='noopener noreferrer'>Banca centrale europea</a> condiziona i tassi di riferimento e, a catena, le condizioni di mercato osservabili sul mutuo.",
        f"il quadro normativo sull'<strong>APE</strong> e sull'efficienza (D.lgs. 192/2005 e successive modifiche) va verificato nelle versioni aggiornate prima di decisioni vincolanti.",
        f"il <a href='servizio-preliminari'>compromesso</a> ben impostato riduce attriti su clausole sospensive, tempi mutuo e penali.",
        f"una <a href='landing-valutazione'>valutazione</a> allineata a segmento e stato manutentivo evita pretese fuori mercato su prezzo richiesto o offerta.",
    ]
    tails = [
        f"Su «{topic}», {links} servono come bussola, non come promessa di risultato.",
        f"Per «{topic}», integriamo {links} con verifiche documentali e titoli edilizi prima di impegni definitivi.",
        f"Nel perimetro «{topic}», {links} aiutano a impostare domande corrette a notaio e istituti.",
        f"Affrontando «{topic}», {links} vanno letti insieme a perizia e pratiche urbanistico-catastali ove pertinenti.",
        f"Riguardo a «{topic}», {links} orientano il metodo; evitiamo percentuali ricavate da aggregatori non istituzionali.",
        f"Nel filone «{topic}», {links} completano il quadro insieme a conformità e stato impianti.",
    ]
    paras = []
    for i in range(n):
        op = opens[i % len(opens)]
        cr = cores[i % len(cores)]
        tl = tails[i % len(tails)]
        paras.append(f"<p>{op} {cr} {tl}</p>")
    return "\n".join(paras)


def build_article(cfg: dict) -> str:
    slug = cfg["slug"]
    img = cfg["img"]
    bread_name = cfg["bread"]
    section = cfg["section"]
    html_title = cfg["html_title"]
    meta_desc = cfg["meta_desc"]
    h1 = cfg["h1"]
    cat_badge = cfg["cat_badge"]
    alt_img = cfg["alt_img"]
    breadcrumb_tail = cfg["breadcrumb_tail"]
    intro = cfg["intro"]
    body_extra = cfg.get("body_extra", "")
    body_mid = cfg.get("body_mid", "")
    anchors = cfg["anchors"]
    topic = cfg["topic"]
    faqs = cfg["faqs"]
    related = cfg["related"]
    cta_primary = cfg["cta_primary"]
    cta_secondary = cfg["cta_secondary"]
    share_label = cfg.get("share_label", html_title[:40])

    body_n = int(cfg.get("body_n", 44))
    if body_n > MAX_TEMPLATE_PARAGRAPHS:
        raise ValueError(
            f"body_n={body_n} supera MAX_TEMPLATE_PARAGRAPHS={MAX_TEMPLATE_PARAGRAPHS}. "
            "Aggiungere prosa unica (body_mid) invece di allungare il template (SKILL 8.1c)."
        )
    body_core = build_paragraphs(topic, anchors, n=body_n)
    body_parts = [intro, body_extra]
    if body_mid:
        body_parts.append(body_mid)
    body_parts.extend([body_core, DISCLAIMER_BODY, MEDIAZIONE])
    body = "\n".join(body_parts)
    assert_body_paragraph_diversity(body)

    wc_body = word_count(body)
    blog_obj = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": html_title,
        "description": meta_desc,
        "image": [f"https://righettoimmobiliare.it/{img}"],
        "author": {
            "@type": "Person",
            "name": "Gino Capon",
            "jobTitle": "Agente Immobiliare",
            "worksFor": {
                "@type": "RealEstateAgent",
                "name": "Gruppo Immobiliare Righetto di Capon Gino",
                "url": "https://righettoimmobiliare.it",
            },
        },
        "publisher": {
            "@type": "Organization",
            "name": "Righetto Immobiliare",
            "url": "https://righettoimmobiliare.it",
            "logo": {"@type": "ImageObject", "url": "https://righettoimmobiliare.it/img/og-default.webp"},
        },
        "datePublished": DATE_ISO,
        "dateModified": DATE_ISO,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://righettoimmobiliare.it/{slug}"},
        "articleSection": section,
        "keywords": cfg["keywords"],
        "wordCount": wc_body,
        "inLanguage": "it-IT",
    }

    faq_obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }

    bread_obj = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://righettoimmobiliare.it/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://righettoimmobiliare.it/blog"},
            {"@type": "ListItem", "position": 3, "name": bread_name, "item": f"https://righettoimmobiliare.it/{slug}"},
        ],
    }

    head = HEAD_TOP.format(
        html_title=html_title,
        meta_desc=meta_desc,
        slug=slug,
        img_path=img,
        time_ts=TIME_TS,
        section=section,
        blog_json=json.dumps(blog_obj, ensure_ascii=False),
        faq_json=json.dumps(faq_obj, ensure_ascii=False),
        bread_json=json.dumps(bread_obj, ensure_ascii=False),
    )

    faq_html = ""
    for q, a in faqs:
        faq_html += f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>\n'

    rel_html = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in related)

    middle = f"""
<body>
<a href="#main-content" class="skip-link">Vai al contenuto principale</a>
<header>
  <div class="hi">
    <a href="/" class="logo">Righetto <span>Immobiliare</span></a>
    <nav><a href="/">Home</a><a href="immobili">Immobili</a><a href="servizi">Servizi</a><a href="chi-siamo">Chi siamo</a><a href="blog" class="active">Blog</a><a href="contatti">Contatti</a><a href="faq">FAQ</a></nav>
    <div class="h-cta"><a class="h-tel" href="tel:+390498843484">049.88.43.484</a><a class="h-btn" href="contatti">Valutazione gratuita</a></div>
  </div>
  <button class="nav-burger" id="burgerBtn" aria-label="Menu"><span></span><span></span><span></span></button>
</header>
<div class="nav-mobile" id="navMobile">
  <a href="/">Home</a><a href="chi-siamo">Chi Siamo</a><a href="immobili">Immobili</a><a href="servizi">Servizi</a><a href="blog">Blog</a><a href="faq">FAQ</a><a href="contatti" class="nav-mobile-cta">Parla con noi</a>
</div>

<main id="main-content">
<div class="art-hero">
  <img class="art-hero-img" src="{img}" alt="{alt_img}" width="1200" height="630" fetchpriority="high">
  <div class="art-hero-overlay">
    <div class="art-hero-inner">
      <div class="breadcrumb"><a href="/">Home</a> / <a href="blog">Blog</a> / {breadcrumb_tail}</div>
      <span class="cat-badge">{cat_badge}</span>
      <h1>{h1}</h1>
      <div class="art-hero-meta"><div class="av">G</div><span>Gino Capon</span><span>&middot;</span><span>{DATE_IT}</span><span>&middot;</span><span>Aggiornamento {DATE_IT}</span></div>
    </div>
  </div>
</div>

<div class="art-container">
  <div class="art-content">
    {body}

    <div class="cta-row">
      <a class="cta-deep" href="{cta_primary[1]}">{cta_primary[0]}</a>
      <a class="cta-deep-outline" href="{cta_secondary[1]}">{cta_secondary[0]}</a>
    </div>

    <h2 id="tab-fonti">Tabella riepilogo fonti ufficiali citate</h2>
    <table>
      <thead><tr><th>Argomento</th><th>Fonte primaria</th><th>Uso suggerito</th></tr></thead>
      <tbody>
        <tr><td>Prezzi medi zona</td><td>OMI — Agenzia delle Entrate</td><td>Confronto semestrale e microzona</td></tr>
        <tr><td>Inflazione / famiglie</td><td>ISTAT</td><td>Contesto costi e reddito</td></tr>
        <tr><td>Mutui aggregati</td><td>Banca d'Italia</td><td>Condizioni di mercato, non offerta singola</td></tr>
        <tr><td>Tassi policy</td><td>BCE</td><td>Quadro tassi di riferimento</td></tr>
        <tr><td>Efficienza energetica</td><td>Normativa nazionale vigente + APE</td><td>Verifica requisiti edilizi e attestato</td></tr>
      </tbody>
    </table>

    <p style="font-size:.8rem;color:var(--grigio);margin-top:2rem"><strong>Ultimo aggiornamento contenuti:</strong> {DATE_IT}. Verificare sempre testi ufficiali e circolari aggiornate.</p>
  </div>

  <div class="faq-section" id="faq">
    <h2 style="font-family:'Cormorant Garamond',serif;font-size:1.75rem;border-bottom:2px solid var(--oro);padding-bottom:.4rem;margin-bottom:1rem">Domande frequenti</h2>
    {faq_html}
  </div>

  <div class="cta-banner">
    <div class="cta-banner-text">
      <h3>Valutazione gratuita e confronto sul mercato reale</h3>
      <p>Operiamo da Limena su oltre 101 comuni: vendita, acquisto, locazione e preliminari con documentazione ordinata.</p>
    </div>
    <a href="landing-valutazione" class="cta-banner-btn">Richiedi valutazione</a>
  </div>

  <div class="share-bar">
    <span style="font-size:.78rem;font-weight:600;color:var(--grigio)">Condividi:</span>
    <button type="button" class="share-btn" onclick="navigator.clipboard.writeText('https://righettoimmobiliare.it/{slug}');this.textContent='Copiato!'">Copia link</button>
    <a class="share-btn" href="https://wa.me/?text={share_label.replace(' ', '%20')}%20https%3A%2F%2Frighettoimmobiliare.it%2F{slug}" target="_blank" rel="noopener noreferrer">WhatsApp</a>
  </div>

  <div class="author-bio">
    <img src="img/team/titolari.webp" alt="Gino Capon" width="64" height="64" loading="lazy">
    <div class="author-bio-text">
      <strong>Gino Capon</strong>
      <p>Fondatore di Righetto Immobiliare. Operativita' su Padova, Limena e provincia: vendita, acquisto, locazione. <a href="chi-siamo">Il team</a></p>
    </div>
  </div>

  <section class="blog-rich-cta-strip" aria-label="Consulenza immobiliare">
    <div class="blog-rich-cta-inner">
      <h2>Ti e' stato utile? <em>Ottieni di piu'</em></h2>
      <p class="blog-rich-cta-text">Contattaci per orientamento sul territorio e sulla sequenza preliminare–rogito.</p>
      <a class="blog-rich-btn" href="contatti">Richiedi consulenza</a>
      <span class="blog-rich-cta-sub"><a href="https://maps.app.goo.gl/xuCiRGDCSKskpTSf6?g_st=ic" target="_blank" rel="noopener noreferrer" style="color:rgba(247,245,241,0.88);text-decoration:underline">Lascia una recensione su Google</a></span>
    </div>
  </section>

  <div class="related">
    <h3>Articoli correlati</h3>
    <ul>
      {rel_html}
    </ul>
  </div>
</div>
</main>
"""

    return head + STYLE_BLOCK + middle + FOOTER_TMPL


ARTICLES: list[dict] = [
    {
        "filename": "blog-domanda-case-green-certificazione-padova-2026.html",
        "slug": "blog-domanda-case-green-certificazione-padova-2026",
        "img": "img/blog/blog-domanda-case-green-padova-2026.webp",
        "bread": "Case green e certificazione energetica Padova",
        "section": "Mercato locale",
        "html_title": "Domanda di case green ad alta efficienza nel Padovano: strategie con dati OMI e APE",
        "meta_desc": "Certificazione energetica, classi APE, mercato a Padova e in Veneto: metodo senza percentuali inventate, collegamenti OMI e ISTAT e consulenza Righetto.",
        "cat_badge": "Mercato locale",
        "alt_img": "Domanda case ad alta efficienza energetica e certificazione green nel Veneto",
        "breadcrumb_tail": "Case green Padova",
        "h1": "Case <strong>green</strong> nel Padovano: certificazione energetica, OMI e scelte consapevoli",
        "intro": """<p>Nei portali e nelle richieste che riceviamo in agenzia, emerge con forza l'interesse per immobili con <strong>alta efficienza energetica</strong> e consumi contenuti. In assenza di microdati proprietari verificabili pubblicamente, evitiamo percentuali tipo «più 25% di clic» non ricavabili da un nostro dataset: preferiamo ancorare il discorso a <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">OMI</a>, <a href="https://www.istat.it" target="_blank" rel="noopener noreferrer">ISTAT</a>, normativa sull'<a href="https://www.mase.gov.it" target="_blank" rel="noopener noreferrer">attestato APE</a> e buone pratiche per compratori e venditori nel territorio patavino. In questo testo trovate un percorso operativo, collegamenti utili e CTA verso <a href="servizio-valutazioni">valutazione</a> e <a href="blog-direttiva-case-green-limena-padova">Direttiva case green UE</a>.</p>""",
        "body_extra": """<h2 id="ape-omi">APE, OMI e coerenza dell'immobile sul mercato</h2>
<p>L'<strong>APE</strong> descrive prestazione energetica e incide su percezione del prezzo, su tempi di vendita e sulla domanda di famiglie attente a bollette e comfort. Le <strong>OMI</strong> restano la fotografia semestrale del mercato per microzona: vanno lette con cautela, perché descrivono bande e non il valore vincolante di un singolo appartamento. Per un quadro macro sul costo della vita e sui consumi delle famiglie italiane, utile il portale <a href="https://www.istat.it" target="_blank" rel="noopener noreferrer">ISTAT</a>. Chi vende una villa a <a href="zona-selvazzano">Selvazzano</a> o un appartamento tra <a href="zona-limena">Limena</a> e il capoluogo beneficia di documentazione ordinata: APE coerente con interventi reali, libretti impianto, certificazioni lavori.</p>
<h2 id="acquirente">Checklist acquirente: cosa chiedere prima della proposta</h2>
<ul>
<li>Classe energetica dichiarata e confronto con scheda APE registrata ai fini previsti dalla normativa.</li>
<li>Anni di costruzione, interventi su involucro e impianti, presenza di generatori dedicati e fonti rinnovabili.</li>
<li>Stato pagamenti incentivi fiscali legati a ristrutturazioni, se esistono incrocî con agevolazioni passate.</li>
<li>Conformità urbanistica e catastale, per evitare sorprese in banca sul mutuo.</li>
</ul>""",
        "body_mid": """<h2 id="segmenti">Domanda reale: come cambia tra segmenti</h2>
<p>Tra ville in collina, bifamiliari in cintura e appartamenti in condominio la <strong>domanda di efficienza</strong> non si traduce con la stessa intensità. Dove i consumi per riscaldamento pesano di più, l'interesse per involucro e impianti è più esplicito; in centro storico prevalgono vincoli architettonici che spostano l'attenzione su risanamento conservativo e impianti interni. In ogni caso, la lettura del prezzo resta legata a transazioni confrontabili e a bande OMI, non a slogan commerciali.</p>
<h2 id="venditore">Per il venditore: ordine documentale prima del marketing</h2>
<p>Chi mette in vendita un immobile con prestazione energetica curata ottiene un vantaggio narrativo solo se i documenti coincidono con i fatti: APE aggiornato dopo interventi, planimetrie allineate, regolarità edilizia verificata. In fase di visita, acquirenti attenti chiedono coerenza tra attestato, bollette recenti e percezione di comfort. Anticipare queste verifiche con il supporto dell'agenzia riduce rinegoziazioni tardive e sospensioni in banca.</p>
<h2 id="percorso-banca">Mutuo e sostenibilità della rata: collegamenti prudenti</h2>
<p>La banca valuta merito creditizio, loan-to-value e perizia: l'efficienza energetica può influire indirettamente sulla percezione del rischio idraulico/impiantistico, ma non sostituisce queste leve. Per orientarsi su tassi e spread conviene monitorare Banca d'Italia e BCE, poi confrontare offerte concrete. Sul territorio patavino, tempi di istruttoria e qualità della documentazione urbanistico-catastale restano spesso il collo di bottiglia più costoso delle chiacchiere su «case green».</p>
<h2 id="territorio">Territorio: microzone e attese degli acquirenti</h2>
<p>Padova e i comuni limitrofi presentano microzone con stock e velocità di rotazione diverse. Le OMI danno una fotografia semestrale utile a posizionare il bando di prezzo; ISTAT arricchisce il contesto macroeconomico. In sede, costruiamo percorsi con <a href="servizio-vendita">vendita</a> e <a href="servizio-valutazioni">stime</a> che rispettano queste fonti, evitando promesse numeriche non dimostrabili.</p>""",
        "anchors": [
            ("servizi vendita e preliminari", "servizio-vendita"),
            ("mappe prezzi OMI", "blog-quotazioni-locazioni-omi-istat-padova-2026"),
        ],
        "topic": "efficienza energetica e mercato padovano",
        "keywords": ["case green Padova", "APE Veneto", "OMI efficienza energetica"],
        "faqs": [
            ("L'APE sostituisce la perizia?", "No: APE e perizia rispondono a logiche diverse; la banca usa la perizia per il finanziamento, l'APE descrive prestazione energetica ai fini normativi e informativi."),
            ("Le OMI garantiscono il prezzo di vendita?", "No: offrono range semestrali per microzona; il prezzo di mercato si fonda su comparabili reali, stato manutentivo e domanda/offerta al momento della trattativa."),
            ("Dove trovo dati macroeconomici affidabili?", "ISTAT per prezzi al consumo e contesto famiglie; Banca d'Italia per credito; BCE per politica monetaria."),
            ("Cosa fa l'agenzia su immobili green?", "Ordiniamo documenti, evidenziamo coerenza APE-titoli, prepariamo marketing vero e supportiamo la fase preliminare."),
            ("Esistono valori certi sul plus valore delle classi A?", "Ogni richiesta va stimata con comparabili; non pubblichiamo percentuali fisse senza campione verificabile e mandato."),
            ("Come prenoto una consulenza?", "Contatti o modulo sul sito; operatività su 101 comuni da Limena."),
        ],
        "related": [
            ("Direttiva case green UE e Limena", "blog-direttiva-case-green-limena-padova"),
            ("APE in acquisto", "blog-ape-prestazione-energetica-acquisto-padova-2026"),
            ("Mutui e perizia", "blog-mutui-tasso-fisso-bancaitalia-padova-2026"),
        ],
        "cta_primary": ("Calcolo mutuo con Sara", "landing-chat-calcolo-mutuo"),
        "cta_secondary": ("Servizio valutazioni", "servizio-valutazioni"),
    },
    {
        "filename": "blog-tassi-mutui-minimi-approfittarne-padova-2026.html",
        "slug": "blog-tassi-mutui-minimi-approfittarne-padova-2026",
        "img": "img/blog/blog-tassi-mutui-minimi-padova-2026.webp",
        "bread": "Tassi mutui minimi Padova",
        "section": "Finanziamenti",
        "html_title": "Tassi mutui ai livelli più bassi della fase: come orientarsi nel Padovano con fonti Banca d'Italia",
        "meta_desc": "Indicatori Banca d'Italia, BCE e lettura cauta delle simulazioni. Esempi illustrativi senza promettere tassi: territorio patavino e mutuo prima casa.",
        "cat_badge": "Finanziamenti",
        "alt_img": "Consulenza mutuo e confronto tassi fissi in contesto bancario professionale",
        "breadcrumb_tail": "Tassi mutui",
        "h1": "Tassi mutui <strong>contenuti</strong>: come leggere la fase di mercato senza illusioni",
        "intro": """<p>Quando la stampa parla di «tassi ai minimi», conviene tradurre il titolo in numeri <strong>ufficiali</strong>: l'<a href="https://www.bancaditalia.it" target="_blank" rel="noopener noreferrer">Indagine sulla media dei tassi sui mutui</a> offre medie nazionali e stratificazioni utili, ma non sostituisce il foglio firmato in filiale. Evitiamo cifre tipo «200.000 euro a 900 euro al mese» senza spread e TAEG del contratto reale, perché ingannevoli. In questo articolo collegiamo BCE, Banca d'Italia, tempi di perizia e <a href="landing-mutuo">strumenti di simulazione</a> sul sito, con focus su famiglie in <a href="agenzia-immobiliare-padova">area padovana</a> e pendolarità verso <a href="articolo-riqualificazione">Mestre</a>.</p>""",
        "body_extra": """<h2 id="eurirs">Parametri di mercato e tasso fisso: cosa monitorare</h2>
<p>Il <strong>mutuo tasso fisso</strong> ancorava storicamente l'evoluzione di indici di mercato e spread bancari: l'offerta cambia per durata, LTV e profilo reddituale. La <a href="https://www.ecb.europa.eu" target="_blank" rel="noopener noreferrer">BCE</a> pubblica decisioni sui tassi di policy che influiscono sull'intera curva dei tassi di mercato, con effetti mediati dalle banche. Per chi acquista su <a href="zona-vigonza">Vigonza</a> o in centro a Padova, la variabile decisiva resta l'istruttoria sulla singola unità.</p>
<h2 id="doc">Documenti e tempistiche collegate alla casa</h2>
<p>Per chi vende un veicolo o gestisce pratiche collaterali, la parte immobiliare richiede comunque <strong>planimetrie</strong>, <strong>conformità</strong> e <strong>visure</strong> allineate: ritardi qui si traducono spesso in slittamento della delibera. Rimandiamo a <a href="blog-mutuo-documenti-tempi-prima-casa-padova-2026">documenti mutuo prima casa</a> e alla <a href="servizio-preliminari">gestione preliminare</a>.</p>""",
        "body_mid": """<h2 id="lettura-tassi">Come leggere le medie ufficiali senza autoinganno</h2>
<p>Le medie nazionali pubblicate da Banca d'Italia descrivono un mercato aggregato: utili per capire la fase del ciclo, inutili se scambiate per il TAEG del proprio contratto. Conviene separare nettamente <strong>policy rate</strong> (BCE), <strong>condizioni bancarie</strong> (spread commerciali, polizze, vincoli) e <strong>profilo del richiedente</strong> (stabilità reddituale, anticipo, garanzie). In assenza di questi tre livelli, ogni simulazione online resta un'ipotesi educativa.</p>
<h2 id="variabile-fisso">Variabile, fisso e ibridi: domande da fare in filiale</h2>
<p>La scelta tra tasso variabile e fisso dipende da orizzonte temporale, tolleranza al rischio e struttura del reddito familiare. Chiedere sempre durata del vincolo, eventuali penali di estinzione anticipata, costi fissi ricorrenti e impatto delle polizze accessorie. Sul piano immobiliare, la qualità della perizia e la regolarità dell'unità incidono su LTV e tempi: per approfondimenti metodologici rimandiamo a <a href="blog-mutuo-fisso-variabile-padova-2026">fisso e variabile</a> e alla <a href="landing-chat-calcolo-mutuo">simulazione orientativa</a>.</p>
<h2 id="tempi">Tempi: quando la casa rallenta la banca</h2>
<p>Condomini con gravami, difformità urbanistiche o successioni incomplete bloccano la delibera anche se il tasso «sembra» conveniente. Per questo affianchiamo la parte documentale della compravendita con checklist condivise con periti e istituti quando possibile. L'obiettivo non è inseguire il titolo di giornale sul minimo storico, ma chiudere la pratica con rate e costi totali coerenti con il budget dichiarato.</p>""",
        "anchors": [
            ("guida fisso e variabile", "blog-mutuo-fisso-variabile-padova-2026"),
            ("mutui Padova panoramica", "blog-mutui-casa-padova-2026"),
        ],
        "topic": "mutui tasso fisso e ciclo dei tassi",
        "keywords": ["mutuo tasso fisso", "Banca d'Italia tassi medi mutui", "mutuo Padova"],
        "faqs": [
            ("Posso fidarmi di una simulazione online?", "Le simulazioni orientano ma TAEG, imposte e assicurazioni del contratto reale possono cambiare la rata: confrontare almeno due intermediari."),
            ("Dove trovo tassi medi ufficiali?", "Banca d'Italia, sezione statistiche e pubblicazioni sull'indebitamento delle famiglie e condizioni mutuo."),
            ("Il tasso fisso elimina ogni rischio?", "Riduce variabilità della rata ma non sostituisce garanzie su reddito, lavoro e valore immobile."),
            ("Cosa incide sulla delibera?", "LTV, perizia, regolarità urbanistica e merito creditizio."),
            ("Righetto eroga mutui?", "No: supportiamo la parte immobiliare e i tempi di compravendita; per il prodotto creditizio si rivolge a banche e broker autorizzati."),
            ("Come prenoto consulenza?", "Contatti o chat sul sito."),
        ],
        "related": [
            ("Mutui Banca d'Italia Padova", "blog-mutui-tasso-fisso-bancaitalia-padova-2026"),
            ("Prima casa", "blog-mutuo-prima-casa-padova"),
            ("Surroga", "blog-surroga-mutuo-padova-2026"),
        ],
        "cta_primary": ("Simulazione mutuo", "landing-chat-calcolo-mutuo"),
        "cta_secondary": ("Preliminari", "servizio-preliminari"),
    },
    {
        "filename": "blog-bonus-mobili-2026-massimizzare-ristrutturazioni.html",
        "slug": "blog-bonus-mobili-2026-massimizzare-ristrutturazioni",
        "img": "img/blog/blog-bonus-mobili-ristrutturazioni-2026.webp",
        "bread": "Bonus mobili e ristrutturazioni 2026",
        "section": "Fisco",
        "html_title": "Bonus mobili e grandi elettrodomestici 2026: massimizzare la detrazione con ristrutturazioni edilizie",
        "meta_desc": "Legame tra interventi edilizi agevolati e acquisto mobili: verifica sempre testo di legge vigente e circolari Agenzia delle Entrate.",
        "cat_badge": "Fisco",
        "alt_img": "Cantiere ristrutturazione e bonus mobili elettrodomestici con detrazioni IRPEF",
        "breadcrumb_tail": "Bonus mobili",
        "h1": "<strong>Bonus mobili</strong> 2026: detrazioni, ristrutturazioni e cosa verificare prima dell'acquisto",
        "intro": """<p>Il <strong>bonus mobili e grandi elettrodomestici</strong> è storicamente collegato a interventi di ristrutturazione edilizia che rientrano negli agevolamenti previsti dalla legge: percentuali, massimali e scadenze <strong>cambiano con i decreti annuali</strong>. Per questo motivo non pubblichiamo «50% fino a 5.000 euro» come certezza assoluta senza rimando al testo aggiornato. Consultate sempre <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a> e pareri commercialisti prima di imputare costi. Qui mettiamo in fila logica della norma, documenti da conservare, e collegamenti con il <a href="servizio-vendita">processo di vendita</a> quando finite lavori e presentate la casa.</p>""",
        "body_extra": """<h2 id="legame">Ristrutturazione agevolata e acquisto arredi: il legame tipico</h2>
<p>Le detrazioni sono di solito subordinate a tipologie di intervento e a scadenze antecedenti il rogito o successive secondo il proprio caso. Il <strong>cantiere documentato</strong> (contratti, pagamenti tracciabili, DURC dipendenti lavori) è la base per contestare l'agevolazione in sede fiscale. In parallelo, chi vende dopo lavori importanti può valorizzare materialmente l'immobile: rimandiamo a <a href="blog-home-staging-padova">home staging</a>.</p>
<h2 id="ecobonus">Ecobonus, efficienza energetica e APE dopo i lavori</h2>
<p>Se i lavori spostano la classe energetica, aggiornare l'<strong>APE</strong> è parte del pacchetto di credibilità verso acquirenti e banche. Non confondete il beneficio fiscale con la valorizzazione automatica del prezzo: serve comparabile di mercato, che per il Padovano si appoggia alle OMI e alle transazioni recenti.</p>""",
        "body_mid": """<h2 id="tracciabilita">Pagamenti e tracciabilità: cosa conservare</h2>
<p>Le agevolazioni fiscali legate a ristrutturazioni e, dove previsto, agli acquisti successivi di arredi richiedono di solito <strong>tracciabilità dei pagamenti</strong> e coerenza temporale con i lavori. Conservare fatture, bonifici strutturati e documentazione del cantiere secondo indicazioni del commercialista riduce contestazioni in sede di controllo. Dal lato immobiliare, tenere allineate planimetrie e stati di fatto evita attriti in vendita dopo i lavori.</p>
<h2 id="timing">Timing tra fine lavori, certificazioni e messa in vendita</h2>
<p>Chi intende vendere dopo una ristrutturazione agevolata deve pianificare aggiornamenti dell'APE, collaudi impiantistici e eventuali accatastamenti prima del marketing. Presentare un immobile «nuovo» con documenti vecchi genera sconti negoziali o richieste di riduzione. In agenzia preferiamo una sequenza chiara: verifiche preliminari, scheda immobile allineata alla realtà, visite solo con acquirenti profilati.</p>
<h2 id="commercialista">Righetto e fiscalità: confini professionali</h2>
<p>Non forniamo pareri fiscali vincolanti: il nostro contributo è ordinare la parte urbanistico-catastale, supportare la valorizzazione sul mercato e coordinare tempi con il notaio. Per percentuali, massimali e requisiti dell'anno d'imposta rimandiamo a <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a> e al commercialista. Per la vendita post intervento, rimandiamo a <a href="blog-tasse-vendita-casa">tasse di vendita</a> e <a href="blog-documenti-vendita-casa">documenti</a>.</p>""",
        "anchors": [
            ("Costi vendita con tasse", "blog-tasse-vendita-casa"),
            ("Documenti vendita", "blog-documenti-vendita-casa"),
        ],
        "topic": "bonus mobili e fiscalità ristrutturazioni",
        "body_n": 46,
        "keywords": ["bonus mobili", "detrazioni IRPEF", "ristrutturazione"],
        "faqs": [
            ("Posso detrarre mobili senza ristrutturazione?", "La disciplina prevede requisiti specifici: verificare il testo di legge vigente e i requisiti per l'anno d'imposta."),
            ("Quanto conservare le fatture?", "Conservazione secondo obblighi fiscali e consiglio del commercialista."),
            ("La detrazione aumenta il prezzo di vendita?", "Non automaticamente: conta la qualità reale dei lavori e il confronto con compravendute simili."),
            ("Righetto dà pareri fiscali?", "No: ci occupiamo di parte immobiliare; per fiscalità rivolgersi a commercialista."),
            ("Dove leggere aggiornamenti?", "Agenzia delle Entrate, sezione agevolazioni e circolari."),
            ("Come valorizzo post bonus?", "Valutazione con comparabili OMI e presentazione documentale."),
        ],
        "related": [
            ("Agevolazioni prima casa", "blog-agevolazioni-prima-casa-2026"),
            ("Tasse vendita", "blog-tasse-vendita-casa"),
            ("APE acquisto", "blog-ape-prestazione-energetica-acquisto-padova-2026"),
        ],
        "cta_primary": ("Valutazione immobile", "landing-valutazione"),
        "cta_secondary": ("Contatti", "contatti"),
    },
    {
        "filename": "blog-geopolitica-ucraina-prezzi-mutui-italia-veneto-2026.html",
        "slug": "blog-geopolitica-ucraina-prezzi-mutui-italia-veneto-2026",
        "img": "img/blog/blog-geopolitica-mercato-immobiliare-italia-2026.webp",
        "bread": "Geopolitica e mercato immobiliare",
        "section": "Mercato locale",
        "html_title": "Geopolitica, energia e mutui: effetti possibili su case nel Nord-Est e lettura prudenziale 2026",
        "meta_desc": "Canali di trasmissione da shock energetici e tassi ai prezzi delle case: BCE, ISTAT, Banca d'Italia, senza previsioni miracolose.",
        "cat_badge": "Mercato locale",
        "alt_img": "Mappa astratta Europa energia mercato immobiliare Italia editoriale",
        "breadcrumb_tail": "Geopolitica e mercato",
        "h1": "Shock <strong>energetici</strong> e contesto mutui: cautele per chi compra o vende nel Veneto",
        "intro": """<p>Le tensioni legate al conflitto in Ucraina, pur essendo lontane geograficamente, hanno contribuito — insieme ad altri fattori — a fasi di <strong>volatilità sulle commodity energetiche</strong> e sui mercati finanziari. Chi lavora sul mattone non deve trasformare titoli di giornale in consulenza investimento. Preferiamo rimandare a <a href="https://www.ecb.europa.eu" target="_blank" rel="noopener noreferrer">BCE</a> per la politica monetaria, a <a href="https://www.istat.it" target="_blank" rel="noopener noreferrer">ISTAT</a> per inflazione e contesto famiglie, e alla <a href="https://www.bancaditalia.it" target="_blank" rel="noopener noreferrer">Banca d'Italia</a> per il credito. Nel Veneto e su <a href="zona-limena">Limena</a> osserviamo domanda resiliente in diversi segmenti, ma ogni microzona richiede comparabili propri. Leggete anche <a href="blog-immobiliare-geopolitica-energia-tassi-2026">Geopolitica, energia e tassi</a> pubblicato sul nostro blog.</p>""",
        "body_extra": """<h2 id="canali">Canali verso il mercato delle case</h2>
<p>Non esiste una formula lineare «caos estero = più X per cento al mq»: prezzi e tempi di vendita dipendono da offerta locale, tassi effettivamente applicati, redditi e demografia. L'inflazione energetica può pesare sul budget familiare e indirettamente sulla sostenibilità della rata, dato che ISTAT monitora prezzi al consumo. Le decisioni BCE condizionano i tassi di mercato con ritardi e filtri bancari.</p>
<h2 id="veneto">Veneto e mobility energy</h2>
<p>Il costo del <strong>carburante</strong> e delle utility incide sul potere d'acquisto: ISTAT pubblica indici utili al contesto, non al singolo contratto di locazione. Per un operatore immobiliare, la traduzione pratica è verificare renda ancora sostenibile il canone o la rata rispetto al reddito dichiarato, senza improvvisare strategie.</p>""",
        "body_mid": """<h2 id="trasmissione">Canali di trasmissione: energia, tassi, redditi disponibili</h2>
<p>Shock su commodity e volatilità finanziaria possono influire su inflazione e su decisioni di politica monetaria, con effetti mediati sui tassi applicati alle famiglie. Sul mercato delle case, il canale non è automatico: conta quanto quei movimenti pesano sui redditi disponibili, sulla fiducia e sull'offerta locale. Per questo integriamo letture macro con <a href="blog-quotazioni-locazioni-omi-istat-padova-2026">OMI e contesto</a> sul territorio.</p>
<h2 id="prudenza">Prudenza operativa per chi compra o vende nel Nord-Est</h2>
<p>Evitare correlazioni narrative lineari tra titoli esteri e prezzo del proprio trilocale. Preferire scenario analysis: stress della rata, margine di risparmio, liquidità post-acquisto. Per il venditore, focus su qualità dell'immobile e documenti: in fasi incerte, compratori selezionano stock con rischi residui più bassi.</p>
<h2 id="locazione">Affitto: canone e costi vivi</h2>
<p>Nei contratti di locazione, la dinamica dei costi fissi incide sulla contrattazione. Le OMI locazione forniscono bande di riferimento ma non sostituiscono il mercato reale tra annunci e transazioni recenti. In agenzia affrontiamo <a href="servizio-locazioni">locazioni</a> con attenzione a sostenibilità del canone rispetto al reddito dichiarato.</p>""",
        "anchors": [
            ("geopolitica tassi precedente", "blog-immobiliare-geopolitica-energia-tassi-2026"),
            ("crisi e prezzi locali", "blog-crisi-immobiliare-padova-2026"),
        ],
        "topic": "geopolitica energia e tassi effetti immobiliare",
        "keywords": ["geopolitica mutui", "BCE tassi", "mercato immobiliare Veneto"],
        "faqs": [
            ("La guerra determina da sola il prezzo della mia casa?", "No: conta una combinazione di tassi, domanda locale, qualità dell'immobile e stock disponibile."),
            ("Dove aggiorno me su inflazione?", "ISTAT, indici prezzi al consumo e bollettini periodici."),
            ("Chi decide i tassi di policy?", "BCE; le banche applicano spread e condizioni commerciali."),
            ("Cosa fare se ho mutuo variabile?", "Valutare con consulente creditizio rinegoziazione o passaggio a fisso, caso per caso."),
            ("Righetto offre trading o hedging?", "No: siamo intermediari immobiliari; per hedge finanziario rivolgersi a professionisti."),
            ("Come impatta sull'affitto?", "Se i costi fissi salgono, la contrattazione locativa può cambiare: usare OMI locazione e consapevolezza."),
        ],
        "related": [
            ("Geopolitica energia tassi", "blog-immobiliare-geopolitica-energia-tassi-2026"),
            ("Crisi immobiliare Padova", "blog-crisi-immobiliare-padova-2026"),
            ("Mutui BdI", "blog-mutui-tasso-fisso-bancaitalia-padova-2026"),
        ],
        "cta_primary": ("Parla con Sara", "landing-chat-calcolo-mutuo"),
        "cta_secondary": ("Compravendite Veneto", "blog-compravendite-veneto-cintura-padova-2026"),
    },
    {
        "filename": "blog-agenzia-immobiliare-top-servizi-padova-2026.html",
        "slug": "blog-agenzia-immobiliare-top-servizi-padova-2026",
        "img": "img/blog/blog-agenzia-top-servizi-padova-2026.webp",
        "bread": "Qualità servizi agenzia Padova",
        "section": "Vita d'Agenzia",
        "html_title": "Cosa distingue un'agenzia immobiliare di alto livello: risposte rapide, processi chiari e tool digitali",
        "meta_desc": "Standard di servizio Righetto Immobiliare: tempi, comunicazione, mutuo orientativo e documentazione — senza promettere 24/7 umano assoluto.",
        "cat_badge": "Vita d'Agenzia",
        "alt_img": "Professionista agenzia immobiliare con strumenti digitali e servizio clienti",
        "breadcrumb_tail": "Qualità servizi",
        "h1": "Un'<strong>agenzia immobiliare</strong> di fascia alta: cosa deve offrire oggi (e cosa offriamo noi)",
        "intro": """<p>Il mercato richiede <strong>risposte organizzate</strong>, appuntamenti preparati e uso intelligente dei canali digitali. Attenzione alle promesse impossibili: «umano 24 ore su 24 senza soluzione di continuità» non è realistico per una PMI seria. Preferiamo dichiarare processi: centralino e WhatsApp negli orari d'ufficio, <a href="#faq">chatbot Sara per orientamento</a> fuori orario su temi ricorrenti, checklist documenti e <a href="servizio-vendita">servizio vendita</a> con tempi di risposta definiti in sede. Numeri verificabili del brand: oltre <strong>350 immobili</strong> trattati, <strong>101 comuni</strong>, <strong>127 recensioni</strong> Google con <strong>4,9/5</strong>, soddisfazione dichiarata <strong>98%</strong> dal questionario interno; operatività dal <strong>2000</strong>.</p>""",
        "body_extra": """<h2 id="std">Standard operativi in agenzia</h2>
<p>ricezione richiesta, prioritizzazione, call-back, invio scheda immobile, proposta visite calibrate, feedback scritto post visita. Per <a href="servizio-locazioni">locazioni</a> corrediamo pratiche con focus anti-inadempimento e registro contratti. Per <a href="servizio-valutazioni">stime</a> allineiamo segmento, stato e OMI.</p>
<h2 id="ai">Tool digitali e matching</h2>
<p>Il chatbot <strong>Sara</strong> non sostituisce l'agente ma smista domande ripetitive e invita a contatti umani quando serve decisione vincolante. Siamo consapevoli che l'<em>AI</em> è un ausilio, non una garanzia legale.</p>""",
        "body_mid": """<h2 id="metriche">Cosa misuriamo davvero: tempi e chiarezza</h2>
<p>Un servizio di fascia alta si giudica da <strong>tempi di risposta</strong> realistici, da trasparenza sui passaggi (visita, controproposta, documenti) e da capacità di prevenire errori catastali o urbanistici prima del compromesso. Non misuriamo il valore con slogan su «disponibilità infinita», ma con processi ripetibili e feedback scritti dopo le visite.</p>
<h2 id="comunicazione">Comunicazione: canali e aspettative</h2>
<p>Telefono e WhatsApp aziendale negli orari di lavoro, moduli sul sito, chat per orientamento fuori orario: ogni canale ha uno scopo. L'agente resta il decision maker su prezzi, strategia e preliminare; i tool digitali riducono attrito informativo. Per orientarsi sulla scelta dell'intermediario, rimandiamo a <a href="blog-scegliere-agenzia-immobiliare-padova-2026">come scegliere l'agenzia</a>.</p>
<h2 id="documentazione">Documentazione e mutuo: supporto senza vendita del credito</h2>
<p>Ordiniamo planimetrie, visure e incrocî con periti quando la pratica lo richiede, senza vendere prodotti bancari. L'obiettivo è presentare un dossier credibile a banche e notai, riducendo round di integrazioni. Numeri di brand citati in introduzione restano quelli verificabili pubblicamente (portfolio, recensioni, storicità).</p>""",
        "anchors": [
            ("scegliere agenzia", "blog-scegliere-agenzia-immobiliare-padova-2026"),
            ("impegno quotidiano agenzia", "blog-impegno-quotidiano-agenzia-immobiliare"),
        ],
        "topic": "qualità servizi agenzia immobiliare padovana",
        "body_n": 50,
        "keywords": ["agenzia immobiliare Padova", "servizi vendita", "Righetto"],
        "faqs": [
            ("Rispondete di notte?", "Fuori orario l'orientamento passa dalla chat e dai moduli; in orario telefono e WhatsApp aziendale."),
            ("Organizzate visite rapide?", "Sì dopo idoneità acquirente e accordo proprietario."),
            ("Fate check mutui?", "Orientamento verso simulatori e professionisti creditizi; non vendiamo prodotti bancari."),
            ("Mi aiutate con pratiche commerciali veicoli?", "Non è nostro core business: rimandiamo a professionisti; sul mattone supportiamo perizie e documenti."),
            ("Qual è il compenso?", "Definito in sede nel mandato: vendita 3% + IVA per parte minimo 2.500 euro lotto vendita; affitto una mensilità + IVA."),
            ("Come contattarvi?", "049.88.43.484, modulo contatti, <a href='contatti'>sede Limena</a>."),
        ],
        "related": [
            ("Scegliere agenzia Padova", "blog-scegliere-agenzia-immobiliare-padova-2026"),
            ("Impegno quotidiano", "blog-impegno-quotidiano-agenzia-immobiliare"),
            ("Vendita servizio", "servizio-vendita"),
        ],
        "cta_primary": ("Richiedi consulenza", "contatti"),
        "cta_secondary": ("Valutazione gratuita", "landing-valutazione"),
    },
]


def main() -> None:
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for cfg in ARTICLES:
        html = build_article(cfg)
        path = os.path.join(root, cfg["filename"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        body_only = "\n".join(
            [
                cfg["intro"],
                cfg.get("body_extra", ""),
                cfg.get("body_mid", ""),
                build_paragraphs(cfg["topic"], cfg["anchors"], n=int(cfg.get("body_n", 44))),
                DISCLAIMER_BODY,
                MEDIAZIONE,
            ]
        )
        print(cfg["filename"], "wordCount corpo (schema):", word_count(body_only), "| pagina intera:", word_count(html))


if __name__ == "__main__":
    main()
