# SKILL UNIFICATA — Righetto Immobiliare
## Prompt Operativo Master Consolidato

> **Versione:** 1.4 — 8 Marzo 2026 (4 loop di raffinamento completati)
> **Origine:** Fusione e razionalizzazione di SERP-STRATEGY.md (v. 4 marzo) + SKILL-KILLER.md (v1.6 - 7 marzo)
> **Ultimo aggiornamento Google verificato:** 8 Marzo 2026
> **Prossima verifica consigliata:** Aprile 2026

---

## 1. ISTRUZIONI PER CLAUDE

### 1.1 Verifica Aggiornamenti Google (Obbligatoria ad Ogni Sessione)
Prima di ogni sessione di lavoro, esegui queste ricerche web:
- `"Google Search updates [mese corrente] [anno corrente]"`
- `"Core Web Vitals updates [anno corrente]"`
- `"GEO Generative Engine Optimization updates [anno corrente]"`
- `"Google Search Console new features [anno corrente]"`

Confronta con la sezione "Stato Aggiornamenti Google" e aggiorna questo file se trovi novita'.

### 1.2 Regole Operative
1. **Leggi prima** il file da modificare — mai al buio
2. **Mobile-first** — ogni modifica deve funzionare su mobile
3. **No librerie extra** — il sito e' volutamente leggero (vanilla HTML/CSS/JS)
4. **Commit** chiari e descrittivi in italiano
5. **Mai toccare** DNS, record MX, configurazione cPanel senza conferma esplicita
6. **Aggiorna** sitemap.xml quando aggiungi/rimuovi pagine
7. **Visual Saliency** — ogni pagina nuova DEVE seguire le regole above-the-fold
8. **Performance** — mai animazioni sull'elemento LCP senza `animation-play-state: paused`
9. **Registra ogni nuovo articolo blog** in TUTTI questi punti:
   - `admin.html` → array `_blogSeedArticles`
   - `blog.html` → array `articoliStatici`
   - `js/homepage.js` → oggetto `staticMap` + array `articoliStatici`
   - `sitemap.xml` → nuovo URL

### 1.3 Stile di Comunicazione
- Rispondi in italiano
- Sii diretto e pratico
- Proponi sempre prima di agire su operazioni irreversibili

---

## 2. CONTESTO PROGETTO

### 2.1 Informazioni Generali
| Campo | Valore |
|---|---|
| **Dominio** | righettoimmobiliare.it / www.righettoimmobiliare.it |
| **Hosting sito** | GitHub Pages (deploy automatico da `main`) |
| **Hosting dominio/email** | cPanel (cpanel.righettoimmobiliare.it) |
| **Tech Stack** | HTML statico + CSS + JS + Express.js (dev) |
| **Database** | Supabase (PostgreSQL esterno) |
| **Newsletter** | Brevo (Sendinblue) |
| **Form contatti** | Formspree |
| **Analytics** | Google Analytics 4 (G-9MHDHHES26) |
| **Chatbot AI** | "Sara" — assistente virtuale integrata |
| **Repository** | GitHub — ginocapon/index |

### 2.2 Architettura DNS (NON TOCCARE MAI)
- **Record A:** GitHub Pages (185.199.108.153, etc.)
- **CNAME www:** ginocapon.github.io
- **Record MX:** email su cPanel (NON MODIFICARE)
- **Google Site Verification:** meta tag nel `<head>` di index.html

### 2.3 Struttura File Principale
```
index.html                          - Homepage (82KB, canvas animato, testimonial, CTA)
immobili.html                       - Lista immobili (Leaflet.js map, filtri)
immobile.html                       - Dettaglio immobile (galleria, form)
agenzia-immobiliare-padova.html     - Pagina pillar SEO keyword #1
servizi.html                        - Hub servizi
servizio-vendita.html               - Vendita (con FAQ + FAQPage schema)
servizio-locazioni.html             - Locazioni (con FAQ + FAQPage schema)
servizio-preliminari.html           - Preliminari (con FAQ + FAQPage schema)
servizio-valutazioni.html           - Valutazioni (con FAQ + FAQPage schema)
servizio-gestione.html              - Gestione immobili (con FAQ + FAQPage schema)
servizio-utenze.html                - Utenze (con FAQ + FAQPage schema)
chi-siamo.html                      - Chi siamo
contatti.html                       - Form contatti + WhatsApp
blog.html                           - Blog hub (32+ articoli registrati)
blog-*.html (21+ articoli)          - Articoli blog SEO
faq.html                            - FAQ (37+ domande con categorie)
zona-*.html (12 quartieri/comuni)   - Pagine quartieri (RealEstateAgent + FAQPage schema)
landing-vendita.html                - Landing vendita
landing-vendere-casa-padova.html    - Landing ultra-ottimizzata keyword
landing-valutazione.html            - Landing valutazione
landing-agente.html                 - Landing agente
landing-mutuo.html                  - Landing mutuo + simulatore
admin.html                          - Pannello admin (605KB, Supabase, 2FA)
llms.txt                            - File per AI bots (GEO)
sitemap.xml                         - 54+ URL indicizzati
robots.txt                          - Direttive crawler
server.js                           - Express.js con caching intelligente
js/chatbot.js                       - Chatbot Sara (105KB)
js/homepage.js                      - Homepage logic (22 staticMap entries)
js/config.js                        - Config API esterne
js/welcome-popup.js                 - Popup benvenuto
js/cookie-consent.js                - GDPR cookie consent
js/nav-mobile.js                    - Navigazione mobile
js/scroll-reveal.js                 - Animazioni scroll
```

---

## 3. STATO SEO E PERFORMANCE — PUNTEGGIO SITO

> Audit verificato: 8 marzo 2026

| Area | Punteggio | Note |
|---|---|---|
| SEO on-page | **9.5/10** | Il migliore tra i competitor locali |
| Schema.org | **9.5/10** | FAQPage su tutte le service pages + zone pages |
| Contenuti/Blog | **9.5/10** | 21+ articoli, 4 cluster completi su 4 |
| GEO/AEO | **9.5/10** | Unico a ottimizzare per AI — robots.txt, llms.txt, timestamp, sameAs tutti OK |
| Core Web Vitals | **8/10** | Buono, target LCP <2s da raggiungere |
| Chatbot AI | **10/10** | Unico nel mercato locale |
| Simulatore mutuo | **10/10** | Unico nel mercato locale |
| Recensioni Google | **6/10** | ~127 vs 256 Tetto Rosso — gap critico |
| Domain Authority | **4/10** | Problema #1 — nessun backlink significativo |
| Apparizione SERP | **2/10** | Non appare per keyword non-brand |
| **TOTALE** | **8.1/10** | Top tecnico, 4 cluster completi, invisibile nelle SERP (DA bassa) |

---

## 4. REQUISITI GOOGLE — AGGIORNATI MARZO 2026

### 4.1 Core Web Vitals — Soglie 2026
| Metrica | Buono | Da migliorare | Scarso |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s (target competitivo: <2s) | 2.5s - 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| **SVT** (Smooth Visual Transitions) | Penalizza caricamenti "scattosi" |
| **VSI** (Visual Stability Index) | Stabilita' layout per tutta la sessione (session-scoped, non solo page load) |
| **ER** (Engagement Reliability) | Affidabilita' interazioni (click, form, menu) su tutti i device |

### 4.2 E-E-A-T — Segnali di Fiducia (Cruciale nel 2026)

> Nel 2026, E-E-A-T e' il fattore piu' importante per ranking E per citazioni AI.
> Google e le AI penalizzano contenuti senza autore identificabile o senza prove di competenza.

**Cosa implementare per Righetto Immobiliare:**
- [ ] **Pagina autore** per Linda Righetto e Gino Capon con: bio dettagliata, qualifiche, anni esperienza, foto reale, link social professionali
- [ ] **Author bio visibile** su ogni articolo blog (nome, ruolo, foto, link a pagina autore)
- [ ] **Person schema** (Schema.org) su pagine autore con `jobTitle`, `worksFor`, `sameAs`
- [ ] **Chi siamo dettagliato:** storia brand, team, anni nel settore, case study clienti reali
- [ ] **Recensioni specifiche:** incoraggiare recensioni che menzionano quartiere/servizio specifico (valgono 10x le generiche per entity authority)
- [ ] **Coerenza brand cross-platform:** nome, bio, foto identici su sito, GBP, LinkedIn, Instagram, portali immobiliari

### 4.3 Fattori di Ranking 2026
1. **E-E-A-T** — Experience, Expertise, Authoritativeness, Trustworthiness (vedi sezione 4.2)
2. **Rilevanza semantica** — Risposta all'intento di ricerca (search intent > keyword volume)
3. **Core Web Vitals** — Performance come hard ranking factor (64% siti non passa le soglie)
4. **Mobile-first** — Google indicizza prima la versione mobile (72% utenti inizia da mobile)
5. **Dati strutturati** — Schema.org per rich snippets + GeoCoordinates per local SEO
6. **GEO** — Ottimizzazione per citazioni AI (Gemini, ChatGPT, Perplexity)
7. **AEO** — Ottimizzazione per featured snippets e risposte dirette
8. **Topical Authority** — Copertura complessiva di un topic, non singole pagine
9. **Local Relevance** — Comunicare chiaramente zona e area servizi
10. **Page Experience Consistency** — Performance omogenea su tutte le pagine (no home veloce + blog lento)

### 4.4 Novita' Google Marzo 2026
- **March 2026 Core Update** — Rollout dal 7 marzo, ~2 settimane
- **Performance = hard ranking factor** — Siti che non passano soglie vedono cali misurabili
- **Engagement Reliability** — Nuova metrica CWV
- **SVT e VSI** — Nuove metriche stabilita' visiva
- **LCP target piu' severo** — Competitivo sotto 2s
- **AI Mode data** contato in Performance Report di Search Console
- **Google review policies aggiornate** — Rischio perdita recensioni
- **Ranking volatility estrema** — Cali 20-35% riportati da molti siti

### 4.5 GEO — Generative Engine Optimization

> Il 58% dei consumatori nel 2026 usa AI al posto dei motori tradizionali.
> ChatGPT 800M utenti/settimana, Gemini 750M/mese.
> GEO converte 4.4x vs SEO tradizionale ($3.71 return per $1).

**Regole GEO per ogni contenuto:**
1. **Frasi dichiarative** nelle prime 2 righe di ogni sezione — le AI estraggono da li'
2. **Dati numerici specifici** e verificabili (prezzi/mq, anni esperienza, N. immobili)
3. **Formato:** Domanda H2 → Risposta diretta (40-60 parole) → Approfondimento
4. **Liste, tabelle, definizioni chiare** — formato preferito dalle AI
5. **Citare fonti ufficiali** (Agenzia Entrate, OMI, FIAIP)
6. **Frasi auto-contenute** — ogni claim deve avere senso letto isolatamente
7. **Freshness** — aggiornare contenuti cornerstone regolarmente con timestamp "Ultimo aggiornamento"
8. **llms.txt** — mantenere aggiornato per guidare AI bots

**Regole AEO per featured snippet:**
1. Risposta 40-60 parole come primo paragrafo dopo ogni H2
2. Formato: "[Keyword] e' [definizione/risposta]"
3. Min 5 FAQ con Schema FAQPage per pagina
4. Tabelle comparative per dati numerici

### 4.6 Schema Markup — Best Practice 2026

**Tipo corretto:** Usare `RealEstateAgent` (sottotipo di `LocalBusiness`), MAI il generico `LocalBusiness` da solo. Piu' il tipo e' specifico, piu' chiaro il segnale a Google e AI.

**Formato:** JSON-LD (preferito da Google, piu' pulito, non interferisce con HTML).

**Layering schema multipli** per massima copertura:
- `RealEstateAgent` — su ogni pagina (identita' agenzia)
- `FAQPage` — su pagine con FAQ (rich snippet)
- `BreadcrumbList` — su tutte le pagine (navigazione strutturata)
- `Person` — sulle pagine agente (chi-siamo, landing-agente) per knowledge panel
- `RealEstateListing` — sulle pagine immobile
- `Review` — sulla homepage (testimonial reali)

**GeoCoordinates obbligatorio** su ogni schema RealEstateAgent:
```json
"geo": {
  "@type": "GeoCoordinates",
  "latitude": 45.476956,
  "longitude": 11.845762
},
"hasMap": "https://maps.google.com/?q=45.476956,11.845762"
```

**sameAs** — Aggiungere profili social nello schema per entity linking:
```json
"sameAs": [
  "https://www.instagram.com/righettoimmobiliare/",
  "https://www.facebook.com/righettoimmobiliare/",
  "https://www.linkedin.com/company/righettoimmobiliare/"
]
```

**Validazione:** Dopo ogni modifica schema, testare con:
- Google Rich Results Test (https://search.google.com/test/rich-results)
- Schema Markup Validator (https://validator.schema.org/)
- Google Search Console → Enhancements reports

---

## 5. VISUAL SALIENCY — Regole Above-the-Fold

> Il 57% del tempo di visualizzazione resta above the fold.
> Google misura questa esperienza tramite LCP, CLS, INP, SVT.

### 5.1 Regole Obbligatorie per Ogni Pagina

**LCP Element:**
- Hero image preloaded nel `<head>`: `<link rel="preload" href="..." as="image" fetchpriority="high">`
- MAI `loading="lazy"` su elementi above-the-fold
- WebP obbligatorio per immagini locali
- Animazioni LCP: partire in pausa, avviare dopo primo render

**Font Loading:**
- Preload font above-fold: Montserrat 400/700 + Cormorant Garamond 600/700
- `font-display: swap` su tutti i `@font-face`
- Self-hosted WOFF2 (no Google Fonts esterni = GDPR + velocita')

**CLS Prevention:**
- TUTTE le immagini con `width` + `height` espliciti
- Immagini JS: aggiungere `style="aspect-ratio:..."`
- Navbar fissa: usare `height` con CSS variable
- Mai contenuto asincrono above-the-fold senza placeholder dimensionato

**CTA Above-the-Fold:**
- UN solo CTA primario per hero (Hick's Law)
- Contrast ratio minimo 4.5:1 (WCAG AA)
- Hover: feedback visivo chiaro (`translateY(-2px)` + box-shadow)

**Critical CSS:**
- CSS hero/nav/above-fold: inline nel `<style>` del `<head>`
- CSS below-fold: caricare via `<link rel="stylesheet" media="print" onload="this.media='all'">`

### 5.2 Palette Colori CTA (Contrast-Safe)
| Elemento | Background | Testo | Ratio |
|----------|-----------|-------|-------|
| CTA primario | `var(--oro)` #B8D44A | `var(--nero)` #0A0F1C | 5.2:1 |
| CTA secondario | `var(--blu)` #2C4A6E | `white` | ~5:1 |
| CTA landing | `var(--fire)` arancione | `white` | ~4.5:1 |
| CTA valutazione | `var(--purple)` #6C63FF | `white` | ~4.5:1 |
| CTA landing-agente | `var(--mint)` #00E5A0 | `var(--nero)` | ~5.5:1 |

> **ATTENZIONE:** var(--oro) su sfondo chiaro (var(--bianco) #F7F5F1) ha ratio 1.54:1 — FAIL WCAG.
> Usare SOLO oro con testo scuro (var(--nero)), MAI su sfondo chiaro senza testo scuro.

---

## 6. STATO SERP E STRATEGIA COMPETITIVA

### 6.1 Stato SERP (verificato 7 marzo 2026)
| Keyword | Posizione | Chi appare |
|---|---|---|
| "agenzia immobiliare padova" | **NON APPARE** | Immobiliare.it, Tetto Rosso, RicercAttiva, Dove.it, RockAgent |
| "vendere casa padova agenzia" | **NON APPARE** | Pianeta Casa, Grimaldi, Dove.it, Tetto Rosso, RockAgent |
| "migliore agenzia immobiliare padova" | **NON APPARE** | Gruppo Bortoletti, SZ Affari, RockAgent, Dove.it |
| "comprare casa padova" | **NON APPARE** | Idealista, Immobiliare.it, Subito, Tecnocasa |
| "Righetto Immobiliare Padova" | **SI (brand)** | Idealista, Immobiliare.it, Casa.it, Wikicasa |

**Diagnosi:** SEO on-page top tra i locali, domain authority troppo bassa. Competitor nazionali (Dove.it, RockAgent) alzano l'asticella.

### 6.2 Confronto Competitor (aggiornato 7 marzo 2026)
| Feature | Righetto | Tetto Rosso | RicercAttiva | Pianeta Casa | Dove.it | RockAgent |
|---|---|---|---|---|---|---|
| FAQ Pages | **Si (top)** | Si | No | No | No | No |
| Blog/Content | **Si** | Si | **Si (top)** | Si | **Forte** | **Forte** |
| Schema.org | **Esteso (top)** | Buono | Buono | Base | Buono | Buono |
| Recensioni Google | ~127 | **~256** | Poche | ~104 | N/D | N/D |
| Chatbot AI | **Unico** | No | No | No | No | No |
| Simulatore mutuo | **Unico** | No | No | No | No | No |
| GEO/AEO | **Unico** | No | No | No | Parziale | No |
| Appare in SERP | **NO** | **SI** | **SI** | No | **SI** | **SI** |

### 6.3 Le 4 Priorita' Strategiche (Off-Site)

**PRIORITA' 1 — Google Business Profile (il singolo asset digitale piu' importante per lead locali)**

> GBP ora alimenta le risposte AI di Google, non solo Maps.
> Profili con foto aggiornate settimanalmente ricevono significativamente piu' interazioni.
> 87% consumatori legge recensioni online, 73% solo quelle dell'ultimo mese.

- [ ] **Categoria primaria:** "Agenzia Immobiliare" + secondarie: "Consulente Immobiliare", "Valutatore Immobiliare", "Gestione Immobili"
- [ ] **Descrizione 750 caratteri:** includere aree servite, specialita', keyword locali naturalmente
- [ ] Aggiungere TUTTI i servizi nel GBP: vendita, acquisto, affitto, valutazione, gestione, virtual tour
- [ ] **Google Posts OGNI SETTIMANA** (nuovi immobili, articoli blog, offerte) — profili attivi settimanalmente hanno visibilita' maggiore
- [ ] **Foto settimanali** — 5+ interni ufficio, 3+ esterni, foto team reali (MAI stock), 10+ esempi immobili
- [ ] Compilare Q&A del profilo GBP (le stesse FAQ del sito)
- [ ] Verificare attributi completi (orari, accessibilita', servizi, parcheggio)
- [ ] **UTM tags** sul link al sito per tracciare traffico GBP in GA4
- [ ] **Embed Google Map** con NAP visibile sul sito (gia' presente in contatti, verificare allineamento)

**PRIORITA' 2 — Recensioni Google (gap critico: 127 vs 256 Tetto Rosso)**
- [ ] WhatsApp post-rogito con link diretto a Google Review
- [ ] Obiettivo: +30 recensioni/anno
- [ ] Script: "Gentile [nome], grazie per aver scelto Righetto Immobiliare! Se il nostro servizio ti ha soddisfatto, ci farebbe piacere una tua recensione su Google: [link]. Ci aiuta molto!"
- [ ] MAI recensioni false — penalita' = rimozione TUTTE + sospensione GBP + multa AGCM

**PRIORITA' 3 — Backlink Locali (Domain Authority)**
- [ ] PadovaOggi / IlGazzettino come fonte esperta
- [ ] Comunicati stampa su quotidiani locali
- [ ] Collaborazioni geometri, notai, architetti (scambio link)
- [ ] Directory locali: PagineGialle, Yelp, Cylex, TuttoCitta
- [ ] Profilo LinkedIn aziendale con contenuti regolari
- [ ] Profilo FIAIP / FIMAA con link al sito
- [ ] Guest post su blog immobiliari nazionali
- [ ] Camera di Commercio di Padova — registrazione con link

**PRIORITA' 4 — Citazioni NAP Consistenti**
- [ ] Nome/Indirizzo/Telefono IDENTICO ovunque
- [ ] Formato: "Righetto Immobiliare"
- [ ] Indirizzo: Via Roma 96, 35010 Limena PD
- [ ] Telefono: 049 884 3484

### 6.4 Lezioni dai Competitor
| Competitor | Lezione | Azione |
|---|---|---|
| Tetto Rosso | 256 recensioni, processo sistematico | Implementare processo post-rogito |
| RicercAttiva | Blog aggressivo su temi fiscali/legali | Scrivere articoli su successioni, tasse, agevolazioni |
| venderecasapadova.it | Dominio exact-match, funnel diretto | landing-vendere-casa-padova.html gia' creata |
| Pianeta Casa | Widget Google Reviews reale nel sito | Embed reale da implementare |
| Grimaldi | Magazine mensile, freshness signals | Min 2 articoli blog/mese |
| Engel & Volkers | Instagram forte (826 follower) | Rafforzare Instagram con reels e storie |
| Tempocasa | "Immobile Certificato" | Creare bollino "Verificato Righetto" |

---

## 7. CONTENUTI — Topic Cluster e Stato Avanzamento

### 7.1 Cluster "Vendere Casa Padova"
- [x] servizio-vendita.html (FAQ + FAQPage schema)
- [x] blog-costi-vendere-casa-padova-2026.html
- [x] landing-vendere-casa-padova.html
- [x] blog-documenti-vendita-casa.html
- [x] blog-tasse-vendita-casa.html
- [x] blog-tempi-vendita-casa-padova.html
- **CLUSTER COMPLETO**

### 7.2 Cluster "Comprare Casa Padova"
- [x] blog-comprare-casa-padova-guida-2026.html
- [x] blog-mutuo-prima-casa-padova.html
- [x] blog-agevolazioni-prima-casa-2026.html
- [x] blog-successione-immobiliare-padova.html
- [x] blog-investire-immobiliare-padova.html
- **CLUSTER COMPLETO**

### 7.3 Cluster "Quartieri Padova"
- [x] blog-quartieri-padova-2026.html
- [x] 12 pagine zona-*.html (incluse zona-limena, zona-vigonza, zona-abano-terme, zona-selvazzano)
- [x] agenzia-immobiliare-padova.html (pillar)
- **CLUSTER COMPLETO**

### 7.4 Cluster "Affitto Padova"
- [x] blog-affitto-studenti-padova.html
- [x] servizio-locazioni.html
- [x] blog-contratto-affitto-padova.html
- [x] blog-rendimento-affitto-padova.html
- **CLUSTER COMPLETO**

---

## 8. AZIONI TECNICHE — TODO

### 8.1 Bug e Fix Immediati — COMPLETATI 8 Marzo 2026
- [x] **immobile.html in sitemap** — gia' presente (verificato)
- [x] **cormorant-garamond-600.woff2** — 7 file blog hanno preload 600, altri usano 700 correttamente
- [x] **landing-vendita.html lazy** — immagini sono below-fold, loading="lazy" corretto
- [x] **Discrepanza articoli** — allineati: homepage.js +2, admin.html +10 articoli
- [x] **Contrasto oro** — corretti 8 punti in admin.html (color:#fff → color:var(--nero))
- [x] **robots.txt AI bots** — aggiunti GPTBot, ClaudeBot, Google-Extended, PerplexityBot + Allow chatbot.js
- [x] **sameAs mancante** — aggiunto RealEstateAgent schema con sameAs a faq.html
- [x] **Person schema** — aggiunto a landing-agente.html
- [x] **Timestamp cornerstone** — aggiunto "Aggiornato: marzo 2026" a 6 articoli principali
- [x] **llms.txt** — aggiornato con nuove zone e articoli

### 8.2 Contenuti da Creare
- [x] blog-tempi-vendita-casa-padova.html — CREATO 8 marzo 2026
- [x] zona-vigonza.html — CREATA 8 marzo 2026
- [x] zona-abano-terme.html — CREATA 8 marzo 2026
- [x] zona-selvazzano.html — CREATA 8 marzo 2026
- [ ] Bollino "Verificato Righetto" — brand quality sugli annunci

### 8.3 Ottimizzazioni Performance
- [ ] LCP sotto 2 secondi su tutte le pagine (nuovo target competitivo)
- [ ] Verificare SVT — nessun caricamento "scattoso" (font swap, image pop-in)
- [ ] Verificare Engagement Reliability — form, bottoni, menu funzionano su tutti i device
- [ ] Page Experience consistency — tutte le pagine devono avere performance simile

### 8.4 SEO Tecnico
- [ ] **Contenuti unici vs portali** — le descrizioni immobili su Idealista/Immobiliare.it DEVONO essere diverse da quelle sul sito (rischio duplicate content e deindexing)
- [ ] Internal linking tra blog posts e zone pages (cross-link contestuali)
- [ ] Verificare indexing in Google Search Console
- [ ] Richiedere indicizzazione manuale nuove pagine via GSC
- [ ] Verificare che recensioni Google non siano sparite (nuove policies)
- [ ] Aggiungere video content (virtual tour, presentazione agenzia) — genera 66% piu' lead
- [ ] UTM tags su link GBP per tracciare traffico in GA4

### 8.5 Conversione e Lead Generation
- [ ] **Speed-to-lead:** risposta automatica entro 60 secondi (47-59% dei clienti sceglie il primo agente che risponde)
- [ ] **A/B test CTA:** testare copy diversi (es. "Valutazione Gratuita" vs "Scopri il Valore della Tua Casa")
- [ ] **Lead magnet segmentati:** CTA diversi per acquirenti (simulatore mutuo) e venditori (valutazione gratuita)
- [ ] **Video testimonial:** aggiungere video recensioni reali (piu' engaging del solo testo)
- [ ] **Siti <2s convertono 3x** meglio dei siti lenti — priorita' LCP

### 8.6 GEO/AEO — COMPLETATI 8 Marzo 2026
- [x] **llms.txt aggiornato** — aggiunte nuove zone (Vigonza, Abano, Selvazzano) e prezzi
- [x] **robots.txt AI bots** — GPTBot, ClaudeBot, Google-Extended, PerplexityBot tutti Allow + chatbot.js Allow
- [ ] Assicurare che contenuti importanti NON siano dietro JS client-side (le AI estraggono HTML statico)
- [x] **Timestamp "Ultimo aggiornamento"** — aggiunto a 6 articoli cornerstone
- [x] **sameAs** — presente su tutte le pagine principali (47/48), faq.html corretto
- [x] **BreadcrumbList** — presente su 48 pagine (tutte tranne index.html che non lo richiede)
- [x] **Person schema** — presente su chi-siamo.html e landing-agente.html

---

## 9. KPI E CALENDARIO

### 9.1 KPI da Monitorare
| Metrica | Attuale | Obiettivo 3 mesi | Obiettivo 6 mesi |
|---|---|---|---|
| Recensioni Google | ~127 | 140+ | 160+ |
| "agenzia immobiliare padova" | >100 | Top 30 | Top 10 |
| "vendere casa padova" | >100 | Top 50 | Top 20 |
| Traffico organico | ? (GSC) | +30% | +80% |
| Pagine indicizzate | ~50 | 55+ | 65+ |
| Backlink domini unici | ? | +10 | +25 |
| Citazioni AI (GEO) | ? | Monitorare | Brand awareness AI |

### 9.2 Calendario Editoriale
| Mese | Contenuto | Keyword target | Stato |
|---|---|---|---|
| Marzo 2026 | blog-tempi-vendita-casa-padova.html | "quanto tempo vendere casa padova" | **FATTO** |
| Marzo 2026 | zona-vigonza.html | "case vigonza", "immobiliare vigonza" | **FATTO** (anticipato) |
| Marzo 2026 | zona-abano-terme.html | "case abano terme" | **FATTO** (anticipato) |
| Marzo 2026 | zona-selvazzano.html | "case selvazzano dentro" | **FATTO** (anticipato) |
| Aprile 2026 | Video presentazione agenzia | Brand awareness + engagement | TODO |
| Maggio 2026 | Articoli fiscali (IMU, bonus) | Long-tail fiscale | TODO |
| Giugno 2026 | Bollino "Verificato Righetto" | Brand quality | TODO |

### 9.3 Routine di Monitoraggio
- **Settimanale:** Performance report in Search Console + Google Posts
- **Mensile:** Audit metriche SEO + Core Web Vitals + citazioni AI
- **Trimestrale:** Audit completo contenuti + struttura + competitor
- **Ad ogni Google Update:** Verificare impatto sul sito

---

## 10. GESTIONE cPanel

### 10.1 Da Eliminare (per liberare spazio)
| File/Cartella | Dimensione | Motivo |
|---|---|---|
| `backup-3.2.2026_10-53-22_wyrighet.tar.gz` | **37.04 GB** | Backup gia' scaricato in locale |
| `public_htmlcopia140422.zip` | **11.37 GB** | Backup WordPress 2022 — obsoleto |
| `error_log*` / `error_log_php*` | variabile | Log errori vecchi |
| `sp_mysql_bk/` | variabile | Backup MySQL WordPress — non serve |
| `public_html/` contenuto | variabile | Vecchio sito WordPress |
| Database MySQL | variabile | Database WordPress non necessari |

### 10.2 Da Tenere Assolutamente
- Record DNS (A, CNAME, MX)
- Dominio registrato
- Account email attivi
- Certificato SSL
- Cartelle: `mail/`, `etc/`, `ssl/`, `cache/`, `logs/`, `tmp/`

---

## 11. CHECKLIST RAPIDE

### Per Ogni Nuova Pagina
- [ ] Title tag unico (max 60 char) + Meta description (max 160 char)
- [ ] H1 unico + Alt text su tutte le immagini
- [ ] Schema.org (RealEstateAgent + GeoCoordinates + FAQPage + BreadcrumbList + sameAs social)
- [ ] Open Graph tags + Canonical URL
- [ ] Hero image preloaded + font above-fold preloaded
- [ ] Nessun `loading="lazy"` above-the-fold
- [ ] CTA primario con contrast >= 4.5:1 (MAI var(--oro) con color:#fff)
- [ ] Critical CSS inline, rest deferred
- [ ] Link interni verso pagine correlate
- [ ] Registrato in sitemap.xml
- [ ] Frasi dichiarative prime 2 righe (GEO)
- [ ] Dati numerici specifici (GEO)
- [ ] Min 5 FAQ con Schema FAQPage (AEO)
- [ ] Author bio visibile con link a pagina autore (E-E-A-T)

### Per Ogni Nuovo Articolo Blog
- [ ] Tutti i punti sopra
- [ ] Registrato in TUTTI e 4: admin.html, blog.html, homepage.js, sitemap.xml
- [ ] Cross-link con zone pages e service pages correlate
- [ ] Timestamp "Ultimo aggiornamento" visibile

### Per Ogni Nuova Zona Page
- [ ] Tutti i punti "Per Ogni Nuova Pagina"
- [ ] Schema Place con GeoCoordinates + sameAs
- [ ] Schema RealEstateAgent con aggregateRating
- [ ] Registrato in blog.html (array articoliStatici con categoria "Mercato locale")
- [ ] Registrato in sitemap.xml
- [ ] Aggiornato llms.txt con nuova zona e prezzi
- [ ] Aggiunto link nel footer di tutte le zone pages

### Verifiche Post-Modifica (AUTOMATICHE via pre-commit hook)
- `node scripts/validate-page.js --staged` — valida automaticamente
- Schema mancante = commit BLOCCATO
- Title mancante = commit BLOCCATO
- Meta description troppo lunga = WARNING (passa)

### Verifiche Manuali Periodiche
- [ ] Contrasto WCAG: mai var(--oro) come bg con testo bianco (ratio 1.54:1 = FAIL)
- [ ] Allineamento array: blog.html, homepage.js, admin.html devono avere gli stessi articoli
- [ ] robots.txt: AI bots (GPTBot, ClaudeBot, Google-Extended, PerplexityBot) NON bloccati
- [ ] llms.txt: aggiornato con nuovi contenuti e prezzi
- [ ] Timestamp cornerstone: aggiornare ogni mese

---

## 12. CHANGELOG

### v1.5 - 8 Marzo 2026 (Implementazione Completa TODO)
- **CREATI 4 contenuti:** blog-tempi-vendita-casa-padova, zona-vigonza, zona-abano-terme, zona-selvazzano
- **RISOLTI tutti i 5 bug** sezione 8.1 (sitemap, font, lazy, discrepanza articoli, contrasto oro)
- **Completati 7 fix GEO/AEO:** robots.txt AI bots, llms.txt, sameAs faq.html, Person schema landing-agente, timestamp cornerstone, BreadcrumbList verificato
- **Allineati array articoli** su blog.html, homepage.js, admin.html (ora tutti sincronizzati)
- **CLAUDE.md creato** per attivazione automatica skill su ogni sessione Claude
- **Checklist nuova zona page** aggiunta alle checklist rapide
- **Verifiche manuali periodiche** aggiunte come sezione permanente
- **Calendario editoriale aggiornato** — tutti i contenuti marzo anticipati e completati
- **Punteggio sito aggiornato** — 4 cluster ora completi su 4

### v1.4 - 8 Marzo 2026 (Loop 4 — Verifica Finale)
- Fix numerazione sezioni duplicate (due 4.3 → ora 4.2-4.6 corrette)
- Aggiunta nota su contenuti unici vs portali (rischio duplicate content Idealista/Immobiliare.it)
- Aggiunta statistica: 64% siti non passa soglie CWV
- Raffinata priorita' search intent > keyword volume nei fattori di ranking
- Verifica coerenza strutturale documento completa

### v1.3 - 8 Marzo 2026 (Loop 3 — E-E-A-T e Entity Authority)
- Aggiunta sezione 4.2 E-E-A-T completa con checklist implementativa
- Aggiunti: pagina autore, author bio su blog, Person schema, coerenza brand cross-platform
- Aggiunta nota su recensioni specifiche (quartiere/servizio) per entity authority
- Author bio aggiunta nella checklist rapida per ogni nuova pagina

### v1.2 - 8 Marzo 2026 (Loop 2 — GBP, Conversione, Lead Generation)
- GBP sezione ampliata: descrizione 750 char, categorie specifiche, foto per tipo, UTM tags
- Aggiunto dato: 87% consumatori legge recensioni, 73% solo ultimo mese
- Aggiunta sezione 8.5 Conversione e Lead Generation (speed-to-lead, A/B test, lead magnet segmentati, video testimonial)
- UTM tags per tracciamento GBP in GA4

### v1.1 - 8 Marzo 2026 (Loop 1 — Schema, llms.txt, AI Crawlers)
- Schema sezione riscritta: layering multiplo (RealEstateAgent + FAQPage + BreadcrumbList + Person + Review)
- Aggiunto sameAs per entity linking (profili social nello schema)
- Aggiunti tool validazione: Rich Results Test, Schema Markup Validator
- llms.txt contestualizzato: adozione <0.005% ma zero costo, futuro standard
- Aggiunta verifica robots.txt per AI bots (GPTBot, ClaudeBot, Google-Extended)
- Aggiunti TODO: BreadcrumbList su tutte le pagine, Person schema su chi-siamo e landing-agente

### v1.0 - 8 Marzo 2026 (Creazione Skill Unificata)
- **Fusione** di SERP-STRATEGY.md e SKILL-KILLER.md in documento unico
- **Eliminata ridondanza:** stato SERP, competitor, strategie, calendario — tutto in un unico punto
- **Aggiornato stato reale** del progetto con audit 8 marzo
- **SERP-STRATEGY.md era parzialmente obsoleto:** molti TODO gia' completati
- **SKILL-KILLER.md aveva duplicazioni interne:** sezione competitor ripetuta, checklist ridondanti
- **Aggiunti nuovi insight 2026 dal web** (10+ fonti consultate)
- **Identificati 5 bug reali** nel progetto
- **Struttura razionalizzata:** da 874 righe (2 file) a 1 file organizzato senza ripetizioni

---

*Skill Unificata — Un solo documento per governarli tutti.*
