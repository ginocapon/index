---
name: righetto-immobili-admin
description: >-
  Gestisce foto annunci, sync media Supabase→GitHub, tour virtuali 360° e admin
  immobili Righetto. Usa quando l'utente chiede upload foto admin, sync immagini,
  annunci non visibili, tour 360°, visite virtuali homepage, reel, o migrazione media.
---

# Immobili admin e media Righetto

## Prima di iniziare

1. `TEST-SKILL/skill-essentials.md` (§14 foto annunci, §15 visite virtuali)
2. `TEST-SKILL/skill-media-migration.md` (BLOCCANTE)
3. `TEST-SKILL/skill-context.md` (architettura Supabase/admin)

## Sync foto annunci (flusso normale)

**Dopo upload in admin → NON chiedere comandi manuali all'utente.**

- GitHub Actions `.github/workflows/sync-media-github.yml` ogni **6 ore**
- Messaggio utente: «Le foto saranno sul sito entro ~6 ore»
- URL pubbliche: `img/immobili/{CODICE}/` su GitHub Pages — **non** Supabase Storage live

**Solo se urgenza esplicita:**
```bash
python scripts/sync_media_automation.py
```

## Annunci disattivati — procedura completa (luglio 2026)

Quando un immobile è **venduto, ritirato o non più in portafoglio**, servono **due azioni** (sito + admin):

| Passo | Dove | Azione |
|-------|------|--------|
| 1 | **Admin** (`admin.html`) | Disattivare annuncio: `attivo=false` (icona 👁️ → 🚫) |
| 2 | **Catalogo tour** | Se aveva tour: `"homepage": false` in `data/visite-virtuali.json` (per slug o codice) |
| 3 | **Verifica** | Homepage `/` → sezione tour senza quell'immobile; `immobili` senza card |

**Solo `homepage: false` non basta** se in Supabase resta `attivo=true` — l'annuncio compare ancora in catalogo e può entrare nei tour.

**Codici esempio disattivati:** LA0319 (Sacro Cuore terrazzo), LP0286 (Altichiero), LA0317 (Mandria) — verificare stato in admin a ogni venerdì.

## Homepage — Visite virtuali 360° (`#vtGridHome`)

- **Nessun elenco fisso** in `homepage.js`
- Supabase: `attivo=true`, `venduto=false`, `affittato=false`, ordine `created_at` DESC
- Max **4** immobili con `virtual_tour_scenes`
- Scene arricchite da `data/visite-virtuali.json` se mancanti
- Immobili disattivati **non** compaiono (`attivo=false` in admin + opz. `"homepage": false` in `visite-virtuali.json`)
- **Match catalogo:** slug Supabase può differire dal key JSON (es. UFF2247) — `homepage.js` risolve anche per **codice**; entry in `visite-virtuali.json` con slug reale DB o codice allineato
- Tour senza scene in DB: scene da catalogo JSON se presenti
- Nuovo tour: aggiornare `data/visite-virtuali.json` (cover + scene + `immobile_href` con slug DB) + scene in admin + bump `homepage.js?v=N`

## Checklist verifica

- [ ] Foto servite da `righettoimmobiliare.it/img/immobili/` (non `supabase.co/storage`)
- [ ] `data/media-manifest.json` coerente se rewrite client
- [ ] Reel: `REEL_LOCAL=1` → `img/video/reels/` (non bucket `foto-immobili`)
- [ ] Secret `SUPABASE_KEY` solo in GitHub Actions — mai in commit
- [ ] Toast admin conferma sync automatico

## Script utili

| Script | Quando |
|--------|--------|
| `scripts/sync_media_automation.py` | Urgenza post-upload |
| `scripts/migrate_supabase_media.py` | Migrazione batch |
| `scripts/purge_supabase*.py` | Pulizia bucket (con cautela) |

## Rule Cursor

`.cursor/rules/righetto-supabase-admin.mdc`

## Output atteso

Media allineati, homepage tour corretti, commit solo se file repo modificati
