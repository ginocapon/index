-- Cache ultimi contenuti pubblicati su Instagram Business (Graph: /{ig-user-id}/media).
-- Esegui su Supabase SQL Editor. Poi: python sync_instagram_feed.py

CREATE TABLE IF NOT EXISTS instagram_feed_cache (
  id             bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  media_id       text NOT NULL UNIQUE,
  caption        text,
  permalink      text,
  media_url      text,
  thumbnail_url  text,
  media_type     text,
  timestamp      timestamptz,
  synced_at      timestamptz NOT NULL DEFAULT now(),
  raw            jsonb
);

CREATE INDEX IF NOT EXISTS idx_instagram_feed_cache_ts ON instagram_feed_cache ("timestamp" DESC NULLS LAST);

ALTER TABLE instagram_feed_cache ENABLE ROW LEVEL SECURITY;

CREATE POLICY "instagram_feed_cache_anon_select"
  ON instagram_feed_cache FOR SELECT
  TO anon
  USING (true);

COMMENT ON TABLE instagram_feed_cache IS 'Snapshot ultimi media IG da Graph API; aggiornare con sync_instagram_feed.py';
