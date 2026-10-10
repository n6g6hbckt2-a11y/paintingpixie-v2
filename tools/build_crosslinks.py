# -*- coding: utf-8 -*-
"""Town <-> service links inside the page: each town page gets "What Kat does in <town>",
each service page gets "Find your area". Runs after build_photos, before build_breadcrumbs."""
import os, re

OUT = __import__('os').environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')

SERV = {
    'kids':   ('childrens-face-painting.html', 'Children’s parties', 'Birthday parties at home, in a hall or a garden.', 'From £130'),
    'hens':   ('adult-face-painting.html', 'Hen &amp; adult parties', 'Glitter, gems and grown-up designs.', 'From £150'),
    'glitter':('glitter-bar.html', 'Glitter bar', 'Chunky bio-glitter and gems for festivals and parties.', 'Bespoke quote'),
    'events': ('corporate-events.html', 'Corporate &amp; events', 'Staff days, fêtes, launches and big crowds.', 'Bespoke quote'),
    'body':   ('body-art.html', 'Body art', 'Painted arm and body designs for Pride, festivals and shoots.', 'Bespoke quote'),
    'learn':  ('workshops.html', 'Workshop parties', 'Guests learn to face paint and paint each other, with Kat.', '£15 per child'),
}
DEFAULT = ['kids', 'hens', 'glitter', 'events']
EVENTS_FIRST = ['events', 'glitter', 'hens']   # Brighton: Kat targets events; parties via get in touch

TOWNS = {   # page: (name used in headings, service order)
    'face-painter-horsham.html': ('Horsham', DEFAULT + ['learn']),
    'face-painter-crawley.html': ('Crawley', DEFAULT),
    'face-painter-haywards-heath.html': ('Haywards Heath', DEFAULT),
    'face-painter-burgess-hill.html': ('Burgess Hill', DEFAULT),
    'face-painter-east-grinstead.html': ('East Grinstead', DEFAULT),
    'face-painter-worthing.html': ('Worthing', DEFAULT),
    'face-painter-brighton.html': ('Brighton &amp; Hove', EVENTS_FIRST),
    'face-painter-lewes.html': ('Lewes', DEFAULT),
    'face-painter-west-sussex-villages.html': ('the West Sussex villages', DEFAULT),
    'face-painter-south-downs.html': ('Midhurst &amp; Petworth', DEFAULT),
    'face-painter-sussex.html': ('Sussex', DEFAULT + ['learn']),
    'face-painter-guildford.html': ('Guildford', DEFAULT),
    'face-painter-dorking.html': ('Dorking', DEFAULT),
    'face-painter-reigate.html': ('Reigate &amp; Redhill', DEFAULT),
    'face-painter-surrey-villages.html': ('the Surrey villages', DEFAULT),
    'face-painter-surrey.html': ('Surrey', DEFAULT + ['learn']),
}
SUSSEX = [('face-painter-horsham.html', 'Horsham'), ('face-painter-crawley.html', 'Crawley'), ('face-painter-haywards-heath.html', 'Haywards Heath'),
          ('face-painter-burgess-hill.html', 'Burgess Hill'), ('face-painter-east-grinstead.html', 'East Grinstead'), ('face-painter-worthing.html', 'Worthing'),
          ('face-painter-brighton.html', 'Brighton &amp; Hove'), ('face-painter-lewes.html', 'Lewes'),
          ('face-painter-west-sussex-villages.html', 'West Sussex villages'), ('face-painter-south-downs.html', 'Midhurst &amp; Petworth')]
SURREY = [('face-painter-guildford.html', 'Guildford'), ('face-painter-dorking.html', 'Dorking'), ('face-painter-reigate.html', 'Reigate &amp; Redhill'),
          ('face-painter-surrey-villages.html', 'Surrey villages')]
SERVICE_PAGES = {   # page: lead-in naming the service
    'childrens-face-painting.html': 'Children’s party face painting',
    'adult-face-painting.html': 'Hen and adult party face painting',
    'glitter-bar.html': 'The glitter bar',
    'corporate-events.html': 'Corporate and event face painting',
    'christmas-face-painting.html': 'Christmas face painting',
    'workshops.html': 'Workshop parties',
}

CSS = '''
/* town <-> service links */
.xl-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px;margin-top:22px}
.xl-card{display:flex;flex-direction:column;gap:6px;background:var(--panel);border:1px solid var(--line);border-left:5px solid var(--c,var(--pink));border-radius:14px;padding:18px 18px 16px;text-decoration:none;color:var(--ink);transition:transform .15s,border-color .15s}
.xl-card:nth-child(4n+2){--c:var(--teal)}.xl-card:nth-child(4n+3){--c:var(--violet)}.xl-card:nth-child(4n){--c:var(--gold)}
.xl-card:hover{transform:translateY(-2px);border-color:var(--c,var(--pink))}
.xl-card b{font-family:'Fraunces',serif;font-weight:400;font-size:22px}
.xl-card span{color:var(--muted);font-size:15px;flex:1}
.xl-card em{font-style:normal;font-weight:800;color:var(--gold);font-size:14px}
.xl-more{margin-top:18px;color:var(--muted)}.xl-more a{font-weight:700}
.xl-areas{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:20px}
.xl-areas h3{margin:0 0 10px;font-size:13px;letter-spacing:1.6px;text-transform:uppercase;color:var(--teal);font-family:inherit}
.xl-chips{display:flex;flex-wrap:wrap;gap:10px}
.xl-chips a{border:1px solid var(--line);background:var(--panel);border-radius:999px;padding:9px 16px;color:var(--ink);text-decoration:none;font-weight:600;font-size:15px}
.xl-chips a:hover{border-color:var(--gold);color:var(--gold)}
@media(max-width:700px){.xl-areas{grid-template-columns:1fr}}
'''

def town_block(page, name, order):
    cards = ''.join(f'<a class="xl-card" href="{SERV[k][0]}"><b>{SERV[k][1]}</b><em>{SERV[k][3]} →</em></a>' for k in order)   # no blurb: the same blurb on every town page made them look alike
    note = ''
    if page == 'face-painter-brighton.html':
        note = ' Children’s parties in Brighton &amp; Hove are welcome too: <a href="contact.html">get in touch</a> with your date.'
    return (f'<section class="band band-dark xl-town"><div class="wrap"><p class="eyebrow">Services</p>'
            f'<h2>What Kat does in {name}</h2>'
            f'<p>Pick the kind of event you’re planning to see designs, prices and reviews.{note}</p>'
            f'<div class="xl-cards">{cards}</div>'
            f'<p class="xl-more">Something else? See <a href="services.html">all services</a> or <a href="prices.html">every price</a>.</p></div></section>\n')

def area_block(lead):
    chips = lambda l: ''.join(f'<a href="{h}">{t}</a>' for h, t in l)
    return (f'<section class="band band-dark xl-area"><div class="wrap"><p class="eyebrow">Areas</p>'
            f'<h2>Find your area</h2>'
            f'<p>{lead} is available across Sussex and Surrey, within about 40 minutes of Horsham. Choose your area for local details.</p>'
            f'<div class="xl-areas"><div><h3>Sussex</h3><div class="xl-chips">{chips(SUSSEX)}</div></div>'
            f'<div><h3>Surrey</h3><div class="xl-chips">{chips(SURREY)}</div></div></div>'
            f'<p class="xl-more">Not sure if you’re covered? See the <a href="areas.html">map of every area</a>.</p></div></section>\n')

def insert_before(s, pattern, block):
    m = re.search(pattern, s)
    return (s[:m.start()] + block + s[m.start():]) if m else None

REDIRECTS = {  # retired pages -> where they now live (old address keeps working and passes on its Google standing)
    'animal-print-face-painting.html': ('gallery.html#animal', 'gallery.html', 'Animal print designs in the gallery'),
    'body-art.html': ('gallery.html#glitter', 'gallery.html', 'Glitter and body art in the gallery'),
}
REDIRECT_HTML = '''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={go}">
<link rel="canonical" href="https://paintingpixie.com/{canon}">
<meta name="robots" content="noindex,follow">
<title>Redirecting… | The Painting Pixie</title>
<script>location.replace('{go}');</script>
</head>
<body>
<p>This page has moved. Please continue to <a href="{go}">{label}</a>.</p>
</body>
</html>
'''

ONLY = os.environ.get('PP_TOWNS', '').split()   # switch build: town links on these town pages only, nothing else

def build():
    import glob
    for page, (go, canon, label) in ({} if ONLY else REDIRECTS).items():
        open(f'{OUT}/{page}', 'w').write(REDIRECT_HTML.format(go=go, canon=canon, label=label))
        for f in glob.glob(OUT + '/*.html'):   # point in-page links straight at the new place
            if f.endswith('/' + page): continue
            t = open(f).read()
            if f'href="{page}"' in t: open(f, 'w').write(t.replace(f'href="{page}"', f'href="{go}"'))
    with open(f'{OUT}/site.css') as f: css = f.read()
    if '/* town <-> service links */' not in css:
        with open(f'{OUT}/site.css', 'a') as f: f.write(CSS)
    n = 0
    for page, (name, order) in TOWNS.items():
        if ONLY and page not in ONLY: continue
        p = f'{OUT}/{page}'; s = open(p).read()
        if 'xl-town' in s: continue
        m = re.search(r'<section class="band band-jewel loc-prices.*?</section>\s*', s, re.S)
        if not m: print('no place on', page); continue
        nxt = re.match(r'<section class="band (band-\w+)', s[m.end():])
        block = town_block(page, name, order)
        if nxt and nxt.group(1) == 'band-dark': block = block.replace('band band-dark xl-town', 'band band-panel xl-town', 1)
        s2 = s[:m.end()] + block + s[m.end():]
        if not s2: print('no place on', page); continue
        open(p, 'w').write(s2); n += 1
    for page, lead in ({} if ONLY else SERVICE_PAGES).items():
        p = f'{OUT}/{page}'
        if not os.path.exists(p): print('missing', page); continue
        s = open(p).read()
        if 'xl-area' in s: continue
        s2 = insert_before(s, r'<section class="band band-panel k-enquire', area_block(lead))
        if not s2: print('no place on', page); continue
        open(p, 'w').write(s2); n += 1
    print('town/service links on', n, 'pages')

if __name__ == '__main__':
    build()
