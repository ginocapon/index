-- Solo se il pannello segnala: permission denied for function righetto_is_admin_request.
-- Permette al ruolo autenticato di chiamare il controllo admin gia esistente.
-- Non cambia chi e admin e non concede accesso anonimo.
GRANT EXECUTE ON FUNCTION public.righetto_is_admin_request() TO authenticated;
NOTIFY pgrst, 'reload schema';
-- Annullamento del solo permesso, se non era presente prima:
-- REVOKE EXECUTE ON FUNCTION public.righetto_is_admin_request() FROM authenticated;
