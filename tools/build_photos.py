# -*- coding: utf-8 -*-
"""Final photo pass (runs last): best-quality header photos per page, and swap weaker or bordered photos site-wide
for the cleaned, higher-resolution versions in img/g/."""
import glob, os, re

OUT = '/home/claude/paintingpixie-v2/draft'
g = lambda slug, size=1600: f'../img/g/{slug}-{size}.webp'

# page: (photo, object-position)
HEROES = {
    'about.html': (g('kat-painting-smile'), '45% 35%'),
    'gallery.html': (g('teen-red-dragon'), '50% 30%'),
    'workshops.html': (g('kat-close-painting'), '40% 40%'),
    'areas.html': (g('kat-painting-wide'), '45% 40%'),
    'services.html': (g('leopard-being-painted'), '60% 35%'),
    'face-painter-sussex.html': (g('rainbow-laughing'), '70% 40%'),
    'contact.html': (g('rainbow-unicorn-girl'), '50% 30%'),
    'face-painter-reigate.html': (g('leopard-indoors'), '50% 30%'),
    'face-painter-surrey-villages.html': (g('unicorn-soft-play'), '50% 30%'),
    'face-painter-lewes.html': (g('tiger-girl-closeup'), '50% 30%'),
    'childrens-face-painting.html': (g('unicorn-party'), '50% 30%'),
}
# old file name (any path) -> better version
SWAP = {
    'n-crown-girl-blue-sky.webp': g('rainbow-unicorn-girl', 800),
    'pink-and-gold-flame-tiara-face-paint-for-girls.webp': g('adult-pink-glitter', 800),
    'n-tiger-girl-closeup.webp': g('tiger-girl-closeup', 800),
    'n-unicorn-girl-party.webp': g('unicorn-party', 800),
}

def build():
    n = 0
    for p in glob.glob(OUT + '/*.html'):
        page = os.path.basename(p); s0 = s = open(p).read()
        if page in HEROES:
            src, pos = HEROES[page]
            s = re.sub(r'(<header class="phero[^"]*"><img src=")[^"]+("[^>]*?style="object-position:)[^"]*', lambda m: m.group(1) + src + m.group(2) + pos, s, count=1)
        for old, new in SWAP.items():
            s = re.sub(r'(["\'(])(?:\.\./img/|img/)?' + re.escape(old), lambda m: m.group(1) + new, s)
        if s != s0: open(p, 'w').write(s); n += 1
    print('photo pass:', n, 'pages updated')

if __name__ == '__main__':
    build()
