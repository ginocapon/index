export async function startPasswordSetup({sb,win=window,doc=document,linkIntent=null}){
 const status=doc.getElementById('setupStatus'),form=doc.getElementById('setupForm'),button=doc.getElementById('savePassword');
 const say=(text)=>{status.textContent=text;};let user=null,busy=false,closed=false;
 form.hidden=true;
 // This dedicated page accepts only an email invitation/recovery link.
 // Existing admin cookies alone never grant a password-setting flow here.
 const fragment=new URLSearchParams(win.location.hash.slice(1));
 const allowed=linkIntent===true||(['invite','recovery'].includes(fragment.get('type'))&&fragment.has('access_token')&&fragment.has('refresh_token'));
 if(!allowed){say('Apri il collegamento ricevuto via email. Se è scaduto, chiedi un nuovo invito.');return ()=>{};}
 // SDK consumes the fragment, not our logs/storage. URL cleaned before any app navigation.
 try{
  const session=await sb.auth.getSession();
  win.history.replaceState(null,'',win.location.pathname);
  if(session.error||!session.data?.session)throw Error();
  const result=await sb.auth.getUser();
  if(result.error||!result.data?.user?.id||!result.data.user.email)throw Error();
  user=result.data.user;doc.getElementById('setupAccount').textContent=user.email;
  form.hidden=false;say('Imposta una password personale. Non inviarla in chat.');
 }catch{win.history.replaceState(null,'',win.location.pathname);say('Collegamento non valido o scaduto. Chiedi un nuovo invito.');return ()=>{};}
 const submit=async(e)=>{
  e.preventDefault();if(busy||closed)return;
  const password=doc.getElementById('newPassword'),confirm=doc.getElementById('confirmPassword');
  if(password.value.length<12){say('Usa almeno 12 caratteri.');return;}
  if(password.value!==confirm.value){say('Le password non coincidono.');return;}
  busy=true;button.disabled=true;
  try{
   const before=await sb.auth.getUser();if(before.error||before.data?.user?.id!==user.id)throw Error('session');
   const result=await sb.auth.updateUser({password:password.value});
   if(result.error)throw Error('password');
   if(result.data?.user?.id!==user.id)throw Error('session');
   password.value='';confirm.value='';form.hidden=true;closed=true;
   await sb.auth.signOut({scope:'local'});
   say('Password impostata. Il tuo accesso amministratore sarà disponibile dopo la conferma di attivazione.');
   doc.getElementById('setupLogin').hidden=false;
  }catch(error){password.value='';confirm.value='';say(error.message==='password'?'Password non accettata. Usa una password più lunga e riprova.':'Sessione cambiata o scaduta. Riapri il collegamento email.');}
  finally{busy=false;button.disabled=false;}
 };
 form.addEventListener('submit',submit);
 return ()=>{closed=true;form.removeEventListener('submit',submit);};
}
