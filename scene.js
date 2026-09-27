// Анимация ролика: детерминированная, управляется только временем → window.renderAt(t).
// Тайминг сцен и метки синхронизации приходят из assets/timeline.js (его пишет voice.py).
const H = 1920, FPS = 60;
const MIN = [2.9, 6.5, 4, 5.5, 5, 4.5];
const LOOP = .55;                              // финальный перелёт камеры обратно к первому кадру
const SC = window.SCENES || MIN.reduce((a, d, i) => (a.push({ start: i ? a[i - 1].start + MIN[i - 1] : 0, dur: d, marks: {} }), a), []);
const DUR = SC.at(-1).start + SC.at(-1).dur + LOOP;
const $ = id => document.getElementById(id);
const SFX = [];
const sfx = (t, type, o = {}) => SFX.push({ t: +t.toFixed(3), type, ...o });
const mk = (i, k, def) => SC[i].marks?.[k] ?? SC[i].start + def;   // метка из озвучки или запасное время

const tl = gsap.timeline({ paused: true, defaults: { ease: 'power2.out' } });
const P = { cam: 0, mb: 0, fade: 0, flash: 0, spd: 0, fps: 32, t2a: 0, t2b: 0, w: 100, c4a: 0, c4b: 0, c4c: 0, c4d: 0 };
const T2A = '/console DynamicRenderScale 1', T2B = '/console DynamicRenderScaleMin 0.5';

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

// камера: быстрый переход (0.5 с) со вспышкой и линиями скорости
for (let i = 1; i < SC.length; i++) {
  const t = SC[i].start - .4;
  tl.fromTo(P, { cam: (i - 1) * H }, { cam: i * H, duration: .5, ease: 'power4.inOut', immediateRender: false }, t);
  tl.fromTo(P, { mb: 0 }, { mb: 34, duration: .25, ease: 'power2.in', immediateRender: false }, t);
  tl.to(P, { mb: 0, duration: .25, ease: 'power2.out' }, t + .25);
  tl.fromTo(P, { spd: 1 }, { spd: 0, duration: .6, ease: 'power2.out', immediateRender: false }, t + .05);
  tl.fromTo(P, { flash: .55 }, { flash: 0, duration: .3, ease: 'power2.out', immediateRender: false }, t + .45);
  const c = CONN[i - 1];
  tl.fromTo(c.el, { height: 0, opacity: 0 }, { height: c.len, opacity: 1, duration: .45, ease: 'power2.inOut', immediateRender: false }, t + .05);
  sfx(t, 'whoosh', { d: .5 }); sfx(t + .45, 'thump', { g: .55 });
}
const hdr = (i, el) => { pop(el, SC[i].start + .02, { s: .7, d: .5 }); sfx(SC[i].start + .02, 'thump', { g: .8 }); };

const glowC = (el, t, rgb) => tl.fromTo(el, { boxShadow: `0 0 0 0px rgba(${rgb},0), 0 0 0 rgba(${rgb},0)` },
  { boxShadow: `0 0 0 6px rgba(${rgb},1), 0 0 50px rgba(${rgb},.55)`, duration: .3, immediateRender: false }, t);
const hide = (el) => tl.set(el, { opacity: 0 }, 0);
const flashAt = (t, v = .8, d = .35) => tl.fromTo(P, { flash: v }, { flash: 0, duration: d, ease: 'power2.out', immediateRender: false }, t);
const speedAt = (t, d = .6) => tl.fromTo(P, { spd: 1 }, { spd: 0, duration: d, ease: 'power2.out', immediateRender: false }, t);
const slamIn = (el, t, s0 = 2.6) => tl.fromTo(el, { scale: s0, opacity: 0 }, { scale: 1, opacity: 1, duration: .24, ease: 'power3.in', immediateRender: false }, t);
const typeOut = (key, t, d, n) => {   // печать команды + щелчки клавиш
  tl.fromTo(P, { [key]: 0 }, { [key]: 1, duration: d, ease: 'none', immediateRender: false }, t);
  for (let k = 0; k < n; k += 3) sfx(t + d * k / n, 'tick', { f: 1.3 + (k % 7) * .05, g: .45 });
};

// ================================================================ 1. хук: три удара за 3 секунды
{
  const h = .04, CUT = 1.75;
  hide('#x1'); hide('#s1b');
  flashAt(h, .95, .45); speedAt(h, .8);
  tl.fromTo('#n1', { scale: 1.55 }, { scale: 1, duration: .5, ease: 'back.out(3)', immediateRender: false }, h);
  pulse('#q1', .5, 1.12); pulse('#q1', .8, 1.12);
  tl.fromTo('#l1', { scale: 1.3, opacity: .3 }, { scale: 1, opacity: 1, duration: .45, ease: 'back.out(2)', immediateRender: false }, h + .05);
  shake('#s1a', h); sfx(h, 'impact', { g: .9 }); sfx(h, 'thump');
  // счётчик 32 → 112 с разгоном
  tl.fromTo(P, { fps: 32 }, { fps: 112, duration: .8, ease: 'power2.in', immediateRender: false }, .25);
  ticks(.25, .8, 14, 1, 2.2);
  pulse('#n1', 1.05, 1.18); flashAt(1.05, .6, .3); speedAt(1.05, .5); sfx(1.05, 'success');
  // печать ×3,5
  tl.to('#q1', { opacity: 0, scale: .6, duration: .12, immediateRender: false }, 1.0);
  slamIn('#x1', 1.12); shake('#s1a', 1.36); sfx(1.34, 'impact', { g: .7 }); sfx(1.36, 'bonk', { g: .5 });
  pulse('#p1', 1.45, 1.14);
  // склейка ко второму кадру: сравнение трёх скриншотов
  tl.set('#s1a', { opacity: 0 }, CUT); tl.set('#s1b', { opacity: 1 }, CUT);
  flashAt(CUT, 1, .35); speedAt(CUT, .6); sfx(CUT - .08, 'whoosh', { d: .3 }); sfx(CUT, 'impact', { g: .5 });
  pop('#h1b', CUT, { s: 1.6, o: 0, d: .4, ease: 'back.out(2.2)' });
  [['#pa', -1], ['#pb', 0], ['#pc', 1]].forEach(([id, dx], k) => {
    pop(id, CUT + .08 + k * .1, { y: 260, x: dx * 80, r: dx * 8, s: .7, d: .45, ease: 'back.out(1.6)' });
    sfx(CUT + .08 + k * .1, 'pop', { f: 1 + k * .15 });
  });
  glowC('#pc', CUT + .55, '62,224,122'); pulse('#pc', CUT + .55, 1.06); sfx(CUT + .55, 'ding');
  pop('#k1b', CUT + .5, { s: .7 });
  tl.fromTo('#s1b .panels', { scale: 1 }, { scale: 1.06, duration: 1.4, ease: 'none', immediateRender: false }, CUT + .5);
}

// ================================================================ 2. команда №1
{
  const s = SC[1].start, a = mk(1, 'a', .5), b = mk(1, 'b', 2.8), c = mk(1, 'c', 4.8);
  hdr(1, '#h2');
  pop('#tm2', s + .12, { y: 80, s: .9, d: .4 }); sfx(s + .12, 'pop');
  const ta = Math.max(s + .3, a - .15), da = .9;
  typeOut('t2a', ta, da, T2A.length);
  typeOut('t2b', ta + da + .15, .9, T2B.length);
  hide('#p2a'); hide('#p2b'); hide('#k2');
  const b0 = Math.max(ta + da + 1.1, b - .25);
  pop('#p2a', b0, { x: -220, r: -8, s: .8, d: .45, ease: 'back.out(1.6)' }); sfx(b0, 'pop');
  pop('#p2b', b0 + .15, { x: 220, r: 8, s: .8, d: .45, ease: 'back.out(1.6)' }); sfx(b0 + .15, 'pop', { f: 1.2 });
  glowC('#p2b', b0 + .6, '62,224,122'); pulse('#f2b', b0 + .6, 1.25); flashAt(b0 + .6, .4, .3); sfx(b0 + .6, 'success');
  const c0 = Math.max(b0 + 1.1, c - .1);
  pop('#k2', c0, { s: .6 }); shake('#k2', c0 + .3); sfx(c0, 'bonk', { g: .7 });
}

// ================================================================ 3. освещение: шторка до/после
{
  const s = SC[2].start, a = mk(2, 'a', .6), b = mk(2, 'b', 2.2);
  hdr(2, '#h3');
  pop('#wp', s + .12, { s: .85, d: .45 }); sfx(s + .12, 'pop');
  hide('#wTag');
  const a0 = Math.max(s + .5, a - .1);
  shake('#wp', a0); sfx(a0, 'bonk', { g: .6 });
  const b0 = Math.max(a0 + .6, b - .3);
  tl.fromTo(P, { w: 100 }, { w: 42, duration: .9, ease: 'power3.inOut', immediateRender: false }, b0);
  sfx(b0, 'zip', { d: .8 }); speedAt(b0 + .1, .5);
  pop('#wTag', b0 + .7, { s: .3, d: .35 }); flashAt(b0 + .8, .35, .3); sfx(b0 + .8, 'sparkle');
  tl.fromTo('#wp', { scale: 1 }, { scale: 1.04, duration: 1.2, ease: 'none', immediateRender: false }, b0 + .9);
}

// ================================================================ 4. ещё 4 команды — пулемётом
{
  const s = SC[3].start;
  hdr(3, '#h4');
  let prev = s + .15;
  ['a', 'b', 'c', 'd'].forEach((k, n) => {
    const t = Math.max(prev + .55, mk(3, k, .5 + n * 1.1) - .15); prev = t;
    const id = '#c4' + k;
    hide(id);
    pop(id, t, { x: n % 2 ? -260 : 260, r: n % 2 ? -6 : 6, s: .85, d: .38, ease: 'back.out(1.7)' });
    sfx(t, 'swoosh', { f: 1 + n * .1 }); speedAt(t, .35);
    typeOut('c4' + k, t + .15, .45, 26);
    glowC(id, t + .6, '255,209,0'); sfx(t + .6, 'check', { g: .8 });
  });
}

// ================================================================ 5. важно
{
  const s = SC[4].start, a = mk(4, 'a', .5), b = mk(4, 'b', 2.4);
  tl.fromTo('#s5 .stripes', { x: -1100 }, { x: 0, duration: .45, ease: 'power3.out', immediateRender: false, stagger: .08 }, s + .02);
  pop('#h5', s + .05, { s: 1.8, o: 0, d: .4, ease: 'back.out(2.4)' }); shake('#s5', s + .3); sfx(s + .05, 'impact', { g: .7 });
  hide('#w5a'); hide('#w5b'); hide('#w5c');
  const a0 = Math.max(s + .45, a - .1);
  pop('#w5a', a0, { x: -240, s: .9, d: .4, ease: 'back.out(1.6)' }); sfx(a0, 'blip');
  const b0 = Math.max(a0 + .7, b - .15);
  pop('#w5b', b0, { x: 240, s: .9, d: .4, ease: 'back.out(1.6)' }); glowC('#w5b', b0 + .4, '232,51,42'); shake('#w5b', b0 + .45); sfx(b0 + .4, 'bonk');
  pop('#w5c', b0 + .9, { x: -240, s: .9, d: .4, ease: 'back.out(1.6)' }); sfx(b0 + .9, 'blip', { f: .8 });
}

// ================================================================ 6. воронка в бота + перелёт к первому кадру (петля)
{
  const s = SC[5].start, a = mk(5, 'a', 2.2);
  pop('#lg6', s, { s: .7, d: .45 });
  pop('#h6', s + .05, { s: 1.5, o: 0, d: .45, ease: 'back.out(2)' }); sfx(s + .05, 'thump', { g: .8 });
  pop('#qr', s + .2, { s: .75, d: .5 }); sfx(s + .2, 'pop', { f: .9 });
  tl.fromTo('#qrsvg .qm', { opacity: 0, scale: .2, transformOrigin: '50% 50%' },
    { opacity: 1, scale: 1, duration: .3, ease: 'back.out(2)', stagger: { each: 0, from: 'center', amount: .5 } }, s + .3);
  tl.fromTo('#qrsvg .qf', { opacity: 0 }, { opacity: 1, duration: .25 }, s + .35);
  ticks(s + .3, .5, 6, 1.2, 1.9);
  pop('#qrlogo', s + .7, { s: .2, d: .5, ease: 'back.out(2.5)' }); sfx(s + .7, 'pop', { f: 1.3 });
  pop('#p6', s + .85, { s: .6 }); sfx(s + .85, 'blip', { f: 1.2 });
  fadeUp('#f6', s + 1.05);
  const a0 = Math.max(s + 1.3, a);
  pulse('#p6', a0, 1.14); pulse('#qr', a0 + .1, 1.04); sfx(a0, 'ding', { f: 1.2 });
  const L0 = DUR - LOOP;
  tl.fromTo(P, { cam: 5 * H }, { cam: 0, duration: LOOP, ease: 'power3.in', immediateRender: false }, L0);
  tl.fromTo(P, { mb: 0 }, { mb: 60, duration: LOOP * .8, ease: 'power2.in', immediateRender: false }, L0);
  speedAt(L0, LOOP);
  // возвращаем первый кадр в исходное состояние — приземление совпадёт с кадром 0
  tl.set('#s1a', { opacity: 1 }, L0); tl.set('#s1b', { opacity: 0 }, L0); tl.set('#x1', { opacity: 0 }, L0); tl.set('#q1', { opacity: 1, scale: 1 }, L0);
  tl.set(P, { fps: 32 }, L0);
  tl.set(P, { mb: 0 }, DUR);
  sfx(L0, 'whoosh', { d: LOOP + .1 });
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
const BG_FOREST = [0, 0, 1, 1, 0, 1];          // 0 — тропа (bgA), 1 — Тельдрассил (bgB)
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

// ---------------------------------------------------------------- линии скорости (детерминированные)
const spc = document.getElementById('speed').getContext('2d');
const SPL = [...Array(90)].map((_, k) => { const r = n => { const x = Math.sin(k * 91.7 + n * 47.3) * 43758.5453; return x - Math.floor(x); };
  return { a: r(1) * Math.PI * 2, w: 2 + r(2) * 6, r0: 420 + r(3) * 260, len: 300 + r(4) * 700, sp: r(5) }; });
function drawSpeed(t) {
  spc.clearRect(0, 0, 1080, 1920);
  if (P.spd < .02) return;
  spc.save(); spc.translate(540, 820);
  for (const l of SPL) {
    const o = ((t * 3 + l.sp) % 1) * 200, r0 = l.r0 + o, r1 = r0 + l.len;
    spc.strokeStyle = `rgba(255,236,190,${(P.spd * .55).toFixed(3)})`; spc.lineWidth = l.w;
    spc.beginPath(); spc.moveTo(Math.cos(l.a) * r0, Math.sin(l.a) * r0); spc.lineTo(Math.cos(l.a) * r1, Math.sin(l.a) * r1); spc.stroke();
  }
  spc.restore();
}

// ---------------------------------------------------------------- субтитры: по 1–3 слова, текущее слово золотое
const CHUNKS = [];
SC.forEach((sc, i) => {
  // короткие слова (а, в, и, на…) приклеиваем к следующему, чтобы не висели на строке
  const ws = []; (sc.words || []).forEach(([t, w]) => {
    const prev = ws.at(-1);
    if (prev && prev.glue) { prev[1] += '\u00a0' + w; prev.glue = /^[^.,!?:;…]{1,2}$/.test(w) && false; return; }
    const it = [t, w]; it.glue = /^[А-Яа-яЁёA-Za-z]{1,2}$/.test(w); ws.push(it);
  });
  let cur = [];
  const flush = () => { if (cur.length) CHUNKS.push({ sc: i, words: cur }); cur = []; };
  ws.forEach(([t, w], k) => {
    if (cur.length && (t - cur.at(-1).t > .6)) flush();
    cur.push({ t, w });
    if (cur.length >= 3 || /[.,!?:;…]$/.test(w) || (w.length > 11 && cur.length >= 2)) flush();
  });
  flush();
});
CHUNKS.forEach((c, k) => {
  const nx = CHUNKS[k + 1], scEnd = SC[c.sc].start + SC[c.sc].dur;
  c.start = c.words[0].t - .06;
  c.end = nx && nx.sc === c.sc ? nx.words[0].t - .06 : Math.min(c.words.at(-1).t + .9, scEnd - .15);
});
let lastChunk = null;
function subs(t) {
  const el = $('subs');
  const c = CHUNKS.find(c => t >= c.start && t < c.end);
  if (!c) { if (lastChunk) { el.innerHTML = ''; lastChunk = null; } return; }
  if (c !== lastChunk) {
    const chars = c.words.reduce((n, w) => n + w.w.length + 1, 0), longest = Math.max(...c.words.map(w => w.w.length));
    const fs = Math.max(50, Math.min(74, 860 / Math.max(chars * .62, longest * .66)));   // вся фраза — максимум в 2 строки
    el.innerHTML = `<div class="ln" style="font-size:${fs.toFixed(0)}px">` + c.words.map(w => `<span class="w">${w.w.replace(/[—–]/g, '')}</span>`).join('') + '</div>';
    lastChunk = c;
  }
  const dt = t - c.start, ln = el.firstChild;
  const sc = 1 - .22 * Math.exp(-dt * 11) * Math.cos(dt * 18);
  ln.style.transform = `scale(${sc.toFixed(3)})`; ln.style.opacity = Math.min(1, dt / .05).toFixed(2);
  [...ln.children].forEach((sp, k) => {
    const w = c.words[k], nx = c.words[k + 1];
    sp.className = 'w' + (t >= w.t && (!nx || t < nx.t) ? ' on' : '');
  });
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
  $('flash').style.opacity = P.flash.toFixed(3);
  // счётчик FPS: красный → зелёный
  const fv = Math.round(P.fps) + '';
  if ($('n1').textContent !== fv) { $('n1').textContent = fv; $('n1').dataset.text = fv; }
  const green = P.fps >= 100, n1s = $('n1').style;
  n1s.setProperty('--c1', green ? '#c8ffd8' : '#ffd0b8'); n1s.setProperty('--c2', green ? '#1fd060' : '#e8332a'); n1s.setProperty('--ex', green ? '#063a18' : '#3e0703');
  // печать команд
  const typed = (el, txt, p) => {
    const n = Math.round(p * txt.length), cmd = txt.slice(0, n).replace(/^(\/console)/, '<span class="k">$1</span>');
    el.innerHTML = cmd + (p > 0 && p < 1 || (p >= 1 && Math.floor(t * 3) % 2 === 0 && el.dataset.last === '1') ? '<span class="caret"></span>' : '');
  };
  $('t2a').dataset.last = P.t2b > 0 ? '0' : '1'; $('t2b').dataset.last = '1';
  typed($('t2a'), T2A, P.t2a); typed($('t2b'), T2B, P.t2b);
  ['a', 'b', 'c', 'd'].forEach(k => { const el = $('cc4' + k); el.dataset.last = '0'; typed(el, el.dataset.cmd, P['c4' + k]); });
  // шторка до/после
  $('wAft').style.clipPath = `inset(0 0 0 ${P.w.toFixed(2)}%)`;
  $('wLine').style.left = P.w.toFixed(2) + '%'; $('wKnob').style.left = P.w.toFixed(2) + '%';
  $('wLine').style.opacity = $('wKnob').style.opacity = P.w > 99.5 ? 0 : 1;
  drawSpeed(t);
  subs(t);
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
