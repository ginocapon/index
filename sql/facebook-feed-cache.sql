-- Cache ultimi post pubblicati dalla Pagina Facebook (popolata da righetto_social/sync_facebook_feed.py).
-- Esegui su Supabase SQL Editor. Poi: python sync_facebook_feed.py

CREATE TABLE IF NOT EXISTS facebook_feed_cache (
  id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  post_id       text NOT NULL UNIQUE,
  message       text,
  permalink_url text,
  picture_url   text,
  created_time  timestamptz,
  status_type   text,
  synced_at     timestamptz NOT NULL DEFAULT now(),
  raw           jsonb
);

CREATE INDEX IF NOT EXISTS idx_facebook_feed_cache_created ON facebook_feed_cache (created_time DESC NULLS LAST);

ALTER TABLE facebook_feed_cache ENABLE ROW LEVEL SECURITY;

-- Lettura da admin.html (chiave anon nel client). Scrittura solo con service_role / chiave server (RLS bypass).
CREATE POLICY "facebook_feed_cache_anon_select"
  ON facebook_feed_cache FOR SELECT
  TO anon
  USING (true);

COMMENT ON TABLE facebook_feed_cache IS 'Snapshot ultimi post Pagina FB da Graph API published_posts; aggiornare con sync_facebook_feed.py';
