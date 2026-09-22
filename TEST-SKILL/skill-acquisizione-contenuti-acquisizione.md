# Skill — Contenuti web e social per acquisizione venditori

> **Scopo:** tradurre la strategia «**alleato del venditore**» in **articoli blog**, **post social** e **reel** che portano a valutazione/consulenza/incarico — senza copiare prompt SEO generici esterni.
>
> **Pipeline venerdì:** `data/venerdi-friday-pipeline.json`  
> **Territorio:** `data/advisor-territorio-limena-10km.json`  
> **Advisor:** `skill-real-estate-advisor.md` · **Funnel:** `skill-acquisizione-proprietari.md`

---

## 1. Repository esterni (provocazione utente — come usarli)

Su GitHub esistono bozze tipo **`ginocapon/-ISTRUZIONI-PER-PUBBLICAZIONE`** (prompt SEO + spintax social).

| Prendere | Scartare su Righetto |
|----------|----------------------|
| Struttura **TARGET → problema → CTA** | Dialetto / «92% umano» / errori casuali |
| Idea **varianti caption** (spintax controllato) | Dati `[DATO]` o percentuali senza fonte |
| Checklist lunghezze title/meta (allineata a §1.2 essentials) | Keyword stuffing, tono «vendi al momento giusto» senza OMI |
| Caroselli / reel con **foto + testo** | Unsplash, CDN, foto annunci reali nel blog |

**Fonte di verità Righetto:** solo `TEST-SKILL/*` + questa skill. I repo esterni sono **ispirazione strutturale**, non copy-paste.

---

## 2. Framework post social proprietari (BLOCCANTE)

Ogni post **orientato acquisizione** (venerdì slot 3 o bozza manuale) segue:

```
TARGET (chi è il proprietario)
→ PROBLEMA (1 frase empatica)
→ PROMESSA (cosa fa Righetto, tono alleato)
→ PROVA (claim consentiti o fatto verificabile)
→ CTA (link landing/servizio/hub)
→ 10+ hashtag (skill-social §2b)
```

**Media (ordine preferenza):**

1. **Carosello IG/FB** — 3–5 slide: problema / 2 insight / CTA (testo su palette brand, font leggibile mobile)
2. **Foto team o ufficio** — `img/team/` (reali, no FOTO AI)
3. **Copertina blog owner** — stesso titolo pari pari in caption
4. **Reel 9:16** — `righetto_social/genera_reel.py` o tour acquisizioni; max 30–45 s

**Copy:** `righetto_social/templates/social_sezioni.json` → sezione **`proprietari_acquisizione`**.

Dettaglio canali: **`skill-social-automation.md`** §2b (titolo pari pari solo per immobili/blog catalogo; per post owner **campagna** il titolo è la prima riga caption, può essere hook dedicato se link va a landing).

---

## 3. Articoli blog venerdì (slot repo #2)

Quando `venerdi-friday-pipeline.json` indica `mode: publish` (o coda `scheduled` + macrociclo blog):

### Checklist unificata (skill nuove + esistenti)

| Requisito | Skill |
|-----------|--------|
| Messaggio **alleato** in intro e CTA | `skill-real-estate-advisor.md` |
| `owner_path` A–L, `acquisition_priority: true` | `skill-acquisizione-proprietari.md` |
| 2500+ parole, anti-doppioni | `skill-content.md`, `check_doppioni_sito.py` |
| 1 hero IA + 3 figure IA, 2 tabelle, 2 SVG | `skill-content.md` §2.1, `skill-editoriale-visivo.md` |
| Marchio FOTO AI + audit | `skill-ai-act-compliance.md` |
| GEO Limena 10 km se tema locale | `advisor-territorio-limena-10km.json` |
| CTA Class A | `landing-valutazione`, `servizio-vendita`, `landing-consulenza` |
| Gate | `audit_editorial_acquisition.py`, `audit_blog_visuals.py` |

### Angoli titolo (Area 1 — non duplicare skimm)

Usare tabella intent in `skill-acquisizione-proprietari.md` § Equilibrio editoriale + settimana specifica in `venerdi-friday-pipeline.json` → `weeks_aligned_acquisition[].blog_friday`.

---

## 4. Coordinamento con `righetto_social`

| Giorno | Azione |
|--------|--------|
| **Venerdì (agente)** | Prepara 1 testo post proprietari (file in `righetto_social/bozze_manuali/` o commento in agenda) usando `social_proprietari` della settimana N |
| **Domenica cron** | `genera_bozze_settimanali.py` — rotazione catalogo; **non** sostituisce post owner dedicato |
| **Mar/Gio** | RSS notizie — angolo proprietario solo in chiusura caption (già in template notizia) |

**Reel acquisizione:** `genera_reel_portale_acquisizioni.py` — collegare a blog tour acquisizioni o nuovo incarico; CTA valutazione in descrizione.

---

## 5. KPI contenuto → acquisizione

Dopo publish venerdì, annotare in `skill-memoria-progressi.md`:

- Slug blog / URL landing toccati
- Post social preparato (sì/no)
- `owner_path` servito
- Prossimo passo funnel (awareness → considerazione → decisione)

KPI commerciali: `data/acquisition-kpi-template.json` (manuale agenzia).

---

## 6. Collegamenti

- Cron venerdì: **`skill-acquisizione-cron-venerdi.md`**
- Venerdì macrociclo: **`.cursor/skills/righetto-venerdi-sito-90giorni/SKILL.md`**
- Piano Q2 storico: **`docs/piano-editoriale-q2-2026.md`** (filoni, non sostituisce pipeline JSON)
