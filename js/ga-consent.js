/* Google Analytics 4 + Consent Mode v2 — G-PHEL8KXLBX */
(function () {
  'use strict';

  var GA_ID = 'G-PHEL8KXLBX';
  var STORAGE_KEY = 'rig_cookie_consent';

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  window.gtag = gtag;

  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });

  function applyFromPrefs(prefs) {
    if (!prefs) return;
    gtag('consent', 'update', {
      analytics_storage: prefs.analytics ? 'granted' : 'denied',
      ad_storage: prefs.marketing ? 'granted' : 'denied',
      ad_user_data: prefs.marketing ? 'granted' : 'denied',
      ad_personalization: prefs.marketing ? 'granted' : 'denied'
    });
  }

  function readStored() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  window.rigGaConsentUpdate = applyFromPrefs;

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);
  gtag('js', new Date());
  gtag('config', GA_ID, { anonymize_ip: true });

  applyFromPrefs(readStored());

  /* Trasparenza AI Act UE — barra sito (tutte le pagine pubbliche con ga-consent) */
  (function loadAiDisclosure() {
    if (/admin\.html$/i.test((location.pathname || ''))) return;
    var css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = 'css/site-ai-disclosure.css?v=5';
    document.head.appendChild(css);
    var s = document.createElement('script');
    s.src = 'js/site-ai-disclosure.js?v=5';
    s.defer = true;
    document.head.appendChild(s);
  })();
})();
