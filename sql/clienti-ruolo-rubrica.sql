-- Rubrica: distingue chi cerca immobile vs proprietario (incarico)
-- Eseguire una tantum in Supabase SQL Editor

ALTER TABLE public.clienti
  ADD COLUMN IF NOT EXISTS ruolo_rubrica text DEFAULT 'cerca';

COMMENT ON COLUMN public.clienti.ruolo_rubrica IS 'cerca = acquirente/inquilino; proprietario = vende/affitta';

-- Record esistenti restano cerca (default)
