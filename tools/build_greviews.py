# -*- coding: utf-8 -*-
"""21 Oct 2026: our own Google reviews box on the home page, in place of the Elfsight widget (its free plan has a
monthly view limit; once it runs out the box disappears). Same idea as the widget: rating summary, a "Review us on
Google" button, a short summary and a swipeable row of review cards, but it's part of the page, so there's no limit,
no third-party script and it loads instantly.
Reviews are copied word for word from Kat's Google Business Profile (read 21 Oct 2026). Update REVIEWS when new
ones arrive; reviews with a star rating but no words aren't shown, but they count in TOTAL.
Used by both builds, and run on the live home page with:  python3 tools/build_greviews.py /home/claude/Painting-Pixie/index.html"""
import os, re, sys, html

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
PLACE = 'ChIJ9RzrvqH2gYcR35xDxwANJEE'
WRITE = f'https://search.google.com/local/writereview?placeid={PLACE}'
READ = f'https://search.google.com/local/reviews?placeid={PLACE}'
RATING, TOTAL = '5.0', 10

REVIEWS = [   # (name as shown: first name + initial, month, words exactly as written on Google)
    ('James W.', 'August 2026', "Kat came to our son's birthday party and she was great, the kids loved her and her designs were fantastic. Thanks Kat, we'll be booking you again next year ⭐"),
    ('Rosemarie L.', 'August 2026', "My son had he’s face painted at a party and this lady was very good! He is deaf & she was polite and pointing for him to turn he’s head rather than some would just shove hes face into a direction upsetting him so this was a big brownie point! Very artistic and finished of with lovely little details"),
    ('Daniel C.', 'August 2026', "So amazing. Hired for our daughter’s 4th and was phenomenal. Non stop and everyone was so complimentary of the amazing face paints! Thank you Kat!!!"),
    ('Emily A.', 'August 2026', "Amazing lady! Done a fanatic job for 30 children! Would recommend fully"),
    ('Chantelle C.', 'October 2026', "So cute. She's brilliant"),
    ('Jamie D.', 'October 2026', "Amazing face Painting really good with the kids"),
    ('Claire C.', 'August 2026', "Amazing face painting! My son loved it!"),
    ('Alessandra F.', 'August 2026', "Great artwork! My daughters loved them"),
]
SUMMARY = ['Great with children, from small parties to 30 at once',
           'Detailed, artistic designs with lovely finishing touches',
           'Patient and considerate with every child']
COLOURS = ['#B0006A', '#2F8F5B', '#6A4BC4', '#C8641E', '#1F7FB8', '#A0376E', '#4E7D2E', '#8A4FB0']

STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.6l2.6 5.3 5.8.8-4.2 4.1 1 5.8L10 14.9l-5.2 2.7 1-5.8L1.6 7.7l5.8-.8z"/></svg>'
STARS = f'<span class="gr-stars" role="img" aria-label="5 out of 5 stars">{STAR * 5}</span>'
TICK = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7.6 14.2L3.7 10.3l1.4-1.4 2.5 2.5 7.3-7.3 1.4 1.4z"/></svg>'

CSS = '''<style>
/* our own Google reviews box (21 Oct 2026): replaces the Elfsight widget */
.gr{background:#FBF5EF;border-radius:18px;padding:30px 0 26px;max-width:1140px;margin:44px auto;width:calc(100% - 32px);box-sizing:border-box;color:#1B1712;font-family:Manrope,system-ui,sans-serif}
.gr-head{display:flex;flex-direction:column;align-items:center;gap:12px;padding:0 18px;text-align:center}
.gr-score{display:flex;align-items:center;gap:12px}
.gr-score b{font:700 52px/1 Fraunces,Georgia,serif}
.gr-score>span{display:flex;flex-direction:column;align-items:flex-start;gap:4px;font-size:15px;color:#4E463F}
.gr-stars{display:inline-flex;gap:2px}.gr-stars svg{width:20px;height:20px;fill:#F5B301}
.gr-btn{display:inline-block;background:#1A73E8;color:#fff!important;font-weight:800;font-size:15px;padding:11px 22px;border-radius:999px;text-decoration:none}
.gr-btn:hover{background:#1557B0}.gr-btn:focus-visible,.gr-arrow:focus-visible,.gr-more:focus-visible{outline:3px solid #B0006A;outline-offset:3px}
.gr-wrap{position:relative;margin-top:24px}
.gr-row{display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding:0 18px;padding:4px 18px 10px;scrollbar-width:none}
.gr-row::-webkit-scrollbar{display:none}
.gr-card{flex:0 0 300px;scroll-snap-align:start;background:#fff;border:1px solid #EADFD3;border-radius:16px;padding:18px 18px 16px;display:flex;flex-direction:column;gap:10px;box-sizing:border-box}
.gr-sum{background:#FFF7E8;border-color:#EBD3A6}
.gr-sum h3{margin:0;font:700 18px/1.2 Fraunces,Georgia,serif;color:#1B1712}
.gr-sum ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:9px}
.gr .gr-sum li{display:flex;gap:8px;font-size:15px;line-height:1.4;color:#2C2620}.gr-sum li svg{flex:0 0 18px;height:18px;fill:#2F8F5B;margin-top:1px}
.gr-who{display:flex;align-items:center;gap:10px}
.gr-av{flex:0 0 40px;height:40px;border-radius:50%;display:grid;place-items:center;color:#fff;font-weight:800;font-size:17px}
.gr-who b{display:block;font-size:16px;color:#1B1712}.gr .gr-who small{display:block;font-size:13px;color:#6B6157}
.gr .gr-text{margin:0;font-size:15.5px;line-height:1.5;color:#2C2620!important;opacity:1;display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden}
.gr .gr-card.open .gr-text{-webkit-line-clamp:unset;display:block}
.gr-more{align-self:flex-start;background:none;border:0;padding:0;font:inherit;font-size:14px;font-weight:700;color:#1A73E8;cursor:pointer}
.gr-arrow{position:absolute;top:50%;translate:0 -50%;width:42px;height:42px;border-radius:50%;border:0;background:#1B1712;color:#fff;font-size:20px;line-height:1;cursor:pointer;box-shadow:0 6px 16px rgba(0,0,0,.25);z-index:2}
.gr-prev{left:6px}.gr-next{right:6px}.gr-arrow[disabled]{opacity:0;pointer-events:none}
.gr-foot{display:flex;justify-content:center;margin-top:14px;padding:0 18px}
.gr .gr-foot a{font-size:14px;font-weight:700;color:#5A4E60!important}
@media(max-width:600px){.gr-card{flex-basis:84%}.gr-arrow{display:none}.gr-score b{font-size:44px}}
@media(prefers-reduced-motion:reduce){.gr-row{scroll-behavior:auto}}
</style>
'''

JS = '''<script>
(function(){
  var box=document.getElementById('greviews'); if(!box) return;
  var row=box.querySelector('.gr-row'), prev=box.querySelector('.gr-prev'), next=box.querySelector('.gr-next');
  function step(){ var c=row.querySelector('.gr-card'); return c ? c.getBoundingClientRect().width + 18 : 300; }
  function upd(){ prev.disabled = row.scrollLeft < 8; next.disabled = row.scrollLeft + row.clientWidth > row.scrollWidth - 8; }
  prev.addEventListener('click', function(){ row.scrollBy({left:-step(), behavior:'smooth'}); });
  next.addEventListener('click', function(){ row.scrollBy({left:step(), behavior:'smooth'}); });
  row.addEventListener('scroll', upd, {passive:true}); window.addEventListener('resize', upd); upd();
  box.querySelectorAll('.gr-card').forEach(function(c){
    var t=c.querySelector('.gr-text'), b=c.querySelector('.gr-more'); if(!t||!b) return;
    if(t.scrollHeight <= t.clientHeight + 2) { b.hidden = true; return; }
    b.addEventListener('click', function(){ var o=c.classList.toggle('open'); b.textContent = o ? 'Show less' : 'Read more'; b.setAttribute('aria-expanded', o); });
  });
  box.querySelectorAll('a[data-gr]').forEach(function(a){ a.addEventListener('click', function(){ if(window.gtag) gtag('event','google_reviews_click',{link:a.getAttribute('data-gr')}); }); });
})();
</script>
'''

def block():
    cards = ['<article class="gr-card gr-sum"><h3>What families say</h3><ul>'
             + ''.join(f'<li>{TICK}<span>{html.escape(s)}</span></li>' for s in SUMMARY) + f'</ul>{STARS}</article>']
    for i, (name, when, text) in enumerate(REVIEWS):
        cards.append(f'<article class="gr-card"><div class="gr-who"><span class="gr-av" style="background:{COLOURS[i % len(COLOURS)]}" aria-hidden="true">{html.escape(name[0])}</span>'
                     f'<span><b>{html.escape(name)}</b><small>Google review · {when}</small></span></div>{STARS}'
                     f'<p class="gr-text">{html.escape(text, quote=False)}</p><button class="gr-more" type="button" aria-expanded="false">Read more</button></article>')
    return (f'<section class="gr" id="greviews" aria-label="Google reviews">'
            f'<div class="gr-head"><div class="gr-score"><b>{RATING}</b><span>{STARS}<span>{TOTAL} reviews on Google</span></span></div>'
            f'<a class="gr-btn" href="{WRITE}" target="_blank" rel="noopener" data-gr="write">Review us on Google</a></div>'
            f'<div class="gr-wrap"><button class="gr-arrow gr-prev" type="button" aria-label="Previous reviews">‹</button>'
            f'<div class="gr-row" tabindex="0" aria-label="Reviews, scroll sideways for more">{"".join(cards)}</div>'
            f'<button class="gr-arrow gr-next" type="button" aria-label="More reviews">›</button></div>'
            f'<div class="gr-foot"><a href="{READ}" target="_blank" rel="noopener" data-gr="read">Read all our reviews on Google →</a></div></section>\n')

OLD = re.compile(r'(?:<!-- Elfsight Google Reviews[^>]*-->\s*)?<script src="https://elfsightcdn\.com/platform\.js" async></script>\s*'
                 r'(?:<div class="k-greviews"[^>]*>)?<div class="elfsight-app-[^"]*"[^>]*></div>(?:</div>)?\s*')

def apply(s):
    if 'id="greviews"' in s: return s, False
    if not OLD.search(s): return s, False
    s = OLD.sub(lambda m: block(), s, count=1)
    s = s.replace('</head>', CSS + '</head>', 1)
    s = s.replace('</body>', JS + '</body>', 1)
    return s, True

def run(path):
    s = open(path).read(); s, ok = apply(s)
    if ok: open(path, 'w').write(s)
    print('google reviews box:', 'added to' if ok else 'not changed on', os.path.basename(path))

if __name__ == '__main__':
    run(sys.argv[1] if len(sys.argv) > 1 else f'{OUT}/index.html')
