# -*- coding: utf-8 -*-
"""Seasonal banner at the top of every page. Bright, so it stands out against the dark site.
Change SEASON to switch the banner (e.g. to Christmas from 1 November)."""
import glob, os, re

OUT = '/home/claude/paintingpixie-v2/draft'

SEASON = dict(
    href='halloween-face-painting.html',
    icon='🎃',
    text='Now booking Halloween parties',
    cta='See the spooky designs',
    css_bg='linear-gradient(90deg,#FF7A1A 0%,#FFB020 30%,#FF7A1A 55%,#B83CFF 100%)',
    ink='#1A0B24',
)

CSS = '''<style id="seasoncss">
.seasonbar{position:relative;z-index:6;display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;
  padding:11px 16px;text-decoration:none;text-align:center;color:%(ink)s;background:%(css_bg)s;background-size:200%% 100%%;
  font:800 15.5px/1.3 Manrope,system-ui,sans-serif;letter-spacing:.01em;box-shadow:0 4px 18px rgba(255,122,26,.45);animation:seasonslide 9s ease-in-out infinite alternate}
.seasonbar .si{font-size:20px;line-height:1;display:inline-block;animation:seasonbob 2.4s ease-in-out infinite}
.seasonbar .sc{display:inline-flex;align-items:center;gap:6px;background:%(ink)s;color:#FFD27A;padding:6px 14px;border-radius:999px;font-size:14px}
.seasonbar:hover .sc{background:#000;color:#fff}
.seasonbar:focus-visible{outline:3px solid #fff;outline-offset:-3px}
@keyframes seasonslide{to{background-position:100%% 0}}
@keyframes seasonbob{50%%{transform:translateY(-3px) rotate(-8deg)}}
@media(max-width:600px){.seasonbar{font-size:14px;padding:9px 12px;gap:8px}.seasonbar .sc{padding:5px 11px;font-size:13px}}
@media(prefers-reduced-motion:reduce){.seasonbar,.seasonbar .si{animation:none}}
</style>''' % SEASON

def bar():
    return (f'<a class="seasonbar" href="{SEASON["href"]}"><span class="si" aria-hidden="true">{SEASON["icon"]}</span>'
            f'<span>{SEASON["text"]}</span><span class="sc">{SEASON["cta"]} →</span></a>')

def build():
    n = 0
    for p in glob.glob(OUT + '/*.html'):
        page = os.path.basename(p)
        if page.startswith('design-ideas') or page == SEASON['href']: continue
        s0 = s = open(p).read()
        if 'http-equiv="refresh"' in s or '<body' not in s: continue
        s = re.sub(r'<a class="season"[^>]*>.*?</a>\s*', '', s, flags=re.S)       # old dark banner (homepage)
        s = re.sub(r'<a class="seasonbar".*?</a>', '', s, flags=re.S)
        s = re.sub(r'<style id="seasoncss">.*?</style>', '', s, flags=re.S)
        s = s.replace('</head>', CSS + '\n</head>', 1)
        s = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + bar(), s, count=1)
        if s != s0: open(p, 'w').write(s); n += 1
    print('season banner on', n, 'pages')

if __name__ == '__main__':
    build()
