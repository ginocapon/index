/* Filtro anti-bot gratuito per i moduli che salvano richieste. Nessun servizio esterno.
   Regole (solo lato browser, vedi limiti nel README):
   1. Campo trappola nascosto (honeypot): se compilato, la richiesta e' scartata in silenzio.
   2. Tempo minimo dalla apertura pagina all'invio: sotto 3 secondi, errore visibile "riprova".
   3. Nome o cognome fatto di lettere maiuscole/minuscole casuali: errore visibile con telefono dell'agenzia,
      cosi' un cliente vero non perde la richiesta.
   Mai blocco per telefono, email o zona: troppi clienti veri hanno formati insoliti (esteri, alias). */
(function (global) {
  'use strict';
  var MIN_MS = 3000;
  var loadedAt = Date.now();

  function caseFlips(tok) { // passaggi minuscola->MAIUSCOLA dentro una parola
    var n = 0;
    for (var i = 1; i < tok.length; i++) {
      if (/[a-zà-ÿ]/.test(tok[i - 1]) && /[A-ZÀ-Ý]/.test(tok[i])) n++;
    }
    return n;
  }
  function gibberishToken(tok) {
    tok = String(tok || '').replace(/[^A-Za-zÀ-ÿ]/g, '');
    if (tok.length < 7) return false;
    return caseFlips(tok) >= 3; // McDonald=1, DeLuca=1, MariaGrazia=1: mai >=3
  }
  function gibberishName(s) {
    return String(s || '').split(/\s+/).some(gibberishToken);
  }

  function check(o) {
    o = o || {};
    if (String(o.honeypot || '').trim() !== '') return { ok: false, action: 'drop-silent', reason: 'honeypot' };
    var elapsed = typeof o.elapsedMs === 'number' ? o.elapsedMs : (Date.now() - loadedAt);
    if (elapsed < MIN_MS) return { ok: false, action: 'block-visible', reason: 'too-fast' };
    if (gibberishName(o.nome) || gibberishName(o.cognome)) return { ok: false, action: 'block-visible', reason: 'gibberish-name' };
    return { ok: true, action: 'allow', reason: '' };
  }

  var MSG = {
    'too-fast': 'Invio troppo rapido. Attendi qualche secondo e riprova.',
    'gibberish-name': 'Il nome inserito non sembra valido. Controllalo, oppure chiamaci al 049.8843484 o scrivici su WhatsApp.'
  };

  // Aggiunge il campo trappola al form (nascosto a persone e screen reader) e legge il valore.
  function attachHoneypot(form) {
    if (!form || form.querySelector('[data-rig-hp]')) return;
    var w = document.createElement('div');
    w.setAttribute('aria-hidden', 'true');
    w.style.cssText = 'position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden';
    var i = document.createElement('input');
    i.type = 'text'; i.name = 'sito_web_2'; i.tabIndex = -1; i.autocomplete = 'off';
    i.setAttribute('data-rig-hp', '1');
    w.appendChild(i); form.appendChild(w);
  }
  function honeypotValue(form) {
    var i = form && form.querySelector('[data-rig-hp]');
    return i ? i.value : '';
  }

  // Punto unico per i moduli: ritorna true se si puo' procedere. Se blocca, mostra il messaggio.
  function gate(form, o) {
    attachHoneypot(form);
    o = o || {}; o.honeypot = honeypotValue(form);
    var r = check(o);
    if (r.ok) return true;
    if (r.action === 'block-visible' && global.alert) global.alert(MSG[r.reason]);
    return false; // drop-silent: nessun messaggio, nessuna mail, nessun salvataggio
  }

  var api = { check: check, gate: gate, attachHoneypot: attachHoneypot, _gibberishName: gibberishName, MESSAGES: MSG };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.RigAntiBot = api;
  // il campo trappola esiste dall'apertura della pagina
  if (typeof document !== 'undefined') {
    var add = function () { [].forEach.call(document.querySelectorAll('form'), attachHoneypot); };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', add); else add();
  }
})(typeof window !== 'undefined' ? window : globalThis);
