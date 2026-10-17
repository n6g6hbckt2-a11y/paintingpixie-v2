# -*- coding: utf-8 -*-
"""Breadcrumbs on every page: the small trail above each heading, and BreadcrumbList data Google can read.
17 Oct: every page gets an explicit trail. Town pages show the town (not a tagline) and sit under their county:
Home > Areas > Surrey > Reigate. Short names in Google's version (e.g. 'Hen & adult parties', not the full title)."""
import glob, json, os, re, html
OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
SITE = 'https://paintingpixie.com/'

import build_crosslinks as X
AREAS = ('Areas', 'areas.html')
SUSSEX = ('Sussex', 'face-painter-sussex.html')
SURREY = ('Surrey', 'face-painter-surrey.html')
SERVICES = ('Services', 'services.html')
GALLERY = ('Gallery', 'gallery.html')

TRAILS = {   # page: [parents...] + (own short name)
    'about.html': [], 'contact.html': [], 'gallery.html': [], 'reviews.html': [], 'areas.html': [], 'services.html': [],
    'prices.html': [], 'book.html': [],
    'face-painter-sussex.html': [AREAS], 'face-painter-surrey.html': [AREAS],
    'childrens-face-painting.html': [SERVICES], 'adult-face-painting.html': [SERVICES], 'glitter-bar.html': [SERVICES],
    'corporate-events.html': [SERVICES], 'workshops.html': [SERVICES], 'christmas-face-painting.html': [SERVICES],
    'halloween-face-painting.html': [SERVICES], 'animal-print-face-painting.html': [GALLERY],
}
NAMES = {
    'about.html': 'About Kat', 'contact.html': 'Book', 'gallery.html': 'Gallery', 'reviews.html': 'Reviews', 'areas.html': 'Areas',
    'services.html': 'Services', 'prices.html': 'Prices', 'book.html': 'Book online',
    'face-painter-sussex.html': 'Sussex', 'face-painter-surrey.html': 'Surrey',
    'childrens-face-painting.html': 'Children’s parties', 'adult-face-painting.html': 'Hen &amp; adult parties',
    'glitter-bar.html': 'Glitter bar', 'corporate-events.html': 'Corporate &amp; events', 'workshops.html': 'Workshop parties',
    'christmas-face-painting.html': 'Christmas', 'halloween-face-painting.html': 'Halloween',
    'animal-print-face-painting.html': 'Animal print designs',
}
for page, name in X.SUSSEX:
    TRAILS[page] = [AREAS, SUSSEX]; NAMES[page] = name
for page, name in X.SURREY:
    TRAILS[page] = [AREAS, SURREY]; NAMES[page] = name

def trail(page):
    if page not in TRAILS: return None
    return [('Home', './')] + TRAILS[page] + [(NAMES[page], None)]

def visible(t):
    return ' · '.join(f'<a href="{h}">{n}</a>' if h else n for n, h in t)

def schema(t, page):
    items = []
    for i, (n, h) in enumerate(t, 1):
        url = SITE if h == './' else SITE + (h or page)
        items.append({"@type": "ListItem", "position": i, "name": html.unescape(n), "item": url})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def apply(s, page, add_visible_before_h1=False):
    t = trail(page)
    if not t: return s, False
    m = re.search(r'<p class="crumb">(.*?)</p>', s, re.S)
    if m:
        s = s.replace(m.group(0), f'<p class="crumb">{visible(t)}</p>', 1)
    elif add_visible_before_h1:
        s = re.sub(r'(<h1[ >])', '<p class="crumb hwcrumb">' + visible(t) + '</p>\\1', s, count=1)
    s = re.sub(r'<script type="application/ld\+json" id="crumbs">.*?</script>\s*', '', s, flags=re.S)
    s = s.replace('</head>', '<script type="application/ld+json" id="crumbs">' + json.dumps(schema(t, page), ensure_ascii=False) + '</script>\n</head>', 1)
    return s, True

def build():
    n = 0
    for p in glob.glob(OUT + '/*.html'):
        page = os.path.basename(p)
        s = open(p).read()
        s2, ok = apply(s, page)
        if ok and s2 != s: open(p, 'w').write(s2); n += 1
    print('breadcrumbs on', n, 'pages')

HW_CSS = '<style>.hwcrumb{font:800 12.5px/1 Manrope,system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#FFC24A;margin:0 0 14px}.hwcrumb a{color:#FFC24A;text-decoration:none}.hwcrumb a:hover{text-decoration:underline}</style>\n'

def halloween(path):
    """The live Halloween page is its own design (hw/): add the trail above its heading and Google's version."""
    s = open(path).read()
    if 'hwcrumb' in s: return
    s, ok = apply(s, 'halloween-face-painting.html', add_visible_before_h1=True)
    s = s.replace('</head>', HW_CSS + '</head>', 1)
    open(path, 'w').write(s); print('breadcrumbs on the Halloween page')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1: halloween(sys.argv[1])
    else: build()
