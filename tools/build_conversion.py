# -*- coding: utf-8 -*-
"""Conversion improvements applied across the whole draft (runs last):
1 'Check my date' as the main button   2 no-obligation reassurance by every form
3 number-of-children choice + example  4 contact page as the final booking step
5 'what's included' on prices          6 short real review quotes by booking buttons
7 GA4 form_start event so the full enquiry journey can be measured."""
import re, glob, os

OUT = '/home/claude/paintingpixie-v2/draft'

REASSURE = ('<p class="reassure"><span aria-hidden="true">🔒</span> <b>No obligation, and no payment to enquire.</b> '
            'Kat checks her diary and replies with availability and the best option for your party, usually the same day.</p>')

CHILDREN = ('<label>How many children?<select name="children" required>'
            '<option value="">Choose one</option><option>Under 10</option><option>10–15</option>'
            '<option>16–25</option><option>25+</option><option>Adults / hen party</option></select></label>')

EXAMPLE = 'e.g. 6th birthday, 18 children, Horsham, 2–4pm, unicorn theme'

INCLUDED = ('<div class="incl"><b>Every booking includes</b><ul>'
            '<li>All equipment, brought by Kat</li><li>Set-up and pack-away</li>'
            '<li>Professional, skin-safe paints</li><li>Fully insured &amp; DBS checked</li>'
            '<li>A design board for children to choose from</li></ul></div>')

# word-for-word extracts from real reviews on the live site
QUOTES = [  # word-for-word from real reviews
    ('At times there were people literally sprinting to get to her', 'Lisa K, wedding, Brighton'),
    ('So patient with a big group of excited kids', 'Liam, Horsham'),
    ('Everyone was so complimentary of the amazing face paints!', 'Daniel C, 4th birthday'),
]
QUOTE_STRIP = '<div class="qstrip">' + ''.join(
    f'<figure><span aria-hidden="true">★★★★★</span><blockquote>“{q}”</blockquote><figcaption>{n}</figcaption></figure>' for q, n in QUOTES) + '</div>'

WA_TEMPLATE = ("https://wa.me/447852300125?text=" +
               "Hi%20Kat!%20I'd%20like%20to%20check%20a%20date.%0A%F0%9F%93%85%20Date%3A%20%0A%F0%9F%93%8D%20Town%3A%20%0A%F0%9F%91%A7%20Number%20of%20children%3A%20")

CTA_TEXT = [
    (r'>(?:📅\s*)?Check Availability<', '>Check my date<'),
    (r'>Check availability<', '>Check my date<'),
    (r'>Book Your Date<', '>Check my date<'),
    (r'>📅 Book Your Event<', '>Check my date<'),
    (r'>Book The Painting Pixie</a>', '>Check my date</a>'),
    (r'>Check a date<', '>Check my date<'),
    (r'>Send Booking Request ✨<', '>Check my date →<'),
    (r'>Send my enquiry<', '>Check my date →<'),
]

CSS = r'''
/* ===== Conversion helpers ===== */
.reassure{max-width:760px;margin:14px auto 0!important;padding:14px 18px;border-radius:12px;background:rgba(47,212,196,.12);border:1px solid rgba(47,212,196,.4);color:var(--ink)!important;font-size:15px!important;text-align:left}
.reassure b{color:var(--ink)}
.band-light .reassure{color:#1B1712!important;background:#E7F7F3;border-color:#9ADBCF}.band-light .reassure b{color:#1B1712}
.qstrip{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;max-width:980px;margin:28px auto 0;text-align:left}
.qstrip figure{margin:0;background:rgba(255,255,255,.06);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.qstrip span{color:var(--gold);letter-spacing:2px;font-size:13px}
.qstrip blockquote{margin:6px 0 8px;font-family:'Fraunces',serif;font-size:18px;line-height:1.35;color:var(--ink)}
.qstrip figcaption{font-size:13px;font-weight:700;color:var(--muted)}
.band-light .qstrip figure{background:#fff;border-color:#E8DED3}.band-light .qstrip blockquote{color:#1B1712}.band-light .qstrip figcaption{color:#6B5F57}
.incl{max-width:980px;margin:22px auto 0;padding:18px 22px;border-radius:14px;background:rgba(255,255,255,.07);border:1px dashed rgba(226,190,122,.6);text-align:left}
.incl b{color:var(--gold);font-size:14px;letter-spacing:1.4px;text-transform:uppercase}
.incl ul{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px 22px}
.incl li{color:var(--ink);font-size:15px}.incl li::before{content:"✓ ";color:var(--teal);font-weight:800}
.band-light .incl{background:#fff}.band-light .incl li{color:#1B1712}
.wa-steps{margin:18px 0 0;padding:16px 18px;border-radius:12px;background:rgba(37,211,102,.1);border:1px solid rgba(37,211,102,.4)}
.wa-steps p{margin:0 0 8px!important;color:var(--ink)!important}
.wa-steps ul{margin:0 0 12px;padding-left:4px;list-style:none;color:var(--ink)}
.wa-steps li{padding:2px 0}
.lg select{appearance:auto}
@media(max-width:800px){.qstrip{grid-template-columns:1fr}}
'''

FORM_START_JS = '''
// GA4: count when someone starts filling in a booking form (form_start), alongside booking_request on submit
document.addEventListener('focusin', function(e) {
  var f = e.target.closest && e.target.closest('form');
  if (!f || f.dataset.started) return;
  f.dataset.started = '1';
  gtag('event', 'form_start', {'page_path': location.pathname, 'form_destination': f.action || ''});
});
'''

def patch_form(m):
    form = m.group(0)
    if 'name="children"' not in form:
        # put the children choice just before the free-text box
        form = re.sub(r'(<label[^>]*>(?:Tell Kat about your event|Event Details)?)', lambda x: x.group(1), form)
        idx = form.find('<label for="message"')
        if idx == -1: idx = form.find('<label>Tell Kat about your event')
        if idx != -1: form = form[:idx] + CHILDREN + '\n' + form[idx:]
    form = form.replace('Tell Kat about your event', 'Tell Kat about your party')
    form = form.replace('>Event Details<', '>Tell Kat about your party<')
    form = re.sub(r'placeholder="(Tell me about your event[^"]*|Number of children or guests, ages, theme\.\.\.)"', f'placeholder="{EXAMPLE}"', form)
    return form

def patch(path):
    s = open(path).read()
    page = os.path.basename(path)
    for pat, rep in CTA_TEXT:
        s = re.sub(pat, rep, s)
    # forms
    s = re.sub(r'<form[^>]*formspree[^>]*>.*?</form>', patch_form, s, flags=re.S)
    if 'class="reassure"' not in s:
        s = re.sub(r'(</form>)', r'\1' + REASSURE, s, count=1)
    # quotes beside the booking buttons (final booking band on inner pages, final CTA on the homepage)
    if 'class="qstrip"' not in s:
        if 'k-enquire' in s:
            s = re.sub(r'(<section class="[^"]*k-enquire[^"]*"><div class="wrap">.*?)(<form)', lambda m: m.group(1) + QUOTE_STRIP + m.group(2), s, count=1, flags=re.S)
        elif page == 'index.html':
            s = re.sub(r'(<section class="cta">.*?<div class="ctas">.*?</div>)', lambda m: m.group(1) + QUOTE_STRIP, s, count=1, flags=re.S)
    # what's included, after the first set of price cards
    if 'class="incl"' not in s:
        if page == 'index.html':
            s = s.replace('<p class="price-note">', INCLUDED + '<p class="price-note">', 1)
        else:
            s = re.sub(r'(<div class="pcards">.*?</div></div>)(\s*<p class="small-note">)', lambda m: m.group(1) + INCLUDED + m.group(2), s, count=1, flags=re.S)
            if 'class="incl"' not in s and 'class="packages-grid"' in s:
                s = re.sub(r'(<div class="packages-grid">.*?</div>\s*</div>\s*</div>)', lambda m: m.group(1) + INCLUDED, s, count=1, flags=re.S)
    if page == 'contact.html':
        s = contact(s)
    open(path, 'w').write(s)

def contact(s):
    s = re.sub(r'(<header class="phero">.*?<h1>).*?(</h1>\s*)<p>.*?</p>',
               lambda m: m.group(1) + 'Let’s make your party amazing' + m.group(2) +
               '<p>Book The Painting Pixie for parties, weddings and events across Sussex &amp; Surrey. Tell Kat a little about your event and she’ll check her diary and suggest the best option.</p>',
               s, count=1, flags=re.S)
    s = s.replace('<h2>Booking Request</h2>', '<h2>Check your date</h2>')
    s = s.replace('<h2>Quick Contact</h2>', '<h2>Prefer WhatsApp?</h2>')
    wa_block = ('<div class="wa-steps"><p>Sometimes a quick message is easier. Send Kat:</p>'
                '<ul><li>📅 Your date</li><li>📍 Your town or venue</li><li>👧 Number of children</li></ul>'
                f'<a class="btn btn-wa" href="{WA_TEMPLATE}" target="_blank" rel="noopener">Message Kat on WhatsApp</a></div>')
    s = re.sub(r'<a class="btn btn-wa"\s*href="https://wa\.me/447852300125\?text=Hi%20I\'d%20like%20to%20book%20a%20party"\s*target="_blank">\s*💬 Message on WhatsApp\s*</a>', wa_block, s, count=1)
    # prices in the side card: list what's included
    s = re.sub(r'(<div class="package-summary">.*?</div>)', lambda m: m.group(1) + INCLUDED, s, count=1, flags=re.S)
    if 'class="qstrip"' not in s:
        s = re.sub(r'(</form>.*?</section>)', lambda m: m.group(1) + '<section class="band band-light centred"><div class="wrap"><h2>What families say</h2>' + QUOTE_STRIP + '</div></section>', s, count=1, flags=re.S)
    return s

def build():
    with open(f'{OUT}/site.css', 'a') as f: f.write(CSS)
    with open(f'{OUT}/site.js', 'a') as f: f.write(FORM_START_JS)
    for p in glob.glob(OUT + '/*.html'):
        if 'http-equiv="refresh"' in open(p).read(): continue
        patch(p)
    print('conversion changes applied')


# ---------- Latest verified reviews from Add to Event (add new ones to the top of this list) ----------
LATEST_REVIEWS = [
    dict(name='Bethany S', occasion="Son's birthday party", date='25 Aug 2026', pages=('index.html', 'childrens-face-painting.html', 'contact.html'),
         text="Absolutely amazing face painter! She came to my son’s birthday party and was brilliant with all the children. "
              "The children absolutely loved choosing their designs and were so excited with the finished results. "
              "She was professional, reliable and added such a lovely touch to the party. I would definitely recommend her "
              "to anyone looking for a face painter for a children’s party. Thank you so much!"),
    dict(name='Olivia W', occasion='Wedding', date='6 Jul 2026', pages=('index.html', 'contact.html'),
         text="Brilliant. We used [Kat] for our wedding to entertain kids – she was so good, the kids absolutely loved it… Would definitely use again."),
    dict(name='Louise R', occasion='“Kat is amazing, book her with confidence”', date='2 Jun 2026', pages=('index.html', 'contact.html'),
         text="Kat was fantastic, great communication, great service and fair price… everyone commented that [it] was some of the best they have seen."),
    dict(name='Hina T', occasion="Son's first birthday", date='30 Jan 2026', pages=('childrens-face-painting.html',),
         text="She was friendly, patient, and brilliant with the children, making everyone feel comfortable and included. The face painting was beautiful, creative, and done with great care using safe products. All the kids loved it, and even the parents were impressed!"),
]
ATE = 'https://www.addtoevent.co.uk/suppliers/the-painting-pixie-ltd'
LATEST_CSS = r'''
.latest-wrap{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:16px;margin:16px 0 0}
.latest{margin:0;text-align:left;background:linear-gradient(135deg,rgba(255,79,163,.14),rgba(47,212,196,.10));border:1px solid rgba(226,190,122,.45);border-radius:18px;padding:26px 28px;position:relative}
.latest .lbadge{display:inline-flex;align-items:center;gap:10px;font-size:12px;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;color:var(--gold)}
.latest .lbadge img{width:44px;height:auto;border-radius:4px}
.latest blockquote{margin:12px 0;font-family:'Fraunces',serif;font-size:18px;line-height:1.5;color:var(--ink)}
.latest figcaption{font-size:14px;color:var(--muted)}.latest figcaption b{color:var(--ink)}
.latest figcaption a{font-weight:700}
.band-light .latest blockquote,.band-light .latest figcaption b{color:#1B1712}.band-light .latest figcaption{color:#6B5F57}
'''

def latest_html(page):
    out = '<div class="latest-wrap">'
    for r in [r for r in LATEST_REVIEWS if page in r['pages']]:
        out += (f'<figure class="latest"><span class="lbadge"><img src="../img/addtoevent-top-rated.webp" alt="" width="44" height="42">'
                f'Verified on Add to Event · ★★★★★</span>'
                f'<blockquote>“{r["text"]}”</blockquote>'
                f'<figcaption><b>{r["name"]}</b> · {r["occasion"]} · {r["date"]} · <a href="{ATE}" target="_blank" rel="noopener">Read on Add to Event →</a></figcaption></figure>')
    return out + '</div>'

def add_latest():
    with open(f'{OUT}/site.css', 'a') as f: f.write(LATEST_CSS)
    targets = {
        'index.html': (r'(<div class="reviews">.*?</div>)(\s*<div class="rev-links">)', 'after-grid'),
        'childrens-face-painting.html': (r'(<div class="testimonials">.*?</div>\s*</div>)', 'after-grid'),
        'contact.html': (r'(<h2>What families say</h2>' + re.escape(QUOTE_STRIP) + ')', 'after-grid'),
    }
    for page, (pat, _) in targets.items():
        p = f'{OUT}/{page}'; s = open(p).read()
        if 'class="latest"' in s: continue
        s2 = re.sub(pat, lambda m: m.group(1) + latest_html(page) + (m.group(2) if m.lastindex and m.lastindex > 1 else ''), s, count=1, flags=re.S)
        if s2 == s: print('latest review not placed on', page)
        open(p, 'w').write(s2)

_orig_build = build
def build():
    _orig_build()
    add_latest()

if __name__ == '__main__':
    build()
