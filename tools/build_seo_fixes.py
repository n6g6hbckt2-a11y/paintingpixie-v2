# -*- coding: utf-8 -*-
"""13 Oct, from the Google AI SEO review: "5.0-rated" in the Google descriptions (the snippet under the blue link),
and a link in the text from the Horsham page to Crawley, Kat's best page for clicks. Runs after build_adult_links."""
import glob, os, re
OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
DESC = [('Insured, DBS-checked face painter', '5.0-rated, insured &amp; DBS-checked face painter'),
        ('Professional, insured &amp; DBS-checked face painters', 'Professional, 5.0-rated, insured &amp; DBS-checked face painters'),
        ('Professional, insured & DBS-checked face painters', 'Professional, 5.0-rated, insured & DBS-checked face painters'),
        ('Professional, insured face painters', 'Professional, 5.0-rated, insured face painters')]
HORSHAM = ('keep the queue moving and the children smiling.',
           'keep the queue moving and the children smiling. I’m also just up the A264 as a <a href="face-painter-crawley.html">face painter in Crawley</a>.')
n = 0
for p in [f'{OUT}/index.html'] + sorted(glob.glob(f'{OUT}/face-painter-*.html')):
    if not os.path.exists(p): continue
    s = open(p).read(); s0 = s
    def fix(m):
        c = m.group(0)
        if '5.0' in c: return c
        for a, b in DESC:
            if a in c: return c.replace(a, b, 1)
        return c
    s = re.sub(r'<meta (?:name|property)="(?:description|og:description|twitter:description)" content="[^"]*"', fix, s)
    if p.endswith('face-painter-horsham.html') and 'face painter in Crawley</a>' not in s:
        s = re.sub(r'keep the queue moving\s+and the children\s+smiling\.', HORSHAM[1], s, count=1)
    if s != s0: open(p, 'w').write(s); n += 1
print('SEO fixes on', n, 'pages')
