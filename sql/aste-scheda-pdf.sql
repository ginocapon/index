-- Colonna scheda_path su aste_immobili: percorso del PDF riassuntivo nel bucket privato "aste-pratica".
-- Il pulsante "Apri scheda PDF" dell'admin genera un signed URL (5 min) e lo mostra in anteprima.
-- Nome file secondo la regola di Gino (20/10/2026): "<id_pvp> - <via civico> - <comune> (<provincia>).pdf"
-- Caricare il PDF con contentType 'application/pdf', altrimenti Safari su iPad lo scarica invece di mostrarlo.
alter table public.aste_immobili
  add column if not exists scheda_path text not null default '';
