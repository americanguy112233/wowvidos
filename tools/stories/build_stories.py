"""Статичные сторис для «Актуального» Ники: python tools/stories/build_stories.py → tools/stories/out/*.png
Стиль как в роликах: светлый фон, красный акцент, 3D-стикеры, «пластилиновые» иконки, рукописные пометки."""
import os, sys, subprocess, time, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'tools')); from clay_icons import DEFS, svg
T = lambda n: f'../../assets/nika/toon/{n}.png'
A = lambda n: f'../../assets/nika/{n}'

CSS = '''
@font-face { font-family: Unb; src: url(../../assets/fonts/Unbounded-VF.ttf); font-weight: 200 900; }
@font-face { font-family: Man; src: url(../../assets/fonts/Manrope-VF.ttf); font-weight: 200 800; }
@font-face { font-family: Hand; src: url(../../assets/fonts/Caveat-VF.ttf); font-weight: 400 700; }
:root { --bg:#f4f1ec; --ink:#121212; --muted:#8b857e; --red:#c8102e; --green:#1aa36b; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #ddd; font-family: Man; color: var(--ink); }
.st { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); margin-bottom: 40px; }
.st::before { content:''; position:absolute; inset:0; background: radial-gradient(60% 40% at 88% 10%, #fbdfe2 0, transparent 70%), radial-gradient(55% 35% at 8% 92%, #efe3cf 0, transparent 70%); }
.st.red { background: var(--red); } .st.red::before { background: radial-gradient(60% 40% at 80% 15%, rgba(255,255,255,.12) 0, transparent 70%); }
.ab { position: absolute; }
.row { position: absolute; left: 0; right: 0; display: flex; justify-content: center; align-items: center; }
.h1 { font: 900 104px/1.02 Unb; letter-spacing: -3px; text-align: center; } .h1 em, .h2 em { font-style: normal; color: var(--red); }
.h2 { font: 800 64px/1.1 Unb; letter-spacing: -1px; text-align: center; }
.red .h1, .red .h2 { color: #fff; } .red .h1 em { color: #121212; }
.kick { font: 800 32px/1 Unb; letter-spacing: 5px; color: var(--red); text-transform: uppercase; }
.red .kick { color: #fff; opacity: .8; }
.card { background: #fff; border-radius: 44px; box-shadow: 0 24px 60px rgba(60,40,20,.12); }
.tag { display: inline-block; font: 800 40px/1 Unb; padding: 24px 40px 26px; border-radius: 999px; background: var(--red); color: #fff; box-shadow: 0 14px 34px rgba(200,16,46,.3); white-space: nowrap; }
.tag.dark { background: var(--ink); box-shadow: 0 14px 34px rgba(0,0,0,.2); }
.tag.white { background: #fff; color: var(--ink); }
.hand { font: 700 70px/1 Hand; color: var(--red); white-space: nowrap; }
.red .hand { color: #fff; }
.tst { position: absolute; filter: drop-shadow(0 18px 30px rgba(60,40,20,.25)); }
.clay { display: block; filter: drop-shadow(0 22px 26px rgba(120,60,30,.22)); overflow: visible; }
.photo { position: absolute; border-radius: 48px; overflow: hidden; box-shadow: 0 30px 70px rgba(60,40,20,.25); border: 12px solid #fff; background: #fff; }
.photo img { display: block; width: 100%; height: 100%; object-fit: cover; }
.ph-tag { position: absolute; left: 50%; bottom: -34px; translate: -50% 0; }
.num { position: absolute; font: 900 600px/1 Unb; color: rgba(200,16,46,.07); letter-spacing: -30px; }
.red .num { color: rgba(255,255,255,.1); }
.ul { position: absolute; }
.bubble { position: relative; background: #fff; border-radius: 56px; padding: 44px 58px; box-shadow: 0 24px 60px rgba(60,40,20,.14); }
.bubble::after { content:''; position:absolute; left: 50%; bottom: -46px; margin-left: -40px; border: 40px solid transparent; border-top: 52px solid #fff; border-bottom: 0; }
.notes { width: 900px; padding: 46px 50px; background: #fff8dc; border-radius: 44px; box-shadow: 0 24px 60px rgba(60,40,20,.1); }
.notes .nh { font: 900 52px/1 Unb; padding-bottom: 20px; margin-bottom: 26px; border-bottom: 3px solid #f0e2b0; }
.notes .ni { display: flex; align-items: center; gap: 24px; font: 700 46px/1.2 Man; margin: 22px 0; }
.notes .ni i { width: 54px; height: 54px; border-radius: 14px; flex: none; display: flex; align-items: center; justify-content: center; font: 900 34px/1 Unb; font-style: normal; color: #fff; background: var(--red); }
.notes .ni.ok i { background: var(--green); }
.notes s { text-decoration: line-through 5px var(--red); color: #9a8f86; }
.give { width: 920px; padding: 34px 40px; display: flex; align-items: center; gap: 30px; margin: 0 auto 28px; }
.give b { display: block; font: 900 44px/1.1 Unb; } .give span { display: block; font: 600 32px/1.3 Man; color: var(--muted); margin-top: 10px; }
.give .ic { width: 180px; flex: none; display: flex; justify-content: center; }
.link { width: 860px; height: 240px; border-radius: 48px; border: 6px dashed rgba(200,16,46,.45); display: flex; align-items: center; justify-content: center; font: 700 34px/1.3 Man; color: rgba(200,16,46,.6); text-align: center; background: rgba(255,255,255,.5); }
.fact { width: 920px; padding: 40px 46px; }
.fact .k { font: 800 28px/1 Unb; letter-spacing: 4px; color: var(--muted); margin-bottom: 18px; }
.fact .t { font: 800 46px/1.2 Unb; } .fact .t em { font-style: normal; color: var(--red); }
.fix { width: 920px; padding: 34px 44px; background: var(--ink); color: #fff; border-radius: 44px; display: flex; gap: 26px; align-items: center; }
.fix i { width: 84px; height: 84px; border-radius: 50%; background: var(--green); flex: none; font: 900 46px/84px Unb; text-align: center; font-style: normal; }
.fix b { font: 800 40px/1.25 Unb; }
.errno { position: absolute; left: 70px; top: 230px; display: flex; align-items: center; gap: 18px; }
.errno span { font: 900 34px/1 Unb; color: #fff; background: var(--red); padding: 16px 26px; border-radius: 999px; }
.errno small { font: 800 30px/1 Unb; color: var(--muted); letter-spacing: 3px; }
.cmt { width: 900px; padding: 32px 36px; display: flex; align-items: center; gap: 26px; }
.cmt img { width: 104px; height: 104px; border-radius: 50%; object-fit: cover; }
.cmt .who { font: 700 30px/1 Man; color: var(--muted); margin-bottom: 12px; }
.cmt .txt { font: 900 78px/1 Unb; letter-spacing: 3px; }
.cmt .heart { margin-left: auto; font: 900 64px/1 Unb; color: var(--red); }
.steps { width: 920px; }
.step { display: flex; align-items: center; gap: 30px; padding: 34px 40px; margin-bottom: 24px; }
.step i { width: 100px; height: 100px; border-radius: 50%; background: var(--red); color: #fff; flex: none; font: 900 50px/100px Unb; text-align: center; font-style: normal; }
.step b { font: 800 42px/1.2 Unb; } .step span { display: block; font: 600 30px/1.3 Man; color: var(--muted); margin-top: 8px; }
.guide { width: 640px; height: 760px; padding: 56px 50px; display: flex; flex-direction: column; justify-content: space-between; background: var(--ink); color: #fff; border-radius: 48px; position: relative; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,.25); }
.guide > * { position: relative; z-index: 1; }
.guide .k { font: 800 30px/1 Unb; letter-spacing: 5px; color: #ff4a5e; }
.guide .t { font: 900 80px/1.02 Unb; letter-spacing: -2px; } .guide .t em { font-style: normal; color: #ff4a5e; }
.guide .b { display: flex; align-items: center; gap: 18px; font: 700 32px/1 Man; color: #cfc9c2; }
.guide .b img { width: 76px; height: 76px; border-radius: 50%; object-fit: cover; border: 3px solid #fff; }
.guide::before { content: ''; position: absolute; right: -150px; bottom: -150px; width: 420px; height: 420px; border-radius: 50%; background: var(--red); }
.loopc { position: relative; width: 760px; height: 760px; }
.node { position: absolute; translate: -50% -50%; background: #fff; border-radius: 999px; padding: 22px 36px 24px; font: 900 42px/1.05 Unb; text-align: center; white-space: nowrap; box-shadow: 0 16px 40px rgba(60,40,20,.14); }
.node.r { background: var(--red); color: #fff; }
.vs { width: 920px; padding: 40px 44px; }
.vrow { display: flex; align-items: center; gap: 24px; margin: 18px 0; }
.vrow .l { width: 250px; font: 800 40px/1 Unb; } .vrow .l small { display: block; font: 700 24px/1 Man; color: var(--muted); margin-top: 8px; }
.vrow .tr { flex: 1; height: 54px; border-radius: 27px; background: #f1ece6; overflow: hidden; } .vrow .fl { height: 100%; border-radius: 27px; }
.vrow .ar { width: 60px; font: 900 60px/1 Unb; text-align: center; }
.cover { width: 1080px; height: 1920px; }
.cover .disc { position: absolute; left: 140px; top: 560px; width: 800px; height: 800px; border-radius: 50%; background: #fff; box-shadow: 0 30px 80px rgba(60,40,20,.15); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; }
.cover .disc .w { font: 900 96px/1 Unb; letter-spacing: -2px; }
'''

def st(body, cls='', name=''):
    return f'<div class="st {cls}" data-name="{name}">{body}</div>'

S = []
# ======================= СТАРТ =======================
S.append(st(f'''
  <div class="row" style="top:250px"><div class="kick">привет 👋</div></div>
  <div class="row" style="top:320px"><div class="h1">Я <em>НИКА</em></div></div>
  <div class="photo" style="left:150px;top:500px;width:780px;height:975px;rotate:-2deg"><img src="{A('photo_after.jpg')}" style="object-position:50% 20%"></div>
  <img class="tst" src="{T('03_wink')}" style="right:-50px;top:1130px;width:380px;rotate:8deg">
  <div class="row" style="top:1580px"><div class="tag dark" style="font-size:34px">фитнес · питание · без голодовок</div></div>
''', name='start_1'))
S.append(st(f'''
  <div class="row" style="top:230px"><div class="h1" style="font-size:96px">МОЯ <em>ИСТОРИЯ</em></div></div>
  <div class="ab" style="left:30px;top:400px;width:1020px;height:1060px;border-radius:48px;overflow:hidden;box-shadow:0 30px 70px rgba(60,40,20,.22);background:#fff">
    <div class="ab" style="left:0;top:0;width:505px;height:1060px;overflow:hidden"><img src="{A('photo_before.jpg')}" style="width:100%;height:100%;object-fit:cover;object-position:46% 12%"></div>
    <div class="ab" style="left:515px;top:0;width:505px;height:1060px;overflow:hidden"><img src="{A('photo_after.jpg')}" style="width:100%;height:100%;object-fit:cover;object-position:26% 8%"></div>
  </div>
  <div class="ab" style="left:110px;top:1380px"><span class="tag white" style="font-size:46px">было</span></div>
  <div class="ab" style="left:650px;top:1380px"><span class="tag" style="font-size:46px">стало</span></div>
  <div class="ab" style="left:460px;top:840px;width:160px;height:160px;border-radius:50%;background:var(--red);box-shadow:0 18px 40px rgba(200,16,46,.4);display:flex;align-items:center;justify-content:center;font:900 86px/1 Unb;color:#fff">→</div>
  <div class="row" style="top:1520px"><div class="hand" style="rotate:-4deg;font-size:76px">без голодовок и срывов</div></div>
  <div class="row" style="top:1630px"><div class="h2" style="font-size:40px;color:var(--muted)">рассказываю, как это было ↓</div></div>
''', name='start_2'))
S.append(st(f'''
  <div class="row" style="top:250px"><div class="h1" style="font-size:84px">ЧТО Я <em>ПРОБОВАЛА</em></div></div>
  <div class="row" style="top:440px"><div class="notes">
    <div class="nh">Мои ошибки 🙈</div>
    <div class="ni"><i>✕</i><s>не есть до вечера</s></div>
    <div class="ni"><i>✕</i><s>безуглеводка</s></div>
    <div class="ni"><i>✕</i><s>«отрабатывать» срыв в зале</s></div>
    <div class="ni"><i>✕</i><s>спать по 5 часов</s></div>
    <div class="ni"><i>✕</i><s>не считать то, что пью</s></div></div></div>
  <div class="row" style="top:1230px"><div class="hand" style="rotate:-3deg">и вес возвращался снова и снова</div></div>
  <img class="tst" src="{T('08_sad')}" style="left:300px;top:1320px;width:480px">
''', name='start_3'))
S.append(st(f'''
  <div class="row" style="top:240px"><div class="h1" style="font-size:84px">ЧЕМ Я <em>ПОМОГУ</em></div></div>
  <div class="ab" style="left:0;right:0;top:440px">
    <div class="card give"><div class="ic">{svg('BOWL',180)}</div><div><b>Питание без голодовок</b><span>обычная еда, 4 приёма, без запретов</span></div></div>
    <div class="card give"><div class="ic">{svg('CAKE',170)}</div><div><b>Сушка без срывов</b><span>сладкое и праздники — не катастрофа</span></div></div>
    <div class="card give"><div class="ic">{svg('CLOCK',140)}</div><div><b>Режим, который держится</b><span>сон, вода, белок — без фанатизма</span></div></div>
  </div>
  <img class="tst" src="{T('10_cool')}" style="left:310px;top:1250px;width:460px">
''', name='start_4'))
S.append(st(f'''
  <div class="num" style="left:-40px;top:200px">→</div>
  <div class="row" style="top:300px"><div class="h1" style="font-size:110px">НАЧНИ<br><em>ЗДЕСЬ</em></div></div>
  <div class="row" style="top:600px"><div class="h2" style="font-size:44px;color:#fff;line-height:1.3">гайды, план питания<br>и всё, что мне помогло</div></div>
  <div class="row" style="top:860px"><div class="link" style="border-color:rgba(255,255,255,.7);color:#fff;background:rgba(255,255,255,.1)">сюда — стикер «Ссылка»<br>на сайт</div></div>
  <div class="row" style="top:1140px"><div class="hand" style="rotate:-4deg;font-size:84px">тапни 👆</div></div>
  <img class="tst" src="{T('02_happy')}" style="left:290px;top:1250px;width:500px">
''', cls='red', name='start_5'))

# ======================= ОШИБКИ =======================
S.append(st(f'''
  <div class="num" style="right:-60px;top:160px">5</div>
  <div class="row" style="top:300px"><div class="h1" style="font-size:100px">5 ОШИБОК,</div></div>
  <div class="row" style="top:420px"><div class="h2" style="font-size:66px">из-за которых<br>ты <em>не худеешь</em></div></div>
  <div class="row" style="top:640px"><div class="hand" style="rotate:-4deg">я делала все пять</div></div>
  <img class="tst" src="{T('01_shock')}" style="left:220px;top:760px;width:640px">
  <div class="row" style="top:1460px"><div class="tag dark">листай →</div></div>
''', name='err_0'))
def err(n, title, sub, body, sticker, fix, name):
    return st(f'''
  <div class="errno"><span>ОШИБКА №{n}</span><small>из 5</small></div>
  <div class="row" style="top:330px"><div class="h1" style="font-size:80px">{title}</div></div>
  <div class="row" style="top:{520 if '<br>' in title else 440}px"><div class="h2" style="font-size:36px;color:var(--muted);font-weight:700">{sub}</div></div>
  {body}
  <div class="row" style="top:1430px">{fix}</div>
  {sticker}
''', name=name)
S.append(err(1, 'ГОЛОДОВКИ', 'не ем до вечера — и горжусь собой',
  f'''<div class="row" style="top:600px"><div class="card vs">
     <div class="vrow"><div class="l">раньше<small>за весь день</small></div><div class="tr"><div class="fl" style="width:68%;background:#c9c0b4"></div></div></div>
     <div class="vrow"><div class="l">теперь<small>за один вечер</small></div><div class="tr"><div class="fl" style="width:96%;background:var(--red)"></div></div><div class="ar" style="color:var(--red)">↑</div></div></div></div>
     <div class="row" style="top:900px"><div class="hand" style="rotate:-3deg;font-size:62px">голод копится — вечером срыв</div></div>
     <div class="ab" style="left:90px;top:1030px">{svg('CLOCK',300)}</div>''',
  f'<img class="tst" src="{T("08_sad")}" style="right:-30px;top:960px;width:440px">',
  '<div class="fix"><i>✓</i><b>3–4 нормальных приёма пищи — режим, который ты можешь держать</b></div>', 'err_1'))
S.append(err(2, 'ПЬЁШЬ<br><em>КАЛОРИИ</em>', 'напитки никто не считает за еду',
  f'''<div class="row" style="top:690px"><div style="display:grid;grid-template-columns:repeat(2,440px);gap:26px">
     <div class="card fact" style="width:auto;padding:30px"><div class="k">РАФ НА СИРОПЕ</div><div class="t"><em>300–400</em> ккал</div></div>
     <div class="card fact" style="width:auto;padding:30px"><div class="k">СОК 250 МЛ</div><div class="t"><em>≈110</em> ккал</div></div>
     <div class="card fact" style="width:auto;padding:30px"><div class="k">СМУЗИ 300 МЛ</div><div class="t"><em>≈200</em> ккал</div></div>
     <div class="card fact" style="width:auto;padding:30px"><div class="k">ВИНО 150 МЛ</div><div class="t"><em>≈120</em> ккал</div></div></div></div>
     <div class="row" style="top:1110px"><div class="hand" style="rotate:-3deg;font-size:62px">и это совсем не насыщает</div></div>''',
  f'<img class="tst" src="{T("06_think")}" style="left:350px;top:1180px;width:250px">',
  '<div class="fix"><i>✓</i><b>капучино без сиропа и вода с лимоном</b></div>', 'err_2'))
S.append(err(3, 'НЕДОСЫП', 'спала по 5–6 часов',
  f'''<div class="row" style="top:560px"><div class="card vs">
     <div class="vrow"><div class="l">голод<small>гормон грелин</small></div><div class="tr"><div class="fl" style="width:92%;background:var(--red)"></div></div><div class="ar" style="color:var(--red)">↑</div></div>
     <div class="vrow"><div class="l">сытость<small>гормон лептин</small></div><div class="tr"><div class="fl" style="width:36%;background:var(--green)"></div></div><div class="ar" style="color:var(--green)">↓</div></div></div></div>
     <div class="row" style="top:860px"><div class="hand" style="rotate:-3deg;font-size:62px">весь день тянет на сладкое</div></div>''',
  f'<img class="tst" src="{T("05_tired")}" style="left:310px;top:960px;width:460px">',
  '<div class="fix"><i>✓</i><b>7–8 часов сна — и тяга к сладкому падает сама</b></div>', 'err_3'))
S.append(err(4, 'НАКАЗЫВАЕШЬ<br><em>СЕБЯ</em>', 'после срыва голодать и «отрабатывать»',
  f'''<div class="row" style="top:640px"><div class="loopc">
     <svg width="760" height="760" viewBox="0 0 760 760" style="position:absolute;inset:0"><circle cx="380" cy="380" r="290" stroke="#c8102e" stroke-width="20" fill="none" stroke-dasharray="80 30"/></svg>
     <div class="node" style="left:380px;top:90px">голод</div><div class="node r" style="left:670px;top:380px">срыв</div>
     <div class="node r" style="left:380px;top:670px">вина</div><div class="node" style="left:90px;top:380px">голод</div>
     <div class="ab" style="left:230px;top:230px">{svg('DONUT',300)}</div></div></div>''',
  '',
  '<div class="fix"><i>✓</i><b>после срыва — просто обычный день. Один вечер ничего не решает</b></div>', 'err_4'))
S.append(err(5, 'БЕЗУГЛЕВОДКА', '−3 кг за неделю… а потом +2 за ночь',
  f'''<div class="row" style="top:560px"><div class="card fact"><div class="k">ПЕРВЫЕ КИЛОГРАММЫ — ЭТО</div>
     <div style="display:flex;height:120px;border-radius:26px;overflow:hidden;margin-top:10px"><div style="width:80%;background:linear-gradient(180deg,#9fdcff,#2f97dc);color:#fff;font:900 38px/120px Unb;text-align:center">вода + гликоген</div><div style="flex:1;background:linear-gradient(180deg,#ffd98f,#d98f2e);color:#fff;font:900 30px/120px Unb;text-align:center">жир</div></div></div></div>
     <div class="row" style="top:850px"><div class="hand" style="rotate:-3deg;font-size:58px">1 г гликогена держит ≈3 г воды</div></div>
     <div class="ab" style="left:70px;top:960px">{svg('PASTA',340)}</div><div class="ab" style="left:430px;top:960px">{svg('DROP',170)}</div>''',
  f'<img class="tst" src="{T("01_shock")}" style="right:-30px;top:920px;width:420px;rotate:-6deg">',
  '<div class="fix"><i>✓</i><b>жир уходит на обычной еде с дефицитом калорий</b></div>', 'err_5'))
S.append(st(f'''
  <div class="row" style="top:280px"><div class="h1" style="font-size:88px">УЗНАЛА<br>СЕБЯ?</div></div>
  <div class="row" style="top:560px"><div class="h2" style="font-size:46px;color:#fff;line-height:1.3">как худеть без этих ошибок —<br>по шагам на моём сайте</div></div>
  <div class="row" style="top:820px"><div class="link" style="border-color:rgba(255,255,255,.7);color:#fff;background:rgba(255,255,255,.1)">сюда — стикер «Ссылка»<br>на сайт</div></div>
  <div class="row" style="top:1100px"><div class="hand" style="rotate:-4deg;font-size:84px">тапни 👆</div></div>
  <img class="tst" src="{T('03_wink')}" style="left:290px;top:1220px;width:500px">
''', cls='red', name='err_6'))

# ======================= ДЕСЕРТ =======================
S.append(st(f'''
  <div class="row" style="top:260px"><div class="kick">кодовое слово</div></div>
  <div class="row" style="top:330px"><div class="h1" style="font-size:120px"><em>ДЕСЕРТ</em></div></div>
  <div class="row" style="top:500px"><div class="h2" style="font-size:52px">что это значит? 🍰</div></div>
  <div class="row" style="top:650px"><div class="card cmt"><img src="{A('gym.jpg')}"><div><div class="who">ты · под рилсом</div><div class="txt">ДЕСЕРТ</div></div><div class="heart">♥</div></div></div>
  <div class="row" style="top:900px"><div class="hand" style="rotate:-3deg">пишешь — получаешь гайд</div></div>
  <div class="ab" style="left:90px;top:1060px">{svg('CAKE',380)}</div>
  <img class="tst" src="{T('07_love')}" style="right:-20px;top:1000px;width:480px">
''', name='dessert_1'))
S.append(st(f'''
  <div class="row" style="top:250px"><div class="h1" style="font-size:84px">КАК ЭТО<br><em>РАБОТАЕТ</em></div></div>
  <div class="ab steps" style="left:80px;top:560px">
    <div class="card step"><i>1</i><div><b>Найди любой мой рилс</b><span>в конце каждого — свой гайд</span></div></div>
    <div class="card step"><i>2</i><div><b>Напиши «ДЕСЕРТ» в комментарии</b><span>одно слово — и всё</span></div></div>
    <div class="card step"><i>3</i><div><b>Я скину тебе гайд</b><span>бесплатно, без регистрации</span></div></div></div>
  <img class="tst" src="{T('02_happy')}" style="left:320px;top:1240px;width:440px">
''', name='dessert_2'))
S.append(st(f'''
  <div class="row" style="top:250px"><div class="h1" style="font-size:84px">НЕ ХОЧЕШЬ<br>ЖДАТЬ?</div></div>
  <div class="row" style="top:500px"><div class="guide" style="width:560px;height:620px"><div class="k">ГАЙДЫ ОТ НИКИ</div><div class="t" style="font-size:66px">ВСЕ<br><em>СРАЗУ</em><br>НА САЙТЕ</div><div class="b"><img src="{A('face.jpg')}">забирай</div></div></div>
  <div class="row" style="top:1180px"><div class="link">сюда — стикер «Ссылка»<br>на сайт</div></div>
  <div class="row" style="top:1460px"><div class="hand" style="rotate:-4deg">тапни 👆</div></div>
''', name='dessert_3'))

# ======================= ОБЛОЖКИ =======================
def cover(word, inner, name):
    return st(f'<div class="disc ab" style="left:140px;top:560px;width:800px;height:800px;border-radius:50%;background:#fff;box-shadow:0 30px 80px rgba(60,40,20,.15);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px">{inner}<div style="font:900 92px/1 Unb;letter-spacing:-2px">{word}</div></div>', name=name)
S.append(cover('СТАРТ', f'<img src="{T("03_wink")}" style="width:420px">', 'cover_start'))
S.append(cover('ОШИБКИ', f'<img src="{T("01_shock")}" style="width:420px">', 'cover_errors'))
S.append(cover('ДЕСЕРТ', svg('CAKE', 400), 'cover_dessert'))

html = f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{DEFS}{"".join(S)}</body></html>'
open(os.path.join(HERE, 'stories.html'), 'w', encoding='utf-8').write(html)

async def render():
    from playwright.async_api import async_playwright
    out = os.path.join(HERE, 'out'); os.makedirs(out, exist_ok=True)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8791'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
            await pg.goto('http://127.0.0.1:8791/tools/stories/stories.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(800)
            for el in await pg.query_selector_all('.st'):
                n = await el.get_attribute('data-name'); await el.screenshot(path=os.path.join(out, n + '.png')); print('  ', n)
            await b.close()
    finally: srv.terminate()
asyncio.run(render())
