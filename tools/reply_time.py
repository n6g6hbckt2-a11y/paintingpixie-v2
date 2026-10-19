# -*- coding: utf-8 -*-
"""19 Oct (Phil): Kat's reply promise is now "will try to reply within 4 hours" everywhere, instead of "usually the same day".
Applied to every built page (last step of the build) and, run with a folder, to the live site's pages."""
import os, re, sys, glob

SWAPS = [
    ('Kat checks her diary and replies with availability and the best option for your party, usually the same day.',
     'Kat checks her diary and will try to reply within 4 hours with availability and the best option for your party.'),
    ('and Kat usually replies the same day.', 'and Kat will try to reply within 4 hours.'),
    ('Kat usually replies the same day.', 'Kat will try to reply within 4 hours.'),
    ('She usually replies the same day.', 'She will try to reply within 4 hours.'),
    ('I usually reply the same day.', 'I’ll try to reply within 4 hours.'),
    ("I'll usually reply the same day", "I'll try to reply within 4 hours"),
    ("Message Kat and she'll get back to you, usually the same day.", "Message Kat and she'll try to get back to you within 4 hours."),
    ('Kat will check her diary, usually the same day.', 'Kat will check her diary and try to reply within 4 hours.'),
    ('Usually the same day. Message me with the date', 'I try to reply within 4 hours. Message me with the date'),
    ("Fill this in and I'll get back to you as soon as possible (usually same day).", "Fill this in and I'll try to get back to you within 4 hours."),
    ("Fill this in and I'll get back to you as soon as possible (usually same day)", "Fill this in and I'll try to get back to you within 4 hours"),
]

def apply(s):
    for a, b in SWAPS:
        s = s.replace(a, b)
        s = s.replace(a.replace("'", '&#39;'), b.replace("'", '&#39;')).replace(a.replace("'", '’'), b.replace("'", '’'))
    return s

def run(folder):
    n = 0
    for p in glob.glob(folder + '/**/*.html', recursive=True):
        s = open(p).read(); t = apply(s)
        if t != s: open(p, 'w').write(t); n += 1
    left = [p for p in glob.glob(folder + '/**/*.html', recursive=True) if re.search(r'same[- ]day', open(p).read(), re.I)]
    print('reply time (4 hours) on', n, 'pages' + (f'; still says same day: {left}' if left else ''))

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft'))
