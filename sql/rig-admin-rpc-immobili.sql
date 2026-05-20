-- Toggle attivo / in_evidenza dall'admin anche se l'header x-righetto-admin non arriva a PostgREST.
-- Esegui in Supabase SQL Editor (una volta). Il segreto p_secret deve coincidere con righetto_admin_secret().

CREATE OR REPLACE FUNCTION public.rig_admin_set_attivo(
  p_id uuid,
  p_attivo boolean,
  p_secret text
)
RETURNS TABLE (id uuid, attivo boolean)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  IF coalesce(trim(p_secret), '') <> public.righetto_admin_secret() THEN
    RAISE EXCEPTION 'admin_unauthorized' USING ERRCODE = '42501';
  END IF;
  RETURN QUERY
  UPDATE public.immobili i
  SET attivo = p_attivo
  WHERE i.id = p_id
  RETURNING i.id, i.attivo;
END;
$$;

CREATE OR REPLACE FUNCTION public.rig_admin_set_evidenza(
  p_id uuid,
  p_in_evidenza boolean,
  p_secret text
)
RETURNS TABLE (id uuid, in_evidenza boolean)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  IF coalesce(trim(p_secret), '') <> public.righetto_admin_secret() THEN
    RAISE EXCEPTION 'admin_unauthorized' USING ERRCODE = '42501';
  END IF;
  RETURN QUERY
  UPDATE public.immobili i
  SET in_evidenza = p_in_evidenza
  WHERE i.id = p_id
  RETURNING i.id, i.in_evidenza;
END;
$$;

REVOKE ALL ON FUNCTION public.rig_admin_set_attivo(uuid, boolean, text) FROM PUBLIC;
REVOKE ALL ON FUNCTION public.rig_admin_set_evidenza(uuid, boolean, text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.rig_admin_set_attivo(uuid, boolean, text) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION public.rig_admin_set_evidenza(uuid, boolean, text) TO anon, authenticated;
