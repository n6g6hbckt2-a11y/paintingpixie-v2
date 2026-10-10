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

(function(){
  /* phones and tablets: no mouse, so the fairy flies across the screen by herself every so often,
     and flies to wherever you tap, with a puff of pixie dust */
  if(!window.matchMedia||matchMedia('(hover:hover) and (pointer:fine)').matches)return;
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var f=document.createElement('div');f.id='fairy';f.className='fly';f.setAttribute('aria-hidden','true');
  f.innerHTML='<img src="../img/fairy-cursor.webp" alt="">';document.body.appendChild(f);
  var W=innerWidth,H=innerHeight,x=-80,y=0,path=null,t0=0,dur=0,raf=0,lastDust=0,wait=0,typing=false;
  addEventListener('resize',function(){W=innerWidth;H=innerHeight;},{passive:true});
  function dust(n,spread){for(var i=0;i<n;i++){var d=document.createElement('span');d.className='fdust';
    var a=Math.random()*6.28,r=(spread||12)*Math.random();
    d.style.left=(x+10)+'px';d.style.top=(y+14)+'px';
    d.style.setProperty('--dx',(Math.cos(a)*r)+'px');d.style.setProperty('--dy',(Math.sin(a)*r+18)+'px');
    document.body.appendChild(d);setTimeout(function(e){e.remove()},950,d);}}
  function bez(p,t){var u=1-t;return u*u*u*p[0]+3*u*u*t*p[1]+3*u*t*t*p[2]+t*t*t*p[3];}
  function fly(x1,y1,ms,after){   /* curved flight from where she is to (x1,y1) */
    var x0=x,y0=y,lift=(Math.random()*.5+.2)*H*(Math.random()<.5?-1:1)*.4;
    path={x:[x0,x0+(x1-x0)*.33,x0+(x1-x0)*.66,x1],y:[y0,y0+lift,y1-lift,y1],after:after};
    t0=performance.now();dur=ms;f.classList.toggle('right',x1>x0);
    if(!raf)raf=requestAnimationFrame(step);}
  function step(now){
    raf=0;if(!path)return;
    var t=Math.min(1,(now-t0)/dur),e=t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
    x=bez(path.x,e);y=bez(path.y,e)+Math.sin(now/180)*4;
    f.style.transform='translate('+x+'px,'+y+'px)';
    if(now-lastDust>70){dust(1,8);lastDust=now;}
    if(t<1)raf=requestAnimationFrame(step);else{var a=path.after;path=null;a&&a();}}
  function crossing(){   /* in from one side, out the other */
    if(document.hidden||typing){later();return;}
    var ltr=Math.random()<.5;x=ltr?-70:W+10;y=H*(.15+Math.random()*.5);f.style.opacity=1;
    fly(ltr?W+10:-70,H*(.15+Math.random()*.5),5200+Math.random()*2000,function(){f.style.opacity=0;later();});}
  function later(){clearTimeout(wait);wait=setTimeout(crossing,9000+Math.random()*9000);}
  document.addEventListener('touchstart',function(e){
    if(typing||!e.touches[0])return;
    var tx=e.touches[0].clientX-10,ty=e.touches[0].clientY-14;
    if(f.style.opacity!=='1'){x=tx<W/2?-70:W+10;y=ty-60;f.style.opacity=1;}
    clearTimeout(wait);
    fly(tx,ty,650,function(){dust(12,34);setTimeout(function(){
      fly(x<W/2?-70:W+10,y-H*.2,1600,function(){f.style.opacity=0;later();});},700);});
  },{passive:true});
  /* stay out of the way while someone fills in the form */
  document.addEventListener('focusin',function(e){if(e.target.closest&&e.target.closest('input,textarea,select')){typing=true;f.style.opacity=0;path=null;}});
  document.addEventListener('focusout',function(){typing=false;});
  setTimeout(crossing,2500);
})();
