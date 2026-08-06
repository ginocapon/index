/**
 * Righetto Immobiliare — Trasparenza Reg. (UE) 2024/1689 (AI Act) e contenuti digitali.
 * Barra informativa sito + didascalie foto + helper testi condivisi.
 */
(function (global) {
  'use strict';

  var PRIVACY_ANCHOR = 'privacy#trasparenza-digitale';
  var PRIVACY_HREF = '/' + PRIVACY_ANCHOR;

  var TEXT = {
    footer:
      '<strong>Trasparenza digitale (AI Act UE):</strong> l\'assistente <strong>Linda</strong> è un sistema ' +
      'automatizzato a regole — non sostituisce un agente. Alcune <strong>foto e grafiche</strong> del sito ' +
      'possono essere state ottimizzate o parzialmente modificate con strumenti digitali, inclusa ' +
      'intelligenza artificiale. Stime e testi hanno valore informativo. ' +
      '<a href="' + PRIVACY_ANCHOR + '">Dettagli</a>',
    photoCaption:
      'Immagine di riferimento reale; possibile ottimizzazione digitale (anche con intelligenza artificiale), ' +
      'senza alterare le caratteristiche dichiarate. ' +
      '<a href="' + PRIVACY_HREF + '">Informativa</a>',
    photoCaptionCompact:
      'Foto reale, eventualmente ottimizzata digitalmente (anche IA). ' +
      '<a href="' + PRIVACY_HREF + '">Info</a>',
    chatHeader: 'Assistente digitale automatizzato',
    chatWelcome:
      'Sono un <strong>assistente digitale automatizzato</strong> (sistema a regole, senza IA generativa). ' +
      'Le risposte e le stime hanno valore <strong>orientativo</strong> e non sostituiscono una perizia, ' +
      'consulenza legale o fiscale. <a href="' + PRIVACY_HREF + '">Informativa</a>',
    chatFirst:
      'Ricorda: sono un assistente automatizzato. Per decisioni vincolanti contatta un agente al ' +
      '049.8843484 o in sede. <a href="' + PRIVACY_HREF + '">Trasparenza AI Act</a>.'
  };

  var SKIP_ANCESTORS =
    'header, footer, nav, button, .logo, #rig-chat-widget, .chat-avatar, .chat-welcome-card, ' +
    '.cf-avatar, .rig-carousel-nav, .cmp-thumb, .gt, .gallery-thumbs, .rig-photo-caption, ' +
    '.rig-ai-act-bar, .cookie-banner, .skip-link, .nav-burger, .rig-lightbox, #rig-lightbox';

  function isAdminPage() {
    var p = (global.location && global.location.pathname) || '';
    return /admin\.html$/i.test(p) || p.indexOf('/admin') !== -1;
  }

  function debounce(fn, ms) {
    var t;
    return function () {
      clearTimeout(t);
      var args = arguments;
      var self = this;
      t = setTimeout(function () {
        fn.apply(self, args);
      }, ms);
    };
  }

  function injectFooterBar() {
    if (isAdminPage()) return;
    if (document.getElementById('rig-ai-act-bar')) return;

    var bar = document.createElement('div');
    bar.id = 'rig-ai-act-bar';
    bar.className = 'rig-ai-act-bar';
    bar.setAttribute('role', 'note');
    bar.setAttribute('aria-label', 'Informativa trasparenza contenuti digitali e assistente automatizzato');
    bar.innerHTML = TEXT.footer;

    var footer = document.querySelector('footer');
    if (footer) {
      var bottom = footer.querySelector('.footer-bottom, .fbot');
      if (bottom) {
        footer.insertBefore(bar, bottom);
      } else {
        footer.appendChild(bar);
      }
      return;
    }

    document.body.appendChild(bar);
  }

  function shouldCaption(img) {
    if (!img || img.tagName !== 'IMG') return false;
    if (img.dataset.rigPhotoCaption === 'done' || img.dataset.rigPhotoCaption === 'skip') return false;
    if (img.closest(SKIP_ANCESTORS)) return false;

    var id = img.id || '';
    if (id === 'rig-chat-btn-avatar' || id === 'rig-chat-icon-close') return false;

    var cls = (img.className || '').toLowerCase();
    if (
      cls.indexOf('chat-welcome-photo') !== -1 ||
      cls.indexOf('cf-avatar') !== -1 ||
      cls.indexOf('chat-header-avatar') !== -1
    ) {
      return false;
    }

    var src = (img.getAttribute('src') || '').toLowerCase();
    if (!src || src.indexOf('data:') === 0) return false;
    if (/favicon|\.svg(\?|$)|spinner|loading\.gif|pixel\.gif|1x1/.test(src)) return false;

    var rect = img.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0 && rect.width < 40 && rect.height < 40) return false;

    return true;
  }

  function captionHtml(compact) {
    return compact ? TEXT.photoCaptionCompact : TEXT.photoCaption;
  }

  function makeCaption(compact) {
    var cap = document.createElement('figcaption');
    cap.className = 'rig-photo-caption' + (compact ? ' rig-photo-caption--compact' : '');
    cap.setAttribute('role', 'note');
    cap.setAttribute('aria-label', 'Informativa trasparenza immagine');
    cap.innerHTML = captionHtml(compact);
    return cap;
  }

  function hasCaptionNear(node) {
    if (!node) return false;
    if (node.querySelector && node.querySelector('.rig-photo-caption')) return true;
    var sib = node.nextElementSibling;
    return !!(sib && sib.classList && sib.classList.contains('rig-photo-caption'));
  }

  function markDone(img) {
    img.dataset.rigPhotoCaption = 'done';
  }

  function captionCarousel(carousel) {
    if (!carousel || carousel.dataset.rigCarouselCaption === 'done') return;
    if (hasCaptionNear(carousel)) {
      carousel.dataset.rigCarouselCaption = 'done';
      return;
    }
    carousel.dataset.rigCarouselCaption = 'done';
    carousel.appendChild(makeCaption(false));
    carousel.querySelectorAll('img').forEach(function (img) {
      markDone(img);
    });
  }

  function insertCaptionForImg(img) {
    if (!shouldCaption(img)) return;

    var carousel = img.closest('.rig-carousel');
    if (carousel) {
      captionCarousel(carousel);
      return;
    }

    if (img.closest('.gallery-thumbs, .gt, .cmp-thumb')) {
      img.dataset.rigPhotoCaption = 'skip';
      return;
    }

    var figure = img.closest('figure');
    if (figure) {
      if (!figure.querySelector('.rig-photo-caption')) {
        figure.appendChild(makeCaption(false));
      }
      markDone(img);
      return;
    }

    var cardImg = img.closest('.card-img');
    if (cardImg) {
      if (!hasCaptionNear(cardImg)) {
        cardImg.parentNode.insertBefore(makeCaption(true), cardImg.nextSibling);
      }
      markDone(img);
      return;
    }

    var blogFig = img.closest('.blog-fig, .art-figure');
    if (blogFig) {
      if (!blogFig.querySelector('.rig-photo-caption')) {
        blogFig.appendChild(makeCaption(false));
      }
      markDone(img);
      return;
    }

    var hero = img.closest('.art-hero');
    if (hero) {
      if (!hasCaptionNear(hero)) {
        hero.parentNode.insertBefore(makeCaption(false), hero.nextSibling);
      }
      markDone(img);
      return;
    }

    var host = img.closest('.gallery-carousel-host, .gallery-main, .gallery-wrap');
    if (host) {
      if (!hasCaptionNear(host)) {
        host.parentNode.insertBefore(makeCaption(false), host.nextSibling);
      }
      markDone(img);
      return;
    }

    var parent = img.parentElement;
    if (!parent) return;
    if (parent.querySelector(':scope > .rig-photo-caption')) {
      markDone(img);
      return;
    }
    parent.insertBefore(makeCaption(false), img.nextSibling);
    markDone(img);
  }

  function injectPhotoCaptions() {
    if (isAdminPage()) return;
    var images = document.querySelectorAll('img:not([data-rig-photo-caption])');
    for (var i = 0; i < images.length; i++) {
      insertCaptionForImg(images[i]);
    }
    document.querySelectorAll('.rig-carousel:not([data-rig-carousel-caption])').forEach(captionCarousel);
  }

  var scheduleCaptions = debounce(injectPhotoCaptions, 280);

  function observeDynamicPhotos() {
    if (isAdminPage() || !global.MutationObserver) return;
    var observer = new MutationObserver(function (mutations) {
      for (var i = 0; i < mutations.length; i++) {
        if (mutations[i].addedNodes && mutations[i].addedNodes.length) {
          scheduleCaptions();
          return;
        }
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }

  function init() {
    injectFooterBar();
    injectPhotoCaptions();
    observeDynamicPhotos();
    global.addEventListener('load', injectPhotoCaptions);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.RigAiDisclosure = {
    TEXT: TEXT,
    PRIVACY_ANCHOR: PRIVACY_ANCHOR,
    injectFooterBar: injectFooterBar,
    injectPhotoCaptions: injectPhotoCaptions
  };
})(typeof window !== 'undefined' ? window : global);
