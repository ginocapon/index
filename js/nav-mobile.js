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
    injectGestionaleDropdown();
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

/* ═══ GESTIONALE DROPDOWN (quando loggato) ═══ */
function injectGestionaleDropdown(){
  var navLinks = document.querySelector('.nav-links');   // index.html
  var hiNav = document.querySelector('.hi nav');          // other pages
  var hcta = document.querySelector('.h-cta');
  var target = null;

  if(navLinks){
    target = navLinks;
  } else if(hiNav){
    target = hiNav;
  }

  if(!target) return;

  var wrap = document.createElement('div');
  wrap.className = 'gestionale-wrap';
  if(navLinks){
    var li = document.createElement('li');
    li.appendChild(wrap);
    var lastLi = navLinks.querySelector('.nav-cta');
    if(lastLi && lastLi.parentElement){
      navLinks.insertBefore(li, lastLi.parentElement);
    } else {
      navLinks.appendChild(li);
    }
  } else {
    var headerInner = target.parentElement;
    if(hcta){
      headerInner.insertBefore(wrap, hcta);
    } else {
      target.insertAdjacentElement('afterend', wrap);
    }
  }

  wrap.innerHTML = '\
    <button class="gestionale-btn" onclick="toggleGestionaleMenu(this)">\
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>\
      Gestionale\
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\
    </button>\
    <div class="gestionale-menu" id="gestionaleMenu">\
      <a href="admin.html#posta">\
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 7L2 7"/></svg>\
        Mail\
      </a>\
      <a href="admin.html#immobili">\
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>\
        Admin Immobili\
      </a>\
      <a href="admin.html#blog">\
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>\
        Articoli Blog\
      </a>\
      <div class="gestionale-menu-divider"></div>\
      <a href="admin.html#clienti">\
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>\
        Clienti\
      </a>\
      <a href="admin.html#impostazioni">\
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09"/></svg>\
        Impostazioni\
      </a>\
    </div>';

  // Close menu on click outside
  document.addEventListener('click', function(e){
    if(!wrap.contains(e.target)){
      var menu = document.getElementById('gestionaleMenu');
      if(menu) menu.classList.remove('open');
      wrap.querySelector('.gestionale-btn').classList.remove('open');
    }
  });
}

function injectGestionaleMobile(){
  var panel = document.getElementById('navMobile');
  if(!panel) return;

  var section = document.createElement('div');
  section.className = 'gestionale-mobile-section';
  section.innerHTML = '\
    <span class="gestionale-mobile-label">Gestionale</span>\
    <a href="admin.html#posta">\
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 7l-10 7L2 7"/></svg>\
      Mail\
    </a>\
    <a href="admin.html#immobili">\
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>\
      Admin Immobili\
    </a>\
    <a href="admin.html#blog">\
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>\
      Articoli Blog\
    </a>\
    <a href="admin.html#clienti">\
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>\
      Clienti\
    </a>\
    <a href="admin.html#impostazioni">\
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33"/></svg>\
      Impostazioni\
    </a>';
  panel.appendChild(section);
}

function toggleGestionaleMenu(btn){
  var menu = document.getElementById('gestionaleMenu');
  if(!menu) return;
  menu.classList.toggle('open');
  btn.classList.toggle('open');
}
