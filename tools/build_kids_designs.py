# -*- coding: utf-8 -*-
"""14 Oct (Phil): a photo under each of the 4 "Popular Children's Designs" cards on the children's party page.
Kat's own photos, from the gallery list. Runs after build_home_faq."""
import os, re
from PIL import Image
OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
G = '/home/claude/paintingpixie-v2/img/g'
DST = '/home/claude/paintingpixie-v2/img/kids'
PAGE = 'childrens-face-painting.html'
# card heading -> (gallery photo, crop box as fractions of the photo (face filling the frame), new file name, alt)
PICS = {
    'Unicorns & princesses': ('unicorn-party-z', (125/599, 250/800, 565/599, 1.0), 'rainbow-unicorn-face-paint-girl', 'Rainbow unicorn face paint on a girl at a party in a village hall'),
    'Dragons & monsters': ('blue-monster-roar-z', (92/602, 210/800, 508/602, 730/800), 'blue-monster-face-paint-roar', 'Blue monster face paint on a child roaring at a birthday party'),
    'Superheroes': ('three-kids-party', (68/800, 168/602, 228/800, 368/602), 'spider-man-face-paint-boy', 'Spider-Man face paint on a boy at a party'),
    'Halloween & seasonal designs': ('pumpkin-face', (97/603, 200/800, 433/603, 620/800), 'pumpkin-face-paint-halloween', 'Jack-o’-lantern pumpkin face paint at a Halloween event'),
}
CSS = ('<style>.fcard:has(.fpic){display:flex;flex-direction:column}.fcard:has(.fpic) p{margin-bottom:14px}'
       '.fcard .fpic{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 50%;border-radius:12px;margin-top:auto}'
       '</style>')
def prep(src, box, name):
    os.makedirs(DST, exist_ok=True)
    im = Image.open(f'{G}/{src}-1600.webp')
    if box:
        x0, y0, x1, y1 = box; W, H = im.size   # box as fractions of the photo, framed tight on the face
        im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    im.save(f'{DST}/{name}.webp', 'WEBP', quality=82)
    s = im.copy(); s.thumbnail((640, 800)); s.save(f'{DST}/{name}-640.webp', 'WEBP', quality=82)
def build():
    p = f'{OUT}/{PAGE}'
    if not os.path.exists(p): return
    s = open(p).read()
    if 'class="fpic"' in s: print('kids designs: already done'); return
    n = 0
    for h, (src, box, name, alt) in PICS.items():
        prep(src, box, name)
        pat = re.compile(r'(<div class="fcard"><h3>' + re.escape(h.replace('&', '&amp;')) + r'</h3><p>.*?</p>)|(<div class="fcard"><h3>' + re.escape(h) + r'</h3><p>.*?</p>)', re.S)
        img = (f'<img class="fpic" src="../img/kids/{name}-640.webp" srcset="../img/kids/{name}-640.webp 640w, ../img/kids/{name}.webp 1200w" '
               f'sizes="(max-width:700px) 90vw, 25vw" alt="{alt}" loading="lazy">')
        s, k = pat.subn(lambda m: m.group(0) + img, s, count=1); n += k
    if n: s = s.replace("<h2>Popular Children's Designs</h2>", CSS + "<h2>Popular Children's Designs</h2>", 1)
    open(p, 'w').write(s); print('kids designs: photos on', n, 'cards')
if __name__ == '__main__':
    build()
