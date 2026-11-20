const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function googleTarget(rows,metric,choice={}) {
 if(!choice.confirmed||!choice.start||!choice.end)return {status:'choice_pending',target:null,goal:false};
 const base=rows.find(r=>r.period_kind==='calendar_month'&&r.period_status==='complete'&&r.effective_start===choice.start&&r.effective_end===choice.end);
 const value=base?.metrics?.[metric];
 if(!value||!Number.isFinite(value.value)||value.value<=0||!['exact','rounded'].includes(value.precision))return {status:'baseline_pending',target:null,goal:false};
 const target=value.value*10,exact=value.precision==='exact';
 const days=r=>(Date.parse(r.effective_end+'T00:00:00Z')-Date.parse(r.effective_start+'T00:00:00Z'))/86400000+1;
 const current=rows.filter(r=>r.period_kind==='calendar_month'&&r.period_status==='complete'&&r.effective_start>choice.end&&r.property===base.property&&r.data_timezone===base.data_timezone&&days(r)===days(base)&&r.metrics?.[metric]?.precision==='exact'&&Number.isFinite(r.metrics[metric].value)).sort((a,b)=>b.effective_end.localeCompare(a.effective_end))[0];
 return {status:exact?'exact':'rounded',target,baseline:value.value,baseDisplay:value.display,baseLabel:choice.label,goal:!!(exact&&current&&current.metrics[metric].value>target),current:current?.metrics[metric]?.value??null};
}
export function googleRoofLabel(state,metric){
 const name=metric==='clicks'?'CLIC':'IMPRESSIONI';
 if(state.target===null)return `<div class="gsc-roof-pending"><b>TETTO 10× · ${name}</b><span>${state.status==='choice_pending'?'Mese base in corso di definizione.':'In attesa del mese base completo e verificato.'} Nessuna soglia numerica presunta.</span></div>`;
 const n=state.target.toLocaleString('it-IT');
 return `<div class="gsc-roof-pending"><b>TETTO · ${state.status==='rounded'?'CIRCA ':''}${n} ${name}</b><span>10× ${esc(state.baseLabel)} · base ${esc(state.baseDisplay)}. Orizzonte: sei mesi.${state.status==='rounded'?' Base arrotondata: nessun GOAL finché manca il numero esatto.':''}</span></div>${state.goal?'<div class="goal-win" role="status"><span class="firework" aria-hidden="true">✺ ✧ ✺</span><strong>GOAL</strong><span>Superato il tetto su un mese completo confrontabile.</span></div>':''}`;
}
