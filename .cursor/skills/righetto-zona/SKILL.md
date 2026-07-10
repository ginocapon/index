---
name: righetto-zona
description: >-
  Crea o aggiorna pagine zona locali Righetto (zona-*.html): SEO locale Padova,
  dati OMI, FAQ schema, Pro/Contro, link interni. Usa quando l'utente chiede
  nuova scheda zona, pagina quartiere, SEO locale Limena/Vigonza/hinterland,
  o ampliamento contenuto zona esistente.
---

# Zone locali Righetto

## Prima di iniziare

1. `TEST-SKILL/skill-essentials.md` + `TEST-SKILL/skill-massimo-punteggio.md`
2. `TEST-SKILL/skill-content.md` §3 (standard zone page)
3. `TEST-SKILL/skill-seo.md` (GEO, schema, title zona)

## Modelli

- `zona-limena.html`, `zona-vigonza.html`
- Pillar: `agenzia-immobiliare-padova.html`

## Struttura obbligatoria

1. H1: «Case in vendita a [ZONA] — Prezzi, Quartiere e Consigli»
2. Intro GEO con dati OMI (€/mq, trend) — **fonte verificabile**
3. Il quartiere — storia, carattere, target
4. Tabella prezzi per tipologia (fonte OMI)
5. Servizi e infrastrutture
6. **Pro e Contro** (4+4) — obbligatorio E-E-A-T
7. FAQ locali (min 5) con `FAQPage` schema
8. CTA valutazione per la zona
9. Link interni blog + servizi del cluster

## Schema obbligatorio

- `RealEstateAgent` + `areaServed`
- `FAQPage` (min 5 domande iper-locali)
- `BreadcrumbList`
- `Place` + `GeoCoordinates`

## Title zona

- Target ≤60 char (max 70)
- **Evitare:** `Case in Vendita e Affitto a {Zona}, Padova | Righetto` (~73 char)
- **Preferire:** `{Zona} Padova: vendita e affitto | Righetto`

## Checklist fine task

- [ ] Dati OMI/ISTAT con fonte nel testo
- [ ] Nome zona max 10–12 occorrenze (no stuffing)
- [ ] `sitemap.xml` + footer zone + `llms.txt` se nuova URL
- [ ] `validate-page.js` — title/meta OK

## Rule Cursor

`.cursor/rules/righetto-seo-geo.mdc`

## Output atteso

`zona-{slug}.html` pubblicato, mesh interno aggiornato, commit in italiano
