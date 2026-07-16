# -*- coding: utf-8 -*-
"""Genera 4 articoli blog + aggiorna lista statica (eseguire: python tools/gen-blog-maggio-2026.py)"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HEAD = """<!DOCTYPE html>
<html lang="it">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PHEL8KXLBX"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-PHEL8KXLBX');</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#2C4A6E">
<title>{title}</title>
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="dns-prefetch" href="https://cdn.jsdelivr.net">
<link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="canonical" href="https://righettoimmobiliare.it/{slug}">
<meta property="og:type" content="article">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_desc}">
<meta property="og:url" content="https://righettoimmobiliare.it/{slug}">
<meta property="og:image" content="https://righettoimmobiliare.it/{img}">
<meta property="article:published_time" content="{iso}">
<meta property="article:author" content="Gino Capon">
<meta name="description" content="{meta_desc}">
<script type="application/ld+json">{article_ld}</script>
<script type="application/ld+json">{faq_ld}</script>
<script type="application/ld+json">{bread_ld}</script>
<link rel="stylesheet" href="css/fonts.css?v=3"><link rel="stylesheet" href="css/nav-mobile.css?v=5">
<link rel="stylesheet" href="css/scroll-reveal.css?v=3" media="print" onload="this.media='all'">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--nero:#152435;--bianco:#F7F5F1;--oro:#FF6B35;--grigio:#6B7A8D;--gc:#E1DBD1;--sfondo:#ECE7DF;--blu:#2C4A6E;--oro2:#FF8F5E}}
body{{font-family:'Montserrat',sans-serif;background:var(--bianco);color:var(--nero)}}
header{{background:var(--nero);position:sticky;top:0;z-index:100}}
.hi{{max-width:1380px;margin:0 auto;padding:0 1.5rem;height:74px;display:flex;align-items:center;gap:2rem}}
.logo{{font-family:'Cormorant Garamond',serif;color:#fff;font-size:1.28rem;font-weight:600}}.logo span{{color:var(--oro);font-style:italic}}
nav{{display:flex;flex:1;gap:.2rem}}nav a{{color:rgba(255,255,255,.72);font-size:.81rem;padding:.4rem .72rem}}nav a.active{{color:var(--oro)}}
.h-btn{{background:var(--oro);color:var(--nero);padding:.4rem .88rem;border-radius:6px;font-size:.76rem;font-weight:600}}
.art-hero{{position:relative}}.art-hero-img{{width:100%;height:468px;object-fit:cover;filter:brightness(.48)}}
.art-hero-overlay{{position:absolute;inset:auto 0 0 0;padding:2.65rem 1.5rem;background:linear-gradient(transparent,rgba(21,36,53,.95))}}
.art-hero-inner{{max-width:820px;margin:0 auto}}
.breadcrumb{{font-size:.72rem;color:rgba(255,255,255,.45);margin-bottom:.86rem}}.breadcrumb a{{color:rgba(255,255,255,.55)}}
.cat-badge{{font-size:.57rem;letter-spacing:.12em;text-transform:uppercase;background:rgba(255,107,53,.2);color:var(--oro);padding:.24rem .68rem;font-weight:700;display:inline-block;margin-bottom:.72rem}}
.art-hero h1{{font-family:'Cormorant Garamond',serif;font-size:1.95rem;font-weight:300;color:#fff;line-height:1.2}}.art-hero h1 strong{{font-weight:600;font-style:italic}}
.art-hero-meta{{display:flex;gap:1rem;align-items:center;font-size:.8rem;color:rgba(255,255,255,.5);margin-top:.92rem;flex-wrap:wrap}}
.av{{width:36px;height:36px;border-radius:50%;background:var(--oro);display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--nero)}}
.art-container{{max-width:820px;margin:0 auto;padding:2.4rem 1.5rem 3.55rem}}
.art-content{{font-size:.91rem;line-height:1.88}}
.art-content h2{{font-family:'Cormorant Garamond',serif;font-size:1.68rem;margin:2.28rem 0 .68rem;border-bottom:2px solid var(--oro);padding-bottom:.34rem}}
.art-content h3{{font-size:1.1rem;color:var(--blu);margin:1.15rem 0 .35rem}}
.art-content p{{margin-bottom:1.04rem}}.art-content ul,.art-content ol{{margin:0 0 1rem 1.28rem}}
.art-content a{{color:var(--blu);text-decoration:underline}}
.art-content table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.84rem}}
.art-content th,.art-content td{{border:1px solid var(--gc);padding:.55rem .65rem;text-align:left}}
.art-content th{{background:var(--sfondo)}}
.warn{{background:linear-gradient(135deg,rgba(44,74,110,.08),rgba(255,107,53,.08));border:1px solid var(--gc);border-radius:10px;padding:1rem 1.2rem;margin:1.2rem 0;font-size:.86rem}}
.aeo-box{{border:2px solid var(--blu);border-radius:12px;padding:1.15rem 1.3rem;margin-bottom:1.65rem;background:linear-gradient(135deg,rgba(44,74,110,.07),rgba(255,107,53,.06))}}
.aeo-box h2{{font-family:'Montserrat',sans-serif;font-size:.95rem;text-transform:uppercase;letter-spacing:.06em;color:var(--blu);margin:0 0 .55rem;border:none}}
.cap-img{{font-size:.72rem;color:var(--grigio);margin:.4rem 0 0}}
.cta-deep{{display:inline-flex;background:linear-gradient(180deg,var(--oro2),var(--oro));color:var(--nero);font-weight:800;padding:.8rem 1.62rem;border-radius:10px;font-size:.8rem;margin:1rem .75rem 1rem 0}}
.faq-item{{border:1px solid var(--gc);border-radius:8px;margin-bottom:.5rem}}
.faq-q{{padding:.86rem .98rem;font-weight:600;font-size:.84rem;cursor:pointer}}.faq-a{{max-height:0;overflow:hidden;transition:max-height .35s;background:var(--sfondo)}}
.faq-item.open .faq-a{{max-height:420px}}.faq-a-inner{{padding:0 .98rem .86rem;font-size:.83rem;color:var(--grigio)}}
.author-bio{{display:flex;gap:1.08rem;padding:1.38rem;border:1px solid rgba(44,74,110,.12);border-radius:12px;margin:1.68rem 0}}
.related{{background:var(--sfondo);border:1px solid var(--gc);padding:1.32rem;border-radius:10px}}
footer{{background:linear-gradient(180deg,var(--nero),#0d1a2a);color:rgba(255,255,255,.65);padding:2.35rem 1.5rem;font-size:.75rem}}
.skip-link{{position:absolute;top:-100%;background:var(--oro);color:var(--nero);padding:.46rem .9rem;z-index:9999}}.skip-link:focus{{top:0}}
@media(max-width:700px){{.art-hero-img{{height:288px}}}}
</style>
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
  <img class="art-hero-img" src="{img}" alt="{img_alt}" width="1200" height="800" fetchpriority="high">
  <div class="art-hero-overlay"><div class="art-hero-inner">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="blog">Blog</a> / {cat}</div>
    <span class="cat-badge">{cat}</span>
    <h1>{h1}</h1>
    <div class="art-hero-meta"><div class="av">G</div><span>Gino Capon</span><span>{date_it}</span><span>Aggiornato: {date_it}</span></div>
  </div></div>
</div>
<div class="art-container"><div class="art-content">
{body}
</div></div>
</main>
<footer><div class="fi">&copy; 2026 Gruppo Immobiliare Righetto — P.IVA 05182390285 — Via Roma 96, Limena (PD)</div></footer>
<script>document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{var p=this.parentElement,o=p.classList.contains('open');document.querySelectorAll('.faq-item.open').forEach(function(x){{x.classList.remove('open');}});if(!o)p.classList.add('open');}});}});</script>
<script src="js/nav-mobile.js?v=3" defer></script>
<script src="js/cookie-consent.js?v=3" defer></script>
</body></html>"""

ARTICLES = []  # filled below in run

def json_ld_article(slug, headline, desc, img, section, wc):
    import json
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": headline,
        "description": desc,
        "image": [f"https://righettoimmobiliare.it/{img}"],
        "author": {"@type": "Person", "name": "Gino Capon"},
        "publisher": {"@type": "Organization", "name": "Righetto Immobiliare", "url": "https://righettoimmobiliare.it"},
        "datePublished": "2026-05-20",
        "dateModified": "2026-05-20",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://righettoimmobiliare.it/{slug}"},
        "articleSection": section,
        "wordCount": wc,
        "inLanguage": "it-IT"
    }, ensure_ascii=False)

def json_ld_faq(items):
    import json
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]
    }, ensure_ascii=False)

def json_ld_bread(name, slug):
    import json
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://righettoimmobiliare.it/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://righettoimmobiliare.it/blog"},
            {"@type": "ListItem", "position": 3, "name": name}
        ]
    }, ensure_ascii=False)

def faq_html(items):
    h = '<div id="faq" style="margin-top:2rem"><h2 style="font-family:\'Cormorant Garamond\',serif;font-size:1.62rem;border-bottom:2px solid var(--oro);margin-bottom:.9rem">Domande frequenti</h2>'
    for q, a in items:
        h += f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>'
    return h + '</div>'

def author_related(related):
    r = '<div class="author-bio"><img src="img/team/titolari.webp" alt="Gino Capon Righetto Immobiliare" width="64" height="64" loading="lazy"><div><strong>Gino Capon</strong><p style="font-size:.8rem;color:#555">Titolare — Righetto Immobiliare, Limena (PD). Analisi di mercato per famiglie e investitori nel territorio patavino.</p><p style="font-size:.78rem;margin-top:.4rem"><a href="chi-siamo">Chi siamo</a></p></div></div>'
    r += '<div class="related"><h3 style="font-family:\'Cormorant Garamond\',serif">Articoli correlati</h3><ul style="margin-left:1.1rem;margin-top:.4rem">'
    for t, u in related:
        r += f'<li><a href="{u}">{t}</a></li>'
    return r + '</ul></div>'

# Content definitions - see gen-blog-maggio-2026-content.py imported or inline
exec(open(ROOT / 'tools' / 'gen-blog-maggio-2026-content.py', encoding='utf-8').read())

for art in ARTICLES:
    body = art['body'] + faq_html(art['faq']) + author_related(art['related'])
    html = HEAD.format(
        title=art['title_tag'],
        slug=art['slug'],
        og_title=art['og_title'],
        og_desc=art['og_desc'],
        img=art['img'],
        iso='2026-05-20T10:00:00+02:00',
        meta_desc=art['meta_desc'],
        article_ld=json_ld_article(art['slug'], art['headline'], art['meta_desc'], art['img'], art['cat'], art.get('wc', 2600)),
        faq_ld=json_ld_faq(art['faq']),
        bread_ld=json_ld_bread(art['bread'], art['slug']),
        cat=art['cat'],
        h1=art['h1'],
        date_it='20 maggio 2026',
        img_alt=art['img_alt'],
        body=body,
    )
    out = ROOT / f"{art['slug']}.html"
    out.write_text(html, encoding='utf-8')
    print('Wrote', out)

print('Done', len(ARTICLES), 'articles')
