-- Parte 1–3 (public schema): eseguibile anche via `supabase db query -f ... --linked`
-- Storage: sql/security-advisor-splinter-2026-storage.sql (solo SQL Editor Dashboard)

-- ═══ 1) Function search_path ═══
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

-- ═══ 2) Helper validazione lead ═══
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

-- ═══ 3) RLS richieste, newsletter, LINDA ═══
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
