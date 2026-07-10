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

## Lezione consolidata — hero landing su iPhone (luglio 2026)

**Caso reale:** `landing-costi-locazione-inquilino.html` — titolo e paragrafo bianchi illeggibili su Safari iOS.

**Causa:** `.v-hero-copy` con `margin-top` negativo si sovrappone alla foto ma **prosegue sullo sfondo chiaro** del `body` (`--bianco`); il gradiente sulla foto non copre quella zona → testo bianco su bianco.

**Fix mobile-only (`@media (max-width: 767px)`):**

1. **Rimuovere** `margin-top` negativo sul blocco testo
2. **Separare** foto e copy: foto in alto (≈38–44vh), copy **sotto** con `background: var(--nero)` fisso
3. Gradiente foto → `linear-gradient(..., var(--nero) 100%)` per transizione pulita
4. `viewport-fit=cover` + `env(safe-area-inset-*)` su body/footer
5. `-webkit-text-size-adjust: 100%` su `html`
6. Input/select/textarea `font-size: 16px` (anti-zoom iOS)
7. Tabelle larghe: hint «↔ Scorri la tabella» + `-webkit-overflow-scrolling: touch`

**Modello CSS (pattern `.v-hero` split):**

```css
@media (max-width: 767px) {
  .v-hero { min-height: auto; background: var(--nero); }
  .v-hero-media { flex: none; min-height: 38vh; max-height: 44vh; }
  .v-hero-copy {
    margin-top: 0;
    background: var(--nero);
    padding: 1.35rem 1.15rem 1.75rem;
    padding-bottom: max(1.75rem, env(safe-area-inset-bottom));
  }
}
```

**Regola:** su landing con foto portrait e testo bianco, **non affidarsi** al solo overlay sulla foto — su mobile usare **pannello scuro dedicato** sotto l'immagine.

Vedi anche `TEST-SKILL/skill-design.md` §7c.

## Fix comuni (priorità)

| Problema | Soluzione |
|----------|-----------|
| Testo bianco su hero chiaro | Pannello scuro fisso sotto foto — vedi lezione sopra |
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
