/**
 * Righetto — carousel foto immobile: swipe touch + drag mouse, frecce, contatore.
 * Uso: RigPhotoCarousel.buildHtml(urls, alt) oppure RigPhotoCarousel.mount(el, opts)
 */
(function (global) {
  'use strict';

  var DRAG_THRESHOLD = 36;
  var weakMap = typeof WeakMap !== 'undefined' ? new WeakMap() : null;
  var stateByEl = weakMap || null;
  var fallbackStates = [];

  function esc(s) {
    return String(s || '')
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/</g, '&lt;');
  }

  function getState(el) {
    if (weakMap) return weakMap.get(el);
    for (var i = 0; i < fallbackStates.length; i++) {
      if (fallbackStates[i].el === el) return fallbackStates[i].state;
    }
    return null;
  }

  function setState(el, state) {
    if (weakMap) weakMap.set(el, state);
    else {
      var found = false;
      for (var i = 0; i < fallbackStates.length; i++) {
        if (fallbackStates[i].el === el) {
          fallbackStates[i].state = state;
          found = true;
          break;
        }
      }
      if (!found) fallbackStates.push({ el: el, state: state });
    }
  }

  function buildHtml(urls, alt) {
    var list = (urls || []).filter(Boolean);
    if (!list.length) return '';
    var slides = list.map(function (url, i) {
      return '<div class="rig-carousel-slide" role="group" aria-roledescription="slide" aria-label="' + (i + 1) + ' di ' + list.length + '">'
        + '<img src="' + esc(url) + '" alt="' + esc(alt) + ' — foto ' + (i + 1) + '" width="900" height="600" loading="' + (i === 0 ? 'eager' : 'lazy') + '" decoding="async">'
        + '</div>';
    }).join('');
    var nav = '';
    if (list.length > 1) {
      nav = '<button type="button" class="rig-carousel-nav rig-carousel-prev" aria-label="Foto precedente" tabindex="-1">&#8249;</button>'
        + '<button type="button" class="rig-carousel-nav rig-carousel-next" aria-label="Foto successiva" tabindex="-1">&#8250;</button>'
        + '<span class="rig-carousel-counter" aria-live="polite">1 / ' + list.length + '</span>';
    }
    return '<div class="rig-carousel" data-rig-carousel tabindex="0" aria-roledescription="carousel">'
      + '<div class="rig-carousel-viewport"><div class="rig-carousel-track">' + slides + '</div></div>'
      + nav + '</div>';
  }

  function updateUI(state) {
    var el = state.root;
    var track = el.querySelector('.rig-carousel-track');
    if (!track) return;
    track.style.transform = 'translate3d(' + (-state.index * 100) + '%,0,0)';
    var counter = el.querySelector('.rig-carousel-counter');
    if (counter) counter.textContent = (state.index + 1) + ' / ' + state.total;
    var dots = el.querySelectorAll('.rig-carousel-dot');
    dots.forEach(function (d, i) {
      d.classList.toggle('is-active', i === state.index);
    });
    if (typeof state.onChange === 'function') state.onChange(state.index);
  }

  function go(state, delta) {
    if (state.total < 2) return;
    state.index = (state.index + delta + state.total) % state.total;
    updateUI(state);
  }

  function mount(container, opts) {
    opts = opts || {};
    var urls = (opts.urls || []).filter(Boolean);
    if (!urls.length) return null;
    container.innerHTML = buildHtml(urls, opts.alt || 'Immobile');
    return init(container.querySelector('[data-rig-carousel]'), opts);
  }

  function init(el, opts) {
    if (!el) return null;
    opts = opts || {};
    var track = el.querySelector('.rig-carousel-track');
    if (!track) return null;
    var total = track.children.length;
    var state = {
      root: el,
      track: track,
      index: Math.max(0, Math.min(opts.startIndex || 0, total - 1)),
      total: total,
      onChange: opts.onChange || null,
      dragging: false,
      didDrag: false,
      startX: 0,
      startY: 0,
      deltaX: 0,
      pointerId: null
    };
    setState(el, state);
    updateUI(state);

    if (total < 2) return state;

    var prev = el.querySelector('.rig-carousel-prev');
    var next = el.querySelector('.rig-carousel-next');
    if (prev) {
      prev.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        go(state, -1);
      });
    }
    if (next) {
      next.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        go(state, 1);
      });
    }

    function onPointerDown(e) {
      if (e.button > 0) return;
      state.dragging = true;
      state.didDrag = false;
      state.startX = e.clientX;
      state.startY = e.clientY;
      state.deltaX = 0;
      state.pointerId = e.pointerId;
      el.classList.add('is-dragging');
      try { el.setPointerCapture(e.pointerId); } catch (err) { /* ignore */ }
    }

    function onPointerMove(e) {
      if (!state.dragging || state.pointerId !== e.pointerId) return;
      var dx = e.clientX - state.startX;
      var dy = e.clientY - state.startY;
      if (!state.didDrag && Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(dy)) {
        state.didDrag = true;
      }
      if (!state.didDrag) return;
      e.preventDefault();
      state.deltaX = dx;
      var pct = (-state.index * 100) + (dx / el.offsetWidth) * 100;
      track.style.transform = 'translate3d(' + pct + '%,0,0)';
    }

    function onPointerUp(e) {
      if (!state.dragging || state.pointerId !== e.pointerId) return;
      state.dragging = false;
      el.classList.remove('is-dragging');
      try { el.releasePointerCapture(e.pointerId); } catch (err) { /* ignore */ }
      if (state.didDrag) {
        if (state.deltaX < -DRAG_THRESHOLD) go(state, 1);
        else if (state.deltaX > DRAG_THRESHOLD) go(state, -1);
        else updateUI(state);
        setTimeout(function () { state.didDrag = false; }, 0);
      }
      state.pointerId = null;
      state.deltaX = 0;
    }

    el.addEventListener('pointerdown', onPointerDown);
    el.addEventListener('pointermove', onPointerMove);
    el.addEventListener('pointerup', onPointerUp);
    el.addEventListener('pointercancel', onPointerUp);

    el.addEventListener('click', function (e) {
      if (state.didDrag) {
        e.preventDefault();
        e.stopPropagation();
      }
    }, true);

    el.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(state, -1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); go(state, 1); }
    });

    return state;
  }

  function initAll(root) {
    var scope = root || document;
    var nodes = scope.querySelectorAll('[data-rig-carousel]:not([data-rig-mounted])');
    nodes.forEach(function (el) {
      el.setAttribute('data-rig-mounted', '1');
      init(el, {});
    });
  }

  function wasDragging(host) {
    if (!host) return false;
    var el = host.querySelector('[data-rig-carousel]');
    if (!el) return false;
    var st = getState(el);
    return st && st.didDrag;
  }

  function getIndex(host) {
    var el = host && host.querySelector ? host.querySelector('[data-rig-carousel]') : null;
    if (!el) return 0;
    var st = getState(el);
    return st ? st.index : 0;
  }

  global.RigPhotoCarousel = {
    buildHtml: buildHtml,
    mount: mount,
    init: init,
    initAll: initAll,
    wasDragging: wasDragging,
    getIndex: getIndex
  };
})(typeof window !== 'undefined' ? window : this);
