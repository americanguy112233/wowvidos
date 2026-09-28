// Анимация ролика: детерминированная, управляется только временем → window.renderAt(t).
// Тайминг сцен и метки синхронизации приходят из assets/timeline.js (его пишет voice.py).
const H = 1920, FPS = 60;
const MIN = [3.8, 5.5, 5.5, 6.5, 5.5, 6.5, 6.5, 6];
const LOOP = .55;                              // финальный перелёт камеры обратно к первому кадру
const SC = window.SCENES || MIN.reduce((a, d, i) => (a.push({ start: i ? a[i - 1].start + MIN[i - 1] : 0, dur: d, marks: {} }), a), []);
const DUR = SC.at(-1).start + SC.at(-1).dur + LOOP;
const $ = id => document.getElementById(id);
const SFX = [];
const sfx = (t, type, o = {}) => SFX.push({ t: +t.toFixed(3), type, ...o });
const mk = (i, k, def) => SC[i].marks?.[k] ?? SC[i].start + def;   // метка из озвучки или запасное время

const tl = gsap.timeline({ paused: true, defaults: { ease: 'power2.out' } });
const P = { cam: 0, mb: 0, fade: 0, flash: 0, spd: 0 };

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

// ================================================================ движок монтажа: сцена = кадр A → склейка → кадр B
// Всё управляется разметкой в index.html: data-fx, data-mark, data-at, data-count, data-shatter.
const COUNTS = [];                                   // счётчики: { el, o: { v }, ph }
const BURSTS = [];                                   // взрывы частиц: { t, x, y (мировые координаты), c }
const SECS = [...document.querySelectorAll('.sec')];
const POS = new Map();                               // центры элементов до анимаций (для частиц)
document.querySelectorAll('[data-fx], [data-shatter]').forEach(el => {
  const r = el.getBoundingClientRect(); POS.set(el, { x: r.left + r.width / 2, y: r.top + r.height / 2 });
});
const burstAt = (t, el, c = '255,209,0') => { const p = POS.get(el) || { x: 540, y: 800 }; BURSTS.push({ t, x: p.x, y: p.y, c }); };
let nsnd = 0;
const FX = {
  pop:   (el, t) => { pop(el, t, { s: .5, d: .4 }); sfx(t, 'pop', { f: .9 + (nsnd++ % 5) * .08 }); },
  left:  (el, t) => { pop(el, t, { x: -280, r: -6, s: .85, d: .42, ease: 'back.out(1.6)' }); sfx(t, 'swoosh', { f: 1.1 }); },
  right: (el, t) => { pop(el, t, { x: 280, r: 6, s: .85, d: .42, ease: 'back.out(1.6)' }); sfx(t, 'swoosh', { f: .95 }); },
  up:    (el, t) => { pop(el, t, { y: 280, s: .85, d: .45, ease: 'back.out(1.5)' }); sfx(t, 'swoosh', { f: .85 }); },
  zoom:  (el, t) => { pop(el, t, { s: 1.6, o: 0, d: .4, ease: 'back.out(2.2)' }); sfx(t, 'thump', { g: .75 }); },
  slam:  (el, t) => { slamIn(el, t); shake(el.closest('.layer') || el, t + .24); burstAt(t + .24, el); sfx(t + .22, 'impact', { g: .6 }); },
};
function startCount(el, t) {
  el.querySelectorAll('[data-count]').forEach(c => {
    const [a, b] = c.dataset.count.split(',').map(Number), t0 = c.dataset.atAbs ? +c.dataset.atAbs : t + .15;
    const o = { v: -1 }; COUNTS.push({ el: c, o, ph: c.dataset.ph ?? String(a) });
    tl.fromTo(o, { v: a }, { v: b, duration: .75, ease: 'power2.in', immediateRender: false }, t0);
    ticks(t0, .75, 10, 1, 2.1); sfx(t0 + .75, 'coin');
  });
}
function layerFx(layer, i, t0, t1) {
  const els = [...layer.querySelectorAll('[data-fx]')];
  els.forEach((el, k) => {
    const at = el.dataset.at != null ? +el.dataset.at : null;
    let t;
    if (el.dataset.mark) {
      const m = SC[i].marks?.[el.dataset.mark];
      t = Math.max(t0 + .05, m != null ? m - .1 : t0 + .45 + k * .18) + (at || 0);
    } else t = t0 + (at ?? (.06 + k * .12));
    t = Math.min(t, t1 - .35);                        // успеть показать до склейки
    if (el.dataset.fx === 'punch') {                 // кадр 0: элемент уже на месте, лишь «ударяется»
      tl.fromTo(el, { scale: 1.28 }, { scale: 1, duration: .5, ease: 'back.out(3)', immediateRender: false }, .04 + k * .03);
    } else (FX[el.dataset.fx] || FX.pop)(el, t);
    startCount(el, t);
  });
  // «рассыпание» вещей на метке
  [...layer.querySelectorAll('[data-shatter]')].forEach((el, k) => {
    const m = SC[i].marks?.[el.dataset.shatter], t = Math.min(t1 - .5, Math.max(t0 + .9, m != null ? m + .15 : t0 + 1.4)) + k * .06;
    tl.to(el, { scale: 0, rotation: k % 2 ? 40 : -40, opacity: 0, duration: .26, ease: 'back.in(2.2)', immediateRender: false }, t);
    burstAt(t + .2, el, k % 2 ? '120,255,150' : '255,209,0'); if (k % 2 === 0) sfx(t + .2, 'impact', { g: .35 });
  });
  // медленный наезд на скриншоты
  layer.querySelectorAll('.shotz img').forEach(img =>
    tl.fromTo(img, { scale: 1 }, { scale: 1.12, duration: Math.max(.5, t1 - t0), ease: 'none', immediateRender: false }, t0));
}
const CUTS = [];
SECS.forEach((sec, i) => {
  const s = i ? SC[i].start : 0, e = SC[i].start + SC[i].dur;
  const L = [...sec.querySelectorAll(':scope > .layer')];
  const cuts = [];
  L.slice(1).forEach((layer, n) => {
    const key = ['x', 'y', 'z'][n], m = SC[i].marks?.[key];
    let c = m != null ? m - .12 : s + SC[i].dur * (n + 1) / L.length;
    const prev = cuts.at(-1) ?? s;
    c = Math.max(prev + 1.3, Math.min(e - 1.4 * (L.length - 1 - n), c));
    if (i === 0 && n === 0) c = Math.min(Math.max(c, 1.6), 2.2);   // хук: склейка до 2.2 с
    cuts.push(c); CUTS.push(c);
    if (n === 0 && i > 0) tl.to(CONN[i - 1].el, { opacity: 0, duration: .15, immediateRender: false }, c - .1);   // стрелка перехода не мешает второму кадру
    tl.set(L[n], { opacity: 0 }, c); tl.set(layer, { opacity: 1 }, c);
    tl.fromTo(layer, { scale: 1.07 }, { scale: 1, duration: .35, ease: 'power2.out', immediateRender: false }, c);
    flashAt(c, .85, .3); speedAt(c, .45); BURSTS.push({ t: c, x: 540, y: i * H + 760, c: '255,220,140' });
    sfx(c - .06, 'whoosh', { d: .3 }); sfx(c, 'thump', { g: .6 });
  });
  L.forEach((layer, n) => layerFx(layer, i, n ? cuts[n - 1] : (i ? s + .02 : 0), cuts[n] ?? e));
});

// хук: удар в первые 0.05 с, счётчик «??» → 45, пульс кнопки
{
  const A = SECS[0].querySelector('.layer.A');
  flashAt(.04, .95, .45); speedAt(.04, .8); shake(A, .04); sfx(.04, 'impact', { g: .9 }); sfx(.04, 'thump');
  pulse('#dc2', 1.08, 1.1); glowC('#dc2', 1.08, '82,240,138'); burstAt(1.08, $('dc2'), '82,240,138'); flashAt(1.08, .5, .3); sfx(1.08, 'success');
  pulse('#p1', 1.4, 1.12);
}
// финал: QR собирается из модулей, пульс кнопки на метке «наводи камеру»
{
  const i = SECS.length - 1, s = CUTS.at(-1) ?? SC[i].start, a = mk(i, 'a', SC[i].dur - 2);
  tl.fromTo('#qrsvg .qm', { opacity: 0, scale: .2, transformOrigin: '50% 50%' },
    { opacity: 1, scale: 1, duration: .3, ease: 'back.out(2)', stagger: { each: 0, from: 'center', amount: .5 } }, s + .3);
  tl.fromTo('#qrsvg .qf', { opacity: 0 }, { opacity: 1, duration: .25 }, s + .35);
  ticks(s + .3, .5, 6, 1.2, 1.9);
  pop('#qrlogo', s + .75, { s: .2, d: .5, ease: 'back.out(2.5)' }); sfx(s + .75, 'pop', { f: 1.3 });
  const a0 = Math.max(s + 1.3, a);
  pulse('#p8', a0, 1.14); sfx(a0, 'ding', { f: 1.2 });
  // смена кадра без склейки: наезд на QR (код остаётся на экране и читается)
  const fin = SECS[i].querySelector(':scope > .layer:last-of-type');
  tl.fromTo(fin, { scale: 1 }, { scale: 1.13, duration: .5, ease: 'power3.out', immediateRender: false, transformOrigin: '50% 38%' }, a0 - .05);
  flashAt(a0 - .05, .5, .25); speedAt(a0 - .05, .4);
}
// петля: камера перелетает к первому кадру, он возвращается в исходное состояние
{
  const L0 = DUR - LOOP, A = SECS[0].querySelector('.layer.A'), B = SECS[0].querySelector('.layer.B');
  tl.fromTo(P, { cam: (SECS.length - 1) * H }, { cam: 0, duration: LOOP, ease: 'power3.in', immediateRender: false }, L0);
  tl.fromTo(P, { mb: 0 }, { mb: 60, duration: LOOP * .8, ease: 'power2.in', immediateRender: false }, L0);
  speedAt(L0, LOOP);
  tl.set(A, { opacity: 1 }, L0); SECS[0].querySelectorAll(':scope > .layer:not(.A)').forEach(l => tl.set(l, { opacity: 0 }, L0));
  COUNTS.filter(c => SECS[0].contains(c.el)).forEach(c => tl.set(c.o, { v: -1 }, L0));
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
const BG_FOREST = [0, 0, 0, 1, 1, 0, 1, 0];    // 0 — Тёмный портал (bgA), 1 — тропа (bgB)
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

// ---------------------------------------------------------------- взрывы частиц (детерминированные)
const fxc = document.getElementById('fx').getContext('2d');
function drawBursts(t) {
  fxc.clearRect(0, 0, 1080, 1920);
  for (const b of BURSTS) {
    const dt = t - b.t; if (dt < 0 || dt > .9) continue;
    const y0 = b.y - P.cam; if (y0 < -400 || y0 > 2300) continue;
    const life = 1 - dt / .9;
    for (let k = 0; k < 28; k++) {
      const ang = k / 28 * Math.PI * 2 + (b.t * 7 % 1), sp = 380 + ((k * 37) % 11) * 45;
      const x = b.x + Math.cos(ang) * sp * dt, y = y0 + Math.sin(ang) * sp * dt + 700 * dt * dt;
      fxc.fillStyle = `rgba(${b.c},${(life * .95).toFixed(3)})`;
      fxc.beginPath(); fxc.arc(x, y, 3 + life * 7 * ((k % 3) / 2 + .5), 0, 7); fxc.fill();
    }
  }
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
  // счётчики
  for (const c of COUNTS) { const v = c.o.v < 0 ? c.ph : String(Math.round(c.o.v)); if (c.el.textContent !== v) c.el.textContent = v; }
  drawBursts(t);
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
window.CUTS = CUTS;
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
