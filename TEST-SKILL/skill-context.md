# SKILL-CONTEXT — Righetto Immobiliare
> Carica quando devi: modificare architettura, integrazioni, API, DNS, struttura file.
> Versione estratta da SKILL-2.0.md — Marzo 2026

---

## 1. INFORMAZIONI GENERALI

| Campo | Valore |
|---|---|
| Dominio | righettoimmobiliare.it (NON www) |
| Hosting sito | GitHub Pages (deploy auto da `main`) |
| Hosting dominio/email | cPanel (cpanel.righettoimmobiliare.it) |
| Tech Stack | HTML statico + CSS + JS vanilla + Express.js (solo dev) |
| Database | Supabase (PostgreSQL esterno) |
| API Email | `api.righettoimmobiliare.it` — PHP relay su cPanel (mail() nativa) |
| Email Marketing | Admin → Supabase Edge Function → API relay |
| Newsletter | Solo raccolta contatti → tabella `newsletter_subscribers` |
| Analytics | Google Analytics 4 (G-9MHDHHES26) |
| Chatbot AI | "Sara" — assistente virtuale integrata |
| Repository | GitHub — ginocapon/index |

---

## 2. ARCHITETTURA EMAIL (NO Brevo — tutto interno)

**Flusso a 2 livelli:**

1. **Frontend → API Relay (diretto)**
   - Landing, form contatti, chatbot Sara
   - Endpoint: `https://api.righettoimmobiliare.it/send-mail.php`
   - Auth: header `X-API-Key` (config in `js/config.js`)
   - Azioni: `send`, `send_single`, `send_batch`, `ping`

2. **Admin Email Marketing → Supabase Edge Function → API Relay**
   - Campagne massive dall'admin
   - Edge Function gestisce coda, tracking, blacklist, rate limiting
   - Tabelle Supabase: `campagne_email`, `coda_email`, `email_tracking`, `email_blacklist`

**File chiave:**
- `api/send-mail.php` — relay PHP (su cPanel)
- `supabase/functions/send-email/index.ts` — Edge Function
- `js/config.js` — `EMAIL_RELAY_URL`, `EMAIL_RELAY_KEY`
- `admin.html` — sezione Email Marketing

---

## 3. ARCHITETTURA DNS (NON TOCCARE MAI)

- **Record A:** GitHub Pages (185.199.108.153 etc.)
- **CNAME www:** ginocapon.github.io
- **Record MX:** email su cPanel (NON MODIFICARE)
- **Google Site Verification:** meta tag nel `<head>` di index.html

---

## 4. STRUTTURA FILE PRINCIPALE

```
index.html                        Homepage (canvas animato, testimonial, CTA)
immobili.html                     Lista immobili (Leaflet.js map, filtri)
immobile.html                     Dettaglio immobile (template dinamico JS)
agenzia-immobiliare-padova.html   Pagina pillar SEO keyword #1
servizi.html                      Hub servizi
servizio-*.html (6)               Vendita/Locazioni/Preliminari/Valutazioni/Gestione/Utenze
chi-siamo.html                    Chi siamo
contatti.html                     Form + WhatsApp
blog.html                         Blog hub (40+ articoli registrati)
blog-*.html (40+)                 Articoli blog SEO statici
blog-articolo.html                Template dinamico per articoli da scraping (?s=slug)
faq.html                          FAQ (37+ domande con categorie)
zona-*.html (14)                  Pagine quartieri/comuni
landing-*.html                    Landing pages vendita/valutazione/agente/mutuo/chat*
admin.html                        Pannello admin (Supabase, 2FA, Email Marketing, Audit, Analytics)
llms.txt                          File per AI bots (GEO)
sitemap.xml                       54+ URL indicizzati
robots.txt                        Direttive crawler (AI bots: Allow)
js/chatbot.js                     Chatbot Sara (105KB)
js/homepage.js                    Homepage logic (22 staticMap entries)
js/config.js                      Config API esterne
js/lead-conversion.js             Lead engine (A/B test, exit intent, sticky CTA, speed-to-lead)
scripts/validate-page.js          Pre-commit validator (blocca commit se schema/title mancanti)
scripts/audit-skill.sh            Audit automatico settimanale
.github/workflows/audit-settimanale.yml   Cron job venerdì 07:00 CET
```

---

## 5. REGISTRAZIONE ARTICOLI BLOG (4 posti — OBBLIGATORIO)

Ogni nuovo articolo blog DEVE essere registrato in TUTTI e 4:
1. `admin.html` → array `_blogSeedArticles` (con `data_pubblicazione: 'YYYY-MM-DD'`)
2. `blog.html` → array `articoliStatici`
3. `js/homepage.js` → oggetto `staticMap` + array `articoliStatici`
4. `sitemap.xml` → nuovo URL con `lastmod` e `priority 0.8`

> **ATTENZIONE:** `data_pubblicazione` mancante = commit BLOCCATO dal pre-commit hook.

---

## 6. CACHE-BUSTING (regola tecnica critica)

- Ogni CSS/JS negli HTML DEVE avere `?v=N` (es. `css/fonts.css?v=3`)
- Quando modifichi un file, incrementa il numero in TUTTI gli HTML che lo referenziano
- GitHub Pages: cache 10 min non modificabile — il `?v=` garantisce aggiornamento immediato
- Cache attuale: `?v=3` — prossima modifica → `?v=4`

---

## 7. GESTIONE cPanel

### Da eliminare (liberare spazio)
| File | Dimensione | Motivo |
|---|---|---|
| `backup-3.2.2026_10-53-22_wyrighet.tar.gz` | 37.04 GB | Backup già scaricato in locale |
| `public_htmlcopia140422.zip` | 11.37 GB | Backup WordPress 2022 — obsoleto |
| `error_log*` | variabile | Log vecchi |
| `sp_mysql_bk/` | variabile | Backup MySQL WordPress |
| `public_html/` contenuto | variabile | Vecchio sito WordPress |

### Da tenere assolutamente
- Record DNS, dominio, account email attivi, SSL
- Cartelle: `mail/`, `etc/`, `ssl/`, `cache/`, `logs/`, `tmp/`

---

## 8. NAP (Citazioni consistenti ovunque)

- **Nome:** Righetto Immobiliare
- **Indirizzo:** Via Roma 96, 35010 Limena PD
- **Telefono:** 049 884 3484
- **Email:** info@righettoimmobiliare.it
- **URL:** righettoimmobiliare.it (senza www)
