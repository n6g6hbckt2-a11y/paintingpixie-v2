# -*- coding: utf-8 -*-
"""'Recent designs' photo rows (.mini-gallery):
- per-page photo choices (children's page: children only, with animal print, which is very popular)
- every photo zoomed in a little towards the face, so the face paint fills more of the tile.
Runs after build_reviewcap in both pipelines."""
import os, re, glob

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
g = lambda slug: f'../img/g/{slug}-800.webp'

# page: [(photo, alt, object-position)]
PICKS = {
    'childrens-face-painting.html': [
        (g('gold-tiger-boy'), 'Golden tiger face paint on a boy at a birthday party', '50% 35%'),
        ('unicorn-birthday-face-paint-girl-horsham-festival.webp', 'Unicorn face paint design for a birthday, girl at a Horsham festival.', '74% 25%'),
        (g('tiger-girl-closeup'), 'Rainbow tiger face paint on a girl at a village hall party', '50% 35%'),
        ('blue-dragon-face-paint-girl-laughing-horsham.webp', 'Blue dragon face paint design for a girl near Horsham.', '86% 25%'),
    ],
}

CSS = '''
/* recent designs: zoomed towards the face */
.mini-gallery .mg{display:block;overflow:hidden;border-radius:10px;aspect-ratio:3/4}
.mini-gallery .mg img{width:100%;height:100%;aspect-ratio:auto;border-radius:0;transform:scale(1.22);transition:transform .3s}
.mini-gallery .mg:hover img{transform:scale(1.28)}
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
            imgs = [(src, alt, pos) for src, alt, pos in PICKS[page]]
        else:
            imgs = []
            for tag in re.findall(r'<img [^>]*>', m.group(1)):
                src = re.search(r'src="([^"]+)"', tag).group(1)
                alt = (re.search(r'alt="([^"]*)"', tag) or [None, ''])[1]
                pos = (re.search(r'object-position:\s*([^;"]+)', tag) or [None, 'center 25%'])[1].strip()
                imgs.append((src, alt, pos))
        tiles = ''.join(f'<span class="mg"><img src="{src}" alt="{alt}" loading="lazy" '
                        f'style="object-position:{pos};transform-origin:{pos}"></span>' for src, alt, pos in imgs)
        s = s[:m.start()] + f'<div class="mini-gallery">\n{tiles}\n</div>' + s[m.end():]
        open(p, 'w').write(s); n += 1
    print('recent designs rows updated on', n, 'pages')

if __name__ == '__main__':
    build()
