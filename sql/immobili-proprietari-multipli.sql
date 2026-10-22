-- PROPRIETARI MULTIPLI - 22 ottobre 2026
-- Un solo blocco: copia tutto in Supabase > SQL Editor > New query.
-- Non eseguirlo finche non ti viene richiesto. Non modifica le foto o i documenti.
-- Crea collegamenti privati fra immobili e clienti, mantenendo il principale esistente.
-- Non cancella immobili o clienti. Tutto il blocco riesce oppure viene annullato.
BEGIN;
-- Interrompe se e ancora in uso la vecchia autenticazione a chiave pubblica.
DO $$ BEGIN
  IF position('auth.uid()' in pg_get_functiondef('public.righetto_is_admin_request()'::regprocedure)) = 0 THEN
    RAISE EXCEPTION 'Stop: verificare prima il login admin Supabase';
  END IF;
  IF to_regclass('public.immobile_proprietari') IS NOT NULL THEN
    RAISE EXCEPTION 'Tabella gia presente: non rieseguire questo blocco';
  END IF;
END $$;
-- I tipi degli ID sono copiati dalle tabelle vere, senza presumere UUID o numeri.
CREATE TABLE public.immobile_proprietari AS
  SELECT i.id AS immobile_id,c.id AS cliente_id,0::integer AS ordine
  FROM public.immobili i CROSS JOIN public.clienti c WITH NO DATA;
ALTER TABLE public.immobile_proprietari
  ALTER COLUMN immobile_id SET NOT NULL,
  ALTER COLUMN cliente_id SET NOT NULL,
  ALTER COLUMN ordine SET NOT NULL,
  ADD PRIMARY KEY (immobile_id,cliente_id),
  ADD FOREIGN KEY (immobile_id) REFERENCES public.immobili(id) ON DELETE CASCADE,
  ADD FOREIGN KEY (cliente_id) REFERENCES public.clienti(id) ON DELETE RESTRICT;
ALTER TABLE public.immobile_proprietari ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.immobile_proprietari FROM anon,PUBLIC;
GRANT SELECT,INSERT,UPDATE,DELETE ON public.immobile_proprietari TO authenticated;
CREATE POLICY proprietari_solo_admin ON public.immobile_proprietari
  FOR ALL TO authenticated
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());
INSERT INTO public.immobile_proprietari (immobile_id,cliente_id,ordine)
  SELECT i.id,c.id,0 FROM public.immobili i
  JOIN public.clienti c ON c.id::text=i.proprietario_id::text;
-- Salva l'elenco e il principale insieme: niente salvataggi a meta.
CREATE FUNCTION public.rig_salva_proprietari(p_immobile_id text,p_clienti text[])
RETURNS void LANGUAGE plpgsql SECURITY INVOKER SET search_path=public AS $$
DECLARE principale public.clienti%ROWTYPE; n integer;
BEGIN
  IF NOT public.righetto_is_admin_request() THEN RAISE EXCEPTION 'Accesso non autorizzato'; END IF;
  IF coalesce(cardinality(p_clienti),0)=0 THEN RAISE EXCEPTION 'Seleziona almeno un proprietario'; END IF;
  SELECT count(DISTINCT c.id) INTO n FROM public.clienti c WHERE c.id::text=ANY(p_clienti);
  IF n<>cardinality(p_clienti) THEN RAISE EXCEPTION 'Cliente mancante o ripetuto'; END IF;
  PERFORM 1 FROM public.immobili WHERE id::text=p_immobile_id FOR UPDATE;
  IF NOT FOUND THEN RAISE EXCEPTION 'Immobile non trovato'; END IF;
  SELECT * INTO STRICT principale FROM public.clienti WHERE id::text=p_clienti[1];
  DELETE FROM public.immobile_proprietari WHERE immobile_id::text=p_immobile_id;
  INSERT INTO public.immobile_proprietari (immobile_id,cliente_id,ordine)
    SELECT i.id,c.id,(a.pos-1)::integer FROM unnest(p_clienti) WITH ORDINALITY a(cid,pos)
    JOIN public.clienti c ON c.id::text=a.cid
    CROSS JOIN public.immobili i WHERE i.id::text=p_immobile_id;
  UPDATE public.immobili SET proprietario_id=principale.id,
    proprietario_nome=coalesce(nullif(principale.nome,''),principale.ragione_sociale),
    proprietario_tel=principale.telefono,proprietario_email=principale.email
    WHERE id::text=p_immobile_id;
END $$;
REVOKE ALL ON FUNCTION public.rig_salva_proprietari(text,text[]) FROM PUBLIC,anon;
GRANT EXECUTE ON FUNCTION public.rig_salva_proprietari(text,text[]) TO authenticated;
-- Le modifiche dal vecchio modulo restano compatibili e non perdono i comproprietari.
CREATE FUNCTION public.rig_sync_proprietario_principale()
RETURNS trigger LANGUAGE plpgsql SECURITY INVOKER SET search_path=public AS $$
BEGIN
  IF TG_OP='UPDATE' THEN
    IF NEW.proprietario_id IS NOT DISTINCT FROM OLD.proprietario_id THEN RETURN NEW; END IF;
    -- Durante il salvataggio multiplo il nuovo elenco e gia completo.
    IF EXISTS (SELECT 1 FROM public.immobile_proprietari WHERE immobile_id=NEW.id AND cliente_id=NEW.proprietario_id AND ordine=0) THEN RETURN NEW; END IF;
    DELETE FROM public.immobile_proprietari WHERE immobile_id=NEW.id AND cliente_id=OLD.proprietario_id;
  END IF;
  IF NEW.proprietario_id IS NOT NULL THEN
    INSERT INTO public.immobile_proprietari (immobile_id,cliente_id,ordine)
      VALUES (NEW.id,NEW.proprietario_id,0)
      ON CONFLICT (immobile_id,cliente_id) DO UPDATE SET ordine=0;
  END IF;
  RETURN NEW;
END $$;
CREATE TRIGGER rig_sync_proprietario_principale
  AFTER INSERT OR UPDATE OF proprietario_id ON public.immobili
  FOR EACH ROW EXECUTE FUNCTION public.rig_sync_proprietario_principale();
REVOKE ALL ON FUNCTION public.rig_sync_proprietario_principale() FROM PUBLIC,anon;
-- La modifica dei dati in rubrica aggiorna anche i dati copiati del principale.
CREATE FUNCTION public.rig_sync_dati_proprietario()
RETURNS trigger LANGUAGE plpgsql SECURITY INVOKER SET search_path=public AS $$
BEGIN
  UPDATE public.immobili SET
    proprietario_nome=coalesce(nullif(NEW.nome,''),NEW.ragione_sociale),
    proprietario_tel=NEW.telefono,proprietario_email=NEW.email
    WHERE proprietario_id=NEW.id;
  RETURN NEW;
END $$;
CREATE TRIGGER rig_sync_dati_proprietario
  AFTER UPDATE OF nome,ragione_sociale,telefono,email ON public.clienti
  FOR EACH ROW EXECUTE FUNCTION public.rig_sync_dati_proprietario();
REVOKE ALL ON FUNCTION public.rig_sync_dati_proprietario() FROM PUBLIC,anon;
NOTIFY pgrst,'reload schema';
COMMIT;
-- Risultato atteso: Success. Poi ricarica l'admin.
