/**
 * RIGHETTO IMMOBILIARE — Lead Conversion Engine
 * Sistema completo: A/B test CTA, tracking GA4, speed-to-lead,
 * segmentazione acquirente/venditore, social proof dinamica
 *
 * Vanilla JS — zero dipendenze esterne
 * Aggiornato: marzo 2026
 */
(function() {
'use strict';

/* ═══════════════════════════════════════════════════
   1. A/B TEST ENGINE
   Testa varianti CTA e traccia conversioni via GA4
   ═══════════════════════════════════════════════════ */

var defined_tests = {
  hero_cta: {
    selector: '.hero-btns .btn-g:first-child',
    variants: [
      { text: 'Quanto vale la tua casa?', id: 'A_quanto_vale' },
      { text: 'Valutazione gratuita in 24h', id: 'B_valutazione_24h' },
      { text: 'Scopri il valore reale', id: 'C_valore_reale' }
    ]
  },
  nav_cta: {
    selector: '.nav-cta',
    variants: [
      { text: 'Contattaci', id: 'A_contattaci' },
      { text: 'Parla con noi', id: 'B_parla' }
    ]
  },
  mobile_cta: {
    selector: '.nav-mobile-cta',
    variants: [
      { text: 'Contattaci', id: 'A_contattaci_m' },
      { text: 'Parla con noi', id: 'B_parla_m' }
    ]
  },
  sticky_primary: {
    selector: '.scta-primary',
    variants: [
      { text: 'Valutazione Gratis', id: 'A_val_gratis' },
      { text: 'Quanto vale casa tua?', id: 'B_quanto_vale_sticky' }
    ]
  }
};

function getOrAssignVariant(testName, variantCount) {
  var key = 'ab_' + testName;
  var stored = localStorage.getItem(key);
  if (stored !== null && parseInt(stored) < variantCount) return parseInt(stored);
  var chosen = Math.floor(Math.random() * variantCount);
  try { localStorage.setItem(key, chosen); } catch(e) {}
  return chosen;
}

function runABTests() {
  Object.keys(defined_tests).forEach(function(testName) {
    var test = defined_tests[testName];
    var el = document.querySelector(test.selector);
    if (!el || !test.variants.length) return;

    var idx = getOrAssignVariant(testName, test.variants.length);
    var variant = test.variants[idx];

    // Aggiorna solo testo, mantieni icone SVG
    var svgChild = el.querySelector('svg');
    if (svgChild) {
      // Ha un'icona: aggiorna solo testo dopo SVG
      var textNodes = [];
      el.childNodes.forEach(function(n) {
        if (n.nodeType === 3 && n.textContent.trim()) textNodes.push(n);
      });
      if (textNodes.length) {
        textNodes[textNodes.length - 1].textContent = '\n          ' + variant.text + '\n        ';
      }
    } else {
      el.textContent = variant.text;
    }

    el.setAttribute('data-ab-test', testName);
    el.setAttribute('data-ab-variant', variant.id);
  });
}


/* ═══════════════════════════════════════════════════
   2. GA4 CTA TRACKING
   Traccia click su ogni CTA importante
   ═══════════════════════════════════════════════════ */

var tracked_selectors = [
  { sel: '.btn-g', category: 'cta_click', label: 'btn_gold' },
  { sel: '.btn-p', category: 'cta_click', label: 'btn_primary' },
  { sel: '.nav-cta', category: 'cta_click', label: 'nav_cta' },
  { sel: '.nav-mobile-cta', category: 'cta_click', label: 'nav_mobile_cta' },
  { sel: '.scta-primary', category: 'cta_click', label: 'sticky_primary' },
  { sel: '.scta-wa', category: 'cta_click', label: 'sticky_whatsapp' },
  { sel: '.scta-tel', category: 'cta_click', label: 'sticky_telefono' },
  { sel: '.wa-float', category: 'cta_click', label: 'whatsapp_float' },
  { sel: '.h-btn', category: 'cta_click', label: 'header_btn' },
  { sel: '.hero-cta', category: 'cta_click', label: 'hero_cta' },
  { sel: '.fsubmit', category: 'form_submit', label: 'contact_form' },
  { sel: '.fc-submit', category: 'form_submit', label: 'landing_form' },
  { sel: 'a[href*="wa.me"]', category: 'cta_click', label: 'whatsapp_link' },
  { sel: 'a[href^="tel:"]', category: 'cta_click', label: 'telefono_link' }
];

function trackEvent(category, action, label, extraData) {
  if (typeof gtag === 'function') {
    var params = { event_category: category, event_label: label };
    if (extraData) {
      Object.keys(extraData).forEach(function(k) { params[k] = extraData[k]; });
    }
    gtag('event', action, params);
  }
}

function setupCTATracking() {
  tracked_selectors.forEach(function(item) {
    document.querySelectorAll(item.sel).forEach(function(el) {
      if (el.hasAttribute('data-tracked')) return;
      el.setAttribute('data-tracked', '1');
      el.addEventListener('click', function() {
        var abTest = el.getAttribute('data-ab-test') || '';
        var abVariant = el.getAttribute('data-ab-variant') || '';
        var extra = {};
        if (abTest) {
          extra.ab_test = abTest;
          extra.ab_variant = abVariant;
        }
        extra.page_path = location.pathname;
        extra.cta_text = (el.textContent || '').trim().substring(0, 50);
        trackEvent(item.category, 'click', item.label, extra);
      });
    });
  });
}


/* ═══════════════════════════════════════════════════
   3. SPEED-TO-LEAD — Auto-risposta immediata
   Mostra conferma istantanea + countdown prossimo contatto
   ═══════════════════════════════════════════════════ */

function enhanceSpeedToLead() {
  // Migliora il messaggio di successo form contatti
  var successDiv = document.getElementById('success');
  if (successDiv) {
    var originalForm = document.getElementById('contact-form');
    if (originalForm) {
      var origSubmit = originalForm.onsubmit;
      // Sovrascriviamo sendForm per aggiungere speed-to-lead
      var origSendForm = window.sendForm;
      if (origSendForm) {
        window.sendForm = function() {
          // Salva il nome per personalizzare il messaggio
          var nome = (document.getElementById('f-nome') || {}).value || '';
          window._leadNome = nome.trim();
          window._leadTime = new Date();
          return origSendForm.apply(this, arguments);
        };
      }

      // Observer per quando il div success diventa visibile
      var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(m) {
          if (m.type === 'attributes' && successDiv.style.display === 'block') {
            showSpeedToLeadConfirmation(successDiv);
          }
        });
      });
      observer.observe(successDiv, { attributes: true, attributeFilter: ['style'] });
    }
  }
}

function showSpeedToLeadConfirmation(container) {
  var nome = window._leadNome || '';
  var saluto = nome ? ('Grazie ' + nome + '!') : 'Grazie!';

  container.innerHTML =
    '<div style="text-align:center;padding:1.5rem">' +
      '<div style="width:64px;height:64px;background:rgba(30,132,73,0.12);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1rem;animation:scaleIn 0.4s ease">' +
        '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#1E8449" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>' +
      '</div>' +
      '<h3 style="font-family:Cormorant Garamond,serif;font-size:1.6rem;color:#1E8449;margin-bottom:0.5rem">' + saluto + '</h3>' +
      '<p style="font-size:0.88rem;color:#2C4A6E;line-height:1.7;margin-bottom:1rem">' +
        'La tua richiesta e\' stata ricevuta. <strong>Ti ricontattiamo entro pochi minuti</strong> durante gli orari di apertura.' +
      '</p>' +
      '<div style="display:flex;gap:0.5rem;justify-content:center;flex-wrap:wrap;margin-bottom:1rem">' +
        '<div style="background:rgba(184,212,74,0.12);border:1px solid rgba(184,212,74,0.25);border-radius:8px;padding:0.6rem 1rem;text-align:center">' +
          '<div style="font-size:0.62rem;text-transform:uppercase;letter-spacing:1px;color:#6B7A8D;margin-bottom:0.2rem">Tempo medio risposta</div>' +
          '<div style="font-size:1.2rem;font-weight:700;color:#2C4A6E" id="speed-counter">< 30 min</div>' +
        '</div>' +
        '<div style="background:rgba(30,132,73,0.08);border:1px solid rgba(30,132,73,0.18);border-radius:8px;padding:0.6rem 1rem;text-align:center">' +
          '<div style="font-size:0.62rem;text-transform:uppercase;letter-spacing:1px;color:#6B7A8D;margin-bottom:0.2rem">Stato richiesta</div>' +
          '<div style="font-size:0.85rem;font-weight:700;color:#1E8449;display:flex;align-items:center;gap:4px;justify-content:center"><span style="width:8px;height:8px;background:#1E8449;border-radius:50%;display:inline-block;animation:pulseUrgency 1.5s infinite"></span> Ricevuta</div>' +
        '</div>' +
      '</div>' +
      '<p style="font-size:0.78rem;color:#6B7A8D;line-height:1.6">' +
        'Vuoi una risposta immediata? Chiamaci o scrivici su WhatsApp:' +
      '</p>' +
      '<div style="display:flex;gap:0.5rem;justify-content:center;flex-wrap:wrap;margin-top:0.75rem">' +
        '<a href="tel:+390498843484" style="display:inline-flex;align-items:center;gap:6px;background:#2C4A6E;color:#fff;padding:10px 18px;border-radius:8px;font-size:0.78rem;font-weight:600;transition:all 0.2s" data-tracked="1" onclick="trackEvent(\'speed_to_lead\',\'click\',\'call_after_form\')">' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 8.81 19.79 19.79 0 01.01 2.18 2 2 0 012 .18H5a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 14.92z"/></svg>' +
          '049.88.43.484' +
        '</a>' +
        '<a href="https://wa.me/393497365930?text=Ciao%2C%20ho%20appena%20compilato%20il%20form%20sul%20sito.%20Vorrei%20parlare%20con%20un%20agente." target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:6px;background:#25d366;color:#fff;padding:10px 18px;border-radius:8px;font-size:0.78rem;font-weight:600;transition:all 0.2s" data-tracked="1" onclick="trackEvent(\'speed_to_lead\',\'click\',\'whatsapp_after_form\')">' +
          '<svg width="14" height="14" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/></svg>' +
          'WhatsApp' +
        '</a>' +
      '</div>' +
    '</div>';

  // Track speed-to-lead conversion
  trackEvent('speed_to_lead', 'form_submitted', 'contact_form', {
    response_promise: 'under_30_min',
    lead_name: nome
  });
}


/* ═══════════════════════════════════════════════════
   4. SEGMENTAZIONE LEAD — Acquirente vs Venditore
   Rileva intento dall'oggetto del form e personalizza UX
   ═══════════════════════════════════════════════════ */

var INTENT_MAP = {
  'Voglio vendere un immobile': 'venditore',
  'Valutazione gratuita del mio immobile': 'venditore',
  'Gestione contratto di locazione': 'venditore',
  'Voglio acquistare un immobile': 'acquirente',
  'Cerco casa in affitto': 'acquirente',
  'Informazioni su un immobile in catalogo': 'acquirente',
  'Consulenza preliminari di compravendita': 'neutro',
  'Voglio affittare un immobile': 'venditore',
  'Altro': 'neutro'
};

function setupLeadSegmentation() {
  var selectObj = document.getElementById('f-obj');
  if (!selectObj) return;

  selectObj.addEventListener('change', function() {
    var intent = INTENT_MAP[selectObj.value] || 'neutro';
    var msgField = document.getElementById('f-msg');
    if (!msgField) return;

    // Aggiorna placeholder in base all'intento
    if (intent === 'venditore') {
      msgField.placeholder = 'Descrivici il tuo immobile: tipo (appartamento, villa...), metratura, zona e quando vorresti vendere.\n\nEs: Ho un appartamento di 120 mq a Padova centro, ristrutturato nel 2020. Vorrei venderlo entro l\'estate.';
    } else if (intent === 'acquirente') {
      msgField.placeholder = 'Dicci cosa cerchi: tipo di immobile, zona preferita, budget e tempistiche.\n\nEs: Cerco un trilocale in zona Arcella o Pontevigodarzere, budget 180-220k, possibilmente con garage.';
    }

    // Salva intento per il tracking
    window._leadIntent = intent;

    trackEvent('lead_segmentation', 'intent_detected', intent, {
      selected_option: selectObj.value
    });
  });
}

// Aggiungi intento al salvataggio Supabase
function patchSupabaseInsert() {
  var origSendForm = window.sendForm;
  if (!origSendForm || window._sendFormPatched) return;
  window._sendFormPatched = true;

  window.sendForm = function() {
    // Aggiungi intento al messaggio per Supabase
    var intent = window._leadIntent || 'non_specificato';
    var obj = document.getElementById('f-obj');
    if (obj && obj.value) {
      window._leadSegment = {
        intent: intent,
        oggetto: obj.value,
        timestamp: new Date().toISOString(),
        page: location.pathname,
        referrer: document.referrer || 'diretto',
        device: window.innerWidth < 768 ? 'mobile' : 'desktop'
      };
    }
    return origSendForm.apply(this, arguments);
  };
}


/* ═══════════════════════════════════════════════════
   5. SOCIAL PROOF DINAMICA
   Mostra notifiche di attivita' recente
   ═══════════════════════════════════════════════════ */

var social_proofs = [
  { text: 'Marco ha richiesto una valutazione a Padova Centro', time: '12 min fa', icon: 'home' },
  { text: 'Famiglia Zanetti ha venduto casa a Limena', time: '2 giorni fa', icon: 'check' },
  { text: 'Anna ha simulato il mutuo per un trilocale', time: '28 min fa', icon: 'calc' },
  { text: 'Luca ha prenotato un virtual tour a Selvazzano', time: '1 ora fa', icon: 'eye' },
  { text: '3 nuove richieste di valutazione oggi', time: 'oggi', icon: 'trending' },
  { text: 'Silvia ha trovato casa ad Albignasego', time: '4 giorni fa', icon: 'heart' }
];

var proofIndex = 0;
var proofContainer = null;

function createProofContainer() {
  var div = document.createElement('div');
  div.id = 'social-proof';
  div.setAttribute('role', 'status');
  div.setAttribute('aria-live', 'polite');
  div.style.cssText = 'position:fixed;bottom:80px;left:20px;z-index:190;max-width:320px;' +
    'background:#fff;border:1px solid rgba(44,74,110,0.12);border-radius:12px;' +
    'padding:14px 18px;box-shadow:0 8px 32px rgba(21,36,53,0.12);' +
    'transform:translateX(-120%);transition:transform 0.4s cubic-bezier(0.22,1,0.36,1);' +
    'font-family:Montserrat,sans-serif;cursor:pointer';
  div.addEventListener('click', function() { hideProof(); });
  document.body.appendChild(div);
  return div;
}

function showProof() {
  if (!proofContainer) proofContainer = createProofContainer();
  var proof = social_proofs[proofIndex % social_proofs.length];
  proofIndex++;

  var icons = {
    home: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#B8D44A" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    check: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1E8449" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>',
    calc: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2C4A6E" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="10" y2="10"/><line x1="14" y1="10" x2="16" y2="10"/></svg>',
    eye: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4E789A" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
    trending: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#B8D44A" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>',
    heart: '<svg width="16" height="16" viewBox="0 0 24 24" fill="#C0392B" stroke="none"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>'
  };

  proofContainer.innerHTML =
    '<div style="display:flex;align-items:flex-start;gap:10px">' +
      '<div style="width:32px;height:32px;background:rgba(184,212,74,0.12);border-radius:8px;display:flex;align-items:center;justify-content:center;flex-shrink:0">' +
        (icons[proof.icon] || icons.home) +
      '</div>' +
      '<div>' +
        '<div style="font-size:0.78rem;font-weight:600;color:#152435;line-height:1.4">' + proof.text + '</div>' +
        '<div style="font-size:0.65rem;color:#6B7A8D;margin-top:3px">' + proof.time + '</div>' +
      '</div>' +
      '<div style="position:absolute;top:6px;right:10px;font-size:0.7rem;color:#9AACBD;cursor:pointer;padding:4px" aria-label="Chiudi">&times;</div>' +
    '</div>';

  requestAnimationFrame(function() {
    proofContainer.style.transform = 'translateX(0)';
  });

  setTimeout(hideProof, 5000);

  trackEvent('social_proof', 'shown', proof.text.substring(0, 40));
}

function hideProof() {
  if (proofContainer) {
    proofContainer.style.transform = 'translateX(-120%)';
  }
}

function startSocialProof() {
  // Non mostrare su mobile (troppo invasivo)
  if (window.innerWidth < 768) return;
  // Prima notifica dopo 25 secondi
  setTimeout(function() {
    showProof();
    // Poi ogni 45 secondi
    setInterval(showProof, 45000);
  }, 25000);
}


/* ═══════════════════════════════════════════════════
   6. EXIT INTENT — Popup per chi sta uscendo
   ═══════════════════════════════════════════════════ */

var exitShown = false;

function setupExitIntent() {
  // Solo desktop — su mobile non funziona il mouseleave
  if (window.innerWidth < 768) return;
  // Non mostrare se ha gia' compilato un form in sessione
  if (sessionStorage.getItem('form_submitted')) return;

  document.addEventListener('mouseleave', function(e) {
    if (e.clientY > 10 || exitShown) return;
    if (sessionStorage.getItem('exit_dismissed')) return;
    exitShown = true;
    showExitPopup();
  });
}

function showExitPopup() {
  var overlay = document.createElement('div');
  overlay.id = 'exit-overlay';
  overlay.style.cssText = 'position:fixed;inset:0;background:rgba(21,36,53,0.6);z-index:9998;' +
    'display:flex;align-items:center;justify-content:center;padding:20px;' +
    'opacity:0;transition:opacity 0.3s';

  var isVenditore = window._leadIntent === 'venditore';
  var headline = isVenditore
    ? 'Stai pensando di vendere casa?'
    : 'Non hai trovato quello che cerchi?';
  var subtitle = isVenditore
    ? 'Richiedi una valutazione gratuita — scopri il valore reale del tuo immobile in 24 ore.'
    : 'Parlaci delle tue esigenze: ti aiutiamo a trovare la casa perfetta a Padova e provincia.';
  var ctaText = isVenditore ? 'Valutazione Gratuita' : 'Parla con un Agente';
  var ctaHref = isVenditore ? 'vendere-casa-padova-errori' : 'contatti';

  overlay.innerHTML =
    '<div style="background:#fff;border-radius:16px;max-width:460px;width:100%;padding:40px 36px;text-align:center;' +
    'box-shadow:0 24px 64px rgba(21,36,53,0.25);position:relative;transform:scale(0.9);transition:transform 0.3s">' +
      '<button onclick="this.closest(\'#exit-overlay\').remove();sessionStorage.setItem(\'exit_dismissed\',\'1\')" ' +
        'style="position:absolute;top:12px;right:16px;background:none;border:none;font-size:1.4rem;color:#6B7A8D;cursor:pointer;padding:8px" aria-label="Chiudi">&times;</button>' +
      '<div style="width:56px;height:56px;background:rgba(184,212,74,0.12);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1.2rem">' +
        '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#B8D44A" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>' +
      '</div>' +
      '<h3 style="font-family:Cormorant Garamond,serif;font-size:1.6rem;font-weight:700;color:#152435;margin-bottom:0.6rem">' + headline + '</h3>' +
      '<p style="font-size:0.85rem;color:#6B7A8D;line-height:1.7;margin-bottom:1.5rem">' + subtitle + '</p>' +
      '<a href="' + ctaHref + '" style="display:inline-flex;align-items:center;gap:8px;background:#B8D44A;color:#152435;' +
        'padding:14px 28px;border-radius:8px;font-weight:800;font-size:0.82rem;letter-spacing:1px;text-transform:uppercase;' +
        'transition:all 0.2s;text-decoration:none" ' +
        'onclick="trackEvent(\'exit_intent\',\'click\',\'' + ctaText + '\')">' +
        ctaText +
      '</a>' +
      '<p style="font-size:0.72rem;color:#9AACBD;margin-top:1rem">127 recensioni — 4.9/5 su Google</p>' +
    '</div>';

  document.body.appendChild(overlay);

  requestAnimationFrame(function() {
    overlay.style.opacity = '1';
    overlay.querySelector('div').style.transform = 'scale(1)';
  });

  overlay.addEventListener('click', function(e) {
    if (e.target === overlay) {
      overlay.remove();
      sessionStorage.setItem('exit_dismissed', '1');
    }
  });

  trackEvent('exit_intent', 'shown', window._leadIntent || 'neutro');
}


/* ═══════════════════════════════════════════════════
   7. SCROLL DEPTH TRACKING
   Traccia quanto in basso scorre l'utente
   ═══════════════════════════════════════════════════ */

function setupScrollTracking() {
  var milestones = [25, 50, 75, 90];
  var fired = {};

  window.addEventListener('scroll', function() {
    var scrollPct = Math.round(
      (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
    );
    milestones.forEach(function(m) {
      if (scrollPct >= m && !fired[m]) {
        fired[m] = true;
        trackEvent('scroll_depth', 'reached', m + '%', { page_path: location.pathname });
      }
    });
  }, { passive: true });
}


/* ═══════════════════════════════════════════════════
   8. TIME ON PAGE TRACKING
   ═══════════════════════════════════════════════════ */

function setupTimeTracking() {
  var intervals = [30, 60, 120, 300];
  var start = Date.now();

  intervals.forEach(function(sec) {
    setTimeout(function() {
      trackEvent('engagement', 'time_on_page', sec + 's', {
        page_path: location.pathname,
        seconds: sec
      });
    }, sec * 1000);
  });
}


/* ═══════════════════════════════════════════════════
   INIT — Avvia tutto dopo il DOM ready
   ═══════════════════════════════════════════════════ */

function init() {
  runABTests();
  setupCTATracking();
  enhanceSpeedToLead();
  setupLeadSegmentation();
  patchSupabaseInsert();
  startSocialProof();
  setupExitIntent();
  setupScrollTracking();
  setupTimeTracking();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// Esponi trackEvent globalmente per i bottoni inline
window.trackEvent = trackEvent;

})();
