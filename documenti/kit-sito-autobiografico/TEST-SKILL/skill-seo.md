# SKILL-SEO — Sito autobiografico

> Carica per: audit SEO, meta, schema, Search Console, GEO/AEO.

---

## 1. Schema markup

### Person (Chi sono / bio blog)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "[Nome Cognome]",
  "jobTitle": "[Personal trainer / …]",
  "description": "[…]",
  "url": "https://[dominio].it/chi-sono",
  "image": "https://[dominio].it/img/[foto].webp",
  "worksFor": {
    "@type": "SportsActivityLocation",
    "name": "[Palestra]"
  },
  "sameAs": ["https://instagram.com/…", "https://linkedin.com/…"]
}
```

### LocalBusiness / palestra

```json
{
  "@type": ["LocalBusiness", "SportsActivityLocation"],
  "name": "[…]",
  "telephone": "+39…",
  "address": { "@type": "PostalAddress", … },
  "geo": { "@type": "GeoCoordinates", "latitude": …, "longitude": … },
  "hasMap": "https://maps.google.com/?q=…",
  "openingHoursSpecification": […],
  "sameAs": […]
}
```

**Regole:** JSON-LD · FAQ = testo visibile · Breadcrumb su tutte tranne home

---

## 2. GEO + AEO

1. Prime 2 righe sezione = frase completa estraibile da AI
2. H2 domanda → 40–60 parole risposta → approfondimento
3. Min 5 FAQ + FAQPage schema
4. Dati numerici solo verificabili
5. Timestamp aggiornamento su cornerstone

---

## 3. Fattori ranking (priorità)

1. E-E-A-T (storia vera, foto reali, certificazioni)
2. Intent di ricerca (locale + personal brand)
3. Core Web Vitals
4. Mobile-first
5. Schema + GeoCoordinates
6. Internal linking (bio ↔ servizi ↔ blog)
7. Google Business Profile allineato al sito

---

## 4. NAP (Name Address Phone)

Identico su: sito · footer · contatti · schema · Google Business Profile · Instagram bio

---

## 5. Search Console — routine

### Setup
- Proprietà tipo **Dominio**: `[dominio].it`
- URL canonici: `https://[dominio].it/...`
- Sitemap inviata: **solo** `sitemap.xml`

### Venerdì (~15 min)

1. **Prestazioni** 7+28 gg → 1 opportunità + 1 anomalia → salva in `gsc-keywords-priority.json`
2. **Indicizzazione → Pagine** → snapshot in `gsc-indexing-weekly.json`
3. Fix 404 deployati → **Convalida correzione**
4. **Sitemap** → stato Riuscita
5. **Ispezione URL** — max ~10 richieste/giorno:

```
https://[dominio].it/
https://[dominio].it/chi-sono
https://[dominio].it/[attivita-palestra]
https://[dominio].it/contatti
https://[dominio].it/blog
+ 5 URL strategiche
```

### Lunedì (~10 min)

- [ ] 10 URL: presenti o richiesta inviata
- [ ] Canonical = dominio ufficiale
- [ ] 404/redirect in calo

### Messaggi GSC — guida rapida

| Messaggio | Azione |
|-----------|--------|
| URL presente su Google | OK |
| Pagina alternativa con canonical | OK su www — ignorare |
| Pagina con reindirizzamento | Aspetta re-crawl post-fix DNS |
| Scansionata non indicizzata | Migliora contenuto + link interni |
| 404 | Redirect 301 o rimuovi link |

**Non reinviare** pagine singole come sitemap.

---

## 6. PAGE SCORE (priorità settimanale)

| Label | Azione |
|-------|--------|
| **SOSTENERE** | imp alte, 0 click → title/meta + sezione + link |
| **GEO** | Manca FAQ → aggiungi schema + box sintesi |
| **AGGIUNGERE** | Keyword senza pagina → 1 articolo (anti-doppioni) |
| **MANTENERE** | OK → solo data aggiornamento |
| **CONSOLIDARE** | 2 URL stesso tema → 301 + link |

---

## 7. Audit SEO — comandi utili

- Ispezione URL manuale in GSC
- Rich Results Test dopo modifica schema
- PageSpeed homepage dopo modifica CSS
- Confronto `sitemap.xml` vs file HTML pubblicati

---

## 8. Anti-pattern

- Due versioni www e non-www indicizzate senza regole
- Title identico su tutte le pagine
- Bio generica «appassionato di fitness»
- Schema aggregateRating inventato
- Articoli duplicati stesso argomento
