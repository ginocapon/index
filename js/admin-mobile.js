/* Admin su telefono: menu a grandi pulsanti, una sola sezione per volta, frecce per tornare.
   Solo presentazione (<=760px). Riusa le funzioni esistenti (editImmobile, editCliente, openClienteModal). */
(function(){
'use strict';
var mq=window.matchMedia('(max-width:760px)');
function phone(){return mq.matches;}
var cur='menu',remote=null,remoteQ='',tmr=null,remoteSeq=0,remoteState='',remoteError='',baseState='idle',baseError='';
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function money(n){return n?'€ '+Number(n).toLocaleString('it-IT'):'—';}
function $(s,r){return (r||document).querySelector(s);}
function photo(i){var f=Array.isArray(i.foto)&&i.foto.length?i.foto[0]:(i.foto_principale||'');return f&&!/^(https?:|\/|data:)/.test(f)?'/'+f:f;}
function photos(i){var a=Array.isArray(i.foto)?i.foto.slice():[];return a.map(function(f){return /^(https?:|\/|data:)/.test(f)?f:'/'+f;});}
function pretty(t){return String(t||'').replace(/_/g,' ');}
function tipoLabel(t){return t==='vendita'?'Vendita':String(t||'').indexOf('affitto')===0?'Affitto':t==='asta_giudiziaria'?'Asta':(t||'');}
function stato(i){return i.venduto?['Venduto','r']:i.affittato?['Affittato','r']:i.attivo?['Attivo','g']:['Non attivo','n'];}

var IC={immobili:'<path d="M3 11l9-8 9 8v10H3z"/><path d="M9 21v-6h6v6"/>',clienti:'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',agenda:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',aste:'<path d="M12 3v18M6 21h12M4 7h16M4 7l-2 7a3 3 0 0 0 6 0zM20 7l-2 7a3 3 0 0 0 6 0z"/>',perizie:'<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/>',documentigenerali:'<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5"/>',richieste:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',blog:'<path d="M4 4h16v16H4z"/><path d="M8 9h8M8 13h8M8 17h5"/>',emailmarketing:'<path d="M3 11v3l14 5V6zM17 9a3 3 0 0 1 0 6M6 15v4"/>',landing:'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 14h6"/>',impostazioni:'<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',web:'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',logout:'<path d="M9 4H4v16h5M16 8l4 4-4 4M20 12H9"/>'};
function icon(k){return '<svg class="rm-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'+IC[k]+'</svg>';}
var MENU=[['immobili','immobili','Immobili'],['clienti','clienti','Clienti'],['agenda','agenda','Agenda'],['attivita','documentigenerali','Attività'],['aste','aste','Aste'],['perizie','perizie','Perizie'],['documentigenerali','documentigenerali','Documenti'],['richieste','richieste','Richieste'],['blog','blog','Blog'],['emailmarketing','emailmarketing','Email marketing'],['landing','landing','Landing pages'],['impostazioni','impostazioni','Impostazioni']];
var TITLES={immobili:'Immobili',nuovo:'Immobile',clienti:'Clienti',agenda:'Agenda',attivita:'Attività',aste:'Aste',perizie:'Perizie',documentigenerali:'Documenti',richieste:'Richieste',blog:'Blog',emailmarketing:'Email marketing',landing:'Landing pages',impostazioni:'Impostazioni',analytics:'Search Console'};

var head,menu,scheda;
function build(){
 head=document.createElement('div');head.id='rm-head';
 head.innerHTML='<button type="button" id="rm-back" aria-label="Indietro">←</button><div id="rm-title">Righetto</div><button type="button" id="rm-prev" aria-label="Argomento precedente">‹</button><button type="button" id="rm-next" aria-label="Argomento successivo">›</button>';
 document.body.appendChild(head);
 menu=document.createElement('div');menu.id='rm-menu';
 menu.innerHTML='<div class="rm-brand"><div class="rm-logo">R</div><div><b>Righetto Immobiliare</b><span>Gestione</span></div></div>'+MENU.map(function(m){return '<button type="button" class="rm-big" data-go="'+m[0]+'">'+icon(m[1])+m[2]+'</button>';}).join('')+'<div id="rm-session" class="rm-sess"></div><a class="rm-big rm-alt" href="/">'+icon("web")+'Vai al sito</a><button type="button" class="rm-big rm-alt" data-go="__logout">'+icon("logout")+'Esci</button>';
 document.body.appendChild(menu);
 scheda=document.createElement('div');scheda.id='rm-scheda';scheda.hidden=true;document.body.appendChild(scheda);
 menu.addEventListener('click',function(e){var b=e.target.closest('[data-go]');if(!b)return;var g=b.dataset.go;if(g==='__logout'){if(window.doLogout)window.doLogout();return;}go(g);});
 $('#rm-back').onclick=back;$('#rm-prev').onclick=function(){step(-1);};$('#rm-next').onclick=function(){step(1);};
}
function go(name){
 closeScheda();
 if(name==='menu'||name==='home'){cur='menu';render();return;}
 cur=name;render();
 window.__rmOrig((name==='agenda'||name==='attivita')?'agenda':name);
 render();
 if(name==='immobili')setTimeout(cardsImm,60);
 if(name==='clienti')setTimeout(cardsCli,400);
}
function step(d){var ids=MENU.map(function(m){return m[0];});var k=ids.indexOf(cur==='nuovo'?'immobili':cur);if(k<0)k=0;go(ids[(k+d+ids.length)%ids.length]);}
function back(){
 if(!scheda.hidden){closeScheda();return;}
 if(cur==='nuovo'){go('immobili');return;}
 go('menu');
}
function render(){
 var on=phone();
 document.body.classList.toggle('rm-on',on);
 if(!on){return;}
 document.body.classList.toggle('rm-menu-open',cur==='menu');
 document.body.classList.toggle('rm-agenda',cur==='agenda'||cur==='attivita');document.body.classList.toggle('rm-attivita',cur==='attivita');
 document.body.classList.toggle('rm-sec-'+'immobili',cur==='immobili');
 document.body.classList.toggle('rm-sec-clienti',cur==='clienti');
 $('#rm-title').textContent=cur==='menu'?'Righetto Immobiliare':(TITLES[cur]||cur);
 $('#rm-back').style.visibility=cur==='menu'?'hidden':'visible';
 $('#rm-prev').style.visibility=$('#rm-next').style.visibility=cur==='menu'?'hidden':'visible';
}
/* ---------- Immobili ---------- */
function ensureBox(secId,boxId,ph,newLabel,newFn){
 var sec=document.getElementById(secId);if(!sec)return null;
 var box=document.getElementById(boxId);
 if(!box){box=document.createElement('div');box.id=boxId;box.className='rm-box';
  box.innerHTML='<input type="search" class="rm-search" placeholder="'+ph+'"><div class="rm-count"></div><div class="rm-cards"></div><div class="rm-bar"><button type="button" class="rm-bar1">+ '+newLabel+'</button></div>';
  sec.insertBefore(box,sec.firstChild);
  $('.rm-search',box).addEventListener('input',function(){if(boxId==='rm-imm')cardsImm();else cardsCli();});
  $('.rm-bar1',box).onclick=newFn;
  var isI=boxId==='rm-imm',key=isI?'__rCestino':'__rStorico',lab=document.createElement('label');
  lab.className='rm-tg';lab.style.cssText='display:flex;align-items:center;gap:8px;margin:6px 2px;font:600 .85rem Montserrat,Arial,sans-serif';
  lab.innerHTML='<input type="checkbox"> '+(isI?'Mostra cestino':'Mostra storico');
  lab.querySelector('input').addEventListener('change',function(e){window[key]=e.target.checked;remote=null;remoteQ='';var f=isI?window.loadImmobili:window.loadClienti;Promise.resolve(f&&f()).then(function(){if(isI)cardsImm();else cardsCli();});});
  box.insertBefore(lab,$('.rm-count',box));}
 return box;}
function cardsImm(){
 if(!phone())return;
 var box=ensureBox('sec-immobili','rm-imm','Cerca codice, comune, indirizzo…','Nuovo immobile',function(){window.__rmOrig('nuovo');cur='nuovo';render();});
 if(!box||typeof allImmobili==='undefined')return;
 var q=$('.rm-search',box).value.trim().toLowerCase();
 var list=allImmobili.filter(function(i){if(!q)return true;var nz=function(v){return String(v==null?'':v).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');};var hay=nz([i.codice,String(i.codice||'').replace(/[\s.\-_\/]+/g,''),i.titolo,i.comune,i.indirizzo,i.proprietario_nome,i.prezzo].join(' '));return nz(q).split(/[\s,;]+/).filter(Boolean).every(function(w){return hay.indexOf(w)>=0||hay.indexOf(w.replace(/[\s.\-_\/]+/g,''))>=0;});});
 $('.rm-count',box).textContent=list.length+' immobili';
 $('.rm-cards',box).innerHTML=list.slice(0,150).map(function(i){var s=stato(i),p=photo(i);
  return '<button type="button" class="rm-card" data-id="'+esc(i.id)+'"><div class="rm-ph">'+(p?'<img loading="lazy" src="'+esc(p)+'" alt="" onerror="this.remove()">':'<span>📷</span>')+'</div><div class="rm-inf"><div class="rm-r1"><b>'+esc(i.codice||'—')+'</b><em class="rm-chip '+s[1]+'">'+s[0]+'</em></div><div class="rm-t">'+esc(i.titolo||(i.tipologia||'')+' '+(i.comune||''))+'</div><div class="rm-s">'+esc([i.comune,i.indirizzo].filter(Boolean).join(' · '))+'</div><div class="rm-r2"><strong>'+money(i.prezzo)+'</strong><span>'+(i.superficie?esc(i.superficie)+' mq':'')+'</span><span>'+esc(tipoLabel(i.tipo_operazione))+'</span></div></div></button>';}).join('')+(list.length>150?'<div class="rm-more">Altri '+(list.length-150)+': usa la ricerca.</div>':'');
}
function field(l,v){return v===null||v===undefined||v===''||v===false?'':'<div class="rm-f"><label>'+l+'</label><div>'+esc(v===true?'Sì':v)+'</div></div>';}
function openImm(id){
 var i=(typeof allImmobili!=='undefined'?allImmobili:[]).find(function(x){return String(x.id)===String(id);});if(!i)return;
 var ph=photos(i),s=stato(i);
 var dati=field('Codice',i.codice)+field('Tipo',tipoLabel(i.tipo_operazione))+field('Tipologia',i.tipologia)+field('Prezzo',i.prezzo?money(i.prezzo):'')+field('Superficie',i.superficie?i.superficie+' mq':'')+field('Locali',i.locali)+field('Camere',i.camere)+field('Bagni',i.bagni)+field('Piano',i.piano)+field('Comune',i.comune)+field('Indirizzo',i.indirizzo)+field('Classe energetica',i.classe_energetica)+field('Spese condominio',i.spese_condominio)+field('Descrizione',i.descrizione);
 var dot=['ascensore','garage','giardino','terrazzo','cantina','arredato','aria_condizionata','posto_auto'].filter(function(k){return i[k];}).map(function(k){return k.replace(/_/g,' ');});
 var prop='<div id="rm-own">'+field('Proprietario',i.proprietario_nome&&i.proprietario_nome!=='--'?i.proprietario_nome:'')+field('Telefono',i.proprietario_tel)+field('Email',i.proprietario_email)+'</div>'+field('Note interne',i.note_interne)+field('Chiavi agenzia',i.chiavi_agenzia?'Sì':'');
 scheda.innerHTML='<div class="rm-banner"><b>'+esc(i.codice||'')+' '+esc(i.titolo||'')+'</b><em class="rm-chip '+s[1]+'">'+s[0]+'</em></div><div class="rm-tabs"><button type="button" class="on" data-t="d">Dettagli</button><button type="button" data-t="f">Foto ('+ph.length+')</button><button type="button" data-t="p">Proprietà</button></div>'+
 '<div class="rm-pane" data-p="d">'+(ph[0]?'<img class="rm-hero" src="'+esc(ph[0])+'" alt="">':'')+dati+(dot.length?'<div class="rm-tags">'+dot.map(function(d){return '<span>'+esc(d)+'</span>';}).join('')+'</div>':'')+'</div>'+
 '<div class="rm-pane" data-p="f" hidden>'+(ph.length?ph.map(function(f){return '<img class="rm-hero" loading="lazy" src="'+esc(f)+'" alt="">';}).join(''):'<p class="rm-empty">Nessuna foto.</p>')+'</div>'+
 '<div class="rm-pane" data-p="p" hidden>'+(prop||'<p class="rm-empty">Nessun dato.</p>')+'</div>'+
 '<div class="rm-bar"><button type="button" data-a="edit">Modifica</button><button type="button" data-a="ops">Operazioni</button><button type="button" data-a="trash">'+(i.cestino?'Ripristina':'Cestino')+'</button>'+(i.proprietario_tel?'<a href="tel:'+esc(String(i.proprietario_tel).replace(/\s+/g,''))+'">Chiama</a>':'')+(i.slug?'<a href="/immobile/'+esc(i.slug)+'" target="_blank" rel="noopener">Sito</a>':'')+'</div>';
 if(i.proprietario_id&&typeof sb!=='undefined')sb.from('clienti').select('id,nome,telefono,email,ragione_sociale').eq('id',i.proprietario_id).limit(1).then(function(r){var o=r.data&&r.data[0],box=document.getElementById('rm-own');if(!o||!box)return;var ph=phones(o.telefono);box.innerHTML=field('Proprietario',o.nome)+(o.ragione_sociale?field('Azienda',o.ragione_sociale):'')+field('Telefono',o.telefono)+field('Email',o.email)+((ph.length||o.email)?'<div class="rm-acts">'+ph.slice(0,2).map(function(n){return '<a href="tel:'+esc(n)+'">Chiama '+esc(n)+'</a>';}).join('')+(o.email?'<a href="mailto:'+esc(o.email)+'">eMail</a>':'')+'<button type="button" data-own="'+esc(o.id)+'">Scheda cliente</button></div>':'<p class="rm-warn">Il proprietario non ha telefono né email nei dati importati.</p>');}).catch(function(){});
 showScheda(function(a){if(a==='trash'){var fn=i.cestino?window.restoreImmobile:window.deleteImmobile;if(fn)Promise.resolve(fn(i.id,i.titolo||'')).then(function(){closeScheda();cardsImm();});return;}if(a==='ops'){if(window.RighettoImmobileOperazioni&&RighettoImmobileOperazioni.openMenu)RighettoImmobileOperazioni.openMenu(i);return;}if(a==='edit'){closeScheda();cur='nuovo';render();window.__rmOrig('nuovo');editImmobile(i.id);}});
}
function showScheda(onAct){
 scheda.hidden=false;scheda.scrollTop=0;document.body.classList.add('rm-scheda-open');
 scheda.onclick=function(e){var t=e.target.closest('[data-t]');if(t){scheda.querySelectorAll('[data-t]').forEach(function(x){x.classList.toggle('on',x===t);});scheda.querySelectorAll('[data-p]').forEach(function(p){p.hidden=p.dataset.p!==t.dataset.t;});return;}var a=e.target.closest('[data-a]');if(a)onAct(a.dataset.a);};
}
function closeScheda(){if(!scheda)return;scheda.hidden=true;document.body.classList.remove('rm-scheda-open');}
/* ---------- Clienti ---------- */
function listCli(q){
 if(!q||q.length<2)return allClienti;
 if(remote&&remoteQ===q)return remote;
 return allClienti.filter(function(c){return [c.nome,c.ragione_sociale,c.telefono,c.email,c.partita_iva,c.indirizzo_cliente].join(' ').toLowerCase().indexOf(q)>=0;});
}
function remoteSearch(q){
 if(typeof sb==='undefined'||q.length<2||q.replace(/[,()%*]/g,'').length<2)return;
 var seq=++remoteSeq, t=q.replace(/[,()%*\\]/g,' ').trim();
 var f=['nome','email','telefono','ragione_sociale','partita_iva','codice_fiscale','indirizzo_cliente','nome_proprio','cognome','comune','cellulare'].map(function(k){return k+'.ilike.%'+t+'%';}).join(',');
 remoteState='loading';remoteError='';remote=null;remoteQ=q;cardsCli(true);
 sb.from('clienti').select('*').or(f).eq('storico',!!window.__rStorico).order('nome').limit(150).then(function(r){
  if(seq!==remoteSeq)return;
  if(r.error){remoteState='error';remoteError=r.error.message||'Riprovare la ricerca';remote=null;}
  else{remoteState='ready';remote=r.data||[];}cardsCli(true);
 }).catch(function(e){if(seq!==remoteSeq)return;remoteState='error';remoteError=e.message||'Riprovare la ricerca';cardsCli(true);});
}
function cardsCli(fromRemote){
 if(!phone())return;
 var box=ensureBox('sec-clienti','rm-cli','Cerca nome, telefono, email…','Nuovo cliente',function(){if(window.openClienteModal)window.openClienteModal();});
 if(!box||typeof allClienti==='undefined')return;
 var q=$('.rm-search',box).value.trim().toLowerCase();
 if(!fromRemote){clearTimeout(tmr);remoteSeq++;remote=null;remoteQ='';remoteState='';remoteError='';if(q.length>=2){remoteState='loading';tmr=setTimeout(function(){remoteSearch(q);},350);}}
 var waiting=q.length>=2?remoteState==='loading':baseState==='loading';
 var error=q.length>=2?remoteError:baseError;
 if(waiting||error){$('.rm-count',box).setAttribute('role','status');$('.rm-count',box).textContent=error?'Clienti non leggibili: '+error:'Caricamento clienti…';$('.rm-cards',box).replaceChildren();return;}
 if(q.length<2&&baseState==='idle'&&!allClienti.length){$('.rm-count',box).textContent='Caricamento clienti…';$('.rm-cards',box).replaceChildren();return;}
 var list=listCli(q);
 var tot=(q.length>=2&&remote&&remoteQ===q)?' trovati su tutto l\'archivio':' (primi '+allClienti.length+' dell\'elenco, scrivi per cercare in tutti)';
 $('.rm-count',box).textContent=(q.length<2&&typeof clientiTotal!=='undefined'?'Archivio: '+clientiTotal+' clienti · '+list.length+' in questa pagina':list.length+' clienti')+(q.length>=2?(remote&&remoteQ===q?' trovati su tutto l\'archivio':''):' · scrivi per cercare in tutto l\'archivio');
 $('.rm-cards',box).innerHTML=list.slice(0,150).map(function(c){var cerca=[pretty(c.tipo_operazione_cercata),c.tipologia_cercata,c.zona_cercata].filter(Boolean).join(' · ');
  return '<button type="button" class="rm-card rm-cc" data-id="'+esc(c.id)+'"><div class="rm-inf"><div class="rm-r1"><b>'+esc(c.nome||'(senza nome)')+'</b><em class="rm-chip n">'+esc(c.storico?'Storico':(c.ruolo_rubrica||''))+'</em></div><div class="rm-s">'+esc([c.telefono,c.email].filter(Boolean).join(' · ')||'nessun recapito')+'</div>'+(cerca?'<div class="rm-s">'+esc(cerca)+'</div>':'')+'</div></button>';}).join('')+(list.length>150?'<div class="rm-more">Altri '+(list.length-150)+': affina la ricerca.</div>':'');
 if(q.length<2&&typeof clientiPage!=='undefined'&&typeof clientiTotal!=='undefined'){var pages=Math.max(1,Math.ceil(clientiTotal/clientiPageSize));$('.rm-cards',box).insertAdjacentHTML('beforeend','<nav class="rm-pages" aria-label="Pagine clienti"><button type="button" data-client-page="'+(clientiPage-1)+'" '+(clientiPage===0?'disabled':'')+'>Precedente</button><span>Pagina '+(clientiPage+1)+' di '+pages+'</span><button type="button" data-client-page="'+(clientiPage+1)+'" '+(clientiPage>=pages-1?'disabled':'')+'>Successiva</button></nav>');}
}
function linked(c){
 var l=(typeof allImmobili!=='undefined'?allImmobili:[]).filter(function(i){return String(i.proprietario_id)===String(c.id);});
 if(!l.length)return '<p class="rm-empty">Nessun immobile collegato come proprietario.</p>';
 return l.map(function(i){return '<button type="button" class="rm-link" data-imm="'+esc(i.id)+'"><b>'+esc(i.codice||'')+'</b> '+esc(i.titolo||'')+'<br><span>'+money(i.prezzo)+(i.superficie?' · '+esc(i.superficie)+' mq':'')+'</span></button>';}).join('');
}
function phones(t){return (String(t||'').match(/\+?\d[\d ]{6,}\d/g)||[]).map(function(x){return x.replace(/\s+/g,'');});}
function openCli(id){
 if(window.RighettoCliente&&typeof window.RighettoCliente.open==='function'){closeScheda();window.RighettoCliente.open(id);return;}
 var c=(listCli(($('#rm-cli .rm-search')||{value:''}).value.trim().toLowerCase())||[]).find(function(x){return String(x.id)===String(id);})||allClienti.find(function(x){return String(x.id)===String(id);});if(!c)return;
 var tel=String(c.telefono||'').replace(/\s+/g,'');
 var dati=field('Tipo',c.tipo_cliente)+field('Telefono',c.telefono)+field('Email',c.email)+field('PEC',c.pec)+field('Indirizzo',c.indirizzo_cliente)+field('Ragione sociale',c.ragione_sociale)+field('P.IVA',c.partita_iva)+field('Codice fiscale',c.codice_fiscale)+field('SDI',c.sdi)+field('Fonte',c.fonte);
 var cerca=field('Operazione',c.tipo_operazione_cercata)+field('Tipologia',c.tipologia_cercata)+field('Zona',c.zona_cercata)+field('Budget min',c.budget_min?money(c.budget_min):'')+field('Budget max',c.budget_max?money(c.budget_max):'')+field('Superficie min',c.superficie_min)+field('Camere min',c.camere_min)+field('Interesse',c.interesse);
 scheda.innerHTML='<div class="rm-banner"><b>'+esc(c.nome||'')+'</b><em class="rm-chip n">'+esc(c.ruolo_rubrica||'')+'</em></div><div class="rm-tabs"><button type="button" class="on" data-t="d">Dettagli</button><button type="button" data-t="r">Cerca</button><button type="button" data-t="n">Note</button><button type="button" data-t="i">Immobili</button></div>'+
 '<div class="rm-pane" data-p="d">'+((c.telefono||c.email)?'':'<p class="rm-warn">Nessun telefono né email nei dati importati.</p>')+(dati||'<p class="rm-empty">Nessun dato.</p>')+'</div><div class="rm-pane" data-p="r" hidden>'+(cerca||'<p class="rm-empty">Nessuna richiesta.</p>')+'</div><div class="rm-pane" data-p="i" hidden>'+linked(c)+'</div><div class="rm-pane" data-p="n" hidden>'+(c.note?'<div class="rm-f"><label>Nota</label><div>'+esc(c.note)+'</div></div>':'')+'<div class="rm-f"><label>Cronistoria note</label><div id="rm-crn"></div><textarea id="rm-crn-t" rows="3" placeholder="Nuova nota…" style="width:100%;margin-top:8px;padding:10px;border:1.5px solid #b9c8d8;border-radius:10px;font:inherit"></textarea><button type="button" id="rm-crn-add" style="margin-top:8px;padding:10px 16px;border:0;border-radius:10px;background:#1f6fb2;color:#fff;font-weight:700">Aggiungi nota</button></div></div>'+
 '<div class="rm-bar"><button type="button" data-a="edit">Modifica</button><button type="button" data-a="sto">'+(c.storico?'Riporta attivo':'Storico')+'</button>'+(tel?'<a href="tel:'+esc(tel)+'">Chiama</a>':'')+(tel?'<a href="https://wa.me/'+esc(tel.replace(/^\+/,'').replace(/^00/,'').replace(/^(?!39)/,'39'))+'" target="_blank" rel="noopener">WhatsApp</a>':'')+(c.email?'<a href="mailto:'+esc(c.email)+'">eMail</a>':'')+'</div>';
 (function(){var el=document.getElementById('rm-crn');if(!el||typeof sb==='undefined')return;function ld(){sb.from('cliente_cronistoria').select('creato_il,tipo,testo,autore').eq('cliente_id',c.id).order('creato_il',{ascending:false}).limit(200).then(function(r){var e=document.getElementById('rm-crn');if(!e)return;if(r.error){e.textContent='Cronistoria non leggibile: '+r.error.message;return;}e.innerHTML=(r.data&&r.data.length)?r.data.map(function(x){return '<div style="border-top:1px solid #e3e8ee;padding:8px 0"><b style="font-size:.8rem;color:#5a6b7d">'+esc(x.creato_il?new Date(x.creato_il).toLocaleString('it-IT'):'')+(x.autore?' · '+esc(x.autore):'')+'</b><div>'+esc(x.testo)+'</div></div>';}).join(''):'<p class="rm-empty">Nessuna nota ancora.</p>';});}ld();document.getElementById('rm-crn-add').onclick=function(){var ta=document.getElementById('rm-crn-t'),t=ta.value.trim();if(!t)return;sb.auth.getUser().then(function(u){return sb.from('cliente_cronistoria').insert([{cliente_id:c.id,tipo:'nota',testo:t,autore:(u.data&&u.data.user&&u.data.user.email)||null}]);}).then(function(r){if(r&&r.error){alert('Nota non salvata: '+r.error.message);return;}ta.value='';ld();});};})();
 showScheda(function(a){if(a==='sto'){var to=!c.storico;if(!confirm(to?'Mettere questo cliente nello storico?\n\nNon viene cancellato: esce dall\'elenco normale e resta in "Mostra storico".':'Riportare questo cliente tra gli attivi?'))return;sb.from('clienti').update({storico:to,storico_il:to?new Date().toISOString():null}).eq('id',c.id).then(function(r){if(r&&r.error){alert('Operazione non riuscita: '+r.error.message);return;}remote=null;remoteQ='';closeScheda();Promise.resolve(window.loadClienti&&window.loadClienti()).then(function(){cardsCli();});});return;}if(a==='edit'){closeScheda();if(window.editCliente)window.editCliente(c.id);}});
}
/* Accesso su telefono: vale 12 ore da quando si inserisce la password. */
var SESSION_HOURS=12,STAMP='rig_login_at',logging=false;
function sessionCheck(){
 if(logging||!phone()||typeof sb==='undefined'||!sb.auth)return;
 sb.auth.getSession().then(function(r){
  if(!r||!r.data||!r.data.session)return;
  var at=Number(localStorage.getItem(STAMP)||0);
  if(!at||Date.now()-at>SESSION_HOURS*3600000){
   localStorage.removeItem(STAMP);
   Promise.resolve(sb.auth.signOut()).catch(function(){}).then(function(){location.reload();});
   return;
  }
  var h=Math.max(0,Math.ceil((at+SESSION_HOURS*3600000-Date.now())/3600000)),el=document.getElementById('rm-session');
  if(el)el.textContent='Accesso valido ancora circa '+h+(h===1?' ora':' ore');
 }).catch(function(){});
}
function initSession(){
 if(typeof window.doLogin==='function'){var od=window.doLogin;window.doLogin=function(){logging=true;return Promise.resolve(od.apply(this,arguments)).then(function(v){if(phone()&&typeof sb!=='undefined')return sb.auth.getSession().then(function(r){if(r&&r.data&&r.data.session)localStorage.setItem(STAMP,String(Date.now()));return v;});return v;}).catch(function(e){throw e;}).finally(function(){logging=false;});};}
 sessionCheck();setInterval(sessionCheck,60000);
 document.addEventListener('visibilitychange',function(){if(!document.hidden)sessionCheck();});
 window.addEventListener('focus',sessionCheck);
}
function init(){
 build();initSession();
 window.addEventListener('righetto:mobile-immobile',function(e){if(phone()&&e.detail&&e.detail.id){cur='immobili';render();openImm(e.detail.id);}});
 window.addEventListener('righetto:clienti-load',function(e){var d=e.detail||{};if(d.state==='loading'){baseState='loading';baseError='';}else if(d.state==='error'){baseState='error';baseError=d.message;}else if(baseState!=='error'){baseState='ready';}if(cur==='clienti')cardsCli(true);});
 var oldShow=window.showSection;window.__rmOrig=oldShow;
 window.showSection=function(name){
  if(!phone()){oldShow(name);render();return;}
  if(name==='home'){go('menu');return;}
  if(name===cur&&name!=='menu'){oldShow(name);render();return;}
  cur=name;render();oldShow(name);render();
  if(name==='immobili')setTimeout(cardsImm,60);
  if(name==='clienti')setTimeout(cardsCli,400);
 };
 document.addEventListener('click',function(e){
  var page=e.target.closest('#rm-cli [data-client-page]');if(page){if(!page.disabled)window.loadClienti(Number(page.dataset.clientPage));return;}
  var c=e.target.closest('#rm-imm .rm-card');if(c){openImm(c.dataset.id);return;}
  c=e.target.closest('#rm-cli .rm-card');if(c){openCli(c.dataset.id);}
  c=e.target.closest('#rm-scheda [data-imm]');if(c){openImm(c.dataset.imm);return;}
  c=e.target.closest('#rm-scheda [data-own]');if(c){var oid=c.dataset.own;if(allClienti.find(function(x){return String(x.id)===String(oid);})){openCli(oid);}else if(typeof sb!=='undefined'){sb.from('clienti').select('*').eq('id',oid).limit(1).then(function(r){if(r.data&&r.data[0]){allClienti.push(r.data[0]);openCli(oid);}});}}
 });
 [['immobiliTableWrap',cardsImm],['clientiTable',cardsCli]].forEach(function(p){var el=document.getElementById(p[0]);if(el)new MutationObserver(function(){setTimeout(p[1],30);}).observe(el,{childList:true,subtree:true});});
 mq.addEventListener?mq.addEventListener('change',function(){cur='menu';render();}):0;
 cur='menu';render();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){setTimeout(init,0);});else setTimeout(init,0);
})();
