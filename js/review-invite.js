/**
 * REVIEW INVITE — Righetto Immobiliare (v3, foto Linda, attesa banner consensi)
 * Invito non bloccante a lasciare una recensione su Google.
 * - Visibile a tutti i visitatori, nessuna selezione (niente gating, niente incentivi).
 * - Card piccola in basso a sinistra con la foto di Linda; non copre i contenuti.
 * - Compare UNA SOLA VOLTA per visita, dopo 60 secondi sulla pagina (scelta di Gino,
 *   9 nov 2026). Nessun trigger su apertura chat, scroll o uscita.
 * - X / "Non ora" / click sul bottone: non riappare per 30 giorni (localStorage, solo
 *   preferenza di chiusura: nessun tracking, nessun dato inviato).
 * - Testo EN automatico sulle pagine con <html lang="en">.
 * - Banner consensi: se il banner cookie del sito e' visibile, la card aspetta
 *   la sua chiusura (il consenso ha priorita', mai un invito tagliato sotto il banner).
 * - Demo/anteprima: aprire una pagina con #demo-recensione per mostrarlo subito.
 */
(function () {
  'use strict';

  var REVIEW_URL = 'https://g.page/r/Cen8QVNvgrKKEAE/review';
  var PHOTO_URL = 'img/team/real-state-linda-righetto.webp?v=20260606';
  var KEY = 'rig_review_invite_hide';
  var SESSION_KEY = 'rig_review_invite_shown';
  var DAYS_HIDDEN = 30;

  var en = /^en/i.test(document.documentElement.lang || '');
  var T = en ? {
    aria: 'Invitation to leave a review',
    close: 'Close',
    photo: 'Linda — Righetto Immobiliare',
    title: 'Have you had an experience with us?',
    body: 'Your review on Google helps other families choose with confidence.',
    btn: 'Leave a review on Google',
    later: 'Not now'
  } : {
    aria: 'Invito a lasciare una recensione',
    close: 'Chiudi',
    photo: 'Linda — Righetto Immobiliare',
    title: 'Hai avuto un\'esperienza con noi?',
    body: 'La tua recensione su Google aiuta altre famiglie a scegliere con fiducia.',
    btn: 'Lascia una recensione su Google',
    later: 'Non ora'
  };

  var demo = location.hash === '#demo-recensione';

  if (!demo) {
    try {
      var hiddenAt = localStorage.getItem(KEY);
      if (hiddenAt && Date.now() - Number(hiddenAt) < DAYS_HIDDEN * 864e5) return;
    } catch (e) { /* storage non disponibile: mostra comunque una volta */ }
  }

  function hide(persist) {
    var el = document.getElementById('rig-review-invite');
    if (el) el.remove();
    if (persist) {
      try { localStorage.setItem(KEY, String(Date.now())); } catch (e) {}
    }
  }

  function show() {
    if (document.getElementById('rig-review-invite')) return;

    var css = document.createElement('style');
    css.textContent =
      '#rig-review-invite{position:fixed;left:16px;bottom:16px;z-index:9990;max-width:340px;' +
      'background:#16283f;color:#f5f2ec;border-radius:14px;padding:16px 18px 14px 84px;' +
      'box-shadow:0 8px 30px rgba(10,20,35,.35);font-family:inherit;line-height:1.45;' +
      'animation:rigReviewIn .35s ease-out}' +
      '@keyframes rigReviewIn{from{transform:translateY(16px);opacity:0}to{transform:none;opacity:1}}' +
      '#rig-review-invite .rri-photo{position:absolute;left:16px;top:16px;width:52px;height:52px;' +
      'border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.25)}' +
      '#rig-review-invite .rri-close{position:absolute;top:6px;right:10px;background:none;border:0;' +
      'color:rgba(245,242,236,.6);font-size:18px;cursor:pointer;padding:4px;line-height:1}' +
      '#rig-review-invite .rri-close:hover{color:#fff}' +
      '#rig-review-invite strong{display:block;font-size:15px;margin-bottom:4px;padding-right:18px}' +
      '#rig-review-invite p{margin:0 0 12px;font-size:13px;color:rgba(245,242,236,.85)}' +
      '#rig-review-invite .rri-btn{display:inline-block;background:#ff6b35;color:#fff;' +
      'padding:10px 16px;border-radius:8px;font-weight:700;font-size:14px;text-decoration:none}' +
      '#rig-review-invite .rri-btn:hover{background:#e85a28}' +
      '#rig-review-invite .rri-later{display:inline-block;margin-left:12px;font-size:12px;' +
      'color:rgba(245,242,236,.6);background:none;border:0;cursor:pointer;text-decoration:underline}' +
      '@media (max-width:560px){#rig-review-invite{left:10px;right:auto;bottom:10px;max-width:calc(100vw - 96px)}}';
    document.head.appendChild(css);

    var card = document.createElement('div');
    card.id = 'rig-review-invite';
    card.setAttribute('role', 'dialog');
    card.setAttribute('aria-label', T.aria);
    card.innerHTML =
      '<img class="rri-photo" src="' + PHOTO_URL + '" alt="' + T.photo + '" loading="lazy" data-ai-generated="false" data-rig-photo-caption="skip">' +
      '<button type="button" class="rri-close" aria-label="' + T.close + '">&times;</button>' +
      '<strong>' + T.title + '</strong>' +
      '<p>' + T.body + '</p>' +
      '<a class="rri-btn" href="' + REVIEW_URL + '" target="_blank" rel="noopener noreferrer">' + T.btn + '</a>' +
      '<button type="button" class="rri-later">' + T.later + '</button>';
    document.body.appendChild(card);

    card.querySelector('.rri-close').addEventListener('click', function () { hide(true); });
    card.querySelector('.rri-later').addEventListener('click', function () { hide(true); });
    // Il click sul bottone conta come risposta: non riproporre per 30 giorni.
    card.querySelector('.rri-btn').addEventListener('click', function () { hide(true); });
  }

  /* Banner consensi del sito (#rig-cookie-banner, bottom, z-index 99999): se e'
     visibile copre la card. Il consenso ha priorita': la card compare solo quando
     il banner e' chiuso o assente (controllo ogni secondo, max 30 minuti). */
  function bannerUp() {
    var b = document.getElementById('rig-cookie-banner');
    return !!(b && !b.classList.contains('rig-hidden'));
  }

  function showWhenClear() {
    if (!bannerUp()) { show(); return; }
    var poll = setInterval(function () {
      if (!bannerUp()) { clearInterval(poll); show(); }
    }, 1000);
    setTimeout(function () { clearInterval(poll); }, 30 * 60 * 1000);
  }

  if (demo) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', showWhenClear);
    } else {
      showWhenClear();
    }
    return;
  }

  var shown = false;
  try {
    if (window.sessionStorage && sessionStorage.getItem(SESSION_KEY)) shown = true;
  } catch (e) {}
  function triggerShow() {
    if (shown) return;
    shown = true;
    try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (e) {}
    showWhenClear();
  }

  /* Unico trigger: 60 secondi sulla pagina (steering Gino 9 nov 11:13).
     Nessun trigger su apertura chat, scroll o uscita: non interrompere chi naviga. */
  setTimeout(triggerShow, 60000);
})();
