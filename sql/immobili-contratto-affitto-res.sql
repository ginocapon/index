-- Tipo contratto affitto residenziale (solo admin / stampa — non esposto sui filtri pubblici)
-- Esegui in Supabase → SQL Editor (progetto righetto-immobiliare).

ALTER TABLE public.immobili
  ADD COLUMN IF NOT EXISTS contratto_affitto_res TEXT;

COMMENT ON COLUMN public.immobili.contratto_affitto_res IS
  'Valori: affitto_ordinario | cedolare_secca | concordato. Solo se tipo_operazione = affitto_residenziale. Uso interno admin.';
