# CLAUDE.md — Righetto Immobiliare

> Questo file viene letto automaticamente da Claude ad ogni sessione.
> Contiene tutte le regole operative del progetto. La skill completa e' in `TEST-SKILL/SKILL-UNIFICATA.md`.

---

## REGOLE FONDAMENTALI

1. **Lingua:** Rispondi sempre in italiano
2. **Mobile-first** — ogni modifica deve funzionare su mobile
3. **No librerie extra** — il sito e' vanilla HTML/CSS/JS, volutamente leggero
4. **Leggi prima** il file da modificare — mai modificare al buio
5. **Commit** chiari e descrittivi in italiano
6. **Mai toccare** DNS, record MX, configurazione cPanel senza conferma esplicita

---

## TECH STACK

| Campo | Valore |
|---|---|
| **Dominio** | righettoimmobiliare.it |
| **Hosting sito** | GitHub Pages (deploy da `main`) |
| **Tech Stack** | HTML statico + CSS + JS vanilla + Express.js (dev) |
| **Database** | Supabase (PostgreSQL) |
| **Newsletter** | Brevo |
| **Form contatti** | Formspree |
| **Analytics** | Google Analytics 4 (G-9MHDHHES26) |
| **Chatbot AI** | "Sara" — assistente virtuale |

---

## CHECKLIST OBBLIGATORIA — OGNI NUOVA PAGINA HTML

### SEO On-Page
- Title tag unico (max 60-70 char)
- Meta description (max 155-160 char)
- H1 unico per pagina
- Canonical URL (`rel="canonical"`)
- Open Graph tags (`og:title`, `og:description`, `og:image`)
- Meta robots (`name="robots"`)
- Alt text su tutte le immagini

### Schema.org (JSON-LD)
- `RealEstateAgent` con `GeoCoordinates` e `sameAs` (Facebook, Instagram, LinkedIn)
- `BreadcrumbList` su tutte le pagine (tranne index.html)
- `FAQPage` su pagine servizio e zona
- Layering: piu' schema nella stessa pagina = piu' segnali a Google

### Performance / Visual Saliency
- Hero image preloaded nel `<head>`: `<link rel="preload" href="..." as="image" fetchpriority="high">`
- Font preloaded: Montserrat (400/700) + Cormorant Garamond (600/700)
- MAI `loading="lazy"` su immagini above-the-fold
- TUTTE le immagini con `width` + `height` espliciti
- WebP obbligatorio per immagini locali
- CTA primario above-the-fold con contrast ratio >= 4.5:1
- Critical CSS inline nel `<head>`

### GEO — Generative Engine Optimization
- Frasi dichiarative nelle prime 2 righe di ogni sezione
- Dati numerici specifici e verificabili
- Formato: H2 domanda -> Risposta diretta (40-60 parole) -> Approfondimento
- Liste, tabelle, definizioni chiare
- Citare fonti ufficiali (Agenzia Entrate, OMI, FIAIP)
- Frasi auto-contenute — ogni claim deve avere senso letto isolatamente

### E-E-A-T
- Author bio visibile su ogni articolo blog
- Nome autore, ruolo, foto, descrizione
- Meta `article:author` su articoli blog
- Coerenza brand cross-platform

---

## REGISTRAZIONE NUOVI ARTICOLI BLOG

Ogni nuovo file `blog-*.html` DEVE essere registrato in TUTTI questi punti:

1. **`sitemap.xml`** — aggiungere URL con lastmod e priority 0.8
2. **`blog.html`** — aggiungere nell'array `articoliStatici`
3. **`js/homepage.js`** — aggiungere in `staticMap` e `articoliStatici`
4. **`admin.html`** — aggiungere nell'array `_blogSeedArticles`

Se anche solo uno manca, il validatore automatico segnalera' errore.

---

## REGISTRAZIONE NUOVE PAGINE

Ogni nuova pagina HTML deve essere aggiunta a:
1. **`sitemap.xml`** — con URL completo, lastmod, changefreq, priority
2. **Navigazione** — link nel menu o nella pagina hub pertinente

---

## VALIDAZIONE AUTOMATICA

Il progetto include un validatore automatico:
- **Script:** `scripts/validate-page.js`
- **Hook:** `.git/hooks/pre-commit` — si attiva ad ogni commit con file HTML
- **Blocca il commit** se ci sono errori critici (schema mancante, title mancante, ecc.)
- **Lascia passare con warning** (meta description troppo lunga, ecc.)

Per testare manualmente:
```bash
node scripts/validate-page.js --all          # tutte le pagine
node scripts/validate-page.js --staged       # solo file staged
node scripts/validate-page.js pagina.html    # pagina specifica
```

---

## PALETTE COLORI

| Variabile | Colore | Uso |
|---|---|---|
| `--blu` | #2C4A6E | Primario, CTA secondario |
| `--oro` | #B8D44A | CTA primario (SOLO con testo scuro) |
| `--nero` | #0A0F1C | Testo principale |
| `--bianco` | #F7F5F1 | Sfondo |
| `--fire` | arancione | CTA landing |
| `--purple` | #6C63FF | CTA valutazione |
| `--mint` | #00E5A0 | CTA landing-agente |

> **ATTENZIONE:** `var(--oro)` su sfondo chiaro ha contrast ratio 1.54:1 = FAIL WCAG. Usare SOLO con testo scuro.

---

## STRUTTURA CONTENUTI

### Topic Cluster Attivi
- **Vendere Casa Padova** — servizio-vendita, blog-costi, blog-documenti, blog-tasse, landing-vendere-casa-padova
- **Comprare Casa Padova** — blog-comprare-casa, blog-mutuo, blog-agevolazioni, blog-successione, blog-investire
- **Quartieri Padova** — 9 pagine zona-*, agenzia-immobiliare-padova (pillar)
- **Affitto Padova** — blog-affitto-studenti, servizio-locazioni, blog-contratto-affitto, blog-rendimento-affitto

### Internal Linking
- Ogni articolo blog deve linkare alle zone pages e service pages correlate
- Cross-link tra articoli dello stesso cluster

---

## STILE CONTENUTI

- Tono: autorevole ma accessibile
- Dati concreti: prezzi/mq, percentuali, statistiche verificabili
- Target: famiglie e investitori zona Padova/hinterland
- Keyword locali: sempre includere "Padova" e zone specifiche
- NO contenuti generici senza localizzazione

---

## SKILL COMPLETA

Per dettagli approfonditi su strategia SERP, competitor, KPI, calendario editoriale e TODO operativi, consulta:
**`TEST-SKILL/SKILL-UNIFICATA.md`**

---

## FILE DA NON VALIDARE

Questi file sono esclusi dalla validazione automatica perche' sono template o pagine speciali:
- `admin.html` — pannello admin
- `blog-articolo.html` — template dinamico
- `immobile.html` — genera contenuto via JS
- `scraping.html`, `bookmarklet-helper.html`, `unsubscribe.html`
- `privacy.html`, `cookie-policy.html`
