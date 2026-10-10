# -*- coding: utf-8 -*-
"""Last step in both pipelines: add a version to the site.css / site.js links (site.css?v=1a2b3c4d), so phones and
iPads load the new files straight after a change instead of an old saved copy."""
import os, glob, hashlib, re
OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')

def build():
    v = {n: hashlib.md5(open(f'{OUT}/{n}', 'rb').read()).hexdigest()[:8] for n in ('site.css', 'site.js')}
    n = 0
    for p in glob.glob(OUT + '/*.html'):
        s0 = s = open(p).read()
        for name, h in v.items():
            s = re.sub(rf'(["\']){re.escape(name)}(?:\?v=\w+)?(["\'])', rf'\g<1>{name}?v={h}\g<2>', s)
        if s != s0: open(p, 'w').write(s); n += 1
    print('file versions on', n, 'pages:', v)

if __name__ == '__main__':
    build()
