# Черновые стикеры ведущей Анны (anna_rich) про голдфарм в WoW Forever.
# Референс — assets/wow/anna.jpg: длинные светлые волосы с прямым пробором, круглые очки, эльфийские уши,
# колечко в носу, чёрный чокер, чёрный топ. Мультяшный рисунок (SVG), подпись — плашка в стиле Warcraft.
# python tools/wow_stickers.py [от-до]  → assets/wow/toon/NN_name.png (800×800, прозрачный фон)
import sys, os, asyncio, math, base64
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'wow', 'toon')

DEFS = '''<defs>
<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe6d6"/><stop offset="1" stop-color="#efb79c"/></linearGradient>
<linearGradient id="hair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6dfae"/><stop offset=".5" stop-color="#ddb978"/><stop offset="1" stop-color="#b98f52"/></linearGradient>
<linearGradient id="hair2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9b676"/><stop offset="1" stop-color="#9c7440"/></linearGradient>
<linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b3946"/><stop offset="1" stop-color="#121218"/></linearGradient>
<linearGradient id="sleeve" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#34323e"/><stop offset="1" stop-color="#16161c"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff1a6"/><stop offset=".45" stop-color="#ffcc33"/><stop offset="1" stop-color="#c47a00"/></linearGradient>
<linearGradient id="bronze" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d38a"/><stop offset="1" stop-color="#8a5a1c"/></linearGradient>
<linearGradient id="green" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b6ff8a"/><stop offset="1" stop-color="#1e9e2e"/></linearGradient>
<linearGradient id="red" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff6b5b"/><stop offset="1" stop-color="#a3121e"/></linearGradient>
<linearGradient id="dark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4a58"/><stop offset="1" stop-color="#16161c"/></linearGradient>
<linearGradient id="grey" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d4d4d8"/><stop offset="1" stop-color="#7c7c86"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c98a4a"/><stop offset="1" stop-color="#6e3f18"/></linearGradient>
<linearGradient id="sack" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8b07a"/><stop offset="1" stop-color="#8a5f30"/></linearGradient>
<linearGradient id="linen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf3df"/><stop offset="1" stop-color="#cdb98f"/></linearGradient>
<linearGradient id="arcane" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3c8ff"/><stop offset="1" stop-color="#8a2be2"/></linearGradient>
<linearGradient id="parch" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbeac4"/><stop offset="1" stop-color="#d9b77a"/></linearGradient>
<linearGradient id="plate" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2614"/><stop offset="1" stop-color="#140c06"/></linearGradient>
<radialGradient id="glowA" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".35" stop-color="#d79bff" stop-opacity=".8"/><stop offset="1" stop-color="#8a2be2" stop-opacity="0"/></radialGradient>
<radialGradient id="glowG" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#eaffd8" stop-opacity=".95"/><stop offset=".4" stop-color="#5cff5c" stop-opacity=".55"/><stop offset="1" stop-color="#1eff00" stop-opacity="0"/></radialGradient>
<filter id="hl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="cut" x="-20%" y="-20%" width="140%" height="140%">
  <feMorphology in="SourceAlpha" operator="dilate" radius="16" result="d"/>
  <feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/>
  <feGaussianBlur in="d" stdDeviation="9" result="b"/><feOffset in="b" dy="8" result="o"/>
  <feFlood flood-color="#000" flood-opacity=".32"/><feComposite in2="o" operator="in" result="s"/>
  <feMerge><feMergeNode in="s"/><feMergeNode in="w"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''
HL = lambda cx, cy, rx, ry, o=.7, r=-20: f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff" opacity="{o}" filter="url(#hl)" transform="rotate({r} {cx} {cy})"/>'
INK = '#2a1a12'
L, R = (345, 318), (455, 318)

def eyes(kind):
    def open_(c, dx=0, dy=0, s=1):
        x, y = c
        return (f'<ellipse cx="{x}" cy="{y}" rx="{24*s}" ry="{28*s}" fill="#fff"/>'
                f'<circle cx="{x+dx}" cy="{y+4+dy}" r="{17*s}" fill="#3d4a5c"/><circle cx="{x+dx}" cy="{y+4+dy}" r="{9*s}" fill="#0c0f16"/>'
                f'<circle cx="{x+dx+6}" cy="{y-3+dy}" r="{6*s}" fill="#fff"/>'
                # стрелки и длинные ресницы, как на фото
                f'<path d="M{x-28} {y-14} Q{x} {y-34} {x+30} {y-16} L{x+42} {y-24}" stroke="#1a1012" stroke-width="7" fill="none" stroke-linecap="round"/>')
    arc_up = lambda c: f'<path d="M{c[0]-24} {c[1]+8} Q{c[0]} {c[1]-22} {c[0]+24} {c[1]+8}" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    arc_dn = lambda c: f'<path d="M{c[0]-24} {c[1]} Q{c[0]} {c[1]+20} {c[0]+24} {c[1]}" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M{c[0]+20} {c[1]+4} l12 -8" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    if kind == 'open': return open_(L) + open_(R)
    if kind == 'side': return open_(L, 8) + open_(R, 8)
    if kind == 'down': return open_(L, 0, 8) + open_(R, 0, 8)
    if kind == 'up': return open_(L, 2, -9) + open_(R, -2, -9)
    if kind == 'wide': return open_(L, 0, 0, 1.18) + open_(R, 0, 0, 1.18)
    if kind == 'happy': return arc_up(L) + arc_up(R)
    if kind == 'closed': return arc_dn(L) + arc_dn(R)
    if kind == 'wink': return open_(L) + arc_up(R)
    if kind == 'narrow':
        return ''.join(f'<path d="M{x-24} {y} Q{x} {y-10} {x+24} {y}" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="{x}" cy="{y+3}" r="7" fill="{INK}"/>' for x, y in (L, R))
    if kind == 'coin':   # глаза-монетки
        return ''.join(f'<circle cx="{x}" cy="{y+2}" r="24" fill="url(#gold)"/><circle cx="{x}" cy="{y+2}" r="15" fill="none" stroke="#c47a00" stroke-width="4"/>' + HL(x - 8, y - 8, 8, 5, .8) for x, y in (L, R))
    return ''

def brows(kind):
    p = {'normal': ('M316 266 Q345 254 374 262', 'M426 262 Q455 254 484 266'),
         'up': ('M314 248 Q345 232 374 244', 'M426 244 Q455 232 486 248'),
         'angry': ('M318 258 Q345 262 376 276', 'M424 276 Q455 262 482 258'),
         'sad': ('M318 272 Q345 256 372 252', 'M428 252 Q455 256 482 272'),
         'smug': ('M316 266 Q345 256 374 264', 'M426 252 Q455 240 484 252')}[kind]
    return ''.join(f'<path d="{d}" stroke="#9a7246" stroke-width="10" fill="none" stroke-linecap="round"/>' for d in p)

LIP = '#c06a6e'
def mouth(kind):
    if kind == 'grin':
        return ('<path d="M352 392 Q400 396 448 392 Q444 446 400 448 Q356 446 352 392Z" fill="#7a2630"/>'
                '<path d="M358 394 Q400 398 442 394 L440 408 Q400 412 360 408Z" fill="#fff"/>'
                '<ellipse cx="400" cy="434" rx="22" ry="9" fill="#ef7f86"/>')
    if kind == 'smile': return f'<path d="M364 398 Q400 426 436 398" stroke="{LIP}" stroke-width="11" fill="none" stroke-linecap="round"/>'
    if kind == 'lips': return f'<path d="M372 404 Q386 394 400 400 Q414 394 428 404 Q414 420 400 420 Q386 420 372 404Z" fill="{LIP}"/>' + HL(392, 410, 8, 3, .5, 0)
    if kind == 'smirk': return f'<path d="M370 408 Q404 418 436 394" stroke="{LIP}" stroke-width="11" fill="none" stroke-linecap="round"/>'
    if kind == 'o': return '<ellipse cx="400" cy="414" rx="20" ry="26" fill="#7a2630"/><ellipse cx="400" cy="426" rx="12" ry="8" fill="#ef7f86"/>'
    if kind == 'flat': return f'<path d="M374 410 L426 410" stroke="{LIP}" stroke-width="10" stroke-linecap="round"/>'
    if kind == 'frown': return f'<path d="M368 420 Q400 398 432 420" stroke="{LIP}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    if kind == 'wavy': return f'<path d="M366 412 q11 -10 22 0 t22 0 t22 0" stroke="{LIP}" stroke-width="9" fill="none" stroke-linecap="round"/>'
    if kind == 'tongue': return f'<path d="M368 400 Q400 424 432 400" stroke="{LIP}" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M406 410 Q420 440 436 418 Q432 404 420 406Z" fill="#ef7f86"/>'
    return ''

GLASSES = (''.join(f'<circle cx="{x}" cy="{y+2}" r="47" fill="#dff3ff" fill-opacity=".14" stroke="#b08a4a" stroke-width="6"/>' for x, y in (L, R))
           + '<path d="M392 314 Q400 304 408 314" stroke="#b08a4a" stroke-width="6" fill="none"/>'
           '<path d="M298 312 L262 300 M502 312 L538 300" stroke="#b08a4a" stroke-width="6" stroke-linecap="round"/>'
           + HL(326, 298, 14, 6, .55) + HL(436, 298, 14, 6, .55))
EARS = ('<path d="M262 290 Q214 262 156 176 Q176 290 258 352Z" fill="url(#skin)"/><path d="M250 300 Q214 270 182 222 Q200 290 250 334Z" fill="#e9a58c" opacity=".55"/>'
        '<path d="M538 290 Q586 262 644 176 Q624 290 542 352Z" fill="url(#skin)"/><path d="M550 300 Q586 270 618 222 Q600 290 550 334Z" fill="#e9a58c" opacity=".55"/>')
BACKHAIR = '<path d="M236 300 Q214 110 400 104 Q586 110 564 300 Q590 470 616 660 L184 660 Q210 470 236 300Z" fill="url(#hair2)"/>'
STRANDS = ('<path d="M252 270 Q226 420 252 560 Q236 610 214 660 L162 660 Q196 470 232 300Z" fill="url(#hair)"/>'
           '<path d="M548 270 Q574 420 548 560 Q564 610 586 660 L638 660 Q604 470 568 300Z" fill="url(#hair)"/>')

def head(e, m, b, tilt=0, extra='', glasses=True):
    return (f'<g transform="rotate({tilt} 400 440)">'
            '<rect x="364" y="400" width="72" height="80" rx="30" fill="url(#skin)"/>'
            '<rect x="362" y="440" width="76" height="20" rx="8" fill="#141418"/>'                      # чокер
            + EARS +
            '<ellipse cx="400" cy="304" rx="148" ry="166" fill="url(#skin)"/>'
            '<path d="M250 330 Q230 126 400 116 Q570 126 550 330 Q544 236 474 186 Q436 168 402 176 Q366 168 326 186 Q256 236 250 330Z" fill="url(#hair)"/>'   # пробор
            '<path d="M402 176 Q396 150 404 120" stroke="#b98f52" stroke-width="5" fill="none"/>'
            + HL(330, 170, 50, 14, .5, -25) + HL(470, 170, 50, 14, .45, 25) + STRANDS +
            '<ellipse cx="316" cy="372" rx="26" ry="14" fill="#ff8f98" opacity=".4"/><ellipse cx="484" cy="372" rx="26" ry="14" fill="#ff8f98" opacity=".4"/>'
            '<path d="M394 340 Q398 366 412 362" stroke="#d48f74" stroke-width="7" fill="none" stroke-linecap="round"/>'
            '<path d="M386 368 a7 7 0 1 0 8 -4" stroke="#d9dde6" stroke-width="4" fill="none"/>'      # колечко в носу
            + eyes(e) + brows(b) + mouth(m) + (GLASSES if glasses else '') + extra + '</g>')

TORSO = ('<path d="M168 660 Q160 520 250 474 Q320 448 400 448 Q480 448 550 474 Q640 520 632 660Z" fill="url(#top)"/>'
         '<path d="M356 450 Q400 560 444 450Z" fill="url(#skin)"/>'
         '<path d="M370 466 Q400 540 430 466" stroke="#e8c27a" stroke-width="3" fill="none"/>'        # цепочка
         + HL(260, 520, 50, 20, .18, -30))

def arm(sh, hand, elbow=None, fist=False, palm=False, skip_hand=False):
    sx, sy = sh; hx, hy = hand
    ex, ey = elbow if elbow else ((sx + hx) / 2 + (40 if sx > 400 else -40), (sy + hy) / 2 + 30)
    d = f'M{sx} {sy} Q{ex} {ey} {hx} {hy}'
    s = (f'<path d="{d}" stroke="#0e0e12" stroke-width="74" fill="none" stroke-linecap="round"/>'
         f'<path d="{d}" stroke="url(#sleeve)" stroke-width="60" fill="none" stroke-linecap="round"/>')
    if not skip_hand:
        s += f'<circle cx="{hx}" cy="{hy}" r="{40 if fist else 42}" fill="url(#skin)"/>' + HL(hx - 12, hy - 14, 12, 8, .5)
        if palm: s += f'<path d="M{hx-26} {hy-30} l-6 -26 M{hx-8} {hy-38} l-2 -28 M{hx+12} {hy-36} l4 -26 M{hx+28} {hy-24} l10 -20" stroke="url(#skin)" stroke-width="20" stroke-linecap="round"/>'
    return s
LS, RS = (232, 520), (568, 520)

def plate(text):
    n = len(text); fs = 66
    while n * fs * .72 + 110 > 760: fs -= 2
    w = n * fs * .72 + 110; h = fs + 50; y = 636
    return (f'<g transform="rotate(-3 400 690)"><rect x="{400-w/2}" y="{y}" width="{w}" height="{h}" rx="18" fill="url(#plate)" stroke="url(#bronze)" stroke-width="9"/>'
            f'<rect x="{400-w/2+12}" y="{y+12}" width="{w-24}" height="{h-24}" rx="10" fill="none" stroke="#c9a14a" stroke-width="2" opacity=".6"/>'
            + ''.join(f'<path d="M{x} {y+h/2-14} l14 14 l-14 14 l-14 -14Z" fill="url(#gold)"/>' for x in (400 - w / 2, 400 + w / 2)) +
            f'<text x="400" y="{y+h/2+fs*.34}" text-anchor="middle" font-family="Aleg" font-weight="900" font-size="{fs}" fill="#ffd100" stroke="#2a1404" stroke-width="3" paint-order="stroke" letter-spacing="1">{text}</text></g>')

coin = lambda x, y, r=30: (f'<circle cx="{x}" cy="{y+r*.12}" r="{r}" fill="#9a5d00"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#gold)"/>'
                           f'<circle cx="{x}" cy="{y}" r="{r*.66}" fill="none" stroke="#c98612" stroke-width="{max(3, r*.12):.0f}"/>' + HL(x - r*.35, y - r*.4, r*.3, r*.2, .8))
def coins(pts): return ''.join(coin(*p) for p in pts)
txt = lambda x, y, t, fs=40, c='#fff', w=900, f='Aleg': f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{f}" font-weight="{w}" font-size="{fs}" fill="{c}" stroke="#2a1404" stroke-width="{fs/18:.1f}" paint-order="stroke">{t}</text>'
def sack(x, y, s=1, spill=True):
    g = (f'<g transform="translate({x} {y}) scale({s})"><path d="M-110 -40 Q-150 120 -60 150 L60 150 Q150 120 110 -40 Q60 -70 0 -66 Q-60 -70 -110 -40Z" fill="url(#sack)"/>'
         '<path d="M-60 -60 Q-80 -110 -40 -120 L40 -120 Q80 -110 60 -60" fill="url(#sack)"/><path d="M-66 -62 Q0 -40 66 -62" stroke="#6a4420" stroke-width="12" fill="none" stroke-linecap="round"/>'
         + coins([(-30, -126, 26), (20, -132, 24), (-4, -150, 22)]) + HL(-60, 10, 24, 50, .35, 10) + '</g>')
    return g
def staff(x1, y1, x2, y2, orb=True):
    return (f'<path d="M{x1} {y1} L{x2} {y2}" stroke="url(#wood)" stroke-width="22" stroke-linecap="round"/>'
            + (f'<circle cx="{x2}" cy="{y2}" r="90" fill="url(#glowA)"/><circle cx="{x2}" cy="{y2}" r="32" fill="url(#arcane)"/>' + HL(x2 - 10, y2 - 12, 10, 7, .9) if orb else ''))
def burst(x, y, r=150, c='#c77dff'):
    pts = ' '.join(f'{x + math.cos(a) * (r if k % 2 == 0 else r * .55):.0f},{y + math.sin(a) * (r if k % 2 == 0 else r * .55):.0f}' for k, a in enumerate(math.pi * 2 * i / 20 for i in range(20)))
    return f'<polygon points="{pts}" fill="{c}" opacity=".85"/><circle cx="{x}" cy="{y}" r="{r*.45}" fill="url(#glowA)"/>'
def mob(x, y, s=1, rot=0):   # разбойник Братства: красная маска-бандана
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><circle cx="0" cy="0" r="54" fill="#e9b08c"/>'
            '<path d="M-56 -6 Q0 -30 56 -6 L52 28 Q0 46 -52 28Z" fill="url(#red)"/><path d="M-54 -14 Q0 -70 54 -14 Q0 -36 -54 -14Z" fill="#7a1018"/>'
            '<circle cx="-18" cy="-8" r="7" fill="#1a0a06"/><circle cx="18" cy="-8" r="7" fill="#1a0a06"/><path d="M-30 -22 L-8 -14 M30 -22 L8 -14" stroke="#1a0a06" stroke-width="6" stroke-linecap="round"/></g>')
def bolt(x, y, rot=0):   # рулон льняной ткани
    return (f'<g transform="rotate({rot} {x} {y})"><rect x="{x-80}" y="{y-34}" width="160" height="68" rx="20" fill="url(#linen)"/>'
            f'<ellipse cx="{x+80}" cy="{y}" rx="20" ry="34" fill="#efe2c2"/><ellipse cx="{x+80}" cy="{y}" rx="8" ry="14" fill="#c8b48a"/>'
            f'<path d="M{x-50} {y-34} L{x-50} {y+34} M{x+30} {y-34} L{x+30} {y+34}" stroke="#b8a273" stroke-width="5"/>' + HL(x - 30, y - 18, 30, 8, .7, 0) + '</g>')
def crate(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-90" y="-80" width="180" height="160" rx="12" fill="url(#wood)"/>'
            '<path d="M-90 -80 L90 80 M90 -80 L-90 80" stroke="#5a3210" stroke-width="12"/><rect x="-90" y="-80" width="180" height="160" rx="12" fill="none" stroke="#5a3210" stroke-width="12"/>'
            '<rect x="-24" y="-20" width="48" height="40" rx="6" fill="url(#gold)"/>' + HL(-50, -50, 30, 10, .4, 0) + '</g>')
def hourglass(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-80" y="-130" width="160" height="26" rx="10" fill="url(#wood)"/><rect x="-80" y="104" width="160" height="26" rx="10" fill="url(#wood)"/>'
            '<path d="M-60 -104 L60 -104 Q60 -30 8 0 Q60 30 60 104 L-60 104 Q-60 30 -8 0 Q-60 -30 -60 -104Z" fill="#dff3ff" fill-opacity=".7" stroke="#b08a4a" stroke-width="6"/>'
            '<path d="M-40 -70 L40 -70 Q30 -24 0 -6 Q-30 -24 -40 -70Z M-50 100 Q0 40 50 100Z" fill="url(#gold)"/><path d="M0 -6 L0 70" stroke="#ffcc33" stroke-width="5" stroke-dasharray="8 6"/></g>')
def scroll(x, y, w=260, h=200, rot=0, inner=''):
    return (f'<g transform="rotate({rot} {x} {y})"><rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="8" fill="url(#parch)"/>'
            f'<rect x="{x-w/2-16}" y="{y-h/2-14}" width="{w+32}" height="28" rx="14" fill="url(#wood)"/><rect x="{x-w/2-16}" y="{y+h/2-14}" width="{w+32}" height="28" rx="14" fill="url(#wood)"/>{inner}</g>')
def bin_(x, y):
    return (f'<path d="M{x-80} {y-60} L{x+80} {y-60} L{x+64} {y+110} L{x-64} {y+110}Z" fill="url(#grey)"/><rect x="{x-96}" y="{y-86}" width="192" height="30" rx="12" fill="url(#dark)"/>'
            f'<path d="M{x-36} {y-30} L{x-30} {y+86} M{x} {y-30} L{x} {y+86} M{x+36} {y-30} L{x+30} {y+86}" stroke="#5a5a66" stroke-width="8" stroke-linecap="round"/>')
def gem(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="0" r="110" fill="url(#glowG)"/>'
            '<path d="M0 -70 L50 -20 L30 60 L-30 60 L-50 -20Z" fill="url(#green)"/><path d="M0 -70 L0 60 M-50 -20 L50 -20" stroke="#d9ffc8" stroke-width="4" opacity=".7"/>' + HL(-16, -30, 10, 18, .9, 0) + '</g>')
def sword(x, y, rot=0, c='url(#green)'):
    return (f'<g transform="rotate({rot} {x} {y})"><path d="M{x} {y-210} L{x+22} {y-170} L{x+18} {y+20} L{x-18} {y+20} L{x-22} {y-170}Z" fill="url(#grey)"/>'
            f'<path d="M{x} {y-200} L{x} {y+10}" stroke="#fff" stroke-width="4" opacity=".6"/><rect x="{x-62}" y="{y+18}" width="124" height="24" rx="10" fill="{c}"/>'
            f'<rect x="{x-12}" y="{y+40}" width="24" height="70" rx="6" fill="url(#wood)"/><circle cx="{x}" cy="{y+118}" r="16" fill="url(#gold)"/></g>')
heart = lambda x, y, s=1, c='url(#red)': f'<path transform="translate({x} {y}) scale({s})" d="M0 30 C-60 -10 -50 -70 0 -40 C50 -70 60 -10 0 30Z" fill="{c}"/>'
def bread(x, y):
    return (f'<ellipse cx="{x}" cy="{y}" rx="110" ry="62" fill="url(#bronze)"/><path d="M{x-60} {y-34} q14 26 0 52 M{x-10} {y-44} q14 30 0 66 M{x+40} {y-38} q14 26 0 56" stroke="#8a5a1c" stroke-width="8" fill="none" stroke-linecap="round"/>'
            + HL(x - 40, y - 30, 40, 12, .6, -10))
qm = lambda x, y, fs=110, c='#ffd100': txt(x, y, '?', fs, c)
xm = lambda x, y, fs=110, c='#ffd100': txt(x, y, '!', fs, c)
def bar(x, y, w, pct, label=''):
    return (f'<rect x="{x-w/2}" y="{y-28}" width="{w}" height="56" rx="12" fill="url(#plate)" stroke="url(#bronze)" stroke-width="6"/>'
            f'<rect x="{x-w/2+10}" y="{y-18}" width="{(w-20)*pct}" height="36" rx="8" fill="#8a2be2"/><rect x="{x-w/2+10}" y="{y-18}" width="{(w-20)*pct}" height="14" rx="7" fill="#c78bff" opacity=".7"/>'
            + (txt(x, y + 13, label, 36, '#fff') if label else ''))

S = []
def st(n, name, cap, e, m, b, back='', front='', arms='', tilt=0, face=''):
    S.append((n, name, cap, f'<g filter="url(#cut)">{back}{BACKHAIR}{TORSO}{head(e, m, b, tilt, face)}{arms}{front}</g>{plate(cap)}'))

st(1, 'rich', 'Я БОГАТА!', 'coin', 'grin', 'up',
   arms=arm(LS, (190, 220), (160, 380), palm=True) + arm(RS, (610, 220), (640, 380), palm=True),
   back=coins([(150, 120, 34), (650, 110, 30), (110, 300, 26), (700, 290, 28), (250, 60, 24), (560, 50, 22)]))
st(2, 'loot', 'ЛУТ ПОШЁЛ', 'happy', 'grin', 'up', front=sack(600, 520, .95),
   arms=arm(RS, (560, 470), (620, 560)) + arm(LS, (190, 320), (160, 450), fist=True))
st(3, 'respawn', 'УЖЕ РЕСПАВН?!', 'wide', 'o', 'up',
   back=mob(140, 200, .9, -14) + mob(660, 180, .9, 12) + mob(700, 400, .75, 18),
   arms=arm(LS, (290, 300), (190, 440), palm=True) + arm(RS, (510, 300), (610, 440), palm=True))
st(4, 'secret', 'ТССС… ТОЧКА', 'wink', 'lips', 'smug',
   arms=arm(RS, (420, 420), (560, 560)),
   front='<path d="M420 430 L420 360" stroke="url(#skin)" stroke-width="28" stroke-linecap="round"/>' + HL(412, 372, 6, 14, .6, 0)
         + scroll(640, 250, 200, 150, 12, '<path d="M590 220 q30 40 70 10 t60 30" stroke="#8a5a1c" stroke-width="6" fill="none" stroke-dasharray="12 10"/>' + txt(690, 285, '✕', 60, '#c8102e')))
st(5, 'bags', 'СУМКИ ПОЛНЫЕ', 'wide', 'wavy', 'sad',
   arms=arm(LS, (300, 560), (210, 640)) + arm(RS, (500, 560), (590, 640)),
   front=sack(400, 560, 1.15) + bolt(250, 470, -20) + coin(560, 420, 26),
   back='<path d="M560 200 q12 30 0 50 q-14 -22 0 -50Z" fill="#8fd3ff"/>')
st(6, 'boom', 'БАБАХ!', 'narrow', 'grin', 'angry', back=burst(400, 250, 330, '#b56cff'),
   arms=arm(RS, (620, 300), (660, 450)), front=staff(640, 560, 640, 180))
st(7, 'nobody', 'А ГДЕ ВСЕ?', 'side', 'frown', 'up',
   arms=arm(RS, (560, 300), (640, 420)),
   front='<path d="M540 300 L610 300" stroke="url(#skin)" stroke-width="30" stroke-linecap="round"/>' + qm(160, 260) + qm(680, 180, 80))
st(8, 'eat', 'ПОРА ПОЕСТЬ', 'happy', 'tongue', 'normal',
   arms=arm(LS, (300, 560), (210, 640)) + arm(RS, (500, 560), (590, 640)), front=bread(400, 560),
   back='<path d="M630 230 l0 -40 M660 230 l0 -50 M690 230 l0 -40" stroke="#ffd1a0" stroke-width="10" stroke-linecap="round" opacity=".8"/>')
st(9, 'trash', 'СЕРОЕ — В МУСОР', 'narrow', 'smirk', 'smug', back=bin_(640, 420),
   arms=arm(RS, (600, 300), (660, 420)),
   front=f'<g transform="rotate(30 610 280)">{sword(610, 330, 0, "url(#grey)")}</g>')
st(10, 'linen', 'ЛЁН РЕКОЙ', 'happy', 'grin', 'up',
   arms=arm(LS, (300, 560), (210, 640)) + arm(RS, (500, 560), (590, 640)),
   front=bolt(400, 560, -6) + bolt(400, 490, 8) + bolt(170, 250, -30) + bolt(640, 210, 25))
st(11, 'lvlup', 'ЛЕВЕЛ АП!', 'happy', 'grin', 'up',
   front=bar(400, 70, 540, .9, 'УР. 15') + '<path d="M690 40 l20 -36 l20 36" stroke="#ffd100" stroke-width="14" fill="none" stroke-linecap="round"/>',
   arms=arm(LS, (190, 300), (160, 430), fist=True) + arm(RS, (610, 300), (640, 430), fist=True),
   back='<circle cx="400" cy="300" r="330" fill="url(#glowA)" opacity=".55"/>')
st(12, 'forbidden', 'ЗАПРЕТНО', 'wink', 'smirk', 'smug',
   arms=arm(RS, (560, 470), (620, 560)),
   front=scroll(600, 420, 200, 230, 8, txt(600, 400, 'МЕТОДЫ', 34, '#5a3210', 900) + txt(600, 444, 'ФАРМА', 34, '#5a3210', 900)
         + '<circle cx="640" cy="500" r="42" fill="url(#red)"/><circle cx="640" cy="500" r="28" fill="none" stroke="#7a0c14" stroke-width="5"/><path d="M630 492 l20 16 M650 492 l-20 16" stroke="#7a0c14" stroke-width="6" stroke-linecap="round"/>'))
st(13, 'green', 'ЗЕЛЁНКА!', 'up', 'grin', 'up', back=gem(630, 200, 1.1),
   arms=arm(RS, (600, 320), (660, 440)), front=sword(170, 360, -14))
st(14, 'crate', 'ЯЩИК!', 'wide', 'o', 'up', front=crate(400, 560, 1.15),
   arms=arm(LS, (300, 520), (220, 600)) + arm(RS, (500, 520), (580, 600)),
   back=xm(150, 220) + xm(660, 200, 90))
st(15, 'easy', 'ИЗИ ГОЛД', 'narrow', 'smirk', 'smug',
   arms=arm(RS, (560, 470), (620, 560)) + arm(LS, (190, 340), (150, 460)),
   back=coins([(140, 260, 30), (180, 190, 26), (120, 140, 22)]),
   front=coin(600, 420, 44))
st(16, 'come', 'ИДИ СЮДА!', 'narrow', 'grin', 'angry',
   back=mob(660, 200, 1.1, 10),
   arms=arm(LS, (230, 400), (150, 520), fist=True) + arm(RS, (570, 400), (650, 520), fist=True),
   front='<path d="M120 200 l40 30 M680 360 l-40 -10" stroke="#ffcc33" stroke-width="14" stroke-linecap="round"/>')
st(17, 'map', 'ВОТ ТУТ', 'down', 'smile', 'normal',
   arms=arm(LS, (300, 560), (210, 640)) + arm(RS, (500, 560), (590, 640)),
   front=scroll(400, 560, 320, 160, 0, '<path d="M270 540 q60 -40 120 0 t110 -10" stroke="#8a5a1c" stroke-width="6" fill="none" stroke-dasharray="12 10"/>'
         '<path d="M300 600 q40 -20 90 0" stroke="#6e9a5a" stroke-width="16" fill="none" opacity=".6"/>' + txt(500, 560, '✕', 60, '#c8102e')))
st(18, 'sub', 'ПОДПИШИСЬ', 'happy', 'smile', 'up',
   arms=arm(LS, (360, 470), (240, 600)) + arm(RS, (440, 470), (560, 600)),
   front=heart(400, 480, 1.5) + heart(170, 200, .8, 'url(#gold)') + heart(640, 170, .7) + heart(680, 330, .5, 'url(#gold)'))
st(19, 'timer', '10 СЕКУНД', 'wide', 'o', 'up', back=hourglass(640, 250, 1),
   arms=arm(LS, (190, 300), (160, 430), palm=True))
st(20, 'gg', 'ГГ, ФАРМИМ', 'happy', 'grin', 'up',
   arms=arm(RS, (620, 300), (660, 450)) + arm(LS, (190, 300), (160, 430), fist=True), front=staff(640, 560, 640, 180),
   back=coins([(140, 150, 30), (230, 80, 24)]))

FONT = ''.join('@font-face{font-family:%s;src:url(data:font/ttf;base64,%s);font-weight:%s}' % (n, base64.b64encode(open(os.path.join(ROOT, 'assets/fonts', f), 'rb').read()).decode(), w)
               for n, f, w in (('Aleg', 'AlegreyaSC-Black.ttf', '900'),))
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 800, 'height': 800})
        lo, hi = (map(int, sys.argv[1].split('-')) if len(sys.argv) > 1 else (1, 99))
        for n, name, cap, body in S:
            if not lo <= n <= hi: continue
            html = f'<html><head><style>{FONT}html,body{{margin:0;background:transparent}}</style></head><body><svg width="800" height="800" viewBox="0 0 800 800">{DEFS}{body}</svg></body></html>'
            await pg.set_content(html); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(80)
            await pg.screenshot(path=os.path.join(OUT, f'{n:02d}_{name}.png'), omit_background=True)
        await b.close()
asyncio.run(main()); print(len(S), 'стикеров →', OUT)
