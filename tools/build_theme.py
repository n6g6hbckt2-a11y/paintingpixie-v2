# -*- coding: utf-8 -*-
"""Site background chosen by Kat (7 Oct 2026): 'Pixie dust' (design idea H) instead of plain black.
The pattern sits still behind the page (like the Halloween page) and shows through every section that used to be black.
Light sections, the coloured price band and photo cards are unchanged. Runs after build_design_ideas (needs img/bg/pixie-dust.svg)."""
OUT = '/home/claude/paintingpixie-v2/draft'
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

def build():
    print('photo sections moved onto pixie dust on', photos_on_dust(), 'pages')
    with open(f'{OUT}/site.css') as f: s = f.read()
    if 'Background: Pixie dust' not in s:
        with open(f'{OUT}/site.css', 'a') as f: f.write(CSS)
    print('pixie dust background on')

if __name__ == '__main__':
    build()
