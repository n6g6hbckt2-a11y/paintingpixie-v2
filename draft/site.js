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
  if(!window.matchMedia||!window.PointerEvent)return;
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var HX=8,HY=13; /* brush tip inside the image */
  var f=null;
  function start(){f=document.createElement('div');f.id='fairy';f.setAttribute('aria-hidden','true');
    f.innerHTML='<img src="../img/fairy-cursor.webp" alt="">';document.body.appendChild(f);
    document.documentElement.classList.add('fairy-on');document.dispatchEvent(new Event('fairy-mouse'));}
  var x=-100,y=-100,lx=0,ly=0,last=0,shown=false;
  function dust(n,spread){for(var i=0;i<n;i++){var d=document.createElement('span');d.className='fdust';
    var a=Math.random()*6.28,r=(spread||14)*Math.random();
    d.style.left=(x-3)+'px';d.style.top=(y-3)+'px';
    d.style.setProperty('--dx',(Math.cos(a)*r)+'px');d.style.setProperty('--dy',(Math.sin(a)*r+18)+'px');
    document.body.appendChild(d);setTimeout(function(e){e.remove()},950,d);}}
  document.addEventListener('pointermove',function(e){
    if(e.pointerType!=='mouse')return;   /* fingers and pencils: the flying fairy handles those */
    if(!f)start();
    x=e.clientX;y=e.clientY;
    if(!shown){f.style.opacity=1;shown=true;}
    f.style.transform='translate('+(x-HX)+'px,'+(y-HY)+'px)';
    var now=performance.now(),dist=Math.abs(x-lx)+Math.abs(y-ly);
    if(dist>14&&now-last>30){dust(1,10);lx=x;ly=y;last=now;}
    var hot=e.target.closest&&e.target.closest('a,button,summary,label,[role=button]');
    f.classList.toggle('hot',!!hot);
  },{passive:true});
  document.addEventListener('pointerdown',function(e){if(!f||e.pointerType!=='mouse')return;f.classList.add('down');dust(10,34);});
  document.addEventListener('pointerup',function(){if(f)f.classList.remove('down');});
  document.documentElement.addEventListener('mouseleave',function(){if(f){f.style.opacity=0;shown=false;}});
  /* over a form field, show the normal text cursor instead of the fairy */
  document.addEventListener('mouseover',function(e){if(!f)return;var t=e.target.closest&&e.target.closest('input,textarea,select');f.style.visibility=t?'hidden':'visible';});
})();

(function(){
  /* Phones and tablets (no mouse): Kat's fairy has a life of her own. She flies across now and then,
     hides behind photos and peeks out with a giggle, hovers to sprinkle fairy dust, and flies to wherever you tap.
     Flapping wings, banking and depth make her look 3D. Sound only after someone taps (browser rule), and quietly. */
  if(!window.matchMedia)return;
  var touch=(navigator.maxTouchPoints||0)>0||('ontouchstart' in window);
  if(!touch&&matchMedia('(hover:hover) and (pointer:fine)').matches)return;
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var FW=66,FH=72;
  var f=document.createElement('div');f.id='fairyfly';f.setAttribute('aria-hidden','true');
  f.innerHTML='<div class="ff-d"><div class="ff-t"><div class="ff-b"><img class="ff-w2" src="../img/fairy-wing.webp" alt=""><img class="ff-w" src="../img/fairy-wing.webp" alt=""><img class="ff-legs" src="../img/fairy-legs.webp" alt=""><img class="ff-body" src="../img/fairy-body.webp" alt=""><img class="ff-arm" src="../img/fairy-arm.webp" alt=""></div></div></div>';
  document.body.appendChild(f);
  var d=f.querySelector('.ff-d'),tw=f.querySelector('.ff-t'),sayW=document.createElement('div'),say,lastWand=0;
  sayW.id='ffsay';sayW.setAttribute('aria-hidden','true');sayW.innerHTML='<span></span>';document.body.appendChild(sayW);say=sayW.firstChild;   /* speech bubble sits outside her so a photo never hides it */
  function cls(c,ms){f.classList.add(c);setTimeout(function(){f.classList.remove(c);},ms);}
  function wave(ms){cls('wave',ms||1300);}                       /* wave her wand (brush), with sparkles off the tip */
  function twirl(){tw.classList.remove('loop');tw.classList.add('twirl');setTimeout(function(){tw.classList.remove('twirl');},750);}
  function loop(){tw.classList.remove('twirl');tw.classList.add('loop');setTimeout(function(){tw.classList.remove('loop');},950);}
  function tip(){return [x+(face>0?.13:.87)*FW,y+.13*FH];}
  var W=innerWidth,H=innerHeight,x=-90,y=0,face=1,bank=0,z=1,path=null,t0=0,dur=0,raf=0,lastDust=0,wait=0,busy=false,typing=false,hideEl=null,alive=true,sparks=0;
  addEventListener('resize',function(){W=innerWidth;H=innerHeight;},{passive:true});
  var COLS=['#FFD24F','#FFF3B0','#FF8FD8','#C9A7FF','#8FF0FF','#FFFFFF'];
  function spark(px,py,spread,up,big){
    if(sparks>80)return;sparks++;
    var s=document.createElement('i');s.className='ffs'+(Math.random()<.35?' dot':'');
    var a=Math.random()*6.283,r=spread*(.3+Math.random()*.7),sz=(big?7:4)+Math.random()*(big?7:4),t=.8+Math.random()*.7;
    s.style.cssText='--x0:'+px+'px;--y0:'+py+'px;--dx:'+(Math.cos(a)*r)+'px;--dy:'+(Math.sin(a)*r-(up||0))+'px;--s:'+sz+'px;--c:'+COLS[Math.random()*COLS.length|0]+';--t:'+t+'s';
    document.body.appendChild(s);setTimeout(function(){s.remove();sparks--;},t*1000+50);}
  function burst(px,py,n){for(var i=0;i<n;i++)spark(px,py,30+Math.random()*40,10,i%3==0);}
  /* sound: a tiny synthesised giggle, only once someone has tapped */
  var ac=null,lastLaugh=0;
  function unlock(){if(ac)return;try{ac=new (window.AudioContext||window.webkitAudioContext)();}catch(e){}}
  function laugh(){
    if(!ac)return;if(ac.state==='suspended'&&ac.resume)ac.resume();
    var now=performance.now();if(now-lastLaugh<3000)return;lastLaugh=now;
    var t=ac.currentTime+.03,n=4+(Math.random()*2|0),base=820+Math.random()*140,out=ac.createGain();out.gain.value=.09;out.connect(ac.destination);
    for(var i=0;i<n;i++){var st=t+i*.105,f0=base*(1-i*.07),o=ac.createOscillator(),g=ac.createGain(),pk=ac.createBiquadFilter();
      o.type='triangle';o.frequency.setValueAtTime(f0*.88,st);o.frequency.linearRampToValueAtTime(f0*1.18,st+.03);o.frequency.linearRampToValueAtTime(f0*.8,st+.085);
      pk.type='peaking';pk.frequency.value=2600;pk.Q.value=1.2;pk.gain.value=9;
      g.gain.setValueAtTime(.0001,st);g.gain.exponentialRampToValueAtTime(1,st+.012);g.gain.exponentialRampToValueAtTime(.0001,st+.09);
      o.connect(pk);pk.connect(g);g.connect(out);o.start(st);o.stop(st+.1);}}
  var LINES=['hee hee!','tee-hee!','peekaboo!','hee hee hee!'];
  function giggle(text,sound){
    say.textContent=text||LINES[Math.random()*LINES.length|0];say.classList.add('on');f.classList.add('giggle');twirl();wave(1400);
    if(sound)laugh();
    setTimeout(function(){say.classList.remove('on');f.classList.remove('giggle');},1300);}
  function bez(p,t){var u=1-t;return u*u*u*p[0]+3*u*u*t*p[1]+3*u*t*t*p[2]+t*t*t*p[3];}
  /* fly from where she is to (x1,y1); opts.arc = how much she curves, opts.depth = swoops towards (+) or away (-) */
  function fly(x1,y1,ms,after,opts){
    opts=opts||{};var x0=x,y0=y,lift=(opts.arc==null?(Math.random()*.5+.2)*H*.35*(Math.random()<.5?-1:1):opts.arc);
    path={x:[x0,x0+(x1-x0)*.33,x0+(x1-x0)*.66,x1],y:[y0,y0+lift,y1-lift,y1],after:after,depth:opts.depth==null?(Math.random()-.5)*.6:opts.depth,dust:opts.dust!==false};
    t0=performance.now();dur=ms;if(Math.abs(x1-x0)>4)face=x1>x0?-1:1;
    if(!raf)raf=requestAnimationFrame(step);}
  function hover(ms,after){var cx=x,cy=y;path={hover:1,cx:cx,cy:cy,after:after};t0=performance.now();dur=ms;if(!raf)raf=requestAnimationFrame(step);}
  function clip(){   /* hide whatever part of her is behind the photo */
    if(!hideEl){f.style.clipPath='';return;}
    if(hideEl!==clip.el){clip.el=hideEl;hideY=scrollY;}
    var r=hideEl.getBoundingClientRect(),a=x+4,b=x+FW-4,c=y+4,e=y+FH-4,v='';
    if(b<=r.left||a>=r.right||e<=r.top||c>=r.bottom)v='';
    else if(a>=r.left&&b<=r.right){   /* within the photo's width: peeking over the top or under the bottom */
      if(c<r.top)v='inset(-80px -80px '+(y+FH-r.top)+'px -80px)';else if(e>r.bottom)v='inset('+(r.bottom-y)+'px -80px -80px -80px)';else v='inset(50%)';}
    else if(a<r.left)v='inset(-80px '+(x+FW-r.left)+'px -80px -80px)';
    else v='inset(-80px -80px -80px '+(r.right-x)+'px)';
    f.style.clipPath=v;}
  function render(now){
    f.style.transform='translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px)';
    sayW.style.transform='translate('+Math.max(56,Math.min(W-56,x+FW/2)).toFixed(1)+'px,'+(y-2).toFixed(1)+'px)';
    d.style.transform='scale('+(z*face).toFixed(3)+','+z.toFixed(3)+') rotate('+(bank*face).toFixed(1)+'deg)';
    d.style.filter=z<.85?'blur(.6px) brightness(.9)':'';clip();}
  function step(now){
    raf=0;if(!path||!alive)return;
    var t=Math.min(1,(now-t0)/dur),px=x,py=y;
    if(path.hover){x=path.cx+Math.sin(now/400)*6;y=path.cy+Math.sin(now/170)*5;bank=Math.sin(now/300)*6;
      if(now-lastDust>90){spark(x+FW*.35,y+FH*.6,14,-30,false);lastDust=now;}}
    else{var e=t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
      x=bez(path.x,e);y=bez(path.y,e)+Math.sin(now/170)*4;
      z=1+path.depth*Math.sin(t*Math.PI);
      var vx=x-px;bank=bank*.8+Math.max(-18,Math.min(18,-Math.abs(vx)*2.2+(y-py)*1.5))*.2;
      if(path.dust&&now-lastDust>45){spark(x+FW*(face>0?.75:.25),y+FH*.55,10,-14,false);lastDust=now;}}
    var waving=f.classList.contains('wave');
    if(now-lastWand>(waving?40:260)){var tp=tip();spark(tp[0],tp[1],waving?26:10,waving?6:-6,waving&&Math.random()<.4);lastWand=now;}
    render(now);
    if(t<1)raf=requestAnimationFrame(step);else{var a=path.after;path=null;a&&a();}}
  function show(){f.style.opacity=1;}
  function hide(){f.style.opacity=0;hideEl=null;f.style.clipPath='';}
  function edge(left){return left?-FW-20:W+20;}
  function done(){hide();busy=false;later();}
  function crossing(){var ltr=Math.random()<.5;x=edge(ltr);y=H*(.15+Math.random()*.5);show();
    fly(edge(!ltr),H*(.15+Math.random()*.5),5200+Math.random()*2000,done);
    if(Math.random()<.6)setTimeout(loop,1800+Math.random()*1500);   /* loop-the-loop on the way */
    setTimeout(wave,1000+Math.random()*2500);}
  function sprinkle(){ /* flutter in, hover and sprinkle dust, giggle, flutter off */
    var ltr=Math.random()<.5;x=edge(ltr);y=H*(.2+Math.random()*.4);show();
    fly(W*(.3+Math.random()*.4),H*(.25+Math.random()*.35),1800,function(){f.classList.add('rest');wave(2000);
      hover(2200,function(){f.classList.remove('rest');giggle(null,false);burst(x+FW/2,y+FH/2,14);
        setTimeout(function(){fly(edge(!ltr),y-H*.15,2000,done);},500);});},{depth:.25});}
  function target(){ /* a photo fully on screen that she can hide behind */
    var best=null,ba=0;[].forEach.call(document.querySelectorAll('img, .postcard'),function(el){
      if(el.closest('#fairyfly,#fairy,nav,.brand,footer,.mbar'))return;var r=el.getBoundingClientRect();
      if(r.width<110||r.height<90||r.top<70||r.bottom>H-90||r.left<-2||r.right>W+2)return;
      if(r.left<FW+12&&W-r.right<FW+12&&r.top<FH+80)return;   /* no room to peek out from */
      var a=r.width*r.height;if(a>ba){ba=a;best=el;}});return best;}
  function peekaboo(){
    var el=target();if(!el){Math.random()<.5?crossing():sprinkle();return;}
    var r=el.getBoundingClientRect(),still={arc:0,dust:false,depth:0},ways=[];
    if(r.left>=FW+12)ways.push('l');if(W-r.right>=FW+12)ways.push('r');if(r.top>=FH+80)ways.push('t');
    if(!ways.length){crossing();return;}
    var way=ways[Math.random()*ways.length|0],fromL=Math.random()<.5;
    function away(){fly(edge(x<W/2),y-H*.15,2000,done,{depth:.25});}
    if(way==='t'){   /* dive in behind the top edge, pop up for a peek, then jump out */
      var cx=r.left+(r.width-FW)*(.25+Math.random()*.5),above=r.top-FH-12,inn=r.top+8,peek=r.top-FH*.6;
      x=edge(fromL);y=above-40;show();
      fly(cx,above,1600,function(){hideEl=el;wave(700);
        fly(cx,inn,500,function(){setTimeout(function(){
          fly(cx+10,peek,420,function(){giggle(null,false);setTimeout(function(){
            fly(cx+10,inn,320,function(){setTimeout(function(){
              x=r.left+(r.width-FW)*(fromL?.8:.2);   /* pops up somewhere else along the edge */
              fly(x,peek,380,function(){giggle('peekaboo!',false);setTimeout(function(){
                fly(x,above-30,450,function(){hideEl=null;loop();setTimeout(away,500);},still);},1100);},still);},800);},still);},1100);},still);},600);},still);},{arc:30});
      return;}
    var L=way==='l',yy=r.top+Math.max(0,(r.height-FH))*(.2+Math.random()*.6);
    var out=L?r.left-FW-8:r.right+8,inn2=L?r.left+6:r.right-FW-6,half=L?r.left-FW*.55:r.right-FW*.45;
    x=edge(L);y=yy;show();
    fly(out,yy,1500,function(){hideEl=el;wave(600);
      fly(inn2,yy,650,function(){setTimeout(function(){
        fly(half,yy,380,function(){giggle('peekaboo!',false);setTimeout(function(){
          fly(inn2,yy,300,function(){setTimeout(function(){
            var other=ways.indexOf(L?'r':'l')>=0,rr=el.getBoundingClientRect();
            if(other){x=L?rr.right-FW-6:rr.left+6;fly(edge(!L),yy-H*.12,2400,done,{arc:-30,depth:.2});}   /* creeps along behind and out the far side */
            else{fly(half,yy,380,function(){giggle(null,false);setTimeout(function(){hideEl=null;away();},900);},still);}
          },700);},still);},1000);},still);},600);},still);},{arc:20});}
  function next(){
    if(document.hidden||typing||busy){later();return;}busy=true;
    var r=Math.random();(r<.42?peekaboo:r<.78?crossing:sprinkle)();}
  function later(){clearTimeout(wait);wait=setTimeout(next,9000+Math.random()*9000);}
  var hideY=0;   /* if the page really scrolls while she's hiding, the photo moves away: stop hiding */
  addEventListener('scroll',function(){if(hideEl&&Math.abs(scrollY-hideY)>40){hideEl=null;f.style.clipPath='';}},{passive:true});
  document.addEventListener('touchend',unlock,{passive:true});
  document.addEventListener('click',unlock,{passive:true});
  document.addEventListener('touchstart',function(e){
    if(typing||!e.touches[0])return;
    var tx=e.touches[0].clientX-FW/2,ty=e.touches[0].clientY-FH*.6;
    clearTimeout(wait);hideEl=null;f.style.clipPath='';busy=true;
    if(f.style.opacity!=='1'){x=edge(tx<W/2);y=ty-60;show();}
    fly(tx,ty,650,function(){var tp=tip();burst(tp[0],tp[1],26);giggle(null,true);setTimeout(function(){
      fly(edge(x<W/2),y-H*.2,1700,done,{depth:.3});},800);},{depth:.3});
  },{passive:true});
  document.addEventListener('focusin',function(e){if(e.target.closest&&e.target.closest('input,textarea,select')){typing=true;path=null;hide();}});
  document.addEventListener('focusout',function(){typing=false;busy=false;later();});
  document.addEventListener('fairy-mouse',function(){alive=false;clearTimeout(wait);path=null;f.remove();});
  if(location.hash==='#fairytest')window.__ff={peekaboo:peekaboo,crossing:crossing,sprinkle:sprinkle,pos:function(){return [x,y]}};   /* for testing only */
  setTimeout(next,2500);
})();
