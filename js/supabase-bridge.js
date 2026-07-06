/* Espone window.supabase dopo js/vendor/supabase.min.js (var supabase globale UMD). */
(function (w) {
  'use strict';

  function lib() {
    if (w.supabase && typeof w.supabase.createClient === 'function') return w.supabase;
    try {
      if (typeof supabase !== 'undefined' && supabase && typeof supabase.createClient === 'function') {
        w.supabase = supabase;
        return supabase;
      }
    } catch (e) { /* strict / cross-frame */ }
    return null;
  }

  w.rigSupabaseLib = lib;

  w.rigWaitSupabase = function (fn, opts) {
    opts = opts || {};
    var tries = 0;
    var max = opts.maxTries || 80;
    var ms = opts.interval || 100;

    function tick() {
      var l = lib();
      if (l) return fn(l);
      if (++tries >= max) {
        if (typeof opts.onFail === 'function') opts.onFail();
        return;
      }
      setTimeout(tick, ms);
    }
    tick();
  };
})(window);
