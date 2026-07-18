# SKILL-MASSIMO-PUNTEGGIO — Gate Google (sito autobiografico)

> **GATE OBBLIGATORIO:** leggere prima di ogni modifica HTML/CSS/contenuti.

---

## Ordine lettura sessione

1. Questo file
2. `skill-essentials.md`
3. Modulo task da `context-map.json`
4. File da modificare

---

## 1. Strumenti gratuiti

| Strumento | URL |
|-----------|-----|
| PageSpeed Insights | https://pagespeed.web.dev/ |
| Search Console | https://search.google.com/search-console |
| Rich Results Test | https://search.google.com/test/rich-results |
| Schema Validator | https://validator.schema.org/ |
| Mobile-Friendly | https://search.google.com/test/mobile-friendly |
| WAVE (accessibilità) | https://wave.webaim.org/ |

---

## 2. Checklist Google — tutte le aree

### 2.1 Indicizzazione
- [ ] `robots.txt` non blocca pagine importanti
- [ ] `sitemap.xml` aggiornata
- [ ] Canonical unica per URL
- [ ] HTTPS, no mixed content
- [ ] Mobile 375px OK

### 2.2 On-page
- [ ] Title ≤60 (max 70), meta 120–155 (max 160)
- [ ] H1 unico, variante del title
- [ ] H2 a domanda dove utile (AEO)
- [ ] Alt text su ogni img
- [ ] OG completi
- [ ] No keyword stuffing (max ~5× stessa frase lunga)

### 2.3 Core Web Vitals
- [ ] LCP < 2,5s — preload hero + font
- [ ] No `loading="lazy"` su hero/LCP
- [ ] CLS < 0,1 — width/height img
- [ ] CSS critico inline; resto differito
- [ ] Immagini WebP, hero leggera
- [ ] No `filter: blur` su animazioni; no `will-change` permanente

### 2.4 Schema.org
- [ ] `Person` su Chi sono / bio
- [ ] `LocalBusiness` o `SportsActivityLocation` su palestra/contatti
- [ ] `geo` + `hasMap` con coordinate reali
- [ ] `sameAs` social + Google Maps
- [ ] `FAQPage` dove ci sono FAQ
- [ ] `BreadcrumbList` (tranne home)
- [ ] `BlogPosting` + `dateModified` su articoli

### 2.5 E-E-A-T (autobiografico)
- [ ] Foto e storia **vere**
- [ ] Certificazioni solo se reali
- [ ] Pagina autore linkata da blog
- [ ] Recensioni Google coerenti con NAP
- [ ] Privacy / GDPR su form contatti
- [ ] «Ultimo aggiornamento» su pillar

### 2.6 Contenuti
- [ ] Anti-doppioni prima di nuovo articolo
- [ ] 1500+ parole utili su pillar (no riempimento)
- [ ] Risposta 40–60 parole dopo H2 (AEO)
- [ ] Fonti verificabili per dati salute/nutrizione

### 2.7 GEO / AI search
- [ ] Frasi dichiarative auto-contenute (prime righe sezione)
- [ ] Opzionale: `llms.txt` + `ai.json` con URL pillar

### 2.8 Accessibilità
- [ ] Contrasto CTA ≥ 4,5:1
- [ ] Label form, focus visibile
- [ ] Touch target ≥ 44px mobile

---

## 3. Routine post-modifica (manuale)

1. Controlla title/meta caratteri
2. Test mobile browser o DevTools 375px
3. Rich Results Test se tocchi schema
4. PageSpeed su homepage se tocchi CSS/hero

---

## 4. Search Console — promemoria

- Proprietà **Dominio**
- Sitemap: solo `/sitemap.xml`
- Ispezione URL: sempre dominio **canonico** (senza www se apex ufficiale)
- Venerdì: aggiorna `data/gsc-indexing-weekly.json`

Dettaglio: `skill-seo.md` §10
