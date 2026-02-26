/**
 * RIGHETTO IMMOBILIARE — Configurazione Servizi Esterni
 *
 * Istruzioni:
 * 1. FORMSPREE: Registrati su https://formspree.io → Crea un form → Copia il Form ID
 * 2. BREVO: Registrati su https://brevo.com → Crea lista contatti → Crea form iscrizione
 */

const SERVIZI_CONFIG = {
  // ── FORMSPREE ──────────────────────────────────────────
  // Ricevi un'email ogni volta che qualcuno compila il form di contatto
  // Vai su https://formspree.io → New Form → copia l'ID (es: "xrgjayzk")
  FORMSPREE_ID: 'IL_TUO_FORM_ID',

  // ── BREVO (ex Sendinblue) ──────────────────────────────
  // Newsletter per nuovi immobili e articoli del blog
  // Vai su https://brevo.com → Contatti → Liste → Crea lista
  // Poi: Contatti → Form → Crea form → copia l'URL di azione
  BREVO_FORM_URL: ''
};
