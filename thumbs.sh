#!/bin/zsh
# Обложки: 16:9 и 9:16 для рилса
#   ./thumbs.sh ["Ролик.mp4"]
set -e
cd "$(dirname "$0")"
VIDEO="${1:-WoW Forever — бан за ник.mp4}"
[ -f assets/stickers/sticker_06_surprised_paladin.png ] || { echo "Нет стикеров в assets/stickers"; exit 1; }
[ -f "$VIDEO" ] || { echo "Нет ролика «$VIDEO» — сначала ./build.sh"; exit 1; }
node thumb.mjs . "YouTube 16x9"
node thumb.mjs . "вертикальное"
echo "готово: Превью — *.png / *.jpg"
