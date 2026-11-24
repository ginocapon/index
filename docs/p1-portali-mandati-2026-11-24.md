# P1 — Portali (Immobiliare.it / Idealista), scadenze incarico, venduti/affittati

**Data:** 24 novembre 2026  
**Branch / PR:** lavoro separato da P0 sicurezza (non mescolare).  
**Stato DB live:** nessuna modifica applicata automaticamente. Serve azione manuale di Gino.

---

## Cosa è stato fatto (in parole semplici)

1. **Esportazione verso i portali**  
   Il gestionale può preparare un elenco (feed) degli annunci da pubblicare su **Immobiliare.it** (file XML) e **Idealista** (file JSON di lavoro).  
   In ogni scheda immobile ci sono due spunte: *Pubblica su Immobiliare.it* e *Pubblica su Idealista*. Solo gli annunci spuntati, attivi e non venduti/affittati entrano nel feed.

2. **Scadenze incarico (mandato)**  
   In home admin (lista Immobili) compare un riquadro che segnala:
   - incarichi **già scaduti**;
   - incarichi che scadono entro **30 giorni**.  
   Cliccando si apre la scheda dell’immobile. Le date restano quelle già presenti in «Data fine incarico».

3. **Venduto / Affittato nascosti dal sito pubblico**  
   Catalogo, homepage e scheda immobile non mostrano più gli annunci marcati venduto o affittato.  
   In più (dopo SQL) il database stesso li nasconde ai visitatori anonimi.

---

## Cosa deve fare il titolare (Gino) — obbligatorio prima dell’uso reale

### A) Applicare l’SQL in Supabase (una volta)

1. Aprire [Supabase](https://supabase.com) → progetto Righetto → **SQL Editor**.
2. Incollare il contenuto di `sql/p1-portali-mandati-2026-11-24.sql` (oppure `supabase/migrations/20261124_p1_portali_mandati.sql`).
3. Eseguire (**Run**).
4. Verificare che non ci siano errori rossi.

Questo aggiunge le colonne `pubblica_immobiliare_it` e `pubblica_idealista` e aggiorna la regola pubblica: solo annunci attivi, non venduti, non affittati, non in cestino.

**Non** eseguire da CI/GitHub Actions. Solo a mano dopo ok.

### B) Contatti e credenziali portali (da richiedere all’agenzia / account manager)

#### Immobiliare.it

| Cosa chiedere | Perché |
|---|---|
| Accesso **Mission Control** / area integrazioni feed | Per registrare l’URL del feed |
| Conferma formato **XML import** (batch `feed.xml` / `.gz` / `.zip` oppure REST) | Documentazione ufficiale: https://feed.immobiliare.it/integration/ii/docs/import/ |
| Email agenzia già nota a Immobiliare.it | Nel feed ogni annuncio porta `info@righettoimmobiliare.it` come agente |
| Eventuale XSD / lista ID tipologie aggiornata | I codici tipologia nel generatore sono una mappa di partenza da validare |

**URL feed (dopo deploy Edge Function):**  
`https://qwkwkemuabfwvwuqrxlu.supabase.co/functions/v1/portal-feeds?portal=immobiliare&token=TOKEN_SEGRETO`

#### Idealista

| Cosa chiedere | Perché |
|---|---|
| Codice **ILC** (Idealista Listing Connector) e omologazione del gestionale | Idealista non pubblica lo schema JSON completo: lo comunica alle piattaforme omologate |
| Credenziali **FTP** (o canale indicato da Idealista) per caricare il file | Tipico per CRM collegati |
| Conferma se accettano il nostro JSON di lavoro o uno schema Idealista diverso | Finché non confermano, **non** considerare il feed «in produzione» |

**URL feed (dopo deploy):**  
`https://qwkwkemuabfwvwuqrxlu.supabase.co/functions/v1/portal-feeds?portal=idealista&token=TOKEN_SEGRETO`

### C) Deploy Edge Function + segreto (tecnico / con assistenza)

```bash
# Segreto lungo (almeno 16 caratteri) — non metterlo nel repository
supabase secrets set PORTAL_FEED_TOKEN="...scegli-un-token-lungo..."
# Opzionale, dopo omologazione Idealista:
supabase secrets set IDEALISTA_ILC="codice-ilc"
supabase functions deploy portal-feeds --no-verify-jwt
```

Il token va comunicato solo a Immobiliare.it / Idealista (o usato in FTP lato nostro), **mai** pubblicato sul sito.

### D) Uso quotidiano in admin

1. Aprire immobile → sezione **Portali esterni**.
2. Spuntare Immobiliare.it e/o Idealista.
3. Salvare.
4. Se marchi **Venduto** o **Affittato**, le spunte portale si azzerano in salvataggio (l’annuncio esce dai feed).
5. Controllare il riquadro **Scadenze incarico** in home Immobili.

---

## Come verificare (test)

### Sito pubblico (anche prima dell’SQL)

1. In admin, su un immobile di prova: Attivo = sì, **Venduto** = sì → Salva.  
2. Aprire `/immobili` e la scheda: non deve comparire.  
3. Togliere Venduto, Salva: ricompare (se Attivo).

### Alert mandati

1. Impostare «Data fine incarico» a ieri → in home deve finire in **Scaduti**.  
2. Impostare tra oggi e +30 giorni → **In scadenza**.

### Feed (dopo SQL + deploy)

1. Spuntare «Pubblica su Immobiliare.it» su 1–2 annunci attivi.  
2. Aprire l’URL feed con il token: deve uscire XML UTF-8 con quei `unique-id`.  
3. Annuncio venduto o senza spunta: assente dal feed.  
4. Stesso per `portal=idealista` (JSON).

### Generazione locale (opzionale)

```bash
node scripts/generate-portal-feeds.mjs --from-json percorso/snapshot-immobili.json
# oppure, con service role (solo macchina sicura):
# SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... node scripts/generate-portal-feeds.mjs --from-supabase
```

Scrive `feeds/immobiliare-feed.xml` e `feeds/idealista-feed.json`.

---

## File toccati (riferimento)

| Area | Path |
|---|---|
| SQL | `sql/p1-portali-mandati-2026-11-24.sql`, `supabase/migrations/20261124_p1_portali_mandati.sql` |
| Feed core | `js/portal-feeds-core.mjs` |
| Edge Function | `supabase/functions/portal-feeds/` |
| Script | `scripts/generate-portal-feeds.mjs` |
| Admin | `admin.html`, `js/admin-mandate-alerts.js`, `css/admin-mandate-alerts.css` |
| Pubblico | `immobili.html`, `immobile.html`, `js/homepage.js`, `index.html` (cache bust) |
| Docs | questo file, `feeds/README.md` |

---

## Limiti noti (onesti)

- Idealista: il JSON è un **formato di lavoro Righetto** fino a omologazione ILC; Idealista può chiedere campi diversi.
- Tipologie Immobiliare.it (`IDType`): mappa iniziale da validare con Mission Control / XSD.
- I feed non caricano automaticamente su FTP Idealista: dopo omologazione si collega un job o un upload manuale.
- P0 sicurezza resta su PR separata; questo P1 non la modifica.

---

## Registro intervento

| Campo | Valore |
|---|---|
| Motivo | Roadmap P1: portali + mandati + venduti |
| Backup | Branch git `cursor/p1-portali-mandati-venduti-1bf7` (PR dedicata) |
| DB live | Non modificato in questo intervento |
| Seguito | Gino applica SQL; richiede accessi portali; deploy `portal-feeds` |
