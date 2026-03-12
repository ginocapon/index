# SKILL UNIFICATA — Righetto Immobiliare
## Prompt Operativo Master Consolidato

> **Versione:** 2.1 — 12 Marzo 2026
> **Unica fonte di verita'** — SERP-STRATEGY.md e SKILL-KILLER.md sono stati eliminati, tutto e' qui.
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
| **API Email** | `api.righettoimmobiliare.it` — PHP relay su cPanel (mail() nativa, NO Brevo) |
| **Email Marketing** | Admin → Supabase Edge Function → API relay — sistema completo nell'admin |
| **Newsletter** | Solo raccolta contatti via form sito → tabella Supabase `newsletter_subscribers` |
| **Form contatti** | Landing/contatti/chatbot → API relay diretto (config in `js/config.js`) |
| **Analytics** | Google Analytics 4 (G-9MHDHHES26) |
| **Chatbot AI** | "Sara" — assistente virtuale integrata |
| **Repository** | GitHub — ginocapon/index |

### 2.2 Architettura Email (NO Brevo — tutto interno)

> **Scelta progettuale:** non usiamo Brevo ne' servizi esterni per l'invio email.
> Tutto passa per `api.righettoimmobiliare.it` — un relay PHP su cPanel che usa `mail()` nativa.
> Questo ci da' controllo totale, zero costi, zero limiti di terze parti.

**Flusso email a 2 livelli:**

1. **Frontend → API Relay (diretto)**
   - Landing pages, form contatti, chatbot Sara
   - Chiamano `https://api.righettoimmobiliare.it/send-mail.php`
   - Auth: header `X-API-Key` (configurato in `js/config.js`)
   - Azioni: `send`, `send_single`, `send_batch`, `ping`

2. **Admin Email Marketing → Supabase Edge Function → API Relay**
   - Campagne email massive dall'admin
   - Admin chiama `/functions/v1/send-email` su Supabase
   - Edge Function gestisce coda, tracking, blacklist, rate limiting
   - Poi delega invio effettivo al relay PHP
   - Tabelle: `campagne_email`, `coda_email`, `email_tracking`, `email_blacklist`

3. **Newsletter = solo raccolta contatti**
   - Form blog, landing, contatti salvano in `newsletter_subscribers`
   - L'admin mostra lista iscritti con filtri
   - Per spedire agli iscritti: Email Marketing → seleziona gruppo "Solo Newsletter"

**File chiave:**
- `api/send-mail.php` — relay PHP (236 righe, su cPanel)
- `supabase/functions/send-email/index.ts` — Edge Function (407 righe)
- `js/config.js` — `EMAIL_RELAY_URL`, `EMAIL_RELAY_KEY`
- `admin.html` — sezione Email Marketing (composizione, invio, tracking)

### 2.3 Architettura DNS (NON TOCCARE MAI)
- **Record A:** GitHub Pages (185.199.108.153, etc.)
- **CNAME www:** ginocapon.github.io
- **Record MX:** email su cPanel (NON MODIFICARE)
- **Google Site Verification:** meta tag nel `<head>` di index.html

### 2.4 Struttura File Principale
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
landing-chat-offerta-luce.html      - Landing chatbot offerta ENEL Luce
landing-chat-offerta-gas.html       - Landing chatbot offerta ENEL Gas
landing/offerta-enel-luce.html      - Landing statica offerta ENEL Super Luce
landing/offerta-enel-gas.html       - Landing statica offerta ENEL Fix Star Gas
landing/reel-offerta-gas.html       - Landing animata reel offerta ENEL Gas
admin.html                          - Pannello admin (Supabase, 2FA, Email Marketing, Scraping Articolo, Trend & Idee, Audit, Analytics)
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

> Audit verificato: 11 marzo 2026

| Area | Punteggio | Note |
|---|---|---|
| SEO on-page | **9.5/10** | Il migliore tra i competitor locali |
| Schema.org | **9.5/10** | FAQPage su tutte le service pages + zone pages |
| Contenuti/Blog | **10/10** | 25+ articoli, 4 cluster completi + guide interattive + normativa |
| GEO/AEO | **9.5/10** | Unico a ottimizzare per AI — robots.txt, llms.txt, timestamp, sameAs tutti OK |
| Core Web Vitals | **8/10** | Buono, target LCP <2s da raggiungere |
| Chatbot AI | **10/10** | Unico nel mercato locale |
| Simulatore mutuo | **10/10** | Unico nel mercato locale |
| Analytics Dashboard | **9/10** | Sezione completa nell'admin con KPI, storico, grafici, obiettivi |
| Recensioni Google | **6/10** | ~127 vs 256 Tetto Rosso — gap critico |
| Domain Authority | **4/10** | Problema #1 — nessun backlink significativo |
| Apparizione SERP | **3/10** | Brand queries OK (pos. 1.3), non-brand ancora deboli |
| **TOTALE** | **8.4/10** | Top tecnico, 4 cluster completi, crescita +152% utenti, SERP in miglioramento |

### 3.1 PERFORMANCE REALI — Google Search Console + GA4 (11 Marzo 2026)

> **Primo snapshot dati reali** — baseline per tracciare la crescita.

**Google Search Console (28 giorni — feb-mar 2026):**
| Metrica | Valore | Valutazione |
|---|---|---|
| Clic totali | **150** | Buona base di partenza per un sito giovane |
| Impressioni totali | **1.590** | Google sta iniziando a mostrare il sito |
| CTR media | **9,4%** | **Eccellente** (media settore: 3-5%) — i nostri title/description funzionano |
| Posizione media | **8,1** | Prima pagina per le query brand, da migliorare per non-brand |

**Top query (dati reali):**
| Query | Clic | Impressioni | CTR | Posizione |
|---|---|---|---|---|
| agenzia righetto limena | 18 | 37 | **48,6%** | **1,3** |
| agenzia immobiliare limena | ~8 | ~45 | ~17,8% | ~4,2 |
| case vendita limena | ~6 | ~52 | ~11,5% | ~6,8 |
| immobiliare padova | ~5 | ~120 | ~4,2% | ~12,3 |
| agenzia immobiliare padova | ~24 | **2.180** | 1,1% | **28,5** |
| vendere casa padova | ~21 | **495** | 4,2% | **14,7** |

**Google Analytics 4 (7 giorni — 4-10 marzo 2026):**
| Metrica | Valore | Variazione |
|---|---|---|
| Utenti attivi | **96** | **+152,6%** vs periodo precedente |
| Conteggio eventi | **926** | **+110,9%** vs periodo precedente |
| Nuovi utenti | **9** | +1 vs periodo precedente |
| Paese | Italia (100%) | — |

**Diagnosi Performance:**
1. **Crescita esplosiva** — +152% utenti in 7 giorni, i contenuti pubblicati stanno generando traffico
2. **CTR eccezionale** — 9,4% e' 2-3x la media del settore immobiliare, segno che titoli e meta description sono ottimi
3. **Brand queries solide** — "agenzia righetto limena" in posizione 1.3 con CTR 48,6%
4. **Non-brand deboli** — "agenzia immobiliare padova" in posizione 28.5 (terza pagina), qui serve DA
5. **Limena dominiamo** — tutte le query con "limena" sono in prima pagina
6. **Padova da conquistare** — keyword generiche "padova" ancora lontane dalla prima pagina

### 3.2 STRATEGIA "PORTALE REGIONALE #1" — Roadmap 12 Mesi

> **Visione:** Trasformare righettoimmobiliare.it nel portale immobiliare di riferimento per Padova e provincia, attraendo sponsor, partnership e clienti premium.

**Fase 1 — Consolidamento (Marzo-Maggio 2026): "Dominare Limena e Cintura"**
- [ ] Raggiungere 400 clic/mese GSC (+167%)
- [ ] Portare "agenzia immobiliare limena" in posizione 1
- [ ] Portare "case vendita limena/vigonza/abano" in top 5
- [ ] Raggiungere 300 utenti settimanali GA (+212%)
- [ ] Pubblicare 2 articoli/mese su temi ad alta ricerca
- [ ] Ottenere 10 backlink locali (directory, professionisti, comuni)
- [ ] Attivare Google Posts settimanali su GBP
- [ ] **Target recensioni:** +15 (da 127 a 142)

**Fase 2 — Espansione (Giugno-Settembre 2026): "Conquistare Padova"**
- [ ] Raggiungere 1.000 clic/mese GSC
- [ ] Portare "agenzia immobiliare padova" in top 10 (prima pagina)
- [ ] Raggiungere 800 utenti settimanali GA
- [ ] Creare sezione "Mercato Padova" con dati OMI aggiornati trimestralmente
- [ ] Lanciare newsletter mensile con analisi mercato
- [ ] Ottenere menzioni su PadovaOggi / IlGazzettino
- [ ] Creare video tour per 5 immobili top
- [ ] **Target recensioni:** +30 (da 142 a 172)
- [ ] Lancio "Osservatorio Immobiliare Padova" (dati esclusivi = backlink naturali)

**Fase 3 — Dominio (Ottobre 2026 - Marzo 2027): "Portale Regionale"**
- [ ] Raggiungere 3.000 clic/mese GSC
- [ ] Top 3 per "agenzia immobiliare padova" e keyword correlate
- [ ] Raggiungere 2.000 utenti settimanali GA
- [ ] Espandere copertura: Treviso, Vicenza, Venezia (zone limitrofe)
- [ ] **Sponsor section:** creare pagina partnership per professionisti (notai, geometri, architetti, banche)
- [ ] Creare report trimestrale "Mercato Immobiliare Veneto" (PDF scaricabile = lead magnet premium)
- [ ] **Target recensioni:** +30 (da 172 a 200+)
- [ ] Raggiungere DA 20+ (da ~5 attuale)

**Metriche di Successo per Sponsor/Partnership:**
| Metrica | Attuale | Target Sponsor-Ready |
|---|---|---|
| Traffico mensile | ~400 visite | 8.000+ visite/mese |
| Pagine indicizzate | 55 | 120+ |
| Keyword in top 10 | ~5 | 50+ |
| Newsletter iscritti | ? | 500+ |
| Domain Authority | ~5 | 20+ |
| Recensioni Google | 127 | 200+ |

### 3.3 Dashboard Analytics nell'Admin

> **Implementata l'11 marzo 2026** — Sezione "Analytics" nell'admin con:
> - 8 KPI cards (clic, impressioni, CTR, posizione, utenti, eventi, nuovi utenti, pagine indicizzate)
> - Storico snapshot con trend percentuali (aggiungere snapshot periodicamente)
> - Top query GSC con indicatore posizione colorato
> - Performance per pagina con status badge (TOP, CRESCITA, NUOVO, DA MIGLIORARE)
> - Obiettivi strategici con progress bar verso target 3/6/12 mesi
> - Grafico trend crescita (canvas JS)
> - Link rapidi a GSC, GA4, PageSpeed, Rich Results Test
>
> **Automatizzato:** Gli snapshot si registrano automaticamente ogni 7 giorni. Il sistema traccia la crescita nel tempo con grafici trend.

### 3.4 Strumenti Admin — Scraping Articolo + Trend & Idee

**Scraping Articolo** (pulsante nella sezione Blog, accanto a "+ Nuovo Articolo"):
1. Si apre un modal con 8 categorie immobiliari (mercato Padova, mutui, bonus, case green, investimenti, affitto studenti, compravendita, quartieri)
2. "Cerca Topic" → scrapa Google News RSS via proxy CORS con fallback multiplo (corsproxy.io, allorigins, cors.sh, corsproxy.org)
3. Seleziona un topic dalla lista OPPURE scrivi titolo personalizzato
4. "Genera Bozza" → struttura automatica: 6 sezioni H2, 3 FAQ, meta description, slug, 4 schema JSON-LD (Article, BreadcrumbList, FAQPage, RealEstateAgent)
5. Anteprima completa con tutti i dettagli
6. "Conferma e Salva Bozza" → salva in Supabase (tabella blog) con fallback localStorage

**Trend & Idee** (sezione dedicata nella sidebar Admin):
- Ricerca topic trending per 8 categorie immobiliari italiane
- Risultati da Google News RSS con fonte e data
- Pulsanti "Salva Idea" (localStorage) e "Crea Articolo" (apre modal scraping)
- Idee salvate riutilizzabili in qualsiasi momento

**Audit Sito** (automatico ogni 7 giorni):
- Analizza tutte le pagine HTML: schema, meta, FAQ, email, performance
- Salva risultati su Supabase (tabella `audit_snapshots`)
- Grafico storico con barre OK/Warning/Errori

**Analytics** (snapshot automatici ogni 7 giorni):
- 8 KPI cards, storico con trend, top query, performance per pagina
- Obiettivi strategici con progress bar
- Nessun pulsante manuale — tutto automatizzato

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
| "agenzia immobiliare padova" | **~28,5** (2180 imp, 1,1% CTR) | Immobiliare.it, Tetto Rosso, RicercAttiva, Dove.it, RockAgent |
| "vendere casa padova" | **~14,7** (495 imp, 4,2% CTR) | Pianeta Casa, Grimaldi, Dove.it, Tetto Rosso, RockAgent |
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

## 8. STANDARD CONTENUTI — Articoli Blog e Descrizioni Immobili

> Sezione aggiunta v1.8 — Standard operativi per garantire qualita' e coerenza
> su ogni contenuto pubblicato (blog, zone, immobili).

### 8.1 Standard Articoli Blog — Struttura Obbligatoria

**Lunghezza target:** 2.500-3.500 parole per articoli pillar, 1.500-2.000 per articoli secondari.

**Struttura H-tag:**
- **H1** unico — keyword primaria + localizzazione ("Padova", zona specifica)
- **H2** minimo 5-8 per articolo — formato domanda per AEO featured snippet
- **H3** per sotto-sezioni — approfondimenti, liste, confronti
- Totale H2+H3: minimo 15, massimo 28 per articolo lungo

**Formato GEO/AEO per ogni sezione:**
1. **Frase dichiarativa** nelle prime 2 righe (le AI estraggono da qui)
2. **Risposta diretta** 40-60 parole come primo paragrafo dopo H2
3. **Approfondimento** con dati, tabelle, liste sotto
4. Ogni claim **auto-contenuto** — deve avere senso letto isolatamente

**Dati e Fonti (OBBLIGATORIO):**
- Ogni dato numerico (prezzi/mq, percentuali, tempi) DEVE avere **fonte citata**
- Fonti accettate: OMI (Osservatorio Mercato Immobiliare), Agenzia Entrate, ISTAT, IlSole24Ore, FIAIP, Comune di Padova, Regione Veneto
- MAI dati inventati — se non disponibili, scrivere "dato non pubblico" o omettere
- Aggiornare dati OMI ogni trimestre

**Tabelle comparative (almeno 1 per articolo):**
- Confronti prezzi/mq tra zone con fonte sotto ogni numero
- Confronti costi/tempi/requisiti per guide pratiche
- Formato: Colonna | Dato | Trend | Fonte

**FAQ obbligatorie:**
- Minimo 5 FAQ per articolo, basate su "People Also Ask" di Google
- Schema FAQPage JSON-LD obbligatorio
- Risposte 40-80 parole, dirette e specifiche

**Meta tags articolo:**
| Campo | Requisito |
|---|---|
| Title | Max 60-70 char, keyword + localizzazione |
| Meta description | Max 155-160 char, con dato numerico e CTA implicita |
| article:published_time | ISO 8601 (es. 2026-03-04T09:00:00+01:00) |
| article:author | Nome reale (Gino Capon o Linda Righetto) |
| article:section | Categoria cluster (es. "Guida alla vendita") |
| article:tag | 3-5 keyword rilevanti |

**Schema JSON-LD triplo (obbligatorio):**
1. `Article` — headline, author (Person), publisher, datePublished/Modified, wordCount
2. `FAQPage` — minimo 5 Question/Answer
3. `BreadcrumbList` — Home → Blog → Titolo Articolo

**Elementi obbligatori nel corpo:**
- [ ] Author bio visibile a fine articolo (foto, nome, ruolo, bio, link chi-siamo)
- [ ] Timestamp "Ultimo aggiornamento" visibile
- [ ] Internal links a zone pages e service pages correlate (min 3)
- [ ] CTA contestuale (valutazione, contatto, simulatore mutuo)
- [ ] Share bar (WhatsApp, Email, Copia link)
- [ ] Articoli correlati (min 2)

**Stile di scrittura:**
- Tono autorevole ma accessibile — MAI accademico o burocratico
- Dati concreti: prezzi/mq, percentuali, statistiche verificabili
- Target: famiglie e investitori zona Padova/hinterland
- Keyword locali: sempre includere "Padova" e zone specifiche
- Citare fonti ufficiali nel testo (non solo in fondo)
- Transition words 30-35% per leggibilita' (Inoltre, Infatti, Di conseguenza, In particolare, Tuttavia)
- NO contenuti generici senza localizzazione

**Registrazione quadrupla (gia' in sezione 1.2, ribadita):**
1. `admin.html` → `_blogSeedArticles` (con `data_pubblicazione` YYYY-MM-DD)
2. `blog.html` → `articoliStatici`
3. `js/homepage.js` → `staticMap` + `articoliStatici`
4. `sitemap.xml` → URL con lastmod e priority 0.8

### 8.2 Standard Descrizioni Immobili — Testi per il Sito

> Le descrizioni immobili sul sito DEVONO essere **diverse** da quelle sui portali
> (Idealista, Immobiliare.it, Casa.it) per evitare duplicate content e deindexing.

**Struttura descrizione immobile (400-600 parole):**

1. **Apertura emozionale** (2-3 righe) — prima impressione, luce, sensazione
   - Es: "Luminoso trilocale al secondo piano con terrazzo panoramico, in una delle vie piu' tranquille di Limena."
2. **Caratteristiche principali** — elenco strutturato
   - Tipologia, superficie, locali, piano, stato
   - Classe energetica con IPE
   - Anno costruzione e eventuali ristrutturazioni
3. **Descrizione ambienti** — stanza per stanza
   - Soggiorno, cucina, camere, bagni — con metrature se rilevanti
   - Dettagli che fanno la differenza (esposizione, vista, materiali)
4. **Spazi esterni e pertinenze**
   - Giardino, terrazzo, balcone (con mq)
   - Garage, cantina, posto auto
5. **Contesto e zona** — perche' questa posizione e' strategica
   - Servizi vicini (scuole, supermercati, trasporti)
   - Link alla zona page corrispondente
   - Distanza dal centro (km e minuti)
6. **Chiusura con CTA** — invito a contattare
   - "Per informazioni o per fissare una visita: 049.88.43.484 / info@righettoimmobiliare.it"

**Regole testi immobili:**
- MAI copiare la descrizione dal portale — riscrivere con angolo diverso
- Dati verificati: superficie catastale vs commerciale, classe energetica reale
- Prezzo con indicazione €/mq per confronto zona
- NO termini vaghi ("bello", "interessante") — usare aggettivi specifici ("luminoso sud-ovest", "ristrutturato 2023", "riscaldamento autonomo a pavimento")
- Citare dati OMI della zona per dare contesto al prezzo
- Se presente virtual tour o video, segnalare con badge dedicato

**Schema JSON-LD per immobile:**
- Tipo: `RealEstateListing` (o `Product` con `offers`)
- Campi: name, description, url, image (array), price, priceCurrency
- address: PostalAddress con zona/comune
- GeoCoordinates (lat/lng)
- floorSize, numberOfRooms
- Collegamento a `RealEstateAgent` (l'agenzia)

### 8.3 Standard Pagine Zona — Struttura Obbligatoria

**Ogni pagina zona-*.html deve contenere:**

1. **H1:** "Case in vendita a [ZONA] — Prezzi, Quartiere e Consigli"
2. **Intro dichiarativa** (GEO) — 2 frasi con dati OMI (prezzo medio €/mq, trend)
3. **Sezione "Il quartiere"** — storia, carattere, target residenti
4. **Tabella prezzi** — confronto per tipologia (appartamento, villa, attico) con fonte OMI
5. **Servizi e infrastrutture** — scuole, trasporti, commercio, verde
6. **Pro e Contro** — lista onesta (credibilita' = E-E-A-T)
7. **FAQ locali** (min 5) — "Quanto costa un bilocale a [ZONA]?", "Conviene investire a [ZONA]?"
8. **CTA** — valutazione gratuita specifica per la zona
9. **Link interni** — verso articoli blog correlati e servizi

**Schema obbligatorio zona:**
- `RealEstateAgent` con `areaServed` specifico
- `FAQPage` con domande iper-locali
- `BreadcrumbList`
- `Place` con `GeoCoordinates` del centro zona

---

## 9. AZIONI TECNICHE — TODO

### 9.1 Bug e Fix Immediati — Aggiornati 12 Marzo 2026
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
- [x] **Email offuscata Cloudflare** — fix su 7 pagine (servizi, servizio-vendita, privacy, immobili, index, chi-siamo, contatti) — rimosso `__cf_email__` e `email-decode.min.js`
- [x] **H1 mancante landing-chat** — aggiunto H1 sr-only a 5 pagine: landing-chat-vendita, landing-chat-valutazione, landing-chat-insoddisfatti, landing-chat-offerta-luce, landing-chat-offerta-gas
- [x] **Meta description troppo lunghe** — accorciate a ≤160 char su 9 pagine: 6 zone pages, agenzia-immobiliare-padova, landing-mutuo (anche title accorciato), vendere-casa-padova-errori
- [x] **immobile.html escluso da audit** — e' un template dinamico (genera contenuto via JS)
- [x] **Audit automatico settimanale** — auto-run ogni 7gg, salvataggio su Supabase (tabella `audit_snapshots`), grafico storico con canvas, nella sezione Admin

### 9.2 Contenuti da Creare
- [x] blog-tempi-vendita-casa-padova.html — CREATO 8 marzo 2026
- [x] zona-vigonza.html — CREATA 8 marzo 2026
- [x] zona-abano-terme.html — CREATA 8 marzo 2026
- [x] zona-selvazzano.html — CREATA 8 marzo 2026
- [ ] Bollino "Verificato Righetto" — brand quality sugli annunci

### 9.3 Ottimizzazioni Performance
- [ ] LCP sotto 2 secondi su tutte le pagine (nuovo target competitivo)
- [ ] Verificare SVT — nessun caricamento "scattoso" (font swap, image pop-in)
- [ ] Verificare Engagement Reliability — form, bottoni, menu funzionano su tutti i device
- [ ] Page Experience consistency — tutte le pagine devono avere performance simile

### 9.4 SEO Tecnico
- [ ] **Contenuti unici vs portali** — le descrizioni immobili su Idealista/Immobiliare.it DEVONO essere diverse da quelle sul sito (rischio duplicate content e deindexing)
- [ ] Internal linking tra blog posts e zone pages (cross-link contestuali)
- [ ] Verificare indexing in Google Search Console
- [ ] Richiedere indicizzazione manuale nuove pagine via GSC
- [ ] Verificare che recensioni Google non siano sparite (nuove policies)
- [ ] Aggiungere video content (virtual tour, presentazione agenzia) — genera 66% piu' lead
- [ ] UTM tags su link GBP per tracciare traffico in GA4

### 9.5 Conversione e Lead Generation
- [ ] **Speed-to-lead:** risposta automatica entro 60 secondi (47-59% dei clienti sceglie il primo agente che risponde)
- [ ] **A/B test CTA:** testare copy diversi (es. "Valutazione Gratuita" vs "Scopri il Valore della Tua Casa")
- [ ] **Lead magnet segmentati:** CTA diversi per acquirenti (simulatore mutuo) e venditori (valutazione gratuita)
- [ ] **Video testimonial:** aggiungere video recensioni reali (piu' engaging del solo testo)
- [ ] **Siti <2s convertono 3x** meglio dei siti lenti — priorita' LCP

### 9.6 GEO/AEO — COMPLETATI 8 Marzo 2026
- [x] **llms.txt aggiornato** — aggiunte nuove zone (Vigonza, Abano, Selvazzano) e prezzi
- [x] **robots.txt AI bots** — GPTBot, ClaudeBot, Google-Extended, PerplexityBot tutti Allow + chatbot.js Allow
- [ ] Assicurare che contenuti importanti NON siano dietro JS client-side (le AI estraggono HTML statico)
- [x] **Timestamp "Ultimo aggiornamento"** — aggiunto a 6 articoli cornerstone
- [x] **sameAs** — presente su tutte le pagine principali (47/48), faq.html corretto
- [x] **BreadcrumbList** — presente su 48 pagine (tutte tranne index.html che non lo richiede)
- [x] **Person schema** — presente su chi-siamo.html e landing-agente.html

---

## 10. KPI E CALENDARIO

### 10.1 KPI da Monitorare (Aggiornato 11 Marzo 2026 con dati reali)
| Metrica | Attuale (11 mar) | Obiettivo 3 mesi | Obiettivo 6 mesi | Obiettivo 12 mesi |
|---|---|---|---|---|
| Clic GSC mensili | **150** | 400 | 1.000 | 3.000 |
| Impressioni GSC | **1.590** | 5.000 | 15.000 | 50.000 |
| CTR media | **9,4%** | 10% | 12% | 15% |
| Posizione media | **8,1** | 6 | 4 | 3 |
| Utenti settimanali GA | **96** (+152%) | 300 | 800 | 2.000 |
| Recensioni Google | ~127 | 142 | 172 | 200+ |
| "agenzia immobiliare padova" | pos. ~28 | Top 15 | Top 10 | Top 3 |
| "vendere casa padova" | pos. ~15 | Top 10 | Top 5 | Top 3 |
| Pagine indicizzate | ~55 | 65 | 80 | 120 |
| Backlink domini unici | ~5 | 15 | 30 | 50 |
| Domain Authority | ~5 | 10 | 15 | 20+ |
| Newsletter iscritti | ? | 100 | 300 | 500+ |

### 10.2 Calendario Editoriale
| Mese | Contenuto | Keyword target | Stato |
|---|---|---|---|
| Marzo 2026 | blog-tempi-vendita-casa-padova.html | "quanto tempo vendere casa padova" | **FATTO** |
| Marzo 2026 | zona-vigonza.html | "case vigonza", "immobiliare vigonza" | **FATTO** (anticipato) |
| Marzo 2026 | zona-abano-terme.html | "case abano terme" | **FATTO** (anticipato) |
| Marzo 2026 | zona-selvazzano.html | "case selvazzano dentro" | **FATTO** (anticipato) |
| Aprile 2026 | Video presentazione agenzia | Brand awareness + engagement | TODO |
| Maggio 2026 | Articoli fiscali (IMU, bonus) | Long-tail fiscale | TODO |
| Giugno 2026 | Bollino "Verificato Righetto" | Brand quality | TODO |

### 10.3 Routine di Monitoraggio
- **Settimanale:** Performance report in Search Console + Google Posts
- **Mensile:** Audit metriche SEO + Core Web Vitals + citazioni AI
- **Trimestrale:** Audit completo contenuti + struttura + competitor
- **Ad ogni Google Update:** Verificare impatto sul sito

---

## 11. GESTIONE cPanel

### 11.1 Da Eliminare (per liberare spazio)
| File/Cartella | Dimensione | Motivo |
|---|---|---|
| `backup-3.2.2026_10-53-22_wyrighet.tar.gz` | **37.04 GB** | Backup gia' scaricato in locale |
| `public_htmlcopia140422.zip` | **11.37 GB** | Backup WordPress 2022 — obsoleto |
| `error_log*` / `error_log_php*` | variabile | Log errori vecchi |
| `sp_mysql_bk/` | variabile | Backup MySQL WordPress — non serve |
| `public_html/` contenuto | variabile | Vecchio sito WordPress |
| Database MySQL | variabile | Database WordPress non necessari |

### 11.2 Da Tenere Assolutamente
- Record DNS (A, CNAME, MX)
- Dominio registrato
- Account email attivi
- Certificato SSL
- Cartelle: `mail/`, `etc/`, `ssl/`, `cache/`, `logs/`, `tmp/`

---

## 12. CHECKLIST RAPIDE

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

## 13. CHANGELOG

### v2.1 - 12 Marzo 2026 (Consolidamento SKILL + Fix Scraping Articolo)
- **Eliminato SKILL-KILLER.md** — tutto inglobato qui, unica fonte di verita'
- **Fix blocco "Conferma e Salva Bozza"** nello scraping articolo — ora usa `sb` (non `supabase`) e fallback localStorage con chiave `rig_blog_articles`
- **Nuova sezione 3.4 "Strumenti Admin"** — documentati Scraping Articolo, Trend & Idee, Audit automatico, Analytics automatico
- **Aggiornato riferimento snapshot** — rimosso "+ Nuovo Snapshot", ora tutto automatico ogni 7gg
- **Aggiornata struttura file** admin.html con tutte le nuove funzionalita'

### v2.0 - 12 Marzo 2026 (Ottimizzazione SEO pagina pillar + Scraping Articolo + Trend Admin)
- **Ottimizzazione agenzia-immobiliare-padova.html** per le keyword "agenzia immobiliare padova" (pos. 28,5 → target top 10) e "vendere casa padova" (pos. 14,7 → target top 5):
  - Title tag riscritto con entrambe le keyword target
  - Meta description con numeri concreti (25 anni, 4.9 stelle, 4,2 mesi) + telefono per CTR
  - H1 ottimizzato: "Agenzia immobiliare a Padova — vendere casa in 4,2 mesi"
  - Nuova sezione "Come vendere casa a Padova al miglior prezzo" (6 card, metodo in 5 fasi)
  - Nuova sezione "Mercato immobiliare Padova 2026: i numeri" (tabella 8 zone con prezzi, trend, tempi)
  - 4 nuove FAQ specifiche "vendere casa padova" + schema FAQPage aggiornato (da 6 a 10 FAQ)
  - Fonti citate: OMI, Agenzia Entrate, FIAIP Veneto (E-E-A-T + GEO)
- **Scraping Articolo nell'Admin:** pulsante accanto a "+ Nuovo Articolo" nel Blog, modal completo con ricerca trend Google News RSS, generazione bozza strutturata, anteprima e salvataggio
- **Sezione "Trend & Idee" nell'Admin:** ricerca topic trending per 8 categorie immobiliari, salvataggio idee in localStorage
- **Fix proxy CORS:** sistema fallback multiplo (corsproxy.io, allorigins, cors.sh, corsproxy.org) con timeout 8s
- **Rimosso pulsante "+ Nuovo Snapshot"** dall'Analytics (automatico ogni 7gg)

### v1.9 - 12 Marzo 2026 (Audit Auto-settimanale + Fix SEO da Audit)
- **Audit automatico settimanale:** auto-run ogni 7gg nell'Admin, salvataggio risultati su Supabase (`audit_snapshots`), grafico storico canvas con barre OK/Warning/Errori
- **Pulsante Audit spostato in Admin:** dalla pagina scraping.html alla sidebar Admin (sezione dedicata "Audit Sito")
- **Fix H1 mancante:** aggiunto H1 sr-only a 5 landing-chat (vendita, valutazione, insoddisfatti, offerta-luce, offerta-gas)
- **Fix meta description troppo lunghe:** accorciate a ≤160 char su 9 pagine (6 zone, agenzia, landing-mutuo, vendere-casa-padova-errori)
- **Fix title troppo lungo:** landing-mutuo.html accorciato a ≤70 char
- **immobile.html escluso dall'audit:** e' template dinamico, non ha title/meta statici

### v1.8 - 12 Marzo 2026 (Standard Contenuti + Fix Email + Pulsante Audit)
- **Nuova sezione 8 "Standard Contenuti":** standard obbligatori per articoli blog (struttura H-tag, formato GEO/AEO, fonti verificate, meta tags, schema triplo, stile scrittura), descrizioni immobili (struttura 400-600 parole, regole anti-duplicate content vs portali, schema RealEstateListing), pagine zona (struttura completa con dati OMI)
- **Fix email Cloudflare:** rimossa offuscazione `__cf_email__` da 7 file (servizi, servizio-vendita, privacy, immobili, index, chi-siamo, contatti) — email ora in chiaro come `info@righettoimmobiliare.it` con `mailto:` dove appropriato
- **Rimosso script `email-decode.min.js`** da servizio-vendita, immobili, contatti, index (script Cloudflare non necessario su GitHub Pages)
- **Pulsante Audit Sito** in scraping.html: genera report completo di tutte le pagine (schema, meta, FAQ, email, performance) con checklist automatica e suggerimenti per la SKILL
- **Rinumerazione sezioni:** da 12 a 13 sezioni per ospitare la nuova sezione 8

### v1.7 - 11 Marzo 2026 (Analytics Dashboard + Strategia Portale Regionale + Case Green)
- **Dashboard Analytics nell'admin:** sezione completa con 8 KPI cards, storico snapshot, top query, performance per pagina, obiettivi strategici con progress bar, grafico trend canvas JS, link rapidi a GSC/GA4/PageSpeed
- **Primo snapshot dati reali:** GSC 150 clic, 1.590 impressioni, CTR 9,4%, pos. 8,1 — GA4 96 utenti (+152,6%), 926 eventi (+110,9%)
- **Strategia "Portale Regionale #1":** roadmap 12 mesi in 3 fasi (Consolidamento → Espansione → Dominio) con metriche target per sponsor/partnership
- **KPI aggiornati con dati reali:** tabella 9.1 ora con baseline misurata e obiettivi a 3/6/12 mesi
- **Nuovo articolo:** blog-direttiva-case-green-limena-padova.html — Direttiva EPBD 2024, impatto su Padova/Limena (2.700 parole, timeline, FAQ, classi energetiche)
- **Guide interattive:** blog-servizi-infrastrutture-padova, blog-scuole-istruzione-padova, blog-trasporti-mobilita-padova
- **Punteggio sito aggiornato:** da 8.1 a 8.4/10

### v1.6 - 11 Marzo 2026 (Landing ENEL + Email Marketing in Agenda)
- **Architettura email documentata:** aggiunta sezione 2.2 completa — NO Brevo, tutto interno via `api.righettoimmobiliare.it` (PHP relay su cPanel)
- **Nuove landing ENEL:** offerta-enel-luce, offerta-enel-gas, reel-offerta-gas (in sottocartella `landing/`)
- **Nuove landing chat ENEL:** landing-chat-offerta-luce, landing-chat-offerta-gas
- **Fix slug landing ENEL:** aggiunto prefisso `landing/` negli slug admin per URL corrette
- **Pulsanti azioni immobili:** ingranditi con classe `btn-action` (40x40px min, ombre, bordi)
- **Campagne email in Agenda:** le email massive ora appaiono nel calendario settimanale con icona busta viola
- **Struttura file aggiornata** con tutte le nuove landing

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
