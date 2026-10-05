# Prompt per un'altra AI — allineare i 147 articoli blog (design/contrasti)

**Copia tutto sotto la linea nella chat dell'altra AI** (con accesso al repo `index`).

---

Lavori sul repo Righetto Immobiliare (HTML/CSS/JS vanilla, GitHub Pages, zero CDN). Leggi PRIMA: `CLAUDE.md`, `TEST-SKILL/skill-design.md` **§14**, `data/blog-design-audit-2026-10-05.json`. Non scrivere altro codice che non sia richiesto qui sotto. **Non fare push** (solo commit). Nessun dato nuovo, nessun claim nuovo: tocchi solo layout/colori/dimensioni.

## Passo 1 — Applica il CSS condiviso a tutti gli articoli (1 comando)
```
python scripts/apply-blog-article-css.py --all
```
Inserisce `css/rig-blog-article.css?v=2` dopo `blog-lead-form.css` in tutti i `blog-*.html` e porta `blog-lead-form.css` a `?v=3`. Verifica `git diff --stat`: solo righe `<link>` cambiate. Poi aggiorna i template: in ogni `scripts/build_blog_*.py` che contiene `blog-lead-form.css` aggiungi subito dopo `<link rel="stylesheet" href="css/rig-blog-article.css?v=2">` e porta il link lead-form a `?v=3` (cerca con `rg "blog-lead-form.css" scripts`). Commit: `Blog: CSS condiviso articoli (tipografia e contrasti)`.

## Passo 2 — Misura
```
python -m http.server 8765
```
Apri `http://localhost:8765/robots.txt` nel browser, poi in console/CDP:
```js
const s = await (await fetch('/scripts/audit-blog-design.js')).text(); (0,eval)(s);
const slugs = await (await fetch('/_tmp_blog_slugs.json')).json();   // oppure elenco a mano, SENZA .html
const r1440 = await rigAuditBatch(slugs.slice(0,40), 1440);          // a blocchi da ~40
const r390  = await rigAuditBatch(slugs.slice(0,40), 390);
```
(Crea `_tmp_blog_slugs.json` con `Get-ChildItem blog-*.html | % BaseName | ConvertTo-Json` e **cancellalo a fine lavoro**.) Output = solo pagine con problemi. Non usare `inject`: ora il CSS è davvero nelle pagine.

## Passo 3 — Correggi i residui (≈50 pagine, vedi JSON `residual_*`)
Per ogni pagina non a 0 issues, modifica **lo `<style>` inline di quella pagina** (o l'HTML) — non il CSS condiviso, salvo se lo stesso difetto compare in ≥ 5 pagine (allora aggiungi una regola in `css/rig-blog-article.css` e porta `?v=` a 3 ovunque con lo script).
Regole di decisione (da §14):
- testo chiaro su fondo chiaro (1.0–1.8:1): quasi sempre un blocco scuro rimasto senza sfondo, o un `<div>` non chiuso → chiudi il div / ripristina il fondo `--nero`/`--blu`, **non** scurire il testo se il design è un box scuro;
- `TH` bianco su chiaro: dai a `thead th` sfondo `--blu` e testo `#fff`;
- `font-size` < 0.7rem → 0.7rem; paragrafi < 0.95rem → 1rem; salto titoli → correggi il livello (H4→H3) mantenendo la grafica con classe;
- overflow a 390px: `minmax(0,1fr)` + `min-width:0`, tabelle in wrapper con `overflow-x:auto`, `overflow-wrap:anywhere` sui testi lunghi;
- data non visibile: aggiungi una riga «Aggiornamento: <data già presente in dateModified>» a fine articolo; **non** inventare date;
- `blog-articolo`, `blog-prova-mercato-limena-zona-imma-2027`: NON correggere a caso — riporta se sono pagine da pubblicare o residui.
Vietato: `#FF6B35` come colore testo su fondo chiaro o testo bianco su arancio; `filter: blur` animato; librerie/CDN.

## Passo 4 — Verifica e chiusura
1. Rilancia l'audit su tutte le pagine toccate a 1440 e 390 → **0 issues** (o motivazione scritta per ognuna rimasta).
2. Per 3 pagine a campione (una con `.cta-banner`, una con `.stat-card`, una con tabella) fai uno **screenshot** a 390 e a 1440 e guardalo davvero: il bianco-su-bianco non sempre è catturato dai numeri.
3. `node scripts/validate-page.js --staged` e `python scripts/check_doppioni_sito.py` senza nuovi errori.
4. Aggiorna `data/blog-design-audit-2026-10-05.json` (campo `result_with_shared_css`) e cancella `_tmp_blog_slugs.json`.
5. Un commit finale in italiano. **Niente push.** Riporta: n. pagine a 0 issues, elenco pagine rimaste con motivo, nessuna chiacchiera.

Fuori scope (segnala soltanto, non toccare): errori di `google-compliance-check.py` (servizio-gestione, servizio-locazioni, GeoCoordinates), contenuto testuale degli articoli.
