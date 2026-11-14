// Private, read-only creator provenance. Never use assigned agents as creators.
const uuid=v=>typeof v==='string'&&/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(v);
export async function resolveCreator({db,event,principal,isCurrent=()=>true,signal}){
 if(!uuid(event?.id)||!uuid(event?.created_by)||!uuid(principal)||!isCurrent())return null;
 const valid=()=>isCurrent()&&!signal?.aborted;
 const auth=async()=>{const r=await db.auth.getUser();if(!valid()||r.error||r.data?.user?.id!==principal)throw Error('Sessione o evento cambiati.');};
 await auth();
 const q=db.from('agenda_events').select('id,created_by').eq('id',event.id).is('deleted_at',null);const fresh=await q.abortSignal(signal).maybeSingle();
 await auth();if(fresh.error||fresh.data?.id!==event.id||fresh.data?.created_by!==event.created_by)return null;
 const members=await db.from('agenda_members').select('user_id,label').eq('user_id',fresh.data.created_by).limit(2).abortSignal(signal);
 await auth();
 if(members.error||!Array.isArray(members.data)||members.data.length!==1)return null;
 const row=members.data[0];if(row.user_id!==fresh.data.created_by||typeof row.label!=='string'||!row.label.trim()||row.label.length>120)return null;
 return row.label.trim();
}
export function attachCreator({node,db,event,getPrincipal,isCurrent=()=>true}){
 const unknown='Autore tecnico nel nuovo: autore non disponibile';node.textContent=unknown;
 const principal=getPrincipal(),controller=new AbortController();let active=true,subscription=null,timer=null;
 const valid=()=>active&&node.isConnected&&isCurrent()&&principal===getPrincipal();
 const stop=()=>{active=false;controller.abort();node.textContent=unknown;subscription?.unsubscribe();observer.disconnect();clearTimeout(timer);};
 const observer=new MutationObserver(()=>{if(!node.isConnected)stop();});observer.observe(document.body,{childList:true,subtree:true});
 subscription=db.auth.onAuthStateChange?.((event,session)=>{if(event==='SIGNED_OUT'||session?.user?.id&&session.user.id!==principal)stop();})?.data?.subscription;
 timer=setTimeout(()=>controller.abort(),12000);
 return resolveCreator({db,event,principal,isCurrent:valid,signal:controller.signal}).then(label=>{if(valid())node.textContent=label?'Autore tecnico nel nuovo: '+label:unknown;return label;}).catch(()=>{if(node.isConnected)node.textContent=unknown;return null;}).finally(()=>clearTimeout(timer));
}
