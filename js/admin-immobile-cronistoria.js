/* CANDIDATE: current native property_id history. Existing authenticated read, no new relation RPC. */
(function(){
'use strict';
let pendingHandle=null;
const fields='id,source_id,starts_at,ends_at,type_id,agents,title,notes_internal,client_id,property_id,done,personal,highlight';
let panel,id=null,principal=null,epoch=0,rows=[],busy=false,page=0,more=true,filter='',query='';
const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
const current=()=>document.getElementById('editId')?.value||null;
async function verify(ticket){const u=await sb.auth.getUser();if(ticket!==epoch||current()!==id||window.RighettoGatedPrincipal!==principal||u.error||u.data?.user?.id!==principal)throw Error('Sessione o immobile cambiato. Riapri la scheda.');}
function draw(){
 const list=panel.querySelector('[data-ich-list]');list.replaceChildren();
 const types=window.RighettoAgendaTypes||[];
 const shown=rows.filter(r=>(!filter||r.type_id===filter)&&(!query||[r.title,r.notes_internal,...(r.agents||[])].join(' ').toLocaleLowerCase('it').includes(query)));
 for(const r of shown){
  const card=el('article');card.className='ich-event';
  const type=types.find(t=>t.id===r.type_id);card.style.borderLeftColor=/^#[0-9a-f]{6}$/i.test(type?.color||'')?type.color:'#005b80';
  const date=new Date(r.starts_at);card.append(el('h4',Number.isFinite(date.getTime())?date.toLocaleString('it-IT',{timeZone:'Europe/Rome',day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'}):'Data non valida'));
  card.append(el('b',type?.name||r.type_id||'Tipo non indicato'));
  if(r.title)card.append(el('p',r.title));
  if(r.agents?.length)card.append(el('p','Agenti: '+r.agents.join(', ')));
  card.append(el('p','Stato: '+(r.done===true?'eseguito':r.done===false?'da eseguire':'non indicato')+(r.personal===true?' · personale':'')));
  if(r.notes_internal){const note=el('p',r.notes_internal);note.className='ich-note';card.append(note);}
  const open=el('button','Apri evento in Agenda');open.type='button';open.onclick=async()=>{
   const ticket=epoch;open.disabled=true;try{await verify(ticket);if(!window.RighettoNavigation)throw Error('Navigazione Agenda non disponibile');await RighettoNavigation.open({section:'agenda',view:'agenda-detail',id:String(r.id)});}catch(e){if(ticket===epoch)panel.querySelector('[data-ich-status]').textContent=e.message;}finally{open.disabled=false;}
  };card.append(open);list.append(card);
 }
 if(!shown.length)list.append(el('p',rows.length?'Nessun evento corrisponde ai filtri nelle pagine caricate.':'Nessuna attività collegata nel nuovo gestionale. Lo storico del vecchio gestionale potrebbe essere diverso.'));
 panel.querySelector('[data-ich-count]').textContent=shown.length+' visibili / '+rows.length+' caricati';
 const select=panel.querySelector('[data-ich-type]'),previous=select.value;select.replaceChildren(new Option('Tutti i tipi',''));
 for(const type of [...new Set(rows.map(r=>r.type_id).filter(Boolean))])select.append(new Option(types.find(t=>t.id===type)?.name||type,type));select.value=previous;
 panel.querySelector('[data-ich-more]').hidden=!more;panel.querySelector('[data-ich-more]').disabled=busy;
}
async function load(reset=false){
 if(busy||!id||!principal)return;busy=true;const ticket=epoch,property=id,status=panel.querySelector('[data-ich-status]');status.textContent='Caricamento eventi collegati...';panel.querySelector('[data-ich-reload]').disabled=true;
 try{
  await verify(ticket);const n=reset?0:page;
  const result=await sb.from('agenda_events').select(fields).eq('property_id',property).is('deleted_at',null).order('starts_at',{ascending:false}).order('id',{ascending:true}).range(n*100,n*100+99);
  await verify(ticket);if(result.error||!Array.isArray(result.data))throw Error(result.error?.message||'Risposta non verificata');
  if(result.data.some(r=>!r.id||!r.starts_at||r.property_id!==property))throw Error('Collegamento evento non verificato');
  if(reset)rows=[];const known=new Set(rows.map(r=>r.id));for(const r of result.data)if(!known.has(r.id)){rows.push(r);known.add(r.id);}
  page=n+1;more=result.data.length===100;status.textContent='Sono mostrate le attività presenti nel nuovo gestionale.';draw();pendingHandle?.refresh();
 }catch(e){if(ticket===epoch){if(reset){rows=[];panel.querySelector('[data-ich-list]').replaceChildren();panel.querySelector('[data-ich-count]').textContent='';panel.querySelector('[data-ich-more]').hidden=true;}status.textContent='Lettura non verificata: '+e.message+'. Non equivale a nessun evento.';}}
 finally{if(ticket===epoch){busy=false;panel.querySelector('[data-ich-reload]').disabled=false;panel.querySelector('[data-ich-more]').disabled=false;}}
}
function mount(){
 const host=document.getElementById('ril-panel-cronistoria');if(!host)return;
 const next=current(),uid=window.RighettoGatedPrincipal||null;if(panel?.isConnected&&id===next&&principal===uid)return;
 epoch++;id=next;principal=uid;rows=[];page=0;more=true;busy=false;filter='';query='';panel=host;panel.replaceChildren();
 panel.append(el('h3','Cronistoria immobile'));if(!id||!principal){panel.append(el('p','Apri un immobile salvato per leggere gli eventi collegati.'));return;}
 const bar=el('div');bar.className='ich-bar';bar.dataset.propertyHistoryFilters='';
 const reload=el('button','Leggi eventi collegati');reload.type='button';reload.dataset.ichReload='';reload.onclick=()=>load(true);
 const type=el('select');type.dataset.ichType='';type.setAttribute('aria-label','Tipo evento');type.append(new Option('Tutti i tipi',''));type.onchange=()=>{filter=type.value;draw();};
 const search=el('input');search.type='search';search.placeholder='Cerca nei testi caricati';search.setAttribute('aria-label','Cerca negli eventi caricati');search.oninput=()=>{query=search.value.trim().toLocaleLowerCase('it');draw();};bar.append(reload,type,search);panel.append(bar);
 const status=el('p','Premi Leggi eventi collegati per consultare le attività presenti nel nuovo gestionale.');status.dataset.ichStatus='';status.setAttribute('role','status');
 const count=el('p');count.dataset.ichCount='';const list=el('div');list.dataset.ichList='';
 const nextButton=el('button','Carica 100 eventi precedenti');nextButton.type='button';nextButton.dataset.ichMore='';nextButton.hidden=true;nextButton.onclick=()=>load();panel.append(status,count,list,nextButton);const pending=document.createElement('section');panel.append(pending);const ticket=epoch,property=id,pendingUid=principal;import('./whatsapp-pending-ui.mjs?v=20261107-simple-v3').then(m=>m.mountPending({host:pending,db:sb,principal:pendingUid,visibleEventIds:()=>rows.map(e=>e.id),scope:{propertyId:property},alive:()=>ticket===epoch&&pending.isConnected&&id===property&&principal===pendingUid})).then(handle=>{if(ticket===epoch)pendingHandle=handle;}).catch(()=>{if(ticket===epoch&&pending.isConnected)pending.textContent='Richieste WhatsApp pendenti non leggibili. Non equivale a nessuna richiesta.';});
}
const style=el('style');style.textContent='#ril-panel-cronistoria:not([hidden]){display:block}.ich-bar{display:flex;flex-wrap:wrap;gap:8px}.ich-bar input,.ich-bar select{max-width:100%;min-height:42px;padding:8px;border:1px solid #abc2cf}.ich-event{border:1px solid #cbdce5;border-left:6px solid #005b80;padding:12px;margin:12px 0;background:#fff}.ich-event h4{margin:0 0 8px}.ich-event p{margin:6px 0;overflow-wrap:anywhere}.ich-note{white-space:pre-wrap}.ril-panel button{cursor:pointer}.ich-bar button,.ich-event button,[data-ich-more]{min-height:42px;padding:8px 12px;color:#17324d;border:1px solid #91b5c8;background:#edf6fa}';document.head.append(style);
const observer=new MutationObserver(mount);observer.observe(document.body,{childList:true,subtree:true});mount();
sb.auth.onAuthStateChange?.(event=>{if(event==='SIGNED_OUT'){epoch++;panel?.replaceChildren(el('p','Sessione terminata. Riapri la scheda dopo l’accesso.'));rows=[];id=null;principal=null;}});
})();
