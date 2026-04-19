# CLAUDE.md — Righetto Immobiliare

## Istruzione Primaria
**LEGGI SEMPRE `SKILL-2.0.md` (in root: indice) e il testo completo in `TEST-SKILL/SKILL-2.0.md` prima di qualsiasi operazione.**
La skill e' l'unica fonte di verita' per questo progetto.

## Regole Automatiche

### Prima di ogni modifica:
1. Leggi il file da modificare — mai al buio
2. Verifica coerenza con SKILL-2.0.md (claim, commissioni, struttura)
3. Mobile-first — ogni modifica deve funzionare su mobile

### Codice:
- Solo HTML/CSS/JS vanilla — zero framework, zero librerie esterne
- No `filter: blur` su animazioni — solo `opacity` e `transform`
- No `will-change` permanente
- CTA contrasto minimo 4.5:1 (WCAG AA)
- Nessun CDN esterno

### Contenuti Blog:
- Seguire template e checklist in `TEST-SKILL/SKILL-2.0.md` Sezioni 3, 5 e **8.1c** (anti-riempimento, asset, wordCount onesto)
- 2500+ parole nel corpo utile (no «fabbrica» di paragrafi identici), 10-15 H2/H3, 35% transition words
- **Vietato** gonfiare il `wordCount` con loop di paragrafi sostanzialmente uguali; copertine blog hero in **WebP** 1200×630 leggere (Sezione 8.1c)
- OGNI dato numerico DEVE avere fonte verificata (OMI, FIMAA, ISTAT, Banca d'Italia)
- Zero claim inventati, zero dialetto, tono professionale
- Compenso mediazione: non pubblicare tariffe o percentuali online; sempre da concordare in sede nel mandato (blog e testi istituzionali allineati).
- Claim consentiti: 350+ immobili, 101 comuni, 98% soddisfazione, 127 recensioni 4.9/5, dal 2000

### Dopo ogni modifica:
- Aggiornare sitemap.xml se pagine aggiunte/rimosse
- Commit in italiano, descrittivo
- Verificare checklist automatiche in SKILL-2.0.md Sezione 5

### Pubblicazione:
- Regola d'oro: "Se non hai fonte verificabile, NON inserire il dato"
- Sostituire TUTTI i placeholder [DATO], [ZONA], [FONTE] prima di pubblicare
- URL sempre senza www: righettoimmobiliare.it
