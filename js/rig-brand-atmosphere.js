/* Righetto — grain + monogramma RI (watermark di fondo) */
(function () {
  'use strict';

  function initBrandAtmosphere() {
    if (document.documentElement.dataset.rigBrandAtmosphere === '1') return;
    if (/admin\.html$/i.test(location.pathname || '')) return;
    if (!document.body) {
      document.addEventListener('DOMContentLoaded', initBrandAtmosphere, { once: true });
      return;
    }

    document.documentElement.dataset.rigBrandAtmosphere = '1';
    document.body.classList.add('rig-sugar-paper');

    if (!document.querySelector('.rig-brand-watermark')) {
      var wrap = document.createElement('div');
      wrap.className = 'rig-brand-watermark';
      wrap.setAttribute('aria-hidden', 'true');
      wrap.innerHTML =
        '<div class="rig-brand-watermark-item rig-brand-watermark-a">' + monogramSvg() + '</div>' +
        '<div class="rig-brand-watermark-item rig-brand-watermark-b">' + monogramSvg() + '</div>' +
        '<div class="rig-brand-watermark-item rig-brand-watermark-c">' + monogramSvg() + '</div>';
      document.body.insertBefore(wrap, document.body.firstChild);
    }
  }

  function monogramSvg() {
    return (
      '<svg viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' +
      '<circle cx="60" cy="60" r="50" stroke="currentColor" stroke-width="2.2"/>' +
      '<line x1="60" y1="8" x2="60" y2="2" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>' +
      '<line x1="88" y1="14" x2="91" y2="9" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>' +
      '<line x1="104" y1="38" x2="110" y2="36" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>' +
      '<line x1="16" y1="38" x2="10" y2="36" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>' +
      '<text x="60" y="74" text-anchor="middle" font-family="\'Cormorant Garamond\', Georgia, serif" font-size="38" font-weight="700" fill="currentColor" letter-spacing="-0.04em">RI</text>' +
      '</svg>'
    );
  }

  initBrandAtmosphere();
})();
