---
name: righetto-blog
description: >-
  Crea o aggiorna articoli blog Righetto Immobiliare (Padova, Limena, hinterland):
  anti-doppioni SKIMM, 2500+ parole, fonti istituzionali, schema FAQ, form lead se CTA.
  Usa quando l'utente chiede nuovo articolo, blog su un tema, aggiornamento post,
  keyword long-tail, o contenuto editoriale immobiliare.
---

# Blog Righetto

## Coda editoriale (leggi PRIMA — non chiedere all'utente)

1. **`data/editorial-queue.json`** — prossimo `scheduled` da pubblicare
2. **`TEST-SKILL/skill-editorial-queue.md`** — sequenza automatica completa
3. **`data/gsc-keywords-priority.json`** → `queries_limena_top_volume` per batch Limena locale
4. **Discovery web settimanale:** `python scripts/web-keyword-discovery.py` → 5 proposte + brief hero
5. Se `scheduled` < 3 → discovery aggiunge `proposed` «pubblica blog», «prossimo articolo», venerdì + modifica repo, `/blog` senza tema specifico → prendi prossimo item coda.

## Prima di iniziare (BLOCCANTE)

1. `TEST-SKILL/skill-essentials.md` + `TEST-SKILL/skill-massimo-punteggio.md`
2. `TEST-SKILL/skill-memoria-progressi.md` + **`TEST-SKILL/skill-editorial-queue.md`**
3. `TEST-SKILL/skill-content.md` (template, cluster, standard articoli)
4. **`TEST-SKILL/skill-ai-act-compliance.md`** (trasparenza foto/assistente — priorità permanente)
5. `data/gsc-keywords-priority.json` — SOSTENERE prima di AGGIUNGERE se priorità GSC
6. `TEST-SKILL/skimm.md` — keyword primaria univoca
7. **Anti-doppioni:** `python scripts/check_doppioni_sito.py` + `python scripts/build_skimm.py`
8. Se doppione → marca coda `cancelled`, discovery nuovo tema, STOP publish

## Checklist articolo

- [ ] `kw_primaria` univoca in skimm §3
- [ ] 2500+ parole corpo utile, 10–15 H2/H3, tono professionale
- [ ] Ogni dato numerico con fonte verificata e link
- [ ] Copertina hero **originale HD** generata da zero (§2.1 E) — `verify_blog_hero_assets.py` OK
- [ ] **Hero/figure:** generati da zero 1900×900 WebP — `verify_blog_hero_assets.py` + `geo-aeo-formula.py`
- [ ] **AI Act:** didascalia hero/figure se elaborazione digitale — `skill-ai-act-compliance.md`
- [ ] Title ≤60, meta ≤160, H1 diverso da title
- [ ] JSON-LD: `BlogPosting` + `FAQPage` se FAQ visibile
- [ ] Link interni verso pillar/zone/servizi del cluster
- [ ] Se form/CTA lead → `TEST-SKILL/skill-forms-leads.md` + `rig-lead-form.js`

## Registrazione pagina

- `blog-{slug}.html`
- `blog.html` (`articoliStatici`) + `js/homepage.js`
- `admin.html` (`_blogSeedArticles` con `data_pubblicazione`)
- `sitemap.xml`
- `node scripts/validate-page.js --file blog-{slug}.html`

## Modelli

- Articolo recente dello stesso cluster in `blog-*.html`
- Template completo: `TEST-SKILL/SKILL-2.0.md` §3 e §8.1a/8.1c

## Rule Cursor

`.cursor/rules/righetto-blog-publish.mdc` si attiva su `blog-*.html`

## Output atteso

HTML pubblicato, catalogo aggiornato, `editorial-queue.json` item → `published`, skill-memoria §Log, validate-page OK, commit se richiesto

## Dopo publish

- Aggiorna `data/editorial-queue.json` (status, published_date)
- Aggiorna `data/gsc-keywords-priority.json` → `published_this_week`
- Riga in `TEST-SKILL/skill-memoria-progressi.md` §Log cronologico
