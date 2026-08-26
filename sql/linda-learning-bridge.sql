-- LINDA Learning Bridge — tabelle Supabase (modulo opzionale)
-- NON modifica immobili né dati di catalogo. Solo osservazione e insight.

CREATE TABLE IF NOT EXISTS linda_learning_events (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  event_type TEXT NOT NULL,
  session_id TEXT,
  search_id TEXT,
  page_path TEXT,
  source TEXT DEFAULT 'linda_chatbot',
  payload JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_linda_learning_events_type ON linda_learning_events (event_type);
CREATE INDEX IF NOT EXISTS idx_linda_learning_events_created ON linda_learning_events (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_linda_learning_events_search ON linda_learning_events (search_id);

CREATE TABLE IF NOT EXISTS linda_learning_aggregates (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  period_start TIMESTAMPTZ,
  period_end TIMESTAMPTZ,
  bucket_key TEXT,
  metrics JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS linda_ranking_insights (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  insight_id TEXT NOT NULL,
  text TEXT NOT NULL,
  sample_size INT NOT NULL DEFAULT 0,
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0,
  period JSONB,
  evidence JSONB,
  disclaimer TEXT
);

CREATE TABLE IF NOT EXISTS linda_ranking_versions (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ranking_version TEXT NOT NULL UNIQUE,
  features JSONB NOT NULL DEFAULT '{}'::jsonb,
  weights JSONB NOT NULL DEFAULT '{}'::jsonb,
  sample_size INT NOT NULL DEFAULT 0,
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'proposed',
  metrics_before JSONB,
  metrics_after JSONB
);

-- RLS: insert anonimo eventi (no PII obbligatoria), read solo admin
ALTER TABLE linda_learning_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE linda_learning_aggregates ENABLE ROW LEVEL SECURITY;
ALTER TABLE linda_ranking_insights ENABLE ROW LEVEL SECURITY;
ALTER TABLE linda_ranking_versions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS linda_learning_events_insert_anon ON linda_learning_events;
CREATE POLICY linda_learning_events_insert_anon ON linda_learning_events
  FOR INSERT TO anon WITH CHECK (true);

DROP POLICY IF EXISTS linda_learning_events_select_admin ON linda_learning_events;
CREATE POLICY linda_learning_events_select_admin ON linda_learning_events
  FOR SELECT TO authenticated USING (true);

COMMENT ON TABLE linda_learning_events IS 'Eventi normalizzati LINDA Learning Bridge — no PII';
