/* Uninstalled self-only opening test. Reads identity and properties; no write/send/log. */
export function mountSelfWhatsAppOpen({db,principal,button,mode,body,verifySelected,verifyProperties,isCurrent,notice,onLock=()=>{},active=false,allowExternalOpen=false,selectionReady=()=>true,launchApp,popup}){
 const OWNER='5f55e259-0d0b-46d9-8d77-17ab33db0fdf',SELF='b42e7d31-5db2-417d-84b0-9ec67650359d',PHONE='+393488621888';
 let disposed=false,busy=false,locked=false;
 const normalize=s=>{let n=String(s||'').replace(/\D/g,'');if(n.startsWith('00'))n=n.slice(2);if(n.length===10)n='39'+n;return '+'+n;};
 const alive=()=>!disposed&&isCurrent();
 function sync(){button.disabled=!active||busy||locked||!alive()||principal!==OWNER||!selectionReady()||!body.value.trim();}
 async function auth(){const u=await db.auth.getUser();if(!alive()||u.error||u.data?.user?.id!==principal||principal!==OWNER)throw Error('Sessione Gino non verificata. Nessuna apertura.');}
 async function recipient(){const s=await verifySelected();if(s.length!==1)throw Error('Scegli un solo destinatario.');if(allowExternalOpen){const n=normalize(s[0].address);if(!/^\+[1-9]\d{7,14}$/.test(n))throw Error('Numero non valido.');return n;}if(s[0].id!==SELF||normalize(s[0].address)!==PHONE)throw Error('Questa prova apre soltanto la chat di Gino. Scegli la sua scheda e il suo numero.');return PHONE;}
 async function run(){if(button.disabled||busy||locked||!alive())return;busy=true;button.textContent='Controllo...';button.classList.add('wa-pressed');button.setAttribute('aria-busy','true');sync();let tab=null;
  try{
   const delivery=mode.value,text=body.value;if(!['app','web'].includes(delivery))throw Error('Scegli Web o app.');
   if(delivery==='web'){tab=popup();if(!tab)throw Error('Consenti la nuova finestra. Nessuna apertura.');tab.opener=null;}
   await auth();const phone=await recipient();await verifyProperties();await auth();if(await recipient()!==phone)throw Error('Destinatario cambiato: ricontrolla.');
   if(!alive()||body.value!==text||mode.value!==delivery)throw Error('Testo, destinatario o modalità cambiati: ricontrolla prima di aprire.');
   const url=new URL(delivery==='app'?'whatsapp://send':'https://web.whatsapp.com/send');url.searchParams.set('phone',phone.slice(1));url.searchParams.set('text',text);
   if(!text.trim()||text.length>8000||url.href.length>16000)throw Error('Testo vuoto o troppo lungo. Nessuna apertura.');
   locked=true;onLock();button.textContent='Apertura richiesta';notice.textContent=allowExternalOpen?'Apertura richiesta verso '+phone+'. Controlla numero e testo in WhatsApp e premi invia solo dopo averli verificati. Nessun invio o registrazione automatica dal gestionale.':'Apertura richiesta solo verso Gino. Controlla numero e testo in WhatsApp. Nessun invio né registrazione automatica dal gestionale; questa prova non certifica il salvataggio.';
   if(delivery==='app')launchApp(url.href);else{tab.location.href=url.href;tab=null;}
  }catch(e){if(tab)tab.close();if(alive())notice.textContent=e.message;}
  finally{busy=false;button.setAttribute('aria-busy','false');if(!locked){button.textContent=allowExternalOpen?'Apri WhatsApp':'Invia con WhatsApp';button.classList.remove('wa-pressed');}sync();}
 }
 button.title=allowExternalOpen?'Apre WhatsApp con numero e testo; non invia e non registra':'Prova apertura solo verso Gino; non invia e non registra';button.setAttribute?.('aria-label',allowExternalOpen?'Apri WhatsApp con il destinatario scelto':'Prova apertura WhatsApp solo verso Gino');button.onclick=run;body.addEventListener('input',sync);mode.addEventListener('change',sync);sync();
 return {sync,dispose(){disposed=true;button.onclick=null;body.removeEventListener('input',sync);mode.removeEventListener('change',sync);button.disabled=true;}};
}
