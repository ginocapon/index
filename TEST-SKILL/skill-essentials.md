# SKILL-ESSENTIALS — Righetto Immobiliare
> **GATE:** leggi prima **`TEST-SKILL/skill-massimo-punteggio.md`** (checklist Google completa + strumenti gratuiti).  
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
3. **No librerie extra** — vanilla HTML/CSS/JS; librerie solo in `js/vendor/` (supabase, jspdf, qrcode) — zero CDN jsdelivr/cdnjs/fonts.googleapis
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
14. **Foto annunci (luglio 2026)** — servite da `righettoimmobiliare.it/img/immobili/` (GitHub Pages). Dopo upload in admin: sync **automatico** ogni 6 h via `.github/workflows/sync-media-github.yml` — **non** chiedere all'utente comandi manuali. Dettaglio: **`TEST-SKILL/skill-media-migration.md`**
15. **Title e meta description (BLOCCANTE)** — su **ogni** pagina HTML creata o modificata: vedi **§1.2** sotto; verificare con `validate-page.js` **prima** del commit

### 1.2 Title e Meta — gate obbligatorio (luglio 2026)

**Applies to:** blog, zone, landing, servizi, pillar, pagine generiche — qualsiasi contenuto con `<title>` e meta description.

| Campo | Target SEO (ideale) | Massimo (audit admin = warning) |
|-------|---------------------|----------------------------------|
| `<title>` | **≤60 caratteri** | **≤70** (oltre = warning in Audit Sito) |
| `meta name="description"` | **120–155 caratteri** | **≤160** (oltre = warning) |

**Regola agente (BLOCCANTE a fine task contenuti):**
1. Contare i caratteri di title e meta **prima** di committare.
2. Eseguire `node scripts/validate-page.js --file percorso-pagina.html` (o `--staged`).
3. Se title >70 o meta >160 → **accorciare** nel file; non consegnare con warning evitabili.
4. Title, H1 e meta devono usare **varianti diverse** (mai la stessa frase ripetuta).

**Template zone (evitare):** `Case in Vendita e Affitto a {Zona}, Padova | Righetto Immobiliare` (~73 char).  
**Preferire:** `{Zona} Padova: vendita e affitto | Righetto` oppure `Affitti e vendita {Zona} Padova | Righetto`.

**Strumenti allineati:** Audit admin → Audit Sito · pre-commit `validate-page.js` · venerdì `mini-seo-check.sh` · batch `patch_compliance_warns.py`.

Dettaglio SEO: **`skill-massimo-punteggio.md` §2.2** · **`skill-content.md`** meta articolo · **`skill-seo.md`**.

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

- [ ] **Title/meta (§1.2 BLOCCANTE):** title ≤60 (max 70), meta 120–155 (max 160) — `validate-page.js` OK
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
- [ ] Author bio visibile (E-E-A-T) — blog: link a `/gino-capon` o `/linda-righetto`
- [ ] Se landing: `data_pubblicazione: 'YYYY-MM-DD'` in `_landingSeedPages`
- [ ] Se landing o form lead: checklist **`skill-forms-leads.md`** (invio diretto, GDPR, provenienza, success inline)

### Checklist aggiuntiva blog
- [ ] **Anti-doppioni (§8.1a):** `TEST-SKILL/skimm.md` + `check_doppioni_sito.py` + `build_skimm.py` **prima** di scrivere; kw_primaria univoca; se doppione → altro argomento da fonte istituzionale
- [ ] **Venerdì:** checklist completa in **`skill-massimo-punteggio.md` §4** (compliance 0/0, Issue/email, 8/8, ritmo editoriale)
- [ ] Registrato in TUTTI e 4: admin.html + blog.html + homepage.js + sitemap.xml
- [ ] `data_pubblicazione: 'YYYY-MM-DD'` nel seed (BLOCCANTE per commit)
- [ ] Copertina + corpo: foto **realistiche** (§2.1 `skill-content.md`); **no** illustrazioni/AI/3D; ≥3 figure + ≥2 SVG colorati
- [ ] Elenco blog/homepage articoli: **solo ordine per data** (no featured che nasconde articoli)
- [ ] **Secondo passaggio auto-verifica** (§8.1c.8): validate-page + grep registri + campione immagini — eseguito dall'agente
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

- [ ] **Title e meta verificati** su ogni HTML toccato — §1.2 + `node scripts/validate-page.js --file …`
- [ ] **Commit + push eseguiti** se ci sono file modificati (§1.1) — non delegare all'utente

**Automatiche (pre-commit hook):**
- `node scripts/validate-page.js --staged`
- Schema mancante → commit BLOCCATO
- Title mancante → commit BLOCCATO
- `data_pubblicazione` mancante → commit BLOCCATO

**Manuali periodiche:**
- **Venerdì:** `skill-massimo-punteggio.md` **§4** (compliance, SKIMM, 8/8, azioni da Issue/email)
- Contrasto WCAG: mai `var(--oro)` con testo bianco (ratio 1.54:1 = FAIL)
- Allineamento array: `blog.html`, `homepage.js`, `admin.html` stessi articoli
- `robots.txt`: AI bots (GPTBot, ClaudeBot, Google-Extended, PerplexityBot) NON bloccati
- `llms.txt`: aggiornato con nuovi contenuti e prezzi
- Timestamp cornerstone: aggiornare ogni mese

### Sicurezza — 2 volte a settimana (OBBLIGATORIO)
**Skill:** **`TEST-SKILL/skill-security.md`** — martedì e venerdì (o su richiesta «revisione sicurezza»).

1. `bash scripts/security-check.sh` (statico, anche in CI)
2. `python tools/check_rls_exposure.py` (locale, richiede `.env`)
3. Checklist §3 in `skill-security.md` (admin, Edge email, segreti)
4. Issue GitHub label `security` aggiornata dal workflow `security-check-bisettimanale.yml`

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

## 5b. MEDIA ANNUNCI — sync automatico (luglio 2026)

- Skill dedicata: **`skill-media-migration.md`**
- Sintesi: `SKILL-2.0.md` §**10.5**
- **Dopo upload foto in admin:** sync GitHub Actions ogni **6 h** — **non** chiedere comandi all'utente
- Workflow: `.github/workflows/sync-media-github.yml` · script: `scripts/sync_media_automation.py`
- Foto pubbliche: `img/immobili/` · reel: `img/video/reels/` (`REEL_LOCAL=1`)

---

## 6. SICUREZZA (antihacker)

- Modulo dedicato: **`skill-security.md`**
- **2×/settimana:** martedì + venerdì — revisione generale (segreti, RLS, admin, spam email, XSS)
- **Mai in commit:** `.env`, password admin, `service_role`, token Meta, API relay produzione
- Script: `scripts/security-check.sh`, `tools/check_rls_exposure.py`

---

## 7. CURSOR RULES (`.mdc` scoped)

- Documentazione: **`skill-cursor-rules.md`**
- **`righetto-core.mdc`** → sempre attiva (claim, stack, routing)
- Altre rule si attivano sui file: blog, HTML/CSS, form, social, SEO, SQL/admin
- **`context-map.json`** v1.3 collega task → skill + hint rule
- Aggiornare le `.mdc` solo come **estratto**; la modifica operativa va in `skill-*.md` / `SKILL-2.0.md`
