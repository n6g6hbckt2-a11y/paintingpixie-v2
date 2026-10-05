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

if __name__ == '__main__':
    build()
