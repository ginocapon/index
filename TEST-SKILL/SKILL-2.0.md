# SKILL 2.0 — Righetto Immobiliare
## Prompt Operativo Master Unificato

> **Versione:** 2.0 — 15 Marzo 2026 (patch contenuti **3 Aprile 2026**)
> **Unica fonte di verita'** — Sostituisce SKILL-UNIFICATA.md, AUTOMATION-SITE-2026.md e CLAUDE.md
> **Ultimo aggiornamento Google verificato:** 8 Marzo 2026
> **Prossima verifica consigliata:** Aprile 2026
>
> **Changelog 3 Aprile 2026:** eliminata la CTA Google legacy (sfondo rosso `#B71C1C`) su **45+** pagine (`blog-*`, `landing-*`); sostituita con `section.blog-rich-cta-strip` + link `css/blog-rich.css?v=2` dove mancava. Script riutilizzabili in `scripts/`: `migrate_legacy_red_google_cta.py`, `ensure_blog_rich_css_link.py`, `blog_add_rich_css_and_footer_cta.py`. Allineati claim aggressivi su `landing-vendita.html`, `landing-vendere-casa-padova.html`, `landing-agente.html` e messaggi chat (`landing-chat-vendita`, `landing-chat-insoddisfatti`) ai numeri consentiti in `CLAUDE.md`. `blog-articolo.html`: aggiunto `blog-rich.css` + CTA strip statica sotto il corpo dinamico.

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
10. **URL pulite — MAI .html nei link** — tutti i link interni devono usare URL senza estensione `.html`. GitHub Pages serve automaticamente `pagina.html` quando visiti `/pagina`. I file su disco mantengono l'estensione `.html`, ma ogni `href`, `canonical`, `og:url`, sitemap e link interno deve puntare a URL pulite (es. `/landing-chat-valutazione` e NON `/landing-chat-valutazione.html`)
11. **Auto-registrazione admin** — ogni nuova pagina creata (landing, blog, immobile) DEVE essere registrata automaticamente:
    - **Landing pages** → inserire nella tabella Supabase `landing_pages` tramite seed in `admin.html` (`_landingSeedPages`) + aggiungere in array `EM_SITE_PAGES` + il picker email marketing le carica automaticamente dal seed/Supabase
    - **Blog** → registrare in `sitemap.xml`, `blog.html`, `js/homepage.js`, `admin.html` (`_blogSeedArticles`)
    - **Pagine generiche** → registrare in `sitemap.xml` + navigazione
12. **Data di pubblicazione obbligatoria** — ogni landing page nel seed `_landingSeedPages` in `admin.html` DEVE avere il campo `data_pubblicazione` in formato `YYYY-MM-DD`. Senza questo campo la colonna "Pubblicazione" nell'admin mostra "—"
13. **Entity-Based SEO + Neural Matching (NO keyword stuffing)** — Google ragiona per **entita' semantiche** e **corrispondenza concettuale profonda** (Neural Matching/RankEmbed). Nessuna frase di 2+ parole deve apparire piu' di 5 volte per pagina. "a Padova" max 8-10 volte. Usare sinonimi, varianti e campo semantico ricco. Title, H1 e meta description devono usare varianti diverse. Ogni pagina deve coprire l'intero spazio concettuale del topic (copertura 80%+, co-occorrenze semantiche 70%+, intent chiaro entro 100 parole). Dettagli completi nella sezione 8.3

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

> Audit verificato: 16 marzo 2026 (3a passata definitiva — conversione portata a 9.9/10)

| Area | Punteggio | Note |
|---|---|---|
| SEO on-page | **9.8/10** | 18 meta desc corrette, 4 title corretti, tutti canonical OK, OG completi |
| Schema.org | **9.8/10** | RealEstateAgent+FAQPage+BreadcrumbList+Person completi su 95%+ pagine, sameAs e GeoCoordinates ovunque |
| Contenuti/Blog | **9.8/10** | 40+ articoli, 4 cluster completi, timestamp visibile su tutti, author bio ovunque |
| GEO/AEO | **10/10** | Unico a ottimizzare per AI — robots.txt AI bots Allow, llms.txt completo (servizi, orari, social, landing, 40+ blog; tariffe mediazione solo in sede, non online), timestamp, sameAs tutti OK |
| Core Web Vitals | **9/10** | Font preload completo (5 font), --nero definito, font-display:swap, GA4 deferred con requestIdleCallback, CSS critical/below-fold separato. Target LCP <2s quasi raggiunto |
| Zone Pages | **9.5/10** | 14 zone con Pro/Contro, 5 FAQ schema, tabelle OMI, Place+GeoCoordinates |
| Chatbot AI | **10/10** | Unico nel mercato locale |
| Simulatore mutuo | **10/10** | Unico nel mercato locale |
| **Conversione/Lead** | **9.9/10** | 10 sistemi su 14 pagine: A/B test, speed-to-lead, segmentazione, exit intent con urgency, social proof con trust badges, sticky CTA mobile auto-inject, compatibilita' form homepage, GA4 tracking completo |
| Analytics Dashboard | **9/10** | Sezione completa nell'admin con KPI, storico, grafici, obiettivi |
| Recensioni Google | **6/10** | ~127 vs 256 Tetto Rosso — gap critico |
| Domain Authority | **4/10** | Problema #1 — nessun backlink significativo |
| Apparizione SERP | **3/10** | Brand queries OK (pos. 1.3), non-brand ancora deboli, vecchie pagine WP ancora indicizzate |
| **TOTALE** | **9.2/10** | On-site perfetto (media 9.8), GEO 10/10, Conversione 9.9/10. Unici colli di bottiglia: DA (4), SERP (3), Recensioni (6) — fattori off-site |

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

**Scraping Articolo** (pulsante nella sezione Blog, accanto a "+ Nuovo Articolo") — **3 step**:

**STEP 1 — Topic:**
1. Modal con 9 categorie immobiliari (mercato Padova, mutui, bonus, case green, investimenti, affitto studenti, compravendita, quartieri, normative)
2. "Cerca Topic" → Google News RSS via rss2json.com (CORS nativo)
3. Seleziona un topic dalla lista OPPURE scrivi titolo personalizzato
4. "Avanti: Aggiungi Foto →"

**STEP 2 — Foto:**
5. **Foto copertina (hero):** l'utente puo' incollare un URL proprio OPPURE cercare foto royalty-free su Unsplash con query personalizzata. Vengono mostrate 6 anteprime cliccabili
6. **Foto inline (max 3):** URL personalizzati o ricerca Unsplash per ogni foto. Vengono distribuite automaticamente dopo sezione 1, 3 e 5
7. Preview della foto hero prima di procedere
8. "Genera Bozza con Foto →"

**STEP 3 — Anteprima e salvataggio:**
9. **Contenuto 100% originale generato automaticamente** (no plagio):
   - Titolo rielaborato con 4 template randomizzati (mai copiato dalla fonte)
   - 6 sezioni H2 con prospettiva Righetto Immobiliare
   - **Tabella dati per zona** (8 zone Padova: prezzo/mq, variazione, tempi vendita) con fonte OMI/FIMAA
   - **Highlight box** con 4 numeri chiave del mercato padovano
   - **Tabella attrattivita' investimento** per zona (target, prospettiva)
   - **Citazione** di Gino Capon in blockquote
   - Foto inline distribuite tra le sezioni con `<figure>` e `<figcaption>`
   - 4 FAQ specifiche con risposte originali
   - Meta description unica, slug dal titolo, 4 schema JSON-LD
10. Anteprima scrollabile con tutto il contenuto
11. "Conferma e Salva Bozza" → salva in Supabase + localStorage + redirect a Blog

**TEMPLATE DINAMICO:** gli articoli creati dallo scraping NON hanno file HTML fisici. Usano `blog-articolo.html?s=slug` che:
- Mostra hero con immagine di copertina + overlay scuro + crediti
- Renderizza FAQ interattive con accordion
- Include CTA banner "Contattaci"
- Articoli correlati automatici per categoria

**REGOLA ANTI-PLAGIO OBBLIGATORIA:** ogni contenuto generato dallo scraping DEVE essere originale. Il topic della fonte viene usato solo come ispirazione — titolo, testo e FAQ vengono rielaborati con la prospettiva di Righetto Immobiliare, dati locali di Padova e fonti ufficiali (OMI, FIMAA, Agenzia Entrate).

**REGOLA IMMAGINI:** mai riutilizzare immagini gia' presenti nel sito (img/foto-servizi, img/blog, img/team). Ogni nuovo articolo deve avere foto NUOVE — o caricate dall'utente o cercate su Unsplash.

**Trend & Idee** (sezione dedicata nella sidebar Admin):
- Ricerca topic trending per 8 categorie immobiliari italiane
- Risultati da Google News RSS via rss2json.com (CORS nativo)
- Pulsanti "Salva Idea" (localStorage) e "Crea Articolo" (apre modal scraping)
- Idee salvate riutilizzabili in qualsiasi momento

**Audit Sito** (automatico ogni 7 giorni):
- Analizza tutte le pagine HTML: schema, meta, FAQ, email, performance
- Salva risultati su Supabase (tabella `audit_snapshots`)
- Grafico storico con barre OK/Warning/Errori

**Audit Automatico SKILL-2.0 via GitHub Actions** (ogni venerdi' ore 07:00 CET):
- Workflow: `.github/workflows/audit-settimanale.yml`
- Script: `scripts/audit-skill.sh`
- **Eseguibile anche manualmente:** Actions → "Audit Settimanale SKILL-2.0" → Run workflow
- **Output:** Issue GitHub con label `audit` + email riepilogativa a info@righettoimmobiliare.it
- **16 controlli per pagina:** meta description, canonical, URL pulite (no .html), Open Graph, Schema JSON-LD (RealEstateAgent, GeoCoordinates, sameAs, dateModified), BreadcrumbList, font-display:swap, keyword stuffing ("a Padova" max 10), CDN esterni vietati, framework vietati, link interni con .html, GA4, viewport mobile, filter:blur, will-change, placeholder non sostituiti
- **Controlli globali:** sitemap.xml, robots.txt (regole AI bots), llms.txt (GEO), lessico SEO+AI / AEO / SEM (allineamento contenuti a §4.5.1 — revisione manuale o checklist redazionale)
- **Controlli specifici blog:** FAQPage schema, author bio (E-E-A-T), timestamp visibile
- **Controlli zone:** FAQPage, GeoCoordinates, dati OMI
- **Controlli servizi:** FAQPage schema
- **Email:** inviata tramite API relay interno (secret `EMAIL_RELAY_KEY` in GitHub Actions)
- **Autorizzazione permanente** — il workflow gira automaticamente ogni venerdi' finche' non viene disabilitato

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
5. **Citare fonti ufficiali** (Agenzia Entrate, OMI, FIMAA)
6. **Frasi auto-contenute** — ogni claim deve avere senso letto isolatamente
7. **Freshness** — aggiornare contenuti cornerstone regolarmente con timestamp "Ultimo aggiornamento"
8. **llms.txt** — mantenere aggiornato per guidare AI bots

**Regole AEO per featured snippet:**
1. Risposta 40-60 parole come primo paragrafo dopo ogni H2
2. Formato: "[Keyword] e' [definizione/risposta]"
3. Min 5 FAQ con Schema FAQPage per pagina
4. Tabelle comparative per dati numerici

### 4.5.1 Lessico: SEO + AI, AEO, GEO, SEM (combinazioni di mercato)

> Spesso si sentono acronimi accoppiati a "AI" o usati come sinonimi. Qui **definizioni operative** per Righetto e **legame** con le sezioni gia' presenti in questo file.

| Termine | Significato (breve) | Cosa copriamo sul sito statico | Riferimento SKILL |
|--------|----------------------|--------------------------------|-------------------|
| **SEO + AI** | SEO classico (indicizzazione, intent, contenuti) **piu'** segnali che aiutano **modelli e crawler AI** a citare correttamente il brand | Contenuti chiari, E-E-A-T, `llms.txt`, `robots.txt` (Allow bot AI dove previsto), JSON-LD, **no claim inventati** | §4.2 E-E-A-T, §4.5 GEO, §4.6 Schema, `llms.txt` |
| **AEO** | **Answer Engine Optimization** — contenuti strutturati per **risposte dirette** (snippet, People Also Ask, assistenti) | H2 in formato domanda dove possibile, primo paragrafo dopo H2 40-60 parole, **FAQPage** + FAQ visibili, tabelle | §4.5 regole AEO, checklist blog §5 |
| **GEO** | **Generative Engine Optimization** — ottimizzazione per **citazioni in risposte generate** (Gemini, ChatGPT, Perplexity, AI Overviews) | Frasi dichiarative in apertura sezione, dati verificabili, `llms.txt` aggiornato, freshness | §4.5 GEO |
| **SEM** | **Search Engine Marketing** in senso lato = visibilita' sui motori **organico + a pagamento** | **Sito:** landing con CTA chiare, URL pulite, tracking GA4, allineamento messaggio annuncio↔landing se si usano **Google Ads** (fuori repo). **Nota:** campagne Ads **non** vivono nel codice GitHub; la SKILL copre **asset on-site** (landing, velocita', coerenza keyword) | §4.3 ranking, landing in architettura |

**Regole aggiuntive (bundle):**
1. **Non confondere** GEO con geolocalizzazione geografica: qui GEO = *Generative*, non "geo targeting" generico.
2. **SEO + AI** non significa "testo scritto da bot senza revisione": significa **contenuti umani** ottimizzati anche per **consumo da sistemi AI** (struttura, factuality, fonti).
3. **SEM (Ads)** — ogni nuova landing per campagne deve rispettare **stesso standard** di canonical, meta, mobile-first e CTA del sito; variabili UTM opzionali ma link pubblici senza `.html`.
4. **Audit automatico** (`.github/workflows/audit-settimanale.yml`) continua a essere la **fonte oggettiva** su meta, canonical, schema, keyword stuffing, `llms.txt`: integrare manualmente solo cio' che lo script non misura (tono, transition words, % AEO in prosa).

### 4.5.2 Guardrail URL, ancore e visibilita' (obbligatorio)

> Ogni intervento AEO/SEO su titoli o contenuti **non** deve degradare URL indicizzati, canonical o fragment interni.

1. **Non modificare** path pubblici (`/blog-...`, `/zona-...`), `rel="canonical"`, `og:url`, voci in `sitemap.xml`, slug file su disco vs URL pulite senza coordinamento (checklist deploy).
2. **Frammenti `#`:** se un `<h2 id="...">` cambia testo ma **mantiene lo stesso `id`**, i link `href="#id"` restano validi. **Non rinominare `id`** senza aggiornare **tutti** i `href` interni, TOC, eventuali CTA e link da email/admin.
3. **TOC / indice:** si puo' aggiornare il **testo** del link (`<a href="#budget">...</a>`) per allinearlo all'H2; **non** cambiare l'`href` se non si aggiornano anche gli `id` corrispondenti nella pagina.
4. **Riscritture AEO (H2 domanda):** preservare **keyword primarie** del paragrafo sottostante (Padova, quartiere, mutuo, OMI, ecc.) nel titolo o nel primo capoverso; evitare titoli generici che diluiscono il segnale.
5. **Script automatici** (`apply_*_h2_*.py`): dopo ogni run, verificare a campione TOC vs H2 e assenza di `??` in titoli.

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

### 5.2 Palette Colori CTA (Contrast-Safe) — Aggiornata 16 Marzo 2026

> **Cambio colore CTA:** tutti i CTA primari ora usano arancione (#FF6B35) al posto del vecchio gold (#B8D44A).
> L'arancione e' il colore con il piu' alto tasso di conversione secondo studi UX (HubSpot, ConversionXL).
> Ratio contrasto arancione + testo scuro: ~5.0:1 (WCAG AA).

| Elemento | Background | Testo | Ratio |
|----------|-----------|-------|-------|
| **CTA primario (TUTTI)** | `var(--oro)` **#FF6B35** (arancione) | `var(--nero)` #152435 | **~5.0:1** |
| CTA secondario | `var(--blu)` #2C4A6E | `white` | ~5:1 |
| CTA valutazione | `var(--purple)` #6C63FF | `white` | ~4.5:1 |
| CTA landing-agente | `var(--mint)` #00E5A0 | `var(--nero)` | ~5.5:1 |

> **REGOLA:** var(--oro) #FF6B35 si usa SOLO con testo scuro (var(--nero) #152435), MAI con testo bianco (ratio troppo basso).

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
- [ ] Profilo FIMAA / FIMAA con link al sito
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
| venderecasapadova.it | Dominio exact-match, funnel diretto, tecnica Open House | landing-vendere-casa-padova.html gia' creata; valutare Open House come differenziazione |
| Pianeta Casa | Widget Google Reviews reale nel sito | Embed reale da implementare |
| Grimaldi | Magazine mensile, freshness signals | Min 2 articoli blog/mese |
| Engel & Volkers | Instagram forte (826 follower) | Rafforzare Instagram con reels e storie |
| Tempocasa | "Immobile Certificato", Matterport virtual tour 3D | Creare bollino "Verificato Righetto"; valutare tour 3D professionale |

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
- Fonti accettate: OMI (Osservatorio Mercato Immobiliare), Agenzia Entrate, ISTAT, IlSole24Ore, FIMAA, Comune di Padova, Regione Veneto
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

### 8.1b Layout long-read, engagement e alternanza grafica (Righetto)

> **Riferimento esterno (solo ispirazione):** articoli tipo "magazine" (hero chiaro, indice, metriche, tabelle con fonte,
> callout, FAQ, CTA finale, correlati) aumentano **tempo in pagina** e scansionabilita'. Su Righetto si adotta lo **stesso
> principio editoriale**, ma **rispettando i vincoli del progetto** (Sezione 5, `CLAUDE.md`).

**Vincoli tecnici (non negoziabili):**

- Solo **HTML/CSS/JS vanilla** — nessun framework, **nessun CDN esterno** (niente Google Fonts nel contenuto: usare
  `fonts.css` / font self-hosted gia' in pagina).
- Animazioni e hover: **solo `opacity` e `transform`** — **vietato** `filter: blur(...)` sulle animazioni.
- **No `will-change` permanente** su elementi decorativi.
- CTA: contrasto minimo **4.5:1** (WCAG AA) — palette ufficiale Sezione **5.2** (`--oro` + testo `--nero`, oppure `--blu` + bianco).
- **CTA di chiusura articolo:** **non** usare sfondi rossi accesi o aggressivi. Preferire **gradiente blu → nero**
  (brand) con bottone **arancione** (`--oro`) e testo scuro — pattern in `css/blog-rich.css` (classe `blog-rich-cta-strip`).
- **Contenuto CMS (Supabase / admin):** salvare **solo frammento HTML del corpo** — **mai** incollare pagine complete
  (`<!DOCTYPE>`, `<html>`, `<head>`, `<meta>` nel corpo). Il lettore `blog-articolo.html` sanifica il body, ma la fonte
  deve restare pulita per evitare doppi schema e DOM corrotti.

**Foglio di stile condiviso — `css/blog-rich.css`:**

- Caricato da **`blog-articolo.html`** (articoli dinamici) e dalle pagine che usano i componenti. Per ogni **`blog-*.html`** statico, aggiungere nella `<head>`:
  `<link rel="stylesheet" href="css/blog-rich.css?v=2">` (stesso `?v=` delle altre risorse quando si aggiorna il foglio).
- Le classi `blog-rich-*` sono definite in `css/blog-rich.css` (anche **fuori** da `.art-content`, es. CTA strip a fine `main`); il corpo articolo resta in `.art-content` dove presente.

**Blocchi raccomandati (copiare/incollare nel corpo e riempire):**

1. **Indice (TOC)** — `nav.blog-rich-toc` o `div.blog-rich-toc` con titolo + `<ol>` di link interni (`href="#id-sezione"`).
   Ogni **H2** citato nell'indice deve avere **`id`** stabile (slug ASCII).
2. **Badge aggiornamento** — `span.blog-rich-badge` (es. "Aggiornato: aprile 2026") quando il contenuto e' stato rivisto.
3. **Metriche a scheda** — `div.blog-rich-stats` > tre `div.blog-rich-stat` con `.blog-rich-stat-value`, `.blog-rich-stat-label`,
   `.blog-rich-stat-src` (obbligatoria **fonte** sotto ogni numero, come da 8.1).
4. **Callout** — `div.blog-rich-callout` per sintesi / "in sintesi" / avvertenze normative.
5. **Tabella premium** — `div.blog-rich-table-wrap` > `<table>`; riga evidenziata: `tr.blog-rich-row-highlight`;
   sotto la tabella: `p.blog-rich-table-source` con citazione fonti (OMI, ISTAT, Banca d'Italia, …).
6. **CTA di chiusura (non rossa)** — `section.blog-rich-cta-strip` > `.blog-rich-cta-inner` > H2 + testo + link
   `a.blog-rich-btn` verso `contatti` o CTA pertinente; `.blog-rich-cta-sub` per micro-copy secondario.
7. **Correlati inline** — `div.blog-rich-related` con `a.blog-rich-related-card` (2–3 link interni verso altri articoli/zone).
8. **Box fonti** — `div.blog-rich-sources` con lista di link/titoli documentali verificabili.

**Alternanza tra articoli ("visual rhythm"):**

- Alternare **3 layout mentali** per non rendere tutto uguale:
  - **Modalita' A — "dati"**: subito dopo l'intro, TOC + tabella comparativa + callout.
  - **Modalita' B — "guida"**: TOC dopo il primo H2; metriche a meta' articolo; CTA strip prima delle FAQ.
  - **Modalita' C — "storytelling"**: callout in apertura; metriche sparse; correlati prima del box fonti.
- **Immagini:** almeno 1 figura ogni 2–3 H2 dove esiste materiale (foto reale, grafico da fonte, schema). Sempre
  `width`/`height` o `aspect-ratio` (Sezione 5.1 CLS).

**Pulsanti "3D" (leggeri, conformi):**

- Effetto tridimensionale solo con **`border-radius`**, **`box-shadow`** stratificato leggero e su **`:hover`**:
  `transform: translateY(-2px)` + ombra piu' ampia. **Vietato** usare blur animato o parallasse pesante.

**Checklist prima di pubblicare un articolo "ricco":**

- [ ] `blog-rich.css` incluso se pagina statica `blog-*.html`
- [ ] Nessun dato numerico senza fonte visibile (tabella, callout o nota)
- [ ] FAQ + JSON-LD allineati (gia' obbligatori in 8.1)
- [ ] CTA finale con **blu/nero + bottone oro**, non rosso pieno
- [ ] Link interni (zone, servizi, altri blog) **funzionanti** e non duplicati
- [ ] Verifica mobile: TOC, tabella (`overflow-x: auto` nel wrap), schede metriche a colonna singola

**Migrazione articoli esistenti (lavoro graduale):**

- Non e' obbligatorio aggiornare tutti i file in un solo intervento: priorita' **pillar** e articoli con traffico GSC.
- Ogni migrazione: stesso articolo in `blog.html` / `homepage.js` / `sitemap` gia' registrato — si interviene solo sul
  markup dentro `.art-content` + link al CSS.

### 8.1c Qualità corpo, SEO 2026, crawler AI e GEO/AEO (OBBLIGATORIO — prima pubblicazione)

> **Obiettivo:** contenuti utili per utente e motori, segnale pulito per **Neural Matching** e per **estrazione risposta**
> (snippet, assistenti, citazioni). Il «riempimento» meccanico danneggia fiducia, SEO e qualità percepita da sistemi AI.

**1) Divieto di «fabbrica di paragrafi»**

- **Vietato** usare cicli (`for`, template) che ripetono la **stessa frase** o lo **stesso blocco** cambiando solo
  l'incipit, per raggiungere un numero di parole o un `wordCount` nello schema.
- Eccezione minima: **al massimo 24** paragrafi da template **solo se** ogni paragrafo differisce in **sostanza**
  (fonte, leva, azione) e non solo in transizione iniziale; preferire **prosa unica** (H2, liste, tabelle, callout).
- Ogni nuovo **script di generazione batch** (`scripts/*.py`) deve includere un **controllo automatico** che fallisce
  (o avvisa in CI) se più di **2** paragrafi `<p>` del corpo hanno **testo normalizzato identico**.

**2) `wordCount` nello schema BlogPosting / Article**

- Deve riflettere il **corpo principale** reale (intro + sezioni + FAQ visibili solo se incluse nel conteggio documentato),
  **non** boilerplate ripetuto artificiosamente.
- Non sommare testo duplicato intenzionalmente per superare soglie.

**3) Disclaimer e nota mediazione**

- **Un solo** blocco disclaimer generale per pagina (salvo esigenze normative distinte).
- **Una sola** nota compensi/mediazione in linea con `CLAUDE.md` e mandato in sede.

**4) Immagini copertina articoli (`blog-*.html`, CMS)**

- **Vietato** caricare asset editoriali da `unsplash.com`, `images.unsplash.com`, `source.unsplash.com` o CDN esterni
  non previsti dal progetto (`CLAUDE.md`): solo path sotto `img/` o URL assoluti `https://righettoimmobiliare.it/img/...`.
- Formato preferito: **WebP**, proporzione consigliata **1200×630** (Open Graph), peso tipico **sotto ~120 KiB**
  dopo export mirato (qualità ~80–85).
- Evitare PNG/JPEG **piccoli** upscalati nell'hero (sfocatura e LCP peggiore).
- Dopo nuove copertine: allineare `og:image`, `BlogPosting.image`, `src` hero, `blog.html`, `js/homepage.js`, `admin.html`
  se l'articolo è in elenco statico.

**5) SEO tecnico e contenuto (sinergia)**

- Snellire il testo significa **togliere ripetizione inutile**, non ridurre fonti o profondità: mantenere **tabelle fonti**,
  link istituzionali (OMI, ISTAT, Banca d'Italia, BCE, Entrate) e **internal link** utili (Sezione 8.1).
- **Entity / anti-stuffing:** restano valide le regole della Sezione **8.3** (nessuna frase 2+ parole >5 volte, «a Padova»
  limitato, sinonimi).

**6) GEO / AEO (risposte da motori e assistenti)**

- Le risposte estratte sono migliori se ogni **H2** ha **primo capoverso** diretto (40–60 parole) e **claim** isolabili,
  senza loop di frasi quasi uguali che confondono il ranker e riduono utilità per l'utente.

**7) Checklist obbligatoria quando si genera un nuovo articolo o pagina (anche via script)**

- [ ] Nessun paragrafo duplicato oltre le soglie del punto 1.
- [ ] Copertina WebP (o piano di conversione immediata) + dimensioni dichiarate coerenti con layout.
- [ ] `wordCount` coerente con corpo reale.
- [ ] Schema triplo (BlogPosting / FAQ / Breadcrumb) allineato al contenuto visibile.
- [ ] Registrazione in `blog.html`, `homepage.js`, `admin.html`, `sitemap.xml` se applicabile (processo gia' definito altrove).

### 8.3 Entity-Based SEO + Neural Matching — Ottimizzazione Semantica Completa (OBBLIGATORIO)

> **Aggiornamento Marzo 2026:** Google ragiona per **entita' semantiche**, non piu' per keyword esatte ripetute.
> Ripetere "agenzia immobiliare Padova" 20 volte in una pagina e' **keyword stuffing** e causa penalizzazione.
> Google riconosce sinonimi, varianti e concetti correlati — il campo semantico conta piu' della singola keyword.
>
> **Neural Matching (RankEmbed):** Sistema AI di Google (attivo dal 2018, potenziato 2025-2026) che collega
> query e pagine a livello **concettuale profondo**, non solo lessicale. Funziona come **re-ranker**: prima
> Google recupera risultati con l'indice tradizionale, poi Neural Matching ri-ordina in base alla corrispondenza
> semantica. Una pagina su "cedere la proprieta' nel Padovano" puo' posizionarsi per "vendere casa a Padova"
> anche senza quelle keyword esatte — se il campo concettuale e' coperto.
> **Zero impatto tecnico** — sono regole editoriali, nessun script/CSS/codice aggiunto.

**Due livelli di ottimizzazione:**
- **Livello 1 — Lessicale:** evitare keyword stuffing, usare sinonimi e varianti (regole anti-ripetizione)
- **Livello 2 — Semantico profondo (Neural Matching):** coprire l'intero spazio concettuale del topic, allineare l'intento, garantire profondita' tematica

---

#### LIVELLO 1 — Regole Anti-Keyword-Stuffing

**Principio fondamentale:** Ogni pagina deve coprire un **campo semantico ricco** attorno all'entita' principale,
usando sinonimi, varianti, termini correlati e contesto. MAI ripetere la stessa frase esatta piu' di 3-4 volte per pagina.

**Regole operative:**

1. **Limite ripetizione keyword:** nessuna frase di 2+ parole deve apparire piu' di **5 volte** in una singola pagina (testo visibile, esclusi tag tecnici come schema JSON-LD)
2. **"a Padova" / "di Padova":** max **8-10 occorrenze** per pagina (prima erano 20-43 — keyword stuffing critico)
3. **Nome zona nelle pagine zona:** max **10-12 occorrenze** (prima erano 19-29)
4. **"Righetto Immobiliare":** max **3-4 menzioni** per pagina
5. **Title, H1, meta description:** devono usare **varianti diverse** della keyword, MAI la stessa frase esatta in tutti e tre
6. **H2:** almeno il 50% degli H2 deve usare **sinonimi o riformulazioni**, non ripetere la keyword del title

**Mappa sinonimi obbligatoria per il settore immobiliare:**

| Keyword esatta | Sinonimi e varianti da alternare |
|---|---|
| agenzia immobiliare | studio immobiliare, consulenza immobiliare, professionisti del settore, esperti del mercato locale |
| vendere casa | mettere in vendita un immobile, cedere la proprieta', alienare l'immobile, concludere la compravendita |
| comprare casa | acquistare un immobile, trovare la casa ideale, investire nel mattone, finalizzare l'acquisto |
| mutuo prima casa | finanziamento ipotecario, prestito per l'acquisto, credito immobiliare, piano di ammortamento |
| valutazione immobiliare | stima del valore, perizia dell'immobile, analisi comparativa di mercato, quotazione |
| affitto / locazione | contratto di locazione, canone mensile, soluzione in affitto, formula locativa |
| a Padova | nel capoluogo euganeo, nel Padovano, in citta', nel territorio patavino, nell'area metropolitana |
| mercato immobiliare | comparto residenziale, settore delle compravendite, panorama immobiliare, dinamiche di mercato |
| prezzi al mq | quotazioni medie, valori di mercato, costo per metro quadrato, listino immobiliare |
| zona/quartiere | rione, comprensorio, area residenziale, contesto urbano, realta' locale |
| virtual tour | visita virtuale 360, tour immersivo, esperienza digitale dell'immobile, sopralluogo da remoto |
| caparra confirmatoria | anticipo contrattuale, garanzia economica, deposito vincolante, somma a conferma |
| home staging | valorizzazione dell'immobile, allestimento per la vendita, preparazione scenica, restyling pre-vendita |
| investimento immobiliare | rendimento da locazione, operazione buy-to-let, asset nel mattone, reddito passivo immobiliare |

**Entita' correlate da includere (campo semantico):**

Per ogni pagina, Google si aspetta di trovare anche le **entita' collegate** al topic. Esempio:
- **Vendita casa:** rogito, notaio, visura catastale, APE, conformita' urbanistica, plusvalenza, agenzia delle entrate
- **Mutuo:** LTV, spread, TAEG, Euribor, IRS, perizia bancaria, ipoteca, piano ammortamento
- **Affitto:** cedolare secca, canone concordato, deposito cauzionale, registrazione contratto, sublocazione
- **Quartiere Padova:** servizi, scuole, trasporti, aree verdi, qualita' della vita, prezzi medi, trend demografico
- **Caparra:** codice civile art. 1385, clausola risolutiva, inadempimento, recesso, restituzione doppio

---

#### LIVELLO 2 — Neural Matching (Ottimizzazione Semantica Profonda)

> **Come funziona:** Google traduce query e pagine in **vettori nello stesso spazio multidimensionale**.
> Piu' il vettore della tua pagina e' vicino al vettore della query, piu' sei rilevante.
> Per avvicinare i vettori servono: copertura concettuale completa, intent match e profondita' tematica.
> **Impatto stimato:** guadagno di 5-15 posizioni su query non-brand (es. "agenzia immobiliare padova" da pos. 28 a pos. 13-18).

**1. Copertura Concettuale Completa (Topic Coverage)**

Ogni pagina deve rispondere non solo alla keyword principale, ma a TUTTE le domande
che un utente potrebbe avere su quel topic:

| Topic pagina | Concetti che DEVONO essere presenti |
|---|---|
| Vendita casa Padova | processo di vendita, tempistiche medie, documenti necessari, costi (notaio, agenzia, tasse), valutazione preliminare, come scegliere l'agenzia, errori da evitare, mercato attuale |
| Mutuo prima casa | requisiti reddituali, differenza tasso fisso/variabile, LTV, spread, Euribor/IRS, detrazioni fiscali, tempi approvazione, documenti banca, perizia, ipoteca |
| Quartiere (es. Arcella) | confini geografici, storia, servizi (scuole, trasporti, commercio), prezzi medi attuali, trend, pro/contro, tipologia abitanti, progetti urbanistici, confronto con quartieri simili |
| Affitto studenti Padova | canone medio per zona, cedolare secca, contratto transitorio vs 4+4, deposito cauzionale, diritti/doveri, universita' vicine, trasporti |

**Regola:** se un competitor copre 8 sottotopic su 10 e tu ne copri 5, Neural Matching favorira' il competitor
anche se le tue 5 sezioni sono scritte meglio.

**2. Intent Mapping — Una Pagina per Ogni Intento**

Neural Matching valuta l'allineamento tra l'**intento** della query e il **purpose** della pagina.
Non mischiare intenti diversi nella stessa pagina:

| Intento | Tipo pagina corretta | Errore da evitare |
|---|---|---|
| Informazionale ("come vendere casa") | Articolo blog/guida | Pagina servizio con CTA aggressive |
| Navigazionale ("righetto immobiliare") | Homepage/chi siamo | Redirect a landing promozionale |
| Transazionale ("valutazione casa gratis padova") | Landing page dedicata | Articolo blog generico |
| Commerciale ("migliore agenzia immobiliare padova") | Pagina pillar + recensioni | Lista servizi senza social proof |

**Regola:** title, H1 e primo paragrafo DEVONO dichiarare chiaramente l'intento della pagina
entro le prime 100 parole. Neural Matching decide la rilevanza nei primi secondi di analisi.

**3. Co-occorrenze Semantiche (Semantic Co-occurrence)**

Google si aspetta che certi concetti appaiano INSIEME. Se mancano, la pagina risulta incompleta:

| Topic | Coppie obbligatorie |
|---|---|
| Vendita | vendita + rogito + notaio + APE + conformita' urbanistica |
| Mutuo | mutuo + tasso + banca + perizia + ipoteca + LTV |
| Affitto | affitto + contratto + deposito + registrazione + cedolare secca |
| Valutazione | valutazione + comparativa + OMI + mq + classe energetica |
| Ristrutturazione | ristrutturazione + bonus + CILA + classe energetica + capitolato |
| Acquisto | acquisto + proposta + caparra + compromesso + rogito |

**Regola:** ogni articolo/pagina deve contenere almeno il **70% delle co-occorrenze** previste per il suo topic.

**4. Profondita' vs Superficialita' (Depth Signal)**

Neural Matching premia pagine che vanno in profondita' su UN topic
rispetto a pagine che toccano molti topic superficialmente.

**Segnali di profondita':**
- Dati numerici specifici e aggiornati (NON generici)
- Tabelle comparative con fonti (OMI, FIMAA, ISTAT)
- FAQ che rispondono a domande SPECIFICHE (non generiche)
- Esempi concreti localizzati (es. "un trilocale in zona Arcella a 185.000 euro" > "una casa a Padova")
- Citazioni di normative specifiche (art. 1385 c.c., D.Lgs. 28/2010)

**Regola:** meglio 1 articolo da 3.000 parole che copre tutto il topic
che 3 articoli da 1.000 parole che si sovrappongono (cannibalizzazione).

**5. Freshness Signal per Neural Matching**

Le pagine con contenuti aggiornati ricevono un boost nel re-ranking:
- **Timestamp visibile** "Ultimo aggiornamento: [data]" su ogni pagina cornerstone
- **Aggiornare dati** OMI/prezzi almeno ogni trimestre
- **Aggiungere sezioni** quando cambiano normative o mercato
- **dateModified** nello schema JSON-LD DEVE corrispondere all'ultimo aggiornamento reale

---

#### COME APPLICARE IN PRATICA (Livello 1 + Livello 2)

1. Prima stesura: scrivi naturalmente coprendo TUTTI i sottotopic previsti (vedi tabella Topic Coverage)
2. Verifica intent: il title e primo paragrafo dichiarano chiaramente l'intento? (informazionale/transazionale/commerciale)
3. Review keyword: cerca ogni frase ripetuta 4+ volte e sostituisci almeno il 50% con sinonimi dalla mappa sopra
4. Review co-occorrenze: verifica che almeno il 70% delle coppie semantiche obbligatorie sia presente
5. H2: riformula come domande naturali, non come ripetizioni del title
6. Primo paragrafo dopo H2: usa la keyword esatta (per GEO/AEO), poi alterna con varianti
7. Meta description: usa una variante diversa dal title
8. Aggiungi entita' correlate nel testo — arricchiscono il campo semantico senza forzare la keyword
9. Verifica profondita': ci sono dati numerici specifici, tabelle, esempi localizzati, riferimenti normativi?
10. Timestamp: aggiorna "Ultimo aggiornamento" e dateModified nello schema

**Esempio pratico — PRIMA (keyword stuffing):**
> "Il **mutuo prima casa a Padova** e' la soluzione per chi vuole comprare. Il **mutuo prima casa a Padova** offre tassi agevolati. Con il **mutuo prima casa a Padova** puoi risparmiare."

**Esempio pratico — DOPO (entity-based SEO + Neural Matching):**
> "Il **mutuo prima casa a Padova** e' la soluzione piu' richiesta nel 2026. Il **finanziamento ipotecario** per l'acquisto della prima abitazione prevede tassi agevolati (Euribor + spread). Con un **prestito immobiliare** nel capoluogo euganeo, le famiglie possono accedere a **detrazioni IRPEF** sugli interessi passivi fino a 4.000 euro/anno. La **perizia bancaria** richiede in media 10-15 giorni, con un LTV massimo dell'80% del valore stimato dall'istituto di credito."

#### CHECKLIST NEURAL MATCHING — Prima di Pubblicare

- [ ] La pagina copre almeno l'80% dei sottotopic previsti per la keyword principale?
- [ ] L'intento (informazionale/transazionale/commerciale) e' chiaro entro le prime 100 parole?
- [ ] Sono presenti almeno il 70% delle co-occorrenze semantiche obbligatorie per il topic?
- [ ] Ci sono dati numerici specifici e localizzati (non generici)?
- [ ] Le FAQ rispondono a domande reali e specifiche (non filler)?
- [ ] Il timestamp e' aggiornato e coerente con dateModified nello schema?
- [ ] La pagina va in profondita' su UN topic (no multi-topic superficiale)?
- [ ] Nessuna frase di 2+ parole ripetuta piu' di 5 volte?
- [ ] Title, H1 e meta description usano varianti diverse?

**Registrazione quadrupla (gia' in sezione 1.2, ribadita):**
1. `admin.html` → `_blogSeedArticles` (**OBBLIGATORIO:** campo `data_pubblicazione: 'YYYY-MM-DD'`)
2. `blog.html` → `articoliStatici`
3. `js/homepage.js` → `staticMap` + `articoliStatici`
4. `sitemap.xml` → URL con lastmod e priority 0.8

> **ATTENZIONE — data_pubblicazione:** Senza questo campo la colonna "Pubblicazione" nell'admin mostra "—" e non e' possibile tracciare quando l'articolo e' stato pubblicato. Il validatore automatico (`validate-page.js`) blocca il commit se manca. Usare la data di pubblicazione effettiva in formato YYYY-MM-DD (es. `data_pubblicazione: '2026-03-15'`).

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

### 9.1b Audit Completo SKILL 2.0 — 16 Marzo 2026 (50 file corretti)

**SEO Tecnico:**
- [x] **Meta description** — accorciate a ≤158 char su 18 pagine (articolo-riqualificazione, 11 blog, cookie-policy, landing-calcolo-mutuo, servizi, 3 zone)
- [x] **Title tag** — accorciati a ≤68 char su 4 pagine (articolo-riqualificazione, landing-chat-offerta-gas, landing-vendere-casa-padova, offerta-enel-luce)
- [x] **Link .html** — corretto 1 link in landing/email-offerta-luce.html (rimosso .html e www)
- [x] **URL pulite** — verificate su tutte le pagine: nessun link interno con .html
- [x] **Canonical e OG tags** — verificati su tutte le pagine principali

**Schema.org:**
- [x] **articolo-riqualificazione.html** — aggiunto sameAs, GeoCoordinates, aggregateRating al RealEstateAgent
- [x] **3 blog (scuole, servizi, trasporti)** — aggiunto wordCount al BlogPosting schema
- [x] **servizio-virtual-tour.html** — aggiunto Person schema (Gino Capon) per coerenza con altri servizi

**Zone Pages (14):**
- [x] **Sezione Pro/Contro** — aggiunta a tutte le 14 pagine zona (4 Pro + 4 Contro per zona, onesti per E-E-A-T)
- [x] **5a FAQ** — aggiunta allo schema FAQPage di 13 zone (abano-terme ne aveva gia' 5)

**Blog (40+):**
- [x] **Timestamp "Aggiornato: marzo 2026"** — aggiunto a 17 articoli che ne erano privi (ora 40/40 con timestamp visibile)

**Sitemap e llms.txt:**
- [x] **sitemap.xml** — verificato, 2 pagine landing gia' presenti (erano state aggiunte in precedenza)
- [x] **llms.txt** — verificato completo, tutte le 14 zone e 40 blog presenti
- [x] **robots.txt** — AI bots tutti Allow (GPTBot, ClaudeBot, Google-Extended, PerplexityBot)

**Indicizzazione Google (verificata 16 marzo 2026):**
- Le vecchie pagine WordPress sono ancora indicizzate — Google le sta sostituendo gradualmente
- Brand queries funzionano (pos. 1.3 per "agenzia righetto limena")
- Non-brand keyword ancora deboli — DA troppo bassa
- March 2026 Core Update: pesa su Gemini 4.0 Semantic Filter, Information Gain, CWV a livello sito
- GEO: 58% consumatori usa AI, 99% citazioni AI Overview da top 10 organica

**Decisioni prese:**
1. **Pro/Contro obbligatorio** — ogni nuova zona page DEVE avere sezione Pro/Contro (credibilita' E-E-A-T)
2. **5 FAQ minimo** — confermato come standard per zone pages (schema FAQPage)
3. **Timestamp obbligatorio** — ogni articolo blog DEVE avere "Aggiornato: [mese anno]" visibile
4. **llms.txt completo** — deve essere aggiornato ad ogni nuovo contenuto (tutte le zone e blog)

### 9.1c Lead Conversion Engine — 16 Marzo 2026 (14 pagine aggiornate)

**js/lead-conversion.js — 10 sistemi integrati (651 righe, vanilla JS, zero dipendenze):**
- [x] **A/B test engine** — 4 test attivi (hero CTA, nav CTA, mobile CTA, sticky CTA), varianti persistite in localStorage
- [x] **GA4 CTA tracking** — 14 selettori tracciati con eventi custom (cta_click, form_submit), dati A/B variant inclusi
- [x] **Speed-to-lead** — conferma personalizzata post-form con nome utente, tempo risposta "< 30 min", stato live, CTA immediati (tel + WhatsApp), flag sessionStorage per disabilitare exit intent
- [x] **Segmentazione lead** — rilevamento intento acquirente/venditore dal campo oggetto, placeholder dinamici, dati comportamentali salvati
- [x] **Social proof dinamica** — 8 notifiche a rotazione su desktop (incluse trust badges: recensioni Google + statistiche agenzia), ogni 45 secondi, icona star per reviews
- [x] **Exit intent popup** — popup segmentato (venditore vs acquirente), CTA personalizzata, urgency badge ("Disponibilita' limitata — rispondiamo entro 30 minuti"), social proof reviews, una sola volta per sessione
- [x] **Scroll depth tracking** — milestone 25/50/75/90%
- [x] **Time on page tracking** — eventi a 30s, 60s, 120s, 300s
- [x] **Sticky CTA mobile auto-inject** — genera automaticamente barra CTA su mobile per le 8 pagine che non l'avevano (landing-valutazione, landing-agente, landing-vendere-casa-padova, servizi, servizio-vendita, servizio-valutazioni, servizio-locazioni, chi-siamo), con CTA e colore personalizzati per pagina
- [x] **Homepage form compatibility** — speed-to-lead e segmentazione adattati ai form homepage (ID diversi: contattoForm, cf-nome, cf-interesse, cf-ok), observer su MutationObserver per intercettare il successo

**Pagine aggiornate (14 totali):**
- [x] index.html, contatti.html
- [x] landing-vendita, landing-valutazione, landing-mutuo, landing-calcolo-mutuo, landing-agente, landing-vendere-casa-padova
- [x] servizi, servizio-vendita, servizio-valutazioni, servizio-locazioni
- [x] chi-siamo, vendere-casa-padova-errori

**Altre modifiche:**
- [x] **Video testimonial** — 2 video con facade YouTube lazy-load nella sezione testimonial homepage
- [x] **Speed-to-lead contatti.html** — messaggi aggiornati ("Ti ricontattiamo entro pochi minuti"), form hero e success migliorati
- [x] **Sticky CTA mobile** — gia' presente su 6 pagine + auto-inject JS su 8 restanti, ora A/B testato

### 9.2 Contenuti da Creare
- [x] **Blog / landing — CTA chiusura 8.1b** — (3 aprile 2026) rimossa CTA rossa duplicata; `blog-rich-cta-strip` + CSS su tutti i `blog-*.html` interessati e landings con form. Restano miglioramenti **editoriali** graduali (TOC, fonti, badge data) per articoli a bassa priorita' GSC.
- [ ] **Blog statici — arricchimento corpo 8.1b** (prosa, `blog-rich-toc`, tabelle con `blog-rich-table-source` dove servono dati):
  priorita' pillar + top click GSC; script di supporto in `scripts/` come sopra.
- [x] blog-tempi-vendita-casa-padova.html — CREATO 8 marzo 2026
- [x] zona-vigonza.html — CREATA 8 marzo 2026
- [x] zona-abano-terme.html — CREATA 8 marzo 2026
- [x] zona-selvazzano.html — CREATA 8 marzo 2026
- [ ] Bollino "Verificato Righetto" — brand quality sugli annunci

### 9.3 Ottimizzazioni Performance
- [x] **Supabase Image Transforms** — 13 Marzo 2026: `resolveImageUrl()` in `homepage.js`, `immobile.html`, `immobili.html` ora usa `/storage/v1/render/image/public/` con parametri `width` e `quality` per ridimensionare le immagini al volo. Risparmio stimato: ~2300 KiB (~85%) sulle immagini Supabase. Dimensioni: card homepage/listing width=600 q=75, gallery hero width=1200 q=80, thumbnails width=300 q=70, lightbox full-size originale.
- [x] **Cache-busting ?v=N su tutti i CSS/JS** — 18 Marzo 2026: aggiunto parametro `?v=3` a tutti i riferimenti CSS e JS in 88 file HTML. Cache CSS/JS estesa da 1 mese a 1 anno con flag `immutable` nel `.htaccess`. Il cache-busting garantisce refresh immediato ad ogni aggiornamento incrementando il numero di versione.
- [x] **Immagini WebP come formato primario** — tutti i `<picture>` e `<img>` puntano direttamente a `.webp`. I file `.png` nella cartella `img/foto-servizi/` sono ridondanti e possono essere eliminati (nessun HTML li referenzia).
- [ ] LCP sotto 2 secondi su tutte le pagine (nuovo target competitivo)
- [ ] Verificare SVT — nessun caricamento "scattoso" (font swap, image pop-in)
- [ ] Verificare Engagement Reliability — form, bottoni, menu funzionano su tutti i device
- [ ] Page Experience consistency — tutte le pagine devono avere performance simile
- [ ] **Cache headers GitHub Pages** — il TTL di 10 minuti sulle risorse proprietarie (fonts, CSS, JS, immagini locali) e' un limite di GitHub Pages non modificabile. Valutare Cloudflare come proxy per cache piu' aggressiva.

### 9.3b Strategia Cache e Performance — Regole per Ogni Nuovo Sito

> **Applicabile a qualsiasi sito statico su hosting tradizionale (cPanel, Plesk, VPS).**
> GitHub Pages ha limiti diversi (cache 10 min non modificabile, no .htaccess).

**1. Cache-Busting obbligatorio su CSS/JS:**
- OGNI riferimento CSS e JS negli HTML DEVE avere un parametro `?v=N` (es. `css/fonts.css?v=3`)
- Quando modifichi un CSS o JS, incrementa il numero di versione in TUTTI gli HTML che lo referenziano (es. `?v=3` → `?v=4`)
- Questo permette di tenere cache molto lunga (1 anno) senza rischio di servire versioni vecchie
- **MAI** linkare CSS/JS senza parametro `?v=` — la cache del provider/browser servira' la versione vecchia

**2. .htaccess — Configurazione cache standard:**
```apache
# Immagini e font: 1 anno, immutable
ExpiresByType image/webp "access plus 1 year"
ExpiresByType image/jpeg "access plus 1 year"
ExpiresByType image/png "access plus 1 year"
ExpiresByType image/svg+xml "access plus 1 year"
ExpiresByType font/woff2 "access plus 1 year"
Header set Cache-Control "public, max-age=31536000, immutable"

# CSS e JS: 1 anno con cache-busting via ?v=
ExpiresByType text/css "access plus 1 year"
ExpiresByType application/javascript "access plus 1 year"
Header set Cache-Control "public, max-age=31536000, immutable"

# HTML: mai cachare (sempre fresco)
ExpiresByType text/html "access plus 0 seconds"
Header set Cache-Control "no-cache, must-revalidate"

# Compressione Gzip obbligatoria
AddOutputFilterByType DEFLATE text/html text/css application/javascript text/javascript application/json image/svg+xml

# ETag disabilitato (usa Cache-Control)
Header unset ETag
FileETag None
```

**3. Formato immagini:**
- Usare SEMPRE WebP come formato primario (30-50% piu' leggero di PNG/JPEG)
- Se servono fallback per browser vecchi, usare tag `<picture>` con `<source type="image/webp">` + `<img src="fallback.jpg">`
- Se il sito non ha utenti su browser vecchi (IE11), puntare direttamente a `.webp` senza fallback
- **NON tenere PNG/JPEG duplicati nel repo se nessun HTML li referenzia** — sono peso morto

**4. Security Headers (standard per ogni sito):**
```apache
Header set X-Content-Type-Options "nosniff"
Header set X-Frame-Options "SAMEORIGIN"
Header set Referrer-Policy "strict-origin-when-cross-origin"
Header set Permissions-Policy "geolocation=(), microphone=(), camera=()"
```

**5. Redirect www → non-www (o viceversa):**
- Scegliere UNA versione e fare redirect 301 permanente
- Per Righetto: senza www (`righettoimmobiliare.it`)

**6. Checklist performance per ogni nuovo sito:**
- [ ] `.htaccess` con cache 1 anno per statici + cache-busting `?v=` su CSS/JS
- [ ] Compressione Gzip attiva
- [ ] Immagini in formato WebP
- [ ] Font con `font-display: swap` + preload above-fold
- [ ] CSS critical inline, rest deferred (`media="print" onload="this.media='all'"`)
- [ ] JS con `defer` (mai `async` per script che dipendono l'uno dall'altro)
- [ ] Nessun `loading="lazy"` above-the-fold
- [ ] Security headers attivi
- [ ] ETag disabilitato (Cache-Control basta)
- [ ] Redirect www configurato

### 9.4 SEO Tecnico
- [ ] **Contenuti unici vs portali** — le descrizioni immobili su Idealista/Immobiliare.it DEVONO essere diverse da quelle sul sito (rischio duplicate content e deindexing)
- [ ] Internal linking tra blog posts e zone pages (cross-link contestuali)
- [ ] Verificare indexing in Google Search Console
- [ ] Richiedere indicizzazione manuale nuove pagine via GSC
- [ ] Verificare che recensioni Google non siano sparite (nuove policies)
- [x] Aggiungere video content — video testimonial con facade YouTube in homepage (virtual tour dedicato ancora da fare)
- [ ] UTM tags su link GBP per tracciare traffico in GA4
- [ ] Valutare hreflang se si prevede versione EN per clientela internazionale

### 9.5 Conversione e Lead Generation — 3a PASSATA DEFINITIVA 16 Marzo 2026 (9.9/10)
- [x] **Speed-to-lead:** conferma istantanea personalizzata con nome, tempo risposta "< 30 min", stato richiesta live, CTA telefono + WhatsApp immediati post-form, flag sessionStorage per disabilitare exit intent
- [x] **A/B test CTA:** sistema vanilla JS con localStorage, 4 test attivi (hero CTA, nav CTA, mobile CTA, sticky CTA), varianti tracciate via GA4
- [x] **Lead magnet segmentati:** rilevamento intento acquirente/venditore dal campo oggetto, placeholder form dinamici, routing comportamentale, dati segmentazione salvati
- [x] **Video testimonial:** sezione video con lazy-load YouTube (click-to-play), 2 video con facade pattern per performance, integrata nella homepage
- [x] **GA4 CTA tracking:** 14 selettori tracciati (btn-g, btn-p, nav-cta, sticky, WhatsApp, tel, form), eventi con A/B variant, page path, cta text
- [x] **Social proof dinamica:** 8 notifiche a rotazione su desktop (incluse trust badges: 127 recensioni 4.9/5 + 350+ immobili dal 2000), ogni 45s, icona star dedicata
- [x] **Exit intent popup:** popup segmentato venditore/acquirente con **urgency badge** ("Disponibilita' limitata — rispondiamo entro 30 minuti"), CTA personalizzata, social proof reviews
- [x] **Scroll depth + time tracking:** milestone 25/50/75/90% scroll, tempo 30s/60s/120s/300s tracciati via GA4
- [x] **Sticky CTA mobile universale:** presente su TUTTE le 14 pagine — 6 con HTML manuale + 8 con auto-inject JS (lead-conversion.js crea automaticamente la barra se non esiste), CTA e colore personalizzati per tipo pagina
- [x] **Homepage form compatibility:** speed-to-lead e segmentazione adattati ai form homepage (ID diversi), MutationObserver per intercettare il successo
- [ ] **Siti <2s convertono 3x** meglio dei siti lenti — priorita' LCP (gia' buono, target <2s)

### 9.6 GEO/AEO — COMPLETATI 8 Marzo 2026
- [x] **Lotto zona Aprile 2026** — tutte le `zona-*.html`: correzione chiusura hero (`</section></div>...`), blocco **FAQ visibile** (`<details>`) prima del CTA allineato al JSON-LD FAQPage gia' presente, CSS `.zona-faq-*`. Script: `scripts/zona_aeo_faq_visible.py` (rieseguibile; salta se sezione gia' presente).
- [x] **blog-articolo.html** — `injectFaqJsonLd(art)`: genera/rimuove `<script id="jsonld-faq">` FAQPage da `art.faq` (Supabase) dopo il render; su articolo non trovato rimuove il blocco.
- [x] **H2 in formato domanda** su ogni sezione `.sec` delle pagine `zona-*.html` — titoli riscritti (Aprile 2026). Script: `scripts/apply_zona_h2_aeo.py`. Snippet visivo: regola CSS sul primo `<p>` in `.sec-text`.
- [x] **Blog statici H2 AEO** — `scripts/apply_blog_h2_aeo.py` (pattern ripetuti + guide/strategie) e `scripts/apply_blog_h2_question_suffix.py` (suffisso `?` controllato sui titoli senza interrogativo). Escluso `blog-articolo.html` (dinamico).
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
- [ ] **Tutti i CSS/JS con `?v=N`** — mai linkare senza parametro cache-busting
- [ ] Link interni verso pagine correlate
- [ ] Registrato in sitemap.xml
- [ ] Frasi dichiarative prime 2 righe (GEO)
- [ ] Dati numerici specifici (GEO)
- [ ] Min 5 FAQ con Schema FAQPage (AEO)
- [ ] Author bio visibile con link a pagina autore (E-E-A-T)
- [ ] **Se landing page:** registrata in `_landingSeedPages` di admin.html con `data_pubblicazione: 'YYYY-MM-DD'`

### Per Ogni Nuovo Articolo Blog
- [ ] Tutti i punti sopra
- [ ] Registrato in TUTTI e 4: admin.html, blog.html, homepage.js, sitemap.xml
- [ ] **`data_pubblicazione: 'YYYY-MM-DD'`** presente nel seed `_blogSeedArticles` di admin.html (BLOCCANTE)
- [ ] Cross-link con zone pages e service pages correlate
- [ ] Timestamp "Ultimo aggiornamento" visibile

### Per Ogni Nuova Zona Page
- [ ] Tutti i punti "Per Ogni Nuova Pagina"
- [ ] Schema Place con GeoCoordinates + sameAs
- [ ] Schema RealEstateAgent con aggregateRating
- [ ] **Sezione Pro/Contro** — 4 Pro + 4 Contro, lista onesta (credibilita' E-E-A-T)
- [ ] **Minimo 5 FAQ** nello schema FAQPage + visibili nel body se applicabile
- [ ] Registrato in blog.html (array articoliStatici con categoria "Mercato locale")
- [ ] Registrato in sitemap.xml
- [ ] Aggiornato llms.txt con nuova zona e prezzi
- [ ] Aggiunto link nel footer di tutte le zone pages

### Verifiche Post-Modifica (AUTOMATICHE via pre-commit hook)
- `node scripts/validate-page.js --staged` — valida automaticamente
- Schema mancante = commit BLOCCATO
- Title mancante = commit BLOCCATO
- `data_pubblicazione` mancante nel seed admin.html = commit BLOCCATO (blog e landing)
- Landing page non registrata in `_landingSeedPages` = WARNING
- Meta description troppo lunga = WARNING (passa)

### Audit Automation (Admin)
- **Pulsante "Lancia Analisi Skill"** nell'admin → esegue audit completo + carica analisi Claude
- Storico salvato in `data/audit-analyses.json` con data, ora, risultati audit, problemi, analisi completa e sintesi
- Ogni analisi include: stato audit (OK/warning/errori), azioni prioritarie, stato KPI, TODO aperti
- La tabella "Storico Analisi Skill" mostra cronologia cliccabile con sintesi per ogni run
- Per aggiungere una nuova analisi: Claude esegue audit, analizza risultati con SKILL, salva in JSON

### Verifiche Manuali Periodiche
- [ ] Contrasto WCAG: mai var(--oro) come bg con testo bianco (ratio 1.54:1 = FAIL)
- [ ] Allineamento array: blog.html, homepage.js, admin.html devono avere gli stessi articoli
- [ ] robots.txt: AI bots (GPTBot, ClaudeBot, Google-Extended, PerplexityBot) NON bloccati
- [ ] llms.txt: aggiornato con nuovi contenuti e prezzi
- [ ] Timestamp cornerstone: aggiornare ogni mese

---

## 13. DESIGN SYSTEM UNIVERSALE

> Estratto e generalizzato dal progetto Righetto Immobiliare. Replicabile su qualsiasi settore.

### 13.1 Variabili CSS

```css
:root {
  /* === COLORI PRIMARI === */
  --primario:    #2C4A6E;   /* Colore brand principale */
  --primario-2:  #3A5F8C;   /* Hover state */
  --primario-3:  #4E789A;   /* Accento light */

  /* === COLORI ACCENT (CTA) — ARANCIONE CONVERSIONE === */
  --accent:      #FF6B35;   /* CTA primario arancione — SOLO con testo scuro */
  --accent-2:    #FF8F5E;   /* Hover CTA */
  --accent-3:    #FFB899;   /* Accent extra light */
  --accent-bg:   rgba(255,107,53,0.10); /* Background badge */

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

**REGOLA colori personalizzati:** Quando si cambia colore primario:
1. Sostituire `--primario` col colore scelto
2. Calcolare `--primario-2` (+15% luminosita') e `--primario-3` (+30% luminosita')
3. Verificare contrast ratio >= 4.5:1 per testo su sfondo
4. Se `--accent` su sfondo chiaro ha contrast < 4.5:1 → usare SOLO con testo scuro

### 13.2 Tipografia

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

### 13.3 Spacing System

| Contesto | Desktop | Tablet | Mobile |
|----------|---------|--------|--------|
| Sezione padding | 90px 44px | 60px 28px | 60px 20px |
| Card padding | 28px 24px | 24px 20px | 20px 16px |
| Grid gap | 24px | 24px | 16px |
| Eyebrow → Heading | 12px–22px | — | — |
| Heading → Content | 22px–32px | — | — |
| Content → CTA | 40px | — | — |
| Form field gap | 16px | — | — |

### 13.4 Breakpoint Responsive

| Breakpoint | Target | Azione |
|------------|--------|--------|
| `max-width: 1024px` | Laptop | Grid 3→2 colonne |
| `max-width: 900px` | Tablet landscape | Footer/form collapse |
| **`max-width: 768px`** | **Tablet portrait** | **Navbar → hamburger, grid → 1 col** |
| `max-width: 600px` | Mobile grande | Card grid → 1 col, padding ridotto |
| `max-width: 520px` | Mobile piccolo | Popup/modal compatti |

### 13.5 Shadow System

```css
/* Livelli di elevazione */
--shadow-xs:  0 2px 16px rgba(21,36,53,0.05);    /* Card base */
--shadow-sm:  0 6px 20px rgba(21,36,53,0.08);     /* Card hover lieve */
--shadow-md:  0 20px 50px rgba(21,36,53,0.14);    /* Card hover forte */
--shadow-lg:  0 30px 100px rgba(0,0,0,0.4);       /* Hero/overlay */
--shadow-cta: 0 6px 20px rgba(184,212,74,0.35);   /* CTA button glow */
```

### 13.6 Animazioni

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

/* Hero background zoom */
@keyframes slowZoom { from { transform: scale(1.05); } to { transform: scale(1.10); } }

/* Fade up ingresso */
@keyframes fadeUp { from { opacity: 0; transform: translateY(36px); } to { opacity: 1; transform: translateY(0); } }

/* Card lift hover */
.card-lift { transition: transform 0.3s var(--ease-bounce), box-shadow 0.3s ease; }
.card-lift:hover { transform: translateY(-6px); box-shadow: var(--shadow-md); }

/* Link underline reveal */
.link-reveal { position: relative; }
.link-reveal::after {
  content: ''; position: absolute; bottom: -2px; left: 0;
  width: 0; height: 2px; background: var(--accent);
  transition: width 0.35s var(--ease-out);
}
.link-reveal:hover::after { width: 100%; }

/* Accessibilita': rispetta preferenze utente */
@media (prefers-reduced-motion: reduce) {
  .sr, .sr-left, .sr-right, .sr-scale { opacity: 1; transform: none; transition: none; }
}
```

---

## 14. COMPONENTI E TEMPLATE HTML

### 14.1 Card Grid

```html
<div class="card-grid">
  <div class="card card-lift sr sr-d1">
    <div class="card-icon">[emoji/svg]</div>
    <h3 class="card-title">[Titolo]</h3>
    <p class="card-desc">[Descrizione]</p>
    <a href="#" class="card-link link-reveal">Scopri di piu' →</a>
  </div>
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

### 14.2 CTA Buttons

```css
/* Primario — accent su sfondo scuro */
.btn-accent {
  display:inline-block; background:var(--accent); color:var(--nero);
  padding:15px 32px; border-radius:var(--radius-sm);
  font-family:'Montserrat',sans-serif; font-weight:800; font-size:0.78rem;
  letter-spacing:1px; text-transform:uppercase; transition:all 0.25s;
}
.btn-accent:hover { background:var(--accent-2); transform:translateY(-2px); box-shadow:var(--shadow-cta); }

/* Secondario — outline su sfondo scuro */
.btn-outline {
  display:inline-block; border:1px solid rgba(255,255,255,0.2); color:#fff;
  padding:15px 32px; border-radius:var(--radius-sm);
  font-family:'Montserrat',sans-serif; font-weight:600; font-size:0.78rem;
  letter-spacing:1px; text-transform:uppercase; transition:all 0.25s;
}
.btn-outline:hover { border-color:var(--accent); color:var(--accent); }

/* Terziario — scuro su sfondo chiaro */
.btn-dark {
  display:inline-block; background:var(--nero); color:#fff;
  padding:15px 32px; border-radius:var(--radius-sm);
  font-family:'Montserrat',sans-serif; font-weight:700; font-size:0.78rem;
  letter-spacing:1px; text-transform:uppercase; transition:all 0.25s;
}
.btn-dark:hover { background:var(--accent); color:var(--nero); transform:translateY(-2px); }
```

### 14.3 Form Contatti

```html
<div class="form-box">
  <div class="form-head">
    <h3>[Titolo Form]</h3>
    <p>[Sottotitolo]</p>
  </div>
  <form class="form-body">
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
```

### 14.4 FAQ / Accordion

```html
<div class="faq-list">
  <div class="faq-item sr">
    <button class="faq-btn" aria-expanded="false">
      <span class="faq-q">[Domanda]</span>
      <span class="faq-icon">+</span>
    </button>
    <div class="faq-answer"><p>[Risposta]</p></div>
  </div>
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
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    if (!wasOpen) item.classList.add('open');
    btn.setAttribute('aria-expanded', !wasOpen);
  });
});
```

---

## 15. I 4 LOOP DI VALIDAZIONE

> Ogni volta che Claude genera o modifica una pagina, DEVE eseguire questi 4 loop **in sequenza**.
> Ogni loop ricontrolla **tutta la struttura del sito** e **tutte le regole** da capo.

### LOOP 1 — STRUTTURA & HTML (25 check per pagina)

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
| 10 | Skip link primo elemento del body | Accessibilita' | Aggiungere |
| 11 | `<header>` con navbar presente | Struttura | Aggiungere |
| 12 | Nav-mobile con hamburger menu | Struttura | Aggiungere |
| 13 | Breadcrumb presente (se non homepage) | SEO | Aggiungere |
| 14 | `<main id="main-content">` presente | Accessibilita' | Aggiungere |
| 15 | Hero section come prima sezione | Struttura | Riordinare |
| 16 | Sezioni con classe `.sec` + `.sec-inner` | Struttura | Correggere |
| 17 | Footer completo (brand, link, legal) | Struttura | Aggiungere |
| 18 | JS deferred in fondo al body | Performance | Spostare/aggiungere defer |
| 19 | Tutte le immagini con `width` + `height` | Performance | Aggiungere |
| 20 | Tutte le immagini con `alt` text | Accessibilita' | Aggiungere |
| 21 | Hero image con `loading="eager"` | Performance | Correggere |
| 22 | Immagini below-fold con `loading="lazy"` | Performance | Aggiungere |
| 23 | Formato WebP per immagini locali | Performance | Segnalare |
| 24 | `aria-label` su bottoni icon-only | Accessibilita' | Aggiungere |
| 25 | `aria-hidden="true"` su SVG decorativi | Accessibilita' | Aggiungere |

### LOOP 2 — SEO & SCHEMA (25 check per pagina)

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
| 13 | Schema JSON-LD attivita' (tipo corretto) | Schema | Aggiungere |
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
| 25 | Contrast ratio CTA >= 4.5:1 | Accessibilita' | Correggere colori |

### LOOP 3 — COERENZA GLOBALE & REGISTRI (18 check)

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

### LOOP 4 — PERFORMANCE & MOBILE (25 check)

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
| 24 | `prefers-reduced-motion` rispettata | Accessibilita' | Aggiungere media query |
| 25 | Scrollbar custom presente e coerente | Design | Aggiungere CSS |

**Report finale Loop 4:**
- Totale check eseguiti: 93 per pagina × N pagine + 18 globali
- Fix applicati automaticamente
- Warning che richiedono decisione dell'utente
- Stato: PASS / FAIL per ogni loop
- Score stimato Lighthouse (Performance, Accessibility, SEO, Best Practices)

---

## 16. CHANGELOG

### v3.2 - 19 Marzo 2026 (Audit Automatico SKILL-2.0 via GitHub Actions)
- **Nuovo workflow GitHub Actions** (`.github/workflows/audit-settimanale.yml`): audit automatico ogni venerdi' alle 07:00 CET
- **Script audit** (`scripts/audit-skill.sh`): 16 controlli per pagina + controlli globali + controlli specifici blog/zone/servizi
- **Issue GitHub automatica** con label `audit` e report completo in markdown
- **Email riepilogativa** a info@righettoimmobiliare.it tramite API relay interno
- **Secret GitHub:** `EMAIL_RELAY_KEY` configurato per invio email automatico
- **Eseguibile manualmente** dal tab Actions → "Audit Settimanale SKILL-2.0" → Run workflow
- **Autorizzazione permanente** — gira automaticamente finche' non disabilitato
- **Documentazione aggiunta** nella sezione 3.4 (Strumenti Admin)

### v3.1 - 18 Marzo 2026 (Cache-busting + Strategia Performance per nuovi siti)
- **Cache-busting `?v=3` su 88 file HTML** — tutti i riferimenti CSS e JS ora hanno parametro di versione
- **Cache CSS/JS estesa a 1 anno** con flag `immutable` nel `.htaccess` (prima era 1 mese)
- **Nuova sezione 9.3b "Strategia Cache e Performance"** — regole replicabili per ogni nuovo sito su hosting tradizionale: configurazione .htaccess standard, cache-busting obbligatorio, formato WebP, security headers, checklist completa
- **Checklist aggiornata** (sezione 12) — aggiunto punto "Tutti i CSS/JS con `?v=N`" nella checklist "Per Ogni Nuova Pagina"
- **Confermato:** i file `.png` in `img/foto-servizi/` sono ridondanti (nessun HTML li referenzia, solo `.webp` usati)

### v3.0 - 15 Marzo 2026 (SKILL 2.0 — Fusione completa 3 documenti)
- **Fusione SKILL-UNIFICATA.md + AUTOMATION-SITE-2026.md + CLAUDE.md** in un unico documento master
- **Regole 10-13 da CLAUDE.md:** URL pulite (no .html), auto-registrazione admin, data pubblicazione obbligatoria, Entity-Based SEO (no keyword stuffing)
- **Sezione 13 — Design System Universale:** variabili CSS, tipografia, spacing system, breakpoint responsive, shadow system, animazioni con easing curves e scroll reveal
- **Sezione 14 — Componenti e Template HTML:** card grid, CTA buttons (accent/outline/dark), form contatti, FAQ accordion con toggle JS
- **Sezione 15 — 4 Loop di Validazione (93+ check):** Loop 1 Struttura (25), Loop 2 SEO & Schema (25), Loop 3 Coerenza Globale (18), Loop 4 Performance & Mobile (25)
- **Sezione 12.7 — Audit Automation:** pulsante "Lancia Analisi Skill" nell'admin con storico analisi in JSON
- **Entity-Based SEO + Neural Matching** confermato in sezione 8.3 con mappa sinonimi completa, regole anti-keyword-stuffing, copertura concettuale, intent mapping, co-occorrenze semantiche e checklist pre-pubblicazione
- **Checklist aggiornata** con verifiche audit automation

### v2.4 - 12 Marzo 2026 (Scraping 3-step: Topic → Foto → Preview con contenuto ricco)
- **Modal scraping a 3 step:** Step 1 scelta topic (9 categorie + custom + Google News), Step 2 gestione foto (hero + 3 inline con ricerca Unsplash o URL personalizzato), Step 3 anteprima con conferma e salvataggio
- **Foto hero + 3 inline:** ricerca Unsplash royalty-free integrata (6 risultati per query, click per selezionare), possibilità di incollare URL propri — MAI riutilizzare immagini già presenti nel sito
- **Contenuto ricco generato:** tabella prezzi/mq per 8 zone Padova con variazione % e tempi vendita, highlight box con 4 statistiche chiave, tabella attrattività investimento per zona, blockquote citazione Gino Capon, lista errori numerata
- **Figure con didascalia:** immagini inline distribuite tra le sezioni con `<figure><img><figcaption>` e crediti fotografo
- **Immagini in pagina:** **vietati** `images.unsplash.com`, `source.unsplash.com` e CDN esterni per asset editoriali; usare solo file in `img/` (self-hosted). Per anteprime admin usare path locali o `img/og-default.webp`, non generatori remoti.
- **REGOLA IMMAGINI:** ogni nuovo articolo deve avere foto coerenti e licenziabili; preferire scatti/commissioni propri o stock gia' in repo — vedi anche **8.1c** (WebP hero).

### v2.3 - 12 Marzo 2026 (Fix 404 articoli + template dinamico migliorato)
- **Fix link 404 articoli scraping:** gli articoli creati dallo scraping non hanno file HTML fisico — ora il link nell'admin punta correttamente a `blog-articolo?s=slug` (template dinamico) invece di `/slug` (file inesistente)
- **Template blog-articolo.html migliorato:** hero con immagine di copertina (se presente) con overlay e crediti fotografo, sezione FAQ interattiva con accordion, CTA banner "Contattaci" con link a /contatti
- **Fix bozze locali → Supabase:** le bozze con id `bozza_*` ora fanno INSERT (non UPDATE) su Supabase alla pubblicazione, evitando la perdita dell'articolo
- **Slug e meta_description** aggiunti al payload di saveBlogArticle (mancavano)
- **REGOLA IMPORTANTE:** gli articoli creati dallo scraping usano il template dinamico `blog-articolo.html`, non file HTML statici. Solo gli articoli nel seed `_blogSeedArticles` hanno file fisici dedicati

### v2.3 - 13 Marzo 2026 (Ottimizzazione immagini Supabase — -85% payload)
- **Supabase Image Transforms:** `resolveImageUrl()` aggiornata in `homepage.js`, `immobile.html`, `immobili.html` per usare endpoint `/storage/v1/render/image/public/` con parametri `width`, `quality`, `resize=contain`
- **Dimensioni ottimizzate per contesto:** card homepage/listing width=600 q=75, gallery hero width=1200 q=80, thumbnails width=300 q=70, lightbox full-size originale
- **Width/height espliciti** aggiunti su tutte le immagini dinamiche per ridurre CLS
- **Risparmio stimato:** ~2300 KiB (~85%) sulle immagini Supabase (da ~2737 KiB a ~400 KiB)
- **Nota cache GitHub Pages:** TTL 10 min non modificabile senza CDN esterno — documentato in TODO

### v2.2 - 12 Marzo 2026 (Scraping Articolo v2: anti-plagio, immagini, bozze visibili)
- **Contenuto 100% originale:** titoli rielaborati con 4 template randomizzati, 6 sezioni H2 con prospettiva Righetto, zone Padova randomizzate, 4 FAQ originali — il topic della fonte e' solo ispirazione, mai copiato
- **Immagini royalty-free automatiche:** ricerca Unsplash integrata con crediti fotografo, fallback su query generica immobiliare Italia
- **Bozze ora visibili nella lista Blog:** salvataggio doppio (Supabase + localStorage), merge bozze localStorage in getBlogArticles, redirect automatico a sezione Blog dopo salvataggio
- **Fix critico showToast → toast():** la funzione showToast non esisteva (il nome corretto e' toast), causava blocco JS che impediva chiusura modal e salvataggio
- **Proxy CORS rimossi:** sostituiti 4 proxy fragili (corsproxy.io, allorigins, cors.sh, corsproxy.org) con rss2json.com (CORS nativo, stabile)
- **Regola anti-plagio aggiunta** alla sezione 3.4 Strumenti Admin
- **SKILL-UNIFICATA.md aggiornata** ad ogni modifica come da regola operativa

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
  - Fonti citate: OMI, Agenzia Entrate, FIMAA Veneto (E-E-A-T + GEO)
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

*SKILL 2.0 — Un solo documento per governarli tutti.*
