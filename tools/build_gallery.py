# -*- coding: utf-8 -*-
"""Gallery page: curated photos, filters, masonry layout, lightbox with 'Book this look'.
Photos are prepared once into img/g/ (800px and 1600px WebP). Runs after build_extra, before build_conversion."""
import os, re, html, json
from PIL import Image, ImageOps, ImageStat

V2 = '/home/claude/paintingpixie-v2'
OUT = __import__('os').environ.get('PP_OUT', V2 + '/draft')
G = V2 + '/img/g'
UP = '/mnt/user-data/uploads/Painting Pixie Photos/Recommended for website'
WA = 'https://wa.me/447852300125?text='

CATS = [('all', 'All'), ('kids', "Kids' parties"), ('animal', 'Animal print'), ('grown', 'Grown-ups & hens'),
        ('glitter', 'Glitter & body art'), ('halloween', 'Halloween'), ('festival', 'Festivals & events'), ('kat', 'Kat at work')]

# slug, source, title (the design), setting, tags.  Settings only say what the photo shows.
PHOTOS = [
 ('kat-blue-monster-palette', UP + '/6 Kat at work/C139-kat-painting-blue-monster-palette.jpeg', 'Blue monster in progress', 'Kat at work', 'kat kids'),
 ('blue-monster-roar', 'img/n-blue-monster-roar.webp', 'Blue monster', 'Birthday party', 'kids'),
 ('rainbow-laughing', UP + '/1 Homepage heroes/C069-rainbow-laughing.jpeg', 'Rainbow with glitter', 'At a summer festival', 'kids festival kat'),
 ('adult-lilac-flower', 'img/n-lilac-flower-eye.webp', 'Lilac flower with rose-gold glitter', 'Grown-up glitter', 'grown glitter'),
 ('unicorn-party', 'img/n-unicorn-girl-party.webp', 'Rainbow unicorn', 'Party in a village hall', 'kids'),
 ('tiger-boy-festival', 'img/v2-tiger-boy.webp', 'Tiger', 'At a summer festival', 'animal kids festival'),
 ('festival-rainbow-body-art', 'img/n-festival-rainbow-body-art.webp', 'Rainbow and clouds body art', 'Festival body art', 'glitter grown festival'),
 ('leopard-tiger-kids', 'img/n-leopard-and-tiger-kids.webp', 'Leopard and tiger', 'Pumpkin-picking day', 'animal kids festival'),
 ('teen-red-dragon', UP + '/2 Adult glitter and hen/C111-teen-red-dragon-eye.jpeg', 'Red dragon eye', 'At a summer festival', 'grown festival'),
 ('kat-painting-smile', UP + '/6 Kat at work/C006-kat-painting-smile.jpeg', 'Butterfly in progress', 'Kat at work', 'kat festival'),
 ('pumpkin-face', 'img/n-pumpkin-face.webp', 'Jack-o’-lantern', 'Halloween event', 'halloween kids'),
 ('adult-leopard-eye', 'img/n-adult-leopard-eye.webp', 'Gold leopard with gems', 'Grown-up party', 'grown animal glitter'),
 ('unicorn-hall', 'img/n-unicorn-girl-party-hall.webp', 'Unicorn crown', 'Birthday party', 'kids'),
 ('arm-glitter-swirl', 'img/n-arm-glitter-swirl.webp', 'Glitter swirl arm art', 'Body art', 'glitter grown'),
 ('tiger-girl-closeup', 'img/n-tiger-girl-closeup.webp', 'Rainbow tiger', 'Party in a village hall', 'animal kids'),
 ('minecraft-boy', UP + '/5 Childrens parties indoors/C249-minecraft-boy.jpeg', 'Minecraft creeper', 'Birthday party', 'kids'),
 ('adult-tiger-eye', 'img/v2-adult-tiger.webp', 'Tiger eye', 'At a summer festival', 'grown animal festival'),
 ('skull-boy', UP + '/4 Halloween/C049-skull-boy.jpeg', 'Monster skull', 'Halloween party', 'halloween kids'),
 ('fairy-festival', 'img/v2-fairy.webp', 'Fairy queen', 'At a summer festival', 'kids festival'),
 ('rainbow-unicorn-girl', UP + '/5 Childrens parties indoors/C242-rainbow-unicorn-girl.jpeg', 'Rainbow unicorn', 'Birthday party', 'kids'),
 ('arm-flowers-pair', 'img/n-arm-art-flowers-pair.webp', 'Matching floral arm art', 'Body art for two', 'glitter grown'),
 ('leopard-claws', 'img/v2-leopard-girl.webp', 'Leopard', 'At a summer festival', 'animal kids festival'),
 ('kat-using-stencil', UP + '/6 Kat at work/E313-kat-using-stencil.jpg', 'Glitter tattoo with a stencil', 'Kat at work', 'kat glitter'),
 ('spiderman-cat', UP + '/5 Childrens parties indoors/C253-spiderman-costume-cat.jpeg', 'Green cat', 'Birthday party', 'kids animal'),
 ('adult-pink-glitter', 'img/n-adult-pink-glitter-event.webp', 'Pink glitter and gems', 'Grown-up party', 'grown glitter'),
 ('skeleton-crown', UP + '/4 Halloween/C047-skeleton-costume-crown.jpeg', 'Pink princess crown', 'Halloween event', 'halloween kids'),
 ('rainbow-sisters', 'img/v2-sisters.webp', 'Rainbow butterflies for sisters', 'At a summer festival', 'kids festival'),
 ('blue-flower-festival', UP + '/2 Adult glitter and hen/C247-teen-blue-flower.jpeg', 'Blue flower swirl', 'At a summer festival', 'grown festival'),
 ('half-skull-boy', UP + '/4 Halloween/C127-half-skull-boy.jpeg', 'Half skull', 'Kat at work', 'halloween kat'),
 ('shooting-stars', 'draft/blue-shooting-stars-face-paint-for-girls.webp', 'Icy shooting stars', 'Family celebration', 'kids'),
 ('gold-tiger-boy', 'img/n-tiger-boy-party.webp', 'Golden tiger', 'Birthday party', 'animal kids'),
 ('adult-flower-closeup', 'img/n-adult-flower-eye-closeup.webp', 'Blue and purple flower', 'Grown-up glitter', 'grown glitter'),
 ('three-kids-party', UP + '/5 Childrens parties indoors/C246-three-kids-party.jpeg', 'Spider-Man, butterfly and unicorn', 'Party in a hall', 'kids'),
 ('kat-close-painting', UP + '/6 Kat at work/C033-kat-close-painting.jpeg', 'Butterfly in progress', 'Kat at work', 'kat'),
 ('pumpkin-sisters', 'draft/pumpkin-face-paint-for-sisters.webp', 'Pumpkin faces for sisters', 'Halloween event', 'halloween kids'),
 ('snowflake-crown', 'draft/blue-snowflake-crown-face-paint-for-girls.webp', 'Snow queen crown', 'At a summer festival', 'kids festival'),
 ('leopard-indoors', UP + '/3 Animal print/C245-leopard-girl-indoors.jpeg', 'Leopard', 'Family event', 'animal kids'),
 ('werewolf', 'img/werewolf-event.webp', 'Werewolf', 'Grown-up event', 'grown halloween'),
 ('unicorn-soft-play', UP + '/5 Childrens parties indoors/C068-unicorn-soft-play.jpeg', 'Rainbow unicorn', 'Soft play party', 'kids'),
 ('fire-ice-dragon', 'draft/fire-and-ice-dragon-eye-face-paint.webp', 'Fire and ice dragon', 'At a summer festival', 'kids festival'),
 ('red-devil', 'draft/red-devil-face-paint-for-girls.webp', 'Red devil', 'Halloween party', 'halloween kids'),
 ('purple-leopard', UP + '/3 Animal print/C037-purple-glitter-leopard.jpeg', 'Purple glitter leopard', 'At a summer festival', 'animal grown festival glitter'),
 ('kat-painting-wide', UP + '/6 Kat at work/C092-kat-painting-wide.jpeg', 'Painting at a festival', 'Kat at work', 'kat festival'),
 ('green-dragon', 'draft/green-dragon-face-paint-for-kids.webp', 'Green dragon', 'At a summer festival', 'kids festival'),
 ('adult-skull', 'img/n-adult-skull.webp', 'Sugar-blue skull', 'Grown-up Halloween', 'halloween grown'),
 ('blue-monster-festival', UP + '/1 Homepage heroes/C098-blue-butterfly-boy-festival.jpeg', 'Blue monster', 'At a summer festival', 'kids festival'),
 ('leopard-being-painted', UP + '/3 Animal print/C001-leopard-girl-being-painted.jpeg', 'Leopard in progress', 'Kat at work', 'animal kat festival'),
 ('glitter-tattoo-unicorn', 'draft/unicorn-crown-face-paint-girl-glitter-tattoo-horsham.webp', 'Unicorn crown and glitter tattoo', 'At a summer festival', 'kids glitter festival'),
 ('blue-monster-arsenal', 'draft/blue-monster-face-paint-for-girls.webp', 'Blue monster', 'At a summer festival', 'kids festival'),
 ('leopard-boy', UP + '/3 Animal print/C014-leopard-boy.jpeg', 'Tiger with gems', 'At a summer festival', 'animal kids festival'),
]

def trim_border(im):
    """Remove flat black/white borders left by phone screenshots (tolerates a thin edge line)."""
    g = im.convert('L'); w, h = g.size
    def flat(box):
        st = ImageStat.Stat(g.crop(box)); m, sd = st.mean[0], st.stddev[0]
        return sd < 16 and (m < 45 or m > 235)
    def scan(n, lim, box):
        last, miss = 0, 0
        for k in range(0, lim, 2):
            if flat(box(k)): last, miss = k + 2, 0
            else:
                miss += 1
                if miss > 3: break
        return last
    l = scan(w, int(w * .12), lambda k: (k, 0, k + 2, h))
    r = w - scan(w, int(w * .12), lambda k: (w - k - 2, 0, w - k, h))
    t = scan(h, int(h * .12), lambda k: (0, k, w, k + 2))
    b = h - scan(h, int(h * .12), lambda k: (0, h - k - 2, w, h - k))
    if (l, t, r, b) != (0, 0, w, h): im = im.crop((l + 3 * (l > 0), t + 3 * (t > 0), r - 3 * (r < w), b - 3 * (b < h)))
    return im

def prepare():
    os.makedirs(G, exist_ok=True)
    sizes = {}
    for slug, src, *_ in PHOTOS:
        big = f'{G}/{slug}-1600.webp'; small = f'{G}/{slug}-800.webp'
        if not os.path.exists(big):
            path = src if src.startswith('/') else f'{V2}/{src}'
            im = trim_border(ImageOps.exif_transpose(Image.open(path)).convert('RGB'))
            b = im.copy(); b.thumbnail((1600, 1600), Image.LANCZOS); b.save(big, 'WEBP', quality=82, method=6)
            s = im.copy(); s.thumbnail((800, 800), Image.LANCZOS); s.save(small, 'WEBP', quality=78, method=6)
        sizes[slug] = Image.open(small).size
    return sizes

# photos where the face is a small part of the picture: crop in towards it.
# slug: (centre x, centre y, share of width/height kept), all as fractions of the photo
ZOOM = {
    'blue-monster-roar': (.50, .36, .75), 'unicorn-party': (.46, .42, .62), 'tiger-boy-festival': (.42, .36, .75),
    'leopard-tiger-kids': (.50, .36, .72), 'teen-red-dragon': (.42, .36, .72), 'unicorn-hall': (.46, .32, .60),
    'fairy-festival': (.50, .30, .66), 'rainbow-unicorn-girl': (.48, .36, .70), 'leopard-claws': (.48, .38, .75),
    'spiderman-cat': (.42, .32, .70), 'skeleton-crown': (.40, .22, .56), 'adult-pink-glitter': (.42, .44, .75),
    'rainbow-sisters': (.42, .32, .75), 'shooting-stars': (.54, .40, .70), 'gold-tiger-boy': (.45, .32, .70),
    'three-kids-party': (.52, .44, .64), 'snowflake-crown': (.42, .34, .62), 'leopard-indoors': (.48, .36, .66),
    'werewolf': (.48, .40, .56), 'unicorn-soft-play': (.50, .36, .70), 'fire-ice-dragon': (.46, .30, .56),
    'green-dragon': (.45, .32, .62), 'blue-monster-festival': (.50, .42, .36), 'glitter-tattoo-unicorn': (.58, .42, .46),
    'blue-monster-arsenal': (.42, .32, .62),
}

def zoomed(slug):
    """File stem to use for this photo: the original, or a cropped-in copy (made once)."""
    if slug not in ZOOM: return slug
    big, small = f'{G}/{slug}-z-1600.webp', f'{G}/{slug}-z-800.webp'
    if not (os.path.exists(big) and os.path.exists(small)):
        cx, cy, k = ZOOM[slug]
        im = Image.open(f'{G}/{slug}-1600.webp'); W, H = im.size
        w, h = int(W * k), int(H * k)
        l = min(max(int(cx * W - w / 2), 0), W - w); t = min(max(int(cy * H - h / 2), 0), H - h)
        c = im.crop((l, t, l + w, t + h))
        b = c.resize((int(w * 1600 / max(w, h)), int(h * 1600 / max(w, h))), Image.LANCZOS) if max(w, h) < 1600 else c
        b.save(big, 'WEBP', quality=82, method=6)
        sm = c.copy(); sm.thumbnail((800, 800), Image.LANCZOS); sm.save(small, 'WEBP', quality=80, method=6)
    return slug + '-z'

def wa(t): return WA + t.replace(' ', '%20').replace("'", '%27').replace('’', '%27').replace('&', 'and')
esc = lambda t: html.escape(t, quote=True)

def gallery_html(sizes):
    counts = {k: (len(PHOTOS) if k == 'all' else sum(k in p[4].split() for p in PHOTOS)) for k, _ in CATS}
    chips = ''.join(f'<button type="button" class="gchip{" on" if k == "all" else ""}" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{esc(n)} <small>{counts[k]}</small></button>' for k, n in CATS)
    items = []
    for i, (slug, src, title, setting, tags) in enumerate(PHOTOS):
        w, h = sizes[slug]
        f = zoomed(slug)
        if f != slug: w, h = Image.open(f'{G}/{f}-800.webp').size
        alt = f'{title} face painting by The Painting Pixie, {setting.lower()}' if 'kat' not in tags.split()[:1] else f'Kat from The Painting Pixie painting a {title.lower().replace(" in progress", "")}'
        items.append(
            f'<figure class="gi" data-tags="{tags}" data-title="{esc(title)}" data-setting="{esc(setting)}" data-full="../img/g/{f}-1600.webp">'
            f'<button type="button" class="gopen" aria-label="View larger: {esc(title)}">'
            f'<img src="../img/g/{f}-800.webp" srcset="../img/g/{f}-800.webp 800w, ../img/g/{f}-1600.webp 1600w" sizes="(max-width:700px) 50vw, (max-width:1100px) 33vw, 25vw" '
            f'width="{w}" height="{h}" alt="{esc(alt)}" loading="{"eager" if i < 6 else "lazy"}" decoding="async"></button>'
            f'<figcaption><b>{esc(title)}</b><span>{esc(setting)}</span></figcaption></figure>')
    return f'''<section class="band band-light k-gallery2"><div class="wrap">
<p class="eyebrow">The gallery</p><h2>Real faces, real parties</h2>
<p class="glede">Every photo here is Kat’s own work at real parties, festivals and events, not stock images. Pick a category, tap a photo to see it up close, and book the look you love. Looking for animal print? Tigers, leopards and big cats for kids and grown-ups are under <a href="#animal" class="glink" data-go="animal">Animal print</a>.</p>
<div class="gchips" role="toolbar" aria-label="Filter the gallery">{chips}</div>
<div class="gmason" id="gmason">{"".join(items)}</div>
<p class="gmore">Can’t see the design you want? Kat paints <b>almost anything</b>: football kits, favourite characters, party themes and brand colours. <a href="{wa("Hi Kat! Can you paint a design I have in mind? It's: ")}" target="_blank" rel="noopener">Ask Kat on WhatsApp</a></p>
</div></section>
<div class="glb" id="glb" role="dialog" aria-modal="true" aria-label="Photo viewer" hidden>
<button type="button" class="glb-x" aria-label="Close">&times;</button>
<button type="button" class="glb-nav glb-prev" aria-label="Previous photo">&#8249;</button>
<figure class="glb-fig"><img id="glbImg" src="" alt=""><figcaption><div><b id="glbTitle"></b><span id="glbSet"></span></div>
<div class="glb-cta"><a class="btn btn-wa" id="glbBook" href="#" target="_blank" rel="noopener">Book this look</a><a class="btn btn-gold" href="contact.html">Check my date</a></div>
<small id="glbCount"></small></figcaption></figure>
<button type="button" class="glb-nav glb-next" aria-label="Next photo">&#8250;</button>
</div>'''

CSS = r'''<style>
.k-gallery2 .glede{max-width:720px;color:#5A5049;font-size:17px}
.gchips{display:flex;flex-wrap:wrap;gap:10px;margin:22px 0 26px}
.gchip{font:700 14.5px/1 Manrope,system-ui,sans-serif;padding:11px 16px;border-radius:999px;border:1.5px solid #E2D6C8;background:#fff;color:#2A231D;cursor:pointer;transition:all .2s}
.gchip small{font-weight:800;opacity:.55;margin-left:4px}
.gchip:hover{border-color:var(--pink,#FF4FA3)}
.gchip.on{background:#1B1712;border-color:#1B1712;color:#fff}
.gmason{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:8px;column-gap:16px}
@media(max-width:1100px){.gmason{grid-template-columns:repeat(3,1fr)}}
.gi{grid-row-end:span 46;margin:0 0 16px;position:relative;border-radius:16px;overflow:hidden;background:#EFE7DD;box-shadow:0 18px 36px -24px rgba(40,20,30,.55);animation:gin .45s ease both}
.gi[hidden]{display:none}
@keyframes gin{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.gopen{display:block;width:100%;height:100%;padding:0;border:0;background:none;cursor:zoom-in}
.gi img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.gi:hover img{transform:scale(1.04)}
.k-gallery2 .gi figcaption{color:#fff!important;}.gi figcaption{position:absolute;left:0;right:0;bottom:0;padding:34px 14px 12px;background:linear-gradient(180deg,transparent,rgba(15,12,18,.82));color:#fff;pointer-events:none;opacity:0;transform:translateY(6px);transition:all .3s}
.gi:hover figcaption,.gi:focus-within figcaption{opacity:1;transform:none}
.gi figcaption b{color:#fff;display:block;font-family:Fraunces,serif;font-weight:400;font-size:19px;line-height:1.2}
.gi figcaption span{color:#fff;font-size:12.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;opacity:.8}
.gmore{margin-top:26px;text-align:center;color:#5A5049}
.gmore a{font-weight:800}
.glb{position:fixed;inset:0;z-index:100000;background:rgba(12,10,14,.94);display:flex;align-items:center;justify-content:center;padding:20px}
.glb[hidden]{display:none}
.glb-fig{margin:0;display:flex;flex-direction:column;align-items:center;max-width:min(1100px,100%);max-height:100%}
.glb-fig img{max-width:100%;max-height:calc(100vh - 170px);border-radius:12px;object-fit:contain;box-shadow:0 30px 80px rgba(0,0,0,.6)}
.glb-fig figcaption{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 24px;width:100%;margin-top:14px;color:#F5F1EA}
.glb-fig figcaption b{display:block;font-family:Fraunces,serif;font-weight:400;font-size:24px}
.glb-fig figcaption span{font-size:13px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;opacity:.7}
.glb-fig small{width:100%;text-align:center;opacity:.5;font-weight:700}
.glb-cta{display:flex;gap:10px;flex-wrap:wrap}
.glb-cta .btn{margin:0}
.glb-x{position:absolute;top:12px;right:16px;font-size:40px;line-height:1;background:none;border:0;color:#fff;cursor:pointer;padding:6px 12px}
.glb-nav{position:absolute;top:50%;transform:translateY(-50%);width:54px;height:54px;border-radius:50%;border:0;background:rgba(255,255,255,.12);color:#fff;font-size:38px;line-height:1;cursor:pointer}
.glb-nav:hover{background:rgba(255,255,255,.25)}
.glb-prev{left:16px}.glb-next{right:16px}
@media(max-width:700px){.gmason{grid-template-columns:repeat(2,1fr);column-gap:10px}.gi{border-radius:12px;margin-bottom:10px}
.gi figcaption{opacity:1;transform:none;padding:24px 10px 8px}.gi figcaption b{font-size:15px}.gi figcaption span{color:#fff;display:none}
.gchips{flex-wrap:nowrap;overflow-x:auto;margin:18px -16px 20px;padding:0 16px 6px;scrollbar-width:none}.gchips::-webkit-scrollbar{display:none}.gchip{flex:0 0 auto}
.glb{padding:10px}.glb-nav{top:auto;bottom:16px;transform:none;width:46px;height:46px}.glb-fig img{max-height:calc(100vh - 230px)}.glb-fig figcaption{justify-content:center;text-align:center}}
@media(prefers-reduced-motion:reduce){.gi{animation:none}.gi img{transition:none}}
</style>'''

JS = r'''<script>
(function(){
  var chips=[].slice.call(document.querySelectorAll('.gchip')), items=[].slice.call(document.querySelectorAll('.gi'));
  var lb=document.getElementById('glb'), img=document.getElementById('glbImg'), t=document.getElementById('glbTitle'), st=document.getElementById('glbSet'), cnt=document.getElementById('glbCount'), book=document.getElementById('glbBook');
  var list=items, cur=0, last=null, grid=document.getElementById('gmason');
  function lay(){var cs=getComputedStyle(grid), gap=parseFloat(cs.columnGap)||16, row=8, cols=cs.gridTemplateColumns.split(' ').length, w=(grid.clientWidth-gap*(cols-1))/cols;
    items.forEach(function(i){var im=i.querySelector('img'), r=im.getAttribute('height')/im.getAttribute('width'); r=Math.min(Math.max(r,.62),1.45); i.style.gridRowEnd='span '+Math.round((w*r+gap)/(row))})}
  grid.style.rowGap='0px'; lay(); var rt; window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(lay,120)});
  function filter(f){
    chips.forEach(function(c){var on=c.dataset.f===f;c.classList.toggle('on',on);c.setAttribute('aria-pressed',on)});
    list=items.filter(function(i){var ok=f==='all'||i.dataset.tags.split(' ').indexOf(f)>-1;i.hidden=!ok;if(ok){i.style.animation='none';i.offsetHeight;i.style.animation='';}return ok});
    if(history.replaceState)history.replaceState(null,'',f==='all'?location.pathname:'#'+f);
    if(window.gtag)gtag('event','gallery_filter',{filter:f});
  }
  chips.forEach(function(c){c.addEventListener('click',function(){filter(c.dataset.f)})});
  function show(n){
    cur=(n+list.length)%list.length; var i=list[cur], im=i.querySelector('img');
    img.src=i.dataset.full; img.alt=im.alt; t.textContent=i.dataset.title; st.textContent=i.dataset.setting;
    cnt.textContent=(cur+1)+' of '+list.length;
    book.href='https://wa.me/447852300125?text='+encodeURIComponent("Hi Kat! I love the "+i.dataset.title+" design in your gallery. Are you free on my date? Date: Town: Guests: ");
  }
  function open(i){last=document.activeElement;lb.hidden=false;document.body.style.overflow='hidden';show(list.indexOf(i));lb.querySelector('.glb-x').focus();if(window.gtag)gtag('event','gallery_open',{design:i.dataset.title})}
  function close(){lb.hidden=true;img.src='';document.body.style.overflow='';if(last)last.focus()}
  items.forEach(function(i){i.querySelector('.gopen').addEventListener('click',function(){open(i)})});
  lb.querySelector('.glb-x').addEventListener('click',close);
  lb.querySelector('.glb-prev').addEventListener('click',function(){show(cur-1)});
  lb.querySelector('.glb-next').addEventListener('click',function(){show(cur+1)});
  lb.addEventListener('click',function(e){if(e.target===lb)close()});
  book.addEventListener('click',function(){if(window.gtag)gtag('event','whatsapp_click',{button_position:'gallery_book_look',design:t.textContent})});
  document.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1)});
  var x0=null;lb.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
  lb.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>45)show(cur+(dx<0?1:-1));x0=null});
  var h=location.hash.slice(1); if(h&&chips.some(function(c){return c.dataset.f===h}))filter(h);
  window.addEventListener('hashchange',function(){var h=location.hash.slice(1);if(chips.some(function(c){return c.dataset.f===h}))filter(h);});
})();
</script>'''

def build():
    sizes = prepare()
    p = f'{OUT}/gallery.html'; s = open(p).read()
    # new gallery section replaces old grid, old lightbox and the old text band
    s = re.sub(r'<section class="band band-light k-gallery centred[^"]*">.*?(?=<!-- CTA -->)', lambda m: gallery_html(sizes) + '\n', s, count=1, flags=re.S)
    # drop the old masonry + lightbox scripts
    s = re.sub(r'<script>\s*\(function\(\) \{\s*// TRUE MASONRY.*?</script>\s*', '', s, count=1, flags=re.S)
    s = re.sub(r'<script>\s*\(function\(\) \{\s*const galleryImgs.*?</script>\s*', '', s, count=1, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = s.replace('<script src="site.js"></script>', JS + '\n<script src="site.js"></script>', 1)
    # hero: Kat at work
    s = re.sub(r'(<header class="phero"><img src=")[^"]+("[^>]*?style="object-position:)[^"]*', r'\g<1>../img/g/kat-blue-monster-palette-1600.webp\g<2>55% 40%', s, count=1)
    s = re.sub(r'(<header class="phero">.*?<h1>).*?(</h1>\s*<p>).*?(</p>)', r'\g<1>Face Painting Gallery\g<2>Kat’s real work at parties, festivals and events across Sussex and Surrey. Find a look you love and book it.\g<3>', s, count=1, flags=re.S)
    open(p, 'w').write(s)
    print('gallery built:', len(PHOTOS), 'photos')

if __name__ == '__main__':
    build()
