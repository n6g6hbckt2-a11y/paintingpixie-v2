# -*- coding: utf-8 -*-
"""Home page 'Areas We Cover': the drawn area map (pins link to each town page) plus a clear link to the full
Areas page with the live map, and the Sussex / Surrey pages. Runs after build_areas in both pipelines (12 Oct 2026)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_areas as A

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')

CSS = '''<style>
.k-homeareas .hmap{display:block;max-width:920px;margin:22px auto 0;border-radius:18px;overflow:hidden;box-shadow:0 24px 50px -28px rgba(0,0,0,.6)}
.k-homeareas .hmap svg{display:block;width:100%;height:auto}
.k-homeareas .hmap a text{text-decoration:none}
.k-homeareas .hbtns{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:22px}
.k-homeareas .hkey{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:center;margin:12px auto 0;font-size:14px}
.k-homeareas .hkey i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:6px;vertical-align:-1px;box-sizing:border-box}
.k-homeareas .hnote{max-width:720px;margin:14px auto 0;font-size:15px;opacity:.85}
</style>'''

def build():
    if os.environ.get('PP_NO_HOMEMAP'): return print('home areas: held back (PP_NO_HOMEMAP)')
    p = f'{OUT}/index.html'
    s = open(p).read()
    if 'k-homeareas' in s: return print('home areas: already done')
    m = re.search(r'<!-- AREAS WE COVER -->\s*<section[^>]*>.*?</section>', s, re.S)
    if not m: return print('home areas: section not found')
    html = ('<!-- AREAS WE COVER -->\n<section class="band band-dark k-text centred k-homeareas"><div class="wrap">'
            '<h2 style="text-align:center;">Areas We Cover</h2>'
            '<p>From home in Horsham, Kat paints across Sussex and Surrey, from <a href="face-painter-crawley.html">children’s parties in Crawley</a> to <a href="face-painter-brighton.html">hen dos in Brighton</a>, and travels further for weddings, festivals and corporate events. '
            'Tap a town on the map to see its page.</p>'
            f'<div class="hmap">{A.static_map(A.recent_places(), box=(51.56, 50.72, -1.12, 0.72), roads=True)}</div>'
            '<p class="hkey"><span><i style="background:#FF4FA3"></i>Regular area</span><span><i style="background:#E2BE7A"></i>Painted here recently</span>'
            '<span><i style="background:#A77BFF"></i>Coming up</span><span><i style="background:transparent;border:2px solid #9C83D1"></i>Further afield</span>'
            '<span><b style="display:inline-block;width:22px;border-top:3px dashed #E9DFF5;vertical-align:middle;margin-right:6px"></b>Train from Horsham to London</span></p>'
            '<div class="hbtns"><a href="areas.html" class="btn btn-gold">See the full map &amp; every area →</a>'
            '<a href="face-painter-sussex.html" class="btn btn-ghost">Sussex</a>'
            '<a href="face-painter-surrey.html" class="btn btn-ghost">Surrey</a></div>'
            '<p class="hnote">Not sure if your town is covered? <a href="contact.html">Ask Kat</a>, she travels further for the right event.</p>'
            '</div></section>')
    s = s[:m.start()] + html + s[m.end():]
    s = s.replace('</head>', CSS + '\n</head>', 1)
    open(p, 'w').write(s)
    print('home areas: map added')

if __name__ == '__main__':
    build()
