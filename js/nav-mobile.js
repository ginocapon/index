/* ═══ HAMBURGER MENU + LOGIN/GESTIONALE — Tutte le pagine ═══ */
document.addEventListener('DOMContentLoaded', function(){

  // ── Hamburger Menu ──
  var btn = document.getElementById('burgerBtn');
  var panel = document.getElementById('navMobile');
  if(btn && panel){
    btn.addEventListener('click', function(){
      this.classList.toggle('open');
      panel.classList.toggle('open');
    });
    panel.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){
        btn.classList.remove('open');
        panel.classList.remove('open');
      });
    });
  }

  // ── Login / Gestionale (desktop + mobile) ──
  if(sessionStorage.getItem('rig_admin') === 'ok'){
    injectGestionaleLink();
    injectGestionaleMobile();
  } else {
    injectLoginButton();
    injectLoginMobile();
  }
});

/* ═══ PULSANTE LOGIN (quando NON loggato) ═══ */
function injectLoginButton(){
  var navLinks = document.querySelector('.nav-links');   // index.html
  var hiNav = document.querySelector('.hi nav');          // other pages
  var hcta = document.querySelector('.h-cta');

  if(navLinks){
    var li = document.createElement('li');
    li.innerHTML = '<a href="admin.html" class="nav-login-btn">Accedi</a>';
    var ctaLi = navLinks.querySelector('.nav-cta');
    if(ctaLi && ctaLi.parentElement){
      navLinks.insertBefore(li, ctaLi.parentElement);
    } else {
      navLinks.appendChild(li);
    }
  } else if(hiNav){
    var loginBtn = document.createElement('a');
    loginBtn.href = 'admin.html';
    loginBtn.className = 'nav-login-btn';
    loginBtn.textContent = 'Accedi';
    var headerInner = hiNav.parentElement;
    if(hcta){
      headerInner.insertBefore(loginBtn, hcta);
    } else {
      hiNav.insertAdjacentElement('afterend', loginBtn);
    }
  }
}

function injectLoginMobile(){
  var panel = document.getElementById('navMobile');
  if(!panel) return;
  var loginLink = document.createElement('a');
  loginLink.href = 'admin.html';
  loginLink.className = 'nav-mobile-login';
  loginLink.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg> Accedi';
  panel.appendChild(loginLink);
}

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
