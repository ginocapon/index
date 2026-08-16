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
      'intelligenza artificiale. Le immagini <strong>generate con IA</strong> sono marchiate <strong>FOTO AI</strong>. ' +
      'Stime e testi hanno valore informativo. ' +
      '<a href="' + PRIVACY_ANCHOR + '">Dettagli</a>',
    photoCaptionListing:
      'Foto dell\'annuncio riferita all\'immobile reale. Possiamo correggere graficamente luminosità, contrasto, esposizione e nitidezza, anche con strumenti digitali o IA, ' +
      'senza alterare tipologia, metrature e stato dichiarati in scheda. ' +
      '<a href="' + PRIVACY_HREF + '">Informativa</a>',
    photoCaptionListingCompact:
      'Foto reale; possibili correzioni grafiche (esposizione, luminosità, anche IA). ' +
      '<a href="' + PRIVACY_HREF + '">Info</a>',
    photoCaptionBlog:
      'Immagine editoriale <strong>elaborata digitalmente</strong> (anche con intelligenza artificiale): illustrazione a scopo informativo, ' +
      'non documento fotografico dell\'immobile o della scena descritta nel testo. Le immagini generate con IA sono contrassegnate con il marchio <strong>FOTO AI</strong> in basso a sinistra. ' +
      '<a href="' + PRIVACY_HREF + '">Informativa</a>',
    photoCaptionGeneral:
      'Immagine a scopo informativo; eventuale elaborazione digitale (anche IA) come da ' +
      '<a href="' + PRIVACY_HREF + '">informativa trasparenza</a>.',
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

  var AI_MANIFEST = {
    pathPrefixes: ['img/blog/'],
    excludePaths: [],
    explicitPaths: [],
    files: []
  };

  var WATERMARK_LABEL = 'FOTO AI';

  function isAdminPage() {
    var p = (global.location && global.location.pathname) || '';
    return /admin\.html$/i.test(p) || p.indexOf('/admin') !== -1;
  }

  function normalizeSrc(src) {
    if (!src) return '';
    var s = src.split('?')[0].split('#')[0].toLowerCase();
    if (s.indexOf('//') === 0) return s;
    if (s.indexOf('http') === 0) {
      try {
        s = new URL(s).pathname.toLowerCase();
      } catch (e) { /* keep */ }
    }
    return s.replace(/^\//, '');
  }

  function loadAiManifest() {
    return fetch('/data/ai-generated-images.json', { cache: 'no-store' })
      .then(function (r) {
        if (!r.ok) return;
        return r.json();
      })
      .then(function (data) {
        if (!data) return;
        if (data.pathPrefixes) AI_MANIFEST.pathPrefixes = data.pathPrefixes;
        if (data.excludePaths) AI_MANIFEST.excludePaths = data.excludePaths;
        if (data.explicitPaths) AI_MANIFEST.explicitPaths = data.explicitPaths;
        if (data.files) AI_MANIFEST.files = data.files;
      })
      .catch(function () { /* manifest opzionale offline */ });
  }

  function isAiGeneratedImage(img) {
    if (!img) return false;
    if (img.dataset.aiGenerated === 'false' || img.getAttribute('data-ai-generated') === 'false') {
      return false;
    }
    if (img.dataset.aiGenerated === 'true' || img.getAttribute('data-ai-generated') === 'true') {
      return true;
    }
    var src = normalizeSrc(img.getAttribute('src') || img.currentSrc || '');
    if (!src) return false;
    for (var i = 0; i < AI_MANIFEST.excludePaths.length; i++) {
      if (src.indexOf(AI_MANIFEST.excludePaths[i].toLowerCase()) !== -1) return false;
    }
    for (var j = 0; j < AI_MANIFEST.explicitPaths.length; j++) {
      if (src.indexOf(AI_MANIFEST.explicitPaths[j].toLowerCase()) !== -1) return true;
    }
    for (var k = 0; k < AI_MANIFEST.files.length; k++) {
      if (src === AI_MANIFEST.files[k].toLowerCase() || src.endsWith('/' + AI_MANIFEST.files[k].toLowerCase())) {
        return true;
      }
    }
    for (var p = 0; p < AI_MANIFEST.pathPrefixes.length; p++) {
      var pref = AI_MANIFEST.pathPrefixes[p].toLowerCase();
      if (src.indexOf(pref) !== -1 || src.indexOf('/' + pref) !== -1) return true;
    }
    return false;
  }

  function watermarkHostFor(img) {
    return (
      img.closest('.art-hero__frame, .blog-fig__frame, .rig-ai-photo-wrap, .card-img, figure.blog-fig, .art-hero') ||
      img.parentElement
    );
  }

  function applyAiWatermark(img) {
    if (!img || img.dataset.rigAiWatermark === 'done') return;
    if (!isAiGeneratedImage(img)) return;

    var host = watermarkHostFor(img);
    if (!host) return;
    if (host.querySelector('.rig-ai-photo-watermark')) {
      img.dataset.rigAiWatermark = 'done';
      return;
    }

    if (!host.classList.contains('rig-ai-photo-wrap') &&
        !host.classList.contains('art-hero__frame') &&
        !host.classList.contains('blog-fig__frame') &&
        !host.classList.contains('card-img') &&
        host.tagName !== 'FIGURE') {
      host.classList.add('rig-ai-photo-wrap');
    }

    var wm = document.createElement('span');
    wm.className = 'rig-ai-photo-watermark';
    wm.setAttribute('aria-hidden', 'true');
    wm.textContent = WATERMARK_LABEL;
    host.appendChild(wm);
    img.dataset.rigAiWatermark = 'done';
    img.setAttribute('data-ai-generated', 'true');
  }

  function applyAllAiWatermarks() {
    if (isAdminPage()) return;
    var images = document.querySelectorAll('img');
    for (var i = 0; i < images.length; i++) {
      var img = images[i];
      if (img.dataset.rigAiWatermark === 'done') continue;
      if (img.closest(SKIP_ANCESTORS)) continue;
      var src = (img.getAttribute('src') || '').toLowerCase();
      if (!src || src.indexOf('data:') === 0) continue;
      var rect = img.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0 && rect.width < 40 && rect.height < 40) continue;
      applyAiWatermark(img);
    }
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

  function classifyImage(img) {
    var src = (img.getAttribute('src') || '').toLowerCase();
    if (src.indexOf('/img/blog/') !== -1 || src.indexOf('img/blog/') !== -1) return 'blog';
    if (src.indexOf('/img/immobili/') !== -1 || src.indexOf('img/immobili/') !== -1) return 'listing';
    if (img.closest('.art-hero, .blog-fig, .art-figure, article .article-content')) return 'blog';
    if (img.closest('.card-img, .gallery-wrap, .gallery-main, .rig-carousel, .immobile')) return 'listing';
    return 'general';
  }

  function captionHtmlFor(img, compact) {
    var kind = classifyImage(img);
    if (kind === 'blog') return TEXT.photoCaptionBlog;
    if (kind === 'listing') return compact ? TEXT.photoCaptionListingCompact : TEXT.photoCaptionListing;
    return TEXT.photoCaptionGeneral;
  }

  function makeCaption(img, compact) {
    var cap = document.createElement('figcaption');
    cap.className = 'rig-photo-caption' + (compact ? ' rig-photo-caption--compact' : '');
    cap.setAttribute('role', 'note');
    cap.setAttribute('aria-label', 'Informativa trasparenza immagine');
    cap.innerHTML = captionHtmlFor(img, compact);
    return cap;
  }

  function upsertFigureCaption(figure, img, compact) {
    var existing = figure.querySelector('figcaption');
    var html = captionHtmlFor(img, compact);
    if (existing) {
      existing.className = 'rig-photo-caption' + (compact ? ' rig-photo-caption--compact' : '');
      existing.setAttribute('role', 'note');
      existing.innerHTML = html;
      return existing;
    }
    var cap = makeCaption(img, compact);
    figure.appendChild(cap);
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
    var sampleImg = carousel.querySelector('img');
    carousel.appendChild(makeCaption(sampleImg || carousel, false));
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
      upsertFigureCaption(figure, img, false);
      markDone(img);
      return;
    }

    var cardImg = img.closest('.card-img');
    if (cardImg) {
      if (!hasCaptionNear(cardImg)) {
        cardImg.parentNode.insertBefore(makeCaption(img, true), cardImg.nextSibling);
      }
      markDone(img);
      return;
    }

    var blogFig = img.closest('.blog-fig, .art-figure');
    if (blogFig) {
      if (blogFig.tagName === 'FIGURE') {
        upsertFigureCaption(blogFig, img, false);
      } else if (!blogFig.querySelector('.rig-photo-caption')) {
        blogFig.appendChild(makeCaption(img, false));
      }
      markDone(img);
      return;
    }

    var hero = img.closest('.art-hero');
    if (hero) {
      if (!hasCaptionNear(hero)) {
        hero.parentNode.insertBefore(makeCaption(img, false), hero.nextSibling);
      }
      markDone(img);
      return;
    }

    var host = img.closest('.gallery-carousel-host, .gallery-main, .gallery-wrap');
    if (host) {
      if (!hasCaptionNear(host)) {
        host.parentNode.insertBefore(makeCaption(img, false), host.nextSibling);
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
    parent.insertBefore(makeCaption(img, false), img.nextSibling);
    markDone(img);
  }

  function refreshExistingCaptions() {
    document.querySelectorAll('.rig-photo-caption, figure.blog-fig figcaption').forEach(function (cap) {
      var figure = cap.closest('figure, .blog-fig');
      var img = figure && figure.querySelector('img');
      if (!img) return;
      cap.className = 'rig-photo-caption';
      cap.innerHTML = captionHtmlFor(img, false);
    });
  }

  function injectPhotoCaptions() {
    if (isAdminPage()) return;
    var images = document.querySelectorAll('img:not([data-rig-photo-caption])');
    for (var i = 0; i < images.length; i++) {
      applyAiWatermark(images[i]);
      insertCaptionForImg(images[i]);
    }
    document.querySelectorAll('.rig-carousel:not([data-rig-carousel-caption])').forEach(captionCarousel);
    applyAllAiWatermarks();
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
    loadAiManifest().finally(function () {
      injectPhotoCaptions();
      refreshExistingCaptions();
      applyAllAiWatermarks();
    });
    observeDynamicPhotos();
    global.addEventListener('load', function () {
      injectPhotoCaptions();
      refreshExistingCaptions();
      applyAllAiWatermarks();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.RigAiDisclosure = {
    TEXT: TEXT,
    PRIVACY_ANCHOR: PRIVACY_ANCHOR,
    WATERMARK_LABEL: WATERMARK_LABEL,
    injectFooterBar: injectFooterBar,
    injectPhotoCaptions: injectPhotoCaptions,
    isAiGeneratedImage: isAiGeneratedImage,
    applyAiWatermark: applyAiWatermark,
    applyAllAiWatermarks: applyAllAiWatermarks
  };
})(typeof window !== 'undefined' ? window : global);
