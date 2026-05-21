-- Bozze social: approvazione manuale in admin → poi riga in pianificazioni.
-- Esegui in Supabase → SQL Editor.

CREATE TABLE IF NOT EXISTS public.bozze_social (
  id                         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  stato                      text NOT NULL DEFAULT 'bozza',
  tipo_canale                text NOT NULL DEFAULT 'facebook_post',
  fonte                      text NOT NULL DEFAULT 'immobile',
  titolo                     text NOT NULL,
  corpo                      text,
  hashtags                   text[] NOT NULL DEFAULT '{}',
  link_pagina                text,
  media_direct_url           text,
  riferimento_id             text,
  data_pubblicazione_proposta date,
  ora_proposta               text NOT NULL DEFAULT '12:30',
  note                       text,
  meta                       jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at                 timestamptz NOT NULL DEFAULT now(),
  updated_at                 timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_bozze_social_stato ON public.bozze_social (stato, created_at DESC);

COMMENT ON TABLE public.bozze_social IS 'Bozze post social in attesa di approvazione admin';

ALTER TABLE public.bozze_social ENABLE ROW LEVEL SECURITY;

CREATE POLICY "bozze_social_anon_select"
  ON public.bozze_social FOR SELECT TO anon USING (true);

CREATE POLICY "bozze_social_anon_insert"
  ON public.bozze_social FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "bozze_social_anon_update"
  ON public.bozze_social FOR UPDATE TO anon USING (true) WITH CHECK (true);

CREATE POLICY "bozze_social_anon_delete"
  ON public.bozze_social FOR DELETE TO anon USING (true);

CREATE POLICY "bozze_social_authenticated_all"
  ON public.bozze_social FOR ALL TO authenticated USING (true) WITH CHECK (true);
