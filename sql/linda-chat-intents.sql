-- Linda chat intents — log anonimo per question intelligence (privacy minimization)
-- Esegui in Supabase SQL Editor. Dopo deploy: verificare INSERT anon da sito.

CREATE TABLE IF NOT EXISTS public.linda_chat_intents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at timestamptz NOT NULL DEFAULT now(),
  intent_type text NOT NULL CHECK (intent_type IN (
    'faq', 'search', 'stima', 'contatto', 'ricerca_guidata', 'saluto', 'lead', 'default'
  )),
  topic_label text,
  operation text,
  location text,
  budget_band text,
  rooms_min smallint,
  property_type text,
  hard_constraints jsonb DEFAULT '{}'::jsonb,
  soft_preferences jsonb DEFAULT '{}'::jsonb,
  msg_hash text NOT NULL,
  msg_length smallint,
  pagina text,
  session_bucket text
);

CREATE INDEX IF NOT EXISTS linda_chat_intents_created_at_idx
  ON public.linda_chat_intents (created_at DESC);

CREATE INDEX IF NOT EXISTS linda_chat_intents_topic_label_idx
  ON public.linda_chat_intents (topic_label);

CREATE INDEX IF NOT EXISTS linda_chat_intents_intent_type_idx
  ON public.linda_chat_intents (intent_type);

ALTER TABLE public.linda_chat_intents ENABLE ROW LEVEL SECURITY;

-- Sito: solo INSERT anon (nessuna lettura elenco)
DROP POLICY IF EXISTS "linda_intents_public_insert" ON public.linda_chat_intents;
CREATE POLICY "linda_intents_public_insert"
  ON public.linda_chat_intents FOR INSERT TO anon
  WITH CHECK (true);

-- Admin: lettura/gestione con header x-righetto-admin
DROP POLICY IF EXISTS "linda_intents_admin_all" ON public.linda_chat_intents;
CREATE POLICY "linda_intents_admin_all"
  ON public.linda_chat_intents FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

COMMENT ON TABLE public.linda_chat_intents IS
  'Intent Linda anonimi — no testo messaggio, solo hash e metadati aggregabili (AI Act / privacy).';
