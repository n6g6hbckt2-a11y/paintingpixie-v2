# -*- coding: utf-8 -*-
"""Switch build only: take out new pages that aren't approved yet (PP_HOLD), and point their links somewhere sensible.
Release a page by removing it from PP_HOLD in build_switch.sh and rebuilding."""
import os, re, glob
OUT = os.environ['PP_OUT']
HOLD = os.environ.get('PP_HOLD', '').split()
FALLBACK = {'prices.html': 'index.html#prices', 'corporate-events.html': 'contact.html'}
MENU_LABEL = {'corporate-events.html': True}   # drop from menus and footer rather than redirect the label

def build():
    for page in HOLD:
        p = f'{OUT}/{page}'
        if os.path.exists(p): os.remove(p)
    for f in glob.glob(OUT + '/*.html'):
        s0 = s = open(f).read()
        for page in HOLD:
            if MENU_LABEL.get(page):   # remove the item from the drop-down, phone menu and footer lists
                s = re.sub(rf'<a href="{re.escape(page)}">[^<]*</a>', '', s)
            s = re.sub(r'\{"@type": "ListItem", "position": \d+, "name": "[^"]*", "url": "https://paintingpixie.com/' + re.escape(page) + r'"\},? ?', '', s)   # structured data lists
            s = s.replace(f'href="{page}"', f'href="{FALLBACK.get(page, "contact.html")}"')
        if f.endswith('/index.html') and 'id="prices"' not in s:   # anchor for the Prices menu item
            s = s.replace('<section class="band band-jewel k-packages centred packages-section"', '<section id="prices" class="band band-jewel k-packages centred packages-section"', 1)
        if s != s0: open(f, 'w').write(s)
    print('held back:', ', '.join(HOLD) or 'nothing')

if __name__ == '__main__':
    build()
