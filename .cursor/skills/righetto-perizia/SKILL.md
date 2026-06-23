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

## Struttura PDF (3 pagine)

1. **Relazione** — logo, data incorniciata, riepilogo proprietario/tipologia/mq/valore, sezioni 1–3, box valore €, blocco contatti, note legali in calce (no pagine vuote)
2. **Planimetrie** — composito piano terra + piano primo, stessa larghezza, senza buchi
3. **Prospetti** — EST e OVEST, elevazioni affiancate in orizzontale + note limiti

## Script

```bash
python scripts/genera_perizia_turato.py
```

Output default: `documenti/Perizia_<Cognome>_<Tipologia>.pdf`

Dipendenze: `pymupdf`, `reportlab`, `pillow`

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

- `scripts/genera_perizia_turato.py` — generatore attuale (da generalizzare con JSON config)
- `documenti/anteprima-perizia-righetto.html` — anteprima HTML layout v2
