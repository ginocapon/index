/* Cestino immobili e storico clienti: interruttori negli elenchi. Nessuna cancellazione. */
(function(){
'use strict';
function add(afterId,key,label,reload){
 const sel=document.getElementById(afterId);if(!sel||document.getElementById('rb2-'+key))return;
 const l=document.createElement('label');l.id='rb2-'+key;l.style.cssText='display:inline-flex;align-items:center;gap:6px;margin-left:10px;font:600 0.8rem Montserrat,Arial,sans-serif;cursor:pointer';
 l.innerHTML='<input type="checkbox"> '+label;
 l.querySelector('input').addEventListener('change',e=>{window[key]=e.target.checked;if(typeof window[reload]==='function')window[reload]();});
 sel.insertAdjacentElement('afterend',l);}
function boot(){add('filtroTipo','__rCestino','Mostra cestino','loadImmobili');add('filtroFonteCliente','__rStorico','Mostra storico','loadClienti');}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
