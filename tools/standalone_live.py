# -*- coding: utf-8 -*-
"""Put single new-design pages on the CURRENT live site, ahead of the full switch.
Takes the page from golive/ (run package_golive.py first), removes links to pages the live site
doesn't have yet, and copies the page plus every asset it uses into the live repo.
Usage: python3 tools/standalone_live.py reviews.html [more pages]"""
import os, re, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from package_golive import assets_in, DST as GOLIVE, LIVE

def fix_links(s, publishing=()):
    live = lambda page: page in publishing or os.path.exists(f'{LIVE}/{page}')
    # menu items for pages that only arrive with the switch
    for page in ('christmas-face-painting.html', 'workshops.html', 'corporate-events.html', 'prices.html'):
        if not live(page):
            s = re.sub(rf'<a href="{page}">[^<]*</a>', '', s)
    # the live homepage has no FAQ section yet
    s = re.sub(r'<a href="index.html#faq">[^<]*</a>', '', s)
    # Christmas banner (shows from 1 Nov): no Christmas page on live yet, so send people to the enquiry form
    if not live('christmas-face-painting.html'):
        s = re.sub(r'(<a class="seasonbar" data-from="11-01"[^>]*href=")christmas-face-painting.html(")', r'\1contact.html\2', s)
        s = s.replace('See the festive designs →', 'Check my date →')
    return s

def main(pages):
    todo = set()
    for page in pages:
        s = fix_links(open(f'{GOLIVE}/{page}').read(), pages)
        left = [h for h in re.findall(r'href="([^"#:]+\.html)', s) if not os.path.exists(f'{LIVE}/{h}') and h not in pages]
        if left: sys.exit(f'{page}: still links to pages not on live: {sorted(set(left))}')
        open(f'{LIVE}/{page}', 'w').write(s)
        todo |= assets_in(s)
    for name in ('site.css', 'site.js'):
        shutil.copy(f'{GOLIVE}/{name}', f'{LIVE}/{name}')
        todo |= assets_in(open(f'{GOLIVE}/{name}').read())
    done, n = set(), 0
    while todo:
        rel = todo.pop()
        if rel in done or rel.startswith(('http', '/')) or rel in ('site.css', 'site.js'): continue
        done.add(rel)
        src = f'{GOLIVE}/{rel}'
        if not os.path.isfile(src): print('  missing asset:', rel); continue
        out = f'{LIVE}/{rel}'
        os.makedirs(os.path.dirname(out) or LIVE, exist_ok=True)
        if not os.path.exists(out) or open(out, 'rb').read() != open(src, 'rb').read():
            shutil.copy(src, out); n += 1
        if rel.endswith(('.css', '.svg')):
            todo |= {os.path.normpath(os.path.join(os.path.dirname(rel), a)) for a in assets_in(open(src, errors='ignore').read())}
    print(f'standalone: {", ".join(pages)} copied to live with {n} new/changed assets')

if __name__ == '__main__':
    main(sys.argv[1:] or ['reviews.html'])
