# -*- coding: utf-8 -*-
"""Rebuild the draft's location pages from tools/locations.py, each with its own layout.
Run after build_draft.py (it reuses that page's head, nav, footer and mobile bar)."""
import re, os, json, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from locations import PAGES
from postcards import postcard
import inner_layout

OUT = '/home/claude/paintingpixie-v2/draft'
LIVE = '/home/claude/Painting-Pixie'
REVIEWS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'town_reviews.json')))

def esc(t): return html.escape(t, quote=False)
def P(paras): return ''.join(f'<p>{p}</p>' for p in paras)

def band(kind, inner, tone='light', extra=''):
    return f'<section class="band band-{tone} loc-{kind} {extra}"><div class="wrap">{inner}</div></section>'

def town_name(d):
    return d.get('short') or d['eyebrow'].split(',')[0]

def wa_link(town):
    return f"https://wa.me/447852300125?text=Hi%20Kat!%20I'd%20like%20to%20book%20face%20painting%20in%20{town.replace(' ', '%20').replace('&', 'and')}."

# ---------- blocks ----------
def b_letter(d):
    return band('letter', f'''<div class="letter"><p class="eyebrow">A note from Kat</p>{P(d["letter"])}<p class="sig">{d["signoff"]}</p></div>
<blockquote class="pull">“{d["quote"]}”</blockquote>''', 'light')

def b_intro_quote(d, tone='dark'):
    return band('intro', f'<blockquote class="pull big">“{d["quote"]}”<cite>Kat</cite></blockquote><div class="introcols">{P(d["intro"])}</div>', tone)

def b_intro_split(d, tone='light'):
    return band('split', f'''<div class="isplit"><figure class="iphoto"><img src="{d["photo"]}" alt="Face painting by Kat" loading="lazy"></figure>
<div><p class="eyebrow">{esc(d["eyebrow"])}</p>{P(d["intro"])}<blockquote class="pull">“{d["quote"]}”</blockquote></div></div>''', tone)

def b_story(d, tone='light'):
    s = d['story']
    mid = len(s) // 2 + (len(s) % 2)
    return band('story', f'''<div class="story"><p class="eyebrow">{esc(d["eyebrow"])}</p>{P(s[:mid])}
<blockquote class="pull big">“{d["quote"]}”<cite>Kat</cite></blockquote>{P(s[mid:])}</div>''', tone)

def b_postcard(d, slug, town, tone='dark'):
    return f'<section class="band band-{tone} loc-postcard"><div class="wrap">{postcard(slug, town, d["acc"])}</div></section>'

def b_venue_map(d, tone='dark'):
    items = ''.join(f'<li><b>{esc(n)}</b><span>{esc(t)}</span></li>' for n, t in d['venues'])
    return band('map', f'<h2>{esc(d.get("venues_title", "Favourite party spots"))}</h2><ol class="vmap">{items}</ol>', tone)

def b_venue_cards(d, town, tone='dark'):
    items = ''.join(f'<div class="vcard"><b>{esc(n)}</b><span>{esc(t)}</span></div>' for n, t in d['venues'])
    return band('vcards', f'<h2>Party spots I love in {esc(town)}</h2><div class="vcards">{items}</div>', tone)

def b_venue_chips(d, town, tone='light'):
    items = ''.join(f'<details class="chip"><summary>{esc(n)}</summary><span>{esc(t)}</span></details>' for n, t in d['venues'])
    return band('chips', f'<h2>Where {esc(town)} parties happen</h2><p class="lede-s">Tap a place to see why it works.</p><div class="chips">{items}</div>', tone)

def b_events(d, tone='light'):
    items = ''.join(f'<li><span class="when">{esc(w)}</span><b>{esc(n)}</b><p>{esc(t)}</p></li>' for n, w, t in d['events'])
    return band('events', f'<h2>{esc(d.get("events_title", "Where you will find me"))}</h2><ol class="timeline">{items}</ol>', tone)

def b_tiles(d, town, tone='light'):
    cols = ['var(--pink)', 'var(--teal)', 'var(--violet)']
    items = ''.join(f'<div class="wtile" style="--c:{cols[i]}"><span class="wlabel">{esc(t)}</span><p>{esc(x)}</p></div>' for i, (t, x) in enumerate(d['tiles']))
    return band('tiles', f'<h2>A Kat\'s-eye guide to a {esc(town)} party</h2><div class="wtiles">{items}</div>', tone)

def b_seasons(d, town, tone='dark'):
    icons = {'Spring': '✿', 'Summer': '☀', 'Autumn': '❦', 'Winter': '❄'}
    cols = {'Spring': 'var(--lime)', 'Summer': 'var(--gold)', 'Autumn': 'var(--orange)', 'Winter': 'var(--sky)'}
    items = ''.join(f'<div class="season" style="--c:{cols[s]}"><span class="sicon" aria-hidden="true">{icons[s]}</span><b>{s}</b><p>{esc(t)}</p></div>' for s, t in d['seasons'])
    return band('seasons', f'<h2>A year of faces in {esc(town)}</h2><div class="seasons">{items}</div>', tone)

def b_polaroids(d, tone='dark'):
    items = ''.join(f'<figure class="pol"><img src="{img}" alt="" loading="lazy"><figcaption><b>{esc(n)}</b><span>{esc(t)}</span></figcaption></figure>' for n, t, img in d['places'])
    return band('places', f'<h2>{esc(d.get("places_title", "Places I love"))}</h2><div class="pols">{items}</div>', tone)

def b_villages(d, tone='dark'):
    items = ''.join(f'<div class="vill"><b>{esc(n)}</b><p>{esc(t)}</p></div>' for n, t in d['villages'])
    return band('villages', f'<h2>The villages I visit</h2><div class="vills">{items}</div>', tone)

def b_towns(d, tone='dark'):
    items = ''.join(f'<a class="tcard" href="{h}"><b>{esc(n)}</b><span>{esc(t)}</span><i>See the {esc(n)} page →</i></a>' for h, n, t in d['towns'])
    return band('towns', f'<h2>Find your town</h2><div class="tcards">{items}</div>', tone)

def b_gallery(d, tone='dark'):
    imgs = ''.join(f'<img src="{g}" alt="Face painting design by Kat" loading="lazy">' for g in d.get('gallery', []))
    chips = ''.join(f'<span>{esc(x)}</span>' for x in d.get('designs', []))
    return band('gallery', f'<h2>Popular round here</h2><div class="dchips">{chips}</div><div class="gstrip">{imgs}</div>', tone)

def b_hoods(d, town, tone='light'):
    items = ''.join(f'<span>{esc(h)}</span>' for h in d['hoods'])
    head = 'More villages I cover' if town.startswith('the villages') or ',' in town else f'All over {esc(town)} and nearby'
    return band('hoods', f'<h2>{head}</h2><div class="hoods">{items}</div>', tone)

def b_prices(tone='jewel'):
    cards = [("Classic Party", "Up to 15 children, 2 hours", "From £130"), ("Ultimate Sparkle", "Up to 25 children, 3 hours, glitter & gems", "From £160"),
             ("Hens & grown-ups", "Glitter, gems & adult designs", "From £150"), ("Big events", "Weddings, festivals & corporate", "Bespoke quote")]
    inner = ''.join(f'<div class="pcard"><h3>{a}</h3><p>{b}</p><div class="pp">{c}</div></div>' for a, b, c in cards)
    return band('prices', f'<h2>Simple prices</h2><div class="pcards">{inner}</div><p class="small-note">Kat confirms the exact price for your date. A small deposit secures your booking.</p>', tone, 'centred')

def b_reviews(page, town, tone='light'):
    revs = REVIEWS.get(page) or []
    if not revs: return ''
    clean = lambda t: esc(t.strip().strip('"“”'))
    items = ''.join(f'<figure class="testimonial"><p>“{clean(t)}”</p><strong>{esc(n)}</strong></figure>' for t, n in revs)
    return band('reviews', f'<h2>What families say</h2><div class="testimonials">{items}</div>', tone, 'k-reviews')

def b_faq(d, town, tone='dark'):
    items = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in d['faqs'])
    head = 'Your questions' if town.startswith('the ') or ',' in town or '&' in town else f'{esc(town)} questions'
    return band('faq', f'<h2>{head}</h2><div class="faqlist">{items}</div>', tone)

def b_enquire(page, town, title):
    return (f'<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Book face painting in {esc(town)}</h2>'
            f'<p>Tell me your date, where in {esc(town)} and roughly how many guests. I usually reply the same day.</p>'
            f'<a class="btn btn-gold" href="contact.html">Check my date</a><a class="btn btn-wa" href="{wa_link(town)}" target="_blank" rel="noopener">WhatsApp Kat</a>'
            f'{ENQUIRY(page, title)}</div></section>')

# reuse the enquiry form from inner_layout
def ENQUIRY(page, title):
    t = html.escape(re.sub(r'\s*\|.*$', '', title))
    return f"""
<form class="qform" action="https://formspree.io/f/mjgdnged" method="POST">
<p class="draft-note">Draft site: this form is live and sends a real enquiry to Kat.</p>
<input type="hidden" name="_subject" value="Website enquiry: {t}">
<input type="hidden" name="page" value="{page}">
<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
<div class="row2"><label>Name<input type="text" name="name" autocomplete="name" required></label><label>Phone<input type="tel" name="phone" autocomplete="tel" required></label></div>
<div class="row2"><label>Email<input type="email" name="email" autocomplete="email" required></label><label>Event date<input type="date" name="event-date" required></label></div>
<label>Town or venue<input type="text" name="location" placeholder="e.g. {esc(PAGES[page]['eyebrow'].split(',')[0])}" required></label>
<label>Tell Kat about your event<textarea name="message" rows="4" placeholder="Number of children or guests, ages, theme..."></textarea></label>
<button type="submit">Send my enquiry</button>
</form>"""

# ---------- templates (each a different order and set of blocks) ----------
def render(page, d, title):
    town = town_name(d)
    slug = page.replace('face-painter-', '').replace('.html', '')
    pc = lambda tone='dark': b_postcard(d, slug, d['eyebrow'].split(',')[0] if slug not in ('west-sussex-villages', 'surrey-villages', 'south-downs') else d['eyebrow'], tone)
    t = d['tpl']
    if t == 'letter':
        blocks = [b_letter(d), pc('dark'), b_venue_map(d, 'dark'), b_gallery(d, 'light'), b_events(d, 'dark'), b_prices(), b_reviews(page, town, 'light'), b_hoods(d, town, 'dark'), b_faq(d, town, 'light')]
    elif t == 'guide':
        blocks = [b_intro_quote(d, 'light'), b_tiles(d, town, 'dark'), pc('light'), b_venue_chips(d, town, 'light'), b_reviews(page, town, 'dark'), b_prices(), b_hoods(d, town, 'light'), b_faq(d, town, 'dark')]
    elif t == 'seasons':
        blocks = [b_intro_split(d, 'light'), pc('dark'), b_seasons(d, town, 'dark'), b_venue_cards(d, town, 'light'), b_prices(), b_reviews(page, town, 'dark'), b_hoods(d, town, 'light'), b_faq(d, town, 'dark')]
    elif t == 'story':
        blocks = [b_story(d, 'light'), b_polaroids(d, 'dark'), pc('light'), b_reviews(page, town, 'light'), b_prices(), b_hoods(d, town, 'dark'), b_faq(d, town, 'light')]
    elif t == 'villages':
        blocks = [b_intro_quote(d, 'dark'), b_villages(d, 'light'), pc('dark'), b_prices(), b_reviews(page, town, 'light'), b_hoods(d, town, 'dark'), b_faq(d, town, 'light')]
    elif t == 'county':
        blocks = [b_intro_quote(d, 'light'), b_towns(d, 'dark'), pc('light'), b_prices(), b_reviews(page, town, 'light'), b_faq(d, town, 'dark')]
    blocks.append(b_enquire(page, town, title))
    blocks.append(inner_layout.TRUST_BAND)
    return '\n'.join(b for b in blocks if b)

def faq_schema(d):
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d['faqs']]}
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=1) + '\n</script>'

def hero(d, h1, sub, page):
    img, pos = d['hero']
    src = img[5:] if img.startswith('LIVE:') else img
    town = town_name(d)
    return (f'<header class="phero"><img src="{src}" alt="Face painting in {esc(town)}" style="object-position:{pos}" fetchpriority="high">'
            f'<div class="wrap"><div class="hcard"><p class="crumb"><a href="index.html">Home</a> · <a href="areas.html">Areas</a> · {esc(d["kicker"])}</p>'
            f'<h1>{h1}</h1><p>{sub}</p><div class="ctas"><a class="btn btn-gold" href="contact.html">Check my date</a>'
            f'<a class="btn btn-wa" href="{wa_link(town)}" target="_blank" rel="noopener">WhatsApp Kat</a></div></div></div>'
            f'<a class="scrollcue" href="#content" aria-label="Scroll down">⌄</a></header>\n<div class="jewel-rule"></div>')

def build():
    with open(f'{OUT}/site.css', 'a') as f: f.write(LOC_CSS)
    for page, d in PAGES.items():
        p = f'{OUT}/{page}'
        s = open(p).read()
        title = re.search(r'<title>(.*?)</title>', s, re.S).group(1)
        h1 = re.search(r'<header class="phero">.*?<h1>(.*?)</h1>', s, re.S).group(1)
        sub = re.search(r'<header class="phero">.*?</h1>\s*<p>(.*?)</p>', s, re.S)
        sub = sub.group(1) if sub else ''
        # head: replace any FAQPage schema with the new questions
        head, body = s.split('</head>', 1)
        head = re.sub(r'<script type="application/ld\+json">\s*\{[^<]*?"@type"\s*:\s*"FAQPage".*?</script>\s*', '', head, flags=re.S)
        head = head.rstrip() + '\n' + faq_schema(d) + '\n'
        # body: swap hero and main
        body = re.sub(r'<header class="phero">.*?</header>\s*<div class="jewel-rule"></div>', lambda m: hero(d, h1, sub, page), body, count=1, flags=re.S)
        body = re.sub(r'<main class="lg">.*?</main>', lambda m: f'<main class="lg loc tpl-{d["tpl"]}" id="content" style="--acc:{d["acc"]}">\n{render(page, d, title)}\n</main>', body, count=1, flags=re.S)
        open(p, 'w').write(head + '</head>' + body)
    print('location pages rebuilt:', len(PAGES))

LOC_CSS = r'''
/* ===== Header: photo stays fixed, text slides up over it ===== */
.phero{position:relative;height:100vh;height:100svh;min-height:560px;display:flex;align-items:flex-end;padding:0;overflow:visible}
.phero>img{position:fixed;inset:0;width:100%;height:100vh;object-fit:cover;z-index:-1}
.phero::after{background:linear-gradient(180deg,rgba(21,19,26,.55) 0,rgba(21,19,26,0) 20%,rgba(21,19,26,0) 55%,rgba(21,19,26,.75) 100%)}
.phero .wrap{display:block;padding-bottom:64px}
.hcard{max-width:640px;text-align:left;padding:30px 34px;background:rgba(14,12,18,.78)}
.hcard .ctas{justify-content:flex-start}
.hcard h1{font-size:clamp(32px,4.2vw,54px)!important}
.scrollcue{position:absolute;left:50%;bottom:14px;transform:translateX(-50%);z-index:3;color:#fff;text-decoration:none;font-size:30px;line-height:1;animation:bob 2s ease-in-out infinite;opacity:.85}
@keyframes bob{50%{transform:translate(-50%,6px)}}
main.lg,footer,.trustband{position:relative;background:var(--bg)}
@media(max-width:600px){.phero{height:88svh;min-height:480px;display:flex}.phero>img{height:100vh;-webkit-mask-image:none;mask-image:none}.phero .wrap{margin-top:0;padding-bottom:42px}.hcard{padding:22px 20px}}
@media(prefers-reduced-motion:reduce){.scrollcue{animation:none}}

/* ===== Location pages: shared parts ===== */
.loc{--acc:var(--pink)}
.loc .eyebrow{color:var(--acc)}
.loc h2{font-size:clamp(30px,3.6vw,46px)}
.pull{margin:28px 0 0;font-family:'Fraunces',serif;font-size:clamp(22px,2.4vw,30px);line-height:1.3;border-left:5px solid var(--acc);padding:6px 0 6px 22px;max-width:820px}
.pull.big{font-size:clamp(26px,3.4vw,44px);border:0;padding:0;margin:0 0 30px}
.pull cite{display:block;font-style:normal;font-family:'Manrope',sans-serif;font-size:14px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:var(--acc);margin-top:14px}
.band-light .pull{color:#1B1712}
.introcols{columns:2;column-gap:48px}
.introcols p{break-inside:avoid}
.lede-s{margin-top:-8px!important}
.letter{background:#FFFDF8;color:#2B2420;border-radius:6px;padding:46px 52px;max-width:820px;box-shadow:0 30px 60px -30px rgba(60,30,20,.45);position:relative;transform:rotate(-.6deg);background-image:repeating-linear-gradient(180deg,transparent 0 31px,rgba(80,120,200,.12) 31px 32px)}
.letter::before{content:"";position:absolute;top:-14px;left:50%;width:120px;height:28px;margin-left:-60px;background:var(--acc);opacity:.75;transform:rotate(2deg)}
.letter p{color:#2B2420!important;font-size:18px;line-height:1.75}
.letter .sig{font-family:'Fraunces',serif;font-style:italic;font-size:30px!important;color:var(--acc)!important;margin-top:10px}
.postcard{display:block;width:100%;height:auto;border-radius:16px;border:6px solid #fff;box-shadow:0 30px 60px -30px rgba(0,0,0,.6)}
.loc-postcard{padding:46px 0!important}
.vmap{list-style:none;counter-reset:v;padding:0;margin:26px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:12px 32px}
.vmap li{counter-increment:v;display:grid;grid-template-columns:44px 1fr;gap:4px 14px;align-items:start;padding:14px 0;border-bottom:1px solid var(--line)}
.vmap li::before{content:counter(v);grid-row:span 2;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--acc);color:#14101C;font-weight:800}
.vmap b{font-size:18px}.vmap span{color:var(--muted);font-size:15.5px}
.timeline{list-style:none;padding:0;margin:30px 0 0;display:grid;grid-template-columns:repeat(4,1fr);gap:16px;position:relative}
.timeline::before{content:"";position:absolute;left:0;right:0;top:16px;height:4px;background:var(--acc);opacity:.5;border-radius:4px}
.timeline li{position:relative;padding-top:38px}
.timeline li::before{content:"";position:absolute;top:8px;left:0;width:20px;height:20px;border-radius:50%;background:var(--acc);border:4px solid #F6F1EA}
.timeline .when{font-size:12px;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;color:var(--acc)}
.timeline b{display:block;font-size:18px;margin:4px 0}
.band-light .timeline b{color:#1B1712}
.band-dark .timeline li::before{border-color:var(--bg)}
.dchips,.hoods{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.dchips span{background:var(--acc);color:#14101C;font-weight:800;border-radius:999px;padding:8px 16px;font-size:15px}
.hoods span{border:1.5px solid var(--acc);border-radius:999px;padding:8px 16px;font-weight:700;font-size:15px}
.band-light .hoods span{color:#1B1712}
.gstrip{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:24px}
.gstrip img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:12px}
.wtiles{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:26px}
.wtile{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:28px;border-top:6px solid var(--c)}
.wlabel{font-family:'Fraunces',serif;font-size:34px;color:var(--c)}
.wtile p{margin:10px 0 0!important}
.chips{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px}
.chip{background:#fff;border-radius:16px;padding:12px 18px;box-shadow:0 10px 24px -16px rgba(60,30,40,.4);max-width:360px}
.chip summary{cursor:pointer;font-weight:800;color:#1B1712;list-style:none}
.chip summary::before{content:"📍 "}
.chip summary::-webkit-details-marker{display:none}
.chip span{display:block;color:#4E463F;font-size:15px;margin-top:6px}
.band-dark .chip{background:var(--panel)}.band-dark .chip summary{color:var(--ink)}.band-dark .chip span{color:var(--muted)}
.isplit{display:grid;grid-template-columns:.8fr 1.2fr;gap:52px;align-items:center}
.iphoto{margin:0;transform:rotate(-2deg)}
.iphoto img{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:16px;border:8px solid #fff;box-shadow:0 30px 60px -30px rgba(60,30,40,.55)}
.seasons{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}
.season{border-radius:18px;padding:24px;background:var(--panel);border:1px solid var(--line);position:relative;overflow:hidden}
.season::after{content:"";position:absolute;inset:auto -30px -30px auto;width:110px;height:110px;border-radius:50%;background:var(--c);opacity:.18}
.sicon{font-size:30px;color:var(--c)}
.season b{display:block;font-family:'Fraunces',serif;font-weight:400;font-size:26px;margin:6px 0}
.season p{margin:0!important;font-size:15.5px}
.vcards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:24px}
.vcard{background:#fff;border-radius:14px;padding:20px;border-left:5px solid var(--acc);box-shadow:0 12px 26px -18px rgba(60,30,40,.35)}
.vcard b{display:block;color:#1B1712;font-size:17px}.vcard span{color:#4E463F;font-size:15px}
.story{max-width:820px;margin:0 auto}
.story p{font-size:19px;line-height:1.75}
.story>p:first-of-type::first-letter{font-family:'Fraunces',serif;font-size:72px;float:left;line-height:.9;padding:6px 10px 0 0;color:var(--acc)}
.pols{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-top:30px}
.pol{margin:0;background:#fff;padding:12px 12px 18px;border-radius:4px;box-shadow:0 26px 50px -26px rgba(0,0,0,.7)}
.pol:nth-child(1){transform:rotate(-2.5deg)}.pol:nth-child(2){transform:rotate(1.5deg) translateY(14px)}.pol:nth-child(3){transform:rotate(-1deg)}
.pol img{width:100%;aspect-ratio:1;object-fit:cover}
.pol figcaption{padding:12px 4px 0}
.pol b{display:block;font-family:'Fraunces',serif;font-weight:400;font-size:22px;color:#1B1712}
.pol span{color:#5A5048;font-size:15px}
.vills{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:26px}
.vill{background:#fff;border-radius:18px;padding:24px;box-shadow:0 14px 30px -18px rgba(60,30,40,.35);position:relative}
.vill::before{content:"⌂";position:absolute;top:16px;right:18px;font-size:26px;color:var(--acc)}
.vill b{font-family:'Fraunces',serif;font-weight:400;font-size:26px;color:#1B1712}
.vill p{margin:8px 0 0!important;font-size:15.5px}
.tcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;margin-top:26px}
.tcard{display:flex;flex-direction:column;gap:6px;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:22px;text-decoration:none;color:var(--ink);transition:transform .2s,border-color .2s}
.tcard:hover{transform:translateY(-3px);border-color:var(--acc)}
.tcard b{font-family:'Fraunces',serif;font-weight:400;font-size:24px}
.tcard span{color:var(--muted)}
.tcard i{font-style:normal;color:var(--acc);font-weight:800;font-size:14px;margin-top:auto}
@media(max-width:900px){
.vmap,.introcols{grid-template-columns:1fr;columns:1}
.timeline{grid-template-columns:1fr 1fr;row-gap:26px}
.wtiles,.pols,.vills,.vcards{grid-template-columns:1fr 1fr}
.seasons{grid-template-columns:1fr 1fr}
.isplit{grid-template-columns:1fr}
.gstrip{grid-template-columns:1fr 1fr}
}
@media(max-width:600px){
.letter{padding:34px 24px;transform:none}
.wtiles,.pols,.vills,.vcards,.seasons,.timeline{grid-template-columns:1fr}
.timeline::before{display:none}
.pol:nth-child(n){transform:none}
.iphoto{transform:none}
.postcard{border-width:4px;border-radius:12px}
}
'''

if __name__ == '__main__':
    build()
