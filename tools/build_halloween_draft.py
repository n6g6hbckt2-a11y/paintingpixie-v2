# -*- coding: utf-8 -*-
"""Put the live Halloween page (designed in hw/) into the draft site, with links pointing at the draft pages.
Runs last, so it replaces the older draft Halloween page."""
import re
V2 = '/home/claude/paintingpixie-v2'
HW_CSS = '''<style id="ddcss">
.hwnav{display:flex;align-items:center;gap:22px}
.hwnav .dd{position:relative}
.hwnav .navhome{display:inline-flex;align-items:center;gap:6px;padding:7px 12px;border:1.5px solid rgba(255,255,255,.5);border-radius:999px}
.hwnav .navhome:hover{color:#FFB020;border-color:#FFB020}
.hwmenu a.mhome{display:flex;align-items:center;gap:8px;color:#FFB020}
.hwnav .ddtop{display:inline-flex;align-items:center;gap:6px;padding:10px 0}
.hwnav .ddtop svg{transition:transform .2s}
.hwnav .dd:hover .ddtop,.hwnav .dd:focus-within .ddtop{color:#FFB020}
.hwnav .dd:hover .ddtop svg,.hwnav .dd:focus-within .ddtop svg{transform:rotate(180deg)}
.hwnav .ddpanel{display:none;position:absolute;top:100%;left:-18px;min-width:240px;padding:10px;background:rgba(20,10,30,.97);border:1px solid rgba(255,255,255,.18);border-radius:14px;box-shadow:0 24px 50px rgba(0,0,0,.6);z-index:30}
.hwnav .ddpanel::before{content:"";position:absolute;left:0;right:0;top:-12px;height:12px}
.hwnav .dd:hover .ddpanel,.hwnav .dd:focus-within .ddpanel{display:block}
.hwnav .ddpanel a{display:block;padding:8px 12px;border-radius:8px;font:600 15px var(--body);letter-spacing:0;text-transform:none;white-space:nowrap}
.hwnav .ddpanel a:hover{background:rgba(255,255,255,.08);color:#FFB020}
.hwnav .ddpanel a.ddall{color:#FFB020;border-top:1px solid rgba(255,255,255,.18);margin-top:6px}
.hwnav .dd.wide .ddpanel{left:-160px}
.hwnav .ddcols{display:grid;grid-template-columns:1fr 1fr;gap:4px 18px}
.hwnav .ddh{margin:4px 12px;font:800 11.5px var(--body);letter-spacing:.12em;text-transform:uppercase;color:#7CF0C8}
.hwnav .dd:last-of-type .ddpanel{left:auto;right:-18px}
.hwmenu{display:none;position:relative}
.hwmenu summary{list-style:none;cursor:pointer;border:1.5px solid rgba(255,255,255,.6);border-radius:999px;padding:9px 16px;font-weight:800;color:#fff}
.hwmenu summary::-webkit-details-marker{display:none}
.hwmenu .mobmenu{position:absolute;right:0;top:50px;background:rgba(20,10,30,.98);border:1px solid rgba(255,255,255,.18);border-radius:14px;padding:10px 14px;min-width:270px;max-height:75vh;overflow:auto;z-index:30;box-shadow:0 20px 40px rgba(0,0,0,.6)}
.hwmenu a{color:#fff;text-decoration:none}
.hwmenu .msec{border-bottom:1px solid rgba(255,255,255,.15)}
.hwmenu .mrow{display:flex;align-items:center;justify-content:space-between}
.hwmenu a.mtop{flex:1;display:block;padding:14px 4px;font-weight:800}
.hwmenu .marr{background:none;border:1px solid rgba(255,255,255,.25);color:#FFB020;border-radius:10px;width:42px;height:38px;display:grid;place-items:center}
.hwmenu .marr[aria-expanded="true"] svg{transform:rotate(180deg)}
.hwmenu .msub{padding:0 0 10px 10px}.hwmenu .msub a{display:block;padding:8px 10px;font-weight:600}
.hwmenu .mh{margin:8px 10px 2px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#7CF0C8}
.hwmenu .btn{display:block;text-align:center;margin-top:12px}
@media(max-width:980px){.hwnav{display:none}.hwmenu{display:block}}
</style>'''
HW_JS = '''<script>[].forEach.call(document.querySelectorAll('.marr'),function(b){b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!o));b.closest('.msec').querySelector('.msub').hidden=o;});});</script>'''
s = open(V2 + '/hw/halloween-face-painting.html').read()
s = s.replace('href="https://paintingpixie.com/"', 'href="index.html"')
s = re.sub(r'href="https://paintingpixie.com/([a-z0-9-]+\.html)"', r'href="\1"', s)
s = re.sub(r'src="((?:halloween-|logo-lg|addtoevent)[^"]*)"', r'src="../hw/\1"', s)
s = re.sub(r'url\("(halloween-[^"]+\.svg)"\)', r'url("../hw/\1")', s)
s = s.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"', 1)
OUT = __import__('os').environ.get('PP_OUT', V2 + '/draft')
idx = open(OUT + '/index.html').read()
desk = re.search(r'<div class="links">.*?</div>\n(?=<details class="menu">)', idx, re.S).group(0)
mob = re.search(r'<details class="menu">.*?</details>', idx, re.S).group(0)
desk = desk.replace('class="btn btn-gold"', 'class="btn btn-orange"').replace('<div class="links">', '<nav class="links hwnav" aria-label="Main">').rstrip()[:-6] + '</nav>'
mob = mob.replace('class="btn btn-gold"', 'class="btn btn-orange"').replace('class="menu"', 'class="menu hwmenu"')
s = re.sub(r'<nav class="links" aria-label="Main">.*?</nav>', lambda m: desk + mob, s, count=1, flags=re.S)
s = s.replace('</head>', HW_CSS + '\n</head>', 1)
s = s.replace('</body>', HW_JS + '\n</body>', 1)
cols = re.search(r'<footer><div class="wrap">\s*<div class="cols">(.*?)</div>\s*<p class="legal">', idx, re.S).group(1)
links = ''.join(re.findall(r'<a href="[^"]+">[^<]+</a>', re.sub(r'<div><h4>The Painting Pixie</h4>.*?</div>', '', cols, count=1, flags=re.S)))
s = re.sub(r'<div class="flinks">.*?</div>', '<div class="flinks">' + links + '</div>', s, count=1, flags=re.S)
open(OUT + '/halloween-face-painting.html', 'w').write(s)
print('draft Halloween page = live Halloween page')
