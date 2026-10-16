-- UNDO di aste-guida-pratica.sql — annulla tutto (tabelle, spazio file, permessi).
-- ATTENZIONE: cancella anche le checklist salvate e i PDF caricati nello spazio "aste-pratica".

DROP POLICY IF EXISTS "aste_pratica_admin_select" ON storage.objects;
DROP POLICY IF EXISTS "aste_pratica_admin_insert" ON storage.objects;
DROP POLICY IF EXISTS "aste_pratica_admin_update" ON storage.objects;
DROP POLICY IF EXISTS "aste_pratica_admin_delete" ON storage.objects;
DELETE FROM storage.objects WHERE bucket_id = 'aste-pratica';
DELETE FROM storage.buckets WHERE id = 'aste-pratica';
DROP TABLE IF EXISTS public.aste_guida_passi;
DROP TABLE IF EXISTS public.aste_guida_pratiche;
