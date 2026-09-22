---
name: righetto-acquisizione-proprietari
description: >-
  Strategia acquisizione proprietari e incarichi immobiliari Righetto: funnel
  completo, percorsi A-L, hub proprietario-immobile, calcolatore→sopralluogo,
  lead scoring, KPI, equilibrio editoriale, CTA funnel. Priorità assoluta su
  SEO/blog generico. Usa per modifiche sito, homepage, servizi, coda editoriale
  owner, landing valutazione/vendita/locazione.
---

# Acquisizione proprietari — Righetto

**Leggi sempre:** `TEST-SKILL/skill-acquisizione-proprietari.md` (fonte completa).  
**Alleato + advisor + territorio 10 km:** `TEST-SKILL/skill-real-estate-advisor.md` · `/advisor`  
**Script / follow-up / canali:** `TEST-SKILL/skill-acquisizione-playbook-commerciale.md`.  
**Cron venerdì (3 slot):** `skill-acquisizione-cron-venerdi.md` + `data/venerdi-friday-pipeline.json` + `skill-acquisizione-contenuti-acquisizione.md`.

## Concetto fondamentale

**Chi vende trova in noi un alleato** — ogni modifica sito deve rafforzare fiducia e accompagnamento, non la «caccia all’incarico».

## Obiettivo funnel

Visitatore → proprietario → contatto → conversazione → sopralluogo → valutazione → incarico (poss. esclusiva).

**Mai** percentuali mediazione online — sempre da concordare in sede.

## Prima di ogni modifica sito

0. Il venditore si sente **alleato**?
1. Quale **percorso A–L**?
2. Quale **passo funnel**?
3. **Asset esistente** da estendere (no duplicati)?
4. **Prova** che aumenta sopralluogo/incarico?

Se non rispondi → modifica secondaria.

## Asset funnel (non duplicare)

1. `proprietario-immobile.html` — hub + percorsi A–L
2. `landing-valutazione.html` — stima Linda → educazione → sopralluogo
3. `servizio-vendita.html` / `servizio-locazioni.html` — form dedicati
4. `landing-consulenza-immobiliare-gratuita.html` — indecisi B, C, G, L
5. `servizio-gestione.html` — I, K

**Evitare** come unica destinazione owner: `contatti` generico.

## Percorsi A–L (sintesi)

| ID | Situazione | Landing / asset |
|----|------------|-----------------|
| A | Quanto vale? | `landing-valutazione` |
| B | Penso di vendere | `servizio-vendita`, `landing-consulenza` |
| C | Non so quando | `landing-consulenza` |
| D | Vendere o affittare? | `blog-rendimento-affitto-padova`, hub |
| E | Da privato | `vendere-casa-padova-errori` → consulenza |
| F | Già in vendita, non vendo | `landing-consulenza`, `servizio-vendita` |
| G | Altra valutazione | `landing-valutazione` |
| H | Eredità | `blog-successione-immobiliare-padova` |
| I | Immobile vuoto | `servizio-locazioni`, `servizio-gestione` |
| J | Ristrutturare | blog ristrutturazione (gap coda) |
| K | Più immobili | `landing-consulenza`, `servizio-gestione` |
| L | Non so ancora | `proprietario-immobile`, `landing-consulenza` |

Dettaglio completo in skill § Percorsi A–L.

## Blog — equilibrio

- Area 1 owner: min 1 ogni 2 settimane (`acquisition_priority: true`)
- Campi: `owner_path`, `acquisition_contribution`, `funnel_step`
- Gate: `python scripts/audit_editorial_acquisition.py --id eq-XXX`
- CTA Class A: `landing-valutazione` + servizio pertinente

## Lead scoring e KPI

- Regole: `data/lead-scoring-rules.json`
- KPI settimanali: `data/acquisition-kpi-template.json`

## Homepage (checklist)

- [ ] Sezione «Hai un immobile?» visibile
- [ ] Hero CTA → `landing-valutazione`
- [ ] Hub → `proprietario-immobile`
- [ ] Sticky → `landing-valutazione`

## Cron venerdì

Con `"SKILL"` o `/venerdi`: **esegui task sett. N/12** da `acquisition-roadmap-cron.json` (repo #1), poi SOSTENERE/blog.

## Audit

`python scripts/audit_editorial_acquisition.py --report`
