# SKILL-ESSENTIALS — Righetto Immobiliare
> Carica SEMPRE questo file. Contiene le regole operative core.
> Versione estratta da SKILL-2.0.md — Maggio 2026

---

## CLAIM CONSENTITI (verificati)
| Dato | Valore |
|---|---|
| Immobili gestiti | 350+ |
| Comuni coperti | 101 |
| Soddisfazione clienti | 98% |
| Recensioni Google | 127 da 4.9/5 |
| Attivi dal | 2000 |
| Compenso mediazione | Da concordare in sede; non pubblicare listini sul sito |

> **REGOLA D'ORO:** Se non hai fonte verificabile, NON inserire il dato.
> Sostituire TUTTI i placeholder [DATO], [ZONA], [FONTE] prima di pubblicare.

---

## 1. REGOLE OPERATIVE (da seguire sempre)

1. **Leggi prima** il file da modificare — mai al buio
2. **Mobile-first** — ogni modifica deve funzionare su mobile
3. **No librerie extra** — vanilla HTML/CSS/JS (zero framework, zero CDN esterni)
4. **Commit + push automatici** — vedi §1.1 sotto (non chiedere conferma a fine task)
5. **Mai toccare** DNS, record MX, cPanel senza conferma esplicita dell'utente
6. **Aggiorna sitemap.xml** quando aggiungi/rimuovi pagine
7. **Performance** — mai animazioni sull'elemento LCP senza `animation-play-state: paused`
8. **No `filter: blur`** su animazioni — solo `opacity` e `transform`
9. **No `will-change` permanente**
10. **CTA contrasto minimo 4.5:1** (WCAG AA) — MAI `var(--oro)` / `#FF6B35` con testo bianco
11. **URL pulite** — MAI `.html` nei link interni. Tutti gli `href`, canonical, og:url, sitemap → senza `.html`
12. **Cache-busting obbligatorio** — ogni CSS/JS linkato DEVE avere `?v=N`. Incrementare ad ogni modifica
13. **Form lead (landing / blog / servizi)** — invio **in pagina** con `SERVIZI_CONFIG.sendNotifica()` + insert Supabase `richieste`; **mai** solo redirect GET a Contatti; **mai** chiamare `send-mail.php` dal browser. Dettaglio: **`TEST-SKILL/skill-forms-leads.md`**

### Registrazione automatica nuove pagine
- **Blog** → `admin.html` (`_blogSeedArticles` con `data_pubblicazione: 'YYYY-MM-DD'`) + `blog.html` + `js/homepage.js` (staticMap + articoliStatici) + `sitemap.xml`
- **Landing** → `admin.html` (`_landingSeedPages` con `data_pubblicazione: 'YYYY-MM-DD'`) + `sitemap.xml`
- **Pagine generiche** → `sitemap.xml` + navigazione

### Stile di comunicazione
- Rispondi in italiano
- Diretto e pratico
- Proponi sempre prima di agire su operazioni irreversibili (eccetto commit/push: vedi §1.1)

### 1.1 Commit e push automatici (OBBLIGATORIO — giugno 2026)
Dopo **ogni** task che produce o modifica file nel repo (pagine, blog, CSS/JS, script, asset, skill, sitemap, seed admin), l'agente **committa e pusha senza chiedere** — così il sito su GitHub Pages si aggiorna e non si sprecano turni a «vuoi push?».

**Flusso standard (fine task):**
1. `git status` + `git diff` — verifica cosa va incluso
2. **Non** aggiungere `.env`, credenziali, segreti
3. `git add` solo file pertinenti al task
4. Commit in **italiano**, 1–2 frasi sul *perché*
5. `git push origin main` (o branch del task con `-u` se diverso da `main`)
6. In risposta all'utente: hash commit + conferma push (breve)

**Eccezioni (NON commit/push):**
- Solo domande, review o spiegazioni **senza** modifiche ai file
- L'utente chiede esplicitamente di **non** committare o di lasciare bozza locale
- Hook pre-commit fallito → correggere e **nuovo** commit (mai `--no-verify` salvo richiesta esplicita)
- Working tree già pulito → niente commit vuoto

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
- [ ] Se landing o form lead: checklist **`skill-forms-leads.md`** (invio diretto, GDPR, provenienza, success inline)

### Checklist aggiuntiva blog
- [ ] **Anti-doppioni (§8.1a):** `check_doppioni_sito.py` + verifica titolo/slug/tema **prima** di scrivere; se doppione → altro argomento da fonte istituzionale (web)
- [ ] Registrato in TUTTI e 4: admin.html + blog.html + homepage.js + sitemap.xml
- [ ] `data_pubblicazione: 'YYYY-MM-DD'` nel seed (BLOCCANTE per commit)
- [ ] Cross-link con zone pages e service pages (min 3)
- [ ] Timestamp "Ultimo aggiornamento" visibile
- [ ] Se form/CTA lead in articolo: **`skill-forms-leads.md`** (stesso flusso di `contatti.html`)

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

- [ ] **Commit + push eseguiti** se ci sono file modificati (§1.1) — non delegare all'utente

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

---

## 5. SOCIAL / META / GBP (cron `righetto_social/`)

- Skill dedicata: **`skill-social-automation.md`** (rotazione catalogo, token PAGE, reel, checklist avvio).
- Sintesi: `SKILL-2.0.md` §**10.4**. Non committare `.env`; non copiare testi RSS.

---

## 6. CURSOR RULES (`.mdc` scoped)

- Documentazione: **`skill-cursor-rules.md`**
- **`righetto-core.mdc`** → sempre attiva (claim, stack, routing)
- Altre rule si attivano sui file: blog, HTML/CSS, form, social, SEO, SQL/admin
- **`context-map.json`** v1.2 collega task → skill + hint rule
- Aggiornare le `.mdc` solo come **estratto**; la modifica operativa va in `skill-*.md` / `SKILL-2.0.md`
