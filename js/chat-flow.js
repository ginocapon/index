/**
 * RIGHETTO IMMOBILIARE — Motore Landing Page Conversazionali
 * Stile chatbot step-by-step con bolle, immagini e bottoni
 * Salvataggio progressivo su Supabase
 */
(function() {
'use strict';

const SUPABASE_URL = 'https://qwkwkemuabfwvwdqrxlu.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc';

// ══════════════════════════════════════════════
// DATABASE PREZZI (stesso del chatbot principale)
// ══════════════════════════════════════════════
const PREZZI_ZONE = {
  'Padova Centro Storico': 3500, 'Padova Prato della Valle': 3200,
  'Padova Savonarola': 2800, 'Padova Arcella': 1800,
  'Padova Guizza': 2000, 'Padova Nord': 1700,
  'Padova Est': 1900, 'Padova': 2500,
  'Abano Terme': 2100, 'Albignasego': 1900,
  'Selvazzano Dentro': 1850, 'Vigonza': 1700,
  'Rubano': 1900, 'Limena': 1700,
  'Cadoneghe': 1750, 'Noventa Padovana': 1850,
  'Ponte San Nicolo': 1650, 'Cittadella': 3200,
  'Camposampiero': 1600, 'Piove di Sacco': 1800,
  'Monselice': 1050, 'Este': 1100,
  'Montegrotto Terme': 1900, 'Saccolongo': 1750,
  'Mestrino': 1700, 'Curtarolo': 1600,
  'Trebaseleghe': 1600, 'Borgoricco': 1550,
  'Conselve': 1150, 'Teolo': 1400,
  'default': 1700
};

const MULT_STATO = {
  'Nuovo / Ristrutturato': 1.22, 'Buone condizioni': 1.00,
  'Da ristrutturare': 0.75, 'Non lo so': 0.95
};

const MULT_TIPO = {
  'Appartamento': 1.00, 'Villa / Villetta': 1.20,
  'Casa indipendente': 1.10, 'Bifamiliare': 1.08,
  'Attico / Mansarda': 1.30, 'Rustico': 0.85
};

function stimaPrezzo(zona, tipo, mqLabel, stato) {
  var prezzo = PREZZI_ZONE[zona] || PREZZI_ZONE['default'];
  var mq = { 'Fino a 60 mq': 55, '60-90 mq': 75, '90-120 mq': 105, 'Oltre 120 mq': 145 }[mqLabel] || 90;
  var multS = MULT_STATO[stato] || 1.00;
  var multT = MULT_TIPO[tipo] || 1.00;
  var base = prezzo * mq * multS * multT;
  return {
    min: Math.round(base * 0.88 / 1000) * 1000,
    med: Math.round(base / 1000) * 1000,
    max: Math.round(base * 1.12 / 1000) * 1000,
    mqPrezzo: Math.round(prezzo * multS * multT)
  };
}

// ══════════════════════════════════════════════
// CHAT FLOW ENGINE
// ══════════════════════════════════════════════
window.ChatFlow = function(containerId, steps, config) {
  this.container = document.getElementById(containerId);
  this.steps = steps;
  this.config = config || {};
  this.currentStep = 0;
  this.data = {};
  this.avatarSrc = config.avatarSrc || 'img/team/real-state-linda-righetto.webp';
  this.avatarName = config.avatarName || 'Linda';
  this.onComplete = config.onComplete || function() {};
  this.onStepComplete = config.onStepComplete || function() {};
  this.flowId = config.flowId || 'generico';
  this.sessionId = 'cf_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);

  this.container.innerHTML = '';
  this.container.className = 'cf-container';

  // Progress bar
  this.progressWrap = document.createElement('div');
  this.progressWrap.className = 'cf-progress-wrap';
  this.progressBar = document.createElement('div');
  this.progressBar.className = 'cf-progress-bar';
  this.progressLabel = document.createElement('span');
  this.progressLabel.className = 'cf-progress-label';
  this.progressWrap.appendChild(this.progressBar);
  this.progressWrap.appendChild(this.progressLabel);
  this.container.appendChild(this.progressWrap);

  // Chat area
  this.chatArea = document.createElement('div');
  this.chatArea.className = 'cf-chat';
  this.container.appendChild(this.chatArea);

  this.updateProgress();
  this.playStep();
};

ChatFlow.prototype.updateProgress = function() {
  var total = this.steps.length;
  var pct = Math.round(((this.currentStep) / total) * 100);
  this.progressBar.style.width = pct + '%';
  this.progressLabel.textContent = 'Step ' + (this.currentStep + 1) + ' di ' + total;
};

ChatFlow.prototype.addBubble = function(html, type, delay) {
  var self = this;
  return new Promise(function(resolve) {
    setTimeout(function() {
      var row = document.createElement('div');
      row.className = 'cf-row cf-row-' + type;

      if (type === 'bot') {
        var av = document.createElement('img');
        av.src = self.avatarSrc;
        av.alt = self.avatarName;
        av.className = 'cf-avatar';
        av.width = 40;
        av.height = 40;
        row.appendChild(av);
      }

      var bubble = document.createElement('div');
      bubble.className = 'cf-bubble cf-bubble-' + type;
      bubble.innerHTML = html;
      row.appendChild(bubble);

      self.chatArea.appendChild(row);
      requestAnimationFrame(function() {
        row.classList.add('cf-visible');
        self.scrollToBottom();
      });
      resolve();
    }, delay || 0);
  });
};

ChatFlow.prototype.addImage = function(src, alt, delay) {
  var self = this;
  return new Promise(function(resolve) {
    setTimeout(function() {
      var row = document.createElement('div');
      row.className = 'cf-row cf-row-image';
      var img = document.createElement('img');
      img.src = src;
      img.alt = alt || '';
      img.className = 'cf-image';
      img.width = 600;
      img.height = 340;
      img.loading = 'lazy';
      row.appendChild(img);
      self.chatArea.appendChild(row);
      requestAnimationFrame(function() {
        row.classList.add('cf-visible');
        self.scrollToBottom();
      });
      resolve();
    }, delay || 0);
  });
};

ChatFlow.prototype.addButtons = function(options, key) {
  var self = this;
  return new Promise(function(resolve) {
    var row = document.createElement('div');
    row.className = 'cf-row cf-row-buttons';
    var wrap = document.createElement('div');
    wrap.className = 'cf-buttons';

    options.forEach(function(opt) {
      var btn = document.createElement('button');
      btn.className = 'cf-btn';
      btn.textContent = opt;
      btn.addEventListener('click', function() {
        // Disabilita tutti i bottoni
        wrap.querySelectorAll('.cf-btn').forEach(function(b) {
          b.disabled = true;
          b.classList.add('cf-btn-disabled');
        });
        btn.classList.add('cf-btn-selected');
        self.data[key] = opt;

        // Mostra risposta utente
        self.addBubble(opt, 'user', 100).then(function() {
          self.onStepComplete(key, opt, self.data);
          resolve(opt);
        });
      });
    });

    row.appendChild(wrap);
    self.chatArea.appendChild(row);
    requestAnimationFrame(function() {
      row.classList.add('cf-visible');
      self.scrollToBottom();
    });
  });
};

ChatFlow.prototype.addInput = function(fields) {
  var self = this;
  return new Promise(function(resolve) {
    var row = document.createElement('div');
    row.className = 'cf-row cf-row-form';
    var form = document.createElement('div');
    form.className = 'cf-form';

    fields.forEach(function(f) {
      var group = document.createElement('div');
      group.className = 'cf-form-group';
      var label = document.createElement('label');
      label.textContent = f.label;
      label.className = 'cf-form-label';
      var input = document.createElement('input');
      input.type = f.type || 'text';
      input.placeholder = f.placeholder || '';
      input.name = f.key;
      input.required = f.required !== false;
      input.className = 'cf-form-input';
      if (f.type === 'tel') input.pattern = '[0-9+\\s]{6,}';
      group.appendChild(label);
      group.appendChild(input);
      form.appendChild(group);
    });

    // Privacy
    var chk = document.createElement('div');
    chk.className = 'cf-form-check';
    chk.innerHTML = '<label><input type="checkbox" id="cf-gdpr" required> Acconsento al trattamento dei dati. <a href="/privacy" target="_blank">Privacy</a></label>';
    form.appendChild(chk);

    var btn = document.createElement('button');
    btn.className = 'cf-submit';
    btn.textContent = 'Invia richiesta';
    btn.addEventListener('click', function() {
      var inputs = form.querySelectorAll('.cf-form-input');
      var gdpr = document.getElementById('cf-gdpr');
      var valid = true;
      var formData = {};

      inputs.forEach(function(inp) {
        if (inp.required && !inp.value.trim()) {
          inp.classList.add('cf-input-error');
          valid = false;
        } else {
          inp.classList.remove('cf-input-error');
          formData[inp.name] = inp.value.trim();
        }
      });

      if (!gdpr.checked) {
        gdpr.parentElement.style.color = '#e53e3e';
        valid = false;
      }

      if (!valid) return;

      Object.assign(self.data, formData);
      btn.disabled = true;
      btn.textContent = 'Invio in corso...';

      // Salva su Supabase
      self.saveToSupabase(true).then(function() {
        form.style.display = 'none';
        resolve(formData);
      });
    });
    form.appendChild(btn);

    row.appendChild(form);
    self.chatArea.appendChild(row);
    requestAnimationFrame(function() {
      row.classList.add('cf-visible');
      self.scrollToBottom();
    });
  });
};

ChatFlow.prototype.addStima = function() {
  var s = stimaPrezzo(
    this.data.zona || 'Padova',
    this.data.tipo || 'Appartamento',
    this.data.dimensione || '90-120 mq',
    this.data.stato || 'Buone condizioni'
  );
  this.data.stima_min = s.min;
  this.data.stima_med = s.med;
  this.data.stima_max = s.max;
  this.data.stima_mq = s.mqPrezzo;

  var html = '<div class="cf-stima">' +
    '<div class="cf-stima-label">Stima indicativa del tuo immobile</div>' +
    '<div class="cf-stima-value">' + s.med.toLocaleString('it-IT') + ' &euro;</div>' +
    '<div class="cf-stima-range">Range: ' + s.min.toLocaleString('it-IT') + ' &euro; — ' + s.max.toLocaleString('it-IT') + ' &euro;</div>' +
    '<div class="cf-stima-mq">' + s.mqPrezzo.toLocaleString('it-IT') + ' &euro;/mq nella tua zona</div>' +
    '</div>';
  return this.addBubble(html, 'bot', 400);
};

ChatFlow.prototype.scrollToBottom = function() {
  var self = this;
  requestAnimationFrame(function() {
    self.chatArea.scrollTop = self.chatArea.scrollHeight;
    window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
  });
};

ChatFlow.prototype.saveToSupabase = function(isFinal) {
  var self = this;
  var payload = {
    session_id: this.sessionId,
    flow_id: this.flowId,
    step: this.currentStep,
    data: JSON.stringify(this.data),
    is_final: !!isFinal,
    page_url: window.location.href,
    created_at: new Date().toISOString()
  };

  return fetch(SUPABASE_URL + '/rest/v1/chat_flow_leads', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'apikey': SUPABASE_KEY,
      'Authorization': 'Bearer ' + SUPABASE_KEY,
      'Prefer': 'return=minimal'
    },
    body: JSON.stringify(payload)
  }).catch(function(err) {
    console.warn('Salvataggio Supabase fallito:', err);
  });
};

ChatFlow.prototype.playStep = function() {
  var self = this;
  if (this.currentStep >= this.steps.length) {
    this.onComplete(this.data);
    return;
  }

  this.updateProgress();
  var step = this.steps[this.currentStep];

  // Salva dati parziali ad ogni step
  if (this.currentStep > 0) {
    this.saveToSupabase(false);
  }

  step.play(this).then(function() {
    self.currentStep++;
    self.playStep();
  });
};

// Esporta funzione di stima per uso esterno
window.ChatFlowStima = stimaPrezzo;

})();
