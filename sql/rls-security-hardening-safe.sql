-- RIGHETTO — RLS sicurezza (versione SAFE: salta tabelle assenti)
-- Supabase → SQL Editor → incolla tutto → Run
-- Se fallisce ancora, copia il messaggio di errore rosso.

-- ═══ 0) Tabelle minime agenda/cache (se mancano) ═══
CREATE TABLE IF NOT EXISTS public.pianificazioni (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tipo             text NOT NULL DEFAULT 'facebook_post',
  contenuto        text NOT NULL DEFAULT 'immobile',
  titolo           text NOT NULL,
  riferimento_id   text,
  ora              text NOT NULL DEFAULT '12:30',
  giorni           integer[] NOT NULL DEFAULT '{}',
  data_inizio      date NOT NULL,
  data_fine        date NOT NULL,
  keywords         text[] NOT NULL DEFAULT '{}',
  note             text,
  link_media       text,
  corpo_spintax    text,
  media_direct_url text,
  created_at       timestamptz NOT NULL DEFAULT now(),
  updated_at       timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.facebook_feed_cache (
  id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  post_id       text NOT NULL UNIQUE,
  message       text,
  permalink_url text,
  picture_url   text,
  created_time  timestamptz,
  status_type   text,
  synced_at     timestamptz NOT NULL DEFAULT now(),
  raw           jsonb
);

CREATE TABLE IF NOT EXISTS public.instagram_feed_cache (
  id             bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  media_id       text NOT NULL UNIQUE,
  caption        text,
  permalink      text,
  media_url      text,
  thumbnail_url  text,
  media_type     text,
  timestamp      timestamptz,
  synced_at      timestamptz NOT NULL DEFAULT now(),
  raw            jsonb
);

-- ═══ 1) Funzioni segreto admin ═══
CREATE OR REPLACE FUNCTION public.righetto_admin_secret()
RETURNS text LANGUAGE sql IMMUTABLE AS $$
  SELECT 'RIG_SB_ADMIN_2026_CAMBIA_QUESTO_SEGRETO_LUNGO'::text;
$$;

CREATE OR REPLACE FUNCTION public.righetto_is_admin_request()
RETURNS boolean LANGUAGE sql STABLE AS $$
  SELECT coalesce(
    nullif(trim(current_setting('request.headers', true)::json ->> 'x-righetto-admin'), ''),
    ''
  ) = public.righetto_admin_secret();
$$;

-- ═══ 2) Helper: abilita RLS + policy solo se la tabella esiste ═══
CREATE OR REPLACE FUNCTION public._rig_apply_rls_policies()
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE
  t text;
BEGIN
  FOREACH t IN ARRAY ARRAY[
    'immobili','blog','richieste','clienti','newsletter_subscribers',
    'landing_pages','pianificazioni','bozze_social','visualizzazioni_kw',
    'facebook_feed_cache','instagram_feed_cache',
    'campagne_email','coda_email','email_blacklist','email_tracking',
    'smtp_config','gruppi_email','audit_snapshots'
  ]
  LOOP
    IF to_regclass('public.' || t) IS NOT NULL THEN
      EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', t);
    END IF;
  END LOOP;

  -- Rimuovi policy vecchie "Allow all" (solo se tabella esiste)
  IF to_regclass('public.campagne_email') IS NOT NULL THEN
    DROP POLICY IF EXISTS "Allow all for anon" ON public.campagne_email;
  END IF;
  IF to_regclass('public.coda_email') IS NOT NULL THEN
    DROP POLICY IF EXISTS "Allow all for anon" ON public.coda_email;
  END IF;
  IF to_regclass('public.email_blacklist') IS NOT NULL THEN
    DROP POLICY IF EXISTS "Allow all for anon" ON public.email_blacklist;
  END IF;
  IF to_regclass('public.email_tracking') IS NOT NULL THEN
    DROP POLICY IF EXISTS "Allow all for anon" ON public.email_tracking;
  END IF;
  IF to_regclass('public.smtp_config') IS NOT NULL THEN
    DROP POLICY IF EXISTS "Allow all for anon" ON public.smtp_config;
  END IF;
  IF to_regclass('public.gruppi_email') IS NOT NULL THEN
    DROP POLICY IF EXISTS "Allow all for anon" ON public.gruppi_email;
  END IF;

  IF to_regclass('public.pianificazioni') IS NOT NULL THEN
    DROP POLICY IF EXISTS "pianificazioni_anon_select" ON public.pianificazioni;
    DROP POLICY IF EXISTS "pianificazioni_anon_insert" ON public.pianificazioni;
    DROP POLICY IF EXISTS "pianificazioni_anon_update" ON public.pianificazioni;
    DROP POLICY IF EXISTS "pianificazioni_anon_delete" ON public.pianificazioni;
    DROP POLICY IF EXISTS "pianificazioni_authenticated_all" ON public.pianificazioni;
  END IF;

  IF to_regclass('public.bozze_social') IS NOT NULL THEN
    DROP POLICY IF EXISTS "bozze_social_anon_select" ON public.bozze_social;
    DROP POLICY IF EXISTS "bozze_social_anon_insert" ON public.bozze_social;
    DROP POLICY IF EXISTS "bozze_social_anon_update" ON public.bozze_social;
    DROP POLICY IF EXISTS "bozze_social_anon_delete" ON public.bozze_social;
    DROP POLICY IF EXISTS "bozze_social_authenticated_all" ON public.bozze_social;
  END IF;

  -- ── SITO PUBBLICO ──
  IF to_regclass('public.immobili') IS NOT NULL THEN
    DROP POLICY IF EXISTS "immobili_public_select" ON public.immobili;
    CREATE POLICY "immobili_public_select" ON public.immobili
      FOR SELECT TO anon USING (coalesce(attivo, false) = true);
  END IF;

  IF to_regclass('public.blog') IS NOT NULL THEN
    DROP POLICY IF EXISTS "blog_public_select" ON public.blog;
    CREATE POLICY "blog_public_select" ON public.blog
      FOR SELECT TO anon USING (coalesce(stato, 'bozza') = 'pubblicato');
  END IF;

  IF to_regclass('public.richieste') IS NOT NULL THEN
    DROP POLICY IF EXISTS "richieste_public_insert" ON public.richieste;
    CREATE POLICY "richieste_public_insert" ON public.richieste
      FOR INSERT TO anon WITH CHECK (true);
  END IF;

  IF to_regclass('public.newsletter_subscribers') IS NOT NULL THEN
    DROP POLICY IF EXISTS "newsletter_public_insert" ON public.newsletter_subscribers;
    DROP POLICY IF EXISTS "newsletter_public_update" ON public.newsletter_subscribers;
    CREATE POLICY "newsletter_public_insert" ON public.newsletter_subscribers
      FOR INSERT TO anon WITH CHECK (true);
    CREATE POLICY "newsletter_public_update" ON public.newsletter_subscribers
      FOR UPDATE TO anon USING (true) WITH CHECK (true);
  END IF;

  IF to_regclass('public.landing_pages') IS NOT NULL THEN
    DROP POLICY IF EXISTS "landing_public_select" ON public.landing_pages;
    IF EXISTS (
      SELECT 1 FROM information_schema.columns
      WHERE table_schema = 'public' AND table_name = 'landing_pages' AND column_name = 'stato'
    ) THEN
      CREATE POLICY "landing_public_select" ON public.landing_pages
        FOR SELECT TO anon USING (coalesce(stato, 'pubblicata') = 'pubblicata');
    ELSE
      CREATE POLICY "landing_public_select" ON public.landing_pages
        FOR SELECT TO anon USING (true);
    END IF;
  END IF;

  IF to_regclass('public.facebook_feed_cache') IS NOT NULL THEN
    DROP POLICY IF EXISTS "facebook_feed_cache_anon_select" ON public.facebook_feed_cache;
    CREATE POLICY "facebook_feed_cache_anon_select" ON public.facebook_feed_cache
      FOR SELECT TO anon USING (true);
  END IF;

  IF to_regclass('public.instagram_feed_cache') IS NOT NULL THEN
    DROP POLICY IF EXISTS "instagram_feed_cache_anon_select" ON public.instagram_feed_cache;
    CREATE POLICY "instagram_feed_cache_anon_select" ON public.instagram_feed_cache
      FOR SELECT TO anon USING (true);
  END IF;

  -- ── ADMIN (header x-righetto-admin) ──
  IF to_regclass('public.immobili') IS NOT NULL THEN
    DROP POLICY IF EXISTS "immobili_admin_all" ON public.immobili;
    CREATE POLICY "immobili_admin_all" ON public.immobili FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.blog') IS NOT NULL THEN
    DROP POLICY IF EXISTS "blog_admin_all" ON public.blog;
    CREATE POLICY "blog_admin_all" ON public.blog FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.richieste') IS NOT NULL THEN
    DROP POLICY IF EXISTS "richieste_admin_all" ON public.richieste;
    CREATE POLICY "richieste_admin_all" ON public.richieste FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.clienti') IS NOT NULL THEN
    DROP POLICY IF EXISTS "clienti_admin_all" ON public.clienti;
    CREATE POLICY "clienti_admin_all" ON public.clienti FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.newsletter_subscribers') IS NOT NULL THEN
    DROP POLICY IF EXISTS "newsletter_admin_all" ON public.newsletter_subscribers;
    CREATE POLICY "newsletter_admin_all" ON public.newsletter_subscribers FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.landing_pages') IS NOT NULL THEN
    DROP POLICY IF EXISTS "landing_admin_all" ON public.landing_pages;
    CREATE POLICY "landing_admin_all" ON public.landing_pages FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.pianificazioni') IS NOT NULL THEN
    DROP POLICY IF EXISTS "pianificazioni_admin_all" ON public.pianificazioni;
    CREATE POLICY "pianificazioni_admin_all" ON public.pianificazioni FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.bozze_social') IS NOT NULL THEN
    DROP POLICY IF EXISTS "bozze_social_admin_all" ON public.bozze_social;
    CREATE POLICY "bozze_social_admin_all" ON public.bozze_social FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.visualizzazioni_kw') IS NOT NULL THEN
    DROP POLICY IF EXISTS "visualizzazioni_kw_admin_all" ON public.visualizzazioni_kw;
    CREATE POLICY "visualizzazioni_kw_admin_all" ON public.visualizzazioni_kw FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.campagne_email') IS NOT NULL THEN
    DROP POLICY IF EXISTS "campagne_email_admin_all" ON public.campagne_email;
    CREATE POLICY "campagne_email_admin_all" ON public.campagne_email FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.coda_email') IS NOT NULL THEN
    DROP POLICY IF EXISTS "coda_email_admin_all" ON public.coda_email;
    CREATE POLICY "coda_email_admin_all" ON public.coda_email FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.email_blacklist') IS NOT NULL THEN
    DROP POLICY IF EXISTS "email_blacklist_admin_all" ON public.email_blacklist;
    CREATE POLICY "email_blacklist_admin_all" ON public.email_blacklist FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.email_tracking') IS NOT NULL THEN
    DROP POLICY IF EXISTS "email_tracking_admin_all" ON public.email_tracking;
    CREATE POLICY "email_tracking_admin_all" ON public.email_tracking FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.smtp_config') IS NOT NULL THEN
    DROP POLICY IF EXISTS "smtp_config_admin_all" ON public.smtp_config;
    CREATE POLICY "smtp_config_admin_all" ON public.smtp_config FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.gruppi_email') IS NOT NULL THEN
    DROP POLICY IF EXISTS "gruppi_email_admin_all" ON public.gruppi_email;
    CREATE POLICY "gruppi_email_admin_all" ON public.gruppi_email FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.facebook_feed_cache') IS NOT NULL THEN
    DROP POLICY IF EXISTS "facebook_feed_cache_admin_write" ON public.facebook_feed_cache;
    CREATE POLICY "facebook_feed_cache_admin_write" ON public.facebook_feed_cache FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.instagram_feed_cache') IS NOT NULL THEN
    DROP POLICY IF EXISTS "instagram_feed_cache_admin_write" ON public.instagram_feed_cache;
    CREATE POLICY "instagram_feed_cache_admin_write" ON public.instagram_feed_cache FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

  IF to_regclass('public.audit_snapshots') IS NOT NULL THEN
    DROP POLICY IF EXISTS "audit_snapshots_admin_all" ON public.audit_snapshots;
    CREATE POLICY "audit_snapshots_admin_all" ON public.audit_snapshots FOR ALL TO anon
      USING (public.righetto_is_admin_request()) WITH CHECK (public.righetto_is_admin_request());
  END IF;

END;
$$;

SELECT public._rig_apply_rls_policies();

-- Verifica rapida
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN (
    'immobili','blog','richieste','clienti','pianificazioni',
    'smtp_config','campagne_email','facebook_feed_cache'
  )
ORDER BY tablename;
