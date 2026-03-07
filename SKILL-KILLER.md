# SKILL KILLER - Prompt Operativo per righettoimmobiliare.it
### (Il nome e' ironico, ma il contenuto e' serissimo)

> **Versione:** 1.6 - 7 Marzo 2026
> **Ultimo aggiornamento Google verificato:** 7 Marzo 2026 (Core Update confermato + Engagement Reliability)
> **Prossima verifica consigliata:** Aprile 2026

---

## ISTRUZIONI PER CLAUDE

Quando ricevi questo prompt, segui SEMPRE queste regole:

### 1. VERIFICA AGGIORNAMENTI GOOGLE (OBBLIGATORIA)
Prima di ogni sessione di lavoro sul sito, DEVI:
- Fare una ricerca web per: `"Google Search updates [mese corrente] [anno corrente]"`
- Fare una ricerca web per: `"Core Web Vitals updates [anno corrente]"`
- Fare una ricerca web per: `"Google Search Console new features [anno corrente]"`
- Fare una ricerca web per: `"GEO Generative Engine Optimization updates [anno corrente]"`
- Fare una ricerca web per: `"Core Web Vitals LCP CLS best practices [anno corrente]"`
- Confrontare i risultati con la sezione "STATO AGGIORNAMENTI GOOGLE" qui sotto
- Se trovi novita', AGGIORNA questo file aggiungendo le nuove informazioni nella sezione apposita
- Comunica all'utente cosa e' cambiato rispetto all'ultima volta

### 2. AGGIORNA QUESTO PROMPT
Ogni volta che trovi aggiornamenti rilevanti:
- Aggiungi la data e il contenuto nella sezione "CHANGELOG AGGIORNAMENTI"
- Aggiorna i parametri tecnici se sono cambiati (soglie Core Web Vitals, nuovi meta tag, ecc.)
- Fai commit e push delle modifiche a questo file

---

## CONTESTO PROGETTO

### Informazioni Generali
- **Dominio:** righettoimmobiliare.it / www.righettoimmobiliare.it
- **Hosting sito:** GitHub Pages (deploy automatico da branch `main`)
- **Hosting dominio/email:** cPanel su cpanel.righettoimmobiliare.it
- **Utente cPanel:** wyrighet
- **Home directory cPanel:** /home3/wyrighet
- **Tech Stack:** HTML statico + CSS + JavaScript + Express.js (dev)
- **Database:** Supabase (esterno)
- **Newsletter:** Brevo (Sendinblue)
- **Form contatti:** Formspree
- **Analytics:** Google Analytics 4 (G-9MHDHHES26)
- **Chatbot AI:** "Sara" - assistente virtuale integrata
- **Repository:** GitHub - ginocapon/index

### Architettura DNS (NON TOCCARE MAI)
- **Record A:** punta a GitHub Pages (185.199.108.153, etc.)
- **CNAME www:** punta a ginocapon.github.io
- **Record MX:** gestione email su cPanel (NON MODIFICARE)
- **Google Site Verification:** meta tag nel `<head>` di index.html

### File Principali del Sito
```
index.html                          - Homepage
immobili.html                       - Lista immobili
immobile.html                       - Dettaglio immobile
agenzia-immobiliare-padova.html     - Pagina pillar "agenzia immobiliare padova" (keyword #1)
servizi.html                        - Pagina servizi hub
servizio-vendita.html               - Servizio vendita (con FAQ)
servizio-locazioni.html             - Servizio locazioni
servizio-preliminari.html           - Servizio preliminari
servizio-valutazioni.html           - Servizio valutazioni (con FAQ)
servizio-gestione.html              - Servizio gestione immobili
servizio-utenze.html                - Servizio utenze
chi-siamo.html                      - Chi siamo
contatti.html                       - Form contatti
blog.html                           - Blog hub
blog-*.html (18 articoli)           - Articoli blog SEO
faq.html                            - FAQ (30+ domande)
zona-*.html (8 quartieri)           - Pagine quartieri Padova (con RealEstateAgent + FAQPage schema)
landing-vendita.html                - Landing vendita
landing-valutazione.html            - Landing valutazione
landing-agente.html                 - Landing agente
admin.html                          - Pannello admin
js/chatbot.js                       - Chatbot Sara + dati FAQ + database prezzi
js/config.js                        - Configurazioni API
js/welcome-popup.js                 - Popup benvenuto
js/cookie-consent.js                - Cookie consent
js/nav-mobile.js                    - Navigazione mobile
js/scroll-reveal.js                 - Animazioni scroll
scripts/seo-content-generator.js    - Generatore template SEO per nuovi articoli
sitemap.xml                         - Sitemap per Google (40 URL)
robots.txt                          - Direttive crawler
CNAME                               - Dominio GitHub Pages
SKILL-KILLER.md                     - QUESTO FILE — prompt operativo master
SERP-STRATEGY.md                    - Copia dettagliata strategia SERP (deprecato, tutto in SKILL-KILLER.md)
```

---

## GESTIONE cPanel - COSA ELIMINARE E COSA TENERE

### DA ELIMINARE (per liberare spazio)
| File/Cartella | Dimensione | Motivo |
|---|---|---|
| `backup-3.2.2026_10-53-22_wyrighet.tar.gz` | **37.04 GB** | Backup completo - scaricato in locale, eliminare dal server |
| `public_htmlcopia140422.zip` | **11.37 GB** | Backup vecchio sito WordPress del 2022 - obsoleto |
| `error_log` | variabile | Log errori - non servono piu' |
| `error_log-*.gz` | ~13 KB totali | Log errori compressi vecchi |
| `error_log_php` | variabile | Log errori PHP |
| `error_log_php-*.gz` | ~65 KB totali | Log errori PHP compressi |
| `sp_mysql_bk/` | variabile | Backup MySQL vecchi (WordPress non c'e' piu') |
| `public_html/` contenuto | variabile | Vecchio sito WordPress - ora il sito e' su GitHub Pages |
| **Database MySQL** | variabile | Database WordPress - non piu' necessari |
| **Email non utilizzate** | fino a 17 GB | Account email vecchi e messaggi non necessari |

### DA TENERE ASSOLUTAMENTE (NON TOCCARE)
| Elemento | Motivo |
|---|---|
| **Record DNS** | A, CNAME, MX - fanno funzionare sito e email |
| **Dominio** | righettoimmobiliare.it registrato qui |
| **Account email attivi** | Email che usi quotidianamente |
| **Certificato SSL** | Per HTTPS |
| **Cartella `mail/`** | Contiene le caselle email attive |
| **Cartella `etc/`** | Configurazioni del server |
| **Cartella `ssl/`** | Certificati SSL |
| **cPanel stesso** | Pannello di controllo |

### Cartelle di Sistema cPanel (NON ELIMINARE)
- `cache/` - Cache di sistema
- `etc/` - Configurazioni
- `logs/` - Log attivi (si auto-puliscono)
- `mail/` - Caselle email
- `perl5/` - Moduli Perl di sistema
- `php_sessions/` - Sessioni PHP
- `public_ftp/` - FTP pubblico
- `ssl/` - Certificati
- `tmp/` - File temporanei (si auto-puliscono)
- `access-logs` - Symlink ai log

---

## REQUISITI SEO GOOGLE - AGGIORNATI MARZO 2026

### Google Search Console - Configurazione
- [x] Verifica proprieta' tramite meta tag HTML nel `<head>`
- [x] Sitemap XML inviata (`sitemap.xml`)
- [x] robots.txt configurato
- [x] Google Analytics 4 attivo (G-9MHDHHES26)
- [ ] Verifica proprieta' dominio anche via DNS TXT (consigliato come backup)

### Core Web Vitals - Soglie 2026
| Metrica | Buono | Da migliorare | Scarso |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| **SVT** (Smooth Visual Transitions) - NUOVO 2026 | Penalizza caricamenti "scattosi" |
| **VSI** (Visual Stability Index) - NUOVO 2026 | Misura stabilita' durante tutta la sessione |

### Fattori di Ranking Principali 2026
1. **Qualita' del contenuto** - E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
2. **Rilevanza semantica** - Contenuto che risponde all'intento di ricerca
3. **Core Web Vitals** - Performance come fattore decisivo a parita' di contenuto
4. **Mobile-first** - Google indicizza prima la versione mobile
5. **Dati strutturati** - Schema.org per rich snippets + GeoCoordinates per local SEO
6. **GEO (Generative Engine Optimization)** - Ottimizzazione per essere citati da AI (Gemini, ChatGPT, Perplexity)
7. **AEO (Answer Engine Optimization)** - Ottimizzazione per featured snippets e risposte dirette
8. **Link interni** - Ogni pagina importante deve essere collegata internamente
9. **HTTPS** - Obbligatorio
10. **Contenuto originale** - Penalizzazione per clickbait e contenuti superficiali

### Novita' Google Marzo 2026
- **March 2026 Core Update** - Confermato ufficialmente, rollout dal 7 marzo, ~2 settimane per completamento. Focus su: E-E-A-T, topical authority, local relevance, page experience consistency
- **Topical Authority rafforzata** - Google valuta la copertura complessiva di un topic sul sito, non singole pagine
- **Local Relevance potenziata** - Vantaggio per siti che comunicano chiaramente zona e area servizi
- **Page Experience consistency** - Siti con performance inconsistente (home veloce, blog lento) penalizzati
- **AI Analysis Tools** in Search Console - analisi con linguaggio naturale
- **Search Console AI-powered configuration tool** - lanciato marzo 2026
- **Query Groups** in Search Console Insights - raggruppamento query simili
- **Custom Annotations** in Performance Reports - note personalizzate sui grafici
- **Branded Queries Filter** - separazione automatica query brand/non-brand
- **AI Mode data** contato nei totali Performance Report di Search Console
- **Nuovi link styles in AI Mode/AI Overviews** - Google ha aggiornato come mostra i link
- **UCP-powered checkout in AI Mode** - integrazione e-commerce in risposte AI
- **Google review policies aggiornate** - molte recensioni sparite (verificare le nostre!)
- **Discover Core Update** (5 Feb 2026) - piu' contenuti locali, meno clickbait, piu' contenuti originali (completato 27 feb)
- **SVT e VSI** - Nuove metriche per stabilita' visiva
- **Engagement Reliability** - NUOVA metrica CWV: misura affidabilita' interazioni (click, form, menu) nel tempo e su diversi device
- **LCP target piu' severo** - Il target competitivo nel 2026 e' sotto 2 secondi (non piu' 2.5s)
- **Soglie INP piu' strette** - 43% dei siti ancora non passa la soglia 200ms
- Rimosso supporto per **practice problem** e **dataset structured data**
- **GEO tipping point 2026** - ChatGPT 800M utenti/settimana, Gemini 750M/mese, AI Overviews in 16%+ ricerche
- **GEO critico nel 2026** - 40% ricerche via AI, recency bias forte (contenuti >3 mesi perdono citazioni), overlap SEO/GEO sceso sotto 20%
- **GEO content converte 4.4x** vs SEO tradizionale ($3.71 return per $1 investito)
- **llms.txt** - Nuovo standard emergente per guidare AI bots (come robots.txt ma per LLM)
- **Ranking volatility estrema** - Cali organici 20-35% riportati da molti siti da febbraio-marzo 2026

### GEO — Generative Engine Optimization (NUOVO 2026)

> **Cos'e':** Ottimizzazione dei contenuti per essere citati dalle AI generative
> (Gemini, ChatGPT, Perplexity, Copilot). Dove il SEO punta ai click,
> il GEO punta a essere **la fonte citata** nelle risposte AI.

**Perche' e' critico per un'agenzia immobiliare locale:**
- Il 35% delle ricerche nel 2026 passa per assistenti AI
- Le AI con dati strutturati hanno **300% di accuratezza in piu'** nel citare un sito
- Domande tipo "miglior agenzia immobiliare Padova" → le AI rispondono citando fonti strutturate

**Regole GEO per ogni contenuto:**
1. **Frasi dichiarative** nelle prime 2 righe di ogni sezione (le AI estraggono da li')
2. **Dati numerici specifici** e verificabili (prezzi/mq, anni esperienza, N. immobili)
3. **Formato:** Domanda H2 → Risposta diretta (40-60 parole) → Approfondimento
4. **Liste, tabelle, definizioni chiare** — formato che le AI prediligono
5. **Citare fonti ufficiali** (Agenzia Entrate, OMI, FIAIP) per aumentare la fiducia

**Regole AEO (Answer Engine Optimization) per featured snippet:**
1. **Risposta 40-60 parole** come primo paragrafo dopo ogni H2
2. **Formato is-snippet:** "[Keyword] e' [definizione/risposta]"
3. **Min 5 FAQ** in formato Q&A con Schema FAQPage
4. **Tabelle comparative** per dati numerici (prezzi zone, confronti)

### GeoCoordinates — Dati Geografici nello Schema Markup

**Ogni pagina con schema LocalBusiness/RealEstateAgent DEVE includere:**
```json
"geo": {
  "@type": "GeoCoordinates",
  "latitude": 45.476956,
  "longitude": 11.845762
},
"hasMap": "https://maps.google.com/?q=45.476956,11.845762"
```

**Perche':**
- Essenziale per ricerche "vicino a me" / "near me" (in forte crescita)
- Google Maps usa queste coordinate per posizionamento preciso
- Senza `geo`, Google indovina la posizione dall'indirizzo — meno preciso
- Le ricerche vocali (35% nel 2026) dipendono pesantemente da questi dati

### Visual Saliency — Regole Performance Above-the-Fold

> **Cos'e':** La salienza visiva determina cosa cattura l'occhio dell'utente nei primi
> 50-500 millisecondi. Il 57% del tempo di visualizzazione resta above the fold.
> Google misura questa esperienza tramite Core Web Vitals (LCP, CLS, INP).

**Regole obbligatorie per ogni pagina:**

1. **LCP Element (hero image/headline)**
   - L'immagine hero DEVE essere preloaded nel `<head>`: `<link rel="preload" href="..." as="image">`
   - MAI `loading="lazy"` su elementi above-the-fold
   - Formato WebP obbligatorio per immagini locali
   - Il path del preload DEVE corrispondere al path effettivo nell'HTML
   - Animazioni sull'elemento LCP: partire in pausa, avviare dopo il primo render

2. **Font Loading**
   - Preload obbligatorio per i font usati above-the-fold:
     ```html
     <link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
     <link rel="preload" href="fonts/cormorant-garamond-600.woff2" as="font" type="font/woff2" crossorigin>
     ```
   - `font-display: swap` su tutti i `@font-face`
   - Self-hosted WOFF2 (no Google Fonts esterni = GDPR + velocita')

3. **CLS (Layout Shift) Prevention**
   - TUTTE le immagini DEVONO avere `width` E `height` espliciti
   - Immagini caricate via JS: aggiungere `width`, `height` e `style="aspect-ratio:..."`
   - Navbar fissa: usare `height` con CSS variable (`var(--nav-h)`)
   - Mai caricare contenuto asincrono above-the-fold senza placeholder dimensionato

4. **CTA Above-the-Fold**
   - UN solo CTA primario per hero section (Hick's Law: troppe scelte = paralisi)
   - Contrast ratio minimo **4.5:1** (WCAG AA) — meglio **7:1** (WCAG AAA)
   - Il nostro standard: **oro solido `var(--oro)` con testo `var(--nero)`** = 5.2:1
   - MAI usare glass morphism (bianco su bianco) per CTA primarie
   - Hover: feedback visivo chiaro (`translateY(-2px)` + box-shadow)

5. **Critical CSS**
   - CSS per hero/nav/above-fold: inline nel `<style>` del `<head>`
   - CSS per contenuto below-fold: caricare via `<link rel="stylesheet">`
   - Mai caricare l'intero CSS inline se supera 50KB

**Palette colori approvata per CTA (contrast-safe):**
| Elemento | Background | Testo | Ratio |
|----------|-----------|-------|-------|
| CTA primario | `var(--oro)` #B8D44A | `var(--nero)` #0A0F1C | 5.2:1 ✓ |
| CTA secondario | `var(--blu)` #2C4A6E | `white` | ~5:1 ✓ |
| CTA landing | `var(--fire)` arancione | `white` | ~4.5:1 ✓ |
| CTA valutazione | `var(--purple)` #6C63FF | `white` | ~4.5:1 ✓ |
| CTA landing-agente | `var(--mint)` #00E5A0 | `var(--nero)` | ~5.5:1 ✓ |

### Checklist Visual Saliency per Ogni Pagina
- [ ] Hero image preloaded nel `<head>`
- [ ] Font above-fold preloaded (Montserrat 400 + Cormorant 600)
- [ ] Nessun `loading="lazy"` su elementi above-the-fold
- [ ] Tutte le immagini con `width` + `height` espliciti
- [ ] CTA primario con contrast ratio >= 4.5:1
- [ ] Un solo CTA primario nel hero (no doppi bottoni)
- [ ] Animazioni hero: partono dopo il primo render
- [ ] Critical CSS inline, rest deferred

### Checklist SEO per Ogni Pagina
- [ ] Title tag unico (max 60 caratteri)
- [ ] Meta description unica (max 160 caratteri)
- [ ] H1 unico per pagina
- [ ] Alt text su tutte le immagini
- [ ] URL SEO-friendly (slug descrittivi)
- [ ] Link interni verso pagine correlate
- [ ] Open Graph tags per condivisione social
- [ ] Canonical URL impostato
- [ ] Dati strutturati Schema.org (LocalBusiness, RealEstateListing)
- [ ] GeoCoordinates nello schema LocalBusiness/RealEstateAgent
- [ ] Immagini ottimizzate (WebP + lazy loading)

### Checklist GEO/AEO per Ogni Contenuto
- [ ] Frasi dichiarative nelle prime 2 righe di ogni sezione
- [ ] Dati numerici specifici e verificabili
- [ ] Formato: Domanda H2 + Risposta diretta + Approfondimento
- [ ] Liste, tabelle, definizioni chiare
- [ ] Min 5 FAQ con Schema FAQPage
- [ ] Risposta 40-60 parole come primo paragrafo per ogni H2
- [ ] Citazioni fonti ufficiali (Agenzia Entrate, OMI, FIAIP)

### Routine di Monitoraggio
- **Settimanale:** Controllare report performance in Search Console
- **Mensile:** Analisi dettagliata metriche SEO e Core Web Vitals
- **Trimestrale:** Audit completo contenuti e struttura sito
- **Ad ogni aggiornamento Google:** Verificare impatto sul sito

---

## REGOLE OPERATIVE PER CLAUDE

### Quando lavori sul sito, SEMPRE:
1. **Leggi prima** il file che vuoi modificare - mai proporre modifiche al buio
2. **Testa** che le modifiche non rompano niente
3. **Ottimizza** per mobile-first
4. **Mantieni** la coerenza del design esistente
5. **Non aggiungere** librerie/framework non necessari - il sito e' volutamente leggero
6. **Commit** chiari e descrittivi in italiano
7. **Mai toccare** la configurazione DNS o i record MX
8. **Controlla** Core Web Vitals dopo modifiche significative
9. **Aggiorna** sitemap.xml quando aggiungi/rimuovi pagine
10. **Verifica** che tutte le pagine abbiano meta tag SEO completi
11. **Visual Saliency** — ogni pagina nuova DEVE seguire le regole above-the-fold (preload, contrast, CLS)
12. **Performance** — mai introdurre animazioni sull'elemento LCP senza `animation-play-state: paused`
13. **Pubblicazione articoli blog** — OBBLIGATORIO registrare ogni nuovo articolo in TUTTI questi punti, altrimenti non comparira' nel sito ne' nell'admin:
    - `admin.html` → array `_blogSeedArticles` (seed per admin panel)
    - `blog.html` → array `articoliStatici` (listing pagina blog)
    - `js/homepage.js` → oggetto `staticMap` (mapping titolo→url) + array `articoliStatici` (card homepage)
    - `sitemap.xml` → nuovo URL
    - **VERIFICA FINALE:** dopo il push, controllare che l'articolo compaia nell'admin panel come "Pubblicato" e nella pagina blog del sito

### Quando lavori sulle email/cPanel:
1. **NON eliminare** mai account email senza conferma esplicita
2. **NON modificare** record DNS senza conferma esplicita
3. **Suggerisci** sempre prima e aspetta il via libera
4. **Backup** prima di eliminazioni importanti

### Stile di Comunicazione:
- Rispondi in italiano
- Sii diretto e pratico
- Usa termini tecnici ma spiega quando necessario
- Proponi sempre prima di agire su operazioni irreversibili

---

## ANALISI COMPETITIVA E STRATEGIA SERP

> **IMPORTANTE PER CLAUDE:** Questa sezione contiene l'analisi completa dei competitor,
> lo stato delle SERP, le strategie da implementare e i KPI da monitorare.
> Ad ogni sessione di lavoro, VERIFICA lo stato di avanzamento delle checklist qui sotto
> e comunica all'utente cosa e' stato fatto e cosa resta da fare.

### Stato Attuale SERP (verificato 7 marzo 2026)

| Keyword | Posizione Righetto | Chi appare |
|---|---|---|
| "agenzia immobiliare padova" | **NON APPARE** | Immobiliare.it, Tetto Rosso, RicercAttiva, Promopadova, Dove.it, RockAgent |
| "vendere casa padova agenzia" | **NON APPARE** | Pianeta Casa, Grimaldi, Dove.it, Tetto Rosso, RockAgent, Tecnocasa |
| "migliore agenzia immobiliare padova" | **NON APPARE** | Gruppo Bortoletti, SZ Affari, RockAgent, Dove.it, Promopadova, StarOfService |
| "comprare casa padova" | **NON APPARE** | Idealista, Immobiliare.it, Subito, Tecnocasa (portali dominano) |
| "mutuo padova" / "consulenza mutuo padova" | **NON APPARE** (landing creata!) | Banche, comparatori — da monitorare |
| "Righetto Immobiliare Padova" | **SI (brand)** | Idealista, Immobiliare.it, Casa.it, Wikicasa |

**Problema principale**: SEO on-page il migliore tra i competitor locali (confermato), ma domain authority troppo bassa per competere nelle SERP. I nuovi competitor nazionali (Dove.it, RockAgent) alzano l'asticella.

### Punteggio Complessivo Sito (7 marzo 2026)

| Area | Punteggio | Note |
|---|---|---|
| SEO on-page | **9.5/10** | Il migliore tra i competitor locali |
| Schema.org | **9/10** | Solo 4 service pages senza FAQPage |
| Contenuti/Blog | **8/10** | Buono, RicercAttiva ha piu' contenuti fiscali/legali |
| GEO/AEO | **8.5/10** | Unico a ottimizzare per AI — vantaggio forte |
| Core Web Vitals | **8/10** | Buono, target LCP ora <2s da raggiungere |
| Chatbot AI | **10/10** | Unico nel mercato locale — vantaggio esclusivo |
| Simulatore mutuo | **10/10** | Unico nel mercato locale — vantaggio esclusivo |
| Recensioni Google | **6/10** | 127 vs 256 Tetto Rosso — gap critico |
| Domain Authority | **4/10** | Problema #1 — nessun backlink significativo |
| Apparizione SERP | **2/10** | Non appare per nessuna keyword non-brand |
| **TOTALE** | **7.5/10** | Sito tecnicamente top, invisibile nelle SERP |

### Competitor Diretti — Confronto (aggiornato 7 marzo 2026)

| Feature | Righetto | Tetto Rosso | RicercAttiva | Pianeta Casa | Dove.it | RockAgent | Grimaldi |
|---|---|---|---|---|---|---|---|
| Clean URLs | **Forte** | Forte | Forte | Forte | Forte | Forte | Forte |
| FAQ Pages | **Si (top)** | Si | No | No | No | No | No |
| Blog/Content | **Si** | Si | **Si (top)** | Si | **Forte** | **Forte** | Si |
| Schema.org | **Esteso (top)** | Buono | Buono | Base | Buono | Buono | Buono |
| Recensioni Google | ~127 | **~256** | Poche | ~104 | N/D (nazionale) | N/D | N/D |
| Qualita sito | **Alta** | Alta | Buona | Buona | **Alta** | **Alta** | Buona |
| Chatbot AI | **Si (unico!)** | No | No | No | No | No | No |
| Simulatore mutuo | **Si (unico!)** | No | No | No | No | No | No |
| GEO/AEO ottimizzato | **Si (unico!)** | No | No | No | Parziale | No | No |
| Dati mercato visibili | Si | No | No | No | **Si (top)** | **Si (top)** | No |
| Landing dedicate | **5** | 1 | 2 | 1 | Molte | Molte | 1 |
| Zero commissioni | No | No | No | No | **Si (venditore)** | Ridotte | No |
| Appare in SERP | **NO** | **SI** | **SI** | No | **SI** | **SI** | **SI** |

**NUOVI competitor identificati (marzo 2026):**
- **Dove.it** — Zero commissioni venditore, molto aggressivo su Padova, contenuti forti
- **RockAgent** — Agenzia ibrida, dati mercato prominenti (2.456 €/mq medio Padova)
- **Gruppo Bortoletti** — Appare per "migliore agenzia immobiliare Padova"
- **Promopadova** — Marketing locale forte, foto professionali gratuite

**Competitor #1 — Tetto Rosso Immobiliare (PERICOLO ALTO)**
- 4 uffici incluso **Limena** (stessa zona nostra)
- **256 recensioni Google** (il doppio delle nostre)
- FAQ page + Magazine/Blog
- **Appaiono in SERP** per "vendere casa padova agenzia"
- LEZIONE: la differenza e' nei backlink e nella longevita del dominio

### SUPER KILL 1 — Google Business Profile (PRIORITA N.1)
- [ ] Ottimizzare profilo GBP al 100%: tutte le categorie (agenzia immobiliare, consulente immobiliare, valutatore immobiliare)
- [ ] Aggiungere TUTTI i servizi nel GBP: vendita, acquisto, affitto, valutazione, gestione, virtual tour
- [ ] Pubblicare Google Posts OGNI SETTIMANA (nuovi immobili, articoli blog, offerte)
- [ ] Aggiungere foto OGNI SETTIMANA (immobili, team, ufficio, eventi)
- [ ] Compilare tutte le Q&A del profilo GBP (le stesse FAQ del sito)
- [ ] Verificare che gli attributi siano completi (orari, accessibilita, servizi)

### SUPER KILL 2 — Recensioni Google (GAP PIU CRITICO)
- [ ] Tetto Rosso ha 256 recensioni, Pianeta Casa 104, Righetto ~127 (non verificato)
- [ ] AZIONE: messaggio WhatsApp post-rogito con link diretto a Google Review
- [ ] OBIETTIVO: +30 recensioni/anno (bastano i rogiti normali)
- [ ] SCRIPT messaggio: "Gentile [nome], grazie per aver scelto Righetto Immobiliare! Se il nostro servizio ti ha soddisfatto, ci farebbe piacere una tua recensione su Google: [link]. Ci aiuta molto!"
- [ ] MAI comprare recensioni false — penalita = rimozione TUTTE le recensioni + sospensione GBP + multa AGCM fino a 5M euro

### SUPER KILL 3 — Backlink Locali (COSTRUIRE DOMAIN AUTHORITY)
- [ ] Registrarsi su PadovaOggi / IlGazzettino come fonte esperta (articoli mercato immobiliare)
- [ ] Comunicati stampa su quotidiani locali (dati mercato, report annuali)
- [ ] Collaborazioni con geometri, notai, architetti di Padova (scambio link)
- [ ] Registrazione su directory locali: PagineGialle, Yelp, TripAdvisor, Cylex, TuttoCitta
- [ ] Profilo LinkedIn aziendale con link al sito e contenuti regolari
- [ ] Profilo FIAIP / FIMAA con link al sito
- [ ] Guest post su blog immobiliari nazionali (Idealista News, CasaNoi, etc.)

### SUPER KILL 4 — Citazioni NAP Consistenti
- [ ] Verificare che Nome/Indirizzo/Telefono sia IDENTICO su: Google, Idealista, Immobiliare.it, Casa.it, PagineGialle, Yelp, Cylex, TuttoCitta, Virgilio
- [ ] Formato standard: "Righetto Immobiliare" — usare ovunque lo stesso nome
- [ ] Indirizzo: Via Roma 96, 35010 Limena PD (sempre identico)
- [ ] Telefono: 049 884 3484 (stesso formato ovunque)

### Strategie Rubate ai Concorrenti

**Da Tetto Rosso Immobiliare (competitor #1)**
- 256 recensioni Google: processo sistematico post-vendita
- 4 uffici incluso Limena: prossimita geografica come vantaggio
- [ ] AZIONE: verificare backlink di tettorossoimmobiliare.it con Ahrefs/Semrush

**Da RicercAttiva (competitor #2 per content)**
- Blog aggressivo: articoli su successioni, tasse, agevolazioni, legge di bilancio
- Posizionamento unico: "trovo casa in 90 giorni"
- URL long-tail con keyword (slug lunghissimi)
- [ ] AZIONE: scrivere articoli su temi fiscali/legali per catturare traffico informativo

**Da venderecasapadova.it (Federico Rigato)**
- Dominio exact-match: vantaggio SERP enorme per "vendere casa padova"
- Landing page singola: funnel di conversione diretto, "vendo in 59 giorni"
- Open House technique
- [ ] AZIONE: creare landing-vendere-casa-padova.html ultra-ottimizzata
- [ ] AZIONE: valutare tecnica Open House come differenziazione

**Da Pianeta Casa Padova**
- Widget Google Reviews integrato nel sito (embed reale)
- 104 recensioni con processo strutturato
- Tool confronto immobili
- [ ] AZIONE: aggiungere widget Google Reviews nel footer o homepage

**Da Grimaldi Padova**
- Magazine mensile: freshness signals per Google
- Articoli tecnico-legali che attirano link naturali
- [ ] AZIONE: pubblicare almeno 2 articoli blog al mese

**Da Engel & Volkers**
- Instagram forte: 826 follower per singolo ufficio Padova
- [ ] AZIONE: rafforzare presenza Instagram con reels immobili, storie quartieri

**Da Tempocasa**
- 20.775 recensioni Trustpilot nazionali
- Matterport virtual tour 3D
- "Immobile Certificato": bollino qualita sugli annunci
- [ ] AZIONE: creare bollino "Verificato Righetto" (certificazione documentale pre-pubblicazione)

### Contenuti Mancanti da Creare (Topic Cluster)

**Cluster "Vendere Casa Padova"**
- [x] servizio-vendita.html (pagina servizio + FAQ)
- [x] blog-costi-vendere-casa-padova-2026.html
- [ ] landing-vendere-casa-padova.html (landing dedicata, ultra-ottimizzata)
- [ ] blog-tempi-vendita-casa-padova.html ("quanto tempo per vendere casa a Padova")
- [x] blog-documenti-vendita-casa.html ("documenti per vendere casa")
- [x] blog-tasse-vendita-casa.html ("tasse e costi vendita immobiliare")

**Cluster "Comprare Casa Padova"**
- [x] blog-comprare-casa-padova-guida-2026.html
- [x] blog-mutuo-prima-casa-padova.html
- [x] blog-agevolazioni-prima-casa-2026.html ("bonus prima casa under 36")
- [x] blog-successione-immobiliare-padova.html ("casa ereditata, cosa fare")
- [x] blog-investire-immobiliare-padova.html ("investimento immobiliare Padova")

**Cluster "Quartieri Padova"**
- [x] blog-quartieri-padova-2026.html
- [x] 8 pagine zona-*.html (con RealEstateAgent + FAQPage schema)
- [x] agenzia-immobiliare-padova.html (pagina pillar)
- [ ] zona-limena.html (CRITICO — comune sede agenzia!)
- [ ] zona-vigonza.html
- [ ] zona-abano-terme.html
- [ ] zona-selvazzano.html

**Cluster "Affitto Padova"**
- [x] blog-affitto-studenti-padova.html
- [x] servizio-locazioni.html
- [x] blog-contratto-affitto-padova.html ("canone concordato Padova")
- [x] blog-rendimento-affitto-padova.html ("rendimento locativo per quartiere")

### Azioni Tecniche SEO — Stato Avanzamento

**Completate (4 marzo 2026)**
- [x] Aggiunto RealEstateAgent schema a tutte le 8 zone pages
- [x] Aggiunto FAQPage schema con 4 FAQ specifiche per ogni quartiere
- [x] Aggiunto FAQ section visibile + FAQPage schema a servizio-vendita.html (5 FAQ)
- [x] Aggiunto FAQ section visibile + FAQPage schema a servizio-valutazioni.html (5 FAQ)
- [x] Creata pagina pillar agenzia-immobiliare-padova.html (keyword #1 mancante)
- [x] Aggiornato sitemap.xml con nuova pagina
- [x] Clean URLs: rimosso .html da tutti i link interni
- [x] Fix pagina FAQ vuota (chatbot.js sincrono)

**Da fare (prossime sessioni)**
- [ ] Aggiungere FAQPage schema alle altre 4 service pages (locazioni, preliminari, gestione, utenze)
- [ ] Aggiungere immobile.html alla sitemap (manca!)
- [ ] Creare landing-vendere-casa-padova.html (keyword "vendere casa padova") — PRIORITA ALTA
- [ ] Creare zona-limena.html (comune sede agenzia — CRITICO)
- [x] Creare llms.txt (nuovo standard per guidare AI bots — vantaggio GEO)
- [ ] Aggiungere internal linking tra blog posts e zone pages (cross-link contestuali)
- [x] Aggiunto link alla pagina agenzia-immobiliare-padova nel footer (7 marzo 2026)
- [x] GeoCoordinates aggiunto a landing-mutuo.html (7 marzo 2026)
- [x] CLS fix: width/height su immagini dinamiche blog.html (7 marzo 2026)
- [x] FAQ Mutuo dedicata con 15 domande + schema aggiornato (7 marzo 2026)
- [ ] Verificare tutti i link interni (nessun broken link — audit dice OK)
- [ ] Verificare indexing in Google Search Console dopo deploy
- [ ] Richiedere indicizzazione manuale delle nuove pagine via GSC
- [ ] Aggiungere widget Google Reviews reale nella homepage
- [ ] Verificare che recensioni Google non siano sparite (nuove policies Google!)
- [ ] Ottimizzare LCP sotto 2 secondi (nuovo target competitivo 2026)
- [ ] Configurare hreflang se si prevede versione EN

### KPI da Monitorare

| Metrica | Valore attuale | Obiettivo 3 mesi | Obiettivo 6 mesi |
|---|---|---|---|
| Recensioni Google | ~127 | 140+ | 160+ |
| Posizione "agenzia immobiliare padova" | >100 | Top 30 | Top 10 |
| Posizione "vendere casa padova" | >100 | Top 50 | Top 20 |
| Traffico organico mensile | ? (verificare GSC) | +30% | +80% |
| Pagine indicizzate | ~39 | 45+ | 55+ |
| Backlink da domini unici | ? (verificare) | +10 | +25 |

### Calendario Editoriale Suggerito

| Mese | Contenuto | Keyword target |
|---|---|---|
| Marzo 2026 | zona-limena.html | "case limena", "immobiliare limena" |
| Marzo 2026 | blog-agevolazioni-prima-casa-2026.html | "bonus prima casa 2026" |
| Aprile 2026 | landing-vendere-casa-padova.html | "vendere casa padova" |
| Aprile 2026 | blog-successione-immobiliare.html | "casa ereditata cosa fare" |
| Maggio 2026 | zona-vigonza.html + zona-abano-terme.html | "case vigonza", "case abano terme" |
| Maggio 2026 | blog-rendimento-affitto-padova.html | "investimento affitto padova" |
| Giugno 2026 | blog-contratto-affitto-padova.html | "contratto affitto canone concordato" |
| Giugno 2026 | zona-selvazzano.html | "case selvazzano dentro" |

---

## CHANGELOG AGGIORNAMENTI

### v1.6 - 7 Marzo 2026 (Fix Audit + FAQ Mutuo Dedicata)
- **GeoCoordinates aggiunto a landing-mutuo.html** — mancava nello schema LocalBusiness
- **Link pagina pillar** agenzia-immobiliare-padova aggiunto nel footer homepage (era orfana!)
- **CLS fix blog.html** — aggiunto width/height a tutte le immagini dinamiche (featured, card, sidebar)
- **FAQ Mutuo dedicata** — 15 domande nella pagina FAQ con categoria propria (era sparsa in Acquisto)
- **FAQPage schema aggiornato** — 7 nuove domande mutuo nello structured data (da ~30 a ~37 FAQ)
- **Bottone "Mutuo" in barra categorie FAQ** + link sidebar

### v1.5 - 7 Marzo 2026 (Audit Completo Sito + Aggiornamento Competitor + Google Updates)
- **Audit completo sito vs competitor** — punteggio 7.5/10 (top tecnico, invisibile SERP)
- **Nuovi competitor identificati:** Dove.it (zero commissioni), RockAgent (ibrida), Gruppo Bortoletti, Promopadova
- **Tabella competitor aggiornata** — da 9 a 7 competitor con metriche piu' rilevanti (chatbot, simulatore, GEO)
- **SERP verificata 7 marzo:** Righetto NON appare per nessuna keyword non-brand (confermato)
- **Google March 2026 Core Update confermato ufficialmente** — rollout dal 7 marzo
- **Engagement Reliability** — nuova metrica CWV documentata
- **LCP target aggiornato** — competitivo sotto 2s (non piu' 2.5s)
- **GEO 2026 tipping point:** ChatGPT 800M/settimana, Gemini 750M/mese, conversioni 4.4x vs SEO
- **llms.txt** — nuovo standard emergente documentato (da implementare)
- **Google review policies aggiornate** — rischio perdita recensioni (da verificare!)
- **Ranking volatility estrema** — cali 20-35% riportati da molti siti
- **Aggiunto punteggio complessivo sito** con 10 aree di valutazione
- **Aggiornata lista "Da fare"** — aggiunta immobile.html in sitemap, llms.txt, verifica recensioni, LCP <2s

### v1.4 - 7 Marzo 2026 (5 Conversion Features + Audit SKILL-KILLER)
- **5 feature di conversione implementate:**
  1. Testimonial section in homepage con 3 recensioni reali + Review schema markup
  2. Email gate modal su vendere-casa-padova-errori.html (lead capture prima del PDF)
  3. Sticky mobile CTA bar su homepage, landing-vendita, landing-mutuo, calcolatore
  4. Sezione video fondatore su landing-vendita con YouTube facade pattern
  5. Urgency badges su homepage e calcolatore (prezzi +7% 2026)
- **Audit Visual Saliency completato:** rimosso loading="lazy" da avatar testimonial e video thumbnail
- **Audit GEO/AEO completato:** aggiornato testo intro testimonial con frasi dichiarative
- **Review schema aggiunto:** 3 Review objects individuali nello schema LocalBusiness homepage
- **Fix CLS:** aggiunto width/height a immagine form contatto homepage (700x700)
- **Fix render-blocking CSS:** deferring css/fonts.css e css/nav-mobile.css su calcolatore
- **Hero preload aggiunto:** landing-mutuo.html mancava preload immagine hero
- **Sitemap aggiornato:** aggiunte 4 landing pages mancanti (vendita, mutuo, valutazione, agente) → 47 URL totali
- **Google Core Update Marzo 2026:** documentato rollout, focus su topical authority e local relevance
- **GEO 2026:** aggiornata sezione con dati recenti (40% ricerche via AI, recency bias, overlap <20%)

### v1.3 - 4 Marzo 2026 (Analisi Competitiva + Strategia SERP)
- Aggiunta sezione completa "ANALISI COMPETITIVA E STRATEGIA SERP"
- Tabella confronto 9 competitor (Tetto Rosso, RicercAttiva, Pianeta Casa, Tecnocasa, Gabetti, Engel & Volkers, Tempocasa, Grimaldi, venderecasapadova.it)
- 4 SUPER KILL: Google Business Profile, Recensioni Google, Backlink Locali, Citazioni NAP
- Strategie rubate ai competitor con azioni specifiche
- Topic Cluster con contenuti mancanti da creare (vendere, comprare, quartieri, affitto)
- Stato avanzamento azioni tecniche SEO (completate e da fare)
- KPI da monitorare con obiettivi a 3 e 6 mesi
- Calendario editoriale marzo-giugno 2026
- Implementate: pagina pillar agenzia-immobiliare-padova.html, RealEstateAgent + FAQPage schema su 8 zone pages, FAQ su servizio-vendita e servizio-valutazioni

### v1.2 - 4 Marzo 2026 (Visual Saliency + Performance Rules)
- Aggiunta sezione completa "Visual Saliency — Regole Performance Above-the-Fold"
- Regole LCP: preload obbligatorio hero image + font, no lazy above-fold
- Regole CLS: width+height obbligatori su tutte le immagini
- Regole CTA: contrast ratio minimo 4.5:1, palette colori approvata
- Regole Critical CSS: inline above-fold, defer below-fold
- Aggiunta checklist Visual Saliency per ogni pagina
- Aggiunta verifica Core Web Vitals nella routine obbligatoria
- Fix applicati: CTA oro su index.html, preload corretti, slowZoom pausata

### v1.1 - 4 Marzo 2026 (GEO/AEO + GeoCoordinates)
- Aggiunta sezione GEO (Generative Engine Optimization) con regole per ottimizzazione AI
- Aggiunta sezione AEO (Answer Engine Optimization) per featured snippets
- Aggiunta sezione GeoCoordinates con coordinate GPS azienda (45.476956, 11.845762)
- Aggiunta checklist GEO/AEO per ogni contenuto
- Aggiornata checklist SEO con voce GeoCoordinates
- Aggiornati fattori di ranking con GEO e AEO (punti 6 e 7)
- Aggiunta verifica GEO nella routine di aggiornamento obbligatoria
- Aggiornato seo-content-generator.js con GeoCoordinates nello schema
- Aggiornate tutte le pagine HTML con GeoCoordinates nello schema RealEstateAgent

### v1.0 - 2 Marzo 2026 (Creazione)
- Creato prompt iniziale con stato aggiornamenti Google Marzo 2026
- Documentate soglie Core Web Vitals 2026 (LCP, INP, CLS, SVT, VSI)
- Registrate novita': AI Analysis Tools in GSC, Query Groups, Discover Core Update
- Mappata struttura completa del progetto
- Documentata gestione cPanel con lista eliminazioni/mantenimento
- Impostate regole operative per Claude

---

## NOTE PER L'UTENTE

### Come usare questo prompt:
1. **All'inizio di ogni sessione** con Claude, copia/incolla questo file come contesto
2. Claude fara' automaticamente una verifica web degli aggiornamenti Google
3. Se ci sono novita', Claude aggiornera' questo file
4. Controlla il CHANGELOG per vedere cosa e' cambiato nel tempo

### Questo file si trova in:
- **Nel repository:** `/SKILL-KILLER.md`
- **Scaricalo** e tienine una copia anche in locale

### Per emergenze:
- Il sito e' su GitHub Pages - se qualcosa va storto, basta fare rollback del commit
- Le email sono su cPanel - completamente separate dal sito
- Il dominio e il DNS sono su cPanel - NON toccarli mai senza sapere cosa fai

---

*"Skill Killer" - Perche' con le competenze giuste, si ammazzano i problemi prima che nascano* 😄
