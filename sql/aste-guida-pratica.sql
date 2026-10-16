-- Guida partecipazione aste — spazio privato di Gino
-- Esegui in Supabase → SQL Editor
-- Cosa fa: (1) due tabelle per salvare lo stato della checklist guida aste
-- (2) uno spazio file PRIVATO (bucket "aste-pratica") per i PDF che Gino carica.
-- Accesso: SOLO admin, come le altre tabelle riservate (stessa protezione).
-- Nessun dato pubblico: i documenti caricati non sono raggiungibili dai visitatori.

-- ── 1. Tabella: pratiche (una per asta a cui Gino partecipa) ──
CREATE TABLE IF NOT EXISTS public.aste_guida_pratiche (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  titolo text NOT NULL DEFAULT '',            -- es. "Appartamento Padova, asta 12/11"
  link_annuncio text DEFAULT '',
  modalita text DEFAULT '',                   -- asincrona / sincrona / sincrona mista
  created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE public.aste_guida_pratiche ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "aste_guida_pratiche_admin_all" ON public.aste_guida_pratiche;
CREATE POLICY "aste_guida_pratiche_admin_all"
  ON public.aste_guida_pratiche FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

-- ── 2. Tabella: passi della checklist (stato + file allegato) ──
CREATE TABLE IF NOT EXISTS public.aste_guida_passi (
  pratica_id uuid NOT NULL REFERENCES public.aste_guida_pratiche(id) ON DELETE CASCADE,
  step_key text NOT NULL,                     -- es. "pec", "cauzione", "offerta"
  fatto boolean NOT NULL DEFAULT false,
  note text DEFAULT '',
  file_path text DEFAULT '',                  -- percorso nel bucket privato
  file_nome text DEFAULT '',                  -- nome originale del PDF
  updated_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (pratica_id, step_key)
);

ALTER TABLE public.aste_guida_passi ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "aste_guida_passi_admin_all" ON public.aste_guida_passi;
CREATE POLICY "aste_guida_passi_admin_all"
  ON public.aste_guida_passi FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

-- ── 3. Spazio file privato per i documenti della pratica ──
INSERT INTO storage.buckets (id, name, public)
VALUES ('aste-pratica', 'aste-pratica', false)
ON CONFLICT (id) DO UPDATE SET public = false;

-- Solo admin può vedere, caricare, modificare, cancellare i file di questo spazio.
DROP POLICY IF EXISTS "aste_pratica_admin_select" ON storage.objects;
CREATE POLICY "aste_pratica_admin_select"
  ON storage.objects FOR SELECT TO anon
  USING (bucket_id = 'aste-pratica' AND public.righetto_is_admin_request());

DROP POLICY IF EXISTS "aste_pratica_admin_insert" ON storage.objects;
CREATE POLICY "aste_pratica_admin_insert"
  ON storage.objects FOR INSERT TO anon
  WITH CHECK (bucket_id = 'aste-pratica' AND public.righetto_is_admin_request());

DROP POLICY IF EXISTS "aste_pratica_admin_update" ON storage.objects;
CREATE POLICY "aste_pratica_admin_update"
  ON storage.objects FOR UPDATE TO anon
  USING (bucket_id = 'aste-pratica' AND public.righetto_is_admin_request())
  WITH CHECK (bucket_id = 'aste-pratica' AND public.righetto_is_admin_request());

DROP POLICY IF EXISTS "aste_pratica_admin_delete" ON storage.objects;
CREATE POLICY "aste_pratica_admin_delete"
  ON storage.objects FOR DELETE TO anon
  USING (bucket_id = 'aste-pratica' AND public.righetto_is_admin_request());
