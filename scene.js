// Анимация ролика: детерминированная, управляется только временем → window.renderAt(t).
// Тайминг сцен и метки синхронизации приходят из assets/timeline.js (его пишет voice.py).
const H = 1920, FPS = 60;
const MIN = [4, 4.5, 4.5, 5, 5, 3.5];
const LOOP = .55;                              // финальный перелёт камеры обратно к первому кадру
const SC = window.SCENES || MIN.reduce((a, d, i) => (a.push({ start: i ? a[i - 1].start + MIN[i - 1] : 0, dur: d, marks: {} }), a), []);
const DUR = SC.at(-1).start + SC.at(-1).dur + LOOP;
const $ = id => document.getElementById(id);
const SFX = [];
const sfx = (t, type, o = {}) => SFX.push({ t: +t.toFixed(3), type, ...o });
const mk = (i, k, def) => SC[i].marks?.[k] ?? SC[i].start + def;   // метка из озвучки или запасное время

const tl = gsap.timeline({ paused: true, defaults: { ease: 'power2.out' } });
const P = { cam: 0, mb: 0, fade: 0, flash: 0, pct: 70 };
// данные из графиков игрока (9150 уникальных персонажей Альянса, неделя бэты Forever)
const CLASSES = [['Паладин', 1349, 14.7, '#F58CBA'], ['Охотник', 1324, 14.5, '#ABD473'], ['Маг', 1238, 13.5, '#3FC7EB'],
  ['Воин', 1128, 12.3, '#C79C6E'], ['Жрец', 977, 10.7, '#FFFFFF'], ['Шаман', 963, 10.5, '#0070DE'],
  ['Друид', 859, 9.4, '#FF7D0A'], ['Чернокнижник', 751, 8.2, '#8787ED'], ['Разбойник', 561, 6.1, '#FFF569']];
const RACES = [['Люди', 2878, 31.5, '#e3bd5e'], ['Дворфы', 1845, 20.2, '#b8733c'], ['Небесно­рожденные', 1768, 19.3, '#5ec8ff'],
  ['Гномы', 1653, 18.1, '#e98bd0'], ['Ночные эльфы', 1006, 11.0, '#9b7bff']];
const COMBOS = [1018, 963, 22];
const CV = CLASSES.map(() => ({ v: 0 })), RV = RACES.map(() => ({ v: 0 })), KV = COMBOS.map(() => ({ v: 0 }));
const buildBars = (id, data, big) => {
  $(id).innerHTML = data.map(([n, , , c], k) => `<div class="br${big ? ' big' : ''}" id="${id}${k}">
    <div class="nm"${n.length > 10 ? ' style="font-size:' + (big ? 34 : 27) + 'px"' : ''}>${n}</div>
    <div class="tr"><div class="fl" id="${id}f${k}" style="background:linear-gradient(90deg, ${c}cc, ${c})"></div></div>
    <div class="vl" id="${id}v${k}">0</div></div>`).join('');
};
buildBars('cls', CLASSES, false); buildBars('rcs', RACES, true);
const addTag = (row, text, cls = '') => { const d = document.createElement('div'); d.className = 'tagw ' + cls; d.textContent = text; $(row).appendChild(d); return d; };

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

const glowC = (el, t, rgb) => tl.fromTo(el, { boxShadow: `0 0 0 0px rgba(${rgb},0), 0 0 0 rgba(${rgb},0)` },
  { boxShadow: `0 0 0 5px rgba(${rgb},1), 0 0 44px rgba(${rgb},.5)`, duration: .3, immediateRender: false }, t);
const grow = (fill, obj, val, max, t, d = .7) => {
  tl.fromTo(fill, { width: '0%' }, { width: (val / max * 100).toFixed(1) + '%', duration: d, ease: 'power3.out', immediateRender: false }, t);
  tl.fromTo(obj, { v: 0 }, { v: val, duration: d, ease: 'power3.out', immediateRender: false }, t);
};
const hide = (el) => tl.set(el, { opacity: 0 }, 0);

// ================================================================ 1. хук: кадр 0 уже полный, удар в первые 0.05 с
{
  const a = mk(0, 'a', 1.7), b = mk(0, 'b', 3.0), h = .04;
  tl.fromTo(P, { flash: .95 }, { flash: 0, duration: .45, ease: 'power2.out', immediateRender: false }, h);
  tl.fromTo('#n1', { scale: 1.45 }, { scale: 1, duration: .5, ease: 'back.out(3)', immediateRender: false }, h);
  tl.fromTo('#st1', { scale: .6, rotation: -14 }, { scale: 1, rotation: 0, duration: .6, ease: 'back.out(2.6)', immediateRender: false }, h + .05);
  shake('#s1', h); sfx(h, 'impact', { g: .9 }); sfx(h, 'thump'); sfx(h + .1, 'sparkle');
  pulse('#n1', Math.max(h + .7, a - .05), 1.12); sfx(Math.max(h + .7, a - .05), 'coin');
  pulse('#p1', Math.max(h + 1.2, b - .05), 1.12); sfx(Math.max(h + 1.2, b - .05), 'pop', { f: 1.2 });
}

// ================================================================ 2. классы
{
  const s = SC[1].start, a = mk(1, 'a', .9), b = mk(1, 'b', 3.0);
  hdr(1, '#h2');
  const max = CLASSES[0][1];
  CLASSES.forEach((c, k) => {
    const t = s + .2 + k * .06;
    pop('#cls' + k, t, { x: -120, s: .95, d: .4, ease: 'back.out(1.4)' });
    grow('#clsf' + k, CV[k], c[1], max, t + .12, .75);
    if (k % 2 === 0) sfx(t, 'tick', { f: 1 + k * .08, g: .6 });
  });
  const top = addTag('cls0', 'ТОП-1', 'gold'), last = addTag('cls8', 'ПОСЛЕДНИЙ');
  hide(top); hide(last);
  const a0 = Math.max(s + .9, a - .05);
  pop(top, a0, { s: .3, d: .35 }); glowC('#cls0', a0, '255,209,0'); pulse('#cls0', a0, 1.04); sfx(a0, 'success');
  const b0 = Math.max(a0 + .8, b - .05);
  pop(last, b0, { s: .3, d: .35 }); glowC('#cls8', b0, '232,51,42'); shake('#cls8', b0); sfx(b0, 'bonk');
}

// ================================================================ 3. расы
{
  const s = SC[2].start, a = mk(2, 'a', .9), b = mk(2, 'b', 2.8);
  hdr(2, '#h3');
  const max = RACES[0][1];
  RACES.forEach((r, k) => {
    const t = s + .2 + k * .08;
    pop('#rcs' + k, t, { x: 120, s: .95, d: .4, ease: 'back.out(1.4)' });
    grow('#rcsf' + k, RV[k], r[1], max, t + .12, .8);
    sfx(t, 'tick', { f: 1 + k * .1, g: .6 });
  });
  const third = addTag('rcs0', 'ПОЧТИ ТРЕТЬ', 'gold'), fresh = addTag('rcs2', 'НОВАЯ РАСА', 'blue');
  hide(third); hide(fresh); hide('#k3');
  const a0 = Math.max(s + .9, a - .05);
  pop(third, a0, { s: .3, d: .35 }); glowC('#rcs0', a0, '255,209,0'); pulse('#rcs0', a0, 1.04); sfx(a0, 'success');
  const b0 = Math.max(a0 + .8, b - .05);
  pop(fresh, b0, { s: .3, d: .35 }); glowC('#rcs2', b0, '94,200,255'); pulse('#rcs2', b0, 1.04); sfx(b0, 'blip', { f: 1.3 });
  pop('#k3', b0 + .3, { s: .8 }); sfx(b0 + .3, 'pop');
}

// ================================================================ 4. связки
{
  const s = SC[3].start, a = mk(3, 'a', .7), b = mk(3, 'b', 2.4), c = mk(3, 'c', 3.9);
  hdr(3, '#h4');
  let prev = s + .15;
  [['#c4a', a, '255,209,0', 'success'], ['#c4b', b, '94,200,255', 'sparkle'], ['#c4c', c, '232,51,42', 'bonk']].forEach(([id, m, rgb, snd], k) => {
    const t = Math.max(prev + .5, m - .15); prev = t;
    hide(id);
    pop(id, t, { x: k % 2 ? 160 : -160, s: .9, d: .45, ease: 'back.out(1.5)' }); sfx(t, 'pop', { f: 1 + k * .15 });
    tl.fromTo(KV[k], { v: 0 }, { v: COMBOS[k], duration: .7, ease: 'power3.out', immediateRender: false }, t + .1);
    ticks(t + .1, .6, 6, 1.1, 1.6);
    glowC(id, t + .8, rgb); sfx(t + .8, snd);
    if (k === 2) shake(id, t + .8);
  });
}

// ================================================================ 5. нюанс
{
  const s = SC[4].start, a = mk(4, 'a', .9), b = mk(4, 'b', 3.2);
  hdr(4, '#h5');
  pop('#n5', s + .2, { s: 1.6, o: 0, d: .5, ease: 'back.out(2.4)' }); shake('#s5', s + .3); sfx(s + .25, 'impact', { g: .6 });
  tl.fromTo(P, { pct: 0 }, { pct: 70, duration: .6, ease: 'power3.out', immediateRender: false }, s + .2);
  hide('#f5a'); hide('#f5b'); hide('#st5');
  const a0 = Math.max(s + .7, a - .1);
  pop('#f5a', a0, { x: -140, s: .9, d: .45 }); sfx(a0, 'pop');
  const b0 = Math.max(a0 + .9, b - .1);
  pop('#f5b', b0, { x: 140, s: .9, d: .45 }); sfx(b0, 'pop', { f: 1.2 });
  pop('#st5', b0 + .3, { s: .3, d: .5, ease: 'back.out(2.2)' }); sfx(b0 + .3, 'blip');
}

// ================================================================ 6. вопрос + QR, в конце — перелёт к первому кадру (петля)
{
  const s = SC[5].start, a = mk(5, 'a', 1.8);
  pop('#h6', s + .02, { s: .7 }); sfx(s + .02, 'thump', { g: .8 });
  pop('#qr', s + .15, { s: .75, d: .55 }); sfx(s + .15, 'pop', { f: .9 });
  tl.fromTo('#qrsvg .qm', { opacity: 0, scale: .2, transformOrigin: '50% 50%' },
    { opacity: 1, scale: 1, duration: .3, ease: 'back.out(2)', stagger: { each: 0, from: 'center', amount: .5 } }, s + .25);
  tl.fromTo('#qrsvg .qf', { opacity: 0 }, { opacity: 1, duration: .25 }, s + .3);
  ticks(s + .25, .5, 6, 1.2, 1.9);
  pop('#qrlogo', s + .65, { s: .2, d: .5, ease: 'back.out(2.5)' }); sfx(s + .65, 'pop', { f: 1.3 });
  pop('#p6', s + .8, { s: .6 }); sfx(s + .8, 'blip', { f: 1.2 });
  fadeUp('#f6', s + 1.0);
  pulse('#p6', Math.max(s + 1.2, a), 1.12); sfx(Math.max(s + 1.2, a), 'ding', { f: 1.2 });
  const L0 = DUR - LOOP;
  tl.fromTo(P, { cam: 5 * H }, { cam: 0, duration: LOOP, ease: 'power3.in', immediateRender: false }, L0);
  tl.fromTo(P, { mb: 0 }, { mb: 60, duration: LOOP * .8, ease: 'power2.in', immediateRender: false }, L0);
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
  // числа на графиках
  CLASSES.forEach((c, k) => ($('clsv' + k).innerHTML = `${Math.round(CV[k].v)}<small>${(CV[k].v / c[1] * c[2]).toFixed(1).replace('.', ',')}%</small>`));
  RACES.forEach((r, k) => ($('rcsv' + k).innerHTML = `${Math.round(RV[k].v)}<small>${(RV[k].v / r[1] * r[2]).toFixed(1).replace('.', ',')}%</small>`));
  ['v4a', 'v4b', 'v4c'].forEach((id, k) => ($(id).textContent = Math.round(KV[k].v)));
  const pc = Math.round(P.pct) + '%'; if ($('n5').textContent !== pc) { $('n5').textContent = pc; $('n5').dataset.text = pc; }
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
