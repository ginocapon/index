-- DEPRECATED per le RPC admin (24/11/2026).
-- Questo file concedeva EXECUTE a `anon` su rig_admin_* / righetto_is_admin_request.
-- Usare invece: sql/p0-security-2026-11-24.sql
-- (o supabase/migrations/20261124_p0_revoke_admin_rpc_anon.sql)
--
-- Non eseguire questo script sul DB live.

SELECT 'Usa sql/p0-security-2026-11-24.sql al posto di security-advisor-function-grants-2026.sql'::text AS notice;
