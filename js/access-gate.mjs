// Shared owner/admin authority. Technical uncertainty never grants access.
const denial=error=>[401,403].includes(Number(error?.status));
export async function decideAccess(sb){
 try{
  const before=await sb.auth.getUser();
  if(before.error)return {kind:denial(before.error)?'denied':'unavailable'};
  const id=before.data?.user?.id;if(!id)return {kind:'denied'};
  const permitted=await sb.rpc('righetto_is_admin_request');
  if(permitted.error)return {kind:denial(permitted.error)?'denied':'unavailable'};
  if(permitted.data!==true)return {kind:'denied'};
  const after=await sb.auth.getUser();
  if(after.error)return {kind:denial(after.error)?'denied':'unavailable'};
  if(after.data?.user?.id!==id)return {kind:'denied'};
  return {kind:'admin',id};
 }catch{return {kind:'unavailable'};}
}
export function watchAdminAccess(sb,{onDenied,onUnavailable=()=>{},onRecovered=()=>{},principalId=null,intervalMs=30000,timers=globalThis}){
 let stopped=false,busy=false,generation=0,principal=principalId,unavailable=false,terminal=false;
 const deny=()=>{if(stopped||terminal)return;terminal=true;generation++;principal=null;onDenied();};
 async function check(){if(stopped||busy||terminal)return;busy=true;const ticket=generation;
  try{const a=await decideAccess(sb);if(stopped||terminal||ticket!==generation)return;
   if(a.kind==='unavailable'){if(!unavailable){unavailable=true;onUnavailable();}return;}
   if(a.kind!=='admin'||(principal&&principal!==a.id)){deny();return;}
   principal=a.id;if(unavailable){unavailable=false;onRecovered(a.id);}
  }finally{busy=false;}
 }
 const listener=sb.auth.onAuthStateChange((event,session)=>{
  // Keep callbacks synchronous. Same-user SIGNED_IN is also a normal resume.
  if(event==='SIGNED_OUT'||!session?.user?.id||(principal&&session.user.id!==principal))deny();
  else timers.setTimeout(check,0);
 });
 const timer=timers.setInterval(check,intervalMs);check();
 return()=>{stopped=true;generation++;timers.clearInterval(timer);listener.data?.subscription?.unsubscribe();};
}
