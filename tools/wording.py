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
        ('Tiger & Leopard Face Painting in Sussex & Surrey | Painting Pixie', 'Animal Print Face Painting in Sussex, Surrey & Brighton'),
        ("Tiger, leopard and butterfly face paint for kids' parties, festivals and grown-ups across Sussex & Surrey. 5.0 rated, insured. Parties from £130.",
         "Tiger, leopard and butterfly face painting for parties, festivals and events in Sussex, Surrey & Brighton. See the designs and check your date. 5.0 rated."),
        ('<h1>Animal Print Face Painting in Sussex & Surrey ✨', '<h1>Animal Print Face Painting in Sussex, Surrey & Brighton ✨'),
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
