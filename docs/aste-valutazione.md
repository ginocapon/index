# Aste Veneto: valutazione Scartato / Interessante (2026-10-20)

- Nuova colonna "Valutazione" (tendina: da valutare / Interessante / Scartato) con data della scelta.
- Interessante: riga gialla (#FFEB00). Scartato: riga nascosta (resta nel database, il sync non la reimporta); pulsante "Mostra scartate" per rivederle.
- Data asta evidenziata (pillola blu); su telefono (<700px) data e tendina nella cella del comune.
- Database: sql/aste-valutazione.sql (colonne valutazione, valutazione_data), undo sql/aste-valutazione-undo.sql. Eseguito da Gino il 2026-10-20.
- Backup: branch e tag backup-pre-aste-valutazione. Per tornare indietro: git revert del commit.
- File toccati: admin.html (intestazioni tabella, cache js v=2), js/admin-aste.js.
