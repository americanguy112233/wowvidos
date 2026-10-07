# Черновые 3D-«пластилиновые» стикеры автора ИИ-блога (персонаж условный, без сходства).
# python tools/ai_stickers.py [от-до, напр. 21-40]  → assets/ai/toon/NN_name.png (800×800, прозрачный фон) + preview
import sys, os, asyncio, math
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'ai', 'toon')

DEFS = '''<defs>
<linearGradient id="skin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe0c8"/><stop offset="1" stop-color="#e9a27e"/></linearGradient>
<linearGradient id="hair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b4a33"/><stop offset="1" stop-color="#2e1e14"/></linearGradient>
<linearGradient id="shirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fe0d6"/><stop offset="1" stop-color="#1f9c94"/></linearGradient>
<linearGradient id="shirt2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5fcfc4"/><stop offset="1" stop-color="#16857e"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe27a"/><stop offset="1" stop-color="#e09a12"/></linearGradient>
<linearGradient id="green" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9be89b"/><stop offset="1" stop-color="#2c9a52"/></linearGradient>
<linearGradient id="red" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a86"/><stop offset="1" stop-color="#c8102e"/></linearGradient>
<linearGradient id="dark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4a58"/><stop offset="1" stop-color="#16161c"/></linearGradient>
<linearGradient id="white" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#dcd6cc"/></linearGradient>
<linearGradient id="bot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9f1ff"/><stop offset="1" stop-color="#8fa6d6"/></linearGradient>
<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9a466"/><stop offset="1" stop-color="#93592a"/></linearGradient>
<linearGradient id="leaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8be08a"/><stop offset="1" stop-color="#1f7a43"/></linearGradient>
<linearGradient id="screen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b3550"/><stop offset="1" stop-color="#121826"/></linearGradient>
<filter id="hl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="cut" x="-20%" y="-20%" width="140%" height="140%">
  <feMorphology in="SourceAlpha" operator="dilate" radius="16" result="d"/>
  <feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/>
  <feGaussianBlur in="d" stdDeviation="9" result="b"/><feOffset in="b" dy="8" result="o"/>
  <feFlood flood-color="#000" flood-opacity=".28"/><feComposite in2="o" operator="in" result="s"/>
  <feMerge><feMergeNode in="s"/><feMergeNode in="w"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''
HL = lambda cx, cy, rx, ry, o=.7, r=-20: f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff" opacity="{o}" filter="url(#hl)" transform="rotate({r} {cx} {cy})"/>'
INK = '#2a1a12'

def eyes(kind):
    L, R = (345, 318), (455, 318)
    def open_(c, dx=0, dy=0, s=1):
        x, y = c
        return (f'<ellipse cx="{x}" cy="{y}" rx="{24*s}" ry="{29*s}" fill="#fff"/>'
                f'<circle cx="{x+dx}" cy="{y+4+dy}" r="{17*s}" fill="#4a2b18"/><circle cx="{x+dx}" cy="{y+4+dy}" r="{9*s}" fill="#120a06"/>'
                f'<circle cx="{x+dx+6}" cy="{y-3+dy}" r="{6*s}" fill="#fff"/>')
    arc_up = lambda c: f'<path d="M{c[0]-24} {c[1]+8} Q{c[0]} {c[1]-22} {c[0]+24} {c[1]+8}" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    arc_dn = lambda c: f'<path d="M{c[0]-24} {c[1]} Q{c[0]} {c[1]+20} {c[0]+24} {c[1]}" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/>'
    if kind == 'open': return open_(L) + open_(R)
    if kind == 'side': return open_(L, 8) + open_(R, 8)
    if kind == 'down': return open_(L, 0, 8) + open_(R, 0, 8)
    if kind == 'up': return open_(L, 2, -9) + open_(R, -2, -9)
    if kind == 'wide': return open_(L, 0, 0, 1.18) + open_(R, 0, 0, 1.18)
    if kind == 'happy': return arc_up(L) + arc_up(R)
    if kind == 'closed': return arc_dn(L) + arc_dn(R)
    if kind == 'wink': return open_(L) + arc_up(R)
    if kind == 'cool':
        return ('<path d="M300 296 L500 296 L494 340 Q470 362 438 344 L420 316 L380 316 L362 344 Q330 362 306 340Z" fill="url(#dark)"/>'
                '<path d="M300 300 L250 290 M500 300 L550 290" stroke="#16161c" stroke-width="8" stroke-linecap="round"/>' + HL(340, 312, 18, 6, .6) + HL(458, 312, 18, 6, .6))
    if kind == 'narrow':
        return ''.join(f'<path d="M{x-24} {y} Q{x} {y-10} {x+24} {y}" stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="{x}" cy="{y+3}" r="7" fill="{INK}"/>' for x, y in (L, R))
    return ''

def brows(kind):
    p = {'normal': ('M318 270 Q345 258 372 266', 'M428 266 Q455 258 482 270'),
         'up': ('M316 252 Q345 236 372 248', 'M428 248 Q455 236 484 252'),
         'angry': ('M318 262 Q345 266 374 280', 'M426 280 Q455 266 482 262'),
         'sad': ('M318 276 Q345 260 372 256', 'M428 256 Q455 260 482 276'),
         'smug': ('M318 270 Q345 260 372 268', 'M428 256 Q455 244 482 256')}[kind]
    return ''.join(f'<path d="{d}" stroke="#3a2416" stroke-width="12" fill="none" stroke-linecap="round"/>' for d in p)

def mouth(kind):
    if kind == 'grin':
        return ('<path d="M352 392 Q400 396 448 392 Q444 446 400 448 Q356 446 352 392Z" fill="#7a1e24"/>'
                '<path d="M358 394 Q400 398 442 394 L440 408 Q400 412 360 408Z" fill="#fff"/>'
                '<ellipse cx="400" cy="434" rx="22" ry="9" fill="#ef6f7a"/>')
    if kind == 'smile': return '<path d="M362 398 Q400 428 438 398" stroke="#7a1e24" stroke-width="10" fill="none" stroke-linecap="round"/>'
    if kind == 'smirk': return '<path d="M368 408 Q404 418 436 394" stroke="#7a1e24" stroke-width="10" fill="none" stroke-linecap="round"/>'
    if kind == 'o': return '<ellipse cx="400" cy="414" rx="20" ry="26" fill="#7a1e24"/><ellipse cx="400" cy="426" rx="12" ry="8" fill="#ef6f7a"/>'
    if kind == 'flat': return '<path d="M374 410 L426 410" stroke="#7a1e24" stroke-width="10" stroke-linecap="round"/>'
    if kind == 'frown': return '<path d="M368 420 Q400 398 432 420" stroke="#7a1e24" stroke-width="10" fill="none" stroke-linecap="round"/>'
    if kind == 'wavy': return '<path d="M366 412 q11 -10 22 0 t22 0 t22 0" stroke="#7a1e24" stroke-width="9" fill="none" stroke-linecap="round"/>'
    if kind == 'sleep': return '<ellipse cx="400" cy="412" rx="12" ry="9" fill="#7a1e24"/>'
    return ''

def head(e, m, b, tilt=0, extra=''):
    return (f'<g transform="rotate({tilt} 400 440)">'
            '<rect x="364" y="400" width="72" height="80" rx="30" fill="url(#skin)"/>'
            '<ellipse cx="252" cy="318" rx="30" ry="40" fill="url(#skin)"/><ellipse cx="548" cy="318" rx="30" ry="40" fill="url(#skin)"/>'
            '<ellipse cx="400" cy="304" rx="150" ry="166" fill="url(#skin)"/>'
            '<path d="M252 300 Q236 150 400 128 Q564 150 548 300 Q536 236 488 214 Q470 240 430 226 Q400 244 360 222 Q318 238 300 214 Q262 240 252 300Z" fill="url(#hair)"/>'
            '<path d="M330 150 Q420 96 500 160 Q450 140 410 158 Q380 132 330 150Z" fill="url(#hair)"/>'
            + HL(372, 168, 60, 14, .35, -10) +
            '<ellipse cx="318" cy="372" rx="26" ry="15" fill="#ff8f98" opacity=".45"/><ellipse cx="482" cy="372" rx="26" ry="15" fill="#ff8f98" opacity=".45"/>'
            '<path d="M392 344 Q400 368 412 362" stroke="#c97c5c" stroke-width="7" fill="none" stroke-linecap="round"/>'
            + eyes(e) + brows(b) + mouth(m) + HL(330, 236, 50, 22, .45, -25) + extra + '</g>')

TORSO = ('<path d="M168 660 Q160 520 250 474 Q320 448 400 448 Q480 448 550 474 Q640 520 632 660Z" fill="url(#shirt)"/>'
         '<path d="M352 452 L400 532 L448 452" fill="url(#skin)"/><path d="M340 454 L400 540 L460 454" stroke="#f4fffd" stroke-width="10" fill="none" stroke-linejoin="round"/>'
         '<circle cx="400" cy="580" r="7" fill="#f4fffd"/><circle cx="400" cy="626" r="7" fill="#f4fffd"/>' + HL(260, 520, 50, 20, .35, -30))

def arm(sh, hand, elbow=None, fist=False, palm=False, skip_hand=False):
    sx, sy = sh; hx, hy = hand
    ex, ey = elbow if elbow else ((sx + hx) / 2 + (40 if sx > 400 else -40), (sy + hy) / 2 + 30)
    d = f'M{sx} {sy} Q{ex} {ey} {hx} {hy}'
    s = (f'<path d="{d}" stroke="#16857e" stroke-width="74" fill="none" stroke-linecap="round"/>'
         f'<path d="{d}" stroke="url(#shirt2)" stroke-width="60" fill="none" stroke-linecap="round"/>')
    if not skip_hand:
        s += f'<circle cx="{hx}" cy="{hy}" r="{40 if fist else 42}" fill="url(#skin)"/>' + HL(hx - 12, hy - 14, 12, 8, .5)
        if palm: s += f'<path d="M{hx-26} {hy-30} l-6 -26 M{hx-8} {hy-38} l-2 -28 M{hx+12} {hy-36} l4 -26 M{hx+28} {hy-24} l10 -20" stroke="url(#skin)" stroke-width="20" stroke-linecap="round"/>'
    return s

LS, RS = (232, 520), (568, 520)

def plate(text):
    n = len(text); fs = 64
    while n * fs * .9 + 80 > 740: fs -= 2
    w = n * fs * .9 + 80
    return (f'<g transform="rotate(-4 400 690)"><rect x="{400-w/2}" y="640" width="{w}" height="{fs+44}" rx="{(fs+44)/2}" fill="#121212"/>'
            f'<text x="400" y="{640+(fs+44)/2+fs*.36}" text-anchor="middle" font-family="Unb" font-weight="900" font-size="{fs}" fill="#fff" letter-spacing="-1">{text}</text></g>')

coin = lambda x, y, r=30: f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#gold)"/><circle cx="{x}" cy="{y}" r="{r*.68}" fill="none" stroke="#c98612" stroke-width="5"/><text x="{x}" y="{y+r*.36}" text-anchor="middle" font-family="Unb" font-weight="900" font-size="{r}" fill="#b4730a">₽</text>' + HL(x - r*.35, y - r*.4, r*.3, r*.2, .7)
def phone(x, y, w=150, h=250, rot=0, inner=''):
    return (f'<g transform="rotate({rot} {x} {y})"><rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="26" fill="url(#dark)"/>'
            f'<rect x="{x-w/2+10}" y="{y-h/2+12}" width="{w-20}" height="{h-24}" rx="18" fill="url(#screen)"/>{inner}' + HL(x - w/4, y - h/3, 14, 30, .35, 0) + '</g>')
def laptop(x, y, w=380, inner=''):
    h = w * .62
    return (f'<rect x="{x-w/2}" y="{y-h}" width="{w}" height="{h}" rx="20" fill="url(#dark)"/><rect x="{x-w/2+14}" y="{y-h+14}" width="{w-28}" height="{h-28}" rx="10" fill="url(#screen)"/>{inner}'
            f'<path d="M{x-w/2-30} {y} L{x+w/2+30} {y} L{x+w/2+10} {y+26} L{x-w/2-10} {y+26}Z" fill="url(#bot)"/>')
def robot(x, y, s=1, wave=True):
    g = (f'<g transform="translate({x} {y}) scale({s})">'
         '<rect x="-70" y="-10" width="140" height="120" rx="36" fill="url(#bot)"/>'
         '<rect x="-80" y="-130" width="160" height="120" rx="44" fill="url(#bot)"/><rect x="-60" y="-110" width="120" height="76" rx="30" fill="url(#screen)"/>'
         '<circle cx="-24" cy="-72" r="12" fill="#7ff3ff"/><circle cx="24" cy="-72" r="12" fill="#7ff3ff"/><path d="M-16 -50 Q0 -40 16 -50" stroke="#7ff3ff" stroke-width="6" fill="none" stroke-linecap="round"/>'
         '<path d="M0 -130 L0 -162" stroke="#8fa6d6" stroke-width="8"/><circle cx="0" cy="-168" r="12" fill="url(#red)"/>')
    if wave: g += '<path d="M70 20 Q120 0 118 -50" stroke="#8fa6d6" stroke-width="26" fill="none" stroke-linecap="round"/><circle cx="118" cy="-58" r="20" fill="url(#bot)"/>'
    return g + HL(-40, -110, 20, 10, .6) + '</g>'
def bills(x, y, rot=0):
    s = ''.join(f'<g transform="rotate({a} {x} {y+60})"><rect x="{x-46}" y="{y-60}" width="92" height="150" rx="10" fill="url(#green)"/><circle cx="{x}" cy="{y+12}" r="22" fill="#cbf5c8"/><text x="{x}" y="{y+24}" text-anchor="middle" font-family="Unb" font-weight="900" font-size="34" fill="#2c9a52">₽</text></g>' for a in (-36, -18, 0, 18, 36))
    return f'<g transform="rotate({rot} {x} {y})">{s}</g>'
txt = lambda x, y, t, fs=40, c='#fff', w=900: f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Unb" font-weight="{w}" font-size="{fs}" fill="{c}">{t}</text>'
palm_tree = lambda x, y, s=1, f=1: (f'<g transform="translate({x} {y}) scale({s*f} {s})"><path d="M0 0 Q-10 -150 20 -300" stroke="url(#wood)" stroke-width="30" fill="none" stroke-linecap="round"/>'
    + ''.join(f'<path d="M20 -300 Q{dx} {dy} {ex} {ey} Q{(20+ex)/2} {(-300+ey)/2-30} 20 -300Z" fill="url(#leaf)"/>' for dx, dy, ex, ey in ((120, -380, 190, -280), (-80, -380, -150, -270), (60, -420, 40, -420), (140, -300, 170, -200), (-60, -300, -120, -190))) + '</g>')
zzz = '<text x="590" y="170" font-family="Unb" font-weight="900" font-size="64" fill="#7fb7ff">Z</text><text x="640" y="110" font-family="Unb" font-weight="900" font-size="46" fill="#7fb7ff">z</text><text x="676" y="70" font-family="Unb" font-weight="900" font-size="34" fill="#7fb7ff">z</text>'
notif = lambda x, y, t, w=300: f'<g><rect x="{x-w/2}" y="{y-44}" width="{w}" height="88" rx="30" fill="url(#white)"/><circle cx="{x-w/2+44}" cy="{y}" r="24" fill="#ff6b3d"/><text x="{x-w/2+44}" y="{y+10}" text-anchor="middle" font-family="Unb" font-weight="900" font-size="26" fill="#fff">B</text>{txt(x+26, y+14, t, 36, "#1f9c4f")}</g>'

S = []
def st(n, name, cap, e, m, b, back='', front='', arms='', tilt=0, face=''):
    S.append((n, name, cap, f'<g filter="url(#cut)">{back}{TORSO}{head(e, m, b, tilt, face)}{arms}{front}</g>{plate(cap)}'))

st(1, 'money', '+403 000 ₽', 'happy', 'grin', 'up',
   arms=arm(LS, (330, 560), (250, 640)) + arm(RS, (470, 560), (550, 640)), front=bills(400, 520))
st(2, 'sleep', 'ПОКА Я СПАЛ', 'closed', 'sleep', 'normal', tilt=-12,
   back=palm_tree(110, 640, .9) + palm_tree(690, 640, .9, -1) + zzz,
   front=phone(600, 470, 120, 200, 12, txt(600, 490, '+₽', 40, '#7cf29a')) + coin(520, 380, 28) + coin(660, 330, 24) + coin(560, 290, 20))
st(3, 'eleven', '11 ПОДПИСЧИКОВ', 'happy', 'smirk', 'smug',
   arms=arm(RS, (560, 330), (640, 450)) + arm(LS, (190, 600), (150, 540)),
   front=phone(560, 250, 160, 260, 8, txt(560, 250, '11', 100, '#7cf29a') + txt(560, 310, 'платят', 28, '#cfe')))
st(4, 'nocode', 'НЕ ПРОГРАММИСТ', 'wide', 'wavy', 'up',
   arms=arm(LS, (150, 400), (150, 520), palm=True) + arm(RS, (650, 400), (650, 520), palm=True),
   front=laptop(400, 660, 360, ''.join(f'<rect x="{240+(i%3)*30}" y="{470+i*22}" width="{120+((i*53)%140)}" height="10" rx="5" fill="{c}"/>' for i, c in enumerate(['#7ff3ff', '#ff9f7a', '#c79bff', '#7cf29a', '#ffe27a', '#7ff3ff']))))
st(5, 'ai_do', 'ИИ, СДЕЛАЙ!', 'down', 'smile', 'normal',
   back=robot(640, 380, .8),
   arms=arm(LS, (340, 610), (250, 640)) + arm(RS, (460, 610), (550, 640)),
   front=laptop(400, 680, 340, txt(400, 560, '▌', 50, '#7ff3ff')))
st(6, 'lazy', 'ЛЕНИВЫЙ ДОХОД', 'cool', 'smile', 'normal',
   back=palm_tree(110, 640, .95),
   arms=arm(RS, (590, 380), (660, 480)) + arm(LS, (180, 420), (150, 540)),
   front=f'<circle cx="610" cy="350" r="56" fill="url(#wood)"/><circle cx="610" cy="350" r="40" fill="#fff6e0"/><path d="M620 330 L660 270" stroke="#ff6b7d" stroke-width="10" stroke-linecap="round"/>' + notif(250, 300, '+990 ₽', 260))
st(7, 'paid', 'ДЕНЬГИ ПРИШЛИ', 'wide', 'grin', 'up',
   arms=arm(LS, (190, 190), (170, 360)) + arm(RS, (610, 190), (630, 360)),
   front=phone(610, 140, 120, 190, 14, txt(610, 160, '+₽', 46, '#7cf29a')) + coin(200, 120, 32) + coin(120, 230, 24) + coin(700, 280, 26))
st(8, 'honest', 'ЭТО НЕ РАЗВОД', 'narrow', 'flat', 'normal',
   arms=arm(RS, (330, 560), (520, 640)) + arm(LS, (190, 600), (160, 560)))
st(9, 'numbers', 'ВОТ ЦИФРЫ', 'side', 'smile', 'up',
   arms=arm(LS, (250, 460), (190, 560)) + arm(RS, (640, 420), (650, 520)),
   front='<g transform="rotate(-6 210 410)"><rect x="80" y="300" width="270" height="210" rx="22" fill="url(#dark)"/><rect x="94" y="314" width="242" height="182" rx="14" fill="#fff"/>'
         '<rect x="120" y="440" width="34" height="40" rx="6" fill="#9be89b"/><rect x="170" y="410" width="34" height="70" rx="6" fill="#5cc97a"/><rect x="220" y="370" width="34" height="110" rx="6" fill="#2c9a52"/><rect x="270" y="330" width="34" height="150" rx="6" fill="#1f7a43"/>'
         '<path d="M120 420 L190 390 L240 350 L310 316" stroke="#c8102e" stroke-width="8" fill="none" stroke-linecap="round"/></g>'
         '<path d="M640 390 L700 330" stroke="url(#skin)" stroke-width="26" stroke-linecap="round"/>')
st(10, 'pain', 'НАШЁЛ БОЛЬ', 'wink', 'smirk', 'smug',
   face='<path d="M250 210 Q400 120 552 210 Q560 236 530 230 Q400 190 270 230 Q240 236 250 210Z" fill="#8a5a3a"/><path d="M520 222 Q600 230 640 212" stroke="#8a5a3a" stroke-width="22" stroke-linecap="round"/>',
   arms=arm(RS, (470, 330), (600, 450)),
   front='<circle cx="460" cy="320" r="70" fill="#d6f2ff" opacity=".55"/><circle cx="460" cy="320" r="70" fill="none" stroke="url(#gold)" stroke-width="18"/><path d="M510 372 L580 450" stroke="url(#wood)" stroke-width="26" stroke-linecap="round"/>' + HL(436, 296, 22, 12, .8))
st(11, 'niche', 'УЗКАЯ НИША', 'side', 'smirk', 'angry',
   back=''.join(f'<circle cx="650" cy="190" r="{r}" fill="{c}"/>' for r, c in ((110, '#c8102e'), (82, '#fff'), (56, '#c8102e'), (30, '#fff'), (12, '#c8102e'))),
   arms=arm(RS, (600, 420), (660, 520)),
   front='<path d="M600 400 L644 206" stroke="#3a3a46" stroke-width="10" stroke-linecap="round"/><path d="M644 196 l-16 22 l22 6Z" fill="#3a3a46"/><path d="M600 400 l-22 14 M600 400 l8 24" stroke="#c8102e" stroke-width="14" stroke-linecap="round"/>')
st(12, 'secret', 'ПО СЕКРЕТУ', 'wink', 'sleep', 'smug',
   arms=arm(RS, (420, 420), (560, 560)),
   front='<path d="M420 430 L420 360" stroke="url(#skin)" stroke-width="28" stroke-linecap="round"/>' + HL(412, 372, 6, 14, .6, 0))
st(13, 'write_ai', 'ПИШИ «ИИ»', 'down', 'o', 'up',
   arms=arm(LS, (230, 640), (180, 560)) + arm(RS, (570, 640), (620, 560)),
   back='<path d="M120 300 L120 520 M90 480 L120 530 L150 480" stroke="#c8102e" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M680 300 L680 520 M650 480 L680 530 L710 480" stroke="#c8102e" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
st(14, 'go', 'ПОГНАЛИ', 'narrow', 'grin', 'angry',
   arms=arm(LS, (230, 400), (150, 520), fist=True) + arm(RS, (570, 400), (650, 520), fist=True),
   back='<path d="M120 200 l40 30 M680 200 l-40 30 M100 300 l50 6 M700 300 l-50 6" stroke="#ffb31a" stroke-width="14" stroke-linecap="round"/>')
st(15, 'empty', 'ГДЕ ПРОДУКТ?', 'wide', 'wavy', 'sad',
   arms=arm(LS, (290, 560), (210, 640)) + arm(RS, (510, 560), (590, 640)),
   front='<path d="M270 520 L530 520 L510 640 L290 640Z" fill="url(#wood)"/><path d="M270 520 L230 470 L360 470 L380 520Z M530 520 L570 470 L440 470 L420 520Z" fill="#c48a4c"/><path d="M300 540 L500 540" stroke="#7a4a20" stroke-width="8" opacity=".5"/>'
         + txt(640, 210, '?', 110, '#c8102e') + txt(170, 230, '?', 80, '#c8102e'))
st(16, 'channels', '5 КАНАЛОВ', 'up', 'grin', 'up',
   arms=arm(LS, (190, 240), (160, 400)) + arm(RS, (610, 240), (640, 400)),
   back=''.join(phone(x, y, 92, 150, r, txt(x, y + 14, t, 40)) for x, y, r, t in ((150, 120, -20, '▶'), (290, 60, -8, '★'), (400, 40, 0, 'N'), (510, 60, 8, 'AI'), (650, 120, 20, '♪'))))
st(17, 'auto', 'РАБОТАЕТ САМО', 'happy', 'smile', 'normal',
   back=robot(640, 400, .75, False) + ''.join(f'<g transform="rotate({r} {x} {y})"><rect x="{x-40}" y="{y-34}" width="80" height="68" rx="10" fill="#fff"/><rect x="{x-32}" y="{y-26}" width="64" height="40" rx="6" fill="{c}"/><circle cx="{x+14}" cy="{y-14}" r="7" fill="#fff6a0"/></g>' for x, y, r, c in ((560, 160, -14, '#7fd0ff'), (680, 120, 10, '#ff9fc0'), (740, 230, 18, '#9be89b'), (600, 60, -4, '#ffd27a'))),
   arms=arm(LS, (330, 470), (240, 600)),
   front='<path d="M290 430 L370 430 L362 520 Q330 536 298 520Z" fill="url(#white)"/><path d="M370 450 Q400 456 396 482 Q392 500 366 500" stroke="#dcd6cc" stroke-width="12" fill="none"/><ellipse cx="330" cy="434" rx="38" ry="8" fill="#7a4a2a"/><path d="M314 400 q10 -20 0 -40 M340 400 q10 -20 0 -40" stroke="#c9bfb4" stroke-width="6" fill="none" stroke-linecap="round" opacity=".7"/>')
st(18, 'nomoney', 'А ДЕНЕГ НЕТ', 'closed', 'frown', 'sad',
   arms=arm(RS, (430, 290), (580, 470)),
   front=laptop(400, 690, 360, txt(400, 560, '100 000 👁', 40, '#7ff3ff') + txt(400, 615, '0 ₽', 50, '#ff6b7d')))
st(19, 'checked', 'ПРОВЕРЕНО', 'wink', 'grin', 'smug',
   arms=arm(RS, (620, 380), (660, 520), fist=True),
   front='<path d="M600 360 Q590 320 610 300" stroke="url(#skin)" stroke-width="30" stroke-linecap="round"/>' + HL(604, 306, 6, 10, .6, 0))
st(20, 'course', 'КУРС ГОТОВ', 'happy', 'grin', 'up',
   arms=arm(LS, (290, 560), (210, 640)) + arm(RS, (510, 560), (590, 640)),
   front='<rect x="250" y="470" width="300" height="200" rx="18" fill="url(#red)"/><rect x="262" y="482" width="276" height="176" rx="12" fill="none" stroke="#ffd3d8" stroke-width="4"/>' + txt(400, 560, 'КУРС', 58)
         + '<g transform="rotate(-14 400 620)"><rect x="300" y="590" width="200" height="56" rx="10" fill="none" stroke="#fff" stroke-width="6"/>' + txt(400, 630, 'БЕЗ ВОДЫ', 30) + '</g>')

# ── вторая пачка: ИИ и заработок на ИИ (21–40) ──
bulb = lambda x, y, s=1: (f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="0" r="70" fill="url(#gold)"/><rect x="-32" y="56" width="64" height="44" rx="10" fill="url(#bot)"/>'
    '<path d="M-22 70 L22 70 M-22 86 L22 86" stroke="#6b7fae" stroke-width="6"/><path d="M-20 10 Q0 -30 20 10" stroke="#fff6c0" stroke-width="10" fill="none" stroke-linecap="round"/>'
    + ''.join(f'<path d="M{math.cos(a)*92:.0f} {math.sin(a)*92:.0f} L{math.cos(a)*120:.0f} {math.sin(a)*120:.0f}" stroke="#ffb31a" stroke-width="12" stroke-linecap="round"/>' for a in [math.pi*(1+i/6) for i in range(7)])
    + HL(-24, -26, 18, 12, .8) + '</g>')
rocket = lambda x, y, r=30: (f'<g transform="rotate({r} {x} {y})"><path d="M{x} {y-130} Q{x+56} {y-60} {x+46} {y+40} L{x-46} {y+40} Q{x-56} {y-60} {x} {y-130}Z" fill="url(#white)"/>'
    f'<circle cx="{x}" cy="{y-40}" r="24" fill="url(#bot)"/><circle cx="{x}" cy="{y-40}" r="14" fill="url(#screen)"/>'
    f'<path d="M{x-46} {y+10} L{x-80} {y+60} L{x-40} {y+40}Z M{x+46} {y+10} L{x+80} {y+60} L{x+40} {y+40}Z" fill="url(#red)"/>'
    f'<path d="M{x-28} {y+46} Q{x} {y+150} {x+28} {y+46}Z" fill="url(#gold)"/><path d="M{x-14} {y+46} Q{x} {y+110} {x+14} {y+46}Z" fill="#fff6c0"/></g>')
def bar(x, y, w, pct, c='url(#green)', label=''):
    return (f'<rect x="{x-w/2}" y="{y-28}" width="{w}" height="56" rx="28" fill="url(#dark)"/><rect x="{x-w/2+8}" y="{y-20}" width="{(w-16)*pct}" height="40" rx="20" fill="{c}"/>'
            + (txt(x, y + 13, label, 34) if label else ''))
piggy = lambda x, y: (f'<g><ellipse cx="{x}" cy="{y}" rx="130" ry="100" fill="url(#red)" opacity="0"/><ellipse cx="{x}" cy="{y}" rx="130" ry="100" fill="#ff9fb4"/><ellipse cx="{x}" cy="{y}" rx="130" ry="100" fill="url(#hlpig)" opacity="0"/>'
    f'<ellipse cx="{x+118}" cy="{y+6}" rx="34" ry="28" fill="#ff7f9c"/><circle cx="{x+110}" cy="{y+2}" r="6" fill="#b84a66"/><circle cx="{x+128}" cy="{y+2}" r="6" fill="#b84a66"/>'
    f'<circle cx="{x+62}" cy="{y-30}" r="10" fill="#3a2416"/><path d="M{x+20} {y-96} L{x+44} {y-130} L{x+60} {y-90}Z" fill="#ff7f9c"/>'
    f'<rect x="{x-80}" y="{y+80}" width="34" height="44" rx="12" fill="#ff7f9c"/><rect x="{x+40}" y="{y+80}" width="34" height="44" rx="12" fill="#ff7f9c"/>'
    f'<rect x="{x-30}" y="{y-104}" width="60" height="12" rx="6" fill="#b84a66"/>' + HL(x - 50, y - 50, 40, 20, .6) + '</g>')
trophy = lambda x, y: (f'<path d="M{x-90} {y-120} L{x+90} {y-120} Q{x+90} {y+10} {x} {y+30} Q{x-90} {y+10} {x-90} {y-120}Z" fill="url(#gold)"/>'
    f'<path d="M{x-90} {y-100} Q{x-150} {y-90} {x-120} {y-20} Q{x-100} {y+6} {x-70} {y-10}" stroke="#e09a12" stroke-width="16" fill="none"/>'
    f'<path d="M{x+90} {y-100} Q{x+150} {y-90} {x+120} {y-20} Q{x+100} {y+6} {x+70} {y-10}" stroke="#e09a12" stroke-width="16" fill="none"/>'
    f'<rect x="{x-18}" y="{y+26}" width="36" height="50" fill="#e09a12"/><rect x="{x-70}" y="{y+70}" width="140" height="40" rx="10" fill="url(#wood)"/>'
    + txt(x, y - 34, '1', 80, '#b4730a') + HL(x - 40, y - 90, 20, 30, .7, 0))
heart = lambda x, y, s=1, c='url(#red)': f'<path transform="translate({x} {y}) scale({s})" d="M0 30 C-60 -10 -50 -70 0 -40 C50 -70 60 -10 0 30Z" fill="{c}"/>'
bag = lambda x, y: (f'<path d="M{x-80} {y-60} L{x+80} {y-60} L{x+96} {y+90} L{x-96} {y+90}Z" fill="url(#red)"/><path d="M{x-40} {y-60} Q{x-40} {y-130} {x} {y-130} Q{x+40} {y-130} {x+40} {y-60}" stroke="#a00a22" stroke-width="14" fill="none"/>'
    + txt(x, y + 46, '₽', 90) + HL(x - 40, y - 30, 16, 30, .5, 0))
funnel = lambda x, y: (f'<path d="M{x-150} {y-150} L{x+150} {y-150} L{x+30} {y} L{x+30} {y+80} L{x-30} {y+110} L{x-30} {y}Z" fill="url(#bot)"/>'
    + ''.join(f'<circle cx="{x+dx}" cy="{y-190}" r="20" fill="#ffb38a"/><path d="M{x+dx-22} {y-150} Q{x+dx} {y-176} {x+dx+22} {y-150}" fill="#ffb38a"/>' for dx in (-110, -55, 0, 55, 110))
    + coin(x, y + 150, 30))
steam = '<path d="M300 140 q-20 -30 0 -60 q20 -30 0 -60 M400 120 q-20 -30 0 -60 q20 -30 0 -60 M500 140 q-20 -30 0 -60 q20 -30 0 -60" stroke="#c9d4e6" stroke-width="18" fill="none" stroke-linecap="round" opacity=".9"/>'
clock = lambda x, y: (f'<circle cx="{x}" cy="{y}" r="90" fill="url(#white)"/><circle cx="{x}" cy="{y}" r="90" fill="none" stroke="url(#red)" stroke-width="14"/>'
    f'<path d="M{x} {y} L{x} {y-60} M{x} {y} L{x+44} {y+20}" stroke="#121212" stroke-width="12" stroke-linecap="round"/><circle cx="{x}" cy="{y}" r="10" fill="#121212"/>')

st(21, 'partner', 'МОЙ НАПАРНИК', 'happy', 'grin', 'up',
   front=robot(640, 560, .75, True), arms=arm(RS, (560, 470), (600, 560)))
st(22, 'idea', 'ИДЕЯ!', 'wide', 'o', 'up', front=bulb(640, 150, .85),
   arms=arm(RS, (600, 330), (660, 450)))
st(23, 'launch', 'ЗАПУСКАЮ', 'narrow', 'grin', 'angry', back=rocket(640, 250, 25),
   arms=arm(LS, (220, 300), (150, 440), fist=True))
st(24, 'loading', 'ГЕНЕРИРУЮ…', 'down', 'flat', 'normal',
   arms=arm(LS, (330, 610), (250, 640)) + arm(RS, (470, 610), (550, 640)),
   front=laptop(400, 690, 340, bar(400, 570, 240, .7, 'url(#green)', '70%')))
st(25, 'ai_fail', 'ИИ ОШИБСЯ', 'wide', 'wavy', 'sad',
   back=robot(630, 470, .85, False) + '<path d="M600 300 q-20 -30 0 -60 M650 300 q20 -30 0 -60" stroke="#9aa3b5" stroke-width="14" fill="none" stroke-linecap="round"/>' + txt(700, 250, '!', 90, '#c8102e'),
   arms=arm(LS, (180, 380), (150, 500), palm=True))
st(26, 'redo', 'ПЕРЕДЕЛАЙ', 'narrow', 'frown', 'angry',
   arms=arm(LS, (330, 610), (250, 640), fist=True) + arm(RS, (470, 610), (550, 640), fist=True),
   front=laptop(400, 690, 340, txt(400, 575, '↻', 90, '#ffb31a')),
   back='<path d="M150 180 l40 30 M650 180 l-40 30" stroke="#c8102e" stroke-width="14" stroke-linecap="round"/>')
st(27, 'lead', 'НОВАЯ ЗАЯВКА', 'wide', 'grin', 'up',
   arms=arm(RS, (600, 300), (660, 450)),
   front=phone(600, 220, 160, 250, 10, '<rect x="545" y="170" width="110" height="74" rx="10" fill="#fff"/><path d="M545 172 L600 214 L655 172" stroke="#c8102e" stroke-width="8" fill="none"/>' + txt(600, 300, '+1', 50, '#7cf29a')))
st(28, 'sale', 'ПРОДАЖА!', 'happy', 'grin', 'up', back=bag(640, 300),
   arms=arm(LS, (190, 220), (160, 380)) + coin(190, 160, 34))
st(29, 'piggy', 'КОПЛЮ НА МЕЧТУ', 'happy', 'smile', 'normal',
   arms=arm(LS, (300, 560), (210, 640)) + arm(RS, (500, 560), (590, 640)),
   front=piggy(400, 560) + coin(400, 420, 30))
st(30, 'office', 'МОЙ ОФИС', 'cool', 'smirk', 'smug',
   back=palm_tree(110, 640, .95) + palm_tree(700, 640, .9, -1) + '<circle cx="640" cy="120" r="60" fill="url(#gold)" opacity=".9"/>',
   front=laptop(400, 690, 320, txt(400, 580, 'AI', 70, '#7ff3ff')))
st(31, 'saved', '−5 ЧАСОВ РАБОТЫ', 'happy', 'smile', 'up', back=clock(640, 230),
   arms=arm(RS, (580, 360), (650, 460)))
st(32, 'argue', 'СПОРИМ?', 'narrow', 'smirk', 'smug',
   arms=arm(LS, (500, 560), (300, 640)) + arm(RS, (300, 580), (500, 660)))
st(33, 'sub', 'ПОДПИСКА +1', 'happy', 'grin', 'up',
   arms=arm(RS, (590, 340), (650, 460)),
   front=phone(590, 260, 160, 250, 8, '<circle cx="590" cy="230" r="36" fill="#ff6b3d"/>' + txt(590, 244, 'B', 40) + txt(590, 320, '+1', 50, '#7cf29a')) + heart(470, 140, .9))
st(34, 'overheat', 'МОЗГ КИПИТ', 'closed', 'wavy', 'sad', back=steam,
   arms=arm(LS, (260, 300), (170, 440)) + arm(RS, (540, 300), (630, 440)))
st(35, 'levelup', 'ЛЕВЕЛ АП', 'happy', 'grin', 'up',
   front=bar(400, 70, 520, .86, 'url(#gold)', 'LVL 99') + '<path d="M680 40 l20 -36 l20 36" stroke="#2c9a52" stroke-width="14" fill="none" stroke-linecap="round"/>',
   arms=arm(LS, (190, 300), (160, 430), fist=True) + arm(RS, (610, 300), (640, 430), fist=True))
st(36, 'top1', 'ТОП-1 В НИШЕ', 'wink', 'grin', 'smug', back=trophy(640, 280),
   arms=arm(RS, (560, 380), (630, 480)))
st(37, 'funnel', 'ВОРОНКА', 'side', 'smile', 'up', back=funnel(640, 310),
   arms=arm(LS, (190, 420), (160, 530), palm=True))
st(38, 'million', 'ЦЕЛЬ: 1 МЛН', 'up', 'smile', 'up',
   front='<path d="M640 420 L640 90" stroke="#a8692f" stroke-width="16" stroke-linecap="round"/><path d="M648 96 L780 140 L648 190Z" fill="url(#red)"/>' + txt(706, 156, '1М', 38),
   arms=arm(RS, (630, 380), (680, 480)))
st(39, 'nowater', 'БЕЗ ВОДЫ', 'narrow', 'flat', 'normal',
   front='<path d="M250 470 Q250 400 330 400 L470 400 Q550 400 550 470 L550 560 L250 560Z" fill="url(#bot)" opacity="0"/>'
         '<g transform="translate(660 330) scale(.85)"><path d="M0 -90 Q60 -10 60 30 A60 60 0 0 1 -60 30 Q-60 -10 0 -90Z" fill="url(#bot)"/><path d="M-80 -80 L80 110" stroke="#c8102e" stroke-width="20" stroke-linecap="round"/></g>',
   arms=arm(LS, (230, 400), (150, 520), palm=True))
st(40, 'thanks', 'СПАСИБО!', 'happy', 'grin', 'up',
   arms=arm(LS, (360, 470), (240, 600)) + arm(RS, (440, 470), (560, 600)),
   front=heart(400, 480, 1.5) + heart(170, 200, .8, 'url(#gold)') + heart(640, 170, .7) + heart(680, 330, .5, 'url(#gold)'))

import base64
FONT = '@font-face{font-family:Unb;src:url(data:font/ttf;base64,' + base64.b64encode(open(os.path.join(ROOT, 'assets/fonts/Unbounded-VF.ttf'), 'rb').read()).decode() + ');font-weight:200 900}'
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
