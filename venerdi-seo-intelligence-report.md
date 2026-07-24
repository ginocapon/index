# SEO/GEO Intelligence — Report venerdì
**Data:** 2026-07-24

> Framework PAGE SCORE e decisioni: `TEST-SKILL/skill-seo.md` §11

---

## 1. Sintesi esecutiva

- **Pagine analizzate:** 128
- **Da sostenere (refresh/GEO):** 12
- **Keyword gap (nuovi articoli):** 6
- **Probe tecnico issue:** 3

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
| `/blog-affitto-studenti-padova` | 80 | 271 | 8 | **SOSTENERE** | CTR basso su contenuto già corposo |
| `/blog-rendimento-affitto-padova` | 93 | 139 | 0 | **SOSTENERE** | 139 imp, 0 click — ottimizzare title/meta/snippet |
| `/agenzia-immobiliare-padova` | 75 | 68 | 0 | **SOSTENERE** | 68 imp, 0 click — ottimizzare title/meta/snippet |
| `/blog-affitto-breve-padova-2026` | 85 | 10 | 0 | **SOSTENERE** | CTR basso su contenuto già corposo |
| `/blog-articolo` | 40 | 0 | 0 | **SOSTENERE** | contenuto thin (147 parole) |
| `/blog-scuole-istruzione-padova` | 43 | 0 | 0 | **SOSTENERE** | contenuto thin (443 parole) |
| `/blog-servizi-infrastrutture-padova` | 43 | 0 | 0 | **SOSTENERE** | contenuto thin (430 parole) |
| `/blog-trasporti-mobilita-padova` | 43 | 0 | 0 | **SOSTENERE** | contenuto thin (433 parole) |
| `/blog-previsioni-immobiliari-scenari-geopolitica-2026` | 52 | 0 | 0 | **SOSTENERE** | contenuto thin (652 parole) |
| `/blog-mercato-italiano-tensioni-medio-oriente-2026` | 53 | 0 | 0 | **SOSTENERE** | contenuto thin (781 parole) |
| `/blog-prospettive-mercato-residenziale-italia-2026` | 55 | 0 | 0 | **SOSTENERE** | contenuto thin (625 parole) |
| `/blog-limena-vicino-padova-comprare-2026` | 57 | 0 | 0 | **SOSTENERE** | contenuto thin (807 parole) |

---

## 3. WINNER — MANTENERE

- `/blog-contratto-affitto-padova` — score 85, 6 click / 150 imp

---

## 4. AGGIUNGERE — keyword gap (max 1/settimana)

1. **omi padova affitti spiegati** → `blog-quotazioni-locazioni-omi-istat-padova-2026` — Query corta omi padova — pillar esistente aggiornato luglio 2026 (box AEO + FAQ)
2. **affitti limena** → `blog-affitti-limena` — GSC: 39 imp, 3 click
3. **agenzia immobiliare limena** → `blog-agenzia-immobiliare-limena` — GSC: 58 imp, 5 click
4. **agenzie immobiliari limena** → `blog-agenzie-immobiliari-limena` — GSC: 33 imp, 3 click
5. **omi padova** → `blog-omi-padova` — GSC: 14 imp, 0 click
6. **immobiliare** → `blog-immobiliare` — GSC: 28 imp, 0 click

---

## 5. Query GSC crescita (0 click)

- `agenzia immobiliare limena` — 58 imp, 5 click
- `affitti limena` — 39 imp, 3 click
- `agenzie immobiliari limena` — 33 imp, 3 click
- `immobiliare` — 28 imp, 0 click
- `omi padova` — 14 imp, 0 click
- `affitto limena` — 5 imp, 0 click
- `appartamento limena` — 5 imp, 0 click
- `immobiliare limena` — 5 imp, 0 click
- `affitti a limena` — 4 imp, 0 click
- `appartamento in affitto limena` — 4 imp, 0 click

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
