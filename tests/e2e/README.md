# Test e2e Righetto (Playwright)

**Cosa verificano:** percorso lead (email + salvataggio in `richieste` + conferma) su 5 form, consenso privacy, honeypot, errori JavaScript, overflow mobile, H1 unico, link telefono/WhatsApp, zero CDN, etichette dei campi.

**Sicurezza:** nessuna richiesta reale. Supabase, funzione email, analytics e qualunque host esterno sono simulati in `helpers.js`. Dati di test su dominio `.invalid`.

## Uso
```
npm install          # una volta (installa @playwright/test 1.60.0)
npx playwright install chromium   # una volta (se manca il browser)
npm run test:e2e     # mobile 390px + desktop 1440px
```
Il server statico dei test (`static-server.js`) replica GitHub Pages: `/pagina` → `pagina.html`.

## Quando eseguirli
Prima di ogni commit che tocca form, `rig-lead-form.js`, `config.js`, `ga-consent.js`, header/footer o pagine funnel.

## Limiti noti (test marcati `fixme`, non nascosti)
- `/immobili`: Leaflet da `unpkg.com` (viola zero CDN) e nessun telefono/WhatsApp visibile finché non si apre una scheda.

## Aggiungere un form
Aggiungere una voce a `FORMS` in `leads.spec.js` con i selettori dei campi. Un test che fallisce con «lead NON salvato in richieste» significa che il contatto arriva solo via email e non entra nel CRM/scoring.
