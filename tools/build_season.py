# -*- coding: utf-8 -*-
"""Seasonal banner at the top of every page. Bright, so it stands out against the dark site.
Change SEASON to switch the banner (e.g. to Christmas from 1 November)."""
import glob, os, re

OUT = __import__('os').environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')

import datetime
HALLOWEEN = dict(
    href='halloween-face-painting.html',
    icon='🎃',
    text='Now booking Halloween parties',
    cta='See the spooky designs',
    css_bg='linear-gradient(90deg,#FF7A1A 0%,#FFB020 30%,#FF7A1A 55%,#B83CFF 100%)',
    ink='#1A0B24',
)
CHRISTMAS = dict(
    href='christmas-face-painting.html',
    icon='🎄',
    text='Now booking Christmas parties',
    cta='See the festive designs',
    css_bg='linear-gradient(90deg,#C8102E 0%,#E8344B 35%,#1E8A4C 70%,#C8102E 100%)',
    ink='#FFFFFF',
)
# Both banners are in every page; a one-line script shows the right one for today's date, so the live site
# changes over by itself: Halloween 1 Sep - 31 Oct, Christmas 1 Nov - 24 Dec, no banner otherwise.
SEASONS = [(HALLOWEEN, '09-01', '10-31', '#1A0B24', '#FFD27A'), (CHRISTMAS, '11-01', '12-24', '#1B1712', '#FFFFFF')]

CSS = '''<style id="seasoncss">
.seasonbar{display:none;position:relative;z-index:6;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;
  padding:11px 16px;text-decoration:none;text-align:center;color:var(--sink);background:var(--sbg);background-size:200% 100%;
  font:800 15.5px/1.3 Manrope,system-ui,sans-serif;letter-spacing:.01em;box-shadow:0 4px 18px rgba(0,0,0,.35);animation:seasonslide 9s ease-in-out infinite alternate}
.seasonbar.on{display:flex}
.seasonbar .si{font-size:20px;line-height:1;display:inline-block;animation:seasonbob 2.4s ease-in-out infinite}
.seasonbar .sc{display:inline-flex;align-items:center;gap:6px;background:var(--scbg);color:var(--scink);padding:6px 14px;border-radius:999px;font-size:14px}
.seasonbar:hover .sc{background:#000;color:#fff}
.seasonbar:focus-visible{outline:3px solid #fff;outline-offset:-3px}
@keyframes seasonslide{to{background-position:100% 0}}
@keyframes seasonbob{50%{transform:translateY(-3px) rotate(-8deg)}}
@media(max-width:600px){.seasonbar{font-size:14px;padding:9px 12px;gap:8px}.seasonbar .sc{padding:5px 11px;font-size:13px}}
@media(prefers-reduced-motion:reduce){.seasonbar,.seasonbar .si{animation:none}}
</style>'''

def bar(page):
    out = ''
    for S, a, b, scbg, scink in SEASONS:
        if S['href'] == page: continue
        out += (f'<a class="seasonbar" data-from="{a}" data-to="{b}" href="{S["href"]}" style="--sbg:{S["css_bg"]};--sink:{S["ink"]};--scbg:{scbg};--scink:{scink}">'
                f'<span class="si" aria-hidden="true">{S["icon"]}</span><span>{S["text"]}</span><span class="sc">{S["cta"]} →</span></a>')
    out += ("<script>(function(){var d=new Date(),m=('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2);"
            "[].forEach.call(document.querySelectorAll('.seasonbar'),function(b){if(m>=b.dataset.from&&m<=b.dataset.to)b.classList.add('on')})})();</script>")
    return out

def build():
    n = 0
    for p in glob.glob(OUT + '/*.html'):
        page = os.path.basename(p)
        if page.startswith('design-ideas'): continue
        s0 = s = open(p).read()
        if 'http-equiv="refresh"' in s or '<body' not in s: continue
        s = re.sub(r'<a class="season"[^>]*>.*?</a>\s*', '', s, flags=re.S)       # old dark banner (homepage)
        s = re.sub(r'<a class="seasonbar".*?</a>', '', s, flags=re.S)
        s = re.sub(r"<script>\(function\(\)\{var d=new Date\(\),m=.*?</script>", '', s, flags=re.S)
        s = re.sub(r'<style id="seasoncss">.*?</style>', '', s, flags=re.S)
        s = s.replace('</head>', CSS + '\n</head>', 1)
        s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + bar(page), s, count=1)
        if s != s0: open(p, 'w').write(s); n += 1
    print('season banners (by date) on', n, 'pages')

if __name__ == '__main__':
    build()
