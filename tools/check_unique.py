# -*- coding: utf-8 -*-
"""How different are the town pages from each other? Compares the visible text of every pair of town pages
(5-word phrases, ignoring the shared trust strip and enquiry form). Target: no pair shares more than 20%.
Usage: python3 tools/check_unique.py [draft|switch]"""
import re, sys, itertools, os
sys.path.insert(0, os.path.dirname(__file__))
import locations as L
OUT = sys.argv[1] if len(sys.argv) > 1 else 'draft'
def words(f):
    s = open(f).read(); m = re.search(r'<main[^>]*>(.*)</main>', s, re.S); s = m.group(1) if m else s
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S)
    s = re.sub(r'<section class="band (trustband|band-panel k-enquire).*?</section>', '', s, flags=re.S)
    return re.findall(r"[a-z']+", re.sub(r'&[a-z#0-9]+;', ' ', re.sub(r'<[^>]+>', ' ', s)).lower())
sh = lambda w: {' '.join(w[i:i + 5]) for i in range(len(w) - 4)}
S = {p: sh(words(f'{OUT}/{p}')) for p in L.PAGES if os.path.exists(f'{OUT}/{p}')}
pairs = sorted(((len(S[a] & S[b]) / len(S[a] | S[b]), a, b) for a, b in itertools.combinations(S, 2)), reverse=True)
for v, a, b in pairs[:10]: print(f'{v:4.0%}  {a[13:-5]} ~ {b[13:-5]}{"   <-- over 20%" if v > .2 else ""}')
print('average %.0f%%, pairs over 20%%: %d' % (100 * sum(v for v, *_ in pairs) / len(pairs), sum(v > .2 for v, *_ in pairs)))
