// Custom PNG/WebP sticker pack for Opus 5.5.
// Loaded BEFORE scene.js. It keeps the original animation API alive,
// but renders local PNG stickers instead of downloading Telegram Lottie files.
(() => {
  const MAP = {
    u24: 'sticker_01_happy_orc.png',
    u09: 'sticker_02_love_elf.png',
    u16: 'sticker_03_laughing_dwarf.png',
    u17: 'sticker_04_undead_drink.png',
    u13: 'sticker_05_winking_orc.png',
    u29: 'sticker_06_surprised_paladin.png'
  };

  // Prevent the old scene.js from failing when it tries to read uXX.json.
  const nativeFetch = window.fetch.bind(window);
  window.fetch = async (input, init) => {
    const url = typeof input === 'string' ? input : input?.url || '';
    if (/assets\/stickers\/u\d+\.json(?:\?|$)/.test(url)) {
      return new Response('{}', {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    return nativeFetch(input, init);
  };

  // Fake the tiny part of the Lottie API used by scene.js.
  const originalLoad = window.lottie?.loadAnimation;
  if (window.lottie) {
    window.lottie.loadAnimation = (opts) => {
      const el = opts.container;
      const name = el?.dataset?.anim;
      const file = MAP[name];

      if (el && file) {
        el.innerHTML = '';
        el.style.overflow = 'visible';

        const img = document.createElement('img');
        img.src = `assets/my-stickers/${file}`;
        img.alt = '';
        img.draggable = false;
        img.style.cssText = [
          'display:block',
          'width:100%',
          'height:100%',
          'object-fit:contain',
          'pointer-events:none',
          'user-select:none'
        ].join(';');
        el.appendChild(img);
      }

      return {
        isLoaded: true,
        totalFrames: 1,
        addEventListener() {},
        goToAndStop() {}
      };
    };
  }
})();
