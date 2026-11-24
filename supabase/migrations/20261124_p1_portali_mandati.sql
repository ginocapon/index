-- P1 2026-11-24 — Flag pubblicazione portali + RLS pubblico senza venduti/affittati
-- Applicare a mano in Supabase SQL Editor (NON da CI).
-- Istruzioni: docs/p1-portali-mandati-2026-11-24.md

-- 1) Flag per-immobile: includi nel feed Immobiliare.it / Idealista
ALTER TABLE public.immobili
  ADD COLUMN IF NOT EXISTS pubblica_immobiliare_it boolean NOT NULL DEFAULT false;

ALTER TABLE public.immobili
  ADD COLUMN IF NOT EXISTS pubblica_idealista boolean NOT NULL DEFAULT false;

COMMENT ON COLUMN public.immobili.pubblica_immobiliare_it IS
  'Se true e annuncio pubblicabile, incluso nel feed XML Immobiliare.it';
COMMENT ON COLUMN public.immobili.pubblica_idealista IS
  'Se true e annuncio pubblicabile, incluso nel feed JSON Idealista (dopo omologazione ILC)';

-- 2) Indice scadenze mandato (alert dashboard)
CREATE INDEX IF NOT EXISTS immobili_incarico_scadenza_idx
  ON public.immobili (incarico_scadenza)
  WHERE incarico_scadenza IS NOT NULL
    AND coalesce(cestino, false) = false;

-- 3) Sito pubblico: solo attivi, non venduti, non affittati, non in cestino
DROP POLICY IF EXISTS "immobili_public_select" ON public.immobili;
CREATE POLICY "immobili_public_select" ON public.immobili
  FOR SELECT TO anon
  USING (
    coalesce(attivo, false) = true
    AND coalesce(venduto, false) = false
    AND coalesce(affittato, false) = false
    AND coalesce(cestino, false) = false
  );

-- Admin autenticato: lettura/scrittura invariata (policy admin esistenti restano)
