/* Sezione Attivita sotto l'agenda. ANTEPRIMA: dati solo in memoria, nulla viene salvato o inviato.
   Tipi attivita proposti (modificabili): documento mancante, scadenza, promemoria, altro. */
(function(){'use strict';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const kinds=['Documento mancante','Scadenza','Promemoria','Altro'];
let root,items=[],filter='tutte',open=new Set();
const pct=p=>{const t=p.tasks.length;return t?Math.round(p.tasks.filter(x=>x.done).length/t*100):0;};
function task(p,t){t.files=t.files||[];const st=t.files.length?'<b class="at-ok">recuperato</b>':(t.kind==='Documento mancante'?'<b class="at-no">mancante</b>':'');
return `<div class="at-task ${t.done?'done':''}"><input type="checkbox" data-pr="${esc(p.id)}" data-t="${esc(t.id)}" ${t.done?'checked':''}><div class="at-tx"><span class="at-t">${esc(t.text)}</span> ${st}<span class="at-sub">${esc(t.kind)}${t.due?' - entro '+esc(t.due):''}${t.done&&t.doneAt?' - fatto '+esc(t.doneAt):''}</span>
${t.files.map((f,i)=>`<div class="at-file"><span>${esc(f)}</span><span><button type="button" data-dl="${esc(p.id)}|${esc(t.id)}|${i}">Scarica</button> <label class="at-sel"><input type="checkbox" data-mail="${esc(p.id)}|${esc(t.id)}|${i}"> per email</label></span></div>`).join('')}
<form class="at-addf" data-pr="${esc(p.id)}" data-t="${esc(t.id)}"><input name="f" placeholder="Nome file (es. APE)" required><button>Allega</button></form></div></div>`;}
function card(p){const o=p.tasks.filter(x=>!x.done);const mancano=o.slice(0,2).map(x=>esc(x.text)).join(', ')||'Nessuna attivita aperta';
return `<details class="at-pr" data-id="${esc(p.id)}" ${open.has(p.id)?'open':''}><summary><span class="at-id">${esc(p.id)}</span><span>${esc(p.titolo)}<span class="at-sub"> ${esc(p.cliente||'')}</span></span><span>${mancano}</span><span><span class="at-bar"><i style="width:${pct(p)}%"></i></span><span class="at-sub">${p.tasks.filter(x=>x.done).length}/${p.tasks.length} fatte</span></span><span class="at-sub">${esc(p.scadenza||'')}</span></summary>
<div class="at-body"><div><h4>Attivita</h4>${p.tasks.map(t=>task(p,t)).join('')||'<div class="at-empty">Nessuna attivita.</div>'}
<form class="at-add" data-pr="${esc(p.id)}"><input name="text" placeholder="Nuova attivita" required><select name="kind">${kinds.map(k=>`<option>${esc(k)}</option>`).join('')}</select><input name="due" type="date"><button>Aggiungi</button></form></div>
<div class="at-files"><h4>Riepilogo</h4><div class="at-sub">${p.tasks.filter(t=>(t.files||[]).length).length} attivita con allegati, ${p.tasks.filter(t=>t.kind==='Documento mancante'&&!(t.files||[]).length).length} documenti mancanti</div><button type="button" data-mailprep="${esc(p.id)}">Prepara email con i file scelti</button><div class="at-sub">Solo bozza da rivedere: nessun invio senza ok di Gino. File privati, salvataggio dopo approvazione.</div><div class="at-mailbox" data-box="${esc(p.id)}"></div></div></div></details>`;}
function draw(){const list=items.filter(p=>filter==='tutte'||(filter==='aperte'?p.tasks.some(x=>!x.done):p.tasks.length&&p.tasks.every(x=>x.done)));
root.innerHTML=`<div class="at"><div class="at-head"><h2>Attivita</h2><span><select data-f><option value="tutte">Tutte le pratiche</option><option value="aperte">Con attivita aperte</option><option value="chiuse">Completate</option></select></span></div><form class="at-newp"><input name="titolo" placeholder="Nuova pratica" required><input name="cliente" placeholder="Cliente o immobile (facoltativo)"><button>Crea pratica</button></form><div class="at-banner">ANTEPRIMA: pratiche di esempio, nulla viene salvato.</div><div class="at-list">${list.map(card).join('')||'<div class="at-empty">Nessuna pratica.</div>'}</div></div>`;
root.querySelector('[data-f]').value=filter;}
function init(el,o={}){root=el;if(o.open)o.open.forEach(x=>open.add(x));items=JSON.parse(JSON.stringify(o.items||[]));
root.addEventListener('toggle',e=>{const d=e.target.closest&&e.target.closest('details.at-pr');if(d){d.open?open.add(d.dataset.id):open.delete(d.dataset.id);}},true);
root.addEventListener('change',e=>{const t=e.target;if(t.matches('[data-f]')){filter=t.value;draw();return;}
if(t.matches('input[type=checkbox][data-pr]')){const p=items.find(x=>x.id===t.dataset.pr),k=p.tasks.find(x=>x.id===t.dataset.t);k.done=t.checked;k.doneAt=t.checked?new Date().toLocaleDateString('it-IT'):'';draw();}});
root.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;if(b.dataset.dl){alert('Anteprima: il download funzionera con i file veri.');}
if(b.dataset.mailprep){const id=b.dataset.mailprep,sel=[...root.querySelectorAll('input[data-mail]:checked')].filter(c=>c.dataset.mail.startsWith(id+'|')).map(c=>{const[a,t,i]=c.dataset.mail.split('|');return items.find(x=>x.id===a).tasks.find(x=>x.id===t).files[+i];});
root.querySelector('[data-box="'+id+'"]').innerHTML=sel.length?`<div class="at-draft"><b>BOZZA, non inviata</b><br>Allegati: ${sel.map(esc).join(', ')}<br>Destinatario e testo da scegliere. Parte solo dopo ok di Gino.</div>`:'<div class="at-sub">Spunta almeno un file "per email".</div>';}});
root.addEventListener('submit',e=>{const nf=e.target.closest('form.at-newp');if(nf){e.preventDefault();const d=new FormData(nf);const id='P'+(items.length+1);items.push({id,titolo:d.get('titolo'),cliente:d.get('cliente'),scadenza:'',files:[],tasks:[]});open.add(id);draw();return;}const f=e.target.closest('form.at-add,form.at-addf');if(!f)return;e.preventDefault();const p=items.find(x=>x.id===f.dataset.pr),d=new FormData(f);
if(f.classList.contains('at-add')){p.tasks.push({id:'n'+Date.now(),text:d.get('text'),kind:d.get('kind'),due:d.get('due')||'',done:false,files:[]});}else{const k=p.tasks.find(x=>x.id===f.dataset.t);(k.files=k.files||[]).push(d.get('f'));}draw();});
draw();}
window.RighettoAttivita={init};})();
