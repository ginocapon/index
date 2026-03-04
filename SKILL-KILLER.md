# SKILL KILLER - Prompt Operativo per righettoimmobiliare.it
### (Il nome e' ironico, ma il contenuto e' serissimo)

> **Versione:** 1.2 - 4 Marzo 2026
> **Ultimo aggiornamento Google verificato:** Marzo 2026
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
index.html          - Homepage (1.1 MB, canvas animato)
immobili.html       - Lista immobili
immobile.html       - Dettaglio immobile
servizi.html        - Pagina servizi
chi-siamo.html      - Chi siamo
contatti.html       - Form contatti
blog.html           - Blog
faq.html            - FAQ
admin.html          - Pannello admin
js/chatbot.js       - Chatbot Sara (1,595 righe)
js/config.js        - Configurazioni API
js/welcome-popup.js - Popup benvenuto
js/cookie-consent.js - Cookie consent
sitemap.xml         - Sitemap per Google
robots.txt          - Direttive crawler
CNAME               - Dominio GitHub Pages
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
- **AI Analysis Tools** in Search Console - analisi con linguaggio naturale
- **Query Groups** in Search Console Insights - raggruppamento query simili
- **Discover Core Update** (5 Feb 2026) - algoritmo separato per Google Discover
- **SVT e VSI** - Nuove metriche per stabilita' visiva
- **Soglie INP piu' strette** - Google ha reso piu' severi i requisiti di interattivita'
- Rimosso supporto per **practice problem** e **dataset structured data**

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

## CHANGELOG AGGIORNAMENTI

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
