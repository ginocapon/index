-- Aggiunge a ogni asta la scelta "Scartato / Interessante" e la data della scelta.
-- Non tocca nessun dato esistente. Si annulla con sql/aste-valutazione-undo.sql
alter table public.aste_immobili add column if not exists valutazione text
  check (valutazione in ('interessante','scartato'));
alter table public.aste_immobili add column if not exists valutazione_data timestamptz;
