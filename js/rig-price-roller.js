/* ═══════════════════════════════════════════════════════════════
   RIGHETTO IMMOBILIARE — Rullino prezzo (stile iPhone)
   Sostituisce visivamente il select "Prezzo max" con un selettore
   a rullo: ogni scatto aumenta del passo giusto per il contesto:
     - Vendita:                 € 10.000 a scatto
     - Affitto residenziale:    € 50 a scatto
     - Affitto commerciale:     € 100 a scatto (ufficio, negozio,
                                locale commerciale, capannone)
   - Nessun tetto: avvicinandosi al fondo il rullo aggiunge altri
     scatti dello stesso passo, senza limiti commerciali.
   - Valori fuori scala (es. da link condivisi) non vengono
     arrotondati: entrano nel rullo come scatto extra esatto.
   - Tab Aste: comportamento invariato, resta il select originale
     con le opzioni di sempre (richiesta non riguardava le aste).
   Il select originale resta nel DOM come portatore del valore:
   filtri, reset, alert ricerca e parametri URL seguono la prassi
   esistente.
   ═══════════════════════════════════════════════════════════════ */
window.RigPriceRoller = (function () {
  'use strict';

  var TIPI_COMMERCIALI = ['ufficio', 'negozio', 'locale', 'capannone'];
  var ITEM_H = 36;          // altezza riga del rullo (px)
  var VISIBLE = 5;          // righe visibili (dispari: selezione al centro)
  var CHUNK = 25;           // scatti aggiunti ogni volta che si arriva in fondo

  function scaleFor(op, tipo) {
    if (op === 'affitto') {
      if (TIPI_COMMERCIALI.indexOf(tipo) >= 0) return { step: 100, min: 100, max: 5000 };
      return { step: 50, min: 100, max: 3000 };
    }
    return { step: 10000, min: 10000, max: 1000000 };
  }

  function fmt(n) {
    return '€ ' + String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }

  function injectCss() {
    if (document.getElementById('rroll-css')) return;
    var st = document.createElement('style');
    st.id = 'rroll-css';
    st.textContent = [
      '.rroll-src{position:absolute!important;width:1px!important;height:1px!important;opacity:0!important;pointer-events:none!important}',
      '.rroll{position:relative;height:' + (ITEM_H * VISIBLE) + 'px;border:1px solid var(--gc,#d8cfc0);border-radius:8px;background:#fff;overflow:hidden;font-family:Montserrat,sans-serif;-webkit-user-select:none;user-select:none;outline:none}',
      '.rroll:focus-visible{border-color:var(--blu,#17324d);box-shadow:0 0 0 2px rgba(23,50,77,.18)}',
      '.rroll-list{height:100%;overflow-y:auto;scroll-snap-type:y mandatory;scrollbar-width:none;-ms-overflow-style:none}',
      '.rroll-list::-webkit-scrollbar{display:none}',
      '.rroll-pad{height:' + (ITEM_H * ((VISIBLE - 1) / 2)) + 'px}',
      '.rroll-item{height:' + ITEM_H + 'px;line-height:' + ITEM_H + 'px;text-align:center;scroll-snap-align:center;font-size:.82rem;color:var(--grigio,#6b6257);cursor:pointer;transition:font-size .12s,color .12s,font-weight .12s}',
      '.rroll-item.sel{font-size:.95rem;font-weight:700;color:var(--blu,#17324d)}',
      '.rroll-item.rroll-extra{font-style:italic}',
      '.rroll-band{position:absolute;left:6px;right:6px;top:' + (ITEM_H * ((VISIBLE - 1) / 2)) + 'px;height:' + ITEM_H + 'px;border-top:1px solid var(--gc,#d8cfc0);border-bottom:1px solid var(--gc,#d8cfc0);background:rgba(23,50,77,.045);border-radius:6px;pointer-events:none}',
      '.rroll-fade{position:absolute;left:0;right:0;height:' + ITEM_H + 'px;pointer-events:none;z-index:2}',
      '.rroll-fade.top{top:0;background:linear-gradient(#fff 20%,rgba(255,255,255,0))}',
      '.rroll-fade.bot{bottom:0;background:linear-gradient(rgba(255,255,255,0),#fff 80%)}',
      '.rroll-step-hint{margin-top:.3rem;font-size:.66rem;letter-spacing:.05em;text-transform:uppercase;color:var(--grigio,#6b6257)}',
      '@media(max-width:600px){.rroll-item{font-size:.9rem}.rroll-item.sel{font-size:1.02rem}}'
    ].join('\n');
    document.head.appendChild(st);
  }

  function Roller(select, ctx) {
    this.select = select;
    this.ctx = ctx; // {op:function, tipo:function, tipoEl:Element}
    this.scaleKey = '';
    this.values = [];
    this.extras = [];       // valori esatti fuori scala (URL/condivisi)
    this.origOptions = Array.prototype.map.call(select.options, function (o) {
      return { v: o.value, label: o.textContent };
    });
    this.buildDom();
    this.rebuild();
    this.bind();
    this.wrapValue();
  }

  Roller.prototype.buildDom = function () {
    injectCss();
    var root = document.createElement('div');
    root.className = 'rroll';
    root.tabIndex = 0;
    root.setAttribute('role', 'listbox');
    root.setAttribute('aria-label', 'Prezzo massimo');

    this.list = document.createElement('div');
    this.list.className = 'rroll-list';

    var band = document.createElement('div'); band.className = 'rroll-band';
    var fadeT = document.createElement('div'); fadeT.className = 'rroll-fade top';
    var fadeB = document.createElement('div'); fadeB.className = 'rroll-fade bot';

    root.appendChild(this.list);
    root.appendChild(band);
    root.appendChild(fadeT);
    root.appendChild(fadeB);

    this.hint = document.createElement('div');
    this.hint.className = 'rroll-step-hint';

    this.select.parentNode.insertBefore(root, this.select.nextSibling);
    this.select.parentNode.insertBefore(this.hint, root.nextSibling);
    this.root = root;
  };

  Roller.prototype.setMode = function (orig) {
    // orig=true: tab aste — select originale visibile, rullo nascosto
    this.select.classList.toggle('rroll-src', !orig);
    this.select.setAttribute('aria-hidden', orig ? 'false' : 'true');
    this.select.tabIndex = orig ? 0 : -1;
    this.root.style.display = orig ? 'none' : '';
    this.hint.style.display = orig ? 'none' : '';
  };

  Roller.prototype.currentScale = function () {
    return scaleFor(this.ctx.op(), this.ctx.tipo());
  };

  // Ricostruisce valori e opzioni per il contesto corrente
  Roller.prototype.rebuild = function () {
    var op = this.ctx.op();
    if (op === 'aste' || op === 'asta') {
      if (this.scaleKey !== 'orig') {
        this.scaleKey = 'orig';
        this.restoreOriginal();
        this.setMode(true);
      }
      return;
    }
    var s = this.currentScale();
    var key = s.step + '-' + s.min;
    var keep = this.select.value;
    if (key === this.scaleKey) { this.syncFromSelect(); return; }
    this.scaleKey = key;
    this.max = s.max;
    this.step = s.step;
    this.min = s.min;
    this.extras = [];
    this.rebuildValues();
    this.setMode(false);

    this.hint.textContent = 'Rullino: scatti da ' + fmt(s.step).replace('€ ', '€ ');

    // Ripristina selezione se ancora valida nella nuova scala,
    // altrimenti la inserisce come scatto extra esatto (niente arrotondamenti)
    this.setSelectRaw('');
    if (keep) {
      this.ensureValue(keep, false);
      for (var i = 0; i < this.select.options.length; i++) {
        if (this.select.options[i].value === keep) { this.setSelectRaw(keep); break; }
      }
    }
    this.syncFromSelect(true);
  };

  Roller.prototype.restoreOriginal = function () {
    var keep = this.select.value;
    this.select.innerHTML = '';
    var self = this;
    this.origOptions.forEach(function (o) {
      var el = document.createElement('option');
      el.value = o.v;
      el.textContent = o.label;
      self.select.appendChild(el);
    });
    var ok = this.origOptions.some(function (o) { return o.v === keep; });
    this.setSelectRaw(ok ? keep : '');
  };

  // Rigenera this.values da scala + extra, ridisegna select e lista
  Roller.prototype.rebuildValues = function () {
    var self = this;
    var vals = [{ v: '', label: this.anyLabel(), extra: false }];
    for (var n = this.min; n <= this.max; n += this.step) {
      vals.push({ v: String(n), label: fmt(n), extra: false });
    }
    this.extras.forEach(function (v) {
      vals.push({ v: v, label: fmt(parseInt(v, 10)), extra: true });
    });
    vals.sort(function (a, b) {
      if (a.v === '') return -1;
      if (b.v === '') return 1;
      return parseInt(a.v, 10) - parseInt(b.v, 10);
    });
    this.values = vals;

    this.select.innerHTML = '';
    vals.forEach(function (it, i) {
      var o = document.createElement('option');
      o.value = it.v;
      o.textContent = it.v === '' ? it.label : 'fino a ' + it.label;
      self.select.appendChild(o);
    });

    this.list.innerHTML = '';
    var pad1 = document.createElement('div'); pad1.className = 'rroll-pad';
    this.list.appendChild(pad1);
    vals.forEach(function (it, i) {
      var d = document.createElement('div');
      d.className = 'rroll-item' + (it.extra ? ' rroll-extra' : '');
      d.id = 'rroll-' + self.select.id + '-' + i;
      d.setAttribute('role', 'option');
      d.dataset.v = it.v;
      d.textContent = it.label;
      self.list.appendChild(d);
    });
    var pad2 = document.createElement('div'); pad2.className = 'rroll-pad';
    this.list.appendChild(pad2);
  };

  Roller.prototype.anyLabel = function () {
    return this.origOptions.length && this.origOptions[0].v === ''
      ? this.origOptions[0].label
      : 'Qualsiasi';
  };

  // Garantisce che un valore esista nel rullo: se fuori scala lo aggiunge
  // come scatto extra esatto; se oltre il fondo, allunga la scala fino a coprirlo.
  Roller.prototype.ensureValue = function (v, allowExtend) {
    if (!v) return;
    var num = parseInt(v, 10);
    if (!isFinite(num) || num <= 0) return;
    var onScale = num >= this.min && num <= this.max && ((num - this.min) % this.step === 0);
    if (onScale) return;
    if (num > this.max) {
      // cambio contesto (tab): non ereditare valori oltre la nuova scala
      if (!allowExtend) return;
      // valore impostato da codice/URL: allunga la scala fino a coprirlo
      while (this.max < num) this.max += this.step * CHUNK;
      if ((num - this.min) % this.step === 0) { this.rebuildValues(); return; }
    }
    if (this.extras.indexOf(String(num)) < 0) this.extras.push(String(num));
    this.rebuildValues();
  };

  // Allungamento infinito: vicino al fondo aggiunge un blocco di scatti
  Roller.prototype.maybeGrow = function () {
    if (this.scaleKey === 'orig') return;
    var nearEnd = this.list.scrollTop + this.list.clientHeight >= this.list.scrollHeight - ITEM_H * 6;
    if (nearEnd) {
      this.max += this.step * CHUNK;
      var cur = this.select.value;
      this.rebuildValues();
      this.setSelectRaw(cur);
      this.syncFromSelect(true);
    }
  };

  Roller.prototype.indexOfValue = function (v) {
    for (var i = 0; i < this.values.length; i++) if (this.values[i].v === v) return i;
    return 0;
  };

  Roller.prototype.setSelectRaw = function (v) {
    // bypassa il setter decorato per non rientrare in sync
    Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value').set.call(this.select, v);
  };

  Roller.prototype.syncFromSelect = function (instant) {
    if (this.scaleKey === 'orig') return;
    var v = this.select.value;
    if (v && this.indexOfValue(v) === 0 && v !== this.values[0].v) this.ensureValue(v);
    var idx = this.indexOfValue(this.select.value);
    this.applyIndex(idx, { silent: true, instant: !!instant });
  };

  Roller.prototype.applyIndex = function (idx, opts) {
    opts = opts || {};
    idx = Math.max(0, Math.min(this.values.length - 1, idx));
    var items = this.list.querySelectorAll('.rroll-item');
    for (var i = 0; i < items.length; i++) {
      items[i].classList.toggle('sel', i === idx);
      items[i].setAttribute('aria-selected', i === idx ? 'true' : 'false');
    }
    this.root.setAttribute('aria-activedescendant', items[idx] ? items[idx].id : '');
    var top = idx * ITEM_H;
    if (opts.instant) this.list.scrollTop = top;
    else this.list.scrollTo({ top: top, behavior: 'smooth' });
    if (!opts.silent) {
      var v = this.values[idx].v;
      if (this.select.value !== v) {
        this.setSelectRaw(v);
        this.select.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }
  };

  Roller.prototype.bind = function () {
    var self = this;
    var scrollTimer = null;

    this.list.addEventListener('scroll', function () {
      self.maybeGrow();
      if (scrollTimer) clearTimeout(scrollTimer);
      scrollTimer = setTimeout(function () {
        var idx = Math.round(self.list.scrollTop / ITEM_H);
        self.applyIndex(idx, { silent: false });
        self.list.scrollTo({ top: idx * ITEM_H, behavior: 'smooth' });
      }, 90);
    }, { passive: true });

    this.list.addEventListener('click', function (e) {
      var item = e.target.closest('.rroll-item');
      if (!item) return;
      var idx = Array.prototype.indexOf.call(self.list.querySelectorAll('.rroll-item'), item);
      self.applyIndex(idx, {});
    });

    this.root.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return;
      e.preventDefault();
      var cur = self.indexOfValue(self.select.value);
      self.applyIndex(cur + (e.key === 'ArrowDown' ? 1 : -1), {});
    });

    // Cambi di contesto: tab operazione e tipologia
    document.addEventListener('click', function (e) {
      if (e.target.closest && e.target.closest('.s-tab, .r-tab')) {
        setTimeout(function () { self.rebuild(); }, 0);
      }
    }, true);
    if (this.ctx.tipoEl) {
      this.ctx.tipoEl.addEventListener('change', function () { self.rebuild(); });
    }
    // Cambi diretti sul select (es. ripristino da URL o codice esterno)
    this.select.addEventListener('change', function () { self.syncFromSelect(); });
  };

  // Intercetta anche le assegnazioni programmatiche select.value = ...
  Roller.prototype.wrapValue = function () {
    var self = this;
    var proto = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value');
    Object.defineProperty(this.select, 'value', {
      configurable: true,
      enumerable: true,
      get: function () { return proto.get.call(this); },
      set: function (v) {
        // Valori fuori scala (es. da link condivisi): inserisci lo scatto
        // esatto PRIMA di assegnare, altrimenti il browser azzera il select
        if (v && self.scaleKey && self.scaleKey !== 'orig') {
          var exists = false;
          for (var i = 0; i < self.select.options.length; i++) {
            if (self.select.options[i].value === v) { exists = true; break; }
          }
          if (!exists) self.ensureValue(v, true);
        }
        proto.set.call(this, v);
        // sync rullo quando il valore cambia da codice (reset, URL, ecc.)
        setTimeout(function () { self.syncFromSelect(true); }, 0);
      }
    });
  };

  var rollers = [];

  function opFromTabs(tabSel) {
    var active = document.querySelector(tabSel);
    if (!active) return 'vendita';
    var oc = active.getAttribute('onclick') || '';
    var m = oc.match(/(?:setTab|setRTab)\(this\s*,\s*'([^']+)'\)/);
    return m ? m[1] : 'vendita';
  }

  function attach() {
    // Pagina immobili: #f-prezzo con tab .s-tab e #f-tipo
    var fPrezzo = document.getElementById('f-prezzo');
    if (fPrezzo && !fPrezzo.dataset.rrollAttached) {
      fPrezzo.dataset.rrollAttached = '1';
      rollers.push(new Roller(fPrezzo, {
        op: function () { return opFromTabs('.s-tab.active'); },
        tipo: function () { var t = document.getElementById('f-tipo'); return t ? t.value : ''; },
        tipoEl: document.getElementById('f-tipo')
      }));
    }
    // Home: #r-prezzo con tab .r-tab e #r-tipo
    var rPrezzo = document.getElementById('r-prezzo');
    if (rPrezzo && !rPrezzo.dataset.rrollAttached) {
      rPrezzo.dataset.rrollAttached = '1';
      rollers.push(new Roller(rPrezzo, {
        op: function () { return opFromTabs('.r-tab.active'); },
        tipo: function () { var t = document.getElementById('r-tipo'); return t ? t.value : ''; },
        tipoEl: document.getElementById('r-tipo')
      }));
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attach);
  } else {
    attach();
  }

  return {
    refresh: function () { rollers.forEach(function (r) { r.rebuild(); }); },
    sync: function () { rollers.forEach(function (r) { r.syncFromSelect(true); }); }
  };
})();
