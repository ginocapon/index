-- Rimuove policy legacy che lasciano dati sensibili leggibili con chiave anon.
-- Idempotente: salta tabelle assenti.

DO $$
DECLARE
  t text;
  pol text;
BEGIN
  FOREACH t IN ARRAY ARRAY[
    'audit_snapshots','blog','clienti','landing_pages','newsletter_subscribers',
    'richieste','bozze_social','pianificazioni',
    'campagne_email','coda_email','email_blacklist','email_tracking','smtp_config','gruppi_email'
  ]
  LOOP
    IF to_regclass('public.' || t) IS NULL THEN
      CONTINUE;
    END IF;

    FOREACH pol IN ARRAY ARRAY[
      'Allow all for anon',
      'Lettura pubblica blog',
      'Inserimento blog',
      'Aggiornamento blog',
      'Eliminazione blog',
      'public_access',
      'Admin gestisce landing',
      'Admin legge tutto',
      'Chiunque può iscriversi',
      'Chiunque può aggiornare la propria iscrizione',
      'richieste_admin_read',
      'bozze_social_anon_select',
      'bozze_social_anon_insert',
      'bozze_social_anon_update',
      'bozze_social_anon_delete',
      'bozze_social_authenticated_all',
      'pianificazioni_anon_select',
      'pianificazioni_anon_insert',
      'pianificazioni_anon_update',
      'pianificazioni_anon_delete',
      'pianificazioni_authenticated_all'
    ]
    LOOP
      EXECUTE format('DROP POLICY IF EXISTS %I ON public.%I', pol, t);
    END LOOP;
  END LOOP;
END $$;

REVOKE EXECUTE ON FUNCTION public.righetto_admin_secret() FROM anon, authenticated;
GRANT EXECUTE ON FUNCTION public.righetto_is_admin_request() TO anon, authenticated;
