# -*- coding: utf-8 -*-
"""Turn switch/ (the preview of the switch) into golive/: the exact files to copy into the live repo.
- image/script paths changed from the preview layout (../img/...) to the live layout (img/...)
- preview-only lines removed (noindex, draft notes); canonical links made absolute again
- redirect pages copied from live unchanged; every asset the pages use is copied in
- sitemap.xml updated with the new pages
golive/ is built locally only and never pushed to the preview site (it has no noindex)."""
import os, re, shutil, glob, html

V2 = '/home/claude/paintingpixie-v2'
LIVE = '/home/claude/Painting-Pixie'
SRC = V2 + '/switch'
DST = V2 + '/golive'
SITE = 'https://paintingpixie.com/'
NEW_PAGES = ['prices.html', 'reviews.html', 'workshops.html', 'corporate-events.html', 'christmas-face-painting.html']

def fix(s, page):
    s = s.replace('../img/', 'img/').replace('../vendor/', 'vendor/').replace('../hw/', '')
    s = re.sub(r'\s*<!-- DRAFT ONLY:[^>]*-->', '', s)
    s = re.sub(r'\s*<!-- PREVIEW ONLY:[^>]*-->', '', s)
    s = re.sub(r'\s*<meta name="robots" content="noindex[^"]*">', '', s)
    s = re.sub(r'<p class="draft-note">.*?</p>\s*', '', s, flags=re.S)
    s = re.sub(r'(<link rel="canonical" href=")(?!https?:)([^"]*)"', lambda m: m.group(1) + SITE + ('' if m.group(2) in ('', 'index.html') else m.group(2)) + '"', s)
    s = re.sub(r'(<meta property="og:url" content=")(?!https?:)([^"]*)"', lambda m: m.group(1) + SITE + m.group(2) + '"', s)
    return s

ASSET = re.compile(r'''(?:src|href|data-full|poster)="([^"#?:]+?\.(?:webp|jpe?g|png|svg|gif|ico|mp4|css|js))"|url\(["']?([^"')#?:]+?\.(?:webp|jpe?g|png|svg|gif))["']?\)''', re.I)

def assets_in(text):
    return {a or b for a, b in ASSET.findall(text)}

def find_source(rel):
    """Where to copy an asset from: the switch build, the preview repo, or the live repo."""
    for base in (SRC, V2, LIVE):
        for cand in (rel, rel.replace('img/', '', 1) if base == LIVE else None):
            if cand and os.path.isfile(os.path.join(base, cand)): return os.path.join(base, cand)
    return None

def build():
    if os.path.exists(DST): shutil.rmtree(DST)
    os.makedirs(DST)
    pages, missing, copied = [], [], 0
    for p in sorted(glob.glob(SRC + '/*.html')):
        page = os.path.basename(p)
        if page.startswith('design-ideas'): continue
        s = open(p).read()
        if 'http-equiv="refresh"' in s:   # redirect stubs: keep the live file exactly
            if os.path.exists(f'{LIVE}/{page}'): shutil.copy(f'{LIVE}/{page}', f'{DST}/{page}')
            continue
        s = fix(s, page)
        open(f'{DST}/{page}', 'w').write(s); pages.append(page)
    for name in ('site.css', 'site.js'):
        t = fix(open(f'{SRC}/{name}').read(), name)
        open(f'{DST}/{name}', 'w').write(t)
    # copy every asset referenced by the pages, site.css and site.js (and assets used inside SVGs/CSS they pull in)
    todo = set()
    for f in glob.glob(DST + '/*.html') + [DST + '/site.css', DST + '/site.js']:
        todo |= assets_in(open(f).read())
    done = set()
    while todo:
        rel = todo.pop()
        if rel in done or rel.startswith('http'): continue
        done.add(rel)
        if rel in ('site.css', 'site.js'): continue
        src = find_source(rel)
        if not src: missing.append(rel); continue
        out = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copy(src, out); copied += 1
        if rel.endswith(('.css', '.svg')):
            todo |= {os.path.normpath(os.path.join(os.path.dirname(rel), a)) for a in assets_in(open(src, errors='ignore').read())}
    # leaflet ships its marker images next to its css
    if os.path.isdir(V2 + '/vendor'):
        shutil.copytree(V2 + '/vendor', DST + '/vendor', dirs_exist_ok=True)
    # sitemap: live sitemap plus the new pages
    sm = open(f'{LIVE}/sitemap.xml').read()
    if f'<loc>{SITE}</loc>' not in sm:   # the homepage was missing from the live sitemap
        sm = sm.replace('<url>', f'<url>\n    <loc>{SITE}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>\n  <url>', 1)
    for page in NEW_PAGES:
        if os.path.exists(f'{DST}/{page}') and f'{SITE}{page}<' not in sm:
            sm = sm.replace('</urlset>', f'  <url>\n    <loc>{SITE}{page}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n</urlset>')
    open(f'{DST}/sitemap.xml', 'w').write(sm)
    print(f'golive: {len(pages)} pages, {copied} assets copied, {len(missing)} missing')
    for m in missing: print('  missing asset:', m)

if __name__ == '__main__':
    build()
