/* Inquilini scheda immobile - archivio privato immobile_inquilini.
   Port dal candidato approvato: lettura esplicita, date/S.I. con salvataggio CAS,
   nessun nome dedotto, nessun avviso creato. Pannello iniettato prima di "Localizzazione". */
(function(){
'use strict';
const FIELDS='id,immobile_id,cliente_id,fonte_relazione_id,fonte_immobile_id,fonte_cliente_id,inizio,fine,scadenza_intermedia,versione,creato_il,aggiornato_il';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function safeRead(q){try{return await q;}catch(e){return {data:null,error:{message:(e&&e.message)||'Connessione non disponibile'}};};}
function writePending(){return window.rigPropertySaving===true;}
const date=v=>v===null||v===undefined||v===''||/^\d{4}-\d{2}-\d{2}$/.test(v);
const tri=v=>v===null||v===true||v===false;
const uuid=v=>typeof v==='string'&&/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(v),numstr=v=>typeof v==='string'&&/^\d+$/.test(v);
function valid(r){return r&&uuid(r.id)&&typeof r.immobile_id==='string'&&r.immobile_id===immobileId&&uuid(r.cliente_id)&&['fonte_relazione_id','fonte_immobile_id','fonte_cliente_id'].every(k=>numstr(r[k]))&&Number.isSafeInteger(r.versione)&&r.versione>0&&date(r.inizio)&&date(r.fine)&&(!r.inizio||!r.fine||r.fine>=r.inizio)&&tri(r.scadenza_intermedia);}
function sameSaved(a,b){for(const k of ['inizio','fine','scadenza_intermedia','versione'])if(a[k]!==b[k])return false;return true;}

let panel=null,rows=[],draft=new Map(),names=new Map(),busy=false,uncertain=false,immobileId=null;

function currentImmobile(){const el=document.getElementById('editId');return el&&el.value?String(el.value):null;}

function render(){
 const list=panel.querySelector('[data-inq-rows]');list.textContent='';
 for(const r of rows){
  const card=document.createElement('div');card.style.cssText='border:1.5px solid #c9b896;border-radius:10px;padding:12px;margin:10px 0;background:#fbf8f2';
  const nome=names.get(r.cliente_id);
  const h=document.createElement('b');h.textContent=nome||('Cliente #'+r.cliente_id+' (nome non leggibile, collegamento conservato per ID)');card.append(h);
  const values=draft.get(r.id)||r;
  for(const [key,label] of [['inizio','Data inizio'],['fine','Data fine']]){
   const l=document.createElement('label');l.style.cssText='display:block;margin:8px 0';l.append(label+' ');
   const el=document.createElement('input');el.type='date';el.value=values[key]??'';el.disabled=busy||uncertain;
   el.onchange=()=>{const d=draft.get(r.id)||{inizio:r.inizio,fine:r.fine,scadenza_intermedia:r.scadenza_intermedia};d[key]=el.value||null;draft.set(r.id,d);if(!changed(r))draft.delete(r.id);update();};
   l.append(el);card.append(l);
  }
  const l=document.createElement('label');l.style.display='block';l.append('S.I. - scadenza intermedia ');
  const si=document.createElement('select');
  for(const [v,t] of [['','Non verificato'],['true','Sì'],['false','No']]){const op=document.createElement('option');op.value=v;op.textContent=t;si.append(op);}
  si.value=values.scadenza_intermedia===null?'':String(values.scadenza_intermedia);si.disabled=busy||uncertain;
  si.onchange=()=>{const d=draft.get(r.id)||{inizio:r.inizio,fine:r.fine,scadenza_intermedia:r.scadenza_intermedia};d.scadenza_intermedia=si.value===''?null:si.value==='true';draft.set(r.id,d);if(!changed(r))draft.delete(r.id);update();};
  l.append(si);card.append(l);
  const note=document.createElement('p');note.style.cssText='font-size:12px;color:#6b675f';note.textContent='S.I. è solo un dato della relazione. Non crea scadenze, avvisi in home o messaggi.';
  const save=document.createElement('button');save.type='button';save.textContent='Salva solo date e S.I.';save.className='btn btn-primary btn-sm';
  const err=document.createElement('p');err.style.cssText='font-size:12px;color:#923400';err.setAttribute('role','status');
  function changed(rr){const d=draft.get(rr.id);return d&&(d.inizio!==rr.inizio||d.fine!==rr.fine||d.scadenza_intermedia!==rr.scadenza_intermedia);}
  function update(){const d=draft.get(r.id)||r,ok=date(d.inizio)&&date(d.fine)&&(!d.inizio||!d.fine||d.fine>=d.inizio);err.textContent=!ok?'Date non valide: la fine non può precedere l\u2019inizio.':'';save.disabled=busy||uncertain||!ok||!changed(r);}
  save.onclick=async()=>{
   if(save.disabled||busy||uncertain||writePending())return;
   const d=structuredClone(draft.get(r.id));if(!d||!date(d.inizio)||!date(d.fine)||(d.inizio&&d.fine&&d.fine<d.inizio)||!tri(d.scadenza_intermedia))return;
   busy=true;panel.querySelector('[data-inq-load]').disabled=true;render();
   try{
    const patch={...d,versione:r.versione+1,aggiornato_il:new Date().toISOString()};
    let q=sb.from('immobile_inquilini').update(patch);
    for(const k of ['id','immobile_id','cliente_id','fonte_relazione_id','fonte_immobile_id','fonte_cliente_id','versione','creato_il','aggiornato_il','inizio','fine','scadenza_intermedia'])q=r[k]===null?q.is(k,null):q.eq(k,r[k]);
    const result=await q.select(FIELDS);
    if(result.error)throw Error(result.error.message);
    const saved=result.data&&result.data[0];
    if(!result.data||result.data.length!==1||!valid(saved)||!sameSaved({...saved,aggiornato_il:null},{...r,...patch,aggiornato_il:null})||Date.parse(saved.aggiornato_il)!==Date.parse(patch.aggiornato_il))throw Error('Relazione cambiata o salvataggio non confermato');
    Object.assign(r,saved);draft.delete(r.id);
    panel.querySelector('[data-inq-status]').textContent='Salvate solo date e S.I. Identità e altri dati invariati. Nessun avviso o invio creato.';
   }catch(e){uncertain=true;panel.querySelector('[data-inq-status]').textContent='Esito da verificare: '+e.message+'. Riapri la scheda prima di riprovare; bozza conservata.';}
   finally{busy=false;panel.querySelector('[data-inq-load]').disabled=uncertain;render();}
  };
  card.append(note,save,err);list.append(card);update();
 }
}

async function load(){
 if(busy||uncertain||writePending())return;
 if(draft.size&&!confirm('Scartare le sole modifiche inquilini in bozza e rileggere?'))return;
 busy=true;panel.querySelector('[data-inq-load]').disabled=true;
 const status=panel.querySelector('[data-inq-status]');const id=immobileId;
 try{
  const data=[];
  for(let offset=0;;offset+=100){
   const page=await sb.from('immobile_inquilini').select(FIELDS).eq('immobile_id',id).order('id').range(offset,offset+99);
   if(id!==currentImmobile())return;
   if(page.error)throw Error(page.error.message);
   if(!Array.isArray(page.data))throw Error('Risposta non verificata');
   data.push(...page.data);if(page.data.length<100)break;
  }
  if(data.some(r=>!valid(r))||new Set(data.map(r=>r.id)).size!==data.length||new Set(data.map(r=>r.fonte_relazione_id)).size!==data.length)throw Error('Identità o date della relazione non verificate');
  names.clear();const ids=[...new Set(data.map(r=>r.cliente_id))];let namesError=false;
  for(let offset=0;offset<ids.length;offset+=100){
   const r=await safeRead(sb.from('clienti').select('id,nome').in('id',ids.slice(offset,offset+100)));
   if(id!==currentImmobile())return;
   if(r.error){namesError=true;break;}
   for(const c of r.data||[])if(ids.includes(c.id)&&typeof c.nome==='string')names.set(c.id,c.nome);
  }
  rows=structuredClone(data);draft.clear();
  status.textContent=rows.length?('Relazioni inquilini verificate: '+rows.length+(namesError?'. Nomi clienti non leggibili, collegamenti conservati per ID.':'')):'Nessun inquilino collegato in questo archivio. Non prova che manchi nel vecchio.';
 }catch(e){rows=[];status.textContent='Lettura inquilini non verificata: '+e.message+'. Non equivale a nessun inquilino.';}
 finally{busy=false;panel.querySelector('[data-inq-load]').disabled=uncertain;render();}
}

function mount(){
 if(panel&&panel.isConnected)return;
 if(!currentImmobile())return;
 const dividers=[...document.querySelectorAll('.section-divider')];
 const loc=dividers.find(d=>/^Localizzazione/.test(d.textContent.trim()));if(!loc)return;
 panel=document.createElement('div');panel.id='inqPanel';
 panel.innerHTML='<div class="section-divider">Inquilini <span style="background:#e67e22;color:white;font-size:0.65rem;padding:2px 6px;border-radius:4px;margin-left:4px">🔒 SOLO OPERATORE</span></div>'
 +'<div class="form-group form-full" style="border:1.5px solid #c9b896;border-radius:10px;padding:12px">'
 +'<button type="button" class="btn btn-primary btn-sm" data-inq-load>Leggi inquilini collegati</button>'
 +'<p style="font-size:12px;color:#6b675f;margin:8px 0" data-inq-status role="status">Archivio privato predisposto. Nessun proprietario viene trattato come inquilino e nessun collegamento è dedotto dal nome.</p>'
 +'<div data-inq-rows></div></div>';
 loc.parentNode.insertBefore(panel,loc);
 immobileId=currentImmobile();
 panel.querySelector('[data-inq-load]').onclick=load;
}
const mo=new MutationObserver(()=>{const t=document.getElementById('formTitle');if(t&&t.offsetParent)mount();});
mo.observe(document.documentElement,{childList:true,subtree:true});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();
