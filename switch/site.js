(function(){
  var trigs=[].slice.call(document.querySelectorAll('.marr'));
  trigs.forEach(function(b){b.addEventListener('click',function(){var open=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!open));b.closest('.msec').querySelector('.msub').hidden=open;});});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&document.activeElement&&document.activeElement.closest('.dd'))document.activeElement.blur();});
})();

document.addEventListener('click', function(e) {
  var link = e.target.closest('a[href*="wa.me"]');
  if (link) {
    var isFloating = function(a){ return !!a.closest('.mbar') || getComputedStyle(a).position === 'fixed'; };
    var inPage = [].slice.call(document.querySelectorAll('a[href*="wa.me"]')).filter(function(a){ return !isFloating(a); });
    var pos = isFloating(link) ? 'floating' : (inPage.indexOf(link) === 0 ? 'top' : 'lower');
    gtag('event', 'whatsapp_click', {'link_url': link.href, 'page_location': location.href, 'page_path': location.pathname, 'button_position': pos, 'transport_type': 'beacon'});
  }
  var tel = e.target.closest('a[href^="tel:"]');
  if (tel) { gtag('event', 'phone_click', {'link_url': tel.href, 'page_location': location.href}); }
});
document.addEventListener('submit', function(e) {
  gtag('event', 'booking_request', {'form_destination': e.target.action || '', 'page_location': location.href, 'transport_type': 'beacon'});
});

// GA4: count when someone starts filling in a booking form (form_start), alongside booking_request on submit
document.addEventListener('focusin', function(e) {
  var f = e.target.closest && e.target.closest('form');
  if (!f || f.dataset.started) return;
  f.dataset.started = '1';
  gtag('event', 'form_start', {'page_path': location.pathname, 'form_destination': f.action || ''});
});

(function(){
  if(!window.matchMedia||!matchMedia('(hover:hover) and (pointer:fine)').matches)return;
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var HX=8,HY=13; /* brush tip inside the image */
  var f=document.createElement('div');f.id='fairy';f.setAttribute('aria-hidden','true');
  f.innerHTML='<img src="../img/fairy-cursor.webp" alt="">';document.body.appendChild(f);
  document.documentElement.classList.add('fairy-on');
  var x=-100,y=-100,lx=0,ly=0,last=0,shown=false;
  function dust(n,spread){for(var i=0;i<n;i++){var d=document.createElement('span');d.className='fdust';
    var a=Math.random()*6.28,r=(spread||14)*Math.random();
    d.style.left=(x-3)+'px';d.style.top=(y-3)+'px';
    d.style.setProperty('--dx',(Math.cos(a)*r)+'px');d.style.setProperty('--dy',(Math.sin(a)*r+18)+'px');
    document.body.appendChild(d);setTimeout(function(e){e.remove()},950,d);}}
  document.addEventListener('mousemove',function(e){
    x=e.clientX;y=e.clientY;
    if(!shown){f.style.opacity=1;shown=true;}
    f.style.transform='translate('+(x-HX)+'px,'+(y-HY)+'px)';
    var now=performance.now(),dist=Math.abs(x-lx)+Math.abs(y-ly);
    if(dist>14&&now-last>30){dust(1,10);lx=x;ly=y;last=now;}
    var hot=e.target.closest&&e.target.closest('a,button,summary,label,[role=button]');
    f.classList.toggle('hot',!!hot);
  },{passive:true});
  document.addEventListener('mousedown',function(){f.classList.add('down');dust(10,34);});
  document.addEventListener('mouseup',function(){f.classList.remove('down');});
  document.documentElement.addEventListener('mouseleave',function(){f.style.opacity=0;shown=false;});
  /* over a form field, show the normal text cursor instead of the fairy */
  document.addEventListener('mouseover',function(e){var t=e.target.closest&&e.target.closest('input,textarea,select');f.style.visibility=t?'hidden':'visible';});
})();
