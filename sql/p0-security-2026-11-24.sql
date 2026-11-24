-- ============================================================================
-- P0 SICUREZZA Righetto — 24/11/2026 (file unico da incollare nel SQL Editor)
-- Ordine: 1) WhatsApp RLS  2) REVOKE RPC admin da anon
-- Fonte versionata anche in:
--   supabase/migrations/20261124_p0_whatsapp_rls.sql
--   supabase/migrations/20261124_p0_revoke_admin_rpc_anon.sql
-- Istruzioni italiane: docs/p0-security-2026-11-24.md
-- ============================================================================

-- ─── 1) WhatsApp RLS ─────────────────────────────────────────────────────────
ALTER TABLE public.whatsapp_personal_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_personal_audit ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_draft_config ENABLE ROW LEVEL SECURITY;

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

REVOKE ALL ON TABLE public.whatsapp_personal_config FROM PUBLIC, anon;
REVOKE ALL ON TABLE public.whatsapp_draft_config FROM PUBLIC, anon;
REVOKE ALL ON TABLE public.whatsapp_personal_audit FROM PUBLIC, anon;

-- ─── 2) REVOKE admin RPC da anon / PUBLIC ─────────────────────────────────────
DO $$
DECLARE
  r record;
  admin_rpcs text[] := ARRAY[
    'rig_admin_set_attivo',
    'rig_admin_set_evidenza',
    'rig_admin_property_state_v1',
    'righetto_admin_set_member',
    'righetto_is_admin_request',
    'righetto_save_asta_editor',
    'immobile_registra_modifica_privata',
    'immobile_registra_relazione_proprietario',
    'immobile_salva_scelte_info',
    'immobile_contratto_mutate',
    'agenda_retire_type',
    'cestino_percorso_bloccato',
    'righetto_esito_promemoria_etichetta_v1',
    'righetto_gestisci_etichetta_v1',
    'righetto_leggi_promemoria_etichetta_v1',
    'righetto_salva_promemoria_etichetta_v1',
    'righetto_salva_concordato_v1',
    'righetto_modulo_append_revision',
    'righetto_modulo_create_personale',
    'righetto_modulo_save_documento'
  ];
  wa_prefix text := 'righetto_wa_';
BEGIN
  FOR r IN
    SELECT p.oid::regprocedure AS sig
    FROM pg_proc p
    JOIN pg_namespace n ON p.pronamespace = n.oid
    WHERE n.nspname = 'public'
      AND (
        p.proname = ANY (admin_rpcs)
        OR p.proname LIKE wa_prefix || '%'
      )
  LOOP
    EXECUTE format('REVOKE ALL ON FUNCTION %s FROM PUBLIC', r.sig);
    EXECUTE format('REVOKE EXECUTE ON FUNCTION %s FROM anon', r.sig);
    EXECUTE format('GRANT EXECUTE ON FUNCTION %s TO authenticated', r.sig);
  END LOOP;
END $$;

DO $$
BEGIN
  IF to_regprocedure('public.righetto_admin_secret()') IS NOT NULL THEN
    REVOKE ALL ON FUNCTION public.righetto_admin_secret() FROM PUBLIC;
    REVOKE EXECUTE ON FUNCTION public.righetto_admin_secret() FROM anon, authenticated;
  END IF;
END $$;

DO $$
DECLARE
  r record;
  keep_anon text[] := ARRAY[
    'disiscrivi_email',
    'linda_kb_search',
    'linda_log_question',
    'linda_feedback',
    'foto_sopralluogo_lista',
    'foto_sopralluogo_svuota',
    'salva_scheda_path',
    'salva_stima_asta',
    'salva_voto_asta',
    'righetto_asta_normal_identity'
  ];
BEGIN
  FOR r IN
    SELECT p.oid::regprocedure AS sig
    FROM pg_proc p
    JOIN pg_namespace n ON p.pronamespace = n.oid
    WHERE n.nspname = 'public'
      AND p.proname = ANY (keep_anon)
  LOOP
    EXECUTE format('GRANT EXECUTE ON FUNCTION %s TO anon', r.sig);
  END LOOP;
END $$;
