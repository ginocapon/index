/* Private proposal. Preparation only. No retry, send or persistent state. */
(function(){'use strict';const openings=new WeakMap();async function openPrivacyEmail({client,kind,host,p,current}){
 p.textContent='Verifica destinatario email. Nessun invio automatico.';
 const principal=window.RighettoGatedPrincipal;
 const live=()=>current()&&!!principal&&window.RighettoGatedPrincipal===principal;
 try{
  if(!live()||typeof sb==='undefined')throw Error('Sessione non verificata');
  const user=await sb.auth.getUser();if(!live()||user.error||user.data?.user?.id!==principal)throw Error('Sessione cambiata');
  const r=await sb.from('clienti').select('id,nome,nome_proprio,cognome,email').eq('id',client.id).maybeSingle();
  if(!live()||r.error||r.data?.id!==client.id)throw Error('Scheda cliente non verificata');
  const check=await sb.auth.getUser();if(!live()||check.error||check.data?.user?.id!==principal)throw Error('Sessione cambiata');
  const title=document.createElement('h3');title.textContent=kind==='privacy-sign'?'Richiesta firma consenso privacy via email':'Informativa privacy via email';host.insertBefore(title,p);
  const recipient=document.createElement('p');recipient.dataset.privacyEmailRecipient='';const address=String(r.data.email||'').trim();recipient.textContent=address?'Email dalla scheda: '+address:'Email non presente nella scheda cliente. Nessun numero telefonico verrà usato come alternativa.';host.append(recipient);
  const rule=document.createElement('p');rule.textContent='Solo email per informativa e richiesta firma del consenso privacy. Nessun WhatsApp, SMS o telefonata. Gli altri comandi di contatto restano separati.';host.append(rule);
  const gate=document.createElement('p');gate.setAttribute('role','note');gate.textContent=kind==='privacy-sign'?'Preparazione della richiesta di firma non ancora attiva: occorrono modello e percorso di firma verificati. Nessun documento firmabile creato.':'Preparazione email non ancora attiva: occorrono informativa e testo email verificati.';host.append(gate);
  p.textContent='Nessun messaggio inviato o registrato come inviato. Nessun consenso o stato privacy modificato.';
  return {opened:true,channel:'email',sent:false,enabled:false};
 }catch(e){if(current())p.textContent='Preparazione email non completata: sessione o scheda non verificata. Nessun invio e nessun passaggio a un altro canale.';return {opened:false,reason:'context_changed',channel:'email'};}
}
window.RighettoClienteComunicazioni=Object.freeze({async open({client,kind,host,isCurrent=()=>true}){const ticket={};openings.set(host,ticket);host.replaceChildren();const p=document.createElement('p');p.setAttribute('role','status');p.textContent='Preparazione del messaggio WhatsApp. Nessun invio automatico.';host.append(p);const current=()=>openings.get(host)===ticket&&p.isConnected&&host.contains(p)&&isCurrent();if(kind==='privacy'||kind==='privacy-sign')return openPrivacyEmail({client,kind,host,p,current});if(!window.RighettoWhatsApp){if(current())p.textContent='Preparazione WhatsApp non disponibile.';return {opened:false,reason:'unavailable'};}try{const result=await RighettoWhatsApp.open({id:client.id,kind,isCurrent});if(!current())return result;if(result?.opened===true)p.textContent='Preparazione WhatsApp aperta. Nessun invio automatico.';else if(result?.reason==='context_changed')p.textContent='Preparazione interrotta: la sessione o la scheda è cambiata. Se il cliente è ancora quello corretto, riapri il comando. Nessun invio automatico.';else p.textContent='Preparazione WhatsApp non completata. Verifica la scheda e riapri il comando. Nessun invio automatico.';return result;}catch(error){if(current())p.textContent='Preparazione WhatsApp non completata. Verifica la scheda e riapri il comando. Nessun invio automatico.';return {opened:false,reason:'failed'};}}});})();
