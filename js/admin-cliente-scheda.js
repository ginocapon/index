/* Scheda cliente in consultazione (non modifica). Solo letture; nessun invio, firma, fattura o archiviazione. */
(function(){
'use strict';
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let box=null;
function css(){if(document.getElementById('rcs-css'))return;const s=document.createElement('style');s.id='rcs-css';s.textContent=
'.rcs{position:fixed;inset:0;z-index:12000;background:#18314980;overflow:auto;padding:14px;font:15px/1.45 Arial,sans-serif;color:#17324d}'+
'.rcs-d{max-width:980px;margin:auto;background:#fff;border-radius:14px;padding:18px 20px 22px;box-shadow:0 12px 50px #0004;position:relative}'+
'.rcs-top{display:flex;gap:12px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap}.rcs-top h2{margin:0;font-size:24px}.rcs-sub{color:#566773;font-size:13px;margin-top:4px}'+
'.rcs button{font:600 14px Arial,sans-serif;min-height:40px;border:1px solid #b9c7d1;border-radius:8px;background:#f3f6f8;color:#17324d;padding:8px 12px;cursor:pointer}'+
'.rcs button[aria-selected=true]{background:#00508f;color:#fff;border-color:#00508f}.rcs button:disabled{opacity:.5;cursor:not-allowed}'+
'.rcs-tabs{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0;border-bottom:2px solid #00508f;padding-bottom:8px}'+
'.rcs-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px}.rcs-grid div{padding:6px 0;border-bottom:1px solid #eef2f5}.rcs-grid b{display:block;font-size:11px;text-transform:uppercase;color:#607184;letter-spacing:.04em}'+
'.rcs h3{background:#00508f;color:#fff;margin:18px 0 8px;padding:7px 12px;font-size:14px;border-radius:4px}'+
'.rcs-ops{position:relative;display:flex;gap:8px}.rcs-menu{position:absolute;right:0;top:44px;z-index:5;background:#fff;border:1px solid #00508f;min-width:290px;box-shadow:0 8px 24px #0003}'+
'.rcs-menu button{display:block;width:100%;text-align:left;border:0;border-radius:0;background:#fff;min-height:36px}.rcs-menu button:hover:not(:disabled){background:#eaf2f8}.rcs-menu hr{margin:2px 0;border:0;border-top:1px solid #d9e2e7}.rcs-menu small{color:#8a5a00;font-size:11px;margin-left:6px}'+
'.rcs-ev{border-left:6px solid #99cc00;background:#f7f9fa;padding:8px 12px;margin:8px 0;border-radius:6px}.rcs-note{color:#566773;font-size:13px}'+
'@media(max-width:760px){.rcs-menu{max-height:60vh}.rcs-grid{grid-template-columns:1fr}.rcs-d{padding:14px}.rcs-menu{position:fixed;left:12px;right:12px;top:auto;bottom:12px;max-height:70vh;overflow:auto}}';
document.head.appendChild(s);}
const fmtD=d=>d?new Date(d).toLocaleDateString('it-IT',{timeZone:'Europe/Rome'}):'';
const fmtDT=d=>d?new Date(d).toLocaleString('it-IT',{timeZone:'Europe/Rome',day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'}):'';
const row=(l,v)=>`<div class="${v?'':'rcs-empty'}"><b>${esc(l)}</b><span>${esc(v||'')}</span></div>`;
function close(){if(box){box.remove();box=null;}}
async function open(id,tab){
 css();close();
 const r=await sb.from('clienti').select('*').eq('id',id).maybeSingle();
 if(r.error||!r.data){alert('Cliente non trovato nel database.');return;}
 const c=r.data;
 const maybe=(l,v)=>v?row(l,v):'';const cerca=maybe('Operazione',c.tipo_operazione_cercata)+maybe('Tipologia',c.tipologia_cercata)+maybe('Zona',c.zona_cercata)+maybe('Budget',(c.budget_min||c.budget_max)?('€ '+(c.budget_min||'0')+' - '+(c.budget_max||'qualsiasi')):'')+maybe('Camere minime',c.camere_min)+maybe('Superficie minima',c.superficie_min?c.superficie_min+' mq':'');
 box=document.createElement('div');box.className='rcs';box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');
 const budget=(c.budget_min||c.budget_max)?('€ '+(c.budget_min||'0')+' - '+(c.budget_max||'qualsiasi')):'';
 box.innerHTML=`<div class="rcs-d"><div class="rcs-top"><div><h2>${esc(c.nome||c.ragione_sociale||'Cliente')}${c.storico?' <span style="font-size:13px;background:#eee;padding:2px 8px;border-radius:10px">Storico</span>':''}</h2><div class="rcs-sub">${c.telefono?`<a href="tel:${esc(c.telefono)}">${esc(c.telefono)}</a>`:''}${c.telefono&&c.email?' · ':''}${c.email?`<a href="mailto:${esc(c.email)}">${esc(c.email)}</a>`:''}</div><div class="rcs-sub">Inserito il ${esc(fmtD(c.created_at))}${c.fonte?' · fonte: '+esc(c.fonte):''}</div></div>
 <div class="rcs-ops"><button data-ops aria-haspopup="true">🔧 Operazioni</button><button data-x>Chiudi</button><div class="rcs-menu" hidden></div></div></div>
 <div class="rcs-tabs" role="tablist"><button data-t="scheda" aria-selected="true">Scheda</button><button data-t="cron" aria-selected="false">Cronistoria</button><button disabled title="SMS non ancora disponibile">SMS</button><span style="flex:1"></span><button data-op="edit">✎ modifica</button><button data-t="all" aria-selected="false">♧ allegati</button><button data-t="crn" aria-selected="false">Note interne</button><button data-t="imm" aria-selected="false">Immobili</button></div>
 <section data-p="scheda"><h3>Informazioni <span style="float:right;font-weight:normal">inserito il ${esc(fmtD(c.created_at))}</span></h3><div class="rcs-information"><div><div class="rcs-grid">${row('Data di nascita:',c.nascita_data?fmtD(c.nascita_data):'')}${row('Indirizzo:',c.indirizzo_cliente)}${row('Luogo di nascita:',c.nascita_luogo)}${row('Fax:',c.fax)}${row('Email:',c.email)}${row('Social:',[c.instagram,c.facebook,c.linkedin].filter(Boolean).join(' · '))}${row('Email (2):',c.email_secondaria)}${row('Email Pec:',c.pec)}${row('Località:',[c.comune,c.provincia].filter(Boolean).join(' '))}${row('Provenienza:',c.fonte)}</div></div><aside><div class="rcs-aside-buttons"><button disabled title="Stampe e modelli non ancora disponibili">▤ stampe</button><button disabled title="Firma documento non ancora disponibile">✎ firma doc.</button><button data-ops>⚒ operazioni</button></div><p><b>Cod.Cliente:</b> ${esc((c.note||'').match(/(?:originale:|gestionale)\s*(\d+)/)?.[1]||'n.d.')} <span style="float:right">Agente: ${esc(c.agente_assegnato||'n.d.')}</span></p><details><summary>Visualizza note</summary><p>${esc(c.note||'')}</p></details></aside></div><h3>Documento di riconoscimento</h3><div class="rcs-grid">${row('Documento di riconoscimento:',c.documento_tipo)}${row('Numero:',c.documento_numero)}${row('Rilasciato il:',c.documento_rilasciato_il?fmtD(c.documento_rilasciato_il):'')}${row('Rilasciato da:',c.documento_rilasciato_da)}${row('Scadenza:',c.documento_scadenza?fmtD(c.documento_scadenza):'')}</div><h3>Richieste</h3><p class="rcs-note">Richieste strutturate del vecchio gestionale non ancora collegate. ${cerca?'Criteri di ricerca già presenti nel nuovo:':''}</p>${cerca?`<div class="rcs-grid">${cerca}</div>`:''}<h3>Allegati</h3><div data-doc-summary></div></section>
 <section data-p="cron" hidden><p class="rcs-note">Eventi dell'agenda collegati a questo cliente. Telefonate, email e SMS del vecchio gestionale non sono importati.</p><div data-cron>Caricamento…</div></section>
 <section data-p="all" hidden></section><section data-p="imm" hidden><p class="rcs-note">Immobili collegati come proprietario.</p><div data-linked>Caricamento…</div></section>
 <section data-p="crn" hidden><p class="rcs-note">Note interne con data e autore. Non vengono inviate a nessuno. Le telefonate, email e SMS del vecchio gestionale non sono importati.</p><div data-crn>Caricamento…</div><div style="margin-top:10px"><textarea data-crn-t rows="3" style="width:100%;box-sizing:border-box;font:15px Arial;padding:8px;border:1px solid #b9c7d1;border-radius:8px" placeholder="Scrivi una nota (es. richiamato, interessato a visita)"></textarea><button data-crn-add style="margin-top:6px">Aggiungi nota</button></div></section></div>`;
 document.body.appendChild(box);
 if(tab==='cron'){box.querySelectorAll('[data-t]').forEach(x=>x.setAttribute('aria-selected',String(x.dataset.t==='cron')));box.querySelectorAll('[data-p]').forEach(x=>x.hidden=x.dataset.p!=='cron');}
 const docs=Array.isArray(c.documenti_cliente)?c.documenti_cliente:[];
 box.querySelector('[data-p=all]').innerHTML=docs.length?docs.map(d=>`<div class="rcs-ev"><a href="${esc(d.url)}" target="_blank" rel="noopener">📄 ${esc(d.nome||'documento')}</a> <span class="rcs-note">${esc(d.tipo||'')}</span></div>`).join(''):'<p class="rcs-note">Nessun allegato collegato a questa scheda. I file dei clienti sono nell\'archivio privato GitHub clienti-docs, non collegati qui.</p>';
 box.querySelector('[data-doc-summary]').innerHTML=docs.length?docs.map(d=>`<p>📄 ${esc(d.nome||'documento')}</p>`).join(''):'<p class="rcs-note">Nessun allegato collegato nel nuovo. Allegati del vecchio da recuperare e verificare.</p>';
 const menu=box.querySelector('.rcs-menu');
 menu.innerHTML=`<button disabled title="Non disponibile; nessun invio">invio informativa privacy</button><button disabled>richiesta firma consenso tratt. dati</button><button disabled>invia follow up richiesta cliente</button><hr><button disabled title="Inserimento nel vecchio gestionale">aggiungi evento</button><button disabled title="Inserimento nel vecchio gestionale">nuovo appuntamento</button><button data-op="mail" ${c.email?'':'disabled'}>contatta via email</button><button disabled>inserisci notizia</button><button disabled>crea fattura</button><button disabled>mostra fatture</button><hr><button disabled>scheda catastale</button><button disabled>adeguata verifica</button><button disabled>verifica cliente</button><button disabled>ispezione ipotecaria soggetto</button><hr><button data-op="storico">${c.storico?'riporta tra i clienti attivi':'metti nello storico'}</button>`;
 const aside=box.querySelector('.rcs-aside-buttons');if(aside){const topOps=box.querySelector('.rcs-top [data-ops]');if(topOps)topOps.remove();aside.style.position='relative';aside.append(menu);}
 const todoBox=document.createElement('details');todoBox.style.cssText='margin-top:18px;border:1px dashed #b9c7d1;border-radius:8px;padding:8px 12px';
 todoBox.innerHTML='<summary style="cursor:pointer;font-weight:700">Da completare (non ancora disponibili qui)</summary><p class="rcs-note">Presenti nel vecchio gestionale, non ancora costruiti in questa scheda: invio informativa privacy, richiesta firma consenso, follow up richiesta, inserisci notizia, crea e mostra fatture, scheda catastale, adeguata verifica, verifica cliente, stampe e modelli, firma documento, cronistoria completa importata (telefonate, email, SMS).</p>';
 box.querySelector('.rcs-d').appendChild(todoBox);
 box.addEventListener('click',ev=>{
  if(ev.target===box){close();return;}
  const b=ev.target.closest('button');if(!b)return;
  if(b.dataset.x!==undefined){close();return;}
  if(b.dataset.mobileImm){const imm=b.dataset.mobileImm;if(window.matchMedia('(max-width:760px)').matches){close();window.dispatchEvent(new CustomEvent('righetto:mobile-immobile',{detail:{id:imm}}));}else{close();showSection('immobili');if(typeof editImmobile==='function')editImmobile(imm);}return;}
  if(b.dataset.ops!==undefined){menu.hidden=!menu.hidden;return;}
  if(b.dataset.t){box.querySelectorAll('[data-t]').forEach(x=>x.setAttribute('aria-selected',String(x===b)));box.querySelectorAll('[data-p]').forEach(x=>x.hidden=x.dataset.p!==b.dataset.t);return;}
  const op=b.dataset.op;if(!op)return;menu.hidden=true;
  if(op==='edit'){close();if(typeof showSection==='function')showSection('clienti');if(typeof allClienti!=='undefined'&&!allClienti.some(x=>String(x.id)===String(c.id)))allClienti.push(c);editCliente(c.id);}
  else if(op==='match'){close();showMatchingImmobili(c.id);}
  else if(op==='ev'){close();if(typeof showSection==='function')showSection('agenda');if(window.RighettoAgenda&&RighettoAgenda.newEvent)RighettoAgenda.newEvent({client_id:c.id,client:c.nome,phone:c.telefono});}
  else if(op==='mail'){location.href='mailto:'+c.email;}
  else if(op==='storico'){toggleStorico(c);}
 });
 document.addEventListener('keydown',function k(e){if(e.key==='Escape'){close();document.removeEventListener('keydown',k);}});
 loadCrn(c.id);
 const linkedBox=box.querySelector('[data-linked]');sb.from('immobili').select('id,codice,titolo').eq('proprietario_id',c.id).order('codice').then(r=>{if(r.error){linkedBox.textContent='Immobili non leggibili: '+r.error.message;return;}linkedBox.innerHTML=(r.data||[]).length?r.data.map(i=>'<button type="button" data-mobile-imm="'+esc(i.id)+'" class="rcs-ev"><b>'+esc(i.codice)+'</b> '+esc(i.titolo||'')+'</button>').join(''):'<p class="rcs-note">Nessun immobile collegato come proprietario.</p>';});
 box.querySelector('[data-crn-add]').addEventListener('click',async()=>{const ta=box.querySelector('[data-crn-t]');const t=ta.value.trim();if(!t)return;const u=await sb.auth.getUser();const r=await sb.from('cliente_cronistoria').insert([{cliente_id:c.id,tipo:'nota',testo:t,autore:(u.data&&u.data.user&&u.data.user.email)||null}]);if(r.error){alert('Nota non salvata: '+r.error.message);return;}ta.value='';loadCrn(c.id);});
 const ev=await sb.from('agenda_events').select('id,starts_at,type_id,agents,title,notes_internal,property_id,done').eq('client_id',c.id).is('deleted_at',null).order('starts_at',{ascending:false}).limit(100);
 const el=box&&box.querySelector('[data-cron]');if(!el)return;
 if(ev.error){el.textContent='Cronistoria non leggibile: '+ev.error.message;return;}
 if(!ev.data.length){el.innerHTML='<p class="rcs-note">Nessun appuntamento in agenda per questo cliente. La cronistoria completa del vecchio gestionale non è stata importata.</p>';return;}
 const pids=[...new Set(ev.data.map(e=>e.property_id).filter(Boolean))];let pm={};
 if(pids.length){const p=await sb.from('immobili').select('id,codice').in('id',pids);(p.data||[]).forEach(x=>pm[x.id]=x.codice);}
 el.innerHTML=ev.data.map(e=>`<div class="rcs-ev"><b>${esc(fmtDT(e.starts_at))}</b> · ${esc((e.agents||[]).join(', '))}${e.property_id&&pm[e.property_id]?' · immobile '+esc(pm[e.property_id]):''}${e.done?' · eseguito':''}<div class="rcs-note">${esc(e.title||e.notes_internal||'')}</div></div>`).join('')+'<p class="rcs-note">La cronistoria completa del vecchio gestionale (telefonate, email, SMS) non è stata importata.</p>';
}
async function loadCrn(id){const el=box&&box.querySelector('[data-crn]');if(!el)return;const r=await sb.from('cliente_cronistoria').select('creato_il,tipo,testo,autore').eq('cliente_id',id).order('creato_il',{ascending:false}).limit(200);if(r.error){el.textContent='Cronistoria non leggibile: '+r.error.message;return;}el.innerHTML=r.data.length?r.data.map(x=>`<div class="rcs-ev"><b>${esc(fmtDT(x.creato_il))}</b>${x.autore?' · '+esc(x.autore):''}<div>${esc(x.testo)}</div></div>`).join(''):'<p class="rcs-note">Nessuna nota interna inserita. Gli appuntamenti sono nella scheda Cronistoria.</p>';}
async function toggleStorico(c){const to=!c.storico;if(!confirm(to?'Mettere questo cliente nello storico?\n\nNon viene cancellato: esce dall\'elenco normale e resta in "Mostra storico".':'Riportare questo cliente tra gli attivi?'))return;const r=await sb.from('clienti').update({storico:to,storico_il:to?new Date().toISOString():null}).eq('id',c.id);if(r.error){alert('Operazione non riuscita: '+r.error.message);return;}close();if(typeof loadClienti==='function')loadClienti();open(c.id);}
window.RighettoCliente={open,close};
})();
