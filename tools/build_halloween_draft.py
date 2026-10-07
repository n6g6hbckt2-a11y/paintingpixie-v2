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
s = re.sub(r'<nav class="links" aria-label="Main">.*?</nav>',
  '<nav class="links" aria-label="Main"><a href="services.html">Services</a><a href="areas.html">Areas</a><a href="about.html">About</a>'
  '<a href="gallery.html">Gallery</a><a href="prices.html">Prices</a><a class="btn btn-orange" href="contact.html">Check my date</a></nav>', s, count=1, flags=re.S)
idx = open(V2 + '/draft/index.html').read()
cols = re.search(r'<footer><div class="wrap">\s*<div class="cols">(.*?)</div>\s*<p class="legal">', idx, re.S).group(1)
links = ''.join(re.findall(r'<a href="[^"]+">[^<]+</a>', re.sub(r'<div><h4>The Painting Pixie</h4>.*?</div>', '', cols, count=1, flags=re.S)))
s = re.sub(r'<div class="flinks">.*?</div>', '<div class="flinks">' + links + '</div>', s, count=1, flags=re.S)
open(V2 + '/draft/halloween-face-painting.html', 'w').write(s)
print('draft Halloween page = live Halloween page')
