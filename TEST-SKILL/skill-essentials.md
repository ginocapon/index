# SKILL-ESSENTIALS — Righetto Immobiliare
> Carica SEMPRE questo file. Contiene le regole operative core.
> Versione estratta da SKILL-2.0.md — Marzo 2026

---

## CLAIM CONSENTITI (verificati)
| Dato | Valore |
|---|---|
| Immobili gestiti | 350+ |
| Comuni coperti | 101 |
| Soddisfazione clienti | 98% |
| Recensioni Google | 127 da 4.9/5 |
| Attivi dal | 2000 |
| Commissione vendita | 3% + IVA per parte (min. 2.500€) |
| Commissione affitto | 1 mensilità + IVA |

> **REGOLA D'ORO:** Se non hai fonte verificabile, NON inserire il dato.
> Sostituire TUTTI i placeholder [DATO], [ZONA], [FONTE] prima di pubblicare.

---

## 1. REGOLE OPERATIVE (da seguire sempre)

1. **Leggi prima** il file da modificare — mai al buio
2. **Mobile-first** — ogni modifica deve funzionare su mobile
3. **No librerie extra** — vanilla HTML/CSS/JS (zero framework, zero CDN esterni)
4. **Commit** chiari e descrittivi in italiano
5. **Mai toccare** DNS, record MX, cPanel senza conferma esplicita dell'utente
6. **Aggiorna sitemap.xml** quando aggiungi/rimuovi pagine
7. **Performance** — mai animazioni sull'elemento LCP senza `animation-play-state: paused`
8. **No `filter: blur`** su animazioni — solo `opacity` e `transform`
9. **No `will-change` permanente**
10. **CTA contrasto minimo 4.5:1** (WCAG AA) — MAI `var(--oro)` / `#FF6B35` con testo bianco
11. **URL pulite** — MAI `.html` nei link interni. Tutti gli `href`, canonical, og:url, sitemap → senza `.html`
12. **Cache-busting obbligatorio** — ogni CSS/JS linkato DEVE avere `?v=N`. Incrementare ad ogni modifica

### Registrazione automatica nuove pagine
- **Blog** → `admin.html` (`_blogSeedArticles` con `data_pubblicazione: 'YYYY-MM-DD'`) + `blog.html` + `js/homepage.js` (staticMap + articoliStatici) + `sitemap.xml`
- **Landing** → `admin.html` (`_landingSeedPages` con `data_pubblicazione: 'YYYY-MM-DD'`) + `sitemap.xml`
- **Pagine generiche** → `sitemap.xml` + navigazione

### Stile di comunicazione
- Rispondi in italiano
- Diretto e pratico
- Proponi sempre prima di agire su operazioni irreversibili

---

## 2. CHECKLIST PER OGNI NUOVA PAGINA

- [ ] Title unico (max 60 char) + Meta description (max 160 char)
- [ ] H1 unico + Alt text su tutte le immagini
- [ ] Schema.org: `RealEstateAgent` + `GeoCoordinates` + `FAQPage` + `BreadcrumbList` + `sameAs` social
- [ ] Open Graph tags + Canonical URL (senza `.html`)
- [ ] Hero image `<link rel="preload">` + font above-fold preloaded
- [ ] Nessun `loading="lazy"` above-the-fold
- [ ] CTA primario contrast >= 4.5:1 (MAI `var(--oro)` con `color:#fff`)
- [ ] Critical CSS inline, rest deferred (`media="print" onload="this.media='all'"`)
- [ ] Tutti i CSS/JS con `?v=N`
- [ ] Link interni verso pagine correlate (senza `.html`)
- [ ] Registrata in `sitemap.xml`
- [ ] Frasi dichiarative prime 2 righe (GEO)
- [ ] Dati numerici specifici con fonte (GEO)
- [ ] Min 5 FAQ con Schema FAQPage (AEO)
- [ ] Author bio visibile (E-E-A-T) — solo blog
- [ ] Se landing: `data_pubblicazione: 'YYYY-MM-DD'` in `_landingSeedPages`

### Checklist aggiuntiva blog
- [ ] Registrato in TUTTI e 4: admin.html + blog.html + homepage.js + sitemap.xml
- [ ] `data_pubblicazione: 'YYYY-MM-DD'` nel seed (BLOCCANTE per commit)
- [ ] Cross-link con zone pages e service pages (min 3)
- [ ] Timestamp "Ultimo aggiornamento" visibile

### Checklist aggiuntiva zona page
- [ ] Schema `Place` con `GeoCoordinates` + `sameAs`
- [ ] Schema `RealEstateAgent` con `aggregateRating`
- [ ] Sezione **Pro/Contro** (4+4, lista onesta — E-E-A-T)
- [ ] Minimo 5 FAQ nello schema FAQPage
- [ ] Registrata in `blog.html` (array `articoliStatici`) + `sitemap.xml`
- [ ] Aggiornato `llms.txt` con nuova zona e prezzi
- [ ] Link nel footer di tutte le zone pages

---

## 3. VERIFICHE POST-MODIFICA

**Automatiche (pre-commit hook):**
- `node scripts/validate-page.js --staged`
- Schema mancante → commit BLOCCATO
- Title mancante → commit BLOCCATO
- `data_pubblicazione` mancante → commit BLOCCATO

**Manuali periodiche:**
- Contrasto WCAG: mai `var(--oro)` con testo bianco (ratio 1.54:1 = FAIL)
- Allineamento array: `blog.html`, `homepage.js`, `admin.html` stessi articoli
- `robots.txt`: AI bots (GPTBot, ClaudeBot, Google-Extended, PerplexityBot) NON bloccati
- `llms.txt`: aggiornato con nuovi contenuti e prezzi
- Timestamp cornerstone: aggiornare ogni mese

---

## 4. I 4 LOOP DI VALIDAZIONE (sintesi)

Eseguire sempre in sequenza dopo ogni modifica:

| Loop | Cosa controlla | N. check |
|---|---|---|
| **Loop 1** | Struttura HTML (DOCTYPE, viewport, preload, skip link, breadcrumb, immagini, aria) | 25 |
| **Loop 2** | SEO & Schema (title, meta, H1, canonical, OG, schema JSON-LD, sitemap, GEO, E-E-A-T) | 25 |
| **Loop 3** | Coerenza globale (sitemap, nav, footer, blog listing, CSS vars, schema uniforme, GA4, GDPR) | 18 |
| **Loop 4** | Performance & Mobile (critical CSS, font, lazy/eager, JS defer, responsive, touch target, WebP) | 25 |

> Dettaglio completo di ogni check: vedi SKILL-2.0.txt sezioni 15.1–15.4
