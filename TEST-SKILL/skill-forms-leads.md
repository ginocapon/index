# SKILL-FORMS-LEADS — Righetto Immobiliare
> Carica per: **qualsiasi landing**, **articolo blog con CTA/form**, **pagina servizio con lead form**, fix invio email.
> Va caricata **insieme a** `skill-essentials.md`. Riferimento implementativo: `contatti.html`, `landing-consulenza-immobiliare-gratuita.html`, `landing-valutazione.html`.

---

## 1. Regola obbligatoria (BLOCCANTE)

Ogni pagina con form di contatto/lead deve:

1. **Inviare in pagina** — un solo passaggio per l’utente (niente redirect a Contatti solo per inviare).
2. Usare **`SERVIZI_CONFIG.sendNotifica()`** da `js/config.js` (POST Edge Function).
3. Salvare su Supabase tabella **`richieste`** con campo **`provenienza`** = slug pagina (es. `landing-consulenza-immobiliare-gratuita`, `blog-prezzi-padova-2026`).
4. Mostrare **stato successo inline** (box verde, nascondere campi form) — come `contatti.html` / landing consulenza.

### Vietato

| Errore | Perché |
|--------|--------|
| `action="contatti" method="get"` come unico invio | Non manda email né Supabase; solo URL con parametri |
| Aprire `send-mail.php` nel browser | Risponde `{"error":"Solo POST"}` — endpoint server, non per test manuali GET |
| Chiamare `send-mail.php` dal frontend | Solo Edge Function (server) o admin; il sito usa `send-email` |
| Form senza checkbox **GDPR** obbligatoria | Blocco legale + `sendForm` non parte |
| `config.js` / Supabase con **`defer`** + handler inline che invia al load | Race: `SERVIZI_CONFIG` può essere `undefined` al primo click |

---

## 2. Architettura email (flusso reale)

```
Browser (landing/blog/contatti)
  → POST https://qwkwkemuabfwvwuqrxlu.supabase.co/functions/v1/send-email
     body: { action: "send_test", to_email: "info@righettoimmobiliare.it", subject, html_body, reply_to }
  → Edge Function send-email (supabase/functions/send-email/index.ts)
  → POST https://api.righettoimmobiliare.it/send-mail.php  (solo POST + X-API-Key)
  → mail() cPanel → casella agenzia
```

**Destinatario notifiche lead:** `info@righettoimmobiliare.it` (non email automatica al visitatore).

**File:** `js/config.js` (`sendNotifica`), `api/send-mail.php` (relay cPanel), secrets Supabase `MAIL_RELAY_URL` / `MAIL_RELAY_KEY`.

---

## 3. Modulo condiviso (preferito)

Per servizi, blog e landing semplici usa **`js/rig-lead-form.js`** con attributi sul form:

```html
<form data-rig-lead-form data-provenienza="servizio-vendita" data-extra-labels='{"#f-comune":"Comune"}' novalidate>
  ...
  <div class="rig-lead-success" style="display:none">...</div>
</form>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="js/config.js?v=4"></script>
<script src="js/rig-lead-form.js?v=1"></script>
```

Migrazione batch: `python tools/migrate-forms-leads.py`

## 3b. Template script manuale (copia da contatti)

In fondo alla pagina, **prima** dello script inline di invio:

```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="js/config.js?v=4"></script>
```

> **Senza `defer`** su queste due righe se lo script di submit è subito sotto. In alternativa: tutto `defer` + invio solo su `DOMContentLoaded` o al click dopo `await` su disponibilità di `SERVIZI_CONFIG`.

Handler minimo (adattare id e `provenienza`):

```html
<form id="lead-form" onsubmit="sendLeadForm(event);return false;" novalidate>
  <!-- campi + checkbox gdpr required -->
  <div class="lead-success" id="lead-ok" style="display:none">...</div>
</form>
<script>
var SB_URL = 'https://qwkwkemuabfwvwuqrxlu.supabase.co';
var SB_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'; // anon key in config.js / contatti.html

async function sendLeadForm(e) {
  e.preventDefault();
  // validazione nome + telefono + gdpr
  var btn = document.querySelector('.lead-submit');
  btn.disabled = true; btn.textContent = 'Invio in corso...';

  var emailOk = false;
  try {
    if (typeof SERVIZI_CONFIG !== 'undefined') {
      emailOk = await SERVIZI_CONFIG.sendNotifica({
        subject: 'Nuovo contatto dal sito: ' + nomeCompleto,
        html_body: bodyParts.join('<br>'),
        reply_to: email || undefined
      });
    }
  } catch (err) { emailOk = false; }

  var supaOk = false;
  try {
    var sb = window.supabase && supabase.createClient(SB_URL, SB_ANON);
    if (sb) {
      await sb.from('richieste').insert([{
        nome: nomeCompleto, email: email, telefono: tel,
        messaggio: messaggioDb,
        provenienza: 'SLUG-PAGINA',
        newsletter: false, letto: false
      }]);
      supaOk = true;
    }
  } catch (err) { supaOk = false; }

  btn.disabled = false; btn.textContent = 'Invia richiesta';
  if (emailOk || supaOk) {
    document.getElementById('lead-form').classList.add('is-sent');
    document.getElementById('lead-ok').style.display = 'block';
  } else {
    alert('Errore nell\'invio. Chiama il 049.88.43.484 o scrivi a info@righettoimmobiliare.it');
  }
}
</script>
```

**Oggetto email:** preferire `Nuovo contatto dal sito: {nome}` (allineato a Contatti). In `html_body` includere slug pagina: `<b>Pagina:</b> landing-...` o `blog-...`.

---

## 4. UI successo (landing / blog)

- Classe wrapper form: `.is-sent` nasconde `.v-form-fields` o equivalente.
- Box successo: sfondo `#e8f5e9`, titolo «Messaggio inviato!», testo come Contatti.
- Se `emailOk === false` ma `supaOk`: messaggio che la richiesta è in Admin → Richieste.

---

## 5. Checklist nuova landing

- [ ] Form `onsubmit` + `return false` (no submit nativo GET/POST verso altra pagina)
- [ ] GDPR checkbox `required`
- [ ] `sendNotifica` + insert `richieste` con `provenienza` univoca
- [ ] Script Supabase + `config.js` caricati correttamente (no race defer)
- [ ] Success state inline
- [ ] Seed `admin.html` → `_landingSeedPages` + `data_pubblicazione`
- [ ] `sitemap.xml` URL senza `.html`
- [ ] Test Rete: POST `send-email` → status 200 / `sent` (non GET su `send-mail.php`)

---

## 6. Checklist articolo blog (se ha form lead)

- [ ] Stesso pattern §3 (non linkare solo a `/contatti` senza invio dedicato se la CTA è «Richiedi consulenza» in pagina)
- [ ] `provenienza`: `blog-{slug-articolo}` o cluster concordato
- [ ] Registrazione blog: admin seed + `blog.html` + `homepage.js` + sitemap (skill-content)
- [ ] CTA strip può puntare a `#form` in pagina **con** form che rispetta questa skill

---

## 7. Debug

| Sintomo | Causa probabile |
|---------|----------------|
| JSON `Solo POST` | Aperto `send-mail.php` in browser (GET) |
| Successo UI ma no mail | Solo Supabase ok; verificare secrets Edge + relay PHP; Admin → Richieste |
| `SERVIZI_CONFIG is undefined` | `config.js` defer dopo handler o non caricato |
| Redirect `contatti?nome=...` senza mail | Utente non ha cliccato Invia su Contatti (flusso vecchio) |

Test corretto: DevTools → **Rete** → filtro `send-email` → metodo **POST** dopo submit form in pagina.

---

*Aggiornato: maggio 2026 — allineato a fix landing consulenza (invio diretto).*
