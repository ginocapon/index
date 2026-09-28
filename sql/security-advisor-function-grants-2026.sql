-- Security Advisor: "Public / Signed-In Users can execute SECURITY DEFINER function"
-- Esegui in Supabase SQL Editor (schema public — di solito OK, non è storage.objects).
--
-- Cosa fa: toglie EXECUTE al ruolo PUBLIC e a authenticated; lascia solo anon dove serve
-- (admin con chiave anon, disiscrizione newsletter, policy RLS).

DO $$
DECLARE
  r record;
BEGIN
  FOR r IN
    SELECT p.oid::regprocedure AS sig
    FROM pg_proc p
    JOIN pg_namespace n ON p.pronamespace = n.oid
    WHERE n.nspname = 'public'
      AND p.proname IN (
        'righetto_is_admin_request',
        'disiscrivi_email',
        'rig_admin_set_attivo',
        'rig_admin_set_evidenza'
      )
  LOOP
    EXECUTE format('REVOKE ALL ON FUNCTION %s FROM PUBLIC', r.sig);
    EXECUTE format('REVOKE EXECUTE ON FUNCTION %s FROM authenticated', r.sig);
    EXECUTE format('GRANT EXECUTE ON FUNCTION %s TO anon', r.sig);
  END LOOP;
END $$;

-- Segreto admin: mai eseguibile da client (solo uso interno nelle funzioni)
DO $$
BEGIN
  IF to_regprocedure('public.righetto_admin_secret()') IS NOT NULL THEN
    REVOKE ALL ON FUNCTION public.righetto_admin_secret() FROM PUBLIC;
    REVOKE EXECUTE ON FUNCTION public.righetto_admin_secret() FROM anon, authenticated;
  END IF;
END $$;

-- Verifica (opzionale): elenco grant
SELECT
  p.proname AS function,
  pg_get_function_identity_arguments(p.oid) AS args,
  array_agg(DISTINCT acl.grantee::regrole::text ORDER BY acl.grantee::regrole::text) AS grantees
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
LEFT JOIN LATERAL aclexplode(COALESCE(p.proacl, acldefault('f', p.proowner))) AS acl ON true
WHERE n.nspname = 'public'
  AND p.proname IN (
    'righetto_is_admin_request',
    'disiscrivi_email',
    'rig_admin_set_attivo',
    'rig_admin_set_evidenza'
  )
GROUP BY p.oid, p.proname
ORDER BY p.proname, args;
