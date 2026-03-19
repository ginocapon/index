# Regole Universali per Siti Web Performanti
### Guida riutilizzabile per qualsiasi progetto web

> **Versione:** 1.0 — Marzo 2026
> **Basato su:** Google Core Updates 2026, Core Web Vitals, GEO/AEO best practices

---

## 1. CORE WEB VITALS — Soglie 2026

| Metrica | Buono | Da migliorare | Scarso |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.0s (target competitivo) | 2.0s - 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| **SVT** (Smooth Visual Transitions) | Penalizza caricamenti "scattosi" |
| **VSI** (Visual Stability Index) | Misura stabilita' visiva durante tutta la sessione |
| **Engagement Reliability** | Misura affidabilita' interazioni (click, form, menu) nel tempo e su diversi device |

> **Nota:** Il target LCP competitivo nel 2026 e' sotto 2 secondi (non piu' 2.5s). Il 43% dei siti ancora non passa la soglia INP di 200ms.

---

## 2. PERFORMANCE ABOVE-THE-FOLD (Visual Saliency)

> Il 57% del tempo di visualizzazione resta above the fold. Google misura questa esperienza tramite LCP, CLS, INP.

### 2.1 LCP — Largest Contentful Paint

- L'immagine hero DEVE essere preloaded nel `<head>`:
  ```html
  <link rel="preload" href="img/hero.webp" as="image">
  ```
- **MAI** `loading="lazy"` su elementi above-the-fold
- Formato **WebP obbligatorio** per immagini locali
- Il path del preload DEVE corrispondere al path effettivo nell'HTML
- Animazioni sull'elemento LCP: partire in **pausa**, avviare dopo il primo render
  ```css
  .hero-bg { animation-play-state: paused; }
  .hero-bg.loaded { animation-play-state: running; }
  ```

### 2.2 Font Loading

- **Preload obbligatorio** per i font usati above-the-fold:
  ```html
  <link rel="preload" href="fonts/mio-font-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/mio-font-700.woff2" as="font" type="font/woff2" crossorigin>
  ```
- `font-display: swap` su tutti i `@font-face`
- **Self-hosted WOFF2** preferibile (no Google Fonts esterni = GDPR compliance + velocita')

### 2.3 CLS — Prevenzione Layout Shift

- **TUTTE** le immagini DEVONO avere `width` e `height` espliciti
- Immagini caricate via JS: aggiungere `width`, `height` e `style="aspect-ratio:..."`
- Navbar fissa: usare `height` con CSS variable (`var(--nav-h)`)
- Mai caricare contenuto asincrono above-the-fold senza **placeholder dimensionato**

### 2.4 CTA Above-the-Fold

- **UN solo CTA primario** per hero section (Hick's Law: troppe scelte = paralisi)
- Contrast ratio minimo **4.5:1** (WCAG AA) — meglio **7:1** (WCAG AAA)
- MAI usare glass morphism (bianco su bianco) per CTA primarie
- Hover: feedback visivo chiaro (`translateY(-2px)` + `box-shadow`)

### 2.5 Critical CSS

- CSS per hero/nav/above-fold: **inline** nel `<style>` del `<head>`
- CSS per contenuto below-fold: caricare via `<link rel="stylesheet">`
- Mai caricare l'intero CSS inline se supera **50KB**
- CSS non critico: defer con tecnica media swap:
  ```html
  <link rel="stylesheet" href="css/below-fold.css" media="print" onload="this.media='all'">
  ```

---

## 3. SEO ON-PAGE — Checklist per Ogni Pagina

### 3.1 Meta Tag e Struttura

- [ ] **Title tag** unico (max 60 caratteri)
- [ ] **Meta description** unica (max 160 caratteri)
- [ ] **H1 unico** per pagina
- [ ] **Alt text** su tutte le immagini
- [ ] **URL SEO-friendly** (slug descrittivi, senza .html)
- [ ] **Canonical URL** impostato
- [ ] **Open Graph tags** per condivisione social
- [ ] **HTTPS** obbligatorio

### 3.2 Link e Struttura

- [ ] **Link interni** verso pagine correlate (cross-linking contestuale)
- [ ] **Clean URLs** — rimuovere estensioni .html dai link interni
- [ ] **Breadcrumbs** con schema BreadcrumbList
- [ ] Nessun **broken link** (audit periodico)

### 3.3 Immagini

- [ ] Formato **WebP** per tutte le immagini locali
- [ ] `loading="lazy"` su immagini **below-the-fold**
- [ ] `width` + `height` espliciti su **tutte** le immagini
- [ ] Alt text descrittivo e con keyword dove naturale

### 3.4 Dati Strutturati (Schema.org)

- [ ] Schema appropriato al tipo di pagina (LocalBusiness, Product, Article, FAQPage, ecc.)
- [ ] **GeoCoordinates** nello schema per attivita' locali:
  ```json
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 45.123456,
    "longitude": 11.654321
  },
  "hasMap": "https://maps.google.com/?q=45.123456,11.654321"
  ```
- [ ] **FAQPage** schema per pagine con domande frequenti (minimo 5 FAQ)
- [ ] **Review** schema per pagine con testimonianze/recensioni
- [ ] Validare con [Google Rich Results Test](https://search.google.com/test/rich-results)

### 3.5 File Tecnici

- [ ] `sitemap.xml` aggiornata con tutte le pagine pubbliche
- [ ] `robots.txt` configurato correttamente
- [ ] `llms.txt` — nuovo standard emergente per guidare AI bots (come robots.txt ma per LLM)

---

## 4. FATTORI DI RANKING GOOGLE 2026

1. **Qualita' del contenuto** — E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
2. **Rilevanza semantica** — Contenuto che risponde all'intento di ricerca
3. **Core Web Vitals** — Performance come fattore decisivo a parita' di contenuto
4. **Mobile-first** — Google indicizza prima la versione mobile
5. **Dati strutturati** — Schema.org per rich snippets
6. **GEO (Generative Engine Optimization)** — Ottimizzazione per essere citati da AI
7. **AEO (Answer Engine Optimization)** — Ottimizzazione per featured snippets
8. **Link interni** — Ogni pagina importante deve essere collegata internamente
9. **HTTPS** — Obbligatorio
10. **Contenuto originale** — Penalizzazione per clickbait e contenuti superficiali
11. **Topical Authority** — Google valuta la copertura complessiva di un topic, non singole pagine
12. **Page Experience consistency** — Siti con performance inconsistente (home veloce, blog lento) penalizzati

---

## 5. GEO — Generative Engine Optimization

> Ottimizzazione dei contenuti per essere citati dalle AI generative (Gemini, ChatGPT, Perplexity, Copilot). Il 40% delle ricerche nel 2026 passa per assistenti AI.

### 5.1 Regole GEO per Ogni Contenuto

1. **Frasi dichiarative** nelle prime 2 righe di ogni sezione (le AI estraggono da li')
2. **Dati numerici specifici** e verificabili
3. **Formato:** Domanda H2 → Risposta diretta (40-60 parole) → Approfondimento
4. **Liste, tabelle, definizioni chiare** — formato che le AI prediligono
5. **Citare fonti ufficiali** per aumentare la fiducia
6. Contenuti **freschi** — contenuti >3 mesi perdono citazioni AI (recency bias forte)

### 5.2 Regole AEO per Featured Snippets

1. **Risposta 40-60 parole** come primo paragrafo dopo ogni H2
2. **Formato is-snippet:** "[Keyword] e' [definizione/risposta]"
3. **Min 5 FAQ** in formato Q&A con Schema FAQPage
4. **Tabelle comparative** per dati numerici

### 5.3 Checklist GEO/AEO

- [ ] Frasi dichiarative nelle prime 2 righe di ogni sezione
- [ ] Dati numerici specifici e verificabili
- [ ] Formato: Domanda H2 + Risposta diretta + Approfondimento
- [ ] Liste, tabelle, definizioni chiare
- [ ] Min 5 FAQ con Schema FAQPage
- [ ] Risposta 40-60 parole come primo paragrafo per ogni H2
- [ ] Citazioni fonti ufficiali

---

## 6. PERFORMANCE — Regole Generali

### 6.1 JavaScript

- **No librerie/framework non necessari** — mantenere il sito leggero
- Script non critici: `defer` o `async`
- Lazy load per componenti below-the-fold (IntersectionObserver)
- Mai bloccare il rendering con script sincroni nel `<head>`

### 6.2 CSS

- **Critical CSS inline** nel `<head>` (solo above-the-fold)
- CSS non critico caricato in modo asincrono
- Minificare CSS in produzione
- Evitare `@import` nei CSS (causa richieste sequenziali)

### 6.3 Immagini e Media

- **WebP** come formato predefinito
- Dimensioni appropriate (non caricare immagini 4000px per uno spazio 400px)
- `loading="lazy"` per tutto cio' che e' below-the-fold
- Placeholder/skeleton per immagini caricate dinamicamente
- Video: usare **facade pattern** (thumbnail + click per caricare iframe)
  ```html
  <!-- Non caricare iframe YouTube direttamente — usa un thumbnail cliccabile -->
  <div class="video-facade" onclick="loadVideo(this)">
    <img src="thumbnail.webp" alt="Video" width="640" height="360">
    <button aria-label="Play">▶</button>
  </div>
  ```

### 6.4 Network

- **Preconnect** a domini esterni necessari:
  ```html
  <link rel="preconnect" href="https://api.esempio.com">
  <link rel="dns-prefetch" href="https://api.esempio.com">
  ```
- Minimizzare richieste HTTP (combinare file dove possibile)
- Abilitare **compressione gzip/brotli** lato server

---

## 7. MOBILE-FIRST — Regole

- **Progettare prima per mobile**, poi adattare per desktop
- Touch target minimo: **44x44px** (Apple HIG) / **48x48px** (Material Design)
- Font size minimo: **16px** per body text (evita zoom automatico su iOS)
- Viewport meta tag obbligatorio:
  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1">
  ```
- Testare su dispositivi reali, non solo emulatori
- Menu hamburger: area tocco generosa, animazione fluida
- Form: input `type` appropriati (`tel`, `email`, `number`) per tastiera corretta

---

## 8. ACCESSIBILITA' (WCAG)

- Contrast ratio minimo **4.5:1** per testo normale, **3:1** per testo grande
- **Alt text** su tutte le immagini informative, `alt=""` per immagini decorative
- **Focus visible** su tutti gli elementi interattivi
- Struttura heading gerarchica (H1 → H2 → H3, senza salti)
- **aria-label** su icone/bottoni senza testo visibile
- Form: ogni input ha un `<label>` associato
- Skip navigation link per screen reader

---

## 9. SICUREZZA

- **HTTPS** obbligatorio su tutto il sito
- **Content Security Policy** headers dove possibile
- Sanitizzare tutti gli input utente (prevenzione XSS)
- **SameSite** cookies
- API keys: mai esposte nel frontend se sono segrete
- Form: protezione CSRF + rate limiting

---

## 10. LOCAL SEO (per attivita' locali)

### 10.1 Google Business Profile

- [ ] Profilo ottimizzato al 100%: categorie, servizi, attributi
- [ ] **Google Posts** settimanali (novita', offerte, articoli)
- [ ] **Foto** settimanali (prodotti, team, sede)
- [ ] **Q&A** del profilo compilate
- [ ] Orari, accessibilita', servizi completi

### 10.2 Recensioni

- [ ] Processo sistematico di richiesta recensioni post-servizio
- [ ] Mai comprare recensioni false (penalita' gravissime)
- [ ] Rispondere a TUTTE le recensioni (positive e negative)

### 10.3 Citazioni NAP

- [ ] Nome/Indirizzo/Telefono **IDENTICO** su tutti i portali e directory
- [ ] Stesso formato ovunque (es. "Via Roma 1, 35100 Padova PD")

### 10.4 Backlink Locali

- [ ] Directory locali (PagineGialle, Yelp, Cylex, TuttoCitta)
- [ ] Collaborazioni con professionisti del settore (scambio link)
- [ ] Comunicati stampa su quotidiani/portali locali
- [ ] Guest post su blog di settore
- [ ] Profili associazioni di categoria con link al sito

---

## 11. CONTENT STRATEGY

### 11.1 Topic Cluster

- Creare **pagine pillar** per keyword principali
- Creare **cluster di contenuti** collegati alla pillar
- **Cross-linking** tra tutti i contenuti del cluster
- Ogni cluster copre un topic in modo completo (topical authority)

### 11.2 Blog/Contenuti

- Minimo **2 articoli al mese** per freshness signals
- Articoli **>1500 parole** per contenuti informativi
- Formato consigliato: Domanda → Risposta → Approfondimento
- Aggiornare contenuti esistenti (non solo crearne di nuovi)
- Data di pubblicazione/aggiornamento visibile

### 11.3 Landing Pages

- Una landing per ogni **keyword/servizio principale**
- **Un solo obiettivo** per landing (CTA unica)
- Social proof (recensioni, numeri, loghi clienti)
- Form contatto breve (meno campi = piu' conversioni)

---

## 12. CHECKLIST VISUAL SALIENCY (per ogni pagina)

- [ ] Hero image preloaded nel `<head>`
- [ ] Font above-fold preloaded
- [ ] Nessun `loading="lazy"` su elementi above-the-fold
- [ ] Tutte le immagini con `width` + `height` espliciti
- [ ] CTA primario con contrast ratio >= 4.5:1
- [ ] Un solo CTA primario nel hero
- [ ] Animazioni hero: partono dopo il primo render
- [ ] Critical CSS inline, rest deferred

---

## 13. MONITORAGGIO

### Routine Consigliata

- **Settimanale:** Controllare report performance in Search Console
- **Mensile:** Analisi dettagliata metriche SEO e Core Web Vitals
- **Trimestrale:** Audit completo contenuti e struttura sito
- **Ad ogni aggiornamento Google:** Verificare impatto sul sito

### Strumenti

- [Google Search Console](https://search.google.com/search-console)
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Web Vitals Extension](https://chrome.google.com/webstore/detail/web-vitals/) (Chrome)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/) (DevTools)

---

## 14. REGOLE OPERATIVE PER LO SVILUPPATORE / AI

1. **Leggi prima** il file che vuoi modificare — mai proporre modifiche al buio
2. **Testa** che le modifiche non rompano niente
3. **Ottimizza** per mobile-first
4. **Mantieni** la coerenza del design esistente
5. **Non aggiungere** librerie/framework non necessari — il sito deve restare leggero
6. **Commit** chiari e descrittivi
7. **Controlla** Core Web Vitals dopo modifiche significative
8. **Aggiorna** sitemap.xml quando aggiungi/rimuovi pagine
9. **Verifica** che tutte le pagine abbiano meta tag SEO completi
10. **Visual Saliency** — ogni pagina nuova DEVE seguire le regole above-the-fold
11. **Performance** — mai introdurre animazioni sull'elemento LCP senza `animation-play-state: paused`
12. **Non sovra-ingegnerizzare** — solo le modifiche necessarie, niente di piu'

---

*Questo file puo' essere usato come riferimento per qualsiasi progetto web. Copia, adatta i valori specifici (colori, font, coordinate GPS) e segui le checklist.*
