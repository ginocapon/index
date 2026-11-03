// Fragment-only token is captured privately and never verified by page load.
export function readActivationIntent(win=window){
 const params=new URLSearchParams(win.location.hash.slice(1));
 const token=params.get('token_hash'),type=params.get('type'),email=params.get('email');
 if(!token)return null;
 win.history.replaceState(null,'',win.location.pathname);
 if(!/^[a-f0-9]{40,128}$/i.test(token)||!['invite','recovery'].includes(type)||email!=='linda@righettoimmobiliare.it')return {invalid:true};
 return {token,type,email};
}
export function mountActivation({sb,intent,doc=document,onReady}){
 const status=doc.getElementById('setupStatus'),button=doc.getElementById('activateAccess');let busy=false,closed=false;
 if(!intent||intent.invalid){status.textContent='Collegamento non valido. Chiedi assistenza senza richiedere altri inviti.';return()=>{};}
 doc.getElementById('setupAccount').textContent=intent.email;
 status.textContent='Tocca Continua per verificare il tuo collegamento e scegliere la password personale.';button.hidden=false;
 const activate=async()=>{if(busy||closed)return;busy=true;button.disabled=true;
  try{
   const result=await sb.auth.verifyOtp({token_hash:intent.token,type:intent.type});
   intent.token=null;
   if(result.error||!result.data?.session||result.data.user?.email!==intent.email)throw Error();
   const verified=await sb.auth.getUser();
   if(verified.error||verified.data?.user?.id!==result.data.user.id||verified.data?.user?.email!==intent.email)throw Error();
   closed=true;button.hidden=true;await onReady();
  }catch{
   closed=true;intent.token=null;button.hidden=true;
   try{await sb.auth.signOut({scope:'local'});}catch{}
   status.textContent='Collegamento non valido o già usato. Chiedi assistenza, non ripetere e non richiedere altri inviti.';
  }finally{busy=false;button.disabled=false;}
 };
 button.addEventListener('click',activate);
 return()=>{closed=true;intent.token=null;button.removeEventListener('click',activate);};
}
