/* ═══ HAMBURGER MENU + LOGIN/GESTIONALE — Tutte le pagine ═══ */
document.addEventListener('DOMContentLoaded', function(){

  // ── Hamburger Menu ──
  var btn = document.getElementById('burgerBtn');
  var panel = document.getElementById('navMobile');
  if(btn && panel){
    btn.setAttribute('aria-expanded','false');
    panel.inert = true;
    btn.setAttribute('aria-controls','navMobile');
    btn.addEventListener('click', function(){
      this.classList.toggle('open');
      panel.classList.toggle('open');
      this.setAttribute('aria-expanded', panel.classList.contains('open') ? 'true' : 'false');
      panel.inert = !panel.classList.contains('open');
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && panel.classList.contains('open')){
        btn.classList.remove('open');
        panel.classList.remove('open');
        btn.setAttribute('aria-expanded','false');
        panel.inert = true;
        btn.focus();
      }
    });
    panel.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){
        btn.classList.remove('open');
        panel.classList.remove('open');
        btn.setAttribute('aria-expanded','false');
        panel.inert = true;
      });
    });
  }

  // ── Login / Gestionale (desktop + mobile) ──
  if(sessionStorage.getItem('rig_admin') === 'ok'){
    injectGestionaleLink();
    injectGestionaleMobile();
  }
  // Public login links removed by owner's request. Direct /admin remains unchanged.
});

/* ═══ LINK DIRETTO GESTIONALE (quando loggato) ═══ */
function injectGestionaleLink(){
  var navLinks = document.querySelector('.nav-links');   // index.html
  var hiNav = document.querySelector('.hi nav');          // other pages
  var hcta = document.querySelector('.h-cta');

  var link = document.createElement('a');
  link.href = 'admin.html';
  link.className = 'gestionale-link';
  link.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg> Gestionale';

  if(navLinks){
    var li = document.createElement('li');
    li.appendChild(link);
    var ctaLi = navLinks.querySelector('.nav-cta');
    if(ctaLi && ctaLi.parentElement){
      navLinks.insertBefore(li, ctaLi.parentElement);
    } else {
      navLinks.appendChild(li);
    }
  } else if(hiNav){
    var headerInner = hiNav.parentElement;
    if(hcta){
      headerInner.insertBefore(link, hcta);
    } else {
      hiNav.insertAdjacentElement('afterend', link);
    }
  }
}

function injectGestionaleMobile(){
  var panel = document.getElementById('navMobile');
  if(!panel) return;

  var link = document.createElement('a');
  link.href = 'admin.html';
  link.className = 'nav-mobile-login';
  link.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg> Gestionale';
  panel.appendChild(link);
}
