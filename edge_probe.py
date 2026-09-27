"""Какие варианты фразы сервер Microsoft озвучивает, а какие нет.
   python edge_probe.py
Каждый вариант пробуется 2 раза с паузой; результат — OK или FAIL.
"""
import asyncio, time
import edge_tts

VOICE = 'ru-RU-DmitryNeural'
PHRASES = [
    'Привет, это проверка.',
    'Больше половины дворфов — шаманы.',
    'Больше половины дворфов, шаманы.',
    'Больше половины дворфов стали шаманами.',
    'Больше половины дворфов',
    'дворфы шаманы',
    'Половина дворфов выбрала шамана.',
    'А дворфов-разбойников всего 22.',
    'А дворфов разбойников всего двадцать два.',
]

async def say(text):
    n = 0
    async for ch in edge_tts.Communicate(text, VOICE).stream():
        if ch['type'] == 'audio': n += len(ch['data'])
    return n

for p in PHRASES:
    res = 'FAIL'
    for attempt in range(2):
        try:
            if asyncio.run(say(p)): res = 'OK'; break
        except Exception:
            pass
        time.sleep(3)
    print(f'{res:5} {p}')
    time.sleep(1.5)
