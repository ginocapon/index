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

## Pacchetto admin 21/10/2026 (commit bb6162a1 + c7acd41d, push ore 10:40)
- **Foto sopralluogo di Gino** (bb6162a1): box drag&drop/click nel dettaglio asta, upload nel bucket privato aste-pratica/sopralluogo/, anteprime con link firmati, rimozione logica dalla scheda. Richiede i 2 passi SQL di Gino: colonna `foto_sopralluogo` (passo 1) + policy insert `foto_sopralluogo_upload` (passo 2). Finche' non li esegue il box non carica.
- **Testo +20% pannello espanso** (c7acd41d): `zoom:1.2` solo sul contenuto del dettaglio aperto; tabella invariata.
- **Mappa OSM aste Interessanti** (c7acd41d): bottone "🗺 Mappa interessanti", Leaflet 1.9.4 + tile OpenStreetMap (gratuite), spilli SVG locali con capocchia rossa stile 3D solo per valutazione "interessante" in tutto il Veneto; tooltip comune/indirizzo/prezzo/data, click apre la riga. Coordinate dai campi `latitudine`/`longitudine` gia' scritti dal sync (nessuno SQL nuovo).
- Backup: branch `backup/pre-push-20261021-admin-aste`, tag `backup-admin-aste-20261021` (entrambi su origin).
- Verifica live 10:42: `js/admin-aste.js` e `admin.html` su righettoimmobiliare.it contengono astePinIcon, zoom:1.2, asteMapWrap/asteMapBtn.
- Device flow GitHub: primo codice 1F41-1466 scaduto per errore procedurale (token perso prima del push); secondo codice 9A8D-46A5 autorizzato da Gino ore 10:40, push immediato, token non salvato su disco.
