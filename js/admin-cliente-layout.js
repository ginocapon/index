/* Layout cliente: campi opzionali collegati al salvataggio esistente. Nessun invio automatico. */
(function(){
'use strict';
const m=document.getElementById('clienteModal');if(!m)return;
m.classList.add('legacy-client-editor');
const original=m.querySelector('.modal-body'),wrap=document.createElement('div');wrap.className='legacy-edit-sections';
const used=new Set();
function field(id,label){let el=document.getElementById(id);if(!el)return missing(label);used.add(id);const cell=document.createElement('label');cell.className='legacy-field';const text=document.createElement('span');text.textContent=label;cell.append(text,el);return cell;}
const newFields={"Nome": "nome_proprio", "Cognome": "cognome", "Data di nascita": "nascita_data", "Luogo di nascita": "nascita_luogo", "Codice EORI": "codice_eori", "Nazione": "nazione", "Provincia": "provincia", "Comune": "comune", "Zona": "zona_residenza", "Via": "indirizzo_via", "Numero civico": "numero_civico", "CAP": "cap", "Telefono (2)": "telefono_secondario", "Cellulare": "cellulare", "Fax": "fax", "Email (2)": "email_secondaria", "Instagram": "instagram", "Facebook": "facebook", "Linkedin": "linkedin", "Tipo di documento": "documento_tipo", "Numero": "documento_numero", "Rilasciato il": "documento_rilasciato_il", "Rilasciato da": "documento_rilasciato_da", "Scadenza": "documento_scadenza", "Agente assegnato": "agente_assegnato"};
function missing(label){const key=newFields[label];const cell=document.createElement('label');cell.className='legacy-field';const text=document.createElement('span');text.textContent=label;const el=document.createElement('input');if(key){el.id='clienteExtra_'+key;el.dataset.clientExtra=key;el.lang='it-IT';el.type=key==='email_secondaria'?'email':'text';if(['nascita_data','documento_rilasciato_il','documento_scadenza'].includes(key)){el.dataset.clientDate='true';el.placeholder='gg/mm/aaaa';el.inputMode='numeric';el.pattern='[0-9]{2}/[0-9]{2}/[0-9]{4}';el.addEventListener('input',()=>el.setCustomValidity(''));}el.autocomplete='off';}else{el.disabled=true;el.placeholder='Non ancora disponibile';}cell.append(text,el);return cell;}
function displayDate(v){if(!v)return '';const m=String(v).match(/^(\d{4})-(\d{2})-(\d{2})$/);return m?m[3]+'/'+m[2]+'/'+m[1]:'';}
function saveDate(el){const value=el.value.trim();if(!value){el.setCustomValidity('');return null;}const m=value.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);if(!m){el.setCustomValidity('Usa gg/mm/aaaa');return null;}const d=new Date(Date.UTC(Number(m[3]),Number(m[2])-1,Number(m[1])));if(d.getUTCFullYear()!==Number(m[3])||d.getUTCMonth()+1!==Number(m[2])||d.getUTCDate()!==Number(m[1])){el.setCustomValidity('Data non valida. Usa gg/mm/aaaa');return null;}el.setCustomValidity('');return m[3]+'-'+m[2]+'-'+m[1];}
window.righettoExtraFill=function(c){document.querySelectorAll('[data-client-extra]').forEach(el=>{el.value=el.dataset.clientDate?displayDate(c?.[el.dataset.clientExtra]):c?.[el.dataset.clientExtra]??'';el.setCustomValidity('');});};
window.righettoExtraRead=function(){let values={};document.querySelectorAll('[data-client-extra]').forEach(el=>{values[el.dataset.clientExtra]=el.dataset.clientDate?saveDate(el):el.value.trim()||null});return values;};

function section(title,left,right){const h=document.createElement('h3');h.textContent=title;wrap.append(h);const grid=document.createElement('div');grid.className='legacy-edit-grid';[left,right].forEach(items=>{const col=document.createElement('div');items.forEach(([id,label])=>col.append(id?field(id,label):missing(label)));grid.append(col)});wrap.append(grid);}
const editId=document.getElementById('clienteEditId');wrap.append(editId);
section('Anagrafica', [[null,'Nome'],[null,'Cognome'],['clienteNome','Nome completo / visualizzato'],[null,'Data di nascita'],[null,'Luogo di nascita']], [['clienteTipoCliente','Privato / Azienda'],['clienteRagioneSociale','Ragione sociale'],['clientePartitaIva','Partita I.V.A.'],['clienteCodiceFiscale','Codice fiscale']]);
const note=document.createElement('p');note.className='legacy-edit-gap';note.textContent='Nome e cognome sono facoltativi: i dati esistenti non sono stati separati automaticamente. Nome completo resta il valore visualizzato e usato nei collegamenti.';wrap.append(note);
section('Dati per la fattura elettronica',[['clienteSdi','Codice SDI']],[[null,'Codice EORI']]);
section('Recapiti e contatti',[[null,'Nazione'],[null,'Provincia'],[null,'Comune'],[null,'Zona'],[null,'Via'],[null,'Numero civico'],[null,'CAP'],['clienteIndirizzo','Indirizzo completo esistente'],[null,'Instagram'],[null,'Facebook'],[null,'Linkedin']],[['clienteTelefono','Telefono / recapito esistente'],[null,'Telefono (2)'],[null,'Cellulare'],[null,'Fax'],['clienteEmail','Email'],[null,'Email (2)'],['clientePec','Email PEC']]);
section('Documento di identità',[[null,'Tipo di documento'],[null,'Rilasciato il'],[null,'Scadenza']],[[null,'Numero'],[null,'Rilasciato da']]);
section('Dettagli',[[null,'Agente assegnato'],['clienteFonte','Provenienza']],[['clienteNote','Note']]);
const extra=document.createElement('details');extra.className='legacy-existing-fields';extra.innerHTML='<summary>Ricerca, ruolo rubrica e allegati già disponibili nel nuovo</summary>';
// Preserve all remaining live fields and their event handlers, rather than deleting hidden dependencies.
const role=original.querySelector('.cliente-ruolo-row');if(role)extra.append(role);
const search=document.getElementById('clienteCampiRicerca');if(search)extra.append(search);
const docs=document.getElementById('clienteDocumentiList');if(docs)extra.append(docs);
const upload=document.getElementById('clienteDocumentiInput');if(upload){upload.disabled=true;upload.title='Archivio privato da collegare; nessun upload pubblico';extra.append(upload);}
const azienda=document.getElementById('campiAzienda');if(azienda){azienda.hidden=true;extra.append(azienda);}
wrap.append(extra);
original.replaceChildren(wrap);
const footer=m.querySelector('.modal-footer');footer.querySelector('[onclick="saveCliente()"]').textContent='Salva';
const next=document.createElement('button');next.className='btn';next.textContent='Salva e vai alla scheda cliente';next.addEventListener('click',()=>saveCliente(true));next.title='Salva e apre la scheda solo dopo esito riuscito';footer.append(next);
})();
