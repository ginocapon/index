// Shared owner/admin authority. No hardcoded Linda UID, no email claim, no client registry writes.
export async function decideAccess(sb){
 const before=await sb.auth.getUser();const id=before.data?.user?.id;
 if(before.error||!id)return {kind:'denied'};
 const permitted=await sb.rpc('righetto_is_admin_request');
 if(permitted.error||permitted.data!==true)return {kind:'denied'};
 const after=await sb.auth.getUser();
 if(after.error||after.data?.user?.id!==id)return {kind:'denied'};
 return {kind:'admin',id};
}
export function watchAdminAccess(sb,{onDenied,intervalMs=30000,timers=globalThis}){
 let stopped=false,busy=false,generation=0,principal=null;
 const deny=()=>{if(stopped)return;generation++;principal=null;onDenied();};
 async function check(){if(stopped||busy)return;busy=true;const ticket=generation;
  try{const a=await decideAccess(sb);if(stopped||ticket!==generation)return;
   if(a.kind!=='admin'||(principal&&principal!==a.id)){deny();return;}principal=a.id;
  }catch{if(!stopped&&ticket===generation)deny();}finally{busy=false;}
 }
 const listener=sb.auth.onAuthStateChange((event,session)=>{
  // Callbacks stay synchronous, avoid auth-client deadlocks.
  if(!session?.user?.id||(principal&&session.user.id!==principal))deny();
  else timers.setTimeout(check,0);
 });
 const timer=timers.setInterval(check,intervalMs);check();
 return()=>{stopped=true;generation++;timers.clearInterval(timer);listener.data?.subscription?.unsubscribe();};
}
