# Sicurezza admin - 19/10/2026
- Login admin con Supabase Auth (email + password). Tolti: password in pagina, scorciatoia reset2fa, chiave RIG_ADMIN_RLS_SECRET e intestazione x-righetto-admin.
- Edge function send-email: send_single e process_queue solo per l'utente con id = segreto ADMIN_UID; MAIL_RELAY_KEY solo da segreti, nessun valore di riserva.
- api/send-mail.php: chiave letta da relay-secret.php (creato a mano su cPanel, ignorato da git).
- Workflow static.yml: tolto il passo che iniettava la password.
- Le vecchie chiavi restano nella storia git pubblica: per questo vanno ruotate (SQL blocco + nuova MAIL_RELAY_KEY).
- Gli script scripts/update_lf0353_*.py e scripts/migrate_supabase_media.py leggevano la chiave da admin.html: non funzionano piu' finche' non vengono adeguati.
