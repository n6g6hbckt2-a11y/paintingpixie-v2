# -*- coding: utf-8 -*-
"""Christmas night background (SVG) for the Christmas page only: winter sky, stars, snowflakes, falling snow,
a string of fairy lights across the top and snowy fir trees along the bottom. Landscape + phone (tall) versions."""
import math, random

def flake(x, y, r, op, rot):
    arms = ''
    for k in range(6):
        a = rot + k * math.pi / 3
        ex, ey = x + math.cos(a) * r, y + math.sin(a) * r
        arms += f'M{x:.1f},{y:.1f}L{ex:.1f},{ey:.1f}'
        for f in (.55, .8):
            bx, by = x + math.cos(a) * r * f, y + math.sin(a) * r * f
            for s in (-1, 1):
                b = a + s * .7
                arms += f'M{bx:.1f},{by:.1f}L{bx + math.cos(b) * r * .28:.1f},{by + math.sin(b) * r * .28:.1f}'
    return f'<path d="{arms}" stroke="#EAF4FF" stroke-width="{max(1.2, r * .09):.1f}" stroke-linecap="round" fill="none" opacity="{op:.2f}"/>'

def tree(x, base, h, snow=True):
    w = h * .42
    o = f'<rect x="{x - h * .03:.0f}" y="{base - h * .1:.0f}" width="{h * .06:.0f}" height="{h * .1:.0f}" fill="#06120F"/>'
    tiers = 4
    for t in range(tiers):
        top = base - h + t * h * .2
        bot = top + h * .38
        ww = w * (.45 + t * .2)
        o += f'<path d="M{x:.0f},{top:.0f} L{x + ww:.0f},{bot:.0f} L{x - ww:.0f},{bot:.0f}Z" fill="#0A231C"/>'
        if snow:
            o += (f'<path d="M{x - ww * .3:.0f},{top + h * .11:.0f} L{x:.0f},{top:.0f} L{x + ww * .3:.0f},{top + h * .11:.0f} '
                  f'q-{ww * .15:.0f},-{h * .03:.0f} -{ww * .3:.0f},{h * .01:.0f} q-{ww * .15:.0f},-{h * .04:.0f} -{ww * .3:.0f},-{h * .01:.0f}Z" fill="#EAF4FF" opacity=".9"/>'
                  f'<path d="M{x - ww * .95:.0f},{bot - 2:.0f} q{ww * .3:.0f},-{h * .035:.0f} {ww * .6:.0f},0 q{ww * .35:.0f},-{h * .03:.0f} {ww * .7:.0f},0 q{ww * .3:.0f},-{h * .035:.0f} {ww * .6:.0f},0" stroke="#EAF4FF" stroke-width="{max(2, h * .018):.0f}" stroke-linecap="round" fill="none" opacity=".8"/>')
    return o


def xtree(x, base, h):
    """Decorated Christmas tree: green tiers, baubles, tinsel and a gold star."""
    w = h * .4
    o = f'<circle cx="{x:.0f}" cy="{base - h * .5:.0f}" r="{h * .55:.0f}" fill="url(#tglow)"/>'
    o += f'<rect x="{x - h * .04:.0f}" y="{base - h * .1:.0f}" width="{h * .08:.0f}" height="{h * .1:.0f}" fill="#5A3418"/>'
    for t in range(4):
        top = base - h * .92 + t * h * .19; bot = top + h * .34; ww = w * (.42 + t * .2)
        o += f'<path d="M{x:.0f},{top:.0f} L{x + ww:.0f},{bot:.0f} Q{x:.0f},{bot + h * .04:.0f} {x - ww:.0f},{bot:.0f}Z" fill="{["#1F7A45", "#1B6E3E", "#176237", "#135630"][t]}"/>'
        o += f'<path d="M{x - ww * .8:.0f},{bot - h * .04:.0f} Q{x:.0f},{bot + h * .02:.0f} {x + ww * .8:.0f},{bot - h * .08:.0f}" stroke="#FFD24F" stroke-width="{h * .012:.1f}" fill="none" opacity=".85" stroke-dasharray="{h * .02:.0f} {h * .012:.0f}"/>'
    rng = random.Random(int(x))
    cols = ['#E3243B', '#FFC93C', '#4FB6FF', '#FF7AD9', '#F2F2F2']
    for k in range(16):
        fy = rng.uniform(.2, .95); yy = base - h * .92 + fy * h * .9; half = w * (.25 + fy * .95) * .8
        xx = x + rng.uniform(-half, half); r = h * rng.uniform(.022, .032)
        o += f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{r:.1f}" fill="{cols[k % 5]}"/><circle cx="{xx - r * .35:.1f}" cy="{yy - r * .35:.1f}" r="{r * .3:.1f}" fill="#fff" opacity=".7"/>'
    sy = base - h * .95; r = h * .07
    pts = ' '.join(f'{x + math.cos(-math.pi / 2 + i * math.pi / 5) * (r if i % 2 == 0 else r * .45):.1f},{sy + math.sin(-math.pi / 2 + i * math.pi / 5) * (r if i % 2 == 0 else r * .45):.1f}' for i in range(10))
    o += f'<circle cx="{x:.0f}" cy="{sy:.0f}" r="{r * 2.2:.0f}" fill="url(#sglow)"/><polygon points="{pts}" fill="#FFD24F"/>'
    return o

def present(x, base, w, h, col, rib):
    return (f'<rect x="{x:.0f}" y="{base - h:.0f}" width="{w:.0f}" height="{h:.0f}" rx="3" fill="{col}"/>'
            f'<rect x="{x + w * .42:.0f}" y="{base - h:.0f}" width="{w * .16:.0f}" height="{h:.0f}" fill="{rib}"/>'
            f'<rect x="{x:.0f}" y="{base - h * .62:.0f}" width="{w:.0f}" height="{h * .14:.0f}" fill="{rib}"/>'
            f'<ellipse cx="{x + w * .38:.0f}" cy="{base - h - 6:.0f}" rx="{w * .16:.0f}" ry="7" fill="{rib}" transform="rotate(-20 {x + w * .38:.0f} {base - h - 6:.0f})"/>'
            f'<ellipse cx="{x + w * .62:.0f}" cy="{base - h - 6:.0f}" rx="{w * .16:.0f}" ry="7" fill="{rib}" transform="rotate(20 {x + w * .62:.0f} {base - h - 6:.0f})"/>')

def snowman(x, base, s):
    o = f'<ellipse cx="{x:.0f}" cy="{base:.0f}" rx="{s * 1.1:.0f}" ry="{s * .18:.0f}" fill="#A9C4E2" opacity=".6"/>'
    o += f'<circle cx="{x:.0f}" cy="{base - s * .75:.0f}" r="{s * .8:.0f}" fill="#F4F9FF"/><circle cx="{x:.0f}" cy="{base - s * 1.85:.0f}" r="{s * .55:.0f}" fill="#F4F9FF"/><circle cx="{x:.0f}" cy="{base - s * 2.65:.0f}" r="{s * .4:.0f}" fill="#F4F9FF"/>'
    hy = base - s * 2.65
    o += f'<rect x="{x - s * .32:.0f}" y="{hy - s * .78:.0f}" width="{s * .64:.0f}" height="{s * .5:.0f}" fill="#1B1B22"/><rect x="{x - s * .48:.0f}" y="{hy - s * .32:.0f}" width="{s * .96:.0f}" height="{s * .1:.0f}" fill="#1B1B22"/>'
    o += f'<rect x="{x - s * .32:.0f}" y="{hy - s * .42:.0f}" width="{s * .64:.0f}" height="{s * .08:.0f}" fill="#E3243B"/>'
    o += f'<circle cx="{x - s * .14:.0f}" cy="{hy - s * .06:.0f}" r="{s * .05:.1f}" fill="#1B1B22"/><circle cx="{x + s * .14:.0f}" cy="{hy - s * .06:.0f}" r="{s * .05:.1f}" fill="#1B1B22"/>'
    o += f'<path d="M{x:.0f},{hy + s * .04:.0f} l{s * .42:.0f},{s * .08:.0f} l-{s * .42:.0f},{s * .08:.0f}Z" fill="#FF8A1F"/>'
    o += f'<path d="M{x - s * .45:.0f},{hy + s * .32:.0f} Q{x:.0f},{hy + s * .5:.0f} {x + s * .45:.0f},{hy + s * .32:.0f} l{s * .05:.0f},{s * .14:.0f} Q{x:.0f},{hy + s * .66:.0f} {x - s * .5:.0f},{hy + s * .46:.0f}Z" fill="#E3243B"/>'
    o += f'<path d="M{x + s * .25:.0f},{hy + s * .45:.0f} l{s * .1:.0f},{s * .55:.0f} l{s * .18:.0f},-{s * .05:.0f} l-{s * .1:.0f},-{s * .5:.0f}Z" fill="#C81D33"/>'
    for k in range(3):
        o += f'<circle cx="{x:.0f}" cy="{base - s * 1.6 - k * s * .2 + s * .1:.0f}" r="{s * .06:.1f}" fill="#1B1B22"/>'
    o += f'<path d="M{x - s * .5:.0f},{base - s * 1.9:.0f} l-{s * .7:.0f},-{s * .45:.0f} m{s * .25:.0f},{s * .16:.0f} l-{s * .1:.0f},-{s * .25:.0f}" stroke="#5A3418" stroke-width="{s * .07:.1f}" stroke-linecap="round" fill="none"/>'
    o += f'<path d="M{x + s * .5:.0f},{base - s * 1.9:.0f} l{s * .7:.0f},-{s * .4:.0f} m-{s * .25:.0f},{s * .14:.0f} l{s * .05:.0f},-{s * .26:.0f}" stroke="#5A3418" stroke-width="{s * .07:.1f}" stroke-linecap="round" fill="none"/>'
    return o

def sleigh(x, y, s):
    """Santa's sleigh and reindeer in silhouette, flying across the moon."""
    c = '#0A1428'
    o = ''
    for k in range(3):
        rx = x - s * (1.4 + k * 1.05); ry = y - s * (.22 + k * .2)
        o += (f'<path d="M{rx - s * .5:.0f},{ry:.0f} q{s * .1:.0f},-{s * .28:.0f} {s * .55:.0f},-{s * .26:.0f} l{s * .14:.0f},-{s * .22:.0f} l{s * .12:.0f},{s * .04:.0f} '
              f'l-{s * .05:.0f},{s * .24:.0f} q-{s * .05:.0f},{s * .2:.0f} -{s * .3:.0f},{s * .24:.0f} l{s * .1:.0f},{s * .24:.0f} l-{s * .08:.0f},0 l-{s * .14:.0f},-{s * .2:.0f} '
              f'l-{s * .18:.0f},0 l-{s * .16:.0f},{s * .22:.0f} l-{s * .08:.0f},0 l{s * .06:.0f},-{s * .26:.0f}Z" fill="{c}"/>'
              f'<path d="M{rx + s * .14:.0f},{ry - s * .46:.0f} l-{s * .05:.0f},-{s * .2:.0f} m{s * .03:.0f},{s * .1:.0f} l-{s * .12:.0f},-{s * .06:.0f} M{rx + s * .22:.0f},{ry - s * .46:.0f} l{s * .06:.0f},-{s * .2:.0f} m-{s * .03:.0f},{s * .1:.0f} l{s * .12:.0f},-{s * .05:.0f}" stroke="{c}" stroke-width="{s * .04:.1f}" fill="none" stroke-linecap="round"/>')
    o += f'<path d="M{x - s * 1.4:.0f},{y - s * .3:.0f} L{x - s * .35:.0f},{y + s * .05:.0f}" stroke="{c}" stroke-width="{s * .025:.1f}"/>'
    o += (f'<path d="M{x - s * .45:.0f},{y + s * .25:.0f} q{s * .1:.0f},-{s * .5:.0f} {s * .45:.0f},-{s * .45:.0f} l{s * .55:.0f},0 q{s * .15:.0f},-{s * .2:.0f} {s * .1:.0f},-{s * .4:.0f} '
          f'l{s * .15:.0f},0 l0,{s * .7:.0f} q0,{s * .15:.0f} -{s * .2:.0f},{s * .15:.0f}Z" fill="{c}"/>'
          f'<circle cx="{x + s * .1:.0f}" cy="{y - s * .32:.0f}" r="{s * .16:.0f}" fill="{c}"/><path d="M{x - s * .08:.0f},{y - s * .4:.0f} l{s * .18:.0f},-{s * .3:.0f} l{s * .16:.0f},{s * .28:.0f}Z" fill="{c}"/>'
          f'<path d="M{x - s * .25:.0f},{y + s * .1:.0f} l{s * .45:.0f},-{s * .38:.0f} l{s * .35:.0f},{s * .1:.0f} l-{s * .1:.0f},{s * .4:.0f}Z" fill="{c}"/>'
          f'<path d="M{x - s * .6:.0f},{y + s * .38:.0f} L{x + s * .75:.0f},{y + s * .38:.0f} q{s * .15:.0f},0 {s * .15:.0f},-{s * .15:.0f}" stroke="{c}" stroke-width="{s * .05:.1f}" fill="none" stroke-linecap="round"/>')
    return o

def holly(x, y, s, rot):
    leaf = (f'<path d="M0,0 q{s * .3:.0f},-{s * .3:.0f} {s * .5:.0f},-{s * .15:.0f} q-{s * .05:.0f},-{s * .2:.0f} {s * .2:.0f},-{s * .2:.0f} q0,{s * .2:.0f} {s * .3:.0f},{s * .15:.0f} '
            f'q-{s * .15:.0f},{s * .2:.0f} {s * .1:.0f},{s * .35:.0f} q-{s * .25:.0f},0 -{s * .3:.0f},{s * .12:.0f} q-{s * .1:.0f},-{s * .2:.0f} -{s * .3:.0f},-{s * .1:.0f} q-{s * .1:.0f},-{s * .2:.0f} -{s * .5:.0f},-{s * .17:.0f}Z" fill="#1F7A45" stroke="#145A32" stroke-width="2"/>')
    o = f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot})">'
    for a in (-35, 25, 95):
        o += f'<g transform="rotate({a})">{leaf}</g>'
    for dx, dy in ((0, 0), (s * .16, s * .1), (-s * .06, s * .17)):
        o += f'<circle cx="{dx:.0f}" cy="{dy:.0f}" r="{s * .1:.0f}" fill="#D7192F"/><circle cx="{dx - s * .03:.0f}" cy="{dy - s * .03:.0f}" r="{s * .03:.0f}" fill="#fff" opacity=".6"/>'
    return o + '</g>'

def bauble(x, y, r, col, drop):
    return (f'<line x1="{x}" y1="0" x2="{x}" y2="{y - r:.0f}" stroke="#E2BE7A" stroke-width="1.5" opacity=".8"/>'
            f'<rect x="{x - r * .3:.0f}" y="{y - r * 1.15:.0f}" width="{r * .6:.0f}" height="{r * .3:.0f}" fill="#E2BE7A"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/><path d="M{x - r * .9:.0f},{y:.0f} Q{x:.0f},{y + r * .35:.0f} {x + r * .9:.0f},{y:.0f}" stroke="#FFE7A3" stroke-width="{r * .1:.1f}" fill="none" opacity=".8"/>'
            f'<circle cx="{x - r * .35:.0f}" cy="{y - r * .35:.0f}" r="{r * .22:.1f}" fill="#fff" opacity=".55"/>')

def christmas(w=1600, h=1000, portrait=False):
    rng = random.Random(25)
    body = '<rect width="100%" height="100%" fill="url(#sky)"/>'
    body += f'<ellipse cx="{w * .5:.0f}" cy="{h * .35:.0f}" rx="{w * .55:.0f}" ry="{h * .35:.0f}" fill="url(#aur)"/>'
    mx, my, mr = (w * .8, h * .3, 95) if not portrait else (w * .7, h * .2, 85)
    body += f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="{mr * 2:.0f}" fill="url(#moonglow)"/><circle cx="{mx:.0f}" cy="{my:.0f}" r="{mr}" fill="#FFF1C9"/>'
    body += f'<circle cx="{mx - mr * .3:.0f}" cy="{my - mr * .2:.0f}" r="{mr * .15:.0f}" fill="#F2DFA8" opacity=".6"/><circle cx="{mx + mr * .35:.0f}" cy="{my + mr * .3:.0f}" r="{mr * .1:.0f}" fill="#F2DFA8" opacity=".55"/>'
    body += sleigh(mx + mr * .45, my + mr * .15, mr * .55)
    for _ in range(int(160 * w / 1600) + 40):
        body += f'<circle cx="{rng.uniform(0, w):.0f}" cy="{rng.uniform(0, h * .8):.0f}" r="{rng.uniform(.6, 1.8):.1f}" fill="#FFF6D6" opacity="{rng.uniform(.3, .9):.2f}"/>'
    # a few bright gold stars
    for _ in range(7):
        x, y, r = rng.uniform(w * .05, w * .95), rng.uniform(h * .12, h * .55), rng.uniform(5, 9)
        body += (f'<g opacity=".9"><circle cx="{x:.0f}" cy="{y:.0f}" r="{r * 2.6:.0f}" fill="url(#sglow)"/>'
                 f'<path d="M{x:.0f},{y - r * 1.8:.0f} Q{x + r * .25:.0f},{y - r * .25:.0f} {x + r * 1.8:.0f},{y:.0f} Q{x + r * .25:.0f},{y + r * .25:.0f} {x:.0f},{y + r * 1.8:.0f} '
                 f'Q{x - r * .25:.0f},{y + r * .25:.0f} {x - r * 1.8:.0f},{y:.0f} Q{x - r * .25:.0f},{y - r * .25:.0f} {x:.0f},{y - r * 1.8:.0f}Z" fill="#FFE7A3"/></g>')
    # snowflakes
    n = 16 if not portrait else 11
    for _ in range(n):
        body += flake(rng.uniform(0, w), rng.uniform(h * .08, h * .82), rng.uniform(9, 26), rng.uniform(.18, .45), rng.uniform(0, 1))
    # falling snow
    for _ in range(int(260 * w / 1600) + 60):
        body += f'<circle cx="{rng.uniform(0, w):.0f}" cy="{rng.uniform(0, h):.0f}" r="{rng.uniform(1, 3.4):.1f}" fill="#FFFFFF" opacity="{rng.uniform(.25, .75):.2f}"/>'
    # fairy lights: two drooping strings across the top
    cols = ['#FF3B4E', '#FFC93C', '#2FE08A', '#4FB6FF', '#FF7AD9']
    for (x0, x1, y0, sag) in ([(-20, w * .52, 18, 70), (w * .48, w + 20, 18, 80)] if not portrait else [(-20, w + 20, 18, 90)]):
        d = f'M{x0:.0f},{y0} Q{(x0 + x1) / 2:.0f},{y0 + sag * 2:.0f} {x1:.0f},{y0}'
        body += f'<path d="{d}" stroke="#0B1410" stroke-width="2.4" fill="none" opacity=".9"/>'
        steps = 13
        for k in range(1, steps):
            t = k / steps
            bx = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * (x0 + x1) / 2 + t * t * x1
            by = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * (y0 + sag * 2) + t * t * y0
            c = cols[(k + int(x0)) % len(cols)]
            body += (f'<circle cx="{bx:.0f}" cy="{by + 10:.0f}" r="20" fill="{c}" opacity=".22"/>'
                     f'<rect x="{bx - 3:.0f}" y="{by - 1:.0f}" width="6" height="5" fill="#2B2B2B"/>'
                     f'<ellipse cx="{bx:.0f}" cy="{by + 10:.0f}" rx="5.5" ry="8" fill="{c}"/>'
                     f'<ellipse cx="{bx - 1.5:.0f}" cy="{by + 7:.0f}" rx="1.6" ry="2.6" fill="#FFFFFF" opacity=".7"/>')
    # snowy ground and fir trees
    gy = h - (110 if not portrait else 140)
    body += f'<path d="M0,{h} L0,{gy + 20} Q{w * .2:.0f},{gy - 30} {w * .45:.0f},{gy + 10} T{w * .8:.0f},{gy} T{w},{gy + 10} L{w},{h}Z" fill="#DCEBFA"/>'
    body += f'<path d="M0,{h} L0,{gy + 50} Q{w * .3:.0f},{gy + 20} {w * .6:.0f},{gy + 45} T{w},{gy + 35} L{w},{h}Z" fill="#BFD6EE"/>'
    trees = ([(.03, 260), (.08, 190), (.86, 170), (.92, 250), (.98, 200), (.6, 120)] if not portrait
             else [(.94, 320), (.5, 160)])
    for fx, th in trees:
        body += tree(w * fx, gy + 30, th)
    if not portrait:
        body += xtree(w * .2, gy + 40, 330)
        for (fx, pw, ph, c, r) in [(.135, 70, 55, '#E3243B', '#FFD24F'), (.235, 60, 70, '#1F7A45', '#E3243B'), (.265, 52, 40, '#4FB6FF', '#FFFFFF'), (.165, 46, 34, '#FFD24F', '#E3243B')]:
            body += present(w * fx, gy + 44, pw, ph, c, r)
        body += snowman(w * .73, gy + 42, 62)
        body += holly(40, 150, 110, 20) + holly(w - 40, h * .55, 90, 200)
        for bx, by, br, bc in [(w * .06, 210, 24, '#E3243B'), (w * .38, 140, 16, '#FFC93C'), (w * .62, 120, 18, '#1F9E5B'), (w * .95, 240, 22, '#E3243B')]:
            body += bauble(bx, by, br, bc, 0)
    else:
        body += xtree(w * .22, gy + 40, 360)
        body += present(w * .38, gy + 46, 80, 60, '#E3243B', '#FFD24F') + present(w * .05, gy + 46, 70, 70, '#1F7A45', '#E3243B')
        body += snowman(w * .7, gy + 46, 70)
        body += holly(30, 170, 110, 20)
        for bx, by, br, bc in [(w * .1, 260, 26, '#E3243B'), (w * .9, 300, 24, '#FFC93C')]:
            body += bauble(bx, by, br, bc, 0)
    defs = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07142A"/><stop offset=".55" stop-color="#0E2A44"/><stop offset="1" stop-color="#163C4E"/></linearGradient>'
            '<radialGradient id="aur"><stop offset="0" stop-color="#2FD4A0" stop-opacity=".16"/><stop offset=".6" stop-color="#3A6BD8" stop-opacity=".08"/><stop offset="1" stop-color="#3A6BD8" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="moonglow"><stop offset=".45" stop-color="#FFF1C9" stop-opacity=".45"/><stop offset="1" stop-color="#FFF1C9" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="tglow"><stop offset="0" stop-color="#FFD24F" stop-opacity=".25"/><stop offset="1" stop-color="#FFD24F" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="sglow"><stop offset="0" stop-color="#FFE7A3" stop-opacity=".55"/><stop offset="1" stop-color="#FFE7A3" stop-opacity="0"/></radialGradient>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs>{body}</svg>'

if __name__ == '__main__':
    d = '/home/claude/paintingpixie-v2/img/bg/'
    open(d + 'christmas-night.svg', 'w').write(christmas())
    open(d + 'christmas-night-tall.svg', 'w').write(christmas(900, 1600, True))
    print('ok')
