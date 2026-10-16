-- Aste immobiliari Veneto — archivio annunci per la pagina admin "Aste"
-- Esegui in Supabase → SQL Editor
-- Fonte dati: Portale delle Vendite Pubbliche (Ministero) + foto da aggregatore pubblico.
-- Accesso: SOLO admin (stessa protezione delle altre tabelle admin).

CREATE TABLE IF NOT EXISTS public.aste_immobili (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  id_pvp bigint NOT NULL UNIQUE,              -- id annuncio sul Portale Vendite Pubbliche
  prezzo_base numeric(12,2),
  offerta_minima numeric(12,2),
  rialzo_minimo numeric(12,2),
  data_asta timestamptz,                      -- data/ora vendita (o udienza)
  termine_offerte timestamptz,                -- termine presentazione offerte
  data_pubblicazione date,
  comune text DEFAULT '',
  provincia text DEFAULT '',
  indirizzo text DEFAULT '',
  latitudine double precision,
  longitudine double precision,
  descrizione text DEFAULT '',
  tipologia_bene text DEFAULT '',             -- es. "Abitazione Di Tipo Civile"
  disponibilita text DEFAULT '',              -- libero / occupato / non specificata
  tribunale text DEFAULT '',
  procedura text DEFAULT '',                  -- es. "119/2025"
  modalita_vendita text DEFAULT '',
  link_dettaglio text DEFAULT '',             -- pagina ufficiale PVP
  documenti jsonb NOT NULL DEFAULT '[]'::jsonb,  -- [{nome, url, tipo, dimensione}]
  foto_url text DEFAULT '',                   -- foto principale (aggregatore), se trovata
  foto_fonte text DEFAULT '',
  note_admin text DEFAULT '',                 -- note private di Gino
  attivo boolean NOT NULL DEFAULT true,       -- false = asta passata/annullata
  hash_cambio text DEFAULT '',                -- per rilevare aggiornamenti al sync
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS aste_immobili_data_idx ON public.aste_immobili (attivo, data_asta);
CREATE INDEX IF NOT EXISTS aste_immobili_geo_idx ON public.aste_immobili (provincia, comune);
CREATE INDEX IF NOT EXISTS aste_immobili_prezzo_idx ON public.aste_immobili (prezzo_base);

ALTER TABLE public.aste_immobili ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "aste_immobili_admin_all" ON public.aste_immobili;
CREATE POLICY "aste_immobili_admin_all"
  ON public.aste_immobili FOR ALL TO anon
  USING (public.righetto_is_admin_request())
  WITH CHECK (public.righetto_is_admin_request());

-- Nessuna policy pubblica: solo admin (le perizie contengono dati personali dei debitori).
