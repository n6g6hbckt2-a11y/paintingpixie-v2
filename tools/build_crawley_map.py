# -*- coding: utf-8 -*-
"""16 Oct (Phil): on the Crawley page, join the illustrated postcard, "Where Crawley parties happen" and
"Halls and party venues" into one section, with a drawn town map showing where each place is.
Reads the place blurbs and venue links from the page that build_locations / build_venue_insert made, so the
wording stays theirs. Runs after build_venue_insert."""
import os, re, math, html, json

OUT = os.environ.get('PP_OUT', '/home/claude/paintingpixie-v2/draft')
PAGE = 'face-painter-crawley.html'

# positions (lat, lon), checked 16 Oct: Wikipedia (K2, Tilgate Lake), Great Britain Guide (Goffs Park), Historic England listing (Worth Park fountain)
PLACES = {
    'Tilgate Park': (51.0950, -0.1750),
    'Goffs Park': (51.1135, -0.1990),
    'K2 Crawley': (51.0972, -0.1914),
    'Worth Park': (51.1274, -0.1502),
    'Memorial Gardens': (51.1132, -0.1852),
}
HOODS = [('Ifield', 51.126, -0.216), ('Langley Green', 51.134, -0.208), ('Northgate', 51.124, -0.181), ('West Green', 51.1195, -0.205),
         ('Gossops Green', 51.110, -0.219), ('Bewbush', 51.0965, -0.228), ('Broadfield', 51.090, -0.206), ('Southgate', 51.104, -0.188),
         ('Tilgate', 51.0995, -0.184), ('Furnace Green', 51.1050, -0.170), ('Three Bridges', 51.1110, -0.163), ('Pound Hill', 51.1165, -0.148),
         ('Maidenbower', 51.1015, -0.158), ('Forge Wood', 51.1360, -0.153)]
ROADS = [('M23', [(51.160, -0.166), (51.136, -0.150), (51.118, -0.137), (51.102, -0.146), (51.090, -0.170), (51.080, -0.196)], '#4A7FC1', 7),
         ('A23', [(51.160, -0.190), (51.128, -0.191), (51.114, -0.194), (51.098, -0.199), (51.080, -0.198)], '#3F8F5A', 5),
         ('A264', [(51.098, -0.260), (51.101, -0.235), (51.104, -0.212), (51.098, -0.199)], '#3F8F5A', 4),
         ('A264', [(51.118, -0.137), (51.122, -0.110)], '#3F8F5A', 4)]
RAIL = [[(51.160, -0.170), (51.118, -0.161), (51.095, -0.152), (51.078, -0.150)],
        [(51.118, -0.161), (51.113, -0.186), (51.115, -0.214), (51.112, -0.255)]]
STATIONS = [('Crawley', 51.1125, -0.1865), ('Three Bridges', 51.1170, -0.1610), ('Ifield', 51.1155, -0.2145)]
BOX = (51.142, 51.080, -0.250, -0.120)   # north, south, west, east

def town_map(pins):
    n, s, w, e = BOX
    kx = math.cos(math.radians(51.11))
    W = 760; H = int(W * (n - s) / ((e - w) * kx))
    xy = lambda la, lo: ((lo - w) / (e - w) * W, (n - la) / (n - s) * H)
    f = 'font-family="Manrope,system-ui,sans-serif"'
    o = [f'<svg class="cmap" viewBox="0 0 {W} {H}" role="img" aria-label="Map of Crawley showing where the parks and venues are">',
         f'<rect width="{W}" height="{H}" fill="#F6F0E6"/>']
    # parks as soft green blobs
    for nm in ('Tilgate Park', 'Goffs Park', 'Worth Park'):
        x, y = xy(*PLACES[nm]); o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="34" ry="24" fill="#C9E2A8" opacity=".9"/>')
    x, y = xy(51.0950, -0.1720); o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="22" ry="10" fill="#9CCBEA"/>')   # Tilgate lake
    for pts in RAIL:
        d = 'M' + ' L'.join('%.0f,%.0f' % xy(*p) for p in pts)
        o.append(f'<path d="{d}" stroke="#7A6F80" stroke-width="3" fill="none"/><path d="{d}" stroke="#F6F0E6" stroke-width="1.6" fill="none" stroke-dasharray="6 6"/>')
    for name, pts, col, sw in ROADS:
        d = 'M' + ' L'.join('%.0f,%.0f' % xy(*p) for p in pts)
        o.append(f'<path d="{d}" stroke="#fff" stroke-width="{sw + 4}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<path d="{d}" stroke="{col}" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    for name, pts, col, sw in ROADS[:3]:
        x, y = xy(*pts[1 if name != 'A264' else 1])
        if name == 'M23': x, y = xy(51.128, -0.144)
        if name == 'A23': x, y = xy(51.1285, -0.1912)
        if name == 'A264': x, y = xy(51.0985, -0.2455)
        o.append(f'<rect x="{x - 19:.0f}" y="{y - 10:.0f}" width="38" height="20" rx="4" fill="{col}"/><text x="{x:.0f}" y="{y + 5:.0f}" text-anchor="middle" font-size="12.5" font-weight="800" fill="#fff" {f}>{name}</text>')
    for nm, la, lo in STATIONS:
        x, y = xy(la, lo)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#fff" stroke="#7A6F80" stroke-width="2.5"/>')
    for nm, la, lo in HOODS:
        x, y = xy(la, lo)
        o.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-size="13" font-weight="700" fill="#7E7386" letter-spacing=".3" stroke="#F6F0E6" stroke-width="4" paint-order="stroke" {f}>{nm}</text>')
    x, y = xy(51.140, -0.186); o.append(f'<text x="{x:.0f}" y="{y:.0f}" font-size="12" font-style="italic" fill="#8B8091" {f}>▲ Gatwick</text>')
    x, y = xy(51.1118, -0.1840); o.append(f'<text x="{x:.0f}" y="{y + 20:.0f}" text-anchor="middle" font-size="12" font-weight="800" fill="#5A4E60" stroke="#F6F0E6" stroke-width="4" paint-order="stroke" {f}>Town centre</text>')
    for i, nm in enumerate(pins, 1):
        x, y = xy(*PLACES[nm])
        o.append(f'<g class="cpin"><path d="M{x:.0f},{y:.0f} c-12,-14 -16,-20 -16,-27 a16,16 0 1 1 32,0 c0,7 -4,13 -16,27z" fill="#FF4FA3" stroke="#fff" stroke-width="2.5"/>'
                 f'<text x="{x:.0f}" y="{y - 22:.0f}" text-anchor="middle" font-size="15" font-weight="800" fill="#fff" {f}>{i}</text></g>')
    o.append(f'<text x="{W - 10}" y="{H - 10}" text-anchor="end" font-size="11" fill="#8B8091" {f}>Approximate positions</text>')
    o.append('</svg>')
    return ''.join(o)

CSS = '''
/* Crawley: places + venues + map in one section (16 Oct) */
.loc-where .cwgrid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:34px;align-items:start;margin-top:22px}
.loc-where .cmap{display:block;width:100%;height:auto;border-radius:18px;border:1px solid rgba(0,0,0,.08);box-shadow:0 18px 40px -28px rgba(40,20,40,.5)}
.loc-where ol.cplaces{list-style:none;counter-reset:p;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.loc-where ol.cplaces li{counter-increment:p;position:relative;padding:12px 14px 12px 54px;background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:14px}
.loc-where ol.cplaces li::before{content:counter(p);position:absolute;left:14px;top:12px;width:28px;height:28px;border-radius:50%;background:#FF4FA3;color:#fff;font-weight:800;display:grid;place-items:center;font-size:14px}
.loc-where ol.cplaces li.nopin::before{content:"★";background:#9C83D1}
.loc-where ol.cplaces b{display:block;color:#1B1712;font-size:17px}
.loc-where ol.cplaces span{display:block;color:#4E463F;font-size:15px}
.loc-where ol.cplaces a{font-weight:700;font-size:14px;color:#B0337A}
.loc-where .vnote{margin-top:16px;color:var(--muted);font-size:14px}
@media(max-width:860px){.loc-where .cwgrid{grid-template-columns:1fr}}
.loc-where .cmapbox{position:relative;border-radius:18px;overflow:hidden;box-shadow:0 18px 40px -28px rgba(40,20,40,.5);aspect-ratio:760/628;background:#F6F0E6}
.loc-where .cmapbox .cmap{border:0;border-radius:0;box-shadow:none;position:absolute;inset:0}
.loc-where .cmapbox #cmaplive{position:absolute;inset:0;opacity:0;transition:opacity .4s}
.loc-where .cmapbox.is-live #cmaplive{opacity:1}
.loc-where .cnum{width:30px;height:30px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#FF4FA3;border:3px solid #fff;box-shadow:0 4px 10px rgba(0,0,0,.35);display:grid;place-items:center}
.loc-where .cnum b{transform:rotate(45deg);color:#fff;font:800 14px/1 Manrope,system-ui,sans-serif}
.loc-where .leaflet-popup-content{font:600 14px/1.45 Manrope,system-ui,sans-serif;margin:10px 14px}
.loc-where .leaflet-popup-content b{display:block;font-size:16px;color:#1B1712}
'''

LIVE_JS = """<script src="../vendor/leaflet/leaflet.js"></script>
<script>
(function(){
  if (!window.L) return;   // the drawn map stays if the live map can't load
  var box = document.getElementById('cmapbox'); if (!box) return;
  var pins = __PINS__;
  var live = document.createElement('div'); live.id = 'cmaplive'; box.appendChild(live);
  var map = L.map('cmaplive', {scrollWheelZoom:false, zoomControl:true});
  var bounds = pins.map(function(p){ return [p.lat, p.lon]; });
  map.fitBounds(bounds, {padding:[50,50]});
  var ok = 0, shown = false;
  function show(){ if (shown) return; shown = true; box.classList.add('is-live'); var sv = box.querySelector('.cmap'); if (sv) sv.style.visibility = 'hidden'; map.invalidateSize(); map.fitBounds(bounds, {padding:[50,50]}); }
  var t = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    {maxZoom: 18, subdomains: 'abcd', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'});
  t.on('tileload', function(){ ok++; if (ok >= 3) show(); });
  t.addTo(map);
  setTimeout(function(){ if (ok === 0) { map.remove(); live.remove(); } }, 8000);   // no map pictures reachable: keep the drawn map
  pins.forEach(function(p, i){
    var icon = L.divIcon({className:'', html:'<div class="cnum"><b>'+(i+1)+'</b></div>', iconSize:[30,30], iconAnchor:[15,34], popupAnchor:[0,-30]});
    L.marker([p.lat, p.lon], {icon:icon, title:p.n, alt:p.n}).addTo(map).bindPopup('<b>'+(i+1)+'. '+p.n+'</b>'+p.t);
  });
})();
</script>"""

def build():
    p = f'{OUT}/{PAGE}'
    if not os.path.exists(p): return
    s = open(p).read()
    if 'loc-where' in s: return
    chips = re.search(r'<section class="band band-light loc-chips[^"]*">.*?</section>', s, re.S)
    hire = re.search(r'<section class="band band-\w+ loc-hire[^"]*">.*?</section>', s, re.S)
    card = re.search(r'<section class="band band-light loc-postcard">.*?</section>', s, re.S)
    if not (chips and hire): print('crawley map: sections not found'); return
    places = re.findall(r'<summary>(.*?)</summary><span>(.*?)</span>', chips.group(0))
    venues = re.findall(r'<li><b>(.*?)</b><i>(.*?)</i>(.*?)</li>', hire.group(0), re.S)
    vnote = re.search(r'<p class="vnote">.*?</p>', hire.group(0), re.S)
    pins = [nm for nm, _ in places if nm in PLACES]
    items = ''
    for nm, txt in places:
        if nm in PLACES: items += f'<li><b>{nm}</b><span>{txt}</span></li>'
    seen = {nm for nm, _ in places}
    for nm, where, rest in venues:
        if nm in seen:   # same thing listed in both: merge the venue link into the place line
            link = re.search(r'<a [^>]*>.*?</a>', rest)
            items = items  # pinned places already listed
        txt = re.sub(r'\s*<a [^>]*>.*?</a>', '', rest).strip()
        link = re.search(r'<a [^>]*>.*?</a>', rest)
        items += f'<li class="nopin"><b>{nm}</b><span>{where}. {txt}</span>{link.group(0) if link else ""}</li>'
    for nm, txt in places:
        if nm not in PLACES and nm not in {v[0] for v in venues}:
            items += f'<li class="nopin"><b>{nm}</b><span>{txt}</span></li>'
    sec = ('<section class="band band-dark loc-where"><div class="wrap"><h2>Where Crawley parties happen</h2>'
           '<p class="lede-s">Parks for summer parties, and halls to hire when it’s cold or wet. The numbers match the map.</p>'
           f'<div class="cwgrid"><div class="cmapbox" id="cmapbox">{town_map(pins)}</div><div><ol class="cplaces">{items}</ol>{vnote.group(0) if vnote else ""}</div></div></div></section>\n')
    # replace: postcard (if any) + chips + hire  ->  one section where the chips were
    s = s.replace(hire.group(0), '', 1)
    if card: s = s.replace(card.group(0), '', 1)
    s = s.replace(chips.group(0), sec, 1)
    s = re.sub(r'\n\s*\n\s*\n', '\n\n', s)
    js = LIVE_JS.replace('__PINS__', json.dumps([dict(n=nm, lat=PLACES[nm][0], lon=PLACES[nm][1], t=dict(places).get(nm, '')) for nm in pins], ensure_ascii=False))
    s = s.replace('</head>', '<link rel="stylesheet" href="../vendor/leaflet/leaflet.css">\n</head>', 1)
    s = s.replace('<script src="site.js"></script>', js + '\n<script src="site.js"></script>', 1)
    open(p, 'w').write(s)
    cp = f'{OUT}/site.css'; c = open(cp).read()
    if '.loc-where' not in c: open(cp, 'a').write(CSS)
    print('crawley: places, venues and map joined up')

if __name__ == '__main__':
    build()
