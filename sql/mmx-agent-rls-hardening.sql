-- mmx-agent / Raas-automazioni — RLS sicurezza (Supabase ieeriszlalrsbfsnarih)
-- Dopo l'esecuzione: in Raas-automazioni/admin.html allinea RAAS_ADMIN_RLS_SECRET.

CREATE OR REPLACE FUNCTION public.raas_admin_secret()
RETURNS text
LANGUAGE sql
IMMUTABLE
AS $$
  SELECT 'RAAS_SB_ADMIN_2026_CAMBIA_QUESTO_SEGRETO_LUNGO'::text;
$$;

CREATE OR REPLACE FUNCTION public.raas_is_admin_request()
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT coalesce(
    nullif(trim(current_setting('request.headers', true)::json ->> 'x-raas-admin'), ''),
    ''
  ) = public.raas_admin_secret();
$$;

GRANT EXECUTE ON FUNCTION public.raas_is_admin_request() TO anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.raas_admin_secret() FROM anon, authenticated;

-- Abilita RLS ovunque
ALTER TABLE IF EXISTS public.admin_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.bandi ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.subscribers ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.newsletter_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS public.user_search_preferences ENABLE ROW LEVEL SECURITY;

-- Rimuovi policy legacy permissive
DO $$
DECLARE
  t text;
  pol text;
BEGIN
  FOREACH t IN ARRAY ARRAY[
    'admin_users','bandi','brands','categories','products',
    'subscribers','newsletter_log','user_search_preferences'
  ]
  LOOP
    IF to_regclass('public.' || t) IS NULL THEN CONTINUE; END IF;
    FOREACH pol IN ARRAY ARRAY[
      'Permetti tutto','Bandi visibili a tutti','Permetti tutto su newsletter_log',
      'Permetti tutto su subscribers','Permetti tutto su preferenze',
      'bandi_anon_all','bandi_authenticated_all'
    ]
    LOOP
      EXECUTE format('DROP POLICY IF EXISTS %I ON public.%I', pol, t);
    END LOOP;
  END LOOP;
END $$;

-- admin_users: mai esporre password_hash
DROP POLICY IF EXISTS admin_users_service_only ON public.admin_users;
CREATE POLICY admin_users_service_only ON public.admin_users
  FOR ALL TO anon
  USING (public.raas_is_admin_request())
  WITH CHECK (public.raas_is_admin_request());

-- bandi: sito legge solo attivi; admin scrive con header
DROP POLICY IF EXISTS bandi_public_select ON public.bandi;
CREATE POLICY bandi_public_select ON public.bandi
  FOR SELECT TO anon
  USING (coalesce(attivo, false) = true);

DROP POLICY IF EXISTS bandi_admin_all ON public.bandi;
CREATE POLICY bandi_admin_all ON public.bandi
  FOR ALL TO anon
  USING (public.raas_is_admin_request())
  WITH CHECK (public.raas_is_admin_request());

-- catalogo (se usato): sola lettura
DROP POLICY IF EXISTS products_public_select ON public.products;
CREATE POLICY products_public_select ON public.products
  FOR SELECT TO anon USING (true);
DROP POLICY IF EXISTS products_admin_all ON public.products;
CREATE POLICY products_admin_all ON public.products
  FOR ALL TO anon
  USING (public.raas_is_admin_request())
  WITH CHECK (public.raas_is_admin_request());

DROP POLICY IF EXISTS brands_public_select ON public.brands;
CREATE POLICY brands_public_select ON public.brands
  FOR SELECT TO anon USING (true);
DROP POLICY IF EXISTS brands_admin_all ON public.brands;
CREATE POLICY brands_admin_all ON public.brands
  FOR ALL TO anon
  USING (public.raas_is_admin_request())
  WITH CHECK (public.raas_is_admin_request());

DROP POLICY IF EXISTS categories_public_select ON public.categories;
CREATE POLICY categories_public_select ON public.categories
  FOR SELECT TO anon USING (true);
DROP POLICY IF EXISTS categories_admin_all ON public.categories;
CREATE POLICY categories_admin_all ON public.categories
  FOR ALL TO anon
  USING (public.raas_is_admin_request())
  WITH CHECK (public.raas_is_admin_request());

-- subscribers: iscrizione da sito, no elenco pubblico
DROP POLICY IF EXISTS subscribers_public_insert ON public.subscribers;
CREATE POLICY subscribers_public_insert ON public.subscribers
  FOR INSERT TO anon WITH CHECK (true);

DROP POLICY IF EXISTS subscribers_admin_all ON public.subscribers;
CREATE POLICY subscribers_admin_all ON public.subscribers
  FOR ALL TO anon
  USING (public.raas_is_admin_request())
  WITH CHECK (public.raas_is_admin_request());

-- preferenze ricerca: upsert da form
DROP POLICY IF EXISTS user_prefs_public_insert ON public.user_search_preferences;
CREATE POLICY user_prefs_public_insert ON public.user_search_preferences
  FOR INSERT TO anon WITH CHECK (true);
DROP POLICY IF EXISTS user_prefs_public_update ON public.user_search_preferences;
CREATE POLICY user_prefs_public_update ON public.user_search_preferences
  FOR UPDATE TO anon USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS user_prefs_admin_all ON public.user_search_preferences;
CREATE POLICY user_prefs_admin_all ON public.user_search_preferences
  FOR ALL TO anon
  USING (public.raas_is_admin_request())
  WITH CHECK (public.raas_is_admin_request());

-- log newsletter: solo admin / service_role
DROP POLICY IF EXISTS newsletter_log_admin_all ON public.newsletter_log;
CREATE POLICY newsletter_log_admin_all ON public.newsletter_log
  FOR ALL TO anon
  USING (public.raas_is_admin_request())
  WITH CHECK (public.raas_is_admin_request());
