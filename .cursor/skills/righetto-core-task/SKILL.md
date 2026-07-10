---
name: righetto-core-task
description: >-
  Avvia qualsiasi task sul sito Righetto Immobiliare (righettoimmobiliare.it):
  carica regole essenziali, gate Google 10/10 e routing moduli TEST-SKILL.
  Usa quando l'utente chiede modifiche generiche al sito, fix pagine, aggiornamenti
  contenuti, commit/push, o non specifica una skill più mirata (blog, landing, mobile).
---

# Righetto — task generico sito

## Prima di iniziare (sempre)

1. Leggi `TEST-SKILL/skill-essentials.md`
2. Leggi `TEST-SKILL/skill-massimo-punteggio.md` (gate Google)
3. Consulta `TEST-SKILL/context-map.json` per il task specifico → carica i moduli indicati

## Regole non negoziabili

- Vanilla HTML/CSS/JS — zero CDN esterni
- URL interne **senza** `.html`
- Mobile-first + WCAG AA (CTA: **mai** `#FF6B35` con testo bianco)
- CSS/JS con `?v=N` — incrementa a ogni modifica
- Claim consentiti: 350+ immobili · 101 comuni · 98% · 127 recensioni 4.9/5 · dal 2000
- Mediazione: **mai** listini o percentuali online
- Se non hai fonte verificabile (OMI, FIMAA, ISTAT, ADE…), **non inserire il dato**

## Checklist fine task

- [ ] File letto prima di modificare
- [ ] Title ≤60 (max 70), meta ≤160 — `node scripts/validate-page.js --file pagina.html`
- [ ] `sitemap.xml` se nuova/rimossa URL
- [ ] **Commit:** a fine task se ci sono modifiche (messaggio in italiano, no `.env`/segreti)
- [ ] **Push:** solo se l'utente lo chiede esplicitamente («push», «pushia», «metti online»). Senza richiesta → commit locale o solo file modificati, **no push**

## Lezioni consolidate (aggiornare dopo ogni fix)

Dopo un fix importante, l'utente può dire: *«aggiorna skill con questa lezione»* → documentare in:
- skill specializzata (es. `righetto-fix-mobile`)
- `TEST-SKILL/skill-design.md` o modulo pertinente
- changelog `SKILL-2.0.md`

Lezioni già registrate (luglio 2026): hero landing iPhone, tour 360° slug/codice, annunci disattivati admin+catalogo.

## Routing verso skill specializzate

| Task | Skill progetto | Command |
|------|----------------|---------|
| Nuovo articolo blog | `righetto-blog` | `/blog` |
| Landing / form lead | `righetto-landing` | `/landing` |
| Fix mobile / iPhone | `righetto-fix-mobile` | `/mobile` |
| Foto admin / tour 360° | `righetto-immobili-admin` | `/immobili` |
| Audit SEO / meta / schema | `righetto-seo` | `/seo` |
| Pagina zona / quartiere | `righetto-zona` | `/zona` |
| Social / copy post | `righetto-social` | `/social` |
| Audit sicurezza | `righetto-security` | `/sicurezza` |
| Piano venerdì / 90 giorni | `righetto-venerdi-sito-90giorni` | `/venerdi` |
| Perizia PDF | `righetto-perizia` | `/perizia` |

Mappa completa: `TEST-SKILL/skill-cursor-rules.md` §2b

## Rules Cursor attive

- Sempre: `.cursor/rules/righetto-core.mdc`
- Per globs: vedi `TEST-SKILL/skill-cursor-rules.md`
