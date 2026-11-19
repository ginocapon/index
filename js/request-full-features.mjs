import{requestFeatureSchema as schema}from'./request-feature-schema.mjs?v=20261119-requests-full-v1';
import{normalizeFeatures}from'./request-features.mjs?v=20261119-requests-full-v1';
export function mountFullFeatures({form,tabs,features,raw={},countControls,readOnly=false}){
 const values={...normalizeFeatures(raw)},controls=new Map();
 for(const b of tabs.children){b.disabled=false;b.removeAttribute('title');b.onclick=()=>show(b.textContent);}
 function show(tab){for(const b of tabs.children)b.setAttribute('aria-selected',String(b.textContent===tab));features.replaceChildren();for(const s of schema.filter(s=>s.tab===tab)){
 const row=document.createElement('div');row.className='rr-legacy-feature';const order=schema.filter(s=>s.tab===tab).indexOf(s);const split=tab==='ambienti'?(window.innerWidth>=1600?[8,16]:[7,15]):[Math.ceil(schema.filter(s=>s.tab===tab).length/3),2*Math.ceil(schema.filter(s=>s.tab===tab).length/3)];const column=order<split[0]?1:order<split[1]?2:3;row.style.gridColumn=String(column);row.style.gridRow=String(order-(column===1?0:split[column-2])+1);const label=document.createElement('span');label.textContent=s.label;row.append(label);const box=document.createElement('div');box.className='rr-feature-control';row.append(box);
 const current=()=>s.count_key?(countControls[s.count_key]?.value()??'unset'):(values[s.source_id]??'');
 const sourceToSaved=v=>s.count_key?(v===s.unset?'unset':v==='-1'?'gt3':v):v;
 const set=v=>{if(s.count_key){countControls[s.count_key].set(v);}else if(v==='')delete values[s.source_id];else values[s.source_id]=v;};
 if(s.kind==='boolean'||s.kind==='number-group'){
  const opts=s.options;for(const option of opts){const button=document.createElement('button');button.type='button';button.textContent=option.label;button.disabled=readOnly;button.dataset.value=option.value;button.setAttribute('aria-label',s.label+': '+(option.label==='×'?'non definito':option.label));button.onclick=()=>{set(current()===option.value?'':option.value);paint();};box.append(button);}function paint(){for(const b of box.children){const selected=b.dataset.value===current();b.setAttribute('aria-pressed',String(selected));b.style.setProperty('background',selected?'#075c42':'#f4f4f4','important');b.style.setProperty('color',selected?'white':'#222','important');}}paint();
 }else{const select=document.createElement('select');select.setAttribute('aria-label',s.label);select.disabled=readOnly;for(const o of s.options)select.append(new Option(o.label,sourceToSaved(o.value)));const existing=current();if(s.count_key&&![...select.options].some(o=>o.value===existing))select.append(new Option((existing==='gt3'?'più di 3':existing)+' (criterio esistente)',existing));select.value=existing||sourceToSaved(s.unset);select.onchange=()=>{const v=select.value;set(s.count_key?v:v===s.unset?'':v);};box.append(select);}
 features.append(row);controls.set(s.source_id,box);
 }}show('ambienti');return{read:()=>normalizeFeatures(values)};
}
