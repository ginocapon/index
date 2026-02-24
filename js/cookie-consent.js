/*  Cookie Consent — Righetto Immobiliare
    Conforme: GDPR UE 2016/679, Linee Guida Garante Privacy 10/06/2021
    ──────────────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var STORAGE_KEY = 'rig_cookie_consent';
  var COOKIE_POLICY_URL = 'cookie-policy.html';

  // ── Utilities ──────────────────────────────────────────────────────
  function getConsent() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)); } catch (e) { return null; }
  }
  function saveConsent(prefs) {
    prefs.timestamp = new Date().toISOString();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
  }

  // ── CSS (injected once) ────────────────────────────────────────────
  function injectCSS() {
    if (document.getElementById('rig-cc-style')) return;
    var s = document.createElement('style');
    s.id = 'rig-cc-style';
    s.textContent = [
      '#rig-cc-banner{position:fixed;bottom:0;left:0;right:0;z-index:99999;background:#152435;color:#fff;font-family:"Montserrat",sans-serif;padding:1.1rem 1.5rem;box-shadow:0 -4px 24px rgba(0,0,0,.25);display:flex;align-items:center;gap:1.2rem;flex-wrap:wrap;animation:rig-cc-up .35s ease}',
      '@keyframes rig-cc-up{from{transform:translateY(100%)}to{transform:translateY(0)}}',
      '#rig-cc-banner p{flex:1;min-width:260px;font-size:.82rem;line-height:1.7;color:rgba(255,255,255,.7);margin:0}',
      '#rig-cc-banner a{color:#B8D44A;text-decoration:underline}',
      '#rig-cc-banner a:hover{color:#CDED62}',
      '.rig-cc-btns{display:flex;gap:.5rem;flex-shrink:0;flex-wrap:wrap}',
      '.rig-cc-btn{padding:.5rem 1.1rem;border:none;border-radius:6px;font-family:"Montserrat",sans-serif;font-size:.76rem;font-weight:600;cursor:pointer;transition:all .2s;letter-spacing:.03em}',
      '.rig-cc-btn:hover{transform:translateY(-1px)}',
      '.rig-cc-accept{background:#B8D44A;color:#152435}',
      '.rig-cc-accept:hover{background:#CDED62}',
      '.rig-cc-prefs{background:transparent;color:rgba(255,255,255,.6);border:1px solid rgba(255,255,255,.2)}',
      '.rig-cc-prefs:hover{border-color:#B8D44A;color:#B8D44A}',

      /* Overlay + Panel */
      '#rig-cc-overlay{position:fixed;inset:0;z-index:100000;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;animation:rig-cc-fade .25s ease}',
      '@keyframes rig-cc-fade{from{opacity:0}to{opacity:1}}',
      '#rig-cc-panel{background:#fff;color:#152435;border-radius:12px;max-width:520px;width:92%;max-height:85vh;overflow-y:auto;font-family:"Montserrat",sans-serif;box-shadow:0 20px 60px rgba(0,0,0,.3)}',
      '.rig-cc-panel-head{display:flex;align-items:center;justify-content:space-between;padding:1.2rem 1.4rem;border-bottom:1px solid #E1DBD1}',
      '.rig-cc-panel-head h3{font-family:"Cormorant Garamond",serif;font-size:1.3rem;font-weight:600;margin:0}',
      '.rig-cc-close{background:none;border:none;font-size:1.4rem;cursor:pointer;color:#6B7A8D;padding:.2rem;line-height:1}',
      '.rig-cc-close:hover{color:#152435}',
      '.rig-cc-panel-body{padding:1.2rem 1.4rem}',
      '.rig-cc-cat{border:1px solid #E1DBD1;border-radius:8px;padding:.85rem 1rem;margin-bottom:.6rem}',
      '.rig-cc-cat-head{display:flex;align-items:center;justify-content:space-between;gap:.6rem}',
      '.rig-cc-cat-name{font-size:.85rem;font-weight:600}',
      '.rig-cc-cat-desc{font-size:.76rem;color:#6B7A8D;line-height:1.7;margin-top:.35rem}',
      '.rig-cc-tag{font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;background:#ECE7DF;color:#6B7A8D;padding:.15rem .45rem;border-radius:2px;font-weight:600}',
      '.rig-cc-tag.on{background:rgba(184,212,74,.15);color:#7a9e1a}',

      /* Toggle switch */
      '.rig-cc-toggle{position:relative;width:40px;height:22px;flex-shrink:0}',
      '.rig-cc-toggle input{opacity:0;width:0;height:0}',
      '.rig-cc-toggle label{position:absolute;inset:0;background:#E1DBD1;border-radius:11px;cursor:pointer;transition:background .2s}',
      '.rig-cc-toggle label::after{content:"";position:absolute;left:2px;top:2px;width:18px;height:18px;background:#fff;border-radius:50%;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.15)}',
      '.rig-cc-toggle input:checked+label{background:#B8D44A}',
      '.rig-cc-toggle input:checked+label::after{transform:translateX(18px)}',
      '.rig-cc-toggle input:disabled+label{opacity:.5;cursor:default}',

      '.rig-cc-panel-foot{padding:1rem 1.4rem;border-top:1px solid #E1DBD1;display:flex;justify-content:flex-end;gap:.5rem}',
      '.rig-cc-save{background:#152435;color:#fff;padding:.55rem 1.4rem;border:none;border-radius:6px;font-family:"Montserrat",sans-serif;font-size:.78rem;font-weight:600;cursor:pointer;transition:all .2s}',
      '.rig-cc-save:hover{background:#B8D44A;color:#152435;transform:translateY(-1px)}',

      '@media(max-width:600px){#rig-cc-banner{flex-direction:column;text-align:center;padding:1rem}.rig-cc-btns{width:100%;justify-content:center}}'
    ].join('\n');
    document.head.appendChild(s);
  }

  // ── Banner (primo livello) ─────────────────────────────────────────
  function showBanner() {
    if (document.getElementById('rig-cc-banner')) return;
    var b = document.createElement('div');
    b.id = 'rig-cc-banner';
    b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', 'Informativa cookie');
    b.innerHTML =
      '<p>Questo sito utilizza esclusivamente <strong>cookie tecnici</strong> necessari al funzionamento. ' +
      'Non utilizziamo cookie di profilazione o marketing. ' +
      'Per saperne di pi\u00f9 leggi la nostra <a href="' + COOKIE_POLICY_URL + '">Cookie Policy</a>.</p>' +
      '<div class="rig-cc-btns">' +
        '<button class="rig-cc-btn rig-cc-prefs" onclick="window.__rigCC.openPanel()">Preferenze</button>' +
        '<button class="rig-cc-btn rig-cc-accept" onclick="window.__rigCC.acceptAll()">Ho capito \u2713</button>' +
      '</div>';
    document.body.appendChild(b);
  }

  function hideBanner() {
    var b = document.getElementById('rig-cc-banner');
    if (b) b.remove();
  }

  // ── Panel (secondo livello) ────────────────────────────────────────
  function openPanel() {
    if (document.getElementById('rig-cc-overlay')) return;
    var consent = getConsent() || {};

    var ov = document.createElement('div');
    ov.id = 'rig-cc-overlay';
    ov.innerHTML =
      '<div id="rig-cc-panel">' +
        '<div class="rig-cc-panel-head">' +
          '<h3>Preferenze Cookie</h3>' +
          '<button class="rig-cc-close" onclick="window.__rigCC.closePanel()" aria-label="Chiudi">&times;</button>' +
        '</div>' +
        '<div class="rig-cc-panel-body">' +
          '<p style="font-size:.8rem;color:#6B7A8D;line-height:1.75;margin:0 0 1rem">Gestisci le tue preferenze sui cookie. I cookie necessari non possono essere disattivati perch\u00e9 essenziali al funzionamento del sito.</p>' +

          /* Necessari */
          '<div class="rig-cc-cat">' +
            '<div class="rig-cc-cat-head">' +
              '<span class="rig-cc-cat-name">Necessari</span>' +
              '<span class="rig-cc-tag on">Sempre attivi</span>' +
            '</div>' +
            '<div class="rig-cc-cat-desc">Cookie tecnici indispensabili per il funzionamento del sito: gestione delle preferenze, funzionalit\u00e0 di ricerca immobili e moduli di contatto.</div>' +
          '</div>' +

          /* Analitici */
          '<div class="rig-cc-cat">' +
            '<div class="rig-cc-cat-head">' +
              '<span class="rig-cc-cat-name">Analitici</span>' +
              '<div class="rig-cc-toggle"><input type="checkbox" id="rig-cc-analytics"' + (consent.analytics ? ' checked' : '') + '><label for="rig-cc-analytics"></label></div>' +
            '</div>' +
            '<div class="rig-cc-cat-desc">Cookie per analisi statistiche anonime sul traffico del sito. <em>Attualmente non utilizzati.</em></div>' +
          '</div>' +

          /* Marketing */
          '<div class="rig-cc-cat">' +
            '<div class="rig-cc-cat-head">' +
              '<span class="rig-cc-cat-name">Marketing</span>' +
              '<div class="rig-cc-toggle"><input type="checkbox" id="rig-cc-marketing"' + (consent.marketing ? ' checked' : '') + '><label for="rig-cc-marketing"></label></div>' +
            '</div>' +
            '<div class="rig-cc-cat-desc">Cookie per mostrare pubblicit\u00e0 pertinenti e misurarne l\u2019efficacia. <em>Attualmente non utilizzati.</em></div>' +
          '</div>' +

        '</div>' +
        '<div class="rig-cc-panel-foot">' +
          '<button class="rig-cc-save" onclick="window.__rigCC.savePrefs()">Salva preferenze</button>' +
        '</div>' +
      '</div>';

    /* Close on overlay click (outside panel) */
    ov.addEventListener('click', function (e) {
      if (e.target === ov) window.__rigCC.closePanel();
    });

    document.body.appendChild(ov);
  }

  function closePanel() {
    var ov = document.getElementById('rig-cc-overlay');
    if (ov) ov.remove();
  }

  // ── Actions ────────────────────────────────────────────────────────
  function acceptAll() {
    saveConsent({ necessary: true, analytics: true, marketing: true });
    hideBanner();
    closePanel();
  }

  function savePrefs() {
    var analytics = document.getElementById('rig-cc-analytics');
    var marketing = document.getElementById('rig-cc-marketing');
    saveConsent({
      necessary: true,
      analytics: analytics ? analytics.checked : false,
      marketing: marketing ? marketing.checked : false
    });
    hideBanner();
    closePanel();
  }

  // ── Public API (for footer link & inline onclick) ──────────────────
  window.__rigCC = {
    openPanel: openPanel,
    closePanel: closePanel,
    acceptAll: acceptAll,
    savePrefs: savePrefs
  };

  // ── Init ───────────────────────────────────────────────────────────
  injectCSS();
  if (!getConsent()) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', showBanner);
    } else {
      showBanner();
    }
  }
})();
