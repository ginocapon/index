# CLAUDE.md — Righetto Immobiliare

## Istruzione Primaria
**LEGGI SEMPRE `SKILL.md` prima di qualsiasi operazione.**
SKILL.md e' l'unica fonte di verita' per questo progetto.

## Regole Automatiche

### Prima di ogni modifica:
1. Leggi il file da modificare — mai al buio
2. Verifica coerenza con SKILL.md (claim, commissioni, struttura)
3. Mobile-first — ogni modifica deve funzionare su mobile

### Codice:
- Solo HTML/CSS/JS vanilla — zero framework, zero librerie esterne
- No `filter: blur` su animazioni — solo `opacity` e `transform`
- No `will-change` permanente
- CTA contrasto minimo 4.5:1 (WCAG AA)
- Nessun CDN esterno

### Contenuti Blog:
- Seguire template e checklist in SKILL.md Sezione 3 e 5
- 2500+ parole, 10-15 H2/H3, 35% transition words
- OGNI dato numerico DEVE avere fonte verificata (OMI, FIAIP, ISTAT, Banca d'Italia)
- Zero claim inventati, zero dialetto, tono professionale
- Commissioni: 3% + IVA per parte (min. 2.500€ vendita), 1 mensilita' + IVA (affitto)
- Claim consentiti: 350+ immobili, 101 comuni, 98% soddisfazione, 127 recensioni 4.9/5, dal 2000

### Dopo ogni modifica:
- Aggiornare sitemap.xml se pagine aggiunte/rimosse
- Commit in italiano, descrittivo
- Verificare checklist automatiche in SKILL.md Sezione 5

### Pubblicazione:
- Regola d'oro: "Se non hai fonte verificabile, NON inserire il dato"
- Sostituire TUTTI i placeholder [DATO], [ZONA], [FONTE] prima di pubblicare
- URL sempre senza www: righettoimmobiliare.it
