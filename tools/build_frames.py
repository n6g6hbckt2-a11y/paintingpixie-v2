# -*- coding: utf-8 -*-
"""Page headings with a face photo: put the photo whole in a tilted white frame beside the text box,
instead of full-width behind it (where the text box covered the face paint).
Scenery headings (Brighton pier, Worthing beach, Burgess Hill) keep the full-width photo.
Runs after build_theme in both pipelines."""
import os, re
from PIL import Image

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
V2 = '/home/claude/paintingpixie-v2'

# page: (photo or None to keep the current one, alt text, caption)
g = lambda slug: f'../img/g/{slug}-1600.webp'
FRAMES = {
    'childrens-face-painting.html': ('../img/g/unicorn-party-portrait.webp',
                                     'Girl with rainbow unicorn face paint at a birthday party', '★★★★★ Rainbow unicorn at a birthday party'),
    'index.html': (None, 'Kat face painting a blue monster design on a smiling girl', '★★★★★ Kat at work'),
    'about.html': (None, 'Kat face painting a design on a smiling girl', '★★★★★ Hi, I’m Kat'),
    'services.html': (None, 'Boy having leopard face paint applied by Kat', '★★★★★ Leopard in progress'),
    'gallery.html': (None, 'Teenager with a red dragon face paint design', '★★★★★ Red dragon'),
    'areas.html': (None, 'Kat face painting at an event', '★★★★★ Across Sussex & Surrey'),
    'contact.html': (None, 'Girl with rainbow unicorn face paint', '★★★★★ Rainbow unicorn'),
    'adult-face-painting.html': (g('adult-pink-glitter'), 'Woman with pink glitter and gem face art at a party', '★★★★★ Pink glitter for the party'),
    'glitter-bar.html': (None, 'Woman with lilac flower glitter face art', '★★★★★ Lilac flower glitter'),
    'animal-print-face-painting.html': (None, 'Two children with leopard and tiger face paint', '★★★★★ Leopard and tiger'),
    'face-painter-horsham.html': (g('spiderman-cat'), 'Boy in a Spider-Man costume with green cat face paint at a party', '★★★★★ Party cat'),
    'face-painter-crawley.html': (None, 'Boy with golden tiger face paint at a birthday party', '★★★★★ Golden tiger'),
    'face-painter-dorking.html': (None, 'Boy with tiger face paint at a festival', '★★★★★ Tiger'),
    'face-painter-east-grinstead.html': (None, 'Girl with leopard face paint at a summer festival', '★★★★★ Leopard'),
    'face-painter-guildford.html': (None, 'Girl with blue monster face paint roaring', '★★★★★ Blue monster'),
    'face-painter-haywards-heath.html': (None, 'Girl with unicorn face paint at a party in a hall', '★★★★★ Unicorn party'),
    'face-painter-lewes.html': (None, 'Girl with rainbow tiger face paint', '★★★★★ Rainbow tiger'),
    'face-painter-reigate.html': (None, 'Girl with leopard face paint at an indoor party', '★★★★★ Leopard'),
    'face-painter-south-downs.html': (None, 'Two sisters with matching face paint designs', '★★★★★ Sisters'),
    'face-painter-surrey-villages.html': (None, 'Girl with unicorn face paint at a soft play party', '★★★★★ Unicorn at soft play'),
    'face-painter-surrey.html': (None, 'Woman with tiger eye face paint at a festival', '★★★★★ Tiger eye'),
    'face-painter-sussex.html': (None, 'Girl laughing while having rainbow face paint applied', '★★★★★ Rainbow giggles'),
    'face-painter-west-sussex-villages.html': (None, 'Little girl with fairy face paint at a festival', '★★★★★ Fairy'),
}

FRAME_CSS = '''
/* centred text bands: inline margin:0 from the old pages must not pin paragraphs to the left */
.k-text.centred .wrap>p{margin-left:auto!important;margin-right:auto!important;text-align:center!important}
.k-text.centred .ate-badge{display:inline-block}.k-text.centred .ate-badge img{display:inline-block;margin:0 auto}
/* framed heading photo */
.phero.rvh{min-height:0;padding-top:150px;align-items:center}
.phero.rvh::after{background:linear-gradient(180deg,rgba(21,19,26,.55),rgba(21,19,26,.25))}
.phero .wrap.rvh-grid{display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:center;padding-bottom:56px}
.rvh .hcard{text-align:left;margin:0}.rvh .ctas{justify-content:flex-start}
.rvh-pic{margin:0;justify-self:center;max-width:560px;width:100%;transform:rotate(2deg);background:#fff;padding:12px 12px 0;border-radius:6px;box-shadow:0 24px 60px rgba(0,0,0,.45)}
.rvh-pic img{display:block;width:100%;height:auto;border-radius:3px}
.rvh-pic figcaption{font-size:14px;color:#3b3442;text-align:center;padding:10px 4px 12px;font-weight:600}
.rvh-pic.tall{max-width:380px}
@media(max-width:860px){.phero.rvh{padding-top:150px}.phero .wrap.rvh-grid{grid-template-columns:1fr;gap:26px}.rvh-pic{order:-1;max-width:460px;transform:rotate(1.5deg)}.rvh-pic.tall{max-width:300px}.rvh .hcard{text-align:center}.rvh .ctas{justify-content:center}}
@media(max-width:600px){.phero.rvh{padding:178px 0 0}.phero .wrap.rvh-grid{padding-bottom:30px}.rvh-pic{max-width:330px}.rvh-pic.tall{max-width:250px}}
'''

def end_of_div(s, start):
    """Index just after the </div> closing the <div ...> that starts at `start`."""
    depth, i = 0, start
    for m in re.finditer(r'<div\b|</div>', s[start:]):
        depth += 1 if m.group() == '<div' else -1
        if depth == 0: return start + m.end()
    raise ValueError('unclosed div')

def frame(page, photo, alt, caption):
    p = f'{OUT}/{page}'
    if not os.path.exists(p): return False
    s = open(p).read()
    if 'rvh-grid' in s: return False
    m = re.search(r'<header class="phero([^"]*)"><img src="([^"]+)"[^>]*>', s)
    if not m: print('  no heading photo on', page); return False
    src = photo or m.group(2)
    w, h = Image.open(os.path.normpath(os.path.join(OUT, src))).size
    tall = ' tall' if h > w else ''
    extra = m.group(1).replace(' hero-right', '')
    s = s[:m.start()] + f'<header class="phero rvh{extra}">' + s[m.end():]
    w0 = s.index('<div class="wrap">', m.start())
    hc = s.index('<div class="hcard">', w0)
    he = end_of_div(s, hc)
    fig = (f'<figure class="rvh-pic{tall}"><img src="{src}" width="{w}" height="{h}" alt="{alt}" fetchpriority="high">'
           f'<figcaption>{caption}</figcaption></figure>')
    s = s[:w0] + '<div class="wrap rvh-grid">' + s[w0 + len('<div class="wrap">'):he] + fig + s[he:]
    open(p, 'w').write(s)
    return True

def build():
    css = open(f'{OUT}/site.css').read()
    if '/* framed heading photo */' not in css:
        open(f'{OUT}/site.css', 'a').write(FRAME_CSS)
    n = sum(frame(pg, *v) for pg, v in FRAMES.items())
    print('framed heading photos on', n, 'pages')

if __name__ == '__main__':
    build()
