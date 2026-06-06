(function () {
  'use strict';

  var params = new URLSearchParams(window.location.search);
  var slug = params.get('slug') || '';
  var embed = params.get('embed') === '1';

  var state = {
    tour: null,
    index: 0,
    scale: 1,
    panX: 0,
    panY: 0,
    dragging: false,
    startX: 0,
    startY: 0,
    originPanX: 0,
    originPanY: 0
  };

  var els = {};

  function $(id) { return document.getElementById(id); }

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function applyTransform() {
    if (!els.panLayer) return;
    els.panLayer.style.transform =
      'translate(calc(-50% + ' + state.panX + 'px), calc(-50% + ' + state.panY + 'px)) scale(' + state.scale + ')';
  }

  function resetPan() {
    state.scale = 1;
    state.panX = 0;
    state.panY = 0;
    applyTransform();
  }

  function setScene(i) {
    if (!state.tour || !state.tour.scenes.length) return;
    state.index = (i + state.tour.scenes.length) % state.tour.scenes.length;
    var scene = state.tour.scenes[state.index];
    resetPan();

    if (els.sceneName) els.sceneName.textContent = scene.nome;
    if (els.sceneCounter) {
      els.sceneCounter.textContent = (state.index + 1) + ' / ' + state.tour.scenes.length;
    }

    els.sceneImg.classList.remove('is-ready');
    els.sceneImg.onload = function () {
      els.sceneImg.classList.add('is-ready');
      fitScene();
    };
    els.sceneImg.src = scene.img;
    els.sceneImg.alt = 'Visita virtuale — ' + scene.nome + ', ' + state.tour.titolo;

    var thumbs = document.querySelectorAll('.vv-thumb');
    thumbs.forEach(function (btn, idx) {
      btn.classList.toggle('is-active', idx === state.index);
      if (idx === state.index) btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    });
  }

  function fitScene() {
    var vw = els.viewport.clientWidth;
    var vh = els.viewport.clientHeight;
    var iw = els.sceneImg.naturalWidth || vw;
    var ih = els.sceneImg.naturalHeight || vh;
    if (!iw || !ih) return;

    var coverScale = Math.max(vw / iw, vh / ih);
    var panScale = coverScale * 1.18;
    els.sceneImg.style.width = iw + 'px';
    els.sceneImg.style.height = ih + 'px';
    state.baseScale = coverScale;
    state.panScale = panScale;
    state.scale = coverScale;
    applyTransform();
  }

  function nextScene() { setScene(state.index + 1); }
  function prevScene() { setScene(state.index - 1); }

  function onPointerDown(e) {
    if (!els.viewport) return;
    state.dragging = true;
    els.viewport.classList.add('is-dragging');
    state.startX = e.clientX;
    state.startY = e.clientY;
    state.originPanX = state.panX;
    state.originPanY = state.panY;
    if (els.hint) els.hint.classList.add('is-hidden');
  }

  function onPointerMove(e) {
    if (!state.dragging) return;
    var dx = e.clientX - state.startX;
    var dy = e.clientY - state.startY;
    var maxX = Math.max(0, ((els.sceneImg.naturalWidth || 0) * state.scale - els.viewport.clientWidth) * 0.5);
    var maxY = Math.max(0, ((els.sceneImg.naturalHeight || 0) * state.scale - els.viewport.clientHeight) * 0.5);
    state.panX = clamp(state.originPanX + dx, -maxX, maxX);
    state.panY = clamp(state.originPanY + dy, -maxY, maxY);
    applyTransform();
  }

  function onPointerUp() {
    state.dragging = false;
    if (els.viewport) els.viewport.classList.remove('is-dragging');
  }

  function onWheel(e) {
    e.preventDefault();
    var delta = e.deltaY > 0 ? -0.08 : 0.08;
    var next = clamp(state.scale + delta, state.baseScale || 1, (state.panScale || 1.4));
    state.scale = next;
    applyTransform();
  }

  function bindViewport() {
    els.viewport.addEventListener('pointerdown', onPointerDown);
    window.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerup', onPointerUp);
    window.addEventListener('pointercancel', onPointerUp);
    els.viewport.addEventListener('wheel', onWheel, { passive: false });
  }

  function renderThumbs() {
    if (!els.thumbs || !state.tour) return;
    els.thumbs.innerHTML = state.tour.scenes.map(function (scene, i) {
      return '<button type="button" class="vv-thumb' + (i === 0 ? ' is-active' : '') + '" data-idx="' + i + '" aria-label="' + scene.nome + '">' +
        '<img src="' + scene.img + '" alt="" loading="lazy" width="92" height="69">' +
        '<span>' + scene.nome + '</span></button>';
    }).join('');

    els.thumbs.querySelectorAll('.vv-thumb').forEach(function (btn) {
      btn.addEventListener('click', function () {
        setScene(parseInt(btn.getAttribute('data-idx'), 10));
      });
    });
  }

  function showError(msg) {
    if (els.loading) els.loading.style.display = 'none';
    if (els.error) {
      els.error.style.display = 'flex';
      var p = els.error.querySelector('p');
      if (p) p.textContent = msg;
    }
  }

  function initUI(tour) {
    state.tour = tour;
    if (embed && els.app) els.app.classList.add('is-embed');

    if (els.title) els.title.textContent = tour.titolo;
    if (els.location) els.location.textContent = tour.comune + (tour.codice ? ' · ' + tour.codice : '');
    if (els.immobileLink) els.immobileLink.href = 'immobile?s=' + encodeURIComponent(slug);

    renderThumbs();
    bindViewport();
    setScene(0);

    if (els.loading) els.loading.style.display = 'none';
    window.addEventListener('resize', fitScene);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') nextScene();
      if (e.key === 'ArrowLeft') prevScene();
      if (e.key === 'Escape' && document.fullscreenElement) document.exitFullscreen();
    });

    if (els.btnPrev) els.btnPrev.addEventListener('click', prevScene);
    if (els.btnNext) els.btnNext.addEventListener('click', nextScene);
    if (els.btnFs) {
      els.btnFs.addEventListener('click', function () {
        var root = document.documentElement;
        if (!document.fullscreenElement && root.requestFullscreen) root.requestFullscreen();
        else if (document.exitFullscreen) document.exitFullscreen();
      });
    }

    setTimeout(function () {
      if (els.hint) els.hint.classList.add('is-hidden');
    }, 4200);
  }

  function boot() {
    els.app = $('vvApp');
    els.loading = $('vvLoading');
    els.error = $('vvError');
    els.title = $('vvTitle');
    els.location = $('vvLocation');
    els.sceneName = $('vvSceneName');
    els.sceneCounter = $('vvSceneCounter');
    els.sceneImg = $('vvSceneImg');
    els.panLayer = $('vvPanLayer');
    els.viewport = $('vvViewport');
    els.thumbs = $('vvThumbs');
    els.hint = $('vvHint');
    els.btnPrev = $('vvPrev');
    els.btnNext = $('vvNext');
    els.btnFs = $('vvFullscreen');
    els.immobileLink = $('vvImmobileLink');

    if (!slug) {
      showError('Nessun immobile selezionato. Apri la visita dalla scheda o dalla homepage.');
      return;
    }

    fetch('data/visite-virtuali.json')
      .then(function (r) {
        if (!r.ok) throw new Error('Catalogo visite non disponibile');
        return r.json();
      })
      .then(function (data) {
        var tour = data[slug];
        if (!tour || !tour.scenes || !tour.scenes.length) {
          showError('Visita virtuale non ancora disponibile per questo immobile.');
          return;
        }
        initUI(tour);
      })
      .catch(function () {
        showError('Impossibile caricare la visita virtuale. Riprova tra qualche istante.');
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
