# -*- coding: utf-8 -*-
"""14 Oct: the menu's "FAQs" link goes to index.html#faq, but the live home page (pre-switch wording) has no FAQ section,
so it landed nowhere. Adds a short FAQ to the home page, before the enquiry box. Facts only from the site / Kat's rules.
The draft home page has its own FAQ, so this only acts when there is no id="faq". Runs after build_animal."""
import os, re
OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
FAQS = [
    ("Where do you travel to?",
     'Kat is based in Horsham and paints across West Sussex, East Sussex, Brighton and Surrey, including Crawley, Haywards Heath, '
     'Worthing, Guildford, Reigate and Dorking. Bigger events further afield are welcome too. <a href="areas.html">See every area on the map</a>.'),
    ("How much does it cost?",
     'Children’s parties start at £130 for 2 hours (Classic Party) or £160 for 3 hours with glitter and gems (Ultimate Sparkle). '
     'Hen parties and adult celebrations start at £150. Weddings, festivals and corporate events are quoted individually.'),
    ("How long should I book Kat for?",
     'Tell Kat roughly how many guests you are expecting and she will suggest the right length: the Classic Party is 2 hours and the Ultimate Sparkle is 3 hours.'),
    ("What do I need to provide?",
     'Nothing special. Kat brings all her own equipment, including her table and paints, and sets up and packs away within your booking. '
     'Just let her know where you’d like her to set up.'),
    ("How long does the face paint take to dry?",
     'Only a minute or so. The paints are water-based, so they dry quickly. Ask children not to touch or rub their face for the first minute while it sets.'),
    ("How do I remove the face paint afterwards?",
     'Warm water and a little soap or gentle face wash, or baby wipes, will take it off. Rub gently rather than scrubbing. '
     'For glitter, wipe it away first, then wash.'),
    ("Are the paints safe for children’s skin?",
     'Yes. Kat uses professional, skin-safe face paints and bio-glitter. If a child has sensitive skin, a small patch test on the arm is a good idea.'),
    ("Do you paint adults and hen parties?",
     'Yes. Hen parties and adult celebrations start from £150, with glitter, gems and grown-up designs. See <a href="adult-face-painting.html">adult face painting</a> '
     'and the <a href="glitter-bar.html">glitter bar</a>.'),
    ("How far ahead should I book?",
     'Weekend dates often book several weeks in advance, and Halloween and Christmas go first. A deposit secures your date.'),
    ("Are you insured and DBS checked?", 'Yes. Kat is fully insured and DBS checked.'),
]
def build():
    p = f'{OUT}/index.html'
    if not os.path.exists(p): return
    s = open(p).read()
    if 'id="faq"' in s: print('home FAQ: already there'); return
    items = ''.join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQS))
    sec = ('<section class="band band-dark faq" id="faq"><div class="wrap" style="max-width:900px">'
           '<p class="eyebrow">Good to know</p><h2>Questions parents ask</h2>' + items + '</div></section>\n')
    m = re.search(r'<section class="band band-panel k-enquire', s)
    if not m: print('home FAQ: no place'); return
    open(p, 'w').write(s[:m.start()] + sec + s[m.start():]); print('home FAQ added')
if __name__ == '__main__':
    build()
