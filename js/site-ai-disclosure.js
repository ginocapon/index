/**
 * Righetto Immobiliare — Trasparenza Reg. (UE) 2024/1689 (AI Act) e contenuti digitali.
 * Barra informativa sito + helper testi condivisi.
 */
(function (global) {
  'use strict';

  var PRIVACY_ANCHOR = 'privacy#trasparenza-digitale';

  var TEXT = {
    footer:
      '<strong>Trasparenza digitale (AI Act UE):</strong> l\'assistente <strong>Linda</strong> è un sistema ' +
      'automatizzato a regole — non sostituisce un agente. Alcune <strong>foto e grafiche</strong> del sito ' +
      'possono essere state ottimizzate o parzialmente modificate con strumenti digitali, inclusa ' +
      'intelligenza artificiale. Stime e testi hanno valore informativo. ' +
      '<a href="' + PRIVACY_ANCHOR + '">Dettagli</a>',
    photo:
      'Le foto di questo annuncio sono riferite all\'immobile reale. Eventuali ottimizzazioni digitali ' +
      '(nitidezza, luminosità o ritocco) non alterano le caratteristiche dichiarate. ' +
      '<a href="/' + PRIVACY_ANCHOR + '">Trasparenza contenuti</a>.',
    catalog:
      'Foto annunci: immagini reali, eventualmente ottimizzate digitalmente. Copertine blog e grafiche editoriali ' +
      'possono includere elaborazioni con strumenti digitali (anche IA), come indicato in ' +
      '<a href="/' + PRIVACY_ANCHOR + '">informativa trasparenza</a>.',
    chatHeader: 'Assistente digitale automatizzato',
    chatWelcome:
      'Sono un <strong>assistente digitale automatizzato</strong> (sistema a regole, senza IA generativa). ' +
      'Le risposte e le stime hanno valore <strong>orientativo</strong> e non sostituiscono una perizia, ' +
      'consulenza legale o fiscale. <a href="/' + PRIVACY_ANCHOR + '">Informativa</a>',
    chatFirst:
      'Ricorda: sono un assistente automatizzato. Per decisioni vincolanti contatta un agente al ' +
      '049.8843484 o in sede. <a href="/' + PRIVACY_ANCHOR + '">Trasparenza AI Act</a>.'
  };

  function isAdminPage() {
    var p = (global.location && global.location.pathname) || '';
    return /admin\.html$/i.test(p) || p.indexOf('/admin') !== -1;
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

  function injectCatalogNote() {
    if (isAdminPage()) return;
    var path = (global.location && global.location.pathname) || '';
    var isCatalog = /immobili(\.html)?$/i.test(path) || /\/immobili\/?$/i.test(path);
    if (!isCatalog) return;
    if (document.getElementById('rig-catalog-ai-note')) return;
    var grid = document.getElementById('grid') || document.querySelector('.props-grid, #propsGrid');
    var note = document.createElement('p');
    note.id = 'rig-catalog-ai-note';
    note.className = 'rig-media-ai-note';
    note.setAttribute('role', 'note');
    note.innerHTML = TEXT.catalog;
    if (grid && grid.parentNode) {
      grid.parentNode.insertBefore(note, grid);
    }
  }

  function injectImmobileNote() {
    if (isAdminPage()) return;
    var path = (global.location && global.location.pathname) || '';
    var isDetail = /immobile(\.html)?$/i.test(path) || /\/immobile\/?$/i.test(path);
    if (!isDetail) return;
    if (document.getElementById('rig-immobile-ai-note')) return;
    var gallery = document.getElementById('galleryWrap') || document.querySelector('.gallery-wrap');
    if (!gallery || !gallery.parentNode) return;
    var note = document.createElement('p');
    note.id = 'rig-immobile-ai-note';
    note.className = 'rig-media-ai-note';
    note.setAttribute('role', 'note');
    note.innerHTML = TEXT.photo;
    gallery.parentNode.insertBefore(note, gallery.nextSibling);
  }

  function init() {
    injectFooterBar();
    injectCatalogNote();
    injectImmobileNote();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.RigAiDisclosure = {
    TEXT: TEXT,
    PRIVACY_ANCHOR: PRIVACY_ANCHOR,
    injectFooterBar: injectFooterBar
  };
})(typeof window !== 'undefined' ? window : global);
