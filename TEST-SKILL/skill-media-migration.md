# Migrazione media Supabase → GitHub Pages

**Obiettivo:** eliminare egress Supabase su foto annunci e reel, servendo tutto da `righettoimmobiliare.it/img/`.

**Supabase resta per:** database (immobili, richieste, blog admin), bucket `documenti` (PDF privati).

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

### 2. Dopo ogni upload foto in admin

L'admin carica ancora su Supabase (browser). Poi sul PC:

```powershell
python scripts/migrate_supabase_media.py --photos --update-db --sync-og
git add img/ data/media-manifest.json share-immobile-*.html
git commit -m "Sync foto immobili su GitHub Pages"
git push
```

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
