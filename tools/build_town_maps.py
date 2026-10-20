# -*- coding: utf-8 -*-
"""17 Oct: the Crawley treatment for more town pages. Each page's favourite places and its halls to hire become one
section with a live street map (OpenStreetMap) and numbered pins; the illustrated postcard goes. Horsham already has
its own party map, so there the live street map goes over the drawn one.
Positions from OpenStreetMap (Nominatim lookups, 17 Oct). Runs after build_crawley_map (shares its CSS and map script)."""
import os, re, json, math
import build_crawley_map as C

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')

POS = {
    # Burgess Hill
    'The Triangle': (50.9649, -0.1521), "St John's Park": (50.9581, -0.1362), 'Ditchling &amp; the Downs': (50.9467, -0.1011),
    'Cyprus Hall': (50.9566, -0.1291), "St Andrew's Community Centre": (50.9600, -0.1222), 'Adastra Hall': (50.9240, -0.1379),
    'Sidney West Sports &amp; Community Centre': None,
    # Reigate & Redhill
    'Priory Park': (51.2313, -0.2123), 'Memorial Park, Redhill': (51.2433, -0.1672), 'Earlswood Lakes': (51.2206, -0.1857),
    'Reigate Hill &amp; Colley Hill': (51.2558, -0.2176), 'The Harlequin, Redhill': (51.2406, -0.1676),
    'Woodhatch Community Centre': (51.2250, -0.1970),
    # Brighton & Hove
    'The seafront hotels': (50.8213, -0.1470), 'Preston Park': (50.8460, -0.1553), 'Stanmer Park': (50.8665, -0.0970),
    'Hove Lawns': (50.8235, -0.1644), 'Brighton Pride': None, 'Wedding venues on the Downs': None,
    # Haywards Heath (20 Oct; Nominatim)
    'Victoria Park': (50.9971, -0.1060), 'Beech Hurst Gardens': (50.9984, -0.1154), 'Lindfield Common': (51.0088, -0.0805),
    'Cuckfield': None, 'Borde Hill Garden': (51.0196, -0.1178), 'The Dolphin Leisure Centre': (51.0056, -0.1104),
    "Queen's Hall, Cuckfield": (51.0073, -0.1421), 'Cuckfield Village Hall': None,
    'Scaynes Hill Millennium Village Centre': (50.9926, -0.0536),
    # Horsham
    'Horsham Park': (51.0674, -0.3265), 'Denne Park &amp; Hills Farm': (51.0486, -0.3330), 'Broadbridge Heath': (51.0642, -0.3584),
    'Southwater Country Park': (51.0197, -0.3497), 'Chesworth Farm': (51.0530, -0.3231), 'The Carfax': (51.0625, -0.3282),
}
MERGE = {   # page: (heading, lede, tone)
    'face-painter-brighton.html': ('Where Brighton &amp; Hove events happen',
                                   'Seafront hotels, parks and festival fields where Kat paints. The numbers match the map.', 'light'),
    'face-painter-burgess-hill.html': ('Where Burgess Hill parties happen',
                                       'Favourite spots for summer parties, and halls to hire when it’s cold or wet. The numbers match the map.', 'dark'),
    'face-painter-haywards-heath.html': ('Where Haywards Heath parties happen',
                                         'Parks and gardens for summer parties, and village halls to hire when it’s cold or wet. The numbers match the map.', 'light'),
    'face-painter-reigate.html': ('Where Reigate and Redhill parties happen',
                                  'Parks and hills for summer parties, and halls to hire when it’s cold or wet. The numbers match the map.', 'light'),
}

CSS = '''
/* town maps (17 Oct): light-band version and Horsham's live map */
.loc-where.band-light .vnote{color:#4E463F}
.loc-where.band-light .cmapbox{border:1px solid rgba(0,0,0,.08)}
.loc-map .cmapbox{position:relative;border-radius:18px;overflow:hidden;aspect-ratio:1200/560;margin-bottom:8px}
.loc-map .cmapbox .vmapsvg{position:absolute;inset:0;width:100%;height:100%;margin:0}
.loc-map .cmapbox #cmaplive{position:absolute;inset:0;opacity:0;transition:opacity .4s}
.loc-map .cmapbox.is-live #cmaplive{opacity:1}
.loc-map .cnum{width:30px;height:30px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#FF4FA3;border:3px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.35);display:grid;place-items:center}
.loc-map .cnum b{transform:rotate(45deg);color:#fff;font:800 14px/1 Manrope,system-ui,sans-serif}
.loc-map .leaflet-popup-content{font:600 14px/1.45 Manrope,system-ui,sans-serif;margin:10px 14px}
.loc-map .leaflet-popup-content b{display:block;font-size:16px;color:#1B1712}
@media(max-width:700px){.loc-map .cmapbox{aspect-ratio:4/3}}
.cplaces .ptag{font-style:normal;display:inline-block;font-size:12px;font-weight:800;padding:2px 8px;border-radius:20px;background:#2f8f5b;color:#fff;margin-left:6px;vertical-align:2px}
'''

def plain_map(pins):
    """Fallback if street maps can't load: the numbered pins in their real positions on a plain background."""
    la = [p[1] for p in pins]; lo = [p[2] for p in pins]
    n, s, w, e = max(la), min(la), min(lo), max(lo)
    padla, padlo = (n - s) * .18 + .004, (e - w) * .18 + .006
    n, s, w, e = n + padla, s - padla, w - padlo, e + padlo
    kx = math.cos(math.radians((n + s) / 2)); W = 760; H = 577
    sc = min(W / ((e - w) * kx), H / (n - s)); ox = (W - (e - w) * kx * sc) / 2; oy = (H - (n - s) * sc) / 2
    xy = lambda a, b: (ox + (b - w) * kx * sc, oy + (n - a) * sc)
    f = 'font-family="Manrope,system-ui,sans-serif"'
    o = [f'<svg class="cmap" viewBox="0 0 {W} {H}" role="img" aria-label="Map showing where the places are">', f'<rect width="{W}" height="{H}" fill="#F6F0E6"/>']
    for i, (nm, a, b) in enumerate(pins, 1):
        x, y = xy(a, b)
        o.append(f'<path d="M{x:.0f},{y:.0f} c-12,-14 -16,-20 -16,-27 a16,16 0 1 1 32,0 c0,7 -4,13 -16,27z" fill="#FF4FA3" stroke="#fff" stroke-width="2.5"/>'
                 f'<text x="{x:.0f}" y="{y - 22:.0f}" text-anchor="middle" font-size="15" font-weight="800" fill="#fff" {f}>{i}</text>'
                 f'<text x="{x + 20:.0f}" y="{y - 18:.0f}" font-size="13" font-weight="700" fill="#5A4E60" stroke="#F6F0E6" stroke-width="4" paint-order="stroke" {f}>{nm}</text>')
    o.append(f'<text x="{W - 10}" y="{H - 10}" text-anchor="end" font-size="11" fill="#8B8091" {f}>Not to scale</text></svg>')
    return ''.join(o)

def js(pins, box_id='cmapbox'):
    return C.LIVE_JS.replace('__PINS__', json.dumps([dict(n=n, lat=a, lon=b, t=t) for n, a, b, t in pins], ensure_ascii=False)).replace("'cmapbox'", f"'{box_id}'")

def add_head_and_js(s, script):
    if 'vendor/leaflet/leaflet.css' not in s:
        s = s.replace('</head>', '<link rel="stylesheet" href="../vendor/leaflet/leaflet.css">\n</head>', 1)
    return s.replace('<script src="site.js"></script>', script + '\n<script src="site.js"></script>', 1)

def merge(page, heading, lede, tone):
    p = f'{OUT}/{page}'
    s = open(p).read()
    if 'loc-where' in s: return
    places_sec = re.search(r'<section class="band [^"]*loc-(?:chips|places|vcards)[^"]*">.*?</section>\s*', s, re.S)
    hire_sec = re.search(r'<section class="band [^"]*loc-hire[^"]*">.*?</section>\s*', s, re.S)
    card = re.search(r'<section class="band [^"]*loc-postcard">.*?</section>\s*', s, re.S)
    if not places_sec: print('town maps: no places on', page); return
    t = places_sec.group(0)
    places = re.findall(r'<summary>(.*?)</summary><span>(.*?)</span>', t) or re.findall(r'<figcaption><b>(.*?)</b><span>(.*?)</span></figcaption>', t) \
             or re.findall(r'<div class="vcard"><b>(.*?)</b><span>(.*?)</span></div>', t)
    venues = re.findall(r'<li>(?:<span class="tag[^"]*">(.*?)</span>)?<b>(.*?)</b><i>(.*?)</i>(.*?)</li>', hire_sec.group(0), re.S) if hire_sec else []
    vnote = re.search(r'<p class="vnote">.*?</p>', hire_sec.group(0), re.S) if hire_sec else None
    pins, items, extra = [], '', ''
    for nm, txt in places:
        if POS.get(nm):
            pins.append((nm, *POS[nm], txt)); items += f'<li><b>{nm}</b><span>{txt}</span></li>'
        else:
            extra += f'<li class="nopin"><b>{nm}</b><span>{txt}</span></li>'
    for tag, nm, where, rest in venues:
        txt = re.sub(r'\s*<a [^>]*>.*?</a>', '', rest).strip(); link = re.search(r'<a [^>]*>.*?</a>', rest)
        badge = f' <em class="ptag">{tag}</em>' if tag else ''   # e.g. "Recommends Kat ✓" (20 Oct: was being dropped)
        line = f'<b>{nm}{badge}</b><span>{where}. {txt}</span>{link.group(0) if link else ""}'
        if POS.get(nm):
            pins.append((nm, *POS[nm], f'{where}. {txt}')); items += f'<li>{line}</li>'
        else:
            extra += f'<li class="nopin">{line}</li>'
    if not vnote:
        vnote_html = ''
    else:
        vnote_html = vnote.group(0)
    sec = (f'<section class="band band-{tone} loc-where"><div class="wrap"><h2>{heading}</h2><p class="lede-s">{lede}</p>'
           f'<div class="cwgrid"><div class="cmapbox" id="cmapbox">{plain_map([(n, a, b) for n, a, b, _ in pins])}</div>'
           f'<div><ol class="cplaces">{items}{extra}</ol>{vnote_html}</div></div></div></section>\n')
    if hire_sec: s = s.replace(hire_sec.group(0), '', 1)
    if card: s = s.replace(card.group(0), '', 1)
    s = s.replace(places_sec.group(0), sec, 1)
    s = add_head_and_js(s, js(pins))
    s = retone(s)
    open(p, 'w').write(s)
    print('town maps:', page, len(pins), 'pins')

def retone(s):
    """Removing sections can leave two light (or two dark) bands touching: flip the later one so they alternate."""
    main = re.search(r'<main.*?</main>', s, re.S)
    if not main: return s
    m = main.group(0); prev = None; out = []; last = 0
    for t in re.finditer(r'<section class="band (band-(light|dark|jewel|panel)|trustband)', m):
        tone = t.group(2)
        if tone in ('light', 'dark'):
            if tone == prev:
                new = 'dark' if tone == 'light' else 'light'
                out.append(m[last:t.start(1)] + 'band-' + new); last = t.end(1); tone = new
        prev = tone if tone in ('light', 'dark') else None
    out.append(m[last:])
    return s.replace(m, ''.join(out), 1)

def horsham():
    p = f'{OUT}/face-painter-horsham.html'
    s = open(p).read()
    m = re.search(r'<section class="band [^"]*loc-map[^"]*">.*?</section>', s, re.S)
    if not m or 'cmapbox' in m.group(0): return
    sec = m.group(0)
    names = re.findall(r'<li><b>(.*?)</b><span>(.*?)</span>', sec)
    pins = [(n, *POS[n], t) for n, t in names if POS.get(n)]
    if len(pins) != len(names): print('town maps: Horsham pins missing'); return
    svg = re.search(r'<svg class="postcard vmapsvg".*?</svg>', sec, re.S).group(0)
    new = sec.replace(svg, f'<div class="cmapbox" id="cmapbox">{svg}</div>', 1)
    new = new.replace('Map not to scale.', '').replace('<p class="vmapnote">Venue links go to each venue’s own website. </p>', '<p class="vmapnote">Venue links go to each venue’s own website.</p>')
    s = s.replace(sec, new, 1)
    script = js(pins).replace("var sv = box.querySelector('.cmap')", "var sv = box.querySelector('.vmapsvg')")
    s = add_head_and_js(s, script)
    open(p, 'w').write(s)
    print('town maps: Horsham live map,', len(pins), 'pins')

ONLY = os.environ.get('PP_TOWNS', '').split()

def build():
    for page, (h, lede, tone) in MERGE.items():
        if ONLY and page not in ONLY: continue
        if os.path.exists(f'{OUT}/{page}'): merge(page, h, lede, tone)
    if (not ONLY or 'face-painter-horsham.html' in ONLY) and os.path.exists(f'{OUT}/face-painter-horsham.html'): horsham()
    cp = f'{OUT}/site.css'; c = open(cp).read()
    if '/* town maps (17 Oct)' not in c: open(cp, 'a').write(CSS)

if __name__ == '__main__':
    build()
