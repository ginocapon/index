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

  // ── Avatar Sara REALISTICO SVG (quasi 3D, animabile) ──
  var SARA_SVG = '<svg class="welcome-avatar-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">' +
    '<defs>' +
      // Sfondo
      '<radialGradient id="wbg" cx="50%" cy="40%" r="55%">' +
        '<stop offset="0%" stop-color="#5C7A9E"/>' +
        '<stop offset="100%" stop-color="#2C4A6E"/>' +
      '</radialGradient>' +
      // Pelle con effetto 3D
      '<radialGradient id="wskin" cx="45%" cy="38%" r="55%">' +
        '<stop offset="0%" stop-color="#FDE8D0"/>' +
        '<stop offset="60%" stop-color="#F5D0A9"/>' +
        '<stop offset="100%" stop-color="#E8B88A"/>' +
      '</radialGradient>' +
      // Ombra sotto il mento
      '<radialGradient id="wchin" cx="50%" cy="0%" r="80%">' +
        '<stop offset="0%" stop-color="#D4A07A" stop-opacity="0.4"/>' +
        '<stop offset="100%" stop-color="#D4A07A" stop-opacity="0"/>' +
      '</radialGradient>' +
      // Capelli
      '<linearGradient id="whair" x1="0" y1="0" x2="0.3" y2="1">' +
        '<stop offset="0%" stop-color="#4A3728"/>' +
        '<stop offset="40%" stop-color="#3B2A1E"/>' +
        '<stop offset="100%" stop-color="#2A1D14"/>' +
      '</linearGradient>' +
      // Riflesso capelli
      '<linearGradient id="whairhl" x1="0.3" y1="0" x2="0.7" y2="1">' +
        '<stop offset="0%" stop-color="#7A5C42" stop-opacity="0.6"/>' +
        '<stop offset="100%" stop-color="#7A5C42" stop-opacity="0"/>' +
      '</linearGradient>' +
      // Iride
      '<radialGradient id="wiris" cx="45%" cy="42%">' +
        '<stop offset="0%" stop-color="#6B8E5A"/>' +
        '<stop offset="50%" stop-color="#4A7040"/>' +
        '<stop offset="100%" stop-color="#2E4A28"/>' +
      '</radialGradient>' +
      // Labbra
      '<linearGradient id="wlips" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0%" stop-color="#D4726A"/>' +
        '<stop offset="100%" stop-color="#B85A55"/>' +
      '</linearGradient>' +
      // Vestito
      '<linearGradient id="wdress" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0%" stop-color="#2C4A6E"/>' +
        '<stop offset="100%" stop-color="#1E3650"/>' +
      '</linearGradient>' +
      // Filtro ombra morbida
      '<filter id="wshadow" x="-10%" y="-10%" width="120%" height="120%">' +
        '<feGaussianBlur in="SourceAlpha" stdDeviation="2" result="blur"/>' +
        '<feOffset dx="0" dy="2" result="off"/>' +
        '<feFlood flood-color="#1a1a1a" flood-opacity="0.2"/>' +
        '<feComposite in2="off" operator="in"/>' +
        '<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>' +
      '</filter>' +
    '</defs>' +
    // Sfondo circolare
    '<circle cx="100" cy="100" r="100" fill="url(#wbg)"/>' +
    // Corpo/spalle
    '<path d="M45 168 Q50 148 72 140 L80 138 Q90 136 100 135 Q110 136 120 138 L128 140 Q150 148 155 168 L155 200 L45 200Z" fill="url(#wdress)"/>' +
    // Collana
    '<ellipse cx="100" cy="142" rx="12" ry="3" fill="none" stroke="#D4A843" stroke-width="1" opacity="0.6"/>' +
    '<circle cx="100" cy="145" r="2.5" fill="#D4A843" opacity="0.7"/>' +
    // Collo
    '<path d="M88 126 Q88 135 87 140 Q93 142 100 142 Q107 142 113 140 Q112 135 112 126" fill="#F5D0A9"/>' +
    '<path d="M88 126 Q88 135 87 140 Q93 142 100 142 Q107 142 113 140 Q112 135 112 126" fill="url(#wchin)" opacity="0.5"/>' +
    '<g id="sara-head" filter="url(#wshadow)">' +
      // Capelli dietro (volume)
      '<ellipse cx="100" cy="72" rx="52" ry="55" fill="url(#whair)"/>' +
      // Viso ovale realistico
      '<path d="M62 78 Q62 55 78 42 Q88 34 100 34 Q112 34 122 42 Q138 55 138 78 Q138 100 128 112 Q120 122 100 125 Q80 122 72 112 Q62 100 62 78Z" fill="url(#wskin)"/>' +
      // Ombra lato sinistro viso (3D)
      '<path d="M62 78 Q62 55 78 42 Q80 50 72 75 Q68 95 72 112 Q62 100 62 78Z" fill="#D4A07A" opacity="0.2"/>' +
      // Naso — ombra e punta
      '<path d="M98 78 Q100 88 98 95" stroke="#D4A07A" stroke-width="1.2" fill="none" stroke-linecap="round" opacity="0.5"/>' +
      '<ellipse cx="96" cy="96" rx="3.5" ry="2" fill="#E8BA90" opacity="0.4"/>' +
      '<ellipse cx="104" cy="96" rx="3" ry="1.5" fill="#D4A07A" opacity="0.2"/>' +
      // Sopracciglia
      '<path d="M76 67 Q82 63 90 65" stroke="#3B2A1E" stroke-width="2" fill="none" stroke-linecap="round"/>' +
      '<path d="M110 65 Q118 63 124 67" stroke="#3B2A1E" stroke-width="2" fill="none" stroke-linecap="round"/>' +
      // Occhi — sclera (bianco con ombra)
      '<ellipse cx="84" cy="78" rx="9" ry="7" fill="white"/>' +
      '<ellipse cx="116" cy="78" rx="9" ry="7" fill="white"/>' +
      // Ombra superiore occhio (profondità)
      '<ellipse cx="84" cy="76" rx="9" ry="3" fill="#D4A07A" opacity="0.15"/>' +
      '<ellipse cx="116" cy="76" rx="9" ry="3" fill="#D4A07A" opacity="0.15"/>' +
      // Iride
      '<circle cx="86" cy="78" r="5" fill="url(#wiris)"/>' +
      '<circle cx="118" cy="78" r="5" fill="url(#wiris)"/>' +
      // Pupille
      '<circle cx="86" cy="78" r="2.5" fill="#1A2A1A"/>' +
      '<circle cx="118" cy="78" r="2.5" fill="#1A2A1A"/>' +
      // Riflesso occhi (effetto luce)
      '<circle cx="88" cy="76" r="1.8" fill="white" opacity="0.9"/>' +
      '<circle cx="120" cy="76" r="1.8" fill="white" opacity="0.9"/>' +
      '<circle cx="84" cy="80" r="0.8" fill="white" opacity="0.5"/>' +
      '<circle cx="116" cy="80" r="0.8" fill="white" opacity="0.5"/>' +
      // Ciglia superiori
      '<path d="M74 74 Q78 70 84 72 Q90 70 94 74" stroke="#2A1D14" stroke-width="1.8" fill="none" stroke-linecap="round"/>' +
      '<path d="M106 74 Q110 70 116 72 Q122 70 126 74" stroke="#2A1D14" stroke-width="1.8" fill="none" stroke-linecap="round"/>' +
      // Ciglia inferiori sottili
      '<path d="M77 83 Q84 85 91 83" stroke="#3B2A1E" stroke-width="0.5" fill="none" opacity="0.4"/>' +
      '<path d="M109 83 Q116 85 123 83" stroke="#3B2A1E" stroke-width="0.5" fill="none" opacity="0.4"/>' +
      // Palpebre (per blink)
      '<ellipse id="sara-blink-l" cx="84" cy="78" rx="10" ry="0" fill="#F0C8A0"/>' +
      '<ellipse id="sara-blink-r" cx="116" cy="78" rx="10" ry="0" fill="#F0C8A0"/>' +
      // Guance — rossore animato
      '<ellipse id="sara-cheek-l" cx="76" cy="98" rx="10" ry="5" fill="#E8A090" opacity="0.12"/>' +
      '<ellipse id="sara-cheek-r" cx="124" cy="98" rx="10" ry="5" fill="#E8A090" opacity="0.12"/>' +
      // Bocca — labbro superiore
      '<path id="sara-mouth" d="M90 108 Q95 105 100 107 Q105 105 110 108 Q105 112 100 113 Q95 112 90 108Z" fill="url(#wlips)" stroke="#B85A55" stroke-width="0.5"/>' +
      // Bocca aperta (animazione parlato)
      '<ellipse id="sara-mouth-open" cx="100" cy="112" rx="6" ry="0" fill="#8B3A3A" opacity="0"/>' +
      // Riflesso labbra
      '<ellipse cx="100" cy="108" rx="4" ry="1" fill="white" opacity="0.15"/>' +
      // Capelli sopra (frangia e volume)
      '<path d="M52 68 Q55 32 80 24 Q95 20 100 20 Q105 20 120 24 Q145 32 148 68 Q145 50 130 40 Q115 30 100 28 Q85 30 70 40 Q55 50 52 68Z" fill="url(#whair)"/>' +
      // Riflesso capelli (luce)
      '<path d="M70 40 Q80 30 100 28 Q108 28 115 32 Q105 26 95 28 Q80 32 72 45Z" fill="url(#whairhl)"/>' +
      // Ciocche laterali con volume
      '<path d="M52 68 Q48 85 50 105 Q52 112 56 115" stroke="#3B2A1E" stroke-width="12" fill="none" stroke-linecap="round" opacity="0.9"/>' +
      '<path d="M148 68 Q152 85 150 105 Q148 112 144 115" stroke="#3B2A1E" stroke-width="12" fill="none" stroke-linecap="round" opacity="0.9"/>' +
      // Riflesso ciocche
      '<path d="M54 72 Q50 88 52 105" stroke="#7A5C42" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.3"/>' +
      '<path d="M146 72 Q150 88 148 105" stroke="#7A5C42" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.3"/>' +
    '</g>' +
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
  var cheekL = null;
  var cheekR = null;
  var mouthTimer = null;
  var blinkTimer = null;
  var headTimer = null;
  var blushTimer = null;

  function initAvatarRefs() {
    mouthPath = document.getElementById('sara-mouth');
    mouthOpen = document.getElementById('sara-mouth-open');
    blinkL = document.getElementById('sara-blink-l');
    blinkR = document.getElementById('sara-blink-r');
    headGroup = document.getElementById('sara-head');
    cheekL = document.getElementById('sara-cheek-l');
    cheekR = document.getElementById('sara-cheek-r');
  }

  // ══════════════════════════════════════════════
  // ANIMAZIONI AVATAR
  // ══════════════════════════════════════════════

  // ── Lip-sync: bocca che si apre/chiude a ritmo del parlato ──
  var mouthShapes = [
    { d: 'M90 108 Q95 105 100 107 Q105 105 110 108 Q105 112 100 113 Q95 112 90 108Z', ry: 0, op: 0 },
    { d: 'M90 108 Q95 104 100 106 Q105 104 110 108 Q105 114 100 115 Q95 114 90 108Z', ry: 4, op: 0.8 },
    { d: 'M91 108 Q95 103 100 105 Q105 103 109 108 Q105 116 100 117 Q95 116 91 108Z', ry: 6, op: 1 },
    { d: 'M90 108 Q95 105 100 107 Q105 105 110 108 Q105 113 100 114 Q95 113 90 108Z', ry: 2.5, op: 0.6 },
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
    if (mouthPath) mouthPath.setAttribute('d', 'M90 108 Q95 105 100 107 Q105 105 110 108 Q105 112 100 113 Q95 112 90 108Z');
    if (mouthOpen) { mouthOpen.setAttribute('ry', '0'); mouthOpen.setAttribute('opacity', '0'); }
  }

  // ── Blink: occhi che sbattono periodicamente ──
  function doBlink() {
    if (!blinkL || !blinkR) return;

    // Chiudi palpebre
    blinkL.setAttribute('ry', '8');
    blinkR.setAttribute('ry', '8');

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
      'rotate(' + headAngle.toFixed(1) + ' 100 80) translate(0 ' + ty.toFixed(1) + ')');

    headTimer = setTimeout(animateHead, 200);
  }

  function stopHead() {
    if (headTimer) clearTimeout(headTimer);
    if (headGroup) headGroup.setAttribute('transform', '');
  }

  // ── Blush: guance che si arrossano quando parla ──
  var blushLevel = 0.12;

  function animateBlush() {
    if (!cheekL || !cheekR) return;

    // Sale gradualmente fino a 0.55-0.7 con piccole oscillazioni
    if (isSpeaking && blushLevel < 0.6) {
      blushLevel += 0.03;
    }
    // Oscillazione naturale: rossore che pulsa leggermente
    var pulse = Math.sin(Date.now() / 800) * 0.08;
    var val = Math.min(0.7, blushLevel + pulse);

    cheekL.setAttribute('opacity', val.toFixed(2));
    cheekR.setAttribute('opacity', val.toFixed(2));

    blushTimer = setTimeout(animateBlush, 120);
  }

  function fadeBlush() {
    if (blushTimer) clearTimeout(blushTimer);
    // Sfuma lentamente il rossore dopo che smette di parlare
    function fade() {
      if (blushLevel <= 0.15) {
        blushLevel = 0.12;
        if (cheekL) cheekL.setAttribute('opacity', '0.12');
        if (cheekR) cheekR.setAttribute('opacity', '0.12');
        return;
      }
      blushLevel -= 0.02;
      if (cheekL) cheekL.setAttribute('opacity', blushLevel.toFixed(2));
      if (cheekR) cheekR.setAttribute('opacity', blushLevel.toFixed(2));
      blushTimer = setTimeout(fade, 80);
    }
    fade();
  }

  // ── Start/stop tutte le animazioni ──
  function startAnimations() {
    isSpeaking = true;
    animateMouth();
    doBlink();
    animateHead();
    animateBlush();
  }

  function stopAnimations() {
    isSpeaking = false;
    stopMouth();
    stopBlink();
    stopHead();
    fadeBlush();
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
      if (mouthPath) mouthPath.setAttribute('d', 'M90 108 Q95 104 100 106 Q105 104 110 108 Q105 113 100 114 Q95 113 90 108Z');
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
