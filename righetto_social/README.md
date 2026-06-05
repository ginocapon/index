# Righetto Social — automazione Meta (senza AI a pagamento)

**Skill progetto (operativa):** [`TEST-SKILL/skill-social-automation.md`](../TEST-SKILL/skill-social-automation.md) — rotazione, token, cron, checklist avvio. Sintesi in `TEST-SKILL/SKILL-2.0.md` §10.4.

## Flusso consigliato (~16 bozze/settimana + agenda)

**Admin (senza token Meta):** Social → *Genera 12 bozze (auto)* oppure bozza singola da immobile/articolo/landing → **Approva** → Agenda.

**PC (token solo in `.env`):** reel FFmpeg + pubblicazione Meta + Google Business.

Ogni settimana (lun/mer/ven) vengono create **3 bozze per sezione** — **3 contenuti diversi** (rotazione sul catalogo; a fine giro si ricomincia):

| Sezione | Slot (lun / mer / ven) | Rotazione |
|---------|------------------------|-----------|
| **Immobile** | Reel · IG feed · FB | Tutti gli annunci **attivi** sul sito (ordine codice) |
| **Blog** | IG · FB · IG | Tutti gli articoli pubblicati |
| **Landing** | FB · IG · FB | Tutte le landing pubblicate |
| **Agenzia** | IG · FB · Reel | Pagine in `templates/social_sezioni.json` → `pagine_agenzia` |
| **Notizia esterna** | 2× FB + 2× Google | RSS Sole 24 Ore, Agenzia Entrate, Milano Finanza |

| Sezione | Media |
|---------|-------|
| **Immobile** | Video reel (più foto), foto singola per feed |
| **Blog** | Copertina articolo |
| **Landing** | Immagine landing |
| **Agenzia** | Reel / immagine da pagina |

**Notizie (≥2/settimana):** titolo rielaborato con keyword Padova/immobiliare, commento originale in spintax, link alla fonte — **mai copiare** il testo dell’articolo. Mar/gio in agenda.

Ogni bozza ha **spintax** nel testo e **almeno 10 hashtag** specialistici.

```powershell
cd righetto_social

# 1) Crea ~16 bozze in Supabase (12 sito + 4 notizie FB/Google)
python genera_bozze_settimanali.py

# 2) Genera MP4 per i reel (immobili + agenzia; blog/landing = 1 foto ripetuta)
python genera_reel.py --pending

# 3) Admin → Social → controlla → Approva (oppure programma da terminale)
python programma_da_bozze.py --min 8

# 4) Pubblicazione Meta (token in .env)
python publish_from_agenda.py --dry-run
```

Opzionale tutto-in-uno dopo le bozze: `python genera_bozze_settimanali.py --programma-agenda` (salta approvazione manuale).

## Setup iniziale

```bash
cd righetto_social
pip install -r requirements.txt
copy .env.example .env   # Windows
# Compila .env — minimo per generare bozze:
#   SUPABASE_URL = https://TUO-ID.supabase.co
#   SUPABASE_KEY = chiave service_role (Supabase → Settings → API)
cp config/settings.example.json config/settings.json   # OBBLIGATORIO per cron — senza non pubblica nulla
```

**Prima di affidarsi al cron:** `python scheduler.py --dry-run` deve dire `Finestra OK: True` negli orari 10/13/15/19.

Agenda rotazione catalogo (4 slot/giorno):

```bash
python programma_oggi_slot.py --dry-run --ciclo-completo
python programma_oggi_slot.py --ciclo-completo
```

Anteprima **senza** compilare `.env`:

```bash
python genera_bozze_settimanali.py --dry-run
```

Su Supabase SQL Editor, in ordine:

- `sql/pianificazioni.sql`
- `sql/bozze-social.sql`
- `sql/facebook-feed-cache.sql` / `sql/instagram-feed-cache.sql` (cache feed)
- **`sql/rls-security-hardening-safe.sql`** (sostituisce policy «anon scrive tutto» — vedi Sicurezza)

## Flusso attuale (manuale — cron Windows disabilitato)

**Niente Task Scheduler ogni 10 min** (evita flash PowerShell). Tu pianifichi il giorno e gli orari; pubblicazione quando decidi.

1. **Agenda del giorno** (con Cursor o script):
   ```powershell
   python programma_oggi_slot.py --include-oggi --giorni 2026-06-03
   ```
   (sostituisci la data; oppure `--pubblica` per pianificare + pubblicare subito)

2. **Token** (circa ogni 60 gg): `.\rinnova_token.ps1`

3. **Pubblica** quando vuoi:
   ```powershell
   .\pubblica_adesso.ps1
   ```
   oppure `python publish_from_agenda.py --modo manuale` (solo slot già passati) / `--forza` (tutto oggi)

**Disabilitare di nuovo il cron** (se reinstallato): `.\disabilita_cron_windows.ps1`

### Cron automatico (opzionale, non in uso)

Se in futuro vuoi ripristinarlo: `installa_cron_windows.ps1` come amministratore. Altrimenti lascia disabilitato con `disabilita_cron_windows.ps1`.

1. **Domenica 20:00** (opz.): `cron_settimanale.bat` → bozze settimana
2. **Ogni 5–10 min**: `cron_pubblica.bat` — **disattivato** su questo PC

Token Meta e Google solo in `.env`. Mai nell'admin.

**Google Business:** scheda [Gruppo Immobiliare Righetto](https://www.google.com/maps/place/Gruppo+Immobiliare+Righetto/). Con `GBP_MIRROR_META=1` ogni post/reel Meta viene replicato anche su GBP; le notizie RSS hanno righe `tipo=google` dedicate (mar/gio).

## Test pubblicazione Facebook / Instagram

```bash
python verifica_meta.py
python publish_from_agenda.py --dry-run --modo manuale
python publish_from_agenda.py --modo manuale
python publish_from_agenda.py --modo cron --dry-run
```

Requisiti token Meta: `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish` (se IG).

### Token Meta — solo `.env` (non admin)

| Variabile | Quando la cambi |
|-----------|------------------|
| `META_PAGE_ID` | Una volta |
| `META_IG_USER_ID` | Una volta |
| `META_PAGE_ACCESS_TOKEN` | Solo quando scade (~60 gg) |

L’admin **non legge** il file `.env` (è sul PC). I campi Social nell’admin sono opzionali e servono solo ai pulsanti “Pubblica da browser”; **bozze, agenda e `publish_from_agenda.py` usano solo `.env`.**

## Cron esempio (server Linux / Windows Task Scheduler)

```cron
# Ogni 10 min in fascia pubblicazione
*/10 9-11,13-14,18-21 * * 1-5 cd /path/righetto_social && python publish_from_agenda.py --modo cron >> logs/pub.log 2>&1

# Domenica 20:00 — bozze settimana successiva (12 sito + 2 notizie RSS)
0 20 * * 0 cd /path/righetto_social && python genera_bozze_settimanali.py >> logs/bozze.log 2>&1

# Sync feed (opzionale, 1×/giorno)
30 6 * * * cd /path/righetto_social && python sync_facebook_feed.py && python sync_instagram_feed.py
```

Windows: `cron_settimanale.bat` (domenica) + `cron_pubblica.bat` (ogni 5–10 min).

## Reel MP4 automatici (FFmpeg)

```powershell
winget install ffmpeg
cd righetto_social
python genera_reel.py --pending
```

Crea MP4 1080×1920 dalle foto immobile/blog/landing, carica su Storage (`foto-immobili/reels/`) e aggiorna la bozza. Con `GENERA_REEL_AUTO=1` in `.env` succede anche dopo `genera_bozze_settimanali.py`.

## Sicurezza — checklist

| Rischio | Stato attuale | Azione |
|--------|----------------|--------|
| `pianificazioni` / `bozze_social` scrivibili da chiunque con chiave `anon` | Alto se non hardened | Esegui `sql/rls-security-hardening-safe.sql` e cambia `righetto_admin_secret()` |
| Token Meta in `localStorage` (sezione Social admin) | Medio | Preferire solo `.env` sul server; non salvare token in browser in produzione |
| Chiave Supabase `anon` nel frontend admin | Noto | Limitare con RLS + header `x-righetto-admin` |
| Reel | Automatizzati se `media_direct_url` è .mp4 HTTPS | `genera_reel.py` + `publish_from_agenda.py` |

## Cosa NON fa questo pacchetto

- Remotion/OpenAI/voiceover AI (solo slideshow FFmpeg locale).
- Voiceover AI o sottotitoli automatici.
- Pubblicazione TikTok via API.
- Copia integrale articoli Sole24/ADE/Milano Finanza (solo titolo RSS + link + commento tuo in spintax).
- Storie Instagram automatizzate (tipo instagram_story).
