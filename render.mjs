// Покадровый рендер index.html через системный Chrome.
//   node render.mjs --out <dir> [--fps 60] [--workers 4]      → кадры f_00000.jpg … + sfx.json
//   node render.mjs --out <dir> --stills 1.2,5.5,...          → отдельные PNG для проверки
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => (v.startsWith('--') && a.push([v.slice(2), arr[i + 1]]), a), []));
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
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto(URL, { waitUntil: 'load' });
  const ok = await Promise.race([page.evaluate(() => window.READY).then(() => true), new Promise(r => setTimeout(() => r(false), 90000))]);
  if (!ok) {
    const stage = await Promise.race([page.evaluate(() => window.STAGE), new Promise(r => setTimeout(() => r('страница не отвечает'), 5000))]);
    throw new Error(`Страница не загрузилась за 90 с, застряла на этапе: «${stage}». Пришли этот текст.`);
  }
  return page;
}
const withTimeout = (p, ms, what) => Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error(`${what}: нет ответа ${ms / 1000} с`)), ms))]);
const shot = (page, t, file, type = 'jpeg') => withTimeout(page.evaluate(t => window.renderAt(t), t)
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
  const pages = [first, ...await Promise.all([...Array(WORKERS - 1)].map(newPage))];
  let done = 0;
  const chunk = Math.ceil(N / WORKERS);
  await Promise.all(pages.map(async (page, w) => {
    for (let i = w * chunk; i < Math.min(N, (w + 1) * chunk); i++) {
      await shot(page, i / FPS, path.join(OUT, `f_${String(i).padStart(5, '0')}.jpg`));
      if (++done % 60 === 0) console.log(`${done}/${N} кадров, ${((Date.now() - t0) / 1000).toFixed(0)} с`);
    }
  }));
  console.log(`rendered ${N} frames in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
}
await Promise.all(BROWSERS.map(b => b.close()));
server.close();
