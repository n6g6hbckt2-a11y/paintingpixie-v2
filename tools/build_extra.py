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
 ("Animal print", "../img/n-tiger-girl-closeup.webp", "50% 35%", "Bold tigers, leopards and butterflies for kids and grown-ups.", "Included in packages", "animal-print-face-painting.html", "See the designs"),
 ("Body art", "rainbow-chest-paint-with-glitter-clouds.webp", "50% 40%", "Painted body art and flowing arm designs with glitter, for festivals, Pride, photoshoots and themed events.", "Bespoke quote", "contact.html", "Ask about body art"),
 ("Halloween & seasonal", "../img/n-pumpkin-face.webp", "50% 30%", "Pumpkins, skulls, devils and monsters, from sweet to spooky. Christmas fairs too.", "From £130", "halloween-face-painting.html", "Halloween"),
 ("Festivals, fêtes & community days", "../img/v2-hero.webp", "60% 35%", "Fast, queue-friendly designs for school fairs, village fêtes and festivals, as a stall or a set fee.", "Bespoke quote", "contact.html", "Get a quote"),
 ("Learn to face paint", "../img/kat-painting-poster.webp", "50% 40%", "Workshops for children and groups: design and paint faces, arms and hands with stencils and glitter.", "From £15 per child", "workshops.html", "Workshops"),
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
<p>Hands-on sessions where children (and grown-ups!) learn to design and paint faces, arms and hands, using the same professional paints, stencils and glitter Kat uses at parties.</p>
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
<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Questions about workshops?</h2>
<p>Message Kat and she'll get back to you, usually the same day.</p>
<a class="btn btn-gold" href="contact.html">Check my date</a></div></section>
{inner_layout.TRUST_BAND}
</main>'''
    page_from('services.html', 'workshops.html', 'Face Painting Workshops | Learn to Face Paint | The Painting Pixie',
              'Learn to face paint with Kat. Next: Half-Term Halloween Workshop at Good Hotel London, Fri 30 Oct 2026, £15 per child. Group workshops on request.',
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
              hero('../img/n-arm-art-flowers-pair.webp', '50% 50%', 'Occasions · Events', 'Corporate &amp; Brand Event Face Painting',
                   'Statement face painting and glitter for staff parties, launches, festivals and weddings, with extra artists for big crowds.',
                   '<a class="btn btn-gold" href="contact.html">Get a quote</a>'), main)

def build():
    services(); workshops(); corporate()
    print('extra pages built: services, workshops, corporate-events')

if __name__ == '__main__':
    build()
