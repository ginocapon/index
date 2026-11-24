-- P0 security 2026-11-24 — WhatsApp config/audit tables without RLS
-- Apply manually in Supabase SQL Editor (do NOT auto-apply from CI).
-- Safe with existing SECURITY DEFINER WhatsApp RPCs (owner bypasses RLS unless FORCE).

ALTER TABLE public.whatsapp_personal_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_personal_audit ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_draft_config ENABLE ROW LEVEL SECURITY;

-- No FORCE ROW LEVEL SECURITY: SECURITY DEFINER RPCs (righetto_wa_*) keep working.

DROP POLICY IF EXISTS whatsapp_personal_config_admin_all ON public.whatsapp_personal_config;
CREATE POLICY whatsapp_personal_config_admin_all
  ON public.whatsapp_personal_config
  FOR ALL
  TO authenticated
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS whatsapp_draft_config_admin_all ON public.whatsapp_draft_config;
CREATE POLICY whatsapp_draft_config_admin_all
  ON public.whatsapp_draft_config
  FOR ALL
  TO authenticated
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

DROP POLICY IF EXISTS whatsapp_personal_audit_admin_select ON public.whatsapp_personal_audit;
CREATE POLICY whatsapp_personal_audit_admin_select
  ON public.whatsapp_personal_audit
  FOR SELECT
  TO authenticated
  USING (public.righetto_is_admin_request());

DROP POLICY IF EXISTS whatsapp_personal_audit_admin_insert ON public.whatsapp_personal_audit;
CREATE POLICY whatsapp_personal_audit_admin_insert
  ON public.whatsapp_personal_audit
  FOR INSERT
  TO authenticated
  WITH CHECK (public.righetto_is_admin_request());

-- Anon must never get table privileges (defense in depth; today only service_role has GRANT).
REVOKE ALL ON TABLE public.whatsapp_personal_config FROM PUBLIC, anon;
REVOKE ALL ON TABLE public.whatsapp_draft_config FROM PUBLIC, anon;
REVOKE ALL ON TABLE public.whatsapp_personal_audit FROM PUBLIC, anon;
