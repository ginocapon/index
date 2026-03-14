#!/usr/bin/env node
/**
 * validate-page.js — Validazione automatica pagine Righetto Immobiliare
 *
 * Basato su TEST-SKILL/SKILL-UNIFICATA.md
 * Verifica che ogni nuova pagina HTML rispetti le checklist SEO, GEO, Visual Saliency.
 *
 * Uso:
 *   node scripts/validate-page.js [file.html ...]
 *   node scripts/validate-page.js --all          # valida tutte le pagine
 *   node scripts/validate-page.js --staged       # valida solo i file staged in git
 *
 * Exit code 0 = tutto ok, 1 = warning trovati, 2 = errori critici
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ═══ CONFIGURAZIONE ═══
const ROOT = path.resolve(__dirname, '..');
const SITEMAP = path.join(ROOT, 'sitemap.xml');
const BLOG_HTML = path.join(ROOT, 'blog.html');
const HOMEPAGE_JS = path.join(ROOT, 'js', 'homepage.js');
const ADMIN_HTML = path.join(ROOT, 'admin.html');

const REQUIRED_SAME_AS = [
  'facebook.com/righettoimmobiliare',
  'instagram.com/righettoimmobiliare',
  'linkedin.com/company/righetto-immobiliare'
];

// ═══ COLORI TERMINALE ═══
const RED = '\x1b[31m';
const YEL = '\x1b[33m';
const GRN = '\x1b[32m';
const CYN = '\x1b[36m';
const RST = '\x1b[0m';
const BOLD = '\x1b[1m';

// ═══ RISULTATI ═══
let totalErrors = 0;
let totalWarnings = 0;

function error(file, msg) {
  console.log(`  ${RED}ERRORE${RST}  ${msg}`);
  totalErrors++;
}
function warn(file, msg) {
  console.log(`  ${YEL}WARN${RST}    ${msg}`);
  totalWarnings++;
}
function ok(file, msg) {
  console.log(`  ${GRN}OK${RST}      ${msg}`);
}

// ═══ VALIDATORI ═══

function validateMeta(file, html) {
  // Title tag
  const title = html.match(/<title>(.*?)<\/title>/s);
  if (!title) return error(file, 'Manca <title> tag');
  if (title[1].length > 70) warn(file, `Title troppo lungo (${title[1].length} char, max 60-70)`);
  else ok(file, `Title OK (${title[1].length} char)`);

  // Meta description
  const desc = html.match(/<meta\s+name="description"\s+content="([^"]*)"/);
  if (!desc) return error(file, 'Manca meta description');
  if (desc[1].length > 170) warn(file, `Meta description troppo lunga (${desc[1].length} char, max 160)`);
  else ok(file, `Meta description OK (${desc[1].length} char)`);

  // H1
  const h1s = html.match(/<h1[\s>]/g);
  if (!h1s) error(file, 'Manca tag H1');
  else if (h1s.length > 1) warn(file, `${h1s.length} tag H1 trovati (dovrebbe essere 1)`);
  else ok(file, 'H1 unico presente');

  // Canonical
  if (!html.includes('rel="canonical"')) warn(file, 'Manca canonical URL');
  else ok(file, 'Canonical URL presente');

  // OG tags
  if (!html.includes('og:title')) warn(file, 'Manca og:title');
  if (!html.includes('og:description')) warn(file, 'Manca og:description');
  if (!html.includes('og:image')) warn(file, 'Manca og:image');

  // Robots
  if (!html.includes('name="robots"')) warn(file, 'Manca meta robots');
}

function validateSchema(file, html) {
  if (!html.includes('application/ld+json')) {
    error(file, 'Manca schema JSON-LD');
    return;
  }
  ok(file, 'Schema JSON-LD presente');

  // sameAs check (solo per pagine con RealEstateAgent nello schema statico, non in JS)
  // Estrae solo i blocchi ld+json statici
  const ldJsonBlocks = html.match(/<script[^>]*type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/g) || [];
  const staticSchema = ldJsonBlocks.join(' ');

  if (staticSchema.includes('RealEstateAgent')) {
    if (!staticSchema.includes('"sameAs"')) {
      error(file, 'Schema RealEstateAgent senza sameAs (profili social)');
    } else {
      ok(file, 'sameAs presente');
    }
    if (!staticSchema.includes('GeoCoordinates')) {
      error(file, 'Schema RealEstateAgent senza GeoCoordinates');
    } else {
      ok(file, 'GeoCoordinates presente');
    }
  }

  // BreadcrumbList (non serve per index.html)
  const basename = path.basename(file);
  if (basename !== 'index.html' && !html.includes('BreadcrumbList')) {
    warn(file, 'Manca BreadcrumbList schema');
  }

  // FAQPage per pagine servizio e zona
  if ((basename.startsWith('servizio-') || basename.startsWith('zona-')) && !html.includes('FAQPage')) {
    warn(file, 'Pagina servizio/zona senza FAQPage schema');
  }
}

function validatePerformance(file, html) {
  // Font preload
  if (!html.includes('preload') || !html.includes('montserrat')) {
    warn(file, 'Manca preload font Montserrat');
  }

  // Hero image preload (non per tutte le pagine)
  const basename = path.basename(file);
  const needsHeroPreload = ['index.html', 'landing-vendita.html', 'landing-mutuo.html',
    'landing-valutazione.html', 'landing-agente.html', 'landing-vendere-casa-padova.html'];
  if (needsHeroPreload.includes(basename)) {
    const preloads = html.match(/rel="preload".*as="image"/g);
    if (!preloads) warn(file, 'Manca preload hero image');
    else ok(file, 'Hero image preloaded');
  }

  // Lazy loading above fold — check first img tags
  const firstImgMatch = html.match(/<img[^>]*>/g);
  if (firstImgMatch) {
    // Check first 3 images for lazy loading (rough above-fold check)
    for (let i = 0; i < Math.min(3, firstImgMatch.length); i++) {
      if (firstImgMatch[i].includes('loading="lazy"') && !firstImgMatch[i].includes('author-bio')) {
        // Only warn if it's in the first ~500 lines (rough above-fold)
        const imgPos = html.indexOf(firstImgMatch[i]);
        const linesBefore = html.substring(0, imgPos).split('\n').length;
        if (linesBefore < 500) {
          // Could be above fold, but not necessarily - just info
        }
      }
    }
  }

  // Images without width/height
  const imgs = html.match(/<img[^>]*>/g) || [];
  let missingDims = 0;
  for (const img of imgs) {
    if (!img.includes('width=') && !img.includes('style=')) {
      missingDims++;
    }
  }
  if (missingDims > 0) warn(file, `${missingDims} immagini senza width/height espliciti`);
}

function validateBlogRegistration(file, html) {
  const basename = path.basename(file);
  if (!basename.startsWith('blog-') || basename === 'blog.html' || basename === 'blog-articolo.html') return;

  const slug = basename.replace('.html', '');

  // Check sitemap
  try {
    const sitemap = fs.readFileSync(SITEMAP, 'utf8');
    if (!sitemap.includes(slug)) {
      error(file, `NON registrato nella sitemap.xml`);
    } else {
      ok(file, 'Registrato in sitemap.xml');
    }
  } catch(e) {}

  // Check blog.html
  try {
    const blog = fs.readFileSync(BLOG_HTML, 'utf8');
    if (!blog.includes(slug)) {
      error(file, `NON registrato in blog.html (articoliStatici)`);
    } else {
      ok(file, 'Registrato in blog.html');
    }
  } catch(e) {}

  // Check homepage.js staticMap
  try {
    const hp = fs.readFileSync(HOMEPAGE_JS, 'utf8');
    if (!hp.includes(slug)) {
      warn(file, `NON registrato in js/homepage.js (staticMap) — non apparira' in homepage`);
    } else {
      ok(file, 'Registrato in homepage.js');
    }
  } catch(e) {}

  // Check author bio
  if (!html.includes('author-bio')) {
    warn(file, 'Manca author bio box');
  } else {
    ok(file, 'Author bio presente');
  }

  // Check article:author meta
  if (!html.includes('article:author')) {
    warn(file, 'Manca meta article:author');
  }
}

function validateGEO(file, html) {
  const basename = path.basename(file);
  // Solo per pagine contenuto (blog, servizi, zone)
  if (!basename.startsWith('blog-') && !basename.startsWith('servizio-') &&
      !basename.startsWith('zona-') && !basename.startsWith('landing-')) return;

  // Check for declarative first sentences (H2 followed by content)
  const h2Count = (html.match(/<h2/g) || []).length;
  if (h2Count === 0 && basename.startsWith('blog-')) {
    warn(file, 'Nessun H2 trovato — struttura GEO non ottimale');
  }
}

// ═══ MAIN ═══

function validateFile(filePath) {
  const basename = path.basename(filePath);
  console.log(`\n${BOLD}${CYN}Validazione: ${basename}${RST}`);
  console.log('─'.repeat(60));

  try {
    const html = fs.readFileSync(filePath, 'utf8');
    validateMeta(filePath, html);
    validateSchema(filePath, html);
    validatePerformance(filePath, html);
    validateBlogRegistration(filePath, html);
    validateGEO(filePath, html);
  } catch(e) {
    error(filePath, `Impossibile leggere: ${e.message}`);
  }
}

// Parse arguments
const args = process.argv.slice(2);
let files = [];

if (args.includes('--all')) {
  files = fs.readdirSync(ROOT)
    .filter(f => f.endsWith('.html') && !['admin.html', 'scraping.html', 'bookmarklet-helper.html', 'unsubscribe.html', 'privacy.html', 'cookie-policy.html', 'blog-articolo.html', 'immobile.html'].includes(f))
    .map(f => path.join(ROOT, f));
} else if (args.includes('--staged')) {
  try {
    const staged = execSync('git diff --cached --name-only --diff-filter=ACM', { cwd: ROOT, encoding: 'utf8' });
    files = staged.trim().split('\n')
      .filter(f => f.endsWith('.html') && !f.startsWith('admin') && !['blog-articolo.html', 'immobile.html'].includes(f))
      .map(f => path.join(ROOT, f));
  } catch(e) {
    console.log('Nessun file HTML staged');
    process.exit(0);
  }
} else if (args.length > 0) {
  files = args.map(f => path.resolve(f));
} else {
  console.log(`
${BOLD}validate-page.js${RST} — Validazione automatica pagine Righetto Immobiliare

${BOLD}Uso:${RST}
  node scripts/validate-page.js [file.html ...]
  node scripts/validate-page.js --all        ${GRN}# tutte le pagine${RST}
  node scripts/validate-page.js --staged     ${GRN}# solo file staged git${RST}
`);
  process.exit(0);
}

if (files.length === 0) {
  console.log('Nessun file HTML da validare.');
  process.exit(0);
}

console.log(`\n${BOLD}Validazione SKILL UNIFICATA — ${files.length} pagine${RST}`);
console.log('═'.repeat(60));

for (const file of files) {
  if (fs.existsSync(file)) {
    validateFile(file);
  } else {
    console.log(`${RED}File non trovato: ${file}${RST}`);
  }
}

// Summary
console.log('\n' + '═'.repeat(60));
if (totalErrors > 0) {
  console.log(`${RED}${BOLD}RISULTATO: ${totalErrors} errori, ${totalWarnings} warning${RST}`);
  process.exit(2);
} else if (totalWarnings > 0) {
  console.log(`${YEL}${BOLD}RISULTATO: 0 errori, ${totalWarnings} warning${RST}`);
  process.exit(1);
} else {
  console.log(`${GRN}${BOLD}RISULTATO: Tutto OK!${RST}`);
  process.exit(0);
}
