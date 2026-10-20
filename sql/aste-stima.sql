-- Aggiunge a ogni asta il "prezzo di vendita stimato" (forbice + fonte + data),
-- mostrato in rosso nella pagina admin Aste, sia su PC sia su telefono.
-- La stima la compila Gianna dopo ogni import, SOLO per le aste in provincia di Padova.
-- Non tocca nessun dato esistente. Si annulla con sql/aste-stima-undo.sql
alter table public.aste_immobili add column if not exists prezzo_stimato_min numeric(12,2);
alter table public.aste_immobili add column if not exists prezzo_stimato_max numeric(12,2);
alter table public.aste_immobili add column if not exists prezzo_stimato_fonte text not null default '';
alter table public.aste_immobili add column if not exists prezzo_stimato_data date;
