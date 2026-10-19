# -*- coding: utf-8 -*-
"""19 Oct (draft, next/ only): the contact page offers three ways to book, side by side:
  1. Book online: children's parties, with Kat's free dates shown live from Cal.com (deposit to secure)
  2. WhatsApp Kat: the quickest way to ask anything
  3. Ask for a quote: the form, for weddings, festivals, corporate, hens and multi-day events
The live calendar sits under the three cards, with a switch between the 3-hour and 2-hour party.
Runs after build_contact_wa (replaces its WhatsApp-first block). Only applied when PP_BOOK3=1."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_booking import CAL, PACKAGES, deposit
from build_contact_wa import WA

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
SLUG = {k: v.split('cal.com/', 1)[1] for k, v in CAL.items()}

WA_SVG = ('<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>')

def tabs():
    out = []
    for i, (key, name, length, price, _f) in enumerate(PACKAGES):
        badge = '<em>Most popular</em>' if i == 0 else ''
        out.append(f'<button type="button" role="tab" class="b3tab" id="b3tab-{key}" aria-selected="{"true" if i == 0 else "false"}" '
                   f'aria-controls="b3cal" data-key="{key}" data-link="{SLUG[key]}" data-url="{CAL[key]}">'
                   f'<b>{name}</b><span>{length} party · £{price} · £{deposit(price):.2f} deposit</span>{badge}</button>')
    return ''.join(out)

BLOCK = f'''<section class="band band-light b3 centred"><div class="wrap">
<h2>Book Kat for your event</h2>
<p class="b3-lede">Three ways to book. Pick whichever suits you.</p>
<div class="b3grid">
<article class="b3card b3-main"><p class="b3tag">Children’s parties</p><h3>Book online now</h3>
<p>See the dates and times Kat is free, choose your party and secure it with a deposit. You’re confirmed straight away.</p>
<a class="btn btn-gold" href="#book-online" data-b3="online">See Kat’s free dates ↓</a></article>
<article class="b3card"><p class="b3tag">Quickest reply</p><h3>WhatsApp Kat</h3>
<p>Send your date, town and roughly how many children. Kat usually replies the same day.</p>
<a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{WA_SVG}WhatsApp Kat</a></article>
<article class="b3card"><p class="b3tag">Weddings, festivals, corporate, hens</p><h3>Ask for a quote</h3>
<p>For bigger or longer events, or anything that isn’t a standard party, tell Kat what you have in mind.</p>
<a class="btn btn-ghost" href="#cwa-form" data-b3="form">Fill in the form ↓</a></article>
</div>
<div class="b3cal-wrap" id="book-online">
<h3 class="b3cal-h">Kat’s free dates</h3>
<div class="b3tabs" role="tablist" aria-label="Choose your party">{tabs()}</div>
<div id="b3cal" class="b3cal" role="tabpanel" aria-live="polite"><p class="b3load">Loading Kat’s calendar…</p></div>
<p class="b3terms">Deposit is a third of the price (up to £60); the balance and any travel are paid on the day. Book at least 7 days ahead.
Cancel 14 days or more before for a full deposit refund, or 7 to 13 days before for half; after that the deposit can move to a new date.</p>
<p class="b3fall">Calendar not showing? <a id="b3open" href="{CAL[PACKAGES[0][0]]}" target="_blank" rel="noopener">Open it in a new tab</a> or <a href="{WA}" target="_blank" rel="noopener">WhatsApp Kat</a>.</p>
</div>
<p class="cwa-alt">Or call <a href="tel:+447852300125">07852 300125</a></p>
<p class="cwa-trust">★★★★★ 5.0 rated · Parties from £130 · Fully insured &amp; DBS checked</p>
</div></section>
'''

CSS = '''<style>
.b3{padding:46px 0 44px}.b3 h2{margin:0 0 8px}.b3-lede{margin:0 auto 24px;font-size:18px}
.b3grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;text-align:left}
.b3card{background:#fff;border:1px solid #E8DED3;border-radius:18px;padding:22px;display:flex;flex-direction:column;gap:8px;color:#1B1712}
.b3card h3{margin:0;font-size:24px;color:#1B1712}.b3card p{margin:0}.b3card .btn{margin-top:auto;align-self:flex-start;display:inline-flex;align-items:center;gap:8px}
.b3card>p:not(.b3tag){margin-bottom:12px}
.b3tag{font-size:12px;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;color:#B0006A}
.b3-main{border:2px solid var(--gold);box-shadow:0 10px 28px rgba(226,190,122,.28)}
.b3cal-wrap{margin-top:30px;background:#fff;border:1px solid #E8DED3;border-radius:20px;padding:22px;text-align:left;scroll-margin-top:90px;color:#1B1712}
.b3cal-h{margin:0 0 12px;font-size:24px;color:#1B1712}
.b3tabs{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px}
.b3tab{position:relative;font:inherit;text-align:left;background:#FBF8F4;border:2px solid #E8DED3;border-radius:14px;padding:14px 16px;cursor:pointer;color:#1B1712;display:flex;flex-direction:column;gap:2px}
.b3tab b{font-size:18px}.b3tab span{font-size:14px;color:#5A4E60}
.b3tab em{position:absolute;top:-10px;right:12px;font-style:normal;font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;background:#FF4FA3;color:#fff;border-radius:999px;padding:3px 10px}
.b3tab[aria-selected="true"]{border-color:var(--gold);background:#FFF7E8}
.b3tab:focus-visible{outline:3px solid #B0006A;outline-offset:2px}
.b3cal{min-height:520px;border-radius:14px;overflow:hidden}
.b3load{padding:40px 0;text-align:center;color:#5A4E60}
.b3 .cwa-alt{margin-top:24px}
.b3terms{font-size:14px;color:#5A4E60;margin:14px 0 4px}.b3fall{font-size:14px;margin:0;color:#5A4E60}
.b3fall a,.b3terms a{color:#B0006A}
@media(max-width:860px){.b3grid{grid-template-columns:1fr}.b3tabs{grid-template-columns:1fr}.b3cal-wrap{padding:14px}}
</style>
'''

JS = '''<script>
(function(){
  var box=document.getElementById('b3cal'), open=document.getElementById('b3open'), started=false, current=null;
  function track(n,p){ if(window.gtag) gtag('event',n,p||{}); }
  function loadCal(){
    if(started) return; started=true;
    (function (C, A, L) { var p = function (a, ar) { a.q.push(ar); }; var d = C.document; C.Cal = C.Cal || function () { var cal = C.Cal; var ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { var api = function () { p(api, arguments); }; var namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar); return; } p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "init");
    Cal("init", "pp", {origin: "https://cal.com"});
    Cal.ns.pp("ui", {theme: "light", hideEventTypeDetails: false, layout: "month_view", cssVarsPerTheme: {light: {"cal-brand": "#B0006A"}}});
    Cal.ns.pp("on", {action: "bookingSuccessful", callback: function(){ track('cal_booking', {party: current}); }});
    show(document.querySelector('.b3tab[aria-selected="true"]'));
    setTimeout(function(){ if(!box.querySelector('iframe')) box.innerHTML='<p class="b3load">The calendar didn’t load. Use the link below to open it in a new tab.</p>'; }, 12000);
  }
  function show(tab){
    var key=tab.getAttribute('data-key'); if(key===current) return; current=key;
    document.querySelectorAll('.b3tab').forEach(function(t){ t.setAttribute('aria-selected', t===tab ? 'true' : 'false'); });
    open.href=tab.getAttribute('data-url');
    if(!started) return;
    box.innerHTML='<p class="b3load">Loading Kat’s calendar…</p>';
    Cal.ns.pp("inline", {elementOrSelector: "#b3cal", calLink: tab.getAttribute('data-link'), config: {layout: "month_view", theme: "light"}});
    track('book_online_view', {party: key});
  }
  document.querySelectorAll('.b3tab').forEach(function(t){
    t.addEventListener('click', function(){ if(!started){ current=null; loadCal(); } show(t); });
  });
  document.querySelectorAll('[data-b3]').forEach(function(a){
    a.addEventListener('click', function(){ track('book_option', {option: a.getAttribute('data-b3')}); if(a.getAttribute('data-b3')==='online') loadCal(); });
  });
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ loadCal(); io.disconnect(); } }); }, {rootMargin: '300px'});
    io.observe(document.getElementById('book-online'));
  } else loadCal();
})();
</script>
'''

def build():
    if os.environ.get('PP_BOOK3') != '1': return
    p = f'{OUT}/contact.html'
    if not os.path.exists(p): return
    s = open(p).read()
    if 'b3grid' in s: return
    m = re.search(r'<section class="band band-light cwa-top centred">.*?</section>\s*', s, re.S)
    if not m: print('contact three ways: WhatsApp block not found'); return
    s = s.replace(m.group(0), BLOCK, 1)
    s = s.replace('</head>', CSS + '</head>', 1)
    s = s.replace('</body>', JS + '</body>', 1)
    open(p, 'w').write(s); print('contact page: three ways to book (with live Cal.com calendar)')

if __name__ == '__main__':
    build()
