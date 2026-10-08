# Генератор index.html для WoW-ролика 16:9 (ветка wow-anna): python tools/wow_page.py
# Вёрстку удобнее править здесь: V() — слой с геймплеем, ST() — стикер Ани, остальное — обычный HTML.
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NF = 7878                                   # кадров в assets/video/wowfarm (262.6 с × 30)

def V(frm, rate=1, roi=None, cls='', zd=None):
    """Геймплей на весь кадр: frm — секунда исходника, rate — скорость, roi="x,y,w x,y,w" — наезд в область кадра."""
    a = f' data-roi="{roi}"' if roi else ''
    a += f' data-zd="{zd}"' if zd else ''
    return (f'<div class="shotz vid full game {cls}" data-video="wowfarm" data-from="{frm}" data-rate="{rate}" data-frames="{NF}" data-audio="0"{a}>'
            f'<img src="assets/video/wowfarm/f_{int(frm * 30) + 1:04d}.jpg" alt=""></div>')

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

# 1. Хук: 7 мобов, респавн 10 с → ни одного фармера, почему все пропускают?
sec('1. Хук: 7 мобов, респавн 10 сек → ни одного фармера, почему?',
    [V(79.5), '<div class="abs" style="left:110px;top:240px"><div class="h1 hk hkx" data-fx="punch" style="font-size:170px;text-align:left">7 МОБОВ</div></div>',
     '<div class="abs hk" style="left:120px;top:450px"><div class="chip wp">' + ico('i-hg') + 'РЕСПАВН <b class="qy">10 СЕК</b></div></div>'],
    [V(2, 1.2), '<div class="abs" style="left:110px;top:250px"><div class="h2" data-fx="up" data-at=".1" style="text-align:left">НИ ОДНОГО<br><em>ФАРМЕРА</em></div></div>',
     ST('07_nobody', 1450, 420, 440, frm='right', at=.5, rot=-5)])

# 2. Привет, я Аня + логотип → задание «досмотри до конца»
sec('2. Я Аня · голдфарм-точка в Форевер → задание «досмотри до конца»',
    [V(6), '<div class="row" style="top:170px"><img class="logo" data-fx="zoom" data-at=".05" src="assets/wow/logo.png" alt="" style="width:470px"></div>',
     '<div class="row" style="top:600px"><div class="h2" data-fx="up" data-at=".5" style="font-size:62px">ГОЛДФАРМ-ТОЧКА, КОТОРУЮ <em>НИКТО НЕ ТРОГАЕТ</em></div></div>'],
    [V(30), '<div class="abs" style="left:110px;top:200px"><div class="quest" data-fx="up" data-at=".05" data-sfx="questacc">'
     '<div class="qh">❗ НОВОЕ ЗАДАНИЕ</div><div class="qt">Досмотри до конца</div>'
     '<div class="qo" data-fx="left" data-mark="a"><i>◆</i>Точка на карте <b>0/1</b></div>'
     '<div class="qo" data-fx="left" data-mark="b"><i>◆</i>Фарм с 12 уровня <b>0/1</b></div>'
     '<div class="qr2">Награда: <span class="qy">● голда</span> и <span class="q2">[зелёнка]</span></div></div></div>',
     ST('20_gg', 1440, 420, 440, frm='right', at=.6, rot=-5)])

# 3. Точка: гиперспавн 7 гуманоидов = 3 бродят + Докмастер + 3 охраны
sec('3. Глава «Гиперспавн»: 3 бродят + Докмастер зовёт 3 охраны = 7 в пачке',
    [V(20), ZONE('ГИПЕРСПАВН', 'Элвиннский лес · старый причал')],
    [V(50), '<div class="abs" style="left:110px;top:190px"><div class="grp wp" data-fx="up" data-at=".05">'
     '<div class="gc" data-fx="pop" data-at=".25"><div class="gi">' + mobs(3) + '</div><b>3 бродят</b></div>'
     '<div class="gp" data-fx="pop" data-mark="a">+</div>'
     '<div class="gc" data-fx="pop" data-mark="a" data-at=".1"><div class="gi">' + mobs(1, 'boss') + '</div><b class="qy">Докмастер</b><span>Defias Dockmaster</span></div>'
     '<div class="gp" data-fx="pop" data-mark="b">+</div>'
     '<div class="gc" data-fx="pop" data-mark="b" data-at=".1"><div class="gi">' + mobs(3, 'mobg') + '</div><b>3 охраны</b></div></div></div>',
     '<div class="abs" style="left:110px;top:560px"><div class="chip wp" data-fx="up" data-mark="c">' + ico('i-mob') + '<b class="qy">7</b> мобов в одной пачке</div></div>',
     ST('16_come', 1450, 420, 440, frm='right', mark='b', at=.3, rot=-5)], stage=0)

# 4. Маг 20 — не соперники; еле успеваю облутаться → таймер; запись ускорена
sec('4. Маг 20 ур. не соперники → еле успеваю облутаться → запись ускорена',
    [V(64), '<div class="abs" style="left:110px;top:220px"><div class="chip wp" data-fx="left" data-at=".2">' + ico('i-arc', 'arc') + 'МАГ <b class="qy">20</b> УР.: <span class="q2">изи</span></div></div>',
     ST('15_easy', 1450, 420, 440, frm='right', at=.6, rot=-5)],
    [V(100.5), '<div class="abs" style="left:120px;top:220px">' + TIMER(12, 2.6, 'до респавна', ' data-mark="a"') + '</div>',
     '<div class="abs" style="left:470px;top:270px"><div class="h2" data-fx="left" data-mark="a" data-at=".3" style="text-align:left">ЕЛЕ УСПЕВАЮ<br><em>ОБЛУТАТЬСЯ</em></div></div>',
     '<div class="abs" style="left:120px;top:600px"><div class="chip wp sm" data-fx="up" data-mark="b">⏩ запись ускорена ×2.5</div></div>',
     ST('03_respawn', 1450, 420, 440, frm='right', mark='a', at=.8, rot=-4)])

# 5. Лут: гуманоиды → окно добычи → лён дождём
sec('5. Глава «Добыча»: ткань, серое, зелёнка, свитки, ящики',
    [V(136), ZONE('ДОБЫЧА', 'что падает с гуманоидов', 2.0), ST('02_loot', 1450, 420, 440, frm='right', at=1.4, rot=-5)],
    [V(140), '<div class="abs" style="left:110px;top:170px"><div class="loot wp" data-fx="up" data-at="0" data-sfx="bagopen">'
     '<div class="ph">ДОБЫЧА</div>'
     '<div class="li" data-fx="left" data-at=".2" data-sfx="wcoin">' + ico('i-linen') + '<span class="q1">Льняная ткань</span></div>'
     '<div class="li" data-fx="left" data-mark="b">' + ico('i-grey') + '<span class="q0">Серые вещи</span></div>'
     '<div class="li" data-fx="left" data-mark="c" data-sfx="wcoin">' + ico('i-green', 'gr') + '<span class="q2">Зелёнка</span></div>'
     '<div class="li" data-fx="left" data-mark="d">' + ico('i-scroll') + '<span class="q1">Свитки и ящики</span></div></div></div>',
     '<div class="rain" data-fx="rain" data-img="linen" data-n="16" data-mark="e"></div>',
     ST('01_rich', 1450, 420, 440, frm='right', mark='c', at=.2, rot=-5)], stage=1)

# 6. Нюансы: здоровье тает (ешь) → сумки за 5-10 мин → Dejunk + 1 кнопка
sec('6. Глава «Нюансы»: здоровье тает → сумки за 5-10 мин → аддон Dejunk',
    [V(36), ZONE('НЮАНСЫ', 'мана, здоровье, сумки', 1.6),
     '<div class="abs" style="left:110px;top:420px"><div class="bars wp" data-fx="up" data-mark="a" data-at="-.3">'
     '<div class="br"><span>МАНА</span><div class="tr"><i class="mp"></i></div><em class="q3">не проблема</em></div>'
     '<div class="br" data-fx="left" data-mark="b" data-at="-.2"><span>ЗДОРОВЬЕ</span><div class="tr"><i class="hp" data-fx="grow" data-w="96,34" data-mark="b" data-at=".3"></i></div><em style="color:#ff6b5b">тает</em></div></div></div>',
     ST('08_eat', 1450, 420, 440, frm='right', mark='b', at=.6, rot=-4)],
    [V(152, 1, roi='0,0,1 .45,.2,.55'), '<div class="abs" style="left:110px;top:230px"><div class="chip wp" data-fx="left" data-at=".3" data-sfx="bagopen">' + ico('i-bag') + 'сумки полные за <b class="qy">5-10 мин</b></div></div>',
     ST('05_bags', 110, 420, 440, frm='left', at=.7, rot=4)],
    [V(128.2, .8, roi='0,0,1 .19,.12,.62'), '<div class="abs" style="left:1120px;top:190px"><div class="chip wp sm" data-fx="right" data-at=".4">' + ico('i-bag') + 'аддон <b class="qy">Dejunk</b></div></div>',
     '<div class="abs" style="left:1120px;top:330px"><div class="chip wp sm" data-fx="right" data-mark="c">' + ico('i-key') + '1 кнопка: <b class="q0">серое</b> в мусор</div></div>',
     ST('09_trash', 1460, 470, 400, frm='right', mark='c', at=.4, rot=-4)], stage=2)

# 7. Boosty в середине: сундук на цепях → замок трескается → секретные листки → карточка Boosty
sec('7. Boosty (середина ролика): сундук с запретными методами → ссылка',
    [V(117.3, 1, cls='soft'), '<div class="row" style="top:150px"><div class="h2" data-fx="up" data-at=".2">ЗАПРЕТНЫЕ МЕТОДЫ <em>ГОЛДФАРМА</em></div></div>',
     '<div class="chest" data-fx="chest" data-crack="a" data-at=".4" style="left:760px;top:330px">'
     '<div class="rays"></div><svg class="cbody" viewBox="0 0 400 300"><use href="#chest"/></svg><svg class="lid" viewBox="0 0 400 160"><use href="#chestlid"/></svg>'
     '<svg class="chain c1" viewBox="0 0 60 360"><use href="#chain"/></svg><svg class="chain c2" viewBox="0 0 60 360"><use href="#chain"/></svg>'
     '<svg class="lock" viewBox="0 0 100 120"><use href="#lock"/></svg></div>',
     '<div class="page" data-fx="fly" data-mark="b" data-dx="-520" data-rot="-8" style="left:250px;top:330px"><i></i><i></i><i class="s"></i><i></i><i class="s"></i><i></i><b>ЗАСЕКРЕЧЕНО</b></div>',
     '<div class="page" data-fx="fly" data-mark="b" data-at=".25" data-dx="520" data-rot="7" style="left:1280px;top:350px"><i></i><i class="s"></i><i></i><i></i><i class="s"></i><i></i><b>ЗАСЕКРЕЧЕНО</b></div>'],
    [V(44, 1, cls='soft'), '<div class="abs" style="left:110px;top:200px">' + BOOSTY('запретные методы голдфарма') + '</div>',
     ST('12_forbidden', 1450, 400, 460, frm='right', at=.6, rot=-5)], trans='portal')

# 8. Низкий уровень: маг 12 + Чародейский взрыв → до 15-го + голда → тактика без патруля
sec('8. Глава «Низкий уровень»: Чародейский взрыв → тактика без патруля',
    [V(164, 1.2), ZONE('НИЗКИЙ УРОВЕНЬ', 'маг с 12 уровня', 1.8)],
    [V(196), '<div class="abs" style="left:110px;top:200px"><div class="chip wp" data-fx="left" data-at=".2">' + ico('i-arc', 'arc') + '<span><small>маг 12 ур.</small>Чародейский взрыв</span></div></div>',
     '<div class="abs" style="left:110px;top:380px"><div class="lvl wp" data-fx="left" data-mark="a" data-sfx="levelup"><span>УР. <b data-count="12,15">12</b></span><div class="tr"><i data-fx="grow" data-w="8,92" data-mark="a" data-at=".2"></i></div></div></div>',
     '<div class="rain" data-fx="rain" data-n="14" data-mark="b"></div>',
     ST('11_lvlup', 1450, 400, 460, frm='right', mark='a', at=.3, rot=-5)],
    [V(188), '<div class="abs" style="left:110px;top:170px"><div class="tact wp" data-fx="up" data-at=".05"><div class="ph">ТАКТИКА НА 12 УРОВНЕ</div>'
     '<div class="ti no" data-fx="left" data-at=".25">' + mobs(3) + '<span>бродячую группу <b>пропускай</b></span><em>✕</em></div>'
     '<div class="ti ok" data-fx="left" data-mark="c">' + mobs(1, 'boss') + mobs(3, 'mobg') + '<span>Докмастер и охрана</span><em>✓</em></div>'
     '<div class="ti" data-fx="left" data-mark="d"><i class="arw">↩</i><span>идёт патруль: <b>отойди назад</b></span></div></div></div>',
     ST('06_boom', 1450, 430, 440, frm='right', mark='c', at=.3, rot=-4)], stage=3)

# 9. Таланты (Чародейская сосредоточенность) → шмот: рандомная зелёнка, жду кап 30
sec('9. Таланты → шмот: обычная зелёнка, жду кап 30',
    [V(171.3, .35, roi='0,0,1 .14,0,.72'), '<div class="abs" style="left:1180px;top:560px"><div class="tip" data-fx="right" data-at=".5"><div class="qy" style="font:900 44px/1.1 Aleg">Чародейская<br>сосредоточенность</div><div>держит ману на пуллах</div></div></div>'],
    [V(175.8, .45, roi='0,0,1 0,.03,.55'), '<div class="abs" style="left:1130px;top:220px"><div class="tip" data-fx="right" data-at=".3"><div class="q2" style="font:900 52px/1.1 Aleg">[Рандомная зелёнка]</div><div class="q0">ничего не собирала под фарм</div></div></div>',
     '<div class="abs" style="left:1130px;top:420px"><div class="chip wp" data-fx="right" data-mark="c">' + ico('i-hg') + 'жду кап <b class="qy">30</b></div></div>',
     ST('13_green', 1480, 520, 380, frm='right', mark='b', at=.2, rot=-4)])

# 10. Где точка: экран загрузки → карта, южнее Голдшира, граница с Сумеречным лесом
sec('10. Глава «Где точка»: южнее Голдшира, на границе с Сумеречным лесом',
    [V(166, 1.1), ZONE('ГДЕ ЭТА ТОЧКА', 'обещанное', 1.6), ST('04_secret', 1450, 420, 440, frm='right', at=1.0, rot=-5)],
    [V(180, .7, roi='0,0,1 .315,.66,.34', zd=1.6), '<div class="pin" data-fx="zoom" data-at="1.5" data-sfx="questdone" style="left:960px;top:730px"><i></i><i></i></div>',
     '<div class="abs" style="left:1200px;top:240px"><div class="chip wp" data-fx="right" data-at="1.2">' + ico('i-map') + 'южнее <b class="qy">Голдшира</b></div></div>',
     '<div class="abs" style="left:1200px;top:400px"><div class="chip wp" data-fx="right" data-mark="a"><span><small>граница с</small>Сумеречным лесом</span></div></div>',
     '<div class="abs" style="left:1200px;top:560px"><div class="chip wp sm" data-fx="right" data-mark="b">📌 сохрани видео</div></div>',
     ST('17_map', 60, 440, 420, frm='left', at=1.6, rot=5)], trans='load', stage=4,
    hint='Подсказка: гиперспавн-точка южнее Голдшира, на границе с Сумеречным лесом.')

# 11. Удивило: в классике гиперспавн у одной группы, здесь у обеих; 10-12 с
sec('11. Раньше гиперспавн у одной группы, сейчас у обеих, 10-12 сек',
    [V(208), '<div class="row" style="top:150px"><div class="h2" data-fx="up" data-at=".2">И ВОТ ЧТО <em>МЕНЯ УДИВИЛО</em></div></div>',
     ST('19_timer', 1450, 420, 440, frm='right', at=.7, rot=-5)],
    [V(216), '<div class="abs" style="left:110px;top:180px"><div class="cmp">'
     '<div class="wp old" data-fx="left" data-at=".05"><div class="ph">РАНЬШЕ · КЛАССИКА</div><div class="cr">' + mobs(3) + '<em class="q2">⟳</em></div><div class="cr">' + mobs(3) + '<em style="color:#ff6b5b">✕</em></div></div>'
     '<div class="vs">VS</div>'
     '<div class="wp new" data-fx="right" data-mark="a"><div class="ph">СЕЙЧАС · FOREVER</div><div class="cr">' + mobs(3) + '<em class="q2">⟳</em></div><div class="cr">' + mobs(3) + '<em class="q2">⟳</em></div></div></div></div>',
     '<div class="abs" style="left:1500px;top:560px">' + TIMER(12, 2.4, '10-12 сек', ' data-mark="b"') + '</div>'], trans='portal')

# 12. Финал: задание выполнено → Boosty (ссылка) + подписка
sec('12. Финал: задание выполнено → Boosty (ссылка) + подписка',
    [V(240), '<div class="row" style="top:170px"><div class="banner" data-fx="zoom" data-at=".05" data-sfx="questdone">ЗАДАНИЕ ВЫПОЛНЕНО</div></div>',
     '<div class="abs" style="left:110px;top:400px"><div class="quest done" data-fx="up" data-at=".4"><div class="qo"><i>✓</i>Точка на карте <b>1/1</b></div><div class="qo"><i>✓</i>Фарм с 12 уровня <b>1/1</b></div></div></div>',
     ST('20_gg', 1450, 420, 440, frm='right', at=.6, rot=-5)],
    [V(250, 1, cls='soft'), '<div class="abs" style="left:110px;top:170px" id="guide">' + BOOSTY('запретные методы голдфарма') + '</div>',
     '<div class="abs" style="left:110px;top:640px"><div class="subbtn" id="cta" data-fx="pop" data-mark="b">ПОДПИШИСЬ ✦</div></div>',
     ST('18_sub', 1450, 400, 460, fx='plop', mark='b', at=.1)])

CSS = open(os.path.join(ROOT, 'tools', 'wow_style.css'), encoding='utf-8').read()
DEFS = open(os.path.join(ROOT, 'tools', 'wow_defs.svg'), encoding='utf-8').read()
html = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>WoW Forever: голдфарм-точка с гиперспавном (Аня, 16:9)</title>
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
      <div class="qss"><span class="qs">Точка</span><span class="qs">Добыча</span><span class="qs">Нюансы</span><span class="qs">12 уровень</span><span class="qs">Карта</span></div></div>
  </div>
  <div id="dip"></div>
  <div id="portal"></div>
  <div id="load"><img src="assets/video/wowfarm/f_0121.jpg" alt=""><div class="lshade"></div><img class="llogo" src="assets/wow/logo.png" alt="">
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
