/* ══ SUPABASE ══ */
const SB_URL = 'https://qwkwkemuabfwvwuqrxlu.supabase.co';
const SB_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc';
let sb;
function initSB(){try{if(window.supabase&&!sb)sb=window.supabase.createClient(SB_URL,SB_KEY);}catch(e){}}
initSB();



/* ══ LAZY-LOAD TERRITORIO BG ══ */
(function(){
  const tb=document.getElementById('territorio-bg');
  if(!tb) return;
  const io=new IntersectionObserver(function(e){
    if(e[0].isIntersecting){tb.classList.add('loaded');io.disconnect();}
  },{rootMargin:'200px'});
  io.observe(tb);
})();

/* ══ NAVBAR SCROLL ══ */
const nav = document.getElementById('navbar');
window.addEventListener('scroll',()=>{ nav.classList.toggle('scrolled', window.scrollY>60); },{passive:true});

/* ══ HERO BG: animazione parte subito (no delay per LCP) ══ */

/* ══ BURGER MENU — gestito da js/nav-mobile.js ══ */


function toggleQ(btn){
  const item = btn.closest('.cs-q');
  const allOpen = document.querySelectorAll('.cs-q.open');
  allOpen.forEach(el=>{ if(el!==item) el.classList.remove('open'); });
  item.classList.toggle('open');
}
function toggleFaq(btn){
  const item = btn.closest('.faq-item');
  const allOpen = document.querySelectorAll('.faq-item.open');
  allOpen.forEach(el=>{ if(el!==item) el.classList.remove('open'); });
  item.classList.toggle('open');
}

/* ══ COUNT UP ══ */
function countUp(el, target, duration=1800){
  const start = Date.now();
  function tick(){
    const pct = Math.min((Date.now()-start)/duration,1);
    const ease = 1-Math.pow(1-pct,3);
    el.textContent = Math.round(ease*target);
    if(pct<1) requestAnimationFrame(tick);
  }
  tick();
}
const cuObs = new IntersectionObserver(entries=>{
  entries.forEach(e=>{ if(e.isIntersecting){
    e.target.querySelectorAll('.cu').forEach(el=>countUp(el,+el.dataset.t));
    cuObs.unobserve(e.target);
  }});
},{threshold:0.3});
document.querySelectorAll('.cu').forEach(el=>cuObs.observe(el.closest('section')||document.body));

/* ══ REVEAL SCROLL ══ */
const rvObs = new IntersectionObserver(entries=>{
  entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('vis'); rvObs.unobserve(e.target); }});
},{threshold:0.12});
document.querySelectorAll('.rv').forEach(el=>rvObs.observe(el));

/* ══ RISOLVI URL IMMAGINI SUPABASE ══ */
function resolveImageUrl(url, opts) {
  if (!url || typeof url !== 'string') return '';
  url = url.trim();
  if (!url) return '';
  // URL completo (Supabase, http, data) → usa direttamente senza render/image
  if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url;
  // Percorso locale (img/, css/, fonts/) → lascia così com'è
  if (url.startsWith('img/') || url.startsWith('./') || url.startsWith('css/') || url.startsWith('fonts/')) return url;
  // Percorso relativo Supabase Storage → costruisci URL object/public
  var path = url.replace(/^\/+/, '');
  return SB_URL + '/storage/v1/object/public/' + path;
}

/* ══ SEO SLUG PER IMMOBILI ══ */
function generatePropertySlug(d) {
  if (!d) return '';
  const parts = [
    d.tipologia || d.categoria || 'immobile',
    d.tipo_operazione || d.tipo_contratto || 'vendita',
    d.comune || 'padova',
    d.codice || ''
  ];
  return parts.map(p => (p || '').toLowerCase()
    .replace(/[àáâãäå]/g,'a').replace(/[èéêë]/g,'e').replace(/[ìíîï]/g,'i')
    .replace(/[òóôõö]/g,'o').replace(/[ùúûü]/g,'u').replace(/ç/g,'c').replace(/ñ/g,'n')
    .replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')
  ).filter(Boolean).join('-');
}

/* ══ IMMOBILI DA SUPABASE ══ */
async function loadImmobili(){
  if(!sb){ showDemoProps(); return; }
  try{
    // Prima carica gli immobili in evidenza
    const {data:evidenza,error:e1} = await sb.from('immobili').select('*')
      .eq('attivo',true).eq('venduto',false).eq('in_evidenza',true)
      .order('created_at',{ascending:false}).limit(6);
    let risultati = (e1 || !evidenza) ? [] : evidenza;
    // Se meno di 4, riempi con gli ultimi immobili attivi (non gia' inclusi)
    if(risultati.length < 4){
      const ids = risultati.map(r=>r.id);
      const {data:altri} = await sb.from('immobili').select('*')
        .eq('attivo',true).eq('venduto',false).eq('affittato',false)
        .order('created_at',{ascending:false}).limit(8);
      if(altri){
        for(const a of altri){
          if(!ids.includes(a.id)){ risultati.push(a); ids.push(a.id); }
          if(risultati.length>=6) break;
        }
      }
    }
    if(!risultati.length){ showDemoProps(); return; }
    renderProps(risultati);
  }catch(e){ showDemoProps(); }
}

function renderProps(arr){
  const grid = document.getElementById('propsGrid');
  if(!arr||!arr.length){ showDemoProps(); return; }
  grid.innerHTML = arr.slice(0,6).map((p,i)=>{
    const isFirst = i===0;
    const tipo = p.tipo_operazione || p.tipo_contratto || 'vendita';
    const tipClass = tipo==='affitto'?'ta':tipo==='asta'?'te':'tv';
    const tipLabel = tipo==='affitto'?'Affitto':tipo==='asta'?'Asta':'Vendita';
    const price = tipo==='affitto'
      ? `€ ${p.prezzo?.toLocaleString('it-IT')}/mese`
      : `€ ${p.prezzo?.toLocaleString('it-IT')}`;
    const rawImg = p.foto_principale || (p.foto_urls&&p.foto_urls[0]) || (p.foto&&p.foto[0]) || '';
    const imgUrl = resolveImageUrl(rawImg, {width: 600, quality: 75});
    const imgTag = imgUrl
      ? `<img src="${imgUrl}" alt="${p.titolo||'Immobile'}" width="600" height="400" loading="lazy" onerror="this.parentNode.innerHTML='<div class=pi-ph>🏠</div>'">`
      : `<div class="pi-ph">🏠</div>`;
    const propSlug = generatePropertySlug(p);
    return `<a href="immobile?s=${encodeURIComponent(propSlug)}" class="pc">
      <div class="pi">
        ${imgTag}
        <span class="ptag ${tipClass}">${tipLabel}</span>
        ${p.in_evidenza?'<span class="pev">★ Evidenza</span>':''}
        ${p.virtual_tour?'<span class="pvt">360° Tour</span>':''}
      </div>
      <div class="pb">
        <div class="pp">${price}</div>
        <div class="pn">${p.titolo||'Immobile a '+p.comune}</div>
        <div class="ploc">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;min-width:18px;max-width:18px;flex-shrink:0;display:block" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          ${p.comune||'Padova'}${p.indirizzo?' — '+p.indirizzo:''}
        </div>
        <div class="pfeats">
          ${p.superficie?`<span class="pfeat"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;min-width:18px;max-width:18px;flex-shrink:0;display:block" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="1"/></svg>${p.superficie} mq</span>`:''}
          ${p.locali?`<span class="pfeat"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;min-width:18px;max-width:18px;flex-shrink:0;display:block" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>${p.locali} loc.</span>`:''}
          ${p.bagni?`<span class="pfeat"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;min-width:18px;max-width:18px;flex-shrink:0;display:block" aria-hidden="true"><path d="M4 12h16M4 6h16M4 18h16"/></svg>${p.bagni} bagni</span>`:''}
        </div>
      </div>
    </a>`;
  }).join('');
}

function showDemoProps(){
  const DEMO=[
    {id:'d1',tipo_contratto:'vendita',prezzo:295000,titolo:'Appartamento luminoso con balcone',comune:'Padova',superficie:88,locali:3,bagni:1,in_evidenza:true},
    {id:'d2',tipo_contratto:'vendita',prezzo:480000,titolo:'Villa con giardino e garage doppio',comune:'Selvazzano Dentro',superficie:180,locali:5,bagni:2,in_evidenza:false},
    {id:'d3',tipo_contratto:'affitto',prezzo:850,titolo:'Bilocale arredato vicino all\'università',comune:'Padova',superficie:52,locali:2,bagni:1,in_evidenza:false},
    {id:'d4',tipo_contratto:'vendita',prezzo:165000,titolo:'Trilocale ristrutturato centro storico',comune:'Monselice',superficie:74,locali:3,bagni:1,in_evidenza:false},
    {id:'d5',tipo_contratto:'asta',prezzo:112000,titolo:'Appartamento piano terzo con ascensore',comune:'Cittadella',superficie:65,locali:2,bagni:1,in_evidenza:false},
  ];
  renderProps(DEMO);
}

/* ══ STIMA PREZZI ══ */
const PREZZI = {
  'padova centro storico':3500,'padova':2500,'padova arcella':1950,
  'padova guizza':1750,'selvazzano dentro':2100,'albignasego':1950,
  'noventa padovana':2200,'vigonza':1900,'rubano':2000,'limena':1700,
  'cadoneghe':1850,'saccolongo':1650,'cittadella':3200,'abano terme':2100,
  'montegrotto terme':1900,'galzignano terme':1450,'battaglia terme':1350,
  'arquà petrarca':1600,'teolo':1700,'due carrare':1550,
  'camposampiero':1750,'trebaseleghe':1600,'borgoricco':1500,'piombino dese':1450,
  'piove di sacco':1600,'conselve':1350,'este':1100,'monselice':1050,
  'montagnana':950,'default':1200
};
const TIPO_MULT = {
  'attico':1.35,'monolocale':1.10,'bilocale':1.05,'villa singola':1.20,
  'villa bifamiliare':1.10,'villetta':1.08,'duplex':1.05,'appartamento':1.0,
  'trilocale':1.0,'capannone':0.55,'terreno edificabile':3.8,'terreno agricolo':0.05
};
const STATO_MULT = {
  'nuovo':1.25,'ottimo':1.10,'buono':1.0,'discreto':0.90,'da ristrutturare':0.75,'grezzo':0.65
};

function calcolaStima(){
  const comune = document.getElementById('st-comune').value;
  const tipo   = document.getElementById('st-tipo').value;
  const mq     = parseFloat(document.getElementById('st-mq').value);
  const stato  = document.getElementById('st-stato').value;
  if(!comune){alert('Seleziona il comune'); return;}
  if(!mq||mq<5){alert('Inserisci la superficie in mq'); return;}

  const basePrice = PREZZI[comune]||PREZZI['default'];
  const tMult = TIPO_MULT[tipo]||1.0;
  const sMult = STATO_MULT[stato]||1.0;

  /* correzione scala */
  let scaleMult = 1;
  if(tipo.includes('terreno')){ /* terreno usa euro/mq diretti */ }
  else if(mq>200) scaleMult=0.91;
  else if(mq>150) scaleMult=0.96;
  else if(mq<40)  scaleMult=1.10;
  else if(mq<60)  scaleMult=1.05;

  let pricePerMq, totale;
  if(tipo.includes('terreno')){
    pricePerMq = tipo==='terreno agricolo' ? (basePrice*0.003) : (basePrice*1.8);
    totale = mq * pricePerMq;
  } else {
    pricePerMq = basePrice * tMult * sMult * scaleMult;
    totale = mq * pricePerMq;
  }

  const min = Math.round(totale*0.88/1000)*1000;
  const med = Math.round(totale/1000)*1000;
  const max = Math.round(totale*1.12/1000)*1000;
  const fmt = n => '€ '+n.toLocaleString('it-IT');

  document.getElementById('sr-min').textContent=fmt(min);
  document.getElementById('sr-med').textContent=fmt(med);
  document.getElementById('sr-max').textContent=fmt(max);
  document.getElementById('sr-mq-t').textContent=
    tipo.includes('terreno')
      ? `${mq} mq · ${fmt(Math.round(pricePerMq))}/mq`
      : `${mq} mq · circa ${fmt(Math.round(pricePerMq))}/mq`;
  document.getElementById('stima-result').style.display='block';
  document.getElementById('stima-result').scrollIntoView({behavior:'smooth',block:'nearest'});

  loadCorrelati(comune, mq, tipo);
}

async function loadCorrelati(comune, mq, tipo){
  const div=document.getElementById('stima-correlati');
  div.innerHTML='';
  if(!sb) return;
  try{
    const {data} = await sb.from('immobili').select('*')
      .ilike('comune','%'+comune.split(' ')[0]+'%')
      .eq('attivo',true).eq('venduto',false)
      .gte('superficie',mq*0.75).lte('superficie',mq*1.25).limit(3);
    if(!data||!data.length) return;
    div.innerHTML='<div class="sr-lbl" style="margin-top:14px">Immobili simili nel portfolio</div>'+
      data.map(p=>`<a href="immobile?s=${encodeURIComponent(generatePropertySlug(p))}" class="scl">
        <img class="sc-th" src="${p.foto_principale||(p.foto&&p.foto[0])||''}" onerror="this.style.display='none'">
        <div><div class="sc-nm">${p.titolo||p.comune}</div>
        <div class="sc-mt">${p.superficie||''} mq · ${p.comune}</div>
        <div class="sc-pr">€ ${p.prezzo?.toLocaleString('it-IT')}</div></div>
      </a>`).join('');
  }catch(e){}
}

/* ══ FORM CONTATTO ══ */
async function inviaContatto(e){
  e.preventDefault();
  const btn = e.target.querySelector('.btn-send');
  btn.textContent='Invio in corso...'; btn.disabled=true;
  const payload = {
    nome: document.getElementById('cf-nome').value+' '+document.getElementById('cf-cognome').value,
    email: document.getElementById('cf-email').value,
    telefono: document.getElementById('cf-tel').value,
    tipo_richiesta: document.getElementById('cf-interesse').value,
    messaggio: document.getElementById('cf-msg').value,
    sorgente: 'homepage',
    data_richiesta: new Date().toISOString()
  };
  try{
    if(sb){ await sb.from('richieste').insert([payload]); }
    if(typeof SERVIZI_CONFIG !== 'undefined'){
      await SERVIZI_CONFIG.sendNotifica({
        subject: 'Nuovo contatto dal sito: ' + payload.nome,
        html_body: '<b>Nome:</b> ' + payload.nome +
          '<br><b>Email:</b> ' + payload.email +
          '<br><b>Telefono:</b> ' + payload.telefono +
          '<br><b>Interesse:</b> ' + (payload.tipo_richiesta || '-') +
          '<br><b>Messaggio:</b> ' + (payload.messaggio || '-') +
          '<br><b>Sorgente:</b> ' + payload.sorgente,
        reply_to: payload.email
      });
    }
  }catch(er){}
  document.getElementById('cf-ok').style.display='block';
  e.target.querySelectorAll('input,select,textarea').forEach(el=>el.value='');
  btn.textContent='✓ Inviato'; btn.style.background='var(--verde)';
}



/* ══ RICERCA RAPIDA ══ */
let rTabAttivo = 'vendita';
function setRTab(btn, tab) {
  rTabAttivo = tab;
  document.querySelectorAll('.r-tab').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}
function doRicerca() {
  const p = new URLSearchParams();
  p.set('tab', rTabAttivo);
  const tipo   = document.getElementById('r-tipo').value;
  const zona   = document.getElementById('r-zona').value;
  const prezzo = document.getElementById('r-prezzo').value;
  const mq     = document.getElementById('r-mq').value;
  if (tipo)   p.set('tipo', tipo);
  if (zona)   p.set('zona', zona);
  if (prezzo) p.set('prezzo_max', prezzo);
  if (mq)     p.set('mq_min', mq);
  window.location.href = 'immobili?' + p.toString();
}

/* Attendi Supabase (caricato lazy dopo il render) */
function waitSBThen(fn,tries){
  initSB();
  if(sb||tries>20) return fn();
  setTimeout(function(){waitSBThen(fn,(tries||0)+1);},250);
}
/* Mobile: skip caricamento immobili (CTA diretto a /immobili) — Desktop: ritardo 2s */
if(window.innerWidth > 768){
  setTimeout(function(){ waitSBThen(loadImmobili,0); }, 2000);
}

/* ══ MODAL INCARICO VENDITA (solo desktop ≥769px, max 1 volta per sessione) — prima di loadBlogHome così il bind esiste anche se Supabase non fa await ══ */
(function () {
  const SK = 'ri_incarico_vendita_v2';
  const mqDesk = window.matchMedia('(min-width: 769px)');
  let pendingHref = null;
  let rootEl = null;
  let prevFocus = null;
  let keyHandler = null;

  function desk() { return mqDesk.matches; }
  function shown() { return sessionStorage.getItem(SK) === '1'; }
  function mark() { sessionStorage.setItem(SK, '1'); }

  function ensureDom() {
    if (document.getElementById('ri-incarico-root')) {
      rootEl = document.getElementById('ri-incarico-root');
      return;
    }
    document.body.insertAdjacentHTML('beforeend', ''
      + '<div id="ri-incarico-root" class="ri-incarico-root" aria-hidden="true" role="dialog" aria-modal="true" aria-labelledby="ri-incarico-title">'
      + '  <div class="ri-incarico-backdrop" data-ri-incarico-dismiss="1"></div>'
      + '  <div class="ri-incarico-panel">'
      + '    <button type="button" class="ri-incarico-x" data-ri-incarico-dismiss="1" aria-label="Chiudi finestra">&times;</button>'
      + '    <div class="ri-incarico-kicker">Consulenza vendita</div>'
      + '    <h2 id="ri-incarico-title" class="ri-incarico-title">Affidaci l&rsquo;incarico per la vendita nel Padovano</h2>'
      + '    <p class="ri-incarico-lead">Se stai approfondendo le nostre guide, &egrave; il momento giusto per un confronto professionale senza impegno.</p>'
      + '    <p class="ri-incarico-body">Un unico referente segue l&rsquo;immobile dall&rsquo;analisi di mercato alla strategia di valorizzazione e alla trattativa. Onorari e modalit&agrave; di incarico chiari fin dal primo incontro in agenzia.</p>'
      + '    <div class="ri-incarico-actions">'
      + '      <a href="contatti" class="ri-incarico-btn ri-incarico-btn--pri" id="ri-incarico-cta">Richiedi consulenza per la vendita</a>'
      + '      <button type="button" class="ri-incarico-btn ri-incarico-btn--sec ri-incarico-foc" id="ri-incarico-secondary"></button>'
      + '    </div>'
      + '    <p class="ri-incarico-foot">Puoi chiudere in qualsiasi momento (anche con Esc). Questo messaggio non comparir&agrave; di nuovo in questa sessione.</p>'
      + '  </div>'
      + '</div>');
    rootEl = document.getElementById('ri-incarico-root');
    const sec = document.getElementById('ri-incarico-secondary');
    const cta = document.getElementById('ri-incarico-cta');
    rootEl.addEventListener('click', function (e) {
      if (!e.target.closest('[data-ri-incarico-dismiss]')) return;
      closeModal(pendingHref || null);
    });
    if (sec) sec.addEventListener('click', function () { closeModal(pendingHref || null); });
    if (cta) cta.addEventListener('click', function (e) {
      e.preventDefault();
      closeModal(null);
      window.location.href = 'contatti';
    });
  }

  function onKey(e) {
    if (e.key === 'Escape' && rootEl && rootEl.classList.contains('is-open')) {
      e.preventDefault();
      closeModal(pendingHref || null);
    }
  }

  function openModal(href) {
    if (!desk() || shown()) return false;
    mark();
    pendingHref = href || null;
    ensureDom();
    if (!rootEl) return false;
    const sec = document.getElementById('ri-incarico-secondary');
    if (sec) sec.textContent = pendingHref ? 'Continua a leggere la guida' : 'Chiudi';
    rootEl.classList.add('is-open');
    rootEl.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    prevFocus = document.activeElement;
    keyHandler = onKey;
    document.addEventListener('keydown', keyHandler);
    const fb = rootEl.querySelector('.ri-incarico-foc');
    if (fb && typeof fb.focus === 'function') setTimeout(function () { fb.focus(); }, 60);
    return true;
  }

  function closeModal(navHref) {
    if (!rootEl) return;
    rootEl.classList.remove('is-open');
    rootEl.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (keyHandler) document.removeEventListener('keydown', keyHandler);
    keyHandler = null;
    const h = navHref;
    pendingHref = null;
    if (prevFocus && typeof prevFocus.focus === 'function') try { prevFocus.focus(); } catch (x) {}
    prevFocus = null;
    if (h) window.location.href = h;
  }

  function bindGrid(gridEl) {
    if (!gridEl || gridEl.dataset.riIncaricoBound === '1') return;
    gridEl.dataset.riIncaricoBound = '1';
    gridEl.addEventListener('click', function (ev) {
      const card = ev.target.closest('.blog-card');
      if (!card || !gridEl.contains(card)) return;
      const href = card.getAttribute('data-card-href');
      if (!href) return;
      if (!desk() || shown()) {
        window.location.href = href;
        return;
      }
      ev.preventDefault();
      openModal(href);
    });
    gridEl.addEventListener('keydown', function (ev) {
      if (ev.key !== 'Enter' && ev.key !== ' ') return;
      const card = ev.target.closest('.blog-card');
      if (!card || !gridEl.contains(card)) return;
      const href = card.getAttribute('data-card-href');
      if (!href) return;
      ev.preventDefault();
      if (!desk() || shown()) {
        window.location.href = href;
        return;
      }
      openModal(href);
    });
  }

  const blogSec = document.getElementById('blog');
  if (blogSec) {
    const io = new IntersectionObserver(function (ents) {
      if (!ents[0] || !ents[0].isIntersecting) return;
      if (!desk() || shown()) return;
      io.disconnect();
      openModal(null);
    }, { threshold: 0.12, rootMargin: '0px 0px 0px 0px' });
    io.observe(blogSec);
  }

  window._rigBindIncaricoGrid = bindGrid;
})();

// ══ BLOG DINAMICO HOMEPAGE ══
function generateSlug(titolo) {
  let s = String(titolo || '')
    .replace(/\u2019/g, "'").replace(/\u2018/g, "'").replace(/\u2013/g, '-').replace(/\u2014/g, '-')
    .toLowerCase()
    .replace(/[àáâãäå]/g,'a').replace(/[èéêë]/g,'e').replace(/[ìíîï]/g,'i')
    .replace(/[òóôõö]/g,'o').replace(/[ùúûü]/g,'u').replace(/[ç]/g,'c')
    .replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,80).replace(/-+$/g,'');
  if (!s.endsWith('-padova') && !s.endsWith('padova')) s += '-padova';
  return s;
}

(async function loadBlogHome() {
  const grid = document.getElementById('blogGridHome');
  if (!grid) return;
  // Mappa fallback per articoli statici (immagine + url dedicato)
  const staticMap = {
    'righetto immobiliare: bilancio 2025, valori e soluzioni affitto nel 2026': { img: 'img/team/titolari.webp', url: 'blog-righetto-bilancio-2025-soluzioni-affitto-2026' },
    'guida ai quartieri di padova: dove comprare casa nel 2026': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-quartieri-padova-2026' },
    'affitto studenti padova 2026: zone, prezzi e guida completa': { img: 'img/foto-servizi/contratti-di-locazione-padova.webp', url: 'blog-affitto-studenti-padova' },
    'mercato immobiliare padova 2026: prezzi, tendenze e previsioni': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-mercato-immobiliare-padova-2026' },
    'conviene comprare casa a padova o restare in affitto? analisi su 20 anni': { img: 'img/blog/comprare-affittare-padova.webp', url: 'blog-comprare-affittare-padova' },
    'case in vendita padova 2026: prezzi, zone migliori e guida completa': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-case-vendita-padova' },
    'mutuo prima casa a padova: guida completa 2026': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-mutuo-prima-casa-padova' },
    "ca' marcello mestre: riqualificazione e investimento nel veneto": { img: 'img/blog/ca-marcello-hero.webp', url: 'articolo-riqualificazione' },
    "l'impegno quotidiano di un'agenzia immobiliare: tra burocrazia e incertezza mutui": { img: 'img/blog/ufficio-righetto-immobiliare.webp', url: 'blog-impegno-quotidiano-agenzia-immobiliare' },
    'appartamento nuova costruzione limena: 101 mq con giardino 310 mq in classe a4': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-appartamento-nuova-costruzione-limena' },
    'comprare casa a padova nel 2026: guida definitiva passo dopo passo': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-comprare-casa-padova-guida-2026' },
    'quanto costa vendere casa a padova nel 2026? costi, tasse e tempi reali': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-costi-vendere-casa-padova-2026' },
    'home staging padova: come vendere casa prima e meglio': { img: 'img/blog/home-staging.webp', url: 'blog-home-staging-padova' },
    'vendere casa a padova: 7 errori costosi da evitare': { img: 'img/team/titolari.webp', url: 'vendere-casa-padova-errori' },
    'documenti per vendere casa nel 2026: lista completa e guida pratica': { img: 'img/foto-servizi/gestione-preliminari-padova.webp', url: 'blog-documenti-vendita-casa' },
    'tasse vendita casa 2026: plusvalenza, imposte e guida fiscale completa': { img: 'img/foto-servizi/attivazione-utenze-e-servizi-padova.webp', url: 'blog-tasse-vendita-casa' },
    'casa ereditata a padova: cosa fare, tasse e come venderla nel 2026': { img: 'img/foto-servizi/gestioni-immobili-padova.webp', url: 'blog-successione-immobiliare-padova' },
    'agevolazioni prima casa 2026: bonus, requisiti e come ottenerli': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-agevolazioni-prima-casa-2026' },
    'investire nel mercato immobiliare a padova nel 2026: guida completa': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-investire-immobiliare-padova' },
    'contratto di affitto a padova 2026: canone concordato e guida completa': { img: 'img/foto-servizi/contratti-di-locazione-padova.webp', url: 'blog-contratto-affitto-padova' },
    'rendimento affitto padova 2026: calcolo e analisi per quartiere': { img: 'img/foto-servizi/contratti-di-locazione-padova.webp', url: 'blog-rendimento-affitto-padova' },
    'tempi vendita casa padova 2026: quanto ci vuole davvero?': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-tempi-vendita-casa-padova' },
    'servizi e infrastrutture nelle zone di padova — guida interattiva': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-servizi-infrastrutture-padova' },
    'scuole e istruzione a padova per zone — guida interattiva': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-scuole-istruzione-padova' },
    'trasporti e mobilita\' a padova per zone — guida interattiva': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-trasporti-mobilita-padova' },
    'direttiva case green ue 2024: cosa cambia per le case a limena e padova': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-direttiva-case-green-limena-padova' },
    'vendere casa a padova nel 2026: 7 strategie per massimizzare il prezzo': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-vendita-immobiliare-padova-strategie-2026' },
    'compravendite padova 2026: l\'anno record con 800.000 transazioni in italia': { img: 'img/foto-servizi/gestione-preliminari-padova.webp', url: 'blog-compravendite-padova-record-2026' },
    'prezzi case padova 2026 zona per zona: mappa completa e previsioni': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-prezzi-case-padova-zona-2026' },
    'affitti padova 2026: canoni in crescita del +8%, zone e previsioni': { img: 'img/foto-servizi/contratti-di-locazione-padova.webp', url: 'blog-affitti-padova-canoni-2026' },
    'affitto breve a padova 2026: rendimenti, regole e opportunita\'': { img: 'img/foto-servizi/gestioni-immobili-padova.webp', url: 'blog-affitto-breve-padova-2026' },
    'affitti padova: perche\' la domanda supera l\'offerta nel 2026': { img: 'img/foto-servizi/attivazione-utenze-e-servizi-padova.webp', url: 'blog-squilibrio-domanda-offerta-affitti-padova' },
    'crisi immobiliare 2026: cosa succede a padova tra prezzi e compravendite': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-crisi-immobiliare-padova-2026' },
    'bolla immobiliare a padova nel 2026? analisi dei rischi reali': { img: 'img/foto-servizi/gestione-preliminari-padova.webp', url: 'blog-bolla-immobiliare-padova-2026' },
    'emergenza casa padova 2026: dati, cause e possibili soluzioni': { img: 'img/foto-servizi/attivazione-utenze-e-servizi-padova.webp', url: 'blog-emergenza-abitativa-padova-2026' },
    'mutui casa a padova 2026: tassi aggiornati e migliori offerte': { img: 'img/foto-servizi/gestione-preliminari-padova.webp', url: 'blog-mutui-casa-padova-2026' },
    'surroga mutuo 2026: quando conviene e come risparmiare a padova': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-surroga-mutuo-padova-2026' },
    'mutuo tasso fisso o variabile nel 2026? guida alla scelta a padova': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-mutuo-fisso-variabile-padova-2026' },
    'caparra confirmatoria: guida completa per chi compra o vende casa a padova': { img: 'img/foto-servizi/gestione-preliminari-padova.webp', url: 'blog-caparra-confirmatoria-padova' },
    'mercato immobiliare limena 2026: guida omi, territorio e valori': { img: 'img/blog/limena-oratorio-beata-vergine-rosario.jpg', url: 'blog-mercato-immobiliare-limena-2026' },
    'mercato immobiliare sacro cuore padova: guida omi zona d6 e valori 2026': { img: 'img/blog/padova-arcella-gesu-buon-pastore.jpg', url: 'blog-mercato-sacrocuore-padova-omi-2026' },
    'immobili centro storico padova 2026: prezzi, rendimenti e analisi': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-mercato-immobiliare-padova-centro-2026' },
    'limena o centro padova? dove comprare casa nel 2026: confronto dati': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-limena-vs-padova-centro-dove-comprare-2026' },
    'mutui a tasso fisso nel padovano: dati banca d\'italia e orientamento 2026': { img: 'img/blog/blog-mutui-coppia-giovani-padova.webp', url: 'blog-mutui-tasso-fisso-bancaitalia-padova-2026' },
    'quotazioni e locazioni a padova: omi e monitor istat 2026': { img: 'img/blog/blog-omi-professionisti-ufficio.webp', url: 'blog-quotazioni-locazioni-omi-istat-padova-2026' },
    'compravendite nel veneto e sulla cintura di padova: lettura dei dati 2026': { img: 'img/blog/comprare-affittare-padova.webp', url: 'blog-compravendite-veneto-cintura-padova-2026' },
    'imposte di registro e ipotecarie nella compravendita: guida per il padovano': { img: 'img/blog/tasse-vendita-casa.webp', url: 'blog-imposte-registro-catasto-compravendita-padova-2026' },
    'dal prezzo alla proposta: percorso operativo per vendere nel padovano (2026)': { img: 'img/blog/home-staging.webp', url: 'blog-percorso-vendita-immobile-padova-2026' },
    'geopolitica, energia e tassi: effetti sul mercato immobiliare e cautele pratiche': { img: 'img/blog/blog-geopolitica-fiore-carrarmato.webp', url: 'blog-immobiliare-geopolitica-energia-tassi-2026' },
    'mercato immobiliare a piazzola sul brenta nel 2026: come leggere omi e contesto provinciale': { img: 'img/blog/blog-piazzola-brenta-mercato-2026.webp', url: 'blog-mercato-immobiliare-piazzola-sul-brenta-2026' },
    'vigonza e rubano: guida all\'acquisto nella cintura del capoluogo euganeo (2026)': { img: 'img/blog/blog-vigonza-rubano-cintura-2026.webp', url: 'blog-vigonza-rubano-comprare-casa-cintura-2026' },
    'planimetria catastale e compravendita nel padovano: controlli prima del rogito (2026)': { img: 'img/blog/blog-planimetria-catasto-padova-2026.webp', url: 'blog-planimetria-catastale-compravendita-padova-2026' },
    'permuta immobiliare nel padovano: come funziona e quali cautele adottare (2026)': { img: 'img/blog/blog-permuta-immobiliare-padova-2026.webp', url: 'blog-permuta-immobiliare-padova-2026' },
    'ape e prestazione energetica nell\'acquisto di casa nel padovano: cosa verificare nel 2026': { img: 'img/blog/blog-ape-acquisto-padova-2026.webp', url: 'blog-ape-prestazione-energetica-acquisto-padova-2026' }
  };
  // Articoli statici (sempre presenti)
  const articoliStatici = [
    { titolo: 'Mercato immobiliare a Piazzola sul Brenta nel 2026: come leggere OMI e contesto provinciale', categoria: 'Mercato locale', data: '2026-04-14', stato: 'pubblicato', immagine_copertina: 'img/blog/blog-piazzola-brenta-mercato-2026.webp', url_statico: 'blog-mercato-immobiliare-piazzola-sul-brenta-2026' },
    { titolo: 'Vigonza e Rubano: guida all\'acquisto nella cintura del capoluogo euganeo (2026)', categoria: 'Consigli acquisto', data: '2026-04-14', stato: 'pubblicato', immagine_copertina: 'img/blog/blog-vigonza-rubano-cintura-2026.webp', url_statico: 'blog-vigonza-rubano-comprare-casa-cintura-2026' },
    { titolo: 'Planimetria catastale e compravendita nel Padovano: controlli prima del rogito (2026)', categoria: 'Normativa', data: '2026-04-14', stato: 'pubblicato', immagine_copertina: 'img/blog/blog-planimetria-catasto-padova-2026.webp', url_statico: 'blog-planimetria-catastale-compravendita-padova-2026' },
    { titolo: 'Permuta immobiliare nel Padovano: come funziona e quali cautele adottare (2026)', categoria: 'Consigli acquisto', data: '2026-04-14', stato: 'pubblicato', immagine_copertina: 'img/blog/blog-permuta-immobiliare-padova-2026.webp', url_statico: 'blog-permuta-immobiliare-padova-2026' },
    { titolo: 'APE e prestazione energetica nell\'acquisto di casa nel Padovano: cosa verificare nel 2026', categoria: 'Normativa', data: '2026-04-14', stato: 'pubblicato', immagine_copertina: 'img/blog/blog-ape-acquisto-padova-2026.webp', url_statico: 'blog-ape-prestazione-energetica-acquisto-padova-2026' },
    { titolo: 'Righetto Immobiliare: bilancio 2025, valori e soluzioni affitto nel 2026', categoria: 'Vita d\'Agenzia', data: '2026-04-10', stato: 'pubblicato', immagine_copertina: 'img/team/titolari.webp', url_statico: 'blog-righetto-bilancio-2025-soluzioni-affitto-2026' },
    { titolo: 'Home Staging Padova: Come Vendere Casa Prima e Meglio', categoria: 'Guida alla vendita', data: '2026-03-06', stato: 'pubblicato', immagine_copertina: 'img/blog/home-staging.webp', url_statico: 'blog-home-staging-padova' },
    { titolo: 'Vendere Casa a Padova: 7 Errori Costosi da Evitare', categoria: 'Guida alla vendita', data: '2026-03-06', stato: 'pubblicato', immagine_copertina: 'img/team/titolari.webp', url_statico: 'vendere-casa-padova-errori' },
    { titolo: 'Comprare Casa a Padova nel 2026: Guida Definitiva Passo dopo Passo', categoria: 'Consigli acquisto', data: '2026-03-04', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-comprare-casa-padova-guida-2026' },
    { titolo: 'Quanto Costa Vendere Casa a Padova nel 2026? Costi, Tasse e Tempi Reali', categoria: 'Guida alla vendita', data: '2026-03-04', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url_statico: 'blog-costi-vendere-casa-padova-2026' },
    { titolo: "L'impegno quotidiano di un'agenzia immobiliare: tra burocrazia e incertezza mutui", categoria: "Vita d'Agenzia", data: '2026-03-03', stato: 'pubblicato', immagine_copertina: 'img/blog/ufficio-righetto-immobiliare.webp', url_statico: 'blog-impegno-quotidiano-agenzia-immobiliare' },
    { titolo: 'Appartamento Nuova Costruzione Limena: 101 mq con Giardino 310 mq in Classe A4', categoria: 'Nuove Costruzioni', data: '2026-03-03', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-appartamento-nuova-costruzione-limena' },
    { titolo: 'Guida ai Quartieri di Padova: Dove Comprare Casa nel 2026', categoria: 'Mercato locale', data: '2026-03-02', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-quartieri-padova-2026' },
    { titolo: 'Affitto Studenti Padova 2026: Zone, Prezzi e Guida Completa', categoria: 'Affitti', data: '2026-03-02', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/contratti-di-locazione-padova.webp', url_statico: 'blog-affitto-studenti-padova' },
    { titolo: 'Mercato Immobiliare Padova 2026: Prezzi, Tendenze e Previsioni', categoria: 'Mercato locale', data: '2026-03-02', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url_statico: 'blog-mercato-immobiliare-padova-2026' },
    { titolo: 'Conviene comprare casa a Padova o restare in affitto? Analisi su 20 anni', categoria: 'Consigli acquisto', data: '2026-03-02', stato: 'pubblicato', immagine_copertina: 'img/blog/comprare-affittare-padova.webp', url_statico: 'blog-comprare-affittare-padova' },
    { titolo: 'Case in Vendita Padova 2026: Prezzi, Zone Migliori e Guida Completa', categoria: 'Mercato locale', data: '2026-03-01', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-case-vendita-padova' },
    { titolo: 'Documenti per Vendere Casa nel 2026: Lista Completa e Guida Pratica', categoria: 'Guida alla vendita', data: '2026-03-07', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/gestione-preliminari-padova.webp', url_statico: 'blog-documenti-vendita-casa' },
    { titolo: 'Tasse Vendita Casa 2026: Plusvalenza, Imposte e Guida Fiscale Completa', categoria: 'Fisco', data: '2026-03-07', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/attivazione-utenze-e-servizi-padova.webp', url_statico: 'blog-tasse-vendita-casa' },
    { titolo: 'Casa Ereditata a Padova: Cosa Fare, Tasse e Come Venderla nel 2026', categoria: 'Normativa', data: '2026-03-07', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/gestioni-immobili-padova.webp', url_statico: 'blog-successione-immobiliare-padova' },
    { titolo: 'Agevolazioni Prima Casa 2026: Bonus, Requisiti e Come Ottenerli', categoria: 'Fisco', data: '2026-03-07', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-agevolazioni-prima-casa-2026' },
    { titolo: 'Investire nel Mercato Immobiliare a Padova nel 2026: Guida Completa', categoria: 'Consigli acquisto', data: '2026-03-07', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url_statico: 'blog-investire-immobiliare-padova' },
    { titolo: 'Contratto di Affitto a Padova 2026: Canone Concordato e Guida Completa', categoria: 'Affitti', data: '2026-03-07', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/contratti-di-locazione-padova.webp', url_statico: 'blog-contratto-affitto-padova' },
    { titolo: 'Rendimento Affitto Padova 2026: Calcolo e Analisi per Quartiere', categoria: 'Affitti', data: '2026-03-07', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/contratti-di-locazione-padova.webp', url_statico: 'blog-rendimento-affitto-padova' },
    { titolo: 'Mutuo Prima Casa a Padova: Guida Completa 2026', categoria: 'Consigli acquisto', data: '2026-03-01', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url_statico: 'blog-mutuo-prima-casa-padova' },
    { titolo: "Ca' Marcello Mestre: Hub Turistico da 70 Milioni", categoria: 'Investimenti', data: '2026-02-24', stato: 'pubblicato', immagine_copertina: 'img/blog/ca-marcello-hero.webp', url_statico: 'blog-ca-marcello-mestre' },
    { titolo: 'Tempi Vendita Casa Padova 2026: Quanto Ci Vuole Davvero?', categoria: 'Guida alla vendita', data: '2026-03-08', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-tempi-vendita-casa-padova' },
    { titolo: 'Servizi e Infrastrutture nelle Zone di Padova — Guida Interattiva', categoria: 'Mercato locale', data: '2026-03-11', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-servizi-infrastrutture-padova' },
    { titolo: 'Scuole e Istruzione a Padova per Zone — Guida Interattiva', categoria: 'Mercato locale', data: '2026-03-11', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-scuole-istruzione-padova' },
    { titolo: 'Trasporti e Mobilita\' a Padova per Zone — Guida Interattiva', categoria: 'Mercato locale', data: '2026-03-11', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-trasporti-mobilita-padova' },
    { titolo: 'Direttiva Case Green UE 2024: Cosa Cambia per le Case a Limena e Padova', categoria: 'Normativa', data: '2026-03-11', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url_statico: 'blog-direttiva-case-green-limena-padova' },
    { titolo: 'Vendere Casa a Padova nel 2026: 7 Strategie per Massimizzare il Prezzo', categoria: 'Guida alla vendita', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-vendita-immobiliare-padova-strategie-2026' },
    { titolo: 'Compravendite Padova 2026: l\'Anno Record con 800.000 Transazioni in Italia', categoria: 'Mercato locale', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/gestione-preliminari-padova.webp', url_statico: 'blog-compravendite-padova-record-2026' },
    { titolo: 'Prezzi Case Padova 2026 Zona per Zona: Mappa Completa e Previsioni', categoria: 'Mercato locale', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url_statico: 'blog-prezzi-case-padova-zona-2026' },
    { titolo: 'Affitti Padova 2026: Canoni in Crescita del +8%, Zone e Previsioni', categoria: 'Affitti', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/contratti-di-locazione-padova.webp', url_statico: 'blog-affitti-padova-canoni-2026' },
    { titolo: 'Affitto Breve a Padova 2026: Rendimenti, Regole e Opportunita\'', categoria: 'Affitti', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/gestioni-immobili-padova.webp', url_statico: 'blog-affitto-breve-padova-2026' },
    { titolo: 'Affitti Padova: Perche\' la Domanda Supera l\'Offerta nel 2026', categoria: 'Affitti', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/attivazione-utenze-e-servizi-padova.webp', url_statico: 'blog-squilibrio-domanda-offerta-affitti-padova' },
    { titolo: 'Crisi Immobiliare 2026: Cosa Succede a Padova tra Prezzi e Compravendite', categoria: 'Mercato locale', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url_statico: 'blog-crisi-immobiliare-padova-2026' },
    { titolo: 'Bolla Immobiliare a Padova nel 2026? Analisi dei Rischi Reali', categoria: 'Mercato locale', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/gestione-preliminari-padova.webp', url_statico: 'blog-bolla-immobiliare-padova-2026' },
    { titolo: 'Emergenza Casa Padova 2026: Dati, Cause e Possibili Soluzioni', categoria: 'Normativa', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/attivazione-utenze-e-servizi-padova.webp', url_statico: 'blog-emergenza-abitativa-padova-2026' },
    { titolo: 'Mutui Casa a Padova 2026: Tassi Aggiornati e Migliori Offerte', categoria: 'Consigli acquisto', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/gestione-preliminari-padova.webp', url_statico: 'blog-mutui-casa-padova-2026' },
    { titolo: 'Surroga Mutuo 2026: Quando Conviene e Come Risparmiare a Padova', categoria: 'Consigli acquisto', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url_statico: 'blog-surroga-mutuo-padova-2026' },
    { titolo: 'Mutuo Tasso Fisso o Variabile nel 2026? Guida alla Scelta a Padova', categoria: 'Consigli acquisto', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-mutuo-fisso-variabile-padova-2026' },
    { titolo: 'Caparra Confirmatoria: Guida Completa per Chi Compra o Vende Casa a Padova', categoria: 'Normativa', data: '2026-03-14', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/gestione-preliminari-padova.webp', url_statico: 'blog-caparra-confirmatoria-padova' },
    { titolo: 'Mercato Immobiliare Limena 2026: Guida OMI, Territorio e Valori', categoria: 'Mercato locale', data: '2026-04-01', stato: 'pubblicato', immagine_copertina: 'img/blog/limena-oratorio-beata-vergine-rosario.jpg', url_statico: 'blog-mercato-immobiliare-limena-2026' },
    { titolo: 'Mercato Immobiliare Sacro Cuore Padova: Guida OMI Zona D6 e Valori 2026', categoria: 'Mercato locale', data: '2026-04-01', stato: 'pubblicato', immagine_copertina: 'img/blog/padova-arcella-gesu-buon-pastore.jpg', url_statico: 'blog-mercato-sacrocuore-padova-omi-2026' },
    { titolo: 'Immobili Centro Storico Padova 2026: Prezzi, Rendimenti e Analisi', categoria: 'Mercato locale', data: '2026-03-16', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-mercato-immobiliare-padova-centro-2026' },
    { titolo: 'Limena o Centro Padova? Dove Comprare Casa nel 2026: Confronto Dati', categoria: 'Consigli acquisto', data: '2026-03-16', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url_statico: 'blog-limena-vs-padova-centro-dove-comprare-2026' },
    { titolo: 'Mutui a tasso fisso nel Padovano: dati Banca d\'Italia e orientamento 2026', categoria: 'Finanziamenti', data: '2026-04-10', stato: 'pubblicato', immagine_copertina: 'img/blog/blog-mutui-coppia-giovani-padova.webp', url_statico: 'blog-mutui-tasso-fisso-bancaitalia-padova-2026' },
    { titolo: 'Quotazioni e locazioni a Padova: OMI e monitor ISTAT 2026', categoria: 'Mercato locale', data: '2026-04-10', stato: 'pubblicato', immagine_copertina: 'img/blog/blog-omi-professionisti-ufficio.webp', url_statico: 'blog-quotazioni-locazioni-omi-istat-padova-2026' },
    { titolo: 'Compravendite nel Veneto e sulla cintura di Padova: lettura dei dati 2026', categoria: 'Mercato locale', data: '2026-04-10', stato: 'pubblicato', immagine_copertina: 'img/blog/comprare-affittare-padova.webp', url_statico: 'blog-compravendite-veneto-cintura-padova-2026' },
    { titolo: 'Imposte di registro e ipotecarie nella compravendita: guida per il Padovano', categoria: 'Fisco', data: '2026-04-10', stato: 'pubblicato', immagine_copertina: 'img/blog/tasse-vendita-casa.webp', url_statico: 'blog-imposte-registro-catasto-compravendita-padova-2026' },
    { titolo: 'Dal prezzo alla proposta: percorso operativo per vendere nel Padovano (2026)', categoria: 'Guida alla vendita', data: '2026-04-10', stato: 'pubblicato', immagine_copertina: 'img/blog/home-staging.webp', url_statico: 'blog-percorso-vendita-immobile-padova-2026' },
    { titolo: 'Geopolitica, energia e tassi: effetti sul mercato immobiliare e cautele pratiche', categoria: 'Mercato locale', data: '2026-04-10', stato: 'pubblicato', immagine_copertina: 'img/blog/blog-geopolitica-fiore-carrarmato.webp', url_statico: 'blog-immobiliare-geopolitica-energia-tassi-2026' }
  ];
  // Carica da Supabase e merge con statici
  let articles = [];
  try {
    if (sb) {
      const { data, error } = await sb.from('blog').select('*').eq('stato','pubblicato').order('data',{ascending:false});
      if (!error && data) articles = data;
    }
  } catch(e) {}
  if (!articles.length) {
    try { articles = JSON.parse(localStorage.getItem('rig_blog_articles')||'[]').filter(a=>a.stato==='pubblicato'); } catch(e) { articles = []; }
  }
  // Merge: aggiungi statici non presenti in Supabase
  const titoliEsistenti = new Set(articles.map(a => (a.titolo || '').toLowerCase()));
  articoliStatici.forEach(s => {
    if (!titoliEsistenti.has(s.titolo.toLowerCase())) articles.push(s);
  });
  // Arricchisci con immagini/url statici se mancanti
  articles.forEach(a => {
    const key = (a.titolo || '').toLowerCase();
    const s = staticMap[key];
    if (s) {
      if (!a.immagine_copertina) a.immagine_copertina = s.img;
      if (!a.url_statico) a.url_statico = s.url;
    }
  });
  // Ordina per data e prendi i 3 piu' recenti
  articles.sort((a,b) => new Date(b.data) - new Date(a.data));
  articles = articles.slice(0, 3);
  function extractImg(a) {
    if (a.immagine_copertina) return resolveImageUrl(a.immagine_copertina);
    if (!a.contenuto) return '';
    const m = a.contenuto.match(/<img[^>]+src=["']([^"']+)["']/i);
    if (m) return resolveImageUrl(m[1]);
    const j = a.contenuto.match(/"image"\s*:\s*\[?\s*"(https?:\/\/[^"]+)"/i);
    if (j) return resolveImageUrl(j[1]);
    return '';
  }
  function fmtMese(d) { return d ? new Date(d).toLocaleDateString('it-IT',{month:'long',year:'numeric'}) : ''; }
  function escAttr(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  grid.innerHTML = articles.map((a,i) => {
    const img = extractImg(a);
    const slug = generateSlug(a.titolo);
    const href = a.url_statico || ('blog-articolo?s=' + encodeURIComponent(slug));
    return '<div class="blog-card rv d'+(i+1)+'" data-card-href="'+escAttr(href)+'" role="link" tabindex="0">'
      + '<div class="blog-cover"'+(img?' style="background:url('+img+') center/cover;font-size:0"':'')+'>'+(img?'':a.emoji||'📝')+'</div>'
      + '<div class="blog-body"><div class="blog-cat">'+((a.categoria||'Blog').replace(/</g,'&lt;'))+'</div>'
      + '<h3 class="blog-title">'+((a.titolo||'').replace(/</g,'&lt;'))+'</h3>'
      + '<div class="blog-date">'+fmtMese(a.data)+'</div></div></div>';
  }).join('');
  // Attiva animazione reveal sulle card appena create
  grid.querySelectorAll('.rv').forEach(el => { if(typeof rvObs!=='undefined') rvObs.observe(el); else el.classList.add('vis'); });
  if (typeof window._rigBindIncaricoGrid === 'function') window._rigBindIncaricoGrid(grid);
})();
