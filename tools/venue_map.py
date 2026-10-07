# -*- coding: utf-8 -*-
"""Simple drawn map of Horsham with numbered party spots, plus booking links for each spot.
Used by build_locations.py on the Horsham page in place of the postcard."""
import html
from urllib.parse import quote

S_LAT, S_LON = 7000, 4403          # pixels per degree (lon scaled by cos 51°)
C_LAT, C_LON = 51.052, -0.335      # centre of the map
def xy(lat, lon): return round(600 + (lon - C_LON) * S_LON), round(260 - (lat - C_LAT) * S_LAT)

# number: (true lat, lon, pin offset dx, dy)
PINS = {1: (51.0668, -0.3254, 34, -28), 2: (51.0570, -0.3400, -20, 22), 3: (51.0715, -0.3640, 0, 0),
        4: (51.0245, -0.3460, 0, 0), 5: (51.0550, -0.3240, 40, 26), 6: (51.0637, -0.3268, -42, -6)}

# Booking links for each spot (only real venues that take bookings, or the official info page)
LINKS = {
    'Horsham Park': [('Hire Horsham Park Barn', 'https://www.horsham.gov.uk/community/rooms-for-hire/horsham-park-barn'),
                     ('Pavilions party packages', 'https://www.placesleisure.org/centres/the-pavilions-in-the-park/centre-activities/family-kids/')],
    'Broadbridge Heath': [('The Bridge party packages', 'https://www.placesleisure.org/centres/the-bridge-leisure-centre/centre-activities/family-kids/')],
    'Southwater Country Park': [('Park info', 'https://horsham.gov.uk/parks-and-countryside/southwater-country-park')],
    'Chesworth Farm': [('Farm info', 'https://www.horsham.gov.uk/parks-and-countryside/chesworth-farm')],
}

def path(points, close=False):
    pts = [xy(a, b) for a, b in points]
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    return d + (' Z' if close else '')

def smooth(points):
    pts = [xy(a, b) for a, b in points]
    d = f'M{pts[0][0]} {pts[0][1]}'
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        d += f' Q{x0} {y0} {(x0 + x1) // 2} {(y0 + y1) // 2}'
    return d + f' T{pts[-1][0]} {pts[-1][1]}'

def horsham_svg():
    town = smooth([(51.083, -0.345), (51.086, -0.320), (51.082, -0.295), (51.073, -0.283), (51.060, -0.287),
                   (51.051, -0.305), (51.049, -0.330), (51.053, -0.350), (51.066, -0.352), (51.078, -0.350), (51.083, -0.345)])
    bbh = smooth([(51.078, -0.372), (51.078, -0.357), (51.069, -0.355), (51.066, -0.368), (51.072, -0.378), (51.078, -0.372)])
    sw = smooth([(51.031, -0.362), (51.031, -0.345), (51.020, -0.343), (51.013, -0.352), (51.018, -0.366), (51.031, -0.362)])
    river = smooth([(51.062, -0.270), (51.058, -0.300), (51.056, -0.318), (51.055, -0.332), (51.061, -0.350),
                    (51.068, -0.372), (51.063, -0.400), (51.055, -0.430), (51.040, -0.465)])
    a24 = smooth([(51.095, -0.352), (51.080, -0.353), (51.068, -0.352), (51.058, -0.345), (51.045, -0.338), (51.030, -0.335), (51.010, -0.331)])
    a264e = smooth([(51.072, -0.290), (51.080, -0.260), (51.090, -0.230), (51.095, -0.200)])
    a281 = smooth([(51.074, -0.372), (51.082, -0.395), (51.092, -0.425), (51.100, -0.450)])
    a264w = smooth([(51.070, -0.372), (51.058, -0.400), (51.042, -0.430), (51.025, -0.460)])
    pins = ''
    for n, (la, lo, dx, dy) in PINS.items():
        x, y = xy(la, lo); px, py = x + dx, y + dy
        lead = f'<line x1="{x}" y1="{y}" x2="{px}" y2="{py}" stroke="#14101C" stroke-width="2"/><circle cx="{x}" cy="{y}" r="4" fill="#14101C"/>' if (dx or dy) else ''
        pins += (f'<g class="vpin">{lead}<circle cx="{px}" cy="{py}" r="19" fill="#FF4FA3" stroke="#fff" stroke-width="3"/>'
                 f'<text x="{px}" y="{py + 6}" text-anchor="middle" font-size="18" font-weight="800" fill="#14101C" font-family="Manrope,system-ui,sans-serif">{n}</text></g>')
    lab = lambda x, y, t, size=15, w=700, fill='#4E463F', anchor='middle', ls='0': (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{w}" fill="{fill}" letter-spacing="{ls}" font-family="Manrope,system-ui,sans-serif">{t}</text>')
    tx, ty = xy(51.079, -0.312); bx, by = xy(51.0795, -0.366); sx, sy = xy(51.0225, -0.3655)
    return f'''<svg class="postcard vmapsvg" viewBox="0 0 1200 560" preserveAspectRatio="xMidYMid slice" role="img" aria-label="Simple map of Horsham showing Kat's six favourite party spots, numbered to match the list below">
<rect width="1200" height="560" fill="#E4EFD6"/>
<path d="{town}" fill="#F7EFE3" stroke="#D9C9B3" stroke-width="2"/>
<path d="{bbh}" fill="#F7EFE3" stroke="#D9C9B3" stroke-width="2"/>
<path d="{sw}" fill="#F7EFE3" stroke="#D9C9B3" stroke-width="2"/>
<path d="{river}" fill="none" stroke-linecap="round" stroke="#8FC3E0" stroke-width="7"/>
<g fill="none" stroke-linecap="round" stroke="#FFFFFF" stroke-width="9"><path d="{a24}"/><path d="{a264e}"/><path d="{a281}"/><path d="{a264w}"/></g>
<g fill="none" stroke-linecap="round" stroke="#E2BE7A" stroke-width="4"><path d="{a24}"/><path d="{a264e}"/><path d="{a281}"/><path d="{a264w}"/></g>
{lab(tx, ty, 'HORSHAM', 26, 800, '#2B2420', ls='4')}
{lab(bx, by, 'Broadbridge Heath', 14)}
{lab(sx, sy, 'Southwater', 14, anchor='end')}
{lab(1185, 40, 'Crawley →', 14, 700, '#6B5F57', 'end')}
{lab(70, 40, '← Guildford', 14, 700, '#6B5F57', 'start')}
{lab(60, 470, '← Billingshurst', 14, 700, '#6B5F57', 'start')}
{lab(560, 22, '↑ Dorking', 14, 700, '#6B5F57')}
{lab(640, 548, '↓ Worthing', 14, 700, '#6B5F57')}
{lab(990, 230, 'River Arun', 13, 600, '#4F8DB3')}
{pins}
<g transform="translate(1040 480)"><rect x="-8" y="-24" width="160" height="58" rx="10" fill="#fff" opacity=".85"/>
<circle cx="12" cy="-4" r="9" fill="#FF4FA3"/><text x="28" y="1" font-size="13" font-weight="700" fill="#2B2420" font-family="Manrope,sans-serif">Party spot</text>
<line x1="2" y1="20" x2="22" y2="20" stroke="#E2BE7A" stroke-width="4"/><text x="28" y="25" font-size="13" font-weight="700" fill="#2B2420" font-family="Manrope,sans-serif">Main road</text></g>
</svg>'''

def wa(text):
    return 'https://wa.me/447852300125?text=' + quote(text)

def venue_list(venues):
    items = ''
    for name, text in venues:
        key = next((k for k in LINKS if name.startswith(k)), None)
        links = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(l)} ↗</a>' for l, u in (LINKS.get(key) or []))
        book = f'<a class="vbook" href="{wa(f"Hi Kat! I’m planning a party at {name} in Horsham. Date: Guests: ")}" target="_blank" rel="noopener">Book Kat here</a>'
        items += f'<li><b>{html.escape(name)}</b><span>{html.escape(text)}</span><span class="vlinks">{book}{links}</span></li>'
    return items

CSS = '''
.vmapsvg{margin-bottom:8px;aspect-ratio:1200/560}
@media(max-width:600px){.vmapsvg{aspect-ratio:auto;height:360px}}
.vmap li::before{grid-row:span 3}
.vlinks{display:flex;flex-wrap:wrap;gap:8px 14px;margin-top:6px;font-size:14px!important}
.vlinks a{font-weight:700;color:var(--gold)}
.vlinks a.vbook{background:#25D366;color:#0B1F12;text-decoration:none;border-radius:999px;padding:4px 12px}
.vmapnote{color:var(--muted);font-size:14px;margin-top:14px}
'''
