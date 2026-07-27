---
name: righetto-perizia
description: >-
  Genera perizie immobiliari PDF Righetto Immobiliare con logo, brand, planimetrie
  e prospetti. Usa quando l'utente chiede perizia, stima immobiliare, relazione di
  valutazione, valutazione per proprietario o «facciamo perizia».
---

# Perizia immobiliare Righetto — template v2

## Quando attivare

- «Facciamo perizia», «perizia per…», «relazione di stima», «valutazione immobile»
- PDF con planimetrie/prospetti allegati per un proprietario

## Anteprima layout

Apri nel browser: `documenti/anteprima-perizia-righetto.html`

## Contatti (sempre nel documento)

| Campo | Valore |
|-------|--------|
| Sede | Via Roma n.96 — 35010 Limena (PD) |
| Tel | **049.8843484** (`tel:+390498843484`) |
| Cell | 349 736 5930 |
| Email | info@righettoimmobiliare.it |
| Web | righettoimmobiliare.it |
| P.IVA | 05182390285 |

Formato tel in PDF/footer: `049.8843484` oppure `049.8843484` (equivalenti).

## Brand visivo

- Logo: `img/brand/logo-righetto-ri.png`
- Colori: `#152435` nero · `#2C4A6E` blu · `#FF6B35` oro · `#ECE7DF` sfondo
- Cornice blu + barra oro in alto + footer nero su ogni pagina

## Struttura PDF (4–6 pagine)

1. **Relazione** — logo, data, riepilogo, sezioni 1–4 (oggetto, catasto, stato, urbanistico)
2. **Valutazione** — considerazioni commerciali, box valore €, forchette, contatti agenzia
3. **Allegato A** — planimetria catastale (PDF)
4. **Allegato B** — visura / scheda catastale
5. **Allegato C** — vista aerea (opzionale)
6. **Note legali** — disclaimer in calce ultima pagina

## Script

```bash
# Nuovo formato JSON (consigliato — luglio 2026)
python scripts/genera_perizia.py scripts/perizia_config_ragazzo_curtarolo.json

# Legacy monolitico
python scripts/genera_perizia_turato.py
```

Output: `documenti/Perizia_<Nome>.pdf` + copia in `Downloads/`

Dipendenze: `pymupdf`, `reportlab`, `pillow`

## Config JSON (template riutilizzabile)

Copiare e adattare un file `scripts/perizia_config_<cognome>.json`:

| Campo | Obbligatorio | Descrizione |
|-------|--------------|-------------|
| `output_nome` | sì | Nome file PDF in `documenti/` |
| `data` | sì | ISO `YYYY-MM-DD` |
| `proprietario` | sì | Intestatario / erede |
| `proprietario_dettaglio` | no | Nascita, CF, visura |
| `tipologia` | sì | Es. porzione bifamiliare |
| `ubicazione` | sì | Indirizzo completo |
| `superficie_commerciale` | sì | mq |
| `valore_principale` | sì | € partenza / stima |
| `valore_secondario` | no | Forchetta prudenziale testo |
| `valore_conservativo` | no | Scenario peggiore |
| `catasto` | sì | `unita[]` sub/cat/consistenza/rendita |
| `caratteristiche` | no | Elenco bullet |
| `criticita_urbanistiche` | no | Elenco |
| `attivita_prioritarie` | no | Elenco |
| `allegati.planimetria_catastale` | no | Path PDF planimetria |
| `allegati.scheda_catastale` | no | Path PDF visura |
| `allegati.vista_aerea` | no | Path JPG/PNG satellite |

Esempi config: `perizia_config_turato.json`, `perizia_config_ragazzo_curtarolo.json`

## Dati da chiedere se mancanti

1. Proprietario (es. Sig. Turato Antonio)
2. Tipologia immobile
3. Valore stimato €
4. Superficie commerciale (mq) + tabella calcolo se disponibile
5. PDF planimetrie/prospetti (path file)
6. Data perizia (default: oggi)

## Regole impaginazione (apprese da feedback)

- **Mai** lasciare pagine quasi vuote: note legali vanno in calce pagina prospetti con `KeepTogether`
- Planimetrie/prospetti: ruotare da verticale a orizzontale, ritagliare bordi bianchi
- Prospetti: splittare e affiancare le due elevazioni
- Compositi verticali alla stessa larghezza per riempire la pagina
- Logo sempre in header pagina 1

## Disclaimer obbligatorio

> La presente stima ha carattere indicativo e non sostituisce una perizia tecnico-giuridica redatta da perito abilitato.

## File correlati

- `scripts/genera_perizia.py` — **generatore JSON** (consigliato)
- `scripts/genera_perizia_turato.py` — legacy monolitico
- `scripts/perizia_config_*.json` — dati per immobile
- `documenti/anteprima-perizia-righetto.html` — anteprima HTML layout v2
