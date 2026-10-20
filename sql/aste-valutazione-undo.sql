-- Annulla aste-valutazione.sql (ATTENZIONE: cancella le scelte Scartato/Interessante gia' fatte)
alter table public.aste_immobili drop column if exists valutazione_data;
alter table public.aste_immobili drop column if exists valutazione;
