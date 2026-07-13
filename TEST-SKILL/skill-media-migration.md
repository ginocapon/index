# Migrazione media Supabase → GitHub Pages

**Obiettivo:** eliminare egress Supabase su foto annunci e reel, servendo tutto da `righettoimmobiliare.it/img/`.

**Supabase resta per:** database (immobili, richieste, blog admin), bucket `documenti` (PDF privati).

---

## Per gli agenti IA (BLOCCANTE — luglio 2026)

**Carica questo file** per: upload foto in admin, sync media, egress Supabase, reel MP4, `img/immobili/`, `js/media-url.js`.

| Regola | Dettaglio |
|--------|-----------|
| **Sync automatico** | Dopo upload in admin **non** chiedere all'utente comandi manuali. GitHub Actions `sync-media-github.yml` gira ogni **6 h** (+ `workflow_dispatch`). |
| **Messaggio utente** | «Le foto saranno sul sito entro ~6 ore» — toast già in `admin.html`. |
| **Manuale** | Solo se l'utente chiede urgenza: `python scripts/sync_media_automation.py` + commit/push. |
| **URL foto pubbliche** | `img/immobili/{CODICE}/…` su GitHub Pages — **non** Supabase Storage per annunci live. |
| **Reel** | `REEL_LOCAL=1` → `img/video/reels/` — **non** bucket `foto-immobili`. |
| **Secret CI** | `SUPABASE_KEY` (service_role) in GitHub Actions — mai in commit. |
| **Vietato** | Suggerire purge/sync manuale come flusso normale; ripristinare URL `supabase.co/storage` su annunci attivi. |

---

## Struttura file

```
img/
  immobili/{CODICE}/     # foto annunci (WebP)
  planimetrie/{CODICE}/  # planimetrie pubbliche
  video/
    reels/               # reel Instagram (MP4)
    blog/                # video hero blog
data/
  media-manifest.json    # mappa URL Supabase → path locale (rewrite client)
js/
  media-url.js           # resolveImageUrl unificato
```

---

## Flusso operativo

### 1. Migrazione iniziale (una tantum)

```powershell
cd c:\Users\Utente\progetti\index

# Anteprima
python scripts/migrate_supabase_media.py --dry-run

# Scarica foto + aggiorna DB + manifest
python scripts/migrate_supabase_media.py --photos --update-db --sync-og

# Video/reel da Storage (opzionale)
python scripts/migrate_supabase_media.py --videos

# Visite virtuali JSON
python scripts/migrate_supabase_media.py --visite
```

### 2. Dopo ogni upload foto in admin (automatico)

**Non serve più lanciare comandi a mano.** Il workflow GitHub Actions
`.github/workflows/sync-media-github.yml` gira **ogni 6 ore** (e su richiesta manuale):

1. Scarica nuove foto da Supabase → `img/immobili/`
2. Aggiorna DB, manifest, share social
3. Commit + push su `main`
4. Svuota bucket `foto-immobili` su Supabase

**Dopo upload in admin:** attendi al massimo ~6 ore (spesso meno). Toast in admin lo conferma.

**Manuale (solo se urgente):**
```powershell
python scripts/sync_media_automation.py
git add img/ data/ share-immobile-*.html && git commit -m "Sync foto" && git push
```

**Secret GitHub:** `SUPABASE_KEY` (service_role) in Settings → Secrets and variables → Actions → Repository secrets.

### Setup secret (una tantum, manuale)

1. Supabase Dashboard → Project Settings → API → copia **service_role** (non anon).
2. GitHub repo `index` → Settings → Secrets and variables → Actions → **New repository secret**.
3. Nome: `SUPABASE_KEY` — valore: chiave service_role.
4. Verifica: Actions → `sync-media-github.yml` → **Run workflow** → job deve completare (non «SUPABASE_KEY mancante»).
5. Locale: stessa chiave in `.env` (gitignored) per `python scripts/sync_media_automation.py` urgente.

**Senza secret:** il workflow termina in skip — il sito resta servito da `img/immobili/` già migrati; nuove foto in admin attendono sync manuale o secret.

### 3. Reel Instagram

`righetto_social/genera_reel.py` con `REEL_LOCAL=1` (default in `.env.example`):

- MP4 salvato in `img/video/reels/{slug}.mp4`
- URL pubblicazione: `https://righettoimmobiliare.it/img/video/reels/…`
- **Nessun upload Supabase** per i reel

Reel manuali (es. RTC studenti): `righetto_social/assets/…` → copia in `img/video/reels/` e commit.

### 4. Commit e deploy

GitHub Pages serve `img/` senza costi egress Supabase. Repo può crescere: preferire WebP (script converte con Pillow se installato: `pip install Pillow`).

---

## Cosa non migrare

| Risorsa | Dove resta |
|---------|------------|
| PDF documenti immobile | Supabase `documenti` |
| Schede catastali | Supabase `documenti` |
| Documenti clienti CRM | Supabase `documenti/clienti-docs/` |

---

## Checklist post-migrazione

- [ ] `data/media-manifest.json` aggiornato
- [ ] `immobili.foto[]` in DB con path `img/immobili/…`
- [ ] `share-immobile-*.html` rigenerati (`sync_og_immobili.py`)
- [ ] Dashboard Supabase: egress in calo nel ciclo successivo
- [ ] `REEL_LOCAL=1` in `righetto_social/.env`

---

## Riferimenti codice

- `scripts/migrate_supabase_media.py` — tool principale
- `js/media-url.js` — risoluzione URL lato sito
- `scripts/sync_og_immobili.py` — OG share pages (supporta `img/`)
- `righetto_social/genera_reel.py` — reel locali
