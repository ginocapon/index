-- Event type retirement. Installing the functions does not change event or type rows.
BEGIN;
CREATE OR REPLACE FUNCTION public.agenda_protect_types()
RETURNS trigger LANGUAGE plpgsql SET search_path=public AS $$
BEGIN
 IF TG_OP='DELETE' THEN RAISE EXCEPTION 'Usa Elimina tipo: gli appuntamenti devono restare collegati'; END IF;
 IF OLD.id='gi-6' AND (NEW.id IS DISTINCT FROM OLD.id OR NEW.name IS DISTINCT FROM OLD.name OR NEW.active IS NOT TRUE) THEN
  RAISE EXCEPTION 'Il tipo altro deve restare disponibile';
 END IF;
 IF OLD.active IS FALSE AND NEW.active IS TRUE THEN RAISE EXCEPTION 'Un tipo eliminato non puo essere riattivato'; END IF;
 RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS agenda_protect_types ON public.agenda_event_types;
CREATE TRIGGER agenda_protect_types BEFORE UPDATE OR DELETE ON public.agenda_event_types FOR EACH ROW EXECUTE FUNCTION public.agenda_protect_types();

CREATE OR REPLACE FUNCTION public.agenda_route_retired_type()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path=public AS $$
DECLARE current_active boolean;
BEGIN
 SELECT active INTO current_active FROM public.agenda_event_types WHERE id=NEW.type_id FOR SHARE;
 IF NOT FOUND THEN RAISE EXCEPTION 'Tipo evento non disponibile'; END IF;
 IF current_active IS FALSE THEN
  PERFORM 1 FROM public.agenda_event_types WHERE id='gi-6' AND active IS TRUE FOR SHARE;
  IF NOT FOUND THEN RAISE EXCEPTION 'Il tipo altro non e disponibile'; END IF;
  NEW.type_id:='gi-6';
 END IF;
 RETURN NEW;
END $$;
DROP TRIGGER IF EXISTS agenda_route_retired_type ON public.agenda_events;
CREATE TRIGGER agenda_route_retired_type BEFORE INSERT OR UPDATE ON public.agenda_events FOR EACH ROW EXECUTE FUNCTION public.agenda_route_retired_type();

CREATE OR REPLACE FUNCTION public.agenda_retire_type(p_type_id text,p_expected_name text)
RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER SET search_path=public SET lock_timeout='3s' AS $$
DECLARE t public.agenda_event_types%ROWTYPE; moved bigint; trashed bigint;
BEGIN
 IF auth.uid() IS NULL OR NOT public.righetto_is_admin_request() THEN RAISE EXCEPTION 'Operazione riservata all amministratore'; END IF;
 IF p_type_id IS NULL OR p_type_id='gi-6' THEN RAISE EXCEPTION 'Il tipo altro non puo essere eliminato'; END IF;
 -- Serialize with writers before locking types: all matching rows are converted in one transaction.
 LOCK TABLE public.agenda_events IN SHARE ROW EXCLUSIVE MODE;
 PERFORM 1 FROM public.agenda_event_types WHERE id IN(p_type_id,'gi-6') ORDER BY id FOR UPDATE;
 SELECT * INTO t FROM public.agenda_event_types WHERE id=p_type_id;
 IF NOT FOUND OR t.active IS NOT TRUE OR t.name IS DISTINCT FROM p_expected_name THEN RAISE EXCEPTION 'Elenco tipi cambiato: riapri Gestisci tipi'; END IF;
 PERFORM 1 FROM public.agenda_event_types WHERE id='gi-6' AND name='altro' AND active IS TRUE;
 IF NOT FOUND THEN RAISE EXCEPTION 'Il tipo altro non e disponibile'; END IF;
 -- No cross-account edits to private appointments, including trash. Roll back the whole operation.
 IF EXISTS(SELECT 1 FROM public.agenda_events WHERE type_id=p_type_id AND personal IS TRUE AND created_by IS DISTINCT FROM auth.uid()) THEN
  RAISE EXCEPTION 'Operazione non eseguita: questo tipo ha appuntamenti privati non modificabili dalla sessione corrente';
 END IF;
 SELECT count(*) INTO trashed FROM public.agenda_events WHERE type_id=p_type_id AND deleted_at IS NOT NULL;
 UPDATE public.agenda_events SET type_id='gi-6' WHERE type_id=p_type_id;
 GET DIAGNOSTICS moved=ROW_COUNT;
 UPDATE public.agenda_event_types SET active=false WHERE id=p_type_id;
 RETURN jsonb_build_object('type_id',p_type_id,'moved',moved,'in_trash',trashed,'replacement','gi-6');
END $$;
REVOKE ALL ON FUNCTION public.agenda_protect_types() FROM PUBLIC,anon,authenticated;
REVOKE ALL ON FUNCTION public.agenda_route_retired_type() FROM PUBLIC,anon,authenticated;
REVOKE ALL ON FUNCTION public.agenda_retire_type(text,text) FROM PUBLIC,anon;
GRANT EXECUTE ON FUNCTION public.agenda_retire_type(text,text) TO authenticated;
COMMIT;
