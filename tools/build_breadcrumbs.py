# -*- coding: utf-8 -*-
"""Breadcrumbs: link 'Services' and 'Areas' in the page crumb, and add BreadcrumbList data Google can read."""
import glob, json, os, re, html
OUT = __import__('os').environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
SITE = 'https://paintingpixie.com/'
LINKS = {'Services': 'services.html', 'Areas': 'areas.html'}

def build():
    n = 0
    for p in glob.glob(OUT + '/*.html'):
        page = os.path.basename(p)
        s = open(p).read()
        m = re.search(r'<p class="crumb">(.*?)</p>', s, re.S)
        if not m or page.startswith('design-ideas'): continue
        inner = m.group(1)
        parts = [x.strip() for x in inner.split('·')]
        new_parts = []
        for i, x in enumerate(parts):
            plain = re.sub(r'<[^>]+>', '', x).strip()
            if '<a ' not in x and plain in LINKS and LINKS[plain] != page and i < len(parts) - 1:
                x = f'<a href="{LINKS[plain]}">{plain}</a>'
            new_parts.append(x)
        crumb = ' · '.join(new_parts)
        s = s.replace(m.group(0), f'<p class="crumb">{crumb}</p>', 1)
        items, pos = [], 1
        for x in new_parts:
            if '<a ' not in x: continue   # unlinked labels (e.g. 'Kids') are not pages; the page itself is added below
            href = re.search(r'href="([^"]+)"', x)
            name = html.unescape(re.sub(r'<[^>]+>', '', x).strip())
            url = SITE + ('' if href and href.group(1) == 'index.html' else href.group(1)) if href else SITE + ('' if page == 'index.html' else page)
            items.append({"@type": "ListItem", "position": pos, "name": name, "item": url}); pos += 1
        h1 = re.search(r'<h1>(.*?)</h1>', s, re.S)
        if h1 and items[-1]["item"] != SITE + page:
            items.append({"@type": "ListItem", "position": pos, "name": html.unescape(re.sub(r'<[^>]+>', '', h1.group(1)).strip()), "item": SITE + page})
        data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
        s = re.sub(r'<script type="application/ld\+json" id="crumbs">.*?</script>\s*', '', s, flags=re.S)
        s = s.replace('</head>', '<script type="application/ld+json" id="crumbs">' + json.dumps(data, ensure_ascii=False) + '</script>\n</head>', 1)
        open(p, 'w').write(s); n += 1
    print('breadcrumbs on', n, 'pages')

if __name__ == '__main__':
    build()
