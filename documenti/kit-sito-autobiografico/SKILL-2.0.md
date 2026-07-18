# SKILL-2.0 — Indice sito autobiografico

> **Fonte di verità** del progetto. L'agente legge questo file **prima** di ogni operazione.  
> Testo completo nei moduli `TEST-SKILL/skill-*.md`.

---

## 1. Tipo di sito

Sito **autobiografico**: persona + storia + attività (es. palestra) + contatti + blog opzionale.

**Pagine tipiche:** Home · Chi sono · La mia storia · Palestra/Attività · Contatti · Blog

---

## 2. Moduli skill (routing)

| Task | File da leggere |
|------|-----------------|
| **Sempre** | `skill-essentials.md` + `skill-massimo-punteggio.md` |
| SEO / GSC / schema | `skill-seo.md` |
| Blog / testi | `skill-content.md` |
| CSS / mobile | `skill-design.md` |
| Form contatti | `skill-forms-contatti.md` |
| Google Maps / social | `skill-social-gbp.md` |
| Regole Cursor | `skill-cursor-rules.md` |
| Routing automatico | `context-map.json` |

---

## 3. Regola d'oro

**Se non hai fonte verificabile, NON inserire il dato.**  
Niente «miglior», «numero 1», percentuali risultati inventate.

---

## 4. Stack (personalizza una volta)

Default consigliato:
- HTML / CSS / JS **vanilla**
- Hosting: [GitHub Pages / Netlify / altro]
- **Zero CDN esterni** (font/script locali)
- URL interne coerenti (con o senza `.html`, ma **uniformi**)
- Dominio canonico: **apex o www — uno solo**

---

## 5. Checklist universale (ogni modifica)

1. Leggi il file da modificare
2. Mobile-first (375px)
3. Title ≤60 (max 70), meta 120–155 (max 160)
4. CSS/JS con `?v=N` incrementato
5. Nuova pagina → `sitemap.xml`
6. Commit se richiesto; push solo se esplicito
7. No DNS/hosting senza conferma utente

---

## 6. Cursor Skills

Slash: `/sito` `/seo` `/blog` `/mobile` `/venerdi` `/chi-sono`  
Indici: `.cursor/skills/*/SKILL.md`  
Rule sempre attiva: `.cursor/rules/core.mdc`

---

## 7. Dati da tenere aggiornati

- `data/gsc-indexing-weekly.json` — venerdì, Search Console
- `data/gsc-keywords-priority.json` — query Google
- `data/editorial-queue.json` — prossimi articoli blog

---

## 8. Documentazione utente semplice

Per spiegazioni in italiano facile: `GUIDA-SITO-AUTOBIOGRAFICO.md` (opzionale, stesso kit o `documenti/` Righetto).
