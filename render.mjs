// Покадровый рендер index.html через системный Chrome.
//   node render.mjs --out <dir> [--fps 60] [--workers 4]      → кадры f_00000.jpg … + sfx.json
//   node render.mjs --out <dir> --stills 1.2,5.5,...          → отдельные PNG для проверки
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => (v.startsWith('--') && a.push([v.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]), a), []));
const OUT = path.resolve(args.out || path.join(ROOT, 'frames'));
const FPS = +(args.fps || 60);
const WORKERS = +(args.workers || 4);
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
fs.mkdirSync(OUT, { recursive: true });

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.ttf': 'font/ttf', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const URL = `http://127.0.0.1:${server.address().port}/index.html?render=1`;

// у каждого потока свой браузер: на Windows Chrome не рисует фоновые вкладки, и скриншот в них висит вечно
const BROWSERS = [];
async function launch() {
  const b = await puppeteer.launch({
    executablePath: CHROME, headless: true, protocolTimeout: 600000,
    args: ['--hide-scrollbars', '--force-color-profile=srgb', '--font-render-hinting=none', '--disable-lcd-text',
      '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--disable-backgrounding-occluded-windows'],
  });
  BROWSERS.push(b);
  return b;
}
async function newPage() {
  const browser = await launch();
  const page = (await browser.pages())[0] || await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });   // WoW: 16:9 для YouTube
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto(URL, { waitUntil: 'load' });
  const ok = await Promise.race([page.evaluate(() => window.READY).then(() => true), new Promise(r => setTimeout(() => r(false), 90000))]);
  if (!ok) {
    const stage = await Promise.race([page.evaluate(() => window.STAGE), new Promise(r => setTimeout(() => r('страница не отвечает'), 5000))]);
    throw new Error(`Страница не загрузилась за 90 с, застряла на этапе: «${stage}». Пришли этот текст.`);
  }
  // картинки, которых нет на диске (в ролике вместо них пустая рамка) — сразу останавливаемся и называем файлы
  const miss = await page.evaluate(() => [...new Set([...document.images].filter(i => i.getAttribute('src') && !i.naturalWidth).map(i => decodeURI(new URL(i.src).pathname).slice(1)))]);
  if (miss.length) throw new Error('Нет картинок (положи файлы по этим путям в папке проекта):\n  ' + miss.join('\n  '));
  return page;
}
const withTimeout = (p, ms, what) => Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error(`${what}: нет ответа ${ms / 1000} с`)), ms))]);
// после renderAt ждём, пока браузер реально перерисует страницу (2 кадра): иначе скриншот может вернуть старую картинку
const painted = page => page.evaluate(() => new Promise(r => { requestAnimationFrame(() => requestAnimationFrame(r)); setTimeout(r, 300); }));
const shot = (page, t, file, type = 'jpeg') => withTimeout(page.evaluate(t => window.renderAt(t), t)
  .then(() => painted(page))
  .then(() => page.screenshot({ path: file, type, ...(type === 'jpeg' ? { quality: 94 } : {}), optimizeForSpeed: true, captureBeyondViewport: false })), 60000, `кадр ${file}`);

const t0 = Date.now();
if (args.stills) {
  const page = await newPage();
  for (const t of args.stills.split(',').map(Number)) await shot(page, t, path.join(OUT, `still_${t.toFixed(2)}.png`), 'png');
  console.log('stills done', ((Date.now() - t0) / 1000).toFixed(1) + 's');
} else {
  const first = await newPage();
  const dur = await first.evaluate(() => window.DUR);
  fs.writeFileSync(path.join(OUT, 'sfx.json'), JSON.stringify(await first.evaluate(() => window.SFX), null, 1));
  fs.writeFileSync(path.join(OUT, 'timeline.json'), JSON.stringify(await first.evaluate(() => window.TIMELINE)));
  const N = Math.round(dur * FPS);
  const fname = i => path.join(OUT, `f_${String(i).padStart(5, '0')}.jpg`);
  // подпись рендера: если с прошлого раза поменялись вёрстка/анимация/озвучка — старые кадры не годятся
  const sig = ['index.html', 'scene.js', 'assets/timeline.js'].map(f => { try { return fs.readFileSync(path.join(ROOT, f), 'utf8'); } catch { return ''; } }).join('|') + `|${FPS}|${N}`;
  const sigHash = (await import('node:crypto')).createHash('sha1').update(sig).digest('hex');
  const sigFile = path.join(OUT, 'frames.sig');
  try { fs.unlinkSync(path.join(OUT, 'frames.ok')); } catch {}
  const oldSig = fs.existsSync(sigFile) ? fs.readFileSync(sigFile, 'utf8') : '';
  if ('resume' in args && oldSig !== sigHash) {
    console.log('проект изменился с прошлого рендера — рисую все кадры заново');
    for (const f of fs.readdirSync(OUT)) if (/^f_\d+\.jpg$/.test(f)) fs.unlinkSync(path.join(OUT, f));
  }
  fs.writeFileSync(sigFile, sigHash);
  // лишние кадры от прошлого, более длинного ролика
  for (const f of fs.readdirSync(OUT)) { const m = /^f_(\d+)\.jpg$/.exec(f); if (m && +m[1] >= N) fs.unlinkSync(path.join(OUT, f)); }
  // кадр годен, если это целый JPEG (начало FFD8, конец FFD9): обрезанный файл ffmpeg молча пропустит
  const have = i => { try { const b = fs.readFileSync(fname(i)); return b.length > 1000 && b[0] === 0xFF && b[1] === 0xD8 && b[b.length - 2] === 0xFF && b[b.length - 1] === 0xD9; } catch { return false; } };
  // --resume: дорисовываем только недостающие кадры (после прерванного рендера)
  const todo = [...Array(N).keys()].filter(i => !('resume' in args) || !have(i));
  if ('resume' in args) console.log(`уже готово ${N - todo.length}/${N} кадров, осталось ${todo.length}`);
  const pages = [first, ...await Promise.all([...Array(Math.max(0, Math.min(WORKERS, todo.length) - 1))].map(newPage))];
  let done = 0;
  const chunk = Math.ceil(todo.length / pages.length);
  await Promise.all(pages.map(async (page, w) => {
    for (const i of todo.slice(w * chunk, (w + 1) * chunk)) {
      await shot(page, i / FPS, fname(i));
      if (++done % 60 === 0) console.log(`${done}/${todo.length} кадров, ${((Date.now() - t0) / 1000).toFixed(0)} с`);
    }
  }));
  // проверка: ffmpeg молча обрезает видео на первом пропущенном кадре — дорисовываем пропуски
  let miss = [...Array(N).keys()].filter(i => !have(i));
  if (miss.length) {
    console.log(`пропущено ${miss.length} кадров — дорисовываю`);
    for (const i of miss) await shot(first, i / FPS, fname(i));
    miss = [...Array(N).keys()].filter(i => !have(i));
  }
  if (miss.length) { console.error(`НЕ ХВАТАЕТ ${miss.length} кадров (первый: ${miss[0]})`); process.exit(1); }
  // «замёрзшая» картинка: в ролике всё время что-то чуть движется, поэтому соседние кадры никогда не совпадают.
  // Подряд одинаковые кадры = браузер перестал рисовать (видео «обрывается» и стоит на одном кадре) — перерисовываем свежим браузером.
  const crypto = await import('node:crypto');
  // Совпадение 1–2 соседних кадров бывает честным (переход «мазок помадой» на миг закрывает весь экран сплошным красным),
  // поэтому «замёрзшим» считаем только повтор дольше 0.4 с.
  const MINRUN = Math.max(3, Math.round(FPS * .4));
  const frozen = () => { const out = []; let prev = '', run = [];
    const flush = () => { if (run.length >= MINRUN) out.push(...run); run = []; };
    for (let i = 0; i < N; i++) { const h = crypto.createHash('md5').update(fs.readFileSync(fname(i))).digest('hex');
      if (h === prev) run.push(i); else flush(); prev = h; }
    flush(); return out; };
  for (let pass = 1; pass <= 3; pass++) {
    const fr = frozen(); if (!fr.length) break;
    console.log(`картинка «замёрзла» на ${fr.length} кадрах (первый: ${fr[0]}, это ${(fr[0] / FPS).toFixed(2)} с) — перерисовываю, попытка ${pass}`);
    const fresh = await newPage();
    for (const i of [...new Set(fr.flatMap(i => [i - 1, i]))].filter(i => i >= 0)) await shot(fresh, i / FPS, fname(i));
    if (pass === 3 && frozen().length) console.log(`ВНИМАНИЕ: картинка стоит на месте с ${(frozen()[0] / FPS).toFixed(2)} с — проверь это место в готовом ролике. Сборка продолжается.`);
  }
  fs.writeFileSync(path.join(OUT, 'frames.ok'), String(N));
  console.log(`готово: ${N} кадров за ${((Date.now() - t0) / 1000).toFixed(1)}s`);
}
await Promise.all(BROWSERS.map(b => b.close()));
server.close();
