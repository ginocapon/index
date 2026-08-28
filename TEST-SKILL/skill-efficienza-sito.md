# Skill — Efficienza sito Righetto Immobiliare

> **Principio guida:** buonsenso operativo (Musk/Tesla adattato al web).  
> Meno attrito, più risultato misurabile: lead, indicizzazione, velocità, zero sprechi.

**Carica sempre con:** `skill-essentials.md` + `skill-massimo-punteggio.md`  
**Routing:** `context-map.json` → task `efficienza_sito`, `audit_venerdi`, `modifica_generica`

---

## 1. Le 8 regole (organizzazione → sito)

| # | Regola originale | Traduzione Righetto |
|---|------------------|---------------------|
| 1 | Elimina riunioni grandi inutili | **Niente task a catena** se un passaggio basta (sync foto auto, verify script, push solo se chiesto) |
| 2 | Elimina riunioni frequenti | **Audit ripetuti solo se cambiano azioni** — stesso check GSC/GA senza fix = stop |
| 3 | Esci se non aggiungi valore | **Diff minimo** — 5 righe che risolvono > refactor estetico |
| 4 | Niente acronimi / gergo | Title, H1, CTA in italiano chiaro — no jargon interno nel copy pubblico |
| 5 | Comunicazione percorso più corto | Un file skill = una verità — no regole duplicate sparse |
| 6 | Info libera tra reparti | Admin ↔ sito ↔ SEO: stesso ID GA4, stesso path foto, stesso slug immobile |
| 7 | Buonsenso > regola assurda | Regola che blocca l'ovvio → si cambia regola/codice, non si ignora |
| 8 | Proposte di efficienza benvenute | Fix ricorrente → script + riga in questa skill |

---

## 2. Gate tecnici (BLOCCANTE post-modifica)

```bash
python scripts/verify_media_migration.py          # foto WebP + zero Supabase in DB
python scripts/verify_ga_consent_live.py          # GA4 G-PHEL8KXLBX + Consent Mode
node scripts/validate-page.js --file pagina.html  # title/meta ogni pagina toccata
python scripts/google-compliance-check.py         # audit repo completo
bash scripts/mini-seo-check.sh                    # meta, schema, GEO
```

**ESITO atteso:** 0 errori bloccanti prima di chiudere il task.

---

## 3. Efficienza per area

### 3.1 Performance
- Solo **WebP** in `img/immobili/` e hero blog (≤150 KiB dove possibile)
- Zero CDN esterni — vendor in `js/vendor/`
- CSS/JS con `?v=N` incrementato a ogni modifica
- No `filter: blur` animato, no `will-change` permanente
- LCP: preload font + hero, no lazy su above-the-fold

### 3.2 SEO / GSC
- **Un solo GA4:** account `151722673`, proprietà `393201402`, ID **`G-PHEL8KXLBX`**
- Ignorare account duplicato `385973406`
- Schema: niente Review JSON-LD duplicati su pagine servizio
- Sitemap aggiornata, URL senza `.html`
- Priorità indicizzazione: pillar → servizi → blog recente (`data/gsc-indexing-priority.json`)

### 3.3 Contenuti
- Anti-doppioni **prima** di scrivere (`check_doppioni_sito.py`)
- Blog: 2500+ parole **utili**, no filler ripetuto (`fix_blog_filler_duplicates.py`)
- Box «In sintesi» / `righetto-sol` dove manca
- Dati numerici solo con fonte (OMI, ISTAT, ADE, FIMAA)
- Compenso mediazione: mai online

### 3.4 Media annunci
- Dopo upload admin: sync **automatico** 6 h — non chiedere comandi manuali
- Urgenza: `sync_media_automation.py` → verify → commit
- Dettaglio: `skill-media-migration.md`

### 3.5 Lead / conversione
- Form in pagina (sendNotifica + Supabase), mai solo redirect a contatti
- CTA contrasto WCAG AA — mai oro `#FF6B35` con testo bianco
- Mobile-first su ogni modifica

---

## 4. Checklist venerdì (15 min)

- [ ] `verify_media_migration.py` → OK
- [ ] `verify_ga_consent_live.py` → OK
- [ ] GSC: errori critici schema / indicizzazione pillar
- [ ] `gsc-indexing-weekly.json` aggiornato
- [ ] Immobili in evidenza coerenti con admin
- [ ] Nessun commit pendente critico (foto, fix GSC)

---

## 5. Vietato (sprechi)

- Duplicare account GA4 o lasciare URL Supabase Storage su annunci attivi
- JPG/PNG in `img/immobili/` senza conversione WebP
- Blog doppione o paragrafi clone per gonfiare wordCount
- Push senza richiesta esplicita utente
- Listini commissioni online
- Dati inventati senza fonte

---

## 6. Script batch efficienza

| Script | Quando |
|--------|--------|
| `patch_compliance_warns.py` | Title/meta/geo/breadcrumb/stuffing su massa |
| `patch_audit_warns.py` | dateModified JSON-LD, OG mancanti |
| `fix_blog_filler_duplicates.py` | Rimuove paragrafi filler duplicati blog |
| `patch_righetto_sol_blog.py` | Box sintesi blog |
| `patch_ga_consent.py` | Migra gtag inline → ga-consent.js |
| `convert_immobili_to_webp.py` | JPG/PNG residui in immobili |

---

*Ultimo aggiornamento: agosto 2026*
