# -*- coding: utf-8 -*-
"""Winter wonderland background (SVG) for the Christmas page: icy blue dusk, soft snow bokeh, trees wrapped in
warm fairy lights, a frozen path and a pixie skating on it. Inspired by the photo Phil sent on 16 Oct; drawn from scratch."""
import math, random

def lit_tree(x, base, h, lean, rng, scale=1.0):
    """A bare trunk wrapped in a spiral of warm fairy lights, with snowy branches."""
    o = f'<ellipse cx="{x + lean * .5:.0f}" cy="{base - h * .55:.0f}" rx="{220 * scale:.0f}" ry="{h * .5:.0f}" fill="url(#halo)"/>'
    top = base - h
    tw = 26 * scale
    o += (f'<path d="M{x - tw:.0f},{base} C{x - tw * .8:.0f},{base - h * .4:.0f} {x + lean * .5 - tw * .5:.0f},{top + h * .3:.0f} {x + lean - tw * .25:.0f},{top:.0f} '
          f'L{x + lean + tw * .25:.0f},{top:.0f} C{x + lean * .5 + tw * .5:.0f},{top + h * .3:.0f} {x + tw * .8:.0f},{base - h * .4:.0f} {x + tw:.0f},{base}Z" fill="url(#bark)"/>')
    for k, (fy, side, L) in enumerate([(.35, -1, 170), (.5, 1, 150), (.62, -1, 130), (.75, 1, 120), (.85, -1, 90), (.92, 1, 80)]):
        bx = x + lean * fy; by = base - h * fy
        ex = bx + side * L * scale; ey = by - 60 * scale
        o += f'<path d="M{bx:.0f},{by:.0f} Q{(bx + ex) / 2:.0f},{by - 10:.0f} {ex:.0f},{ey:.0f}" stroke="#4A3B44" stroke-width="{8 * scale:.0f}" fill="none" stroke-linecap="round"/>'
        o += f'<path d="M{bx:.0f},{by - 5:.0f} Q{(bx + ex) / 2:.0f},{by - 18:.0f} {ex:.0f},{ey - 6:.0f}" stroke="#F4FAFF" stroke-width="{5 * scale:.0f}" fill="none" stroke-linecap="round" opacity=".9"/>'
        for t in [i / 7 for i in range(1, 8)]:
            lx = bx + (ex - bx) * t; ly = by + (ey - by) * t - 8 * math.sin(t * math.pi)
            o += f'<circle cx="{lx:.0f}" cy="{ly + 6:.0f}" r="{20 * scale:.0f}" fill="url(#warm)"/><circle cx="{lx:.0f}" cy="{ly + 6:.0f}" r="{2.2 * scale:.1f}" fill="#FFF4C9"/>'
    # spiral of lights round the trunk
    n = int(h / 9)
    for i in range(n):
        fy = i / n
        cx = x + lean * fy; w = tw * (1 - fy * .7)
        ang = fy * 26
        lx = cx + math.sin(ang) * w; ly = base - h * fy
        front = math.cos(ang) > -0.2
        if front:
            o += f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="{22 * scale:.0f}" fill="url(#warm)"/><circle cx="{lx:.0f}" cy="{ly:.0f}" r="{2.6 * scale:.1f}" fill="#FFF7D6"/>'
    return o

def pixie(x, y, s):
    """A pixie skating to the right, one arm reaching out, feathery skirt and gauzy wings."""
    o = f'<g transform="translate({x:.0f},{y:.0f}) scale({s:.2f})">'
    o += '<ellipse cx="0" cy="250" rx="120" ry="10" fill="#FFFFFF" opacity=".25"/>'
    # wings
    o += ('<g opacity=".72"><path d="M-6,-10 C-70,-120 -150,-90 -120,-30 C-100,10 -40,0 -6,-4Z" fill="url(#wing)" stroke="#FFFFFF" stroke-width="1.5"/>'
          '<path d="M-6,0 C-90,10 -110,80 -60,80 C-30,80 -14,40 -6,6Z" fill="url(#wing)" stroke="#FFFFFF" stroke-width="1.5"/>'
          '<path d="M-6,-6 C-50,-60 -90,-80 -112,-60 M-6,-2 C-50,-30 -80,-30 -110,-28 M-6,4 C-40,30 -60,50 -66,74" stroke="#FFFFFF" stroke-width="1" fill="none" opacity=".8"/></g>')
    # back leg (extended behind) and skate
    o += '<path d="M-4,120 C-30,160 -60,190 -86,214" stroke="#F3E9F4" stroke-width="13" stroke-linecap="round" fill="none"/>'
    o += '<path d="M-98,206 l26,16 l-6,8 l-28,-14Z" fill="#FFFFFF"/><path d="M-110,224 L-60,236" stroke="#C9D8E8" stroke-width="3" stroke-linecap="round"/>'
    # front leg and skate
    o += '<path d="M8,120 C12,170 14,200 16,232" stroke="#F3E9F4" stroke-width="13" stroke-linecap="round" fill="none"/>'
    o += '<path d="M8,228 l26,0 l2,10 l-30,0Z" fill="#FFFFFF"/><path d="M-6,246 L50,246" stroke="#C9D8E8" stroke-width="3" stroke-linecap="round"/>'
    # feathery skirt
    rng = random.Random(7)
    skirt = ''
    for k in range(26):
        a = .45 + k * (2.25 / 25) + rng.uniform(-.04, .04)
        L = rng.uniform(80, 118)
        ex, ey = math.cos(a) * L * 1.15, 60 + math.sin(a) * L * .85
        skirt += f'<path d="M0,60 Q{ex * .5:.0f},{60 + (ey - 60) * .3:.0f} {ex:.0f},{ey:.0f}" stroke="#FFFFFF" stroke-width="{rng.uniform(3, 7):.1f}" stroke-linecap="round" fill="none" opacity="{rng.uniform(.6, .95):.2f}"/>'
    o += '<path d="M-20,60 C-60,90 -80,120 -86,140 C-40,128 40,128 86,140 C70,110 50,86 20,60Z" fill="#F7F1FA"/>' + skirt
    # body
    o += '<path d="M-16,-8 C-20,20 -18,44 -20,64 L20,64 C18,40 20,18 14,-8 C6,-16 -8,-16 -16,-8Z" fill="#FBF6FD"/>'
    # arms: front arm reaching forward, back arm behind
    o += '<path d="M10,-2 C40,0 70,10 104,30" stroke="#F3E9F4" stroke-width="9" stroke-linecap="round" fill="none"/>'
    o += '<path d="M-12,0 C-30,20 -44,36 -52,58" stroke="#F3E9F4" stroke-width="8" stroke-linecap="round" fill="none"/>'
    # head, hair, hat
    o += '<path d="M-4,-14 L-2,-24" stroke="#F3E9F4" stroke-width="9" stroke-linecap="round"/>'
    o += '<circle cx="2" cy="-40" r="17" fill="#F6DCCB"/>'
    o += '<path d="M-14,-44 C-30,-40 -34,-20 -26,-6 C-20,-18 -14,-28 -10,-36Z" fill="#C98A5A"/>'
    o += '<path d="M-16,-46 C-14,-66 18,-70 22,-46 Z" fill="#E8F1F8"/><rect x="-18" y="-50" width="42" height="8" rx="4" fill="#FFFFFF"/>'
    o += '<circle cx="-12" cy="-66" r="7" fill="#FFFFFF"/>'
    # sparkle at the fingertips
    o += '<circle cx="110" cy="32" r="26" fill="url(#warm)"/><path d="M110,20 L113,30 L122,32 L113,35 L110,44 L107,35 L98,32 L107,30Z" fill="#FFF4C9"/>'
    return o + '</g>'

def wonderland(w=1600, h=1000, portrait=False):
    rng = random.Random(11)
    body = '<rect width="100%" height="100%" fill="url(#sky)"/>'
    body += f'<ellipse cx="{w * .5:.0f}" cy="{h * .62:.0f}" rx="{w * .5:.0f}" ry="{h * .35:.0f}" fill="url(#centreglow)"/>'
    # distant lit trees: soft glowing columns
    for i in range(14 if not portrait else 8):
        x = rng.uniform(w * .15, w * .85); top = rng.uniform(h * .25, h * .45)
        body += f'<rect x="{x - 9:.0f}" y="{top:.0f}" width="18" height="{h * .72 - top:.0f}" rx="9" fill="#FFE2A8" opacity="{rng.uniform(.25, .5):.2f}" filter="url(#soft)"/>'
    # snowy ground and the frozen path
    gy = h * .72
    body += f'<path d="M0,{gy:.0f} Q{w * .3:.0f},{gy - 30:.0f} {w * .5:.0f},{gy - 10:.0f} T{w},{gy - 20:.0f} L{w},{h} L0,{h}Z" fill="url(#snow)"/>'
    body += (f'<path d="M{w * .34:.0f},{h} C{w * .44:.0f},{h * .9:.0f} {w * .4:.0f},{h * .8:.0f} {w * .47:.0f},{gy:.0f} L{w * .53:.0f},{gy:.0f} '
             f'C{w * .62:.0f},{h * .8:.0f} {w * .58:.0f},{h * .9:.0f} {w * .7:.0f},{h}Z" fill="url(#ice)"/>')
    body += f'<ellipse cx="{w * .5:.0f}" cy="{h * .86:.0f}" rx="{w * .12:.0f}" ry="{h * .1:.0f}" fill="url(#warmice)"/>'
    for k in range(int(40 * w / 1600)):
        x = rng.uniform(0, w); y = rng.uniform(gy, h)
        body += f'<path d="M{x:.0f},{y - 4:.0f} L{x + 1:.0f},{y:.0f} L{x:.0f},{y + 4:.0f} L{x - 1:.0f},{y:.0f}Z M{x - 4:.0f},{y:.0f} L{x:.0f},{y - 1:.0f} L{x + 4:.0f},{y:.0f} L{x:.0f},{y + 1:.0f}Z" fill="#FFFFFF" opacity=".9"/>'
    for i in range(10):
        x = rng.uniform(w * .38, w * .62)
        body += f'<rect x="{x:.0f}" y="{h * .76:.0f}" width="5" height="{h * .2:.0f}" fill="#FFE2A8" opacity=".35" filter="url(#soft)"/>'
    # foreground lit trees at both edges
    if not portrait:
        body += lit_tree(w * .06, h * 1.02, h * 1.1, 60, rng, 1.1) + lit_tree(w * .2, h * .86, h * .7, 20, rng, .7)
        body += lit_tree(w * .94, h * 1.02, h * 1.1, -70, rng, 1.1) + lit_tree(w * .8, h * .86, h * .66, -20, rng, .7)
    else:
        body += lit_tree(w * .08, h * 1.02, h * .95, 50, rng, 1.0) + lit_tree(w * .92, h * 1.02, h * .95, -50, rng, 1.0)
    # snow banks over the tree roots
    body += f'<path d="M0,{h} L0,{h * .9:.0f} Q{w * .12:.0f},{h * .84:.0f} {w * .28:.0f},{h * .93:.0f} L{w * .3:.0f},{h}Z" fill="#F2F8FF"/>'
    body += f'<path d="M{w},{h} L{w},{h * .9:.0f} Q{w * .88:.0f},{h * .84:.0f} {w * .72:.0f},{h * .93:.0f} L{w * .7:.0f},{h}Z" fill="#F2F8FF"/>'
    # the pixie skater
    px, py, ps = (w * .5, h * .55, .82) if not portrait else (w * .5, h * .62, .9)
    body += pixie(px, py, ps)
    # bokeh snow: big soft discs and crisp flakes
    for _ in range(int(55 * w / 1600) + 15):
        r = rng.uniform(8, 34)
        c = rng.choice(['#FFFFFF', '#FFFFFF', '#FFE2A8', '#CDEBFF'])
        body += f'<circle cx="{rng.uniform(0, w):.0f}" cy="{rng.uniform(0, h):.0f}" r="{r:.0f}" fill="{c}" opacity="{rng.uniform(.14, .42):.2f}" filter="url(#bokeh)"/>'
    for _ in range(int(380 * w / 1600) + 80):
        body += f'<circle cx="{rng.uniform(0, w):.0f}" cy="{rng.uniform(0, h):.0f}" r="{rng.uniform(1, 3.6):.1f}" fill="#FFFFFF" opacity="{rng.uniform(.45, .95):.2f}"/>'
    defs = (
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B2A55"/><stop offset=".45" stop-color="#1F5C95"/><stop offset=".72" stop-color="#6FB0DA"/><stop offset="1" stop-color="#BFE3F6"/></linearGradient>'
        '<radialGradient id="centreglow"><stop offset="0" stop-color="#FFE9B8" stop-opacity=".55"/><stop offset=".5" stop-color="#FFE9B8" stop-opacity=".15"/><stop offset="1" stop-color="#FFE9B8" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="warm"><stop offset="0" stop-color="#FFD98A" stop-opacity=".95"/><stop offset=".4" stop-color="#FFB84A" stop-opacity=".35"/><stop offset="1" stop-color="#FFB84A" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="halo"><stop offset="0" stop-color="#FFC970" stop-opacity=".28"/><stop offset="1" stop-color="#FFC970" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="warmice"><stop offset="0" stop-color="#FFE2A8" stop-opacity=".45"/><stop offset="1" stop-color="#FFE2A8" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="bark" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2E2836"/><stop offset=".5" stop-color="#5A4A52"/><stop offset="1" stop-color="#2E2836"/></linearGradient>'
        '<linearGradient id="snow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D2E9FA"/><stop offset=".5" stop-color="#B4D6F0"/><stop offset="1" stop-color="#8DBCE2"/></linearGradient>'
        '<linearGradient id="ice" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9F6FF"/><stop offset=".5" stop-color="#9CCBEA"/><stop offset="1" stop-color="#6FA9D6"/></linearGradient>'
        '<linearGradient id="wing" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".85"/><stop offset=".5" stop-color="#E6D9FF" stop-opacity=".5"/><stop offset="1" stop-color="#BFE9FF" stop-opacity=".35"/></linearGradient>'
        f'<filter id="soft" filterUnits="userSpaceOnUse" x="-200" y="-200" width="{w + 400}" height="{h + 400}"><feGaussianBlur stdDeviation="12"/></filter>'
        f'<filter id="bokeh" filterUnits="userSpaceOnUse" x="-200" y="-200" width="{w + 400}" height="{h + 400}"><feGaussianBlur stdDeviation="3"/></filter>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs>{body}</svg>'

if __name__ == '__main__':
    d = '/home/claude/paintingpixie-v2/img/bg/'
    open(d + 'winter-wonderland.svg', 'w').write(wonderland())
    open(d + 'winter-wonderland-tall.svg', 'w').write(wonderland(900, 1600, True))
    print('ok')
