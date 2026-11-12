import {createHistoryRouter} from './history-core.mjs';
// Requires source hooks in patch-live.py. Install after login and final wrappers.
export function installAppHistory(win=window,{scope='local-fixture'}={}){
 if(win.RighettoNavigation)return win.RighettoNavigation;
 const listeners=[],listen=(target,type,fn,capture=false)=>{target.addEventListener(type,fn,capture);listeners.push(()=>target.removeEventListener(type,fn,capture));};
 const d=win.document,baseShow=win.showSection,baseShowById=win.showSectionById,views=new Map(),sections=new Set([...d.querySelectorAll('.section[id]')].map(x=>x.id.slice(4)));sections.add('analytics');sections.add('attivita');
 let replaying=false,router,epoch=0,baseline=new Map(),attachmentBase=null,disposed=false;
 const containers=()=>[...d.querySelectorAll('form,#clienteModal.open,.rcs,.ra-modal')].filter(x=>x.getClientRects().length);
 const value=x=>x.type==='checkbox'||x.type==='radio'?x.checked:x.type==='file'?Array.from(x.files||[],f=>f.name+'|'+f.size+'|'+f.lastModified):x.value;
 const snapshot=()=>new Map(containers().flatMap(c=>[...c.querySelectorAll('input,textarea,select')]).filter(x=>!x.closest('[data-property-history-filters]')).map(x=>[x,JSON.stringify(value(x))]));
 const attachments=()=>{const a=win.RighettoNavigationAttachments?.();if(!a)return null;const result={};if(d.querySelector('#immobileForm')?.getClientRects().length)result.property=a.property;if(d.querySelector('#clienteModal.open'))result.client=a.client;return JSON.stringify(result);};
 const clean=()=>{baseline=snapshot();attachmentBase=attachments();};
 const dirty=()=>!!win.RighettoPropertyReferences?.dirty()||!!win.RighettoPropertyExtra?.dirty()||!!win.RighettoPropertyReferences?.pending()||!!win.RighettoPropertyExtra?.pending()||!!win.RighettoLabels?.pending()||!!win.RighettoLabels?.dirty()||attachmentBase!==attachments()||[...baseline].some(([el,v])=>el.isConnected&&JSON.stringify(value(el))!==v);
 const key=r=>JSON.stringify(r),valid=r=>r&&sections.has(r.section)&&(!r.view||['client','client-edit','client-new','property-edit','agenda-detail','agenda-edit','agenda-new','mobile-property'].includes(r.view))&&(!r.id||/^[a-zA-Z0-9-]{1,80}$/.test(r.id))&&(!r.tab||['scheda','cron','all','imm','crn','doc','readonly'].includes(r.tab));
 function close(){win.RighettoMobileNavigation?.closeScheda?.();win.RighettoCliente?.close();d.querySelectorAll('.ra-modal').forEach(x=>x.remove());d.querySelector('#clienteModal')?.classList.remove('open');}
 async function render(r){
  const now=++epoch;const current=()=>!disposed&&now===epoch;const action=(!r.id&&r.view?.startsWith('agenda-')?views.get(key(r)):null)||resolve(r,current)||views.get(key(r));replaying=true;close();
  try{
   baseShow(r.section);
   if(action)await action(current);
  }catch(error){const p=d.createElement('p');p.setAttribute('role','alert');p.dataset.navigationError='';p.textContent=!r.id&&r.view?.startsWith('agenda-')?'Bozza non ripristinabile dopo aggiornamento pagina. Nessun evento salvato: usa Nuovo evento, Duplica o la fascia desiderata.':'La schermata richiesta non è disponibile. Nessuna modifica salvata. Usa il menu per riaprire la scheda.';d.querySelector('.content,main')?.prepend(p);throw error;}finally{replaying=false;if(!disposed&&now===epoch)clean();}
 }
 function resolve(r,isCurrent){
  if(!r.view)return null;
  if(r.view==='client')return()=>win.RighettoCliente.open(r.id,r.tab);
  if(r.view==='client-edit')return()=>win.editCliente(r.id);
  if(r.view==='client-new')return()=>win.openClienteModal();
  if(r.view==='property-edit')return()=>{Promise.resolve(win.editImmobile(r.id,isCurrent)).then(()=>{if(isCurrent())clean();}).catch(error=>{if(isCurrent())console.error('Immobile non caricato',error);});};
  if(r.view==='mobile-property')return()=>win.RighettoMobileNavigation.openImm(r.id);
  // Agenda routes require the exact current event from its private event collection.
  if(r.view.startsWith('agenda-')&&win.RighettoAgenda?.restoreRoute)return()=>win.RighettoAgenda.restoreRoute(r,isCurrent);
  throw Error('Vista non ripristinabile in questa versione');
 }
 const api={hydratedControl(el,previous){if(!el||!baseline.has(el))return;if(baseline.get(el)===JSON.stringify(previous))baseline.set(el,JSON.stringify(value(el)));},saved(container){if(!container)return;container.querySelectorAll('input,textarea,select').forEach(x=>baseline.set(x,JSON.stringify(value(x))));const state=attachments();if(state&&attachmentBase){const old=JSON.parse(attachmentBase),now=JSON.parse(state);if(container.id==='clienteModal')old.client=now.client;if(container.id==='immobileForm')old.property=now.property;attachmentBase=JSON.stringify(old);}},allowClose(){if(win.RighettoPropertyReferences?.pending()||win.RighettoPropertyExtra?.pending()||win.RighettoLabels?.pending())return false;return replaying||!dirty()||win.confirm('Ci sono modifiche non salvate. Chiudere senza salvarle?');},get replaying(){return replaying;},clean,closeClientEditor(){const r=router.current;return api.open(r.view==='client-edit'&&r.id?{section:'clienti',view:'client',id:r.id,tab:r.tab||'scheda'}:{section:r.section});},open(route,action){if(disposed)return false;if(replaying&&action)return action();if(action&&!route.id)views.set(key(route),action);return router.navigate(route);},dispose(){disposed=true;epoch++;replaying=true;close();replaying=false;router.dispose();listeners.splice(0).forEach(fn=>fn());views.clear();baseline.clear();win.showSection=baseShow;if(baseShowById)win.showSectionById=baseShowById;delete win.RighettoNavigation;}};
 const section=()=>d.body.dataset.adminArea||d.querySelector('.section.active')?.id.slice(4)||'home';
 let initialHash='';try{initialHash=decodeURIComponent(win.location.hash.slice(1));}catch{}if(sections.has(initialHash))baseShow(initialHash);
 const previous=win.history.state?.righettoNav===1&&win.history.state.scope===scope&&valid(win.history.state.route)?win.history.state.route:null;
 router=createHistoryRouter({win,scope,read:()=>previous||({section:section()}),render,valid,dirty,confirmLeave:()=>{if(win.RighettoPropertyReferences?.pending()||win.RighettoPropertyExtra?.pending()){win.toast?.('Operazione sulla scheda in corso: attendi il risultato.','error');return false;}if(win.RighettoLabels?.pending()){win.toast?.('Operazione etichetta da verificare: rileggi prima di uscire.','error');return false;}return win.confirm('Ci sono modifiche non salvate. Uscire dalla schermata senza salvarle?');}});api.router=router;
 win.RighettoNavigation=api;win.showSection=name=>api.open({section:name});if(baseShowById)win.showSectionById=name=>api.open({section:name});
 // Capture phase runs before a close/menu handler can destroy unsaved controls.
 const editing=e=>{const el=e.target;if(el.matches('input,select,textarea')&&!el.closest('[data-property-history-filters]')&&el.closest('form,#clienteModal.open,.rcs,.ra-modal')&&!baseline.has(el))baseline.set(el,JSON.stringify(value(el)));};
 const closeTypes=()=>{const m=d.querySelector('.ra-types-modal');if(!m)return false;if(m.dataset.retirePending==='true')return true;if(api.allowClose()){m.remove();clean();d.querySelector('[data-action=types]')?.focus();}return true;};
 listen(d,'click',e=>{if(e.target.closest('.ra-types-modal [data-action=close]')){e.preventDefault();e.stopImmediatePropagation();closeTypes();return;}const transition=e.target.closest('.rcs [data-op=edit],.rcs [data-op=requestedit],.rcs [data-op=ev],.rcs [data-mobile-imm]');if(transition&&!api.allowClose()){e.preventDefault();e.stopImmediatePropagation();return;}const close=e.target.closest('[data-action=close],.rcs [data-x],#clienteModal .modal-close,#clienteModal [onclick*=closeClienteModal]');if(close||e.target.matches('.rcs')){e.preventDefault();e.stopImmediatePropagation();if(d.querySelector('#clienteModal.open'))api.closeClientEditor();else api.open({section:router.current.section});}},true);
 listen(d,'keydown',e=>{if(e.key==='Escape'&&d.querySelector('.ra-types-modal')){e.preventDefault();e.stopImmediatePropagation();closeTypes();return;}if(e.key==='Escape'&&d.querySelector('.ra-modal,.rcs,#clienteModal.open')){e.preventDefault();e.stopImmediatePropagation();if(d.querySelector('#clienteModal.open'))api.closeClientEditor();else api.open({section:router.current.section});}},true);
 listen(d,'focusin',editing,true);listen(d,'beforeinput',editing,true);listen(d,'pointerdown',editing,true);
 if(previous?.view)render(previous).catch(()=>{});else clean();return api;
}
