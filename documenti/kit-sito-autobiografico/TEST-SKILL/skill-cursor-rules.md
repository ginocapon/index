# SKILL-CURSOR-RULES — Regole agente Cursor

> Architettura: TEST-SKILL = fonte verità · .cursor/rules = trigger automatici · .cursor/skills = slash command

---

## 1. Layer

| Layer | Ruolo |
|-------|--------|
| `SKILL-2.0.md` | Indice |
| `TEST-SKILL/skill-*.md` | Moduli completi |
| `context-map.json` | Routing task → skill |
| `.cursor/skills/*/SKILL.md` | Indici operativi (/seo, /blog…) |
| `.cursor/rules/*.mdc` | Regole auto su file aperti |

---

## 2. Regole Cursor

| File | alwaysApply | Si attiva su |
|------|-------------|--------------|
| `core.mdc` | **true** | Ogni sessione |
| `vanilla-ui.mdc` | false | `*.html`, `css/**`, `js/**` |
| `blog-seo.mdc` | false | `blog-*`, `sitemap.xml`, `llms.txt` |

---

## 3. Cursor Skills + slash

| Skill | Command | Moduli TEST-SKILL |
|-------|---------|-------------------|
| `core-task` | `/sito` | essentials + massimo-punteggio |
| `seo` | `/seo` | seo + massimo-punteggio |
| `blog` | `/blog` | content + essentials |
| `mobile` | `/mobile` | design |
| `venerdi` | `/venerdi` | seo + content |
| `chi-sono` | `/chi-sono` | content + seo |

---

## 4. Routing task → skill

Vedi `context-map.json`. Regola: **essentials + massimo-punteggio sempre**, poi modulo specifico.

---

## 5. Manutenzione kit

Nuova regola operativa → prima `TEST-SKILL/skill-*.md`, poi estratto in `.cursor/skills/` se cambia workflow.
