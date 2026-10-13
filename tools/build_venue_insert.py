# -*- coding: utf-8 -*-
"""Town pages still in the older layout (not yet rewritten): add the venue guide once at least one venue there has said
yes (flag 'listed' in venues_hire.py). Goes just before the reviews section. Rewritten pages get it from build_locations.
Runs after build_reviewcap in both pipelines (13 Oct 2026)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import venues_hire, build_locations as BL

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')

def build():
    n = 0
    for page in venues_hire.HIRE:
        p = f'{OUT}/{page}'
        if not os.path.exists(p): continue
        s = open(p).read()
        if 'locpage' in s or 'loc-hire' in s: continue          # rewritten page: already has it
        blk = BL.b_hire({'_page': page}, 'dark')
        if not blk: continue
        css = '<style>' + venues_hire.CSS + '.loc-hire .lede-s{margin-top:-6px}</style>'
        m = re.search(r'<section class="band [^"]*k-reviews', s)
        if not m: print('venue guide: no place on', page); continue
        s = s[:m.start()] + blk + '\n' + s[m.start():]
        s = s.replace('</head>', css + '\n</head>', 1)
        open(p, 'w').write(s); n += 1
    print('venue guide added to', n, 'older town pages')

if __name__ == '__main__':
    build()
