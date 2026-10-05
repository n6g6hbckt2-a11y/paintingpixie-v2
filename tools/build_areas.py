# -*- coding: utf-8 -*-
"""Areas page: interactive map + crawlable town list + service-area schema (matches the 20 Google Business Profile areas)."""
import re, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recent import RECENT

OUT = '/home/claude/paintingpixie-v2/draft'

# name, lat, lon, county, page, in Google Business Profile service areas
TOWNS = [
 ("Horsham", 51.0629, -0.3259, "West Sussex", "face-painter-horsham.html", True),
 ("Southwater", 51.0226, -0.3521, "West Sussex", "face-painter-west-sussex-villages.html", True),
 ("Crawley", 51.1092, -0.1872, "West Sussex", "face-painter-crawley.html", True),
 ("Haywards Heath", 50.9977, -0.1050, "West Sussex", "face-painter-haywards-heath.html", True),
 ("Cuckfield", 51.0060, -0.1440, "West Sussex", "face-painter-haywards-heath.html", True),
 ("Burgess Hill", 50.9581, -0.1335, "West Sussex", "face-painter-burgess-hill.html", True),
 ("East Grinstead", 51.1232, -0.0073, "West Sussex", "face-painter-east-grinstead.html", True),
 ("Billingshurst", 51.0226, -0.4526, "West Sussex", "face-painter-west-sussex-villages.html", True),
 ("Henfield", 50.9290, -0.2716, "West Sussex", "face-painter-west-sussex-villages.html", True),
 ("Steyning", 50.8870, -0.3270, "West Sussex", "face-painter-west-sussex-villages.html", True),
 ("Storrington", 50.9160, -0.4520, "West Sussex", "face-painter-west-sussex-villages.html", True),
 ("Pulborough", 50.9580, -0.5080, "West Sussex", "face-painter-west-sussex-villages.html", True),
 ("Midhurst", 50.9860, -0.7380, "West Sussex", "face-painter-south-downs.html", True),
 ("Petworth", 50.9870, -0.6100, "West Sussex", "face-painter-south-downs.html", True),
 ("Worthing", 50.8179, -0.3729, "West Sussex", "face-painter-worthing.html", False),
 ("Brighton & Hove", 50.8225, -0.1372, "East Sussex", "face-painter-brighton.html", False),
 ("Lewes", 50.8739, 0.0088, "East Sussex", "face-painter-lewes.html", False),
 ("Guildford", 51.2362, -0.5704, "Surrey", "face-painter-guildford.html", True),
 ("Godalming", 51.1857, -0.6148, "Surrey", "face-painter-guildford.html", True),
 ("Cranleigh", 51.1410, -0.4880, "Surrey", "face-painter-surrey-villages.html", True),
 ("Dorking", 51.2320, -0.3310, "Surrey", "face-painter-dorking.html", True),
 ("Leatherhead", 51.2960, -0.3330, "Surrey", "face-painter-surrey-villages.html", True),
 ("Horley", 51.1740, -0.1720, "Surrey", "face-painter-surrey-villages.html", True),
 ("Reigate & Redhill", 51.2370, -0.2060, "Surrey", "face-painter-reigate.html", False),
]
WIDER = [  # specialist events only (weddings, festivals, corporate): places Kat has travelled to, no local page
 ("Chichester", 50.8365, -0.7792), ("Arundel", 50.8550, -0.5550), ("Bognor Regis", 50.7830, -0.6760), ("Farnham", 51.2150, -0.7990),
 ("Woking", 51.3190, -0.5580), ("Epsom", 51.3330, -0.2670), ("Croydon", 51.3720, -0.1000), ("London", 51.5070, -0.1280),
 ("Sevenoaks", 51.2720, 0.1900), ("Tunbridge Wells", 51.1320, 0.2630), ("Uckfield", 50.9690, 0.0960), ("Eastbourne", 50.7680, 0.2900),
 ("Hastings", 50.8540, 0.5730), ("Maidstone", 51.2720, 0.5220), ("Portsmouth", 50.8050, -1.0870), ("Southampton", 50.9090, -1.4040),
]
EVENTS_ONLY = {"Brighton & Hove"}
COUNTY_PAGE = {"West Sussex": "face-painter-sussex.html", "East Sussex": "face-painter-sussex.html", "Surrey": "face-painter-surrey.html"}
NOTES = {  # one line per town for the pop-up
 "Horsham": "Home! No travel charge in town.", "Crawley": "Where Kat teaches and knows so many families.",
 "Haywards Heath": "One of Kat's most regular areas.", "Burgess Hill": "Just down the road from Macs Farm.",
 "East Grinstead": "A town Kat fell for.", "Worthing": "Parties by the sea.", "Brighton & Hove": "Events here: hens, weddings, Pride, festivals and corporate days.",
 "Lewes": "Bonfire town.", "Guildford": "Painted at the Festival of the Arts.", "Dorking": "Hills and vineyards.",
 "Reigate & Redhill": "Busy all year round.", "Midhurst": "Worth the drive.", "Petworth": "Painted here twice this summer.",
}

def recent_places():
    names = set()
    for items in RECENT.values():
        for p, n in items: names.add(p.split(',')[0].strip())
    return names

def build():
    p = f'{OUT}/areas.html'
    s = open(p).read()
    recent = recent_places()
    pins = [dict(n=n, lat=a, lon=b, c=c, u=u, note=NOTES.get(n, f'Parties and events in {n}.'), r=(n.split(' ')[0] in recent or n in recent)) for n, a, b, c, u, g in TOWNS]
    groups = {}
    for n, a, b, c, u, g in TOWNS: groups.setdefault(c, []).append((n, u))
    lists = ''.join(
        f'<div class="acol"><h3><a href="{COUNTY_PAGE[c]}">{c}</a></h3><ul>' +
        ''.join(f'<li><a href="{u}">Face painter in {n}{" (events)" if n in EVENTS_ONLY else ""}</a></li>' for n, u in items) + '</ul></div>'
        for c, items in groups.items())
    main = f'''<main class="lg loc" id="content" style="--acc:#FF4FA3">
<section class="band band-light"><div class="wrap">
<p class="eyebrow">Find your local page</p>
<h2>Where Kat paints</h2>
<p>The Painting Pixie brings face painting, festival glitter and party fun to events across Sussex and Surrey, from home in Horsham.
Tap a pin to see Kat's local page, or scroll down for the full list. Gold pins are places Kat has painted recently.</p>
<div id="areamap" class="areamap" role="region" aria-label="Map of the towns The Painting Pixie covers"></div>
<div class="legend"><span><i class="pin home"></i> Home: Horsham</span><span><i class="pin"></i> Regular area (within about 40 minutes), with a local page</span><span><i class="pin recent"></i> Painted here recently</span><span><i class="pin wide"></i> Wider area: specialist events</span></div>
<p class="small-note">The shaded zone is Kat's regular area: parties and local events within about 40 minutes of Horsham. Further afield, inside the dashed line, Kat travels for higher-value specialist events: weddings, festivals, corporate days and brand activations. <a href="contact.html">Ask about your event</a>.</p>
</div></section>
<section class="band band-dark"><div class="wrap">
<h2>Every area, by county</h2>
<div class="acols">{lists}</div>
<h3 class="wide-h">Further afield: weddings, festivals &amp; corporate events</h3>
<p class="wide-list">{', '.join(n for n, a, b in WIDER)}. <a href="contact.html">Ask about your event →</a></p>
</div></section>
<section class="band band-panel k-enquire centred"><div class="wrap"><h2>Is Kat free on your date?</h2>
<p>Tell Kat your date, town and roughly how many guests. She usually replies the same day.</p>
<a class="btn btn-gold" href="contact.html">Check my date</a></div></section>
</main>'''
    s = re.sub(r'<main class="lg">.*?</main>', lambda m: main, s, count=1, flags=re.S)
    # schema: service areas (the same 20 towns as the Google Business Profile, plus the other town pages)
    schema = {"@context": "https://schema.org", "@type": "Service", "serviceType": "Face painting",
              "name": "Face painting across Sussex and Surrey",
              "provider": {"@type": "LocalBusiness", "@id": "https://paintingpixie.com/#business", "name": "The Painting Pixie", "url": "https://paintingpixie.com/"},
              "areaServed": [{"@type": "City", "name": n.replace(' & ', ' and ') if '&' in n else n,
                              "containedInPlace": {"@type": "AdministrativeArea", "name": c}} for n, a, b, c, u, g in TOWNS]}
    head, body = s.split('</head>', 1)
    head += ('<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">\n'
             '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=1) + '\n</script>\n')
    css = '''<style>
.areamap{height:560px;border-radius:16px;margin-top:24px;border:6px solid #fff;box-shadow:0 30px 60px -30px rgba(60,30,40,.45);background:#1B1A22;z-index:0}
.areamap .leaflet-popup-content-wrapper{background:#1F1C25;color:#F5F1EA;border-radius:12px}
.areamap .leaflet-popup-tip{background:#1F1C25}
.areamap .leaflet-popup-content{margin:12px 16px;font:600 14px/1.45 Manrope,system-ui,sans-serif}
.areamap .leaflet-popup-content b{display:block;font-family:Fraunces,serif;font-weight:400;font-size:20px;color:#F5F1EA}
.areamap .leaflet-popup-content a{color:#E2BE7A;font-weight:800}
.pin{width:18px;height:18px;border-radius:50%;background:#FF4FA3;border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,.4)}
.pin.recent{background:#E2BE7A;width:22px;height:22px}
.pin.home{background:#2FD4C4;width:24px;height:24px}
.pin.wide{background:transparent;border:3px solid #7A5BB0;width:14px;height:14px;box-shadow:none}
.legend{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:16px;font-size:14px;font-weight:700;color:#4E463F}
.legend span{display:inline-flex;align-items:center;gap:8px}
.legend .pin{display:inline-block}
.wide-h{margin:34px 0 6px;font-family:Fraunces,serif;font-weight:400;font-size:24px}
.wide-list{color:var(--muted)}
.acols{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:20px}
.acol h3{margin:0 0 10px;font-family:Fraunces,serif;font-weight:400;font-size:26px}
.acol h3 a{color:var(--ink);text-decoration:none}
.acol ul{list-style:none;margin:0;padding:0}
.acol li{padding:7px 0;border-bottom:1px solid var(--line)}
.acol li a{color:var(--muted);text-decoration:none;font-weight:600}
.acol li a:hover{color:var(--gold)}
@media(max-width:800px){.acols{grid-template-columns:1fr}.areamap{height:440px}}
</style>'''
    js = f'''<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script>
(function(){{
  if (!window.L) return;
  var pins = {json.dumps(pins, ensure_ascii=False)};
  var WIDER_PINS = {json.dumps(WIDER)};
  var map = L.map('areamap', {{scrollWheelZoom:false}}).setView([51.03,-0.33], 9);
  L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
    maxZoom: 14, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
  }}).addTo(map);
  var home = [51.0629,-0.3259];
  L.circle(home, {{radius: 36000, color:'#FF4FA3', weight:1.5, fillColor:'#FF4FA3', fillOpacity:.08}}).addTo(map);
  L.circle(home, {{radius: 80000, color:'#7A5BB0', weight:1.5, dashArray:'6 8', fill:false}}).addTo(map);
  var wider = WIDER_PINS;
  wider.forEach(function(p){{
    var icon = L.divIcon({{className:'', html:'<div class="pin wide"></div>', iconSize:[16,16], iconAnchor:[8,8]}});
    L.marker([p[1],p[2]], {{icon:icon, title:p[0], alt:p[0]}}).addTo(map)
      .bindPopup('<b>'+p[0]+'</b>Further afield: Kat travels here for weddings, festivals, corporate and brand events.<br><a href="contact.html">Ask about your event &rarr;</a>');
  }});
  var bounds = [];
  pins.forEach(function(p){{
    var cls = 'pin' + (p.n === 'Horsham' ? ' home' : (p.r ? ' recent' : ''));
    var icon = L.divIcon({{className:'', html:'<div class="'+cls+'"></div>', iconSize:[24,24], iconAnchor:[12,12]}});
    L.marker([p.lat,p.lon], {{icon:icon, title:p.n, alt:p.n}}).addTo(map)
      .bindPopup('<b>'+p.n+'</b>'+p.note+(p.r?'<br>&#9733; Painted here recently':'')+'<br><a href="'+p.u+'">See the '+p.n+' page &rarr;</a>');
    bounds.push([p.lat,p.lon]);
  }});
  map.fitBounds(bounds, {{padding:[40,40]}});
}})();
</script>'''
    body = body.replace('<script src="site.js"></script>', css + '\n' + js + '\n<script src="site.js"></script>', 1)
    open(p, 'w').write(head + '</head>' + body)
    print('areas page built with', len(TOWNS), 'towns')

if __name__ == '__main__':
    build()
