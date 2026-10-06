# -*- coding: utf-8 -*-
"""Design ideas page: colourful header backgrounds for Kat to choose from (instead of plain black).
Backgrounds are generated as lightweight SVG files in img/bg/. Page: draft/design-ideas.html (not indexed)."""
import json, math, os, random, re

V2 = '/home/claude/paintingpixie-v2'
BG = V2 + '/img/bg'
W, H = 1600, 1000

def svg(body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
            f'<defs>{defs}</defs>{body}</svg>')

def glow(id_, sd):
    return f'<filter id="{id_}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{sd}" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'

# ---------- A: lightning ----------
def bolt(rng, x, y, length, angle, steps):
    pts = [(x, y)]
    for i in range(steps):
        a = angle + rng.uniform(-.55, .55)
        seg = length / steps * rng.uniform(.7, 1.3)
        x += math.cos(a) * seg; y += math.sin(a) * seg
        pts.append((x, y))
    return pts

def lightning():
    rng = random.Random(7)
    cols = ['#B36BFF', '#FF4FD8', '#4FE3FF', '#FFD84F', '#B36BFF']
    body = '<rect width="100%" height="100%" fill="url(#sky)"/>'
    for i, (x, y, L, ang) in enumerate([(120, -20, 900, 1.25), (520, -40, 700, 1.6), (980, -30, 1100, 1.75), (1350, -20, 800, 1.9), (300, 1020, 500, -1.3)]):
        pts = bolt(rng, x, y, L, ang, 9)
        d = 'M' + ' L'.join(f'{a:.0f},{b:.0f}' for a, b in pts)
        c = cols[i]
        body += f'<path d="{d}" stroke="{c}" stroke-width="5" fill="none" stroke-linejoin="miter" filter="url(#gl)" opacity=".95"/>'
        body += f'<path d="{d}" stroke="#fff" stroke-width="1.6" fill="none" opacity=".9"/>'
        for k in range(2, len(pts) - 1, 3):  # forks
            fx, fy = pts[k]
            f = bolt(rng, fx, fy, L * .35, ang + rng.choice([-.8, .8]), 4)
            fd = 'M' + ' L'.join(f'{a:.0f},{b:.0f}' for a, b in f)
            body += f'<path d="{fd}" stroke="{c}" stroke-width="2.5" fill="none" filter="url(#gl)" opacity=".75"/><path d="{fd}" stroke="#fff" stroke-width=".8" fill="none" opacity=".7"/>'
    defs = glow('gl', 7) + '<radialGradient id="sky" cx="50%" cy="0%" r="110%"><stop offset="0" stop-color="#241237"/><stop offset=".6" stop-color="#0B0712"/><stop offset="1" stop-color="#050308"/></radialGradient>'
    return svg(body, defs)

# ---------- B: colour swirls (dark) / C: bright swirls ----------
def swirl_paths(rng, cols, n, width):
    out = ''
    for i in range(n):
        cx, cy = rng.uniform(-100, W + 100), rng.uniform(-100, H + 100)
        r0 = rng.uniform(40, 120); turns = rng.uniform(1.6, 2.6); grow = rng.uniform(55, 95)
        pts = []
        for t in range(0, int(turns * 60)):
            a = t / 60 * 2 * math.pi + i
            r = r0 + grow * t / 60 * 2
            pts.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
        d = 'M' + ' L'.join(f'{a:.0f},{b:.0f}' for a, b in pts)
        c = cols[i % len(cols)]
        out += f'<path d="{d}" stroke="{c}" stroke-width="{width * rng.uniform(.6, 1.4):.0f}" fill="none" stroke-linecap="round" opacity="{rng.uniform(.55, .9):.2f}"/>'
    return out

def swirls_dark():
    rng = random.Random(3)
    body = '<rect width="100%" height="100%" fill="#140C1E"/>' + swirl_paths(rng, ['#FF4FA3', '#9B5BFF', '#2FD4C4', '#FFC94F', '#FF7A3C'], 9, 22)
    body += swirl_paths(random.Random(11), ['#ffffff'], 5, 3)
    return svg(body)

def swirls_bright():
    rng = random.Random(5)
    body = '<rect width="100%" height="100%" fill="url(#g)"/>' + swirl_paths(rng, ['#FFE14F', '#2FD4C4', '#ffffff', '#FF9ED2', '#7A3BFF'], 10, 26)
    defs = '<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7A2BD9"/><stop offset=".5" stop-color="#E0348F"/><stop offset="1" stop-color="#FF7A3C"/></linearGradient>'
    return svg(body, defs)

# ---------- D: fireworks ----------
def fireworks():
    rng = random.Random(9)
    body = '<rect width="100%" height="100%" fill="url(#night)"/>'
    for _ in range(140):
        body += f'<circle cx="{rng.uniform(0, W):.0f}" cy="{rng.uniform(0, H):.0f}" r="{rng.uniform(.6, 1.8):.1f}" fill="#fff" opacity="{rng.uniform(.3, .9):.2f}"/>'
    cols = [('#FFD84F', '#FF9E3C'), ('#FF4FD8', '#FF8AC4'), ('#4FE3FF', '#9BF0FF'), ('#B36BFF', '#E0C2FF'), ('#7CFF7A', '#D6FFB0'), ('#FF5A5A', '#FFC2A0')]
    for i, (x, y, R) in enumerate([(220, 230, 170), (620, 140, 120), (420, 620, 140), (1050, 260, 200), (1420, 150, 110), (1300, 650, 160), (820, 480, 90)]):
        c1, c2 = cols[i % len(cols)]
        rays = 26 + i * 2
        g = f'<g filter="url(#gl)">'
        for k in range(rays):
            a = k / rays * 2 * math.pi + rng.uniform(-.05, .05)
            r1 = R * rng.uniform(.25, .4); r2 = R * rng.uniform(.8, 1.05)
            x1, y1, x2, y2 = x + math.cos(a) * r1, y + math.sin(a) * r1, x + math.cos(a) * r2, y + math.sin(a) * r2
            g += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{c1}" stroke-width="2.4" stroke-linecap="round"/>'
            g += f'<circle cx="{x2:.0f}" cy="{y2:.0f}" r="{rng.uniform(2.5, 4.5):.1f}" fill="{c2}"/>'
        g += f'<circle cx="{x}" cy="{y}" r="{R * .12:.0f}" fill="{c2}" opacity=".85"/></g>'
        body += g
        body += f'<path d="M{x + rng.uniform(-30, 30):.0f},{H} Q{x + 40:.0f},{(H + y) / 2:.0f} {x},{y + R * .2:.0f}" stroke="{c1}" stroke-width="1.6" fill="none" opacity=".35" stroke-dasharray="4 10"/>'
    defs = glow('gl', 3) + '<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A0920"/><stop offset=".7" stop-color="#1C0F33"/><stop offset="1" stop-color="#3A1240"/></linearGradient>'
    return svg(body, defs)

# ---------- E: glitter galaxy ----------
def galaxy():
    rng = random.Random(21)
    body = '<rect width="100%" height="100%" fill="#0E0718"/>'
    for cx, cy, r, c in [(300, 700, 600, '#7A2BD9'), (1200, 300, 650, '#E0348F'), (800, 900, 500, '#1B8FA8'), (100, 100, 400, '#3B2B9F')]:
        body += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#n{c[1:]})"/>'
    defs = ''.join(f'<radialGradient id="n{c[1:]}"><stop offset="0" stop-color="{c}" stop-opacity=".75"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>' for c in ['#7A2BD9', '#E0348F', '#1B8FA8', '#3B2B9F'])
    cols = ['#FFFFFF', '#FFD84F', '#FF9ED2', '#9BF0FF', '#D6B8FF']
    for _ in range(650):
        body += f'<circle cx="{rng.uniform(0, W):.0f}" cy="{rng.uniform(0, H):.0f}" r="{rng.uniform(.5, 2.4):.1f}" fill="{rng.choice(cols)}" opacity="{rng.uniform(.4, 1):.2f}"/>'
    for _ in range(26):
        x, y, s = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(6, 16)
        body += f'<path d="M{x:.0f},{y - s:.0f} Q{x:.0f},{y:.0f} {x + s:.0f},{y:.0f} Q{x:.0f},{y:.0f} {x:.0f},{y + s:.0f} Q{x:.0f},{y:.0f} {x - s:.0f},{y:.0f} Q{x:.0f},{y:.0f} {x:.0f},{y - s:.0f}Z" fill="{rng.choice(cols)}"/>'
    return svg(body, defs)

# ---------- F: rainbow waves ----------
def rainbow_waves():
    body = '<rect width="100%" height="100%" fill="#120B1C"/>'
    cols = ['#FF4F6E', '#FF9A3C', '#FFD84F', '#7CE36B', '#2FD4C4', '#4FA3FF', '#9B5BFF', '#FF4FD8']
    for i, c in enumerate(cols):
        y0 = 160 + i * 52
        d = f'M-50,{y0} C300,{y0 - 220} 600,{y0 + 260} 900,{y0 + 40} S1400,{y0 - 200} 1700,{y0 + 60} L1700,{y0 + 60 + 44} S1400,{y0 - 156} 900,{y0 + 84} S300,{y0 - 176} -50,{y0 + 44}Z'
        body += f'<path d="{d}" fill="{c}" opacity=".92"/>'
    rng = random.Random(4)
    for _ in range(90):
        body += f'<circle cx="{rng.uniform(0, W):.0f}" cy="{rng.uniform(560, H):.0f}" r="{rng.uniform(.8, 2.4):.1f}" fill="#fff" opacity="{rng.uniform(.3, .8):.2f}"/>'
    return svg(body)

# ---------- G: paint splashes ----------
def splat(rng, x, y, r, c):
    pts = []
    n = 22
    for k in range(n):
        a = k / n * 2 * math.pi
        rr = r * (rng.uniform(.75, 1.05) if k % 3 else rng.uniform(1.15, 1.6))
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    d = 'M' + ' '.join(f'{a:.0f},{b:.0f}' for a, b in pts) + 'Z'
    out = f'<path d="{d}" fill="{c}" stroke="{c}" stroke-width="18" stroke-linejoin="round"/>'
    for _ in range(9):
        a = rng.uniform(0, 2 * math.pi); dd = r * rng.uniform(1.5, 2.6)
        out += f'<circle cx="{x + math.cos(a) * dd:.0f}" cy="{y + math.sin(a) * dd:.0f}" r="{r * rng.uniform(.05, .16):.0f}" fill="{c}"/>'
    return out

def paint_splash():
    rng = random.Random(12)
    body = '<rect width="100%" height="100%" fill="#16101F"/>'
    for x, y, r, c in [(180, 220, 150, '#FF4FA3'), (520, 760, 170, '#2FD4C4'), (900, 160, 120, '#FFD84F'), (1250, 520, 190, '#9B5BFF'), (1480, 120, 110, '#FF7A3C'), (80, 820, 120, '#4FA3FF'), (760, 460, 80, '#7CE36B'), (1500, 880, 140, '#FF4FD8')]:
        body += splat(rng, x, y, r, c)
    return svg(body)

# ---------- H: pixie dust ----------
def pixie_dust():
    rng = random.Random(2)
    body = '<rect width="100%" height="100%" fill="url(#pg)"/>'
    pts = [(-50, 900), (180, 600), (420, 800), (620, 330), (900, 520), (1300, 220), (1700, 120)]
    for k in range(700):
        t = rng.random(); i = min(int(t * (len(pts) - 1)), len(pts) - 2); f = t * (len(pts) - 1) - i
        x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f + rng.gauss(0, 34)
        y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f + rng.gauss(0, 34)
        body += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rng.uniform(.6, 3):.1f}" fill="{rng.choice(["#FFE38A", "#FFD24F", "#FFF6D6", "#FFB3E0"])}" opacity="{rng.uniform(.4, 1):.2f}"/>'
    for _ in range(18):
        x, y, s = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(8, 20)
        body += f'<path d="M{x:.0f},{y - s:.0f} Q{x:.0f},{y:.0f} {x + s:.0f},{y:.0f} Q{x:.0f},{y:.0f} {x:.0f},{y + s:.0f} Q{x:.0f},{y:.0f} {x - s:.0f},{y:.0f} Q{x:.0f},{y:.0f} {x:.0f},{y - s:.0f}Z" fill="#FFE38A" filter="url(#gl)"/>'
    defs = glow('gl', 4) + '<linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2A0F4A"/><stop offset=".55" stop-color="#5A1A6E"/><stop offset="1" stop-color="#8A2462"/></linearGradient>'
    return svg(body, defs)

OPTIONS = [
    ('lightning', 'Electric lightning', 'Black night sky with neon lightning bolts in violet, pink, blue and gold. Bold and dramatic.', lightning),
    ('swirls-dark', 'Colour swirls', 'Deep plum with big swirls of pink, purple, teal and gold, like brush strokes on a palette.', swirls_dark),
    ('swirls-bright', 'Bright sunset swirls', 'No black at all: purple through pink to orange, with yellow, teal and white swirls.', swirls_bright),
    ('fireworks', 'Fireworks', 'Midnight-blue sky with fireworks bursting in gold, pink, blue and green.', fireworks),
    ('galaxy', 'Glitter galaxy', 'Purple and pink nebula clouds scattered with coloured glitter and sparkles.', galaxy),
    ('rainbow', 'Rainbow waves', 'Flowing rainbow ribbons across a dark background, like a painted rainbow.', rainbow_waves),
    ('splash', 'Paint splashes', 'Big colourful paint splats, the face painter’s palette.', paint_splash),
    ('pixie-dust', 'Pixie dust', 'Purple-to-pink with a trail of golden fairy dust. A nod to the Pixie name.', pixie_dust),
]

PHOTO = '../img/g/{}-1600.webp'

def page():
    secs = []
    for i, (slug, name, desc, _) in enumerate(OPTIONS):
        letter = chr(65 + i)
        photo = PHOTO.format(['unicorn-party', 'blue-monster-roar', 'rainbow-laughing', 'tiger-girl-closeup', 'adult-lilac-flower', 'rainbow-sisters', 'leopard-claws', 'fairy-festival'][i])
        secs.append(f'''<section class="opt" id="{slug}">
<div class="ohead"><span class="letter">{letter}</span><div><h2>{name}</h2><p>{desc}</p></div></div>
<div class="previews">
<div class="desk" style="background-image:url(../img/bg/{slug}.svg)"><img src="{photo}" alt=""><div class="card"><small>HOME · OCCASIONS</small><b>Children’s Party Face Painting</b><span>Magical, skin-safe face painting for birthday parties across Sussex and Surrey.</span><i>Check my date</i><i class="wa">WhatsApp Kat</i></div></div>
<div class="phone" style="background-image:url(../img/bg/{slug}.svg)"><img src="{photo}" alt=""><div class="card"><b>Children’s Party Face Painting</b><span>Skin-safe face painting for parties.</span><i>Check my date</i></div></div>
</div>
<div class="band" style="background-image:url(../img/bg/{slug}.svg)"><b>Also works as a section background</b><span>For example behind reviews, prices or the booking form.</span></div>
</section>''')
    nav = ''.join(f'<a href="#{s}">{chr(65 + i)} · {n}</a>' for i, (s, n, _, _) in enumerate(OPTIONS))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Design ideas: header backgrounds | The Painting Pixie</title><meta name="robots" content="noindex,nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--ink:#1B1712;--muted:#5A5049;--bg:#F6F1EA;--gold:#E2BE7A}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Manrope,system-ui,sans-serif}}
.wrap{{max-width:1200px;margin:0 auto;padding:0 20px}}
header.top{{padding:40px 0 10px}}header.top img{{width:84px;height:84px;border-radius:50%}}
h1{{font:400 clamp(34px,5vw,56px)/1.05 Fraunces,serif;margin:14px 0 10px}}
.lede{{max-width:760px;color:var(--muted);font-size:18px}}
.jump{{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 10px}}.jump a{{padding:9px 14px;border-radius:999px;background:#fff;border:1.5px solid #E2D6C8;color:var(--ink);text-decoration:none;font-weight:700;font-size:14px}}
.opt{{padding:46px 0;border-top:1px solid #E2D6C8}}
.ohead{{display:flex;gap:18px;align-items:center;margin-bottom:18px}}
.letter{{flex:0 0 58px;height:58px;border-radius:50%;background:var(--ink);color:#fff;display:grid;place-items:center;font:600 28px Fraunces,serif}}
.ohead h2{{margin:0;font:400 32px/1.1 Fraunces,serif}}.ohead p{{margin:4px 0 0;color:var(--muted)}}
.previews{{display:grid;grid-template-columns:3fr 1fr;gap:18px;align-items:start}}
.desk,.phone,.band{{background-size:cover;background-position:center;border-radius:16px;overflow:hidden;position:relative;box-shadow:0 26px 50px -30px rgba(30,10,30,.6)}}
.desk{{aspect-ratio:16/9}}
.desk>img{{position:absolute;right:0;top:0;width:60%;height:100%;object-fit:cover;-webkit-mask-image:linear-gradient(90deg,transparent,#000 6%);mask-image:linear-gradient(90deg,transparent,#000 6%)}}
.card{{position:absolute;background:rgba(14,12,18,.8);color:#fff;border-radius:14px;display:flex;flex-direction:column;gap:6px}}
.desk .card{{left:5%;bottom:9%;width:40%;padding:22px 24px}}
.card small{{color:var(--gold);font-weight:800;letter-spacing:.12em;font-size:10px}}
.card b{{font:400 clamp(18px,2.4vw,30px)/1.1 Fraunces,serif}}.card span{{font-size:13px;opacity:.85}}
.card i{{font-style:normal;display:inline-block;width:max-content;padding:8px 14px;border-radius:999px;background:var(--gold);color:#1B1712;font-weight:800;font-size:12px;margin-top:4px}}
.card i.wa{{background:#25D366;color:#fff;margin-top:-34px;margin-left:120px}}
.phone{{aspect-ratio:9/19;border:6px solid #1B1712;border-radius:28px}}
.phone>img{{position:absolute;left:0;top:0;width:100%;height:54%;object-fit:cover;-webkit-mask-image:linear-gradient(180deg,#000 80%,transparent);mask-image:linear-gradient(180deg,#000 80%,transparent)}}
.phone .card{{left:7%;right:7%;bottom:6%;padding:14px}}.phone .card b{{font-size:17px}}.phone .card span{{font-size:11px}}.phone .card i{{font-size:11px;width:100%;text-align:center}}
.band{{margin-top:18px;padding:34px 30px;color:#fff;display:flex;flex-direction:column}}
.band b{{font:400 24px Fraunces,serif;text-shadow:0 2px 12px rgba(0,0,0,.6)}}.band span{{text-shadow:0 2px 10px rgba(0,0,0,.7)}}
.foot{{padding:40px 0 70px;color:var(--muted)}}
@media(max-width:800px){{.previews{{grid-template-columns:1fr}}.phone{{max-width:240px;margin:0 auto}}.desk .card{{width:52%;padding:12px}}.card i.wa{{display:none}}.card span{{display:none}}}}
</style></head><body>
<header class="top"><div class="wrap"><img src="../img/logo-lg.webp" alt="The Painting Pixie">
<h1>Design ideas: colourful backgrounds</h1>
<p class="lede">Kat would like colour behind the page headers instead of plain black. Here are eight ideas, each shown on a laptop header, a phone, and as a section background. Pick a favourite (or two to mix), and it can go across the whole site.</p>
<p class="lede"><a href="design-ideas-homepage.html"><b>See them on the real homepage →</b></a> Every section that’s currently black shows a different idea, with a chooser to try one everywhere.</p>
<nav class="jump">{nav}</nav></div></header>
<main class="wrap">{"".join(secs)}</main>
<p class="foot wrap">Draft page for choosing a design. It isn’t linked from the site menus and is hidden from Google. <a href="index.html">Back to the draft site</a></p>
</body></html>'''

def homepage_demo():
    s = open(V2 + '/draft/index.html').read()
    s = s.replace('<meta name="robots" content="index, follow">', '')
    s = s.replace('</head>', '<meta name="robots" content="noindex,nofollow">\n</head>', 1)
    s = re.sub(r'<title>.*?</title>', '<title>Design ideas: homepage backgrounds | The Painting Pixie</title>', s, count=1, flags=re.S)
    opts = [(sl, chr(65 + i), n) for i, (sl, n, _, _) in enumerate(OPTIONS)]
    btns = '<button type="button" data-o="mix" class="on">Mix: a different idea in each section</button><button type="button" data-o="none">Current (plain black)</button>' + ''.join(
        f'<button type="button" data-o="{sl}"><b>{l}</b> {n}</button>' for sl, l, n in opts)
    panel = f'''<div id="dpanel" role="region" aria-label="Background chooser"><div class="dp-h"><b>Background ideas</b><button type="button" id="dpmin" aria-label="Hide or show the chooser">–</button></div>
<p>Kat’s colourful backgrounds on every section that’s currently black. Pick one to see it everywhere.</p><div class="dp-b">{btns}</div></div>'''
    css = '''<style>
#dpanel{position:fixed;right:16px;bottom:96px;z-index:9999;width:300px;max-height:70vh;overflow:auto;background:#fff;color:#1B1712;border-radius:16px;box-shadow:0 24px 60px rgba(0,0,0,.45);padding:14px 14px 12px;font:14px/1.4 Manrope,system-ui,sans-serif}
#dpanel p{margin:6px 0 10px;color:#5A5049;font-size:13px}
.dp-h{display:flex;justify-content:space-between;align-items:center}.dp-h b{font:400 20px Fraunces,serif}
#dpmin{border:0;background:#F1EAE1;border-radius:8px;width:30px;height:30px;font-size:18px;cursor:pointer}
.dp-b{display:flex;flex-direction:column;gap:6px}
.dp-b button{text-align:left;border:1.5px solid #E2D6C8;background:#fff;border-radius:10px;padding:9px 12px;font:600 14px Manrope,system-ui,sans-serif;cursor:pointer;color:#1B1712}
.dp-b button b{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:#1B1712;color:#fff;font-size:12px;margin-right:6px}
.dp-b button.on{border-color:#FF4FA3;background:#FFF0F7}
#dpanel.min p,#dpanel.min .dp-b{display:none}#dpanel.min{width:auto}
.bgx{background-size:cover!important;background-position:center!important;position:relative}
.bgtag{position:absolute;top:12px;left:12px;z-index:5;background:#fff;color:#1B1712;font:800 12px Manrope,system-ui,sans-serif;padding:6px 10px;border-radius:999px;box-shadow:0 6px 16px rgba(0,0,0,.35)}
@media(max-width:600px){#dpanel{left:12px;right:12px;width:auto;bottom:90px;max-height:46vh}}
</style>'''
    names = {sl: (l, n) for sl, l, n in opts}
    js = '''<script>
(function(){
  var OPTS=%s, NAMES=%s;
  function lum(c){var m=c.match(/[0-9.]+/g);if(!m||(m[3]!==undefined&&+m[3]<.5))return null;return (0.299*m[0]+0.587*m[1]+0.114*m[2]);}
  var bodyL=lum(getComputedStyle(document.body).backgroundColor);
  var cands=[].slice.call(document.querySelectorAll('body > div, body > section, main > *, body > footer, .trust, .strip'));
  var dark=cands.filter(function(e){
    if(e.id==='dpanel'||e.closest('#dpanel')||e.matches('header.hero, nav, .wa-float, .mbar, .jewel-rule, script, style')||e.offsetHeight<120)return false;
    var cs=getComputedStyle(e), L=lum(cs.backgroundColor), T=lum(cs.color);
    if(L!==null)return L<70;
    return T!==null&&T>170;
  });
  // keep only outermost dark blocks
  dark=dark.filter(function(e){return !dark.some(function(o){return o!==e&&o.contains(e)})});
  dark.forEach(function(e){e.dataset.bg0=e.style.backgroundImage||'';});
  function apply(o){
    document.querySelectorAll('.bgtag').forEach(function(t){t.remove()});
    dark.forEach(function(e,i){
      var sl=o==='mix'?OPTS[i%%OPTS.length]:o;
      if(o==='none'){e.style.backgroundImage=e.dataset.bg0;e.classList.remove('bgx');return}
      e.classList.add('bgx');e.style.backgroundImage='linear-gradient(rgba(14,11,20,.38),rgba(14,11,20,.38)),url(../img/bg/'+sl+'.svg)';
      if(getComputedStyle(e).position==='static')e.style.position='relative';
      var t=document.createElement('span');t.className='bgtag';t.textContent=NAMES[sl][0]+' · '+NAMES[sl][1];e.appendChild(t);
    });
    document.querySelectorAll('.dp-b button').forEach(function(b){b.classList.toggle('on',b.dataset.o===o)});
  }
  document.querySelectorAll('.dp-b button').forEach(function(b){b.addEventListener('click',function(){apply(b.dataset.o)})});
  document.getElementById('dpmin').addEventListener('click',function(){document.getElementById('dpanel').classList.toggle('min')});
  var h=location.hash.slice(1); apply(OPTS.indexOf(h)>-1?h:'mix');
})();
</script>''' % (json.dumps([sl for sl, _, _ in opts]), json.dumps(names))
    s = s.replace('</head>', css + '\n</head>', 1)
    s = s.replace('</body>', panel + js + '\n</body>', 1)
    open(V2 + '/draft/design-ideas-homepage.html', 'w').write(s)

def build():
    os.makedirs(BG, exist_ok=True)
    for slug, _, _, fn in OPTIONS:
        open(f'{BG}/{slug}.svg', 'w').write(fn())
    open(V2 + '/draft/design-ideas.html', 'w').write(page())
    homepage_demo()
    print('design ideas built:', len(OPTIONS), 'options')

if __name__ == '__main__':
    build()
