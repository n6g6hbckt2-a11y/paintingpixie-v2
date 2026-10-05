# -*- coding: utf-8 -*-
"""Illustrated 'postcard' banners of local landmarks (original flat illustrations, 1200x340)."""

W, H = 1200, 340
INK = "#1B1712"

def sky(acc, night=False):
    top, bot = ("#1E1B4B", "#5B3B8C") if night else ("#FFE9D6", "#FFF6EC")
    return (f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bot}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#sky)"/>')

def sun(x=1020, y=80, r=42, acc="#FFB347"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{acc}" opacity=".85"/>'

def clouds():
    c = lambda x, y, s: (f'<g fill="#fff" opacity=".9"><ellipse cx="{x}" cy="{y}" rx="{46*s}" ry="{16*s}"/>'
                         f'<ellipse cx="{x+28*s}" cy="{y-10*s}" rx="{30*s}" ry="{18*s}"/></g>')
    return c(220, 70, 1) + c(640, 50, .8)

def hills(cols=("#B9D99A", "#8CC084", "#5FA26B"), base=250):
    out = ''
    for i, col in enumerate(cols):
        y = base - 70 + i * 35
        out += (f'<path d="M0 {y+40} C 150 {y-30}, 300 {y+10}, 450 {y-20} S 750 {y+30}, 900 {y-10} S 1100 {y+20}, 1200 {y-15} V {H} H 0 Z" fill="{col}"/>')
    return out

def ground(col="#7FB77E", y=290):
    return f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="{col}"/>'

def sea(y=250):
    waves = ''.join(f'<path d="M{x} {y+30} q 15 -8 30 0 t 30 0" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/>' for x in range(30, 1200, 140))
    return (f'<rect x="0" y="{y}" width="{W}" height="{H-y}" fill="#4FA8D8"/><rect x="0" y="{y}" width="{W}" height="10" fill="#7CC6EA"/>' + waves
            + f'<rect x="0" y="{H-28}" width="{W}" height="28" fill="#F3D9A4"/>')

def pier(x=520, y=250, length=520, pavilion=True, lights=False):
    legs = ''.join(f'<rect x="{x+i}" y="{y}" width="6" height="40" fill="{INK}"/>' for i in range(0, length, 44))
    deck = f'<rect x="{x}" y="{y-8}" width="{length}" height="10" fill="#E8DCC8" stroke="{INK}" stroke-width="2"/>'
    pav = ''
    if pavilion:
        px = x + length - 150
        pav = (f'<rect x="{px}" y="{y-60}" width="120" height="52" fill="#F7F1E6" stroke="{INK}" stroke-width="2"/>'
               f'<path d="M{px-6} {y-60} Q {px+60} {y-120} {px+126} {y-60} Z" fill="#E2BE7A" stroke="{INK}" stroke-width="2"/>'
               f'<rect x="{px+52}" y="{y-118}" width="16" height="14" fill="#FF4FA3"/>')
    lit = ''.join(f'<circle cx="{x+i}" cy="{y-12}" r="4" fill="#FFD23F"/>' for i in range(10, length - 160, 30)) if lights else ''
    return legs + deck + pav + lit

def domes(x=180, y=250):
    d = lambda cx, w, h: (f'<path d="M{cx-w} {y-60} Q {cx-w} {y-60-h} {cx} {y-60-h*1.3} Q {cx+w} {y-60-h} {cx+w} {y-60} Z" fill="#F7F1E6" stroke="{INK}" stroke-width="2"/>'
                          f'<line x1="{cx}" y1="{y-60-h*1.3}" x2="{cx}" y2="{y-60-h*1.3-14}" stroke="{INK}" stroke-width="2"/>')
    return (f'<rect x="{x-110}" y="{y-62}" width="260" height="62" fill="#F7F1E6" stroke="{INK}" stroke-width="2"/>'
            + d(x, 34, 40) + d(x - 80, 18, 24) + d(x + 90, 18, 24)
            + ''.join(f'<rect x="{x-96+i*34}" y="{y-44}" width="14" height="30" rx="7" fill="#A77BFF"/>' for i in range(8)))

def castle(x=600, y=230, scale=1.0):
    s = scale; w = 160 * s; h = 90 * s
    cren = ''.join(f'<rect x="{x - w/2 + i*20*s}" y="{y - h - 14*s}" width="{12*s}" height="{14*s}" fill="#CFC3B0" stroke="{INK}" stroke-width="2"/>' for i in range(8))
    return (f'<rect x="{x-w/2}" y="{y-h}" width="{w}" height="{h}" fill="#CFC3B0" stroke="{INK}" stroke-width="2"/>' + cren
            + f'<path d="M{x-14*s} {y} V {y-36*s} Q {x} {y-52*s} {x+14*s} {y-36*s} V {y} Z" fill="{INK}"/>'
            + f'<rect x="{x-50*s}" y="{y-64*s}" width="{10*s}" height="{18*s}" fill="{INK}"/><rect x="{x+40*s}" y="{y-64*s}" width="{10*s}" height="{18*s}" fill="{INK}"/>'
            + f'<line x1="{x}" y1="{y-h-14*s}" x2="{x}" y2="{y-h-56*s}" stroke="{INK}" stroke-width="2"/><path d="M{x} {y-h-56*s} l 34 9 l -34 9 Z" fill="#FF4FA3"/>')

def windmill(x=600, y=250, body="#F7F1E6", sails=INK, s=1.0):
    return (f'<path d="M{x-28*s} {y} L {x-18*s} {y-90*s} L {x+18*s} {y-90*s} L {x+28*s} {y} Z" fill="{body}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x-22*s} {y-90*s} Q {x} {y-118*s} {x+22*s} {y-90*s} Z" fill="#8C6A4F" stroke="{INK}" stroke-width="2"/>'
            f'<g transform="translate({x} {y-96*s}) rotate(20)" stroke="{sails}" stroke-width="3">'
            f'<line x1="-70" y1="0" x2="70" y2="0"/><line x1="0" y1="-70" x2="0" y2="70"/>'
            f'<rect x="12" y="-8" width="56" height="12" fill="#fff" stroke-width="2"/><rect x="-68" y="-4" width="56" height="12" fill="#fff" stroke-width="2"/>'
            f'<rect x="-4" y="12" width="12" height="56" fill="#fff" stroke-width="2"/><rect x="-8" y="-68" width="12" height="56" fill="#fff" stroke-width="2"/></g>'
            f'<rect x="{x-7*s}" y="{y-30*s}" width="{14*s}" height="{30*s}" fill="{INK}"/>')

def timber_houses(x=120, y=270, n=5):
    out = ''
    for i in range(n):
        hx = x + i * 92; hh = 90 + (i % 2) * 18
        out += (f'<rect x="{hx}" y="{y-hh}" width="88" height="{hh}" fill="#FBF3E4" stroke="{INK}" stroke-width="2"/>'
                f'<path d="M{hx-6} {y-hh} L {hx+44} {y-hh-46} L {hx+94} {y-hh} Z" fill="#9A5B3C" stroke="{INK}" stroke-width="2"/>'
                f'<line x1="{hx+44}" y1="{y-hh}" x2="{hx+44}" y2="{y}" stroke="{INK}" stroke-width="5"/>'
                f'<line x1="{hx}" y1="{y-hh/2}" x2="{hx+88}" y2="{y-hh/2}" stroke="{INK}" stroke-width="5"/>'
                f'<line x1="{hx}" y1="{y-hh}" x2="{hx+44}" y2="{y-hh/2}" stroke="{INK}" stroke-width="4"/>'
                f'<line x1="{hx+88}" y1="{y-hh}" x2="{hx+44}" y2="{y-hh/2}" stroke="{INK}" stroke-width="4"/>'
                f'<rect x="{hx+12}" y="{y-34}" width="20" height="24" fill="#4FB6FF" stroke="{INK}" stroke-width="2"/>')
    return out

def train(x=700, y=280, col="#2E7D4F"):
    return (f'<rect x="{x}" y="{y-60}" width="120" height="44" rx="6" fill="{col}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{x+86}" y="{y-92}" width="44" height="76" fill="{col}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{x+20}" y="{y-86}" width="16" height="28" fill="{INK}"/>'
            f'<circle cx="{x+30}" cy="{y-12}" r="14" fill="{INK}"/><circle cx="{x+72}" cy="{y-12}" r="14" fill="{INK}"/><circle cx="{x+112}" cy="{y-12}" r="14" fill="{INK}"/>'
            f'<rect x="{x+136}" y="{y-56}" width="110" height="40" rx="4" fill="#9A3B3B" stroke="{INK}" stroke-width="2"/>'
            f'<circle cx="{x+160}" cy="{y-12}" r="12" fill="{INK}"/><circle cx="{x+222}" cy="{y-12}" r="12" fill="{INK}"/>'
            f'<g fill="#fff" opacity=".9"><circle cx="{x+28}" cy="{y-104}" r="14"/><circle cx="{x+6}" cy="{y-128}" r="18"/><circle cx="{x-30}" cy="{y-146}" r="22"/></g>'
            f'<rect x="0" y="{y}" width="{W}" height="6" fill="{INK}"/>')

def trees(xs, y=270, col="#3F8F5A"):
    return ''.join(f'<rect x="{x-5}" y="{y-30}" width="10" height="30" fill="#7A5236"/><circle cx="{x}" cy="{y-50}" r="30" fill="{col}"/><circle cx="{x-18}" cy="{y-36}" r="20" fill="{col}"/><circle cx="{x+18}" cy="{y-36}" r="20" fill="{col}"/>' for x in xs)

def lake(x=600, y=285, w=380):
    return f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="26" fill="#6EC1E4"/><path d="M{x-80} {y-4} q 12 -6 24 0" stroke="#fff" stroke-width="3" fill="none"/><path d="M{x+40} {y+6} q 12 -6 24 0" stroke="#fff" stroke-width="3" fill="none"/>'

def church(x=900, y=270):
    return (f'<rect x="{x-40}" y="{y-70}" width="80" height="70" fill="#E9E1D3" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{x+40}" y="{y-110}" width="40" height="110" fill="#E9E1D3" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x+36} {y-110} L {x+60} {y-190} L {x+84} {y-110} Z" fill="#8F8578" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x-46} {y-70} L {x} {y-100} L {x+46} {y-70} Z" fill="#8F8578" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M{x-8} {y} V {y-28} Q {x} {y-38} {x+8} {y-28} V {y} Z" fill="{INK}"/>')

def bandstand(x=320, y=275):
    return (f'<rect x="{x-70}" y="{y-14}" width="140" height="14" fill="#E9E1D3" stroke="{INK}" stroke-width="2"/>'
            + ''.join(f'<rect x="{x-62+i*30}" y="{y-80}" width="6" height="66" fill="{INK}"/>' for i in range(5))
            + f'<path d="M{x-80} {y-80} Q {x} {y-140} {x+80} {y-80} Z" fill="#2FB8A7" stroke="{INK}" stroke-width="2"/>'
            + f'<line x1="{x}" y1="{y-122}" x2="{x}" y2="{y-140}" stroke="{INK}" stroke-width="2"/>')

def huts(x=80, y=300, n=7):
    cols = ["#FF4FA3", "#4FB6FF", "#FFD23F", "#9BE15D", "#A77BFF", "#FF9A3C", "#2FD4C4"]
    return ''.join(f'<rect x="{x+i*56}" y="{y-46}" width="44" height="46" fill="{cols[i%7]}" stroke="{INK}" stroke-width="2"/><path d="M{x+i*56-4} {y-46} L {x+i*56+22} {y-66} L {x+i*56+48} {y-46} Z" fill="#fff" stroke="{INK}" stroke-width="2"/><rect x="{x+i*56+15}" y="{y-28}" width="14" height="28" fill="#fff" opacity=".7"/>' for i in range(n))

def fireworks(pts):
    out = ''
    cols = ["#FFD23F", "#FF4FA3", "#2FD4C4", "#A77BFF"]
    for i, (x, y, r) in enumerate(pts):
        c = cols[i % 4]
        out += ''.join(f'<line x1="{x}" y1="{y}" x2="{x + r*__import__("math").cos(a/6*3.14159)}" y2="{y + r*__import__("math").sin(a/6*3.14159)}" stroke="{c}" stroke-width="3" stroke-linecap="round"/>' for a in range(12))
    return out

def deer(x=850, y=270):
    return (f'<g fill="#8C5A3C" stroke="{INK}" stroke-width="2"><ellipse cx="{x}" cy="{y-46}" rx="40" ry="18"/>'
            f'<rect x="{x-30}" y="{y-34}" width="7" height="34"/><rect x="{x+24}" y="{y-34}" width="7" height="34"/>'
            f'<path d="M{x+30} {y-56} l 20 -30 l 14 4 l -10 30 Z"/></g>'
            f'<path d="M{x+56} {y-86} l -6 -20 M{x+56} {y-86} l 10 -18 M{x+52} {y-98} l -10 -6" stroke="{INK}" stroke-width="3"/>')

def vines(x=650, y=255, rows=6):
    return ''.join(f'<path d="M{x+i*18} {y+i*6} L {x+300+i*18} {y-60+i*6}" stroke="#4E7F3A" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 12"/>' for i in range(rows))

def plane(x=980, y=70):
    return (f'<g transform="translate({x} {y}) rotate(-12)"><ellipse cx="0" cy="0" rx="52" ry="9" fill="#fff" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M-6 0 L -26 -30 L -12 -30 L 14 0 Z M-6 0 L -26 30 L -12 30 L 14 0 Z" fill="#fff" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M-44 0 L -56 -18 L -46 -18 L -36 0 Z" fill="#FF4FA3" stroke="{INK}" stroke-width="2"/></g>')

def viaduct(x=380, y=250, n=9):
    arches = ''.join(f'<path d="M{x+i*50} {y+60} V {y+22} Q {x+i*50+25} {y-4} {x+i*50+50} {y+22} V {y+60}" fill="#D9B48A" stroke="{INK}" stroke-width="2"/>' for i in range(n))
    return f'<rect x="{x}" y="{y-10}" width="{n*50}" height="34" fill="#C99A6B" stroke="{INK}" stroke-width="2"/>' + arches

def label(text, acc):
    return (f'<g transform="translate(40 40)"><rect width="{len(text)*17+70}" height="54" rx="10" fill="#fff" stroke="{INK}" stroke-width="2"/>'
            f'<text x="20" y="22" font-family="Manrope, Arial, sans-serif" font-size="13" font-weight="800" letter-spacing="2" fill="{acc}">GREETINGS FROM</text>'
            f'<text x="20" y="44" font-family="Fraunces, Georgia, serif" font-size="22" fill="{INK}">{text}</text></g>')

SCENES = {
 "horsham": lambda a: sky(a) + sun() + clouds() + hills(base=250) + trees([90, 160, 1120]) + bandstand(380) + church(760) + ground(),
 "crawley": lambda a: sky(a) + sun(900) + plane() + clouds() + hills(("#C9E2A8", "#9ACB86", "#6DAF73"), 260) + lake(560, 292, 520) + trees([120, 210, 980, 1080, 1150]),
 "haywards-heath": lambda a: sky(a) + sun() + clouds() + hills(base=230) + viaduct(330, 205, 11) + train(380, 199, "#3B5B9A") + trees([90, 1110]) + ground("#86BE80", 300),
 "burgess-hill": lambda a: sky(a) + sun(1060) + clouds() + hills(("#CDE5AE", "#A3CF8B", "#74B276"), 240) + windmill(470, 215, "#F7F1E6") + windmill(700, 222, "#1B1712", "#1B1712", .9) + trees([140, 1000]),
 "east-grinstead": lambda a: sky(a) + sun(1080) + clouds() + timber_houses(60, 262, 5) + train(560, 300, "#2E7D4F") + ground("#A9A9A9", 306),
 "worthing": lambda a: sky(a) + sun(980, 70) + clouds() + sea(232) + pier(420, 232, 600) + huts(60, 312, 6),
 "brighton": lambda a: sky(a) + sun(1080, 70) + clouds() + sea(240) + domes(190, 240) + pier(520, 240, 560, True, True),
 "lewes": lambda a: sky(a, night=True) + fireworks([(260, 90, 46), (980, 70, 54), (760, 120, 34)]) + hills(("#3C4A6E", "#2E3B5A", "#22304B"), 270) + castle(560, 215, 1.1) + trees([120, 1060], 290, "#1F3A2E"),
 "south-downs": lambda a: sky(a) + sun(980, 80) + clouds() + hills(("#D3E9B4", "#A8D18F", "#7BB57A"), 240) + castle(330, 255, .7) + deer(820, 300) + trees([1100]),
 "west-sussex-villages": lambda a: sky(a) + sun() + clouds() + hills(base=250) + church(780, 280) + trees([120, 220, 1080]) + bandstand(430, 290) + ground("#86BE80", 300),
 "guildford": lambda a: sky(a) + sun(1060) + clouds() + hills(("#CDE5AE", "#A3CF8B", "#74B276"), 260) + castle(300, 200, .9) + timber_houses(520, 290, 5),
 "reigate": lambda a: sky(a) + sun(980) + clouds() + hills(("#CFE6B0", "#A6D08C", "#77B378"), 230) + windmill(600, 240) + trees([180, 260, 1030, 1110]),
 "dorking": lambda a: sky(a) + sun(1040, 70) + clouds() + '<path d="M0 260 C 200 120, 380 110, 560 200 S 900 260, 1200 230 V 340 H 0 Z" fill="#7FB77E"/>' + vines(640, 300, 7) + trees([150, 230, 300], 220, "#2F6E46") + ground("#6DA96B", 312),
 "surrey-villages": lambda a: sky(a) + plane(980, 70) + clouds() + hills(base=250) + church(330, 285) + trees([600, 680, 1100]) + ground("#86BE80", 300),
 "sussex": lambda a: sky(a) + sun(1080, 70) + clouds() + hills(("#CDE5AE", "#A3CF8B", "#74B276"), 220) + windmill(330, 210, s=.8) + sea(270) + pier(620, 270, 480),
 "surrey": lambda a: sky(a) + sun(1040) + clouds() + hills(("#CFE6B0", "#A6D08C", "#77B378"), 240) + castle(320, 230, .8) + windmill(800, 245, s=.9) + trees([1080, 1150]),
}

def postcard(slug, town, acc):
    body = SCENES[slug](acc) + label(town, acc)
    return (f'<svg class="postcard" viewBox="0 0 {W} {H}" role="img" aria-label="Illustrated postcard of {town}" preserveAspectRatio="xMidYMid slice">'
            f'{body}</svg>')
