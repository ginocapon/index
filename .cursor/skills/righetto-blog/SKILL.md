---
name: righetto-blog
description: >-
  Crea o aggiorna articoli blog Righetto Immobiliare (Padova, Limena, hinterland):
  ricerca strategica, anti-doppioni SKIMM, 2500+ parole, fonti istituzionali,
  immagini/grafiche pertinenti, schema FAQ, form lead se CTA.
  Usa quando l'utente chiede nuovo articolo, blog su un tema, aggiornamento post,
  keyword long-tail, o contenuto editoriale immobiliare.
---

# Blog Righetto

## Coda editoriale (leggi PRIMA — non chiedere all'utente)

1. **`TEST-SKILL/skill-editoriale-visivo.md`** — comando permanente (ricerca §8–17 + visivo §1–7)
2. **`data/editorial-queue.json`** — prossimo `scheduled`
3. **`TEST-SKILL/skill-editorial-queue.md`** — sequenza 12 passi + discovery
4. **`data/gsc-keywords-priority.json`** — SOSTENERE prima di AGGIUNGERE
5. Se coda `scheduled` < 3 → discovery (§15–16 skill-editoriale-visivo)

**Trigger autonomi:** «pubblica blog», «prossimo articolo», venerdì, `/blog` senza tema → coda + ricerca.

## Prima di iniziare (BLOCCANTE)

1. `skill-essentials.md` + `skill-massimo-punteggio.md` + `skill-efficienza-sito.md`
2. **`skill-editoriale-visivo.md`** — ricerca e visivo (PRIORITÀ editoriale)
3. `skill-memoria-progressi.md` + `skill-editorial-queue.md`
4. `skill-content.md` + `skill-ai-act-compliance.md`
5. `data/gsc-keywords-priority.json`
6. `skimm.md` + `python scripts/check_doppioni_sito.py` + `build_skimm.py`
7. Se doppione → `cancelled` in coda, discovery, STOP
8. **§16-TER:** `python scripts/build_editorial_memory.py` — rileggi memoria sostanziale recente

## Checklist PRE-SCRITTURA (ricerca §15 + continuità §16-TER)

- [ ] Scansione 3 aree: mercato Padova/Veneto · politica con impatto · normativa verificata
- [ ] Fonti primarie (GU/ADE/ISTAT/OMI) + seconda fonte indipendente
- [ ] GSC + Google Trends analizzati se disponibili
- [ ] Top 5 contenuti web → `gap_analysis` + `value_add` in coda
- [ ] `editorial_type`: `trend` (~50%) o `evergreen` (~50%)
- [ ] Domande §16-TER: valore nuovo? lettore abituale lo percepisce nuovo?
- [ ] `substantive_area`, `main_question`, `reader_novelty` in coda; `update_reason` se area saturata
- [ ] `python scripts/audit_editorial_research.py --id eq-XXX` → OK
- [ ] `python scripts/audit_editorial_continuity.py --id eq-XXX` → OK

## Checklist articolo (visivo §7 + contenuto)

- [ ] `audit_blog_visuals.py --file blog-{slug}.html` → OK
- [ ] ≥3 foto IA pertinenti al paragrafo + 1 hero + ≥2 SVG + ≥2 tabelle
- [ ] `kw_primaria` univoca · 2500+ parole · fonti verificate
- [ ] Distinzione fatto / dichiarazione / analisi / previsione nel testo
- [ ] Valore aggiunto Padova/Veneto — non copia concorrenti
- [ ] FOTO AI: `build-ai-image-manifest.mjs` + `audit-foto-ai.mjs` OK
- [ ] Title ≤60, meta ≤160, JSON-LD, link interni, form se CTA

## Registrazione pagina

- `blog-{slug}.html` · `blog.html` · `homepage.js` · `admin.html` · `sitemap.xml`
- `validate-page.js --file blog-{slug}.html`

## Dopo publish

- Coda → `published` · `gsc-keywords` · `skill-memoria` §Log
- `python scripts/build_editorial_memory.py` (memoria §16-TER)
