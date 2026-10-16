-- UNDO aste-immobili.sql — annulla tutto: elimina tabella e policy
-- Esegui in Supabase → SQL Editor solo se vuoi rimuovere la funzione Aste.

DROP POLICY IF EXISTS "aste_immobili_admin_all" ON public.aste_immobili;
DROP TABLE IF EXISTS public.aste_immobili;
