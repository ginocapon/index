/**
 * WELCOME POPUP — Righetto Immobiliare
 * Avatar Sara ANIMATA: lip-sync, blinking, head movement.
 * Audio: MP3 pre-generato (priorità) → fallback Web Speech API.
 * Si mostra una sola volta per sessione (sessionStorage).
 */
(function () {
  'use strict';

  // ── Non mostrare su pagine admin/utility ──
  var path = location.pathname;
  if (/admin|bookmarklet|scraping|cookie-policy|privacy/i.test(path)) return;

  // ── Una volta per sessione ──
  if (sessionStorage.getItem('welcome_shown')) return;

  // ── Avatar Sara INLINE SVG (animabile) ──
  var SARA_SVG = '<svg class="welcome-avatar-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">' +
    '<defs>' +
      '<linearGradient id="wbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#3A5578"/><stop offset="100%" stop-color="#5C7A9E"/></linearGradient>' +
      '<linearGradient id="whair" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#F2D06B"/><stop offset="100%" stop-color="#D4A843"/></linearGradient>' +
    '</defs>' +
    '<circle cx="60" cy="60" r="60" fill="url(#wbg)"/>' +
    '<g id="sara-head">' +
      // Capelli dietro
      '<ellipse cx="60" cy="48" rx="35" ry="38" fill="url(#whair)"/>' +
      // Viso
      '<ellipse cx="60" cy="62" rx="24" ry="28" fill="#FDDCB5"/>' +
      // Capelli sopra
      '<ellipse cx="60" cy="45" rx="30" ry="20" fill="url(#whair)"/>' +
      '<path d="M30 42 Q35 20 60 18 Q85 20 90 42 Q88 35 75 32 Q60 28 45 32 Q32 35 30 42Z" fill="url(#whair)"/>' +
      // Ciocche laterali
      '<path d="M25 55 Q28 70 35 78" stroke="#D4A843" stroke-width="8" fill="none" stroke-linecap="round"/>' +
      '<path d="M95 55 Q92 70 85 78" stroke="#D4A843" stroke-width="8" fill="none" stroke-linecap="round"/>' +
      // Occhi - bianchi
      '<ellipse cx="48" cy="58" rx="5" ry="4" fill="white"/>' +
      '<ellipse cx="72" cy="58" rx="5" ry="4" fill="white"/>' +
      // Pupille
      '<circle cx="49" cy="58" r="2.5" fill="#2C4A6E"/>' +
      '<circle cx="73" cy="58" r="2.5" fill="#2C4A6E"/>' +
      // Riflesso occhi
      '<circle cx="50" cy="57" r="0.8" fill="white"/>' +
      '<circle cx="74" cy="57" r="0.8" fill="white"/>' +
      // Palpebre (per blink) - inizialmente invisibili
      '<ellipse id="sara-blink-l" cx="48" cy="58" rx="6" ry="0" fill="#FDDCB5"/>' +
      '<ellipse id="sara-blink-r" cx="72" cy="58" rx="6" ry="0" fill="#FDDCB5"/>' +
      // Occhiali
      '<rect x="38" y="55" width="14" height="9" rx="4.5" fill="none" stroke="#556B7A" stroke-width="1.5"/>' +
      '<rect x="62" y="55" width="14" height="9" rx="4.5" fill="none" stroke="#556B7A" stroke-width="1.5"/>' +
      '<line x1="52" y1="59" x2="62" y2="59" stroke="#556B7A" stroke-width="1.2"/>' +
      '<line x1="38" y1="59" x2="28" y2="56" stroke="#556B7A" stroke-width="1.2"/>' +
      '<line x1="76" y1="59" x2="86" y2="56" stroke="#556B7A" stroke-width="1.2"/>' +
      // Guance
      '<ellipse cx="48" cy="66" rx="2" ry="0.8" fill="#E8A090" opacity="0.5"/>' +
      '<ellipse cx="72" cy="66" rx="2" ry="0.8" fill="#E8A090" opacity="0.5"/>' +
      // Bocca — animata! ID per JS
      '<path id="sara-mouth" d="M55 72 Q60 76 65 72" stroke="#C0756B" stroke-width="1.8" fill="none" stroke-linecap="round"/>' +
      // Bocca aperta (riempimento, invisibile di default)
      '<ellipse id="sara-mouth-open" cx="60" cy="74" rx="4" ry="0" fill="#B05050" opacity="0"/>' +
    '</g>' +
    // Corpo
    '<path d="M40 95 Q42 82 60 80 Q78 82 80 95" fill="#3A5578"/>' +
    '<path d="M52 82 L55 90 L60 84 L65 90 L68 82" fill="white" opacity="0.9"/>' +
  '</svg>';

  // ── Testo che Sara "dice" ──
  var WELCOME_LINES = [
    "Ciao! Sono Sara, la tua assistente virtuale di Righetto Immobiliare.",
    "\n\nDal 2000 aiutiamo chi cerca, vende o affitta casa a Padova e in tutta la provincia.",
    "\n\nQui trovi valutazioni gratuite, consulenza su vendita e locazione, gestione completa del tuo immobile e molto altro.",
    "\n\nSe hai domande, la nostra chatbot \u00e8 pronta a risponderti subito! E per tutto il resto, i nostri consulenti sono sempre a disposizione.",
    "\n\nScegli come vuoi continuare \u2935\ufe0f"
  ];

  var fullText = WELCOME_LINES.join('');

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
        '<div class="welcome-avatar-wrap">' + SARA_SVG + '</div>' +
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
  var mouthPath = null;
  var mouthOpen = null;
  var blinkL = null;
  var blinkR = null;
  var headGroup = null;
  var mouthTimer = null;
  var blinkTimer = null;
  var headTimer = null;

  function initAvatarRefs() {
    mouthPath = document.getElementById('sara-mouth');
    mouthOpen = document.getElementById('sara-mouth-open');
    blinkL = document.getElementById('sara-blink-l');
    blinkR = document.getElementById('sara-blink-r');
    headGroup = document.getElementById('sara-head');
  }

  // ══════════════════════════════════════════════
  // ANIMAZIONI AVATAR
  // ══════════════════════════════════════════════

  // ── Lip-sync: bocca che si apre/chiude a ritmo del parlato ──
  var mouthShapes = [
    { d: 'M55 72 Q60 76 65 72', ry: 0, op: 0 },       // chiusa (sorriso)
    { d: 'M54 73 Q60 78 66 73', ry: 2.5, op: 0.8 },   // semi-aperta
    { d: 'M53 73 Q60 80 67 73', ry: 4, op: 1 },        // aperta
    { d: 'M55 73 Q60 77 65 73', ry: 1.5, op: 0.6 },    // leggermente aperta
  ];

  function animateMouth() {
    if (!isSpeaking || !mouthPath || !mouthOpen) return;

    var shape = mouthShapes[Math.floor(Math.random() * mouthShapes.length)];
    mouthPath.setAttribute('d', shape.d);
    mouthOpen.setAttribute('ry', shape.ry);
    mouthOpen.setAttribute('opacity', shape.op);

    // Velocità variabile per sembrare naturale (80-180ms)
    var delay = 80 + Math.random() * 100;
    mouthTimer = setTimeout(animateMouth, delay);
  }

  function stopMouth() {
    if (mouthTimer) clearTimeout(mouthTimer);
    if (mouthPath) mouthPath.setAttribute('d', 'M55 72 Q60 76 65 72');
    if (mouthOpen) { mouthOpen.setAttribute('ry', '0'); mouthOpen.setAttribute('opacity', '0'); }
  }

  // ── Blink: occhi che sbattono periodicamente ──
  function doBlink() {
    if (!blinkL || !blinkR) return;

    // Chiudi palpebre
    blinkL.setAttribute('ry', '5');
    blinkR.setAttribute('ry', '5');

    setTimeout(function () {
      // Riapri
      blinkL.setAttribute('ry', '0');
      blinkR.setAttribute('ry', '0');
    }, 120);

    // Prossimo blink: 2-5 secondi (naturale)
    blinkTimer = setTimeout(doBlink, 2000 + Math.random() * 3000);
  }

  function stopBlink() {
    if (blinkTimer) clearTimeout(blinkTimer);
    if (blinkL) blinkL.setAttribute('ry', '0');
    if (blinkR) blinkR.setAttribute('ry', '0');
  }

  // ── Head: leggero movimento della testa ──
  var headAngle = 0;
  function animateHead() {
    if (!headGroup) return;

    // Oscillazione lenta: -2° a +2°
    headAngle += (Math.random() - 0.5) * 1.5;
    headAngle = Math.max(-2, Math.min(2, headAngle));

    // Leggero shift verticale
    var ty = Math.sin(Date.now() / 1500) * 1.5;

    headGroup.setAttribute('transform',
      'rotate(' + headAngle.toFixed(1) + ' 60 60) translate(0 ' + ty.toFixed(1) + ')');

    headTimer = setTimeout(animateHead, 200);
  }

  function stopHead() {
    if (headTimer) clearTimeout(headTimer);
    if (headGroup) headGroup.setAttribute('transform', '');
  }

  // ── Start/stop tutte le animazioni ──
  function startAnimations() {
    isSpeaking = true;
    animateMouth();
    doBlink();
    animateHead();
  }

  function stopAnimations() {
    isSpeaking = false;
    stopMouth();
    stopBlink();
    stopHead();
  }

  // ── Init ──
  preloadAudio().then(function () {
    setTimeout(function () {
      overlay.classList.add('visible');
      sessionStorage.setItem('welcome_shown', '1');
      setTimeout(function () {
        initAvatarRefs();
        startTypewriter();
      }, 600);
    }, 1200);
  });

  // ── Typewriter ──
  function startTypewriter() {
    charIndex = 0;
    playAudio();
    typeNext();
  }

  function typeNext() {
    if (charIndex >= fullText.length) {
      var cursor = typeEl.querySelector('.cursor');
      if (cursor) cursor.remove();
      actionsEl.classList.add('visible');
      stopAnimations();
      // Sorriso finale
      if (mouthPath) mouthPath.setAttribute('d', 'M54 72 Q60 77 66 72');
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
    if ('speechSynthesis' in window) { window.speechSynthesis.cancel(); }
    stopAnimations();
  }

  // ── Speech API fallback ──
  function speakWithSpeechAPI() {
    if (!speechEnabled || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    var text = fullText.replace(/\n/g, ' ').replace(/\u2935\ufe0f/g, '');
    var utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'it-IT';
    utterance.rate = 0.95;
    utterance.pitch = 1.1;

    utterance.onstart = function () { startAnimations(); };
    utterance.onend = function () { stopAnimations(); };

    function pickVoice() {
      var voices = window.speechSynthesis.getVoices();
      var italian = voices.filter(function (v) { return /it[-_]IT/i.test(v.lang); });
      var preferred = italian.filter(function (v) {
        return /female|donna|google.*it|alice|elsa|federica|isabella|natural/i.test(v.name);
      });
      if (preferred.length) return preferred[0];
      if (italian.length) return italian[0];
      return null;
    }

    var voice = pickVoice();
    if (voice) {
      utterance.voice = voice;
      window.speechSynthesis.speak(utterance);
    } else {
      window.speechSynthesis.onvoiceschanged = function () {
        var v = pickVoice();
        if (v) utterance.voice = v;
        window.speechSynthesis.speak(utterance);
        window.speechSynthesis.onvoiceschanged = null;
      };
      setTimeout(function () {
        if (!window.speechSynthesis.speaking) window.speechSynthesis.speak(utterance);
      }, 300);
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

  // ── Chiudi popup ──
  function closePopup() {
    if (typeTimer) clearTimeout(typeTimer);
    stopAudio();
    overlay.classList.remove('visible');
    setTimeout(function () { overlay.remove(); }, 400);
  }

  overlay.querySelector('.welcome-close').addEventListener('click', closePopup);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) closePopup(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && document.getElementById('welcome-overlay')) closePopup();
  });

  // ── CTA: Apri chatbot ──
  document.getElementById('welcome-chatbot').addEventListener('click', function () {
    closePopup();
    setTimeout(function () {
      if (window.rigChat && typeof window.rigChat.toggle === 'function') {
        var box = document.getElementById('rig-chat-box');
        if (!box || !box.classList.contains('open')) window.rigChat.toggle();
      }
    }, 500);
  });

  // ── CTA: Buona navigazione ──
  document.getElementById('welcome-browse').addEventListener('click', closePopup);

})();
