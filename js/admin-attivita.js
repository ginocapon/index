/* Sezione Attivita sotto l'agenda. Due modi: memoria (anteprima, nulla salvato) e database (tabelle pratiche/attivita/allegati_attivita + bucket privato attivita-pratiche). Nessun invio email.
   Colore pratica libero, scelto da chi la crea; pratiche visibili per agenda (Gino o Linda). Tipi attivita proposti (modificabili): documento mancante, scadenza, promemoria, altro. */
(function(){'use strict';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const kinds=['Documento mancante','Scadenza','Promemoria','Altro'];
let root,items=[],filter='tutte',open=new Set(),agent='Gino',store=null,msg='';
const pct=p=>{const t=p.tasks.length;return t?Math.round(p.tasks.filter(x=>x.done).length/t*100):0;};
function task(p,t){t.files=t.files||[];const st=t.files.length?'<b class="at-ok">recuperato</b>':(t.kind==='Documento mancante'?'<b class="at-no">mancante</b>':'');
return `<div class="at-task ${t.done?'done':''}"><input type="checkbox" data-pr="${esc(p.id)}" data-t="${esc(t.id)}" ${t.done?'checked':''}><div class="at-tx"><span class="at-t">${esc(t.text)}</span> ${st}<span class="at-sub">${esc(t.kind)}${t.due?' - entro '+esc(t.due):''}${t.done&&t.doneAt?' - fatto '+esc(t.doneAt):''}</span>
${t.files.map((f,i)=>`<div class="at-file"><span>${esc(f.name)}</span><span><button type="button" data-dl="${esc(p.id)}|${esc(t.id)}|${i}">Scarica</button> <label class="at-sel"><input type="checkbox" data-mail="${esc(p.id)}|${esc(t.id)}|${i}"> per email</label></span></div>`).join('')}
<form class="at-addf" data-pr="${esc(p.id)}" data-t="${esc(t.id)}">${store.mode==='database'?'<input name="file" type="file" accept=".pdf,.jpg,.jpeg,.png,.docx,.xlsx" required>':'<input name="f" placeholder="Nome file (es. APE)" required>'}<button>Allega</button></form></div></div>`;}
function card(p){const o=p.tasks.filter(x=>!x.done);const mancano=o.slice(0,2).map(x=>esc(x.text)).join(', ')||'Nessuna attivita aperta';
const col=/^#[0-9a-f]{6}$/i.test(p.colore||'')?p.colore:'#ffffff';
return `<details class="at-pr" style="border-left:8px solid ${col};background:${col}22" data-id="${esc(p.id)}" ${open.has(p.id)?'open':''}><summary><span class="at-id">${esc(p.id)}</span><span>${esc(p.titolo)}<span class="at-sub"> ${esc(p.cliente||'')}</span></span><span>${mancano}</span><span><span class="at-bar"><i style="width:${pct(p)}%"></i></span><span class="at-sub">${p.tasks.filter(x=>x.done).length}/${p.tasks.length} fatte</span></span><span class="at-sub">${esc(p.scadenza||'')}</span></summary>
<div class="at-body"><div class="at-meta"><label>Colore pratica <input type="color" data-color="${esc(p.id)}" value="${col}"></label> <span class="at-sub">Agenda: ${esc(p.agente)}</span></div><div><h4>Attivita</h4>${p.tasks.map(t=>task(p,t)).join('')||'<div class="at-empty">Nessuna attivita.</div>'}
<form class="at-add" data-pr="${esc(p.id)}"><input name="text" placeholder="Nuova attivita" required><select name="kind">${kinds.map(k=>`<option>${esc(k)}</option>`).join('')}</select><input name="due" type="date"><button>Aggiungi</button></form></div>
<div class="at-files"><h4>Riepilogo</h4><div class="at-sub">${p.tasks.filter(t=>(t.files||[]).length).length} attivita con allegati, ${p.tasks.filter(t=>t.kind==='Documento mancante'&&!(t.files||[]).length).length} documenti mancanti</div><button type="button" data-mailprep="${esc(p.id)}">Prepara email con i file scelti</button><div class="at-sub">Solo bozza da rivedere: nessun invio senza ok di Gino. File privati, salvataggio dopo approvazione.</div><div class="at-mailbox" data-box="${esc(p.id)}"></div></div></div></details>`;}
function draw(){const list=items.filter(p=>p.agente===agent).filter(p=>filter==='tutte'||(filter==='aperte'?p.tasks.some(x=>!x.done):p.tasks.length&&p.tasks.every(x=>x.done)));
root.innerHTML=`<div class="at"><div class="at-head"><h2>Attivit\u00e0</h2><span><span class="at-tabs"><button type="button" data-ag="Gino" class="${agent==='Gino'?'on':''}">Attivit\u00e0 Gino</button><button type="button" data-ag="Linda" class="${agent==='Linda'?'on':''}">Attivit\u00e0 Linda</button></span> <select data-f><option value="tutte">Tutte le pratiche</option><option value="aperte">Con attivita aperte</option><option value="chiuse">Completate</option></select></span></div><form class="at-newp"><input name="titolo" placeholder="Nuova pratica (es. Rossi - Via Roma)" required><button>Crea pratica</button></form><div class="at-banner ${store.mode==='database'?'at-live':''}">${store.mode==='database'?'Salvato nel database privato. Nessuna email parte da qui.':'ANTEPRIMA: pratiche di esempio, nulla viene salvato.'}${msg?' <b>'+esc(msg)+'</b>':''}</div><div class="at-list">${list.map(card).join('')||'<div class="at-empty">Nessuna pratica.</div>'}</div></div>`;
root.querySelector('[data-f]').value=filter;}
const memStore=()=>({mode:'memoria',async load(o){return JSON.parse(JSON.stringify(o||[]));},
async newPratica(d){return {id:'P'+Date.now(),titolo:d.titolo,cliente:'',agente:d.agente,colore:'',tasks:[]};},
async setColor(){},async newTask(pid,d){return {id:'n'+Date.now(),text:d.text,kind:d.kind,due:d.due||'',done:false,files:[]};},
async toggle(pid,tid,done){return done?new Date().toLocaleDateString('it-IT'):'';},
async addFile(pid,tid,fd){return {id:'f'+Date.now(),name:fd.get('f'),path:''};},async download(){alert('Anteprima: il download funzionera con i file veri.');}});
const dbStore=sb=>({mode:'database',
async load(){const r=await sb.from('pratiche').select('id,titolo,agente,colore,creata_il,attivita(id,testo,tipo,scadenza,fatta,fatta_il,allegati_attivita(id,nome,percorso,stato))').order('creata_il',{ascending:false});if(r.error)throw r.error;
return (r.data||[]).map(p=>({id:p.id,titolo:p.titolo,cliente:'',agente:p.agente||'Gino',colore:p.colore||'',tasks:(p.attivita||[]).map(a=>({id:a.id,text:a.testo,kind:a.tipo||'Altro',due:a.scadenza||'',done:!!a.fatta,doneAt:a.fatta_il?new Date(a.fatta_il).toLocaleDateString('it-IT'):'',files:(a.allegati_attivita||[]).map(f=>({id:f.id,name:f.nome,path:f.percorso}))}))}));},
async newPratica(d){const r=await sb.from('pratiche').insert({titolo:d.titolo,agente:d.agente}).select('id,titolo,agente,colore').single();if(r.error)throw r.error;return {id:r.data.id,titolo:r.data.titolo,cliente:'',agente:r.data.agente,colore:'',tasks:[]};},
async setColor(id,c){const r=await sb.from('pratiche').update({colore:c}).eq('id',id);if(r.error)throw r.error;},
async newTask(pid,d){const r=await sb.from('attivita').insert({pratica_id:pid,testo:d.text,tipo:d.kind,scadenza:d.due||null}).select('id').single();if(r.error)throw r.error;return {id:r.data.id,text:d.text,kind:d.kind,due:d.due||'',done:false,files:[]};},
async toggle(pid,tid,done){const at=done?new Date().toISOString():null;const r=await sb.from('attivita').update({fatta:done,fatta_il:at}).eq('id',tid);if(r.error)throw r.error;return done?new Date().toLocaleDateString('it-IT'):'';},
async addFile(pid,tid,fd){const f=fd.get('file');if(!f||!f.size)throw new Error('Scegli un file');if(f.size>10485760)throw new Error('File oltre 10 MB');
const safe=f.name.replace(/[^A-Za-z0-9._-]+/g,'_');const path=pid+'/'+tid+'/'+Date.now()+'-'+safe;
const u=await sb.storage.from('attivita-pratiche').upload(path,f,{contentType:f.type||undefined,upsert:false});if(u.error)throw u.error;
const r=await sb.from('allegati_attivita').insert({attivita_id:tid,nome:f.name,percorso:path,dimensione:f.size,stato:'recuperato'}).select('id').single();
if(r.error){await sb.storage.from('attivita-pratiche').remove([path]);throw r.error;}return {id:r.data.id,name:f.name,path};},
async download(file){const r=await sb.storage.from('attivita-pratiche').createSignedUrl(file.path,60,{download:file.name});if(r.error)throw r.error;window.open(r.data.signedUrl,'_blank');}});
async function run(fn){try{msg='';await fn();}catch(e){msg='Non salvato: '+(e&&e.message||e);}draw();}
async function init(el,o={}){root=el;store=o.store||memStore();if(o.open)o.open.forEach(x=>open.add(x));
try{items=await store.load(o.items);}catch(e){items=[];msg='Non riesco a leggere le pratiche: '+(e&&e.message||e);}
root.addEventListener('toggle',e=>{const d=e.target.closest&&e.target.closest('details.at-pr');if(d){d.open?open.add(d.dataset.id):open.delete(d.dataset.id);}},true);
root.addEventListener('change',e=>{const t=e.target;if(t.matches('[data-color]')){const p=items.find(x=>x.id===t.dataset.color);run(async()=>{await store.setColor(p.id,t.value);p.colore=t.value;});return;}if(t.matches('[data-f]')){filter=t.value;draw();return;}
if(t.matches('input[type=checkbox][data-pr]')){const p=items.find(x=>x.id===t.dataset.pr),k=p.tasks.find(x=>x.id===t.dataset.t);run(async()=>{const at=await store.toggle(p.id,k.id,t.checked);k.done=t.checked;k.doneAt=at;});}});
root.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;if(b.dataset.ag){agent=b.dataset.ag;draw();return;}
if(b.dataset.dl){const[a,t,i]=b.dataset.dl.split('|');const f=items.find(x=>x.id===a).tasks.find(x=>x.id===t).files[+i];run(()=>store.download(f));return;}
if(b.dataset.mailprep){const id=b.dataset.mailprep,sel=[...root.querySelectorAll('input[data-mail]:checked')].filter(c=>c.dataset.mail.startsWith(id+'|')).map(c=>{const[a,t,i]=c.dataset.mail.split('|');return items.find(x=>x.id===a).tasks.find(x=>x.id===t).files[+i].name;});
root.querySelector('[data-box="'+id+'"]').innerHTML=sel.length?`<div class="at-draft"><b>BOZZA, non inviata</b><br>Allegati: ${sel.map(esc).join(', ')}<br>Destinatario e testo da scegliere. Parte solo dopo ok di Gino.</div>`:'<div class="at-sub">Spunta almeno un file "per email".</div>';}});
root.addEventListener('submit',e=>{const nf=e.target.closest('form.at-newp');if(nf){e.preventDefault();const d=new FormData(nf);run(async()=>{const p=await store.newPratica({titolo:String(d.get('titolo')).trim(),agente:agent});items.unshift(p);open.add(p.id);});return;}
const f=e.target.closest('form.at-add,form.at-addf');if(!f)return;e.preventDefault();const p=items.find(x=>x.id===f.dataset.pr),d=new FormData(f);
if(f.classList.contains('at-add')){run(async()=>{p.tasks.push(await store.newTask(p.id,{text:String(d.get('text')).trim(),kind:d.get('kind'),due:d.get('due')}));});}
else{const k=p.tasks.find(x=>x.id===f.dataset.t);run(async()=>{(k.files=k.files||[]).push(await store.addFile(p.id,k.id,d));});}});
draw();}
window.RighettoAttivita={init,dbStore};})();
