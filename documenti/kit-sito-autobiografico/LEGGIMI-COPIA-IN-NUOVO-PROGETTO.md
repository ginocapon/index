# Kit skill — sito autobiografico (copia nel nuovo progetto)

## Cosa contiene

Cartella completa con regole per Cursor/Claude: SEO, GEO, blog, mobile, Google Search Console, GBP.

**Adatto a:** sito personale + storia + palestra/attività + blog + contatti.

---

## Come installare (5 minuti)

1. Copia **tutto** il contenuto di `kit-sito-autobiografico/` nella **root** del nuovo repo.
2. Struttura risultante:

```
nuovo-progetto/
├── SKILL-2.0.md              ← indice (leggere sempre)
├── CLAUDE.md
├── TEST-SKILL/
│   ├── skill-essentials.md
│   ├── skill-massimo-punteggio.md
│   ├── skill-seo.md
│   ├── skill-content.md
│   ├── skill-design.md
│   ├── skill-forms-contatti.md
│   ├── skill-social-gbp.md
│   ├── skill-cursor-rules.md
│   └── context-map.json
├── .cursor/
│   ├── rules/
│   │   ├── core.mdc
│   │   ├── vanilla-ui.mdc
│   │   └── blog-seo.mdc
│   └── skills/
│       ├── core-task/SKILL.md
│       ├── blog/SKILL.md
│       ├── seo/SKILL.md
│       ├── mobile/SKILL.md
│       ├── venerdi/SKILL.md
│       └── chi-sono/SKILL.md
└── data/
    ├── gsc-indexing-weekly.json
    ├── gsc-keywords-priority.json
    └── editorial-queue.json
```

3. Apri `TEST-SKILL/skill-essentials.md` → compila **§ CLAIM E DATI**.
4. In Cursor: le rule `core.mdc` si attivano da sole (`alwaysApply: true`).

---

## Slash command in chat Cursor

| Comando | Uso |
|---------|-----|
| `/sito` | Modifiche generiche al sito |
| `/seo` | Audit meta, schema, GSC |
| `/blog` | Nuovo articolo |
| `/mobile` | Fix iPhone / responsive |
| `/venerdi` | Checklist settimanale Google |
| `/chi-sono` | Pagina biografica / storia |

---

## Prima modifica nel nuovo progetto

Chiedi in chat:

> Leggi SKILL-2.0.md e skill-essentials.md. Compila i placeholder […] con i miei dati: [incolla nome, città, dominio].

---

*Kit generato da workflow Righetto Immobiliare — luglio 2026.*
