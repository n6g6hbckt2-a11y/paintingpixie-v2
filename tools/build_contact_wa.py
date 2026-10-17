# -*- coding: utf-8 -*-
"""17 Oct: about 33 visits a month land straight on the contact page and leave after ~9 seconds. Put the quickest way
to reach Kat (WhatsApp) at the very top, with the form one tap below. Runs late in the chain (after conversion tweaks)."""
import os, re
OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
WA = ('https://wa.me/447852300125?text=Hi%20Kat!%20I%27d%20like%20to%20check%20a%20date.%0A%F0%9F%93%85%20Date%3A%20'
      '%0A%F0%9F%93%8D%20Town%3A%20%0A%F0%9F%91%A7%20Number%20of%20children%3A%20')
BLOCK = f'''<section class="band band-light cwa-top centred"><div class="wrap">
<h2>Is Kat free on your date?</h2>
<p class="cwa-lede">The quickest way is WhatsApp. Send your date, town and roughly how many children, and Kat usually replies the same day.</p>
<a class="btn btn-wa cwa-btn" href="{WA}" target="_blank" rel="noopener"><svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>WhatsApp Kat</a>
<p class="cwa-alt">Prefer a form? <a href="#cwa-form">Fill in the booking form below ↓</a> · or call <a href="tel:+447852300125">07852 300125</a></p>
<p class="cwa-trust">★★★★★ 5.0 rated · Parties from £130 · Fully insured &amp; DBS checked</p>
</div></section>
'''
CSS = '''<style>
.cwa-top{padding:46px 0 40px}.cwa-top h2{margin:0 0 10px}
.cwa-lede{max-width:620px;margin:0 auto 22px;font-size:18px}
.cwa-btn{font-size:20px;padding:18px 34px;gap:10px;display:inline-flex;align-items:center}
.cwa-alt{margin:18px 0 6px;font-weight:600}.cwa-trust{margin:0;color:#6B6157;font-size:14px;font-weight:700}
</style>
'''
def build():
    p = f'{OUT}/contact.html'
    if not os.path.exists(p): return
    s = open(p).read()
    if 'cwa-top' in s: return
    m = re.search(r'<main class="lg"[^>]*>\s*', s)
    if not m: print('contact WhatsApp: no main'); return
    s = s[:m.end()] + BLOCK + s[m.end():]
    s = re.sub(r'(<!-- FORM -->\s*<div class="card")', r'\1 id="cwa-form"', s, count=1)
    s = s.replace('</head>', CSS + '</head>', 1)
    open(p, 'w').write(s); print('contact page: WhatsApp first')
if __name__ == '__main__':
    build()
