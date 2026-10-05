"""Luminosity-style inner page layout helpers for the draft build."""
import re, html

def make(strip_emoji, clean_inline):
    def cap(t):
        return t[:1].upper() + t[1:] if t else t

    def strong_lines(inner):
        return re.findall(r'<p>\s*<strong>(.*?)</strong>\s*(?:[—–-]\s*)?(.*?)</p>', inner, re.S)

    def price_cards(inner):
        items = []
        for label, rest in strong_lines(inner):
            pm = re.search(r'<strong>(.*?)</strong>\s*$', rest.strip(), re.S)
            price = pm.group(1) if pm else ''
            desc = rest.strip()[:pm.start()] if pm else rest
            desc = re.sub(r'\s*[—–-]\s*$', '', desc.strip()).lstrip('–—- ').strip()
            items.append(f'<div class="pcard"><h3>{strip_emoji(label)}</h3><p>{desc}</p><div class="pp">{price}</div></div>')
        return '<div class="pcards">' + ''.join(items) + '</div>'

    def feature_cards(inner):
        return '<div class="fcards">' + ''.join(
            f'<div class="fcard"><h3>{strip_emoji(l)}</h3><p>{cap(r.strip())}</p></div>' for l, r in strong_lines(inner)) + '</div>'

    def split_h3(inner):
        parts = re.split(r'(<h3[^>]*>.*?</h3>)', inner, flags=re.S)
        return parts[0], [(parts[i], parts[i + 1] if i + 1 < len(parts) else '') for i in range(1, len(parts), 2)]

    def faq_details(inner):
        head, qs = split_h3(inner)
        return head + '<div class="faqlist">' + ''.join(
            f'<details><summary>{strip_emoji(re.sub(r"</?h3[^>]*>", "", q))}</summary>{a}</details>' for q, a in qs) + '</div>'

    def h3_cards(inner):
        head, qs = split_h3(inner)
        return head + '<div class="fcards">' + ''.join(f'<div class="fcard">{q}{a}</div>' for q, a in qs) + '</div>'

    def enquiry_form(page, title):
        t = html.escape(re.sub(r'\s*\|.*$', '', title))
        return f"""
<form class="qform" action="https://formspree.io/f/mjgdnged" method="POST">
<p class="draft-note">Draft site: this form is live and sends a real enquiry to Kat.</p>
<input type="hidden" name="_subject" value="Website enquiry: {t}">
<input type="hidden" name="page" value="{page}">
<input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
<div class="row2"><label>Name<input type="text" name="name" autocomplete="name" required></label><label>Phone<input type="tel" name="phone" autocomplete="tel" required></label></div>
<div class="row2"><label>Email<input type="email" name="email" autocomplete="email" required></label><label>Event date<input type="date" name="event-date" required></label></div>
<label>Town or venue<input type="text" name="location" placeholder="e.g. Horsham" required></label>
<label>Tell Kat about your event<textarea name="message" rows="4" placeholder="Number of children or guests, ages, theme..."></textarea></label>
<button type="submit">Send my enquiry</button>
<p class="small-note">Prefer WhatsApp? <a href="https://wa.me/447852300125" target="_blank" rel="noopener">Message Kat on 07852 300125</a></p>
</form>"""

    def convert_sections(body, page, title):
        out = []; pos = 0; light = True
        for m in re.finditer(r'<section([^>]*)>(.*?)</section>', body, re.S):
            out.append(body[pos:m.start()])
            attrs, inner = m.group(1), m.group(2)
            cm = re.search(r'class="([^"]*)"', attrs); cls = cm.group(1) if cm else ''
            alt = bool(re.search(r'background\s*:\s*#f8f8f8', attrs))
            centred = 'text-align:center' in attrs.replace(' ', '')
            inner = re.sub(r'(<h2[^>]*>)(.*?)(</h2>)', lambda x: x.group(1) + strip_emoji(x.group(2)) + x.group(3), inner, flags=re.S)
            inner = re.sub(r'style="([^"]*)"', lambda x: f'style="{clean_inline(x.group(1))}"', inner).replace(' style=""', '')
            h2 = re.search(r'<h2[^>]*>(.*?)</h2>', inner, re.S); h2t = h2.group(1) if h2 else ''
            n_h3 = inner.count('<h3'); has_media = '<img' in inner or '<div' in inner
            sl = strong_lines(inner); n_p = inner.count('<p')
            kind = 'text'
            if 'contact-box' in cls: kind = 'enquire'
            elif 'about' in cls.split() or 'about-container' in cls: kind = 'split'
            elif 'booking-grid' in cls: kind = 'booking'
            elif 'testimonials-section' in cls: kind = 'reviews'
            elif 'packages-section' in cls: kind = 'packages'
            elif alt and len(sl) >= 2 and '£' in inner: kind = 'prices'
            elif n_h3 >= 3 and not has_media and re.search(r'question|faq', h2t, re.I): kind = 'faq'
            elif n_h3 >= 3 and not has_media: kind = 'cards'
            elif len(sl) >= 3 and not has_media and len(sl) >= n_p - 1: kind = 'features'
            elif 'mini-gallery' in inner or 'insta-gallery' in inner: kind = 'gallery'
            if kind == 'prices':
                inner = inner[:inner.index('<p')] + price_cards(inner) + '<p class="small-note">Kat confirms the exact price for your date. A small deposit secures your booking.</p>'
            elif kind == 'features':
                first = inner.index('<p'); last = inner.rindex('</p>') + 4
                inner = inner[:first] + feature_cards(inner[first:last]) + inner[last:]
            elif kind == 'faq': inner = faq_details(inner)
            elif kind == 'cards': inner = h3_cards(inner)
            if kind == 'enquire': band = 'panel'
            elif kind in ('prices', 'packages'): band = 'jewel'
            else:
                band = 'light' if light else 'dark'; light = not light
            centre = (centred or kind in ('text', 'features', 'prices', 'reviews', 'gallery', 'packages')) and kind not in ('split', 'faq', 'booking', 'cards')
            extra = enquiry_form(page, title) if kind == 'enquire' and page != 'contact.html' else ''
            out.append(f'<section class="band band-{band} k-{kind}{" centred" if centre else ""} {cls}"><div class="wrap">{inner}{extra}</div></section>')
            pos = m.end()
        out.append(body[pos:])
        s = ''.join(out)
        return re.sub(r'style="([^"]*)"', lambda x: f'style="{clean_inline(x.group(1))}"', s).replace(' style=""', '')

    return convert_sections

TRUST_BAND = '''<section class="band trustband"><div class="wrap">
<p class="eyebrow">Trusted across Sussex &amp; Surrey</p>
<div class="trustrow">
<a class="ate" href="https://www.addtoevent.co.uk/suppliers/the-painting-pixie-ltd" target="_blank" rel="noopener" title="Top rated on Add to Event"><img src="../img/addtoevent-top-rated.webp" alt="Top rated on Add to Event, 5 stars" width="84" height="81" loading="lazy"></a>
<div><b>&#9733;&#9733;&#9733;&#9733;&#9733; 5.0</b><span>30+ reviews</span></div>
<div><b>1,000+</b><span>faces painted</span></div>
<div><b>Insured</b><span>&amp; DBS checked</span></div>
<div><b>Guildford</b><span>Festival of the Arts</span></div>
</div></div></section>'''

INNER_CSS = '''
/* ===== Inner pages, Luminosity-style: centred hero card + alternating bands ===== */
.phero{min-height:78vh;align-items:center;justify-content:center;padding:150px 0 70px}
.phero::after{background:linear-gradient(180deg,rgba(21,19,26,.55),rgba(21,19,26,.25) 40%,rgba(21,19,26,.6))}
.phero .wrap{padding-bottom:0;display:flex;justify-content:center}
.hcard{background:rgba(14,12,18,.86);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.08);border-radius:22px;padding:42px 46px;max-width:780px;text-align:center;box-shadow:0 30px 70px -20px rgba(0,0,0,.7)}
.hcard h1{font-size:clamp(34px,4.6vw,58px)!important;max-width:none}
.hcard p{margin:16px auto 0!important;font-size:18px!important;color:var(--muted)!important}
.hcard .crumb{margin:0 0 12px!important;color:var(--gold)!important;font-size:12px!important}
.hcard .ctas{justify-content:center}
.lg section.band{padding:84px 0;margin:0}
.lg section.band+section.band{padding-top:84px}
.band-dark{background:var(--bg)}
.band-light{background:#F6F1EA;color:#1B1712}
.band-light h2,.band-light h3,.band-light p strong{color:#1B1712}
.band-light p,.band-light li{color:#4E463F}
.band-light a:not(.btn){color:#A3245F}
.band-light .btn-ghost{border-color:#1B1712;color:#1B1712}
.band-panel{background:linear-gradient(180deg,#221D2B,#15131A)}
.band-jewel{background:linear-gradient(135deg,#3B1240 0%,#1E1B4B 50%,#0E3B3A 100%)}
.lg .centred,.lg .centred h2{text-align:center}
.lg .centred .wrap>p,.lg .centred .wrap>h2{max-width:820px;margin-left:auto;margin-right:auto}
.lg section.band h2{font-size:clamp(30px,3.6vw,46px);margin-bottom:20px}
.fcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;margin-top:30px;text-align:left}
.fcard{border-radius:16px;padding:24px;position:relative;overflow:hidden}
.band-light .fcard{background:#fff;box-shadow:0 14px 30px -18px rgba(60,30,40,.35)}
.band-dark .fcard{background:var(--panel);border:1px solid var(--line)}
.fcard::before{content:"";display:block;width:36px;height:5px;border-radius:5px;margin-bottom:16px;background:var(--c,var(--pink))}
.fcard:nth-child(5n+2){--c:var(--teal)}.fcard:nth-child(5n+3){--c:var(--violet)}.fcard:nth-child(5n+4){--c:var(--orange)}.fcard:nth-child(5n){--c:var(--gold)}
.lg .fcard h3{margin:0 0 8px;font-size:18px}
.lg .fcard p{margin:0;font-size:15.5px}
.pcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:30px;text-align:left}
.pcard{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:16px;padding:26px;display:flex;flex-direction:column;gap:10px}
.lg .pcard h3{margin:0;font-family:'Fraunces',serif;font-weight:400;font-size:24px;color:#fff}
.lg .pcard p{margin:0;color:#D8D2E6;font-size:15px;flex:1}
.pcard .pp{font-family:'Fraunces',serif;font-size:30px;color:var(--gold)}
.lg .band-jewel h2{color:#fff}
.small-note{font-size:14px!important;opacity:.85;margin-top:22px!important}
.faqlist{max-width:860px;margin-top:20px}
.faqlist details{border-bottom:1px solid rgba(128,118,140,.35);padding:18px 0}
.faqlist summary{cursor:pointer;font-weight:800;font-size:18px;list-style:none;display:flex;justify-content:space-between;gap:16px}
.faqlist summary::-webkit-details-marker{display:none}
.faqlist summary::after{content:"+";color:var(--gold);font-size:22px;line-height:1}
.faqlist details[open] summary::after{content:"\\2013"}
.faqlist details p{margin:10px 0 0}
.band-light .faqlist summary{color:#1B1712}
.lg section.k-split .wrap{display:flex;gap:56px;align-items:center}
.lg section.k-split .wrap>img,.lg section.k-split .about-image img{width:420px;max-width:44%;height:540px;object-fit:cover;object-position:50% 20%;border-radius:18px;flex:0 0 auto}
.lg section.k-split .about-image{flex:0 0 44%}.lg section.k-split .about-image img{max-width:100%;width:100%}
.lg section.k-split .wrap>div{flex:1}
.lg section.k-booking .wrap{display:grid;grid-template-columns:1fr 1.2fr;gap:20px;align-items:start}
.band-light .card{background:#fff;border-color:#E8DED3}
.band-light .card p,.band-light .card label{color:#3A322C}
.band-light input,.band-light textarea,.band-light select{background:#FBF8F4;color:#1B1712;border-color:#D9CFC4}
.lg section.k-reviews .testimonial{text-align:left}
.band-light .testimonial{background:#fff;border-color:#E8DED3}
.band-light .testimonial p{color:#1B1712}
.band-light .package-card{background:#fff;border-color:#E8DED3}
.lg section.k-enquire{text-align:center}
.lg section.k-enquire .wrap>p{max-width:640px;margin-left:auto;margin-right:auto}
.qform{max-width:760px;margin:34px auto 0;text-align:left;display:flex;flex-direction:column;gap:12px}
.qform .row2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.qform label{display:flex;flex-direction:column;gap:6px;font-weight:700;font-size:14px;color:var(--ink);margin:0!important}
.qform button{align-self:flex-start}
.trustband{background:#0E0C12;border-top:1px solid var(--line);padding:46px 0!important}
.trustband .eyebrow{text-align:center}
.trustrow{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:22px 46px}
.trustrow div{text-align:center}
.trustrow b{display:block;font-family:'Fraunces',serif;font-weight:400;font-size:24px;color:var(--ink)}
.trustrow span{color:var(--muted);font-size:14px}

.lg section.booking-grid,.lg section.about-container,.lg section.about{display:block}
.lg section.about-container .wrap{display:flex;gap:56px;align-items:flex-start}.lg section.about-container .about-image{position:sticky;top:30px}
.band-light li strong,.band-light p strong,.band-light b{color:#1B1712}
.band-light .testimonial>strong{color:#6B5F57}
.band-light .testimonial::before{color:#C9962E}
.brand span{text-shadow:0 1px 10px rgba(0,0,0,.7)}
@media(max-width:860px){.lg section.about-container .wrap{flex-direction:column;align-items:stretch}}
@media(max-width:860px){
.lg section.k-split .wrap{flex-direction:column;align-items:stretch}
.lg section.k-split .wrap>img,.lg section.k-split .about-image{width:100%;max-width:100%;height:420px;flex:none}
.lg section.k-booking .wrap{grid-template-columns:1fr}
.qform .row2{grid-template-columns:1fr}
}
@media(max-width:600px){
.phero{display:block;min-height:0;padding:0}
.phero .wrap{margin-top:-90px;padding-bottom:20px}
.hcard{padding:28px 20px}
.lg section.band{padding:60px 0}
.lg section.band+section.band{padding-top:60px}
.trustrow{gap:18px 28px}
}
'''
