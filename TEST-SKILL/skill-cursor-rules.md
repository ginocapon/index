# SKILL-CURSOR-RULES — Righetto Immobiliare

> Architettura regole Cursor (formato `.mdc` scoped) — **Maggio 2026**  
> Ispirata al pattern [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules): regole sottili in `.cursor/rules/`, **fonte di verità** resta `TEST-SKILL/*`.

---

## 1. Principio

| Layer | Ruolo |
|-------|--------|
| **`TEST-SKILL/SKILL-2.0.md`** | Manuale operativo completo (SEO, blog, architettura, checklist) |
| **`TEST-SKILL/skill-*.md`** | Moduli caricati per task (content, seo, design, forms, social…) |
| **`TEST-SKILL/context-map.json`** | Routing: quale skill per quale task |
| **`.cursor/skills/*/SKILL.md`** | **Indice operativo** Cursor — trigger + checklist breve → punta a `TEST-SKILL/` |
| **`.cursor/commands/*.md`** | **Slash command** in chat (`/blog`, `/landing`…) — wrapper verso le skill |
| **`.cursor/rules/*.mdc`** | **Trigger automatici** Cursor per file aperti — estratto actionable, zero duplicazione massiva |
| **`CLAUDE.md`** | Entry point per agenti Claude/Cursor |

Le `.mdc` **non sostituiscono** la skill: la **indirizzano** e applicano guardrail quando lavori su file specifici.  
Le **Cursor Skills** (`.cursor/skills/`) **non duplicano** `TEST-SKILL/`: dicono all'agente *quando* e *quali moduli* caricare.

---

## 2. Mappa regole Cursor

| File `.mdc` | `alwaysApply` | Si attiva su | Skill di riferimento |
|-------------|---------------|--------------|----------------------|
| `righetto-core.mdc` | **true** | Ogni sessione | `skill-essentials.md`, `context-map.json` |
| `righetto-vanilla-ui.mdc` | false | `*.html`, `css/**`, `js/**` | `skill-design.md` |
| `righetto-blog-publish.mdc` | false | `blog-*.html`, `scripts/**` | `skill-content.md`, §8.1a/8.1c |
| `righetto-forms-leads.mdc` | false | `landing-*`, form, `rig-lead-form.js` | `skill-forms-leads.md` |
| `righetto-social-automation.mdc` | false | `righetto_social/**` | `skill-social-automation.md` |
| `righetto-seo-geo.mdc` | false | `zona-*`, `sitemap.xml`, `llms.txt` | `skill-seo.md` |
| `righetto-supabase-admin.mdc` | false | `sql/**`, `admin.html`, `scripts/sync_media*.py`, `scripts/migrate_supabase_media.py`, `scripts/purge_supabase*.py` | `skill-context.md`, **`skill-media-migration.md`** |

**Deprecato:** `righetto-seo-2026.mdc` → sostituito da `righetto-blog-publish.mdc` + `righetto-seo-geo.mdc`.

---

## 2b. Cursor Skills + Commands (luglio 2026)

| Skill progetto | Command `/` | Trigger utente | Moduli `TEST-SKILL/` |
|----------------|-------------|----------------|----------------------|
| `righetto-core-task` | `/sito` | task generico sul sito | essentials + massimo-punteggio |
| `righetto-blog` | `/blog` | nuovo articolo, blog su… | content + skimm + forms (se CTA) |
| `righetto-landing` | `/landing` | landing, form lead, conversione | forms-leads + design + context |
| `righetto-fix-mobile` | `/mobile` | iPhone, mobile, responsive rotto | design |
| `righetto-immobili-admin` | `/immobili` | foto admin, tour 360°, sync | media-migration + context |
| `righetto-venerdi-sito-90giorni` | `/venerdi` | piano settimanale, venerdì, 90 giorni | essentials + seo + content |
| `righetto-perizia` | `/perizia` | perizia PDF, stima immobile | — (script `genera_perizia_*.py`) |
| `righetto-seo` | `/seo` | audit SEO, meta, schema, GSC, PAGE SCORE | seo + massimo-punteggio |
| `righetto-social` | `/social` | bozze Meta/IG/GBP, copy post/reel | social-automation |
| `righetto-security` | `/sicurezza` | audit sicurezza 2×/sett, RLS, admin | security + context |
| `righetto-zona` | `/zona` | scheda zona, quartiere, SEO locale | content + seo |

Percorsi: `.cursor/skills/<nome>/SKILL.md` · `.cursor/commands/<nome>.md`

**Manutenzione:** regola operativa nuova → prima `TEST-SKILL/skill-*.md`, poi estratto in `.cursor/skills/` se cambia il workflow.

---

## 3. Routing task → skill + rule

Allineato a `context-map.json`:

| Task | Cursor Skill | Skill da caricare | Rule Cursor (hint) |
|------|--------------|-------------------|-------------------|
| Nuovo articolo blog | `righetto-blog` | essentials + content + forms (se CTA) | `righetto-blog-publish` |
| Nuova landing | `righetto-landing` | essentials + forms + design + context | `righetto-forms-leads` + `righetto-vanilla-ui` |
| Fix CSS / mobile | `righetto-fix-mobile` | essentials + design | `righetto-vanilla-ui` |
| Audit SEO / meta / schema | `righetto-seo` | essentials + seo + massimo-punteggio | `righetto-seo-geo` |
| Nuova / update zona | `righetto-zona` | essentials + content + seo | `righetto-seo-geo` |
| Piano venerdì | `righetto-venerdi-sito-90giorni` | essentials + seo + content | `righetto-blog-publish` |
| Social cron / copy post | `righetto-social` | essentials + social-automation | `righetto-social-automation` |
| RLS / admin / foto annunci | `righetto-immobili-admin` | essentials + context + **media-migration** | `righetto-supabase-admin` |
| Sync media / egress Supabase | `righetto-immobili-admin` | essentials + **media-migration** | `righetto-supabase-admin` |
| Audit sicurezza (2×/sett.) | `righetto-security` | essentials + security + context | `righetto-supabase-admin` |

---

## 4. Manutenzione

1. **Modifica operativa** → aggiorna prima `TEST-SKILL/skill-*.md` o `SKILL-2.0.md`.
2. **Estratto in `.mdc`** → solo checklist brevi e link al modulo; max ~40 righe per file.
3. **Nuovo dominio** (es. nuovo canale marketing) → nuovo `skill-*.md` + voce in `context-map.json` + `.mdc` con `globs` mirati.
4. **Non** copiare rule generiche React/Next da awesome-cursorrules — stack Righetto è vanilla static.

---

## 5. Contributo esterno (opzionale)

Il repo potrebbe contribuire a awesome-cursorrules una rule **"Static HTML Real Estate SEO — Italy, vanilla JS, Supabase leads"** come riferimento di nicchia. Non prioritario per visibilità cliente.

---

## 6. Automazioni collegate

- Pre-commit: `scripts/validate-page.js`
- Anti-doppioni: `scripts/check_doppioni_sito.py`
- Audit venerdì: `.github/workflows/audit-settimanale.yml`, `mini-seo-check.yml`
- **Sync foto annunci:** `.github/workflows/sync-media-github.yml` (ogni 6 h) — vedi `skill-media-migration.md`

Dettaglio automazioni: `context-map.json` → `automazioni_attive`.
