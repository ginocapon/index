---
name: righetto-acquisizione-proprietari
description: >-
  Strategia acquisizione proprietari e incarichi immobiliari Righetto: hub
  proprietario-immobile, equilibrio editoriale, CTA funnel, homepage owner-first.
  Priorità assoluta su SEO/blog generico. Usa per modifiche sito, homepage,
  servizi, coda editoriale owner, landing valutazione/vendita/locazione.
---

# Acquisizione proprietari — Righetto

**Leggi sempre:** `TEST-SKILL/skill-acquisizione-proprietari.md` (fonte completa).

## Obiettivo

Aumentare **proprietari che contattano e affidano** immobili (vendita, affitto, gestione, valutazione).

**Non penalizzare:** annunci, ricerca casa, acquirenti, inquilini.

## Prima di ogni modifica sito

1. Quale **proprietario** aiuta?
2. Quale **passo** del percorso (hub → valutazione → servizio → form)?
3. **Prova** che aumenta probabilità di contatto/incarico?

Se non rispondi → modifica secondaria.

## Asset funnel (ordine preferito)

1. `proprietario-immobile.html` — hub decisionale
2. `landing-valutazione.html` — conversione valore
3. `servizio-vendita.html` / `servizio-locazioni.html` — form dedicati
4. `landing-consulenza-immobiliare-gratuita.html` — indecisi
5. `servizio-gestione.html` — delega locazione

**Evitare** come unica destinazione owner: `contatti` generico, `vendere-casa-padova-errori` (resta educazione, non form primario).

## Blog — equilibrio

- **Area 1 owner:** almeno 1 ogni 2 settimane (`acquisition_priority: true`)
- Campi coda: `primary_audience`, `acquisition_contribution`, `traffic_type`
- Gate: `python scripts/audit_editorial_acquisition.py --id eq-XXX`
- CTA Class A: `landing-valutazione` + servizio pertinente

## Homepage (checklist)

- [ ] Sezione «Hai un immobile?» visibile
- [ ] Hero CTA → `landing-valutazione`
- [ ] Servizi → servizio-vendita / valutazione / locazioni
- [ ] Sticky → `landing-valutazione`

## Dati

- `data/editorial-acquisition-balance.json`
- `data/editorial-queue.json` — policy acquisizione

## Audit periodico

`python scripts/audit_editorial_acquisition.py --report`
