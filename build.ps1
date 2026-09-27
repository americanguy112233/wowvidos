# Полная сборка на Windows: голос -> кадры -> звук -> mp4
#   powershell -ExecutionPolicy Bypass -File .\build.ps1
#   параметры: -Engine edge|piper|rec|elevenlabs   -Out имя.mp4   -Music 0|1
param([string]$Engine = 'edge', [string]$Out = 'wow-forever-ban.mp4', [string]$Music = '0')
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

Write-Host '1/4 голос...'
& $PY voice.py build\vo build\voice.wav --engine $Engine
if ($LASTEXITCODE) { throw 'Озвучка не собралась — смотри ошибку выше' }

Write-Host '2/4 кадры...'
if (Test-Path build\frames) { Remove-Item build\frames -Recurse -Force }
node render.mjs --out build\frames --fps 60 --workers 4
if ($LASTEXITCODE) { throw 'Рендер кадров упал' }

Write-Host '3/4 звук...'
$env:MUSIC = $Music
& $PY audio.py build\frames\sfx.json build\mix.wav build\voice.wav
if ($LASTEXITCODE) { throw 'Сведение звука упало' }

Write-Host '4/4 видео...'
$DUR = node -p "require('./build/frames/timeline.json').dur"
ffmpeg -v error -y -framerate 60 -i build\frames\f_%05d.jpg -i build\mix.wav -t $DUR `
  -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -profile:v high `
  -c:a aac -b:a 256k -ar 48000 -movflags +faststart $Out
if ($LASTEXITCODE) { throw 'ffmpeg упал' }
Write-Host "Готово: $Out ($DUR с)"
