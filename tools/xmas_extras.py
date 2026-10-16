# -*- coding: utf-8 -*-
"""Christmas page extras: flying Santa (inline SVG), falling snow, festive styling, Kat's note. Used by build_extra.christmas_holding."""

def santa_svg():
    """Santa in his sleigh pulled by three reindeer (Rudolph in front), flying left to right, with a sparkle trail."""
    def deer(x, y, nose=False, leg=0):
        b = '#8A5A34'; d = '#5E3A1E'
        o = f'<g transform="translate({x},{y})">'
        o += f'<path d="M-30,6 Q-20,{18 + leg} -26,{30 + leg}" stroke="{d}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        o += f'<path d="M-18,8 Q-6,{20 - leg} -12,{32 - leg}" stroke="{d}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        o += f'<path d="M14,8 Q26,{18 - leg} 34,{26 - leg}" stroke="{d}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        o += f'<path d="M20,6 Q34,{14 + leg} 40,{22 + leg}" stroke="{d}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        o += f'<ellipse cx="0" cy="2" rx="34" ry="15" fill="{b}"/><ellipse cx="-4" cy="8" rx="20" ry="7" fill="#C9965E"/>'
        o += f'<path d="M-34,-2 l-9,-6 l4,8Z" fill="{b}"/>'
        o += f'<path d="M24,-4 Q34,-20 40,-26" stroke="{b}" stroke-width="12" fill="none" stroke-linecap="round"/>'
        o += f'<ellipse cx="48" cy="-28" rx="14" ry="9" fill="{b}" transform="rotate(14 48 -28)"/>'
        o += f'<path d="M38,-36 q-4,-16 -14,-22 m10,10 l-10,-2 M44,-37 q4,-16 14,-22 m-8,10 l10,-4" stroke="#6B4423" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
        o += f'<ellipse cx="40" cy="-38" rx="4" ry="7" fill="{b}" transform="rotate(-30 40 -38)"/>'
        o += '<circle cx="47" cy="-31" r="2.2" fill="#1B1B22"/>'
        o += f'<rect x="12" y="-10" width="22" height="5" rx="2.5" fill="#E3243B" transform="rotate(-38 22 -8)"/><circle cx="22" cy="-6" r="3" fill="#FFD24F"/>'
        if nose:
            o += '<circle cx="62" cy="-24" r="12" fill="#FF3B4E" opacity=".35"/><circle cx="61" cy="-25" r="5.5" fill="#FF2A3D"/><circle cx="59.5" cy="-26.5" r="1.6" fill="#fff"/>'
        else:
            o += '<circle cx="61" cy="-25" r="4" fill="#3A2414"/>'
        return o + '</g>'
    trail = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{op}"/>' for x, y, r, c, op in [
        (8, 112, 2, '#FFE7A3', .5), (22, 104, 3, '#FFD24F', .7), (36, 110, 2.2, '#FFF', .6), (48, 100, 3.4, '#FFD24F', .8), (14, 96, 1.8, '#FF7AD9', .6),
        (30, 92, 2.4, '#4FE0FF', .6), (60, 106, 2.6, '#FFF', .8), (70, 96, 2, '#FFD24F', .9)])
    trail += '<path d="M0,118 Q40,96 82,102" stroke="#FFE7A3" stroke-width="3" fill="none" opacity=".45" stroke-dasharray="2 8" stroke-linecap="round"/>'
    sleigh = ('<g transform="translate(78,40)">'
              # sack
              '<path d="M6,34 Q-4,4 18,-2 Q34,-8 38,10 Q44,30 34,40Z" fill="#9A6A3A"/><path d="M14,0 q8,-10 18,-2" stroke="#6B4423" stroke-width="3" fill="none"/>'
              '<rect x="14" y="2" width="12" height="12" rx="2" fill="#2FE08A" transform="rotate(-12 20 8)"/><rect x="26" y="-4" width="10" height="12" rx="2" fill="#4FB6FF" transform="rotate(10 31 2)"/>'
              # Santa
              '<path d="M48,36 Q44,8 62,2 Q80,-2 84,22 L86,40Z" fill="#E3243B"/>'
              '<path d="M60,26 l20,0" stroke="#1B1B22" stroke-width="5"/><rect x="66" y="22" width="8" height="8" rx="1" fill="none" stroke="#FFD24F" stroke-width="2.4"/>'
              '<circle cx="70" cy="-8" r="11" fill="#F6C6A6"/>'
              '<path d="M58,-6 Q60,16 72,14 Q84,12 82,-6 Q76,2 70,2 Q64,2 58,-6Z" fill="#FFFFFF"/>'
              '<path d="M60,-14 Q66,-36 92,-30 Q80,-26 80,-14Z" fill="#E3243B"/><rect x="58" y="-17" width="24" height="7" rx="3.5" fill="#FFFFFF"/><circle cx="93" cy="-30" r="5" fill="#FFFFFF"/>'
              '<circle cx="74" cy="-9" r="1.6" fill="#1B1B22"/><circle cx="79" cy="-6" r="2.4" fill="#F29A8A"/>'
              '<path d="M80,14 Q94,10 104,4" stroke="#E3243B" stroke-width="9" fill="none" stroke-linecap="round"/><circle cx="106" cy="3" r="5" fill="#1B1B22"/>'
              # sleigh body
              '<path d="M-2,30 L112,30 Q122,30 120,44 Q116,62 92,62 L14,62 Q-8,62 -6,40 Q-6,30 -2,30Z" fill="#C8102E"/>'
              '<path d="M-2,30 Q-14,26 -16,14 Q-6,18 2,30Z" fill="#C8102E"/>'
              '<path d="M2,38 L112,38" stroke="#FFD24F" stroke-width="3"/><path d="M14,54 Q60,46 104,54" stroke="#FFD24F" stroke-width="2.4" fill="none"/>'
              '<circle cx="58" cy="50" r="5" fill="#FFD24F"/>'
              '<path d="M18,62 L16,72 M92,62 L94,72" stroke="#B8892E" stroke-width="4"/>'
              '<path d="M-4,74 L116,74 Q136,74 134,58" stroke="#E2BE7A" stroke-width="5" fill="none" stroke-linecap="round"/>'
              '</g>')
    reins = '<path d="M180,64 Q210,54 236,58 Q268,50 300,54 Q332,46 362,50" stroke="#E2BE7A" stroke-width="2" fill="none"/>'
    deers = deer(240, 84, leg=4) + deer(318, 74, leg=-4) + deer(396, 64, True, 3)
    return (f'<svg viewBox="0 0 470 140" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">'
            f'{trail}{sleigh}{reins}{deers}</svg>')

def santa_html():
    return f'<div class="santa-fly" aria-hidden="true"><div class="santa-bob">{santa_svg()}</div></div>'

KAT_NOTE = ('<div class="xkat"><figure class="xkat-pic"><img src="../img/g/kat-painting-smile-800.webp" alt="Kat face painting at a party" loading="lazy" width="800" height="533"></figure>'
            '<div class="xkat-tag"><p class="eyebrow">A note from Kat</p><h2>Why I love Christmas</h2>'
            '<p>Christmas is my favourite time of year to paint. I love the excitement: children who can’t sit still because Santa’s on his way, '
            'friends and family getting together, and everyone up for a bit of sparkle.</p>'
            '<p>A little face paint adds to that magic, and seeing a child run off to show their friends their new design never gets old. '
            'I can’t wait to be part of your Christmas celebrations.</p>'
            '<p class="xkat-sign">Kat x</p></div></div>')

FONT = '<link href="https://fonts.googleapis.com/css2?family=Mountains+of+Christmas:wght@700&display=swap" rel="stylesheet">\n'

CSS = '''<style>
/* flying Santa: behind the text, in front of the background */
header.phero{isolation:isolate;clip-path:inset(0)}
.santa-fly{position:fixed;left:0;top:13vh;width:min(420px,62vw);z-index:-1;pointer-events:none;animation:santaFly 26s linear infinite;animation-delay:1.5s;transform:translate(-110%,0)}
header.phero .santa-fly{z-index:1}
.santa-bob{animation:santaBob 2.2s ease-in-out infinite}
.santa-fly svg{display:block;width:100%;height:auto;filter:drop-shadow(0 0 14px rgba(255,214,120,.35))}
@keyframes santaFly{0%{transform:translate(-110%,10vh) rotate(-5deg)}55%{transform:translate(105vw,-6vh) rotate(-5deg)}100%{transform:translate(105vw,-6vh) rotate(-5deg)}}
@keyframes santaBob{0%,100%{translate:0 0}50%{translate:0 -10px}}
/* falling snow over the whole page (tiny, soft, never blocks clicks) */
.xsnow{position:fixed;inset:-10% 0 0 0;z-index:5;pointer-events:none;
  background-image:radial-gradient(3px 3px at 20px 30px,#fff 60%,transparent 61%),radial-gradient(2px 2px at 120px 80px,#fff 60%,transparent 61%),radial-gradient(4px 4px at 200px 160px,rgba(255,255,255,.9) 60%,transparent 61%),radial-gradient(2.5px 2.5px at 290px 40px,#fff 60%,transparent 61%),radial-gradient(3px 3px at 340px 220px,rgba(255,255,255,.8) 60%,transparent 61%),
  radial-gradient(2px 2px at 60px 260px,#fff 60%,transparent 61%),radial-gradient(3.5px 3.5px at 160px 330px,rgba(255,255,255,.85) 60%,transparent 61%);
  background-size:380px 380px;opacity:.55;animation:xsnow 18s linear infinite}
.xsnow.s2{background-size:260px 260px;opacity:.35;animation-duration:12s;background-position:90px 40px}
@keyframes xsnow{from{transform:translateY(-380px)}to{transform:translateY(0)}}
@media(prefers-reduced-motion:reduce){.santa-fly,.xsnow{display:none}}
/* festive styling */
.phero h1,.lg h2{font-family:'Mountains of Christmas','Fraunces',serif;font-weight:700;letter-spacing:.5px}
.phero h1{font-size:clamp(46px,6.6vw,86px);color:#FFF}
.phero h1 span,.band-light h2{color:#B3122E}
.lg h2{font-size:clamp(36px,4.8vw,58px)}
.band-dark h2{color:#FFE7A3;text-shadow:0 2px 14px rgba(0,0,0,.45)}
.band-dark p,.band-dark .xl-more{text-shadow:0 1px 8px rgba(0,0,0,.55)}
.lg .eyebrow{color:#1F9E5B}.band-dark .eyebrow{color:#7CFF9E}
.band-light{background:#FFFDF8 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cg fill='none' stroke='%23B3122E' stroke-opacity='.06' stroke-width='2' stroke-linecap='round'%3E%3Cpath d='M30 18v24M18 30h24M21 21l18 18M39 21L21 39'/%3E%3Cpath d='M100 88v24M88 100h24M91 91l18 18M109 91l-18 18'/%3E%3C/g%3E%3C/svg%3E")!important;position:relative}
.band-light::before,.band-light::after{content:"";position:absolute;left:0;right:0;height:10px;background:repeating-linear-gradient(-45deg,#C8102E 0 14px,#fff 14px 28px,#1F7A45 28px 42px,#fff 42px 56px)}
.band-light::before{top:0}.band-light::after{bottom:0}
.xprices .fcard{border-top:6px solid #C8102E;position:relative}
.xprices .fcard:nth-child(2){border-top-color:#1F7A45}.xprices .fcard:nth-child(3){border-top-color:#E2BE7A}.xprices .fcard:nth-child(4){border-top-color:#2F7FD4}
.xprices .fcard::before{display:none}
.xprices .fcard::after{content:"";position:absolute;top:-16px;right:14px;width:34px;height:30px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 34 30'%3E%3Cpath d='M17 15C10 4 2 8 3 13c4-1 6 2 4 5 5-1 8 1 10-3z' fill='%231F7A45'/%3E%3Cpath d='M17 15c7-11 15-7 14-2-4-1-6 2-4 5-5-1-8 1-10-3z' fill='%23176237'/%3E%3Ccircle cx='14' cy='19' r='4' fill='%23D7192F'/%3E%3Ccircle cx='20' cy='20' r='4' fill='%23E3243B'/%3E%3Ccircle cx='17' cy='14' r='3.6' fill='%23C8102E'/%3E%3C/svg%3E") center/contain no-repeat}
.xgal figure{background:#fff;padding:8px 8px 0;border-radius:6px;box-shadow:0 14px 30px rgba(0,0,0,.35);transform:rotate(-1.5deg)}
.xgal figure:nth-child(even){transform:rotate(1.5deg)}
.xgal figure img{border-radius:3px}.xgal figcaption{color:#3b3442!important;text-shadow:none;padding:8px 2px 10px;text-align:center;font-weight:600}
.xkat{display:grid;grid-template-columns:minmax(0,360px) minmax(0,1fr);gap:40px;align-items:center;margin-bottom:64px}
.xkat-pic{margin:0;background:#fff;padding:10px 10px 30px;border-radius:6px;transform:rotate(-3deg);box-shadow:0 20px 50px rgba(0,0,0,.45);position:relative}
.xkat-pic::after{content:"";position:absolute;top:-18px;left:50%;width:90px;height:34px;translate:-50% 0;background:rgba(200,16,46,.85);transform:rotate(3deg);border-radius:3px}
.xkat-pic img{display:block;width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;object-position:28% 30%;border-radius:3px}
.xkat-tag{background:rgba(255,253,248,.96);color:#1B1712;border-radius:18px;padding:30px 32px;box-shadow:0 20px 50px rgba(0,0,0,.35);border:3px dashed #C8102E;position:relative}
.xkat-tag h2{color:#B3122E!important;text-shadow:none!important;margin-bottom:10px}
.xkat-tag p{color:#3E352E!important;text-shadow:none!important}.xkat-tag .eyebrow{color:#1F7A45!important}
.xkat-tag .xkat-sign{font-family:'Mountains of Christmas',cursive;font-size:34px;font-weight:700;color:#B3122E!important;margin:6px 0 0}
@media(max-width:760px){.xkat{grid-template-columns:1fr;gap:26px}.xkat-pic{max-width:280px;justify-self:center}.xkat-tag{padding:24px 22px}}
.k-enquire h2{color:#FFE7A3}
</style>
'''

KAT_CHECK = ('<style>'+'''.kat-check{background:#FFF6C9;color:#2A2416;border:3px dashed #E0A100;border-radius:16px;padding:22px 26px;margin:0 0 34px;box-shadow:0 10px 26px -18px rgba(0,0,0,.4)}
.kat-check .kc-h{font-weight:800;font-size:20px;margin:0 0 8px;color:#2A2416}.kat-check .kc-h span{display:inline-block;margin-left:10px;font-size:13px;font-weight:700;background:#E0A100;color:#fff;border-radius:999px;padding:3px 10px;vertical-align:middle}
.kat-check ol{margin:0;padding-left:22px}.kat-check li{margin:6px 0;color:#3E352E}
'''+'</style><div class="kat-check" role="note"><p class="kc-h">For Kat to check <span>Preview only: this box never goes on the live site</span></p>'
             '<ol>'
             '<li><b>Your note</b> (“Why I love Christmas”, below): is it how you’d say it? Change any words you like.</li>'
             '<li><b>Christmas fairs:</b> do you run a stall where families pay per face, or only a set fee?</li>'
             '<li><b>Santa’s grottos:</b> would you paint alongside a grotto at garden centres, farms or community events?</li>'
             '<li><b>New Year’s Eve:</b> do you take NYE bookings?</li>'
             '<li><b>Office Christmas parties:</b> would you offer a kids’ corner at family work events?</li>'
             '<li><b>Your Christmas designs:</b> which do you actually paint? For example reindeer, Rudolph, elves, snowmen, gingerbread, Christmas puddings, candy canes, Christmas trees, snow queens. Then I can list them on the page.</li>'
             '<li><b>Photos:</b> any festive photos from last December you’re happy to use?</li>'
             '</ol></div>')

