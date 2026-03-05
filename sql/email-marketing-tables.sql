-- ═══════════════════════════════════════════════════════════════
-- RIGHETTO IMMOBILIARE — Email Marketing Pro
-- Esegui questo SQL nel Supabase Dashboard → SQL Editor
-- ═══════════════════════════════════════════════════════════════

-- 1. Campagne email
CREATE TABLE IF NOT EXISTS campagne_email (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    oggetto TEXT NOT NULL,
    preheader TEXT,
    corpo_html TEXT NOT NULL,
    mittente_email TEXT DEFAULT 'info@righetto-immobiliare.it',
    mittente_nome TEXT DEFAULT 'Righetto Immobiliare',
    reply_to TEXT DEFAULT 'info@righetto-immobiliare.it',
    stato TEXT DEFAULT 'bozza' CHECK (stato IN ('bozza','in_coda','in_invio','completata','annullata')),
    totale_destinatari INT DEFAULT 0,
    inviati INT DEFAULT 0,
    aperti INT DEFAULT 0,
    click INT DEFAULT 0,
    bounce INT DEFAULT 0,
    disiscritti INT DEFAULT 0,
    errori INT DEFAULT 0,
    pianificata_per TIMESTAMPTZ,
    iniziata_il TIMESTAMPTZ,
    completata_il TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Coda email singole
CREATE TABLE IF NOT EXISTS coda_email (
    id BIGSERIAL PRIMARY KEY,
    campagna_id BIGINT REFERENCES campagne_email(id) ON DELETE CASCADE,
    destinatario_email TEXT NOT NULL,
    destinatario_nome TEXT,
    oggetto TEXT NOT NULL,
    corpo_html TEXT NOT NULL,
    stato TEXT DEFAULT 'in_coda' CHECK (stato IN ('in_coda','inviata','errore','bounce')),
    tentativo INT DEFAULT 0,
    errore_msg TEXT,
    inviata_il TIMESTAMPTZ,
    aperta_il TIMESTAMPTZ,
    click_il TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Blacklist (disiscrizioni e bounce)
CREATE TABLE IF NOT EXISTS email_blacklist (
    id BIGSERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    motivo TEXT DEFAULT 'disiscrizione' CHECK (motivo IN ('disiscrizione','bounce','spam','manuale')),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 4. Tracking eventi email
CREATE TABLE IF NOT EXISTS email_tracking (
    id BIGSERIAL PRIMARY KEY,
    coda_email_id BIGINT REFERENCES coda_email(id) ON DELETE CASCADE,
    campagna_id BIGINT REFERENCES campagne_email(id) ON DELETE CASCADE,
    tipo TEXT NOT NULL CHECK (tipo IN ('apertura','click','disiscrizione','bounce')),
    ip TEXT,
    user_agent TEXT,
    url_cliccato TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 5. Configurazione SMTP
CREATE TABLE IF NOT EXISTS smtp_config (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT DEFAULT 'default',
    host TEXT NOT NULL,
    porta INT DEFAULT 587,
    utente TEXT NOT NULL,
    password TEXT NOT NULL,
    use_tls BOOLEAN DEFAULT true,
    mittente_email TEXT NOT NULL,
    mittente_nome TEXT DEFAULT 'Righetto Immobiliare',
    max_per_ora INT DEFAULT 50,
    max_per_giorno INT DEFAULT 300,
    attivo BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 6. Gruppi personalizzati per email marketing (stile Brevo)
CREATE TABLE IF NOT EXISTS gruppi_email (
    id TEXT PRIMARY KEY DEFAULT 'g_' || extract(epoch from now())::bigint::text,
    nome TEXT NOT NULL UNIQUE,
    colore TEXT DEFAULT '#667eea',
    contatti TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE gruppi_email ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow all for anon" ON gruppi_email FOR ALL USING (true) WITH CHECK (true);

-- Aggiungi colonna gruppo a campagne_email (se non esiste)
DO $$ BEGIN
    ALTER TABLE campagne_email ADD COLUMN IF NOT EXISTS gruppo TEXT DEFAULT 'tutti';
EXCEPTION WHEN others THEN NULL;
END $$;

-- ═══ INDICI per performance ═══
CREATE INDEX IF NOT EXISTS idx_coda_email_stato ON coda_email(stato);
CREATE INDEX IF NOT EXISTS idx_coda_email_campagna ON coda_email(campagna_id);
CREATE INDEX IF NOT EXISTS idx_email_blacklist_email ON email_blacklist(email);
CREATE INDEX IF NOT EXISTS idx_email_tracking_campagna ON email_tracking(campagna_id);
CREATE INDEX IF NOT EXISTS idx_email_tracking_tipo ON email_tracking(tipo);

-- ═══ RLS Policies ═══
ALTER TABLE campagne_email ENABLE ROW LEVEL SECURITY;
ALTER TABLE coda_email ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_blacklist ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_tracking ENABLE ROW LEVEL SECURITY;
ALTER TABLE smtp_config ENABLE ROW LEVEL SECURITY;

-- Permetti tutto per anon (admin panel)
CREATE POLICY "Allow all for anon" ON campagne_email FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON coda_email FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON email_blacklist FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON email_tracking FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all for anon" ON smtp_config FOR ALL USING (true) WITH CHECK (true);

-- ═══ FUNZIONE: Aggiungi alla blacklist e rimuovi da coda ═══
CREATE OR REPLACE FUNCTION disiscrivi_email(p_email TEXT, p_motivo TEXT DEFAULT 'disiscrizione')
RETURNS void AS $$
BEGIN
    INSERT INTO email_blacklist (email, motivo)
    VALUES (LOWER(TRIM(p_email)), p_motivo)
    ON CONFLICT (email) DO NOTHING;

    -- Rimuovi dalla coda futura
    DELETE FROM coda_email
    WHERE LOWER(destinatario_email) = LOWER(TRIM(p_email))
    AND stato = 'in_coda';
END;
$$ LANGUAGE plpgsql;

-- ═══ FUNZIONE: Statistiche campagna ═══
CREATE OR REPLACE FUNCTION stats_campagna(p_campagna_id BIGINT)
RETURNS TABLE(
    totale INT,
    inviati INT,
    aperti INT,
    click INT,
    bounce INT,
    errori INT,
    tasso_apertura NUMERIC,
    tasso_click NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(*)::INT as totale,
        COUNT(*) FILTER (WHERE ce.stato = 'inviata')::INT as inviati,
        COUNT(DISTINCT ce.id) FILTER (WHERE ce.aperta_il IS NOT NULL)::INT as aperti,
        COUNT(DISTINCT ce.id) FILTER (WHERE ce.click_il IS NOT NULL)::INT as click,
        COUNT(*) FILTER (WHERE ce.stato = 'bounce')::INT as bounce,
        COUNT(*) FILTER (WHERE ce.stato = 'errore')::INT as errori,
        CASE WHEN COUNT(*) FILTER (WHERE ce.stato = 'inviata') > 0
            THEN ROUND(COUNT(DISTINCT ce.id) FILTER (WHERE ce.aperta_il IS NOT NULL)::NUMERIC / COUNT(*) FILTER (WHERE ce.stato = 'inviata') * 100, 1)
            ELSE 0 END as tasso_apertura,
        CASE WHEN COUNT(*) FILTER (WHERE ce.stato = 'inviata') > 0
            THEN ROUND(COUNT(DISTINCT ce.id) FILTER (WHERE ce.click_il IS NOT NULL)::NUMERIC / COUNT(*) FILTER (WHERE ce.stato = 'inviata') * 100, 1)
            ELSE 0 END as tasso_click
    FROM coda_email ce
    WHERE ce.campagna_id = p_campagna_id;
END;
$$ LANGUAGE plpgsql;

-- ═══ INSERISCI CONFIG SMTP DI DEFAULT ═══
-- IMPORTANTE: Modifica host/utente/password con i dati del tuo provider email
INSERT INTO smtp_config (nome, host, porta, utente, password, use_tls, mittente_email, mittente_nome, max_per_ora, max_per_giorno)
VALUES (
    'default',
    'smtps.aruba.it',     -- Cambia con il tuo SMTP (es: smtp.gmail.com, smtp.office365.com)
    465,                   -- 587 per STARTTLS, 465 per SSL
    'info@righetto-immobiliare.it',  -- Tuo indirizzo email
    'LA_TUA_PASSWORD',     -- ⚠️ CAMBIA CON LA TUA PASSWORD
    true,
    'info@righetto-immobiliare.it',
    'Righetto Immobiliare',
    50,    -- Max email per ora (warm-up: inizia basso)
    300    -- Max email per giorno
)
ON CONFLICT DO NOTHING;
