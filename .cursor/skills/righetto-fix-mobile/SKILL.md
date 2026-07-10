---
name: righetto-fix-mobile
description: >-
  Corregge problemi mobile e responsive su Righetto Immobiliare (iPhone, Android,
  tablet): leggibilità, hero, form, CTA, overflow, touch target. Usa quando l'utente
  segnala che una pagina non si legge su mobile, su iPhone, layout rotto, testo
  tagliato, zoom form, o fix UI solo mobile.
---

# Fix mobile Righetto

## Prima di iniziare

1. `TEST-SKILL/skill-essentials.md` (mobile-first)
2. `TEST-SKILL/skill-design.md` (variabili, spacing, CTA, form)
3. Leggi il file HTML/CSS **specifico** prima di modificare

## Diagnosi rapida

1. Identifica viewport problematico (375px iPhone, 390px, 768px tablet)
2. Cerca: overflow orizzontale, testo su sfondo illeggibile, margin negativi su hero
3. Verifica CTA visibile senza scroll eccessivo
4. Form: input ≥16px, checkbox cliccabili, submit full-width

## Fix comuni (priorità)

| Problema | Soluzione |
|----------|-----------|
| Testo bianco su hero chiaro | Pannello scuro fisso sotto foto (`background: var(--nero)` o overlay) |
| Zoom automatico iOS su input | `font-size: 16px` minimo su input/textarea/select |
| Overflow orizzontale | `max-width: 100%`, `overflow-x: hidden` su body, immagini `width:100%` |
| CTA oro illeggibile | Testo `var(--nero)` su `#FF6B35`, mai bianco |
| Hero tagliato | `clamp()` su font, padding mobile 60px 20px |
| Nav copre contenuto | `padding-top: var(--nav-h)` su hero/first section |
| Form sotto piega | Ridurre padding hero su `@media (max-width: 768px)` |

## Regole tecniche

- Modifica **minima** — solo CSS/HTML necessari alla pagina segnalata
- Bump `?v=N` su CSS/JS toccati
- No `filter: blur` su animazioni — solo `opacity` e `transform`
- No `will-change` permanente
- Testare mentalmente 375px e 768px prima del commit

## Scope

- **Solo** fix responsive — non riscrivere contenuti o SEO salvo richiesta
- Se il problema è form invio → passa a `righetto-landing` + `skill-forms-leads.md`

## Rule Cursor

`.cursor/rules/righetto-vanilla-ui.mdc`

## Output atteso

Fix mirato su file indicati, cache-bust aggiornato, commit in italiano
