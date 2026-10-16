-- Aggiunge la colonna "tipologia" (appartamento, casa, bifamiliare/villa, …)
-- alla tabella delle aste. Si puo' annullare con sql/aste-immobili-tipologia-undo.sql
alter table public.aste_immobili add column if not exists tipologia text;
