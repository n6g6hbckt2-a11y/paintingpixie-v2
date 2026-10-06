# -*- coding: utf-8 -*-
"""Halloween night background (SVG): moon, bats, pumpkins, spider webs, stars. Written to the draft and the live repo."""
import math, random

W, H = 1600, 1000

def bat(x, y, s, rot, c='#0B0612'):
    return (f'<g transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f}) scale({s:.2f})">'
            f'<path d="M0,6 C-8,-6 -22,-10 -40,-4 C-34,-2 -30,4 -30,10 C-26,6 -20,6 -16,10 C-14,4 -8,4 -4,8 L0,2 '
            f'L4,8 C8,4 14,4 16,10 C20,6 26,6 30,10 C30,4 34,-2 40,-4 C22,-10 8,-6 0,6Z" fill="{c}"/>'
            f'<path d="M-4,-2 L-3,-8 L-1,-3 L1,-3 L3,-8 L4,-2 C3,4 -3,4 -4,-2Z" fill="{c}"/></g>')

def pumpkin(x, y, r, face=True, glow=True):
    o = ''
    if glow:
        o += f'<circle cx="{x}" cy="{y}" r="{r * 2.2:.0f}" fill="url(#pglow)"/>'
    for dx, rr, col in [(-r * .55, r * .62, '#E8660E'), (r * .55, r * .62, '#E8660E'), (-r * .25, r * .7, '#FF7A1A'), (r * .25, r * .7, '#FF7A1A'), (0, r * .72, '#FF8C2A')]:
        o += f'<ellipse cx="{x + dx:.0f}" cy="{y:.0f}" rx="{rr:.0f}" ry="{r * .82:.0f}" fill="{col}" stroke="#B9480A" stroke-width="2"/>'
    o += f'<path d="M{x - 4:.0f},{y - r * .78:.0f} q-2,-{r * .35:.0f} 8,-{r * .45:.0f}" stroke="#3E6B1F" stroke-width="{max(4, r * .14):.0f}" fill="none" stroke-linecap="round"/>'
    if face:
        e = r * .22
        o += (f'<path d="M{x - r * .42:.0f},{y - r * .12:.0f} l{e:.0f},-{e * 1.3:.0f} l{e:.0f},{e * 1.3:.0f}Z" fill="#FFE27A"/>'
              f'<path d="M{x + r * .02:.0f},{y - r * .12:.0f} l{e:.0f},-{e * 1.3:.0f} l{e:.0f},{e * 1.3:.0f}Z" fill="#FFE27A" transform="translate({r * .18:.0f},0)"/>'
              f'<path d="M{x - r * .5:.0f},{y + r * .18:.0f} q{r * .5:.0f},{r * .45:.0f} {r:.0f},0 l-{r * .14:.0f},{r * .12:.0f} l-{r * .12:.0f},-{r * .1:.0f} l-{r * .12:.0f},{r * .12:.0f} '
              f'l-{r * .12:.0f},-{r * .1:.0f} l-{r * .12:.0f},{r * .12:.0f} l-{r * .12:.0f},-{r * .1:.0f} l-{r * .12:.0f},{r * .12:.0f}Z" fill="#FFE27A"/>')
    return o

def web(cx, cy, R, a0, a1):
    o = ''
    spokes = 7
    angs = [a0 + (a1 - a0) * k / (spokes - 1) for k in range(spokes)]
    for a in angs:
        o += f'<line x1="{cx}" y1="{cy}" x2="{cx + math.cos(a) * R:.0f}" y2="{cy + math.sin(a) * R:.0f}" stroke="#D9CCE8" stroke-width="1.6" opacity=".55"/>'
    for ring in range(1, 7):
        rr = R * ring / 6.5
        pts = [(cx + math.cos(a) * rr, cy + math.sin(a) * rr) for a in angs]
        d = f'M{pts[0][0]:.0f},{pts[0][1]:.0f}'
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            qx, qy = cx + (mx - cx) * .88, cy + (my - cy) * .88
            d += f' Q{qx:.0f},{qy:.0f} {x1:.0f},{y1:.0f}'
        o += f'<path d="{d}" stroke="#D9CCE8" stroke-width="1.3" fill="none" opacity=".5"/>'
    return o

def spider(x, y, drop):
    o = f'<line x1="{x}" y1="0" x2="{x}" y2="{y}" stroke="#D9CCE8" stroke-width="1.2" opacity=".6"/>'
    for k in range(4):
        for sgn in (-1, 1):
            o += f'<path d="M{x},{y} q{sgn * 10},{-6 + k * 4} {sgn * 16},{-2 + k * 5}" stroke="#0B0612" stroke-width="2.4" fill="none"/>'
    o += f'<ellipse cx="{x}" cy="{y + 2}" rx="7" ry="9" fill="#0B0612"/><circle cx="{x}" cy="{y - 7}" r="5" fill="#0B0612"/>'
    return o

def halloween(w=1600, h=1000, portrait=False):
    global W, H
    W, H = w, h
    rng = random.Random(31)
    sx = lambda v: v / 1600 * w
    body = '<rect width="100%" height="100%" fill="url(#sky)"/>'
    for _ in range(170):
        body += f'<circle cx="{rng.uniform(0, W):.0f}" cy="{rng.uniform(0, H * .75):.0f}" r="{rng.uniform(.6, 1.9):.1f}" fill="#FFF3D6" opacity="{rng.uniform(.3, .9):.2f}"/>'
    mx, my, mr = (sx(1290), 200, 120) if not portrait else (w * .72, 230, 110)
    body += f'<circle cx="{mx:.0f}" cy="{my}" r="{mr * 1.9:.0f}" fill="url(#moonglow)"/><circle cx="{mx:.0f}" cy="{my}" r="{mr}" fill="#FFE9B0"/>'
    body += f'<circle cx="{mx - mr * .33:.0f}" cy="{my - mr * .25:.0f}" r="{mr * .18:.0f}" fill="#F2D28A" opacity=".6"/><circle cx="{mx + mr * .3:.0f}" cy="{my + mr * .3:.0f}" r="{mr * .12:.0f}" fill="#F2D28A" opacity=".55"/>'
    bats = [(1190, 260, 1.4, -10), (1350, 120, 1.0, 12), (1420, 300, .8, -6), (980, 120, .9, 8), (300, 140, 1.2, -14), (520, 80, .7, 10), (160, 330, .8, 6), (760, 220, .6, -8), (1530, 420, 1.1, 14)]
    for x, y, sc, r in bats:
        body += bat(sx(x), y * (1.25 if portrait else 1), sc, r)
    gy = H - 120
    body += f'<path d="M0,{H} L0,{gy} Q{w * .12:.0f},{gy - 60} {w * .26:.0f},{gy - 10} T{w * .54:.0f},{gy - 20} T{w * .81:.0f},{gy - 30} T{w},{gy - 20} L{w},{H}Z" fill="#0B0612"/>'
    pumpkins = [(.07, 20, 64), (.16, 55, 42), (.89, 25, 70), (.97, 65, 40), (.81, 70, 34)] if not portrait else [(.16, 30, 58), (.4, 70, 36), (.82, 35, 60), (.62, 80, 30)]
    for fx, dy, r in pumpkins:
        body += pumpkin(w * fx, gy + dy, r)
    body += web(0, 0, min(330, w * .36), 0, math.pi / 2) + web(W, 0, min(260, w * .3), math.pi / 2, math.pi)
    body += spider(w * .13, 240, 0) + spider(w * .94, 560 if not portrait else 700, 0)
    defs = ('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A0B2E"/><stop offset=".6" stop-color="#2A1240"/><stop offset="1" stop-color="#3B1530"/></linearGradient>'
            '<radialGradient id="moonglow"><stop offset=".45" stop-color="#FFD98A" stop-opacity=".55"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="pglow"><stop offset="0" stop-color="#FF8C2A" stop-opacity=".45"/><stop offset="1" stop-color="#FF8C2A" stop-opacity="0"/></radialGradient>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs>{body}</svg>'

if __name__ == '__main__':
    land, port = halloween(), halloween(900, 1600, True)
    for d in ['/home/claude/paintingpixie-v2/img/bg/', '/home/claude/paintingpixie-v2/hw/']:
        open(d + 'halloween-night.svg', 'w').write(land); open(d + 'halloween-night-tall.svg', 'w').write(port)
    print('ok')
