#!/bin/bash
# ============================================================
# MINI SEO CHECK — Righetto Immobiliare
# Controlli leggeri basati su skill-seo.md
# Focus: meta tags, schema critico, keyword stuffing, freshness
# Eseguito ogni venerdi' alle 07:00 CET via GitHub Actions
# ============================================================

set -u

REPORT_FILE="${1:-mini-seo-report.md}"
ERRORS=0
WARNINGS=0
OK=0
TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M UTC')

# Pagine da controllare (subset delle principali — no admin, template, helper)
PAGES=$(find . -maxdepth 2 -name '*.html' \
  ! -name 'admin.html' \
  ! -name 'blog-articolo.html' \
  ! -name '404.html' \
  ! -name 'google*.html' \
  ! -name 'bookmarklet-helper.html' \
  ! -name 'email-*.html' \
  ! -name 'unsubscribe.html' \
  ! -name 'scraping.html' \
  | sort)

PAGE_COUNT=$(echo "$PAGES" | wc -l)

# ---- Helper ----
log_ok()   { OK=$((OK+1));            echo "  ✅ $1" >> "$REPORT_FILE"; }
log_warn() { WARNINGS=$((WARNINGS+1)); echo "  ⚠️ $1" >> "$REPORT_FILE"; }
log_err()  { ERRORS=$((ERRORS+1));    echo "  ❌ $1" >> "$REPORT_FILE"; }

# ---- Inizio report ----
cat > "$REPORT_FILE" <<EOF
# 🔍 Mini SEO Check — skill-seo.md — Righetto Immobiliare
**Data:** $TIMESTAMP
**Pagine analizzate:** $PAGE_COUNT
**Focus:** Meta tags · Schema critico · Keyword stuffing · GEO · Freshness

---

EOF

echo "## 1. Meta Tags & SEO Base" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

META_OK=0
META_ERR=0

for page in $PAGES; do
  name=$(basename "$page")

  # Title presente e lunghezza
  title=$(grep -oP '(?<=<title>).*?(?=</title>)' "$page" | head -1)
  if [ -z "$title" ]; then
    echo "  ❌ $name — Title mancante" >> "$REPORT_FILE"
    ERRORS=$((ERRORS+1)); META_ERR=$((META_ERR+1))
  else
    len=${#title}
    if [ "$len" -gt 70 ]; then
      echo "  ⚠️ $name — Title troppo lungo ($len char > 70): $title" >> "$REPORT_FILE"
      WARNINGS=$((WARNINGS+1))
    else
      OK=$((OK+1)); META_OK=$((META_OK+1))
    fi
  fi

  # Meta description
  metadesc=$(grep -oP '(?<=<meta name="description" content=")[^"]*' "$page" | head -1)
  if [ -z "$metadesc" ]; then
    echo "  ❌ $name — Meta description mancante" >> "$REPORT_FILE"
    ERRORS=$((ERRORS+1)); META_ERR=$((META_ERR+1))
  else
    len=${#metadesc}
    if [ "$len" -gt 160 ]; then
      echo "  ⚠️ $name — Meta description troppo lunga ($len char > 160)" >> "$REPORT_FILE"
      WARNINGS=$((WARNINGS+1))
    else
      OK=$((OK+1)); META_OK=$((META_OK+1))
    fi
  fi

  # Canonical URL (no .html)
  canonical=$(grep -oP '(?<=<link rel="canonical" href=")[^"]*' "$page" | head -1)
  if [ -z "$canonical" ]; then
    echo "  ⚠️ $name — Canonical mancante" >> "$REPORT_FILE"
    WARNINGS=$((WARNINGS+1))
  elif echo "$canonical" | grep -q '\.html'; then
    echo "  ❌ $name — Canonical contiene .html (URL non pulita): $canonical" >> "$REPORT_FILE"
    ERRORS=$((ERRORS+1))
  else
    OK=$((OK+1))
  fi
done

echo "" >> "$REPORT_FILE"
echo "**Meta check:** $META_OK OK / $META_ERR errori" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# ============================================================
# SEZIONE 2: SCHEMA CRITICO
# ============================================================
echo "## 2. Schema.org Critico" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

SCHEMA_OK=0
SCHEMA_ERR=0

for page in $PAGES; do
  name=$(basename "$page")

  # RealEstateAgent schema
  if ! grep -q '"RealEstateAgent"' "$page"; then
    echo "  ❌ $name — Schema RealEstateAgent mancante" >> "$REPORT_FILE"
    ERRORS=$((ERRORS+1)); SCHEMA_ERR=$((SCHEMA_ERR+1))
  else
    OK=$((OK+1)); SCHEMA_OK=$((SCHEMA_OK+1))
  fi

  # GeoCoordinates
  if ! grep -q '"GeoCoordinates"' "$page"; then
    echo "  ⚠️ $name — GeoCoordinates mancante nello schema" >> "$REPORT_FILE"
    WARNINGS=$((WARNINGS+1))
  fi

  # sameAs
  if ! grep -q '"sameAs"' "$page"; then
    echo "  ⚠️ $name — sameAs mancante nello schema" >> "$REPORT_FILE"
    WARNINGS=$((WARNINGS+1))
  fi

  # BreadcrumbList (non su homepage)
  if [ "$name" != "index.html" ]; then
    if ! grep -q '"BreadcrumbList"' "$page"; then
      echo "  ⚠️ $name — BreadcrumbList mancante" >> "$REPORT_FILE"
      WARNINGS=$((WARNINGS+1))
    fi
  fi

  # FAQPage su blog e zone
  if echo "$name" | grep -qE '^(blog-|zona-)'; then
    if ! grep -q '"FAQPage"' "$page"; then
      echo "  ❌ $name — FAQPage schema mancante (obbligatorio su blog/zone)" >> "$REPORT_FILE"
      ERRORS=$((ERRORS+1)); SCHEMA_ERR=$((SCHEMA_ERR+1))
    fi
  fi
done

echo "" >> "$REPORT_FILE"
echo "**Schema check:** $SCHEMA_OK OK / $SCHEMA_ERR errori" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# ============================================================
# SEZIONE 3: KEYWORD STUFFING (regole skill-seo.md)
# ============================================================
echo "## 3. Keyword Stuffing — Anti-Ripetizione (skill-seo.md)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

KS_WARNINGS=0

for page in $PAGES; do
  name=$(basename "$page")

  # Estrai solo testo visibile (approssimazione: rimuovi tag HTML)
  text=$(sed 's/<[^>]*>//g; s/&nbsp;/ /g; s/&amp;/\&/g' "$page" | tr '[:upper:]' '[:lower:]')

  # "a padova" max 10 occorrenze
  count_padova=$(echo "$text" | grep -oi 'a padova\|di padova' | wc -l)
  if [ "$count_padova" -gt 10 ]; then
    echo "  ⚠️ $name — 'a/di Padova' ripetuto $count_padova volte (max 10)" >> "$REPORT_FILE"
    WARNINGS=$((WARNINGS+1)); KS_WARNINGS=$((KS_WARNINGS+1))
  fi

  # "agenzia immobiliare" max 5 occorrenze
  count_agenzia=$(echo "$text" | grep -oi 'agenzia immobiliare' | wc -l)
  if [ "$count_agenzia" -gt 5 ]; then
    echo "  ⚠️ $name — 'agenzia immobiliare' ripetuto $count_agenzia volte (max 5)" >> "$REPORT_FILE"
    WARNINGS=$((WARNINGS+1)); KS_WARNINGS=$((KS_WARNINGS+1))
  fi

  # "righetto immobiliare" max 4 occorrenze
  count_righetto=$(echo "$text" | grep -oi 'righetto immobiliare' | wc -l)
  if [ "$count_righetto" -gt 4 ]; then
    echo "  ⚠️ $name — 'Righetto Immobiliare' ripetuto $count_righetto volte (max 4)" >> "$REPORT_FILE"
    WARNINGS=$((WARNINGS+1)); KS_WARNINGS=$((KS_WARNINGS+1))
  fi
done

if [ "$KS_WARNINGS" -eq 0 ]; then
  echo "  ✅ Nessun problema di keyword stuffing rilevato" >> "$REPORT_FILE"
  OK=$((OK+1))
else
  echo "  ⚠️ $KS_WARNINGS pagine con possibile keyword stuffing" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# ============================================================
# SEZIONE 4: GEO — AI OPTIMIZATION
# ============================================================
echo "## 4. GEO — AI Optimization" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# robots.txt: AI bots non bloccati
if [ -f "robots.txt" ]; then
  blocked_bots=""
  for bot in GPTBot ClaudeBot Google-Extended PerplexityBot; do
    if grep -q "Disallow.*$bot\|User-agent: $bot" robots.txt; then
      # Controlla se c'è un Disallow dopo il User-agent del bot
      if grep -A1 "User-agent: $bot" robots.txt 2>/dev/null | grep -q "Disallow: /"; then
        blocked_bots="$blocked_bots $bot"
      fi
    fi
  done
  if [ -n "$blocked_bots" ]; then
    echo "  ❌ robots.txt — AI bot bloccati:$blocked_bots" >> "$REPORT_FILE"
    ERRORS=$((ERRORS+1))
  else
    echo "  ✅ robots.txt — AI bots (GPTBot, ClaudeBot, Google-Extended, PerplexityBot) non bloccati" >> "$REPORT_FILE"
    OK=$((OK+1))
  fi
else
  echo "  ❌ robots.txt non trovato" >> "$REPORT_FILE"
  ERRORS=$((ERRORS+1))
fi

# llms.txt presente e aggiornato
if [ -f "llms.txt" ]; then
  echo "  ✅ llms.txt presente" >> "$REPORT_FILE"
  OK=$((OK+1))
  # Controlla che contenga le zone principali
  for zona in limena vigonza abano selvazzano; do
    if ! grep -qi "$zona" llms.txt; then
      echo "  ⚠️ llms.txt — zona '$zona' non trovata" >> "$REPORT_FILE"
      WARNINGS=$((WARNINGS+1))
    fi
  done
else
  echo "  ❌ llms.txt non trovato (fondamentale per GEO)" >> "$REPORT_FILE"
  ERRORS=$((ERRORS+1))
fi

echo "" >> "$REPORT_FILE"

# ============================================================
# SEZIONE 5: FRESHNESS — Timestamp blog
# ============================================================
echo "## 5. Freshness — Timestamp Blog" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

BLOG_PAGES=$(echo "$PAGES" | grep './blog-' | grep -v 'blog\.html\|blog-articolo')
NO_TIMESTAMP=0
TOTAL_BLOG=0

for page in $BLOG_PAGES; do
  name=$(basename "$page")
  TOTAL_BLOG=$((TOTAL_BLOG+1))
  if ! grep -qi 'aggiornato\|ultimo aggiornamento\|updated\|modified' "$page"; then
    echo "  ⚠️ $name — Timestamp 'Ultimo aggiornamento' non trovato" >> "$REPORT_FILE"
    WARNINGS=$((WARNINGS+1)); NO_TIMESTAMP=$((NO_TIMESTAMP+1))
  fi
done

if [ "$NO_TIMESTAMP" -eq 0 ] && [ "$TOTAL_BLOG" -gt 0 ]; then
  echo "  ✅ Tutti i $TOTAL_BLOG articoli blog hanno timestamp visibile" >> "$REPORT_FILE"
  OK=$((OK+1))
fi
echo "" >> "$REPORT_FILE"

# ============================================================
# SEZIONE 6: URL PULITE (no .html nei link interni)
# ============================================================
echo "## 6. URL Pulite — No .html nei link interni" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

URL_ERR=0
for page in $PAGES; do
  name=$(basename "$page")
  # Cerca href= con .html (escludi CDN e script tag)
  bad_links=$(grep -oP 'href="[^"]*\.html[^"]*"' "$page" | grep -v 'http' | head -5)
  if [ -n "$bad_links" ]; then
    echo "  ⚠️ $name — Link interni con .html trovati:" >> "$REPORT_FILE"
    echo "$bad_links" | while read -r link; do
      echo "      $link" >> "$REPORT_FILE"
    done
    WARNINGS=$((WARNINGS+1)); URL_ERR=$((URL_ERR+1))
  fi
done

if [ "$URL_ERR" -eq 0 ]; then
  echo "  ✅ Nessun link interno con .html trovato" >> "$REPORT_FILE"
  OK=$((OK+1))
fi
echo "" >> "$REPORT_FILE"

# ============================================================
# RIEPILOGO FINALE
# ============================================================
TOTAL=$((OK + WARNINGS + ERRORS))
if [ "$TOTAL" -gt 0 ]; then
  HEALTH=$(( (OK * 100) / TOTAL ))
else
  HEALTH=100
fi

if [ "$ERRORS" -gt 0 ]; then
  STATUS_EMOJI="🔴"
  STATUS_TEXT="ERRORI CRITICI"
elif [ "$WARNINGS" -gt 10 ]; then
  STATUS_EMOJI="🟡"
  STATUS_TEXT="AVVISI DA VALUTARE"
else
  STATUS_EMOJI="🟢"
  STATUS_TEXT="OK"
fi

cat >> "$REPORT_FILE" <<EOF
---

## 📊 Riepilogo Mini SEO Check

| | Valore |
|---|---|
| **Stato** | $STATUS_EMOJI $STATUS_TEXT |
| **Salute SEO** | **${HEALTH}%** |
| ✅ Check OK | $OK |
| ⚠️ Avvisi | $WARNINGS |
| ❌ Errori critici | $ERRORS |
| Pagine analizzate | $PAGE_COUNT |

> Basato su regole **skill-seo.md** — Righetto Immobiliare
> Audit completo strutturale: vedere workflow \`audit-settimanale.yml\`
EOF

# Output per GitHub Actions
echo "health=$HEALTH" >> "${GITHUB_OUTPUT:-/dev/null}"
echo "errors=$ERRORS" >> "${GITHUB_OUTPUT:-/dev/null}"
echo "warnings=$WARNINGS" >> "${GITHUB_OUTPUT:-/dev/null}"

echo ""
echo "Mini SEO Check completato: $OK OK / $WARNINGS avvisi / $ERRORS errori — Salute: ${HEALTH}%"
