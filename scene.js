// Анимация ролика: детерминированная, управляется только временем → window.renderAt(t).
// Тайминг сцен и метки синхронизации приходят из assets/timeline.js (его пишет voice.py).
const H = 1920, FPS = 60;
const MIN = [4, 8, 7, 9, 6];
const LOOP = .55;                              // финальный перелёт камеры обратно к первому кадру
const SC = window.SCENES || MIN.reduce((a, d, i) => (a.push({ start: i ? a[i - 1].start + MIN[i - 1] : 0, dur: d, marks: {} }), a), []);
const DUR = SC.at(-1).start + SC.at(-1).dur + LOOP;
const $ = id => document.getElementById(id);
const SFX = [];
const sfx = (t, type, o = {}) => SFX.push({ t: +t.toFixed(3), type, ...o });
const mk = (i, k, def) => SC[i].marks?.[k] ?? SC[i].start + def;   // метка из озвучки или запасное время

const tl = gsap.timeline({ paused: true, defaults: { ease: 'power2.out' } });
const P = { cam: 0, mb: 0, fade: 0, flash: 0, spd: 0, zs: 1, zx: 540, zy: 960, sm: 0, sm2: 0 };

const W = 1080;
document.querySelectorAll('.sec').forEach((s, i) => { s.style.left = i * W + 'px'; s.style.top = '0px'; });
// ритм: музыка в audio.py — 120 BPM, доля 0.5 с; склейки и переходы ставим на доли
const BEAT = .5, snap = t => Math.round(t / BEAT) * BEAT;
// кинетический текст: слова в [data-fx="kin"] разбиваем на отдельные span.kw
document.querySelectorAll('[data-fx="kin"]').forEach(function split(el) {
  [...el.childNodes].forEach(n => {
    if (n.nodeType === 3) {
      const f = document.createDocumentFragment();
      n.textContent.split(/(\s+)/).forEach(w => { if (!w) return; if (/^\s+$/.test(w)) f.append(w); else { const s = document.createElement('span'); s.className = 'kw'; s.textContent = w; f.append(s); } });
      n.replaceWith(f);
    } else if (n.nodeType === 1 && n.tagName !== 'BR' && !n.classList.contains('kw')) split(n);
  });
});

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
  if (!$('qrsvg')) return;
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

// переходы между сценами (0.5 с, конец — на долю бита). У сцены data-trans: swipe (по умолчанию) | zoom | smear
//   zoom  — камера «влетает» в элемент прошлой сцены с data-zoomto и выходит из элемента новой сцены с data-zoomfrom
//   smear — экран закрашивает красный мазок «помадой», под ним меняется сцена
const secCenter = (sec, sel) => { const el = sec.querySelector(sel); if (!el) return null;
  const r = el.getBoundingClientRect(), s0 = sec.getBoundingClientRect(); return { x: r.left - s0.left + r.width / 2, y: r.top - s0.top + r.height / 2 }; };
const SECS0 = [...document.querySelectorAll('.sec')];
for (let i = 1; i < SC.length; i++) {
  const t = snap(SC[i].start) - .5, tr = SECS0[i]?.dataset.trans || 'swipe';
  if (tr === 'zoom') {
    const a = secCenter(SECS0[i - 1], '[data-zoomto]') || { x: 540, y: 900 }, b = secCenter(SECS0[i], '[data-zoomfrom]') || { x: 540, y: 960 };
    tl.set(P, { zx: a.x, zy: a.y }, t);
    tl.fromTo(P, { zs: 1 }, { zs: 4, duration: .27, ease: 'power3.in', immediateRender: false }, t);
    tl.set(P, { cam: i * H, zx: b.x, zy: b.y, zs: 2.4 }, t + .27);
    tl.to(P, { zs: 1, duration: .33, ease: 'power3.out' }, t + .27);
    tl.set(P, { zx: 540, zy: 960 }, t + .62);
    tl.fromTo(P, { flash: .7 }, { flash: 0, duration: .3, ease: 'power2.out', immediateRender: false }, t + .22);
    tl.fromTo(P, { spd: 1 }, { spd: 0, duration: .6, ease: 'power2.out', immediateRender: false }, t + .1);
    sfx(t, 'riser', { d: .3 }); sfx(t + .27, 'impact', { g: .5 });
  } else if (tr === 'smear') {
    tl.fromTo(P, { sm: 0 }, { sm: 1, duration: .28, ease: 'power2.in', immediateRender: false }, t);
    tl.set(P, { cam: i * H }, t + .28);
    tl.fromTo(P, { sm2: 0 }, { sm2: 1, duration: .3, ease: 'power2.out', immediateRender: false }, t + .3);
    tl.set(P, { sm: 0, sm2: 0 }, t + .61);
    sfx(t, 'swoosh', { f: .8 }); sfx(t + .3, 'swish');
  } else {
    tl.fromTo(P, { cam: (i - 1) * H }, { cam: i * H, duration: .5, ease: 'power3.inOut', immediateRender: false }, t);
    tl.fromTo(P, { mb: 0 }, { mb: 34, duration: .25, ease: 'power2.in', immediateRender: false }, t);
    tl.to(P, { mb: 0, duration: .25, ease: 'power2.out' }, t + .25);
    tl.fromTo(P, { spd: 1 }, { spd: 0, duration: .6, ease: 'power2.out', immediateRender: false }, t + .05);
    tl.fromTo(P, { flash: .3 }, { flash: 0, duration: .3, ease: 'power2.out', immediateRender: false }, t + .45);
    sfx(t, 'whoosh', { d: .5 }); sfx(t + .45, 'thump', { g: .55 });
  }
  const c = CONN[i - 1];
  tl.fromTo(c.el, { height: 0, opacity: 0 }, { height: c.len, opacity: 1, duration: .45, ease: 'power2.inOut', immediateRender: false }, t + .05);
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
const KINS = [];                                     // кинетический текст: слова подпрыгивают, когда их произносит голос
const COUNTS = [];                                   // счётчики: { el, o: { v }, ph }
const VIDS = [];                                     // видео-вставки: { img, name, from, rate, n, t0, t1 }
const BURSTS = [];                                   // взрывы частиц: { t, x, y (мировые координаты), c }
const SECS = [...document.querySelectorAll('.sec')];
const POS = new Map();                               // центры элементов до анимаций (для частиц)
document.querySelectorAll('[data-fx], [data-shatter]').forEach(el => {
  const r = el.getBoundingClientRect(); POS.set(el, { x: r.left + r.width / 2, y: r.top + r.height / 2 });
});
const burstAt = (t, el, c = '200,16,46') => { const p = POS.get(el) || { x: 540, y: 800 }; BURSTS.push({ t, x: p.x, y: p.y, c }); };
let nsnd = 0;
const FX = {
  pop:   (el, t) => { pop(el, t, { s: .5, d: .4 }); sfx(t, 'pop', { f: .9 + (nsnd++ % 5) * .08 }); },
  left:  (el, t) => { pop(el, t, { x: -280, r: -6, s: .85, d: .42, ease: 'back.out(1.6)' }); sfx(t, 'swoosh', { f: 1.1 }); },
  right: (el, t) => { pop(el, t, { x: 280, r: 6, s: .85, d: .42, ease: 'back.out(1.6)' }); sfx(t, 'swoosh', { f: .95 }); },
  up:    (el, t) => { pop(el, t, { y: 280, s: .85, d: .45, ease: 'back.out(1.5)' }); sfx(t, 'swoosh', { f: .85 }); },
  zoom:  (el, t) => { pop(el, t, { s: 1.6, o: 0, d: .4, ease: 'back.out(2.2)' }); sfx(t, 'thump', { g: .75 }); },
  draw:  (el, t) => { tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: .15, immediateRender: false }, t); tl.set(el, { opacity: 0 }, 0);
                      const ps = [...el.querySelectorAll('.dr')];
                      ps.forEach((p, k) => tl.fromTo(p, { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: .55, ease: 'power2.inOut', immediateRender: true }, t + k * .12));
                      sfx(t, 'zip', { d: .5 }); },
  drop:  (el, t) => { tl.set(el, { opacity: 0 }, 0); tl.set(el, { opacity: 1 }, t);   // до падения скрыт — не висит над экраном
                      tl.fromTo(el, { y: -900, rotation: (POS.get(el)?.x % 2 ? 25 : -25) }, { y: 0, rotation: 0, duration: .75, ease: 'bounce.out', immediateRender: true }, t); sfx(t + .45, 'thump', { g: .45 }); },
  grow:  (el, t) => { const [k, v] = el.dataset.h ? ['height', el.dataset.h] : ['width', el.dataset.w || '0,100'], [a, b] = v.split(',');   // столбики/полоски растут
                      tl.fromTo(el, { [k]: a + '%' }, { [k]: b + '%', duration: .8, ease: 'power3.out', immediateRender: true }, t); sfx(t, 'swoosh', { f: 1.2, g: .5 }); },
  kin:   (el, t) => { const ws = [...el.querySelectorAll('.kw')];
                      // строки влетают по очереди (раньше слова разных строк налезали друг на друга)
                      const tops = [...new Set(ws.map(w => w.offsetTop))].sort((a, b) => a - b);
                      const dl = ws.map(w => { const row = ws.filter(v => v.offsetTop === w.offsetTop); return tops.indexOf(w.offsetTop) * .26 + row.indexOf(w) * .08; });
                      ws.forEach((w, k) => tl.fromTo(w, { y: 90, scale: .2, opacity: 0, rotation: k % 2 ? 12 : -12 }, { y: 0, scale: 1, opacity: 1, rotation: 0, duration: .45, ease: 'back.out(2.4)' }, t + dl[k]));
                      ws.forEach((w, k) => k % 2 || sfx(t + dl[k], 'pop', { f: 1 + k * .06, g: .55 }));
                      KINS.push({ ws, t }); },
  // стикер-персонаж: падает и «плюхается» с пружинкой (сплющивается и отскакивает)
  plop:  (el, t) => { tl.set(el, { opacity: 0 }, 0); tl.set(el, { opacity: 1 }, t);
                      tl.fromTo(el, { y: -900 }, { y: 0, duration: .4, ease: 'power2.in', immediateRender: true }, t);
                      tl.fromTo(el, { scaleX: 1, scaleY: 1 }, { keyframes: { scaleX: [1, 1.22, .9, 1.04, 1], scaleY: [1, .76, 1.1, .97, 1] }, duration: .55, ease: 'none', transformOrigin: '50% 100%', immediateRender: false }, t + .4);
                      sfx(t + .4, 'thump', { g: .7 }); sfx(t + .45, 'bonk'); },
  // выглядывает из-за края экрана (data-from="left|right|bottom", data-rot — наклон в конце)
  peek:  (el, t) => { const f = el.dataset.from || 'right', r = +(el.dataset.rot || 0);
                      tl.set(el, { opacity: 0 }, 0); tl.set(el, { opacity: 1 }, t);   // до выезда скрыт, иначе виден на соседней сцене
                      tl.fromTo(el, { x: f === 'left' ? -650 : f === 'right' ? 650 : 0, y: f === 'bottom' ? 700 : 0, rotation: r + (f === 'left' ? -25 : 25) },
                        { x: 0, y: 0, rotation: r, duration: .55, ease: 'back.out(1.6)', immediateRender: true }, t); sfx(t, 'swoosh', { f: .9 }); },
  // облачко-реплика: раздувается из хвостика (transform-origin задан в CSS у .bubble)
  bub:   (el, t) => { tl.fromTo(el, { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: .45, ease: 'back.out(2.2)', immediateRender: true }, t); sfx(t, 'blip', { f: 1.1 }); },
  write: (el, t) => { tl.fromTo(el, { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: .9, ease: 'power1.inOut', immediateRender: true }, t); sfx(t, 'zip', { d: .8 }); },
  slam:  (el, t) => { tl.set(el, { opacity: 0 }, 0); slamIn(el, t); shake(el.closest('.layer') || el, t + .24); burstAt(t + .24, el); sfx(t + .22, 'impact', { g: .6 }); },
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
    (el.dataset.react || '').split(',').filter(Boolean).forEach(k => { const m = SC[i].marks?.[k]; if (m == null || m < t0 || m > t1) return;
      tl.to(el, { keyframes: { rotation: [0, -9, 8, -4, 0], scale: [1, 1.12, .98, 1.04, 1] }, duration: .5, ease: 'none' }, m - .05); sfx(m - .05, 'bonk'); });
  });
  // «рассыпание» вещей на метке
  [...layer.querySelectorAll('[data-shatter]')].forEach((el, k) => {
    const m = SC[i].marks?.[el.dataset.shatter], t = Math.min(t1 - .5, Math.max(t0 + .9, m != null ? m + .15 : t0 + 1.4)) + k * .06;
    tl.to(el, { scale: 0, rotation: k % 2 ? 40 : -40, opacity: 0, duration: .26, ease: 'back.in(2.2)', immediateRender: false }, t);
    burstAt(t + .2, el, k % 2 ? '26,163,107' : '200,16,46'); if (k % 2 === 0) sfx(t + .2, 'impact', { g: .35 });
  });
  // видео: кадры из assets/video/<имя>/f_0001.jpg, 30 кадров/с; звук клипа — из assets/video/<имя>.wav
  layer.querySelectorAll('.vid').forEach(v => {
    const o = { img: v.querySelector('img'), name: v.dataset.video, from: +(v.dataset.from || 0), rate: +(v.dataset.rate || 1),
                n: +(v.dataset.frames || 1), t0, t1 };
    VIDS.push(o);
    if (o.rate === 1 && v.dataset.audio !== '0')
      SFX.push({ t: +t0.toFixed(3), type: 'clip', file: `assets/video/${o.name}.wav`, from: o.from, d: +(t1 - t0).toFixed(3), g: +(v.dataset.gain || .45) });
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
    c = Math.max(prev + 1.2, snap(c));                              // склейка — на долю бита
    cuts.push(c); CUTS.push(c);
    if (n === 0 && i > 0) tl.to(CONN[i - 1].el, { opacity: 0, duration: .15, immediateRender: false }, c - .1);   // стрелка перехода не мешает второму кадру
    tl.set(L[n], { opacity: 0 }, c); tl.set(layer, { opacity: 1 }, c);
    tl.fromTo(layer, { scale: 1.07 }, { scale: 1, duration: .35, ease: 'power2.out', immediateRender: false }, c);
    flashAt(c, .45, .25); speedAt(c, .45); BURSTS.push({ t: c, x: i * W + 540, y: 760, c: '200,16,46' });
    sfx(c - .06, 'whoosh', { d: .3 }); sfx(c, 'thump', { g: .6 });
  });
  // первый кадр сцены начинает оживать, когда камера приезжает (переход кончается на доле бита, иногда раньше начала реплики)
  L.forEach((layer, n) => layerFx(layer, i, n ? cuts[n - 1] : (i ? Math.min(s, snap(s)) - .15 : 0), cuts[n] ?? e));
});

// хук: удар в первые 0.05 с; элементы .hk по очереди «щёлкают», .hkx трясёт (2-й удар), заголовок пульсирует (3-й)
{
  const A = SECS[0].querySelector('.layer.A');
  flashAt(.04, .6, .4); speedAt(.04, .7); shake(A, .04); sfx(.04, 'impact', { g: .8 }); sfx(.04, 'thump');
  A.querySelectorAll('.hk').forEach((o, k) => { const t = .3 + k * .14; pulse(o, t, 1.12); sfx(t, 'tick', { f: 1 + k * .12, g: .5 }); });
  A.querySelectorAll('.hkx').forEach(d => { pulse(d, .95, 1.12); shake(d, .95); }); sfx(.95, 'impact', { g: .6 });
  pulse(A.querySelector('.h1') || A.querySelector('.card'), 1.45, 1.05); sfx(1.45, 'bonk');
}
// финал: гайд пульсирует, кнопка-призыв качается
{
  const i = SECS.length - 1, s = CUTS.at(-1) ?? SC[i].start, b = mk(i, 'b', SC[i].dur - 1.5);
  const g = $('guide');
  tl.fromTo(g, { rotation: -4 }, { rotation: 0, duration: .5, ease: 'back.out(2)', immediateRender: false }, s + .05);
  pulse('#guide', Math.max(s + .9, b - .2), 1.05); sfx(Math.max(s + .9, b - .2), 'ding', { f: 1.2 });
  tl.to('#cta', { keyframes: { rotation: [0, -4, 4, -3, 0] }, duration: .6, ease: 'none' }, Math.max(s + 1.2, b + .4));
  for (let t = s + 1.4; t < DUR - LOOP - .4; t += 1) pulse('#cta', t, 1.06);   // плашка «пиши ДЕСЕРТ» мягко пульсирует до конца
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
const BG_FOREST = [1, 1, 0, 1, 1, 0];          // 0 — Тёмный портал (bgA), 1 — лес (bgB)
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
    spc.strokeStyle = `rgba(18,18,18,${(P.spd * .22).toFixed(3)})`; spc.lineWidth = l.w;
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
    const x0 = b.x - P.cam / H * W, y0 = b.y; if (x0 < -500 || x0 > 1600) continue;
    const life = 1 - dt / .9;
    for (let k = 0; k < 28; k++) {
      const ang = k / 28 * Math.PI * 2 + (b.t * 7 % 1), sp = 380 + ((k * 37) % 11) * 45;
      const x = x0 + Math.cos(ang) * sp * dt, y = y0 + Math.sin(ang) * sp * dt + 700 * dt * dt;
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
    const chars = cur.reduce((n, c) => n + c.w.length + 1, 0);
    if (cur.length >= 3 || /[.,!?:;…]$/.test(w) || (chars > 15 && cur.length >= 2)) flush();
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
    let fs = Math.max(66, Math.min(100, 860 / Math.max(chars * .6, longest * .7)));   // вся фраза — максимум в 2 строки
    el.innerHTML = `<div class="ln" style="font-size:${fs.toFixed(0)}px">` + c.words.map(w => `<span class="w">${(/^[—–]$/.test(w.w) ? '' : w.w)}</span>`).join('') + '</div>';
    // подгон по реальной ширине: у Unbounded широкие заглавные, оценка по буквам ошибалась и текст вылезал за край
    const ln0 = el.firstChild, fits = () => [...ln0.children].every(sp => sp.offsetWidth <= 840) && ln0.offsetHeight <= fs * 1.36 * 2 + 14;
    while (!fits() && fs > 40) { fs -= 3; ln0.style.fontSize = fs + 'px'; }
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

// ---------------------------------------------------------------- микродвижение, зерно, фон
const rnd = (k, n) => { const x = Math.sin(k * 127.1 + n * 311.7) * 43758.5453; return x - Math.floor(x); };
const MICRO = [...document.querySelectorAll('.card,.tst,.plate,.lbl,.tag,.prop,.h1,.h2,.ul:not(.spin),.clay,.bubble')].map((el, k) => ({ el, k, br: el.classList.contains('tst') }));
function micro(t) {
  for (const m of MICRO) {
    const a = 2 * Math.PI * (.12 + rnd(m.k, 1) * .1), ph = rnd(m.k, 2) * 6.28, amp = m.el.classList.contains('h1') || m.el.classList.contains('h2') ? 4 : 9;
    m.el.style.translate = `${(Math.sin(t * a * .7 + ph) * amp * .6).toFixed(2)}px ${(Math.sin(t * a + ph) * amp).toFixed(2)}px`;
    m.el.style.rotate = `${(Math.sin(t * a * .8 + ph * 1.3) * (m.br ? 3 : .8)).toFixed(2)}deg`;
    if (m.br) m.el.style.scale = (1 + .035 * Math.sin(t * 2.6 + ph)).toFixed(4);   // стикеры «дышат»
  }
  document.querySelectorAll('.spin').forEach(el => (el.style.rotate = `${(-t * 30).toFixed(2)}deg`));   // круг медленно крутится
  // пузырьки в стакане и блик
  document.querySelectorAll('.bub').forEach((b, k) => {
    const sp = 60 + rnd(k, 3) * 60, y = 330 - ((t * sp + rnd(k, 4) * 300) % 300);
    b.setAttribute('cy', y.toFixed(1)); b.setAttribute('cx', (rnd(k, 5) * 160 + 60 + Math.sin(t * 3 + k) * 6).toFixed(1));
  });
  document.querySelectorAll('.glint').forEach((g, k) => { const p = ((t * .45 + k * .37) % 1.6) - .3; g.setAttribute('transform', `translate(${(p * 400).toFixed(1)} 0) skewX(-20)`); });
  // кинетический текст: слово подпрыгивает, когда голос его произносит
  for (const kn of KINS) kn.ws.forEach(w => { if (w._t == null) {
      const key = w.textContent.toLowerCase().replace(/[^а-яёa-z0-9]/g, ''); const sc = SC.find(s => kn.t >= s.start - .5 && kn.t < s.start + s.dur);
      const hit = (sc?.words || []).find(([tw, ww]) => tw >= kn.t - .3 && ww.toLowerCase().replace(/[^а-яёa-z0-9]/g, '') === key); w._t = hit ? hit[0] : -1; }
    const d = t - w._t; w.style.translate = w._t > 0 && d > 0 && d < .35 ? `0 ${(-26 * Math.sin(Math.PI * d / .35)).toFixed(1)}px` : '0 0';
    w.classList.toggle('hot', w._t > 0 && d > 0 && d < .45);
  });
}
const gc = document.getElementById('grain')?.getContext('2d'), GT = [];
// зерно — один неподвижный кадр, еле заметный: живая «рябь» 24 раза в секунду утомляла глаза
if (gc) { const im = gc.createImageData(360, 640); for (let i = 0; i < im.data.length; i += 4) { const v = 128 + (rnd(i, 1) - .5) * 160; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; } gc.putImageData(im, 0, 0); }
function grain(t) {}
function blobs(t) { document.querySelectorAll('.blob').forEach((b, k) => {
  b.style.translate = `${(Math.sin(t * .12 + k * 2) * 50 - P.cam / H * 60).toFixed(1)}px ${(Math.cos(t * .1 + k) * 40).toFixed(1)}px`; }); }

// ---------------------------------------------------------------- кадр
let lastFilter = '';
function apply(t) {
  const camX = P.cam / H * W, fr0 = (P.cam / H) % 1, sw = Math.sin(Math.PI * fr0);
  $('world').style.transformOrigin = `${(camX + P.zx).toFixed(1)}px ${P.zy.toFixed(1)}px`;
  $('world').style.transform = `translate3d(${(-camX).toFixed(1)}px,0,0) scale(${((1 - .08 * sw) * P.zs).toFixed(4)})`;
  // мазок помадой: рисуется (sm) и стирается с начала (sm2)
  const smp = $('smearp'); if (smp) { const len = Math.max(0, P.sm - P.sm2); smp.style.strokeDasharray = `${len.toFixed(4)} 3`; smp.style.strokeDashoffset = (-P.sm2).toFixed(4); smp.style.opacity = len > 0 ? 1 : 0; }
  micro(t); grain(t); blobs(t);
  $('grid').style.transform = `translate3d(0,${-(P.cam % 108)}px,0)`;
  $('star').style.transform = `rotate(${(t * 3 + P.cam * .012).toFixed(2)}deg) scale(${1 + .03 * Math.sin(t * .8)})`;
  $('arc').style.transform = `rotate(${(-t * 5 - P.cam * .02).toFixed(2)}deg)`;
  const f = P.mb > .3 ? 'url(#mb)' : 'none';
  $('mbg').setAttribute('stdDeviation', `${P.mb.toFixed(2)} 0`);
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
  // видео: нужный кадр клипа; рендер ждёт загрузку картинки
  for (const v of VIDS) {
    const loopBack = v.t0 === 0 && t >= DUR - LOOP;        // петля: первый кадр ролика снова с начала клипа
    if (!loopBack && (t < v.t0 - .05 || t > v.t1 + .05)) continue;
    const vt = loopBack ? v.from : Math.max(0, Math.min((v.n - 1) / 30, v.from + (Math.max(t, v.t0) - v.t0) * v.rate));
    const src = `assets/video/${v.name}/f_${String(Math.floor(vt * 30) + 1).padStart(4, '0')}.jpg`;
    if (v.img.dataset.cur !== src) {
      v.img.dataset.cur = src; v.img.src = src;
      PENDING.push(new Promise(r => { if (v.img.complete && v.img.naturalWidth) return r();
        v.img.addEventListener('load', r, { once: true }); v.img.addEventListener('error', r, { once: true }); setTimeout(r, 5000); }));
    }
  }
  // сторис: полоски прогресса по сценам
  document.querySelectorAll('#bars b').forEach((b, k) => {
    const sc = SC[k]; if (!sc) return;
    const p = t >= DUR - LOOP ? 0 : Math.max(0, Math.min(1, (t - sc.start) / sc.dur));
    b.style.width = (p * 100).toFixed(2) + '%';
  });
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

let PENDING = [];
window.renderAt = t => { PENDING = []; tl.seek(Math.min(t, DUR), false); apply(t); return PENDING.length ? Promise.all(PENDING) : undefined; };
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
