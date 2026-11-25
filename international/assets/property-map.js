(function(){
var SB='https://qwkwkemuabfwvwuqrxlu.supabase.co';
var KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc';
var root=document.getElementById('rw-pmap');if(!root)return;
var L=(document.documentElement.lang||'en').toLowerCase().slice(0,2);
var T={
en:{pre:'',sale:'For sale',rent:'To rent',note:'Towns are real. Each dot sits at an invented position inside its town, never the real address.',one:'property',many:'properties',aria:'Interactive map of the properties',loc:'en-GB',poa:'Price on request',pm:'/month',types:{appartamento:'Apartment',villa:'Villa',villetta:'Detached house',bifamiliare:'Two-family house',trifamiliare:'Three-family house',quadrifamiliare:'Four-family house',capannone:'Warehouse',ufficio:'Office',negozio:'Shop',terreno:'Land','':'Property'},attr:'Region and town boundaries: ISTAT / © OpenStreetMap contributors',zin:'Zoom in',zout:'Zoom out',area:'Padova area',italy:'Italy',hint:'Drag to move. Scroll, pinch or use + and − to zoom.',vn:'Veneto',vc:['Venezia','Verona','Vicenza','Treviso','Padova','Belluno','Rovigo'],oc:['Roma','Milano','Napoli','Torino','Firenze','Bologna','Palermo','Cagliari','Bari','Genova','Trieste']},
ar:{vn:'فينيتو',pre:'ar/',sale:'للبيع',rent:'للإيجار',note:'البلدات حقيقية. كل نقطة في موضع مُختلَق داخل بلدتها، وليست العنوان الحقيقي أبدًا.',one:'عقار',many:'عقارات',aria:'خريطة تفاعلية للعقارات',loc:'ar-u-nu-latn',poa:'السعر عند الطلب',pm:' / شهرياً',types:{appartamento:'شقة',villa:'فيلا',villetta:'منزل مستقل',bifamiliare:'منزل لعائلتين',trifamiliare:'منزل لثلاث عائلات',quadrifamiliare:'منزل لأربع عائلات',capannone:'مستودع',ufficio:'مكتب',negozio:'محل تجاري',terreno:'أرض','':'عقار'},attr:'حدود المناطق والبلدات: ISTAT / © مساهمو OpenStreetMap',zin:'تكبير',zout:'تصغير',area:'منطقة بادوفا',italy:'إيطاليا',hint:'اسحب للتحريك. استخدم التمرير أو القرص أو + و − للتكبير.',vc:['البندقية','فيرونا','فيتشنزا','تريفيزو','بادوفا','بيلونو','روفيغو'],oc:['روما','ميلانو','نابولي','تورينو','فلورنسا','بولونيا','باليرمو','كالياري','باري','جنوة','تريستي']},
tr:{pre:'tr/',sale:'Satılık',rent:'Kiralık',note:'Kasabalar gerçektir. Her nokta, kasabasının içinde uydurma bir konumdadır; asla gerçek adres değildir.',one:'gayrimenkul',many:'gayrimenkul',aria:'Gayrimenkullerin etkileşimli haritası',loc:'tr-TR',poa:'Fiyat talep üzerine',pm:' / ay',types:{appartamento:'Daire',villa:'Villa',villetta:'Müstakil ev',bifamiliare:'İki aileli ev',trifamiliare:'Üç aileli ev',quadrifamiliare:'Dört aileli ev',capannone:'Depo / atölye',ufficio:'Ofis',negozio:'Dükkân',terreno:'Arsa','':'Gayrimenkul'},attr:'Bölge ve kasaba sınırları: ISTAT / © OpenStreetMap katkıda bulunanlar',zin:'Yakınlaştır',zout:'Uzaklaştır',area:'Padova bölgesi',italy:'İtalya',hint:'Taşımak için sürükleyin. Kaydırın, iki parmakla sıkıştırın veya + ve − kullanın.',vc:['Venedik','Verona','Vicenza','Treviso','Padova','Belluno','Rovigo'],oc:['Roma','Milano','Napoli','Torino','Floransa','Bolonya','Palermo','Cagliari','Bari','Cenova','Trieste']},
es:{vn:'Véneto',pre:'es/',sale:'En venta',rent:'En alquiler',note:'Las ciudades son reales. Cada punto está en una posición inventada dentro de su ciudad, nunca en la dirección real.',one:'inmueble',many:'inmuebles',aria:'Mapa interactivo de inmuebles',loc:'es-ES',poa:'Precio a consultar',pm:' / mes',types:{appartamento:'Apartamento',villa:'Villa',villetta:'Casa independiente',bifamiliare:'Casa bifamiliar',trifamiliare:'Casa trifamiliar',quadrifamiliare:'Casa cuadrifamiliar',capannone:'Nave',ufficio:'Oficina',negozio:'Local comercial',terreno:'Terreno','':'Inmueble'},attr:'Límites de regiones y municipios: ISTAT / © colaboradores de OpenStreetMap',zin:'Acercar',zout:'Alejar',area:'Zona de Padova',italy:'Italia',hint:'Arrastre para mover. Use la rueda, el pellizco o + y − para hacer zoom.',vc:['Venecia','Verona','Vicenza','Treviso','Padova','Belluno','Rovigo'],oc:['Roma','Milán','Nápoles','Turín','Florencia','Bolonia','Palermo','Cagliari','Bari','Génova','Trieste']},
pt:{vn:'Vêneto',pre:'pt-br/',sale:'À venda',rent:'Para alugar',note:'As cidades são reais. Cada ponto fica em uma posição inventada dentro da sua cidade, nunca no endereço real.',one:'imóvel',many:'imóveis',aria:'Mapa interativo dos imóveis',loc:'pt-BR',poa:'Preço sob consulta',pm:' / mês',types:{appartamento:'Apartamento',villa:'Villa',villetta:'Casa isolada',bifamiliare:'Casa bifamiliar',trifamiliare:'Casa trifamiliar',quadrifamiliare:'Casa quadrifamiliar',capannone:'Galpão',ufficio:'Escritório',negozio:'Loja',terreno:'Terreno','':'Imóvel'},attr:'Limites de regiões e cidades: ISTAT / © colaboradores do OpenStreetMap',zin:'Aproximar',zout:'Afastar',area:'Área de Pádua',italy:'Itália',hint:'Arraste para mover. Role, faça pinça ou use + e − para o zoom.',vc:['Veneza','Verona','Vicenza','Treviso','Pádua','Belluno','Rovigo'],oc:['Roma','Milão','Nápoles','Turim','Florença','Bolonha','Palermo','Cagliari','Bari','Gênova','Trieste']}
};
var D=T[L]||T.en,NS='/international/'+D.pre,NSV='http://www.w3.org/2000/svg';
function tc(s){return String(s||'').trim().toLowerCase().replace(/(^|[\s'-])([a-zà-ú])/g,function(m,a,b){return a+b.toUpperCase()})}
var STAGED={'LA0317':1};
function isai(u){return /foto[-_ ]?ai/i.test(String(u||''))}
function cover(c,fo){var f=fo[0]||'';if(f&&isai(f)&&!STAGED[c]){for(var k=1;k<fo.length;k++){if(!isai(fo[k]))return fo[k]}}return imgu(f)}
function imgu(u){if(!u)return'';u=String(u).trim();if(!u)return'';if(/^img\//.test(u))return 'https://righettoimmobiliare.it/'+u;if(!/^https?:/.test(u))u=SB+'/storage/v1/object/public/'+u.replace(/^\/+/,'');return u}
function thumb(u){return u.indexOf('/storage/v1/object/public/')>-1?u.replace('/object/public/','/render/image/public/')+'?width=360&quality=70':u}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function hash(s){var h=2166136261;for(var i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return h>>>0}
function rng(seed){var a=seed;return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function inside(p,x,y){var c=false;for(var i=0,j=p.length-1;i<p.length;j=i++){var a=p[i],b=p[j];if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0])c=!c}return c}
function edge(p,x,y){var m=1e9;for(var i=0,j=p.length-1;i<p.length;j=i++){var a=p[i],b=p[j],dx=b[0]-a[0],dy=b[1]-a[1],l=dx*dx+dy*dy,t=l?Math.max(0,Math.min(1,((x-a[0])*dx+(y-a[1])*dy)/l)):0,ex=a[0]+t*dx-x,ey=a[1]+t*dy-y,d=Math.sqrt(ex*ex+ey*ey);if(d<m)m=d}return m}
function mk(tag,at,par){var e=document.createElementNS(NSV,tag);for(var k in at)e.setAttribute(k,at[k]);if(par)par.appendChild(e);return e}
Promise.all([
 fetch('/international/assets/map-data.json?v=3').then(function(r){return r.json()}),
 fetch(SB+'/rest/v1/immobili?select=codice,tipo_operazione,tipologia,comune,prezzo,venduto,affittato,foto&attivo=eq.true&limit=300',{headers:{apikey:KEY,Authorization:'Bearer '+KEY}}).then(function(r){if(!r.ok)throw 0;return r.json()})
]).then(function(res){
 var M=res[0],rows=res[1].filter(function(r){return !r.venduto&&!r.affittato}).map(function(r){return{c:r.codice||'',op:(r.tipo_operazione||'vendita')==='vendita'?'sale':'rent',t:r.tipologia||'',com:tc(r.comune),pr:+r.prezzo||0,im:cover(r.codice||'',Array.isArray(r.foto)?r.foto:[])}});
 var by={};rows.forEach(function(r){(by[r.com]=by[r.com]||[]).push(r)});
 var nf=new Intl.NumberFormat(D.loc,{style:'currency',currency:'EUR',maximumFractionDigits:0});
 root.innerHTML='<div class="rw-pm-box"><svg role="img" aria-label="'+esc(D.aria)+'" focusable="false"></svg><div class="rw-pm-ctl"><button type="button" data-a="in" aria-label="'+esc(D.zin)+'">+</button><button type="button" data-a="out" aria-label="'+esc(D.zout)+'">−</button><button type="button" data-a="area" class="w">'+esc(D.area)+'</button><button type="button" data-a="it" class="w">'+esc(D.italy)+'</button></div></div><div class="rw-pm-leg"><span><i class="sale"></i>'+D.sale+'</span><span><i class="rent"></i>'+D.rent+'</span><b>'+rows.length+' '+(rows.length===1?D.one:D.many)+'</b></div><p class="rw-pm-note">'+D.note+' '+D.hint+'</p><p class="rw-pm-attr">'+D.attr+'</p>';
 var box=root.querySelector('.rw-pm-box'),svg=box.querySelector('svg');
 var tip=document.createElement('div');tip.className='rw-pm-tip';tip.hidden=true;box.appendChild(tip);
 function showTip(a,e){var im=a.getAttribute('data-im'),lab=a.getAttribute('data-lab')||'';tip.innerHTML=(im?'<img alt="" src="'+esc(thumb(im))+'" onerror="this.onerror=null;this.src=\''+esc(im)+'\'"/>':'')+'<span>'+esc(lab)+'</span>';tip.hidden=false;moveTip(e)}
 function moveTip(e){var r=box.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top,w=tip.offsetWidth,h=tip.offsetHeight;var l=Math.min(Math.max(4,x-w/2),r.width-w-4),t=y-h-14;if(t<4)t=y+18;tip.style.left=l+'px';tip.style.top=t+'px'}
 svg.addEventListener('mouseover',function(e){var a=e.target.closest&&e.target.closest('.rw-pm-dot');if(a&&!a.classList.contains('off'))showTip(a,e)});
 svg.addEventListener('mousemove',function(e){if(!tip.hidden)moveTip(e)});
 svg.addEventListener('mouseout',function(e){var a=e.target.closest&&e.target.closest('.rw-pm-dot');if(a)tip.hidden=true});
 svg.addEventListener('pointerdown',function(){tip.hidden=true},true);
 var gR=mk('g',{},svg),gO=mk('g',{},svg),gW=mk('g',{},svg),gV=mk('g',{},svg),gD=mk('g',{},svg),gC=mk('g',{},svg);
 var sized=[],vL=[],oL=[],dL=[],clD=null;
 function txt(par,x,y,s,px,cls,anchor){var t=mk('text',{x:x,y:y,'text-anchor':anchor||'start',class:cls},par);t.textContent=s;sized.push([t,px,'t']);return t}
 function dot(par,x,y,px,cls){var c=mk('circle',{cx:x,cy:y,class:cls},par);sized.push([c,px,'c']);return c}
 M.reg.forEach(function(r){mk('path',{d:r.d,class:'rw-pm-reg'+(r.v?' v':'')},gR)});
 M.oc.forEach(function(c,i){var d0=dot(gO,c[1],c[2],2.5,'rw-pm-od');var t=txt(gO,c[1],c[2],D.oc[i],10,'rw-pm-ot');t.setAttribute('data-dx',6);oL.push({t:t,d:d0,px:10,x:c[1],y:c[2],r:2.5})});
 var padT=null;txt(gW,398,92,D.vn||'Veneto',14,'rw-pm-vt','middle');

 M.vc.forEach(function(c,i){dot(gV,c[1],c[2],3.5,'rw-pm-vd');var t=txt(gV,c[1],c[2],D.vc[i],12,'rw-pm-vt');t.setAttribute('data-dx',[7,-7,-7,7,7,7,7][i]);if(i===1||i===2)t.setAttribute('text-anchor','end');if(c[0]==='Padova'){padT=t;t.setAttribute('data-dx',-20);t.setAttribute('text-anchor','end')}vL.push({t:t,d:gV.lastChild.previousSibling,px:12,x:c[1],y:c[2],r:3.5,p:c[0]==='Padova'?0:1})});
 // detail layer
 var dots=[],cx0=0,cy0=0,bx0=1e9,bx1=-1e9,by0=1e9,by1=-1e9,zb={};
 M.com.forEach(function(z){
  var xs=z.p.map(function(q){return q[0]}),ys=z.p.map(function(q){return q[1]}),x0=Math.min.apply(0,xs),x1=Math.max.apply(0,xs),y0=Math.min.apply(0,ys),y1=Math.max.apply(0,ys);
  zb[z.n]=[x0,y0,x1,y1];bx0=Math.min(bx0,x0);bx1=Math.max(bx1,x1);by0=Math.min(by0,y0);by1=Math.max(by1,y1);
  var n=(by[z.n]||[]).length;
  mk('path',{d:'M'+z.p.map(function(q){return q[0]+' '+q[1]}).join('L')+'Z',class:'rw-pm-area'+(n?' has':'')},gD);
  var list=(by[z.n]||[]).slice().sort(function(a,b){return a.c<b.c?-1:1}),placed=[];
  list.forEach(function(r){
   var rnd=rng(hash(r.c)),best=null,bd=-1;
   for(var k=0;k<800;k++){var x=x0+rnd()*(x1-x0),y=y0+rnd()*(y1-y0);if(!inside(z.p,x,y))continue;var e=edge(z.p,x,y);if(e<0.22)continue;var d=1e9;placed.forEach(function(q){d=Math.min(d,Math.hypot(q[0]-x,q[1]-y))});if(d>=0.5){best=[x,y];break}if(d>bd){bd=d;best=[x,y]}}
   if(!best)best=[z.c[0],z.c[1]];placed.push(best);dots.push({r:r,x:best[0],y:best[1],z:z});
  });
 });
 M.com.forEach(function(z){var n=(by[z.n]||[]).length,a=mk('a',{href:NS+'properties/?area='+encodeURIComponent(z.n),class:'rw-pm-lbl'+(n?'':' none'),'data-area':z.n},gD);var tt=txt(a,z.c[0],zb[z.n][1]-0.12,z.n+(n?' · '+n:''),13,'rw-pm-ct','middle');dL.push({a:a,t:tt,n:n,z:z,b:zb[z.n]})});
 dots.forEach(function(d){var r=d.r,ty=(D.types[r.t]||D.types['']),price=r.pr?nf.format(r.pr)+(r.op==='rent'?D.pm:''):D.poa,lab=ty+' · '+r.com+' · '+price+' · '+r.c;
  var a=mk('a',{href:NS+'property/?ref='+encodeURIComponent(r.c),class:'rw-pm-dot '+r.op,'aria-label':lab,'data-op':r.op,'data-t':r.t,'data-com':r.com,'data-pr':r.pr},gD);dot(a,d.x,d.y,7,'');if(r.im)a.setAttribute('data-im',r.im);a.setAttribute('data-lab',lab)});
 // cluster marker
 var ccx=(bx0+bx1)/2,ccy=(by0+by1)/2;
 var ca=mk('a',{href:'#','class':'rw-pm-cl','aria-label':D.area+' · '+rows.length},gC);clD={x:ccx,y:ccy};dot(ca,ccx,ccy,15,'');txt(ca,ccx,ccy,String(rows.length),12,'rw-pm-cn','middle');
 // view
 var BH=M.h+30,Z={x:405,y:150,z:3.4},ZT=22,cw=1,ch=1,detail=null;
 function size(){var r=box.getBoundingClientRect();cw=r.width||600;ch=r.height||500;BH=Math.max(M.h+30,(M.w+40)*ch/cw)}
 function clamp(){Z.z=Math.max(1,Math.min(260,Z.z));var h=BH/Z.z,w=h*cw/ch;Z.x=Math.max(-w*0.1,Math.min(M.w+w*0.1,Z.x));Z.y=Math.max(0,Math.min(M.h,Z.y))}
 function draw(){size();clamp();var h=BH/Z.z,w=h*cw/ch,s=h/ch;svg.setAttribute('viewBox',(Z.x-w/2)+' '+(Z.y-h/2)+' '+w+' '+h);
  sized.forEach(function(e){var el=e[0],px=e[1]*s;if(e[2]==='c'){el.setAttribute('r',px)}else{el.setAttribute('font-size',px);var dx=+el.getAttribute('data-dx')||0,pv=el.previousSibling;if(dx&&pv){el.setAttribute('x',(+pv.getAttribute('cx'))+dx*s);el.setAttribute('y',(+pv.getAttribute('cy'))+px*0.35)}else{var y0=el.getAttribute('data-y0');if(y0===null){y0=el.getAttribute('y');el.setAttribute('data-y0',y0)}el.setAttribute('y',+y0+px*0.35)}}});
  svg.style.setProperty('--s',s);
  declutter(w,h,s);
  var det=Z.z>=ZT;if(det!==detail){detail=det;gD.style.display=det?'':'none';gC.style.display=det?'none':'';if(padT)padT.style.display=det?'none':''}
  var cityOn=true;gV.style.display=cityOn?'':'none';gW.style.display=cityOn?'none':'';
  svg.style.touchAction=Z.z>1.02?'none':'pan-y';}

 function declutter(w,h,s){
  if(!dL.length)return;
  var X0=Z.x-w/2,Y0=Z.y-h/2,k=cw/w,acc=[];
  function sx(x){return (x-X0)*k}function sy(y){return (y-Y0)*k}
  function hit(a,ign){for(var i=0;i<acc.length;i++){var b=acc[i];if(b===ign)continue;if(a[0]<b[2]+3&&a[2]>b[0]-3&&a[1]<b[3]+2&&a[3]>b[1]-2)return true}return false}
  function bx(t,cx,cy,px,an){var wd=t.textContent.length*px*0.6,x=an==='end'?cx-wd:an==='middle'?cx-wd/2:cx;return[x,cy-px*0.85,x+wd,cy+px*0.3]}
  function inview(r){return r[0]>=3&&r[2]<=cw-3&&r[1]>=3&&r[3]<=ch-3}
  function ring(X,Y,off,an0){var c=[],rs=[off,off+14,off+28,off+44,off+62,off+84],A=[[0,-1],[0,1],[1,0],[-1,0],[.7,-.7],[-.7,-.7],[.7,.7],[-.7,.7]];rs.forEach(function(r){A.forEach(function(a){c.push([a[0]>0.3?'start':a[0]<-0.3?'end':'middle',X+a[0]*r,Y+a[1]*r])})});return c}
  function put(t,px,cands,ign,force){
   var best=null;
   for(var i=0;i<cands.length;i++){var c=cands[i],yb=c[2]+(c[3]===1?0:0),r=bx(t,c[1],yb,px,c[0]);if(inview(r)&&!hit(r,ign)){best=[c,r];break}}
   if(!best&&force&&cands.length){var c0=cands[0];best=[c0,bx(t,c0[1],c0[2],px,c0[0])]}
   if(!best)return false;
   acc.push(best[1]);t.setAttribute('text-anchor',best[0][0]);t.setAttribute('x',X0+best[0][1]/k);t.setAttribute('y',Y0+best[0][2]/k);return true}
  if(Z.z>=ZT){
   var dd=[];dots.forEach(function(d){var X=sx(d.x),Y=sy(d.y);var r=[X-7,Y-7,X+7,Y+7];dd.push(r);acc.push(r)});
   var ord=dL.slice().sort(function(a,b){return (b.n>0)-(a.n>0)||b.n-a.n||(b.b[2]-b.b[0])*(b.b[3]-b.b[1])-(a.b[2]-a.b[0])*(a.b[3]-a.b[1])});
   ord.forEach(function(L2){
    var px=13,X=sx(L2.z.c[0]),Yt=sy(L2.b[1]),Yc=sy(L2.z.c[1]);
    if(X<-120||X>cw+120||Yt>ch+60||sy(L2.b[3])<-60){L2.a.style.display='none';return}
    var c=[['middle',X,Yt-3+px*0.3],['middle',X,Yc+px*0.3]].concat(ring(X,Yc,px*0.9,'middle').map(function(q){return[q[0],q[1],q[2]+px*0.3]}));
    var okp=put(L2.t,px,c,null,false);if(!okp){var sv=acc;acc=acc.filter(function(b){return dd.indexOf(b)<0});okp=put(L2.t,px,c,null,false);var nl=acc.slice(sv.filter(function(b){return dd.indexOf(b)<0}).length);acc=sv.concat(nl)}L2.a.style.display=okp?'':'none';
   });
  }else{
   if(clD){var X=sx(clD.x),Y=sy(clD.y);acc.push([X-15,Y-15,X+15,Y+15])}
   var dots2={};vL.concat(oL).forEach(function(o){var X=sx(o.x),Y=sy(o.y),r=[X-o.r-1,Y-o.r-1,X+o.r+1,Y+o.r+1];o.self=r;acc.push(r)});
   vL.slice().sort(function(a,b){return a.p-b.p}).concat(oL).forEach(function(o){
    var px=o.px,X=sx(o.x),Y=sy(o.y),off=o.r+4;
    if(X<-120||X>cw+120||Y<-60||Y>ch+60){o.t.style.display='none';return}
    if(Z.z<2.4&&o.p===1&&vL.indexOf(o)>-1){o.t.style.display='none';return}
    var c=[];
    if(o.p===0&&clD){var CX=sx(clD.x),CY=sy(clD.y);c.push(['middle',CX,CY+15+px+2],['middle',CX,CY-15-3])}
    c.push(['start',X+off,Y+px*0.35],['end',X-off,Y+px*0.35],['middle',X,Y-off-2],['middle',X,Y+off+px*0.9]);
    c=c.concat(ring(X,Y,off+2).map(function(q){return[q[0],q[1],q[2]+px*0.3]}));
    o.t.style.display=put(o.t,px,c,o.self,false)?'':'none';
   });
  }
 }
 var raf=0;
 function go(x,y,z,ms){cancelAnimationFrame(raf);if(!ms){Z.x=x;Z.y=y;Z.z=z;draw();return}var a={x:Z.x,y:Z.y,lz:Math.log(Z.z)},b={x:x,y:y,lz:Math.log(z)},t0=performance.now();(function f(t){var k=Math.min(1,(t-t0)/ms);k=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;Z.x=a.x+(b.x-a.x)*k;Z.y=a.y+(b.y-a.y)*k;Z.z=Math.exp(a.lz+(b.lz-a.lz)*k);draw();if(k<1)raf=requestAnimationFrame(f)})(t0)}

 root.__pmGo=function(x,y,z){go(x,y,z,0)};
 function fit(x0,y0,x1,y1,pad){size();var w=(x1-x0)*pad,h=(y1-y0)*pad,z=Math.min(BH/h,(BH*cw/ch)/w);go((x0+x1)/2,(y0+y1)/2,Math.min(z,250),350)}
 function toArea(){fit(bx0,by0,bx1,by1,1.3)}
 function zoomAt(f,px,py){size();var h=BH/Z.z,w=h*cw/ch,ux=Z.x-w/2+px/cw*w,uy=Z.y-h/2+py/ch*h,nz=Math.max(1,Math.min(260,Z.z*f)),nh=BH/nz,nw=nh*cw/ch;go(ux-(px/cw-.5)*nw,uy-(py/ch-.5)*nh,nz,0)}
 root.querySelector('.rw-pm-ctl').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var a=b.dataset.a;if(a==='in')go(Z.x,Z.y,Z.z*2,200);if(a==='out')go(Z.x,Z.y,Z.z/2,200);if(a==='area')toArea();if(a==='it')go(M.w/2,M.h/2,1,350)});
 box.addEventListener('wheel',function(e){if(e.deltaY>0&&Z.z<=1)return;e.preventDefault();var r=box.getBoundingClientRect();zoomAt(e.deltaY<0?1.25:0.8,e.clientX-r.left,e.clientY-r.top)},{passive:false});
 var P={},drag=0,pd=0,last=null;
 svg.addEventListener('pointerdown',function(e){P[e.pointerId]={x:e.clientX,y:e.clientY};drag=0;last=null;if(Object.keys(P).length===2){var k=Object.keys(P),a=P[k[0]],b=P[k[1]];pd=Math.hypot(a.x-b.x,a.y-b.y)}});
 svg.addEventListener('pointermove',function(e){var p=P[e.pointerId];if(!p)return;var ks=Object.keys(P),dx=e.clientX-p.x,dy=e.clientY-p.y;
  if(ks.length===2){P[e.pointerId]={x:e.clientX,y:e.clientY};var a=P[ks[0]],b=P[ks[1]],d=Math.hypot(a.x-b.x,a.y-b.y);if(pd&&d){var r=box.getBoundingClientRect();zoomAt(d/pd,(a.x+b.x)/2-r.left,(a.y+b.y)/2-r.top);}pd=d;drag=9;return}
  if(!drag&&Math.hypot(dx,dy)<5)return;if(Z.z<=1.02&&e.pointerType==='touch')return;if(!drag){drag=1;try{svg.setPointerCapture(e.pointerId)}catch(_){}}
  var s=(BH/Z.z)/ch;Z.x-=dx*s;Z.y-=dy*s;P[e.pointerId]={x:e.clientX,y:e.clientY};draw()});
 function up(e){delete P[e.pointerId];pd=0;if(!Object.keys(P).length)setTimeout(function(){drag=0},0)}
 svg.addEventListener('pointerup',up);svg.addEventListener('pointercancel',up);
 svg.addEventListener('click',function(e){if(drag){e.preventDefault();e.stopPropagation();return}var cl=e.target.closest&&e.target.closest('.rw-pm-cl');if(cl){e.preventDefault();toArea()}},true);
 window.addEventListener('resize',draw);
 draw();
 if(window.ResizeObserver)new ResizeObserver(draw).observe(box);
 if(root.getAttribute('data-cat')){
  var grp=function(t){return /terreno/.test(t)?'land':/capannone|ufficio|negozio/.test(t)?'com':'homes'},la='';
  var sync=function(){var g=function(k){var e=document.getElementById('rwp-'+k);return e?e.value:''},op=g('op'),ty=g('type'),ar=g('area'),mx=+g('max');
   root.querySelectorAll('.rw-pm-dot').forEach(function(a){var ok=true;if(op==='buy'&&a.dataset.op!=='sale')ok=false;if(op==='rent'&&a.dataset.op!=='rent')ok=false;if(ty&&grp(a.dataset.t)!==ty)ok=false;if(ar&&a.dataset.com!==ar)ok=false;if(mx&&(!+a.dataset.pr||+a.dataset.pr>mx))ok=false;a.classList.toggle('off',!ok)});
   root.querySelectorAll('.rw-pm-lbl').forEach(function(a){a.classList.toggle('sel',!!ar&&a.dataset.area===ar)});
   if(ar!==la){la=ar;if(ar&&zb[ar])fit(zb[ar][0],zb[ar][1],zb[ar][2],zb[ar][3],1.8);else if(!ar&&Z.z>=ZT)toArea()}};
  root.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.rw-pm-lbl');if(!a||drag)return;var s=document.getElementById('rwp-area');if(!s)return;e.preventDefault();s.value=(s.value===a.dataset.area)?'':a.dataset.area;s.dispatchEvent(new Event('change',{bubbles:true}));var c=document.getElementById('rwp-count');if(c&&c.scrollIntoView)setTimeout(function(){c.scrollIntoView({behavior:'smooth',block:'center'})},400)});
  document.addEventListener('rwfilter',sync);sync();
 }
}).catch(function(){root.innerHTML='<p class="rw-fine">'+D.note+'</p>'});
})();
