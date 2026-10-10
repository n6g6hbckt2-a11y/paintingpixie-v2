# -*- coding: utf-8 -*-
"""Site background chosen by Kat (7 Oct 2026): 'Pixie dust' (design idea H) instead of plain black.
The pattern sits still behind the page (like the Halloween page) and shows through every section that used to be black.
Light sections, the coloured price band and photo cards are unchanged. Runs after build_design_ideas (needs img/bg/pixie-dust.svg)."""
OUT = __import__('os').environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
CSS = '''
/* ===== Background: Pixie dust (Kat's choice, 7 Oct 2026) ===== */
html{background:#2A0F4A}
body{background:transparent}
body::before{content:"";position:fixed;inset:0;z-index:-3;pointer-events:none;
  background:linear-gradient(rgba(14,11,20,.18),rgba(14,11,20,.30)),url(../img/bg/pixie-dust-site.svg) center/cover no-repeat}
main.lg,footer,.trustband,.band-dark,.igband,.cta,.grown{background:transparent!important}
/* inner pages keep their hero photo fixed behind the header, so the page body carries its own still pixie-dust layer */
main.lg,footer{position:relative;isolation:isolate;clip-path:inset(0)}
main.lg::before,footer::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:linear-gradient(rgba(14,11,20,.18),rgba(14,11,20,.30)),url(../img/bg/pixie-dust-site.svg) center/cover no-repeat}
.band-panel,.lg section.alt,.lg section.contact-box{background:rgba(18,10,28,.45)!important}
.trustband{background:rgba(12,8,18,.55)!important}
footer::after{content:"";position:absolute;inset:0;z-index:-1;background:rgba(12,8,18,.55)}
.phero:not(.hero-right)>.hbg{background:transparent!important}
/* photo sections that used to be cream */
.photo-dust .glede{color:#E9DFF2!important}
.photo-dust .glede a{color:var(--gold)}
.photo-dust .gmason{column-gap:22px}
'''
import glob, os, re

def photos_on_dust():
    """Sections that show photos go on the pixie dust (not cream), so the dust is behind every photo."""
    n = 0
    for p in glob.glob(OUT + '/*.html'):
        if os.path.basename(p).startswith('design-ideas'): continue
        s0 = s = open(p).read()
        def swap(m):
            sec = m.group(0)
            imgs = re.findall(r'<img[^>]*src="([^"]+)"', sec)
            if not [i for i in imgs if 'addtoevent' not in i]: return sec      # only review badges: leave cream
            return sec.replace('band band-light', 'band band-dark photo-dust', 1)
        s = re.sub(r'<section class="band band-light[^"]*".*?</section>', swap, s, flags=re.S)
        if s != s0: open(p, 'w').write(s); n += 1
    return n

FAIRY_CSS = """
/* fairy cursor: the logo fairy follows the mouse, brush tip = pointer (computers only) */
html.fairy-on,html.fairy-on *{cursor:none!important}
html.fairy-on input,html.fairy-on textarea,html.fairy-on select,html.fairy-on [contenteditable]{cursor:text!important}
#fairy{position:fixed;left:0;top:0;width:62px;height:72px;z-index:2147483647;pointer-events:none;will-change:transform;opacity:0;transition:opacity .2s}
#fairy img{width:100%;height:100%;display:block;transform-origin:12% 18%;transition:transform .18s ease;filter:drop-shadow(0 4px 8px rgba(0,0,0,.45))}
#fairy.hot img{transform:scale(1.18) rotate(-6deg)}
#fairy.down img{transform:scale(.92) rotate(4deg)}
#fairyfly{position:fixed;left:0;top:0;width:46px;height:54px;z-index:2147483647;pointer-events:none;will-change:transform;opacity:0;transition:opacity .4s}
#fairyfly img{width:100%;height:100%;display:block;filter:drop-shadow(0 4px 8px rgba(0,0,0,.45))}
#fairyfly.right img{transform:scaleX(-1)}
.fdust{position:fixed;left:0;top:0;width:6px;height:6px;border-radius:50%;pointer-events:none;z-index:2147483646;
  background:radial-gradient(circle,#FFF6D6 0,#FFD24F 45%,rgba(255,210,79,0) 70%);animation:fdust .9s ease-out forwards}
@keyframes fdust{to{opacity:0;transform:translate(var(--dx),var(--dy)) scale(.2)}}
"""
FAIRY_JS = """
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
"""

FAIRY_MOBILE_JS = """
(function(){
  /* phones and tablets: no mouse, so the fairy flies across the screen by herself every so often,
     and flies to wherever you tap, with a puff of pixie dust */
  if(!window.matchMedia)return;
  var touch=(navigator.maxTouchPoints||0)>0||('ontouchstart' in window);
  if(!touch&&matchMedia('(hover:hover) and (pointer:fine)').matches)return;
  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  var f=document.createElement('div');f.id='fairyfly';f.className='fly';f.setAttribute('aria-hidden','true');
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
  document.addEventListener('fairy-mouse',function(){clearTimeout(wait);path=null;f.remove();typing=true;});
  setTimeout(crossing,2500);
})();
"""

def build():
    print('photo sections moved onto pixie dust on', photos_on_dust(), 'pages')
    with open(f'{OUT}/site.js') as f: js = f.read()
    if 'fairy-cursor' not in js:
        with open(f'{OUT}/site.js', 'a') as f: f.write(FAIRY_JS + FAIRY_MOBILE_JS)
    with open(f'{OUT}/site.css') as f: s = f.read()
    if 'Background: Pixie dust' not in s:
        with open(f'{OUT}/site.css', 'a') as f: f.write(CSS + FAIRY_CSS)
    print('pixie dust background on')

if __name__ == '__main__':
    build()
