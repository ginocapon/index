/**
 * WELCOME POPUP — Righetto Immobiliare
 * Avatar Sara che accoglie il visitatore con voce e testo animato.
 * Si mostra una sola volta per sessione (sessionStorage).
 */
(function () {
  'use strict';

  // ── Non mostrare su pagine admin/utility ──
  var path = location.pathname;
  if (/admin|bookmarklet|scraping|cookie-policy|privacy/i.test(path)) return;

  // ── Una volta per sessione ──
  if (sessionStorage.getItem('welcome_shown')) return;

  // ── Avatar Sara (stesso SVG del chatbot) ──
  var SARA_AVATAR = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120'%3E%3Cdefs%3E%3ClinearGradient id='bg' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0%25' stop-color='%233A5578'/%3E%3Cstop offset='100%25' stop-color='%235C7A9E'/%3E%3C/linearGradient%3E%3ClinearGradient id='hair' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0%25' stop-color='%23F2D06B'/%3E%3Cstop offset='100%25' stop-color='%23D4A843'/%3E%3C/linearGradient%3E%3C/defs%3E%3Ccircle cx='60' cy='60' r='60' fill='url(%23bg)'/%3E%3Cellipse cx='60' cy='48' rx='35' ry='38' fill='url(%23hair)'/%3E%3Cellipse cx='60' cy='62' rx='24' ry='28' fill='%23FDDCB5'/%3E%3Cellipse cx='60' cy='45' rx='30' ry='20' fill='url(%23hair)'/%3E%3Cpath d='M30 42 Q35 20 60 18 Q85 20 90 42 Q88 35 75 32 Q60 28 45 32 Q32 35 30 42Z' fill='url(%23hair)'/%3E%3Cpath d='M25 55 Q28 70 35 78' stroke='%23D4A843' stroke-width='8' fill='none' stroke-linecap='round'/%3E%3Cpath d='M95 55 Q92 70 85 78' stroke='%23D4A843' stroke-width='8' fill='none' stroke-linecap='round'/%3E%3Cellipse cx='48' cy='58' rx='5' ry='4' fill='white'/%3E%3Cellipse cx='72' cy='58' rx='5' ry='4' fill='white'/%3E%3Ccircle cx='49' cy='58' r='2.5' fill='%232C4A6E'/%3E%3Ccircle cx='73' cy='58' r='2.5' fill='%232C4A6E'/%3E%3Ccircle cx='50' cy='57' r='0.8' fill='white'/%3E%3Ccircle cx='74' cy='57' r='0.8' fill='white'/%3E%3Crect x='38' y='55' width='14' height='9' rx='4.5' fill='none' stroke='%23556B7A' stroke-width='1.5'/%3E%3Crect x='62' y='55' width='14' height='9' rx='4.5' fill='none' stroke='%23556B7A' stroke-width='1.5'/%3E%3Cline x1='52' y1='59' x2='62' y2='59' stroke='%23556B7A' stroke-width='1.2'/%3E%3Cline x1='38' y1='59' x2='28' y2='56' stroke='%23556B7A' stroke-width='1.2'/%3E%3Cline x1='76' y1='59' x2='86' y2='56' stroke='%23556B7A' stroke-width='1.2'/%3E%3Cellipse cx='48' cy='66' rx='2' ry='0.8' fill='%23E8A090' opacity='0.5'/%3E%3Cellipse cx='72' cy='66' rx='2' ry='0.8' fill='%23E8A090' opacity='0.5'/%3E%3Cpath d='M55 72 Q60 76 65 72' stroke='%23C0756B' stroke-width='1.8' fill='none' stroke-linecap='round'/%3E%3Cpath d='M40 95 Q42 82 60 80 Q78 82 80 95' fill='%233A5578'/%3E%3Cpath d='M52 82 L55 90 L60 84 L65 90 L68 82' fill='white' opacity='0.9'/%3E%3C/svg%3E";

  // ── Testo che Sara "dice" ──
  var WELCOME_LINES = [
    "Ciao! Sono Sara, la tua assistente virtuale di Righetto Immobiliare.",
    "\n\nDal 1990 aiutiamo chi cerca, vende o affitta casa a Padova e in tutta la provincia.",
    "\n\nQui trovi valutazioni gratuite, consulenza su vendita e locazione, gestione completa del tuo immobile e molto altro.",
    "\n\nSe hai domande, la nostra chatbot \u00e8 pronta a risponderti subito! E per tutto il resto, i nostri consulenti sono sempre a disposizione.",
    "\n\nScegli come vuoi continuare \u2935\ufe0f"
  ];

  var fullText = WELCOME_LINES.join('');

  // ── Crea il DOM ──
  var overlay = document.createElement('div');
  overlay.id = 'welcome-overlay';
  overlay.innerHTML =
    '<div id="welcome-card" style="position:relative">' +
      '<button class="welcome-close" aria-label="Chiudi">&times;</button>' +
      '<div class="welcome-header">' +
        '<img class="welcome-avatar" src="' + SARA_AVATAR + '" alt="Sara">' +
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
  var speechEnabled = true;
  var speechUtterance = null;
  var charIndex = 0;
  var typeTimer = null;

  // ── Mostra con piccolo ritardo ──
  setTimeout(function () {
    overlay.classList.add('visible');
    sessionStorage.setItem('welcome_shown', '1');
    setTimeout(startTypewriter, 600);
  }, 1200);

  // ── Typewriter ──
  function startTypewriter() {
    charIndex = 0;
    speakText(fullText.replace(/\n/g, ' '));
    typeNext();
  }

  function typeNext() {
    if (charIndex >= fullText.length) {
      // Rimuovi cursore e mostra CTA
      var cursor = typeEl.querySelector('.cursor');
      if (cursor) cursor.remove();
      actionsEl.classList.add('visible');
      return;
    }
    var ch = fullText[charIndex];
    charIndex++;

    if (ch === '\n') {
      // Ignora newline nel typewriter (usiamo <br> per gli a capo doppi)
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
    // Velocità: 28ms/char, pausa più lunga dopo punteggiatura
    var delay = 28;
    if (ch === '.' || ch === '!' || ch === '?') delay = 320;
    else if (ch === ',') delay = 140;

    typeTimer = setTimeout(typeNext, delay);
  }

  // ── Speech Synthesis (italiano) ──
  function speakText(text) {
    if (!speechEnabled || !('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    speechUtterance = new SpeechSynthesisUtterance(text);
    speechUtterance.lang = 'it-IT';
    speechUtterance.rate = 0.95;
    speechUtterance.pitch = 1.1;

    // Cerca una voce femminile italiana
    function pickVoice() {
      var voices = window.speechSynthesis.getVoices();
      var italian = voices.filter(function (v) { return /it[-_]IT/i.test(v.lang); });
      // Preferisci voci femminili
      var female = italian.filter(function (v) {
        return /female|donna|google.*it|alice|elsa|federica|cosimo/i.test(v.name);
      });
      if (female.length) return female[0];
      if (italian.length) return italian[0];
      return null;
    }

    var voice = pickVoice();
    if (voice) {
      speechUtterance.voice = voice;
      window.speechSynthesis.speak(speechUtterance);
    } else {
      // Le voci potrebbero non essere ancora caricate
      window.speechSynthesis.onvoiceschanged = function () {
        var v = pickVoice();
        if (v) {
          speechUtterance.voice = v;
          window.speechSynthesis.speak(speechUtterance);
        } else {
          window.speechSynthesis.speak(speechUtterance);
        }
        window.speechSynthesis.onvoiceschanged = null;
      };
      // Fallback se onvoiceschanged non scatta
      setTimeout(function () {
        if (!window.speechSynthesis.speaking) {
          window.speechSynthesis.speak(speechUtterance);
        }
      }, 300);
    }
  }

  // ── Audio toggle ──
  audioBtn.addEventListener('click', function () {
    speechEnabled = !speechEnabled;
    if (!speechEnabled) {
      window.speechSynthesis.cancel();
      audioBtn.textContent = '\ud83d\udd07 Voce disattivata';
    } else {
      audioBtn.textContent = '\ud83d\udd0a Voce attiva';
      // Se il typewriter è ancora in corso, riavvia la voce dal testo rimanente
      var remaining = fullText.substring(charIndex).replace(/\n/g, ' ');
      if (remaining.length > 5) speakText(remaining);
    }
  });

  // ── Chiudi popup ──
  function closePopup() {
    if (typeTimer) clearTimeout(typeTimer);
    window.speechSynthesis.cancel();
    overlay.classList.remove('visible');
    setTimeout(function () { overlay.remove(); }, 400);
  }

  // X button
  overlay.querySelector('.welcome-close').addEventListener('click', closePopup);

  // Click fuori dal card
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closePopup();
  });

  // ESC
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && document.getElementById('welcome-overlay')) closePopup();
  });

  // ── CTA: Apri chatbot ──
  document.getElementById('welcome-chatbot').addEventListener('click', function () {
    closePopup();
    // Apri il chatbot dopo che il popup è chiuso
    setTimeout(function () {
      if (window.rigChat && typeof window.rigChat.toggle === 'function') {
        var box = document.getElementById('rig-chat-box');
        if (!box || !box.classList.contains('open')) {
          window.rigChat.toggle();
        }
      }
    }, 500);
  });

  // ── CTA: Buona navigazione ──
  document.getElementById('welcome-browse').addEventListener('click', closePopup);

})();
