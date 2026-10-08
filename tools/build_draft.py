#!/usr/bin/env python3
"""Build /draft/: the full Painting Pixie site in the C+ design.
Source pages: live repo /home/claude/Painting-Pixie. Homepage: /c2/index.html."""
import re, os, glob, shutil, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inner_layout

LIVE = '/home/claude/Painting-Pixie'
V2 = '/home/claude/paintingpixie-v2'
OUT = __import__('os').environ.get('PP_OUT', V2 + '/draft')
DOMAIN = 'https://paintingpixie.com/'
os.makedirs(OUT, exist_ok=True)

c2 = open(V2 + '/c2/index.html').read()

def between(s, a, b, start=0):
    i = s.index(a, start); j = s.index(b, i)
    return s[i + len(a):j]

# ---------- shared pieces taken from C+ ----------
c2_css = between(c2, '<style>', '</style>')
c2_nav = c2[c2.index('<nav aria-label="Main"'):c2.index('</nav>') + 6]
c2_footer = c2[c2.index('<footer>'):c2.index('</footer>') + 9]
c2_menu_js = between(c2, '<script>\n(function(){\n  var trigs', '</script>')
c2_menu_js = '(function(){\n  var trigs' + c2_menu_js

GA_HEAD = '''<script>
if (/(^|\\.)paintingpixie\\.com$/.test(location.hostname)) {
  var s = document.createElement('script'); s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-JMFEXJJZ1H';
  document.head.appendChild(s);
}
window.dataLayer = window.dataLayer || [];
// Owner opt-out: open any page once with ?notrack on each phone/computer/browser to stop it being counted (?track undoes it)
try {
  if (/[?&]notrack(=|&|$)/.test(location.search)) localStorage.setItem('pp_notrack', '1');
  if (/[?&]track(=|&|$)/.test(location.search)) localStorage.removeItem('pp_notrack');
  if (localStorage.getItem('pp_notrack') === '1') window['ga-disable-G-JMFEXJJZ1H'] = true;
} catch (e) {}
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-JMFEXJJZ1H');
</script>
<!-- Microsoft Clarity (heatmaps and session replays): only on the real site, and never for the owner (?notrack) -->
<script>
  (function(){
    try {
      if (!/(^|\.)paintingpixie\.com$/.test(location.hostname)) return;
      if (/[?&]notrack(=|&|$)/.test(location.search) || localStorage.getItem('pp_notrack') === '1') return;
    } catch (e) {}
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i+"?ref=bwt";
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "yuoqgfgk81");
  })();
</script>'''

TRACK_JS = '''document.addEventListener('click', function(e) {
  var link = e.target.closest('a[href*="wa.me"]');
  if (link) {
    var isFloating = function(a){ return !!a.closest('.mbar') || getComputedStyle(a).position === 'fixed'; };
    var inPage = [].slice.call(document.querySelectorAll('a[href*="wa.me"]')).filter(function(a){ return !isFloating(a); });
    var pos = isFloating(link) ? 'floating' : (inPage.indexOf(link) === 0 ? 'top' : 'lower');
    gtag('event', 'whatsapp_click', {'link_url': link.href, 'page_location': location.href, 'page_path': location.pathname, 'button_position': pos, 'transport_type': 'beacon'});
  }
  var tel = e.target.closest('a[href^="tel:"]');
  if (tel) { gtag('event', 'phone_click', {'link_url': tel.href, 'page_location': location.href}); }
});
document.addEventListener('submit', function(e) {
  gtag('event', 'booking_request', {'form_destination': e.target.action || '', 'page_location': location.href, 'transport_type': 'beacon'});
});
'''

LEGACY_CSS = '''
/* ===== Draft site: inner pages (restyles the live site's page parts in the C+ look) ===== */
.brand img{background:none}
.phero{position:relative;min-height:64vh;display:flex;align-items:flex-end;padding-top:170px}
.phero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.phero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(21,19,26,.7) 0%,rgba(21,19,26,.2) 38%,rgba(21,19,26,.95) 100%)}
.phero .wrap{position:relative;z-index:2;padding-bottom:56px;width:100%}
.phero .crumb{font-size:13px;font-weight:800;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin:0 0 14px}
.phero .crumb a{color:var(--gold);text-decoration:none}
.phero h1{font-size:clamp(38px,5.4vw,70px);line-height:1.04;max-width:920px}
.phero p{font-size:19px;max-width:660px;margin:16px 0 0;color:var(--ink)}
.phero .ctas{margin-top:26px}
.lg section{padding:72px 0}
.lg section+section{padding-top:24px}
.lg section.alt,.lg section.contact-box,.lg section.testimonials-section{padding-top:72px}
.lg h2{text-align:left}
.lg h3{font-family:'Manrope',sans-serif;font-weight:800;font-size:19px;margin:26px 0 6px;letter-spacing:0}
.lg p{color:var(--muted);margin:0 0 14px}
.lg p strong,.lg li strong{color:var(--ink)}
.lg a:not(.btn){color:var(--gold)}
.lg ul{color:var(--muted)}
.lg .btn{margin:6px 8px 6px 0}
.lg section.alt{background:var(--panel);border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:48px 0}
.lg section.alt p{font-size:17px}
.lg .about .wrap,.lg .about-container{display:flex;gap:56px;align-items:center}
.lg .about .wrap>img{width:400px;max-width:42%;height:520px;object-fit:cover;object-position:50% 20%;border-radius:12px;flex:0 0 auto}
.lg .about .wrap>div{flex:1}
.lg .about-image{flex:1 1 420px}.lg .about-image img{border-radius:12px;width:100%}
.lg .about-text{flex:1 1 420px}
.lg .trust{margin-top:20px;padding:16px;background:var(--panel);border:1px solid var(--line);border-radius:12px;font-size:15px;color:var(--muted)}
.lg .packages-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px;margin-top:30px}
.lg .package-card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:28px;display:flex;flex-direction:column;justify-content:space-between;gap:18px;position:relative;overflow:hidden;text-align:left}
.lg .package-card::before{content:"";position:absolute;left:0;right:0;top:0;height:5px;background:var(--c)}
.lg .package-card:nth-child(6n+1){--c:var(--pink)}.lg .package-card:nth-child(6n+2){--c:var(--gold)}.lg .package-card:nth-child(6n+3){--c:var(--teal)}.lg .package-card:nth-child(6n+4){--c:var(--violet)}.lg .package-card:nth-child(6n+5){--c:var(--orange)}.lg .package-card:nth-child(6n){--c:var(--sky)}
.lg .package-name{font-family:'Fraunces',serif;font-weight:400;font-size:24px;margin:0 0 10px;line-height:1.2}
.lg .package-tagline{color:var(--gold);font-weight:700;font-size:14px}
.lg .package-features{padding-left:20px;margin:0}
.lg .package-price{font-family:'Fraunces',serif;font-size:40px;line-height:1;margin-bottom:14px;color:var(--ink)}
.lg .package-card .btn{margin:0;width:100%}
.lg .packages-title,.lg .packages-subtitle{text-align:center}
.lg .testimonials{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:26px}
.lg .testimonial{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:28px;display:flex;flex-direction:column;gap:14px}
.lg .testimonial::before{content:"★★★★★";color:var(--gold);letter-spacing:3px}
.lg .testimonial p{font-family:'Fraunces',serif;font-size:19px;line-height:1.5;color:var(--ink);margin:0}
.lg .testimonial>strong{margin-top:auto;color:var(--muted);font-size:15px}
.lg section.contact-box{background:var(--panel);border-top:1px solid var(--line);text-align:center;margin-top:48px}
.lg section.contact-box h2{text-align:center;font-size:clamp(34px,4.6vw,56px)}
.lg section.contact-box p{max-width:640px;margin-left:auto;margin-right:auto}
.lg section.contact-box .btn{margin:8px 4px}
.lg .mini-gallery{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:20px}
.lg .mini-gallery img{width:100%;aspect-ratio:3/4;object-fit:cover;object-position:center 25%;border-radius:10px;transition:transform .3s}
.lg .mini-gallery img:hover{transform:scale(1.03)}
.lg .insta-gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));grid-auto-rows:8px;gap:12px;margin-top:20px}
.lg .insta-gallery>img{grid-row:span 30;width:100%;height:100%;object-fit:cover;border-radius:10px}
.lg .gallery-item{position:relative;border-radius:10px;overflow:hidden;cursor:pointer}
.lg .gallery-item img{width:100%;height:auto;display:block;transition:transform .3s}
.lg .gallery-item:hover img{transform:scale(1.05)}
.lg .zoom-hint{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:28px;color:#fff;opacity:0;transition:opacity .2s,background .2s;pointer-events:none}
.lg .gallery-item:hover .zoom-hint{opacity:1;background:rgba(0,0,0,.3)}
.lightbox-overlay{display:none;position:fixed;inset:0;background:rgba(10,9,12,.92);z-index:2000;align-items:center;justify-content:center;padding:30px}
.lightbox-overlay.active{display:flex}
.lightbox-overlay img{max-width:90vw;max-height:86vh;border-radius:10px}
.lightbox-close{position:absolute;top:20px;right:30px;color:#fff;font-size:36px;font-weight:700;cursor:pointer;line-height:1}
.lightbox-nav{position:absolute;top:50%;transform:translateY(-50%);color:#fff;font-size:28px;cursor:pointer;padding:14px 18px;background:rgba(255,255,255,.12);border-radius:50%;user-select:none}
.lightbox-prev{left:20px}.lightbox-next{right:20px}
.lightbox-caption{position:absolute;bottom:24px;left:0;right:0;text-align:center;color:#fff;font-size:15px}
.lightbox-counter{display:block;opacity:.6;font-size:13px;margin-top:4px}
.lg .booking-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.lg .card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:24px}
.lg form{display:flex;flex-direction:column;gap:10px}
.lg label{font-weight:700;font-size:15px;color:var(--ink);margin-top:6px}
.lg input,.lg textarea,.lg select{width:100%;padding:13px 14px;border:1px solid var(--line);border-radius:10px;font:inherit;font-size:16px;background:var(--bg);color:var(--ink)}
.lg input:focus,.lg textarea:focus,.lg select:focus{outline:2px solid var(--gold);border-color:var(--gold)}
.lg form button{margin-top:12px;background:var(--gold);color:var(--goldink);border:0;border-radius:999px;padding:16px 26px;font:inherit;font-weight:800;font-size:17px;cursor:pointer}
.draft-note{background:#3A2A12;color:#F6DDA8;border:1px dashed var(--gold);border-radius:10px;padding:10px 14px;font-size:14px;margin:0 0 16px}
.lg img{max-width:100%}
@media(max-width:860px){
.lg .about .wrap,.lg .about-container{flex-direction:column;align-items:stretch}
.lg .about .wrap>img{width:100%;max-width:100%;height:420px}
.lg .booking-grid{grid-template-columns:1fr}
.lg .mini-gallery{grid-template-columns:1fr 1fr}
}
@media(max-width:600px){
.phero{display:block;min-height:0;padding-top:0}
.phero>img{position:relative;height:48vh;min-height:320px;-webkit-mask-image:linear-gradient(180deg,#000 70%,transparent);mask-image:linear-gradient(180deg,#000 70%,transparent)}
.phero::after{display:none}
.phero .wrap{margin-top:-60px;padding-bottom:30px}
.phero p{font-size:17px}
.lg section{padding:52px 0}
}
'''

# ---------- per-page settings ----------
HERO = {
 'index.html': ('v2-hero.webp', '60% 35%', ''),
 'about.html': ('v2-hero.webp', '60% 35%', 'About'),
 'adult-face-painting.html': ('n-adult-glitter-flower-eye.webp', '45% 40%', 'Services · Grown-ups'),
 'animal-print-face-painting.html': ('n-leopard-and-tiger-kids.webp', '50% 35%', 'Services · Kids & grown-ups'),
 'areas.html': ('v2-hero.webp', '60% 35%', 'Areas'),
 'childrens-face-painting.html': ('n-unicorn-girl-party.webp', '50% 25%', 'Services · Kids'),
 'contact.html': ('n-crown-girl-blue-sky.webp', '50% 25%', 'Book'),
 'gallery.html': ('n-blue-monster-roar.webp', '50% 30%', 'Gallery'),
 'glitter-bar.html': ('n-lilac-flower-eye.webp', '38% 40%', 'Services · Grown-ups'),
 'halloween-face-painting.html': ('n-pumpkin-face.webp', '50% 30%', 'Services · Seasonal'),
 'services.html': ('v2-sisters.webp', '50% 35%', 'Services'),
 'face-painter-sussex.html': ('v2-hero.webp', '60% 35%', 'Areas · Sussex'),
 'face-painter-surrey.html': ('v2-adult-tiger.webp', '50% 35%', 'Areas · Surrey'),
 'face-painter-brighton.html': ('LIVE:brighton-palace-pier.jpg', '50% 50%', 'Areas · Brighton & East Sussex'),
 'face-painter-worthing.html': ('LIVE:worthing-beach.jpg', '50% 50%', 'Areas · West Sussex'),
 'face-painter-burgess-hill.html': ('LIVE:burgess-hill.png', '50% 50%', 'Areas · West Sussex'),
 'face-painter-horsham.html': ('v2-hero.webp', '60% 35%', 'Areas · West Sussex'),
 'face-painter-crawley.html': ('n-tiger-boy-party.webp', '50% 25%', 'Areas · West Sussex'),
 'face-painter-haywards-heath.html': ('n-unicorn-girl-party-hall.webp', '50% 25%', 'Areas · West Sussex'),
 'face-painter-east-grinstead.html': ('v2-leopard-girl.webp', '50% 35%', 'Areas · West Sussex'),
 'face-painter-west-sussex-villages.html': ('v2-fairy.webp', '50% 30%', 'Areas · West Sussex'),
 'face-painter-lewes.html': ('n-tiger-girl-closeup.webp', '50% 35%', 'Areas · Brighton & East Sussex'),
 'face-painter-south-downs.html': ('v2-sisters.webp', '50% 35%', 'Areas · Brighton & East Sussex'),
 'face-painter-guildford.html': ('n-blue-monster-roar.webp', '50% 30%', 'Areas · Surrey'),
 'face-painter-reigate.html': ('n-crown-girl-blue-sky.webp', '50% 25%', 'Areas · Surrey'),
 'face-painter-dorking.html': ('v2-tiger-boy.webp', '50% 25%', 'Areas · Surrey'),
 'face-painter-surrey-villages.html': ('n-unicorn-girl-party.webp', '50% 25%', 'Areas · Surrey'),
}

EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿⭐✨️‍]+')
def strip_emoji(t): return re.sub(r'\s{2,}', ' ', EMOJI.sub('', t)).strip()

def rel_links(s, page):
    """Keep every link inside the draft."""
    def fix(m):
        attr, url = m.group(1), m.group(2)
        u = url
        if u.startswith(DOMAIN): u = u[len(DOMAIN):]
        elif u.startswith('https://www.paintingpixie.com/'): u = u[len('https://www.paintingpixie.com/'):]
        elif u.startswith('/') and not u.startswith('//'): u = u[1:]
        if u == '' and url != '': u = 'index.html'
        if page != 'index.html' and u in ('#prices', '#reviews', '#faq'): u = 'index.html' + u
        return f'{attr}="{u}"'
    return re.sub(r'\b(href|src)="([^"]*)"', fix, s)

def clean_inline(st):
    st = re.sub(r'background(-color)?\s*:\s*(#f8f8f8|#fff(fff)?|white|#f2f2f2)\s*;?', '', st, flags=re.I)
    st = re.sub(r'color\s*:\s*#(777|b8005f)\s*;?', '', st, flags=re.I)
    st = re.sub(r'box-shadow\s*:[^;]+;?', '', st)
    st = st.replace('#3498db', '#E2BE7A')
    return st.strip()

def fix_classes(s):
    s = re.sub(r'class="btn"', 'class="btn btn-gold"', s)
    s = re.sub(r'class="whatsapp-btn"', 'class="btn btn-wa"', s)
    s = re.sub(r'class="package-btn"', 'class="btn btn-ghost"', s)
    return s

def convert_sections(body):
    out = []
    pos = 0
    for m in re.finditer(r'<section([^>]*)>(.*?)</section>', body, re.S):
        out.append(body[pos:m.start()])
        attrs, inner = m.group(1), m.group(2)
        alt = bool(re.search(r'background\s*:\s*#f8f8f8', attrs))
        attrs = re.sub(r'style="([^"]*)"', lambda x: f'style="{clean_inline(x.group(1))}"', attrs)
        attrs = attrs.replace(' style=""', '')
        if alt:
            if 'class="' in attrs: attrs = attrs.replace('class="', 'class="alt ', 1)
            else: attrs += ' class="alt"'
        inner = re.sub(r'(<h2[^>]*>)(.*?)(</h2>)', lambda x: x.group(1) + strip_emoji(x.group(2)) + x.group(3), inner, flags=re.S)
        out.append(f'<section{attrs}><div class="wrap">{inner}</div></section>')
        pos = m.end()
    out.append(body[pos:])
    s = ''.join(out)
    s = re.sub(r'style="([^"]*)"', lambda x: f'style="{clean_inline(x.group(1))}"', s).replace(' style=""', '')
    return s

convert_sections = inner_layout.make(strip_emoji, clean_inline)

def phero(header_html, page):
    img, objpos, crumb = HERO.get(page, ('v2-hero.webp', '50% 35%', ''))
    src = img[5:] if img.startswith('LIVE:') else '../img/' + img
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', header_html, re.S).group(1)
    rest = header_html[header_html.index('</h1>') + 5:]
    rest = re.sub(r'<div style="margin-top:\d+px;?">', '<div class="ctas">', rest)
    rest = re.sub(r'style="([^"]*)"', lambda x: f'style="{clean_inline(x.group(1))}"', rest).replace(' style=""', '')
    alt = strip_emoji(re.sub('<[^>]+>', '', h1))
    crumbs = '<a href="index.html">Home</a>' + (' · ' + crumb if crumb else '')
    return (f'<header class="phero"><img src="{src}" alt="{html.escape(alt)}" style="object-position:{objpos}" fetchpriority="high">'
            f'<div class="wrap"><div class="hcard">{"" if page == "index.html" else f'<p class="crumb">{crumbs}</p>'}<h1>{strip_emoji(h1)}</h1>{rest}</div></div></header>\n<div class="jewel-rule"></div>')

def shared_nav(page):
    return rel_links(c2_nav, page)

def shared_footer(page):
    return rel_links(c2_footer, page)

def mbar(page, wa):
    prices = 'prices.html'
    return (f'<div class="mbar" role="navigation" aria-label="Quick contact">'
            f'<a class="pr" href="{prices}">Prices</a><a href="tel:+447852300125">Call</a>'
            f'<a class="wa" href="{wa}" target="_blank" rel="noopener">WhatsApp</a></div>')

def head_from_live(s):
    head = between(s, '<head>', '</head>')
    # drop live gtag block + async loader
    head = re.sub(r'<!-- Google tag \(gtag\.js\) -->\s*', '', head)
    head = re.sub(r'<script async src="https://www\.googletagmanager\.com[^>]*></script>\s*', '', head)
    head = re.sub(r'<script>\s*window\.dataLayer.*?</script>\s*', '', head, flags=re.S)
    head = re.sub(r'<!-- Microsoft Clarity.*?</script>\s*', '', head, flags=re.S)   # added back by GA_HEAD
    head = re.sub(r'<link rel="stylesheet" href="style\.css">\s*', '', head)
    head = re.sub(r'<meta name="robots"[^>]*>\s*', '', head)
    head = re.sub(r'(<link rel="(?:icon|apple-touch-icon)"[^>]*href=")/?', r'\1', head)
    extra = ('\n<!-- DRAFT ONLY: remove this robots line when the page goes live -->\n<meta name="robots" content="noindex, nofollow">\n'
             + GA_HEAD + '\n'
             '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
             '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
             '<link rel="stylesheet" href="site.css">\n')
    return head.rstrip() + extra

images = set()
def collect_images(s):
    for m in re.findall(r'(?:src|href)="([^"#?:]+\.(?:jpe?g|png|webp|gif|svg|ico))"', s, re.I):
        if not m.startswith('../'): images.add(m)

def build_page(f):
    s = open(f'{LIVE}/{f}').read()
    page = f
    body = s[s.index('<body>') + 6:s.index('</body>')]
    after_nav = body[body.index('</nav>') + 6:]
    content = after_nav[:after_nav.index('<footer')]
    tail = after_nav[after_nav.index('</footer>') + 9:]
    fm = re.search(r'<a[^>]*href="([^"]+)"[^>]*class="whatsapp-float"|<a[^>]*class="whatsapp-float"[^>]*href="([^"]+)"', body, re.S)
    wa = (fm.group(1) or fm.group(2)) if fm else 'https://wa.me/447852300125'
    tail = re.sub(r'<a[^>]*whatsapp-float[^>]*>.*?</a>', '', tail, flags=re.S)
    tail = re.sub(r'<a\s+href="[^"]+"\s*\n?class="whatsapp-float".*?</a>', '', tail, flags=re.S)
    hm = re.search(r'<header class="page-header">(.*?)</header>', content, re.S)
    hero = phero(hm.group(1), page) if hm else ''
    if hm: content = content[:hm.start()] + content[hm.end():]
    title = re.search(r'<title>(.*?)</title>', s, re.S).group(1)
    content = convert_sections(fix_classes(content), page, title) + inner_layout.TRUST_BAND
    tail = fix_classes(tail)
    if page == 'contact.html':
        content = content.replace('<form ', '<p class="draft-note">Draft site: this form is live and sends a real enquiry to Kat.</p>\n<form ', 1)
    doc = ('<!doctype html>\n<html lang="en-GB">\n<head>' + head_from_live(s) + '</head>\n<body>\n'
           + shared_nav(page) + '\n' + rel_links(fix_classes(hero), page) + '\n<main class="lg">\n' + rel_links(content, page)
           + '\n</main>\n' + shared_footer(page) + '\n' + rel_links(tail, page) + '\n' + mbar(page, wa)
           + '\n<script src="site.js"></script>\n</body>\n</html>\n')
    collect_images(doc)
    open(f'{OUT}/{f}', 'w').write(doc)

def build_index():
    s = c2
    s = s.replace('<style>' + c2_css + '</style>', '<link rel="stylesheet" href="site.css">')
    # replace C+ inline GA+tracking with the shared ones
    s = re.sub(r'<!-- Google Analytics:.*?</script>', '<!-- Google Analytics: only runs on the real site, so previews don\'t add fake visits -->\n' + GA_HEAD, s, flags=re.S)
    s = s.replace('<script>\n' + c2_menu_js + '</script>', '<script src="site.js"></script>')
    s = s.replace('<!-- PREVIEW ONLY: remove this robots line when this page goes live as paintingpixie.com -->', '<!-- DRAFT ONLY: remove this robots line when the page goes live -->')
    head, body = s.split('</head>', 1)
    head = re.sub(r'(<link rel="(?:icon|apple-touch-icon)"[^>]*href=")https://paintingpixie\.com/', r'\1', head)
    s = head + '</head>' + rel_links(body, 'index.html')
    collect_images(s)
    open(f'{OUT}/index.html', 'w').write(s)

pages = [os.path.basename(p) for p in sorted(glob.glob(LIVE + '/*.html'))]
built = []
for f in pages:
    src = open(f'{LIVE}/{f}').read()
    if 'http-equiv="refresh"' in src:
        shutil.copy(f'{LIVE}/{f}', f'{OUT}/{f}')
        # keep redirects working inside the draft
        t = open(f'{OUT}/{f}').read().replace(DOMAIN, '')
        open(f'{OUT}/{f}', 'w').write(t)
        continue
    if f == 'index.html' and os.environ.get('PP_MODE') != 'switch': continue
    build_page(f); built.append(f)
if os.environ.get('PP_MODE') != 'switch':   # switch mode: homepage keeps the live wording, in the new design
    build_index(); built.append('index.html')

open(f'{OUT}/site.css', 'w').write(c2_css + LEGACY_CSS + inner_layout.INNER_CSS)
open(f'{OUT}/site.js', 'w').write(c2_menu_js + '\n' + TRACK_JS)

for im in sorted(images):
    srcp = f'{LIVE}/{im}'
    if os.path.exists(srcp): shutil.copy(srcp, f'{OUT}/{im}')
    else: print('missing image', im)
print('built', len(built), 'pages;', len(images), 'images')

# ---------- convert photos to WebP (smaller, faster pages) ----------
from PIL import Image, ImageOps
KEEP = {'favicon-16x16.png', 'favicon-32x32.png', 'apple-touch-icon.png', 'favicon.ico', 'addtoevent-top-rated.webp'}
renamed = {}
before = after = 0
for im in sorted(images):
    p = f'{OUT}/{im}'
    if im in KEEP or not os.path.exists(p) or im.lower().endswith('.webp'): continue
    if not re.search(r'\.(jpe?g|png)$', im, re.I): continue
    new = re.sub(r'\.(jpe?g|png)$', '.webp', im, flags=re.I)
    img = ImageOps.exif_transpose(Image.open(p))
    img = img.convert('RGBA' if img.mode in ('RGBA', 'LA', 'P') else 'RGB')
    img.thumbnail((1600, 1600), Image.LANCZOS)
    img.save(f'{OUT}/{new}', 'WEBP', quality=80, method=6)
    before += os.path.getsize(p); after += os.path.getsize(f'{OUT}/{new}')
    os.remove(p); renamed[im] = new
for f in glob.glob(OUT + '/*.html'):
    t = open(f).read()
    for old, new in renamed.items():
        t = t.replace(f'src="{old}"', f'src="{new}"').replace(f"url('{old}')", f"url('{new}')").replace(f'url("{old}")', f'url("{new}")')
    open(f, 'w').write(t)
print(f'webp: {len(renamed)} photos, {before/1e6:.1f} MB -> {after/1e6:.1f} MB')
