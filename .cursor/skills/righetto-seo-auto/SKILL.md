---
name: righetto-seo-auto
description: >-
  Ciclo SEO automatico settimanale Righetto (venerdì 08:00): dati Search Console
  via API/CSV, selezione max 10 pagine con punteggio, interventi approvati con
  backup e rollback, registro storico, verifica online, valutazione, dashboard e
  report A–H. Usa quando l'utente chiede SEO automatico, ciclo GSC, quali pagine
  aggiornare, approvare proposte SEO, rollback di un intervento o report SEO settimanale.
---

# SEO automatico settimanale

**Fonte completa:** `TEST-SKILL/skill-seo-auto-weekly.md` (leggere prima di agire) + `TEST-SKILL/skill-seo.md` + `TEST-SKILL/skill-acquisizione-proprietari.md`.

## Comandi

```bash
python3 scripts/seo_auto/seo_auto.py weekly
python3 scripts/seo_auto/seo_auto.py apply [--id SEO-AAAAWss-slug]
python3 scripts/seo_auto/seo_auto.py verify      # dopo il deploy di Pages
python3 scripts/seo_auto/seo_auto.py rollback --id SEO-AAAAWss-slug
```

## Flusso con l'utente

1. Leggi `data/seo-auto/selection-latest.json` e l'ultimo `reports/*.md`.
2. Proponi gli interventi (op atomiche, testo esatto, motivazione, rischio).
3. Solo dopo l'«ok» esplicito scrivi `data/seo-auto/approvals.json` (`approved_by`, `approved_on`), poi `apply` e infine commit.
4. Dopo il deploy: `verify`. Non dichiarare un miglioramento senza almeno 28 giorni di dati API reali.

## Vincoli

- Nessun dato simulato: se `stale: true`, dirlo nel report e nell'oggetto dell'email.
- Niente riscritture del corpo, niente claim senza fonte, niente redirect o canonical tra pagine owner senza dati di query.
- Pagine owner prima di tutto (north star: ≥4 mandati al mese ≥300k).
