# Полная сборка на Windows: голос -> кадры -> звук -> mp4
#   powershell -ExecutionPolicy Bypass -File .\build.ps1
#   параметры: -Engine silero|edge|piper|rec|elevenlabs   -Out имя.mp4   -Music 0|1
#   -Resume — не пересобирать голос, дорисовать только недостающие кадры и продолжить
param([string]$Engine = 'silero', [string]$Out = 'wow-anna.mp4', [string]$Music = '0', [switch]$Resume)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$PY = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $PY)) { $PY = 'python' }

if (-not $env:CHROME) {
  $cands = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
             "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
             "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
             "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
             "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe")
  $env:CHROME = $cands | Where-Object { Test-Path $_ } | Select-Object -First 1
  if (-not $env:CHROME) { throw 'Не нашёл Chrome/Edge. Укажи путь: $env:CHROME = "C:\...\chrome.exe"' }
}
Write-Host "Браузер: $env:CHROME"
New-Item -ItemType Directory -Force build | Out-Null

# WoW (ветка wow-anna): ролик 16:9, 30 к/с. Геймплей владельца: assets\video\src\<имя>.mp4, имя берётся из index.html (data-video)
$vids = [regex]::Matches((Get-Content index.html -Raw -Encoding UTF8), 'data-video="([^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
foreach ($v in $vids) {
  if (-not (Test-Path "assets\video\src\$v.mp4") -and -not (Test-Path "assets\video\$v\f_0001.jpg")) { throw "Положи видео для этого ролика в assets\video\src\$v.mp4" }
}
# 0. клипы владельца: assets\video\src\<имя>.mp4 -> кадры assets\video\<имя>\f_0001.jpg (30 к/с) + <имя>.wav
Get-ChildItem assets\video\src\*.mp4 -ErrorAction SilentlyContinue | ForEach-Object {
  $n = ($_.BaseName -replace '\s+', '_').ToLower()
  $dir = "assets\video\$n"
  # сколько кадров должно быть: длина видео × 30 (если нарезка прервалась, кадров меньше — режем заново)
  $len = [double](ffprobe -v error -show_entries format=duration -of csv=p=0 $_.FullName)
  $need = [math]::Floor($len * 30) - 5
  $have = @(Get-ChildItem "$dir\f_*.jpg" -ErrorAction SilentlyContinue).Count
  if ($have -lt $need -or -not (Test-Path "$dir\f_0001.jpg") -or ($_.LastWriteTime -gt (Get-Item "$dir\f_0001.jpg").LastWriteTime)) {
    Write-Host "клип: $($_.Name) -> $dir"
    New-Item -ItemType Directory -Force $dir | Out-Null
    Remove-Item "$dir\f_*.jpg" -ErrorAction SilentlyContinue
    ffmpeg -v error -y -i $_.FullName -vf "fps=30,scale='min(iw,1280)':-2" -q:v 3 -start_number 1 "$dir\f_%04d.jpg"
    ffmpeg -v error -y -i $_.FullName -vn -ac 1 -ar 48000 "assets\video\$n.wav"
    if ($LASTEXITCODE) { throw "Не нарезался клип $($_.Name)" }
    $have = @(Get-ChildItem "$dir\f_*.jpg").Count
    if ($have -lt $need) { throw "Клип $($_.Name) нарезался не полностью: $have кадров из $need. Проверь место на диске и запусти ещё раз." }
    Write-Host "  готово: $have кадров"
  }
}

$voiceFresh = (Test-Path build\voice.wav) -and ((Get-Item build\voice.wav).LastWriteTime -gt (Get-Item voice.py).LastWriteTime)
if ($Resume -and $voiceFresh -and (Test-Path build\frames\timeline.json)) {
  Write-Host '1/4 голос уже готов — пропускаю (-Resume)'
  Write-Host '2/4 кадры: дорисовываю недостающие...'
  node render.mjs --out build\frames --fps 30 --workers 4 --resume
  if ($LASTEXITCODE) { throw 'Рендер кадров упал' }
} else {
Write-Host '1/4 голос...'
& $PY voice.py build\vo build\voice.wav --engine $Engine
if ($LASTEXITCODE) { throw 'Озвучка не собралась — смотри ошибку выше' }

Write-Host '2/4 кадры...'
if (Test-Path build\frames) { Remove-Item build\frames -Recurse -Force }
node render.mjs --out build\frames --fps 30 --workers 4
if ($LASTEXITCODE) { throw 'Рендер кадров упал' }
}
# все ли кадры на месте: иначе ffmpeg молча обрежет видео
$need = [int](Get-Content build\frames\frames.ok -ErrorAction SilentlyContinue)
$have = (Get-ChildItem build\frames\f_*.jpg).Count
if (-not $need -or $have -lt $need) { throw "Кадров $have из $need — запусти сборку ещё раз с -Resume" }

Write-Host '3/4 звук...'
$env:MUSIC = $Music
& $PY audio.py build\frames\sfx.json build\mix.wav build\voice.wav
if ($LASTEXITCODE) { throw 'Сведение звука упало' }

Write-Host '4/4 видео...'
$DUR = node -p "require('./build/frames/timeline.json').dur"
ffmpeg -v error -y -framerate 30 -start_number 0 -i build\frames\f_%05d.jpg -i build\mix.wav -t $DUR `
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -profile:v high `
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart $Out
if ($LASTEXITCODE) { throw 'ffmpeg упал' }
# проверка длины готового ролика
# считаем именно кадры видео (длина файла считается по звуку и не замечает, что картинка кончилась раньше)
$vf = [int](ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 $Out)
$want = [int]([math]::Floor([double]$DUR * 30))
if ($vf + 6 -lt $want) { throw "В видео $vf кадров вместо $want — картинка обрывается на $([math]::Round($vf / 30, 2)) с. Пришли этот текст." }
Write-Host "Готово: $Out ($DUR с)"
