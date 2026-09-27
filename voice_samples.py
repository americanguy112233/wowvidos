"""Образцы голосов Silero: одна и та же фраза всеми голосами → папка voice_samples/, потом она открывается.
   python voice_samples.py
Послушай файлы и впиши понравившийся голос в .env:  SILERO_SPEAKER=имя
"""
import os, subprocess, sys
import numpy as np
from scipy.io import wavfile
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'voice_samples')
os.makedirs(OUT, exist_ok=True)
TEXT = ('Представь: заходишь в бэту Форевер, а там девять тысяч персонажей! '
        'Кем играет весь Альянс? Сейчас покажу.')

model, ver = None, None
for v in ('v5_ru', 'v4_ru'):
    try:
        model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts', language='ru', speaker=v, trust_repo=True)
        ver = v; break
    except Exception as e:
        print(f'{v}: не загрузилась ({e})')
if model is None: sys.exit('Не удалось загрузить Silero')

speakers = [s for s in getattr(model, 'speakers', ['aidar', 'baya', 'kseniya', 'xenia', 'eugene']) if s != 'random']
print(f'модель {ver}, голоса: {", ".join(speakers)}')
for sp in speakers:
    audio = model.apply_tts(text=TEXT, speaker=sp, sample_rate=48000, put_accent=True, put_yo=True)
    path = os.path.join(OUT, f'{sp}.wav')
    wavfile.write(path, 48000, (np.clip(audio.numpy(), -1, 1) * 32767).astype(np.int16))
    print('  готово:', path)
if os.name == 'nt': os.startfile(OUT)
print('Слушай файлы в папке voice_samples и впиши выбранный голос в .env: SILERO_SPEAKER=имя')
