$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "=== PNG stickers installer ===" -ForegroundColor Cyan

if (-not (Test-Path ".\scene.js")) {
    throw "scene.js не найден. Запусти этот скрипт из корня Opus-5.5-."
}
if (-not (Test-Path ".\assets\my-stickers\sticker_01_happy_orc.png")) {
    throw "Не найдены PNG. Распакуй архив со стикерами так, чтобы существовала assets\my-stickers\."
}

# Backups
Copy-Item ".\scene.js" ".\scene-before-png-stickers.js" -Force
if (Test-Path ".\index.html") {
    Copy-Item ".\index.html" ".\index-before-png-stickers.html" -Force
}

# Remove our previous custom loader if it was added to index.html.
$html = Get-Content ".\index.html" -Raw
$html = $html -replace '(?m)^\s*<script src="custom_stickers\.js"></script>\s*\r?\n?', ''
Set-Content ".\index.html" $html -Encoding UTF8

# Replace only the Lottie sticker-loading section in scene.js.
$scene = Get-Content ".\scene.js" -Raw

$startMarker = '// ---------------------------------------------------------------- Lottie-утки'
$endMarker   = '// ---------------------------------------------------------------- кадр'

$start = $scene.IndexOf($startMarker)
$end = $scene.IndexOf($endMarker)

if ($start -lt 0 -or $end -lt 0 -or $end -le $start) {
    throw "Не удалось найти блок загрузки стикеров в scene.js. Файл, возможно, уже изменён."
}

$newBlock = @'
// ---------------------------------------------------------------- PNG-стикеры
const ANIMS = [];

const STICKERS = {
  u24: 'sticker_01_happy_orc.png',
  u09: 'sticker_02_love_elf.png',
  u16: 'sticker_03_laughing_dwarf.png',
  u17: 'sticker_04_undead_drink.png',
  u13: 'sticker_05_winking_orc.png',
  u29: 'sticker_06_surprised_paladin.png'
};

async function loadStickers() {
  const els = [...document.querySelectorAll('[data-anim]')];

  for (const el of els) {
    const file = STICKERS[el.dataset.anim];
    if (!file) continue;

    el.innerHTML = '';
    el.style.overflow = 'visible';

    const img = document.createElement('img');
    img.src = `assets/my-stickers/${file}`;
    img.alt = '';
    img.draggable = false;
    img.style.display = 'block';
    img.style.width = '100%';
    img.style.height = '100%';
    img.style.objectFit = 'contain';
    img.style.pointerEvents = 'none';
    img.style.userSelect = 'none';

    el.appendChild(img);

    const sec = [...document.querySelectorAll('.sec')].indexOf(el.closest('.sec'));
    ANIMS.push({
      anim: {
        totalFrames: 1,
        goToAndStop() {}
      },
      sec,
      t0: SC[sec].start,
      n: 1
    });
  }

  // Wait until all local PNG files are decoded before rendering frames.
  await Promise.all([...document.images].map(img => {
    if (img.complete) return Promise.resolve();
    return new Promise(resolve => {
      img.addEventListener('load', resolve, { once: true });
      img.addEventListener('error', resolve, { once: true });
    });
  }));
}
'@

$scene = $scene.Substring(0, $start) + $newBlock + "`r`n" + $scene.Substring($end)
Set-Content ".\scene.js" $scene -Encoding UTF8

Write-Host ""
Write-Host "Готово." -ForegroundColor Green
Write-Host "PNG-стикеры теперь подключаются прямо из scene.js."
Write-Host "custom_stickers.js больше не нужен."
Write-Host ""
Write-Host "Запусти проверку:"
Write-Host '  node render.mjs --out build/frames --fps 60 --workers 2 --stills 2,7,13,17,22,26'
Write-Host ""
Write-Host "Если понадобится вернуть оригинал:"
Write-Host '  Copy-Item .\scene-before-png-stickers.js .\scene.js -Force'
Write-Host '  Copy-Item .\index-before-png-stickers.html .\index.html -Force'
