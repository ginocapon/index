---
name: righetto-landing
description: >-
  Crea o modifica landing Righetto Immobiliare con form lead, conversione mobile-first
  e vanilla HTML. Usa quando l'utente chiede landing, pagina conversione, valutazione
  gratuita, consulenza, costi locazione, vendere casa, mutuo, o fix UI landing/servizio.
---

# Landing Righetto

## Prima di iniziare

1. `TEST-SKILL/skill-essentials.md` + `TEST-SKILL/skill-massimo-punteggio.md`
2. `TEST-SKILL/skill-forms-leads.md` (invio lead BLOCCANTE)
3. `TEST-SKILL/skill-design.md` (UI, CTA, form)
4. `TEST-SKILL/skill-context.md` (architettura se nuova URL)

## Modelli di riferimento

- `landing-consulenza-immobiliare-gratuita.html`
- `landing-valutazione.html`
- `contatti.html` (form + success inline)
- `landing-costi-locazione-inquilino.html` (se tema affitto)

## Checklist obbligatoria

- [ ] Form: `SERVIZI_CONFIG.sendNotifica()` + insert Supabase `richieste` con `provenienza`
- [ ] **Vietato:** solo redirect GET a `/contatti`; aprire `send-mail.php` nel browser
- [ ] Checkbox GDPR obbligatoria + marketing facoltativa (`rig-lead-form.js`)
- [ ] Success box inline — nascondere campi dopo invio
- [ ] Mobile-first: input `font-size: 16px` minimo (no zoom iOS)
- [ ] CTA contrasto 4.5:1 — **mai** oro `#FF6B35` con testo bianco
- [ ] Hero: testo leggibile su mobile (pannello scuro sotto foto se sfondo chiaro)
- [ ] Title ≤60, meta ≤160 — `validate-page.js`
- [ ] Bump `?v=N` su CSS/JS modificati
- [ ] Nessun listino mediazione online
- [ ] Nuova URL → `sitemap.xml` + `admin.html` (`_landingSeedPages`)

## Schema (landing commerciali)

- `WebPage` + `FAQPage` se FAQ visibile (§8.2.6 SKILL-2.0)
- BreadcrumbList dove previsto

## Rules Cursor

- `.cursor/rules/righetto-forms-leads.mdc`
- `.cursor/rules/righetto-vanilla-ui.mdc`

## Output atteso

HTML landing + sitemap se nuova + validate-page OK + commit in italiano
