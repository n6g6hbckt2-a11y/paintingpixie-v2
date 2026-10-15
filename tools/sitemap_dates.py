# -*- coding: utf-8 -*-
"""15 Oct: every sitemap entry gets a <lastmod> date (Bing leans on these to decide what to recrawl).
Run inside the live repo just before committing a go-live: a page staged in this change gets today's date,
any other page the date of the last commit that changed it. Usage: python3 sitemap_dates.py [repo]"""
import datetime, os, re, subprocess, sys
repo = sys.argv[1] if len(sys.argv) > 1 else '.'
os.chdir(repo)
staged = set(subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True).stdout.split())
today = datetime.date.today().isoformat()
def date_of(f):
    if f in staged: return today
    d = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', f], capture_output=True, text=True).stdout.strip()
    return d or today
sm = open('sitemap.xml').read()
def fix(m):
    block = m.group(0); loc = re.search(r'<loc>https://paintingpixie\.com/([^<]*)</loc>', block)
    if not loc: return block
    f = loc.group(1) or 'index.html'
    if not os.path.exists(f): return block
    block = re.sub(r'\s*<lastmod>[^<]*</lastmod>', '', block)
    return block.replace('</loc>', f'</loc>\n    <lastmod>{date_of(f)}</lastmod>', 1)
new = re.sub(r'<url>.*?</url>', fix, sm, flags=re.S)
if new != sm: open('sitemap.xml', 'w').write(new)
print('sitemap dates:', len(re.findall('<lastmod>', new)), 'entries')
