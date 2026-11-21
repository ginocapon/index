# FRAMEWORK-SKILL — Sito professionale creativo (video maker / portfolio dinamico)

> **Versione:** 1.0 — estratto dalla metodologia operativa Righetto Immobiliare (TEST-SKILL / SKILL-2.0)  
> **Uso:** linea guida fondamentale per un progetto giovane e dinamico — portfolio, blog, landing, lead.  
> **Personalizza:** sostituire tutti i placeholder `[…]` prima del go-live.

---

## Indice moduli (come nel sistema originale)

| Modulo | Contenuto | Priorità |
|--------|-----------|----------|
| **§0** Gate qualità | Checklist Google / performance / compliance | Sempre |
| **§1** Essentials | Regole operative, commit, URL, cache | Sempre |
| **§2** Architettura | Stack, hosting, file, email | Setup |
| **§3** Design & UI | Palette, tipografia, mobile, animazioni | UI |
| **§4** SEO on-page | Title, meta, schema, CWV | Ogni pagina |
| **§5** GEO / AEO | Visibilità AI, snippet, llms.txt | Contenuti |
| **§6** Blog & contenuti | Struttura articoli, editorial catalog | Blog |
| **§7** Form & lead | Invio, GDPR, provenienza | Conversione |
| **§8** Sicurezza | 2×/settimana, segreti, RLS | Permanente |
| **§9** AI Act UE | Trasparenza Reg. 2024/1689 | Permanente |
| **§10** Workflow agenti | Cursor rules, validazione, cron | Ops |
| **§11** Checklist rapide | Nuova pagina, nuovo articolo, audit | Reference |

**Regola d’oro (da mantenere):** se non hai una fonte verificabile per un dato numerico o un claim, **non inserire il dato**.

---

## §0 — Gate qualità (leggere prima di ogni modifica)

Obiettivo: **10/10** su SEO tecnico, contenuti utili, Core Web Vitals, accessibilità, E-E-A-T, GEO/AEO.

### Ordine di lettura per agenti / sviluppatori

1. Questo file (FRAMEWORK-SKILL)
2. §1 Essentials
3. Modulo del task (blog → §6, landing → §7, audit → §4+§8)
4. File HTML/CSS/JS da modificare

### Strumenti gratuiti (zero costo)

| Strumento | Uso |
|-----------|-----|
| [PageSpeed Insights](https://pagespeed.web.dev/) | LCP, INP, CLS |
| [Rich Results Test](https://search.google.com/test/rich-results) | Schema JSON-LD |
| [Search Console](https://search.google.com/search-console) | Indicizzazione, query |
| [WAVE](https://wave.webaim.org/) / axe DevTools | WCAG AA |
| Lighthouse CLI | Audit locale completo |

### Target metriche (2026)

| Area | Target |
|------|--------|
| LCP | < 2,5 s (ideale < 2 s) |
| INP | < 200 ms |
| CLS | < 0,1 |
| Title | ≤ 60 caratteri (max 70) |
| Meta description | 120–155 caratteri (max 160) |
| Contrasto CTA | ≥ 4,5:1 (WCAG AA) |

### Routine post-modifica (adatta al tuo repo)

```bash
# Esempi — creare script equivalenti nel nuovo progetto
node scripts/validate-page.js --file pagina.html    # title/meta/schema
bash scripts/security-check.sh                      # segreti statici
bash scripts/mini-seo-check.sh                      # sitemap, canonical, GEO
```

---

## §1 — Essentials (regole operative)

### 1.1 Claim e dati verificati

Compila la tabella **solo** con dati reali del tuo studio:

| Dato | Valore verificato | Fonte |
|------|-------------------|-------|
| Progetti completati | `[N]` | Portfolio / clienti |
| Anni di attività | `[dal YEAR]` | CV / partita IVA |
| Recensioni | `[N]` a `[X]/5` | Google / piattaforma |
| Specializzazione | `[wedding / corporate / social / reel]` | — |
| Zona operativa | `[città / regione]` | — |

> Vietato inventare numeri per “sembrare più grande”. Meglio pochi dati veri.

### 1.2 Regole da seguire sempre

1. **Leggi il file** prima di modificarlo — mai al buio
2. **Mobile-first** — ogni modifica funziona su 375 px
3. **Stack consigliato (giovane + performante):** HTML/CSS/JS **vanilla** · hosting statico (GitHub Pages, Cloudflare Pages, Netlify) · backend leggero solo se serve (Supabase, form serverless)
4. **Zero CDN esterni** non necessari — self-host font e librerie in `js/vendor/` (GDPR + velocità)
5. **URL pulite** — link interni **senza** `.html`; canonical e sitemap allineati
6. **Cache-busting** — CSS/JS con `?v=N`; incrementare ad ogni modifica
7. **Sitemap** — aggiornare quando aggiungi/rimuovi pagine
8. **Performance** — no `filter: blur` su animazioni; solo `opacity` e `transform`; no `will-change` permanente
9. **LCP** — hero preload, no `loading="lazy"` above-the-fold
10. **Commit** dopo task con file modificati; **push** solo se richiesto o policy CI
11. **DNS / MX / email server** — non toccare senza conferma esplicita
12. **Title e meta** — gate bloccante su ogni pagina (§4.1)
13. **AI Act** — trasparenza su contenuti sintetici e assistenti (§9)

### 1.3 Title e meta — gate obbligatorio

| Campo | Target | Massimo |
|-------|--------|---------|
| `<title>` | ≤ 60 caratteri | ≤ 70 |
| `meta description` | 120–155 caratteri | ≤ 160 |

- Title, H1 e meta = **varianti diverse** (mai la stessa frase ripetuta)
- Verificare prima del commit con script di validazione

### 1.4 Stile di comunicazione (video maker giovane)

| Principio | Applicazione |
|-----------|--------------|
| **Diretto** | Frasi brevi, zero burocratese |
| **Visivo** | Il testo supporta il reel — non lo sostituisce |
| **Autentico** | Behind the scenes, processo, non solo “siamo i migliori” |
| **Professionale** | Niente slang eccessivo; tono creativo ma affidabile |
| **Locale** | Città/regione nel copy quando serve SEO locale |
| **Trasparente** | Prezzi/listini solo se reali; altrimenti “su preventivo” |

---

## §2 — Architettura progetto

### 2.1 Stack consigliato (dinamico ma solido)

| Layer | Scelta | Note |
|-------|--------|------|
| Frontend | HTML + CSS + JS vanilla | Portfolio, blog, landing |
| Hosting sito | GitHub Pages / Cloudflare Pages | Deploy da `main` |
| Media pesanti | Self-host o CDN proprio | Reel, showreel — WebP + MP4 ottimizzati |
| Database (opz.) | Supabase | Lead, blog dinamico, admin |
| Email lead | Edge Function → relay SMTP | Mai aprire relay con GET |
| Analytics | GA4 o Plausible | Con consenso cookie |
| Repo | Git + branch protetto | Pre-commit hooks |

### 2.2 Struttura file suggerita

```
index.html                 # Homepage — hero video/reel, CTA, portfolio preview
portfolio.html             # Griglia progetti / categorie
blog.html                  # Hub articoli (ordine per data)
blog-*.html                # Articoli long-form
servizi-*.html             # Wedding, corporate, social, eventi…
landing-*.html             # Conversione (preventivo, call, reel pack)
contatti.html              # Form lead + mappa
chi-siamo.html             # E-E-A-T, story, team
privacy.html               # GDPR + § trasparenza digitale (AI Act)
css/
  main.css                 # Design system
  blog.css                 # Long-read
js/
  main.js
  config.js                # API, sendNotifica
  vendor/                  # Solo se indispensabile
img/
  portfolio/               # Thumbnail progetti
  blog/                    # Copertine articoli
  brand/                   # Logo, OG
video/
  showreel/                # Hero MP4 (compresso)
data/
  editorial-catalog.json   # Catalogo keyword (equivalente SKIMM)
sitemap.xml
robots.txt
llms.txt                   # Per AI search (ChatGPT, Perplexity…)
ai.json                    # Metadata per crawler AI
.well-known/security.txt
scripts/
  validate-page.js
  security-check.sh
  check-duplicates.py        # Anti-doppioni blog
.github/workflows/
  deploy.yml
  security-weekly.yml
```

### 2.3 URL pattern (senza .html)

| Tipo | Pattern esempio |
|------|-----------------|
| Portfolio item | `/portfolio/slug-progetto` o `portfolio-slug.html` → rewrite |
| Blog | `/blog-slug-tema-anno` |
| Servizio | `/servizi-wedding-video` |
| Landing | `/preventivo-video` |

---

## §3 — Design & UI (giovane, dinamico, accessibile)

### 3.1 Principi per un video maker

- **Hero con movimento** — showreel autoplay muted loop, poster WebP, play controllabile
- **Griglia portfolio** — hover con preview clip o GIF leggera
- **Contrasto** — CTA sempre leggibili; **mai** colore accento con testo bianco se ratio < 4,5:1
- **Tipografia** — un display per titoli + un sans per body (self-hosted WOFF2)
- **Spazio negativo** — il video è protagonista; UI non invadente
- **Dark mode opzionale** — coerente con estetica reel

### 3.2 Spacing mobile (reference)

| Contesto | Mobile |
|----------|--------|
| Sezione padding | 60px 20px |
| Grid gap | 16px |
| Heading → content | 22–32px |
| Content → CTA | 40px |
| Touch target | ≥ 44px |

### 3.3 Animazioni

- Scroll reveal: solo `opacity` + `transform`
- `prefers-reduced-motion: reduce` → disattiva animazioni
- Hero video: `playsinline`, `muted`, `preload="metadata"` o poster first

### 3.4 Palette (personalizza)

```css
:root {
  --primario:     #[COLORE_BRAND];
  --accent:       #[CTA];
  --nero:         #[TESTO];
  --sfondo:       #[BG];
  --radius:       12px;
  --max-w:        1200px;
}
```

> Documentare nel “print tecnico” dedicato i valori finali brand.

---

## §4 — SEO on-page

### 4.1 Checklist ogni pagina

- [ ] Title ≤ 60 (max 70), meta 120–155 (max 160)
- [ ] H1 unico, diverso da title
- [ ] Canonical senza `.html`
- [ ] Open Graph + Twitter Card (immagine 1200×630 min)
- [ ] Alt text su ogni immagine
- [ ] Breadcrumb visivo + `BreadcrumbList` JSON-LD
- [ ] Link interni correlati (min 2–3)
- [ ] Registrata in `sitemap.xml`

### 4.2 Schema.org (video maker)

| Pagina | Schema principale |
|--------|-------------------|
| Homepage | `ProfessionalService` o `LocalBusiness` + `VideoObject` (showreel) |
| Portfolio item | `CreativeWork` + `VideoObject` |
| Blog | `BlogPosting` + `Person` (autore) |
| Servizi | `Service` + `FAQPage` |
| Chi siamo | `Person` + `Organization` |

Obbligatori cross-page dove applicabile:

- `Organization` / `Person` con `sameAs` (Instagram, YouTube, Vimeo, LinkedIn)
- `GeoCoordinates` se servizio locale
- `FAQPage` — min 5 FAQ su servizi e landing

### 4.3 Core Web Vitals

- Preload hero (immagine o poster video)
- Font critici preload + `font-display: swap`
- Immagini con `width` + `height` espliciti
- Video hero: file < 3–5 MB dove possibile; qualità adaptive
- CSS critico inline; resto deferred

### 4.4 E-E-A-T (credibilità creativa)

- Pagina autore con bio, foto reale, link social
- Case study portfolio: cliente (se consentito), problema, soluzione, risultato
- “Ultimo aggiornamento” su contenuti cornerstone
- Recensioni reali — mai false
- Processo di lavoro documentato (pre-produzione, giorno evento, post)

---

## §5 — GEO / AEO (visibilità AI e snippet)

### 5.1 GEO — Generative Engine Optimization

1. **Prime 2 righe** di ogni sezione: frase dichiarativa auto-contenuta
2. **Dati specifici** verificabili (anni, formati, tempi di delivery)
3. Formato: **H2 domanda → risposta 40–60 parole → approfondimento**
4. Liste, tabelle, definizioni chiare
5. Aggiornare `llms.txt` e `ai.json` con nuovi URL pillar
6. `robots.txt`: **non** bloccare GPTBot, ClaudeBot, Google-Extended, PerplexityBot (se vuoi visibilità AI)

### 5.2 AEO — Answer Engine Optimization

- Min 5 FAQ con schema su pagine servizi e articoli pillar
- Risposte FAQ: 40–80 parole, testo identico in HTML e JSON-LD
- Box sintesi nelle prime 150 parole degli articoli macro

### 5.3 Google AI Overviews (2026)

Per Google Search valgono le stesse regole SEO standard: contenuto utile, E-E-A-T, no “farm” di citazioni artificiali.

---

## §6 — Blog e contenuti editoriali

Metodologia estratta dal sistema Righetto (SKIMM + skill-content): adatta al video.

### 6.1 Catalogo editoriale (equivalente SKIMM)

Prima di ogni nuovo articolo:

1. Consultare `data/editorial-catalog.json` (keyword primaria univoca)
2. Eseguire script anti-doppioni (`check-duplicates.py`)
3. Se tema già coperto → **STOP** → nuovo angolo (formato, cliente tipo, strumento, location)

**Strategie long-tail senza cannibalizzazione:**

| Strategia | Esempio video maker |
|-----------|---------------------|
| Intent diverso | “Costo video matrimonio” vs “Come scegliere videomaker” |
| Formato | “Reel vs spot 30s per ristorante” |
| Strumento | “Sony FX3 vs iPhone per eventi” |
| Località | “Videomaker [città] matrimoni” vs generico nazionale |
| Processo | “Timeline post-produzione wedding” |

### 6.2 Standard articolo blog

| Elemento | Standard |
|----------|----------|
| Lunghezza pillar | 2 500–3 500 parole utili |
| Lunghezza secondario | 1 500–2 000 parole |
| H2 | Min 5–8, formato domanda (AEO) |
| H2+H3 totali | Min 15, max 28 |
| FAQ schema | Min 5 |
| Internal links | Min 3 (servizi, portfolio, altri blog) |
| Immagini | Min 3 figure + 2 grafici/SVG se dati |
| Author bio | Visibile, con link pagina autore |
| Timestamp | “Ultimo aggiornamento” visibile |
| Anti-riempimento | Vietato loop di paragrafi identici per word count |

### 6.3 Formato sezione (GEO/AEO)

1. Frase dichiarativa (prime 2 righe)
2. Risposta diretta 40–60 parole dopo H2
3. Approfondimento con esempi, tabelle, embed video proprio (YouTube/Vimeo embed solo URL fissi)

### 6.4 Immagini blog

| Consentito | Vietato |
|------------|---------|
| Frame reali da progetti (con permesso) | Stock generico senza contesto |
| Behind the scenes autentici | Illustrazioni AI “plastic” come sostituto foto |
| WebP hero 1200×630 o 19:9 dedicato | CDN esterni non controllati |
| Didascalie honest | Claim inventati nelle didascalie |

**AI Act:** se hero o grafica è generata/modificata con IA → didascalia + barra sito (§9).

### 6.5 Registrazione nuovo articolo

- [ ] File `blog-slug.html`
- [ ] Hub `blog.html` (array articoli, ordine **solo per data**)
- [ ] `sitemap.xml`
- [ ] Seed admin / CMS se presente
- [ ] `data/editorial-catalog.json` aggiornato
- [ ] `validate-page.js` OK
- [ ] Secondo passaggio auto-verifica (grep slug, immagini, elenco)

### 6.6 Cluster contenuti suggeriti (video maker)

| Cluster | Esempi articoli |
|---------|-----------------|
| Matrimoni | Costi, timeline, cosa chiedere al videomaker |
| Corporate | Video aziendale, interviste, brand film |
| Social / Reel | Pack reel mensile, formati verticali |
| Tecnica | Gear, color grading, audio eventi |
| Local SEO | Videomaker [città], location migliori |
| Processo | Pre-produzione, giorno evento, delivery |

---

## §7 — Form e lead

### 7.1 Regola bloccante

Ogni form di contatto/preventivo deve:

1. **Inviare in pagina** — un solo passaggio (no redirect GET a contatti)
2. Salvare lead con campo **`provenienza`** = slug pagina (`blog-slug`, `landing-preventivo`)
3. Inviare notifica email via backend sicuro (Edge Function / serverless)
4. Mostrare **successo inline** (box verde, nascondere campi)
5. Checkbox **GDPR** obbligatoria

### 7.2 Vietato

| Errore | Perché |
|--------|--------|
| Solo link “contattaci” senza form | Perdi conversione e tracking |
| Aprire endpoint mail con GET | Esposizione + errore |
| Form senza provenienza | Non sai da dove arriva il lead |
| Race `defer` su config + submit inline | `undefined` al primo click |

### 7.3 Checklist nuova landing

- [ ] Form con invio diretto + GDPR
- [ ] `provenienza` univoca
- [ ] Success state inline
- [ ] Title/meta validati
- [ ] `sitemap.xml`
- [ ] CTA contrasto ≥ 4,5:1
- [ ] Test DevTools: POST a endpoint email → 200

---

## §8 — Sicurezza

### 8.1 Cadenza

| Frequenza | Azione |
|-----------|--------|
| 2×/settimana | Checklist §8.2 (martedì + venerdì) |
| Dopo ogni deploy | `security-check.sh` |
| Post-incidente | Rotazione segreti + issue documentata |

### 8.2 Checklist revisione

**Segreti e repo**

- [ ] Nessun `.env`, token, password in git
- [ ] API keys solo in secrets CI / hosting
- [ ] `.gitignore` per env e credenziali

**Backend / database (se Supabase)**

- [ ] RLS attivo: tabelle sensibili non leggibili con chiave `anon`
- [ ] Lead: INSERT anon OK, SELECT solo admin
- [ ] Nessun `service_role` nel frontend

**Form e email**

- [ ] Relay email: solo POST + API key
- [ ] Rate limit su invio
- [ ] Honeypot / validazione base anti-spam
- [ ] Input sanitizzato (no XSS in admin)

**Frontend**

- [ ] No `eval()` con input utente
- [ ] `innerHTML` solo con escape
- [ ] Embed video solo da domini fidati (YouTube, Vimeo)
- [ ] Admin: `noindex`, `robots.txt` Disallow

**Infrastruttura**

- [ ] `security.txt` con scadenza futura
- [ ] HTTPS, no mixed content
- [ ] Branch `main` protetto

### 8.3 Mai committare

- Token social, API relay produzione, password admin
- Chiavi `service_role`
- File `.env` con valori reali

---

## §9 — AI Act UE (Reg. 2024/1689) — priorità permanente

### 9.1 Cosa dichiarare

| Elemento | Obbligo |
|----------|---------|
| Contenuti sintetici (immagini/video IA) | Etichetta visibile “contenuto elaborato / IA” |
| Chatbot / form guidato | “Assistente automatizzato”, non operatore umano live |
| Portfolio | Solo materiale reale o dichiarato se alterato |
| Stime/preventivi automatici | Non presentare come contratto vincolante |

### 9.2 Implementazione tecnica (pattern)

- Barra footer sito: link a `privacy#trasparenza-digitale`
- CSS/JS centralizzati per disclosure (non testi diversi per pagina)
- Manifest immagini IA: JSON con path file generati
- Privacy § dedicata: assistente digitale, media sintetici, diritti

### 9.3 Checklist ogni nuova pagina

- [ ] Disclosure caricata su pagine pubbliche
- [ ] Foto/video IA marchiati
- [ ] Chatbot con etichetta automatizzato
- [ ] Privacy aggiornata se cambia uso IA

---

## §10 — Workflow agenti (Cursor / CI)

### 10.1 Layer documentazione (come Righetto)

| Layer | Ruolo |
|-------|--------|
| `FRAMEWORK-SKILL.md` (questo file) | Manuale master |
| `docs/skill-*.md` | Moduli per task |
| `context-map.json` | Routing task → modulo |
| `.cursor/rules/*.mdc` | Guardrail automatici su file |
| `.cursor/skills/*/SKILL.md` | Indici operativi (/blog, /seo…) |
| `CLAUDE.md` | Entry point agenti |

### 10.2 Mapping task → modulo

| Task | Moduli |
|------|--------|
| Nuovo articolo | §6 + §4 + §9 |
| Nuova landing | §7 + §3 + §4 |
| Fix mobile | §3 |
| Audit SEO | §4 + §5 + §0 |
| Sicurezza | §8 |
| Nuovo progetto portfolio | §3 + §4 + §9 |

### 10.3 Automazioni consigliate (GitHub Actions)

| Cron | Workflow |
|------|----------|
| Deploy | Push `main` → Pages |
| Venerdì | Audit SEO + freschezza contenuti |
| Mar + Ven | Security check statico |
| Opzionale | Sync media da CMS |

### 10.4 I 4 loop di validazione (sintesi)

| Loop | Focus | N. check indicativi |
|------|-------|---------------------|
| 1 | HTML struttura (viewport, skip link, aria, immagini) | ~25 |
| 2 | SEO & Schema (title, meta, JSON-LD, sitemap) | ~25 |
| 3 | Coerenza globale (nav, footer, listing blog, GDPR) | ~18 |
| 4 | Performance & mobile (LCP, lazy, touch, WebP) | ~25 |

---

## §11 — Checklist rapide

### Nuova pagina (qualsiasi)

- [ ] Title/meta §1.3
- [ ] H1 + alt immagini
- [ ] Schema appropriato
- [ ] OG + canonical
- [ ] CTA contrasto OK
- [ ] CSS/JS `?v=N`
- [ ] Sitemap
- [ ] AI disclosure §9
- [ ] Commit

### Nuovo articolo blog

- [ ] Anti-doppioni §6.1
- [ ] Struttura §6.2–6.4
- [ ] FAQ schema ≥ 5
- [ ] Author bio + timestamp
- [ ] Registrazione hub + sitemap §6.5
- [ ] `llms.txt` se pillar

### Audit settimanale (15 min)

- [ ] PageSpeed su homepage + 1 blog
- [ ] Search Console: errori indicizzazione
- [ ] Security script OK
- [ ] Form test: lead arriva con provenienza
- [ ] 1 contenuto nuovo O refresh dato su articolo top

---

## Appendice A — Placeholder da compilare

```yaml
nome_studio: "[NOME]"
dominio: "[esempio.it]"          # senza www
email_lead: "[info@…]"
telefono: "[+39 …]"
citta: "[…]"
instagram: "[url]"
youtube: "[url]"
vimeo: "[url]"
linkedin: "[url]"
color_primario: "[#hex]"
color_accent: "[#hex]"
ga4_id: "[G-…]"
supabase_url: "[se usato]"
```

---

## Appendice B — Origine metodologia

Questo framework deriva dall’organizzazione operativa di **Righetto Immobiliare** (`TEST-SKILL/`, `SKILL-2.0.md`), adattato per:

- Portfolio creativo e video maker
- Tono giovane e dinamico
- Stessa solidità su SEO, GEO, sicurezza, AI Act, blog long-form

**Prossimo step consigliato:** creare il “print tecnico” con palette definitiva, template HTML blog/portfolio, script `validate-page.js` e brand video (codec, risoluzioni reel, naming file).

---

*FRAMEWORK-SKILL v1.0 — Agosto 2026 — estratto per riuso su progetto videomaker.*
