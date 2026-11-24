-- ============================================================================
-- P1 Portali + mandati + venduti — 24/11/2026
-- File unico da incollare in Supabase → SQL Editor (dopo ok di Gino).
-- Fonte versionata: supabase/migrations/20261124_p1_portali_mandati.sql
-- Guida: docs/p1-portali-mandati-2026-11-24.md
-- ============================================================================

ALTER TABLE public.immobili
  ADD COLUMN IF NOT EXISTS pubblica_immobiliare_it boolean NOT NULL DEFAULT false;

ALTER TABLE public.immobili
  ADD COLUMN IF NOT EXISTS pubblica_idealista boolean NOT NULL DEFAULT false;

COMMENT ON COLUMN public.immobili.pubblica_immobiliare_it IS
  'Se true e annuncio pubblicabile, incluso nel feed XML Immobiliare.it';
COMMENT ON COLUMN public.immobili.pubblica_idealista IS
  'Se true e annuncio pubblicabile, incluso nel feed JSON Idealista (dopo omologazione ILC)';

CREATE INDEX IF NOT EXISTS immobili_incarico_scadenza_idx
  ON public.immobili (incarico_scadenza)
  WHERE incarico_scadenza IS NOT NULL
    AND coalesce(cestino, false) = false;

DROP POLICY IF EXISTS "immobili_public_select" ON public.immobili;
CREATE POLICY "immobili_public_select" ON public.immobili
  FOR SELECT TO anon
  USING (
    coalesce(attivo, false) = true
    AND coalesce(venduto, false) = false
    AND coalesce(affittato, false) = false
    AND coalesce(cestino, false) = false
  );
