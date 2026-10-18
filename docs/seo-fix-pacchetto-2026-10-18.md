# Pacchetto modifiche 18 ottobre 2026 (anticipato da lunedi 20)

Richiesta di Gino (WhatsApp 18/10 10:09): fare subito il pacchetto, non sommare al lavoro sicurezza di lunedi.
Fonte strategia: report "strategia-ingressi-righetto-2026-10-18.pdf" (confronto siti piu visitati, inviato per mail il 18/10).
Backup: tag `backup-pre-pacchetto-20261018`. Branch: `pacchetto-2026-10-18`. Tutte le modifiche sono testo/aggiunte piccole, reversibili dal tag.

## Modifiche

1. **Date "Ultimo aggiornamento" obsolete: Marzo 2026 -> Ottobre 2026**
   - URL: /landing-valutazione, /agenzia-immobiliare-padova, /servizio-gestione, /servizio-utenze, /landing-chat-vendita
   - /servizi: "Contenuti: Marzo 2026" -> "Contenuti: Ottobre 2026"
   - Perche: una data vecchia fa sembrare la pagina trascurata (verificato leggendo le pagine). Pagine rilette oggi.
   - NON toccato: /index riga mutuo "tasso aggiornati a Marzo 2026" (e' un dato di mercato, non una data di revisione: serve verifica dei tassi reali).

2. **Home: riga sotto i pulsanti principali** — "3 passi · 2 minuti · risposta entro 24 ore" (classe .hero-cta-note)
   - URL: /index
   - Perche: Casavo scrive i tempi di ogni passo in home; la risposta entro 24 ore e' gia' promessa sia su /landing-valutazione sia su /servizio-valutazioni ("Rispondiamo entro 24 ore"). Ipotesi effetto medio-alto (fonte: report 18/10).

3. **Modulo valutazione: nuova opzione "Voglio affittare / mettere a reddito"** nel campo "Perche vuoi la valutazione?" (step 2)
   - URL: /landing-valutazione
   - Perche: prima c'erano solo motivi di vendita; Gabetti separa vendita/affitto come prima scelta. Strada affitto = incarichi locazione.

4. **Guida affitto studenti: secondo bottone nella CTA finale** — "Quanto posso chiedere di affitto? ->" verso /landing-valutazione
   - URL: /blog-affitto-studenti-padova
   - Perche: la guida studenti e' tra le migliori occasioni in Search Console (baseline 10/10) ma mandava solo a servizio-locazioni; la guida rendimento aveva gia' il bottone valutazione.

## Da decidere con Gino (NON applicato)
- Tempo promesso: /landing-valutazione dice "report in 24 ore", /servizio-valutazioni dice "sopralluogo entro 48h, report in 24-48h dal sopralluogo". Serve la versione vera, poi si uniforma. Coinvolge anche la variante B dell'A/B test home ("Valutazione gratuita in 24h", js/lead-conversion.js) e la meta description di /landing-vendere-casa-padova.

## Misurazione
KPI: visite (GSC 7/28 gg) sulle pagine toccate, dal lunedi successivo alla pubblicazione. Una modifica alla volta non e' possibile in un pacchetto unico: si misura l'effetto complessivo per pagina.

Data intervento: 18/10/2026. Stato: PREPARATO, in attesa di ok di Gino e codice GitHub. NON pubblicato.
