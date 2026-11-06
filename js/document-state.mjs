export const choices={operation:['locazione','vendita'],interest:['proprio','per_conto'],statement:['informazioni','visita'],privacy:['consento','non_consento']};
export function validateDocument(values,selection,blankReviewed){
 const errors=[];for(const [k,options]of Object.entries(choices))if(!options.includes(selection[k]))errors.push('Scelta richiesta: '+k);
 for(const k of ['client_last_name','client_first_name','property_ref','property_street','property_city','owner_name','visit_date'])if(!String(values[k]||'').trim())errors.push('Campo richiesto: '+k);
 const date=values.visit_date||'';if(!/^\d{4}-\d{2}-\d{2}$/.test(date)||!Number.isFinite(Date.parse(date+'T12:00:00Z'))||new Date(date+'T12:00:00Z').toISOString().slice(0,10)!==date)errors.push('Data dichiarativa non valida');
 if(selection.interest==='per_conto'&&!String(values.on_behalf_of||'').trim())errors.push('Indicare per conto di chi');
 if(selection.operation==='vendita'&&!/^\d{1,2}([.,]\d{1,2})?$/.test(String(values.commission_pct||'')))errors.push('Provvigione vendita richiesta nel campo originale');
 if(!blankReviewed)errors.push('Verificare i campi rimasti vuoti');
 if(Object.keys(values).some(k=>k.startsWith('sign_')))errors.push('Data firma non compilabile automaticamente');
 return errors;
}
export function applyDocument(template,values,selection){
 const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const v={...values,property_operazione:selection.operation};if(/^\d{4}-\d{2}-\d{2}$/.test(v.visit_date||'')){const[y,m,d]=v.visit_date.split('-');v.visit_date=d+'/'+m+'/'+y;}
 let html=template.replace(/<span class="doc-fill" data-field="([a-z0-9_]+)">(?:[^<]|<img\b[^>]*>)*<\/span>/g,(all,k)=>v[k]!==undefined&&v[k]!==''?'<span class="doc-filled">'+escape(v[k])+'</span>':all);
 const checked=new Set([selection.operation==='locazione'?0:1,selection.interest==='proprio'?2:3,selection.statement==='informazioni'?4:5,selection.privacy==='consento'?6:7]);let n=0;
 html=html.replace(/<img\b[^>]*src="data:image\/png;base64,[^"]*"[^>]*>/g,(img)=>{if(!/alt="casella"/.test(img))return img;const i=n++;return checked.has(i)?'<span role="img" aria-label="casella selezionata" style="display:inline-block;width:16px;text-align:center;font:bold 16px Arial">☒</span>':img;});
 if(n!==8)throw Error('Modello caselle cambiato');return html;
}
