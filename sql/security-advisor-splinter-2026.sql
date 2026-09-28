-- ═══════════════════════════════════════════════════════════════════════════
-- RIGHETTO — Security Advisor / Splinter (2026)
-- Repository: sql/security-advisor-splinter-2026.sql
--
-- DOVE ESEGUIRE:
--   • Parti 1–3: `supabase db query -f sql/security-advisor-splinter-2026-public.sql --linked`
--   • Parte 4 storage: SQL Editor → sql/security-advisor-splinter-2026-storage.sql (owner storage.objects)
--   • Oppure incolla tutto qui nel SQL Editor (consigliato per storage).
--
-- DOPO: Advisors → Security → Rerun linter
-- TEST: python tools/check_rls_exposure.py  (form sito: invio contatti + newsletter)
--
-- Prerequisito: sql/rls-security-hardening.sql (o -safe) già eseguito almeno una volta.
-- Header admin: x-righetto-admin = righetto_admin_secret() (come admin.html)
-- ═══════════════════════════════════════════════════════════════════════════

-- ─── Diagnostica (opzionale, solo lettura) ───
-- SELECT policyname, roles, cmd, qual, with_check
-- FROM pg_policies
-- WHERE schemaname = 'storage' AND tablename = 'objects'
-- ORDER BY policyname;

-- ═══ 1) Function search_path (Splinter: function_search_path_mutable) ═══

DO $$
BEGIN
  IF to_regprocedure('public.righetto_admin_secret()') IS NOT NULL THEN
    ALTER FUNCTION public.righetto_admin_secret() SET search_path = public, pg_temp;
  END IF;
  IF to_regprocedure('public.update_updated_at()') IS NOT NULL THEN
    ALTER FUNCTION public.update_updated_at() SET search_path = public, pg_temp;
  END IF;
  IF to_regprocedure('public._rig_apply_rls_policies()') IS NOT NULL THEN
    ALTER FUNCTION public._rig_apply_rls_policies() SET search_path = public, pg_temp;
  END IF;
END $$;

-- Se update_updated_at esiste ma senza search_path in definizione, ricrea corpo standard (trigger updated_at)
CREATE OR REPLACE FUNCTION public.update_updated_at()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = public, pg_temp
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- ═══ 2) Helper validazione lead (evita policy RLS con literal `true`) ═══

CREATE OR REPLACE FUNCTION public.righetto_valid_lead_email(p_email text)
RETURNS boolean
LANGUAGE sql
IMMUTABLE
PARALLEL SAFE
SET search_path = public, pg_temp
AS $$
  SELECT coalesce(trim(p_email), '') ~* '^[^\s@]+@[^\s@]+\.[^\s@]+$'
     AND char_length(trim(p_email)) <= 320;
$$;

COMMENT ON FUNCTION public.righetto_valid_lead_email IS
  'Validazione email form pubblici (RLS). Non sostituisce anti-spam lato app.';

-- ═══ 3) RLS — richieste, newsletter, LINDA (Splinter: rls_policy_always_true) ═══

DO $$
BEGIN
  IF to_regclass('public.richieste') IS NOT NULL THEN
    DROP POLICY IF EXISTS "richieste_public_insert" ON public.richieste;
    CREATE POLICY "richieste_public_insert"
      ON public.richieste FOR INSERT TO anon
      WITH CHECK (
        public.righetto_valid_lead_email(email)
        AND char_length(trim(coalesce(nome, ''))) BETWEEN 1 AND 200
        AND char_length(coalesce(messaggio, '')) <= 15000
        AND coalesce(letto, false) = false
      );
  END IF;

  IF to_regclass('public.newsletter_subscribers') IS NOT NULL THEN
    DROP POLICY IF EXISTS "newsletter_public_insert" ON public.newsletter_subscribers;
    DROP POLICY IF EXISTS "newsletter_public_update" ON public.newsletter_subscribers;

    CREATE POLICY "newsletter_public_insert"
      ON public.newsletter_subscribers FOR INSERT TO anon
      WITH CHECK (
        public.righetto_valid_lead_email(email)
        AND char_length(trim(coalesce(nome, ''))) <= 200
        AND char_length(coalesce(telefono, '')) <= 40
      );

    -- Upsert da landing (onConflict email): UPDATE solo con email valida (no SELECT anon)
    CREATE POLICY "newsletter_public_update"
      ON public.newsletter_subscribers FOR UPDATE TO anon
      USING (public.righetto_valid_lead_email(email))
      WITH CHECK (
        public.righetto_valid_lead_email(email)
        AND char_length(trim(coalesce(nome, ''))) <= 200
      );
  END IF;

  IF to_regclass('public.linda_learning_events') IS NOT NULL THEN
    DROP POLICY IF EXISTS linda_learning_events_insert_anon ON public.linda_learning_events;
    CREATE POLICY linda_learning_events_insert_anon ON public.linda_learning_events
      FOR INSERT TO anon
      WITH CHECK (
        event_type IS NOT NULL
        AND char_length(event_type) BETWEEN 1 AND 64
        AND char_length(coalesce(session_id, '')) <= 128
        AND char_length(coalesce(search_id, '')) <= 128
        AND char_length(coalesce(page_path, '')) <= 512
        AND jsonb_typeof(payload) = 'object'
      );

    DROP POLICY IF EXISTS linda_learning_events_select_admin ON public.linda_learning_events;
    DROP POLICY IF EXISTS linda_learning_events_select_righetto_admin ON public.linda_learning_events;
    CREATE POLICY linda_learning_events_select_righetto_admin ON public.linda_learning_events
      FOR SELECT TO anon
      USING (public.righetto_is_admin_request());
  END IF;
END $$;

-- ═══ 4) Storage — documenti & planimetrie (Splinter: public_bucket_allows_listing) ═══
-- Bucket riservati: non pubblici; accesso solo admin (header x-righetto-admin).
-- NOTA: URL public/getPublicUrl non funzionano più per questi bucket → in admin servono signed URL (follow-up codice).
-- foto-immobili: bucket staging/legacy URL; warning listing può restare finché il bucket è public (vedi sql/README.md).

UPDATE storage.buckets
SET public = false
WHERE id IN ('documenti', 'planimetrie');

ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Rimuovi policy generiche spesso create da template Supabase (idempotente)
DROP POLICY IF EXISTS "Public Access" ON storage.objects;
DROP POLICY IF EXISTS "Allow public read access" ON storage.objects;
DROP POLICY IF EXISTS "Public read access" ON storage.objects;
DROP POLICY IF EXISTS "Give anon users access to SELECT" ON storage.objects;
DROP POLICY IF EXISTS "anon read documenti" ON storage.objects;
DROP POLICY IF EXISTS "anon read planimetrie" ON storage.objects;

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

-- foto-immobili: lettura oggetti con nome coerente upload admin (timestamp-nome); no policy `true` su tutto lo schema
DROP POLICY IF EXISTS "rig_storage_foto_public_read" ON storage.objects;
CREATE POLICY "rig_storage_foto_public_read"
  ON storage.objects FOR SELECT TO anon, authenticated
  USING (
    bucket_id = 'foto-immobili'
    AND char_length(name) <= 512
    AND (
      name ~ '^[0-9]+-.+'
      OR name ~ '^blog/.+'
    )
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

-- ═══ Fine ═══
-- Se upload documenti/planimetrie in admin fallisce dopo questo script: verifica header x-righetto-admin
-- e valuta createSignedUrl() per anteprima PDF (bucket privati).
