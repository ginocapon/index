# Strategia Nord Star — acquisizione 12 mesi

> **Aggiornato:** 9 ottobre 2026  
> **Dati:** `data/strategy-nord-star-12m-acquisizione.json`  
> **KPI settimanali:** `data/acquisition-kpi-template.json`  
> **Cron:** `skill-acquisizione-cron-venerdi.md` · `data/venerdi-friday-pipeline.json`

## Scopo

Allineare **acquisizione proprietari**, **contenuti botte/cerchio** e **esecuzione commerciale** a un obiettivo di margine netto a 12 mesi, con **tolleranza massima ±1%** sui KPI operativi settimanali (lead, sopralluoghi, mandati) — non su previsioni di mercato non verificate.

**Regola d'oro:** nessun dato economico inventato online; compenso mediazione solo in sede.

## Quattro pilastri (riorganizzazione)

| ID | Pilastro | Output misurabile |
|----|----------|-------------------|
| P1 | Acquisizione A–L | 1 task repo/venerdì (`acquisition-roadmap-cron.json`) |
| P2 | Botte / cerchio | 1 blog o refresh CTA + mesh hub GSC |
| P3 | Funnel Class A | CTA verso `landing-valutazione`, `servizio-vendita`, `servizio-locazioni`, `landing-consulenza` — non solo `contatti` |
| P4 | Commerciale | Lead giorno 0 + `acquisition-kpi-template.json` ogni venerdì |

## Formula (compilazione obbligatoria in agenzia)

```
Margine_12m ≈ (Mandati_vendita × Margine_netto_medio_vendita)
            + (Mandati_locazione/gestione × Margine_netto_medio_locazione)
```

Per avvicinarsi a **1.000.000 € netti** in 12 mesi:

1. Inserire in JSON `baseline_net_margin_eur_last_12m` e `avg_net_margin_per_mandate_eur` (registro interno).
2. Calcolare `mandates_needed = ceil((target - altri_ricavi) / avg_net_margin_per_mandate_eur)`.
3. Deragare a **mandati/mese** e **lead/mese** usando `conversion_rates` storici (non inventati).

## Prospetti (aggiornare ogni venerdì)

Modificare `prospetti_12m` in `strategy-nord-star-12m-acquisizione.json`:

- **scenario_base** — trend se si mantiene il ritmo KPI attuale
- **scenario_upside** — se migliora lead→sopralluogo o sopralluogo→mandato
- **scenario_risk** — colli di bottiglia (es. task cron pending, GSC, risposta lenta)
- **actions_this_week** — max 3 azioni verificabili

## Integrazione cron venerdì

1. **Fase 0:** leggi `strategy-nord-star-12m-acquisizione.json` + settimana acquisizione N.
2. **Slot #1–#3** come da pipeline.
3. **Chiusura:** aggiorna `acquisition-kpi-template.json`, `prospetti_12m.actions_this_week`, log in `skill-memoria-progressi.md`.

## Cursor skill

Indice operativo: `.cursor/skills/righetto-acquisizione-proprietari/SKILL.md` — sezione Nord Star 12m.

## Fascia alta e investitori (≥300k · 4 mandati/mese)

**Dati operativi:** `data/pipeline-acquisizioni-fascia-alta.json`

| Obiettivo | Valore |
|-----------|--------|
| Nuovi mandati vendita / mese | **min 4** |
| Prezzo immobile target | **≥ 300.000 €** (asking o valutazione) |
| Segmenti prioritari | Centro Storico Padova, ville, patrimonio / investitori |
| Stock catalogo ≥300k (snapshot) | 6 annunci — aggiornare da `og-immobili.json` |

**Percorsi sito:** `valutazione-vendita-riservata-padova` · `segnalazione-immobili-professionisti-padova` · `zona-centro-storico-padova` · `servizio-vendita` · `servizio-valutazioni`.

**Lead scoring:** segnali `price_band_300k_plus`, `investor_buyer`, `off_market_request` in `data/lead-scoring-rules.json`.

## Vietato

- Pubblicare tariffe, percentuali o promesse di guadagno sul sito
- Fissare previsioni €/mq o volumi mercato senza OMI/FIMAA/ISTAT
- Trattare 1M€ come claim marketing — solo obiettivo interno + KPI
