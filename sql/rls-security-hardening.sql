-- ═══════════════════════════════════════════════════════════════════════════
-- RIGHETTO — RLS / sicurezza (mail Supabase "publicly accessible")
-- Esegui in Supabase → SQL Editor (progetto righetto-immobiliare).
--
-- DOPO l'esecuzione: in admin.html imposta RIG_ADMIN_RLS_SECRET uguale a
-- righetto_admin_secret() qui sotto (cambia entrambi con una stringa lunga).
--
-- Script Python (.env service_role) e Edge Functions con service_role: OK senza header.
-- Sito pubblico (immobili, form, newsletter): OK senza header.
-- ═══════════════════════════════════════════════════════════════════════════

-- Segreto condiviso admin ↔ policy (CAMBIA prima di andare in produzione)
CREATE OR REPLACE FUNCTION public.righetto_admin_secret()
RETURNS text
LANGUAGE sql
IMMUTABLE
AS $$
  SELECT 'RIG_SB_ADMIN_2026_CAMBIA_QUESTO_SEGRETO_LUNGO'::text;
$$;

CREATE OR REPLACE FUNCTION public.righetto_is_admin_request()
RETURNS boolean
LANGUAGE sql
STABLE
AS $$
  SELECT coalesce(
    nullif(trim(current_setting('request.headers', true)::json ->> 'x-righetto-admin'), ''),
    ''
  ) = public.righetto_admin_secret();
$$;

-- ─── Rimuovi policy "tutto permesso" (email marketing + altro) ───
DROP POLICY IF EXISTS "Allow all for anon" ON public.campagne_email;
DROP POLICY IF EXISTS "Allow all for anon" ON public.coda_email;
DROP POLICY IF EXISTS "Allow all for anon" ON public.email_blacklist;
DROP POLICY IF EXISTS "Allow all for anon" ON public.email_tracking;
DROP POLICY IF EXISTS "Allow all for anon" ON public.smtp_config;
DROP POLICY IF EXISTS "Allow all for anon" ON public.gruppi_email;

DROP POLICY IF EXISTS "pianificazioni_anon_select" ON public.pianificazioni;
DROP POLICY IF EXISTS "pianificazioni_anon_insert" ON public.pianificazioni;
DROP POLICY IF EXISTS "pianificazioni_anon_update" ON public.pianificazioni;
DROP POLICY IF EXISTS "pianificazioni_anon_delete" ON public.pianificazioni;
DROP POLICY IF EXISTS "pianificazioni_authenticated_all" ON public.pianificazioni;

-- ─── Abilita RLS (idempotente) ───
ALTER TABLE IF EXISTS public.immobili ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.blog ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.richieste ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.clienti ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.newsletter_subscribers ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.landing_pages ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.pianificazioni ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.visualizzazioni_kw ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.facebook_feed_cache ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.instagram_feed_cache ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.campagne_email ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.coda_email ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.email_blacklist ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.email_tracking ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.smtp_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.gruppi_email ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
  IF to_regclass('public.audit_snapshots') IS NOT NULL THEN
    EXECUTE 'ALTER TABLE public.audit_snapshots ENABLE ROW LEVEL SECURITY';
  END IF;
END $$;

-- ═══ SITO PUBBLICO (anon, senza header admin) ═══

-- Immobili: solo attivi in vetrina
DROP POLICY IF EXISTS "immobili_public_select" ON public.immobili;
CREATE POLICY "immobili_public_select"
  ON public.immobili FOR SELECT TO anon
  USING (coalesce(attivo, false) = true);

-- Blog: solo articoli pubblicati
DROP POLICY IF EXISTS "blog_public_select" ON public.blog;
CREATE POLICY "blog_public_select"
  ON public.blog FOR SELECT TO anon
  USING (coalesce(stato, 'bozza') = 'pubblicato');

-- Richieste: solo inserimento da form sito
DROP POLICY IF EXISTS "richieste_public_insert" ON public.richieste;
CREATE POLICY "richieste_public_insert"
  ON public.richieste FOR INSERT TO anon
  WITH CHECK (true);

-- Newsletter: iscrizione / upsert da landing (no lettura elenco)
DROP POLICY IF EXISTS "newsletter_public_insert" ON public.newsletter_subscribers;
DROP POLICY IF EXISTS "newsletter_public_update" ON public.newsletter_subscribers;
CREATE POLICY "newsletter_public_insert"
  ON public.newsletter_subscribers FOR INSERT TO anon
  WITH CHECK (true);
CREATE POLICY "newsletter_public_update"
  ON public.newsletter_subscribers FOR UPDATE TO anon
  USING (true) WITH CHECK (true);

-- Landing pubblicate (se colonna stato esiste)
DROP POLICY IF EXISTS "landing_public_select" ON public.landing_pages;
CREATE POLICY "landing_public_select"
  ON public.landing_pages FOR SELECT TO anon
  USING (coalesce(stato, 'pubblicata') = 'pubblicata');

-- Cache social: solo lettura (dati già pubblici su FB/IG)
DROP POLICY IF EXISTS "facebook_feed_cache_anon_select" ON public.facebook_feed_cache;
CREATE POLICY "facebook_feed_cache_anon_select"
  ON public.facebook_feed_cache FOR SELECT TO anon
  USING (true);
DROP POLICY IF EXISTS "instagram_feed_cache_anon_select" ON public.instagram_feed_cache;
CREATE POLICY "instagram_feed_cache_anon_select"
  ON public.instagram_feed_cache FOR SELECT TO anon
  USING (true);

-- ═══ ADMIN (header x-righetto-admin = righetto_admin_secret()) ═══

DROP POLICY IF EXISTS "immobili_admin_all" ON public.immobili;
CREATE POLICY "immobili_admin_all"
  ON public.immobili FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "blog_admin_all" ON public.blog;
CREATE POLICY "blog_admin_all"
  ON public.blog FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "richieste_admin_all" ON public.richieste;
CREATE POLICY "richieste_admin_all"
  ON public.richieste FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "clienti_admin_all" ON public.clienti;
CREATE POLICY "clienti_admin_all"
  ON public.clienti FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "newsletter_admin_all" ON public.newsletter_subscribers;
CREATE POLICY "newsletter_admin_all"
  ON public.newsletter_subscribers FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "landing_admin_all" ON public.landing_pages;
CREATE POLICY "landing_admin_all"
  ON public.landing_pages FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "pianificazioni_admin_all" ON public.pianificazioni;
CREATE POLICY "pianificazioni_admin_all"
  ON public.pianificazioni FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "visualizzazioni_kw_admin_all" ON public.visualizzazioni_kw;
CREATE POLICY "visualizzazioni_kw_admin_all"
  ON public.visualizzazioni_kw FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "campagne_email_admin_all" ON public.campagne_email;
CREATE POLICY "campagne_email_admin_all"
  ON public.campagne_email FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "coda_email_admin_all" ON public.coda_email;
CREATE POLICY "coda_email_admin_all"
  ON public.coda_email FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "email_blacklist_admin_all" ON public.email_blacklist;
CREATE POLICY "email_blacklist_admin_all"
  ON public.email_blacklist FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "email_tracking_admin_all" ON public.email_tracking;
CREATE POLICY "email_tracking_admin_all"
  ON public.email_tracking FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "smtp_config_admin_all" ON public.smtp_config;
CREATE POLICY "smtp_config_admin_all"
  ON public.smtp_config FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "gruppi_email_admin_all" ON public.gruppi_email;
CREATE POLICY "gruppi_email_admin_all"
  ON public.gruppi_email FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "facebook_feed_cache_admin_write" ON public.facebook_feed_cache;
CREATE POLICY "facebook_feed_cache_admin_write"
  ON public.facebook_feed_cache FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS "instagram_feed_cache_admin_write" ON public.instagram_feed_cache;
CREATE POLICY "instagram_feed_cache_admin_write"
  ON public.instagram_feed_cache FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DO $$
BEGIN
  IF to_regclass('public.audit_snapshots') IS NOT NULL THEN
    EXECUTE 'DROP POLICY IF EXISTS audit_snapshots_admin_all ON public.audit_snapshots';
    EXECUTE $p$
      CREATE POLICY audit_snapshots_admin_all
        ON public.audit_snapshots FOR ALL TO anon
        USING (public.righetto_is_admin_request())
        WITH CHECK (public.righetto_is_admin_request())
    $p$;
  END IF;
END $$;

-- service_role bypassa RLS (script publish_from_agenda, sync FB/IG)
COMMENT ON FUNCTION public.righetto_is_admin_request IS
  'True se la richiesta REST include header x-righetto-admin uguale a righetto_admin_secret().';
