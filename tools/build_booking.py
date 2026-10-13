# -*- coding: utf-8 -*-
"""Book a party page (13 Oct 2026): standard children's parties booked online with a deposit (Cal.com + Stripe),
everything else by quote. Includes a travel-cost checker (postcode -> estimated road miles from Horsham).
Kat's rules: prices £130 (2h) / £160 (3h); deposit 1/3, max £60; travel 55p a mile, return trip, for the miles beyond 15
from home; weekends from 9am and weekdays from 5:30pm, no finish limit; balance paid on the day; at least 7 days' notice; deposit refundable to 14 days, 50% to 7 days,
then not refundable but can move to a new date.
Held back from the live site (PP_HOLD) until Kat approves and the Cal.com links exist."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_extra as X, inner_layout

CAL = {   # Cal.com booking links, filled in once Kat's account is set up
    '2h': os.environ.get('PP_CAL_2H', ''),
    '3h': os.environ.get('PP_CAL_3H', ''),
}
PACKAGES = [
    ('2h', 'Classic Party', '2-hour', 130, ['2 hours of face painting', 'High-quality, skin-safe paints', 'Fast, fun party designs']),
    ('3h', 'Ultimate Sparkle', '3-hour', 160, ['3 hours of face painting', 'Premium paints + bio-glitter', 'Face gems & detailed designs']),
]
def deposit(price): return min(round(price / 3, 2), 60)

CSS = '''<style>
.bkpk{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px}
.bkpk article{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:24px;display:flex;flex-direction:column;gap:10px}
.band-light .bkpk article{background:#fff;border-color:#E8DED3}
.bkpk h3{margin:0;font-size:26px}.bkpk .pr{font-family:Fraunces,serif;font-size:38px;line-height:1}
.bkpk .dp{font-size:15px;opacity:.85}.bkpk ul{margin:4px 0 8px;padding-left:20px}.bkpk .btn{align-self:flex-start;margin-top:auto}
.bksteps{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:20px;counter-reset:s;padding:0;list-style:none}
.bksteps li{counter-increment:s;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px}
.band-light .bksteps li{background:#fff;border-color:#E8DED3;color:#1B1712}.band-light .bksteps li b{color:#1B1712}
.bksteps li::before{content:counter(s);display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--gold);color:#1A1420;font-weight:800;margin-bottom:8px}
.trav{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px;align-items:center}
.trav input{width:auto;flex:0 1 260px;background:#fff;color:#1B1712;font:inherit;font-size:17px;padding:12px 16px;border-radius:12px;border:1px solid var(--line);min-width:220px;text-transform:uppercase}
.travout{margin-top:14px;font-size:18px;font-weight:700;min-height:1.5em}
.bkterms li{margin:6px 0}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
@media(max-width:800px){.bkpk{grid-template-columns:1fr}.bksteps{grid-template-columns:1fr 1fr}}
@media(max-width:500px){.bksteps{grid-template-columns:1fr}}
</style>'''

TRAVEL_JS = '''<script>
(function(){
  /* travel estimate: straight-line distance from Horsham x 1.25 for roads; 55p a mile, there and back, for the miles beyond 15 */
  var HOME=[51.0629,-0.3259], FREE=15, RATE=0.55, ROAD=1.25;
  var f=document.getElementById('travform'), out=document.getElementById('travout'), inp=document.getElementById('pc');
  function miles(a,b){var R=3958.8,r=Math.PI/180,dl=(b[0]-a[0])*r,dn=(b[1]-a[1])*r,
    h=Math.sin(dl/2)*Math.sin(dl/2)+Math.cos(a[0]*r)*Math.cos(b[0]*r)*Math.sin(dn/2)*Math.sin(dn/2);return 2*R*Math.asin(Math.sqrt(h));}
  function show(lat,lon,label){
    var m=Math.round(miles(HOME,[lat,lon])*ROAD), over=Math.max(0,m-FREE), cost=(over*2*RATE).toFixed(2);
    out.innerHTML = m<3 ? label+' is right on Kat’s doorstep: <b>no travel charge</b>.' : over===0 ? label+' is about '+m+' miles from Horsham: <b>no travel charge</b>.'
      : label+' is about '+m+' miles from Horsham: travel is about <b>£'+cost+'</b> ('+over+' miles over 15, there and back, at 55p a mile). Kat confirms the exact figure.';
    if(window.gtag)gtag('event','travel_check',{miles:m});
  }
  function go(){
    var pc=inp.value.trim().toUpperCase().replace(/\\s+/g,'');
    if(!/^[A-Z]{1,2}[0-9][A-Z0-9]?([0-9][A-Z]{2})?$/.test(pc)){out.textContent='Please enter a UK postcode, for example RH12 1AA.';return;}
    out.textContent='Checking…';
    var full=pc.length>4, url='https://api.postcodes.io/'+(full?'postcodes/':'outcodes/')+encodeURIComponent(pc);
    fetch(url).then(function(r){return r.json()}).then(function(d){
      if(!d||d.status!==200||!d.result){out.textContent='Sorry, that postcode wasn\\'t found. Check it, or just ask Kat.';return;}
      var label=(full?(d.result.admin_ward||d.result.admin_district||inp.value.toUpperCase()):(d.result.admin_district&&d.result.admin_district[0]||pc));
      show(d.result.latitude,d.result.longitude,label);
    }).catch(function(){out.textContent='Sorry, the travel checker isn\\'t available right now. Kat will confirm any travel cost.';});
  }
  document.getElementById('travbtn').addEventListener('click',go);
  inp.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();go();}});
})();
</script>'''

def card(key, name, length, price, feats):
    dep = deposit(price)
    url = CAL.get(key)
    btn = (f'<a class="btn btn-gold" href="{url}" target="_blank" rel="noopener">Book the {length} party →</a>' if url else
           f'<a class="btn btn-gold" href="{X.wa(f"Hi Kat! I would like to book a {length} party. Date: Time: Postcode: ")}" target="_blank" rel="noopener">Book the {length} party →</a>')
    lis = ''.join(f'<li>{X.esc(f)}</li>' for f in feats)
    return (f'<article><h3>{X.esc(name)}</h3><div class="pr">£{price}</div>'
            f'<div class="dp">£{dep:.2f} deposit to secure your date · balance plus any travel on the day</div><ul>{lis}</ul>{btn}</article>')

def build():
    cards = ''.join(card(*p) for p in PACKAGES)
    main = f'''<main class="lg" id="content">
<section class="band band-light"><div class="wrap">
<p class="eyebrow">Children's parties</p><h2>Book your party online</h2>
<p>Pick a package, choose a date and time Kat is free, and pay a deposit to secure it. You'll get a confirmation straight away.</p>
<div class="bkpk">{cards}</div>
<p class="small-note">Parties at weekends from 9am, and on weekdays from 5:30pm. Book at least 7 days ahead. Planning a wedding, festival, corporate or hen event? <a href="contact.html">Ask Kat for a quote</a> instead.</p>
</div></section>
<section class="band band-dark"><div class="wrap">
<p class="eyebrow">Travel</p><h2>Is there a travel charge?</h2>
<p>No charge within 15 miles of Kat's home in Horsham. Further away, travel is 55p a mile, there and back, for the miles beyond 15. Check your postcode:</p>
<div id="travform" class="trav"><label class="sr" for="pc">Party postcode</label><input id="pc" name="pc" placeholder="Party postcode" maxlength="8" autocomplete="postal-code"><button id="travbtn" class="btn btn-gold" type="button">Check travel</button></div>
<p id="travout" class="travout" aria-live="polite"></p>
<p class="small-note">An estimate by distance; Kat confirms the exact mileage when she confirms your booking. Travel is added to the balance, not the deposit.</p>
</div></section>
<section class="band band-light"><div class="wrap">
<p class="eyebrow">How it works</p><h2>From booking to party day</h2>
<ol class="bksteps"><li><b>Choose</b><br>Pick the 2-hour or 3-hour party.</li><li><b>Pick a date</b><br>Only dates and times Kat is free are shown.</li>
<li><b>Pay the deposit</b><br>One third of the price, by card.</li><li><b>Party day</b><br>Kat arrives, sets up and paints. The balance and any travel are paid on the day.</li></ol>
</div></section>
<section class="band band-dark"><div class="wrap">
<p class="eyebrow">Booking terms</p><h2>Deposits and changes</h2>
<ul class="bkterms"><li>The deposit is one third of the party price (a maximum of £60).</li>
<li>The balance, plus any travel, is paid on the day.</li>
<li>Cancel 14 days or more before the party: full refund of the deposit.</li>
<li>Cancel 7 to 13 days before: 50% of the deposit is refunded.</li>
<li>Less than 7 days before: the deposit isn't refunded, but it can be used to rearrange to a new date.</li></ul>
</div></section>
<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Prefer to talk first?</h2>
<p>Message Kat and she'll get back to you, usually the same day.</p>
<a class="btn btn-wa" href="{X.wa("Hi Kat! I'd like to ask about a party. Date: Town: ")}" target="_blank" rel="noopener">WhatsApp Kat</a> <a class="btn btn-ghost" href="contact.html">Send an enquiry</a></div></section>
{inner_layout.TRUST_BAND}
</main>'''
    X.page_from('services.html', 'book.html', 'Book a Face Painter for Your Party | The Painting Pixie',
                "Book Kat for your child's party online: 2-hour party £130, 3-hour party £160. Secure your date with a deposit. Sussex & Surrey, 5.0 rated, insured, DBS checked.",
                'https://paintingpixie.com/book.html', X.FRAME_CSS + CSS,
                X.framed_hero('Book a party', 'Book Your Party',
                              'Choose a package, pick a free date and secure it with a deposit. Weekends from 9am, and weekdays from 5:30pm.',
                              '<a class="btn btn-gold" href="#content">See packages</a>',
                              '../img/g/kat-close-painting-1600.webp', 1600, 1067, 'Kat face painting a butterfly design on a girl', '★★★★★ Kat at work'),
                main + TRAVEL_JS)
    print('booking page built (book.html)', 'with Cal.com links' if all(CAL.values()) else '(no Cal.com links yet: buttons go to WhatsApp)')

if __name__ == '__main__':
    build()
