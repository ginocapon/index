-- Parte 4 — Storage (Supabase SQL Editor)
-- NON usare: ALTER TABLE storage.objects … → errore 42501 must be owner of table objects
-- RLS su storage.objects è già attivo di default su Supabase.

-- Bucket riservati: non pubblici (se fallisce, imposta manualmente Storage → bucket → Public OFF)
UPDATE storage.buckets
SET public = false
WHERE id IN ('documenti', 'planimetrie');

-- ─── Rimuovi policy vecchie (nomi reali progetto righetto) ───
DROP POLICY IF EXISTS "Allow public read documenti" ON storage.objects;
DROP POLICY IF EXISTS "Allow public upload documenti" ON storage.objects;
DROP POLICY IF EXISTS "Public read documenti" ON storage.objects;
DROP POLICY IF EXISTS "Upload documenti" ON storage.objects;
DROP POLICY IF EXISTS "Delete documenti" ON storage.objects;

DROP POLICY IF EXISTS "Public read planimetrie" ON storage.objects;
DROP POLICY IF EXISTS "Upload planimetrie" ON storage.objects;
DROP POLICY IF EXISTS "Delete planimetrie" ON storage.objects;

DROP POLICY IF EXISTS "Public read foto" ON storage.objects;
DROP POLICY IF EXISTS "Upload foto" ON storage.objects;
DROP POLICY IF EXISTS "Delete foto" ON storage.objects;

-- Template generici (idempotente)
DROP POLICY IF EXISTS "Public Access" ON storage.objects;
DROP POLICY IF EXISTS "Allow public read access" ON storage.objects;
DROP POLICY IF EXISTS "Public read access" ON storage.objects;

-- ─── Policy Righetto ───
DROP POLICY IF EXISTS "rig_storage_documenti_admin" ON storage.objects;
CREATE POLICY "rig_storage_documenti_admin"
  ON storage.objects FOR ALL TO anon
  USING (bucket_id = 'documenti' AND public.righetto_is_admin_request())
  WITH CHECK (bucket_id = 'documenti' AND public.righetto_is_admin_request());

DROP POLICY IF EXISTS "rig_storage_planimetrie_admin" ON storage.objects;
CREATE POLICY "rig_storage_planimetrie_admin"
  ON storage.objects FOR ALL TO anon
  USING (bucket_id = 'planimetrie' AND public.righetto_is_admin_request())
  WITH CHECK (bucket_id = 'planimetrie' AND public.righetto_is_admin_request());

DROP POLICY IF EXISTS "rig_storage_foto_public_read" ON storage.objects;
CREATE POLICY "rig_storage_foto_public_read"
  ON storage.objects FOR SELECT TO anon, authenticated
  USING (
    bucket_id = 'foto-immobili'
    AND char_length(name) <= 512
    AND (name ~ '^[0-9]+-.+' OR name ~ '^blog/.+')
  );

DROP POLICY IF EXISTS "rig_storage_foto_admin_write" ON storage.objects;
CREATE POLICY "rig_storage_foto_admin_write"
  ON storage.objects FOR INSERT TO anon
  WITH CHECK (
    bucket_id = 'foto-immobili'
    AND public.righetto_is_admin_request()
    AND char_length(name) <= 512
    AND (name ~ '^[0-9]+-.+' OR name ~ '^blog/.+')
  );

DROP POLICY IF EXISTS "rig_storage_foto_admin_update" ON storage.objects;
CREATE POLICY "rig_storage_foto_admin_update"
  ON storage.objects FOR UPDATE TO anon
  USING (bucket_id = 'foto-immobili' AND public.righetto_is_admin_request())
  WITH CHECK (bucket_id = 'foto-immobili' AND public.righetto_is_admin_request());

DROP POLICY IF EXISTS "rig_storage_foto_admin_delete" ON storage.objects;
CREATE POLICY "rig_storage_foto_admin_delete"
  ON storage.objects FOR DELETE TO anon
  USING (bucket_id = 'foto-immobili' AND public.righetto_is_admin_request());
