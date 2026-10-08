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
def sec(comment, *layers, trans=''):
    t = f' data-trans="{trans}"' if trans else ''
    NL, HID = '\n', ' style="opacity:0"'
    body = ''.join(f'{NL}      <div class="layer {chr(65 + k)}"{HID if k else ""}>{NL}        ' + (NL + '        ').join(l) + f'{NL}      </div>' for k, l in enumerate(layers))
    SECS.append(f'    <!-- {comment} -->\n    <section class="sec" id="s{len(SECS) + 1}"{t}>{body}\n    </section>')

# 1. Хук: 7 мобов, респавн 10 с → пусто, ни одного фармера → почему все пропускают?
sec('1. Хук: 7 мобов, респавн 10 сек → ни одного фармера → почему?',
    [V(79.5), '<div class="abs" style="left:120px;top:250px"><div class="h1 hk hkx" data-fx="punch" style="font-size:190px;text-align:left">7 МОБОВ</div></div>',
     '<div class="abs hk" style="left:130px;top:470px"><div class="chip wp">' + ico('i-hg') + 'РЕСПАВН — <b class="qy">10 СЕК</b></div></div>'],
    [V(2, 1.4), '<div class="row" style="top:300px"><div class="stamp" data-fx="slam" data-at=".15">0 ФАРМЕРОВ</div></div>',
     ST('07_nobody', 1440, 440, 440, frm='right', at=.4, rot=-6)],
    [V(88), '<div class="row" style="top:150px"><div class="h1" data-fx="kin" style="font-size:96px;line-height:1.1">ПОЧЕМУ ЕЁ<br><em>ВСЕ ПРОПУСКАЮТ?</em></div></div>',
     ST('04_secret', 60, 470, 420, frm='left', at=.3, rot=6)])

# 2. Привет, я Аня + логотип → «квест»: досмотри до конца (карта, фарм с 12 уровня)
sec('2. Я Аня · голдфарм-точка в Форевер → квест «досмотри до конца»',
    [V(6, 1, cls='dim'), '<div class="row" style="top:150px"><img class="logo" data-fx="zoom" data-at=".05" src="assets/wow/logo.png" alt="" style="width:560px"></div>',
     '<div class="row" style="top:640px"><div class="h2" data-fx="kin" style="font-size:66px">ГОЛДФАРМ-ТОЧКА,<br>КОТОРУЮ <em>НИКТО НЕ ТРОГАЕТ</em></div></div>',
     ST('20_gg', 1460, 300, 400, frm='right', at=.6, rot=-5)],
    [V(30, 1, cls='dim'), '<div class="abs" style="left:300px;top:190px"><div class="quest" data-fx="up" data-at=".05">'
     '<div class="qh">❗ НОВОЕ ЗАДАНИЕ</div><div class="qt">Досмотри до конца</div>'
     '<div class="qo" data-fx="left" data-mark="a"><i>◆</i>Точка на карте <b>0/1</b></div>'
     '<div class="qo" data-fx="left" data-mark="b"><i>◆</i>Фарм с 12 уровня <b>0/1</b></div>'
     '<div class="qr2">Награда: <span class="qy">● голда</span> и <span class="q2">[зелёнка]</span></div></div></div>',
     ST('11_lvlup', 1300, 240, 460, fx='plop', mark='b', at=.1)])

# 3. Boosty: запретные методы голдфарма → карточка с QR
sec('3. Вставка Boosty: запретные методы голдфарма + QR',
    [V(117.3, 1, cls='red'), '<div class="row" style="top:200px"><div class="h1" data-fx="kin" style="font-size:118px;line-height:1.05">ЗАПРЕТНЫЕ МЕТОДЫ<br><em>ГОЛДФАРМА</em></div></div>',
     '<div class="row" style="top:560px"><div class="stamp" data-fx="slam" data-at=".7" style="font-size:72px">НЕ ДЛЯ ЮТУБА</div></div>',
     ST('12_forbidden', 1470, 380, 420, fx='plop', at=.5)],
    [V(44, 1, cls='dim'), '<div class="abs" style="left:250px;top:150px"><div class="bcard wp" data-fx="up" data-at=".05">'
     '<div class="qrbox" data-fx="zoom" data-at=".35" data-react="b"><svg class="qrsvg"></svg></div>'
     '<div class="bt"><div class="kicker">только у меня на</div><div class="bname" data-fx="pop" data-at=".2" data-react="a">BOOSTY</div>'
     '<div class="blink">boosty.to/<b>anna_rich</b></div><div class="bsub">запретные методы голдфарма</div>'
     '<div class="chip wp sm" data-fx="pop" data-mark="b" data-at=".2">⬇ ссылка в описании</div></div></div></div>',
     ST('01_rich', 1480, 380, 400, frm='right', mark='a', at=.1, rot=-4)])

# 4. Точка: гиперспавн 7 гуманоидов = 3 бродят + Докмастер + 3 охраны
sec('4. Гиперспавн: 3 бродят + Докмастер зовёт 3 охраны = 7 в пачке',
    [V(20), '<div class="abs" style="left:110px;top:220px"><div class="kicker" data-fx="pop">итак, точка</div></div>',
     '<div class="abs" style="left:100px;top:270px"><div class="h1" data-fx="slam" data-at=".25" style="font-size:150px">ГИПЕРСПАВН</div></div>',
     '<div class="abs" style="left:120px;top:470px"><div class="chip wp" data-fx="left" data-at=".8">' + ico('i-mob') + '<b class="qy" data-count="0,7">0</b> ГУМАНОИДОВ</div></div>'],
    [V(50, 1, cls='dim'), '<div class="row" style="top:200px"><div class="grp wp" data-fx="up" data-at=".05">'
     '<div class="gc" data-fx="pop" data-at=".25"><div class="gi">' + mobs(3) + '</div><b>3 бродят</b></div>'
     '<div class="gp" data-fx="pop" data-mark="a">+</div>'
     '<div class="gc" data-fx="zoom" data-mark="a" data-at=".1"><div class="gi">' + mobs(1, 'boss') + '</div><b class="qy">Докмастер</b><span>Defias Dockmaster</span></div>'
     '<div class="gp" data-fx="pop" data-mark="b">→</div>'
     '<div class="gc" data-fx="pop" data-mark="b" data-at=".1"><div class="gi">' + mobs(3, 'mobg') + '</div><b>+3 охраны</b></div></div></div>',
     ST('16_come', 1480, 470, 400, frm='right', mark='b', at=.2, rot=-6)],
    [V(196.3), '<div class="abs" style="left:110px;top:230px"><div class="h1" data-fx="slam" data-at=".2" style="font-size:300px;line-height:.9">7</div></div>',
     '<div class="abs" style="left:330px;top:300px"><div class="h2" data-fx="left" data-at=".45" style="text-align:left">МОБОВ<br><em>В ОДНОЙ ПАЧКЕ</em></div></div>'])

# 5. Маг 20 — изи; еле успеваю облутаться → таймер; ускоренная запись ×2.5
sec('5. Маг 20 ур. — изи → еле успеваю облутаться → запись ускорена',
    [V(64), '<div class="abs" style="left:120px;top:240px"><div class="chip wp" data-fx="left" data-at=".1">' + ico('i-arc', 'arc') + 'МАГ <b class="qy">20</b> УР.</div></div>',
     '<div class="abs" style="left:120px;top:400px"><div class="h1" data-fx="slam" data-at=".6" style="font-size:110px">НЕ СОПЕРНИКИ</div></div>',
     ST('15_easy', 1460, 420, 420, frm='right', at=.5, rot=-5)],
    [V(100.5), '<div class="abs" style="left:160px;top:230px"><div class="timer" data-fx="timer" data-n="12" data-d="2.4" data-mark="a"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" class="bgc"/><circle cx="100" cy="100" r="84" class="ring" pathLength="1"/></svg><b>12</b><span>до респавна</span></div></div>',
     '<div class="abs" style="left:520px;top:290px"><div class="h2" data-fx="left" data-mark="a" data-at=".3" style="text-align:left">ЕЛЕ УСПЕВАЮ<br><em>ОБЛУТАТЬСЯ</em></div></div>',
     ST('03_respawn', 1440, 430, 440, frm='right', mark='a', at=.9, rot=-4)],
    [V(108, 1, roi='0,0,1 .355,0,.35'), '<div class="row" style="top:560px"><div class="stamp" data-fx="slam" data-at=".9" style="font-size:70px">ЗАПИСЬ УСКОРЕНА</div></div>'])

# 6. Лут: гуманоиды → окно добычи → лён дождём
sec('6. Лут гуманоидов: ткань, серое, зелёнка, свитки, ящики',
    [V(136), '<div class="abs" style="left:110px;top:240px"><div class="h1" data-fx="kin" style="font-size:112px;text-align:left;line-height:1.05">ГУМАНОИДЫ<br><em>= ЛУТ</em></div></div>',
     ST('02_loot', 1440, 400, 440, frm='right', at=.4, rot=-5)],
    [V(140, 1, cls='dim'), '<div class="abs" style="left:420px;top:150px"><div class="loot wp" data-fx="up" data-at="0">'
     '<div class="ph">ДОБЫЧА</div>'
     '<div class="li" data-fx="left" data-at=".15">' + ico('i-linen') + '<span class="q1">Льняная ткань</span></div>'
     '<div class="li" data-fx="left" data-mark="b">' + ico('i-grey') + '<span class="q0">Серые вещи</span></div>'
     '<div class="li" data-fx="left" data-mark="c">' + ico('i-green', 'gr') + '<span class="q2">Зелёнка</span></div>'
     '<div class="li" data-fx="left" data-mark="d">' + ico('i-scroll') + '<span class="q1">Свитки</span></div>'
     '<div class="li" data-fx="left" data-mark="e">' + ico('i-crate') + '<span class="q1">Ящики</span></div></div></div>',
     ST('14_crate', 1460, 440, 420, frm='right', mark='d', at=.2, rot=-5)],
    [V(150, 1, roi='0,0,1 .53,.45,.4'), '<div class="abs" style="left:100px;top:240px"><div class="h1" data-fx="kin" style="font-size:104px;text-align:left;line-height:1.05">ТКАНЬ<br><em>СЫПЛЕТСЯ</em><br>ДОЖДЁМ</div></div>',
     '<div class="rain" data-fx="rain" data-img="linen" data-n="22" data-at=".3"></div>',
     ST('10_linen', 600, 430, 420, frm='bottom', at=.6)])

# 7. Два нюанса: здоровье тает (ешь) → сумки за 5–10 мин → Dejunk + 1 кнопка
sec('7. Нюансы: здоровье тает → сумки за 5–10 мин → аддон Dejunk',
    [V(36), '<div class="abs" style="left:110px;top:220px"><div class="kicker" data-fx="pop">нюанс №1</div></div>',
     '<div class="abs" style="left:110px;top:280px"><div class="bars wp" data-fx="up" data-at=".2">'
     '<div class="br" data-fx="left" data-mark="a"><span>МАНА</span><div class="tr"><i class="mp"></i></div><em class="q3">не проблема</em></div>'
     '<div class="br" data-fx="left" data-mark="b" data-at="-.2"><span>ЗДОРОВЬЕ</span><div class="tr"><i class="hp" data-fx="grow" data-w="96,34" data-mark="b" data-at=".3"></i></div><em style="color:#ff6b5b">тает</em></div></div></div>',
     ST('08_eat', 1450, 420, 420, frm='right', mark='b', at=.6, rot=-4)],
    [V(152, 1, roi='0,0,1 .55,.25,.45'), '<div class="abs" style="left:110px;top:220px"><div class="kicker" data-fx="pop">нюанс №2</div></div>',
     '<div class="abs" style="left:100px;top:270px"><div class="h1" data-fx="kin" style="font-size:112px;text-align:left;line-height:1.05">СУМКИ<br><em>ЗА 5–10 МИН</em></div></div>',
     ST('05_bags', 160, 500, 400, frm='bottom', at=.6)],
    [V(128.2, .8, roi='0,0,1 .19,.12,.62'), '<div class="abs" style="left:1120px;top:190px"><div class="chip wp sm" data-fx="right" data-at=".5">' + ico('i-bag') + 'аддон <b class="qy">Dejunk</b></div></div>',
     '<div class="abs" style="left:1120px;top:330px"><div class="chip wp sm" data-fx="right" data-mark="c">' + ico('i-key') + '1 кнопка → <b class="q0">серое</b> в мусор</div></div>',
     ST('09_trash', 1480, 470, 400, fx='plop', mark='c', at=.4)])

# 8. Низкий уровень: маг 12 + Чародейский взрыв → до 15-го + голда → тактика: без патруля
sec('8. Фарм с 12 уровня: Чародейский взрыв → тактика без патруля',
    [V(164, 1.3, cls='dim'), '<div class="row" style="top:250px"><div class="h1" data-fx="kin" style="font-size:130px;line-height:1.05">А ТЕПЕРЬ —<br><em>НИЗКИЙ УРОВЕНЬ</em></div></div>'],
    [V(196), '<div class="abs" style="left:110px;top:220px"><div class="chip wp" data-fx="left" data-at=".1">' + ico('i-arc', 'arc') + '<span><small>маг 12 ур.</small>Чародейский взрыв</span></div></div>',
     '<div class="abs" style="left:110px;top:400px"><div class="lvl wp" data-fx="left" data-mark="a"><span>УР. <b data-count="12,15">12</b></span><div class="tr"><i data-fx="grow" data-w="8,92" data-mark="a" data-at=".2"></i></div></div></div>',
     '<div class="rain" data-fx="rain" data-n="20" data-mark="b"></div>',
     ST('06_boom', 1450, 400, 440, frm='right', at=.5, rot=-5)],
    [V(188, 1, cls='dim'), '<div class="abs" style="left:250px;top:170px"><div class="tact wp" data-fx="up" data-at=".05"><div class="ph">ТАКТИКА НА 12 УРОВНЕ</div>'
     '<div class="ti no" data-fx="left" data-at=".25">' + mobs(3) + '<span>бродячую группу — <b>пропускай</b></span><em>✕</em></div>'
     '<div class="ti ok" data-fx="left" data-mark="c">' + mobs(1, 'boss') + mobs(3, 'mobg') + '<span>Докмастер + охрана</span><em>✓</em></div>'
     '<div class="ti" data-fx="left" data-mark="d"><i class="arw">↩</i><span>идёт патруль — <b>отойди назад</b></span></div></div></div>',
     ST('13_green', 1480, 470, 400, frm='right', mark='c', at=.3, rot=-4)])

# 9. Таланты (Чародейская сосредоточенность) → шмот: рандомная зелёнка, жду кап 30
sec('9. Таланты → шмот: обычная зелёнка, жду кап 30',
    [V(171.3, .35, roi='0,0,1 .14,0,.72'), '<div class="abs" style="left:1180px;top:560px"><div class="tip" data-fx="right" data-at=".4"><div class="qy" style="font:900 44px/1.1 Aleg">Чародейская<br>сосредоточенность</div><div>держит ману на пуллах</div></div></div>'],
    [V(175.8, .45, roi='0,0,1 0,.03,.55'), '<div class="abs" style="left:1130px;top:220px"><div class="tip" data-fx="right" data-at=".2"><div class="q2" style="font:900 52px/1.1 Aleg">[Рандомная зелёнка]</div><div class="q0">ничего не собирала под фарм</div></div></div>',
     '<div class="abs" style="left:1130px;top:420px"><div class="chip wp" data-fx="right" data-mark="c">' + ico('i-hg') + 'жду кап <b class="qy">30</b></div></div>',
     ST('19_timer', 1500, 520, 360, frm='right', mark='c', at=.3, rot=-4)])

# 10. Где точка: южнее Голдшира, граница с Сумеречным лесом
sec('10. Карта: южнее Голдшира, на границе с Сумеречным лесом',
    [V(166, 1.2, cls='dim'), '<div class="row" style="top:260px"><div class="h1" data-fx="kin" style="font-size:150px">ГДЕ ЭТА ТОЧКА?</div></div>'],
    [V(180, .7, roi='0,0,1 .315,.66,.34', zd=1.6), '<div class="pin" data-fx="zoom" data-at="1.5" style="left:960px;top:730px"><i></i><i></i></div>',
     '<div class="abs" style="left:1200px;top:240px"><div class="chip wp" data-fx="right" data-at="1.2">' + ico('i-map') + 'южнее <b class="qy">Голдшира</b></div></div>',
     '<div class="abs" style="left:1200px;top:400px"><div class="chip wp" data-fx="right" data-mark="a"><span><small>граница с</small>Сумеречным лесом</span></div></div>',
     ST('17_map', 60, 440, 420, frm='left', at=1.6, rot=5)],
    [V(204), '<div class="row" style="top:300px"><div class="h1" data-fx="slam" data-at=".1" style="font-size:150px">СОХРАНИ ВИДЕО</div></div>',
     '<div class="row" style="top:520px"><div class="chip wp" data-fx="pop" data-at=".5">📌 чтобы не потерять</div></div>'])

# 11. Удивило: в классике гиперспавн был у одной группы, здесь — у обеих; 10–12 с
sec('11. Раньше гиперспавн у одной группы — сейчас у обеих, 10–12 сек',
    [V(208), '<div class="row" style="top:260px"><div class="h1" data-fx="kin" style="font-size:130px;line-height:1.05">И ВОТ ЧТО<br><em>МЕНЯ УДИВИЛО</em></div></div>'],
    [V(216, 1, cls='dim'), '<div class="abs" style="left:230px;top:200px"><div class="cmp">'
     '<div class="wp old" data-fx="left" data-at=".05"><div class="ph">РАНЬШЕ · КЛАССИКА</div><div class="cr">' + mobs(3) + '<em class="q2">⟳</em></div><div class="cr">' + mobs(3) + '<em style="color:#ff6b5b">✕</em></div></div>'
     '<div class="vs">VS</div>'
     '<div class="wp new" data-fx="right" data-mark="a"><div class="ph">СЕЙЧАС · FOREVER</div><div class="cr">' + mobs(3) + '<em class="q2">⟳</em></div><div class="cr">' + mobs(3) + '<em class="q2">⟳</em></div></div></div></div>'],
    [V(230), '<div class="abs" style="left:160px;top:220px"><div class="timer" data-fx="timer" data-n="12" data-d="2.2" data-at=".1"><svg viewBox="0 0 200 200"><circle cx="100" cy="100" r="84" class="bgc"/><circle cx="100" cy="100" r="84" class="ring" pathLength="1"/></svg><b>12</b><span>и снова тут</span></div></div>',
     '<div class="abs" style="left:520px;top:280px"><div class="h1" data-fx="slam" data-at=".5" style="font-size:150px">10–12 СЕК</div></div>',
     ST('16_come', 1460, 430, 420, frm='right', at=.8, rot=-5)])

# 12. Финал: попробуй точку (квест выполнен) → Boosty с QR + подписка
sec('12. Финал: квест выполнен → Boosty (QR) + подписка',
    [V(240), '<div class="row" style="top:190px"><div class="banner" data-fx="zoom" data-at=".05">ЗАДАНИЕ ВЫПОЛНЕНО</div></div>',
     '<div class="abs" style="left:520px;top:400px"><div class="quest done" data-fx="up" data-at=".4"><div class="qo"><i>✓</i>Точка на карте <b>1/1</b></div><div class="qo"><i>✓</i>Фарм с 12 уровня <b>1/1</b></div></div></div>',
     ST('20_gg', 1460, 420, 420, frm='right', at=.6, rot=-5)],
    [V(250, 1, cls='dim'), '<div class="abs" style="left:150px;top:130px" id="guide"><div class="bcard wp big" data-fx="up" data-at=".05">'
     '<div class="qrbox" data-fx="zoom" data-at=".3"><svg class="qrsvg"></svg></div>'
     '<div class="bt"><div class="kicker">запретные методы голдфарма</div><div class="bname" data-fx="pop" data-mark="a">BOOSTY</div>'
     '<div class="blink">boosty.to/<b>anna_rich</b></div>'
     '<div class="chip wp sm" id="cta" data-fx="pop" data-mark="b">⬇ ссылка в описании</div></div></div></div>',
     '<div class="abs" style="left:150px;top:690px"><div class="subbtn" data-fx="pop" data-mark="c">▶ ПОДПИСАТЬСЯ</div></div>',
     ST('18_sub', 1450, 400, 440, fx='plop', mark='c', at=.1)])

CSS = open(os.path.join(ROOT, 'tools', 'wow_style.css'), encoding='utf-8').read()
DEFS = open(os.path.join(ROOT, 'tools', 'wow_defs.svg'), encoding='utf-8').read()
html = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>WoW Forever — голдфарм-точка с гиперспавном (Аня, 16:9)</title>
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

  <canvas id="embers" width="1920" height="1080"></canvas>
  <canvas id="fx" width="1920" height="1080"></canvas>
  <div id="hud">
    <div id="uf"><div class="pt"><img src="assets/wow/avatar.jpg" alt=""></div>
      <div class="ufr"><div class="nm">Аня <span>anna_rich</span></div><div class="bar hp"><i></i></div><div class="bar mp"><i></i></div></div></div>
    <img id="logo" src="assets/wow/logo.png" alt="">
  </div>
  <canvas id="grain" width="480" height="270"></canvas>
  <div id="flash"></div>
  <div id="subs"></div>
  <div id="fade"></div>
</div>
{DEFS}
<svg width="0" height="0" style="position:absolute"><filter id="mb" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur id="mbg" stdDeviation="0 0"/></filter></svg>

<script src="node_modules/gsap/dist/gsap.min.js"></script>
<script src="node_modules/lottie-web/build/player/lottie_svg.min.js"></script>
<script src="assets/wow/qr.js"></script>
<script src="assets/timeline.js"></script>
<script src="scene.js"></script>
</body>
</html>
'''
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
print('index.html:', len(SECS), 'сцен')
