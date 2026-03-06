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
window.addEventListener('scroll',()=>{ nav.classList.toggle('scrolled', window.scrollY>60); });

/* ══ HERO BG: avvia animazione dopo LCP ══ */
requestAnimationFrame(()=>{const hb=document.getElementById('hero-bg');if(hb)hb.classList.add('loaded');});

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
function resolveImageUrl(url) {
  if (!url || typeof url !== 'string') return '';
  url = url.trim();
  if (!url) return '';
  // Già URL completo
  if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) return url;
  // Percorso locale (img/, css/, fonts/) → lascia così com'è
  if (url.startsWith('img/') || url.startsWith('./') || url.startsWith('css/') || url.startsWith('fonts/')) return url;
  // Percorso relativo Supabase Storage → costruisci URL pubblico
  return SB_URL + '/storage/v1/object/public/' + url.replace(/^\/+/, '');
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
    const imgUrl = resolveImageUrl(rawImg);
    const imgTag = imgUrl
      ? `<img src="${imgUrl}" alt="${p.titolo||'Immobile'}" loading="lazy" onerror="this.parentNode.innerHTML='<div class=pi-ph>🏠</div>'">`
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

/* Attendi Supabase se defer non è ancora pronto */
function waitSBThen(fn,tries){
  initSB();
  if(sb||tries>8) return fn();
  setTimeout(function(){waitSBThen(fn,tries+1);},150);
}
waitSBThen(loadImmobili,0);

// ══ BLOG DINAMICO HOMEPAGE ══
function generateSlug(titolo) {
  let s = (titolo || '').toLowerCase()
    .replace(/[àáâãäå]/g,'a').replace(/[èéêë]/g,'e').replace(/[ìíîï]/g,'i')
    .replace(/[òóôõö]/g,'o').replace(/[ùúûü]/g,'u').replace(/[ç]/g,'c')
    .replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,80);
  if (!s.endsWith('-padova') && !s.endsWith('padova')) s += '-padova';
  return s;
}

(async function loadBlogHome() {
  const grid = document.getElementById('blogGridHome');
  if (!grid) return;
  // Mappa fallback per articoli statici (immagine + url dedicato)
  const staticMap = {
    'guida ai quartieri di padova: dove comprare casa nel 2026': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-quartieri-padova-2026' },
    'affitto studenti padova 2026: zone, prezzi e guida completa': { img: 'img/foto-servizi/contratti-di-locazione-padova.webp', url: 'blog-affitto-studenti-padova' },
    'mercato immobiliare padova 2026: prezzi, tendenze e previsioni': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-mercato-immobiliare-padova-2026' },
    'conviene comprare casa a padova o restare in affitto? analisi su 20 anni': { img: 'img/blog/comprare-affittare-padova.webp', url: 'blog-comprare-affittare-padova' },
    'case in vendita padova 2026: prezzi, zone migliori e guida completa': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-case-vendita-padova' },
    'mutuo prima casa a padova: guida completa 2026': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-mutuo-prima-casa-padova' },
    "ca' marcello mestre: riqualificazione e investimento nel veneto": { img: 'img/blog/ca-marcello-hero.webp', url: 'blog-ca-marcello-mestre' },
    "l'impegno quotidiano di un'agenzia immobiliare: tra burocrazia e incertezza mutui": { img: 'img/blog/ufficio-righetto-immobiliare.webp', url: 'blog-impegno-quotidiano-agenzia-immobiliare' },
    'appartamento nuova costruzione limena: 101 mq con giardino 310 mq in classe a4': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-appartamento-nuova-costruzione-limena' },
    'comprare casa a padova nel 2026: guida definitiva passo dopo passo': { img: 'img/foto-servizi/vendita-immobili-padova.webp', url: 'blog-comprare-casa-padova-guida-2026' },
    'quanto costa vendere casa a padova nel 2026? costi, tasse e tempi reali': { img: 'img/foto-servizi/valutazioni-e-perizie-padova.webp', url: 'blog-costi-vendere-casa-padova-2026' },
    'home staging padova: come vendere casa prima e meglio': { img: 'img/blog/home-staging.webp', url: 'blog-home-staging-padova' },
    'vendere casa a padova: 7 errori costosi da evitare': { img: 'img/team/titolari.webp', url: 'vendere-casa-padova-errori' }
  };
  // Articoli statici (sempre presenti)
  const articoliStatici = [
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
    { titolo: 'Case in Vendita Padova 2026: Prezzi, Zone Migliori e Guida Completa', categoria: 'Mercato locale', data: '2026-03-01', stato: 'pubblicato', immagine_copertina: 'img/foto-servizi/vendita-immobili-padova.webp', url_statico: 'blog-case-vendita-padova' }
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
  grid.innerHTML = articles.map((a,i) => {
    const img = extractImg(a);
    const slug = generateSlug(a.titolo);
    const href = a.url_statico || ('blog-articolo?s=' + encodeURIComponent(slug));
    return '<div class="blog-card rv d'+(i+1)+'" onclick="location.href=\''+href+'\'">'
      + '<div class="blog-cover"'+(img?' style="background:url('+img+') center/cover;font-size:0"':'')+'>'+(img?'':a.emoji||'📝')+'</div>'
      + '<div class="blog-body"><div class="blog-cat">'+((a.categoria||'Blog').replace(/</g,'&lt;'))+'</div>'
      + '<h3 class="blog-title">'+((a.titolo||'').replace(/</g,'&lt;'))+'</h3>'
      + '<div class="blog-date">'+fmtMese(a.data)+'</div></div></div>';
  }).join('');
  // Attiva animazione reveal sulle card appena create
  grid.querySelectorAll('.rv').forEach(el => { if(typeof rvObs!=='undefined') rvObs.observe(el); else el.classList.add('vis'); });
})();
