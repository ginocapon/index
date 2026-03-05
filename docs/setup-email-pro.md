# Email Marketing Pro — Guida Setup Completa

## Come funziona (come Brevo, ma TUO)

Il sistema usa 3 livelli di invio:
1. **SMTP proprio** (via Supabase Edge Function) — priorità massima
2. **Brevo API** (fallback gratuito) — se Edge Function non disponibile
3. **Coda intelligente** — warm-up, rate limiting, retry automatici

---

## STEP 1: Configura DNS del dominio (OBBLIGATORIO per evitare spam)

Vai nel pannello DNS del tuo dominio (Aruba, Cloudflare, etc.) e aggiungi:

### SPF (Sender Policy Framework)
Dice ai server email "queste IP sono autorizzate a inviare per il mio dominio".

```
Tipo: TXT
Nome: @
Valore: v=spf1 include:_spf.aruba.it include:sendinblue.com ~all
```

> Se usi un altro provider SMTP, cambia `include:_spf.aruba.it` con quello del tuo provider.

### DKIM (DomainKeys Identified Mail)
Firma crittografica che verifica che l'email non è stata modificata.

**Se usi Aruba:**
Aruba gestisce DKIM automaticamente per le email inviate dai loro server.

**Se usi Brevo:**
Vai in Brevo → Settings → Senders & Domains → Authenticate → copia i 2 record DKIM.

### DMARC (Domain-based Message Authentication)
Dice ai server cosa fare con email che falliscono SPF/DKIM.

```
Tipo: TXT
Nome: _dmarc
Valore: v=DMARC1; p=none; rua=mailto:info@righetto-immobiliare.it; sp=none; aspf=r
```

> Dopo qualche settimana di monitoraggio, cambia `p=none` a `p=quarantine` per protezione migliore.

---

## STEP 2: Configura SMTP

### Opzione A: Aruba SMTP (se il dominio è su Aruba)
- Host: `smtps.aruba.it`
- Porta: `465` (SSL) o `587` (STARTTLS)
- Utente: `info@righetto-immobiliare.it`
- Password: la tua password email
- Limiti: ~200 email/ora

### Opzione B: Gmail SMTP
- Host: `smtp.gmail.com`
- Porta: `587`
- Utente: il tuo account Gmail
- Password: App Password (da generare in Google Account → Security)
- Limiti: 500/giorno (gratuito)

### Opzione C: VPS con Postfix (illimitato)
Per invio illimitato, noleggia un VPS (es. Hetzner €4/mese) e installa Postfix.

---

## STEP 3: Esegui lo SQL nel database

1. Vai su https://supabase.com → Il tuo progetto → SQL Editor
2. Copia-incolla il contenuto di `sql/email-marketing-tables.sql`
3. Esegui

Questo crea:
- `campagne_email` — storico campagne
- `coda_email` — coda email con tracking
- `email_blacklist` — disiscrizioni e bounce
- `email_tracking` — aperture, click
- `smtp_config` — configurazione SMTP

---

## STEP 4: Deploy Edge Function (opzionale ma consigliato)

```bash
# Installa Supabase CLI
npm install -g supabase

# Login
supabase login

# Linka al progetto
supabase link --project-ref qwkwkemuabfwvwuqrxlu

# Deploy
supabase functions deploy send-email
```

---

## STEP 5: Warm-up (FONDAMENTALE)

Per costruire una buona reputazione IP:

| Settimana | Max email/giorno | Note |
|-----------|-----------------|------|
| 1 | 20-50 | Solo contatti attivi |
| 2 | 50-100 | Monitora bounce rate |
| 3 | 100-200 | Se bounce < 5% OK |
| 4+ | 200-500 | Velocità piena |

---

## Tecniche anti-spam implementate

1. **DKIM/SPF/DMARC** — Autenticazione del dominio
2. **List-Unsubscribe header** — Un click per disiscriversi (richiesto da Gmail/Yahoo)
3. **Personalizzazione {{nome}}** — Email personali, non generiche
4. **Preheader text** — Testo visibile nell'inbox per aumentare aperture
5. **Rate limiting** — Max email/ora e /giorno configurabili
6. **Warm-up graduale** — Aumenta volume gradualmente
7. **Bounce handling** — Rimove automaticamente email non valide
8. **Blacklist automatica** — Disiscrizioni immediate
9. **Delay randomizzato** — Simula invio umano (2-7 sec tra email)
10. **Footer GDPR** — Privacy policy e link disiscrizione obbligatori
11. **Oggetto personalizzato** — Con nome del destinatario
12. **Reply-To** — Permette risposte reali
13. **Tracking pixel** — Monitora aperture
14. **Click tracking** — Monitora click su link
