-- righetto_is_admin_request deve essere SECURITY DEFINER:
-- le policy RLS la invocano come anon, ma internamente confronta con righetto_admin_secret()
-- senza esporre il segreto via RPC.

CREATE OR REPLACE FUNCTION public.righetto_is_admin_request()
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT coalesce(
    nullif(trim(current_setting('request.headers', true)::json ->> 'x-righetto-admin'), ''),
    ''
  ) = public.righetto_admin_secret();
$$;

GRANT EXECUTE ON FUNCTION public.righetto_is_admin_request() TO anon, authenticated;
REVOKE EXECUTE ON FUNCTION public.righetto_admin_secret() FROM anon, authenticated;
