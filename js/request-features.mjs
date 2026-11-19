import{requestFeatureSchema}from'./request-feature-schema.mjs?v=20261119-requests-full-v1';
const schema=new Map(requestFeatureSchema.filter(s=>!s.count_key).map(s=>[s.source_id,s]));
const norm=v=>String(v??'').trim().normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('it-IT');
export function normalizeFeatures(raw){if(raw===undefined)return undefined;if(!raw||typeof raw!=='object'||Array.isArray(raw)||Object.keys(raw).length>89)throw Error('Caratteristiche richiesta non valide');const out={};for(const key of Object.keys(raw).sort()){const s=schema.get(key),v=raw[key];if(!s||v===null||typeof v!=='string'||v===s.unset||!s.options.some(o=>o.value===v))throw Error('Caratteristica non supportata: '+key);out[key]=v;}return out;}
export function compareFeatures(raw,property){const result={failed:[],unknown:[],checked:[]};let values;try{values=normalizeFeatures(raw);}catch(e){result.unknown.push(e.message);return result;}for(const[key,wanted]of Object.entries(values||{})){const s=schema.get(key),label=s.label,value=s.property?property[s.property]:undefined;let ok=null;
 if(s.kind==='boolean'){if(typeof value==='boolean')ok=value===(wanted==='1');}
 else if(s.number){const n=typeof value==='number'?value:typeof value==='string'&&/^\d+$/.test(value)?Number(value):null;if(n!==null&&Number.isSafeInteger(n)&&n>=0){const option=s.options.find(o=>o.value===wanted),gt=/^(?:più di|>)\s*(\d+)$/.exec(option.label);ok=gt?n>Number(gt[1]):n===Number(wanted);}}
 else if(s.source_id==='info_100'){if(typeof value==='boolean'&&['0','1'].includes(wanted))ok=value===(wanted==='1');}
 else if(typeof value==='string'&&value.trim()){const allowed=s.options.filter(o=>o.value!==s.unset),wantedLabel=norm(allowed.find(o=>o.value===wanted)?.label);const actual=norm(value);const mapped=s.source_id==='info_104'?({fibra:'fibra',fibra_1gb:'fibra',adsl:'adsl',nessuna:'nessuna'}[actual]||actual):actual;const known=allowed.some(o=>norm(o.label)===mapped);if(known)ok=mapped===wantedLabel;}
 result[ok===null?'unknown':ok?'checked':'failed'].push(label+(ok===null?' immobile da verificare':ok?': conforme':' fuori dai criteri'));
 }return result;}
