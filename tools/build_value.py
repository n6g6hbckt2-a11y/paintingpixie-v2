# -*- coding: utf-8 -*-
"""17 Oct: higher-value enquiries. (1) The 3-hour Ultimate Sparkle goes first everywhere the two party packages sit side
by side, marked "Most popular" (Kat's own wording on the home page), with a line on why bigger parties need 3 hours
(15 / 25 children: from the town-page FAQs). (2) A preview-only checklist on the corporate & events page for Kat.
Runs late in the chain."""
import os, re, glob
OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
NOTE = '<p class="small-note pnote">More than 15 children? Choose 3 hours: it covers up to 25, so every child gets their turn without rushing.</p>'
CSS = '''
/* 3-hour first (17 Oct) */
.pcard.hi{border:2px solid var(--gold,#E2BE7A);position:relative}
.pcard .pbadge{position:absolute;top:-12px;left:50%;translate:-50% 0;background:var(--gold,#E2BE7A);color:#1B1712;font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;padding:4px 12px;border-radius:999px;white-space:nowrap}
.pnote{margin-top:14px}
'''
CARD = r'<div class="pcard"><h3>{name}</h3>.*?</div></div>'

def three_first(s):
    changed = False
    # card grids on service and town pages
    c = re.search(CARD.format(name='Classic Party'), s, re.S); u = re.search(CARD.format(name='Ultimate Sparkle'), s, re.S)
    if c and u and c.end() == u.start():
        ult = u.group(0).replace('<div class="pcard">', '<div class="pcard hi"><span class="pbadge">Most popular</span>', 1)
        s = s[:c.start()] + ult + c.group(0) + s[u.end():]; changed = True
        grid_end = s.find('</div>', s.find(c.group(0)) + len(c.group(0)))
        m = re.search(r'</div>(?=\s*(?:<div class="incl"|<p class="small-note|</div></section>))', s[s.find(ult):])
        if m and 'pnote' not in s:
            at = s.find(ult) + m.end(); s = s[:at] + NOTE + s[at:]
    # home page package cards
    i1 = s.find('<!-- PACKAGE 1 -->'); i2 = s.find('<!-- PACKAGE 2 (FEATURED) -->'); i3 = s.find('<!-- PACKAGE 3 -->')
    if -1 < i1 < i2 < i3 and 'Classic Party' in s[i1:i2]:
        s = s[:i1] + s[i2:i3] + s[i1:i2] + s[i3:]; changed = True
    # contact page summary and form options
    a = re.search(r'<p><strong>🎈 Classic Party</strong>.*?</p>\s*', s, re.S); b = re.search(r'<p><strong>🌟 Ultimate Sparkle</strong>.*?</p>\s*', s, re.S)
    if a and b and a.end() == b.start():
        s = s[:a.start()] + b.group(0).replace('</strong> –', ' (most popular)</strong> –', 1) + a.group(0) + s[b.end():]; changed = True
    a = re.search(r'<option>🎈 Classic Party \(from £130\)</option>\s*', s); b = re.search(r'<option>🌟 Ultimate Sparkle \(from £160\)</option>\s*', s)
    if a and b and a.end() == b.start():
        s = s[:a.start()] + b.group(0) + a.group(0) + s[b.end():]; changed = True
    return s, changed

def kat_check_corporate(s):
    if os.environ.get('PP_GOLIVE') or 'kat-check' in s: return s
    import xmas_extras as X
    box = X.KAT_CHECK
    box = re.sub(r'<ol>.*</ol>', '<ol>'
                 '<li><b>Extra artists:</b> the page says you can bring extra artists for big events (as the home page does). Is that right, and how many?</li>'
                 '<li><b>Risk assessment:</b> can you supply one for venues on request, as the page says?</li>'
                 '<li><b>Event organiser reviews:</b> any reviews from schools, companies, festivals or venues we can quote word for word?</li>'
                 '<li><b>Past events to name:</b> any companies, festivals or venues you’re happy for us to list (e.g. Eats &amp; Beats, Guildford Festival of the Arts)?</li>'
                 '<li><b>Photos:</b> any event photos (queues, glitter bar, brand colours) we can use?</li>'
                 '</ol>', box, flags=re.S)
    return re.sub(r'(<main class="lg"[^>]*>\s*)', lambda m: m.group(1) + '<section class="band band-light"><div class="wrap">' + box + '</div></section>\n', s, count=1)

def build():
    n = 0
    for p in glob.glob(OUT + '/*.html'):
        s = open(p).read(); s2, ch = three_first(s)
        if os.path.basename(p) == 'corporate-events.html': s2 = kat_check_corporate(s2)
        if os.path.basename(p) == 'index.html' and 'corporate-events.html' not in os.environ.get('PP_HOLD', 'corporate-events.html'):
            s2 = re.sub(r'(Festivals, Corporate &amp; Community Events</h3>.*?)<a href="contact.html" class="btn btn-ghost">Check my date</a>',
                        r'\1<a href="corporate-events.html" class="btn btn-ghost">Corporate &amp; events</a>', s2, count=1, flags=re.S)
            s2 = re.sub(r'(Festivals, Corporate & Community Events</h3>.*?)<a href="contact.html" class="btn btn-ghost">Check my date</a>',
                        r'\1<a href="corporate-events.html" class="btn btn-ghost">Corporate &amp; events</a>', s2, count=1, flags=re.S)
        if s2 != s: open(p, 'w').write(s2); n += 1
    cp = f'{OUT}/site.css'; c = open(cp).read()
    if '/* 3-hour first' not in c: open(cp, 'a').write(CSS)
    print('3-hour first on', n, 'pages')
if __name__ == '__main__':
    build()
