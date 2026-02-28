/**
 * Scroll Reveal — IntersectionObserver based
 * Aggiunge la classe "visible" agli elementi con classe "sr"
 * quando entrano nel viewport. Supporta stagger automatico.
 *
 * Principio Skills Anthropic: "One well-orchestrated page load
 * with staggered reveals creates more delight."
 */
(function() {
  'use strict';

  if (!('IntersectionObserver' in window)) {
    // Fallback: mostra tutto subito
    document.querySelectorAll('.sr, .sr-left, .sr-right, .sr-scale').forEach(function(el) {
      el.classList.add('visible');
    });
    return;
  }

  // Auto-stagger: assegna delay sr-d1...sr-d6 ai figli di grid/flex
  document.querySelectorAll('.sr-stagger').forEach(function(parent) {
    var children = parent.children;
    for (var i = 0; i < children.length && i < 6; i++) {
      children[i].classList.add('sr', 'sr-d' + (i + 1));
    }
  });

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.12,
    rootMargin: '0px 0px -40px 0px'
  });

  document.querySelectorAll('.sr, .sr-left, .sr-right, .sr-scale').forEach(function(el) {
    observer.observe(el);
  });
})();
