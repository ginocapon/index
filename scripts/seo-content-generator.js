#!/usr/bin/env node
/**
 * SEO Content Generator — Righetto Immobiliare
 *
 * Script Node.js per generare strutture articoli SEO/GEO/AEO ottimizzate.
 * Genera template HTML con Schema markup JSON-LD, struttura E-E-A-T,
 * sezione FAQ e metadata completi.
 *
 * Utilizzo:
 *   node scripts/seo-content-generator.js --keyword "case in vendita Padova" --length 2000
 *   node scripts/seo-content-generator.js --config scripts/seo-config.json
 *
 * Output: file HTML nella root del progetto + aggiornamento sitemap.xml
 */

const fs = require('fs');
const path = require('path');

// ══════════════════════════════════════════
// CONFIGURAZIONE AZIENDALE (Righetto Immobiliare)
// ══════════════════════════════════════════
const AZIENDA = {
  nome: 'Righetto Immobiliare',
  ragioneSociale: 'Gruppo Immobiliare Righetto di Capon Gino',
  settore: 'Agenzia immobiliare',
  sito: 'https://righettoimmobiliare.it',
  telefono: '049 884 3484',
  cellulare: '348 862 1888',
  indirizzo: 'Via Roma, 96',
  cap: '35010',
  citta: 'Limena',
  provincia: 'PD',
  piva: '05182390285',
  annoFondazione: 2000,
  zona: ['Padova', 'Limena', 'Vigonza', 'Campodarsego', 'Selvazzano', 'Abano Terme', 'Rubano', 'Villafranca Padovana'],
  autore: {
    nome: 'Gino Capon',
    ruolo: 'Agente Immobiliare',
    iniziale: 'G'
  },
  target: [
    'Famiglie che cercano casa',
    'Investitori immobiliari',
    'Proprietari che vogliono vendere'
  ]
};

// ══════════════════════════════════════════
// UTILITA
// ══════════════════════════════════════════
function slugify(text) {
  return text.toLowerCase()
    .replace(/[àáâãäå]/g, 'a').replace(/[èéêë]/g, 'e').replace(/[ìíîï]/g, 'i')
    .replace(/[òóôõö]/g, 'o').replace(/[ùúûü]/g, 'u').replace(/[ç]/g, 'c')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')
    .slice(0, 80);
}

function oggi() {
  return new Date().toISOString().split('T')[0];
}

function annoCorrente() {
  return new Date().getFullYear();
}

// ══════════════════════════════════════════
// GENERATORE JSON-LD SCHEMAS
// ══════════════════════════════════════════
function generateArticleSchema(config) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: config.titleTag,
    description: config.metaDescription,
    image: config.ogImage ? [config.ogImage] : [],
    author: {
      '@type': 'Person',
      name: AZIENDA.autore.nome,
      jobTitle: AZIENDA.autore.ruolo,
      worksFor: {
        '@type': 'RealEstateAgent',
        name: AZIENDA.ragioneSociale,
        url: AZIENDA.sito
      }
    },
    publisher: {
      '@type': 'Organization',
      name: AZIENDA.nome,
      url: AZIENDA.sito,
      logo: {
        '@type': 'ImageObject',
        url: `${AZIENDA.sito}/img/logo.png`
      }
    },
    datePublished: config.dataPublicazione || oggi(),
    dateModified: config.dataModifica || oggi(),
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `${AZIENDA.sito}/${config.filename}`
    },
    articleSection: config.categoria || 'Mercato Immobiliare',
    keywords: config.keywords || [],
    wordCount: config.lunghezza || 2000,
    inLanguage: 'it-IT'
  };
}

function generateFAQSchema(faqItems) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqItems.map(faq => ({
      '@type': 'Question',
      name: faq.domanda,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.risposta
      }
    }))
  };
}

function generateBreadcrumbSchema(config) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: `${AZIENDA.sito}/` },
      { '@type': 'ListItem', position: 2, name: 'Blog', item: `${AZIENDA.sito}/blog.html` },
      { '@type': 'ListItem', position: 3, name: config.breadcrumbName || config.h1 }
    ]
  };
}

function generateLocalBusinessSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'RealEstateAgent',
    name: AZIENDA.ragioneSociale,
    url: AZIENDA.sito,
    telephone: `+39${AZIENDA.telefono.replace(/\s/g, '')}`,
    address: {
      '@type': 'PostalAddress',
      streetAddress: AZIENDA.indirizzo,
      addressLocality: AZIENDA.citta,
      postalCode: AZIENDA.cap,
      addressRegion: AZIENDA.provincia,
      addressCountry: 'IT'
    },
    areaServed: AZIENDA.zona.map(z => ({
      '@type': 'City',
      name: z
    })),
    foundingDate: AZIENDA.annoFondazione.toString(),
    priceRange: '$$'
  };
}

// ══════════════════════════════════════════
// GENERATORE TEMPLATE HTML
// ══════════════════════════════════════════
function generateHTMLTemplate(config) {
  const articleSchema = generateArticleSchema(config);
  const faqSchema = config.faq ? generateFAQSchema(config.faq) : null;
  const breadcrumbSchema = generateBreadcrumbSchema(config);
  const localBizSchema = generateLocalBusinessSchema();

  const faqHTML = config.faq ? config.faq.map(faq => `
    <div class="faq-item">
      <div class="faq-q">${faq.domanda}</div>
      <div class="faq-a"><div class="faq-a-inner">${faq.risposta}</div></div>
    </div>`).join('\n') : '';

  const shareUrl = encodeURIComponent(`${AZIENDA.sito}/${config.filename}`);
  const shareTitle = encodeURIComponent(config.titleTag);

  return `<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#2C4A6E">
  <title>${config.titleTag}</title>
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="dns-prefetch" href="https://cdn.jsdelivr.net">
  <link rel="dns-prefetch" href="https://qwkwkemuabfwvwuqrxlu.supabase.co">
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/cormorant-garamond-600.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="canonical" href="${AZIENDA.sito}/${config.filename}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="${config.titleTag}">
  <meta property="og:description" content="${config.metaDescription}">
  <meta property="og:url" content="${AZIENDA.sito}/${config.filename}">
  <meta property="og:image" content="${config.ogImage || AZIENDA.sito + '/img/team/titolari.webp'}">
  <meta property="og:site_name" content="${AZIENDA.nome}">
  <meta property="og:locale" content="it_IT">
  <meta property="article:published_time" content="${config.dataPublicazione || oggi()}T08:00:00+01:00">
  <meta property="article:author" content="${AZIENDA.autore.nome}">
  <meta property="article:section" content="${config.categoria || 'Mercato Immobiliare'}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${config.titleTag}">
  <meta name="twitter:description" content="${config.metaDescription}">
  <meta name="twitter:image" content="${config.ogImage || AZIENDA.sito + '/img/team/titolari.webp'}">
  <meta name="description" content="${config.metaDescription}">
  <link rel="stylesheet" href="css/fonts.css">
  <link rel="stylesheet" href="css/nav-mobile.css">
  <link rel="stylesheet" href="css/scroll-reveal.css">
  <link rel="stylesheet" href="css/welcome-popup.css">

  <!-- JSON-LD Article -->
  <script type="application/ld+json">
  ${JSON.stringify(articleSchema, null, 2)}
  </script>

  <!-- JSON-LD FAQPage -->
  ${faqSchema ? `<script type="application/ld+json">
  ${JSON.stringify(faqSchema, null, 2)}
  </script>` : ''}

  <!-- JSON-LD BreadcrumbList -->
  <script type="application/ld+json">
  ${JSON.stringify(breadcrumbSchema, null, 2)}
  </script>

  <!-- JSON-LD RealEstateAgent -->
  <script type="application/ld+json">
  ${JSON.stringify(localBizSchema, null, 2)}
  </script>
</head>
<!-- Template generato da seo-content-generator.js — Inserisci style e body dal template blog -->
</html>`;
}

// ══════════════════════════════════════════
// GENERATORE CHECKLIST SEO
// ══════════════════════════════════════════
function generateSEOChecklist(config) {
  return `
═══════════════════════════════════════════
  CHECKLIST SEO/GEO/AEO — ${config.titleTag}
═══════════════════════════════════════════

METADATA:
  Title Tag (${config.titleTag.length}/60 char): ${config.titleTag}
  Meta Description (${config.metaDescription.length}/155 char): ${config.metaDescription}
  Slug URL: ${config.slug}
  Filename: ${config.filename}

E-E-A-T:
  [ ] Experience: min 2-3 riferimenti esperienza diretta
  [ ] Expertise: terminologia tecnica, dati precisi (prezzi/mq)
  [ ] Authoritativeness: fonti ufficiali (Agenzia Entrate, OMI)
  [ ] Trustworthiness: disclaimer, dati verificabili

GEO/LLMO (citazioni AI):
  [ ] Frasi dichiarative nelle prime 2 righe di ogni sezione
  [ ] Dati numerici specifici e verificabili
  [ ] Formato: Domanda H2 + Risposta diretta + Approfondimento
  [ ] Liste, tabelle, definizioni chiare

AEO (Featured Snippet):
  [ ] Risposta 40-60 parole come primo paragrafo per ogni H2
  [ ] Formato is-snippet: "[Keyword] e [definizione]"
  [ ] Min 5 FAQ in formato Q&A alla fine

SEO LOCALE:
  [ ] Zona geografica menzionata 3-4+ volte
  [ ] Riferimenti a quartieri, vie, landmarks
  [ ] Varianti keyword locali

SXO (esperienza utente):
  [ ] Paragrafi max 3-4 righe
  [ ] Punti chiave in grassetto
  [ ] Sommario/indice cliccabile
  [ ] CTA intermedia + CTA finale

SCHEMA MARKUP:
  [x] Article/BlogPosting
  [x] FAQPage (${config.faq ? config.faq.length : 0} FAQ)
  [x] BreadcrumbList
  [x] RealEstateAgent (LocalBusiness)

ARTICOLI SATELLITE (Topic Cluster):
${(config.articoliSatellite || []).map((a, i) => `  ${i + 1}. ${a}`).join('\n')}

KEYWORD LONG-TAIL CORRELATE:
${(config.keywordLongTail || []).map((k, i) => `  ${i + 1}. ${k}`).join('\n')}
`;
}

// ══════════════════════════════════════════
// MAIN — CLI
// ══════════════════════════════════════════
function main() {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.length === 0) {
    console.log(`
Righetto Immobiliare — SEO Content Generator
=============================================

Utilizzo:
  node scripts/seo-content-generator.js --config <file.json>
  node scripts/seo-content-generator.js --keyword "keyword" [opzioni]

Opzioni:
  --config <file>     File JSON di configurazione completa
  --keyword <kw>      Keyword principale
  --secondary <kw>    Keyword secondarie (separare con virgola)
  --length <n>        Lunghezza target in parole (default: 2000)
  --output <file>     Nome file output (default: blog-<slug>.html)
  --checklist         Genera solo la checklist SEO
  --schemas           Genera solo gli schema markup JSON-LD
  --help              Mostra questo messaggio

Esempio:
  node scripts/seo-content-generator.js \\
    --keyword "case in vendita Padova" \\
    --secondary "appartamenti Padova,villa Limena" \\
    --length 2000
`);
    return;
  }

  // Parse argomenti
  let config = {};

  if (args.includes('--config')) {
    const configPath = args[args.indexOf('--config') + 1];
    config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  } else {
    const kw = args[args.indexOf('--keyword') + 1] || 'mercato immobiliare Padova';
    const secondary = args.includes('--secondary')
      ? args[args.indexOf('--secondary') + 1].split(',').map(s => s.trim())
      : [];
    const length = args.includes('--length')
      ? parseInt(args[args.indexOf('--length') + 1])
      : 2000;

    const slug = slugify(kw + ' ' + annoCorrente());
    config = {
      keywordPrincipale: kw,
      keywordSecondarie: secondary,
      lunghezza: length,
      slug: slug,
      filename: `blog-${slug}.html`,
      titleTag: `${kw.charAt(0).toUpperCase() + kw.slice(1)} ${annoCorrente()}: Guida Completa`,
      metaDescription: `${kw.charAt(0).toUpperCase() + kw.slice(1)} nel ${annoCorrente()}. Prezzi aggiornati, zone migliori e consigli esperti. Guida di ${AZIENDA.nome}.`,
      h1: `${kw.charAt(0).toUpperCase() + kw.slice(1)} ${annoCorrente()}: Guida Completa`,
      categoria: 'Mercato locale',
      dataPublicazione: oggi(),
      keywords: [kw, ...secondary],
      faq: [],
      articoliSatellite: [],
      keywordLongTail: []
    };
  }

  // Override output se specificato
  if (args.includes('--output')) {
    config.filename = args[args.indexOf('--output') + 1];
  }

  // Solo checklist
  if (args.includes('--checklist')) {
    console.log(generateSEOChecklist(config));
    return;
  }

  // Solo schemas
  if (args.includes('--schemas')) {
    console.log('\n=== Article Schema ===');
    console.log(JSON.stringify(generateArticleSchema(config), null, 2));
    if (config.faq && config.faq.length > 0) {
      console.log('\n=== FAQPage Schema ===');
      console.log(JSON.stringify(generateFAQSchema(config.faq), null, 2));
    }
    console.log('\n=== BreadcrumbList Schema ===');
    console.log(JSON.stringify(generateBreadcrumbSchema(config), null, 2));
    console.log('\n=== RealEstateAgent Schema ===');
    console.log(JSON.stringify(generateLocalBusinessSchema(), null, 2));
    return;
  }

  // Genera template HTML
  const html = generateHTMLTemplate(config);
  const outputPath = path.join(__dirname, '..', config.filename);

  // Non sovrascrivere file esistenti (genera solo template nuovi)
  if (fs.existsSync(outputPath)) {
    console.log(`\nAttenzione: ${config.filename} esiste gia'. Generazione solo checklist e schemas.\n`);
    console.log(generateSEOChecklist(config));
    return;
  }

  fs.writeFileSync(outputPath, html, 'utf-8');
  console.log(`\nFile generato: ${config.filename}`);
  console.log(generateSEOChecklist(config));
}

main();
