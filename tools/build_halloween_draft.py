# -*- coding: utf-8 -*-
"""Put the live Halloween page (designed in hw/) into the draft site, with links pointing at the draft pages.
Runs last, so it replaces the older draft Halloween page."""
import re
V2 = '/home/claude/paintingpixie-v2'
s = open(V2 + '/hw/halloween-face-painting.html').read()
s = s.replace('href="https://paintingpixie.com/"', 'href="index.html"')
s = re.sub(r'href="https://paintingpixie.com/([a-z0-9-]+\.html)"', r'href="\1"', s)
s = re.sub(r'src="((?:halloween-|logo-lg|addtoevent)[^"]*)"', r'src="../hw/\1"', s)
s = re.sub(r'url\("(halloween-[^"]+\.svg)"\)', r'url("../hw/\1")', s)
s = s.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"', 1)
open(V2 + '/draft/halloween-face-painting.html', 'w').write(s)
print('draft Halloween page = live Halloween page')
