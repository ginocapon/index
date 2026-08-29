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

1. **`TEST-SKILL/skill-editoriale-visivo.md`** — comando permanente (ricerca §8–17 + visivo §1–7 + §16-QUATER/QUINQUIES)
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
9. **§16-QUATER:** `python scripts/build_editorial_visual_memory.py` — struttura/immagini recenti

## Checklist PRE-SCRITTURA (ricerca §15 + continuità §16-TER + varietà §16-QUATER)

- [ ] Scansione 3 aree: mercato Padova/Veneto · politica con impatto · normativa verificata
- [ ] Fonti primarie (GU/ADE/ISTAT/OMI) + seconda fonte indipendente
- [ ] GSC + Google Trends analizzati se disponibili
- [ ] Top 5 contenuti web → `gap_analysis` + `value_add` in coda
- [ ] `editorial_type`: `trend` (~50%) o `evergreen` (~50%)
- [ ] Domande §16-TER: valore nuovo? lettore abituale lo percepisce nuovo?
- [ ] `substantive_area`, `main_question`, `reader_novelty` in coda; `update_reason` se area saturata
- [ ] **`structure_type`** scelto per argomento (GUIDA/ANALITICA/CONFRONTO/… — no clone ultimi 8)
- [ ] **`geo_focus`**, **`owner_relevance`**, **`faq_candidates`**, **`chart_types`** in coda (§16-QUINQUIES)
- [ ] Verifica saturazione struttura in `editorial-visual-memory.json`
- [ ] `python scripts/audit_editorial_research.py --id eq-XXX` → OK
- [ ] `python scripts/audit_editorial_continuity.py --id eq-XXX` → OK
- [ ] Nessun residuo template: no «Further reading», «Note operative», «Approfondimento N»

## Checklist articolo (visivo §7 + §16-QUATER + contenuto)

- [ ] Immagini WebP **dedicate** al slug (`img/blog/blog-{slug}-*.webp`) — no riuso cross-articolo
- [ ] ≥2 SVG con layout/aria-label diversi dagli ultimi articoli
- [ ] `audit_blog_visuals.py --file blog-{slug}.html` → OK
- [ ] `audit_editorial_visual_variety.py --file blog-{slug}.html` → OK (§16-QUATER)
- [ ] ≥3 foto IA pertinenti al paragrafo + 1 hero + ≥2 SVG + ≥2 tabelle
- [ ] **Lunghezza:** target ~2500 parole (±20%) — **qualità prima del conteggio**; vietato `expand_body` filler (`skill-prompt-chirurgo-homepage-editoriale.md`)
- [ ] Distinzione fatto / dichiarazione / analisi / previsione nel testo
- [ ] Valore aggiunto Padova/Veneto — non copia concorrenti
- [ ] FOTO AI: `build-ai-image-manifest.mjs` + `audit-foto-ai.mjs` OK
- [ ] FAQ schema da `faq_candidates` — risposta immediata + condizioni (§16-QUINQUIES)
- [ ] `audit_blog_publishability.py --file blog-{slug}.html` → OK (§18)
- [ ] Title ≤60, meta ≤160, JSON-LD, link interni, form se CTA

## Registrazione pagina

- `blog-{slug}.html` · `blog.html` · `homepage.js` · `admin.html` · `sitemap.xml`
- `validate-page.js --file blog-{slug}.html`

## Dopo publish

- Coda → `published` · `gsc-keywords` · `skill-memoria` §Log
- `python scripts/build_editorial_memory.py` (memoria §16-TER)
- `python scripts/build_editorial_visual_memory.py` (memoria §16-QUATER)
- Valutare FAQ sito/chatbot se emergono nuove domande (`scripts/audit_chatbot_faq.py`)
