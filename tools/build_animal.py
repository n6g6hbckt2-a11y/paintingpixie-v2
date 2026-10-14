# -*- coding: utf-8 -*-
"""14 Oct: the animal print page ranks 1st-3rd for "animal print face painting" (Sussex/Surrey/Brighton) but gets few
clicks: most people searching want design ideas and click the image results. A design-ideas section with large photos,
descriptive file names, alt text and captions helps Kat appear in Google Images, and each photo has a "Book this look" link.
Captions use only what we know about each photo (from the gallery list). Runs after build_seo_fixes."""
import os, re, shutil
from urllib.parse import quote
OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
SRC = '/home/claude/paintingpixie-v2/img/g'
PAGE = 'animal-print-face-painting.html'
WA = 'https://wa.me/447852300125?text='
# (gallery image, new file name, design, where, alt)
LOOKS = [
    ('tiger-boy-festival-z', 'tiger-face-paint-boy', 'Tiger', 'At a summer festival', 'Tiger face paint on a boy at a summer festival'),
    ('gold-tiger-boy-z', 'golden-tiger-face-paint', 'Golden tiger', 'Birthday party', 'Golden tiger face paint with a red gem, at a birthday party'),
    ('tiger-girl-closeup', 'rainbow-tiger-face-paint', 'Rainbow tiger', 'Party in a village hall', 'Rainbow tiger face paint close-up, at a party in a village hall'),
    ('leopard-claws-z', 'leopard-face-paint-girl', 'Leopard', 'At a summer festival', 'Leopard print face paint on a girl at a summer festival'),
    ('purple-leopard', 'purple-glitter-leopard-face-paint', 'Purple glitter leopard', 'At a summer festival', 'Purple leopard print face paint with glitter'),
    ('leopard-boy', 'tiger-face-paint-with-gems', 'Tiger with gems', 'At a summer festival', 'Tiger face paint with gems on a boy at a summer festival'),
    ('adult-leopard-eye', 'gold-leopard-eye-face-paint-adult', 'Gold leopard with gems', 'Grown-up party', 'Gold leopard print eye design with gems on a woman'),
    ('adult-tiger-eye', 'tiger-eye-face-paint-adult', 'Tiger eye', 'At a summer festival', 'Tiger eye face paint design on an adult at a summer festival'),
    ('leopard-tiger-kids-z', 'leopard-and-tiger-face-paint-children', 'Leopard and tiger', 'Pumpkin-picking day', 'Two children with leopard and tiger face paint on a pumpkin-picking day'),
    ('spiderman-cat-z', 'green-cat-face-paint', 'Green cat', 'Birthday party', 'Green cat face paint at a birthday party'),
]
CROP = {'purple-leopard': 0.75, 'leopard-boy': 0.625}   # face centre, as a share of the photo's width
CSS = '''<style>
.k-looks .looks{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px;text-align:left}
.k-looks figure{margin:0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 18px 36px -26px rgba(60,30,40,.5);display:flex;flex-direction:column}
.k-looks img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;object-position:50% 30%}
.k-looks figcaption{padding:12px 16px 16px;color:#1B1712;display:flex;flex-direction:column;gap:2px;flex:1}
.k-looks figcaption b{font-family:Fraunces,serif;font-weight:400;font-size:21px}
.k-looks figcaption span{font-size:14px;color:#6A5F55}
.k-looks figcaption a{margin-top:8px;font-weight:800;font-size:15px;color:#B0337A}
@media(max-width:900px){.k-looks .looks{grid-template-columns:repeat(2,1fr);gap:12px}.k-looks figcaption{padding:10px 12px 12px}.k-looks figcaption b{font-size:18px}}
</style>'''

def section():
    figs = []
    for src, name, design, where, alt in LOOKS:
        msg = quote(f"Hi Kat! I'd love the {design.lower()} look at my party. Date: Postcode: ")
        figs.append(f'<figure><img src="../img/animal/{name}.webp" srcset="../img/animal/{name}-800.webp 800w, ../img/animal/{name}.webp 1600w" '
                    f'sizes="(max-width:900px) 50vw, 33vw" alt="{alt}" loading="lazy">'
                    f'<figcaption><b>{design}</b><span>{where}</span><a href="{WA}{msg}" target="_blank" rel="noopener">Book this look →</a></figcaption></figure>')
    return (f'{CSS}<section class="band band-light k-text centred k-looks"><div class="wrap">'
            '<h2>Animal Print Face Paint Ideas</h2>'
            '<p>Tigers, leopards and cats Kat has painted at real parties and festivals. Every photo is her own work. '
            'See one you like? Tap “Book this look” and tell Kat your date.</p>'
            f'<div class="looks">{"".join(figs)}</div></div></section>\n')

def build():
    p = f'{OUT}/{PAGE}'
    if not os.path.exists(p): print('animal page missing'); return
    s = open(p).read()
    if 'k-looks' in s: print('animal ideas: already done'); return
    os.makedirs(f'{OUT}/../img/animal', exist_ok=True) if False else None
    dst = '/home/claude/paintingpixie-v2/img/animal'; os.makedirs(dst, exist_ok=True)
    from PIL import Image
    for src, name, *_ in LOOKS:
        if src in CROP:   # landscape photos: a portrait crop centred on the face, so the design fills the card
            im = Image.open(f'{SRC}/{src}-1600.webp'); W, H = im.size; w = int(H * 0.8); x = max(0, min(W - w, int(W * CROP[src]) - w // 2))
            c = im.crop((x, 0, x + w, H)); c.save(f'{dst}/{name}.webp', 'WEBP', quality=82)
            c.thumbnail((800, 800)); c.save(f'{dst}/{name}-800.webp', 'WEBP', quality=82)
            continue
        shutil.copyfile(f'{SRC}/{src}-1600.webp', f'{dst}/{name}.webp')
        shutil.copyfile(f'{SRC}/{src}-800.webp', f'{dst}/{name}-800.webp')
    m = re.search(r'<section class="band band-dark k-features centred.*?</section>\s*', s, re.S)
    if not m: print('animal ideas: no place'); return
    s = s[:m.end()] + section() + s[m.end():]
    if 'max-image-preview' not in s:
        s = s.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="robots" content="max-image-preview:large">', 1)
    open(p, 'w').write(s); print(f'animal ideas: {len(LOOKS)} designs added')

if __name__ == '__main__':
    build()
