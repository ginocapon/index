# SKILL-FORMS-CONTATTI — Form e lead

> Carica per: pagina contatti, form prova gratuita, newsletter, WhatsApp CTA.

---

## 1. Principi

- Form **semplice**: nome, email, telefono, messaggio
- Checkbox privacy GDPR obbligatoria
- Messaggio successo **in pagina** (no solo redirect esterno)
- Non aprire endpoint email nel browser (solo POST server-side se backend)
- Honeypot o rate limit anti-spam se possibile

---

## 2. Campi consigliati

| Campo | Obbligatorio |
|-------|--------------|
| Nome | Sì |
| Email o telefono | Almeno uno |
| Messaggio | Sì |
| Privacy | Sì (checkbox) |
| «Come mi hai conosciuto» | Opzionale |

---

## 3. CTA alternative

- Link `tel:` click-to-call mobile
- Link WhatsApp con messaggio precompilato
- Email `mailto:` come fallback

---

## 4. Dopo invio

- Testo conferma visibile («Ti rispondo entro 24h»)
- Non promettere tempi impossibili
- Log lato server se backend (no dati in URL GET)

---

## 5. Accessibilità form

- `<label>` associata a ogni input
- Errori leggibili
- Contrasto OK su bottoni invio

---

## 6. Privacy

- Link a pagina privacy policy
- Testo breve: finalità contatto, conservazione dati, diritti GDPR
