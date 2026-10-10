# -*- coding: utf-8 -*-
"""Areas page: interactive map + crawlable town list + service-area schema (matches the 20 Google Business Profile areas)."""
import re, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recent import RECENT, PERIOD, COMING_UP

OUT = __import__('os').environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')

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
 # added 7 Oct 2026 from Kat's travel log (recent and coming-up places)
 ("Kingsfold", 51.1110, -0.3330, "West Sussex", "face-painter-horsham.html", False),
 ("Small Dole", 50.9030, -0.2650, "West Sussex", "face-painter-west-sussex-villages.html", False),
 ("Upper Beeding", 50.8890, -0.3060, "West Sussex", "face-painter-west-sussex-villages.html", False),
 ("Macs Farm", 50.9390, -0.1100, "West Sussex", "face-painter-burgess-hill.html", False),
 ("Portslade", 50.8420, -0.2160, "East Sussex", "face-painter-brighton.html", False),
 ("Kingswood", 51.2950, -0.2100, "Surrey", "face-painter-reigate.html", False),
]
WIDER = [  # specialist events only (weddings, festivals, corporate): places Kat has travelled to, no local page
 ("Chichester", 50.8365, -0.7792), ("Arundel", 50.8550, -0.5550), ("Bognor Regis", 50.7830, -0.6760), ("Farnham", 51.2150, -0.7990),
 ("Woking", 51.3190, -0.5580), ("Epsom", 51.3330, -0.2670), ("Croydon", 51.3720, -0.1000), ("Sutton", 51.3618, -0.1945), ("Putney", 51.4600, -0.2160), ("London", 51.5070, -0.1280),
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

def recent_text():
    seen = []
    for items in RECENT.values():
        for p, n in items:
            q = p.replace(', near ', ' near ').replace(', ', ' (', 1) + (')' if ', ' in p.replace(', near ', '') else '')
            if q not in seen: seen.append(q)
    return ', '.join(seen[:-1]) + ' and ' + seen[-1]

def recent_places():
    names = set()
    for items in RECENT.values():
        for p, n in items: names.update(x.strip() for x in p.split(','))
    return names

def soon_places():
    return {p.split(',')[0].strip() for p, *_ in COMING_UP}

def wider_soon(n):
    if n == 'London':
        return '; '.join(f'{pl.split(",")[0]}, {d}' for pl, d, *_ in COMING_UP if 'London' in pl)
    return next((d for pl, d, *_ in COMING_UP if pl.split(',')[0].strip() == n), '')

def static_map(recent, towns=None, wider=None, box=(51.42, 50.70, -0.98, 0.30)):
    """Drawn map shown straight away (and kept if the live map can't load): pins at real positions, linked to town pages."""
    import math
    towns = TOWNS if towns is None else towns
    wider = WIDER if wider is None else wider
    lat0, lat1, lon0, lon1 = box
    kx = math.cos(math.radians(51.05))
    W = 1000
    H = 640 if box == (51.42, 50.70, -0.98, 0.30) else int(W * (lat0 - lat1) / ((lon1 - lon0) * kx))
    sc = min(W / ((lon1 - lon0) * kx), H / (lat0 - lat1))
    ox = (W - (lon1 - lon0) * kx * sc) / 2; oy = (H - (lat0 - lat1) * sc) / 2
    xy = lambda la, lo: (ox + (lo - lon0) * kx * sc, oy + (lat0 - la) * sc)
    hx, hy = xy(51.0629, -0.3259)
    km = sc / 111.0
    font = 'font-family="Manrope,system-ui,sans-serif"'
    coast = [(50.80, -2.5), (50.79, -1.2), (50.78, -0.80), (50.80, -0.55), (50.81, -0.37), (50.83, -0.13), (50.79, 0.10), (50.76, 0.30), (50.80, 0.6), (50.82, 1.8)]
    pts = [xy(a, b) for a, b in coast]
    d = f'M{pts[0][0]:.0f},{pts[0][1]:.0f} ' + ' '.join(f'L{x:.0f},{y:.0f}' for x, y in pts[1:]) + f' L{pts[-1][0]:.0f},{H + 50} L{pts[0][0]:.0f},{H + 50}Z'
    o = [f'<svg viewBox="0 0 {W} {H}" style="aspect-ratio:{W}/{H}" class="smap" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Map of the towns The Painting Pixie covers">',
         f'<rect x="-200" y="-200" width="{W + 400}" height="{H + 400}" fill="#231F30"/>',
         f'<path d="{d}" fill="#173149"/>',
         f'<text x="{xy(50.745, -0.62)[0]:.0f}" y="{xy(50.745, -0.62)[1]:.0f}" fill="#5D87AA" font-size="16" font-style="italic" {font}>English Channel</text>',
         f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{80 * km:.0f}" fill="none" stroke="#9C83D1" stroke-width="2" stroke-dasharray="7 9"/>',
         f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="{36 * km:.0f}" fill="#FF4FA3" fill-opacity=".12" stroke="#FF4FA3" stroke-width="2"/>']
    for n, a, b in wider:
        if not (lat1 < a < lat0 and lon0 < b < lon1): continue
        x, y = xy(a, b)
        o.append(f'<a href="contact.html"><circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="{"#A77BFF" if wider_soon(n) and n not in recent else "#E2BE7A" if n in recent else "#231F30"}" stroke="#9C83D1" stroke-width="2.4"><title>{n}: Kat travels here for parties, local events, weddings, festivals and corporate events</title></circle>'
                 f'<text x="{x + 10:.0f}" y="{y + 5:.0f}" fill="#B7A9D6" font-size="14" {font}>{n}</text></a>')
    left = {'Billingshurst', 'Cuckfield', 'Midhurst', 'Guildford', 'Dorking', 'Henfield', 'Storrington', 'Godalming', 'Leatherhead', 'Kingsfold', 'Upper Beeding'}
    dy = {'Steyning': 16, 'Upper Beeding': -6}
    for n, a, b, c, u, g in towns:
        x, y = xy(a, b)
        col = '#2FD4C4' if n == 'Horsham' else ('#E2BE7A' if (n.split(' ')[0] in recent or n in recent) else '#A77BFF' if n in soon_places() else '#FF4FA3')
        r = 11 if n == 'Horsham' else 8
        tx, anchor = (x - 13, 'end') if n in left else (x + 13, 'start')
        o.append(f'<a href="{u}"><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{col}" stroke="#fff" stroke-width="2.4"><title>Face painter in {n}</title></circle>'
                 f'<text x="{tx:.0f}" y="{y + 5 + dy.get(n, 0):.0f}" text-anchor="{anchor}" fill="#F5F1EA" font-size="15" font-weight="700" {font} paint-order="stroke" stroke="#231F30" stroke-width="4">{n}</text></a>')
    o.append('</svg>')
    return ''.join(o)

MAP_CSS = '''<style>
.smap{display:block;width:100%;height:100%}
@media(max-width:800px){.areamap:not(.is-live){height:auto;aspect-ratio:1000/640}}
.smap a:hover circle{stroke:#E2BE7A;stroke-width:3}
.areamap:has(.smap){background:#231F30}
#livemap{position:absolute;inset:0;opacity:0;pointer-events:none;border-radius:10px}
.areamap.is-live #livemap{opacity:1;pointer-events:auto}
.areamap{position:relative;overflow:hidden;height:560px;border-radius:16px;margin-top:24px;border:6px solid #fff;box-shadow:0 30px 60px -30px rgba(60,30,40,.45);background:#1B1A22;z-index:0}
.areamap .leaflet-popup-content-wrapper{background:#1F1C25;color:#F5F1EA;border-radius:12px}
.areamap .leaflet-popup-tip{background:#1F1C25}
.areamap .leaflet-popup-content{margin:12px 16px;font:600 14px/1.45 Manrope,system-ui,sans-serif}
.areamap .leaflet-popup-content b{display:block;font-family:Fraunces,serif;font-weight:400;font-size:20px;color:#F5F1EA}
.areamap .leaflet-popup-content a{color:#E2BE7A;font-weight:800}
.pin{width:18px;height:18px;border-radius:50%;background:#FF4FA3;border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,.4)}
.pin.recent{background:#E2BE7A;width:22px;height:22px}
.pin.home{background:#2FD4C4;width:24px;height:24px}
.pin.wide.wrecent{background:#E2BE7A}
.pin.wide{background:transparent;border:3px solid #7A5BB0;width:14px;height:14px;box-shadow:none}
.pin.soon{background:#A77BFF}.pin.wide.wsoon{background:#A77BFF}
.legend{display:flex;flex-wrap:wrap;gap:10px 22px;margin-top:16px;font-size:14px;font-weight:700;color:#4E463F}
.legend span{display:inline-flex;align-items:center;gap:8px}
.legend .pin{display:inline-block;flex:0 0 auto;margin:0;position:static;transform:none}
.recentareas{margin:14px 0 4px;color:#4E463F;font-size:15px}.recentareas b{color:#1B1712}
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

def map_js(pins, wider_pins):
    """Live map (OpenStreetMap via Leaflet) built under the drawn map; shown once map pictures load."""
    return f'''<script src="../vendor/leaflet/leaflet.js"></script>
<script>
(function(){{
  if (!window.L) return;   // the drawn map stays if the live map can't load
  var box = document.getElementById('areamap'), drawn = box.innerHTML;
  var pins = {json.dumps(pins, ensure_ascii=False)};
  var WIDER_PINS = {json.dumps(wider_pins)};
  // the live map is built in a layer underneath and only shown once real map pictures have loaded
  var live = document.createElement('div'); live.id = 'livemap'; box.appendChild(live);
  var map = L.map('livemap', {{scrollWheelZoom:false}}).setView([51.03,-0.33], 9);
  var shown = false;
  function show(){{ if (shown) return; shown = true; box.classList.add('is-live'); var sv = box.querySelector('.smap'); if (sv) sv.remove(); map.invalidateSize(); map.fitBounds(bounds, {{padding:[40,40]}}); }}
  var ok = 0, bad = 0;
  function tiles(url, attr) {{
    var t = L.tileLayer(url, {{maxZoom: 14, attribution: attr}});
    t.on('tileload', function(){{ ok++; if (ok >= 3) show(); }});
    t.on('tileerror', function(){{ bad++; }});
    return t.addTo(map);
  }}
  var layer = tiles('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors');
  setTimeout(function(){{ if (ok === 0) {{ map.remove(); live.remove(); }} }}, 8000);   // no map pictures reachable: keep the drawn map
  var home = [51.0629,-0.3259];
  L.circle(home, {{radius: 36000, color:'#FF4FA3', weight:1.5, fillColor:'#FF4FA3', fillOpacity:.08}}).addTo(map);
  L.circle(home, {{radius: 80000, color:'#7A5BB0', weight:1.5, dashArray:'6 8', fill:false}}).addTo(map);
  var wider = WIDER_PINS;
  wider.forEach(function(p){{
    var icon = L.divIcon({{className:'', html:'<div class="pin wide'+(p[3]?' wrecent':(p[4]?' wsoon':''))+'"></div>', iconSize:[16,16], iconAnchor:[8,8]}});
    L.marker([p[1],p[2]], {{icon:icon, title:p[0], alt:p[0]}}).addTo(map)
      .bindPopup('<b>'+p[0]+'</b>Further afield: Kat travels here for parties and local events, weddings, festivals, corporate and brand events.'+(p[3]?'<br>&#9733; Painted here recently'+(p[0]==='London'?': Baker Street':''):'')+(p[4]?'<br>&#10024; Coming up in the next 2 months':'')+'<br><a href="contact.html">Ask about your event &rarr;</a>');
  }});
  var bounds = [];
  pins.forEach(function(p){{
    var cls = 'pin' + (p.n === 'Horsham' ? ' home' : (p.r ? ' recent' : (p.s ? ' soon' : '')));
    var icon = L.divIcon({{className:'', html:'<div class="'+cls+'"></div>', iconSize:[24,24], iconAnchor:[12,12]}});
    L.marker([p.lat,p.lon], {{icon:icon, title:p.n, alt:p.n}}).addTo(map)
      .bindPopup('<b>'+p.n+'</b>'+p.note+(p.r?'<br>&#9733; Painted here recently':'')+(p.s?'<br>&#10024; Coming up in the next 2 months':'')+'<br><a href="'+p.u+'">See the '+p.n+' page &rarr;</a>');
    bounds.push([p.lat,p.lon]);
  }});
  map.fitBounds(bounds, {{padding:[40,40]}});
}})();
</script>'''

def build():
    p = f'{OUT}/areas.html'
    s = open(p).read()
    recent = recent_places()
    pins = [dict(n=n, lat=a, lon=b, c=c, u=u, note=NOTES.get(n, f'Parties and events in {n}.'), r=(n.split(' ')[0] in recent or n in recent), s=any(pl.split(',')[0].strip() == n for pl, *_ in COMING_UP)) for n, a, b, c, u, g in TOWNS]
    groups = {}
    for n, a, b, c, u, g in TOWNS:
        if n in ("Macs Farm",): continue   # a venue, not a town: pin only
        groups.setdefault(c, []).append((n, u))
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
<div id="areamap" class="areamap" role="region" aria-label="Map of the towns The Painting Pixie covers">{static_map(recent)}</div>
<div class="legend"><span><i class="pin home"></i> Home: Horsham</span><span><i class="pin"></i> Regular area (within about 40 minutes), with a local page</span><span><i class="pin recent"></i> Painted here recently</span><span><i class="pin soon"></i> Coming up in the next 2 months</span><span><i class="pin wide"></i> Further afield: Kat travels here too</span></div>
<p class="recentareas"><b>Recently painted ({PERIOD}):</b> {recent_text()}.</p>
<p class="recentareas"><b>Coming up in the next 2 months:</b> {'; '.join(f"{p.replace(', ', ' (', 1)}{')' if ', ' in p else ''}" for p, d, *_ in COMING_UP)}.</p>
<p class="small-note">The shaded zone is Kat's regular area: parties and local events within about 40 minutes of Horsham. Kat travels further afield too, inside the dashed line: for weddings, festivals, corporate days and brand activations, and for parties and local events as well. <a href="contact.html">Ask about your date</a>.</p>
</div></section>
<section class="band band-dark"><div class="wrap">
<h2>Every area, by county</h2>
<div class="acols">{lists}</div>
<h3 class="wide-h">Further afield: Kat travels here too</h3>
<p class="wide-list">{', '.join(n for n, a, b in WIDER)}. Parties, local events, weddings, festivals and corporate events. <a href="contact.html">Ask about your date →</a></p>
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
    head += ('<link rel="stylesheet" href="../vendor/leaflet/leaflet.css">\n'
             '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=1) + '\n</script>\n')
    css = MAP_CSS
    js = map_js(pins, [[n, a, b, n in recent, bool(wider_soon(n))] for n, a, b in WIDER])
    body = body.replace('<script src="site.js"></script>', css + '\n' + js + '\n<script src="site.js"></script>', 1)
    open(p, 'w').write(head + '</head>' + body)
    print('areas page built with', len(TOWNS), 'towns')

if __name__ == '__main__':
    build()
