/**
 * WELCOME POPUP — Righetto Immobiliare
 * Avatar Sara ANIMATA: lip-sync, blinking, head movement.
 * Audio: MP3 pre-generato (priorità) → fallback Web Speech API.
 * Si mostra una sola volta per sessione (sessionStorage).
 */
(function () {
  'use strict';

  // ── Mostrare SOLO sulla home page ──
  var path = location.pathname;
  var isHome = path === '/' || path.endsWith('/index.html') || path.endsWith('/index') || path === '/index.html';
  if (!isHome) return;

  // ── Una volta per sessione ──
  if (sessionStorage.getItem('welcome_shown')) return;

  // ── Avatar Sara — FOTO REALE con animazioni CSS ──
  var SARA_PHOTO = 'img/sara-avatar.jpg';
  var SARA_HTML = '<div class="welcome-avatar-photo" id="sara-photo-wrap">' +
    '<img src="' + SARA_PHOTO + '" alt="Sara — Assistente Righetto Immobiliare" class="welcome-avatar-img" id="sara-photo">' +
    '<div class="sara-speaking-ring" id="sara-ring"></div>' +
    '<div class="sara-glow" id="sara-glow"></div>' +
  '</div>';

  // ── Testo che Sara "dice" ──
  var WELCOME_LINES = [
    "Ciao! Sono Sara, la tua assistente virtuale di Righetto Immobiliare.",
    "\n\nDal 2000 aiutiamo chi cerca, vende o affitta casa a Padova e in tutta la provincia.",
    "\n\nQui trovi valutazioni gratuite, consulenza su vendita e locazione, gestione completa del tuo immobile e molto altro.",
    "\n\nSe hai domande, la nostra chatbot \u00e8 pronta a risponderti subito! E per tutto il resto, i nostri consulenti sono sempre a disposizione.",
    "\n\nScegli come vuoi continuare \u2935\ufe0f"
  ];

  var fullText = WELCOME_LINES.join('');

  // ── Detect mobile / touch devices (iPad compreso) ──
  var isMobile = /Mobi|Android|iPad|iPhone|iPod/i.test(navigator.userAgent) ||
                 (('ontouchstart' in window) && navigator.maxTouchPoints > 0) ||
                 (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1); // iPad con iPadOS

  // ── Su mobile/tablet: non mostrare il popup (pesante e scomodo) ──
  if (isMobile) return;

  // ── Audio engine ──
  var AUDIO_MP3 = 'audio/welcome-sara.mp3';
  var audioEl = null;
  var usingMp3 = false;
  var audioReady = false;
  var speechEnabled = true;
  var isSpeaking = false;

  function preloadAudio() {
    return new Promise(function (resolve) {
      audioEl = new Audio();
      audioEl.preload = 'auto';
      audioEl.addEventListener('canplaythrough', function () {
        usingMp3 = true; audioReady = true; resolve(true);
      }, { once: true });
      audioEl.addEventListener('error', function () {
        usingMp3 = false; audioReady = true; resolve(false);
      }, { once: true });
      setTimeout(function () {
        if (!audioReady) { usingMp3 = false; audioReady = true; resolve(false); }
      }, 3000);
      audioEl.src = AUDIO_MP3;
    });
  }

  // ── Crea il DOM ──
  var overlay = document.createElement('div');
  overlay.id = 'welcome-overlay';
  overlay.innerHTML =
    '<div id="welcome-card" style="position:relative">' +
      '<button class="welcome-close" aria-label="Chiudi">&times;</button>' +
      '<div class="welcome-header">' +
        '<div class="welcome-avatar-wrap">' + SARA_HTML + '</div>' +
        '<div class="welcome-header-text">' +
          '<h3>Benvenuto!</h3>' +
          '<p class="welcome-online">Sara &mdash; assistente virtuale</p>' +
        '</div>' +
      '</div>' +
      '<div class="welcome-body">' +
        '<div class="welcome-text" id="welcome-typewriter"><span class="cursor"></span></div>' +
        '<button class="welcome-audio-toggle" id="welcome-audio-btn" title="Attiva/disattiva voce">' +
          '\ud83d\udd0a Voce attiva' +
        '</button>' +
      '</div>' +
      '<div class="welcome-actions" id="welcome-actions">' +
        '<button class="welcome-btn welcome-btn-primary" id="welcome-chatbot">' +
          '\ud83d\udcac Chatta con Sara' +
        '</button>' +
        '<button class="welcome-btn welcome-btn-secondary" id="welcome-browse">' +
          '\ud83d\udc4b Buona navigazione!' +
        '</button>' +
      '</div>' +
    '</div>';

  document.body.appendChild(overlay);

  // ── Refs ──
  var typeEl = document.getElementById('welcome-typewriter');
  var actionsEl = document.getElementById('welcome-actions');
  var audioBtn = document.getElementById('welcome-audio-btn');
  var charIndex = 0;
  var typeTimer = null;

  // ── Avatar animation refs ──
  // ══════════════════════════════════════════════
  // ANIMAZIONI FOTO REALE — effetti CSS dinamici
  // ══════════════════════════════════════════════
  var saraPhoto = null;
  var saraRing = null;
  var saraGlow = null;
  var animTimer = null;

  function initAvatarRefs() {
    saraPhoto = document.getElementById('sara-photo');
    saraRing = document.getElementById('sara-ring');
    saraGlow = document.getElementById('sara-glow');
  }

  // Quando Sara parla: anello luminoso pulsante + movimenti dinamici corpo/testa
  function startAnimations() {
    isSpeaking = true;
    if (saraPhoto) saraPhoto.classList.remove('idle');
    if (saraRing) saraRing.classList.add('speaking');
    if (saraGlow) saraGlow.classList.add('speaking');
    if (saraPhoto) saraPhoto.classList.add('speaking');
  }

  function stopAnimations() {
    isSpeaking = false;
    if (saraRing) saraRing.classList.remove('speaking');
    if (saraGlow) saraGlow.classList.remove('speaking');
    if (saraPhoto) saraPhoto.classList.remove('speaking');
    // Torna all'animazione idle (respiro leggero)
    if (saraPhoto) saraPhoto.classList.add('idle');
  }

  // ── Init ──
  preloadAudio().then(function () {
    setTimeout(function () {
      overlay.classList.add('visible');
      sessionStorage.setItem('welcome_shown', '1');
      setTimeout(function () {
        initAvatarRefs();
        // Attiva subito l'animazione idle (respiro leggero)
        if (saraPhoto) saraPhoto.classList.add('idle');

        if (isMobile) {
          // Mobile/iPad: avvia typewriter SENZA audio (browser lo blocca)
          // Mostra pulsante PLAY sull'avatar per sbloccare l'audio con tap utente
          startTypewriter(false);
          showMobilePlayBtn();
        } else {
          // Desktop: autoplay come prima
          startTypewriter(true);
        }
      }, 600);
    }, 1200);
  });

  // ── Pulsante PLAY per mobile — sblocca audio con gesto utente ──
  function showMobilePlayBtn() {
    var wrap = document.getElementById('sara-photo-wrap');
    if (!wrap) return;

    var btn = document.createElement('button');
    btn.className = 'sara-mobile-play';
    btn.setAttribute('aria-label', 'Ascolta Sara');
    btn.innerHTML =
      '<svg viewBox="0 0 24 24"><polygon points="6,3 20,12 6,21"/></svg>' +
      '<span class="sara-play-label">Tocca per ascoltare</span>';
    wrap.style.position = 'relative';
    wrap.appendChild(btn);

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      // Animazione uscita pulsante
      btn.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      btn.style.opacity = '0';
      btn.style.transform = 'translate(-50%, -50%) scale(0.5)';
      setTimeout(function () { btn.remove(); }, 300);

      // Togli idle, avvia audio (il tap dell'utente sblocca l'audio su iOS/Android)
      if (saraPhoto) saraPhoto.classList.remove('idle');
      playAudio();
    }, { once: true });
  }

  // ── Typewriter ──
  function startTypewriter(withAudio) {
    charIndex = 0;
    if (withAudio !== false) playAudio();
    typeNext();
  }

  function typeNext() {
    if (charIndex >= fullText.length) {
      var cursor = typeEl.querySelector('.cursor');
      if (cursor) cursor.remove();
      actionsEl.classList.add('visible');
      stopAnimations();
      return;
    }
    var ch = fullText[charIndex];
    charIndex++;

    if (ch === '\n') {
      if (charIndex < fullText.length && fullText[charIndex] === '\n') {
        charIndex++;
        var br = document.createElement('br');
        typeEl.insertBefore(br, typeEl.querySelector('.cursor'));
      }
      typeTimer = setTimeout(typeNext, 10);
      return;
    }

    var span = document.createTextNode(ch);
    typeEl.insertBefore(span, typeEl.querySelector('.cursor'));

    var delay = 28;
    if (ch === '.' || ch === '!' || ch === '?') delay = 320;
    else if (ch === ',') delay = 140;

    typeTimer = setTimeout(typeNext, delay);
  }

  // ══════════════════════════════════════════════
  // AUDIO: MP3 (priorità) → Speech API (fallback)
  // ══════════════════════════════════════════════

  function playAudio() {
    if (!speechEnabled) return;

    if (usingMp3 && audioEl) {
      audioEl.currentTime = 0;
      audioEl.addEventListener('play', function () { startAnimations(); }, { once: true });
      audioEl.addEventListener('ended', function () { stopAnimations(); }, { once: true });
      audioEl.addEventListener('pause', function () { if (audioEl.ended) return; stopAnimations(); }, { once: true });
      audioEl.play().catch(function () {
        speakWithSpeechAPI();
      });
    } else {
      speakWithSpeechAPI();
    }
  }

  function stopAudio() {
    if (audioEl) { audioEl.pause(); audioEl.currentTime = 0; }
    speechAborted = true;
    speechQueue = [];
    if ('speechSynthesis' in window) { window.speechSynthesis.cancel(); }
    stopAnimations();
  }

  // ══════════════════════════════════════════════
  // SPEECH API ULTRA-NATURALE — frase per frase
  // con pause, intonazione variabile, voce premium
  // ══════════════════════════════════════════════

  // Frasi separate per parlato naturale (con pause tra ognuna)
  var SPEECH_PHRASES = [
    { text: "Ciao!", rate: 0.92, pitch: 1.15, pause: 500 },
    { text: "Sono Sara, la tua assistente virtuale di Righetto Immobiliare.", rate: 0.88, pitch: 1.08, pause: 700 },
    { text: "Dal 2000 aiutiamo chi cerca, vende o affitta casa a Padova e in tutta la provincia.", rate: 0.85, pitch: 1.05, pause: 800 },
    { text: "Qui trovi valutazioni gratuite, consulenza su vendita e locazione, gestione completa del tuo immobile e molto altro.", rate: 0.87, pitch: 1.06, pause: 700 },
    { text: "Se hai domande, la nostra chatbot è pronta a risponderti subito!", rate: 0.90, pitch: 1.10, pause: 400 },
    { text: "E per tutto il resto, i nostri consulenti sono sempre a disposizione.", rate: 0.86, pitch: 1.04, pause: 600 },
    { text: "Scegli come vuoi continuare!", rate: 0.90, pitch: 1.12, pause: 0 }
  ];

  var speechQueue = [];
  var speechAborted = false;

  function pickVoice() {
    var voices = window.speechSynthesis.getVoices();
    var italian = voices.filter(function (v) { return /it[-_]IT/i.test(v.lang); });

    // Ranking di qualità: preferisci voci neurali/premium
    var ranking = [
      /neural/i,
      /premium/i,
      /enhanced/i,
      /natural/i,
      /isabella/i,
      /elsa/i,
      /federica/i,
      /alice/i,
      /google.*it/i,
      /microsoft.*it/i,
      /female|donna/i
    ];

    var best = null;
    var bestScore = -1;

    italian.forEach(function (v) {
      var score = 0;
      ranking.forEach(function (pattern, i) {
        if (pattern.test(v.name)) score += (ranking.length - i) * 10;
      });
      // Bonus per voci locali (non remote) → più veloci
      if (!v.localService) score += 5;
      if (score > bestScore) { bestScore = score; best = v; }
    });

    return best || (italian.length ? italian[0] : null);
  }

  function speakWithSpeechAPI() {
    if (!speechEnabled || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    speechAborted = false;
    speechQueue = SPEECH_PHRASES.slice();

    function speakNext() {
      if (speechAborted || speechQueue.length === 0) {
        stopAnimations();
        return;
      }

      var phrase = speechQueue.shift();
      var utterance = new SpeechSynthesisUtterance(phrase.text);
      utterance.lang = 'it-IT';
      utterance.rate = phrase.rate;
      utterance.pitch = phrase.pitch;
      utterance.volume = 1;

      var voice = pickVoice();
      if (voice) utterance.voice = voice;

      utterance.onstart = function () { startAnimations(); };
      utterance.onend = function () {
        if (speechAborted) { stopAnimations(); return; }
        // Pausa naturale tra frasi
        if (phrase.pause > 0 && speechQueue.length > 0) {
          stopAnimations();
          setTimeout(function () {
            if (!speechAborted) speakNext();
          }, phrase.pause);
        } else {
          speakNext();
        }
      };
      utterance.onerror = function () {
        if (!speechAborted && speechQueue.length > 0) speakNext();
        else stopAnimations();
      };

      window.speechSynthesis.speak(utterance);
    }

    // Attendi che le voci siano caricate
    var voice = pickVoice();
    if (voice) {
      speakNext();
    } else {
      window.speechSynthesis.onvoiceschanged = function () {
        window.speechSynthesis.onvoiceschanged = null;
        speakNext();
      };
      setTimeout(function () {
        if (!window.speechSynthesis.speaking && !speechAborted) speakNext();
      }, 400);
    }
  }

  // ── Audio toggle ──
  audioBtn.addEventListener('click', function () {
    speechEnabled = !speechEnabled;
    if (!speechEnabled) {
      stopAudio();
      audioBtn.textContent = '\ud83d\udd07 Voce disattivata';
    } else {
      audioBtn.textContent = '\ud83d\udd0a Voce attiva';
      if (charIndex < fullText.length) playAudio();
    }
  });

  // ══════════════════════════════════════════════
  // PARTICLE DISINTEGRATION — Effetto "Thanos snap"
  // Sara si dissolve in particelle che volano via
  // ══════════════════════════════════════════════

  var isDisintegrating = false;

  function disintegrateSara(callback) {
    if (isDisintegrating) return;
    isDisintegrating = true;

    var photo = document.getElementById('sara-photo');
    var wrap = document.getElementById('sara-photo-wrap');
    if (!photo || !wrap) { if (callback) callback(); return; }

    // Misure reali dell'avatar nel DOM
    var rect = photo.getBoundingClientRect();
    var w = Math.round(rect.width);
    var h = Math.round(rect.height);
    if (w === 0 || h === 0) { if (callback) callback(); return; }

    // Canvas sorgente: disegna la foto
    var srcCanvas = document.createElement('canvas');
    srcCanvas.width = w;
    srcCanvas.height = h;
    var srcCtx = srcCanvas.getContext('2d');

    // Clip circolare come la foto
    srcCtx.beginPath();
    srcCtx.arc(w / 2, h / 2, w / 2, 0, Math.PI * 2);
    srcCtx.closePath();
    srcCtx.clip();
    srcCtx.drawImage(photo, 0, 0, w, h);

    var imageData = srcCtx.getImageData(0, 0, w, h);
    var pixels = imageData.data;

    // Crea N canvas-particella sovrapposti
    var PARTICLE_COLS = 80;
    var PARTICLE_ROWS = 80;
    var cellW = w / PARTICLE_COLS;
    var cellH = h / PARTICLE_ROWS;
    var particles = [];

    // Container per le particelle — posizionato sopra l'avatar
    var particleContainer = document.createElement('div');
    particleContainer.style.cssText =
      'position:absolute;top:0;left:0;width:100%;height:100%;' +
      'pointer-events:none;z-index:10;overflow:visible;border-radius:50%;';
    wrap.style.position = 'relative';
    wrap.appendChild(particleContainer);

    // Genera particelle
    for (var row = 0; row < PARTICLE_ROWS; row++) {
      for (var col = 0; col < PARTICLE_COLS; col++) {
        var px = Math.floor(col * cellW + cellW / 2);
        var py = Math.floor(row * cellH + cellH / 2);
        var idx = (py * w + px) * 4;

        // Salta pixel trasparenti (fuori dal cerchio)
        if (pixels[idx + 3] < 30) continue;

        // Colore medio del blocco
        var r = pixels[idx];
        var g = pixels[idx + 1];
        var b = pixels[idx + 2];

        var particle = document.createElement('div');
        var size = Math.random() * 2.5 + 1.5;

        particle.style.cssText =
          'position:absolute;border-radius:50%;' +
          'width:' + size + 'px;height:' + size + 'px;' +
          'background:rgb(' + r + ',' + g + ',' + b + ');' +
          'left:' + (col * cellW) + 'px;top:' + (row * cellH) + 'px;' +
          'opacity:1;pointer-events:none;will-change:transform,opacity;';

        particleContainer.appendChild(particle);

        // Direzione di volo casuale (prevalentemente verso destra e in alto)
        var angle = (Math.random() - 0.3) * Math.PI;
        var speed = Math.random() * 120 + 40;
        var dx = Math.cos(angle) * speed;
        var dy = Math.sin(angle) * speed - Math.random() * 60;

        // Delay progressivo: da sinistra a destra come un'onda
        var delay = (col / PARTICLE_COLS) * 800 + Math.random() * 400;
        var duration = Math.random() * 800 + 800;

        particles.push({
          el: particle,
          dx: dx,
          dy: dy,
          delay: delay,
          duration: duration,
          rotation: Math.random() * 360
        });
      }
    }

    // Nascondi gli effetti glow/ring
    if (saraRing) saraRing.style.transition = 'opacity 0.3s';
    if (saraRing) saraRing.style.opacity = '0';
    if (saraGlow) saraGlow.style.transition = 'opacity 0.3s';
    if (saraGlow) saraGlow.style.opacity = '0';

    // Fade out testo header, body, bottoni
    var card = document.getElementById('welcome-card');
    var header = card.querySelector('.welcome-header-text');
    var body = card.querySelector('.welcome-body');
    var actions = card.querySelector('.welcome-actions');

    if (header) { header.style.transition = 'opacity 0.6s ease'; header.style.opacity = '0'; }
    if (body) { body.style.transition = 'opacity 0.6s ease 0.3s'; body.style.opacity = '0'; }
    if (actions) { actions.style.transition = 'opacity 0.4s ease'; actions.style.opacity = '0'; }

    // Anima ogni particella
    requestAnimationFrame(function () {
      particles.forEach(function (p) {
        setTimeout(function () {
          p.el.style.transition = 'transform ' + p.duration + 'ms cubic-bezier(0.4,0,0.2,1), opacity ' + p.duration + 'ms ease-out';
          p.el.style.transform = 'translate(' + p.dx + 'px,' + p.dy + 'px) rotate(' + p.rotation + 'deg) scale(0.3)';
          p.el.style.opacity = '0';
        }, p.delay);
      });
    });

    // Fade out la foto originale progressivamente
    setTimeout(function () {
      photo.style.transition = 'opacity 0.8s ease';
      photo.style.opacity = '0';
    }, 300);

    // Fade out bordo avatar
    var avatarWrap = card.querySelector('.welcome-avatar-wrap');
    if (avatarWrap) {
      setTimeout(function () {
        avatarWrap.style.transition = 'opacity 0.5s ease';
        avatarWrap.style.opacity = '0';
      }, 1000);
    }

    // Callback quando l'animazione è finita
    var maxDuration = 1800;
    setTimeout(function () {
      // Dissolvi l'intera card
      if (card) {
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        card.style.opacity = '0';
        card.style.transform = 'scale(0.95)';
      }
      overlay.style.transition = 'opacity 0.5s ease';
      overlay.classList.remove('visible');
      setTimeout(function () {
        overlay.remove();
        isDisintegrating = false;
        if (callback) callback();
      }, 500);
    }, maxDuration);
  }

  // ── Chiudi popup CON effetto disintegrazione ──
  function closePopup(callback) {
    if (typeTimer) clearTimeout(typeTimer);
    stopAudio();
    disintegrateSara(callback || null);
  }

  // ── Chiudi rapido (senza effetto, per ESC/click overlay) ──
  function closePopupFast() {
    if (typeTimer) clearTimeout(typeTimer);
    stopAudio();
    overlay.classList.remove('visible');
    setTimeout(function () { overlay.remove(); }, 400);
  }

  overlay.querySelector('.welcome-close').addEventListener('click', function () { closePopup(); });
  overlay.addEventListener('click', function (e) { if (e.target === overlay) closePopupFast(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && document.getElementById('welcome-overlay')) closePopupFast();
  });

  // ── CTA: Apri chatbot (con disintegrazione) ──
  document.getElementById('welcome-chatbot').addEventListener('click', function () {
    closePopup(function () {
      setTimeout(function () {
        if (window.rigChat && typeof window.rigChat.toggle === 'function') {
          var box = document.getElementById('rig-chat-box');
          if (!box || !box.classList.contains('open')) window.rigChat.toggle();
        }
      }, 200);
    });
  });

  // ── CTA: Buona navigazione (con disintegrazione) ──
  document.getElementById('welcome-browse').addEventListener('click', function () { closePopup(); });

})();
