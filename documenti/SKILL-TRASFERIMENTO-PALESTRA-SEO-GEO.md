# SKILL — Palestra / Brand personale (da template Righetto)

> Copia questo file nel nuovo progetto come `SKILL-CORE.md` o cartella `TEST-SKILL/`.  
> Sostituisci tutti i placeholder `[…]`. Documento operativo SEO · GEO · AEO · GSC · contenuti.

---

## 0. Architettura consigliata

```
SKILL-CORE.md                 ← gate obbligatorio (leggere sempre)
skill-essentials.md           ← regole operative quotidiane
skill-massimo-punteggio.md    ← checklist Google 10/10
skill-seo.md                  ← SEO + GEO + Search Console
skill-content.md              ← blog, pillar, anti-doppioni
skill-design.md               ← mobile, WCAG, Core Web Vitals
context-map.json              ← routing task → skill
data/gsc-indexing-weekly.json
data/gsc-keywords-priority.json
data/editorial-queue.json
.cursor/skills/*/SKILL.md     ← slash: /seo /blog /venerdi /mobile
```

**Principio:** una sola fonte di verità. L’agente legge la skill **prima** di modificare file.

---

## 1. Claim consentiti (compilare e verificare)

| Dato | Valore |
|------|--------|
| Nome palestra / brand | […] |
| Nome trainer (se brand personale) | […] |
| Attivo dal | [anno] |
| Indirizzo (NAP ufficiale) | [via, CAP, città] |
| Telefono | […] |
| Recensioni Google | [N] recensioni — [voto]/5 |
| Certificazioni | [CONI, ISSA, NASM, …] |
| Superficie sala / posti corsi | [solo se verificabile] |

> **REGOLA D’ORO:** se non hai fonte verificabile, **NON** inserire il dato.  
> Vietato: «miglior palestra», «N°1 in città», percentuali risultati clienti senza prova.

---

## 2. Regole operative (sempre)

1. **Leggi il file** da modificare — mai al buio
2. **Mobile-first** — ogni modifica deve funzionare su iPhone (375px)
3. **URL pulite** — canonical, sitemap, link interni: stesso formato (con o senza `.html`, ma **coerente**)
4. **Un solo dominio canonico** — apex **oppure** www, non entrambi indicizzati
5. **Sitemap GSC** — inviare **solo** `sitemap.xml`, mai URL singole pagine
6. **Aggiorna `sitemap.xml`** ad ogni pagina aggiunta/rimossa
7. **Cache-busting** — CSS/JS linkati con `?v=N`; incrementa a ogni modifica
8. **WCAG AA** — contrasto CTA ≥ 4,5:1; **mai** arancione acceso + testo bianco
9. **Performance** — no `loading="lazy"` su hero/LCP; preload hero + font critici
10. **No animazioni pesanti** above-the-fold; no `filter: blur` su animazioni
11. **Commit** solo se richiesto; **push** solo se esplicito
12. **DNS / hosting** — non toccare senza conferma utente

---

## 3. Title e meta (BLOCCANTE)

| Campo | Target | Massimo |
|-------|--------|---------|
| `<title>` | ≤60 caratteri | ≤70 |
| `meta description` | 120–155 caratteri | ≤160 |

**Regole:**
- Title, H1 e meta = **varianti diverse** (non copiare la stessa frase)
- Keyword + città + brand nel title
- Verificare conteggio caratteri **prima** di pubblicare

**Esempi palestra:**
- Title: `Personal trainer [Città] | [Nome] — [Specialità]`
- Meta: `Allenamento personalizzato a [Città]. [Nome] — certificato […]. Prova gratuita. Tel. […]`

---

## 4. Checklist ogni nuova pagina

- [ ] Title/meta §3 OK
- [ ] H1 unico
- [ ] Alt text su ogni `<img>`
- [ ] Canonical URL ufficiale
- [ ] Open Graph + Twitter Card
- [ ] Schema.org (vedi §5)
- [ ] Min 3 link interni verso servizi / prenotazione / blog
- [ ] Registrata in `sitemap.xml`
- [ ] Frasi dichiarative prime 2 righe (GEO §6)
- [ ] Min 5 FAQ + schema `FAQPage` (servizi, pillar, zone)
- [ ] Mobile OK, CTA visibile
- [ ] Hero preload, no lazy above-the-fold

---

## 5. Schema.org (JSON-LD)

### Homepage / contatti — `LocalBusiness` + `SportsActivityLocation`

```json
{
  "@context": "https://schema.org",
  "@type": ["LocalBusiness", "SportsActivityLocation"],
  "name": "[Nome Palestra]",
  "description": "[…]",
  "url": "https://[dominio].it",
  "telephone": "+39[…]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[…]",
    "addressLocality": "[Città]",
    "postalCode": "[CAP]",
    "addressCountry": "IT"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": […],
    "longitude": […]
  },
  "hasMap": "https://maps.google.com/?q=[lat],[lon]",
  "openingHoursSpecification": […],
  "priceRange": "€€",
  "sameAs": [
    "https://www.instagram.com/[…]",
    "https://www.facebook.com/[…]",
    "https://g.page/[…]"
  ]
}
```

> `aggregateRating` solo se recensioni Google reali e verificabili.

### Pagina trainer — `Person`

```json
{
  "@type": "Person",
  "name": "[Nome Cognome]",
  "jobTitle": "Personal Trainer",
  "worksFor": { "@type": "SportsActivityLocation", "name": "[Palestra]" },
  "sameAs": ["Instagram", "LinkedIn", …],
  "knowsAbout": ["fitness", "nutrizione sportiva", "…"]
}
```

### Su ogni pagina importante
- `BreadcrumbList`
- `FAQPage` (testo visibile = JSON-LD)
- `BlogPosting` + `dateModified` sugli articoli

---

## 6. GEO + AEO

### GEO (Generative Engine Optimization)
1. **Prime 2 righe** di ogni sezione: frase **dichiarativa** auto-contenuta  
   *Es.: «[Nome Palestra] a [Città] offre personal training e corsi functional in sala da [X] mq, orari […].»*
2. Dati numerici **solo verificabili**
3. Fonti per salute/nutrizione: ISS, ministero Salute — non inventare
4. Timestamp «Ultimo aggiornamento» su pillar
5. Opzionale: `llms.txt` + `ai.json` con URL pillar (ChatGPT/Perplexity; Google usa SEO standard)

### AEO (Answer Engine / featured snippet)
- H2 = **domanda**
- Primo paragrafo dopo H2 = **40–60 parole** risposta diretta
- Min **5 FAQ** con schema per pagina servizio
- Tabelle comparative (abbonamenti, corsi, orari)

---

## 7. E-E-A-T (fiducia)

| Pilastro | Azioni |
|----------|--------|
| **Experience** | Foto reali, video allenamento, storia personale |
| **Expertise** | Certificazioni visibili, metodo, specializzazioni |
| **Authority** | Pagina autore, articoli pillar, presenza GBP/social |
| **Trust** | NAP identico ovunque, privacy GDPR, recensioni, contatti chiari |

**Obbligatorio:**
- Pagina `/chi-sono` o `/[nome-trainer]` con bio + schema `Person`
- Bio autore su ogni articolo blog
- NAP sito = Google Business Profile = social

---

## 8. Contenuti e blog

### Cluster consigliati

| Cluster | Esempi slug |
|---------|-------------|
| Brand + local | `/palestra-[città]`, `/personal-trainer-[città]` |
| Servizi | `/personal-training`, `/crossfit`, `/yoga`, `/nutrizione` |
| Informazionale | `/quanto-costa-palestra-[città]`, `/prima-volta-in-palestra` |
| Zona | `/palestra-[quartiere]` (se ha senso localmente) |
| Brand personale | `/[nome]`, metodo, storia |

### Standard articolo pillar
- **1500–2500+ parole utili** (no paragrafi ripetuti)
- **10–15 H2/H3**
- **Anti-doppioni:** verificare che titolo/slug/intent non esistano già
- **Max 1 articolo nuovo/settimana**
- **3+ link interni** verso servizi e CTA prenotazione
- Copertina WebP 1200×630 leggera
- Box sintesi nelle prime 150 parole

### Editorial queue (JSON)

```json
{
  "updated": "YYYY-MM-DD",
  "items": [
    {
      "id": "eq-001",
      "status": "scheduled",
      "slug": "blog-personal-trainer-[città]-guida-2026",
      "kw": "personal trainer [città]",
      "week": "YYYY-MM-DD"
    }
  ]
}
```

---

## 9. Search Console — routine

### Setup
- Proprietà GSC tipo **Dominio**: `[dominio].it`
- URL canonici: `https://[dominio].it/...` (**senza** www se apex è ufficiale)
- Sitemap: **solo** `https://[dominio].it/sitemap.xml`

### Venerdì (~15 min)

1. **Prestazioni** (7 + 28 gg): 1 opportunità (CTR basso o pos. 11–20) + 1 anomalia
2. **Indicizzazione → Pagine:** snapshot; se fix 404 deployati → **Convalida correzione**
3. **Sitemap:** stato **Riuscita** / Operazione riuscita
4. **Ispezione URL** — 10 pagine chiave (max ~10 richieste/giorno):

```
https://[dominio].it/
https://[dominio].it/chi-sono
https://[dominio].it/palestra-[città]
https://[dominio].it/personal-training
https://[dominio].it/abbonamenti
https://[dominio].it/contatti
https://[dominio].it/blog
https://[dominio].it/[articolo-pillar-1]
https://[dominio].it/[articolo-pillar-2]
https://[dominio].it/[servizio-principale]
```

5. Salva snapshot in `data/gsc-indexing-weekly.json` e `data/gsc-keywords-priority.json`

### Lunedì (~10 min)

- [ ] 10 URL: «URL presente su Google» o «Richiesta inviata»
- [ ] Canonical in ispezione = URL ufficiale (no www se apex)
- [ ] 404 e redirect in calo vs settimana precedente

### Leggere i messaggi GSC

| Messaggio | Significato | Azione |
|-----------|-------------|--------|
| **Pagina alternativa con canonical** | OK su www — Google usa la versione ufficiale | Nessuna |
| **Pagina con reindirizzamento** | Transitorio post-fix DNS | Attendi 1–2 settimane |
| **Scansionata, non indicizzata** | Google ha letto, non prioritizza | Tempo + qualità contenuto |
| **Rilevata, non indicizzata** | In coda | Normale |
| **404** | URL vecchia | Redirect 301 |

**Non fare:** reinviare URL singole nella barra Sitemap.

---

## 10. PAGE SCORE — priorità settimanale

| Etichetta | Quando | Azione |
|-----------|--------|--------|
| **SOSTENERE** | Impressioni ≥20, 0 click | Rifare title/meta + 1 sezione + 3 link interni |
| **GEO** | Manca FAQ/box sintesi | FAQ schema + risposta 40–60 parole |
| **AGGIUNGERE** | Keyword gap senza pagina | 1 articolo (dopo anti-doppioni) |
| **MANTENERE** | Score alto, click ok | Solo timestamp / dato |
| **CONSOLIDARE** | 2 URL stesso intent | 301 + link interni |
| **MONITORARE** | Nessun trigger | Nessuna azione |

**Pesi:** GSC potential 25% · profondità 20% · freshness/GEO 20% · link interni 15% · keyword fit 20%

---

## 11. Ciclo 12 settimane

| Sett. | Focus | Output minimo |
|-------|--------|---------------|
| 1 | Baseline GSC | 5 URL da migliorare (CTR o pos. 11–20) |
| 2 | Link interni | Da homepage → 2 servizi/pillar |
| 3 | Blog | 1 articolo nuovo O refresh + FAQ |
| 4 | Locale | Pagina zona/quartiere o «vicino a…» |
| 5 | CWV | Audit LCP mobile homepage + 1 template |
| 6 | Conversione | Landing prova gratuita — CTA + form |
| 7 | Schema | Allineare JSON-LD su tutte le pagine |
| 8 | Trust | GBP post + recensioni; NAP = sito |
| 9 | Pillar | 1 pezzo 2000+ parole (guida palestra [città]) |
| 10 | Stagionalità | Cluster (settembre iscrizioni, gennaio…) |
| 11 | Sitemap | Confronto sitemap vs pagine live |
| 12 | Review | Cosa ha funzionato + piano trimestre |

---

## 12. Google Business Profile

- NAP **identico** al sito
- Categoria: Palestra / Centro fitness / Personal trainer
- Post 1×/settimana (orari, promo, foto)
- Rispondi a **tutte** le recensioni
- Foto reali sala + team ogni mese
- Link sito = URL canonical
- UTM: `?utm_source=gbp&utm_medium=organic`

---

## 13. Cursor — skill da creare

| Skill | Trigger utente | Moduli |
|-------|----------------|--------|
| `core-task` | modifiche sito generiche | essentials + massimo-punteggio |
| `seo` | audit, meta, GSC, schema | seo + massimo-punteggio |
| `blog` | nuovo articolo | content |
| `landing` | prova gratuita, iscrizione | form + design |
| `venerdi` | piano settimanale, GSC | seo + content |
| `mobile` | iPhone, layout rotto | design |

**Rule always-on (`.cursor/rules/core.mdc`):**
- Leggi SKILL-CORE prima di ogni modifica
- Mobile-first + WCAG
- Aggiorna sitemap
- Regola d’oro sui dati

---

## 14. Strumenti gratuiti

| Strumento | URL | Uso |
|-----------|-----|-----|
| PageSpeed Insights | https://pagespeed.web.dev/ | LCP, INP, CLS |
| Search Console | https://search.google.com/search-console | Indicizzazione, query |
| Rich Results Test | https://search.google.com/test/rich-results | Schema JSON-LD |
| Schema Validator | https://validator.schema.org/ | Errori structured data |
| Mobile-Friendly Test | https://search.google.com/test/mobile-friendly | Mobile-first |
| WAVE | https://wave.webaim.org/ | Accessibilità |

---

## 15. Checklist Google 10/10 (sintesi)

### Indicizzazione
- [ ] robots.txt OK
- [ ] sitemap.xml aggiornata
- [ ] canonical unica
- [ ] HTTPS
- [ ] mobile 375px OK

### On-page
- [ ] title/meta §3
- [ ] H1 unico
- [ ] alt text
- [ ] OG completi
- [ ] no keyword stuffing

### CWV
- [ ] LCP < 2,5s
- [ ] CLS < 0,1
- [ ] no lazy su LCP

### Schema
- [ ] LocalBusiness + geo + sameAs
- [ ] FAQPage dove serve
- [ ] BreadcrumbList
- [ ] Person su pagina autore

### Contenuti
- [ ] pillar utili, no riempimento
- [ ] anti-doppioni
- [ ] fonti verificabili
- [ ] E-E-A-T visibile

---

## 16. Cosa NON copiare da Righetto Immobiliare

- Claim immobiliari (350+ immobili, 101 comuni, OMI, FIMAA…)
- Schema `RealEstateAgent`
- Mandati mediazione / provvigioni
- Script Supabase immobili, sync foto annunci
- Cluster zone Padova/Limena
- `llms.txt` / blog immobiliare specifici

---

## 17. Template `data/gsc-indexing-weekly.json`

```json
{
  "updated": "YYYY-MM-DD",
  "source": "GSC manuale — venerdì",
  "sitemap_main": {
    "url": "https://[dominio].it/sitemap.xml",
    "status": "Riuscita",
    "discovered_pages": 0
  },
  "indexed": 0,
  "not_indexed": 0,
  "by_reason": {
    "redirect": 0,
    "crawled_not_indexed": 0,
    "not_found_404": 0,
    "discovered_not_indexed": 0
  },
  "manual_checks": {
    "sitemap_ok": true,
    "prestazioni_note": ""
  }
}
```

---

*Template generato da workflow Righetto Immobiliare — luglio 2026. Adattare al progetto palestra/brand personale.*
