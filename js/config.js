/* Contact display routing only. No lead sends or notification-recipient changes. */
(function(w){
'use strict';
const people={linda:{name:'Linda Righetto',phone:'393497365930',display:'349 736 5930',email:'linda@righettoimmobiliare.it'},gino:{name:'Gino Capon',phone:'393488621888',display:'348 862 1888',email:'gino@righettoimmobiliare.it'}};
const norm=v=>String(v||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[_-]/g,' ');
function typeLabels(d){
 const dictionary=w.RighettoPublicTypes&&w.RighettoPublicTypes.dictionary;
 const values=[d.tipologia,d.tipo,d.categoria].concat(d.tipi||[]).filter(Boolean);
 return values.map(value=>{
  const key=String(value),m=key.match(/^([sd])-(\d+)$/);if(!m)return key;
  if(!dictionary)return '';
  const row=(m[1]==='s'?dictionary.specific:dictionary.detailed)[m[2]];
  if(!row)return '';
  return m[1]==='d'?((dictionary.specific[row.specific_id]||{}).label||'')+' '+row.label:row.label;
 }).join(' ');
}
function classify(d){
 d=d||{};const op=norm(d.tipo_operazione||d.op||d.tipo_op),type=norm(typeLabels(d));
 if(!/affitt|locaz|rent/.test(op))return 'gino';
 const commercial=/commercial|direzional|produttiv|capannon|uffici|negoz|laborator|magazzin|terren|garage|box|attivita|\blocale\b/.test(type+' '+op);
 const residential=/residenzial|abitativ|appart|casa|villa|villett|bifamiliar|trifamiliar|quadrifamiliar|attico|mansard|monolocal|bilocal|trilocal|quadrilocal|stanza|student|camera/.test(type+' '+op);
 if(commercial&&residential)return 'choose';
 if(commercial)return 'gino';if(residential)return 'linda';
 return 'choose';
}
function fromText(text){
 const s=norm(text);const rent=/affitt|locaz|rent/.test(s),sale=/vendit|vendere|acquist|comprar|mutuo|valutaz|stimare/.test(s);
 if(rent&&sale)return 'choose';
 if(!rent)return /student|stanza|camera/.test(s)&&!sale?'linda':'gino';return classify({op:'affitto',tipo:s});
}
function resolve(d){return people[classify(d)]||null;}
function card(key){const p=people[key];return '<strong>'+p.name+'</strong><br><a data-rig-owner="'+key+'" href="tel:+'+p.phone+'">'+p.display+'</a> · <a data-rig-owner="'+key+'" href="mailto:'+p.email+'">'+p.email+'</a>';}
function html(key){return key==='choose'?'<strong>Affitti residenziali e studenti</strong><br>'+card('linda')+'<br><br><strong>Vendite, affitti commerciali e altri servizi</strong><br>'+card('gino'):card(key||'gino');}
function plain(key){if(key==='choose')return 'Affitti residenziali e studenti: Linda Righetto, '+people.linda.display+', '+people.linda.email+'. Vendite, affitti commerciali e altri servizi: Gino Capon, '+people.gino.display+', '+people.gino.email+'.';const p=people[key]||people.gino;return p.name+': '+p.display+' · '+p.email;}
const page=w.location? w.location.pathname.split('/').pop().replace(/\.html$/,''):'';
let context=page==='linda-righetto'?'linda':(/affitt|locaz/.test(page)?'choose':'gino');
function setContext(d){context=typeof d==='string'?(people[d]||d==='choose'?d:'gino'):classify(d);update();return context;}
function current(){return context;}
function routeAnchor(a){
 if(a.dataset.rigOwner)return;
 let u;try{if(!a.dataset.rigOriginalHref)a.dataset.rigOriginalHref=a.getAttribute('href');u=new URL(a.dataset.rigOriginalHref,w.location.href);}catch(e){return;}
 const known=/393497365930|393488621888|3497365930|3488621888/.test(u.href);
 if(!known)return;
 if(!a.dataset.rigOriginalText)a.dataset.rigOriginalText=a.innerHTML;
 if(context==='choose'){if(/^\s*(?:\+39\s*)?(?:349\s*736\s*5930|348\s*862\s*1888)/.test(a.textContent))a.textContent='Scegli il referente';a.href='/contatti?tipo=affitto';a.title='Scegli il referente: affitto residenziale o commerciale';return;}
 const p=people[context]||people.gino;
 if(a.textContent==='Scegli il referente')a.innerHTML=a.dataset.rigOriginalText;
 if(u.protocol==='tel:'){a.href='tel:+'+p.phone;if(/^(?:\+39\s*)?(?:349\s*736\s*5930|348\s*862\s*1888)(?:\s*\(cell\.\))?$/.test(a.textContent.trim())){if(a.children.length&&a.lastChild&&a.lastChild.nodeType===3){if(a.lastChild.textContent!==' '+p.display)a.lastChild.textContent=' '+p.display;}else if(a.textContent!==p.display)a.textContent=p.display;}}
 else if(u.hostname==='wa.me'){u.pathname='/'+p.phone;a.href=u.toString();}
 a.title=p.name+' - '+p.display;
}
function update(){
 if(!w.document)return;const doc=w.document;
 doc.querySelectorAll('a[href]').forEach(routeAnchor);
 doc.querySelectorAll('[data-rig-contact-card]').forEach(el=>{const h=html(context);if(el.innerHTML!==h)el.innerHTML=h;});
}
function init(){
 const doc=w.document;
 const sel=doc.getElementById('f-obj');if(sel){const sync=()=>setContext(sel.value?fromText(sel.value):(new URLSearchParams(w.location.search).get('tipo')==='affitto'?'choose':'gino'));sel.addEventListener('change',sync);sync();}
 doc.addEventListener('click',e=>{const a=e.target.closest&&e.target.closest('a[href]');if(a)routeAnchor(a);},true);
 if (/affitt|locaz/.test(page)) {const box=doc.createElement('aside');box.setAttribute('data-rig-contact-card','');box.style.cssText='max-width:980px;margin:20px auto;padding:20px;border:1px solid #ddd;border-radius:12px;font:15px/1.6 sans-serif';doc.body.appendChild(box);}
 update();let queued=false;new MutationObserver(()=>{if(queued)return;queued=true;setTimeout(()=>{queued=false;update();},0);}).observe(doc.body,{childList:true,subtree:true});
}
w.RighettoContacts={people,classify,fromText,resolve,html,plain,setContext,current,update};
if(w.document){if(w.document.readyState==='loading')w.document.addEventListener('DOMContentLoaded',init);else init();}
})(typeof window!=='undefined'?window:globalThis);

/**
 * RIGHETTO IMMOBILIARE — Configurazione Servizi Esterni
 */

const SERVIZI_CONFIG = {
  // ── NOTIFICHE EMAIL — Supabase Edge Function ────────────
  // Stessa API usata dall'admin per le email massive.
  // Non richiede send-mail.php su cPanel.
  EMAIL_NOTIFY_TO: 'info@righettoimmobiliare.it',

  // Invia una email di notifica tramite la Edge Function send-email.
  // opts: { subject, html_body, reply_to (opzionale) }
  // Ritorna true se inviata, false in caso di errore.
  sendNotifica: async function(opts) {
    try {
      const r = await fetch(
        'https://qwkwkemuabfwvwuqrxlu.supabase.co/functions/v1/send-email',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc'
          },
          body: JSON.stringify({
            action: 'send_test',
            to_email: this.EMAIL_NOTIFY_TO,
            sender_email: 'info@righettoimmobiliare.it',
            sender_name: 'Righetto Immobiliare',
            subject: opts.subject,
            html_body: opts.html_body,
            reply_to: opts.reply_to || undefined
          })
        }
      );
      if (!r.ok) {
        try {
          const err = await r.json();
          console.warn('sendNotifica fallita:', err);
        } catch (_) { console.warn('sendNotifica HTTP', r.status); }
      }
      return r.ok;
    } catch(e) {
      console.warn('sendNotifica errore rete:', e);
      return false;
    }
  },

  // ── EMAILJS (Email Marketing) ────────────────────────────
  EMAILJS_PUBLIC_KEY: 'n3XE6MEEie7ZxPw-z',
  EMAILJS_SERVICE_ID: 'service_60lyfuu',
  EMAILJS_MARKETING_TEMPLATE_ID: 'template_1gpdcuq'
};
