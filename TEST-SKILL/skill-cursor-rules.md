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
| **`.cursor/rules/*.mdc`** | **Trigger automatici** Cursor per file aperti — estratto actionable, zero duplicazione massiva |
| **`CLAUDE.md`** | Entry point per agenti Claude/Cursor |

Le `.mdc` **non sostituiscono** la skill: la **indirizzano** e applicano guardrail quando lavori su file specifici.

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

## 3. Routing task → skill + rule

Allineato a `context-map.json`:

| Task | Skill da caricare | Rule Cursor (hint) |
|------|-------------------|-------------------|
| Nuovo articolo blog | essentials + content + forms (se CTA) | `righetto-blog-publish` |
| Nuova landing | essentials + forms + design + context | `righetto-forms-leads` + `righetto-vanilla-ui` |
| Fix CSS / homepage | essentials + design | `righetto-vanilla-ui` |
| Audit SEO | essentials + seo | `righetto-seo-geo` |
| Social cron | essentials + social-automation | `righetto-social-automation` |
| RLS / admin / foto annunci | essentials + context + **media-migration** | `righetto-supabase-admin` |
| Sync media / egress Supabase | essentials + **media-migration** | `righetto-supabase-admin` |
| Audit sicurezza (2×/sett.) | essentials + security | `righetto-supabase-admin` |

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
