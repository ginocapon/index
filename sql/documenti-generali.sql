-- Documenti Generali — archivio contratti e riferimenti operativi (admin)
-- Esegui in Supabase → SQL Editor

CREATE TABLE IF NOT EXISTS public.documenti_generali (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  titolo text NOT NULL DEFAULT '',
  tipo text NOT NULL DEFAULT 'documento' CHECK (tipo IN ('riferimento', 'documento')),
  ordine integer NOT NULL DEFAULT 0,
  link_url text DEFAULT '',
  note text DEFAULT '',
  file jsonb NOT NULL DEFAULT '[]'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS documenti_generali_ordine_idx ON public.documenti_generali (tipo, ordine);

ALTER TABLE public.documenti_generali ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "documenti_generali_admin_all" ON public.documenti_generali;
CREATE POLICY "documenti_generali_admin_all"
  ON public.documenti_generali FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

-- Nessuna policy pubblica: solo admin
