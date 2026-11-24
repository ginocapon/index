/**
 * Gate for internal HTML pages (scraping, bookmarklet helper).
 * Shows content only after Supabase Auth + righetto_is_admin_request().
 */
import { decideAccess } from './access-gate.mjs';

const SB_URL = 'https://qwkwkemuabfwvwuqrxlu.supabase.co';
const SB_ANON =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc';

function lib() {
  return window.rigSupabaseLib || window.supabase;
}

export async function gateInternalPage({
  contentSelector = '[data-internal-content]',
  gateSelector = '[data-internal-gate]',
  loginHref = '/admin',
} = {}) {
  const content = document.querySelector(contentSelector);
  const gate = document.querySelector(gateSelector);
  if (!content || !gate) return { kind: 'missing-dom' };

  const showGate = (msg) => {
    content.hidden = true;
    gate.hidden = false;
    const status = gate.querySelector('[data-internal-gate-status]');
    if (status && msg) status.textContent = msg;
  };
  const showContent = () => {
    gate.hidden = true;
    content.hidden = false;
  };

  const Sb = lib();
  if (!Sb?.createClient) {
    showGate('Libreria di accesso non caricata. Ricarica la pagina o apri il pannello admin.');
    return { kind: 'unavailable' };
  }

  const sb = Sb.createClient(SB_URL, SB_ANON, {
    auth: { persistSession: true, autoRefreshToken: true },
  });

  try {
    const { data, error } = await sb.auth.getSession();
    if (error) {
      showGate('Connessione da verificare. Riprova tra poco.');
      return { kind: 'unavailable' };
    }
    if (!data?.session) {
      showGate('Accesso riservato al team. Accedi dal pannello admin, poi ripeti questa pagina.');
      const link = gate.querySelector('a[data-internal-login]');
      if (link) link.href = loginHref;
      return { kind: 'denied' };
    }
    const access = await decideAccess(sb);
    if (access.kind !== 'admin') {
      showGate(
        access.kind === 'unavailable'
          ? 'Connessione da verificare. Riprova senza cambiare password.'
          : 'Questo account non è abilitato come amministratore.'
      );
      await sb.auth.signOut().catch(() => {});
      return { kind: 'denied' };
    }
    showContent();
    return { kind: 'admin', id: access.id };
  } catch {
    showGate('Controllo accesso non riuscito. Riprova.');
    return { kind: 'unavailable' };
  }
}
