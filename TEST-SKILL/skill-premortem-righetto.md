# Premortem Righetto — gate decisionale (sempre attivo)

> **Scopo:** evitare fix SEO/GSC/blog «ottimisti» che falliscono dopo il deploy.  
> **Ispirazione:** tecnica premortem (Klein/Kahneman) — *«il piano è già fallito, spiega perché»* invece di *«è un buon piano?»*.  
> **Stack:** Cursor + agente Righetto — stesso prompt usabile in chat.

---

## 1. Quando è OBBLIGATORIO (agente)

Esegui il premortem **prima di commit/push** se tocchi almeno uno di:

- Pagine **servizio** / **landing** / **blog** / **zona** (HTML pubblico)
- **JSON-LD** (schema, FAQ, rating, recensioni)
- **sitemap.xml**, **GSC** (`gsc-indexing-weekly.json`), batch indicizzazione
- **Venerdì** slot blog owner o fix acquisizione con impatto SERP
- Utente scrive **`Premortem`**, **`/premortem`**, *«premortem questo»*, *«premortem il piano»*

**Eccezione:** typo CSS isolato, copy interno admin senza schema — premortem opzionale.

---

## 2. Prompt utente (copia-incolla in Cursor)

```text
Premortem Righetto — assume che tra 8 settimane questo lavoro sia già fallito (GSC, indicizzazione o reputazione tecnica).

Contesto repo: TEST-SKILL/skill-premortem-righetto.md, skill-memoria-progressi.md, file modificati in questo task.

Per ogni rischio concreto (non consigli generici):
1) catena eventi passo-passo fino al fallimento;
2) assunzione nascosta che stavamo dando per scontata;
3) segnale precocce (GSC, probe, validate-page, Rich Results).

Poi in sintesi:
- fallimento più probabile;
- fallimento più pericoloso;
- assunzione nascosta più costosa;
- piano rivisto (diff minimo);
- checklist pre-push (solo voci non ancora OK).

Non dire solo «valida tutto»: indica file/URL/comandi specifici del repo.
```

---

## 3. Prompt agente (BLOCCANTE — eseguire in silenzio se non chiesto esplicitamente)

Dopo aver preparato le modifiche e **prima** di proporre commit/push:

1. Leggere `skill-memoria-progressi.md` §Prossimi passi + errori GSC recenti.
2. Simulare: *deploy fatto, GSC ancora giallo/rosso tra 6–8 settimane*.
3. Controllare almeno:
   - `grep -r aggregateRating servizio-*.html` → provider solo `@id` `#agenzia`, no rating annidato su Service
   - `grep -r '"@type": "Review"' *.html` → no recensioni self-serving (eccetto doc)
   - FAQ JSON-LD vs testo visibile → no €/mq/% senza fonte OMI/ADE/FIMAA
   - URL toccate in `sitemap.xml` + `validate-page.js`
4. Output **obbligatorio** all’utente (5–15 righe): rischio #1, fix già incluso o azione aggiuntiva, checklist restante.
5. Se premortem rivela gap **non** nel diff corrente → segnalarlo; non chiudere con «push e vediamo».

---

## 4. Checklist pre-push (SEO/GSC)

| # | Controllo | Comando / dove |
|---|-----------|----------------|
| 1 | Schema servizi coerente | `provider`: `{"@id":"https://righettoimmobiliare.it/#agenzia"}` — no `aggregateRating` nel figlio |
| 2 | No Review markup on-site | `rg '"@type": "Review"' --glob '*.html'` |
| 3 | Testimonial con stelle | sezione con `data-nosnippet` se citazioni marketing |
| 4 | FAQ allineate | JSON-LD = corpo pagina; mediazione **in sede** |
| 5 | Pagina validata | `node scripts/validate-page.js --file …` |
| 6 | Probe se URL nuove | `python scripts/probe_live_urls.py` |
| 7 | GSC post-deploy | Ispezione URL live → Richiedi indicizzazione → log in `gsc-indexing-weekly.json` |
| 8 | Memoria | 1 riga log in `skill-memoria-progressi.md` se sprint GSC/blog |

---

## 5. Policy recensioni (rich result — anti-regressione)

| Consentito | Vietato |
|------------|---------|
| `aggregateRating` su **homepage** `#agenzia` allineato a recensioni Google reali (127 · 4,9) | Array `"review": [...]` con testimonial inventati |
| Testimonial **visibili** senza schema Review | `aggregateRating` dentro `provider` di ogni `Service` |
| Link a scheda Google Maps / recensioni | Stelle in schema + 3 box citazione senza `data-nosnippet` (rischio parsing) |

**Batch pendente noto:** allineare tutti `servizio-*.html` al pattern `@graph` di `servizio-gestione` / `servizio-locazioni`.

---

## 6. Integrazione skill

| File | Ruolo |
|------|--------|
| `context-map.json` → `always_load` | Caricato ogni sessione agente |
| `skill-massimo-punteggio.md` §Premortem | Gate prima commit pubblico |
| `skill-seo.md` §Premortem | Rich result, GSC, batch servizi |
| `skill-acquisizione-cron-venerdi.md` | Premortem obbligatorio slot #2 blog se publish |
| `.cursor/skills/righetto-premortem/SKILL.md` | Slash `/premortem` |
| `righetto-core.mdc` | Trigger parole chiave |

---

## 7. Output atteso (formato breve)

```markdown
### Premortem — [data] · [task]
- **Più probabile:** …
- **Più pericoloso:** …
- **Assunzione nascosta:** …
- **Nel diff:** già coperto / manca: …
- **Pre-push:** [ ] … [ ] …
```
