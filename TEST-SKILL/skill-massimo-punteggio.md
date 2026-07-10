# SKILL-MASSIMO-PUNTEGGIO — Righetto Immobiliare

> **GATE OBBLIGATORIO:** leggere questo file **prima di ogni modifica** al sito (HTML, CSS, JS, blog, skill).  
> Obiettivo: **10/10** su SEO tecnico, contenuti, CWV, E-E-A-T, GEO/AEO — nessuna regola Google esclusa.

**Ordine lettura sessione (non saltare):**
1. Questo file (`skill-massimo-punteggio.md`)
2. `skill-essentials.md`
3. `TEST-SKILL/skimm.md` (se blog/contenuti)
4. Modulo task da `context-map.json` (seo → `skill-seo.md`, UI → `skill-design.md`, …)
5. File HTML/CSS da modificare

---

## 1. Strumenti gratuiti (zero costo — usare sempre)

| Strumento | URL / comando | Cosa verifica |
|---|---|---|
| **Google PageSpeed Insights** | https://pagespeed.web.dev/ | LCP, INP, CLS, opportunità |
| **Lighthouse CLI** | `npx lighthouse URL --only-categories=performance,seo,accessibility,best-practices` | Audit locale completo |
| **Google Search Console** | https://search.google.com/search-console | Indicizzazione, CWV campo, query |
| **Rich Results Test** | https://search.google.com/test/rich-results | Schema JSON-LD valido |
| **Schema Markup Validator** | https://validator.schema.org/ | Errori structured data |
| **Mobile-Friendly Test** | https://search.google.com/test/mobile-friendly | Mobile-first indexing |
| **WAVE** | https://wave.webaim.org/ | Accessibilità WCAG |
| **axe DevTools** | Estensione Chrome gratuita | A11y automatica |
| **Built-in repo** | `python scripts/google-compliance-check.py` | Checklist Google completa repo |
| **Built-in repo** | `python scripts/build_skimm.py` + `check_doppioni_sito.py` | Anti-doppioni + keyword |
| **Built-in repo** | `node scripts/validate-page.js --staged` | Pre-commit pagine |
| **Built-in repo** | `bash scripts/mini-seo-check.sh` | Meta, schema, GEO, freshness |
| **Built-in repo** | `python scripts/patch_cdn_local.py` | CDN → `js/vendor/` (supabase, jspdf, qrcode) |
| **Built-in repo** | `python scripts/patch_audit_warns.py` | GA4, dateModified JSON-LD, OG, freshness blog |
| **Built-in repo** | `python scripts/audit_helpers.py` | Conteggi keyword su testo visibile (word boundary) |
| **Built-in repo** | `bash scripts/audit-skill.sh` | Audit SKILL-2.0 strutturale |
| **Built-in repo** | `python scripts/venerdi-contenuti-freschezza.py` | Blog corposità + pillar |

**Routine post-modifica (locale):**
```bash
python scripts/google-compliance-check.py
python scripts/patch_cdn_local.py              # se tocchi JS Supabase/PDF/QR
python scripts/patch_compliance_warns.py       # title/meta/geo/breadcrumb/stuffing
python scripts/patch_audit_warns.py            # GA4, dateModified, OG
python scripts/patch_righetto_sol_blog.py      # se manca righetto-sol su blog
node scripts/validate-page.js --file pagina-modificata.html
python scripts/build_skimm.py   # se tocchi blog
bash scripts/mini-seo-check.sh && bash scripts/audit-skill.sh
```

---

## 2. Checklist Google 2026 — TUTTE le regole (nessuna esclusa)

### 2.1 Indicizzazione e crawl
- [ ] `robots.txt` non blocca pagine importanti né bot AI utili (GPTBot, Google-Extended, PerplexityBot)
- [ ] `sitemap.xml` aggiornata, URL senza `.html`, `lastmod` coerente
- [ ] Canonical unica per URL, senza `.html`
- [ ] No link interni con `.html`
- [ ] `noindex` solo su pagine admin/helper/404
- [ ] HTTPS, no mixed content
- [ ] Mobile-first: layout OK a 375px

### 2.2 On-page SEO
- [ ] `<title>` unico, **≤60 caratteri** (max **70** — soglia audit admin), keyword + località
- [ ] Meta description unica, **120–155 caratteri** (max **160**), dato/beneficio
- [ ] **Verifica automatica:** `node scripts/validate-page.js --file pagina.html` a fine task contenuti (`skill-essentials.md` §1.2)
- [ ] H1 unico allineato al title (variante, non copia)
- [ ] Gerarchia H2/H3 logica, H2 domanda per AEO dove possibile
- [ ] Alt text descrittivo su ogni `<img>`
- [ ] OG + Twitter Card completi
- [ ] Keyword stuffing: max 5× stessa frase 2+ parole; max 10× «a/di Padova»

### 2.3 Core Web Vitals
- [ ] LCP < 2,5s (target < 2s) — preload hero + font critici
- [ ] INP < 200ms — no JS pesante above-fold
- [ ] CLS < 0,1 — dimensioni esplicite img, no layout shift
- [ ] No `loading="lazy"` su LCP/hero
- [ ] CSS critico inline; resto `media="print" onload`
- [ ] No `filter: blur` su animazioni; no `will-change` permanente
- [ ] Immagini WebP, hero < 150 KiB dove possibile

### 2.4 Structured Data (Schema.org)
- [ ] `RealEstateAgent` + `GeoCoordinates` + `sameAs` su ogni pagina pubblica
- [ ] `FAQPage` su blog, zone, servizi, FAQ, landing conversione
- [ ] `BreadcrumbList` su tutte le pagine tranne homepage
- [ ] `BlogPosting` + `dateModified` su articoli
- [ ] `Person` su pagine autore e bio blog
- [ ] FAQ JSON-LD = testo visibile (no mismatch)

### 2.5 E-E-A-T (Experience, Expertise, Authority, Trust)
- [ ] Pagine autore `/gino-capon`, `/linda-righetto` linkate da blog
- [ ] Bio autore visibile su articoli
- [ ] «Cosa può fare Righetto» su articoli nuovi/refresh
- [ ] Claim solo verificati (350+, 101 comuni, 127 recensioni, dal 2000)
- [ ] Mediazione: mai tariffe online
- [ ] Fonti istituzionali per ogni dato numerico
- [ ] Timestamp «Ultimo aggiornamento» su cornerstone

### 2.6 Helpful Content / qualità
- [ ] 2500+ parole utili su pillar blog (no loop paragrafi uguali)
- [ ] Risposta 40–60 parole dopo ogni H2 (AEO)
- [ ] Box sintesi prime 150 parole su articoli macro
- [ ] Sezione Righetto con soluzioni operative linkate
- [ ] ≥3 foto realistiche + ≥2 SVG a tema per articolo
- [ ] Anti-doppioni: `skimm.md` + script prima di nuovo articolo

### 2.7 GEO / AI search
- [ ] `llms.txt` + `ai.json` aggiornati con nuovi URL pillar
- [ ] Frasi dichiarative auto-contenute (estraibili da AI)
- [ ] §4.4b SKILL-2.0: per Google Search, SEO standard (no farm citazioni)

### 2.8 Accessibilità (WCAG AA)
- [ ] Contrasto CTA ≥ 4,5:1 — **mai** `#FF6B35` con testo bianco
- [ ] Skip link, focus visibile, label form
- [ ] `aria-label` su CTA icon-only
- [ ] Touch target ≥ 44px su mobile

### 2.9 Spacing e UI (skill-design §13.3)
- [ ] Sezione padding mobile: 60px 20px
- [ ] Grid gap mobile: 16px
- [ ] Heading → content: 22–32px
- [ ] Content → CTA: 40px
- [ ] Coerenza `var(--*)` palette Righetto

### 2.10 Local SEO
- [ ] NAP coerente (Via Roma 96, Limena, 049.8843484)
- [ ] Pagine zona con OMI, Pro/Contro, FAQ
- [ ] Internal link blog ↔ zone ↔ servizi (min 3)

---

## 3. Punteggio target per area

| Area | Target | Script verifica |
|---|---|---|
| SEO on-page | 10/10 | `google-compliance-check.py` §2 |
| Schema | 10/10 | `validate-page.js` |
| Blog/SKIMM | 10/10 | `build_skimm.py` (0 angoli indefiniti) |
| CWV | 9–10/10 | PageSpeed Insights |
| E-E-A-T | 10/10 | author links + `righetto-sol` su **tutti** i blog (`patch_righetto_sol_blog.py`) |
| GEO | 10/10 | llms.txt + AEO box |
| A11y | 10/10 | WAVE / axe |
| Freschezza | 10/10 | `venerdi-contenuti-freschezza.py` |

**Unico gap strutturale noto (off-site):** Domain Authority / backlink — richiede PR esterno, non solo codice.

**Compliance repo (luglio 2026):** `python scripts/google-compliance-check.py` + `bash scripts/mini-seo-check.sh` + `bash scripts/audit-skill.sh` → target **100% / 0 ERR / 0 WARN** dopo batch `patch_cdn_local.py` + `patch_compliance_warns.py` + `patch_audit_warns.py`.

---

## 3b. Matrice funzionalità competitive (8/8 — zero costo aggiuntivo)

| Feature | Stato | Implementazione |
|---|---|---|
| **Blog** | OK | ~99 articoli + SKIMM + cron venerdì |
| **Zone** | OK | 14 pagine zona OMI + FAQ |
| **Chat** | OK | Linda AI (`js/chatbot.js`) |
| **Valut.** | OK | Landing + servizio valutazioni |
| **Player** | OK | `<video>` nativo homepage (`index.html` + `righetto-storia-hero.mp4`) |
| **Alert** | OK | Iscrizione alert su `immobili.html` → `newsletter_subscribers` (`interesse: alert-immobili`) |
| **Tour** | OK | Filtro «Solo tour 360°» su catalogo + tour su scheda immobile |
| **Live** | OK | CTA «Visita live» su card catalogo + scheda (`visitaLiveGuidata` / WhatsApp) |

Verifica rapida post-modifica: homepage play video, `immobili?vt=1` filtra tour, alert iscrizione, pulsante live su card.

---

## 4. Checklist venerdì — controllo completo (agente + cron)

> **Quando:** ogni venerdì, dopo le GitHub Actions (~07:00 CEST) o su richiesta «cosa fare questa settimana».  
> **Ordine:** leggere prima questa sezione, poi email/Issue `info@righettoimmobiliare.it`.

### 4.1 Automazioni già attive (non rifare a mano se OK)

| Ora (CEST) | Workflow | Output |
|---|---|---|
| 07:00 | `venerdi-contenuti-freschezza.yml` | Issue `contenuti-freschezza` + email SKIMM/pillar/5 azioni |
| 07:00 | `audit-settimanale.yml` | Issue `audit` + email audit SKILL |
| 07:00 | `mini-seo-check.yml` | Issue `seo-check` |
| 08:00 (mar+ven) | `security-check-bisettimanale.yml` | Issue `security` |

### 4.2 Comandi agente (locale — obbligatori se WARN/ERR o dopo modifiche settimana)

```bash
python scripts/google-compliance-check.py      # target: 0 ERR, 0 WARN
python scripts/venerdi-seo-intelligence.py     # PAGE SCORE + SOSTENERE/AGGIUNGERE
python scripts/patch_cdn_local.py              # CDN esterni → js/vendor/
python scripts/patch_audit_warns.py            # GA4, dateModified, OG, freshness
python scripts/build_skimm.py                  # 0 angoli indefiniti
python scripts/check_doppioni_sito.py          # prima di nuovo articolo
python scripts/venerdi-contenuti-freschezza.py # anteprima report (opzionale)
python scripts/probe_live_urls.py              # 0 issue su URL live
```

**Se compliance < 100%:**

```bash
python scripts/patch_righetto_sol_blog.py      # righetto-sol mancante
python scripts/patch_compliance_warns.py       # title/meta/geo/breadcrumb/stuffing
python scripts/google-compliance-check.py      # ri-verifica fino a 0/0
```

### 4.3 Verifica manuale rapida (5 min)

- [ ] Matrice **8/8** (`§3b`): Player, Alert, Tour, Live + Blog, Zone, Chat, Valut.
- [ ] Homepage: play video spot; `/immobili`: alert, filtro tour 360°, CTA visita live
- [ ] Issue/email venerdì: applicare **azione prioritaria #1** del report contenuti
- [ ] **Search Console** — checklist completa: **`skill-seo.md` §10** (10 URL chiave, sitemap, 404/5xx); follow-up **lunedì** se richieste manuali in corso
- [ ] **SEO Intelligence** — leggere report `venerdi-seo-intelligence-report.md` / Issue: eseguire **1× SOSTENERE** prima di nuovo articolo (**`skill-seo.md` §11**)

### 4.4 Ritmo editoriale minimo

| Frequenza | Azione |
|---|---|
| Settimanale | 1 articolo nuovo **oppure** refresh dato su articolo top traffico |
| Settimanale | Timestamp «Ultimo aggiornamento» su pillar toccati |
| Mensile | 1 refresh OMI/BCE/FIMAA su articolo mercato |
| Su segnalazione cron | `ANGLE_OVERRIDES` in `build_skimm.py` per angoli generici |

### 4.5 Unico gap off-site

Backlink / Domain Authority — PR esterno, non codice. Non blocca il deploy.

---

## 5. Priorità fix quando punteggio < 100%

1. Errori rossi `google-compliance-check.py`
2. Angoli SKIMM incompleti → `ANGLE_OVERRIDES` in `build_skimm.py`
3. Pillar senza link blog (servizi, valutazioni)
4. Articoli thin < 1500 parole (top traffico GSC)
5. Sezione Righetto mancante su pillar blog → `python scripts/patch_righetto_sol_blog.py`
6. CWV: LCP hero, font preload
7. Spacing mobile incoerente su pagine ad alto traffico

---

## 5. Collegamenti

- Dettaglio SEO: `skill-seo.md`
- Contenuti blog: `skill-content.md` + `skimm.md`
- Design/spacing: `SKILL-2.0.md` §13
- Cron venerdì: `SKILL-2.0.md` §8.1d
- Architettura: `skill-context.md`
