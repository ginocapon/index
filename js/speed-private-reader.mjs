// PRIVATE REVIEW CANDIDATE, no listeners or network at import. No embedded dataset or persistent cache.
const OWNER='5f55e259-0d0b-46d9-8d77-17ab33db0fdf';
const TABLE='rig_speed_gsc_readings';
const fields='id,property,view_key,period_kind,requested_start,requested_end,effective_start,effective_end,effective_ui,period_status,data_timezone,observed_date,observed_from,observed_until,metrics,notes,source_reference,source_sha256,source_row,record_sha256,supersedes';
export function createSpeedReader({sb,onClear=()=>{}}){
 let epoch=0,stopped=false,controller=null;
 const clear=()=>{epoch++;controller?.abort();controller=null;onClear();};
 const watcher=sb.auth.onAuthStateChange((_event,session)=>{if(session?.user?.id!==OWNER)clear();});
 async function owner(){const r=await sb.auth.getUser();if(r.error||r.data?.user?.id!==OWNER)throw Error('Speed owner access not verified');return OWNER;}
 return {
  clear,
  stop(){stopped=true;clear();watcher.data?.subscription?.unsubscribe();},
  async read(){
   clear();const ticket=epoch;controller=new AbortController();const signal=controller.signal;
   const current=()=>!stopped&&epoch===ticket&&!signal.aborted;
   try{
    await owner();if(!current())throw Error('Session changed');
    // Bounded pages prevent silent server truncation. Rows remain in memory only.
    const rows=[],ids=new Set();let total=null;
    for(let offset=0;offset<10000;offset+=200){
     const result=await sb.from(TABLE).select(fields,{count:'exact'}).order('id').range(offset,offset+199).abortSignal(signal);
     if(!current()||result.error||!Array.isArray(result.data)||!Number.isInteger(result.count))throw Error('Speed data not verified');
     if(total===null)total=result.count;if(total!==result.count||total>10000)throw Error('Speed dataset changed or exceeds reviewed bound');
     for(const row of result.data){if(ids.has(row.id))throw Error('Duplicate reading');ids.add(row.id);rows.push(row);}
     if(rows.length===total)break;if(!result.data.length)throw Error('Incomplete readings');
    }
    await owner();if(!current()||rows.length!==total)throw Error('Incomplete readings or session changed');
    return {state:rows.length?'ready':'empty',rows};
   }catch(error){if(current())clear();throw error;}
  }
 };
}
// Select observations, never sum overlapping windows. Conflicting revisions require reconciliation.
export function calendarSeries(rows,{periodKind,metric='clicks'}){
 if(!['calendar_month','fixed_week_interval'].includes(periodKind)||!['clicks','impressions'].includes(metric))throw Error('Unsupported chart series');
 const groups=new Map();
 for(const r of rows.filter(r=>r.period_kind===periodKind)){
  if(r.property!=='sc-domain:righettoimmobiliare.it'||r.data_timezone!=='America/Los_Angeles')throw Error('Unreviewed property or timezone');
  if(r.period_status!=='complete')continue;
  const k=[r.property,r.period_kind,r.effective_start,r.effective_end].join('|');const a=groups.get(k)||[];a.push(r);groups.set(k,a);
 }
 return [...groups.values()].map(a=>{
  a.sort((x,y)=>Date.parse(y.observed_until||y.observed_date)-Date.parse(x.observed_until||x.observed_date));const selected=a[0];
  for(const older of a.slice(1)){if(JSON.stringify(older.metrics)!==JSON.stringify(selected.metrics)&&selected.supersedes!==older.id)throw Error('Conflicting observations require documented reconciliation');}
  const m=selected.metrics?.[metric];if(!m||!Number.isFinite(m.value)||!['exact','rounded','undocumented'].includes(m.precision))throw Error('Unverified metric');
  return {id:selected.id,start:selected.effective_start,end:selected.effective_end,value:m.value,display:m.display,precision:m.precision,observedUntil:selected.observed_until,observedDate:selected.observed_date,warning:m.precision==='undocumented'?'Precisione non documentata nella fonte custodita':null};
 }).sort((a,b)=>a.start.localeCompare(b.start));
}
