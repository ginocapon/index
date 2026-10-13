# Provenienza richieste per pagina - 13/10/2026

Obiettivo: poter distinguere da quale pagina arriva ogni riga della tabella `richieste`.

Situazione trovata
- Form del sito (js/rig-lead-form.js): scrivono gia' la pagina in `provenienza`; se il database rifiuta (vincolo richieste_provenienza_check) ripiegano su `form` e mettono `[fonte: pagina]` nel messaggio.
- Chatbot (js/chatbot.js): scriveva solo `chatbot`, nessuna pagina, e non controllava l'errore di salvataggio.
- landing-costi-locazione-inquilino.html: nessun ripiego, richiesta persa nel database se la provenienza veniva rifiutata (restava la mail).

Modifiche
- Chatbot: messaggio salvato come `[fonte: chatbot @ /pagina] testo`; provenienza resta `chatbot`; ora legge l'errore di salvataggio.
- landing-costi-locazione-inquilino: stesso ripiego delle altre form.
- Nessuna modifica al database. Nessun cambiamento visibile.

Annullare: ripristinare dal backup (branch/tag `backup-pre-provenienza-20261013`, commit a8b41d0) oppure `git revert` del commit.
Dato di partenza: 30 gg al 13/10/2026 = form-vendita 1, chatbot 2 (pagina non nota).
