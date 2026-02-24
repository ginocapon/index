/* ══════════════════════════════════════════════════
   COOKIE CONSENT — Conforme Linee Guida Garante 10/06/2021
   ══════════════════════════════════════════════════ */
(function () {
  'use strict';

  var STORAGE_KEY = 'rig_cookie_consent';

  /* ── Leggi consenso salvato ── */
  function getConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  /* ── Salva consenso ── */
  function saveConsent(prefs) {
    prefs.timestamp = new Date().toISOString();
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs)); } catch (e) {}
  }

  /* ── Se consenso gia' dato, non mostrare il banner ── */
  if (getConsent()) return;

  /* ── CSS del banner ── */
  var style = document.createElement('style');
  style.textContent = [
    '#rig-cookie-banner{position:fixed;bottom:0;left:0;right:0;z-index:99999;background:#1a1a2e;color:#e0e0e0;font-family:"Montserrat","DM Sans",sans-serif;font-size:.82rem;line-height:1.6;box-shadow:0 -4px 24px rgba(0,0,0,.35);transition:transform .35s ease}',
    '#rig-cookie-banner.rig-hidden{transform:translateY(110%)}',
    '.rig-cb-inner{max-width:1200px;margin:0 auto;padding:18px 24px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}',
    '.rig-cb-text{flex:1;min-width:260px}',
    '.rig-cb-text a{color:#8AB4CE;text-decoration:underline}',
    '.rig-cb-btns{display:flex;gap:10px;flex-shrink:0}',
    '.rig-cb-btn{padding:9px 22px;border:none;border-radius:3px;font-family:inherit;font-size:.78rem;font-weight:600;cursor:pointer;letter-spacing:.3px;transition:opacity .2s}',
    '.rig-cb-accept{background:#B8D44A;color:#152435}',
    '.rig-cb-prefs{background:transparent;color:#8AB4CE;border:1px solid #8AB4CE}',
    '.rig-cb-btn:hover{opacity:.85}',
    /* Pannello preferenze */
    '#rig-cookie-prefs{position:fixed;top:0;left:0;right:0;bottom:0;z-index:100000;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.6)}',
    '#rig-cookie-prefs.rig-open{display:flex}',
    '.rig-cp-box{background:#fff;color:#152435;border-radius:6px;max-width:520px;width:92%;max-height:85vh;overflow-y:auto;padding:28px 26px;font-family:"Montserrat","DM Sans",sans-serif;position:relative}',
    '.rig-cp-box h3{font-size:1.1rem;margin-bottom:14px;font-weight:700}',
    '.rig-cp-box p{font-size:.8rem;color:#6B7A8D;line-height:1.7;margin-bottom:16px}',
    '.rig-cp-cat{border-top:1px solid #e8e4de;padding:14px 0;display:flex;align-items:center;justify-content:space-between}',
    '.rig-cp-cat-info{flex:1}',
    '.rig-cp-cat-name{font-size:.82rem;font-weight:600}',
    '.rig-cp-cat-desc{font-size:.72rem;color:#6B7A8D;margin-top:2px}',
    '.rig-cp-toggle{position:relative;width:42px;height:22px;flex-shrink:0;margin-left:12px}',
    '.rig-cp-toggle input{opacity:0;width:0;height:0}',
    '.rig-cp-slider{position:absolute;top:0;left:0;right:0;bottom:0;background:#ccc;border-radius:22px;cursor:pointer;transition:background .2s}',
    '.rig-cp-slider::before{content:"";position:absolute;height:16px;width:16px;left:3px;bottom:3px;background:#fff;border-radius:50%;transition:transform .2s}',
    '.rig-cp-toggle input:checked+.rig-cp-slider{background:#B8D44A}',
    '.rig-cp-toggle input:checked+.rig-cp-slider::before{transform:translateX(20px)}',
    '.rig-cp-toggle input:disabled+.rig-cp-slider{background:#B8D44A;opacity:.6;cursor:default}',
    '.rig-cp-actions{display:flex;gap:10px;margin-top:18px;justify-content:flex-end}',
    '.rig-cp-save{padding:9px 24px;border:none;border-radius:3px;background:#2C4A6E;color:#fff;font-family:inherit;font-size:.78rem;font-weight:600;cursor:pointer}',
    '.rig-cp-reject{padding:9px 24px;border:1px solid #ccc;border-radius:3px;background:transparent;color:#6B7A8D;font-family:inherit;font-size:.78rem;cursor:pointer}',
    '.rig-cp-close{position:absolute;top:14px;right:16px;background:none;border:none;font-size:1.3rem;cursor:pointer;color:#6B7A8D;line-height:1}',
    '@media(max-width:600px){.rig-cb-inner{flex-direction:column;text-align:center}.rig-cb-btns{justify-content:center;width:100%}}'
  ].join('\n');
  document.head.appendChild(style);

  /* ── Banner HTML ── */
  var banner = document.createElement('div');
  banner.id = 'rig-cookie-banner';
  banner.innerHTML =
    '<div class="rig-cb-inner">' +
      '<div class="rig-cb-text">' +
        'Questo sito utilizza cookie tecnici necessari al funzionamento. ' +
        'Per saperne di pi\u00f9 consulta la nostra <a href="cookie-policy.html">Cookie Policy</a>.' +
      '</div>' +
      '<div class="rig-cb-btns">' +
        '<button class="rig-cb-btn rig-cb-accept" id="rig-cb-accept">Ho capito</button>' +
        '<button class="rig-cb-btn rig-cb-prefs" id="rig-cb-prefs">Preferenze</button>' +
      '</div>' +
    '</div>';
  document.body.appendChild(banner);

  /* ── Pannello preferenze HTML ── */
  var prefs = document.createElement('div');
  prefs.id = 'rig-cookie-prefs';
  prefs.innerHTML =
    '<div class="rig-cp-box">' +
      '<button class="rig-cp-close" id="rig-cp-close" aria-label="Chiudi">&times;</button>' +
      '<h3>Preferenze Cookie</h3>' +
      '<p>Puoi gestire le tue preferenze sui cookie. I cookie necessari sono sempre attivi perch\u00e9 indispensabili per il funzionamento del sito.</p>' +
      /* Necessari */
      '<div class="rig-cp-cat">' +
        '<div class="rig-cp-cat-info">' +
          '<div class="rig-cp-cat-name">Necessari</div>' +
          '<div class="rig-cp-cat-desc">Cookie tecnici indispensabili (consenso, sessione, sicurezza). Sempre attivi.</div>' +
        '</div>' +
        '<label class="rig-cp-toggle"><input type="checkbox" checked disabled><span class="rig-cp-slider"></span></label>' +
      '</div>' +
      /* Analitici */
      '<div class="rig-cp-cat">' +
        '<div class="rig-cp-cat-info">' +
          '<div class="rig-cp-cat-name">Analitici</div>' +
          '<div class="rig-cp-cat-desc">Ci aiutano a capire come i visitatori interagiscono con il sito (es. Google Analytics).</div>' +
        '</div>' +
        '<label class="rig-cp-toggle"><input type="checkbox" id="rig-pref-analytics"><span class="rig-cp-slider"></span></label>' +
      '</div>' +
      /* Marketing */
      '<div class="rig-cp-cat">' +
        '<div class="rig-cp-cat-info">' +
          '<div class="rig-cp-cat-name">Marketing</div>' +
          '<div class="rig-cp-cat-desc">Utilizzati per mostrare annunci pertinenti e misurare l\'efficacia delle campagne.</div>' +
        '</div>' +
        '<label class="rig-cp-toggle"><input type="checkbox" id="rig-pref-marketing"><span class="rig-cp-slider"></span></label>' +
      '</div>' +
      '<div class="rig-cp-actions">' +
        '<button class="rig-cp-reject" id="rig-cp-reject">Rifiuta non necessari</button>' +
        '<button class="rig-cp-save" id="rig-cp-save">Salva preferenze</button>' +
      '</div>' +
    '</div>';
  document.body.appendChild(prefs);

  /* ── Logica ── */
  function closeBanner() {
    banner.classList.add('rig-hidden');
    setTimeout(function () { banner.style.display = 'none'; }, 400);
  }

  function openPrefs() {
    prefs.classList.add('rig-open');
  }

  function closePrefs() {
    prefs.classList.remove('rig-open');
  }

  /* Accetta tutto */
  document.getElementById('rig-cb-accept').addEventListener('click', function () {
    saveConsent({ necessary: true, analytics: false, marketing: false });
    closeBanner();
  });

  /* Apri preferenze */
  document.getElementById('rig-cb-prefs').addEventListener('click', openPrefs);

  /* Chiudi pannello preferenze */
  document.getElementById('rig-cp-close').addEventListener('click', closePrefs);
  prefs.addEventListener('click', function (e) {
    if (e.target === prefs) closePrefs();
  });

  /* Salva preferenze */
  document.getElementById('rig-cp-save').addEventListener('click', function () {
    saveConsent({
      necessary: true,
      analytics: !!document.getElementById('rig-pref-analytics').checked,
      marketing: !!document.getElementById('rig-pref-marketing').checked
    });
    closePrefs();
    closeBanner();
  });

  /* Rifiuta non necessari */
  document.getElementById('rig-cp-reject').addEventListener('click', function () {
    document.getElementById('rig-pref-analytics').checked = false;
    document.getElementById('rig-pref-marketing').checked = false;
    saveConsent({ necessary: true, analytics: false, marketing: false });
    closePrefs();
    closeBanner();
  });

  /* ── Link "Preferenze Cookie" nel footer ── */
  document.addEventListener('DOMContentLoaded', function () {
    var links = document.querySelectorAll('[data-cookie-prefs]');
    for (var i = 0; i < links.length; i++) {
      links[i].addEventListener('click', function (e) {
        e.preventDefault();
        /* Riapre il banner se serve, oppure solo il pannello preferenze */
        prefs.classList.add('rig-open');
      });
    }
  });

})();
