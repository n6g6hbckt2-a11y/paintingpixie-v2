# -*- coding: utf-8 -*-
"""Sussex and Surrey county pages: the Areas page map (live map + drawn backup), zoomed to that county,
with only its towns, each pin linked to the local page. Runs after build_areas in both pipelines."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_areas as A
from recent import COMING_UP

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')

# page: (county name in headings, counties included, drawn-map box (lat top, lat bottom, lon left, lon right), intro)
COUNTIES = {
    'face-painter-sussex.html': ('Sussex', {'West Sussex', 'East Sussex'}, (51.19, 50.72, -0.92, 0.78),
        'From home in Horsham, Kat paints at parties and events across West and East Sussex.'),
    'face-painter-surrey.html': ('Surrey', {'Surrey'}, (51.55, 51.03, -1.08, 0.24),
        'From home in Horsham, just south of the Surrey border, Kat paints at parties and events across Surrey, and travels into London for events.'),
}

def section(name, counties, box, intro):
    recent = A.recent_places()
    towns = [t for t in A.TOWNS if t[3] in counties or t[0] == 'Horsham']
    lat0, lat1, lon0, lon1 = box
    wider = [w for w in A.WIDER if lat1 < w[1] < lat0 and lon0 < w[2] < lon1 - 0.18]   # leave room for the label
    pins = [dict(n=n, lat=a, lon=b, c=c, u=u, note=A.NOTES.get(n, f'Parties and events in {n}.'),
                 r=(n.split(' ')[0] in recent or n in recent), s=any(pl.split(',')[0].strip() == n for pl, *_ in COMING_UP))
            for n, a, b, c, u, g in towns]
    wider_pins = [[n, a, b, n in recent, bool(A.wider_soon(n))] for n, a, b in wider]
    html = (f'<section class="band band-light k-map"><div class="wrap">'
            f'<p class="eyebrow">Map</p><h2>Where Kat paints in {name}</h2>'
            f'<p>{intro} Tap a pin to see the local page. Gold pins are places Kat has painted recently.</p>'
            f'<div id="areamap" class="areamap" role="region" aria-label="Map of the {name} towns The Painting Pixie covers">'
            f'{A.static_map(recent, towns, wider, box)}</div>'
            '<div class="legend"><span><i class="pin home"></i> Home: Horsham</span><span><i class="pin"></i> Regular area, with a local page</span>'
            '<span><i class="pin recent"></i> Painted here recently</span><span><i class="pin soon"></i> Coming up in the next 2 months</span>'
            '<span><i class="pin wide"></i> Further afield: Kat travels here too</span></div>'
            '<p class="small-note">The shaded zone is about 40 minutes from Horsham. Kat travels further afield too, for parties, local events, '
            'weddings, festivals and corporate events. <a href="areas.html">See every area on the full map →</a></p>'
            '</div></section>\n')
    return html, A.map_js(pins, wider_pins, fit_wider=(name == 'Surrey'))   # Surrey map takes in the London venues

def build():
    n = 0
    for page, (name, counties, box, intro) in COUNTIES.items():
        p = f'{OUT}/{page}'
        if not os.path.exists(p): continue
        s = open(p).read()
        if 'k-map' in s: continue
        html, js = section(name, counties, box, intro)
        m = re.search(r'<section class="band [^"]*k-text[^"]*">.*?</section>\s*', s, re.S)   # after the opening text
        if not m: print('  no place for the map on', page); continue
        s = s[:m.end()] + html + s[m.end():]
        s = s.replace('</head>', '<link rel="stylesheet" href="../vendor/leaflet/leaflet.css">\n</head>', 1)
        css = A.MAP_CSS.replace('</style>', '.k-map .areamap:not(.is-live){height:auto}\n</style>')   # drawn map: full size, not squeezed into 560px
        s = s.replace('<script src="site.js"></script>', css + '\n' + js + '\n<script src="site.js"></script>', 1)
        open(p, 'w').write(s); n += 1
    print('county maps on', n, 'pages')

if __name__ == '__main__':
    build()
