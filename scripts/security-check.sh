#!/bin/bash
# ============================================================
# SECURITY CHECK — Righetto Immobiliare
# Controlli statici su segreti, admin, RLS docs, security.txt
# Eseguire 2×/settimana (martedì + venerdì) — vedi skill-security.md
# ============================================================

set -u

REPORT_FILE="${1:-security-report.md}"
ERRORS=0
WARNINGS=0
OK=0
TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M UTC')

log_ok()   { OK=$((OK+1));       echo "  ✅ $1" >> "$REPORT_FILE"; }
log_warn() { WARNINGS=$((WARNINGS+1)); echo "  ⚠️ $1" >> "$REPORT_FILE"; }
log_err()  { ERRORS=$((ERRORS+1));      echo "  ❌ $1" >> "$REPORT_FILE"; }

cat > "$REPORT_FILE" <<EOF
# 🔒 Security Check — Righetto Immobiliare
**Data:** $TIMESTAMP
**Skill:** TEST-SKILL/skill-security.md

EOF

echo "## 1. Segreti nel repository" >> "$REPORT_FILE"

# .env tracciato da git
if git ls-files --error-unmatch righetto_social/.env >/dev/null 2>&1; then
  log_err "righetto_social/.env è tracciato da git — rimuovere subito"
else
  log_ok "righetto_social/.env non in git"
fi

# service_role in file tracciati (pattern grezzo)
if git grep -l 'service_role' -- '*.js' '*.html' '*.ts' '*.py' 2>/dev/null | grep -v '.env.example' | grep -q .; then
  log_err "Possibile service_role in file sorgente tracciati"
  git grep -n 'service_role' -- '*.js' '*.html' '*.ts' 2>/dev/null | head -5 >> "$REPORT_FILE"
else
  log_ok "Nessun service_role evidente in sorgenti tracciati"
fi

# Password admin in chiaro
if grep -q 'const ADMIN_PASSWORD = "' admin.html 2>/dev/null; then
  if grep -q '__RIGHETTO_ADMIN_PW_JSON__' admin.html 2>/dev/null; then
    log_ok "admin.html usa placeholder CI per password"
  else
    log_err "ADMIN_PASSWORD in chiaro in admin.html — usare secret GitHub ADMIN_PASSWORD"
  fi
else
  log_ok "Nessuna ADMIN_PASSWORD letterale in admin.html"
fi

# API secret PHP default
if grep -q "RighettoMail2026" api/send-mail.php 2>/dev/null; then
  log_warn "API_SECRET di default in api/send-mail.php — ruotare su cPanel produzione"
else
  log_ok "API_SECRET PHP non sembra il valore di esempio"
fi

echo "" >> "$REPORT_FILE"
echo "## 2. Superficie admin" >> "$REPORT_FILE"

if grep -q 'Disallow: /admin.html' robots.txt 2>/dev/null; then
  log_ok "robots.txt blocca admin.html"
else
  log_err "robots.txt non blocca /admin.html"
fi

if grep -qi 'noindex' admin.html 2>/dev/null; then
  log_ok "admin.html ha noindex"
else
  log_warn "admin.html senza meta noindex esplicito"
fi

echo "" >> "$REPORT_FILE"
echo "## 3. Documentazione sicurezza" >> "$REPORT_FILE"

if [ -f .well-known/security.txt ]; then
  log_ok "security.txt presente"
  if grep -q 'Expires:' .well-known/security.txt; then
    EXP=$(grep 'Expires:' .well-known/security.txt | head -1 | sed 's/Expires: *//')
    log_ok "security.txt Expires: $EXP"
  else
    log_warn "security.txt senza campo Expires"
  fi
else
  log_err "Manca .well-known/security.txt"
fi

if [ -f sql/rls-security-hardening.sql ]; then
  log_ok "Script RLS hardening presente"
else
  log_warn "Manca sql/rls-security-hardening.sql"
fi

if [ -f TEST-SKILL/skill-security.md ]; then
  log_ok "skill-security.md presente"
else
  log_err "Manca TEST-SKILL/skill-security.md"
fi

echo "" >> "$REPORT_FILE"
echo "## 4. Edge / form (verifica manuale)" >> "$REPORT_FILE"
log_warn "Eseguire localmente: python tools/check_rls_exposure.py (richiede righetto_social/.env)"
log_warn "Verificare Edge send-email: send_test solo verso info@righettoimmobiliare.it"

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "**Riepilogo:** ✅ $OK · ⚠️ $WARNINGS · ❌ $ERRORS" >> "$REPORT_FILE"

cat "$REPORT_FILE"

if [ "$ERRORS" -gt 0 ]; then
  exit 1
fi
exit 0
