# Admin immobili: codice visibile, ricerca prezzo, ordinamento - 22/10/2026
Richiesta di Gino via WhatsApp (22/10/2026): codice immobile subito visibile, ricerca per proprietario/codice/indirizzo/paese/prezzo, ordinamento per paese/prezzo/superficie, clessidra ricerca proprietario piu' visibile. Solo admin.html (lista Immobili + campo proprietario), nessuna modifica al database o al sito pubblico.

- Lista Immobili: nuova colonna "Codice" (chip ben visibile) e nuova colonna "Comune"; nella colonna Immobile resta titolo + indirizzo.
- Ordinamento: click sulle intestazioni Codice, Comune, Prezzo, Superficie (freccia su/giu', secondo click inverte). Valori vuoti sempre in fondo. Ordine iniziale invariato (piu' recenti prima).
- Ricerca: oltre a titolo/codice/comune/indirizzo/proprietario (c'erano gia') cerca anche nel prezzo, confrontando solo le cifre: "285.000" o "285000" trovano il prezzo 285000.
- Campo Proprietario (Nuovo/Modifica immobile): icona ricerca/clessidra da 16px a cerchio 34px con bordo e ombra, sempre visibile in alto a destra del campo.
- Mobile: la tabella immobili scorre orizzontalmente (overflow-x) cosi' il codice resta leggibile e non si schiaccia tutto.

Test: 13 test automatici su ordinamento e ricerca (anche formato prezzo italiano) + screenshot desktop e mobile. Nessun cambio di dati: modifica solo visiva, reversibile con git revert.
- Fix in giornata: larghezza minima 250px sulla colonna Azioni, cosi' i bottoni restano su 2 righe e le righe della tabella non diventano altissime (visto su desktop 1280px: righe da ~500px a ~180px).
