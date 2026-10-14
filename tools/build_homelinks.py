# -*- coding: utf-8 -*-
"""14 Oct (Ahrefs site audit): every internal link pointed at "index.html", so the real home page address
(https://paintingpixie.com/) had no internal links pointing to it (Google and Ahrefs treat /index.html as a separate
address). Links to the home page now use "./" (and "./#prices" etc.). Runs just before build_version."""
import glob, os, re
OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
PAT = re.compile(r'href="index\.html(#[^"]*)?"')
def fix(s): return PAT.sub(lambda m: f'href="./{m.group(1) or ""}"', s)
def build():
    n = 0
    for p in glob.glob(OUT + '/*.html'):
        s = open(p).read(); t = fix(s)
        if t != s: open(p, 'w').write(t); n += 1
    print('home page links use ./ on', n, 'pages')
if __name__ == '__main__':
    build()
