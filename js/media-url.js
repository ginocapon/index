/**
 * Risoluzione URL media — GitHub Pages (img/) con fallback Supabase in transizione.
 * Caricare prima di homepage.js / script pagina immobili.
 */
(function (global) {
  'use strict';

  var SITE = 'https://righettoimmobiliare.it';
  var SB_STORAGE = 'https://qwkwkemuabfwvwuqrxlu.supabase.co/storage/v1/object/public/';
  var manifest = null;
  var manifestReady = null;

  function isSupabaseStorageUrl(url) {
    return /supabase\.co\/storage\/v1\//.test(url || '');
  }

  function toSiteUrl(path) {
    if (!path) return '';
    if (path.indexOf('http://') === 0 || path.indexOf('https://') === 0) return path;
    if (path.indexOf('//') === 0) return 'https:' + path;
    return SITE + '/' + String(path).replace(/^\/+/, '');
  }

  function lookupManifest(url) {
    if (!manifest || !url) return '';
    if (manifest[url]) return manifest[url];
    var key = url.split('/storage/v1/object/public/')[1] || '';
    if (key && manifest[key]) return manifest[key];
    var fname = url.split('/').pop().split('?')[0];
    if (fname && manifest[fname]) return manifest[fname];
    return '';
  }

  function loadManifest() {
    if (manifestReady) return manifestReady;
    manifestReady = fetch(SITE + '/data/media-manifest.json?v=1', { cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : {}; })
      .then(function (j) { manifest = j && typeof j === 'object' ? j : {}; })
      .catch(function () { manifest = {}; });
    return manifestReady;
  }

  /**
   * @param {string} url — URL Supabase, path img/… o path storage relativo
   * @param {{width?:number,quality?:number}} opts — ignorato per img/ locali (WebP già ottimizzate)
   */
  function resolveImageUrl(url, opts) {
    if (!url || typeof url !== 'string') return '';
    url = url.trim();
    if (!url) return '';

    if (url.indexOf('data:') === 0) return url;

    var mapped = lookupManifest(url);
    if (mapped) return toSiteUrl(mapped);

    if (url.indexOf('img/') === 0 || url.indexOf('./img/') === 0) {
      return toSiteUrl(url.replace(/^\.\//, ''));
    }

    if (url.indexOf(SITE + '/img/') === 0) return url;

    if (isSupabaseStorageUrl(url)) {
      return url;
    }

    if (url.indexOf('http://') === 0 || url.indexOf('https://') === 0) {
      return url;
    }

    var path = url.replace(/^\/+/, '');
    if (path.indexOf('foto-immobili/') === 0 || path.indexOf('planimetrie/') === 0) {
      mapped = lookupManifest(path);
      if (mapped) return toSiteUrl(mapped);
      return SB_STORAGE + path;
    }

    return url;
  }

  function resolveVideoUrl(url) {
    if (!url || typeof url !== 'string') return '';
    url = url.trim();
    if (!url) return '';
    var mapped = lookupManifest(url);
    if (mapped) return toSiteUrl(mapped);
    if (url.indexOf('img/video/') === 0) return toSiteUrl(url);
    if (url.indexOf(SITE + '/img/video/') === 0) return url;
    if (url.indexOf('http') === 0) return url;
    if (url.indexOf('reels/') === 0 || url.indexOf('blog/') === 0) {
      mapped = lookupManifest('foto-immobili/' + url);
      if (mapped) return toSiteUrl(mapped);
      return SB_STORAGE + 'foto-immobili/' + url;
    }
    return url;
  }

  loadManifest();

  global.RigMedia = {
    SITE: SITE,
    resolveImageUrl: resolveImageUrl,
    resolveVideoUrl: resolveVideoUrl,
    loadManifest: loadManifest
  };
  global.resolveImageUrl = resolveImageUrl;

})(typeof window !== 'undefined' ? window : global);
