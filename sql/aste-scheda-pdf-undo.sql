-- Undo di aste-scheda-pdf.sql
alter table public.aste_immobili drop column if exists scheda_path;
