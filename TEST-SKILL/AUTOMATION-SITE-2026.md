# AUTOMATION-SITE-2026

> **Skill di automazione universale** per generare siti web completi partendo dal design system di Righetto Immobiliare.
> Un comando, un sito. Claude legge questa skill, riceve il brief, e costruisce tutto.

---

## COME FUNZIONA

### Input richiesto dall'utente
```
Cosa voglio:     [descrizione del sito — es. "Sito per studio dentistico a Milano"]
Tempo:           [deadline — es. "1 settimana"]
Scopo:           [obiettivo — es. "Generare contatti pazienti"]
Pagine:          [elenco pagine — es. "Home, Servizi, Chi siamo, Contatti, Blog"]
Colore primario: [opzionale — es. "#2C4A6E" o "blu professionale"]
```

### Output generato
Claude genera **automaticamente**:
1. Tutte le pagine HTML con SEO completo
2. CSS con design system personalizzato
3. JS per interattività (menu, scroll, form)
4. `sitemap.xml` completo
5. `robots.txt` ottimizzato
6. Schema.org JSON-LD per ogni pagina
7. `CLAUDE.md` del nuovo progetto (con questa skill auto-attivata)

### Attivazione automatica
Il `CLAUDE.md` generato include il riferimento a questa skill. Ogni volta che Claude apre il progetto o crea una nuova pagina, i **4 LOOP di validazione** si attivano automaticamente.

---

## PARTE 1 — DESIGN SYSTEM UNIVERSALE

> Estratto e generalizzato dal progetto Righetto Immobiliare. Replicabile su qualsiasi settore.

### 1.1 VARIABILI CSS (Template)

```css
:root {
  /* === COLORI PRIMARI === */
  --primario:    #2C4A6E;   /* Colore brand principale */
  --primario-2:  #3A5F8C;   /* Hover state */
  --primario-3:  #4E789A;   /* Accento light */

  /* === COLORI ACCENT (CTA) === */
  --accent:      #B8D44A;   /* CTA primario — SOLO con testo scuro */
  --accent-2:    #CDED62;   /* Hover CTA */
  --accent-3:    #DFF09A;   /* Accent extra light */
  --accent-bg:   rgba(184,212,74,0.10); /* Background badge */

  /* === NEUTRALI === */
  --nero:        #152435;   /* Testo principale */
  --bianco:      #F7F5F1;   /* Background principale */
  --sfondo:      #ECE7DF;   /* Background sezioni alternate */
  --sfondo-2:    #E1DBD1;   /* Background cards */
  --carta:       #F2EDE7;   /* Background input/form */

  /* === TESTO === */
  --testo:       #152435;   /* Body text */
  --grigio:      #6B7A8D;   /* Testo secondario */
  --grigio-2:    #9AACBD;   /* Testo disabled/hint */

  /* === STATUS === */
  --verde:       #1E8449;   /* Success */
  --rosso:       #C0392B;   /* Error */

  /* === LAYOUT === */
  --nav-h:       74px;      /* Altezza navbar */
  --max-w:       1200px;    /* Max-width contenuto */
  --max-w-lg:    1400px;    /* Max-width sezioni larghe */
  --radius:      12px;      /* Border radius standard */
  --radius-sm:   8px;       /* Border radius piccolo */
  --radius-pill: 50px;      /* Pill/badge */
}

@media (max-width: 768px) {
  :root { --nav-h: 64px; }
}
```

**REGOLA:** Quando l'utente specifica un colore primario diverso, Claude deve:
1. Sostituire `--primario` col colore scelto
2. Calcolare `--primario-2` (+15% luminosità) e `--primario-3` (+30% luminosità)
3. Verificare contrast ratio >= 4.5:1 per testo su sfondo
4. Se `--accent` su sfondo chiaro ha contrast < 4.5:1 → usare SOLO con testo scuro

---

### 1.2 TIPOGRAFIA

```css
/* Font stack — self-hosted, GDPR compliant */
/* Heading: serif elegante */
font-family: 'Cormorant Garamond', 'Georgia', serif;

/* Body: sans-serif leggibile */
font-family: 'Montserrat', 'Helvetica Neue', sans-serif;
```

| Elemento | Font | Size | Weight | Line-height |
|----------|------|------|--------|-------------|
| H1 (hero) | Cormorant Garamond | clamp(2.5rem, 6vw, 5rem) | 700 | 1.05 |
| H2 (sezione) | Cormorant Garamond | clamp(2rem, 3.5vw, 3rem) | 700 | 1.15 |
| H3 (card/sub) | Cormorant Garamond | 1.35rem | 600 | 1.3 |
| Body | Montserrat | 0.9rem – 1.05rem | 400 | 1.85 |
| Label/Tag | Montserrat | 0.62rem – 0.78rem | 600–800 | 1.4 |
| CTA button | Montserrat | 0.78rem – 0.85rem | 800 | 1.2 |

**Regole tipografiche:**
- Label/tag: SEMPRE `text-transform: uppercase; letter-spacing: 1.5px–3.5px`
- H1 accent: `<strong>` con `font-weight: 600; font-style: italic`
- Body text: colore `--grigio` per descrizioni, `--testo` per contenuto principale
- Hero text su sfondo scuro: `text-shadow: 0 2px 24px rgba(8,16,30,0.55)`

---

### 1.3 SPACING SYSTEM

| Contesto | Desktop | Tablet | Mobile |
|----------|---------|--------|--------|
| Sezione padding | 90px 44px | 60px 28px | 60px 20px |
| Card padding | 28px 24px | 24px 20px | 20px 16px |
| Grid gap | 24px | 24px | 16px |
| Eyebrow → Heading | 12px–22px | — | — |
| Heading → Content | 22px–32px | — | — |
| Content → CTA | 40px | — | — |
| Form field gap | 16px | — | — |

---

### 1.4 BREAKPOINT RESPONSIVE

| Breakpoint | Target | Azione |
|------------|--------|--------|
| `max-width: 1024px` | Laptop | Grid 3→2 colonne |
| `max-width: 900px` | Tablet landscape | Footer/form collapse |
| **`max-width: 768px`** | **Tablet portrait** | **Navbar → hamburger, grid → 1 col** |
| `max-width: 600px` | Mobile grande | Card grid → 1 col, padding ridotto |
| `max-width: 520px` | Mobile piccolo | Popup/modal compatti |

---

### 1.5 SHADOW SYSTEM

```css
/* Livelli di elevazione */
--shadow-xs:  0 2px 16px rgba(21,36,53,0.05);    /* Card base */
--shadow-sm:  0 6px 20px rgba(21,36,53,0.08);     /* Card hover lieve */
--shadow-md:  0 20px 50px rgba(21,36,53,0.14);    /* Card hover forte */
--shadow-lg:  0 30px 100px rgba(0,0,0,0.4);       /* Hero/overlay */
--shadow-cta: 0 6px 20px rgba(184,212,74,0.35);   /* CTA button glow */
```

---

### 1.6 ANIMAZIONI

```css
/* Easing curves standard */
--ease-out:    cubic-bezier(0.16, 1, 0.3, 1);     /* Scroll reveal */
--ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1); /* Card lift */
--ease-smooth: cubic-bezier(0.22, 1, 0.36, 1);    /* Menu slide */

/* Scroll Reveal */
.sr        { opacity:0; transform: translateY(28px);  transition: all 0.7s var(--ease-out); }
.sr-left   { opacity:0; transform: translateX(-32px); transition: all 0.7s var(--ease-out); }
.sr-right  { opacity:0; transform: translateX(32px);  transition: all 0.7s var(--ease-out); }
.sr-scale  { opacity:0; transform: scale(0.88);       transition: all 0.7s var(--ease-out); }
.sr.visible, .sr-left.visible, .sr-right.visible, .sr-scale.visible {
  opacity: 1; transform: none;
}

/* Stagger delays */
.sr-d1 { transition-delay: 0.08s; }
.sr-d2 { transition-delay: 0.16s; }
.sr-d3 { transition-delay: 0.24s; }
.sr-d4 { transition-delay: 0.32s; }
.sr-d5 { transition-delay: 0.40s; }
.sr-d6 { transition-delay: 0.48s; }

/* Auto-stagger: .sr-stagger > figli ricevono sr-d1, sr-d2, ecc. via JS */

/* Hero background zoom */
@keyframes slowZoom {
  from { transform: scale(1.05); }
  to   { transform: scale(1.10); }
}

/* Fade up ingresso */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(36px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Card lift hover */
.card-lift {
  transition: transform 0.3s var(--ease-bounce), box-shadow 0.3s ease;
}
.card-lift:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-md);
}

/* Link underline reveal */
.link-reveal { position: relative; }
.link-reveal::after {
  content: ''; position: absolute; bottom: -2px; left: 0;
  width: 0; height: 2px; background: var(--accent);
  transition: width 0.35s var(--ease-out);
}
.link-reveal:hover::after { width: 100%; }

/* Accessibilità: rispetta preferenze utente */
@media (prefers-reduced-motion: reduce) {
  .sr, .sr-left, .sr-right, .sr-scale {
    opacity: 1; transform: none; transition: none;
  }
}
```

---

## PARTE 2 — STRUTTURA HTML UNIVERSALE

### 2.1 TEMPLATE BASE PAGINA

Ogni pagina generata DEVE seguire questa struttura esatta:

```html
<!DOCTYPE html>
<html lang="it">
<head>
  <!-- ===== META FONDAMENTALI ===== -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="[--primario]">

  <!-- ===== DNS PREFETCH / PRECONNECT ===== -->
  <link rel="dns-prefetch" href="https://www.googletagmanager.com">
  <!-- Aggiungere preconnect per CDN/API usati -->

  <!-- ===== FONT PRELOAD ===== -->
  <link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/montserrat-700.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/cormorant-garamond-700.woff2" as="font" type="font/woff2" crossorigin>

  <!-- ===== HERO IMAGE PRELOAD (se presente) ===== -->
  <link rel="preload" href="img/hero-[pagina].webp" as="image" fetchpriority="high">

  <!-- ===== SEO ===== -->
  <title>[Titolo unico max 60-70 char]</title>
  <meta name="description" content="[Descrizione unica max 155-160 char]">
  <link rel="canonical" href="https://[dominio]/[pagina].html">
  <meta name="robots" content="index, follow, max-image-preview:large">

  <!-- ===== OPEN GRAPH ===== -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="[Titolo]">
  <meta property="og:description" content="[Descrizione]">
  <meta property="og:url" content="https://[dominio]/[pagina].html">
  <meta property="og:image" content="https://[dominio]/img/og/[pagina].webp">
  <meta name="twitter:card" content="summary_large_image">

  <!-- ===== CRITICAL CSS INLINE ===== -->
  <style>
    /* Reset */
    *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
    html { scroll-behavior: smooth; }

    /* Font-face (solo pesi critici) */
    @font-face { font-family:'Montserrat'; src:url('fonts/montserrat-400.woff2') format('woff2'); font-weight:400; font-display:swap; }
    @font-face { font-family:'Montserrat'; src:url('fonts/montserrat-700.woff2') format('woff2'); font-weight:700; font-display:swap; }
    @font-face { font-family:'Cormorant Garamond'; src:url('fonts/cormorant-garamond-700.woff2') format('woff2'); font-weight:700; font-display:swap; }

    /* CSS Variables */
    :root {
      --primario: [COLORE]; --primario-2: [COLORE]; --primario-3: [COLORE];
      --accent: [COLORE]; --accent-2: [COLORE];
      --nero: #152435; --bianco: #F7F5F1; --sfondo: #ECE7DF;
      --testo: #152435; --grigio: #6B7A8D;
      --nav-h: 74px; --max-w: 1200px; --radius: 12px; --radius-sm: 8px;
    }
    @media(max-width:768px) { :root { --nav-h: 64px; } }

    /* Body base */
    body { font-family:'Montserrat',sans-serif; color:var(--testo); background:var(--bianco); line-height:1.85; }
    a { text-decoration:none; color:inherit; }
    img { max-width:100%; height:auto; display:block; }

    /* Navbar (critical — evita FOUC) */
    #navbar { position:fixed; top:0; left:0; right:0; z-index:1000; height:var(--nav-h); display:flex; align-items:center; justify-content:space-between; padding:0 44px; transition:all 0.4s; background:transparent; }
    #navbar.scrolled { background:rgba(253,250,243,0.97); box-shadow:0 2px 32px rgba(21,36,53,0.1); backdrop-filter:blur(16px); }

    /* Skip link (accessibility) */
    .skip-link { position:absolute; top:-100%; left:50%; transform:translateX(-50%); background:var(--accent); color:var(--nero); padding:0.6rem 1.2rem; border-radius:0 0 8px 8px; font-size:0.82rem; z-index:9999; transition:top 0.2s; }
    .skip-link:focus { top:0; }

    /* Hero above-the-fold */
    .hero { position:relative; min-height:70vh; display:flex; align-items:center; overflow:hidden; padding:calc(var(--nav-h) + 60px) 44px 80px; }
  </style>

  <!-- ===== CSS NON-CRITICAL (deferred) ===== -->
  <link rel="stylesheet" href="css/fonts.css" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="css/main.css" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="css/nav-mobile.css" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="css/scroll-reveal.css" media="print" onload="this.media='all'">

  <!-- ===== ANALYTICS (se configurato) ===== -->
  <!-- <script async src="https://www.googletagmanager.com/gtag/js?id=[GA_ID]"></script> -->

  <!-- ===== SCHEMA.ORG JSON-LD ===== -->
  <script type="application/ld+json">
  [
    {
      "@context": "https://schema.org",
      "@type": "[TipoAttivita]",
      "name": "[Nome Attività]",
      "url": "https://[dominio]",
      "logo": "https://[dominio]/img/logo.webp",
      "telephone": "[telefono]",
      "email": "[email]",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "[indirizzo]",
        "addressLocality": "[città]",
        "postalCode": "[CAP]",
        "addressCountry": "IT"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "[lat]",
        "longitude": "[lng]"
      },
      "sameAs": ["[facebook]", "[instagram]", "[linkedin]"]
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type":"ListItem","position":1,"name":"Home","item":"https://[dominio]/"},
        {"@type":"ListItem","position":2,"name":"[Pagina]","item":"https://[dominio]/[pagina].html"}
      ]
    }
  ]
  </script>
</head>

<body>
  <!-- ===== SKIP LINK ===== -->
  <a href="#main-content" class="skip-link">Vai al contenuto principale</a>

  <!-- ===== NAVBAR ===== -->
  <header id="navbar">
    <a href="/" class="nav-logo">
      <span class="logo-text">[Brand]</span>
      <span class="logo-accent">[Sottotitolo]</span>
    </a>

    <nav class="nav-links">
      <a href="/">Home</a>
      <a href="/servizi.html">Servizi</a>
      <a href="/chi-siamo.html">Chi Siamo</a>
      <a href="/blog.html">Blog</a>
      <a href="/contatti.html">Contatti</a>
    </nav>

    <div class="nav-cta">
      <a href="tel:[telefono]" class="nav-tel">[telefono]</a>
      <a href="/contatti.html" class="btn-accent">Contattaci</a>
    </div>

    <button class="nav-burger" id="burgerBtn" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </header>

  <!-- ===== NAV MOBILE ===== -->
  <div class="nav-mobile" id="navMobile">
    <a href="/">Home</a>
    <a href="/servizi.html">Servizi</a>
    <a href="/chi-siamo.html">Chi Siamo</a>
    <a href="/blog.html">Blog</a>
    <a href="/contatti.html">Contatti</a>
    <a href="/contatti.html" class="btn-accent-mobile">Contattaci</a>
  </div>

  <!-- ===== BREADCRUMB (su tutte tranne homepage) ===== -->
  <div class="bc">
    <div class="bc-inner">
      <a href="/">Home</a>
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
      <span>[Pagina corrente]</span>
    </div>
  </div>

  <!-- ===== MAIN CONTENT ===== -->
  <main id="main-content">

    <!-- HERO SECTION -->
    <section class="hero">
      <div class="hero-bg">
        <img src="img/hero-[pagina].webp" alt="[descrizione]" width="1400" height="600" loading="eager">
        <div class="hero-veil"></div>
      </div>
      <div class="hero-inner">
        <div class="sec-tag">[ETICHETTA]</div>
        <h1>[Titolo] <strong>[Accent]</strong></h1>
        <p>[Descrizione 2-3 righe]</p>
        <div class="hero-btns">
          <a href="#contatti" class="btn-accent">CTA Primario</a>
          <a href="#servizi" class="btn-outline">CTA Secondario</a>
        </div>
      </div>
    </section>

    <!-- SEZIONI CONTENUTO (ripetere pattern) -->
    <section class="sec sr">
      <div class="sec-inner">
        <div class="sec-tag">[ETICHETTA]</div>
        <h2 class="sec-t">[Titolo] <strong>[Accent]</strong></h2>
        <p class="sec-sub">[Sottotitolo]</p>
        <!-- Grid cards / contenuto / tabelle / FAQ -->
      </div>
    </section>

    <!-- SEZIONE CON SFONDO ALTERNATO -->
    <section class="sec sec-alt sr">
      <div class="sec-inner">
        <!-- contenuto -->
      </div>
    </section>

  </main>

  <!-- ===== FOOTER ===== -->
  <footer>
    <div class="footer-inner">
      <div class="footer-grid">
        <div class="footer-brand">
          <div class="f-logo">[Brand] <span>[Accent]</span></div>
          <p class="f-desc">[Descrizione breve attività]</p>
          <div class="f-social">
            <a href="[facebook]" class="f-soc" aria-label="Facebook">FB</a>
            <a href="[instagram]" class="f-soc" aria-label="Instagram">IG</a>
            <a href="[linkedin]" class="f-soc" aria-label="LinkedIn">LI</a>
          </div>
        </div>
        <div class="footer-col">
          <div class="f-title">Servizi</div>
          <a href="#">Servizio 1</a>
          <a href="#">Servizio 2</a>
        </div>
        <div class="footer-col">
          <div class="f-title">Risorse</div>
          <a href="/blog.html">Blog</a>
          <a href="/faq.html">FAQ</a>
        </div>
        <div class="footer-col">
          <div class="f-title">Contatti</div>
          <a href="tel:[telefono]">[telefono]</a>
          <a href="mailto:[email]">[email]</a>
          <p>[indirizzo]</p>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© [anno] [Brand]. Tutti i diritti riservati.</span>
        <a href="/privacy.html">Privacy Policy</a>
        <a href="/cookie-policy.html">Cookie Policy</a>
      </div>
    </div>
  </footer>

  <!-- ===== JS (deferred) ===== -->
  <script src="js/nav-mobile.js" defer></script>
  <script src="js/scroll-reveal.js" defer></script>
  <script src="js/cookie-consent.js" defer></script>
  <!-- Aggiungere script specifici per pagina -->
</body>
</html>
```

---

### 2.2 COMPONENTI RIUTILIZZABILI

#### A) CARD GRID

```html
<div class="card-grid">
  <div class="card card-lift sr sr-d1">
    <div class="card-icon">[emoji/svg]</div>
    <h3 class="card-title">[Titolo]</h3>
    <p class="card-desc">[Descrizione]</p>
    <a href="#" class="card-link link-reveal">Scopri di più →</a>
  </div>
  <!-- ripetere -->
</div>
```

```css
.card-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:24px; }
@media(max-width:900px) { .card-grid { grid-template-columns:repeat(2,1fr); } }
@media(max-width:600px) { .card-grid { grid-template-columns:1fr; } }

.card { background:var(--bianco); border:1px solid rgba(44,74,110,0.08); border-radius:var(--radius); padding:28px 24px; }
.card-icon { font-size:2rem; margin-bottom:16px; }
.card-title { font-family:'Cormorant Garamond',serif; font-size:1.35rem; font-weight:600; margin-bottom:8px; }
.card-desc { font-size:0.85rem; color:var(--grigio); line-height:1.75; margin-bottom:16px; }
.card-link { font-size:0.78rem; font-weight:600; color:var(--primario); text-transform:uppercase; letter-spacing:1px; }
```

#### B) CTA BUTTONS

```css
/* Primario — accent su sfondo scuro */
.btn-accent {
  display:inline-block; background:var(--accent); color:var(--nero);
  padding:15px 32px; border-radius:var(--radius-sm);
  font-family:'Montserrat',sans-serif; font-weight:800; font-size:0.78rem;
  letter-spacing:1px; text-transform:uppercase;
  transition:all 0.25s;
}
.btn-accent:hover { background:var(--accent-2); transform:translateY(-2px); box-shadow:var(--shadow-cta); }

/* Secondario — outline su sfondo scuro */
.btn-outline {
  display:inline-block; border:1px solid rgba(255,255,255,0.2); color:#fff;
  padding:15px 32px; border-radius:var(--radius-sm);
  font-family:'Montserrat',sans-serif; font-weight:600; font-size:0.78rem;
  letter-spacing:1px; text-transform:uppercase;
  transition:all 0.25s;
}
.btn-outline:hover { border-color:var(--accent); color:var(--accent); }

/* Terziario — scuro su sfondo chiaro */
.btn-dark {
  display:inline-block; background:var(--nero); color:#fff;
  padding:15px 32px; border-radius:var(--radius-sm);
  font-family:'Montserrat',sans-serif; font-weight:700; font-size:0.78rem;
  letter-spacing:1px; text-transform:uppercase;
  transition:all 0.25s;
}
.btn-dark:hover { background:var(--accent); color:var(--nero); transform:translateY(-2px); }
```

#### C) FORM CONTATTI

```html
<div class="form-box">
  <div class="form-head">
    <h3>[Titolo Form]</h3>
    <p>[Sottotitolo]</p>
  </div>
  <form class="form-body" action="https://formspree.io/f/[ID]" method="POST">
    <div class="form-grid">
      <div class="field">
        <label for="nome">Nome *</label>
        <input type="text" id="nome" name="nome" required>
      </div>
      <div class="field">
        <label for="email">Email *</label>
        <input type="email" id="email" name="email" required>
      </div>
    </div>
    <div class="field">
      <label for="telefono">Telefono</label>
      <input type="tel" id="telefono" name="telefono">
    </div>
    <div class="field">
      <label for="messaggio">Messaggio *</label>
      <textarea id="messaggio" name="messaggio" rows="4" required></textarea>
    </div>
    <button type="submit" class="btn-accent form-submit">Invia Messaggio</button>
  </form>
</div>
```

```css
.form-box { background:var(--bianco); border:1px solid rgba(44,74,110,0.08); border-radius:var(--radius); overflow:hidden; }
.form-head { padding:32px 32px 16px; }
.form-head h3 { font-family:'Cormorant Garamond',serif; font-size:1.6rem; font-weight:600; }
.form-body { padding:0 32px 32px; }
.form-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:16px; }
@media(max-width:600px) { .form-grid { grid-template-columns:1fr; } }

.field { margin-bottom:16px; }
.field label { display:block; font-size:0.62rem; font-weight:600; text-transform:uppercase; letter-spacing:1.5px; color:var(--grigio); margin-bottom:6px; }
.field input, .field textarea, .field select {
  width:100%; padding:12px 14px; border:1px solid rgba(44,74,110,0.12); border-radius:var(--radius-sm);
  font-family:'Montserrat',sans-serif; font-size:0.85rem; color:var(--testo); background:var(--carta);
  transition:border-color 0.2s;
}
.field input:focus, .field textarea:focus, .field select:focus {
  outline:none; border-color:var(--accent); box-shadow:0 0 0 3px rgba(44,74,110,0.1);
}
.form-submit { width:100%; cursor:pointer; border:none; }
```

#### D) FAQ / ACCORDION

```html
<div class="faq-list">
  <div class="faq-item sr">
    <button class="faq-btn" aria-expanded="false">
      <span class="faq-q">[Domanda]</span>
      <span class="faq-icon">+</span>
    </button>
    <div class="faq-answer">
      <p>[Risposta]</p>
    </div>
  </div>
  <!-- ripetere -->
</div>
```

```css
.faq-item { background:var(--bianco); border-radius:var(--radius); border:1px solid rgba(44,74,110,0.09); margin-bottom:12px; overflow:hidden; }
.faq-btn { width:100%; text-align:left; padding:20px 22px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; gap:14px; background:none; border:none; font-family:'Montserrat',sans-serif; font-size:0.92rem; font-weight:600; color:var(--testo); }
.faq-icon { width:28px; height:28px; border-radius:50%; background:var(--sfondo); border:1px solid rgba(44,74,110,0.12); display:flex; align-items:center; justify-content:center; transition:all 0.3s; flex-shrink:0; font-size:1.1rem; }
.faq-item.open .faq-icon { background:var(--accent); color:var(--nero); transform:rotate(45deg); }
.faq-answer { max-height:0; overflow:hidden; transition:max-height 0.4s ease, padding 0.3s ease; padding:0 22px; font-size:0.85rem; color:var(--grigio); line-height:1.75; }
.faq-item.open .faq-answer { max-height:500px; padding:0 22px 20px; }
```

```javascript
// FAQ toggle
document.querySelectorAll('.faq-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const wasOpen = item.classList.contains('open');
    // Chiudi tutti
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    // Toggle corrente
    if (!wasOpen) item.classList.add('open');
    btn.setAttribute('aria-expanded', !wasOpen);
  });
});
```

---

## PARTE 3 — JAVASCRIPT UNIVERSALE

### 3.1 MODULI JS OBBLIGATORI

| File | Funzione | Peso |
|------|----------|------|
| `js/nav-mobile.js` | Hamburger menu toggle | ~1KB |
| `js/scroll-reveal.js` | IntersectionObserver animations | ~1KB |
| `js/cookie-consent.js` | Banner GDPR + preferenze | ~3KB |

### 3.2 nav-mobile.js (Template)

```javascript
(function() {
  'use strict';
  const btn = document.getElementById('burgerBtn');
  const panel = document.getElementById('navMobile');
  if (!btn || !panel) return;

  function toggle() {
    const isOpen = panel.classList.toggle('open');
    btn.classList.toggle('open');
    btn.setAttribute('aria-expanded', isOpen);
    document.body.style.overflow = isOpen ? 'hidden' : '';
  }

  function close() {
    panel.classList.remove('open');
    btn.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  btn.addEventListener('click', toggle);
  panel.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
})();
```

### 3.3 scroll-reveal.js (Template)

```javascript
(function() {
  'use strict';
  if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.sr,.sr-left,.sr-right,.sr-scale').forEach(el => {
      el.style.opacity = '1'; el.style.transform = 'none';
    });
    return;
  }

  // Auto-stagger
  document.querySelectorAll('.sr-stagger').forEach(parent => {
    [...parent.children].forEach((child, i) => {
      if (i < 6) child.classList.add('sr-d' + (i + 1));
    });
  });

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.sr,.sr-left,.sr-right,.sr-scale').forEach(el => observer.observe(el));
})();
```

### 3.4 Navbar scroll effect

```javascript
// Aggiungere in nav-mobile.js o script dedicato
const navbar = document.getElementById('navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
  });
}
```

---

## PARTE 4 — REGOLE SEO / GEO / E-E-A-T

### 4.1 SEO ON-PAGE (Obbligatorio per ogni pagina)

| Elemento | Regola | Validazione |
|----------|--------|-------------|
| `<title>` | Unico, max 60-70 char, keyword + brand | ERRORE se mancante |
| `<meta description>` | Unico, max 155-160 char, CTA implicito | ERRORE se mancante |
| `<h1>` | Uno solo per pagina, keyword principale | ERRORE se mancante/multiplo |
| `<link rel="canonical">` | URL assoluto | WARNING se mancante |
| Open Graph | og:title, og:description, og:image, og:url | WARNING se mancante |
| `<meta robots>` | index, follow, max-image-preview:large | WARNING se mancante |
| Alt text | Su TUTTE le immagini | WARNING se mancante |
| Schema.org | Almeno 1 schema JSON-LD per pagina | ERRORE se mancante |

### 4.2 GEO — Generative Engine Optimization

**Formato contenuti per AI:**
- Frasi dichiarative nelle prime 2 righe di ogni sezione
- Dati numerici specifici e verificabili
- Pattern: `H2 domanda → Risposta diretta (40-60 parole) → Approfondimento`
- Liste, tabelle, definizioni chiare
- Citare fonti ufficiali quando possibile
- Frasi auto-contenute — ogni claim deve avere senso letto isolatamente

### 4.3 E-E-A-T (Esperienza, Competenza, Autorevolezza, Affidabilità)

- Author bio visibile su articoli blog
- Nome autore, ruolo, foto, descrizione
- Meta `article:author` su articoli
- Coerenza brand cross-platform (social links)

### 4.4 PERFORMANCE

| Regola | Dettaglio |
|--------|-----------|
| Hero image preloaded | `<link rel="preload" ... fetchpriority="high">` |
| Font preloaded | Montserrat 400/700, Cormorant Garamond 700 |
| MAI `loading="lazy"` above-the-fold | Solo per immagini below-the-fold |
| Tutte le immagini con `width` + `height` | Evita CLS |
| WebP obbligatorio | Per tutte le immagini locali |
| CTA above-the-fold | Con contrast ratio >= 4.5:1 |
| Critical CSS inline | Nel `<head>` |
| CSS non-critical deferred | `media="print" onload="this.media='all'"` |

### 4.5 ACCESSIBILITÀ

| Regola | Dettaglio |
|--------|-----------|
| Skip link | Primo elemento nel `<body>` |
| Landmark HTML5 | `<header>`, `<nav>`, `<main>`, `<footer>` |
| aria-label | Su tutti i bottoni icon-only |
| aria-hidden | Su SVG decorativi |
| Focus visible | Border/shadow su tutti gli interattivi |
| prefers-reduced-motion | Disabilita animazioni se richiesto |
| Contrast ratio | >= 4.5:1 testo normale, >= 3:1 testo grande |

---

## PARTE 5 — I 4 LOOP DI VALIDAZIONE

> Ogni volta che Claude genera o modifica una pagina, DEVE eseguire questi 4 loop **in sequenza**.
> Ogni loop ricontrolla **tutta la struttura del sito** e **tutte le regole** da capo.

---

### LOOP 1 — STRUTTURA & HTML

**Obiettivo:** Verificare che la struttura HTML sia completa e corretta.

Claude ricontrolla OGNI pagina del sito per:

| # | Check | Tipo | Azione se fallisce |
|---|-------|------|-------------------|
| 1 | DOCTYPE html presente | Struttura | Aggiungere |
| 2 | `<html lang="it">` | Struttura | Correggere |
| 3 | `<meta charset="UTF-8">` | Struttura | Aggiungere |
| 4 | `<meta viewport>` responsive | Struttura | Aggiungere |
| 5 | `<meta theme-color>` presente | Struttura | Aggiungere |
| 6 | Font preload nel `<head>` | Performance | Aggiungere |
| 7 | Hero image preload (se hero presente) | Performance | Aggiungere |
| 8 | Critical CSS inline nel `<head>` | Performance | Aggiungere |
| 9 | CSS non-critical con deferred loading | Performance | Convertire a deferred |
| 10 | Skip link primo elemento del body | Accessibilità | Aggiungere |
| 11 | `<header>` con navbar presente | Struttura | Aggiungere |
| 12 | Nav-mobile con hamburger menu | Struttura | Aggiungere |
| 13 | Breadcrumb presente (se non homepage) | SEO | Aggiungere |
| 14 | `<main id="main-content">` presente | Accessibilità | Aggiungere |
| 15 | Hero section come prima sezione | Struttura | Riordinare |
| 16 | Sezioni con classe `.sec` + `.sec-inner` | Struttura | Correggere |
| 17 | Footer completo (brand, link, legal) | Struttura | Aggiungere |
| 18 | JS deferred in fondo al body | Performance | Spostare/aggiungere defer |
| 19 | Tutte le immagini con `width` + `height` | Performance | Aggiungere |
| 20 | Tutte le immagini con `alt` text | Accessibilità | Aggiungere |
| 21 | Hero image con `loading="eager"` | Performance | Correggere |
| 22 | Immagini below-fold con `loading="lazy"` | Performance | Aggiungere |
| 23 | Formato WebP per immagini locali | Performance | Segnalare |
| 24 | `aria-label` su bottoni icon-only | Accessibilità | Aggiungere |
| 25 | `aria-hidden="true"` su SVG decorativi | Accessibilità | Aggiungere |

**Al termine del Loop 1:** Claude elenca i fix applicati e passa al Loop 2.

---

### LOOP 2 — SEO & SCHEMA

**Obiettivo:** Verificare che SEO, meta tag e Schema.org siano completi e corretti.

Claude ricontrolla OGNI pagina del sito per:

| # | Check | Tipo | Azione se fallisce |
|---|-------|------|-------------------|
| 1 | `<title>` presente e unico | SEO | Aggiungere/correggere |
| 2 | `<title>` max 70 caratteri | SEO | Accorciare |
| 3 | `<meta description>` presente | SEO | Aggiungere |
| 4 | `<meta description>` max 160 char | SEO | Accorciare |
| 5 | Un solo `<h1>` per pagina | SEO | Correggere gerarchia |
| 6 | `<link rel="canonical">` con URL assoluto | SEO | Aggiungere |
| 7 | `<meta robots>` presente | SEO | Aggiungere |
| 8 | `og:title` presente | Social | Aggiungere |
| 9 | `og:description` presente | Social | Aggiungere |
| 10 | `og:image` presente (1200x630) | Social | Aggiungere |
| 11 | `og:url` presente | Social | Aggiungere |
| 12 | `twitter:card` presente | Social | Aggiungere |
| 13 | Schema JSON-LD attività (tipo corretto) | Schema | Aggiungere |
| 14 | Schema con `sameAs` (social links) | Schema | Aggiungere |
| 15 | Schema `BreadcrumbList` (se non homepage) | Schema | Aggiungere |
| 16 | Schema `FAQPage` (se FAQ presenti) | Schema | Aggiungere |
| 17 | Schema `Article` (se blog post) | Schema | Aggiungere |
| 18 | Pagina registrata in `sitemap.xml` | SEO | Aggiungere |
| 19 | URL sitemap con `lastmod` aggiornato | SEO | Aggiornare data |
| 20 | Internal linking coerente | SEO | Segnalare link mancanti |
| 21 | GEO: frasi dichiarative in apertura sezione | GEO | Riscrivere |
| 22 | GEO: dati numerici specifici presenti | GEO | Aggiungere |
| 23 | GEO: formato H2 domanda → risposta diretta | GEO | Ristrutturare |
| 24 | E-E-A-T: author bio su blog post | E-E-A-T | Aggiungere |
| 25 | Contrast ratio CTA >= 4.5:1 | Accessibilità | Correggere colori |

**Al termine del Loop 2:** Claude elenca i fix applicati e passa al Loop 3.

---

### LOOP 3 — COERENZA GLOBALE & REGISTRI

**Obiettivo:** Verificare che il sito sia coerente nel suo insieme e tutti i registri siano allineati.

Claude ricontrolla L'INTERO PROGETTO per:

| # | Check | Tipo | Azione se fallisce |
|---|-------|------|-------------------|
| 1 | TUTTE le pagine in `sitemap.xml` | Registro | Aggiungere mancanti |
| 2 | `sitemap.xml` senza pagine inesistenti | Registro | Rimuovere |
| 3 | `robots.txt` referenzia sitemap corretto | Registro | Correggere |
| 4 | Navigazione (header) include tutte le pagine | Coerenza | Aggiornare nav |
| 5 | Footer link coerenti con nav | Coerenza | Allineare |
| 6 | Blog listing include tutti gli articoli | Registro | Aggiungere |
| 7 | CSS variabili coerenti tra pagine | Design | Allineare |
| 8 | Font stack identico su tutte le pagine | Design | Correggere |
| 9 | Breakpoint responsive coerenti | Design | Allineare |
| 10 | Stile CTA buttons uniforme | Design | Correggere |
| 11 | Naming convention classi CSS uniforme | Design | Rinominare |
| 12 | Spacing/padding coerente tra sezioni | Design | Allineare |
| 13 | Schema.org `name`, `url`, `telephone` identici | Schema | Allineare |
| 14 | Open Graph image presente per ogni pagina | Social | Creare/aggiungere |
| 15 | Nessun link rotto (href a pagine esistenti) | Coerenza | Correggere |
| 16 | GA4 tracking code presente su tutte le pagine | Analytics | Aggiungere |
| 17 | Cookie consent su tutte le pagine | GDPR | Aggiungere script |
| 18 | `CLAUDE.md` aggiornato con nuove pagine | Documentazione | Aggiornare |

**Al termine del Loop 3:** Claude elenca i fix applicati e passa al Loop 4.

---

### LOOP 4 — PERFORMANCE & MOBILE

**Obiettivo:** Verificare che il sito sia veloce, mobile-first e pronto per Lighthouse 90+.

Claude ricontrolla OGNI pagina e L'INTERO PROGETTO per:

| # | Check | Tipo | Azione se fallisce |
|---|-------|------|-------------------|
| 1 | Critical CSS inline copre above-the-fold | Performance | Espandere critical CSS |
| 2 | CSS non-critical caricato con deferred | Performance | Convertire a `media="print"` |
| 3 | Font preload presenti per tutti i font critici | Performance | Aggiungere `<link rel="preload">` |
| 4 | `font-display: swap` su tutti i @font-face | Performance | Aggiungere |
| 5 | Hero image con `fetchpriority="high"` | Performance | Aggiungere attributo |
| 6 | Nessun `loading="lazy"` su immagini above-the-fold | Performance | Rimuovere |
| 7 | Tutte le immagini below-fold con `loading="lazy"` | Performance | Aggiungere |
| 8 | Immagini con `width` + `height` espliciti (no CLS) | Performance | Aggiungere dimensioni |
| 9 | Nessun CSS/JS render-blocking non necessario | Performance | Aggiungere defer/async |
| 10 | JS con attributo `defer` (non blocca parsing) | Performance | Aggiungere `defer` |
| 11 | Navbar responsive: hamburger < 768px | Mobile | Verificare breakpoint |
| 12 | Grid collassa correttamente a 1 colonna | Mobile | Testare media queries |
| 13 | Touch target >= 44x44px su bottoni mobile | Mobile | Aumentare padding |
| 14 | Font-size minimo 16px su input (no zoom iOS) | Mobile | Correggere font-size |
| 15 | CTA sticky mobile presente (se landing page) | Mobile | Aggiungere |
| 16 | `<meta viewport>` con `width=device-width` | Mobile | Correggere |
| 17 | Nessun overflow orizzontale su mobile | Mobile | Fix CSS (max-width/overflow) |
| 18 | Padding ridotto su mobile (3rem 1rem) | Mobile | Aggiungere media query |
| 19 | Immagini in formato WebP | Performance | Convertire/segnalare |
| 20 | `dns-prefetch` per domini esterni usati | Performance | Aggiungere |
| 21 | `preconnect` per CDN/API critici | Performance | Aggiungere |
| 22 | Nessun CSS inutilizzato (> 50% unused) | Performance | Rimuovere o spostare |
| 23 | Animazioni con `will-change` dove necessario | Performance | Aggiungere |
| 24 | `prefers-reduced-motion` rispettata | Accessibilità | Aggiungere media query |
| 25 | Scrollbar custom presente e coerente | Design | Aggiungere CSS |

**Al termine del Loop 4:** Claude produce un **REPORT FINALE** con:
- Totale check eseguiti (93 per pagina × N pagine + 18 globali)
- Fix applicati automaticamente
- Warning che richiedono decisione dell'utente
- Stato: PASS / FAIL per ogni loop
- Score stimato Lighthouse (Performance, Accessibility, SEO, Best Practices)

---

## PARTE 6 — COMANDO UNICO DI GENERAZIONE

### Come usare questa skill

L'utente dice a Claude:

```
Genera un nuovo sito con AUTOMATION-SITE-2026:

Cosa:     Sito per studio dentistico "Sorriso Perfetto" a Bologna
Tempo:    Consegna in 1 settimana
Scopo:    Generare prenotazioni pazienti online
Pagine:   Home, Servizi, Chi Siamo, Contatti, Blog, Prenota
Colore:   #1A7AB5 (azzurro medicale)
Dominio:  sorrisoperfetto.it
Telefono: 051-1234567
Email:    info@sorrisoperfetto.it
Social:   facebook.com/sorrisoperfetto, instagram.com/sorrisoperfetto
```

### Claude esegue automaticamente:

1. **GENERA** tutte le pagine HTML dal template (Parte 2)
2. **PERSONALIZZA** colori, testi, schema.org (Parte 1 + 4)
3. **CREA** CSS, JS, sitemap.xml, robots.txt (Parte 1 + 3)
4. **ESEGUE LOOP 1** — Struttura & HTML (25 check per pagina)
5. **ESEGUE LOOP 2** — SEO & Schema (25 check per pagina)
6. **ESEGUE LOOP 3** — Coerenza globale (18 check sull'intero sito)
7. **ESEGUE LOOP 4** — Performance & Mobile (25 check per pagina)
8. **PRODUCE REPORT** con stato di ogni check + score Lighthouse stimato
9. **GENERA `CLAUDE.md`** con skill auto-attivata per il nuovo progetto

### CLAUDE.md generato per il nuovo progetto:

```markdown
# CLAUDE.md — [Nome Progetto]

## REGOLE
1. Lingua: Italiano
2. Mobile-first
3. No librerie extra — vanilla HTML/CSS/JS
4. Leggi prima il file da modificare
5. Commit chiari in italiano

## SKILL ATTIVA
Questo progetto usa AUTOMATION-SITE-2026.
Ogni nuova pagina o modifica attiva i 4 LOOP di validazione automatica.
Consultare: TEST-SKILL/AUTOMATION-SITE-2026.md

## REGISTRAZIONE NUOVE PAGINE
Ogni nuova pagina deve essere aggiunta a:
1. sitemap.xml
2. Navigazione (header + footer)
3. Schema.org JSON-LD
```

---

## PARTE 7 — CHECKLIST RAPIDA (CHEAT SHEET)

### Per ogni NUOVA PAGINA:
```
□ Template HTML base completo (Parte 2.1)
□ CSS variables nel :root (Parte 1.1)
□ Title + Meta description + Canonical
□ Open Graph tags (og:title, og:description, og:image)
□ Schema.org JSON-LD (attività + breadcrumb)
□ Hero image preloaded + width/height
□ Critical CSS inline nel <head>
□ Skip link + aria labels
□ Registrata in sitemap.xml
□ Link in navigazione (header/footer)
□ LOOP 1 → LOOP 2 → LOOP 3 → LOOP 4 superati
```

### Per ogni MODIFICA:
```
□ Leggere il file prima di modificare
□ Verificare impatto su altre pagine
□ Eseguire i 4 LOOP su pagine impattate
□ Aggiornare sitemap.xml lastmod
□ Commit descrittivo in italiano
```

---

> **AUTOMATION-SITE-2026** — Versione 1.0
> Creata: 2026-03-08
> Basata su: Design System Righetto Immobiliare
> Compatibile con: qualsiasi tipo di sito web
