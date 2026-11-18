import {calendarSeries} from './speed-private-reader.mjs';
export function buildSpeedModel(rows){
 const weeks=calendarSeries(rows,{periodKind:'fixed_week_interval'}),months=calendarSeries(rows,{periodKind:'calendar_month'});
 const byId=new Map(rows.map(r=>[r.id,r]));
 const points=series=>series.map(p=>{const r=byId.get(p.id);const d=r.effective_start;const label=r.period_kind==='fixed_week_interval'?d.slice(8)+'/'+d.slice(5,7)+' - '+r.effective_end.slice(8)+'/'+r.effective_end.slice(5,7):new Date(d+'T12:00:00Z').toLocaleDateString('it-IT',{month:'short',year:'2-digit',timeZone:'UTC'});return {l:label,c:r.metrics.clicks.value,i:r.metrics.impressions.value,ia:r.metrics.impressions.precision==='rounded',undocumented:r.metrics.clicks.precision==='undocumented',id:r.id,start:r.effective_start,end:r.effective_end};});
 return {rows,latestWeek:weeks.length?byId.get(weeks.at(-1).id):null,series:{mese:points(weeks),trimestre:points(months.slice(-3)),anno:points(months.slice(-12))}};
}
