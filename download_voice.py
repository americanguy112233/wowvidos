"""Скачивает русский голос Piper (ruslan, medium) в папку voices/ рядом с этим скриптом.
   python download_voice.py
"""
import os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DST = os.path.join(HERE, 'voices')
BASE = 'https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/ruslan/medium/'
NAME = 'ru_RU-ruslan-medium'
os.makedirs(DST, exist_ok=True)
for ext in ('.onnx.json', '.onnx'):
    path = os.path.join(DST, NAME + ext)
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print('уже есть:', path); continue
    print('качаю', NAME + ext, '...')
    tmp = path + '.part'
    urllib.request.urlretrieve(BASE + NAME + ext, tmp)
    os.replace(tmp, path)
    print('готово:', path, f'{os.path.getsize(path) / 1e6:.1f} МБ')
print('Голос на месте. Теперь: .\\.venv\\scripts\\python.exe voice.py build\\vo build\\voice.wav --engine piper')
