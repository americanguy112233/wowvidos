"""Свои стикеры → assets/stickers/
   python import_stickers.py <папка_со_стикерами>

.tgs (анимированные стикеры Telegram) → распаковываются в Lottie .json
.json (Lottie)                         → копируются как есть
.png / .webp / .jpg                    → копируются как есть (статичные)
.webm (видеостикеры)                   → не поддерживаются, пропускаются
"""
import gzip, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'my_stickers')
dst = os.path.join(HERE, 'assets', 'stickers')
os.makedirs(dst, exist_ok=True)
for f in sorted(os.listdir(src)):
    name, ext = os.path.splitext(f); ext = ext.lower(); p = os.path.join(src, f)
    if ext == '.tgs':
        open(os.path.join(dst, name + '.json'), 'wb').write(gzip.decompress(open(p, 'rb').read()))
        print(f'{f:30} → data-anim="{name}"')
    elif ext == '.json':
        shutil.copy(p, dst); print(f'{f:30} → data-anim="{name}"')
    elif ext in ('.png', '.webp', '.jpg', '.jpeg'):
        shutil.copy(p, dst); print(f'{f:30} → data-anim="{f}"')
    elif ext == '.webm':
        print(f'{f:30} пропущен: видеостикеры не поддерживаются')
