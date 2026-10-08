# Генератор index.html для WoW-ролика 16:9 (ветка wow-anna): python tools/wow_page.py
# Вёрстку удобнее править здесь: V() — слой с геймплеем, ST() — стикер Ани, остальное — обычный HTML.
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# исходник ролика: assets/video/src/<VID>.mp4 → кадры assets/video/<VID>/ (ролик №1 «гиперспавн» — wowfarm, ветка wow-hyperspawn)
VID, NF = 'wetlands', 8862                  # кадров в assets/video/wetlands (295.4 с × 30)
STAGES = ['Напарник', 'Аукцион', 'Редкий дроп', 'Снежная буря', '30 уровень']   # этапы полосы задания сверху

def V(frm, rate=1, roi=None, cls='', zd=None):
    """Геймплей на весь кадр: frm — секунда исходника, rate — скорость, roi="x,y,w x,y,w" — наезд в область кадра."""
    a = f' data-roi="{roi}"' if roi else ''
    a += f' data-zd="{zd}"' if zd else ''
    return (f'<div class="shotz vid full game {cls}" data-video="{VID}" data-from="{frm}" data-rate="{rate}" data-frames="{NF}" data-audio="0"{a}>'
            f'<img src="assets/video/{VID}/f_{int(frm * 30) + 1:04d}.jpg" alt=""></div>')

def ST(n, x, y, size=400, fx='peek', frm='right', mark=None, at=None, rot=0):
    m = f' data-mark="{mark}"' if mark else ''
    m += f' data-at="{at}"' if at is not None else ''
    f = f' data-from="{frm}" data-rot="{rot}"' if fx == 'peek' else ''
    return f'<div class="tst" data-fx="{fx}"{f}{m} style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px"><img src="assets/wow/toon/{n}.png" alt=""></div>'

ico = lambda s, cls='': f'<i class="ico {cls}"><svg viewBox="0 0 100 100"><use href="#{s}"/></svg></i>'
mobs = lambda n, s='mob': ''.join(f'<svg class="mobi" viewBox="0 0 100 100"><use href="#{s}"/></svg>' for _ in range(n))

SECS = []
def sec(comment, *layers, trans='', stage=None, hint=''):
    t = f' data-trans="{trans}"' if trans else ''
    t += f' data-stage="{stage}"' if stage is not None else ''
    t += f' data-hint="{hint}"' if hint else ''
    NL, HID = '\n', ' style="opacity:0"'
    body = ''.join(f'{NL}      <div class="layer {chr(65 + k)}"{HID if k else ""}>{NL}        ' + (NL + '        ').join(l) + f'{NL}      </div>' for k, l in enumerate(layers))
    SECS.append(f'    <!-- {comment} -->\n    <section class="sec" id="s{len(SECS) + 1}"{t}>{body}\n    </section>')


ZONE = lambda big, small, hold=2.4: (f'<div class="row" style="top:110px"><div class="zone" data-fx="zone" data-at=".2" data-hold="{hold}">'
                                    f'<b>{big}</b><span>{small}</span></div></div>')
TIMER = lambda n, d, cap, extra='': (f'<div class="timer" data-fx="timer" data-n="{n}" data-d="{d}"{extra}><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" class="bgc"/>'
                                     f'<circle cx="100" cy="100" r="84" class="ring" pathLength="1"/></svg><b>{n}</b><span>{cap}</span></div>')
BOOSTY = lambda kick, extra='': (f'<div class="bcard wp" data-fx="up" data-at=".05"{extra}><div class="bt">'
                                 f'<div class="kicker">{kick}</div><img class="blogo" src="assets/wow/boosty_logo.png" alt="" data-fx="pop" data-at=".3">'
                                 '<div class="blink">boosty.to/<b>anna_rich</b></div>'
                                 '<div class="chip wp sm" data-fx="pop" data-at=".7">⬇ ссылка в описании</div></div></div>')

# ═══ Ролик №2: маг 28→30 в Болотине, огромные пуллы с шаманом-хилом (исходник assets/video/src/wetlands.mp4) ═══
# 1. Хук: стянула полполяны → не умерла, сейчас расскажу секрет
sec('1. Хук: стянула полполяны мобов → не умерла',
    [V(24), '<div class="abs" style="left:110px;top:240px"><div class="h1 hk hkx" data-fx="punch" style="font-size:150px;text-align:left">ПОЛПОЛЯНЫ<br><em>МОБОВ</em></div></div>'],
    [V(116.5), '<div class="abs" style="left:110px;top:250px"><div class="h2" data-fx="up" data-at=".1" style="text-align:left">И Я <em>НЕ УМЕРЛА</em></div></div>',
     '<div class="abs" style="left:110px;top:400px"><div class="chip wp" data-fx="left" data-at=".6">' + ico('i-key') + 'в чём <b class="qy">секрет</b>?</div></div>',
     ST('16_come', 1450, 420, 440, frm='right', at=.5, rot=-5)])

# 2. Привет, голдфармеры + задание «досмотри до конца»
sec('2. Привет, голдфармеры, с вами Аня · 28 ур., Болотина → задание',
    [V(4), '<div class="row" style="top:150px"><img class="logo" data-fx="zoom" data-at=".05" src="assets/wow/logo.png" alt="" style="width:440px"></div>',
     '<div class="row" style="top:560px"><div class="h2" data-fx="up" data-at=".5" style="font-size:64px">ПРИВЕТ, <em>ГОЛДФАРМЕРЫ!</em></div></div>',
     '<div class="row" style="top:660px"><div class="chip wp sm" data-fx="pop" data-at="1.1">' + ico('i-arc', 'arc') + 'маг <b class="qy">28 ур.</b> · Болотина</div></div>'],
    [V(68), '<div class="abs" style="left:110px;top:200px"><div class="quest" data-fx="up" data-at=".05" data-sfx="questacc">'
     '<div class="qh">❗ НОВОЕ ЗАДАНИЕ</div><div class="qt">Досмотри до конца</div>'
     '<div class="qo" data-fx="left" data-mark="a"><i>◆</i>Апнуть 30 уровень <b>0/1</b></div>'
     '<div class="qo" data-fx="left" data-mark="b"><i>◆</i>Лучшая ферма до 30 <b>0/1</b></div>'
     '<div class="qr2">Награда: <span class="qy">● опыт</span> и <span class="q3">[редкий дроп]</span></div></div></div>',
     ST('20_gg', 1440, 420, 440, frm='right', at=.6, rot=-5)])

# 3. Секрет: шаман-хил → тяну всё больше
sec('3. Глава «Напарник»: шаман хилит → тяну всё больше',
    [V(100), ZONE('НАПАРНИК', 'шаман хилит и качается вместе со мной')],
    [V(120.5), '<div class="abs" style="left:110px;top:190px"><div class="grp wp" data-fx="up" data-at=".05">'
     '<div class="gc" data-fx="pop" data-at=".25"><div class="ico arc" style="width:120px;height:120px"><svg viewBox="0 0 100 100"><use href="#i-arc"/></svg></div><b>маг</b><span>урон</span></div>'
     '<div class="gp" data-fx="pop" data-at=".45">+</div>'
     '<div class="gc" data-fx="pop" data-at=".6"><div class="ico" style="width:120px;height:120px;background:radial-gradient(circle at 40% 35%,#e8fff0,#3fd68a 45%,#0b4a2a)"><svg viewBox="0 0 100 100"><use href="#i-heal"/></svg></div><b>шаман</b><span>хил</span></div>'
     '<div class="gp" data-fx="pop" data-mark="a">=</div>'
     '<div class="gc" data-fx="zoom" data-mark="a" data-at=".1"><div class="gi">' + mobs(4) + '</div><b class="qy">огромные пуллы</b></div></div></div>',
     ST('15_easy', 1450, 420, 440, frm='right', mark='b', at=.1, rot=-5)], stage=0)

# 4. Точка на карте: Болотина, конкурентов почти нет, мобы стоят плотно
sec('4. Где фармлю: карта Болотины, конкурентов нет, мобы плотно',
    [V(40.2, .5, roi='0,0,1 .27,.2,.42', zd=1.4), '<div class="pin" data-fx="zoom" data-at="1.2" style="left:920px;top:565px"><i></i><i></i></div>',
     '<div class="abs" style="left:1300px;top:240px"><div class="chip wp" data-fx="right" data-at="1.0">' + ico('i-map') + '<b class="qy">Болотина</b></div></div>',
     '<div class="abs" style="left:1300px;top:400px"><div class="chip wp sm" data-fx="right" data-mark="a">конкурентов: <b class="q2">почти 0</b></div></div>',
     ST('17_map', 60, 440, 420, frm='left', at=1.4, rot=5)],
    [V(84), '<div class="abs" style="left:110px;top:220px"><div class="chip wp" data-fx="left" data-at=".2">' + ico('i-mob') + 'мобы стоят <b class="qy">впритык</b></div></div>',
     ST('16_come', 1450, 420, 440, frm='right', mark='b', at=.1, rot=-5)], stage=0)

# 5. Шмот так себе: аукцион лежит 2 дня
sec('5. Шмот: аукцион не работает 2 дня',
    [V(59.6, .45, roi='0,0,1 0,.06,.62'), '<div class="abs" style="left:1240px;top:230px"><div class="tip" data-fx="right" data-at=".4"><div class="qy" style="font:900 48px/1.1 Aleg">Шмот бы получше</div><div class="q0">но купить негде</div></div></div>'],
    [V(72), '<div class="abs" style="left:110px;top:210px"><div class="tip" data-fx="left" data-at=".2"><div style="font:900 52px/1.1 Aleg;color:#ff6b5b">Аукцион закрыт ✕</div><div class="q0">не работает уже <b class="q1">2 дня</b></div></div></div>',
     '<div class="abs" style="left:110px;top:420px"><div class="chip wp sm" data-fx="up" data-mark="b">фармлю тем, что есть</div></div>',
     ST('07_nobody', 1450, 420, 440, frm='right', at=.6, rot=-5)], stage=1)

# 6. Соло можно, но кастеры → редкий дроп: сабля
sec('6. Глава «Редкий дроп»: соло мешают кастеры → выпала сабля',
    [V(128), '<div class="abs" style="left:110px;top:220px"><div class="chip wp" data-fx="left" data-at=".2">' + ico('i-mob') + 'соло: <b class="qy">можно</b></div></div>',
     '<div class="abs" style="left:110px;top:370px"><div class="chip wp sm" data-fx="left" data-mark="a">⚠ мешают мобы-кастеры</div></div>'],
    [V(101, .4, roi='0,0,1 .55,.02,.45', zd=1.3), '<div class="abs" style="left:40px;top:520px"><div class="loot wp" style="width:580px;padding:22px 30px" data-fx="up" data-at=".1" data-sfx="wcoin">'
     '<div class="ph">РЕДКИЙ ДРОП</div><div class="li">' + ico('i-sword') + '<span class="q3">[Twisted Sabre]</span></div></div></div>',
     '<div class="abs" style="left:40px;top:770px"><div class="chip wp sm" data-fx="up" data-mark="c">цена? <b class="q0">аукциона-то нет</b></div></div>',
     ST('13_green', 1560, 540, 340, frm='right', at=.6, rot=-5)], stage=2)

# 7. Сумки и банк забиты → тяну ещё больше
sec('7. Сумки и банк забиты → тяну ещё больше',
    [V(48, 1, roi='0,0,1 .55,.35,.45'), '<div class="abs" style="left:110px;top:230px"><div class="chip wp" data-fx="left" data-at=".3" data-sfx="bagopen">' + ico('i-bag') + 'сумки и банк <b class="qy">забиты</b></div></div>',
     ST('05_bags', 110, 420, 440, frm='left', at=.7, rot=4)],
    [V(174), '<div class="abs" style="left:110px;top:240px"><div class="h2" data-fx="up" data-at=".1" style="text-align:left">ТЯНУ<br><em>ЕЩЁ БОЛЬШЕ!</em></div></div>',
     ST('02_loot', 1450, 420, 440, frm='right', at=.5, rot=-5)])

# 8. Boosty в середине: сундук на цепях → секретные листки → карточка
sec('8. Boosty (середина ролика): сундук с запретными методами → ссылка',
    [V(190, 1, cls='soft'), '<div class="row" style="top:150px"><div class="h2" data-fx="up" data-at=".2">ЗАПРЕТНЫЕ МЕТОДЫ <em>ГОЛДФАРМА</em></div></div>',
     '<div class="chest" data-fx="chest" data-crack="a" data-at=".4" style="left:760px;top:330px">'
     '<div class="rays"></div><svg class="cbody" viewBox="0 0 400 300"><use href="#chest"/></svg><svg class="lid" viewBox="0 0 400 160"><use href="#chestlid"/></svg>'
     '<svg class="chain c1" viewBox="0 0 60 360"><use href="#chain"/></svg><svg class="chain c2" viewBox="0 0 60 360"><use href="#chain"/></svg>'
     '<svg class="lock" viewBox="0 0 100 120"><use href="#lock"/></svg></div>',
     '<div class="page" data-fx="fly" data-mark="b" data-dx="-520" data-rot="-8" style="left:250px;top:330px"><i></i><i></i><i class="s"></i><i></i><i class="s"></i><i></i><b>ЗАСЕКРЕЧЕНО</b></div>',
     '<div class="page" data-fx="fly" data-mark="b" data-at=".25" data-dx="520" data-rot="7" style="left:1280px;top:350px"><i></i><i class="s"></i><i></i><i></i><i class="s"></i><i></i><b>ЗАСЕКРЕЧЕНО</b></div>'],
    [V(206, 1, cls='soft'), '<div class="abs" style="left:110px;top:200px">' + BOOSTY('запретные методы голдфарма') + '</div>',
     ST('12_forbidden', 1450, 400, 460, frm='right', at=.6, rot=-5)], trans='portal')

# 9. Снежная буря: не как в классике → 29 уровень
sec('9. Глава «Снежная буря»: не как в классике → 29 уровень',
    [V(52.2, .4, roi='0,0,1 .15,0,.78'), '<div class="abs" style="left:1180px;top:200px"><div class="tact wp" style="width:640px;padding:26px 34px" data-fx="right" data-at=".4"><div class="ph">СНЕЖНАЯ БУРЯ</div>'
     '<div class="ti no" data-fx="left" data-mark="a"><span>замедление <b>слабое</b></span><em>✕</em></div>'
     '<div class="ti no" data-fx="left" data-mark="b"><span>мобы <b>добегают</b></span><em>✕</em></div>'
     '<div class="ti no" data-fx="left" data-mark="c"><span>мана <b>улетает</b></span><em>✕</em></div></div></div>'],
    [V(153.4), '<div class="row" style="top:300px"><div class="banner" data-fx="zoom" data-at=".1" data-sfx="levelup">УРОВЕНЬ 29</div></div>',
     ST('09_trash', 1450, 430, 440, frm='right', at=.6, rot=-5)], stage=3)

# 10. Обратно на Тайную магию → Скачок в толпу как торпеда
sec('10. Обратно на Тайную магию → Скачок в толпу, как торпеда',
    [V(164.4, .4, roi='0,0,1 .15,0,.78'), '<div class="abs" style="left:1180px;top:560px"><div class="tip" data-fx="right" data-at=".4"><div class="qy" style="font:900 46px/1.1 Aleg">Тайная магия</div><div>почти бесконечная мана</div></div></div>'],
    [V(250), '<div class="abs" style="left:110px;top:220px"><div class="chip wp" data-fx="left" data-at=".2">' + ico('i-arc', 'arc') + '<span><small>скачок в толпу</small>как торпеда!</span></div></div>',
     '<div class="abs" style="left:110px;top:420px"><div class="chip wp sm" data-fx="up" data-mark="c">хорошо, что есть <b class="q2">хил</b></div></div>',
     ST('06_boom', 1450, 420, 440, frm='right', mark='b', at=.1, rot=-5)], trans='portal')

# 11. Задания в Красногорье → дзинь, 30 уровень
sec('11. Глава «30 уровень»: задания в Красногорье → дзинь',
    [V(262.5), ZONE('30 УРОВЕНЬ', 'Красногорье · последние задания', 2.0)],
    [V(278.6), '<div class="row" style="top:250px"><div class="banner" data-fx="zoom" data-at=".2" data-sfx="levelup">УРОВЕНЬ 30</div></div>',
     '<div class="rain" data-fx="rain" data-n="16" data-at=".4"></div>',
     ST('01_rich', 1450, 420, 440, frm='right', at=.6, rot=-5)], trans='load', stage=4,
    hint='Подсказка: шаман-хил рядом, значит можно тянуть в два раза больше мобов.')

# 12. Финал: задание выполнено → ферма Орды в следующем видео → Boosty + подписка
sec('12. Финал: задание выполнено → ферма Орды в следующем видео → Boosty + подписка',
    [V(238), '<div class="row" style="top:170px"><div class="banner" data-fx="zoom" data-at=".05" data-sfx="questdone">ЗАДАНИЕ ВЫПОЛНЕНО</div></div>',
     '<div class="abs" style="left:110px;top:400px"><div class="quest done" data-fx="up" data-at=".4"><div class="qo"><i>✓</i>Апнуть 30 уровень <b>1/1</b></div>'
     '<div class="qo" data-fx="left" data-mark="a"><i>✓</i>Лучшая ферма до 30: <b style="color:#b8160e">Орда</b></div></div></div>',
     ST('04_secret', 1450, 420, 440, frm='right', mark='a', at=.2, rot=-5)],
    [V(198, 1, cls='soft'), '<div class="abs" style="left:110px;top:170px" id="guide">' + BOOSTY('запретные методы голдфарма') + '</div>',
     '<div class="abs" style="left:110px;top:640px"><div class="subbtn" id="cta" data-fx="pop" data-at=".5">ПОДПИШИСЬ ✦</div></div>',
     ST('18_sub', 1450, 400, 460, fx='plop', mark='c', at=.1)])

CSS = open(os.path.join(ROOT, 'tools', 'wow_style.css'), encoding='utf-8').read()
DEFS = open(os.path.join(ROOT, 'tools', 'wow_defs.svg'), encoding='utf-8').read()
html = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>WoW Forever: маг 28→30 в Болотине на огромных пуллах (Аня, 16:9)</title>
<!-- файл собран tools/wow_page.py (стили — tools/wow_style.css, иконки — tools/wow_defs.svg) -->
<style>
{CSS}
</style>
</head>
<body>
<div id="view">
  <div id="bg"></div>
  <div class="bgi" id="bgA"></div><div class="bgi" id="bgB"></div>
  <canvas id="speed" width="1920" height="1080"></canvas>
  <svg id="star" viewBox="-100 -100 200 200"><path id="starp"/></svg>
  <div id="arc"></div><div id="grid"></div><div id="floor"></div>

  <!-- Разметка монтажа: .layer = кадр; data-fx (pop/left/right/up/zoom/slam/punch/kin/peek/plop/grow/timer/rain), data-mark, data-at, data-count; у видео data-roi — наезд в область кадра -->
  <div id="world">
{chr(10).join(SECS)}
  </div>

  <div id="fog"><i></i><i></i><i></i></div>
  <canvas id="embers" width="1920" height="1080"></canvas>
  <canvas id="fx" width="1920" height="1080"></canvas>
  <div id="hud">
    <div id="uf"><div class="pt"><img src="assets/wow/avatar.jpg" alt=""></div>
      <div class="ufr"><div class="nm">Аня <span>anna_rich</span></div><div class="bar hp"><i></i></div><div class="bar mp"><i></i></div></div></div>
    <img id="logo" src="assets/wow/logo.png" alt="">
    <div id="qbar"><div class="qt">Досмотри до конца</div><div class="ql"><div id="qfill"></div></div>
      <div class="qss">{''.join(f'<span class="qs">{x}</span>' for x in STAGES)}</div></div>
  </div>
  <div id="dip"></div>
  <div id="portal"></div>
  <div id="load"><img src="assets/video/{VID}/f_0121.jpg" alt=""><div class="lshade"></div><img class="llogo" src="assets/wow/logo.png" alt="">
    <div class="lhint" id="ldhint"></div><div class="lbar"><div id="ldbar"></div></div></div>
  <canvas id="grain" width="480" height="270"></canvas>
  <div id="flash"></div>
  <div id="subs"></div>
  <div id="fade"></div>
</div>
{DEFS}
<svg width="0" height="0" style="position:absolute"><filter id="mb" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur id="mbg" stdDeviation="0 0"/></filter></svg>

<script src="node_modules/gsap/dist/gsap.min.js"></script>
<script src="node_modules/lottie-web/build/player/lottie_svg.min.js"></script>
<script src="assets/timeline.js"></script>
<script src="scene.js"></script>
</body>
</html>
'''
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
print('index.html:', len(SECS), 'сцен')
