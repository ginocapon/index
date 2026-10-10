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

**Delega venerdì attiva (dal 10/10/2026):** quando Gino carica i dati GSC, esegui senza chiedere un altro ok (procedura in §6.1 della skill completa).

1. Export in `data/seo-auto/inbox/` → `weekly` → leggi `selection-latest.json` e il report.
2. Per ogni pagina scegli la leva minima legata al dato: title e meta, link, refresh del testo con fonti.
3. Scrivi `approvals.json` (`approved_by: "delega venerdì 10/10/2026"`) → `apply` → validazioni → commit e push → `verify`.
4. Fuori dalla delega (chiedi prima): URL, redirect, canonical, noindex, eliminazioni, form, nuovi articoli, tariffe.
5. Non dichiarare un miglioramento senza almeno 28 giorni di dati reali.

## Vincoli

- Nessun dato simulato: se `stale: true`, dirlo nel report e nell'oggetto dell'email.
- Niente riscritture del corpo, niente claim senza fonte, niente redirect o canonical tra pagine owner senza dati di query.
- Pagine owner prima di tutto (north star: ≥4 mandati al mese ≥300k).
