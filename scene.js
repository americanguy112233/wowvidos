// Анимация ролика: детерминированная, управляется только временем → window.renderAt(t).
// Тайминг сцен и метки синхронизации приходят из assets/timeline.js (его пишет voice.py).
const H = 1920, FPS = 60;
const MIN = [4.5, 5, 5.5, 4, 5, 4];
const SC = window.SCENES || MIN.reduce((a, d, i) => (a.push({ start: i ? a[i - 1].start + MIN[i - 1] : 0, dur: d, marks: {} }), a), []);
const DUR = SC.at(-1).start + SC.at(-1).dur;
const $ = id => document.getElementById(id);
const SFX = [];
const sfx = (t, type, o = {}) => SFX.push({ t: +t.toFixed(3), type, ...o });
const mk = (i, k, def) => SC[i].marks?.[k] ?? SC[i].start + def;   // метка из озвучки или запасное время

const tl = gsap.timeline({ paused: true, defaults: { ease: 'power2.out' } });
const P = { cam: 0, mb: 0, fade: 0, ta: 0, tb: 0, cz: 0, n1: 0 };
// что «печатают» в поля имени (сцена 3) — символы вместо настоящей ругани
const NAME_A = '#@%&!', NAME_B = '$*#@!!';
// ник в сцене 1: главное имя + второе имя (поменяй на свои)
const NICK = ['Analin', 'Galereed'];
$('nk1').textContent = NICK[0]; $('nk2').textContent = NICK[1];

document.querySelectorAll('.sec').forEach((s, i) => (s.style.top = i * H + 'px'));

// ---------------------------------------------------------------- фон: восьмиконечная звезда
$('starp').setAttribute('d', [...Array(16)].map((_, k) => {
  const r = k % 2 ? 52 : 100, a = (k / 16) * Math.PI * 2 - Math.PI / 2;
  return `${k ? 'L' : 'M'}${(Math.cos(a) * r).toFixed(2)} ${(Math.sin(a) * r).toFixed(2)}`;
}).join('') + 'Z');

// ---------------------------------------------------------------- пунктирные стрелки между сценами
const CONN = [];
document.querySelectorAll('.sec').forEach((s, i) => {
  if (!i) return;
  const hdr = s.querySelector('.row'), top = parseFloat(hdr.style.top) - 26, from = -560;
  const len = top - from;
  const wrap = document.createElement('div');
  wrap.className = 'conn'; wrap.style.top = from + 'px'; wrap.style.height = '0px'; wrap.style.opacity = '0';
  wrap.innerHTML = `<div style="position:absolute;left:-40px;top:0;width:86px;height:100%;overflow:hidden">
      <svg width="86" height="${len}" style="left:0"><path class="dash" d="M43 0V${len - 8}" stroke="#d6b25a" stroke-width="6" stroke-dasharray="22 16" fill="none" stroke-linecap="round"/></svg></div>
    <svg width="86" height="40" style="position:absolute;left:-40px;bottom:-6px;top:auto"><path d="M21 8l22 22 22-22" stroke="#d6b25a" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  s.appendChild(wrap);
  CONN.push({ el: wrap, len, i });
});

// ---------------------------------------------------------------- QR
(function buildQR() {
  const q = window.QR, n = q.length, svg = $('qrsvg');
  svg.setAttribute('viewBox', `-0.5 -0.5 ${n + 1} ${n + 1}`);
  const inFinder = (x, y) => (x < 7 && y < 7) || (x >= n - 7 && y < 7) || (x < 7 && y >= n - 7);
  let out = '';
  for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
    if (!q[y][x] || inFinder(x, y)) continue;
    out += `<g class="qm" data-d="${Math.hypot(x - n / 2, y - n / 2).toFixed(2)}"><rect x="${x + .06}" y="${y + .12}" width=".88" height=".88" rx=".24" fill="#1a0f05"/>` +
      `<rect x="${x + .06}" y="${y + .04}" width=".88" height=".86" rx=".24" fill="#3b2410"/></g>`;
  }
  for (const [fx, fy] of [[0, 0], [n - 7, 0], [0, n - 7]]) {
    out += `<g class="qf"><rect x="${fx + .5}" y="${fy + .62}" width="6" height="6" rx="1.5" fill="none" stroke="#15151c" stroke-width="1"/>` +
      `<rect x="${fx + .5}" y="${fy + .5}" width="6" height="6" rx="1.5" fill="none" stroke="#2b2b35" stroke-width="1"/>` +
      `<rect x="${fx + 2}" y="${fy + 2.1}" width="3" height="3" rx=".7" fill="#15151c"/><rect x="${fx + 2}" y="${fy + 2}" width="3" height="2.9" rx=".7" fill="#2b2b35"/></g>`;
  }
  svg.innerHTML = out;
})();

// ---------------------------------------------------------------- помощники анимации
const pop = (el, t, o = {}) => tl.fromTo(el, { scale: o.s ?? .6, opacity: o.o ?? 0, y: o.y ?? 0, x: o.x ?? 0, rotation: o.r ?? 0 },
  { scale: 1, opacity: 1, y: 0, x: 0, rotation: 0, duration: o.d ?? .45, ease: o.ease ?? 'back.out(1.8)' }, t);
const fadeUp = (el, t) => tl.fromTo(el, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .4 }, t);
const pulse = (el, t, s = 1.08) => tl.to(el, { scale: s, duration: .12, ease: 'power2.out', yoyo: true, repeat: 1 }, t);
const shake = (el, t) => tl.to(el, { keyframes: { x: [0, -14, 12, -8, 5, 0] }, duration: .42, ease: 'none' }, t);
const glow = (el, t) => tl.fromTo(el, { boxShadow: '0 0 0 0px rgba(79,227,178,0), 0 18px 0 rgba(30,0,60,.18), 0 26px 50px rgba(20,0,40,.35)' },
  { boxShadow: '0 0 0 7px rgba(79,227,178,1), 0 18px 0 rgba(30,0,60,.18), 0 26px 60px rgba(40,230,160,.45)', duration: .35 }, t);
const ticks = (t0, d, n, f0 = 1, f1 = 1.6) => { for (let k = 0; k < n; k++) sfx(t0 + d * k / n, 'tick', { f: f0 + (f1 - f0) * k / n, g: .7 }); };

// камера: переход в сцену i занимает [start-0.5, start+0.2]
for (let i = 1; i < SC.length; i++) {
  const t = SC[i].start - .5;
  tl.fromTo(P, { cam: (i - 1) * H }, { cam: i * H, duration: .7, ease: 'power3.inOut', immediateRender: false }, t);
  tl.fromTo(P, { mb: 0 }, { mb: 28, duration: .35, ease: 'power2.in', immediateRender: false }, t);
  tl.to(P, { mb: 0, duration: .35, ease: 'power2.out' }, t + .35);
  const c = CONN[i - 1];
  tl.fromTo(c.el, { height: 0, opacity: 0 }, { height: c.len, opacity: 1, duration: .55, ease: 'power2.inOut', immediateRender: false }, t + .05);
  sfx(t, 'whoosh', { d: .62 });
}
const hdr = (i, el) => { pop(el, SC[i].start + .02, { s: .7, d: .5 }); sfx(SC[i].start + .02, 'thump', { g: .8 }); };

// печать: влетает крупной и «бьёт» по карточке
const slam = (el, t, target) => {
  tl.fromTo(el, { scale: 2.6, opacity: 0 }, { scale: 1, opacity: 1, duration: .26, ease: 'power3.in', immediateRender: false }, t);
  tl.set(el, { opacity: 0 }, 0);
  shake(target, t + .26); pulse(target, t + .26, 1.03);
  sfx(t + .24, 'impact', { g: .7 }); sfx(t + .26, 'bonk', { g: .6 });
};

// ================================================================ 1. хук: ник → бан
{
  const s = SC[0].start, a = mk(0, 'a', 1.0), b = mk(0, 'b', 3.2);
  // первый кадр уже содержательный (превью в ленте): заголовок и ник на месте, лишь «доезжают»
  pop('#lg1', s, { s: 1.15, o: 1, d: .7, ease: 'power3.out' });
  pop('#h1', s, { s: 1.25, o: 1, d: .6, ease: 'power3.out' }); sfx(s, 'thump', { g: .8 });
  pop('#c1', s + .05, { y: 90, s: .92, o: 1, d: .65, ease: 'back.out(1.6)' }); sfx(s + .1, 'pop', { f: 1.1 });
  pop('#k1', s + .5, { s: .8 }); sfx(s + .5, 'blip', { f: .9 });
  const a0 = Math.max(s + .8, a - .2);
  fadeUp('#a1', a0);
  pop('#sh1', a0 + .15, { y: 120, s: .85, d: .55 }); sfx(a0 + .15, 'pop', { f: .9 });
  const b0 = Math.max(a0 + .9, b - .25);
  slam('#st1', b0, '#sh1');
  // ник зачёркивается и краснеет в момент бана
  tl.fromTo('#sk1', { scaleX: 0 }, { scaleX: 1, duration: .25, ease: 'power2.out', immediateRender: false }, b0 + .2);
  tl.fromTo(P, { n1: 0 }, { n1: 1, duration: .01, immediateRender: false }, b0 + .2);
  fadeUp('#f1', b0 + .6);
}

// ================================================================ 2. два исхода
{
  const s = SC[1].start, a = mk(1, 'a', 1.0), b = mk(1, 'b', 3.0);
  hdr(1, '#h2');
  pop('#k2', s + .3, { s: .8 }); sfx(s + .3, 'blip');
  const a0 = Math.max(s + .55, a - .2);
  pop('#r2a', a0, { x: -140, s: .9, d: .5, ease: 'back.out(1.4)' }); sfx(a0, 'pop', { f: 1 });
  pop('#tg2a', a0 + .45, { s: .3, d: .35 }); sfx(a0 + .45, 'blip', { f: 1.2 });
  const b0 = Math.max(a0 + 1, b - .2);
  pop('#r2b', b0, { x: 140, s: .9, d: .5, ease: 'back.out(1.4)' }); sfx(b0, 'pop', { f: .85 });
  pop('#tg2b', b0 + .4, { s: .3, d: .35 }); shake('#r2b', b0 + .45); sfx(b0 + .45, 'bonk');
}

// ================================================================ 3. два имени
{
  const s = SC[2].start, a = mk(2, 'a', .8), b = mk(2, 'b', 3.0);
  hdr(2, '#h3');
  pop('#k3', s + .3, { s: .8 }); sfx(s + .3, 'blip');
  pop('#wd3', s + .45, { y: 100, s: .88, d: .5 }); sfx(s + .45, 'pop');
  pop('#duck3', s + .7, { s: .2, d: .55, ease: 'back.out(2.2)' });
  // печатаем обе половины имени; символы-«ругательства» вместо настоящих слов
  const a0 = Math.max(s + .9, a - .1), b0 = Math.max(a0 + 1.5, b - .15);
  const T = Math.min(.7, (b0 - a0 - .2) / 2);
  tl.fromTo(P, { ta: 0 }, { ta: 1, duration: T, ease: 'none', immediateRender: false }, a0);
  tl.fromTo(P, { tb: 0 }, { tb: 1, duration: T, ease: 'none', immediateRender: false }, a0 + T + .1);
  ticks(a0, T, 5, 1.1, 1.4); ticks(a0 + T + .1, T, 6, 1.2, 1.6);
  // нарушение: поля краснеют, текст закрывается плашками
  tl.fromTo(P, { cz: 0 }, { cz: 1, duration: .01, immediateRender: false }, b0);
  tl.set('#bd3', { opacity: 0 }, 0);
  pop('#bd3', b0, { s: .3, d: .4 }); shake('#wd3', b0); sfx(b0, 'bonk'); sfx(b0 + .05, 'impact', { g: .45 });
  pop('#p3', b0 + .45, { s: .6 }); sfx(b0 + .45, 'pop', { f: 1.2 });
  fadeUp('#f3', b0 + .75);
}

// ================================================================ 4. без шансов
{
  const s = SC[3].start, a = mk(3, 'a', .9), b = mk(3, 'b', 2.2);
  hdr(3, '#h4');
  pop('#tk4', s + .3, { y: 120, s: .88, d: .5 }); sfx(s + .3, 'pop');
  const a0 = Math.max(s + .5, a - .1);
  pop('#k4', a0, { s: .8 }); sfx(a0, 'blip');
  const b0 = Math.max(a0 + .6, b - .2);
  slam('#st4', b0, '#tk4');
  fadeUp('#f4', b0 + .5);
}

// ================================================================ 5. автофильтр (дроп музыки)
{
  const s = SC[4].start;
  hdr(4, '#h5');
  pop('#party', s + .12, { s: .2, d: .7, ease: 'elastic.out(1, .55)' }); sfx(s + .12, 'impact'); sfx(s + .2, 'sparkle');
  let prev = s + .5;
  [['#l5a', 'b', 1.0, 'ding'], ['#l5b', 'c', 1.9, 'bonk'], ['#l5c', 'd', 3.0, 'check']].forEach(([id, k, def, snd]) => {
    const t = Math.max(prev + .35, mk(4, k, def) - .1); prev = t;
    pop(id, t, { x: 140, s: .9, d: .45, ease: 'back.out(1.5)' }); sfx(t, snd, { g: .9 });
  });
}

// ================================================================ 6. QR
{
  const s = SC[5].start, a = mk(5, 'a', 2);
  pop('#lg6', s, { s: .7, d: .5 });
  pop('#h6', s + .02, { s: .7 }); sfx(s + .02, 'thump', { g: .8 });
  pop('#qr', s + .15, { s: .75, d: .55 }); sfx(s + .15, 'pop', { f: .9 });
  tl.fromTo('#qrsvg .qm', { opacity: 0, scale: .2, transformOrigin: '50% 50%' },
    { opacity: 1, scale: 1, duration: .3, ease: 'back.out(2)', stagger: { each: 0, from: 'center', amount: .5 } }, s + .25);
  tl.fromTo('#qrsvg .qf', { opacity: 0 }, { opacity: 1, duration: .25 }, s + .3);
  ticks(s + .25, .5, 6, 1.2, 1.9);
  pop('#qrlogo', s + .65, { s: .2, d: .5, ease: 'back.out(2.5)' }); sfx(s + .65, 'pop', { f: 1.3 });
  pop('#p6', s + .8, { s: .6 }); sfx(s + .8, 'blip', { f: 1.2 });
  fadeUp('#f6', s + 1.0);
  pulse('#h6', Math.max(s + 1.2, a), 1.1); sfx(Math.max(s + 1.2, a), 'ding', { f: 1.2 });
  tl.fromTo(P, { fade: 0 }, { fade: .72, duration: .45, ease: 'power1.in', immediateRender: false }, DUR - .45);
}
tl.set({}, {}, DUR);

// ---------------------------------------------------------------- Lottie-утки
const ANIMS = [], IMGS = [];
// ждём загрузку картинки без img.decode(): в фоновых вкладках headless Chrome decode() может зависнуть навсегда
const imgReady = img => (img.complete && img.naturalWidth) ? Promise.resolve() :
  new Promise(r => { img.addEventListener('load', r, { once: true }); img.addEventListener('error', () => { console.error('нет картинки', img.src); r(); }, { once: true }); setTimeout(r, 8000); });
const cache = {};
async function loadStickers() {
  // data-anim="имя" → assets/stickers/имя.json (Lottie, анимированный)
  // data-anim="имя.png" / ".webp" / ".jpg" → обычная картинка
  const all = [...document.querySelectorAll('[data-anim]')];
  const isImg = n => /\.(png|webp|jpe?g)$/i.test(n);
  await Promise.all(all.filter(el => isImg(el.dataset.anim)).map(el => {
    const img = new Image();
    img.src = `assets/stickers/${el.dataset.anim}`;
    img.style.cssText = 'display:block;width:100%;height:100%;object-fit:contain';
    el.appendChild(img);
    IMGS.push(img);
    return imgReady(img);
  }));
  const els = all.filter(el => !isImg(el.dataset.anim));
  await Promise.all([...new Set(els.map(e => e.dataset.anim))].map(async n => (cache[n] = await (await fetch(`assets/stickers/${n}.json`)).text())));
  await Promise.all(els.map(el => new Promise(res => {
    const anim = lottie.loadAnimation({ container: el, renderer: 'svg', loop: false, autoplay: false, animationData: JSON.parse(cache[el.dataset.anim]),
      rendererSettings: { preserveAspectRatio: 'xMidYMid meet', progressiveLoad: false } });
    const sec = [...document.querySelectorAll('.sec')].indexOf(el.closest('.sec'));
    ANIMS.push({ anim, sec, t0: SC[sec].start, n: 0 });
    if (anim.isLoaded) res(); else { anim.addEventListener('DOMLoaded', res); setTimeout(res, 3000); }
  })));
  ANIMS.forEach(o => (o.n = o.anim.totalFrames));
}

// ---------------------------------------------------------------- фон: скриншоты игры + искры
const BG_FOREST = [0, 1, 1, 0, 1, 0];          // 0 — Тёмный портал, 1 — лес (по сценам)
const EMB = [...Array(70)].map((_, k) => {     // детерминированные искры (одинаковые при каждом рендере)
  const r = n => { const x = Math.sin(k * 127.1 + n * 311.7) * 43758.5453; return x - Math.floor(x); };
  return { x: r(1) * 1080, sp: 40 + r(2) * 90, sz: 1.5 + r(3) * 3.5, ph: r(4) * 1920, sw: 10 + r(5) * 30, fr: .5 + r(6) * 1.5, a: .35 + r(7) * .6 };
});
const emb = document.getElementById('embers').getContext('2d');
function drawEmbers(t) {
  emb.clearRect(0, 0, 1080, 1920);
  for (const e of EMB) {
    const y = 1920 - ((e.ph + t * e.sp) % 2000);
    const x = e.x + Math.sin(t * e.fr + e.ph) * e.sw;
    const g = emb.createRadialGradient(x, y, 0, x, y, e.sz * 3);
    g.addColorStop(0, `rgba(255,214,120,${e.a})`); g.addColorStop(1, 'rgba(255,140,40,0)');
    emb.fillStyle = g; emb.beginPath(); emb.arc(x, y, e.sz * 3, 0, 7); emb.fill();
  }
}

// ---------------------------------------------------------------- кадр
let lastFilter = '';
function apply(t) {
  $('world').style.transform = `translate3d(0,${-P.cam}px,0)`;
  $('grid').style.transform = `translate3d(0,${-(P.cam % 108)}px,0)`;
  $('star').style.transform = `rotate(${(t * 3 + P.cam * .012).toFixed(2)}deg) scale(${1 + .03 * Math.sin(t * .8)})`;
  $('arc').style.transform = `rotate(${(-t * 5 - P.cam * .02).toFixed(2)}deg)`;
  const f = P.mb > .3 ? 'url(#mb)' : 'none';
  $('mbg').setAttribute('stdDeviation', `0 ${P.mb.toFixed(2)}`);
  if (f !== lastFilter) { $('view').style.filter = f; lastFilter = f; }
  $('fade').style.opacity = P.fade;
  // фон: плавная смена скриншота между сценами + медленный наезд
  const c = Math.min(SC.length - 1, Math.max(0, P.cam / H)), i0 = Math.floor(c), fr = c - i0;
  const wB = BG_FOREST[i0] * (1 - fr) + (BG_FOREST[Math.min(i0 + 1, SC.length - 1)] ?? 0) * fr;
  $('bgB').style.opacity = wB.toFixed(3);
  const kb = `scale(${(1.06 + .04 * Math.sin(t * .15)).toFixed(4)}) translate3d(${(Math.sin(t * .11) * 18).toFixed(1)}px,${(-P.cam * .01).toFixed(1)}px,0)`;
  $('bgA').style.transform = kb; $('bgB').style.transform = kb;
  drawEmbers(t);
  $('fld1').classList.toggle('bad', P.n1 > .5);
  // сцена 3: печать в два поля, потом цензура
  const bad = P.cz > .5;
  const na = Math.round(P.ta * NAME_A.length), nb = Math.round(P.tb * NAME_B.length);
  $('t3a').innerHTML = bad ? '<span class="cz" style="width:150px"></span>' : NAME_A.slice(0, na);
  $('t3b').innerHTML = bad ? '<span class="cz" style="width:180px"></span>' : NAME_B.slice(0, nb);
  $('p3a').style.display = na || bad ? 'none' : '';
  $('p3b').style.display = nb || bad ? 'none' : '';
  const blink = Math.floor(t * 2.5) % 2 === 0;
  const onB = P.tb > 0 || (P.ta >= 1 && !bad);
  $('ca3').style.opacity = !bad && !onB && blink ? 1 : 0;
  $('cb3').style.opacity = !bad && onB && blink ? 1 : 0;
  $('fa3').classList.toggle('bad', bad); $('fb3').classList.toggle('bad', bad);
  // картинки-стикеры слегка покачиваются
  IMGS.forEach((im, k) => (im.style.transform = `rotate(${(4 * Math.sin(t * 2.4 + k * 1.7)).toFixed(2)}deg) scale(${(1 + .03 * Math.sin(t * 3.1 + k)).toFixed(3)})`));
  // пунктир «бежит»
  document.querySelectorAll('.dash').forEach(d => d.setAttribute('stroke-dashoffset', (-t * 90).toFixed(1)));
  // утки: играют циклом с момента появления сцены, считаем только видимые
  const cur = P.cam / H;
  for (const o of ANIMS) {
    if (Math.abs(o.sec - cur) > 1.05) continue;
    const fr = Math.max(0, (t - o.t0) * FPS) % o.n;
    o.anim.goToAndStop(fr, true);
  }
}

window.renderAt = t => { tl.seek(Math.min(t, DUR), false); apply(t); };
window.DUR = DUR;
window.SFX = SFX.sort((a, b) => a.t - b.t);
window.TIMELINE = { dur: DUR, drop: SC[4].start, scenes: SC };
window.STAGE = 'старт';
window.READY = (async () => {
  window.STAGE = 'шрифты';
  await Promise.race([Promise.all([...document.fonts].map(f => f.load().catch(() => {}))), new Promise(r => setTimeout(r, 10000))]);
  window.STAGE = 'стикеры';
  await loadStickers();
  window.STAGE = 'картинки';
  await Promise.all([...document.images].map(imgReady));
  window.STAGE = 'первый кадр';
  window.renderAt(0);
  window.STAGE = 'готово';
  return true;
})();

// превью в браузере: ?t=12.3 — стоп-кадр, иначе проигрывание в реальном времени
const qs = new URLSearchParams(location.search);
if (!qs.has('render')) window.READY.then(() => {
  if (qs.has('t')) return window.renderAt(+qs.get('t'));
  const t0 = performance.now();
  const loop = () => { window.renderAt(((performance.now() - t0) / 1000) % DUR); requestAnimationFrame(loop); };
  loop();
});
