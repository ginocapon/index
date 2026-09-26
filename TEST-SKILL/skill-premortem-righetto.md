# Premortem Righetto — gate decisionale (sempre attivo)

> **Scopo:** migliorare **performance reali** del sito (velocità, indicizzazione, lead, compliance) — non produzere testo motivazionale.  
> **Ambito:** **tutte** le superfici pubbliche e ogni sfaccettatura toccata dal diff, finché non sostituiamo questo gate con un prompt più efficace.  
> **Ispirazione:** premortem Klein (HBR) · *prospettiva hindsight* Wharton/Cornell — *«è già fallito, spiega perché»* batte *«cosa potrebbe andare storto?»* (risposte più specifiche e sincere). Kahneman: tecnica decisionale ad alto valore.  
> **Regola anti-chiacchere:** ogni riga dell’output deve citare **file, URL o comando repo**; vietati consigli generici.  
> **Regola anti-ottimismo AI:** **vietato** chiedere all’agente *«è un buon piano?»* / *«valida la mia idea»* — frame obbligatorio: **`Premortem`** / *«rompi questo piano così lo ricostruisco più forte»*.

---

## 0. Confronto metodo (slide / letteratura ↔ Righetto)

| Idea esterna | Già in skill | Ottimizzazione Righetto |
|--------------|--------------|-------------------------|
| Premortem ≠ postmortem (prima del deploy) | §1, §3 simulazione 6–8 sett. | Invariato — core corretto |
| Retrospettiva prospettiva («già fallito») | §2 prompt utente | §3.1 frame agente esplicito |
| Per ogni fallimento: catena + assunzione + segnali | §2 punti 1–3 | §7 espanso per punto (max 5) |
| Sintesi: probabile / pericoloso / assunzione / piano rivisto / checklist | §2, §7 | §7.1 blocco strategico obbligatorio |
| Assunzione nascosta = spesso la parte più costosa | citata in §7 | **Evidenziare in output** (1 frase dedicata) |
| AI tende al sì → cambiare frame | parziale | § anti-ottimismo sopra + §3.2 |
| Skill file + trigger «Premortem questo» | `/premortem`, always_load | Trigger anche *«Premortem questo»* = §2 verbatim |

**Cosa NON copiamo dal marketing TikTok:** «viaggia 6 mesi nel futuro», promesse Claude-specific — restiamo su **repo Righetto** e comandi verificabili.

---

## 1. Quando è OBBLIGATORIO (agente)

Esegui il premortem **prima di commit/push** se tocchi almeno uno di:

- Qualsiasi **HTML/CSS/JS** servito al visitatore (homepage, hub, servizi, landing, blog, zone, immobili, scheda, share, legal, FAQ, funnel owner, visita virtuale, 404, redirect)
- **`homepage.js`**, **`immobili.js`**, **chatbot**, **form lead**, **schema** JSON-LD, **sitemap**, **robots**, **llms.txt** / **ai.json**
- **Admin** solo se impatta il pubblico (sync foto, slug, tour, watermark annunci)
- **Dati** GSC/GA4/editorial/acquisition in `data/*.json` se cambiano URL o priorità indicizzazione
- **Venerdì** publish blog / acquisizione / social che punta a URL live
- Utente: **`Premortem`**, **`/premortem`**, *«premortem questo»*, *«premortem il piano»*

**Eccezione (premortem leggero):** typo copy in `admin.html` o template email interni **senza** effetto su pagine pubbliche — solo `validate-page` se hai toccato HTML pubblico per errore.

**Default fino a nuovo prompt:** se il task modifica il sito e non rientra nell’eccezione → premortem **completo sulla matrice §4.2** (solo righe pertinenti al diff).

---

## 2. Prompt utente (copia-incolla in Cursor — valido su tutto il sito)

```text
Premortem questo — Righetto.

Non chiedere se il piano è buono: assume che tra 8 settimane sia GIÀ fallito (GSC, CWV, lead, trust, indicizzazione) e spiega perché con dettagli del repo, non consigli generici.

Contesto: TEST-SKILL/skill-premortem-righetto.md §4.2, skill-memoria-progressi.md, file nel diff.

Superfici possibili: homepage · servizi · landing owner · blog · zone · immobili/immobile/share · contatti/faq/chi-siamo · legal · JS globali · media annunci.

Sfaccettature: performance (WebP, ?v=, LCP) · SEO title/meta/canonical/sitemap · schema/GSC · form+Supabase · WCAG/mobile · claim/fonti · acquisizione proprietari · AI Act · sicurezza form/admin.

Per ogni rischio CONCRETO (max 5):
1) catena eventi fino al fallimento misurabile (es. CTR↓, URL non indicizzata, form morto, LCP↑);
2) assunzione nascosta;
3) segnale precocce: comando script repo, GSC, probe, validate-page.

Sintesi obbligatoria:
- fallimento più probabile (con URL o file);
- fallimento più pericoloso;
- assunzione più costosa;
- piano rivisto (diff minimo, riferimento skill-efficienza-sito.md);
- checklist pre-push: SOLO voci §4 ancora [ ].

Vietato: paragrafi senza path/comando. Se tutto OK: dirlo in 3 righe + comandi eseguiti.
```

---

## 3. Prompt agente (BLOCCANTE — prima di commit/push)

### 3.1 Frame (prospettiva hindsight — non negoziabile)

- Partire da: *«Il deploy è fatto. Tra 8 settimane GSC/lead/CWV sono peggiori o flat. Il team crede che il fix fosse sufficiente.»*
- **Non** elencare rischi generici da manuale; costruire **catene causali** ancorate a file/URL del diff.
- **Assunzione nascosta:** dedicare almeno una frase alla cosa «ovvia» su cui il piano poggia in silenzio (es. «basta push per chiudere GSC», «il form è uguale a contatti», «nessuno indicizza quella URL»).

### 3.2 Anti-ottimismo (comportamento agente)

- Se l’utente chiede validazione («va bene così?», «posso pushare?») → rispondere con **premortem §7**, non con «sì, sembra ok».
- Vietato chiudere con incoraggiamento senza almeno un rischio concreto **o** elenco comandi eseguiti con esito OK.

### 3.3 Passi operativi

1. Leggere `skill-memoria-progressi.md` §Prossimi passi + `data/gsc-indexing-weekly.json` se SEO.
2. Classificare il diff: quali **righe §4.2** della matrice si applicano (non elencare quelle irrilevanti).
3. Narrativa di fallimento per ogni **sfaccettatura** toccata (max 5 punti).
4. Eseguire controlli **minimi** (solo ciò che il diff richiede + regressione nota):

| Sempre se HTML pubblico nel diff | Comando |
|----------------------------------|---------|
| Title/meta | `node scripts/validate-page.js --file <pagina>` |
| Repo compliance | `python scripts/google-compliance-check.py` (se >1 pagina o schema) |
| Schema recensioni | `rg 'aggregateRating' servizio-*.html` · `rg '"@type": "Review"' --glob '*.html'` |
| URL nuove/modificate | `sitemap.xml` + opz. `python scripts/probe_live_urls.py` |
| Blog | `python scripts/check_doppioni_sito.py` (se nuovo articolo) |
| Foto annunci / img | `python scripts/verify_media_migration.py` (se `img/immobili/` o admin media) |
| Form/CTA | confronto con `contatti.html` / `skill-forms-leads.md` |
| JS globale | bump `?v=N` su CSS/JS linkati dalle pagine toccate |

5. Output utente **§7** (max 15 righe utili). Se gap fuori diff → 1 riga «debito noto» + non spacciare push come chiusura GSC.
6. **Performance:** se aggiungi immagini/script → citare peso WebP e above-the-fold (`skill-efficienza-sito.md` §3.1).

---

## 4. Checklist pre-push

### 4.1 Universale (ogni pagina pubblica nel diff)

| # | Controllo | Dove / comando |
|---|-----------|----------------|
| U1 | Canonical apex, no `.html` negli href interni | pagina + `mini-seo-check.sh` |
| U2 | Title ≤60 (max 70), meta ≤160 | `validate-page.js` |
| U3 | CSS/JS `?v=N` incrementato | file toccati |
| U4 | Mobile-first: niente overflow/CTA illeggibili | ispezione + `skill-design.md` |
| U5 | CTA WCAG AA — no `#FF6B35` + testo bianco | CSS toccato |
| U6 | Claim: 350+/101/98%/127·4,9/dal 2000; mediazione **in sede** | copy |
| U7 | Sitemap `lastmod` se URL nuova/rimossa | `sitemap.xml` |

### 4.2 Matrice superficie × sfaccettatura

Applica **solo** le righe il cui tipo compare nel diff.

| Superficie | Pattern file / URL | Performance | SEO/GSC | Schema | Lead | Contenuto | Altro |
|------------|-------------------|-------------|---------|--------|------|-----------|-------|
| Homepage | `index.html`, `homepage.js` | hero WebP, no lazy LCP | 1 H1, pillar link | `#agenzia` rating OK, no Review array | CTA owner/acquirente | messaggio alleato venditori | GA4 `G-PHEL8KXLBX` |
| Hub | `servizi.html`, `blog.html`, `immobili.html` | card img leggere | index interni | Breadcrumb | — | — | — |
| Servizio | `servizio-*.html` | idem | FAQ keyword naturale | `@graph`, provider `@id` #agenzia | form se presente | no % commissione | batch pattern gestione/locazioni |
| Landing owner | `landing-*.html`, `proprietario-*.html`, `valutazione-*.html` | form above fold | intent acquisizione | FAQ allineate | `SERVIZI_CONFIG` + Supabase | funnel A–L | `skill-acquisizione-proprietari.md` |
| Blog | `blog-*.html` | hero ≤150KiB WebP | anti-doppioni | FAQPage + Article | form CTA | 2500+ utili, fonti, no filler | `audit_blog_visuals.py` se nuovo |
| Zona | `zona-*.html` | map/img lazy sotto fold | OMI/geo reale | LocalBusiness/FAQ | link valutazione | no dati inventati | `skill-zona` |
| Annunci | `immobile.html`, `immobili.html`, `share-immobile-*.html` | foto WebP GitHub | slug coerente | Product/Offer sobrio | richiesta visita | prezzo coerente admin | sync 6h |
| Visita / tool | `visita-virtuale.html`, confronta, alert | JS vanilla, no CDN | indicizzazione se public | — | — | — | `data/visite-virtuali.json` |
| Istituzionale | `contatti`, `faq`, `chi-siamo`, autori | font preload | E-E-A-T link autore | FAQ chatbot sync | form modello contatti | — | `js/chatbot.js` se FAQ |
| Legal / trust | privacy, cookie, termini | leggero | index/noindex corretto | — | — | AI Act bar se sito | `skill-ai-act-compliance.md` |
| Global | `css/`, `js/` condivisi | no blur anim, no will-change permanente | — | — | — | — | diff minimo |

### 4.3 SEO/GSC (se schema o servizi/blog/zone)

| # | Controllo | Comando / dove |
|---|-----------|----------------|
| G1 | Provider Service senza rating annidato | `rg aggregateRating servizio-*.html` |
| G2 | No Review markup self-serving | `rg '"@type": "Review"' --glob '*.html'` |
| G3 | Testimonial visibili | `data-nosnippet` se citazioni |
| G4 | FAQ JSON-LD = corpo | no €/mq/% senza fonte |
| G5 | Post-deploy GSC | Ispezione live → indicizzazione → `gsc-indexing-weekly.json` |
| G6 | Memoria sprint | riga in `skill-memoria-progressi.md` |

---

## 5. Policy recensioni (rich result — anti-regressione)

| Consentito | Vietato |
|------------|---------|
| `aggregateRating` su **homepage** `#agenzia` (127 · 4,9 verificato) | Array `"review": [...]` inventati |
| Testimonial **visibili** senza schema Review | `aggregateRating` in `Service.provider` |
| Link scheda Google Maps | Stelle in schema + citazioni senza `data-nosnippet` |

**Debito noto:** allineare tutti `servizio-*.html` al `@graph` di `servizio-gestione` / `servizio-locazioni`.

---

## 6. Integrazione skill (razionale, non duplicata)

| File | Ruolo |
|------|--------|
| `context-map.json` → `always_load` | Gate ogni sessione |
| `skill-massimo-punteggio.md` §0 | Ordine lettura + premortem pre-commit |
| `skill-efficienza-sito.md` §2–3 | Comandi performance/lead — premortem **non** riscrive, **invoca** |
| `skill-seo.md` §12 | Punto ingresso SEO |
| `skill-forms-leads.md` | Solo se form nel diff |
| `skill-acquisizione-cron-venerdi.md` | Publish venerdì |
| `.cursor/skills/righetto-premortem/SKILL.md` | `/premortem` |
| `righetto-core.mdc` | Trigger + ambito sito intero |

**Sostituzione futura:** quando avremo un prompt/comando più efficace, deprecare §2 mantenendo §4.2 come checklist secca.

---

## 7. Output atteso (formato breve — obbligatorio)

### 7.1 Per ogni punto di fallimento (max 5)

```markdown
#### Fallimento N — [titolo breve]
- **Catena:** passo 1 → 2 → … → esito misurabile (GSC / form / LCP / lead)
- **Assunzione nascosta:** …
- **Segnale precoce:** GSC · probe · validate-page · Rich Results · GA4 — quale e quando
- **Anchor repo:** `path` o URL
```

### 7.2 Sintesi strategica (sempre, anche se un solo rischio)

```markdown
### Premortem · [task] · superfici: […]
- **Più probabile:** …
- **Più pericoloso:** …
- **Assunzione più costosa (Klein):** … — spesso era «ovvia» e non scritta nel piano
- **Piano rivisto (diff minimo):** …
- **Comandi eseguiti:** `…` → esito
- **Nel diff:** coperto / manca: …
- **Checklist pre-lancio:** [ ] U… [ ] G… (solo voci ancora aperte)
```

Se nessun rischio dopo controlli: *«OK push — premortem negativo utile — eseguiti: …»* (comandi elencati). Max ~20 righe totali utili; zero paragrafi motivazionali.
