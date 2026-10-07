# -*- coding: utf-8 -*-
"""Services (card grid), Workshops (learn to face paint) and Corporate & brand events pages.
Runs after build_draft/build_locations and before build_conversion (so they get the shared extras)."""
import re, json, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inner_layout

OUT = '/home/claude/paintingpixie-v2/draft'
WA = "https://wa.me/447852300125?text="
def wa(t): return WA + t.replace(' ', '%20').replace("'", '%27').replace('&', 'and')
def esc(t): return html.escape(t, quote=False)

SERVICES = [
 ("Children's parties", "../img/n-unicorn-girl-party.webp", "50% 25%", "Unicorns, dragons, superheroes and more, painted fast so every child gets their favourite.", "From £130", "childrens-face-painting.html", "Children's parties"),
 ("Hen parties & adult celebrations", "../img/n-adult-leopard-eye.webp", "50% 30%", "Glitter, gems and grown-up designs at your house, venue or hotel. Great for photos.", "From £150", "adult-face-painting.html", "Hen & adult parties"),
 ("Corporate & brand events", "../img/n-arm-art-flowers-pair.webp", "50% 50%", "Staff fun days, summer parties, launches and activations, with extra artists for big crowds.", "Bespoke quote", "corporate-events.html", "Corporate events"),
 ("Weddings", "../img/n-adult-glitter-flower-eye.webp", "45% 40%", "Keeps little guests happy through speeches and photos, and the grown-ups queue for glitter too.", "Bespoke quote", "contact.html", "Check my date"),
 ("Chunky glitter & jewel bar", "../img/n-lilac-flower-eye.webp", "35% 50%", "Bio-glitter, gems and sparkle for faces, hair and arms. Festival vibes for any event.", "Bespoke quote", "glitter-bar.html", "Glitter bar"),
 ("Glitter tattoos", "unicorn-crown-face-paint-girl-glitter-tattoo-horsham.webp", "50% 40%", "Temporary glitter tattoos made with stencils and cosmetic glitter: quick, mess-free and they last well beyond the party. Great for queues and for anyone who would rather not have a painted face.", "Add-on or bespoke quote", "contact.html", "Ask about tattoos"),
 ("Animal print", "../img/n-tiger-girl-closeup.webp", "50% 35%", "Bold tigers, leopards and butterflies for kids and grown-ups.", "Included in packages", "animal-print-face-painting.html", "See the designs"),
 ("Body art", "rainbow-chest-paint-with-glitter-clouds.webp", "50% 40%", "Painted body art and flowing arm designs with glitter, for festivals, Pride, photoshoots and themed events.", "Bespoke quote", "body-art.html", "Body art"),
 ("Halloween", "../img/n-pumpkin-face.webp", "50% 30%", "Pumpkins, skulls, devils and monsters, from sweet to spooky.", "From £130", "halloween-face-painting.html", "Halloween"),
 ("Christmas", "blue-shooting-stars-face-paint-for-girls.webp", "50% 35%", "Reindeer, snowflakes, elves and glitter for Christmas parties, school fairs, grottos and office parties.", "From £130", "christmas-face-painting.html", "Christmas"),
 ("Festivals, fêtes & community days", "../img/v2-hero.webp", "60% 35%", "Fast, queue-friendly designs for school fairs, village fêtes and festivals, as a stall or a set fee.", "Bespoke quote", "contact.html", "Get a quote"),
 ("Learn to face paint", "../img/kat-painting-poster.webp", "50% 40%", "Workshops for children and groups, plus one-to-one masterclasses covering painting skills and how to set up and grow a face painting business.", "Workshops £15 per child · groups £150pp · masterclass £200", "workshops.html", "Workshops & lessons"),
]

CSS = r'''<style>
.svgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:30px}
.svcard{background:#fff;border-radius:18px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 18px 40px -26px rgba(60,30,40,.45);border-top:5px solid var(--c)}
.svcard:nth-child(5n+1){--c:var(--pink)}.svcard:nth-child(5n+2){--c:var(--violet)}.svcard:nth-child(5n+3){--c:var(--teal)}.svcard:nth-child(5n+4){--c:var(--orange)}.svcard:nth-child(5n){--c:var(--gold)}
.svcard img{width:100%;aspect-ratio:4/3;object-fit:cover}
.svcard>div{padding:22px;display:flex;flex-direction:column;gap:8px;flex:1}
.svcard h3{margin:0;font-family:'Fraunces',serif;font-weight:400;font-size:25px;color:#1B1712}
.svcard p{margin:0!important;color:#4E463F!important;font-size:15.5px;flex:1}
.svprice{font-weight:800;color:#1B1712;font-size:15px}
.svcard .btn{align-self:flex-start;margin:6px 0 0!important}
.svmore{grid-column:1/-1;background:linear-gradient(135deg,#2A0F33,#16142A 60%,#0D2B2A);border-radius:18px;padding:30px;color:var(--ink);display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px}
.svmore h3{margin:0 0 6px;font-family:'Fraunces',serif;font-weight:400;font-size:28px}
.svmore p{margin:0!important;color:var(--muted)!important}
.evsplit{display:grid;grid-template-columns:1.2fr .8fr;gap:48px;align-items:center}
.evvideo{justify-self:center;width:100%;max-width:340px;aspect-ratio:9/16;border-radius:22px;overflow:hidden;border:6px solid #fff;box-shadow:0 30px 60px -30px rgba(0,0,0,.7);background:#000}
.evvideo video{width:100%;height:100%;object-fit:cover;display:block}
.evfacts{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:22px}
.evfacts div{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;border-left:5px solid var(--c,var(--pink))}
.evfacts div:nth-child(2){--c:var(--teal)}.evfacts div:nth-child(3){--c:var(--violet)}.evfacts div:nth-child(4){--c:var(--gold)}
.evfacts b{display:block;color:var(--ink);font-size:17px}.evfacts span{color:var(--muted);font-size:14.5px}
.wscard{display:grid;grid-template-columns:.9fr 1.1fr;gap:0;background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 30px 60px -30px rgba(60,30,40,.5);margin-top:26px}
.wscard img{width:100%;height:100%;object-fit:cover;min-height:320px}
.wscard>div{padding:32px}
.wsdate{display:inline-block;background:var(--pink);color:#14101C;font-weight:800;border-radius:999px;padding:6px 14px;font-size:14px}
.wscard h3{margin:14px 0 8px;font-family:'Fraunces',serif;font-weight:400;font-size:32px;color:#1B1712}
.wscard ul{list-style:none;padding:0;margin:12px 0 18px;color:#3A322C}
.wscard li{padding:4px 0}.wscard li b{color:#1B1712}
.lprice{display:flex;flex-wrap:wrap;gap:14px;margin:18px 0 6px}.lprice div{background:#fff;border-radius:14px;padding:16px 22px;border-left:5px solid var(--pink);box-shadow:0 12px 26px -18px rgba(60,30,40,.35)}.lprice b{display:block;font-family:'Fraunces',serif;font-weight:400;font-size:30px;color:#1B1712}.lprice span{color:#4E463F;font-size:14.5px}.incl{background:#fff6fb;border:1px dashed var(--pink);border-radius:12px;padding:12px 16px;margin:14px 0 4px;font-size:15.5px}
.teachnote{background:#fff;border-radius:14px;padding:16px 20px;border-left:5px solid var(--teal);box-shadow:0 12px 26px -18px rgba(60,30,40,.35);color:#3A322C!important}.teachnote b{color:#1B1712}
.wsideas{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}
.wsideas div{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px}
.wsideas b{display:block;font-family:'Fraunces',serif;font-weight:400;font-size:22px;color:var(--ink)}
.wsideas span{color:var(--muted);font-size:15px}
@media(max-width:900px){.svgrid{grid-template-columns:1fr 1fr}.evsplit,.wscard{grid-template-columns:1fr}.wsideas{grid-template-columns:1fr}}
@media(max-width:600px){.svgrid{grid-template-columns:1fr}.evfacts{grid-template-columns:1fr}}
</style>'''

def hero(img, pos, crumb, h1, sub, ctas):
    return (f'<header class="phero"><img src="{img}" alt="{esc(re.sub("<[^>]+>", "", h1))}" style="object-position:{pos}" fetchpriority="high">'
            f'<div class="wrap"><div class="hcard"><p class="crumb"><a href="index.html">Home</a> · {crumb}</p><h1>{h1}</h1><p>{sub}</p>'
            f'<div class="ctas">{ctas}</div></div></div><a class="scrollcue" href="#content" aria-label="Scroll down">⌄</a></header>\n<div class="jewel-rule"></div>')

def page_from(template, out, title, desc, canon, extra_head, hero_html, main_html):
    s = open(f'{OUT}/{template}').read()
    s = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + canon, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title, s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + desc, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + canon, s, count=1)
    s = re.sub(r'(<meta name="twitter:title" content=")[^"]*', lambda m: m.group(1) + title, s, count=1)
    s = re.sub(r'(<meta name="twitter:description" content=")[^"]*', lambda m: m.group(1) + desc, s, count=1)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', '', s, flags=re.S)
    s = s.replace('</head>', extra_head + CSS + '\n</head>', 1)
    s = re.sub(r'<header class="phero">.*?</header>\s*<div class="jewel-rule"></div>', lambda m: hero_html, s, count=1, flags=re.S)
    s = re.sub(r'<main class="lg[^"]*"[^>]*>.*?</main>', lambda m: main_html, s, count=1, flags=re.S)
    open(f'{OUT}/{out}', 'w').write(s)

def services():
    cards = ''.join(
        f'<article class="svcard"><img src="{img}" alt="{esc(t)}" loading="lazy" style="object-position:{pos}"><div><h3>{esc(t)}</h3><p>{esc(d)}</p>'
        f'<span class="svprice">{esc(pr)}</span><a class="btn btn-gold" href="{u}">{esc(b)}</a></div></article>'
        for t, img, pos, d, pr, u, b in SERVICES)
    more = ('<div class="svmore"><div><h3>Something else in mind?</h3><p>Themed parties, branded designs or a creative idea for your event: tell Kat what you are planning.</p></div>'
            f'<a class="btn btn-wa" href="{wa("Hi Kat! I have an idea for an event and would love to chat about it.")}" target="_blank" rel="noopener">Chat to Kat on WhatsApp</a></div>')
    main = f'''<main class="lg" id="content">
<section class="band band-light"><div class="wrap">
<p class="eyebrow">What Kat does</p><h2>Face painting, glitter and workshops</h2>
<p>Professional, fully insured face painting for every kind of celebration across Sussex and Surrey. Pick a service to see designs, prices and reviews.</p>
<div class="svgrid">{cards}{more}</div>
</div></section>
<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Is Kat free on your date?</h2>
<p>Tell Kat your date, town and roughly how many guests. She usually replies the same day.</p>
<a class="btn btn-gold" href="contact.html">Check my date</a></div></section>
{inner_layout.TRUST_BAND}
</main>'''
    schema = {"@context": "https://schema.org", "@type": "ItemList", "name": "The Painting Pixie services",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": t, "url": "https://paintingpixie.com/" + u}
                                  for i, (t, img, pos, d, pr, u, b) in enumerate(SERVICES) if u != 'contact.html']}
    page_from('services.html', 'services.html', 'Face Painting Services in Sussex &amp; Surrey | The Painting Pixie',
              "Children's parties, hen dos, weddings, glitter bar, corporate events and learn-to-face-paint workshops across Sussex & Surrey. 5.0 rated, insured.",
              'https://paintingpixie.com/services.html',
              '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script>\n',
              hero('../img/v2-sisters.webp', '50% 30%', 'Services', 'Our Services',
                   'Everything Kat offers, from kids’ parties to glitter bars, corporate events and workshops.',
                   '<a class="btn btn-gold" href="contact.html">Check my date</a>'), main)

def workshops():
    event = {"@context": "https://schema.org", "@type": "Event", "name": "Half-Term Halloween Face Painting Workshop",
             "startDate": "2026-10-30T10:30:00+00:00", "endDate": "2026-10-30T12:30:00+00:00",
             "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
             "location": {"@type": "Place", "name": "Good Hotel London", "address": {"@type": "PostalAddress", "addressLocality": "London", "postalCode": "E16 1FA", "addressCountry": "GB"}},
             "image": ["https://paintingpixie.com/hero.jpg"],
             "description": "Spooky fun for school-aged children: learn to design and decorate arms, hands and faces with paints, stencils and glitter.",
             "offers": {"@type": "Offer", "price": "15", "priceCurrency": "GBP", "url": "https://www.tickettailor.com/events/goodhotellondon/2442707", "availability": "https://schema.org/InStock"},
             "organizer": {"@type": "Organization", "name": "The Painting Pixie", "url": "https://paintingpixie.com/"},
             "performer": {"@type": "Person", "name": "Kat, The Painting Pixie"}}
    tickets = "https://www.tickettailor.com/events/goodhotellondon/2442707"
    main = f'''<main class="lg" id="content">
<section class="band band-light"><div class="wrap">
<p class="eyebrow">Next workshop</p><h2>Learn to face paint with Kat</h2>
<p>Hands-on sessions where children (and grown-ups!) learn to design and paint faces, arms and hands, using the same professional paints, stencils and glitter Kat uses at parties. Kat is also a GCSE and A level teacher, so sessions are well organised, patient and fun.</p>
<article class="wscard"><img src="../img/n-pumpkin-face.webp" alt="Halloween pumpkin face paint" loading="lazy" style="object-position:50% 30%">
<div><span class="wsdate">Friday 30 October 2026 · 10:30am–12:30pm</span>
<h3>Half-Term Halloween Workshop</h3>
<ul><li><b>Where:</b> Good Hotel London, E16 1FA</li><li><b>Who:</b> school-aged children</li><li><b>What:</b> design and decorate arms, hands and faces with paints, stencils and glitter</li><li><b>Price:</b> £15 per child</li><li>Parents can relax in the lobby or at the bar.</li></ul>
<a class="btn btn-gold" href="{tickets}" target="_blank" rel="noopener">Get tickets</a></div></article>
</div></section>
<section class="band band-dark"><div class="wrap">
<p class="eyebrow">Book a workshop for your group</p><h2>Bring a workshop to you</h2>
<p>Kat can run a learn-to-face-paint session for your group. Tell her what you have in mind and she'll suggest a format.</p>
<div class="wsideas"><div><b>Schools &amp; clubs</b><span>A creative session for a class, club or holiday camp.</span></div>
<div><b>Birthday parties</b><span>Older children learn to paint each other, then go home with their designs.</span></div>
<div><b>Hen dos &amp; team days</b><span>A glittery, sociable activity for grown-ups that is great for photos.</span></div></div>
<p style="margin-top:22px"><a class="btn btn-wa" href="{wa("Hi Kat! I'd like to ask about a face painting workshop for my group.")}" target="_blank" rel="noopener">Ask Kat about a workshop</a></p>
</div></section>
<section class="band band-light"><div class="wrap">
<p class="eyebrow">For grown-ups</p><h2>One-to-one and small-group lessons</h2>
<p>Want to learn face painting properly, or start your own face painting business? Kat teaches in person, one-to-one or in a small group, at a pace that suits you. One-to-one masterclasses and group lessons both last 3 hours and cover the painting and the business: everything you need to know to set up, build a website, market yourself, win work and keep your accounts in order.</p><p class="teachnote"><b>Taught by a real teacher.</b> Alongside The Painting Pixie, Kat is a qualified teacher of GCSE and A level students, so lessons are clear, well structured and paced for you, with plenty of hands-on practice and feedback.</p><div class="lprice"><div><b>£200</b><span>3-hour one-to-one masterclass with Kat</span></div><div><b>£150<small style="font-size:16px"> per person</small></b><span>3-hour small-group lessons, including the full business module</span></div></div>
<p class="incl"><b>Included in every lesson, one-to-one or group:</b> 3 hours with Kat · the full business module · a certificate of completion listing what you covered, to show your insurer · follow-up support by WhatsApp or phone while you get started</p>
<div class="fcards">
<div class="fcard"><h3>The foundations</h3><p>Kit, brushes, loading paint, clean lines and the core strokes every design is built on.</p></div>
<div class="fcard"><h3>Crowd-pleasing designs</h3><p>Butterflies, tigers, unicorns, superheroes and florals, step by step until you can paint them yourself.</p></div>
<div class="fcard"><h3>Glitter, gems &amp; stencils</h3><p>Finishing touches that make designs sparkle, and how to use them safely.</p></div>
<div class="fcard"><h3>Painting for a queue</h3><p>Working quickly and hygienically at parties and events, and keeping children happy in the chair.</p></div>
<div class="fcard"><h3>Turning it into a business</h3><p>Setting up, insurance and DBS, pricing, a website and social media, marketing yourself, finding venues and events, and keeping records for your tax return, all from Kat's own experience of building The Painting Pixie.</p></div>
</div><p class="small-note">The business side is practical, first-hand guidance from Kat, not formal tax or legal advice.</p>
<p style="margin-top:22px"><a class="btn btn-gold" href="{wa("Hi Kat! I'd like to ask about face painting lessons (one-to-one or small group).")}" target="_blank" rel="noopener">Book a one-to-one masterclass</a></p>
</div></section>
<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Questions about workshops or lessons?</h2>
<p>Message Kat and she'll get back to you, usually the same day.</p>
<a class="btn btn-gold" href="contact.html">Check my date</a></div></section>
{inner_layout.TRUST_BAND}
</main>'''
    page_from('services.html', 'workshops.html', 'Face Painting Workshops | Learn to Face Paint | The Painting Pixie',
              'Learn to face paint with Kat: children\'s workshops (next: Good Hotel London, Fri 30 Oct 2026, £15 per child), group workshops £200 three-hour one-to-one masterclasses and small-group lessons at £150 per person.',
              'https://paintingpixie.com/workshops.html',
              '<script type="application/ld+json">' + json.dumps(event, ensure_ascii=False) + '</script>\n',
              hero('../img/n-pumpkin-face.webp', '50% 30%', 'Workshops', 'Face Painting Workshops',
                   'Learn to face paint with Kat. Next up: a Half-Term Halloween Workshop at Good Hotel London.',
                   f'<a class="btn btn-gold" href="{tickets}" target="_blank" rel="noopener">Get tickets</a>'), main)

def corporate():
    service = {"@context": "https://schema.org", "@type": "Service", "serviceType": "Corporate and event face painting",
               "name": "Face painting and glitter for corporate and brand events",
               "provider": {"@type": "LocalBusiness", "@id": "https://paintingpixie.com/#business", "name": "The Painting Pixie"},
               "areaServed": ["Sussex", "Surrey", "London"],
               "description": "Face painting, glitter bars and arm art for staff fun days, summer parties, product launches, brand activations, weddings and festivals, with extra artists for large events."}
    main = f'''<main class="lg" id="content">
<section class="band band-dark"><div class="wrap evsplit">
<div><p class="eyebrow">For events that need a wow</p><h2>The queue everyone wants to join</h2>
<p>From staff summer parties to product launches and festivals, Kat brings statement face painting and glitter that guests talk about and share. She works fast, sets up neatly and keeps the line moving all day, and can bring extra artists for big crowds.</p>
<div class="evfacts"><div><b>Fast &amp; queue-friendly</b><span>Designs in minutes, so more guests take part.</span></div>
<div><b>Extra artists</b><span>A team for festivals and large events.</span></div>
<div><b>Your theme or colours</b><span>Designs matched to your event, outfits or brand colours.</span></div>
<div><b>Insured &amp; DBS checked</b><span>Insurance details and risk assessment on request.</span></div></div>
<p style="margin-top:22px"><a class="btn btn-gold" href="contact.html">Get a quote</a> <a class="btn btn-wa" href="{wa("Hi Kat! I'd like a quote for a corporate event. Date: Venue: Guests: ")}" target="_blank" rel="noopener">WhatsApp Kat</a></p></div>
<div class="evvideo"><video src="../img/kat-painting-loop.mp4" poster="../img/kat-painting-poster.webp" autoplay muted loop playsinline aria-label="Kat in rainbow glitter at an event"></video></div>
</div></section>
<section class="band band-light"><div class="wrap">
<p class="eyebrow">Perfect for</p><h2>Events Kat paints at</h2>
<div class="fcards">
<div class="fcard"><h3>Staff fun days &amp; summer parties</h3><p>A highlight for staff and their families, with designs for all ages.</p></div>
<div class="fcard"><h3>Product launches &amp; brand activations</h3><p>A photo-friendly activity that draws a crowd to your stand.</p></div>
<div class="fcard"><h3>Hotels, venues &amp; family days</h3><p>From hotel family events in London to garden parties at local venues.</p></div>
<div class="fcard"><h3>Festivals &amp; fêtes</h3><p>Glitter and face painting that keeps a festival queue happy.</p></div>
<div class="fcard"><h3>Weddings</h3><p>Entertains little guests and gets the grown-ups glittering too.</p></div>
<div class="fcard"><h3>Glitter tattoos</h3><p>Quick, mess-free stencil tattoos that keep a long queue moving and last beyond the event.</p></div>
</div></div></section>
<section class="band band-dark"><div class="wrap">
<p class="eyebrow">How it works</p><h2>From enquiry to event day</h2>
<ol class="steps"><li><b>Tell Kat about the event</b><span>Date, venue, guest numbers and any theme or brand colours.</span></li>
<li><b>Get a tailored quote</b><span>Hours, number of artists and anything extra, all agreed up front.</span></li>
<li><b>Paperwork sorted</b><span>Insurance details and risk assessment for your venue on request.</span></li>
<li><b>On the day</b><span>Kat arrives early, sets up neatly and keeps the queue moving.</span></li></ol>
</div></section>
<section class="band band-light"><div class="wrap"><h2>What event organisers say</h2><div class="testimonials"></div></div></section>
<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Planning an event?</h2>
<p>Tell Kat the date, venue and roughly how many guests, and she'll send a tailored quote. Kat travels further for weddings, festivals and corporate events.</p>
<a class="btn btn-gold" href="contact.html">Get a quote</a>
<form class="qform" action="https://formspree.io/f/mjgdnged" method="POST">
<input type="hidden" name="_subject" value="Website enquiry: Corporate &amp; brand events">
<input type="hidden" name="page" value="corporate-events.html">
<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
<div class="row2"><label>Name<input type="text" name="name" autocomplete="name" required></label><label>Company or organisation<input type="text" name="company"></label></div>
<div class="row2"><label>Email<input type="email" name="email" autocomplete="email" required></label><label>Phone<input type="tel" name="phone" autocomplete="tel" required></label></div>
<div class="row2"><label>Event date<input type="date" name="event-date" required></label><label>Expected guests<select name="guests" required><option value="">Choose one</option><option>Under 50</option><option>50–100</option><option>100–250</option><option>250+</option></select></label></div>
<label>Venue and town<input type="text" name="location" required></label>
<label>Tell Kat about your event<textarea name="message" rows="4" placeholder="e.g. Staff summer party, 120 guests, 2–5pm, brand colours pink and navy"></textarea></label>
<button type="submit">Get my quote →</button>
</form></div></section>
{inner_layout.TRUST_BAND}
</main>'''
    page_from('services.html', 'corporate-events.html', 'Corporate Event Face Painting &amp; Glitter | Sussex, Surrey &amp; London | The Painting Pixie',
              'Face painting and glitter for staff fun days, summer parties, product launches, festivals and weddings across Sussex, Surrey and London. Extra artists available.',
              'https://paintingpixie.com/corporate-events.html',
              '<script type="application/ld+json">' + json.dumps(service, ensure_ascii=False) + '</script>\n',
              hero('../img/n-arm-art-flowers-pair.webp', '50% 50%', 'Services · Events', 'Corporate &amp; Brand Event Face Painting',
                   'Statement face painting and glitter for staff parties, launches, festivals and weddings, with extra artists for big crowds.',
                   '<a class="btn btn-gold" href="contact.html">Get a quote</a>'), main)


def body_art():
    service = {"@context": "https://schema.org", "@type": "Service", "serviceType": "Body art and body painting",
               "name": "Body art and glitter body painting in Sussex, Surrey and London",
               "provider": {"@type": "LocalBusiness", "@id": "https://paintingpixie.com/#business", "name": "The Painting Pixie"},
               "areaServed": ["Sussex", "Surrey", "London"]}
    faqs = [("Is the body paint safe for skin?", "Yes. Kat uses professional, cosmetic-grade paints made for skin, and bio-glitter. If you have sensitive skin, a small patch test is a good idea."),
            ("How long does body art last?", "It lasts for the whole event, as long as it isn't rubbed or soaked. Lisa K's guests danced for hours at a wedding and their designs stayed perfect."),
            ("How do you remove it?", "The paints wash off with warm soapy water. Glitter and gems lift off gently."),
            ("Can you match a theme or brand colours?", "Yes. Tell Kat your theme, outfits or brand colours and she'll design around them.")]
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    gallery = ''.join(f'<img src="{g}" alt="{a}" loading="lazy">' for g, a in [
        ("../img/n-festival-rainbow-body-art.webp", "Rainbow body art with clouds and stars at a festival"),
        ("../img/v2-adult-tiger.webp", "Tiger eye design with glitter at a summer festival"),
        ("../img/n-arm-glitter-swirl.webp", "Rainbow glitter swirl arm art"),
        ("../img/n-arm-art-flowers-pair.webp", "Floral arm art on two guests"),
        ("../img/n-adult-pink-glitter-event.webp", "Pink glitter face art at an event"),
        ("../img/n-lilac-flower-eye.webp", "Lilac flower design with rose-gold glitter")])
    faq_html = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    main = f"""<main class="lg" id="content">
<section class="band band-light"><div class="wrap">
<p class="eyebrow">Body art</p><h2>Wearable art for festivals, Pride and events</h2>
<p>Body art takes face painting further: rainbows across the chest, flowing designs down the arm, florals over the shoulder, finished with chunky bio-glitter and gems. It's a show-stopper at festivals, Pride, hen dos, themed parties and brand events, and it looks amazing in photos.</p>
<div class="fcards">
<div class="fcard"><h3>Festivals &amp; Pride</h3><p>Rainbows, stars and glitter clouds that make a festival outfit.</p></div>
<div class="fcard"><h3>Arm &amp; shoulder art</h3><p>Flowing florals and swirls, quick enough for a queue of guests.</p></div>
<div class="fcard"><h3>Hen dos &amp; parties</h3><p>Matching designs for the whole group, from subtle to full sparkle.</p></div>
<div class="fcard"><h3>Photoshoots &amp; brand events</h3><p>Designs built around your theme, outfits or brand colours.</p></div>
<div class="fcard"><h3>Glitter tattoos</h3><p>Stencil tattoos in cosmetic glitter, a quick add-on that lasts beyond the day.</p></div>
</div></div></section>
<section class="band band-dark"><div class="wrap"><h2>Recent body art</h2><div class="gstrip">{gallery}</div></div></section>
<section class="band band-light"><div class="wrap"><h2>What people say</h2><div class="testimonials"></div></div></section>
<section class="band band-dark"><div class="wrap"><h2>Good to know</h2><div class="faqlist">{faq_html}</div></div></section>
<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Book body art for your event</h2>
<p>Tell Kat your date, venue and roughly how many people would like body art, and she'll send a quote.</p>
<a class="btn btn-gold" href="contact.html">Check my date</a><a class="btn btn-wa" href="{wa("Hi Kat! I'd like to ask about body art for an event. Date: Venue: People: ")}" target="_blank" rel="noopener">WhatsApp Kat</a></div></section>
{inner_layout.TRUST_BAND}
</main>"""
    page_from('services.html', 'body-art.html', 'Body Art &amp; Body Painting | Festivals, Pride &amp; Events | The Painting Pixie',
              'Glitter body art, arm art and body painting for festivals, Pride, hen dos, photoshoots and brand events across Sussex, Surrey and London. 5.0 rated.',
              'https://paintingpixie.com/body-art.html',
              '<script type="application/ld+json">' + json.dumps(service, ensure_ascii=False) + '</script>\n<script type="application/ld+json">' + json.dumps(faq_schema, ensure_ascii=False) + '</script>\n',
              hero('../img/n-festival-rainbow-body-art.webp', '50% 40%', 'Services · Grown-ups', 'Body Art &amp; Body Painting',
                   'Rainbows, florals and glitter, painted on arms, shoulders and chests for festivals, Pride, hen dos and events.',
                   '<a class="btn btn-gold" href="contact.html">Check my date</a>'), main)

def christmas():
    service = {"@context": "https://schema.org", "@type": "Service", "serviceType": "Christmas face painting",
               "name": "Christmas face painting and glitter in Sussex and Surrey",
               "provider": {"@type": "LocalBusiness", "@id": "https://paintingpixie.com/#business", "name": "The Painting Pixie"},
               "areaServed": ["Sussex", "Surrey"]}
    faqs = [("When should I book Christmas face painting?", "As early as you can. December weekends are the busiest time of Kat's year after Halloween, and Saturdays usually go first. Send your date and Kat will let you know straight away if she's free."),
            ("Do you paint at school and PTA Christmas fairs?", "Yes. Kat can run a face painting stall where families pay per face, or come for a set fee. Fast, queue-friendly Christmas designs keep the line moving."),
            ("Can you come to an office or staff Christmas party?", "Yes. Glitter, gems and glitter tattoos are a hit with grown-ups, and a kids' corner works brilliantly at family Christmas events. Ask for a quote."),
            ("Can you work alongside Santa's grotto?", "Yes. Face painting is a lovely way to keep children happy while they queue for Santa at garden centres, farms and community events."),
            ("What Christmas designs do you paint?", "Reindeer, snowmen, elves, Christmas puddings, snowflake queens, candy canes, gingerbread, Christmas trees and lots of sparkly stars, plus the classic tigers and unicorns for anyone who wants them.")]
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    faq_html = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    designs = [("Rudolph", "#C8102E"), ("Snowflake queen", "#4FB6FF"), ("Cheeky elf", "#2E9E5B"), ("Snowman", "#9FD3FF"), ("Christmas pudding", "#7A4A2A"),
               ("Candy cane", "#E3324A"), ("Gingerbread", "#B5733C"), ("Christmas tree", "#1F7A45"), ("Golden star", "#E2BE7A"), ("Frosty glitter", "#A77BFF")]
    chips = ''.join(f'<li style="--c:{c}">{n}</li>' for n, c in designs)
    gallery = ''.join(f'<img src="{g}" alt="{a}" loading="lazy">' for g, a in [
        ("blue-shooting-stars-face-paint-for-girls.webp", "Icy blue shooting stars with silver glitter"),
        ("blue-snowflake-crown-face-paint-for-girls.webp", "Snow queen crown with gems"),
        ("fire-and-ice-dragon-eye-face-paint.webp", "Fire and ice dragon eye design"),
        ("../img/n-lilac-flower-eye.webp", "Frosty lilac flower with rose-gold glitter")])
    main = f"""<main class="lg" id="content">
<section class="band band-light"><div class="wrap">
<p class="eyebrow">Christmas</p><h2>A sprinkle of Christmas magic</h2>
<p>From Christmas birthday parties to school fairs, Santa's grottos and office parties, Kat brings the sparkle. Reindeer noses, snowflake queens, cheeky elves and lots of glitter, painted quickly so every child gets their favourite before the mince pies run out.</p>
<div class="fcards">
<div class="fcard"><h3>Christmas parties</h3><p>Birthday and Christmas parties at home or in a hall. Classic Party from £130, Ultimate Sparkle from £160.</p></div>
<div class="fcard"><h3>School &amp; PTA fairs</h3><p>A face painting stall that raises money and keeps the queue moving. Per-face or a set fee.</p></div>
<div class="fcard"><h3>Santa's grottos &amp; markets</h3><p>Garden centres, farms, Christmas markets and light trails, keeping families happy while they wait.</p></div>
<div class="fcard"><h3>Office &amp; staff parties</h3><p>Glitter, gems and glitter tattoos for grown-ups, or a kids' corner for family events.</p></div>
<div class="fcard"><h3>New Year's Eve</h3><p>Glitter and gems for party looks that sparkle at midnight.</p></div>
</div></div></section>
<section class="band band-dark"><div class="wrap"><h2>Christmas designs</h2>
<p>A few favourites. Kat will paint whatever your little elves ask for.</p>
<ul class="xmas-designs">{chips}</ul></div></section>
<section class="band band-light"><div class="wrap"><h2>Frosty, sparkly looks</h2><div class="gstrip">{gallery}</div>
<p class="small-note">Draft note: Kat's Christmas photos will go here once she has them.</p></div></section>
<section class="band band-dark"><div class="wrap"><h2>Book early for December</h2>
<p>December weekends fill up fast, especially the Saturdays before Christmas. Send Kat your date now, even if the details aren't fixed yet.</p></div></section>
<section class="band band-light"><div class="wrap"><h2>Christmas questions</h2><div class="faqlist">{faq_html}</div></div></section>
<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Is Kat free on your Christmas date?</h2>
<p>Tell Kat your date, town and roughly how many children or guests. She usually replies the same day.</p>
<a class="btn btn-gold" href="contact.html">Check my date</a><a class="btn btn-wa" href="{wa("Hi Kat! I'd like to book Christmas face painting. Date: Town: Guests: ")}" target="_blank" rel="noopener">WhatsApp Kat</a></div></section>
{inner_layout.TRUST_BAND}
</main>"""
    css = '<style>.xmas-designs{list-style:none;padding:0;margin:20px 0 0;display:flex;flex-wrap:wrap;gap:12px}.xmas-designs li{padding:12px 20px;border-radius:999px;background:var(--panel);border:1px solid var(--line);border-left:8px solid var(--c);font-weight:700}</style>\n'
    page_from('services.html', 'christmas-face-painting.html', 'Christmas Face Painting in Sussex &amp; Surrey | Parties, Fairs &amp; Grottos | The Painting Pixie',
              'Christmas face painting for parties, school fairs, Santa\'s grottos and office parties across Sussex and Surrey. Reindeer, elves, snowflakes and glitter. Book early for December.',
              'https://paintingpixie.com/christmas-face-painting.html',
              css + '<script type="application/ld+json">' + json.dumps(service, ensure_ascii=False) + '</script>\n<script type="application/ld+json">' + json.dumps(faq_schema, ensure_ascii=False) + '</script>\n',
              hero('blue-shooting-stars-face-paint-for-girls.webp', '50% 30%', 'Services · Christmas', 'Christmas Face Painting',
                   'Reindeer, snowflakes, elves and glitter for Christmas parties, school fairs, grottos and office parties across Sussex and Surrey.',
                   '<a class="btn btn-gold" href="contact.html">Check my date</a>'), main)

def prices():
    groups = [
      ("Children’s parties", "Birthday parties at home, in a hall or a garden.", [
        ("Classic Party", "From £130", ["2 hours of face painting", "Fast, fun party designs", "Kids choose from Kat’s design board"], False),
        ("Ultimate Sparkle", "From £160", ["3 hours of face painting", "Bio-glitter, face gems and more detailed designs", "Most popular for bigger parties"], True)]),
      ("Grown-ups", "Hen dos, milestone birthdays and grown-up celebrations.", [
        ("Hen &amp; adult parties", "From £150", ["Glitter, gems and grown-up designs", "At your house, venue or hotel", "Great for photos"], False),
        ("Glitter tattoos", "Add-on or quote", ["Stencil tattoos in cosmetic glitter", "Quick and mess-free, last for days", "Great for queues and toddlers"], False)]),
      ("Events", "Weddings, festivals, school fairs, corporate and brand events.", [
        ("Weddings &amp; festivals", "Bespoke quote", ["Hourly or day rates", "Extra artists for big crowds", "Kids’ corner or glitter for all"], False),
        ("Corporate &amp; brand events", "Bespoke quote", ["Staff days, launches and activations", "Brand colours and themes", "Sussex, Surrey and London"], False)]),
      ("Learn to face paint", "Taught by Kat, a qualified GCSE and A level teacher.", [
        ("Children’s workshops", "£15 per child", ["Fun, hands-on sessions", "Paints, stencils and glitter", "Ask about group bookings"], False),
        ("Small-group lessons", "£150 per person", ["3 hours with Kat", "Full business module", "Certificate and follow-up support"], False),
        ("One-to-one masterclass", "£200", ["3 hours, just you and Kat", "Painting and the business side", "Certificate and follow-up support"], True)]),
    ]
    out = ''
    for title, lede, cards in groups:
        cs = ''.join(f'<article class="pcard2{" hi" if hi else ""}"><h3>{n}</h3><div class="pp2">{pr}</div><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></article>' for n, pr, items, hi in cards)
        out += f'<div class="pgroup"><h2>{title}</h2><p class="lede-s">{lede}</p><div class="pcards2">{cs}</div></div>'
    css = """<style>
.pgroup{margin:0 0 46px}.pgroup h2{margin-bottom:4px}
.pcards2{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;margin-top:16px}
.pcard2{background:#fff;border:1px solid #E8DED3;border-radius:16px;padding:22px 22px 18px;box-shadow:0 14px 30px -24px rgba(60,30,40,.45)}
.pcard2.hi{border:2px solid var(--pink,#FF4FA3)}
.pcard2 h3{margin:0;font-family:Fraunces,serif;font-weight:400;font-size:24px;color:#1B1712}
.pp2{font-family:Fraunces,serif;font-size:30px;color:#B8892E;margin:6px 0 10px}
.pcard2 ul{margin:0;padding-left:18px;color:#4E463F;font-size:15px}
.pcard2 li{margin:4px 0}
</style>
"""
    offers = {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "The Painting Pixie prices",
              "itemListElement": [{"@type": "Offer", "name": re.sub("&amp;", "&", n), "description": "; ".join(items), "priceCurrency": "GBP", **({"price": re.sub(r"[^0-9]", "", pr.split()[1] if pr.startswith("From") else pr.split()[0])} if "£" in pr else {})}
                                  for _, _, cards in groups for n, pr, items, _ in cards]}
    main = f"""<main class="lg" id="content">
<section class="band band-light"><div class="wrap">
<p class="eyebrow">Prices</p><h2 style="margin-bottom:6px">Simple, clear prices</h2>
<p class="lede-s">Every price is confirmed for your date when you enquire. There’s no obligation, and no payment to enquire.</p>
<div style="margin-top:34px">{out}</div>
{INCLUDED_HTML}
<p class="small-note">A small deposit secures your date. Travel is included within about 40 minutes of Horsham.</p>
</div></section>
<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Is Kat free on your date?</h2>
<p>Tell Kat your date, town and roughly how many guests. She usually replies the same day.</p>
<a class="btn btn-gold" href="contact.html">Check my date</a><a class="btn btn-wa" href="{wa("Hi Kat! I'd like a price for face painting. Date: Town: Guests: ")}" target="_blank" rel="noopener">WhatsApp Kat</a></div></section>
{inner_layout.TRUST_BAND}
</main>"""
    page_from('services.html', 'prices.html', 'Face Painting Prices | Kids’ Parties, Hens &amp; Events | The Painting Pixie',
              'Face painting prices in Sussex and Surrey: kids’ parties from £130, hen parties from £150, workshops, masterclasses and bespoke event quotes. Insured and DBS checked.',
              'https://paintingpixie.com/prices.html',
              css + '<script type="application/ld+json">' + json.dumps(offers, ensure_ascii=False) + '</script>\n',
              hero('../img/g/rainbow-laughing-1600.webp', '70% 40%', 'Prices', 'Face Painting Prices',
                   'Kids’ parties, hen dos, events and lessons. Clear prices, confirmed for your date.',
                   '<a class="btn btn-gold" href="contact.html">Check my date</a>'), main)

INCLUDED_HTML = ('<div class="incl" style="margin-top:6px"><b>Every booking includes</b><ul>'
                 '<li>All equipment, brought by Kat</li><li>Set-up and pack-away</li>'
                 '<li>Professional, skin-safe paints</li><li>Fully insured &amp; DBS checked</li>'
                 '<li>A design board for children to choose from</li></ul></div>')

def reviews():
    import reviews_data as R
    from datetime import datetime
    when = lambda d: datetime.strptime(d, '%b %Y')
    items = [dict(src='ate', name=n, date=d, title=t, paras=p, tags=g) for n, d, t, p, g in R.ATE]
    items += [dict(src='google', name=n, date=d, title=None, paras=p, tags=g) for n, d, p, g in R.GOOGLE]
    items.sort(key=lambda r: when(r['date']), reverse=True)   # stable: keeps each site's own order within a month
    n_ate, n_g = len(R.ATE), len(R.GOOGLE) + R.GOOGLE_STAR_ONLY
    total = n_ate + n_g
    cards = ''
    for r in items:
        badge = ('<span class="rsrc ate">Verified booking · Add to Event</span>' if r['src'] == 'ate'
                 else '<span class="rsrc g">Google review</span>')
        title = f'<h3>{esc(r["title"])}</h3>' if r['title'] else ''
        body = ''.join(f'<p>{esc(x)}</p>' for x in r['paras'])
        cards += (f'<figure class="rcard" data-tags="{r["tags"]}"><div class="rtop"><span class="rstars" aria-label="5 out of 5 stars">★★★★★</span>{badge}</div>'
                  f'{title}<blockquote>{body}</blockquote><figcaption><b>{esc(r["name"])}</b> · {r["date"]}</figcaption></figure>')
    count = lambda tag: sum(1 for r in items if tag in r['tags'].split())
    chips = (f'<button class="rchip on" data-f="all">All ({len(items)})</button>'
             + ''.join(f'<button class="rchip" data-f="{t}">{lbl} ({count(t)})</button>'
                       for t, lbl in [('kids', 'Children’s parties'), ('grownups', 'Grown-ups'), ('wedding', 'Weddings'), ('events', 'Events &amp; corporate')]))
    css = """<style>
.rsum{display:grid;grid-template-columns:auto 1fr 1fr;gap:18px;align-items:stretch;margin:6px 0 30px}
.rbig{background:#1B1712;color:#fff;border-radius:18px;padding:22px 30px;text-align:center}
.rbig b{display:block;font-family:Fraunces,serif;font-weight:400;font-size:64px;line-height:1;color:#fff!important}
.rbig span{color:#F2C14E;letter-spacing:3px;font-size:20px}.rbig small{display:block;color:#D9CFC4;font-size:14px;margin-top:4px}
.rsite{background:#fff;border:1px solid #E8DED3;border-radius:18px;padding:20px 22px;display:flex;flex-direction:column;gap:6px;box-shadow:0 14px 30px -24px rgba(60,30,40,.45)}
.rsite b{font-family:Fraunces,serif;font-weight:400;font-size:24px;color:#1B1712}.rsite span{color:#4E463F;font-size:15px}
.rsite a{font-weight:700;margin-top:auto}
.rchips{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 22px}
.rchip{font:700 15px Manrope,system-ui,sans-serif;border:2px solid #1B1712;background:#fff;color:#1B1712;border-radius:999px;padding:8px 16px;cursor:pointer}
.rchip.on{background:#1B1712;color:#fff}
.rgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;align-items:start}
.rcard{margin:0;background:#fff;border-radius:16px;padding:22px 24px;border-top:5px solid var(--pink,#FF4FA3);box-shadow:0 14px 30px -24px rgba(60,30,40,.45)}
.rcard:nth-child(4n+2){border-top-color:var(--teal,#2FD4C4)}.rcard:nth-child(4n+3){border-top-color:var(--violet,#8B5CF6)}.rcard:nth-child(4n){border-top-color:var(--gold,#E2BE7A)}
.rtop{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:8px;margin-bottom:10px}
.rstars{color:#E0A100;letter-spacing:2px;font-size:17px}
.rsrc{font-size:11.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;border-radius:999px;padding:4px 10px}
.rsrc.ate{background:#FFF0D6;color:#7A4E00}.rsrc.g{background:#E6F0FF;color:#1A4DA8}
.rcard h3{margin:0 0 6px;font-family:Fraunces,serif;font-weight:400;font-size:21px;color:#1B1712}
.rcard blockquote{margin:0}.rcard blockquote p{margin:0 0 8px!important;color:#3A322C!important;font-size:16px;line-height:1.55}
.rcard figcaption{color:#6B5F57;font-size:14.5px;margin-top:8px}.rcard figcaption b{color:#1B1712}
.rcard[hidden]{display:none}
.rnote{color:#6B5F57;font-size:14px;margin-top:10px}
@media(max-width:760px){.rsum{grid-template-columns:1fr}.rbig{display:flex;align-items:center;justify-content:center;gap:14px;padding:16px}.rbig b{font-size:48px}.rbig small{margin:0}}
</style>
"""
    js = """<script>document.querySelectorAll('.rchip').forEach(b=>b.addEventListener('click',()=>{const f=b.dataset.f;
document.querySelectorAll('.rchip').forEach(x=>x.classList.toggle('on',x===b));
document.querySelectorAll('.rcard').forEach(c=>c.hidden=!(f==='all'||c.dataset.tags.split(' ').includes(f)));}));</script>"""
    main = f"""<main class="lg" id="content">
<section class="band band-light"><div class="wrap">
<p class="eyebrow">Reviews</p><h2 style="margin-bottom:6px">Every review, word for word</h2>
<p class="lede-s">All {total} ratings Kat has received are five stars. Here is every written review from Add to Event and Google, newest first, exactly as the customers wrote them.</p>
<div class="rsum">
<div class="rbig"><b>5.0</b><span>★★★★★</span><small>{total} reviews</small></div>
<div class="rsite"><b>Add to Event</b><span>{n_ate} reviews, all 5 stars. Every one is from a confirmed booking.</span><a href="{R.ATE_URL}" target="_blank" rel="noopener">See them on Add to Event →</a></div>
<div class="rsite"><b>Google</b><span>{n_g} reviews, all 5 stars.</span><a href="{R.GOOGLE_URL}" target="_blank" rel="noopener">See them on Google →</a></div>
</div>
<div class="rchips" role="group" aria-label="Filter reviews">{chips}</div>
<div class="rgrid">{cards}</div>
<p class="rnote">{R.GOOGLE_STAR_ONLY} more Google customers left five stars without a comment. Reviews are shown as written, including any typos.</p>
</div></section>
<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Want Kat at your party?</h2>
<p>Tell Kat your date, town and roughly how many guests. She usually replies the same day.</p>
<a class="btn btn-gold" href="contact.html">Check my date</a><a class="btn btn-wa" href="{wa("Hi Kat! I've read your reviews and would like to check a date. Date: Town: Guests: ")}" target="_blank" rel="noopener">WhatsApp Kat</a></div></section>
{inner_layout.TRUST_BAND}
</main>{js}"""
    page_from('services.html', 'reviews.html', f'Reviews | 5.0 from {total} Reviews | The Painting Pixie Face Painting',
              f'Read all {total} five-star reviews of Kat, The Painting Pixie: face painting for children’s parties, weddings, hen dos and events across Sussex and Surrey.',
              'https://paintingpixie.com/reviews.html', css,
              hero('../img/g/unicorn-party-1600.webp', '50% 30%', 'Reviews', 'Reviews',
                   f'5.0 from {total} reviews on Add to Event and Google. Read what families and event organisers say.',
                   '<a class="btn btn-gold" href="contact.html">Check my date</a>'), main)

def build():
    services(); workshops(); corporate(); body_art(); christmas(); prices(); reviews()
    print('extra pages built: services, workshops, corporate-events, body-art')

if __name__ == '__main__':
    build()
