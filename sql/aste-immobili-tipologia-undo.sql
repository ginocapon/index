-- Annulla aste-immobili-tipologia.sql: toglie la colonna "tipologia" dalla tabella aste.
alter table public.aste_immobili drop column if exists tipologia;
