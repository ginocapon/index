# SEO/GEO Intelligence — Report venerdì
**Data:** 2026-07-09

> Framework PAGE SCORE e decisioni: `TEST-SKILL/skill-seo.md` §11

---

## 1. Sintesi esecutiva

- **Pagine analizzate:** 130
- **Da sostenere (refresh/GEO):** 12
- **Keyword gap (nuovi articoli):** 5
- **Probe tecnico issue:** 0

### Decisione settimana (regola)

| Priorità | Azione | Quando |
|---|---|---|
| 1 | **SOSTENERE** pagina con imp≥20 e 0 click | title + meta + 1 H2 + link interni |
| 2 | **GEO** FAQ/box sintesi su pillar | schema + Linda allineata |
| 3 | **AGGIUNGERE** 1 solo articolo da gap verificato | dopo check_doppioni |
| 4 | **MANTENERE** winner | timestamp mensile |

---

## 2. TOP — SOSTENERE / GEO (refresh)

| Pagina | Score | Imp | Click | Decisione | Motivo |
|---|---:|---:|---:|---|---|
| `/blog-affitto-studenti-padova` | 77 | 271 | 8 | **SOSTENERE** | CTR basso su contenuto già corposo |
| `/blog-rendimento-affitto-padova` | 93 | 139 | 0 | **SOSTENERE** | 139 imp, 0 click — ottimizzare title/meta/snippet |
| `/agenzia-immobiliare-padova` | 75 | 68 | 0 | **SOSTENERE** | 68 imp, 0 click — ottimizzare title/meta/snippet |
| `/blog-affitto-breve-padova-2026` | 82 | 10 | 0 | **SOSTENERE** | CTR basso su contenuto già corposo |
| `/blog-affitti-canoni-fimaa-q1-2024-padova` | 20 | 0 | 0 | **SOSTENERE** | contenuto thin (11 parole) |
| `/blog-bonus-edilizi-2024-incentivi-casa-padova` | 20 | 0 | 0 | **SOSTENERE** | contenuto thin (11 parole) |
| `/blog-piano-casa-decreto-salva-casa-padova` | 20 | 0 | 0 | **SOSTENERE** | contenuto thin (11 parole) |
| `/blog-vigonza-rubano-comprare-casa-cintura-2024` | 20 | 0 | 0 | **SOSTENERE** | contenuto thin (11 parole) |
| `/blog-articolo` | 40 | 0 | 0 | **SOSTENERE** | contenuto thin (146 parole) |
| `/blog-scuole-istruzione-padova` | 40 | 0 | 0 | **SOSTENERE** | contenuto thin (403 parole) |
| `/blog-servizi-infrastrutture-padova` | 40 | 0 | 0 | **SOSTENERE** | contenuto thin (398 parole) |
| `/blog-trasporti-mobilita-padova` | 40 | 0 | 0 | **SOSTENERE** | contenuto thin (401 parole) |

---

## 3. WINNER — MANTENERE

- `/blog-contratto-affitto-padova` — score 85, 6 click / 150 imp

---

## 4. AGGIUNGERE — keyword gap (max 1/settimana)

1. **omi padova affitti spiegati** → `blog-omi-padova-quotazioni-affitti-2026` — Query corta omi padova — titolo articolo OMI aggiornato luglio 2026
2. **affitti limena** → `blog-affitti-limena` — GSC: 12 imp, 0 click
3. **agenzia immobiliare limena** → `blog-agenzia-immobiliare-limena` — GSC: 13 imp, 0 click
4. **omi padova** → `blog-omi-padova` — GSC: 14 imp, 0 click
5. **immobiliare** → `blog-immobiliare` — GSC: 28 imp, 0 click

---

## 5. Query GSC crescita (0 click)

- `immobiliare` — 28 imp, 0 click
- `omi padova` — 14 imp, 0 click
- `agenzia immobiliare limena` — 13 imp, 0 click
- `affitti limena` — 12 imp, 0 click
- `affitto limena` — 5 imp, 0 click
- `appartamento limena` — 5 imp, 0 click
- `immobiliare limena` — 5 imp, 0 click
- `affitti a limena` — 4 imp, 0 click
- `appartamento in affitto limena` — 4 imp, 0 click
- `canone concordato padova` — 3 imp, 1 click

---

## 6. Idee originali GEO (rotazione mensile)

1. **Box risposta 40 parole** in cima agli articoli affitto (AI Overviews / Linda).
2. **Mesh Limena:** collegare 6 articoli territorio-limena tra loro + zona-limena + immobili filtrati.
3. **Zona pages doppio intent:** title `Vendita e affitto a {zona}` (14 pagine, batch script).
4. **Acquisizioni live:** blocco «ultimi incarichi zona» da Supabase nelle zone page.
5. **OMI in plain language:** tabella semestre ADE su pagina che rankia per `omi padova`.
6. **llms.txt:** aggiungere URL winner GSC entro 48h da ogni refresh.

> Generato da `scripts/venerdi-seo-intelligence.py`
> Aggiorna `data/gsc-keywords-priority.json` ogni venerdì dopo export GSC
