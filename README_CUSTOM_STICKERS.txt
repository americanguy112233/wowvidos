# Custom stickers for Opus-5.5-

В комплекте 6 PNG-стикеров и `custom_stickers.js`.

Соответствие существующим слотам проекта:

- u24 → sticker_01_happy_orc.png
- u09 → sticker_02_love_elf.png
- u16 → sticker_03_laughing_dwarf.png
- u17 → sticker_04_undead_drink.png
- u13 → sticker_05_winking_orc.png
- u29 → sticker_06_surprised_paladin.png

`custom_stickers.js` подключается перед оригинальным `scene.js`, поэтому существующую
анимацию сцен менять не нужно: GSAP продолжит анимировать контейнеры, а вместо Lottie
будут показываться локальные PNG.

Для установки вручную:

1. Скопируй папку `assets/my-stickers` в корень проекта.
2. Скопируй `custom_stickers.js` в корень проекта.
3. В `index.html` сразу после строки с `lottie_svg.min.js` добавь:
   `<script src="custom_stickers.js"></script>`
4. После этого оставь `<script src="scene.js"></script>` как есть.

Telegram/prepare_assets для этих стикеров больше не нужен.
