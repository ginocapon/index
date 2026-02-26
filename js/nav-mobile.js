/* ═══ HAMBURGER MENU — Tutte le pagine ═══ */
document.addEventListener('DOMContentLoaded', function(){
  var btn = document.getElementById('burgerBtn');
  var panel = document.getElementById('navMobile');
  if(!btn || !panel) return;
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
});
