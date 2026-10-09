# -*- coding: utf-8 -*-
"""Reviews section on each page: one grid in one card style, at most two rows
(6 reviews on desktop, 4 on tablet, 2 on phones), then a button to the full Reviews page.
Verified Add to Event reviews go first. Runs after build_frames in both pipelines."""
import os, re, glob, sys
sys.path.insert(0, os.path.dirname(__file__))
import reviews_data as R

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
TOTAL = len(R.ATE) + len(R.GOOGLE) + R.GOOGLE_STAR_ONLY

CSS = '''
/* reviews: two rows max */
.k-reviews .testimonials.rv2{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:26px;align-items:stretch}
.rv2>.testimonial,.rv2>.latest{margin:0;text-align:left;background:linear-gradient(135deg,rgba(255,79,163,.14),rgba(47,212,196,.10));border:1px solid rgba(226,190,122,.45);border-radius:18px;padding:26px 28px}
.rv2>.testimonial p{font-size:18px}
.rv2>:nth-child(n+7){display:none}
.k-reviews .rv-all{margin:34px 0 0!important;text-align:center}
@media(max-width:1000px){.k-reviews .testimonials.rv2{grid-template-columns:repeat(2,1fr)}.rv2>:nth-child(n+5){display:none}}
@media(max-width:640px){.k-reviews .testimonials.rv2{grid-template-columns:1fr}.rv2>:nth-child(n+3){display:none}}
'''

def items(block, tag, cls):
    """Every <tag class="cls">...</tag> in block (handles nesting of the same tag)."""
    out, pos = [], 0
    while True:
        i = block.find(f'<{tag} class="{cls}"', pos)
        if i < 0: return out
        depth, j = 0, i
        for m in re.finditer(rf'<{tag}\b|</{tag}>', block[i:]):
            depth += 1 if m.group() != f'</{tag}>' else -1
            if depth == 0: j = i + m.end(); break
        out.append(block[i:j]); pos = j

def cap(page_path):
    s = open(page_path).read()
    m = re.search(r'<section[^>]*k-reviews.*?</section>', s, re.S)
    if not m or 'rv2' in m.group(): return False
    sec = m.group()
    quotes = items(sec, 'figure', 'latest') + items(sec, 'div', 'testimonial')
    if not quotes: return False
    # drop the old containers, put one grid where the first one was
    start = sec.index('<div class="testimonials">')
    new = sec
    for c in ('<div class="testimonials">', '<div class="latest-wrap">'):
        while c in new:
            a = new.index(c); b = a
            depth = 0
            for mm in re.finditer(r'<div\b|</div>', new[a:]):
                depth += 1 if mm.group() == '<div' else -1
                if depth == 0: b = a + mm.end(); break
            new = new[:a] + ('\x00' if c == '<div class="testimonials">' else '') + new[b:]
    link = '' if 'reviews.html' in sec else f'<p class="rv-all"><a class="btn btn-gold" href="reviews.html">Read all {TOTAL} reviews →</a></p>'
    new = new.replace('\x00', f'<div class="testimonials rv2">{"".join(quotes)}</div>{link}', 1)
    open(page_path, 'w').write(s[:m.start()] + new + s[m.end():])
    return True

def build():
    css = open(f'{OUT}/site.css').read()
    if '/* reviews: two rows max */' not in css:
        open(f'{OUT}/site.css', 'a').write(CSS)
    n = sum(cap(p) for p in sorted(glob.glob(OUT + '/*.html')))
    print('reviews capped at two rows on', n, 'pages')

if __name__ == '__main__':
    build()
