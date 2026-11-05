/* Local preparation only: no send endpoint, mail client, logs or consent state changes. */
(function(){'use strict';
function open({client,kind,host,isCurrent}){
 const add=(tag,text)=>{const e=document.createElement(tag);e.textContent=text;host.append(e);return e;};host.replaceChildren();
 const privacy=kind!=='followup';add('h3',privacy?(kind==='privacy-sign'?'Richiesta firma consenso - preparazione':'Informativa privacy - preparazione'):'Follow up richiesta - preparazione');
 add('p','Solo bozza locale. Non inviata, non registrata come inviata e non salvata. Rivedi destinatario e testo.');
 if(privacy)add('p','Invio non disponibile: il modello 1673 recuperato ha P.IVA discordanti e consensi prespuntati da decidere. Nessun documento valido o collegamento di firma viene aggiunto. La preparazione non attesta alcun consenso.');
 else add('p','Questo testo chiede un riscontro, senza il link automatico del vecchio gestionale. Non modifica richieste, etichette o stato del cliente.');
 const label=add('label','Destinatario email: '),select=document.createElement('select');select.setAttribute('aria-label','Destinatario email bozza');select.append(new Option('Scegli indirizzo',''));for(const address of [...new Set([client.email,client.email_secondaria].filter(x=>typeof x==='string'&&/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(x)))])select.append(new Option(address,address));label.append(select);
 const subject=add('input','');subject.value=privacy?'Informativa sul trattamento dei dati personali':'La sua richiesta immobiliare';subject.setAttribute('aria-label','Oggetto bozza');subject.style.cssText='display:block;width:100%;box-sizing:border-box;margin:12px 0';
 const body=add('textarea','');body.rows=8;body.style.cssText='width:100%;box-sizing:border-box';body.setAttribute('aria-label','Testo comunicazione da rivedere');body.value=privacy?'':'Buongiorno, la contatto in merito alla sua richiesta immobiliare. Sta ancora cercando? Se le sue esigenze sono cambiate, può indicarmi le nuove preferenze.\nGrazie, Gino';
 const copy=add('button','Copia bozza per revisione'),status=add('p','');copy.type='button';status.setAttribute('role','status');copy.disabled=true;const valid=()=>!!select.value&&!!subject.value.trim()&&!!body.value.trim()&&!privacy;select.onchange=body.oninput=subject.oninput=()=>copy.disabled=!valid();
 if(privacy)status.textContent='Preparazione incompleta: manca un modello privacy verificato. Copia e invio bloccati.';
 copy.onclick=async()=>{if(!isCurrent()||!valid())return;try{await navigator.clipboard.writeText('A: '+select.value+'\nOggetto: '+subject.value+'\n\n'+body.value);status.textContent='Bozza copiata per revisione, nessun invio.';}catch(e){body.focus();body.select();status.textContent='Copia manualmente il testo. Nessun invio.';}};
}
if(typeof sb!=='undefined')sb.auth?.onAuthStateChange?.(event=>{if(event==='SIGNED_OUT'||event==='SIGNED_IN')document.querySelectorAll('[data-communication-draft]').forEach(x=>x.replaceChildren());});
window.RighettoClienteComunicazioni=Object.freeze({open});})();
