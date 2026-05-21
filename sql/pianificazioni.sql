-- Tabella agenda social (admin.html + publish_from_agenda.py).
-- Esegui in Supabase → SQL Editor.

CREATE TABLE IF NOT EXISTS public.pianificazioni (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tipo             text NOT NULL DEFAULT 'facebook_post',
  contenuto        text NOT NULL DEFAULT 'immobile',
  titolo           text NOT NULL,
  riferimento_id   text,
  ora              text NOT NULL DEFAULT '12:30',
  giorni           integer[] NOT NULL DEFAULT '{}',
  data_inizio      date NOT NULL,
  data_fine        date NOT NULL,
  keywords         text[] NOT NULL DEFAULT '{}',
  note             text,
  link_media       text,
  corpo_spintax    text,
  media_direct_url text,
  created_at       timestamptz NOT NULL DEFAULT now(),
  updated_at       timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_pianificazioni_date_range ON public.pianificazioni (data_inizio, data_fine);
CREATE INDEX IF NOT EXISTS idx_pianificazioni_created ON public.pianificazioni (created_at DESC);

COMMENT ON TABLE public.pianificazioni IS 'Agenda pubblicazioni social; letta da publish_from_agenda.py';

ALTER TABLE public.pianificazioni ENABLE ROW LEVEL SECURITY;

-- Admin usa chiave anon nel browser (come altre tabelle del progetto).
CREATE POLICY "pianificazioni_anon_select"
  ON public.pianificazioni FOR SELECT TO anon USING (true);

CREATE POLICY "pianificazioni_anon_insert"
  ON public.pianificazioni FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "pianificazioni_anon_update"
  ON public.pianificazioni FOR UPDATE TO anon USING (true) WITH CHECK (true);

CREATE POLICY "pianificazioni_anon_delete"
  ON public.pianificazioni FOR DELETE TO anon USING (true);

-- Opzionale: consenti anche authenticated se in futuro usi login Supabase
CREATE POLICY "pianificazioni_authenticated_all"
  ON public.pianificazioni FOR ALL TO authenticated USING (true) WITH CHECK (true);
