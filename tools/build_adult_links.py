# -*- coding: utf-8 -*-
"""13 Oct: adult/hen searches climbed to positions 9-12 after the 10 Oct adult page changes. Links in the page text with
the words people search ("adult face painting", "hen party glitter") help push them onto page 1.
Adds them to the hen/adult price card on the older town pages and the adult card on the home page. Runs after build_venue_insert."""
import glob, os
OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
CARD = '<p>Glitter, gems & adult-style designs for hen dos and celebrations</p>'
def card(page):
    where = ' in Brighton' if page.endswith('brighton.html') else ''
    return (f'<p><a href="adult-face-painting.html">Adult face painting{where}</a> and <a href="glitter-bar.html">hen party glitter</a>'
            ' for hen dos and celebrations</p>')
HOME = ('<p>Hen parties, festivals, brand activations & corporate events across Sussex and Surrey.</p>',
        '<p><a href="adult-face-painting.html">Hen party and adult face painting</a>, plus festivals, brand activations & corporate events across Sussex, Surrey and Brighton.</p>')
n = 0
for p in sorted(glob.glob(f'{OUT}/face-painter-*.html')):
    s = open(p).read()
    if CARD in s:
        open(p, 'w').write(s.replace(CARD, card(p))); n += 1
p = f'{OUT}/index.html'
if os.path.exists(p):
    s = open(p).read()
    if HOME[0] in s: open(p, 'w').write(s.replace(HOME[0], HOME[1])); n += 1
print('adult page links on', n, 'pages')
