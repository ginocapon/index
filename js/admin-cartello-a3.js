/* Cartello A3 v4. Local-only composer. No account, database or storage writes. */
(function(global){
'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const present=v=>v!==null&&v!==undefined&&v!=='';
const positive=v=>present(v)&&Number.isFinite(Number(v))&&Number(v)>0;
const words=v=>String(v||'').trim().split(/\s+/u).filter(Boolean).length;
const number=v=>Number(String(v).replace(',','.'));
const safeURL=v=>{try{const u=new URL(v,location.href);return /^https?:$/.test(u.protocol)&&!u.username&&!u.password?u.href:null;}catch{return null;}};
const typeOf=i=>String(i.tipologia||'Immobile').replace(/_/g,' ');
const residential=i=>!/capannone|negozio|ufficio|terreno|magazzino/i.test(typeOf(i));
function precise(i){
 // Closed vocabulary only. Text is evidence, never executable HTML or instructions.
 const d=String(i.descrizione||'').toLowerCase();
 return {central:/posizione centrale|zona centrale|centralissim/.test(d),privateGarden:i.giardino===true&&/giardino privato/.test(d),separateKitchen:i.cucina===true&&/cucina separata|cucina abitabile separata/.test(d)};
}
function title(i){
 const f=precise(i),a=[String(i.comune||'').toUpperCase()];
 if(f.central)a.push('posizione centrale');
 let unit=typeOf(i).toLowerCase();
 if(residential(i)&&(i.piano_terra===true||String(i.piano||'').toLowerCase()==='piano terra'))unit+=' al piano terra';
 const extra=[];if(i.ingresso_indipendente===true)extra.push('ingresso indipendente');if(i.giardino===true)extra.push('giardino'+(f.privateGarden?' privato':''));
 if(extra.length)unit+=' con '+extra.join(' e ');a.push(unit);return a.filter(Boolean).join(', ');
}
function facts(i){
 const a=[];const add=(value,label)=>a.push({value:String(value),label});
 if(positive(i.superficie))add(i.superficie+' m²','Superficie');
 if(residential(i)&&positive(i.camere))add(i.camere+(Number(i.camere)===1?' camera':' camere'),'Zona notte');
 if(positive(i.bagni))add(i.bagni+(Number(i.bagni)===1?' bagno':' bagni'),'Comfort');
 if(i.cucina===true)add('Cucina',precise(i).separateKitchen?'Separata':'Presente');
 if(i.taverna===true)add('Taverna','Spazio aggiuntivo');
 if(positive(i.garage_doppio))add('Garage','Doppio');else if(i.garage===true||positive(i.garage_num))add('Garage','Presente');
 if(i.giardino===true)add('Giardino','Presente');
 if(i.terrazzo===true)add('Terrazzo','Presente');
 if(i.ingresso_indipendente===true)add('Ingresso','Indipendente');
 if(positive(i.locali))add(i.locali+' locali','Ambienti');
 return a.slice(0,6);
}
function copy(i){
 const type=typeOf(i),parts=[];let lead=type.charAt(0).toUpperCase()+type.slice(1);
 if(i.comune)lead+=' a '+String(i.comune).trim();
 if(i.tipo_operazione==='vendita')lead+=' in vendita';else if(String(i.tipo_operazione||'').startsWith('affitto'))lead+=' in affitto';
 if(positive(i.superficie))lead+=' di '+i.superficie+' m²';
 parts.push(lead);
 const rooms=[];if(residential(i)&&positive(i.camere))rooms.push(i.camere+(Number(i.camere)===1?' camera':' camere'));
 if(positive(i.bagni))rooms.push(i.bagni+(Number(i.bagni)===1?' bagno':' bagni'));
 if(rooms.length)parts.push('con '+rooms.join(' e '));
 if(i.ingresso_indipendente===true)parts.push('ingresso indipendente');
 if(i.giardino===true)parts.push('giardino');if(i.taverna===true)parts.push('taverna');
 if(positive(i.garage_doppio))parts.push('garage doppio');else if(i.garage===true)parts.push('garage');
 const calls=[
 'Contatta la nostra agenzia immobiliare Righetto Immobiliare per ricevere maggiori informazioni su questo immobile e concordare una visita.',
 'Per informazioni su questo immobile, contatta Righetto Immobiliare.',
 'Per maggiori informazioni su questo immobile, contatta Righetto Immobiliare.',
 'Per maggiori informazioni e per concordare una visita, contatta Righetto Immobiliare.',
 'Per ricevere maggiori informazioni e concordare una visita, contatta direttamente Righetto Immobiliare.',
 'Per ricevere maggiori informazioni su questo immobile e concordare una visita, contatta Righetto Immobiliare.',
 'Per ricevere maggiori informazioni su questo immobile e concordare una visita, contatta direttamente Righetto Immobiliare.',
 'Per ricevere maggiori informazioni su questo immobile e concordare una visita, contatta la nostra agenzia Righetto Immobiliare.',
 'Contatta Righetto Immobiliare per informazioni.',
 'Contatta Righetto Immobiliare per maggiori informazioni.',
 'Contatta Righetto Immobiliare per ricevere maggiori informazioni.',
 'Contatta Righetto Immobiliare per ricevere informazioni su questo immobile.',
 'Contatta Righetto Immobiliare per ricevere maggiori informazioni su questo immobile.',
 'Contatta Righetto Immobiliare per ricevere maggiori informazioni e concordare una visita.',
 'Contatta Righetto Immobiliare per ricevere maggiori informazioni su questo immobile e concordare una visita.',
 'Per maggiori informazioni su questo immobile e per concordare una visita, contatta direttamente la nostra agenzia Righetto Immobiliare.',
 'Per ricevere maggiori informazioni su questo immobile e per concordare una visita, contatta direttamente la nostra agenzia Righetto Immobiliare.',
 'Per ricevere tutte le informazioni su questo immobile e per concordare una visita, puoi contattare direttamente la nostra agenzia Righetto Immobiliare.',
 'Per ricevere tutte le informazioni su questo immobile e per concordare una visita, puoi contattare direttamente la nostra agenzia immobiliare Righetto Immobiliare.'
 ];
 // Only choose complete factual clauses and complete contact sentences, never truncate text.
 for(let n=parts.length;n>0;n--){const core=parts.slice(0,n).join(', ')+'.';for(const call of calls){const text=core+' '+call;if(words(text)===30)return text;}}
 throw Error('Testo standard di 30 parole non disponibile per questa scheda. Segnalare senza inventare dati.');
}
function initialEnergy(i){
 return {className:present(i.classe_energetica)?String(i.classe_energetica):'',nren:present(i.epgl_nren)?String(i.epgl_nren):'',ren:present(i.epgl_ren)?String(i.epgl_ren):''};
}
function addressError(text,i){
 // The public copy never starts from the saved description or title. Also guard user edits.
 const raw=String(i.indirizzo||'').trim().toLowerCase();
 return !!(raw.length>5&&String(text).toLowerCase().includes(raw))||/\b(via|viale|vicolo|piazza|piazzale|strada|corso|civico)\s+[\p{L}\d]/iu.test(text)||/\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b/i.test(text)||/(?:\+?39\s*)?\b3\d{2}[\s.-]?\d{3}[\s.-]?\d{3,4}\b/.test(text);
}
function noApe(i){return String(i.codice||'').trim()==='LO0287';}
function validate(i,s){
 const errors=[];
 if(!Array.isArray(s.photos)||s.photos.length!==2||new Set(s.photos).size!==2)errors.push('Scegli esattamente 2 foto diverse dell’immobile.');
 const allowed=new Set((Array.isArray(i.foto)&&i.foto.length?i.foto:i.foto_urls||[]).filter(x=>typeof x==='string').map(safeURL).filter(Boolean));
 if(s.photos?.some(x=>!allowed.has(x)))errors.push('Una foto non appartiene alla scheda aperta.');
 if(!String(s.title||'').trim())errors.push('Titolo mancante.');
 if(!String(s.description||'').trim()||words(s.description)>30)errors.push('La descrizione deve contenere da 1 a 30 parole.');
 if(addressError(s.title+' '+s.description,i))errors.push('Rimuovi indirizzo, contatti personali o dati riservati dal testo.');
 if(!positive(i.prezzo))errors.push('Prezzo salvato mancante o non valido. Chiedi a Gino.');
 if(!noApe(i)&&(!s.apeSrc||(!s.apeVerified&&!s.sourceAsIs)))errors.push('APE non completa per questo cartello: '+(s.energyMissing||'immagine e valori esatti non collegati')+'.');
 if(!noApe(i)&&!s.sourceAsIs&&!/^(?:A[1-4]|[B-G])$/.test(s.energy?.className||''))errors.push('Classe energetica esatta mancante.');
 for(const [key,label]of [['nren','EPgl,nren'],['ren','EPgl,ren']])if(!noApe(i)&&!s.sourceAsIs&&(!present(s.energy?.[key])||!Number.isFinite(number(s.energy[key]))||number(s.energy[key])<0))errors.push(label+' esatto mancante o non valido. IPE non viene convertito.');
 if(!s.factsVerified)errors.push('Conferma il testo e le voci confrontandoli con la scheda.');
 return errors;
}
const sheetCSS=`@page{size:420mm 297mm;margin:0}*{box-sizing:border-box}body{margin:0;background:white;font-family:"Noto Sans Condensed","Arial Narrow",Arial,sans-serif;color:#111}.sheet{width:420mm;height:297mm;display:flex;flex-direction:column;background:#fff;padding:9mm 11mm 6mm;overflow:hidden}.brand{display:flex;justify-content:space-between;align-items:baseline;padding-bottom:3mm;gap:5mm}.brand b{font-size:21pt;font-weight:600;color:#1a2a7c;letter-spacing:.5pt}.brand span{font-size:15pt;font-weight:600;color:#1a2a7c;letter-spacing:.5pt}h1{font-size:37pt;line-height:1.08;font-weight:700;margin:0;color:#1a2a7c}.desc{font-size:16.5pt;line-height:1.25;padding:3.5mm 0 4mm;margin:0;color:#000;font-weight:500}.mid{display:flex;gap:5mm;flex:1;min-height:0;padding-bottom:5mm}.photos{display:grid;grid-template-columns:1.35fr 1fr;gap:5mm;flex:1;min-height:0;min-width:0}.photos img{width:100%;height:100%;object-fit:cover;min-width:0;min-height:0}.ape{flex:0 0 auto;display:flex;height:60%;align-self:flex-end}.a3-no-ape{max-width:58mm;height:auto;font-size:12pt;padding:4mm;border:1px solid #999;align-self:flex-end}.ape img{height:100%;width:auto;display:block;object-fit:contain}.bottom{display:flex;gap:6mm;align-items:stretch}.pricebox{flex:0 0 24%;display:flex;flex-direction:column;justify-content:center}.price{font-size:42pt;font-weight:800;color:#1a2a7c;line-height:1;white-space:nowrap}.tel{font-size:16pt;font-weight:600;color:#000;padding-top:2mm}.strip{flex:1;background:#8fc94f;border-radius:4mm;display:flex;align-items:center;padding:3mm 4mm;min-width:0}.feat{flex:1;text-align:center;min-width:0}.feat b{display:block;font-size:19pt;color:#000;font-weight:700}.feat span{font-size:11.5pt;color:#000}.toolbar{font:14px Arial;background:#eef5ef;padding:12px;position:sticky;top:0;z-index:2;display:flex;gap:12px;align-items:center}.toolbar button{padding:10px}.toolbar [role=status]{max-width:800px}.preview{overflow:auto}@media print{.toolbar{display:none}.sheet{margin:0;print-color-adjust:exact;-webkit-print-color-adjust:exact}}`;
function html(i,s){
 const fs=facts(i);while(fs.length<6)fs.push({value:'',label:''});
 const op={vendita:'VENDITA',affitto_residenziale:'AFFITTO',affitto_commerciale:'AFFITTO',asta_giudiziaria:'ASTA'}[i.tipo_operazione]||'';
 return '<!doctype html><html lang="it"><meta charset="utf-8"><title>Cartello A3 '+esc(i.codice)+'</title><style>'+sheetCSS+'</style><div class="toolbar"><button id="a3-print" disabled>Attendi controllo</button><span role="status" id="a3-status">Verifica immagini e impaginazione…</span></div><main class="preview"><section class="sheet"><div class="brand"><b>Righetto Immobiliare</b><span>'+esc([String(i.comune||'').toUpperCase(),op,'RIF.'+(i.codice||'')].filter(Boolean).join(' | '))+'</span></div><h1>'+esc(s.title)+'</h1><p class="desc">'+esc(s.description)+'</p><div class="mid"><div class="photos">'+s.photos.map((src,n)=>'<img src="'+esc(src)+'" alt="Foto scelta '+(n+1)+'">').join('')+'</div>'+(noApe(i)?'<div class="ape a3-no-ape">Immobile al grezzo, APE non disponibile</div>':'<div class="ape"><img src="'+esc(s.apeSrc)+'" alt="Immagine APE ufficiale dell’immobile"></div>')+'</div><div class="bottom"><div class="pricebox"><div class="price">'+esc('€ '+new Intl.NumberFormat('it-IT',{maximumFractionDigits:0}).format(i.prezzo))+'</div><div class="tel">049 884 3484</div></div><div class="strip">'+fs.map(f=>'<div class="feat"><b>'+esc(f.value)+'</b><span>'+esc(f.label)+'</span></div>').join('')+'</div></div></section></main></html>';
}
function show(i,context){
 const propertyId=String(i.id||'');if(!propertyId)throw Error('Apri un immobile salvato.');
 document.getElementById('a3-composer')?.remove();
 const ov=document.createElement('div');ov.id='a3-composer';ov.setAttribute('role','dialog');ov.setAttribute('aria-modal','true');ov.setAttribute('aria-label','Cartello A3');
 ov.innerHTML='<style>#a3-composer{position:fixed;inset:0;z-index:15000;background:#1239;padding:18px;overflow:auto;font:15px/1.45 Arial;color:#12382a}#a3-composer *{box-sizing:border-box}#a3-composer .a3-panel{max-width:980px;background:#fff;margin:auto;padding:24px;border-radius:10px}#a3-composer h2{margin:0 0 8px}#a3-composer label{display:block;margin:10px 0}#a3-composer input:not([type=checkbox]),#a3-composer textarea{max-width:100%;width:100%;padding:10px;border:1px solid #8da99b;border-radius:5px;font:inherit}#a3-composer button{min-height:44px;padding:10px 15px;margin:4px;border:1px solid #0b6544;border-radius:5px;background:#fff;color:#064831;font-weight:bold;cursor:pointer}#a3-composer [data-open]{background:#075337;color:white}#a3-composer fieldset{margin:16px 0;border:1px solid #b1c7bb;border-radius:6px}#a3-composer .a3-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}#a3-composer .a3-photo{border:3px solid #ddd;padding:5px;position:relative}#a3-composer .a3-photo[aria-pressed=true]{border-color:#087145;background:#e5f3e9}#a3-composer .a3-photo img{width:100%;height:110px;object-fit:cover}#a3-composer .a3-energy{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}#a3-composer .a3-note{background:#f0f4f1;padding:10px;font-size:13px}#a3-composer [data-errors]{white-space:pre-line;color:#942313}#a3-composer .a3-actions{position:sticky;bottom:0;background:#fff;padding-top:12px;border-top:1px solid #dae4df}@media(max-width:540px){#a3-composer{padding:5px}#a3-composer .a3-panel{padding:14px}#a3-composer .a3-energy{grid-template-columns:1fr}#a3-composer .a3-grid{grid-template-columns:1fr 1fr}}</style><section class="a3-panel"><button type="button" data-close style="float:right">Chiudi</button><h2>Cartello A3 · '+esc(i.codice)+'</h2><p>Modello v4, due foto scelte da te. Nessun invio, salvataggio o stampa automatica.</p><label>Titolo standard<input data-title maxlength="180" readonly></label><label>Testo dell’annuncio, massimo 30 parole<textarea data-description rows="3"></textarea></label><p data-count></p><p class="a3-note">La proposta usa i dati salvati della scheda. Controlla il testo: non include indirizzo, proprietari o note interne. Prezzo salvato: <b>'+esc(positive(i.prezzo)?new Intl.NumberFormat('it-IT',{style:'currency',currency:'EUR'}).format(i.prezzo):'MANCANTE')+'</b>.</p><fieldset><legend>1. Scegli esattamente due foto, nell’ordine desiderato</legend><p data-selection>0 di 2 foto scelte</p><div class="a3-grid" data-gallery></div></fieldset><div class="a3-note" data-energy-note></div><p data-errors role="status" aria-live="polite"></p><div class="a3-actions"><button type="button" data-open>Genera anteprima A3</button><span>Da lì potrai scegliere Stampa / Salva PDF.</span></div></section>';
 document.body.append(ov);let apeSrc='',disposed=false;const selected=[];const q=s=>ov.querySelector(s),energy=initialEnergy(i);
 q('[data-title]').value=title(i);
 q('[data-description]').value=copy(i);
 const fixedEnergy=context?.energy;
 apeSrc=fixedEnergy?.image||'';
 q('[data-energy-note]').textContent=noApe(i)?'Immobile al grezzo, APE non disponibile. Nessun grafico associato.':fixedEnergy?.verified?'Grafico APE del gestionale principale: classe '+fixedEnergy.className+', EPgl,nren '+fixedEnergy.nren+', EPgl,ren '+fixedEnergy.ren+'. Layout, prezzo, striscia e telefono sono standard.':fixedEnergy?.sourceFormat==='ape2014'?'Grafico APE2014 presente nel gestionale principale, senza gli indici EPgl,nren ed EPgl,ren richiesti. Mantenuto originale, senza conversione. Gino verifica i dati prima di stampare.':fixedEnergy?'Grafico presente nel gestionale principale, ma il valore energetico è in fase di definizione. Mantenuto originale. Gino verifica i dati prima di stampare, nessun numero viene inventato.':'Grafico APE non ancora collegato a questo esatto riferimento. Cartello bloccato: segnalare la scheda da verificare.';
 const count=()=>{const n=words(q('[data-description]').value);q('[data-count]').textContent=n+' / 30 parole'+(n<30?' · Attenzione: descrizione sotto le 30 parole.':'');};q('[data-description]').oninput=count;count();
 const refs=[...new Set((Array.isArray(i.foto)&&i.foto.length?i.foto:i.foto_urls||[]).filter(r=>typeof r==='string').map(safeURL).filter(Boolean))];
 for(const [n,url]of refs.entries()){
  const b=document.createElement('button');b.type='button';b.className='a3-photo';b.setAttribute('aria-pressed','false');b.setAttribute('aria-label','Scegli foto '+(n+1));b.innerHTML='<img loading="lazy" src="'+esc(url)+'" alt="Foto immobile '+(n+1)+'"><span>Foto '+(n+1)+'</span>';b.onclick=()=>{const at=selected.indexOf(url);if(at>=0)selected.splice(at,1);else if(selected.length<2)selected.push(url);else{q('[data-errors]').textContent='Hai già scelto due foto. Deselezionane una per cambiarla.';return;}q('[data-errors]').textContent='';for(const button of q('[data-gallery]').children){const index=selected.indexOf(button.dataset.url);button.setAttribute('aria-pressed',String(index>=0));button.querySelector('span').textContent=index>=0?'Scelta '+(index+1):'Foto '+button.dataset.number;}q('[data-selection]').textContent=selected.length+' di 2 foto scelte';};b.dataset.url=url;b.dataset.number=n+1;q('[data-gallery]').append(b);
 }
 const close=()=>{disposed=true;ov.remove();};q('[data-close]').onclick=close;
 q('[data-open]').onclick=async()=>{
  if(global.rigPropertySaving||context?.same&&!context.same(propertyId)){q('[data-errors]').textContent='Scheda o sessione cambiata: chiudi e riapri Cartello A3.';return;}
  if(context?.verify){q('[data-open]').disabled=true;let valid=false;try{valid=await context.verify();}catch(e){}q('[data-open]').disabled=false;if(!valid||disposed){q('[data-errors]').textContent='Dati salvati o sessione cambiati: chiudi e riapri Cartello A3.';return;}}
  const state={title:q('[data-title]').value.trim(),description:q('[data-description]').value.trim(),photos:[...selected],apeSrc,energy:fixedEnergy?{className:fixedEnergy.className,nren:fixedEnergy.nren,ren:fixedEnergy.ren}:{},apeVerified:fixedEnergy?.verified===true,sourceAsIs:fixedEnergy?.sourceImageVerified===true&&fixedEnergy?.allowSourceAsIs===true,energyMissing:fixedEnergy?.missing?.join(', '),factsVerified:true};
  const errors=validate(i,state);q('[data-errors]').textContent=errors.join('\n');if(errors.length)return;
  const w=global.open('about:blank','_blank');if(!w){q('[data-errors]').textContent='Consenti la finestra di anteprima per questo clic.';return;}w.opener=null;w.document.open();w.document.write(html(i,state));w.document.close();
  const button=w.document.getElementById('a3-print'),status=w.document.getElementById('a3-status');
  Promise.all([...w.document.images].map(img=>new Promise(resolve=>{let done=false;const finish=ok=>{if(done)return;done=true;clearTimeout(timer);resolve(ok);};const timer=setTimeout(()=>finish(false),20000);img.onload=()=>finish(img.naturalWidth>0);img.onerror=()=>finish(false);if(img.complete)finish(img.naturalWidth>0);}))).then(async results=>{
   if(w.closed)return;await w.document.fonts.ready;await new Promise(r=>w.requestAnimationFrame(()=>w.requestAnimationFrame(r)));
   const title=w.document.querySelector('h1'),sheet=w.document.querySelector('.sheet'),desc=w.document.querySelector('.desc'),price=w.document.querySelector('.price');
   const overflow=title.getBoundingClientRect().height>parseFloat(w.getComputedStyle(title).lineHeight)*2+1||sheet.scrollHeight>sheet.clientHeight+1||sheet.scrollWidth>sheet.clientWidth+1||price.scrollWidth>price.clientWidth+1||[...w.document.querySelectorAll('.feat')].some(e=>e.scrollWidth>e.clientWidth+1);
   const ok=results.every(Boolean)&&!overflow;button.disabled=!ok;button.textContent=ok?'Stampa / Salva PDF':'PDF bloccato';status.textContent=!results.every(Boolean)?'Una foto o l’APE non si è caricata. Nessun ripiego automatico.':overflow?'Il contenuto non entra nel modello. Il titolo standard o il testo superano lo spazio disponibile. Segnala il problema senza modificare il layout.':(noApe(i)?'Due foto caricate, immobile al grezzo senza grafico APE. ':'Due foto e APE caricate, ' )+'Impaginazione verificata. Controlla visivamente prima di salvare. A3 orizzontale, scala 100%, senza intestazioni del browser.';
   button.onclick=()=>{if(!button.disabled)w.print();};
  });
 };
 q('[data-close]').focus();return ov;
}
global.RighettoCartelloA3={show,copy,title,facts,initialEnergy,validate,html,words};
})(window);
