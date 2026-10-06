# -*- coding: utf-8 -*-
"""New Halloween page, designed offline in paintingpixie-v2/hw/ before it replaces the live halloween-face-painting.html.
Self-contained: its own CSS, images in the same folder (all prefixed halloween- so they can be copied to the live site as they are)."""
import html, json, re

V2 = '/home/claude/paintingpixie-v2'
LIVE = '/home/claude/Painting-Pixie/halloween-face-painting.html'
OUT = V2 + '/hw/halloween-face-painting.html'
SITE = 'https://paintingpixie.com/'
GLITTER_TATTOOS = True  # Kat confirmed 6 Oct 2026; set False to hide the glitter tattoo section and mentions
WA = 'https://wa.me/447852300125?text='
wa = lambda t: WA + t.replace(' ', '%20').replace("'", '%27').replace('’', '%27').replace('&', 'and')
esc = lambda t: html.escape(t, quote=True)

STRIP = [  # file, caption, alt
    ('pumpkin', 'Jack-o’-lantern', 'Jack-o-lantern pumpkin face paint on a girl'),
    ('skull-boy', 'Monster skull', 'Monster skull face paint on a boy'),
    ('devil-girl', 'Red devil', 'Red devil face paint with horns on a girl'),
    ('werewolf', 'Werewolf', 'Werewolf face paint on a grown-up at a Halloween party'),
    ('princess', 'Pink princess crown', 'Pink princess crown face paint with a skeleton costume'),
    ('adult-skull', 'Grown-up skull', 'Blue and white skull face paint on an adult'),
    ('half-skull', 'Half skull', 'Half skull face paint on a boy'),
    ('monster', 'Roaring monster', 'Blue monster face paint on a roaring child'),
    ('pumpkin-big-sister', 'Pumpkin queen', 'Pumpkin face paint on a girl at a Halloween event'),
    ('pumpkin-little-sister', 'Little pumpkin', 'Pumpkin face paint on a little girl'),
]

LEVELS = [
    ('Cute', 'For little ones', 'Smiley pumpkins, friendly monsters, sparkly bats and princess crowns. Bright, happy and not scary at all.', 'pumpkin-little-sister', 'princess', '#FFB347'),
    ('Spooky', 'For brave kids', 'Skulls, little devils and monster faces. Spooky enough to impress their friends, still fun to look at.', 'skull-boy', 'devil-girl', '#B57BFF'),
    ('Properly scary', 'For teens & grown-ups', 'Full-face skulls, werewolves and dramatic creatures for Halloween parties and fancy dress.', 'werewolf', 'adult-skull', '#FF5A4F'),
]

IDEAS = [
    ('Jack-o’-lantern', 'Orange stripes, glowing eyes and a toothy grin.'),
    ('Black cat', 'Whiskers, a little pink nose and glitter ears.'),
    ('Skeleton', 'Classic black and white, full face or half.'),
    ('Sugar skull', 'Colourful flowers and gems, beautiful rather than scary.'),
    ('Witch', 'Green face, warts optional, plus a starry hat line.'),
    ('Vampire', 'Pale skin, dark eyes and a drop of blood.'),
    ('Spider and web', 'A web across one eye with a dangling spider.'),
    ('Bats', 'A swarm of bats flying across the forehead.'),
    ('Little devil', 'Red face, horns and pointy eyebrows.'),
    ('Zombie', 'Grey skin, stitches and a scar or two.'),
    ('Werewolf', 'Fur, fangs and wild eyebrows for the full transformation.'),
    ('Pumpkin princess', 'An orange and gold crown with sparkle.'),
]

EVENTS = [
    ('Halloween birthday parties', 'At home, in village halls or at soft play.'),
    ('School & PTA Halloween discos', 'Fast, queue-friendly designs to get through a crowd.'),
    ('Pumpkin patches & farm days', 'Family-friendly painting for busy public days.'),
    ('Pubs, restaurants & venues', 'Halloween family events and themed nights.'),
    ('Grown-up Halloween parties', 'Full-face skulls, werewolves and dramatic looks.'),
    ('Office Halloween events', 'Office parties and family fun days.'),
]

PACKAGES = [
    ('Classic Party', 'From £130', ['2 hours of face painting', 'Fast, fun Halloween designs', 'Cute to spooky, guests choose'], 'Classic Party', False),
    ('Ultimate Sparkle', 'From £160', ['3 hours of face painting', 'Bio-glitter and face gems', 'More detailed designs'], 'Ultimate Sparkle', True),
    ('Grown-up Halloween party', 'From £150', ['Full-face skulls and creatures', 'Glitter and gems', 'At your house or venue'], 'grown-up Halloween party', False),
    ('School discos & big events', 'Bespoke quote', ['Hourly or per-face options', 'Extra artists for big crowds', 'Glitter tattoos for fast queues'], 'school disco or event', False),
]

REVIEWS = [
    ('"Booked Kat for my daughter\'s 6th birthday and she was brilliant. So patient with a big group of excited kids, and the designs were beautiful. Would book again in a heartbeat!"', 'Liam', 'Birthday party, Horsham'),
    ('"So amazing. Hired for our daughter\'s 4th and was phenomenal. Non stop and everyone was so complimentary of the amazing face paints!"', 'Daniel C', '4th birthday party'),
    ('"There ended up being a long queue at times just because they were so popular with both the kids and adults. All of the designs turned out wonderful."', 'Lisa K', 'Wedding reception, Brighton'),
]

FAQS = [
    ("Can you do Halloween designs that aren't too scary for young children?", "Yes. Most of my Halloween bookings include a mix of ages, so I always have friendly options like pumpkins, cute monsters, black cats and sparkly bats alongside the spookier designs. Children choose their own look, so nobody ends up with something they don't want."),
    ("Do you face paint adults for Halloween parties?", "Absolutely. Adult Halloween parties are some of my favourite bookings. Think full-face skulls, werewolves, devils and dramatic creature looks. Grown-up parties start from £150."),
    ("How long is a party booking?", "The Classic Party package is 2 hours of face painting, and the Ultimate Sparkle package is 3 hours with glitter and gems. For school discos and larger events, get in touch for a quote."),
    ("How far in advance should I book for Halloween?", "As early as you can. Halloween 2026 is on a Saturday, so Halloween weekend (Saturday 31 October) is the busiest of the season, and October half-term dates fill up quickly too."),
    ("Do you do Halloween glitter tattoos?", "Yes. Glitter tattoos of bats, pumpkins, spiders, skulls and stars are quick to do, great for big queues and perfect for little ones who don't want a painted face. They can be added to any party package or booked as a stall for your event."),
    ("Do you paint at school Halloween discos?", "Yes. I keep designs quick so the queue keeps moving, and glitter tattoos are a great extra for big crowds. I can charge per face or a set fee, whichever suits your school or PTA."),
    ("Which areas do you cover?", "I'm based in Horsham and regularly cover Crawley, Guildford, Reigate, Haywards Heath, Dorking, Worthing, Burgess Hill, Brighton, East Grinstead and the villages in between."),
]

CSS = r'''
:root{--night:#150A23;--panel:#22123A;--panel2:#2C1748;--ink:#F7F0FC;--muted:#CDBDDF;--orange:#FF8A1F;--gold:#FFC24A;--purple:#9B5BFF;--line:rgba(255,255,255,.12);--disp:'Fraunces',Georgia,serif;--body:'Manrope',system-ui,-apple-system,'Segoe UI',sans-serif;color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--night);color:var(--ink);font:17px/1.6 var(--body);-webkit-font-smoothing:antialiased}
body::before{content:"";position:fixed;inset:0;z-index:-1;background:url("halloween-night.svg") center/cover no-repeat;pointer-events:none}
body{position:relative}
.webs{position:fixed;inset:0;z-index:-1;background:url("halloween-webs-fixed.svg") center/cover no-repeat;pointer-events:none}
@media(max-aspect-ratio:3/4){.webs{background-image:url("halloween-webs-fixed-tall.svg")}}
@media(max-aspect-ratio:3/4){body::before{background-image:url("halloween-night-tall.svg")}}
img{max-width:100%;display:block}
a{color:var(--gold)}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:var(--disp);font-weight:400;line-height:1.08;text-wrap:balance;margin:0}
h2{font-size:clamp(32px,4.4vw,52px)}
.eyebrow{font:800 12.5px/1 var(--body);letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin:0 0 12px}
.lede{color:var(--muted);max-width:640px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:15px 26px;border-radius:999px;font:800 16px/1 var(--body);text-decoration:none;transition:transform .15s,box-shadow .15s}
.btn:hover{transform:translateY(-2px)}
.btn:focus-visible,.gchip:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid var(--gold);outline-offset:3px}
.btn-orange{background:linear-gradient(135deg,#FF9A2E,#FF6A13);color:#1A0B10;box-shadow:0 10px 30px -10px rgba(255,122,26,.8)}
.btn-wa{background:#25D366;color:#06210F}
.btn-ghost{border:2px solid var(--line);color:var(--ink)}
.btn-ghost:hover{border-color:var(--gold)}
/* nav */
.top{position:absolute;left:0;right:0;top:0;z-index:5}
.top .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding-top:18px}
.brand{display:flex;align-items:center;gap:12px;color:#fff;text-decoration:none;font:400 24px var(--disp)}
.brand img{width:64px;height:64px;border-radius:50%;box-shadow:0 6px 20px rgba(0,0,0,.4)}
.links{display:flex;align-items:center;gap:22px}
.links a{color:#fff;text-decoration:none;font:800 13px var(--body);letter-spacing:.1em;text-transform:uppercase}
.links a.btn{padding:11px 18px;font-size:14px;letter-spacing:0;text-transform:none}
/* hero */
.hero{display:flex;align-items:flex-start;padding:max(96px, calc(50vh - max(18.75vw, 30vh) - 34px)) 0 64px}
.hero h1{font-size:clamp(46px,7.4vw,96px);max-width:900px;text-shadow:0 6px 40px rgba(0,0,0,.5)}
.hero h1 em{font-style:italic;color:var(--orange)}
.hero .lede{font-size:19px;margin:18px 0 26px;color:#EADDF7}
.ctas{display:flex;flex-wrap:wrap;gap:12px}
.dates{margin-top:28px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.dates b{font-size:14px;color:var(--muted);margin-right:4px}
.dates span{padding:8px 13px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid var(--line);font:700 14px var(--body)}
.dates span.hot{background:var(--orange);color:#1A0B10;border-color:transparent}
/* strip */
.strip-wrap{padding:8px 0 4px;background:rgba(12,5,22,.35);backdrop-filter:none}
.strip{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(290px,1fr);gap:12px;overflow-x:auto;padding:16px 16px 10px;scroll-snap-type:x mandatory;scrollbar-width:none}
.strip::-webkit-scrollbar{display:none}
.strip a{position:relative;display:block;scroll-snap-align:start;border-radius:16px;overflow:hidden;text-decoration:none;color:#fff}
.strip img{width:100%;height:auto;aspect-ratio:3/4;object-fit:cover;object-position:50% 40%;transition:transform .4s}
.strip a:hover img{transform:scale(1.04)}
.strip .cap{position:absolute;left:0;right:0;bottom:0;padding:40px 14px 12px;background:linear-gradient(180deg,transparent,rgba(12,5,22,.9));display:flex;justify-content:space-between;align-items:flex-end;gap:8px}
.strip .cap b{font:400 21px/1.1 var(--disp)}
.strip .cap i{font:800 12px var(--body);font-style:normal;background:#25D366;color:#06210F;padding:6px 10px;border-radius:999px;white-space:nowrap}
.strip-note{text-align:center;color:var(--muted);font-size:15px;margin:6px 0 14px}
/* trust */
.trust{display:flex;flex-wrap:wrap;justify-content:center;gap:12px 34px;padding:22px 0;font-weight:700;font-size:15px;color:#EADDF7}
.trust span b{color:var(--gold)}
/* sections */
.band{padding:84px 0}
.panel{background:rgba(20,9,34,.42);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.intro{display:grid;grid-template-columns:5fr 7fr;gap:52px;align-items:center}
.intro img{border-radius:20px;aspect-ratio:4/5;object-fit:cover;box-shadow:0 30px 60px -20px rgba(0,0,0,.7)}
.intro p{color:#E3D5F1}
.sig{font:italic 400 26px var(--disp);color:var(--gold);margin-top:6px}
.gt{display:grid;grid-template-columns:7fr 5fr;gap:52px;align-items:center}
.gt img{border-radius:20px;aspect-ratio:4/5;object-fit:cover;object-position:72% 50%;box-shadow:0 30px 60px -20px rgba(0,0,0,.7)}
.gt p{color:#E3D5F1}
.ticks{list-style:none;padding:0;margin:14px 0;display:grid;gap:8px}
.ticks li{padding-left:28px;position:relative;color:#EADDF7}
.ticks li::before{content:"✦";position:absolute;left:4px;color:var(--orange)}
.levels{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:34px}
.level{background:var(--panel);border:1px solid var(--line);border-top:4px solid var(--c);border-radius:18px;overflow:hidden;display:flex;flex-direction:column}
.level .pics{display:grid;grid-template-columns:1fr 1fr;gap:3px}
.level .pics img{aspect-ratio:4/5;object-fit:cover;width:100%}
.level .txt{padding:20px 22px 24px}
.level h3{font-size:30px}
.level small{display:block;font:800 12px var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--c);margin:4px 0 10px}
.level p{margin:0;color:var(--muted);font-size:16px}
.ideas{display:grid;grid-template-rows:repeat(2,auto);grid-auto-flow:column;grid-auto-columns:minmax(250px,280px);gap:12px;margin-top:30px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px;scrollbar-width:thin;scrollbar-color:var(--orange) transparent}
.idea{scroll-snap-align:start}
.swipe{margin:10px 0 0;color:var(--muted);font-size:14.5px}
.idea{padding:16px 18px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid var(--line)}
.idea b{display:block;font:400 21px var(--disp);color:#fff;margin-bottom:4px}
.idea span{font-size:14.5px;color:var(--muted)}
.ideas-note{margin-top:20px;color:var(--muted)}
.events{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:30px}
.event{padding:20px 22px;border-radius:16px;background:var(--panel);border:1px solid var(--line)}
.event b{display:block;font:400 22px/1.2 var(--disp);margin-bottom:6px}
.event span{color:var(--muted);font-size:15.5px}
.packs{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:32px;align-items:stretch}
.pack{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:24px 22px;display:flex;flex-direction:column;gap:12px}
.pack.hi{background:linear-gradient(180deg,#3A1A55,#2A1442);border:2px solid var(--orange);position:relative}
.pack.hi::before{content:"Most popular";position:absolute;top:-13px;left:22px;background:var(--orange);color:#1A0B10;font:800 12px var(--body);padding:5px 11px;border-radius:999px}
.pack h3{font-size:25px}
.pack .price{font:400 34px var(--disp);color:var(--gold)}
.pack ul{margin:0;padding:0;list-style:none;display:grid;gap:7px;color:var(--muted);font-size:15px;flex:1}
.pack li::before{content:"✦ ";color:var(--orange)}
.pack .btn{padding:12px 16px;font-size:15px}
.packnote{margin-top:18px;color:var(--muted);font-size:15px}
.reviews{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:30px}
.review{background:#FBF5FF;color:#2A1B38;border-radius:18px;padding:24px;margin:0}
.review .s{color:#E8890C;letter-spacing:2px}
.review blockquote{margin:10px 0 14px;font-size:16.5px}
.review figcaption b{display:block}
.review figcaption small{color:#6E5C80}
.rating{margin-top:20px;display:flex;align-items:center;gap:14px;color:var(--muted)}
.rating img{width:74px}
.workshop{display:grid;grid-template-columns:auto 1fr auto;gap:22px;align-items:center;background:linear-gradient(135deg,#3B1658,#5A1F48);border:1px solid var(--line);border-radius:20px;padding:24px 28px}
.workshop .when{font:400 40px/1 var(--disp);color:var(--gold);text-align:center}
.workshop .when small{display:block;font:800 13px var(--body);letter-spacing:.12em;color:#fff;margin-top:4px}
.workshop h3{font-size:26px;margin-bottom:6px}
.workshop p{margin:0;color:#E3D5F1;font-size:15.5px}
.faqs{display:grid;gap:10px;margin-top:28px;max-width:860px}
.faqs details{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:4px 20px}
.faqs summary{cursor:pointer;font:700 17px var(--body);padding:14px 0;list-style:none;display:flex;justify-content:space-between;gap:12px}
.faqs summary::after{content:"+";color:var(--gold);font-size:22px;line-height:1}
.faqs details[open] summary::after{content:"–"}
.faqs p{margin:0 0 16px;color:var(--muted)}
.final{text-align:center;padding:96px 0}
.final h2{font-size:clamp(36px,5vw,62px)}
.final .lede{margin:14px auto 26px}
.final .ctas{justify-content:center}
.phone{margin-top:16px;color:var(--muted)}
footer{background:#0C0614;color:#B9A8CC;font-size:14px;padding:34px 0 90px;text-align:center}
footer a{color:#E3D5F1}
footer .flinks{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 20px;margin-bottom:14px}
footer .ate{display:inline-block;margin-bottom:12px}
footer .ate img{width:70px}
.wa-float{position:fixed;right:18px;bottom:18px;z-index:20;width:60px;height:60px;border-radius:50%;background:#25D366;display:grid;place-items:center;box-shadow:0 10px 30px rgba(0,0,0,.45)}
.wa-float svg{width:32px;height:32px;fill:#fff}
@media(max-width:980px){.packs{grid-template-columns:1fr 1fr}.events{grid-template-columns:1fr 1fr}.links a:not(.btn){display:none}}
@media(max-width:760px){
 body{font-size:16px}
 .brand span{display:none}.brand img{width:54px;height:54px}
 .hero{min-height:auto;padding:max(96px, calc(19vh - 22px)) 0 40px}
 .hero .lede{font-size:17px}
 .ctas .btn{flex:1 1 auto}
 .strip{grid-auto-columns:70%}
 .strip img{max-height:62vh}
 .band{padding:60px 0}
 .intro,.levels,.reviews,.gt{grid-template-columns:1fr}
 .intro{gap:26px}
 .ideas{grid-auto-columns:72%}.events,.packs{grid-template-columns:1fr}
 .workshop{grid-template-columns:1fr;text-align:left}.workshop .when{text-align:left}
}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
'''

WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C9 3 3.3 8.6 3.3 15.6c0 2.5.7 4.8 1.9 6.8L3 29l6.8-2.1c1.9 1 4 1.6 6.2 1.6 7 0 12.7-5.6 12.7-12.6S23 3 16 3zm0 23.2c-2 0-3.9-.6-5.5-1.6l-.4-.2-4 1.2 1.3-3.9-.3-.4a10.4 10.4 0 0 1-1.6-5.6C5.5 9.9 10.2 5.3 16 5.3s10.5 4.6 10.5 10.3S21.8 26.2 16 26.2zm5.8-7.7c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-.3-.2-1.3-.5-2.5-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.6c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.7s1.2 3.2 1.4 3.4c.2.2 2.4 3.6 5.8 5 .8.4 1.4.6 1.9.7.8.3 1.6.2 2.2.1.7-.1 1.9-.8 2.2-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'

def body():
    strip = ''.join(
        f'<a href="{wa("Hi Kat! I love the " + c + " design. Are you free for a Halloween party? Date: Town: ")}" target="_blank" rel="noopener" data-design="{esc(c)}">'
        f'<img src="halloween-{f}.webp" alt="{esc(a)}" width="880" height="1100" loading="{"eager" if i < 4 else "lazy"}">'
        f'<span class="cap"><b>{esc(c)}</b><i>Book this look</i></span></a>' for i, (f, c, a) in enumerate(STRIP))
    levels = ''.join(
        f'<article class="level" style="--c:{col}"><div class="pics"><img src="halloween-{a}-card.webp" alt="" loading="lazy"><img src="halloween-{b}-card.webp" alt="" loading="lazy"></div>'
        f'<div class="txt"><h3>{esc(n)}</h3><small>{esc(who)}</small><p>{esc(d)}</p></div></article>' for n, who, d, a, b, col in LEVELS)
    ideas = ''.join(f'<div class="idea"><b>{esc(n)}</b><span>{esc(d)}</span></div>' for n, d in IDEAS)
    events = ''.join(f'<div class="event"><b>{esc(n)}</b><span>{esc(d)}</span></div>' for n, d in EVENTS)
    packs = ''.join(
        f'<article class="pack{" hi" if hi else ""}"><h3>{esc(n)}</h3><div class="price">{esc(pr)}</div><ul>{"".join(f"<li>{esc(x)}</li>" for x in items)}</ul>'
        f'<a class="btn {"btn-orange" if hi else "btn-ghost"}" href="{wa("Hi Kat! I am interested in a " + w + " for Halloween. Date: Town: ")}" target="_blank" rel="noopener">Check my date</a></article>'
        for n, pr, items, w, hi in PACKAGES)
    reviews = ''.join(f'<figure class="review"><span class="s" aria-label="5 stars">★★★★★</span><blockquote>{esc(q)}</blockquote><figcaption><b>{esc(n)}</b><small>{esc(w)}</small></figcaption></figure>' for q, n, w in REVIEWS)
    faqs = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQS)
    book = wa("Hi Kat! I'd like to book Halloween face painting. Date: Town: Guests: ")
    gt_link = wa("Hi Kat! I'd like to ask about Halloween glitter tattoos. Date: Town: ")
    return f'''<div class="webs" aria-hidden="true"></div>
<header class="top"><div class="wrap"><a class="brand" href="{SITE}"><img src="logo-lg.webp" alt="The Painting Pixie"><span>The Painting Pixie</span></a>
<nav class="links" aria-label="Main"><a href="{SITE}">Home</a><a href="{SITE}services.html">Services</a><a href="{SITE}gallery.html">Gallery</a><a href="{SITE}areas.html">Areas</a><a class="btn btn-orange" href="{SITE}contact.html">Check my date</a></nav></div></header>

<section class="hero"><div class="wrap">
<p class="eyebrow">Halloween 2026 · Sussex &amp; Surrey</p>
<h1>Halloween face painting that’s <em>cute, spooky</em> or properly scary</h1>
<p class="lede">Parties, school discos and Halloween events across Sussex and Surrey, painted by Kat. Every guest picks their own fright level, from smiley pumpkins to full-face skulls, plus sparkly Halloween glitter tattoos.</p>
<div class="ctas"><a class="btn btn-orange" href="{SITE}contact.html">Check my date</a><a class="btn btn-wa" href="{book}" target="_blank" rel="noopener">WhatsApp Kat</a></div>
<div class="dates"><b>Halloween is on a Saturday this year, and dates are already being booked:</b><span>Sat 24 Oct</span><span>Sun 25 Oct</span><span>Fri 30 Oct</span><span class="hot">Sat 31 Oct</span><span>Sun 1 Nov</span></div>
</div></section>

<section class="strip-wrap" aria-label="Halloween face painting by Kat"><div class="strip">{strip}</div>
<p class="strip-note">Swipe for more, tap a look to book it, or <a href="{SITE}gallery.html">see the full gallery</a></p>
<div class="wrap trust"><span><b>Calm and patient</b> with nervous little ones</span><span><b>★★★★★ 5.0</b> on Add to Event</span><span>Insured &amp; DBS checked</span><span>Professional skin-safe paints</span></div></section>

<section class="band panel"><div class="wrap intro">
<img src="halloween-kat-at-work.webp" alt="Kat from The Painting Pixie face painting a child" loading="lazy">
<div><p class="eyebrow">Hello, I’m Kat</p><h2>The one night everyone wants to be transformed</h2>
<p>Halloween is one of my favourite times of year to paint. I’m a professional face painter based in Horsham, and every October I paint parties, school discos and Halloween events across Sussex and Surrey.</p>
<p>I match the designs to your guests: cute and friendly for little ones, properly spooky for older kids and grown-ups. Everyone gets the look they want, and nobody ends up in tears.</p>
<p class="sig">Kat x</p></div></div></section>

<section class="band"><div class="wrap">
<p class="eyebrow">Pick your fright level</p><h2>Cute, spooky or properly scary</h2>
<p class="lede">Most Halloween parties have a mix of ages, so I bring all three. Children choose their own design on the day.</p>
<div class="levels">{levels}</div></div></section>

<section class="band panel"><div class="wrap gt">
<div><p class="eyebrow">Halloween glitter tattoos</p><h2>Sparkly bats, pumpkins and skulls</h2>
<p>Glitter tattoos are a brilliant Halloween extra. I use stencils and cosmetic glitter to make bats, pumpkins, spiders, skulls, witches’ hats and stars on arms and hands.</p>
<ul class="ticks"><li>Quick to do, so great for long queues at school discos and events</li><li>Perfect for toddlers, or anyone who’d rather not have a painted face</li><li>No mess, and they usually last for several days after the party</li></ul>
<p>Add them to any party package, or book a glitter tattoo stall for your event.</p>
<div class="ctas" style="margin-top:20px"><a class="btn btn-orange" href="{gt_link}" target="_blank" rel="noopener">Ask about glitter tattoos</a></div></div>
<img src="halloween-glitter-tattoo.webp" alt="Kat applying a glitter tattoo with a stencil" loading="lazy"></div></section>

<section class="band"><div class="wrap">
<p class="eyebrow">Halloween face paint ideas</p><h2>Twelve favourites to choose from</h2>
<p class="lede">Not sure what to go for? These are the designs I paint most at Halloween. Your guests can pick on the day, or ask for something special when you book.</p>
<div class="ideas" tabindex="0" aria-label="Halloween face paint ideas, scroll sideways for more">{ideas}</div>
<p class="swipe">Swipe or scroll sideways for more ideas →</p>
<p class="ideas-note">Want a costume match, a favourite character or a design from Pinterest? <a href="{wa("Hi Kat! Could you paint this Halloween design? ")}" target="_blank" rel="noopener">Send Kat a picture on WhatsApp</a>.</p>
</div></section>

<section class="band panel"><div class="wrap">
<p class="eyebrow">Halloween events</p><h2>Where I paint at Halloween</h2>
<div class="events">{events}</div></div></section>

<section class="band" id="prices"><div class="wrap">
<p class="eyebrow">Prices</p><h2>Halloween packages</h2>
<p class="lede">Simple prices, confirmed for your date when you enquire. A small deposit secures your booking.</p>
<div class="packs">{packs}</div>
<p class="packnote">Add glitter tattoos for a quick, mess-free extra that lasts beyond the party.</p>
</div></section>

<section class="band panel"><div class="wrap">
<p class="eyebrow">Reviews</p><h2>What people say about Kat</h2>
<div class="reviews">{reviews}</div>
<div class="rating"><img src="addtoevent-top-rated.webp" alt="Top rated on Add to Event" width="74" height="71" loading="lazy"><span><b>5.0</b> from 30+ reviews on <a href="https://www.addtoevent.co.uk/suppliers/the-painting-pixie-ltd" target="_blank" rel="noopener">Add to Event</a></span></div>
</div></section>

<section class="band" style="padding-top:0"><div class="wrap">
<div class="workshop"><div class="when">30<small>OCTOBER</small></div>
<div><h3>Half-term Halloween workshop, London</h3><p>Children learn to decorate arms, hands and faces with paints, stencils and glitter. Friday 30 October, 10:30am to 12:30pm at the Good Hotel, London E16 1FA. £15 per child.</p></div>
<a class="btn btn-orange" href="https://www.tickettailor.com/events/goodhotellondon/2442707" target="_blank" rel="noopener">Get tickets</a></div>
</div></section>

<section class="band panel"><div class="wrap">
<p class="eyebrow">Good to know</p><h2>Halloween questions</h2>
<div class="faqs">{faqs}</div></div></section>

<section class="final"><div class="wrap">
<h2>Halloween weekend goes first</h2>
<p class="lede">Send your date and town and Kat will check her diary, usually the same day. No obligation, and no payment to enquire.</p>
<div class="ctas"><a class="btn btn-orange" href="{SITE}contact.html">Check my date</a><a class="btn btn-wa" href="{book}" target="_blank" rel="noopener">WhatsApp Kat</a></div>
<p class="phone">Or call or WhatsApp Kat on <b>07852 300125</b></p>
</div></section>

<footer><div class="wrap">
<div class="flinks"><a href="{SITE}">Home</a><a href="{SITE}childrens-face-painting.html">Children’s parties</a><a href="{SITE}adult-face-painting.html">Adult &amp; hen parties</a><a href="{SITE}gallery.html">Gallery</a><a href="{SITE}areas.html">Areas</a><a href="{SITE}contact.html">Book</a></div>
<a class="ate" href="https://www.addtoevent.co.uk/suppliers/the-painting-pixie-ltd" target="_blank" rel="noopener"><img src="addtoevent-top-rated.webp" alt="Top rated on Add to Event" loading="lazy"></a>
<p>© 2026 The Painting Pixie. Serving Horsham, Guildford, Brighton, Crawley and across Sussex and Surrey.<br>The Painting Pixie is a trading name of The Painting Pixie Ltd. Registered in England and Wales, company number 14851167.</p>
</div></footer>
<a class="wa-float" href="{book}" target="_blank" rel="noopener" aria-label="WhatsApp Kat">{WA_SVG}</a>'''

def no_tattoos(page):
    page = re.sub(r'<section class="band panel"><div class="wrap gt">.*?</section>\s*', '', page, count=1, flags=re.S)
    page = page.replace('<section class="band"><div class="wrap">\n<p class="eyebrow">Halloween face paint ideas</p>', '<section class="band panel"><div class="wrap">\n<p class="eyebrow">Halloween face paint ideas</p>')
    page = page.replace('<section class="band panel"><div class="wrap">\n<p class="eyebrow">Halloween events</p>', '<section class="band"><div class="wrap">\n<p class="eyebrow">Halloween events</p>')
    page = page.replace('<section class="band" id="prices">', '<section class="band panel" id="prices">')
    page = page.replace('<section class="band panel"><div class="wrap">\n<p class="eyebrow">Reviews</p>', '<section class="band"><div class="wrap">\n<p class="eyebrow">Reviews</p>')
    page = page.replace(', plus sparkly Halloween glitter tattoos.', '.')
    page = re.sub(r'<p class="packnote">Add glitter tattoos[^<]*</p>\s*', '', page)
    page = page.replace('Glitter tattoos for fast queues', 'Quick designs to keep queues moving')
    page = page.replace(', and glitter tattoos are a great extra for big crowds', '')
    page = page.replace('Halloween face painting and glitter tattoos for parties', 'Halloween face painting for parties')
    return page

def build():
    if not GLITTER_TATTOOS:
        FAQS[:] = [f for f in FAQS if 'glitter tattoos?' not in f[0]]
    live = open(LIVE).read()
    ga = live[live.index('<!-- Google tag'):live.index('<meta charset')]
    biz = re.search(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "LocalBusiness".*?</script>', live, re.S).group(0)
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    title = 'Halloween Face Painting in Sussex &amp; Surrey | The Painting Pixie'
    desc = 'Halloween face painting and glitter tattoos for parties, school discos and events across Sussex and Surrey. Cute, spooky or properly scary. Insured and DBS checked.'
    head = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
{ga}<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}halloween-face-painting.html">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:title" content="Halloween Face Painting in Sussex &amp; Surrey">
<meta property="og:site_name" content="The Painting Pixie">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}halloween-pumpkin-wide.webp">
<meta property="og:url" content="{SITE}halloween-face-painting.html">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;1,9..144,400&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
{biz}
<script type="application/ld+json">
{json.dumps(faq_schema, ensure_ascii=False, indent=1)}
</script>
<style>{CSS}</style>
</head>
<body>
'''
    track = '''
<script>
document.querySelectorAll('.strip a').forEach(function(a){a.addEventListener('click',function(){if(window.gtag)gtag('event','whatsapp_click',{button_position:'halloween_book_look',design:a.dataset.design})})});
</script>'''
    page = head + body() + '\n</body>\n</html>\n'
    if not GLITTER_TATTOOS: page = no_tattoos(page)
    open(OUT, 'w').write(page)
    print('written', OUT)

if __name__ == '__main__':
    build()
