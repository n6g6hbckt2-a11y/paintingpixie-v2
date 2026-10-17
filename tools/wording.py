# -*- coding: utf-8 -*-
"""Wording changes made since the switch (10 Oct 2026). The builds read each page from the pre-switch live copy
(tools/source.sh) and apply these changes on top, so they survive every rebuild.
Each entry: page -> list of (old text, new text). Every old text must be found, or the build stops."""

BRIGHTON_HENS = '''
<section>
<h2>Adult Face Painting &amp; Hen Parties in Brighton</h2>
<p>
I regularly paint in Brighton &amp; Hove: hen dos, birthdays, festivals and launch events. For a hen party, guests can
choose face paint, glitter and gems, or a mix of both, and I keep the queue moving so nobody misses the fun.
</p>
<p>
Want all-out sparkle? I'm also a <a href="glitter-bar.html">glitter artist with a full glitter bar</a> for hen parties
and festivals across Brighton, Sussex and Surrey.
</p>
</section>
'''

CHANGES = {
    # 10 Oct: ranks ~3rd for "animal print face painting" Surrey/Brighton/Sussex but gets no clicks
    'animal-print-face-painting.html': [
        ('Tiger & Leopard Face Painting in Sussex & Surrey | Painting Pixie', 'Animal Print Face Paint Ideas: 10 Photos | Sussex &amp; Surrey'),   # 17 Oct: was 'Animal Print Face Painting in Sussex, Surrey & Brighton' - top 5 in Google but 0 clicks; searchers want ideas/photos
        ("Tiger, leopard and butterfly face paint for kids' parties, festivals and grown-ups across Sussex & Surrey. 5.0 rated, insured. Parties from £130.",
         "10 animal print face paint ideas with photos: tigers, leopards and a glitter cat. Book any look for parties in Sussex, Surrey & Brighton. 5.0 rated."),
        ('<h1>Animal Print Face Painting in Sussex & Surrey ✨', '<h1>Animal Print Face Painting in Sussex, Surrey & Brighton ✨'),
    ],
    # 11 Oct: the Google reviews widget has dark text, so it sits on a light band instead of the dark pixie-dust background
    'index.html': [
        # 12 Oct: trust strip under the hero made one compact line; Add to Event badge removed here (it is in the hero and the trust band); 40+ reviews
        ('<p style="margin:0; font-weight:bold; font-size:18px;">\n ⭐⭐⭐⭐⭐ <a href="https://www.addtoevent.co.uk/suppliers/the-painting-pixie-ltd" target="_blank" style="color:inherit; text-decoration:underline;">5.0 Rated — 30+ Reviews</a>\n</p>\n<p style="margin:10px 0 6px;"><a class="ate-badge" href="https://www.addtoevent.co.uk/suppliers/the-painting-pixie-ltd" target="_blank" rel="noopener" title="Top rated on Add to Event"><img src="/addtoevent-top-rated.webp" alt="Top rated on Add to Event, 5 stars" width="96" height="92" loading="lazy"></a></p>\n<p style="margin:0; font-weight:bold; font-size:14px;">\n✨ Fully Insured 📍 DBS Checked 🎨 1000+ Faces Painted 💖 Trusted across Sussex & Surrey\n</p>\n',
         '<style>section:has(>.wrap>.tbar){padding:20px 0!important}.tbar{margin:0!important;font-weight:700;font-size:16px;line-height:1.7}.tbar .st{color:#E2BE7A;letter-spacing:1px}.tbar .dot{opacity:.5;margin:0 3px}.tbar .i{white-space:nowrap}@media(max-width:600px){.tbar{font-size:14px}.tbar .dot{margin:0 1px}.tbar .br{display:block;height:0}.tbar .dot.m{display:none}}</style>\n<p class="tbar"><span class="st">★★★★★</span> <a href="https://www.addtoevent.co.uk/suppliers/the-painting-pixie-ltd" target="_blank" rel="noopener" style="color:inherit;text-decoration:underline">5.0 rated, 40+ reviews</a><span class="dot m">·</span><span class="br"></span><span class="i">Fully insured</span> <span class="dot">·</span> <span class="i">DBS checked</span> <span class="dot">·</span> <span class="i">1,000+ faces painted</span></p>\n'),
        ('<div class="elfsight-app-407943df-9174-4398-bc46-40f1499ff351" data-elfsight-app-lazy></div>',
         '<div class="k-greviews" style="background:#FBF5EF;border-radius:18px;padding:26px 18px;max-width:1140px;margin:44px auto;width:calc(100% - 32px);box-sizing:border-box;color:#1B1712"><div class="elfsight-app-407943df-9174-4398-bc46-40f1499ff351" data-elfsight-app-lazy></div></div>'),
    ],
    # 10 Oct: "adult face painters/painting brighton" 13.7-16.1, the adult page's title did not say Brighton
    'adult-face-painting.html': [
        ('Professional Hen Party & Adult Face Painting in Sussex & Surrey', 'Adult & Hen Party Face Painting | Brighton, Sussex & Surrey'),
        ('for hen dos, birthdays, festivals and corporate events across Sussex, Surrey & Brighton. 5.0 rated. From £150.',
         'for hen dos, birthdays, festivals and corporate events in Brighton, Sussex & Surrey. 5.0 rated. From £150.'),
        ('<section class="about">\n<img src="kat-parker-professional-01.jpeg"', BRIGHTON_HENS.lstrip('\n') + '\n<section class="about">\n<img src="kat-parker-professional-01.jpeg"'),
    ],
}

def apply(page, s):
    for old, new in CHANGES.get(page, []):
        if old not in s:
            raise SystemExit(f'wording.py: "{old[:60]}" not found on {page}')
        s = s.replace(old, new)
    return s
