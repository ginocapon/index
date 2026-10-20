-- Annulla aste-stima.sql (ATTENZIONE: cancella le stime di vendita gia' salvate)
alter table public.aste_immobili drop column if exists prezzo_stimato_data;
alter table public.aste_immobili drop column if exists prezzo_stimato_fonte;
alter table public.aste_immobili drop column if exists prezzo_stimato_max;
alter table public.aste_immobili drop column if exists prezzo_stimato_min;
