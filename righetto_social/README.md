# Righetto Social — automazione Meta (senza AI a pagamento)

## Flusso consigliato

1. **Genera bozze** (lun/mer/ven, no sab/dom):
   - Da Admin → **Social** → «Genera bozze settimanali», oppure
   - Sul PC/server: `python genera_bozze_settimanali.py` (cron domenica sera).
2. **Approva** in Admin → elenco «Bozze da pubblicare» (controlli testo, reel con URL `.mp4`).
3. All’approvazione si crea una riga in **`pianificazioni`** (Agenda).
4. **Pubblicazione automatica**: `publish_from_agenda.py` via cron ogni 5–10 min nelle finestre orarie.

## Setup iniziale

```bash
cd righetto_social
pip install -r requirements.txt
copy .env.example .env   # Windows
# Compila .env — minimo per generare bozze:
#   SUPABASE_URL = https://TUO-ID.supabase.co
#   SUPABASE_KEY = chiave service_role (Supabase → Settings → API)
cp config/settings.example.json config/settings.json
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

## Test pubblicazione Facebook / Instagram

```bash
python publish_from_agenda.py --dry-run
python publish_from_agenda.py --dry-run --ignore-scheduler
python publish_from_agenda.py --ignore-scheduler   # solo collaudo, fuori finestra
```

Requisiti token Meta: `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish` (se IG).

## Cron esempio (server Linux)

```cron
# Ogni 10 min in fascia pubblicazione (scheduler.py)
*/10 9-11,13-14,18-21 * * 1-5 cd /path/righetto_social && python publish_from_agenda.py >> logs/pub.log 2>&1

# Domenica 20:00 — bozze settimana successiva
0 20 * * 0 cd /path/righetto_social && python genera_bozze_settimanali.py >> logs/bozze.log 2>&1

# Sync feed (opzionale, 1×/giorno)
30 6 * * * cd /path/righetto_social && python sync_facebook_feed.py && python sync_instagram_feed.py
```

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
- Copia integrale articoli Sole24/ADE (solo titolo + link RSS + testo tuo in spintax).
