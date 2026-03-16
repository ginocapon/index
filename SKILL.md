# SKILL UNIFICATA — Righetto Immobiliare
## Prompt Operativo Master Consolidato

> **Versione:** 2.2 — 16 Marzo 2026
> **Unica fonte di verita'** per sviluppo, manutenzione, contenuti SEO, strategia GEO e AI Agents.
> **Prossima verifica consigliata:** Giugno 2026

---

## 1. ISTRUZIONI PER CLAUDE

### 1.1 Verifica Aggiornamenti Google (Consigliata ad Ogni Sessione)
Prima di ogni sessione di lavoro SEO, ricercare:
- `"Google Search updates [mese corrente] [anno corrente]"`
- `"Core Web Vitals updates [anno corrente]"`
- `"GEO Generative Engine Optimization updates [anno corrente]"`

Confronta con la sezione "Stato Aggiornamenti Google" e aggiorna questo file se trovi novita'.

### 1.2 Regole Operative
1. **Leggi prima** il file da modificare — mai al buio
2. **Mobile-first** — ogni modifica deve funzionare su mobile
3. **No librerie extra** — il sito e' volutamente leggero (vanilla HTML/CSS/JS)
4. **Commit** chiari e descrittivi in italiano
5. **Aggiorna** sitemap.xml quando aggiungi/rimuovi pagine
6. **Performance** — mai animazioni sull'elemento LCP; usare opacity/transform, mai filter
7. **CTA contrast** — minimo 4.5:1 (WCAG AA)
8. **Commissioni coerenti** — ogni riferimento alle commissioni deve essere: 3% + IVA per parte (min. 2.500€ vendita), 1 mensilita' + IVA (affitto)
9. **Dati verificati** — ogni dato numerico DEVE avere fonte citata. Se non hai fonte, scrivi "dato non disponibile"
10. **Zero claim inventati** — nessuna percentuale o statistica senza fonte verificabile
11. **Claim verificati** — usare solo: 350+ immobili trattati, 101 comuni, 98% soddisfazione, 127 recensioni Google 4.9/5, dal 2000
12. **URL coerenti** — usare sempre `righettoimmobiliare.it` senza www

### 1.3 Stile di Comunicazione
- Rispondi in italiano
- Sii diretto e pratico
- Proponi sempre prima di agire su operazioni irreversibili
- Tono professionale B2B — **ZERO dialetto** (settore web agency)

---

## 2. CONTESTO PROGETTO

### 2.1 Informazioni Generali
| Campo | Valore |
|---|---|
| **Ragione Sociale** | Gruppo Immobiliare Righetto di Capon Gino |
| **P.IVA** | 05182390285 |
| **Dominio** | righettoimmobiliare.it (senza www) |
| **Fondazione** | 2000 |
| **Sede** | Via Roma n.96, 35010 Limena (PD) |
| **Telefono** | 049.88.43.484 / Cell: 349 736 5930 |
| **Email** | info@righettoimmobiliare.it |
| **Orari** | Lun-Ven 9:00-13:00 / 15:00-19:00, Sab 9:00-13:00 |
| **Tech Stack** | HTML statico + CSS custom + JS vanilla + Supabase backend |
| **Framework** | Nessuno — zero dipendenze esterne, codice puro |
| **Lingue** | Italiano (unica versione attiva) |
| **Target** | Proprietari e acquirenti immobili — Padova e 101 comuni provincia |
| **Hosting** | GitHub Pages |
| **Performance** | PageSpeed 90+ |

### 2.2 Struttura File Sito (root — GitHub Pages)
```
/
├── CLAUDE.md                   # Istruzioni automatiche per Claude
├── SKILL.md                    # Questo file — unica fonte di verita'
├── .nojekyll                   # Disabilita Jekyll su GitHub Pages
│
├── index.html                  # Homepage (hero, servizi, prezzi, FAQ, stats)
├── chi-siamo.html              # Chi Siamo
├── contatti.html               # Pagina contatti
├── servizi.html                # Servizi overview
├── faq.html                    # FAQ
├── blog.html                   # Pagina blog principale
├── immobili.html               # Lista immobili
├── immobile.html               # Dettaglio immobile (dinamico via JS)
├── agenzia-immobiliare-padova.html  # Landing agenzia
├── privacy.html                # Privacy Policy GDPR
├── cookie-policy.html          # Cookie Policy
├── admin.html                  # Pannello admin (interno)
│
├── blog-*.html                 # 41 articoli blog in root (BlogPosting schema)
│
├── servizio-*.html             # 7 pagine servizi specifici
│   ├── servizio-gestione.html
│   ├── servizio-locazioni.html
│   ├── servizio-preliminari.html
│   ├── servizio-utenze.html
│   ├── servizio-valutazioni.html
│   ├── servizio-vendita.html
│   └── servizio-virtual-tour.html
│
├── zona-*.html                 # 14 pagine zone Padova
│   ├── zona-abano-terme.html
│   ├── zona-arcella-padova.html
│   ├── zona-centro-storico-padova.html
│   ├── ... (e altre 11 zone)
│   └── zona-voltabarozzo-padova.html
│
├── landing-*.html              # 12 landing pages (conversione, chat, offerte)
├── landing/                    # 5 landing pages offerte energia
│
├── vendere-casa-padova-errori.html  # Articolo vendita
├── articolo-riqualificazione.html   # Articolo riqualificazione
│
├── sitemap.xml                 # 88 URL indicizzate
├── robots.txt                  # Whitelist AI bots + riferimenti file AI
│
├── — FILE AI AGENTS —
├── llms.txt                    # Info sito per AI (standard llmstxt.org)
├── llms-full.txt               # Contenuto completo pagine in Markdown
├── ai.json                     # Permessi AI (standard ai-visibility.org.uk v1.1.0)
├── humans.txt                  # Crediti team
├── manifest.json               # PWA base
├── .well-known/
│   ├── agent.json              # Discovery A2A (Google/Linux Foundation)
│   ├── mcp.json                # Discovery MCP (Anthropic/Linux Foundation)
│   └── security.txt            # Policy sicurezza (RFC 9116)
│
├── css/
│   └── styles.css              # Foglio stile principale
├── js/                         # JavaScript (homepage.js, chatbot.js, etc.)
├── assets/                     # Risorse statiche (immagini, media)
├── data/                       # Dati strutturati JSON
├── templates/                  # Template email (3 HTML)
├── instagram/                  # Landing Instagram
│
├── scraping.html               # Tool interno
├── bookmarklet-helper.html     # Tool interno
└── unsubscribe.html            # Pagina disiscrizione email
```

### 2.3 Modello di Business — Agenzia Immobiliare
**Intermediazione immobiliare completa: dalla valutazione al rogito.**

| Componente | Dettaglio |
|---|---|
| **Commissione vendita** | 3% + IVA per parte (min. 2.500€) |
| **Commissione affitto** | 1 mensilita' + IVA |
| **Valutazione** | Gratuita e senza impegno |
| **Consulenza mutuo** | Gratuita (10+ banche confrontate) |
| **Area operativa** | 101 comuni provincia di Padova |

**Team:**
| Persona | Ruolo |
|---|---|
| **Capon Gino** | Titolare, Agente Immobiliare — ville, immobili di pregio, investimenti |
| **Righetto Linda** | Agente Immobiliare — locazioni, mercato affitti Padova |

**Claim verificati (usare SOLO questi):**
- 350+ immobili trattati (venduti o affittati)
- 101 comuni serviti nella provincia
- 500+ immobili compravenduti (storico dal 2000)
- 1.200+ contratti gestiti
- 98% clienti soddisfatti
- 127 recensioni Google con media 4.9/5
- 25+ anni di esperienza (dal 2000)
- Tempo medio vendita: 45-60 giorni

**Partner:**
- Servizi Immobiliari Padova (serviziimmobiliaripadova.it)
- RaaS Automazioni (raasautomazioni.it) — partner tecnologico

### 2.4 Servizi Core
- **Vendita immobili** — valutazione, promozione multicanale, foto professionali, virtual tour 360, assistenza fino al rogito
- **Locazioni** — valutazione canone, selezione inquilini, contratti (4+4, 3+2, transitorio, studenti), registrazione
- **Valutazioni e perizie** — stima gratuita basata su dati FIAIP, comparabili reali, report scritto
- **Gestione immobili** — rapporti inquilini, supervisione pagamenti, manutenzione, contabilita'
- **Gestione preliminari** — conformita' catastale/urbanistica, bozza compromesso, coordinamento notarile
- **Virtual Tour 360** — tour professionali pubblicati su YouTube
- **Attivazione utenze** — volture, subentri luce/gas, consulenza tariffaria (partner ENEL)
- **Consulenza mutuo gratuita** — confronto 10+ banche, simulatore rate
- **Aste giudiziarie** — analisi, due diligence, assistenza offerta

### 2.5 Messaging Core
**Messaggio primario:** "Vendere e comprare casa a Padova? Ci pensiamo noi."
**Sottotitolo:** "Un unico referente per ogni esigenza — dalla valutazione al rogito."

**Gerarchia messaggi:**
1. Competenza locale: 25+ anni, 101 comuni, 350+ immobili trattati
2. Trasparenza: commissioni chiare, valutazione gratuita, zero costi nascosti
3. Servizio completo: dalla perizia al rogito, un unico referente
4. Fiducia: 127 recensioni Google 4.9/5, 98% soddisfazione
5. Tecnologia: virtual tour 360, chatbot Linda, simulatore mutuo

**NON dire mai:**
- Prezzi di mercato inventati (solo dati FIAIP/OMI verificati)
- "Garantiamo vendita in X giorni" (media 45-60 gg, non garantita)
- Percentuali inventate
- Attacchi a concorrenti o altre agenzie
- Dati su quartieri senza fonte

### 2.6 Struttura Sito Bilingue
```
/                    → Italiano (default, unica versione attiva)
/en/                 → English (NON ANCORA CREATA — da implementare)
```
**NOTA:** La directory /en/ non esiste ancora. Nessuna pagina ha hreflang tags.
Quando la versione EN verra' creata, aggiungere `<link rel="alternate" hreflang="it/en">` su tutte le pagine.

### 2.7 Design — Colori e Componenti
| Elemento | Valore | Note |
|---|---|---|
| **Colore primario** | Blu scuro (dark navy) | Background hero, sezioni scure |
| **Accent / Gold** | Oro/dorato | Badge, dettagli, tagline, titoli accent |
| **Font titoli** | Cormorant Garamond (serif) | Look premium/luxury |
| **Font corpo** | Sans-serif system | Leggibilita' |
| **Stile** | Premium immobiliare — elegante, professionale |
| **Hero** | Foto team titolari, H1 con effetto ghost/outline |
| **Chatbot** | "Linda" — assistente AI, caricato lazy |
| **Landing chat** | UI stile WhatsApp con avatar Linda, progress bar, scelte a bottoni |

### 2.8 Backend e Strumenti
| Componente | Dettaglio |
|---|---|
| **Database** | Supabase (immobili, richieste contatto, newsletter) |
| **Form contatti** | Salva su Supabase tabella "richieste" + notifica email |
| **Newsletter** | Supabase tabella "newsletter_subscribers" |
| **Chatbot** | "Linda" — assistente AI, caricato lazy da js/chatbot.js |
| **FAQ** | Dati condivisi in RIGHETTO_FAQ_DATA (js/chatbot.js) — usati da faq.html e chatbot |
| **Tools** | tools/import-csv-to-supabase.py, tools/upload-contacts-now.py |

---

## 3. STRATEGIA SEO & CONTENUTI BLOG

### 3.1 Executive Summary — Standard Articoli Blog
- 2500+ parole strutturate, orientate al mercato immobiliare Padova
- 35% transition words naturali
- 28 H2/H3 distribuiti
- Meta titles max 60 char + Meta desc max 160 char
- JSON-LD BlogPosting + FAQSchema
- Author: Gino Capon, Agente Immobiliare
- Fonti verificate: OMI (Agenzia Entrate), FIAIP, IlSole24Ore, Banca d'Italia, ISTAT
- Ogni dato di prezzo/mercato DEVE avere fonte e anno

### 3.2 Pilastri Contenuti Blog (41 articoli attivi)
| Pilastro | Articoli | Keyword seed |
|----------|----------|-------------|
| **Mercato immobiliare** | 7 | "mercato immobiliare Padova 2026", "prezzi case zona" |
| **Mutui e finanziamenti** | 6 | "mutuo prima casa Padova", "tasso fisso variabile" |
| **Affitti e locazioni** | 6 | "affitto Padova 2026", "canoni", "studenti" |
| **Vendita casa** | 5 | "vendere casa Padova", "costi vendita", "tempi" |
| **Guide legali/burocratiche** | 4 | "documenti vendita", "tasse", "caparra", "successione" |
| **Zone e quartieri** | 3 | "quartieri Padova", "Limena vs Centro" |
| **Acquisto e investimento** | 2 | "comprare casa guida", "investire immobiliare" |
| **Infrastrutture Padova** | 3 | "scuole Padova", "trasporti", "servizi" |
| **Nuove costruzioni/Green** | 2 | "case green", "nuova costruzione Limena" |
| **Altro** | 3 | "home staging", "vita agenzia", "Ca' Marcello" |

### 3.3 Meta Titoli e Descrizioni (Template)
**TITLE:** `[Topic] Padova 2026: [Beneficio/Dato] | Righetto Immobiliare`
**META DESC:** `[Risposta diretta alla query]. Dati aggiornati [mese] 2026, fonti OMI/FIAIP. Guida completa di Righetto Immobiliare, dal 2000 nel Padovano.`

Esempi:
- `Mutuo Prima Casa Padova 2026: Tassi, Requisiti e Agevolazioni | Righetto Immobiliare`
- `Prezzi Case Padova per Zona 2026: Mappa Completa €/mq | Righetto Immobiliare`

### 3.4 Linguaggio
**Tono:** Professionale, autorevole, accessibile. Come un consulente esperto che spiega al cliente.

**EVITARE:**
- Dialetto Veneto
- Gergo tecnico senza spiegazione
- Tono aggressivo o commerciale
- Promesse di vendita garantita

**Transition words 35% (professionali):**
Inoltre, Infatti, Di conseguenza, In particolare, Tuttavia, Pertanto, Nonostante cio', A tal proposito, In sintesi, D'altra parte, Allo stesso modo, Per questo motivo, Infine, Quindi, In conclusione, Dunque

### 3.5 Struttura Articolo — Template
1. **Intro** (150 parole) — problema del lettore, risposta diretta nelle prime 2 righe
2. **Dato chiave** — numero verificato con fonte (es. "Prezzi +2.3% nel 2025 — fonte OMI")
3. **Sezioni H2** (10-15) — ogni sezione max 200 parole con dato/fonte
4. **Tabella comparativa** — dati zona/prezzo/rendimento con fonte
5. **FAQ** (5-10) — basate su "People Also Ask" Google
6. **CTA** — link a valutazione gratuita o contatti
7. **Fonti** — elenco fonti ufficiali citate

### 3.6 JSON-LD Schema
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "[TITOLO_ARTICOLO]",
  "description": "[DESCRIZIONE_ARTICOLO]",
  "author": {
    "@type": "Person",
    "name": "Gino Capon"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Righetto Immobiliare"
  },
  "datePublished": "[DATA_PUBBLICAZIONE]",
  "dateModified": "[DATA_MODIFICA]",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://righettoimmobiliare.it/[FILENAME]"
  }
}
```

**FAQ Schema (15 FAQ basate su "People Also Ask" Google):**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Quanto costa un sito web professionale nel 2026?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "I prezzi variano: RaaS 249€/anno bloccato, Aruba da 9,90€ a 59,99€/anno (+506%), agenzie tradizionali 1.500-5.000€ una tantum + rinnovi. Fonte: preventivi ufficiali gennaio 2026."
      }
    },
    {
      "@type": "Question",
      "name": "Cos'e' la garanzia anti-rincaro?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Clausola contrattuale che blocca il prezzo per sempre. Es: RaaS 249€/anno nel 2026 resta 249€ anche nel 2030."
      }
    }
  ]
}
```

### 3.7 Dati Mercato Immobiliare (Solo Fonti Verificate)

**PREZZI MEDI PADOVA PER ZONA — Da aggiornare trimestralmente**

| Zona | €/mq (indicativo) | Fonte |
|------|-------------------|-------|
| Centro Storico | ~3.500 | OMI / FIAIP |
| Cittadella | ~3.200 | OMI / FIAIP |
| Arcella | Verificare | OMI |
| Limena | 1.600-2.400 | OMI |

**REGOLA:** Se dato non disponibile o non aggiornato, scrivere "dato in aggiornamento" o non inserire riga. Mai inventare prezzi al mq.

### 3.8 CTA e Conversione Blog
**Ogni articolo deve chiudersi con:**
- Link a valutazione gratuita (landing-valutazione.html o landing-chat-valutazione.html)
- Link a contatti o WhatsApp
- Badge urgenza se pertinente (es. "Marzo 2026: valutazione gratuita + report mercato")

**Landing pages conversione (2 tipi):**
1. **Tradizionali** — landing-valutazione, landing-calcolo-mutuo, landing-vendita
2. **Chat conversazionali** — landing-chat-* con UI WhatsApp e avatar Linda

### 3.9 Zone Pages — Strategia Local SEO
14 pagine zona attive (hub-and-spoke model):
- Ogni zona ha: descrizione quartiere, prezzi €/mq, immobili disponibili, servizi zona
- Keyword pattern: "casa [zona] Padova", "appartamento [zona]", "immobili [zona]"
- Schema: RealEstateAgent + LocalBusiness con geo-coordinates

### 3.10 Template Veloce Articolo Blog Immobiliare
```markdown
# [TITOLO] Padova 2026: [Dato Chiave]

[INTRO 150 parole - problema del lettore, risposta diretta]

## [Dato Verificato]: Situazione Attuale a Padova

[Spiegazione con dati OMI/FIAIP e anno di riferimento]

## [Tema]: Guida Pratica per [Acquirente/Venditore/Inquilino]

[Contenuto pratico con consigli operativi]

## [H2_TEMATICO]

[Sviluppo 200 parole max, con dato e fonte]

...continua per 10-15 H2/H3...

## FAQ: Domande Frequenti

[Da "People Also Ask" Google — 5-10 domande]

## Fonti Verificate

- [OMI Agenzia delle Entrate]
- [FIAIP / Rapporto immobiliare]
- [IlSole24Ore / Banca d'Italia / ISTAT]
```

---

## 4. REQUISITI GOOGLE — AGGIORNATI MARZO 2026

### 4.1 Core Web Vitals — Soglie 2026
| Metrica | Buono | Da migliorare | Scarso |
|---|---|---|---|
| **LCP** | < 2.5s (target: <2s) | 2.5s - 4.0s | > 4.0s |
| **INP** | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** | < 0.1 | 0.1 - 0.25 | > 0.25 |

### 4.2 Performance Rules — OBBLIGATORIO
1. **No `filter: blur` su animazioni** — usare `opacity` e `transform` (GPU-accelerated)
2. **No `will-change` permanente** — solo al `:hover` o quando serve
3. **Hero animations ritardate** — nessuna animazione above-the-fold nei primi 3s
4. **Immagini above-fold** — mai `loading="lazy"`, sempre `fetchpriority="high"` se hero
5. **Font** — preload woff2, `font-display: swap`
6. **Iframe** (YouTube etc.) — sempre `loading="lazy"`

### 4.3 E-E-A-T — Segnali 2026 (Aggiornati)
Il 96% delle citazioni AI Overviews proviene da fonti con forti segnali E-E-A-T (fonte: Wellows 2026).
Pagine con 15+ entita' riconosciute hanno 4.8x piu' probabilita' di essere in AI Overviews (fonte: ClickRank).
Siti con segnali di esperienza hanno visto +23% dopo Core Update dicembre 2025 (fonte: BKND).

**Experience (Esperienza diretta):**
- Immagini originali (screenshot lavori, dashboard, foto eventi) — NO stock photo
- Case study con numeri specifici e risultati misurabili
- Video propri che mostrano il lavoro in azione
- Dettagli che solo un insider conosce

**Expertise (Competenza tecnica):**
- Contenuti 2500+ parole approfonditi su argomenti core
- Uso corretto terminologia tecnica con definizioni
- Spiegare il "perche'" oltre al "cosa"
- Person schema con jobTitle, worksFor, qualifiche

**Authoritativeness (Autorita'):**
- Backlink da fonti credibili del settore
- Presenza su directory settoriali
- Recensioni su piattaforme terze (Google Business, Trustpilot)
- NAP consistente (Nome, Indirizzo, Telefono) su tutto il web
- Menzioni su pubblicazioni indipendenti

**Trustworthiness (Affidabilita' — IL PIU' IMPORTANTE):**
- Contatti chiari: indirizzo fisico, telefono, email
- Team con nomi reali, foto, bio, qualifiche
- Prezzi trasparenti e verificabili
- Privacy/Cookie policy presenti, HTTPS
- Recensioni clienti con attribuzione
- Fonti esterne citate per ogni dato numerico

### 4.4 GEO — Generative Engine Optimization
**Dati chiave:**
- Sessioni AI +527% anno su anno (fonte: Averi 2025)
- AI Overviews su 48% delle query tracciate, +58% anno su anno (fonte: almcorp)
- Sovrapposizione Google top link / fonti AI scesa dal 70% al 20% (fonte: Profound)
- Schema markup = 2.5x piu' probabilita' di apparire in risposte AI (fonte: Stackmatix)
- GPT-4 passa dal 16% al 54% di risposte corrette con structured data (fonte: Medium)
- Solo 38% delle citazioni AI Overview proviene da pagine top-10 (fonte: almcorp)

**I 7 Pilastri GEO:**
1. **Crawling AI** — robots.txt con whitelist completa (GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, GoogleOther)
2. **Struttura per Sintesi** — Risposta diretta nelle prime 2 righe di ogni sezione, poi approfondimento
3. **Contenuti Citabili** — Dati proprietari, benchmark originali, case study con numeri unici
4. **Prompt-style** — Ottimizzare per domande conversazionali ("Quale web agency italiana ha prezzi fissi?"), non solo keyword
5. **Consenso Multi-Fonte** — Presenza coerente su directory, review, forum, social, pubblicazioni terze
6. **Aggiornamento Costante** — Date "ultimo aggiornamento" visibili, refresh trimestrale contenuti cornerstone
7. **Dominio di Nicchia** — Profondita' tematica su argomenti specifici (le AI premiano chi copre un tema in profondita')

**Come le AI scelgono chi citare:**
| Piattaforma | Fonti citate | Preferenze | Nota |
|-------------|-------------|------------|------|
| ChatGPT | 3-5 | Wikipedia, fonti autorevoli | Usa indice Bing — IndexNow accelera discovery |
| Perplexity | 5-8 | Reddit, forum, fonti dirette | Piu' aperto a siti piccoli con dati unici |
| Google AI Overviews | 2-4 | Distribuite, schema.org | 82% citazioni da earned media |
| Gemini | 3-6 | Dati numerici, bullet points | Gemini 3 (gen 2026) ha sostituito 42% dei domini citati |
| Claude | 3-6 | Documentazione tecnica | Preferisce fonti strutturate |

### 4.5 Schema.org — Priorita' per AI e Motori
Schema.org e' il ponte critico tra siti web e AI agents. Contenuti con schema hanno 2.5x piu' probabilita' di apparire in risposte AI. Google e Microsoft usano Schema Markup per le feature di AI generativa.

**Schema prioritari (JSON-LD — formato obbligatorio):**
| Schema | Dove | Impatto AI | Stato |
|--------|------|-----------|-------|
| Organization | Homepage | CRITICO | FATTO |
| LocalBusiness | Homepage | CRITICO | DA FARE |
| ProfessionalService | Homepage | ALTO | DA FARE |
| FAQPage | Tutte con FAQ | ALTO | PARZIALE |
| Service + Offer | Homepage | ALTO | FATTO |
| AggregateRating | Homepage (testimonial) | ALTO | DA FARE |
| Review | Homepage (testimonial) | ALTO | DA FARE |
| BreadcrumbList | Tutte le pagine | MEDIO | PARZIALE |
| BlogPosting | Blog (41 articoli) | MEDIO | FATTO |
| Person | Blog, Chi Siamo | MEDIO | DA FARE |
| VideoObject | Pagine con video | MEDIO | DA FARE |
| ItemList | Bandi | MEDIO | DA FARE |
| HowTo | Guide/tutorial | MEDIO | DA FARE |
| Dataset | Aggregatore bandi | BASSO | DA FARE |

**Regola d'oro Schema:** I dati nello schema DEVONO corrispondere esattamente a cio' che c'e' sulla pagina E su Google Business Profile. Incoerenze riducono la fiducia AI su TUTTE le pagine.

### 4.6 Aggiornamenti Algoritmo Google — Stato Marzo 2026
- **Gennaio 2026:** Prioritizzata esperienza diretta autentica; siti con riassunti AI penalizzati
- **Febbraio 2026:** Discover Core Update — contenuti locali, in-depth, originali premiati; clickbait ridotto
- **Marzo 2026:** Core Update — helpful content rafforzato, AI content scalato e parasitic SEO penalizzati
- Google fa ~500.000 esperimenti e ~4.500 miglioramenti all'anno
- L'algoritmo e' ora alimentato da Gemini AI con comprensione semantica continua

---

## 5. CHECKLIST AUTOMATICHE

### Per Ogni Nuova Pagina
- [ ] Title tag unico (max 60 char)
- [ ] Meta description unica (max 160 char)
- [ ] H1 unico con keyword conversazionale (prompt-style)
- [ ] Schema.org JSON-LD (BreadcrumbList + tipo specifico)
- [ ] Open Graph tags (og:title, og:description, og:url, og:image, og:type, og:locale)
- [ ] `<meta name="theme-color">`
- [ ] `<link rel="canonical">`
- [ ] Hero image con `fetchpriority="high"`, mai `loading="lazy"` above-fold
- [ ] Font preload woff2
- [ ] CTA primario con contrasto >= 4.5:1
- [ ] Registrato in sitemap.xml
- [ ] Link navbar e footer coerenti con tutte le altre pagine
- [ ] Cookie banner presente
- [ ] Nessun CDN esterno (codice puro)
- [ ] GA4 (G-JFM8JG9C2R) presente
- [ ] Risposta diretta nelle prime 2 righe di ogni sezione H2 (GEO)
- [ ] Contenuto risponde a domande conversazionali

### Per Ogni Nuovo Articolo Blog
- [ ] 2500+ parole strutturate
- [ ] 28 H2/H3 distribuiti
- [ ] 35% transition words professionali
- [ ] Errori umani casuali (5-8, max 1 ogni 300 parole)
- [ ] Meta titles 60/160 char + desc 95/200 char
- [ ] JSON-LD BlogPosting + FAQPage + BreadcrumbList
- [ ] 15 FAQ basate su ricerche reali ("People Also Ask")
- [ ] Tabelle confronto con FONTI CITATE
- [ ] Ogni dato numerico ha [FONTE] verificata
- [ ] Link fonti ufficiali preservati
- [ ] Zero claim inventati
- [ ] Zero attacchi personali a concorrenti
- [ ] SPINTAX social pronto (LinkedIn/Facebook)
- [ ] Tono professionale B2B — zero dialetto
- [ ] Author bio con Person schema
- [ ] Table of Contents con anchor link
- [ ] Data "Ultimo aggiornamento" visibile
- [ ] Pulsanti condivisione social (LinkedIn, X, Facebook)

### Per Ogni Modifica CSS
- [ ] Mobile-first: stili base per mobile, `@media` per desktop
- [ ] No `filter` su animazioni — solo `opacity` e `transform`
- [ ] No `will-change` permanente
- [ ] Contrasto minimo 4.5:1 su CTA

### Per Ogni Modifica JS
- [ ] Vanilla JS — nessun framework, nessuna libreria
- [ ] Performance: nessun blocco rendering
- [ ] Chatbot caricato con delay

### Commit
- [ ] Messaggio in italiano, descrittivo
- [ ] Nessun file sensibile (.env, credenziali)

---

## 6. ISTRUZIONI PUBBLICAZIONE

### Prima di Pubblicare Qualsiasi Contenuto:

1. **VERIFICARE [DATO] su fonte ufficiale:**
   - Prezzi: preventivi ufficiali richiesti (screenshot/PDF)
   - Performance: Google PageSpeed Insights (screenshot)
   - Trend: Google Trends, Gartner, IlSole24Ore

2. **SOSTITUIRE placeholder:**
   - [COMPETITOR] → Nome reale (Aruba, Register, Keliweb)
   - [DATO_FONTE] → Numero + fonte tra parentesi
   - [DATA] → Data pubblicazione reale

3. **AGGIORNARE trimestrale:**
   - Prezzi competitors (verificare rinnovi)
   - Dati PageSpeed (ripetere test)
   - Bonus/agevolazioni statali

4. **CITARE fonte sotto ogni tabella/grafico**

### Regola d'Oro
> "Se non hai fonte verificabile, NON inserire il dato."
> Meglio scrivere "dato non disponibile" che inventare numeri.

---

## 7. TODO — Azioni Future

### Infrastruttura
- [x] Sito live su GitHub Pages
- [x] 88 URL indicizzate in sitemap.xml
- [x] Schema.org su tutte le pagine (RealEstateAgent, BlogPosting, FAQPage, VideoObject)
- [x] Open Graph tags su tutte le pagine
- [x] robots.txt con whitelist AI bots

### Contenuti
- [x] 41 articoli blog pubblicati (mercato, mutui, affitti, vendita, zone)
- [x] 14 pagine zona Padova
- [x] 7 pagine servizi
- [x] 12 landing pages (incluse 6 chat conversazionali)
- [ ] Creare nuovi articoli blog seguendo template Sezione 3
- [ ] Aggiornare dati mercato OMI/FIAIP trimestralmente

### Tecnico
- [ ] Implementare `prefers-reduced-motion` per accessibilita'
- [ ] Critical CSS inline per LCP <2s

### GEO & AI Agents
- [x] Creare robots.txt con whitelist AI bots (7 bot configurati)
- [x] Creare llms.txt (standard llmstxt.org)
- [x] Creare llms-full.txt (contenuto completo pagine in Markdown)
- [x] Creare ai.json (permessi AI — standard ai-visibility.org.uk v1.1.0)
- [x] Creare /.well-known/agent.json (discovery A2A — standard Google/Linux Foundation)
- [x] Creare /.well-known/mcp.json (discovery MCP — standard Anthropic/Linux Foundation)
- [ ] Aggiungere AggregateRating schema su testimonial homepage
- [ ] Aggiungere LocalBusiness schema su homepage
- [ ] Aggiungere Person schema per fondatore e team
- [ ] Aggiungere author bio su articoli blog
- [ ] Aggiungere Table of Contents su articoli blog
- [ ] Aggiungere date "Ultimo aggiornamento" visibili su blog
- [x] Usare BlogPosting invece di Article su blog (41 articoli migrati)
- [ ] Aggiungere ItemList schema su bandi.html
- [ ] Embed video YouTube su pagine chiave (youtube-nocookie.com per GDPR)
- [ ] Creare VideoObject schema per video
- [ ] Aggiungere pulsanti share social su blog
- [x] Creare humans.txt
- [x] Creare .well-known/security.txt (RFC 9116)
- [x] Creare manifest.json PWA base
- [ ] Implementare IndexNow per Bing (ChatGPT usa indice Bing)
- [ ] Monitoring citazioni AI (Otterly.AI o Peec AI) — settimanale
- [ ] Registrarsi su directory settoriali italiane
- [ ] Ottimizzare Google Business Profile (post 2x/settimana)
- [ ] Aggiungere favicon link `<link rel="icon">` su tutte le pagine
- [ ] Aggiungere hreflang tags quando sezione EN viene creata

---

## 8. STRATEGIA GEO, AI AGENTS & PREVISIONI 2026-2028

### 8.1 File Speciali per AI Agents
| File | Posizione | Scopo | Stato |
|------|-----------|-------|-------|
| `robots.txt` | `/robots.txt` | Whitelist crawler AI (7 bot) + riferimenti a tutti i file AI | FATTO |
| `llms.txt` | `/llms.txt` | Info sito leggibile da AI (standard llmstxt.org, 600+ siti lo usano) | FATTO |
| `llms-full.txt` | `/llms-full.txt` | Contenuto completo in Markdown (tutte le pagine) | FATTO |
| `ai.json` | `/ai.json` | Permessi AI — allow/deny per tipo uso (v1.1.0, ai-visibility.org.uk) | FATTO |
| `agent.json` | `/.well-known/agent.json` | Discovery A2A — Google/Linux Foundation, descrive servizi per agenti | FATTO |
| `mcp.json` | `/.well-known/mcp.json` | Discovery MCP — Anthropic/Linux Foundation (97M+ download SDK/mese) | FATTO |
| `humans.txt` | `/humans.txt` | Crediti team (Capon Gino, Righetto Linda), trasparenza | FATTO |
| `security.txt` | `/.well-known/security.txt` | Policy sicurezza (RFC 9116, scadenza 2027-03-16) | FATTO |
| `manifest.json` | `/manifest.json` | PWA base (nota: servono icone 192x192 e 512x512) | FATTO |

**Nota su llms.txt:** 844.000+ siti lo implementano (Anthropic, Stripe, Cloudflare). Nessuna AI ha confermato ufficialmente di leggerlo, ma e' una scommessa a basso costo con potenziale futuro.

### 8.2 Standard Emergenti per AI Agents

**NLWeb (Natural Language Web) — Microsoft:**
Protocollo open-source (MIT) creato da R.V. Guha (inventore di RSS, RDF e Schema.org). Trasforma siti web in endpoint conversazionali per AI agents. Funziona consumando il markup Schema.org esistente. Ogni istanza NLWeb e' anche un server MCP. Chiamato "l'HTML della generazione AI."
- **Azione:** Avere Schema.org completo e' gia' la base per NLWeb.
- Fonte: searchengineland.com, github.com/microsoft/NLWeb

**MCP (Model Context Protocol) — Anthropic:**
Donato alla Linux Foundation (dic 2025). Co-fondato da Anthropic, Block, OpenAI. Supportato da Google, Microsoft, AWS, Cloudflare. 97M+ download SDK/mese. Permette agli AI agents di interagire con servizi strutturati.
- **Azione:** Preparare `/.well-known/mcp.json` come endpoint di discovery.
- Fonte: modelcontextprotocol.io, anthropic.com

**A2A (Agent-to-Agent) — Google:**
Protocollo sotto Linux Foundation. Usa `/.well-known/agent.json` per discovery tra agenti. Complementare a MCP.
- **Azione:** Preparare agent card con descrizione servizi.
- Fonte: a2aprotocol.ai

**WebMCP — Chrome 145+ (feb 2026):**
Permette ai siti di esporre form e strumenti come tool dichiarativi per AI agents nel browser.
- **Azione:** Monitorare — quando si stabilizza, i form contatto/preventivo diventano tool AI.
- Fonte: dev.to/czmilo

**NIST AI Agent Standards Initiative (feb 2026):**
Standard per ecosistemi di agenti AI interoperabili e sicuri.
- **Azione:** Monitorare per compliance futura.
- Fonte: nist.gov

**IndexNow — Bing:**
80M+ siti, 5B+ submission/giorno. 22% dei click Bing proviene da URL IndexNow. Google NON lo supporta, ma ChatGPT usa l'indice Bing → indicizzazione Bing piu' rapida = discovery ChatGPT piu' rapida.
- **Azione:** Implementare per contenuti blog (semplice script al deploy).
- Fonte: bing.com/indexnow

### 8.3 Zero-Click Search — Numeri e Strategia
**Stato 2026:**
- 60% delle ricerche Google finisce senza click (fonte: Bain & Company). Su mobile: 77%
- Query con AI Overviews: 83% zero-click. AI Mode: 93% zero-click
- AI Overviews riducono i click del 58% (fonte: Ahrefs, feb 2026)
- MA: il traffico AI converte **23x meglio** del tradizionale organico, con valore economico **4.4x superiore** (fonte: click-vision.com)
- I brand sono **6.5x piu' probabili** di essere citati tramite fonti terze

**Strategia anti-zero-click:**
1. Shift KPI da traffico a **visibilita'**: citazioni AI, brand mentions, snippet appearances
2. Ottimizzare per inclusione nelle risposte: formato Q&A, definizioni concise, dati strutturati
3. Costruire presenza su siti autorevoli esterni (i brand citati tramite terze parti hanno 6.5x piu' citazioni)
4. Ottimizzare conversione del traffico che arriva (qualita' molto piu' alta)

**Previsione 2027:** 75% delle query informazionali risolte direttamente nelle interfacce di ricerca
**Previsione 2028:** Zero-click diventa il default. Solo query transazionali e ricerca complessa generano click

### 8.4 Google AI Overviews & AI Mode — Evoluzione
**Stato 2026:**
- AI Overviews su **48% delle query** tracciate (+58% anno su anno)
- Gemini 3 e' il modello di default (gen 2026)
- Penetrazione per settore: Sanita' 88%, Education 83%, B2B Tech 82%, Ristoranti 78%
- Gli utenti possono fare domande di follow-up direttamente da AI Overviews
- Google ha lanciato Universal Commerce Protocol (UCP) — checkout diretto dentro AI Mode

**Previsione 2027:** AI Overviews su >60% delle query. Risposte personalizzate basate su cronologia
**Previsione 2028:** AI Overviews diventano l'esperienza predefinita. SERP tradizionale (10 link blu) limitata a query di nicchia

### 8.5 Voice Search & Assistenti AI
**Stato 2026:**
- 8.4 miliardi di assistenti vocali in uso globale (fonte: DemandSage)
- 65%+ ricerche locali via voce. 71% utenti preferisce voce a digitazione
- Europa: 25% del mercato globale voice assistant
- Voice commerce: $80 miliardi nel 2026
- Mercato voice assistant: da $7.35B (2024) a $33.74B (2030), CAGR 26.5%

**Azioni per sito statico italiano:**
- Ottimizzare per query conversazionali in italiano ("Quanto costa un sito web per un ristorante a Milano?")
- Implementare FAQ schema e markup speakable
- Google Business Profile completo — gli assistenti vocali attingono pesantemente da GBP
- Ottimizzazione voice in italiano = vantaggio competitivo (quasi nessuno lo fa)

**Previsione 2027:** AI conversazionale domina 70% interazioni cliente. Voice ads a $19B
**Previsione 2028:** Voice search diventa "agentica" — non solo cerca info ma prenota, confronta, acquista

### 8.6 Multimodal Search (Testo + Immagine + Video + Voce)
**Stato 2026:**
- Google Lens: >12 miliardi di ricerche visive/mese
- Ricerca multimodale e' il nuovo standard Google: foto + domanda vocale = query unica
- Short-form video (Shorts, Reels, TikTok) e' il formato contenuto piu' universale 2026
- Google AI "legge" trascrizioni video e "guarda" frame per trovare risposte

**Azioni per sito statico:**
- Immagini di qualita' con alt text descrittivo + ImageObject schema
- Video brevi (case study, demo servizi) con VideoObject schema
- Trascrizioni testuali sotto ogni video (doppio contenuto per AI)
- Embed YouTube con `youtube-nocookie.com` per GDPR, `loading="lazy"` su iframe

**Previsione 2027:** Vector-based retrieval sostituisce keyword matching. Silos contenuto (testo/immagine/video) si dissolvono
**Previsione 2028:** App multimodali AI mostrano +45% conversioni in Europa. Voice search +20-35% featured snippets

### 8.7 AI Agents & Commercio Agentico — La Rivoluzione 2026-2028
**Stato 2026:**
- Traffico da AI agents cresciuto **+1.300%** in 9 mesi (fonte: McKinsey)
- OpenAI + Walmart: acquisti dentro ChatGPT. PayPal: Agentic Toolkit. Visa/Mastercard: tool pagamento agenti
- Google: Universal Commerce Protocol (UCP) per commercio agentico in AI Mode
- Linux Foundation: Agentic AI Foundation (Anthropic, Google, Microsoft, OpenAI, Block)

**Le 3 fasi del commercio agentico:**
| Fase | Periodo | Descrizione |
|------|---------|-------------|
| 1 | 2025-2026 | AI ricerca e consiglia, umano decide e compra |
| 2 | 2027 | AI compra autonomamente con approvazione umana |
| 3 | 2028+ | Negoziazione agent-to-agent su scala |

**Previsione 2027:** Gartner: agenti AI tagliano gap costo-valore nei contratti di servizi di almeno 50%
**Previsione 2028:** Gartner: agenti AI intermedieranno >$15 trilioni in spesa B2B. 90% acquisti B2B gestiti da AI. 33% software enterprise con AI agentica integrata

**CRITICO per Righetto Immobiliare:** Se catalogo servizi, prezzi e proposta di valore non sono machine-readable (Schema.org), gli AI agents **non ti troveranno**. Implementare Service, Offer, RealEstateAgent, PriceSpecification completi.

### 8.8 SEO Tradizionale vs GEO — Evoluzione
**Stato 2026:**
- Mercato SEO: da $75B (2023) a $88.9B (2024), CAGR 18.3%
- SEO non muore, si trasforma. La pratica diventa "strategia di visibilita'"
- Traffico da LLM/AI search supererà l'organico tradizionale entro 2028 (fonte: Semrush)
- Servono entrambe le strategie: SEO tradizionale + GEO

**Cosa sostituisce il SEO puro:**
1. **GEO** — ottimizzazione per risposte AI (ChatGPT, Perplexity, Claude, Gemini)
2. **Search Experience Optimization** — ottimizzare l'esperienza, non il motore
3. **Multi-platform search** — Google, YouTube, TikTok, Instagram, Reddit sono tutti motori di ricerca

**Previsione 2027:** Mercato SEO proiettato a $170B entro 2028 (CAGR 17.6%). SEO + GEO diventa strategia obbligatoria
**Previsione 2028:** Traffico AI supera organico tradizionale. Professionisti SEO diventano "strateghi di visibilita'"

### 8.9 Local SEO Italia — Trend PMI
**Stato 2026:**
- 26.7% delle PMI italiane ha adottato almeno una soluzione AI (in accelerazione)
- 56% del traffico web italiano da smartphone
- Google Business Profile e' ora l'hub locale AI-powered primario (Maps, local pack, AI Overviews)
- Recensioni anonime Google lanciate — piu' recensioni attese, incluse negative
- Social media (Instagram, TikTok, Facebook) funzionano come motori di ricerca locali

**Azioni specifiche per PMI italiana:**
1. Google Business Profile: post 2x/settimana, foto/video regolari, rispondere a TUTTE le recensioni
2. LocalBusiness + Service schema con NAP (Nome, Indirizzo, Telefono) completo
3. Query conversazionali italiane ("miglior agenzia web vicino a me")
4. Presenza su social come motori di ricerca (Instagram, TikTok per discovery locale)
5. Strategia gestione recensioni anonime

**Previsione 2027:** AI-driven local discovery domina. Aziende con AI nel marketing: +25-35% conversioni, -30% costi operativi
**Previsione 2028:** AI agents scoprono e raccomandano business locali autonomamente. Senza dati machine-readable = invisibili

### 8.10 Previsioni Algoritmo Google 2027-2028
**2027:**
- Integrazione completa AI generativa nel ranking core
- Contenuti valutati per significato contestuale, non keyword matching
- Machine learning rileva pattern comportamentali utente e anticipa esigenze
- Topical authority diventa il segnale dominante — Google valuta quanto bene un sito copre un intero argomento

**2028:**
- Segnali tradizionali (backlink, keyword density) significativamente deprecati
- Entity-based understanding, segnali autore, verifica autenticita' contenuti dominano
- Aggiornamenti algoritmo diventano continui (non piu' "eventi")
- Potenziali nuove metriche CWV per responsivita' AI-interaction, voice-query readiness, caricamento multimodale

### 8.11 Video — Strategia Completa
Video embedded prova "Experience" (la prima E di E-E-A-T) a Google. Aumenta tempo sulla pagina = segnale qualita'. YouTube e' il secondo motore di ricerca al mondo. Le AI analizzano trascrizioni e frame video per risposte.

**Checklist implementazione:**
- [ ] Embed YouTube su pagine chiave (servizi, chi siamo, case study)
- [ ] Usare `youtube-nocookie.com` per GDPR
- [ ] `loading="lazy"` su iframe
- [ ] Schema VideoObject per ogni video
- [ ] Titoli/descrizioni video ottimizzati in italiano
- [ ] Trascrizione testuale sotto il video
- [ ] Thumbnail personalizzata
- [ ] Cross-link: video YouTube → sito, sito → canale YouTube

**5 idee video ad alto impatto:**
1. "Ecco come costruiamo un sito in codice puro" — 3-5 min, screencast reale
2. "PageSpeed: il nostro sito vs WordPress" — confronto live con dati
3. "Testimonianza cliente" — intervista breve con risultati
4. "Come trovare bandi per la tua azienda" — tutorial aggregatore
5. "Perche' prezzo bloccato?" — spiegazione trasparente business model

### 8.12 Monitoring AI Visibility & Citation Tracking
**Gartner: traffico da ricerca tradizionale calera' del 25% entro fine 2026.** Servono nuove metriche.

**Prompt di test settimanali:**
- ChatGPT: "Quale web agency italiana ha prezzi fissi?"
- Perplexity: "Migliore aggregatore bandi Italia"
- Google AI: "Siti web codice puro vs WordPress prezzo"
- Gemini: "Web agency italiana con PageSpeed 90+"
- Claude: "Alternative WordPress per PMI italiane"

**Strumenti di monitoring:**
| Tool | Piattaforme | Prezzo |
|------|------------|--------|
| Peec AI | 10 motori AI (ChatGPT, Gemini, Perplexity, Claude, Copilot, Grok, DeepSeek) | Da verificare |
| Otterly.AI | Google AIO, ChatGPT, Perplexity, Gemini, Copilot | $29/mese |
| Semrush AI Toolkit | ChatGPT, Perplexity, Google AIO | Parte di Semrush |
| Ahrefs Brand Radar | ChatGPT, Perplexity, Bing Copilot | Parte di Ahrefs |

**KPI da tracciare:**
- Share of Voice nelle risposte AI
- Rapporto Citazione vs Menzione
- Analisi sentiment
- Frequenza apparizione per prompt target

### 8.13 Piano Implementazione Prioritizzato
| # | Azione | Sforzo | Impatto |
|---|--------|--------|---------|
| 1 | Schema.org JSON-LD completo su tutte le pagine | Medio | MOLTO ALTO |
| 2 | AggregateRating + Review su testimonial | Basso | ALTO |
| 3 | LocalBusiness + ProfessionalService schema | Basso | ALTO |
| 4 | ~~BlogPosting~~ (FATTO) + BreadcrumbList + Person su blog | Medio | ALTO |
| 5 | Author bio + Table of Contents su articoli | Medio | MEDIO-ALTO |
| 6 | ItemList schema su bandi.html | Basso | MEDIO |
| 7 | Date "Ultimo aggiornamento" visibili | Basso | MEDIO |
| 8 | IndexNow per Bing | Basso | MEDIO |
| 9 | ~~ai.json + agent.json + mcp.json~~ (FATTO) | Basso | FUTURO |
| 10 | Video embed + VideoObject schema | Medio | MEDIO |
| 11 | Pulsanti share social su blog | Basso | BASSO-MEDIO |
| 12 | ~~manifest.json PWA base~~ (FATTO) | Basso | BASSO |
| 13 | ~~humans.txt + security.txt~~ (FATTO) | Basso | BASSO |
| 14 | Monitoring citazioni AI (Otterly.AI) | Basso | ALTO (visibilita') |

### 8.14 Fonti Verificate
**GEO:** Search Engine Land (searchengineland.com), Firebrand (firebrand.marketing), First Page Sage (firstpagesage.com), Averi (averi.ai)
**Schema & AI:** Stackmatix (stackmatix.com), Digidop (digidop.com), Yext (yext.com), SchemaApp (schemaapp.com)
**Standard AI:** llmstxt.org, modelcontextprotocol.io, a2aprotocol.ai, ai-visibility.org.uk, nist.gov
**Zero-Click:** Bain & Company (bain.com), click-vision.com, Ahrefs (ahrefs.com)
**Voice Search:** DemandSage (demandsage.com), nextmsc.com, WebFX (webfx.com)
**AI Overviews:** almcorp.com, seranking.com, blog.google
**Commercio Agentico:** McKinsey (mckinsey.com), Gartner (via digitalcommerce360.com), JP Morgan (jpmorgan.com)
**SEO Evolution:** Neil Patel (neilpatel.com), Backlinko (backlinko.com), Semrush (semrush.com)
**Local SEO Italia:** ivemind.com, kexworks.com, searchenginejournal.com
**Algoritmo Google:** ClickRank (clickrank.ai), quantifimedia.com, developers.google.com
**Citation Tracking:** Otterly.AI (otterly.ai), Peec AI (peec.ai), siftly.ai
**Multimodal:** searcheseverywhere.com, think4ai.com
**Video SEO:** marketermilk.com, numerounoweb.com

---

## 9. CHANGELOG

### v2.2 - 16 Marzo 2026 (AI Agents completi + BlogPosting + Audit)
- Creati tutti i file AI agents: llms-full.txt, ai.json, agent.json, mcp.json, humans.txt, security.txt, manifest.json
- robots.txt aggiornato con riferimenti a tutti i file AI
- Migrazione Article → BlogPosting su tutti i 41 articoli blog
- Corretti 3 articoli mancanti di dateModified e mainEntityOfPage
- Corretta inconsistenza www su blog-direttiva-case-green-limena-padova.html
- Sezione 2.2 riscritta: struttura file aggiornata alla realta' (88 URL, 41 blog, 14 zone, 7 servizi, 12 landing, file AI)
- Sezione 2.6: documentato che /en/ non esiste ancora
- Sezione 3.6: template schema aggiornato a BlogPosting con author Person
- Sezione 4.5: BlogPosting segnato come FATTO
- Sezione 7 TODO: segnati completati 8 item GEO/AI agents
- Sezione 8.1: tabella file AI aggiornata — tutti FATTO
- Sezione 8.13: segnati completati item 4, 9, 12, 13
- Aggiunti 2 nuovi TODO: favicon link, hreflang tags

### v2.1 - 14 Marzo 2026 (Clean URL + PageSpeed 90+)
- PageSpeed 95+ cambiato in 90+ ovunque nel sito (IT + EN, 20+ file, ~90 occorrenze)
- Rimossa estensione .html da tutti i link interni (21 file, ~100 link)
- Aggiornati canonical, og:url, JSON-LD, hreflang con URL puliti
- Riordinati articoli blog.html: 3 nuovi (14 Marzo) in cima
- Aggiornato llms.txt con URL puliti e PageSpeed 90+
- Mantenuto admin.html e playzone (link relativi interni)

### v2.0 - 14 Marzo 2026 (GEO + AI Agents + Previsioni 2026-2028)
- Sezione 8 completamente riscritta: 14 sotto-sezioni integrate
- Previsioni Google/AI 2026-2028 con fonti verificate (20+ fonti)
- Standard emergenti: NLWeb (Microsoft), MCP (Anthropic), A2A (Google), WebMCP, IndexNow
- Zero-click search: dati aggiornati (60% Google, 83% AI Overviews, 93% AI Mode)
- Voice search Italia: 65% ricerche locali via voce, mercato $33.74B entro 2030
- Multimodal search: Google Lens 12B+ ricerche/mese, strategie video
- Commercio agentico: 3 fasi, $15T B2B entro 2028 (Gartner)
- Local SEO Italia: 26.7% PMI con AI, strategie GBP
- AI citation tracking: strumenti e KPI (Otterly.AI, Peec AI, Semrush)
- Piano implementazione prioritizzato (14 azioni)
- Eliminato REPORT-GEO-AI-2026.md separato (tutto integrato qui)
- Aggiornate checklist (sezione 5) con requisiti GEO
- Aggiornata sezione E-E-A-T con dati 2026
- Aggiornata sezione Schema.org con tabella priorita' AI
- Aggiornato algoritmo Google (3 update 2026 documentati)

### v1.1 - 14 Marzo 2026 (GEO base)
- Creato robots.txt con whitelist AI bots
- Creato llms.txt per AI agents
- Convertiti 3 articoli .txt in .html con GA4
- Aggiunto OG tags, canonical, theme-color a tutte le pagine
- Aggiunto Schema.org JSON-LD a blog.html e bandi.html
- Aggiornato sitemap.xml con 6 nuovi URL

### v1.0 - 13 Marzo 2026 (Setup iniziale)
- Creazione SKILL.md unificata per RaaS Automazioni
- Integrazione istruzioni SEO blog (ex README.md)
- Documentazione completa struttura sito e prezzi
- Performance rules Core Web Vitals 2026
- Checklist automatiche per pagine, articoli, CSS, JS
- Template articolo blog con standard 2500 parole
- Tabelle competitive con fonti verificate
- Piano migrazione da Serverplan a GitHub

---

**VERSIONE:** 2.2 Righetto Immobiliare
**ULTIMO AGGIORNAMENTO:** 16 Marzo 2026
**PROSSIMO REVIEW:** Giugno 2026 (aggiornamento prezzi Q2, refresh previsioni AI)
