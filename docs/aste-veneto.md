# Aste immobiliari Veneto — pagina admin + sync (2026-10-16)

## Cosa cambia
- Nuova sezione admin "Aste Veneto" (menu + `sec-aste` in `admin.html`, logica in `js/admin-aste.js`): elenco aste residenziali Veneto con filtri (testo, provincia, prezzo max, data), ordinamento per colonna, dettaglio con documenti (link ufficiali PVP), foto (se disponibile), note private admin.
- Tabella Supabase `aste_immobili` (`sql/aste-immobili.sql`, undo `sql/aste-immobili-undo.sql`): RLS admin-only via `righetto_is_admin_request()`, nessuna policy pubblica. SQL lanciato da Gino.
- `scripts/sync_aste.py` + `.github/workflows/sync-aste.yml` (cron 05:45/17:45 UTC + manuale): legge il Portale delle Vendite Pubbliche (JSON anonimo: ricerca `ric-ms/ricerca/vendite`, dettaglio `ve-ms/vendite/{id}/restricted`), filtra `IMMOBILE_RESIDENZIALE`, upsert su Supabase (service_role da secret), disattiva le aste non più in scadenza. Foto principale da astegiudiziarie.it quando disponibile. Gli hash dei microservizi PVP vengono risolti a runtime (cambiano a ogni deploy del portale).
- Documenti (perizie/planimetrie/avvisi): restano link diretti a resource-pvp.giustizia.it. Niente copia ospitata: repo pubblico inadatto (privacy), Supabase free 1 GB insufficiente (~3,6 GB). Previsto repo privato ginocapon/aste-docs per l'archivio PDF (seconda fase).

## Fonti dati
- pvp.giustizia.it (Ministero), uso read-only dei dati pubblici; foto da astegiudiziarie.it.
- Privacy: perizie con dati personali dei debitori → tutto solo in admin, mai su pagine pubbliche.

## Verifica
- Dry-run end-to-end dello script ok (16/10): 593 immobili Veneto in scadenza, 323 residenziali.
- Preview locale della sezione renderizzata e verificata con screenshot (desktop).
