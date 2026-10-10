# -*- coding: utf-8 -*-
"""'Recent designs' photo rows (.mini-gallery):
- per-page photo choices (children's page: children only, with animal print, which is very popular)
- every photo zoomed in a little towards the face, so the face paint fills more of the tile.
Runs after build_reviewcap in both pipelines."""
import os, re, glob

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
g = lambda slug: f'../img/g/{slug}-800.webp'
def gz(slug):   # the gallery's zoomed-in crop when there is one
    return f'../img/g/{slug}-z-800.webp' if os.path.exists(f'{os.path.dirname(OUT)}/img/g/{slug}-z-800.webp') else g(slug)

# page: [(photo, alt, object-position)]
PICKS = {   # (photo, alt, object-position, caption shown on the photo)
    'childrens-face-painting.html': [
        (g('gold-tiger-boy'), 'Golden tiger face paint on a boy at a birthday party', '50% 35%', 'Golden tiger'),
        ('unicorn-birthday-face-paint-girl-horsham-festival.webp', 'Unicorn face paint design for a birthday, girl at a Horsham festival.', '74% 25%', 'Rainbow unicorn'),
        (g('tiger-girl-closeup'), 'Rainbow tiger face paint on a girl at a village hall party', '50% 35%', 'Rainbow tiger'),
        ('blue-dragon-face-paint-girl-laughing-horsham.webp', 'Blue dragon face paint design for a girl near Horsham.', '86% 25%', 'Blue dragon'),
    ],
    'adult-face-painting.html': [
        (g('adult-leopard-eye'), 'Gold leopard print half-face design with gems on a woman', '50% 35%', 'Gold leopard'),
        (g('adult-tiger-eye'), 'Orange tiger eye design on a woman at a festival', '50% 35%', 'Tiger eye'),
        (g('adult-flower-closeup'), 'Blue and purple flower face art with glitter on a woman', '60% 35%', 'Blue flower'),
        (g('adult-lilac-flower'), 'Lilac flower face art with rose-gold glitter on a woman', '45% 35%', 'Lilac flower'),
    ],
    'glitter-bar.html': [
        (g('arm-glitter-swirl'), 'Rainbow glitter swirl with gems painted on an arm', '50% 40%', 'Glitter swirl'),
        (g('festival-rainbow-body-art'), 'Rainbow and clouds glitter body art at a festival', '50% 45%', 'Festival rainbow'),
        (g('adult-pink-glitter'), 'Pink glitter and gem face art at a party', '45% 40%', 'Pink glitter'),
        (gz('glitter-tattoo-unicorn'), 'Girl with a sparkly glitter tattoo on her arm', '50% 40%', 'Glitter tattoo'),
    ],
    'animal-print-face-painting.html': [
        (gz('leopard-claws'), 'Girl with leopard face paint doing cat claws', '50% 35%', 'Leopard'),
        (g('leopard-boy'), 'Boy grinning at his leopard face paint in Kat’s mirror', '60% 35%', 'Leopard in the mirror'),
        (g('purple-leopard'), 'Girl with purple leopard print face paint', '70% 35%', 'Purple leopard'),
        (gz('tiger-boy-festival'), 'Boy with tiger face paint at a summer festival', '50% 35%', 'Tiger'),
    ],
}
# service pages: the photo row moves up to just under the opening text, with a heading for that service
TOP = {
    'childrens-face-painting.html': "Kat’s favourite children’s designs",
    'adult-face-painting.html': 'Grown-up and hen party looks',
    'glitter-bar.html': 'Glitter looks',
    'animal-print-face-painting.html': 'Tigers and leopards',
}

# photos whose face sits near the top edge: aim the crop and zoom higher
FOCUS = {'pumpkin-face-paint-for-sisters.webp': '50% 6%'}

# weak photo -> better one (any page)
SWAP = {
    # tiny boy far away in a field, and not animal print
    'blue-monster-face-paint-for-boys-crawley.webp': (g('leopard-indoors'), 'Leopard face paint on a smiling girl at an indoor party', '50% 30%'),
}
# rows with fewer than 4 photos are topped up from these close-ups (skipping any already on the page)
FILL = [
    (g('gold-tiger-boy'), 'Golden tiger face paint on a boy at a birthday party', '50% 35%'),
    (g('tiger-girl-closeup'), 'Rainbow tiger face paint on a girl at a village hall party', '50% 35%'),
    (g('rainbow-unicorn-girl'), 'Rainbow unicorn face paint on a smiling girl', '50% 30%'),
    (g('blue-monster-roar'), 'Blue monster face paint on a roaring girl', '50% 30%'),
]

CSS = '''
/* recent designs: zoomed towards the face */
.mini-gallery .mg{display:block;overflow:hidden;border-radius:10px;aspect-ratio:3/4}
.mini-gallery .mg img{width:100%;height:100%;aspect-ratio:auto;border-radius:0;transform:scale(1.12);transition:transform .3s}
.mini-gallery .mg:hover img{transform:scale(1.16)}
.mini-gallery .mg{position:relative}
.mini-gallery .mg em{position:absolute;left:0;right:0;bottom:0;padding:26px 10px 9px;font-style:normal;font-weight:700;font-size:14px;color:#fff;background:linear-gradient(180deg,transparent,rgba(15,12,18,.78));text-align:left}
'''

def build():
    css = open(f'{OUT}/site.css').read()
    if '/* recent designs: zoomed' not in css:
        open(f'{OUT}/site.css', 'a').write(CSS)
    n = 0
    for p in sorted(glob.glob(OUT + '/*.html')):
        page = os.path.basename(p); s = open(p).read()
        m = re.search(r'<div class="mini-gallery">(.*?)</div>', s, re.S)
        if not m or 'class="mg"' in m.group(1): continue
        if page in PICKS:
            imgs = list(PICKS[page])
        else:
            imgs = []
            for tag in re.findall(r'<img [^>]*>', m.group(1)):
                src = re.search(r'src="([^"]+)"', tag).group(1)
                alt = (re.search(r'alt="([^"]*)"', tag) or [None, ''])[1]
                pos = (re.search(r'object-position:\s*([^;"]+)', tag) or [None, 'center 25%'])[1].strip()
                pos = FOCUS.get(os.path.basename(src), pos)
                imgs.append(SWAP.get(os.path.basename(src), (src, alt, pos)))
            for extra in FILL:
                if len(imgs) >= 4: break
                if extra[0] not in s and extra[0] not in [i[0] for i in imgs]: imgs.append(extra)
        tiles = ''.join(f'<span class="mg"><img src="{src}" alt="{alt}" loading="lazy" '
                        f'style="object-position:{pos};transform-origin:{pos.replace("center", "50%")}">'
                        + (f'<em>{t[0]}</em>' if t else '') + '</span>' for src, alt, pos, *t in imgs)
        s = s[:m.start()] + f'<div class="mini-gallery">\n{tiles}\n</div>' + s[m.end():]
        if page in TOP and not os.environ.get('PP_NO_TOP'):   # move the row up under the opening text (PP_NO_TOP=1: leave it, until Phil approves)
            g_sec = re.search(r'<section class="band [^"]*k-gallery[^"]*">.*?</section>\s*', s, re.S)
            if g_sec:
                sec = re.sub(r'(<h2[^>]*>)Recent Designs(</h2>)', lambda mm: mm.group(1) + TOP[page] + mm.group(2), g_sec.group(0), count=1)
                sec = sec.replace(' k-gallery', ' k-gallery k-top', 1)
                s = s[:g_sec.start()] + s[g_sec.end():]
                first = re.search(r'<section class="band [^"]*k-text[^"]*">.*?</section>\s*', s, re.S)
                if first: s = s[:first.end()] + sec + s[first.end():]
                else: s = s[:g_sec.start()] + sec + s[g_sec.start():]
        open(p, 'w').write(s); n += 1
    print('recent designs rows updated on', n, 'pages')

if __name__ == '__main__':
    build()
