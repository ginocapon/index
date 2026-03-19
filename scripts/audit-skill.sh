#!/bin/bash
# ============================================================
# AUDIT SKILL-2.0 — Righetto Immobiliare
# Controlla tutte le regole SKILL-2.0.md su ogni pagina HTML
# Eseguito ogni venerdi' alle 07:00 CET via GitHub Actions
# ============================================================

set -euo pipefail

REPORT_FILE="${1:-audit-report.md}"
ERRORS=0
WARNINGS=0
OK=0
TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M UTC')

# Pagine pubbliche (esclude admin, template dinamico, 404)
PAGES=$(find . -maxdepth 2 -name '*.html' \
  ! -name 'admin.html' \
  ! -name 'blog-articolo.html' \
  ! -name '404.html' \
  ! -name 'google*.html' \
  | sort)

PAGE_COUNT=$(echo "$PAGES" | wc -l)

# ---- Helper ----
log_ok()   { OK=$((OK+1));       echo "  ✅ $1" >> "$REPORT_FILE"; }
log_warn() { WARNINGS=$((WARNINGS+1)); echo "  ⚠️ $1" >> "$REPORT_FILE"; }
log_err()  { ERRORS=$((ERRORS+1));      echo "  ❌ $1" >> "$REPORT_FILE"; }

# ---- Inizio report ----
cat > "$REPORT_FILE" <<EOF
# 📋 Audit Settimanale SKILL-2.0 — Righetto Immobiliare
**Data:** $TIMESTAMP
**Pagine analizzate:** $PAGE_COUNT

---

## 1. Controlli Globali

EOF

# ============================================================
# SEZIONE 1: CONTROLLI GLOBALI
# ============================================================

echo "### 1.1 Sitemap" >> "$REPORT_FILE"
if [ -f sitemap.xml ]; then
  SITEMAP_URLS=$(grep -c '<loc>' sitemap.xml || true)
  log_ok "sitemap.xml presente ($SITEMAP_URLS URL)"

  # Verifica che ogni pagina HTML pubblica sia in sitemap
  MISSING_SITEMAP=0
  for page in $PAGES; do
    basename=$(basename "$page" .html)
    if [ "$basename" = "index" ]; then
      # Homepage check
      if ! grep -q 'righettoimmobiliare.it"' sitemap.xml 2>/dev/null && \
         ! grep -q 'righettoimmobiliare.it/' sitemap.xml 2>/dev/null; then
        log_warn "Homepage non trovata in sitemap.xml"
        MISSING_SITEMAP=$((MISSING_SITEMAP+1))
      fi
    else
      if ! grep -qi "$basename" sitemap.xml 2>/dev/null; then
        log_warn "$basename NON in sitemap.xml"
        MISSING_SITEMAP=$((MISSING_SITEMAP+1))
      fi
    fi
  done
  if [ "$MISSING_SITEMAP" -eq 0 ]; then
    log_ok "Tutte le pagine sono in sitemap"
  fi
else
  log_err "sitemap.xml MANCANTE"
fi

echo "" >> "$REPORT_FILE"
echo "### 1.2 robots.txt" >> "$REPORT_FILE"
if [ -f robots.txt ]; then
  if grep -qi 'allow.*llms.txt' robots.txt 2>/dev/null || grep -qi 'User-agent.*GPTBot' robots.txt 2>/dev/null; then
    log_ok "robots.txt presente con regole AI bots"
  else
    log_warn "robots.txt presente ma verifica regole AI bots (GEO)"
  fi
else
  log_err "robots.txt MANCANTE"
fi

echo "" >> "$REPORT_FILE"
echo "### 1.3 llms.txt (GEO)" >> "$REPORT_FILE"
if [ -f llms.txt ]; then
  LLMS_SIZE=$(wc -c < llms.txt)
  if [ "$LLMS_SIZE" -gt 500 ]; then
    log_ok "llms.txt presente e completo ($LLMS_SIZE bytes)"
  else
    log_warn "llms.txt presente ma troppo corto ($LLMS_SIZE bytes)"
  fi
else
  log_err "llms.txt MANCANTE (richiesto da SKILL-2.0 per GEO)"
fi

# ============================================================
# SEZIONE 2: CONTROLLI PER PAGINA
# ============================================================

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## 2. Controlli Per Pagina" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

PAGES_WITH_ISSUES=0

for page in $PAGES; do
  PAGE_ISSUES=""
  pagename=$(basename "$page")
  content=$(cat "$page")

  # --- 2.1 Meta description ---
  if ! echo "$content" | grep -qi 'meta.*name="description"'; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ❌ Meta description MANCANTE"
    ERRORS=$((ERRORS+1))
  fi

  # --- 2.2 Canonical ---
  if ! echo "$content" | grep -qi 'rel="canonical"'; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ❌ Canonical MANCANTE"
    ERRORS=$((ERRORS+1))
  fi

  # --- 2.3 URL pulite nei canonical (no .html) SKILL regola 10 ---
  if echo "$content" | grep -i 'rel="canonical"' | grep -q '\.html'; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ❌ Canonical contiene .html (SKILL regola 10: URL pulite)"
    ERRORS=$((ERRORS+1))
  fi

  # --- 2.4 Open Graph ---
  if ! echo "$content" | grep -qi 'property="og:title"'; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ og:title mancante"
    WARNINGS=$((WARNINGS+1))
  fi
  if ! echo "$content" | grep -qi 'property="og:description"'; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ og:description mancante"
    WARNINGS=$((WARNINGS+1))
  fi

  # --- 2.5 Schema.org JSON-LD ---
  if ! echo "$content" | grep -qi 'application/ld+json'; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ❌ Schema JSON-LD MANCANTE"
    ERRORS=$((ERRORS+1))
  else
    # RealEstateAgent presente?
    if ! echo "$content" | grep -qi 'RealEstateAgent'; then
      PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ Schema RealEstateAgent mancante (SKILL 4.6)"
      WARNINGS=$((WARNINGS+1))
    fi
    # GeoCoordinates?
    if ! echo "$content" | grep -qi 'GeoCoordinates'; then
      PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ GeoCoordinates mancante nello schema (SKILL 4.6)"
      WARNINGS=$((WARNINGS+1))
    fi
    # sameAs?
    if ! echo "$content" | grep -qi 'sameAs'; then
      PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ sameAs mancante nello schema (SKILL 4.6)"
      WARNINGS=$((WARNINGS+1))
    fi
    # dateModified (freshness signal)?
    if ! echo "$content" | grep -qi 'dateModified'; then
      PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ dateModified mancante (freshness signal)"
      WARNINGS=$((WARNINGS+1))
    fi
  fi

  # --- 2.6 BreadcrumbList ---
  if ! echo "$content" | grep -qi 'BreadcrumbList'; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ BreadcrumbList schema mancante (SKILL 4.6)"
    WARNINGS=$((WARNINGS+1))
  fi

  # --- 2.7 font-display: swap (SKILL 5.1) ---
  if echo "$content" | grep -qi '@font-face'; then
    if echo "$content" | grep -A5 '@font-face' | grep -qi 'font-display' && \
       ! echo "$content" | grep -A5 '@font-face' | grep -qi 'font-display.*swap'; then
      PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ @font-face senza font-display:swap (SKILL 5.1)"
      WARNINGS=$((WARNINGS+1))
    fi
  fi

  # --- 2.8 Keyword stuffing: "a Padova" max 10 (SKILL 1.2 regola 13) ---
  A_PADOVA_COUNT=$(echo "$content" | grep -oi 'a padova' | wc -l || true)
  if [ "$A_PADOVA_COUNT" -gt 12 ]; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ❌ Keyword stuffing: 'a Padova' appare $A_PADOVA_COUNT volte (max 10, SKILL 1.2.13)"
    ERRORS=$((ERRORS+1))
  elif [ "$A_PADOVA_COUNT" -gt 10 ]; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ 'a Padova' appare $A_PADOVA_COUNT volte (target max 10)"
    WARNINGS=$((WARNINGS+1))
  fi

  # --- 2.9 CDN esterno (SKILL: nessun CDN esterno) ---
  CDN_HITS=$(echo "$content" | grep -oi 'cdn\.\|cdnjs\.\|unpkg\.\|jsdelivr\.' | wc -l || true)
  if [ "$CDN_HITS" -gt 0 ]; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ Rilevato CDN esterno ($CDN_HITS occorrenze) — SKILL vieta CDN esterni"
    WARNINGS=$((WARNINGS+1))
  fi

  # --- 2.10 Framework/librerie esterne (SKILL: solo vanilla) ---
  if echo "$content" | grep -qi 'react\.\|angular\.\|vue\.\|jquery\.' 2>/dev/null; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ❌ Framework/libreria esterna rilevata (SKILL: solo vanilla HTML/CSS/JS)"
    ERRORS=$((ERRORS+1))
  fi

  # --- 2.11 Link interni con .html (SKILL regola 10) ---
  INTERNAL_HTML_LINKS=$(echo "$content" | grep -oP 'href="[^"]*\.html[^"]*"' | grep -v 'google' | grep -v 'http' | wc -l || true)
  if [ "$INTERNAL_HTML_LINKS" -gt 0 ]; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ $INTERNAL_HTML_LINKS link interni con .html (SKILL regola 10: URL pulite)"
    WARNINGS=$((WARNINGS+1))
  fi

  # --- 2.12 GA4 presente ---
  if ! echo "$content" | grep -qi 'G-9MHDHHES26\|gtag\|googletagmanager'; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ Google Analytics 4 non rilevato"
    WARNINGS=$((WARNINGS+1))
  fi

  # --- 2.13 Viewport meta (mobile-first) ---
  if ! echo "$content" | grep -qi 'name="viewport"'; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ❌ Meta viewport MANCANTE (SKILL: mobile-first)"
    ERRORS=$((ERRORS+1))
  fi

  # --- 2.14 filter: blur (SKILL: vietato su animazioni) ---
  BLUR_COUNT=$(echo "$content" | grep -oi 'filter.*blur' | wc -l || true)
  if [ "$BLUR_COUNT" -gt 0 ]; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ filter:blur rilevato ($BLUR_COUNT) — SKILL vieta blur su animazioni"
    WARNINGS=$((WARNINGS+1))
  fi

  # --- 2.15 will-change permanente (SKILL: vietato) ---
  WILLCHANGE_COUNT=$(echo "$content" | grep -oi 'will-change' | wc -l || true)
  if [ "$WILLCHANGE_COUNT" -gt 2 ]; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ⚠️ will-change usato $WILLCHANGE_COUNT volte (SKILL: no will-change permanente)"
    WARNINGS=$((WARNINGS+1))
  fi

  # --- 2.16 Placeholder non sostituiti [DATO] [ZONA] [FONTE] ---
  PLACEHOLDER_COUNT=$(echo "$content" | grep -oP '\[(DATO|ZONA|FONTE|INSERIRE|TODO)\]' | wc -l || true)
  if [ "$PLACEHOLDER_COUNT" -gt 0 ]; then
    PAGE_ISSUES="${PAGE_ISSUES}\n  ❌ $PLACEHOLDER_COUNT placeholder non sostituiti [DATO]/[ZONA]/[FONTE] (SKILL: regola d'oro)"
    ERRORS=$((ERRORS+1))
  fi

  # Solo stampa se ci sono problemi
  if [ -n "$PAGE_ISSUES" ]; then
    PAGES_WITH_ISSUES=$((PAGES_WITH_ISSUES+1))
    echo "### 📄 $pagename" >> "$REPORT_FILE"
    echo -e "$PAGE_ISSUES" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
  fi
done

# ============================================================
# SEZIONE 3: CONTROLLI SPECIFICI BLOG
# ============================================================

echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## 3. Controlli Blog" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

BLOG_PAGES=$(find . -maxdepth 1 -name 'blog-*.html' ! -name 'blog-articolo.html' | sort)
BLOG_COUNT=$(echo "$BLOG_PAGES" | wc -l)
echo "**Articoli blog trovati:** $BLOG_COUNT" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

for page in $BLOG_PAGES; do
  pagename=$(basename "$page")
  content=$(cat "$page")
  BLOG_ISSUES=""

  # FAQPage schema (SKILL 4.5: min 5 FAQ)
  FAQ_COUNT=$(echo "$content" | grep -oi 'FAQPage' | wc -l || true)
  if [ "$FAQ_COUNT" -eq 0 ]; then
    BLOG_ISSUES="${BLOG_ISSUES}\n  ⚠️ FAQPage schema mancante"
    WARNINGS=$((WARNINGS+1))
  fi

  # Author bio (SKILL 4.2)
  if ! echo "$content" | grep -qi 'author\|autore'; then
    BLOG_ISSUES="${BLOG_ISSUES}\n  ⚠️ Author bio non rilevata (SKILL 4.2 E-E-A-T)"
    WARNINGS=$((WARNINGS+1))
  fi

  # Timestamp visibile (SKILL: freshness)
  if ! echo "$content" | grep -qi 'aggiornamento\|pubblicato\|data.*202[5-9]'; then
    BLOG_ISSUES="${BLOG_ISSUES}\n  ⚠️ Timestamp/data aggiornamento non visibile"
    WARNINGS=$((WARNINGS+1))
  fi

  if [ -n "$BLOG_ISSUES" ]; then
    echo "### 📝 $pagename" >> "$REPORT_FILE"
    echo -e "$BLOG_ISSUES" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
  fi
done

# ============================================================
# SEZIONE 4: CONTROLLI ZONE
# ============================================================

echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## 4. Controlli Zone" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

ZONE_PAGES=$(find . -maxdepth 1 -name 'zona-*.html' | sort)
ZONE_COUNT=$(echo "$ZONE_PAGES" | wc -l)
echo "**Pagine zona trovate:** $ZONE_COUNT" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

for page in $ZONE_PAGES; do
  pagename=$(basename "$page")
  content=$(cat "$page")
  ZONE_ISSUES=""

  # FAQPage schema
  if ! echo "$content" | grep -qi 'FAQPage'; then
    ZONE_ISSUES="${ZONE_ISSUES}\n  ⚠️ FAQPage schema mancante"
    WARNINGS=$((WARNINGS+1))
  fi

  # GeoCoordinates
  if ! echo "$content" | grep -qi 'GeoCoordinates'; then
    ZONE_ISSUES="${ZONE_ISSUES}\n  ⚠️ GeoCoordinates mancante"
    WARNINGS=$((WARNINGS+1))
  fi

  # Tabella OMI
  if ! echo "$content" | grep -qi 'OMI\|prezzo.*mq\|€/mq'; then
    ZONE_ISSUES="${ZONE_ISSUES}\n  ⚠️ Dati OMI/prezzo al mq non trovati"
    WARNINGS=$((WARNINGS+1))
  fi

  if [ -n "$ZONE_ISSUES" ]; then
    echo "### 🏘️ $pagename" >> "$REPORT_FILE"
    echo -e "$ZONE_ISSUES" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
  fi
done

# ============================================================
# SEZIONE 5: CONTROLLI SERVIZI
# ============================================================

echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## 5. Controlli Pagine Servizio" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

SERVICE_PAGES=$(find . -maxdepth 1 -name 'servizio-*.html' | sort)

for page in $SERVICE_PAGES; do
  pagename=$(basename "$page")
  content=$(cat "$page")
  SVC_ISSUES=""

  if ! echo "$content" | grep -qi 'FAQPage'; then
    SVC_ISSUES="${SVC_ISSUES}\n  ⚠️ FAQPage schema mancante (SKILL 4.6)"
    WARNINGS=$((WARNINGS+1))
  fi

  if [ -n "$SVC_ISSUES" ]; then
    echo "### 🔧 $pagename" >> "$REPORT_FILE"
    echo -e "$SVC_ISSUES" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
  fi
done

# ============================================================
# RIEPILOGO FINALE
# ============================================================

echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## 📊 Riepilogo" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| Metrica | Valore |" >> "$REPORT_FILE"
echo "|---|---|" >> "$REPORT_FILE"
echo "| Pagine analizzate | **$PAGE_COUNT** |" >> "$REPORT_FILE"
echo "| Pagine con problemi | **$PAGES_WITH_ISSUES** |" >> "$REPORT_FILE"
echo "| Errori critici (❌) | **$ERRORS** |" >> "$REPORT_FILE"
echo "| Avvisi (⚠️) | **$WARNINGS** |" >> "$REPORT_FILE"
echo "| Check superati (✅) | **$OK** |" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

TOTAL=$((ERRORS+WARNINGS+OK))
if [ "$TOTAL" -gt 0 ]; then
  HEALTH=$(( (OK * 100) / TOTAL ))
else
  HEALTH=100
fi

echo "**Salute complessiva:** ${HEALTH}%" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ "$ERRORS" -gt 0 ]; then
  echo "⚠️ **AZIONE RICHIESTA:** $ERRORS errori critici da correggere." >> "$REPORT_FILE"
elif [ "$WARNINGS" -gt 0 ]; then
  echo "👍 Nessun errore critico. $WARNINGS avvisi da valutare." >> "$REPORT_FILE"
else
  echo "🎉 Tutto in regola! Nessun problema rilevato." >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "*Report generato automaticamente da audit-skill.sh — SKILL-2.0 compliance*" >> "$REPORT_FILE"
echo "*Prossimo audit: venerdi' prossimo ore 07:00 CET*" >> "$REPORT_FILE"

# Output per GitHub Actions
echo "errors=$ERRORS" >> "${GITHUB_OUTPUT:-/dev/null}"
echo "warnings=$WARNINGS" >> "${GITHUB_OUTPUT:-/dev/null}"
echo "health=$HEALTH" >> "${GITHUB_OUTPUT:-/dev/null}"

echo ""
echo "=== AUDIT COMPLETATO ==="
echo "Errori: $ERRORS | Avvisi: $WARNINGS | OK: $OK | Salute: ${HEALTH}%"
echo "Report salvato in: $REPORT_FILE"
