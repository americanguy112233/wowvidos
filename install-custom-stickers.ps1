$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (-not (Test-Path ".\index.html")) {
    throw "index.html не найден. Положи этот файл в корень проекта Opus-5.5-."
}

Copy-Item ".\index.html" ".\index-before-custom-stickers.html" -Force

$html = Get-Content ".\index.html" -Raw
if ($html -notmatch 'custom_stickers\.js') {
    $html = $html -replace '(<script src="node_modules/lottie-web/build/player/lottie_svg\.min\.js"></script>)', '$1`r`n<script src="custom_stickers.js"></script>'
    Set-Content ".\index.html" $html -Encoding UTF8
}

New-Item -ItemType Directory -Force ".\assets\my-stickers" | Out-Null
Copy-Item ".\assets\my-stickers\*" ".\assets\my-stickers\" -Force

Write-Host ""
Write-Host "Готово. Свои стикеры подключены."
Write-Host "Проверь: Get-ChildItem .\assets\my-stickers"
Write-Host ""
Write-Host "Соответствие:"
Write-Host "u24 -> happy orc"
Write-Host "u09 -> love elf"
Write-Host "u16 -> laughing dwarf"
Write-Host "u17 -> undead drink"
Write-Host "u13 -> winking orc"
Write-Host "u29 -> surprised paladin"
