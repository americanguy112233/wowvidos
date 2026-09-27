"""Диагностика edge-tts: какие голоса доступны и что именно не работает.
   python edge_test.py
"""
import asyncio, os, sys
try:
    import edge_tts
except ImportError:
    sys.exit('edge-tts не установлен: .\\.venv\\scripts\\python.exe -m pip install edge-tts')

HERE = os.path.dirname(os.path.abspath(__file__))
env = os.path.join(HERE, '.env')
if os.path.exists(env):
    print('--- .env ---')
    for line in open(env, encoding='utf-8', errors='replace'):
        if line.strip().startswith('EDGE_'): print('  ', line.strip())

async def voices():
    try:
        vs = await edge_tts.list_voices()
        ru = [v['ShortName'] for v in vs if v['ShortName'].startswith('ru-')]
        print(f'Список голосов получен: всего {len(vs)}, русских: {ru}')
        return True
    except Exception as e:
        print('НЕ удалось получить список голосов:', type(e).__name__, e)
        return False

async def say(voice, text, **kw):
    audio = 0
    c = edge_tts.Communicate(text, voice, **kw)
    async for ch in c.stream():
        if ch['type'] == 'audio': audio += len(ch['data'])
    return audio

TESTS = [
    ('en-US-AriaNeural', 'Hello, this is a test.', {}),
    ('ru-RU-DmitryNeural', 'Привет, это проверка.', {}),
    ('ru-RU-SvetlanaNeural', 'Привет, это проверка.', {}),
    ('ru-RU-DmitryNeural', 'Привет, это проверка.', {'rate': '+10%', 'pitch': '+0Hz'}),
    ('ru-RU-DmitryNeural', 'Близзард начали выкидывать игроков из беты вов Форевер — за ники.', {'rate': '+10%'}),
]

async def main():
    print('edge-tts версия:', getattr(edge_tts, '__version__', '?'))
    await voices()
    for v, t, kw in TESTS:
        try:
            n = await say(v, t, **kw)
            print(f'OK    {v:22} {kw}  звук {n // 1024} КБ')
        except Exception as e:
            print(f'FAIL  {v:22} {kw}  {type(e).__name__}: {e}')

asyncio.run(main())
