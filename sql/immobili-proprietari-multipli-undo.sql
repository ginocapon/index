-- ANNULLAMENTO: eseguire SOLO se vuoi togliere la funzione proprietari multipli.
-- Prima ripristina admin.html dal backup-pre-proprietari-20261022.
-- Mantiene immobili, clienti e il proprietario principale attualmente salvato.
-- I collegamenti aggiuntivi NON vengono distrutti: restano nella tabella privata
-- di archivio, consultabile dal solo SQL Editor. Prima di applicare nuovamente
-- la funzione occorre decidere come recuperarli dall'archivio.
BEGIN;
DROP TRIGGER IF EXISTS rig_sync_dati_proprietario ON public.clienti;
DROP TRIGGER IF EXISTS rig_sync_proprietario_principale ON public.immobili;
DROP FUNCTION IF EXISTS public.rig_sync_dati_proprietario();
DROP FUNCTION IF EXISTS public.rig_sync_proprietario_principale();
DROP FUNCTION IF EXISTS public.rig_salva_proprietari(text,text[]);
ALTER TABLE public.immobile_proprietari RENAME TO immobile_proprietari_archivio_20261022;
DROP POLICY proprietari_solo_admin ON public.immobile_proprietari_archivio_20261022;
REVOKE ALL ON public.immobile_proprietari_archivio_20261022 FROM authenticated,anon,PUBLIC;
NOTIFY pgrst,'reload schema';
COMMIT;
