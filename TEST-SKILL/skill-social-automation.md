# Skill — Automazione social Meta + Google Business (`righetto_social/`)

**Versione:** 30 maggio 2026 — agenda 4 slot (10/13/15/19), rotazione catalogo, fix cron `settings.json`.  
**Indice principale:** `TEST-SKILL/SKILL-2.0.md` sezione **10.4** (sintesi).  
**Implementazione:** cartella `righetto_social/`, README tecnico locale.

---

## 1. Obiettivo

- **~16 contenuti/settimana** senza AI a pagamento.
- Fonti: **catalogo sito** (immobili, blog, landing, pagine agenzia) + **≥2 notizie RSS** (testo originale, zero copiatura).
- Canali: **Facebook**, **Instagram** (feed + reel), **Google Business Profile** (scheda [Gruppo Immobiliare Righetto](https://www.google.com/maps/place/Gruppo+Immobiliare+Righetto/)).
- Tono: professionale, claim SKILL (350+ immobili, 101 comuni, 98%, 127 recensioni 4.9/5, dal 2000). **No tariffe mediazione online.**

---

## 2. Rotazione catalogo (regola d’oro)

**Prima:** stesso immobile su reel + feed + FB nella stessa settimana.  
**Ora:** **3 contenuti diversi per settimana** per sezione; **ciclo completo** sul catalogo prima di ripetere.

| Sezione | Slot lun / mer / ven | Pool |
|---------|----------------------|------|
| **immobile** | reel · IG feed · FB | Tutti gli annunci con `attivo=true` e stato ≠ venduto/affittato, ordine **codice** |
| **blog** | 3 canali da template | Tutti gli articoli `stato=pubblicato` |
| **landing** | 3 canali | Tutte le landing non in bozza |
| **agenzia** | 3 canali | `pagine_agenzia` in `righetto_social/templates/social_sezioni.json` |

**Indice rotazione:** conta le bozze già in `bozze_social` per `fonte` (stato ≠ `rifiutata`) + eventuali righe agenda immobile create a mano (senza `[DA_BOZZA]`).  
**Giro completo:** `ceil(N_annunci / 3)` settimane (es. 21 immobili attivi → ~7 settimane, poi ricomincia).  
**Script:** `genera_bozze_settimanali.py` — meta bozza: `rotazione_indice`, `rotazione_pool`.

**Importante:** se in Supabase pochi immobili hanno `attivo=true`, il pool è piccolo (es. 21 su 350+). Per rotazione ampia → allineare flag `attivo` sugli annunci pubblicati sul sito.

**Notizie RSS:** logica separata (mar/gio, 2/settimana), non in rotazione immobili.

---

## 2c. Agenda giornaliera — 4 fasce (10 / 13 / 15 / 19)

**Script:** `programma_oggi_slot.py` — rotazione **catalogo completo**.

| Regola | Dettaglio |
|--------|-----------|
| **Volume/giorno** | **4 immobili** + **4 articoli blog** + pagine sito (landing + agenzia) |
| **Pagine sito** | Ogni landing/pagina agenzia **2 volte a settimana** (rotazione) |
| **Fasce** | `10:00`, `13:00`, `15:00`, `19:00` |
| **Stagger** | In ogni fascia: **+0 min** immobile → **+15 min** blog → **+30 min** pagina sito |
| **Minimo tra post diversi** | **15 minuti** (FB/IG stesso contenuto: +2 min) |
| **Canali** | `facebook_post` + `instagram_feed` |
| **Ripetizioni** | Vietate nello stesso giorno (stesso immobile/articolo/pagina) |
| **Ciclo** | Immobili ordine **codice**; blog `pubblicato`; landing + `pagine_agenzia` in template |

**Comandi:**

```powershell
cd righetto_social
python programma_oggi_slot.py --dry-run --ciclo-completo
python programma_oggi_slot.py --ciclo-completo
```

**Esempio fascia 10:00:** imm 10:00 → blog 10:15 → pagina sito 10:30 (se in turno settimanale).

---

## 2b. Copy social — immobili e articoli blog (BLOCCANTE)

**Valido per:** post Facebook, feed Instagram, **storie**, **reel**, Google Business (testo/summary) e qualsiasi bozza/agenda generata da agente, script o admin per **contenuti del sito**: `immobili`, articoli `blog`, landing, pagine agenzia.

**Non valido per:** notizie RSS esterne (restano titolo rielaborato + link alla fonte terza).

### Titolo — copia pari pari

| Regola | Dettaglio |
|--------|-----------|
| **Obbligatorio** | Il **titolo del post / storia / reel** (= campo `titolo` in bozza o agenda) deve essere **identico** al titolo sul sito: `immobili.titolo` o `blog.titolo`. |
| **Vietato** | Spintax, varianti o riscrittura del titolo (`{Nuovo incarico\|…}`, prefissi inventati, accorciamenti che cambiano il senso). |
| **Eccezione** | Solo notizie RSS (sezione 8): titolo SEO rielaborato ammesso. |

### Descrizione / caption — struttura obbligatoria

Ogni testo di pubblicazione (corpo, `corpo_spintax`, caption reel/storia) deve contenere **nell’ordine**:

1. **Titolo** (ripetuto in prima riga se il canale non ha campo titolo separato — stesso testo, pari pari).
2. **2–4 righe utili** — zona, tipologia, prezzo/indicazione (immobili) o incipit/guide (blog); tono professionale Righetto; **no tariffe mediazione**.
3. **Link URL completo** dell’immobile o dell’articolo, su riga dedicata (HTTPS, dominio `righettoimmobiliare.it`):
   - Immobile: `https://righettoimmobiliare.it/immobile?s={slug}` (slug da titolo+codice come in `genera_bozze_settimanali.slug_immobile`).
   - Blog: `https://righettoimmobiliare.it/blog-articolo?s={slug}`.
4. **Hashtag `#`** — **minimo 10**, in coda al testo, ricavati da:
   - parole chiave **ad alto volume di ricerca** coerenti con Padova / immobiliare (es. mutuo, affitto studenti, quartiere, tipologia);
   - campi SEO già in DB se presenti (`blog.keywords`, `immobili` comune/zona/tipologia);
   - lista base in `templates/social_sezioni.json` (sezione `hashtags`), **integrata** con keyword specifiche del contenuto (non solo generiche ripetute).
   - **Vietato** inventare trend o hashtag fuori tema; **vietato** omettere i `#`.

**Esempio immobile (schema):**

```text
{ titolo esatto da Supabase }

{Visita su appuntamento|Richiedi informazioni}: {comune} — {dettaglio prezzo/mq}.
Tel. 049 8755543

https://righettoimmobiliare.it/immobile?s={slug}

#padova #immobiliare #righettoimmobiliare #… (≥10 totali, anche specifici zona/tipologia)
```

**Esempio blog (schema):**

```text
{ titolo esatto da Supabase }

{Guida pratica|Approfondimento} per chi {vende|acquista} a Padova.
Leggi l’articolo completo ↓

https://righettoimmobiliare.it/blog-articolo?s={slug}

#padova #blogimmobiliare #… (≥10, allineati a keywords articolo)
```

### Checklist agente / script (prima di salvare bozza o agenda)

- [ ] `titolo` = stringa identica a Supabase/sito (immobile o blog)
- [ ] URL canonico presente nel corpo/caption
- [ ] ≥10 hashtag `#`, mix base + keyword ricerca/contenuto
- [ ] Spintax **solo** nel corpo descrittivo (frasi secondarie), **mai** nel titolo
- [ ] Per reel/storie: stesse regole sulla caption (link + hashtag anche se il video è corto)

### Allineamento codice

- `templates/social_sezioni.json`: per `immobile` e `blog`, `titoli_spintax` deve essere solo `["{titolo}"]` (o equivalente senza varianti).
- Script `genera_bozze_settimanali.py`, `programma_ultimi_10.py`, bozze manuali in admin: rispettare questa sezione.
- Righe già in `pianificazioni`: allineare con `python aggiorna_agenda_copy.py` (salta righe con `PUB_OK` in note).
- Facebook: oltre al parametro `link` API, il **messaggio** deve comunque includere l’URL (obbligatorio per IG e per coerenza cross-canale).

---

## 3. Calendario — manuale (cron Windows **disabilitato**)

**Policy PC Righetto (giu 2026):** niente `RighettoSocialPubblica` ogni 10 min. L’utente **pianifica ogni giorno** contenuti e orari; pubblicazione su richiesta o con orari concordati in chat.

| Quando | Cosa | Comando |
|--------|------|---------|
| **Ogni giorno** | Agenda slot (4 imm + 4 blog + sito) | `python programma_oggi_slot.py --include-oggi --giorni YYYY-MM-DD` |
| **Quando pubblicare** | Tu o agente dopo token OK | `.\pubblica_adesso.ps1` oppure `publish_from_agenda.py --modo manuale` / `--forza` |
| **Token ~60 gg** | Rinnovo PAGE | `.\rinnova_token.ps1` |
| **Disabilita cron** | Task Scheduler | `.\disabilita_cron_windows.ps1` |

**Cron automatico (opzionale, non attivo):** `installa_cron_windows.ps1` + `config/settings.json` + `cron_pubblica.bat` — solo se l’utente lo richiede esplicitamente.

Giorni post agenda 4 slot: come deciso giorno per giorno (non ciclo automatico in background).

### Errore cron — nulla pubblicato (maggio 2026)

| Causa | Sintomo | Fix |
|-------|---------|-----|
| **`config/settings.json` assente** | `scheduler.py` → `Finestra OK: False`; cron esce subito | `copy config\settings.example.json config\settings.json` |
| Finestre disallineate | Slot agenda 10:00 ma cron attivo solo 09:30–11:30 | Allineare `run_windows_local_time` agli slot §2c |
| Task Scheduler non attivo | Nessun log mattutino | Registrare `cron_pubblica.bat` ogni 5–10 min |
| Token USER invece di PAGE | `verifica_meta.py` fallisce | `estrai_token_pagina.py --scrivi-env` |

**Verifica rapida:**

```powershell
python scheduler.py --dry-run          # Finestra OK: True nell'orario slot
python publish_from_agenda.py --dry-run --modo cron
python verifica_meta.py
```

---

## 4. Flusso dati

```
genera_bozze_settimanali.py  →  bozze_social (stato=bozza)
        ↓ Approva / programma_da_bozze.py
pianificazioni (agenda)
        ↓ publish_from_agenda.py (cron o manuale)
Facebook / Instagram (+ GBP se GBP_MIRROR_META=1)
```

Tabelle Supabase: `bozze_social`, `pianificazioni`, `immobili`, `blog`, `landing_pages`.  
SQL: `sql/bozze-social.sql`, `sql/pianificazioni.sql`.

---

## 5. Token Meta (solo `.env` sul PC)

**Vietato:** incollare `META_*=...` in PowerShell; non committare `.env`.

| Variabile | Valore / nota |
|-----------|----------------|
| `META_PAGE_ID` | `1036863892837936` (Righetto Immobiliare) |
| `META_IG_USER_ID` | `17841424134341557` (IG Business collegato alla pagina) |
| `META_PAGE_ACCESS_TOKEN` | **Token PAGINA** (non utente) |

### Rinnovo token (~60 giorni)

```powershell
cd C:\Users\Utente\progetti\index\righetto_social
# 1) Token utente breve da Graph API Explorer (permessi sotto)
# 2) Scrivilo temporaneamente in .env come META_PAGE_ACCESS_TOKEN
python estrai_token_pagina.py --scrivi-env
python verifica_meta.py
```

Permessi richiesti: `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`, `pages_show_list`.

**Graph API Explorer:** origini `https://www.righettoimmobiliare.it` e `https://righettoimmobiliare.it`; «Ricevi token d’accesso alla Pagina» → Righetto Immobiliare.  
Se `me/accounts` è vuoto → usare `estrai_token_pagina.py` (GET `/{page_id}?fields=access_token`).

`verifica_meta.py` deve mostrare: `Token tipo: PAGE`, Facebook OK, Instagram OK, pubblicazione test OK.

---

## 6. Reel Instagram — errore 9007

Messaggio: *«Il contenuto multimediale non è pronto»* (code 9007 / subcode 2207027).

**Causa:** video ancora in elaborazione su Meta.  
**Fix in codice:** `publish_from_agenda.py` → `ig_media_publish_with_retry()` ripete `media_publish` ogni 15 s (max 5 min). **Non** usare GET `status_code` sul container con token Pagina (dà Authorization Error 33).

**Manuale retry:**

```powershell
python publish_from_agenda.py --modo manuale --forza --riprova-errati
```

Reel: `media_direct_url` deve essere `.mp4` HTTPS pubblico (Storage `foto-immobili/reels/`).

---

## 7. Google Business Profile

- Scheda: Gruppo Immobiliare Righetto (Maps).
- `.env`: `GOOGLE_GBP_ACCESS_TOKEN`, `GOOGLE_GBP_PARENT` (`accounts/…/locations/…`).
- `GBP_MIRROR_META=1` (default): replica post/reel Meta su GBP.
- Notizie: righe agenda `tipo=google` (mar/gio).
- **Stato maggio 2026:** OAuth può dare **429** se troppi tentativi — attendere e riconnettere da admin; token solo in `.env`, non localStorage produzione.
- Storie IG: **non** automatizzate.

---

## 8. Notizie RSS (≥2/settimana)

Fonti: **Sole 24 Ore**, **Agenzia delle Entrate**, **Milano Finanza** (fallback Google News RSS).

Regole obbligatorie:
- **Zero copiatura** del corpo articolo.
- Titolo rielaborato con keyword Padova / immobiliare / mercato casa.
- Commento originale in spintax + link alla fonte.
- Canali: `facebook_post` + `google`.

---

## 9. Checklist — primo avvio (domani mattina)

Eseguire in ordine su PC con `.env` configurato:

```powershell
cd C:\Users\Utente\progetti\index\righetto_social

# 0) Cron — OBBLIGATORIO (errore maggio 2026: file mancante = zero post)
copy config\settings.example.json config\settings.json
python scheduler.py --dry-run

# 1) Token e API
python verifica_meta.py

# 2) Agenda rotazione catalogo (da domani, ciclo completo imm+blog)
python programma_oggi_slot.py --dry-run --ciclo-completo
python programma_oggi_slot.py --ciclo-completo

# 3) Se ci sono errori in agenda da ieri
python publish_from_agenda.py --modo manuale --riprova-errati

# 4) Anteprima pubblicazione
python publish_from_agenda.py --dry-run --modo cron
```

**Task Scheduler Windows:** `cron_pubblica.bat` ogni 5–10 min (lun–dom finché c’è agenda). Opzionale: `cron_settimanale.bat` (dom 20:00).

**GBP (quando sbloccato 429):** admin → collega Google → copia token/parent in `.env` → test post `tipo=google`.

---

## 10. Comandi rapidi

| Azione | Comando |
|--------|---------|
| Anteprima bozze | `python genera_bozze_settimanali.py --dry-run` |
| 2 settimane bozze | `python genera_bozze_settimanali.py --settimane 2` |
| Anteprima agenda 4 slot | `python programma_oggi_slot.py --dry-run --ciclo-completo` |
| Ciclo completo catalogo | `python programma_oggi_slot.py --ciclo-completo` |
| Verifica cron | `python scheduler.py --dry-run` |
| Un post | `python publish_from_agenda.py --id UUID` |
| Forza prima dell’ora | `--forza` |
| Sync feed | `sync_facebook_feed.py`, `sync_instagram_feed.py` |

---

## 11. File chiave

| File | Ruolo |
|------|--------|
| `genera_bozze_settimanali.py` | Bozze + rotazione catalogo |
| `programma_oggi_slot.py` | Agenda 4 slot — rotazione imm + blog |
| `programma_da_bozze.py` | Bozze → `pianificazioni` |
| `config/settings.json` | **Obbligatorio** per cron (copiare da `settings.example.json`) |
| `scheduler.py` | Verifica finestra oraria locale |
| `publish_from_agenda.py` | Pubblicazione Meta/GBP + retry reel |
| `genera_reel.py` | MP4 1080×1920 → Storage |
| `verifica_meta.py` | Diagnostica token PAGE/USER |
| `estrai_token_pagina.py` | User token → PAGE token in `.env` |
| `templates/social_sezioni.json` | Slot, spintax, hashtag, canali |
| `cron_settimanale.bat` / `cron_pubblica.bat` | Task Scheduler |
| `.env.example` | Variabili documentate |

---

## 12. Sicurezza

- Token solo in `righetto_social/.env` (server/PC), mai in repo.
- Eseguire `sql/rls-security-hardening-safe.sql` se policy anon troppo permissive.
- Admin Social: approvazione umana consigliata prima di `programma_da_bozze.py` in produzione.

---

## 13. Troubleshooting

| Sintomo | Azione |
|---------|--------|
| **Cron non pubblica nulla** | Verificare `config/settings.json` esiste; `python scheduler.py --dry-run` |
| `Unsupported post` ID `965706979395378` | `META_IG_USER_ID` errato → usare `17841424134341557` + token pagina |
| Token USER in verifica | `python estrai_token_pagina.py --scrivi-env` |
| Reel 9007 | Attendere retry automatico o `--riprova-errati` |
| Pochi immobili in rotazione | Verificare `attivo=true` in Supabase |
| GBP 429 | Pausa 24h, riprovare OAuth |
| Bozze duplicate | Normal: dedupe per data+fonte+canale+ora |

---

*Fine skill social — aggiornare questa pagina quando cambiano slot, permessi Meta o flusso GBP.*
