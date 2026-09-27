"""Закадровый голос → voice.wav + assets/timeline.js (тайминг сцен под длину реплик).
   python voice.py <workdir> <out.wav> [--engine auto|edge|piper|elevenlabs|rec|say]

edge-tts (бесплатно, без ключа, нейроголоса Microsoft): pip install edge-tts
  EDGE_VOICE — голос: ru-RU-DmitryNeural (муж., по умолчанию) или ru-RU-SvetlanaNeural (жен.)
  EDGE_RATE  — темп: +10% (по умолчанию), +0%, +20% …   EDGE_PITCH — высота: +0Hz, -5Hz …

Piper (бесплатно, офлайн, работает на Windows):
  pip install piper-tts, модель ru_RU-ruslan-medium.onnx (+ .onnx.json) положи в папку voices/
  или укажи путь в PIPER_MODEL (в .env). Скорость речи — PIPER_SPEED (1.0 обычная, 1.15 быстрее).

ElevenLabs: ключ берётся из ELEVENLABS_API_KEY (окружение или .env рядом со скриптом).
  ELEVENLABS_VOICE_ID — голос (по умолчанию ниже), ELEVENLABS_MODEL — модель.
Без ключа — черновой системный голос macOS (Milena), чтобы можно было собрать монтаж.

Метки |a| |b| … в тексте — моменты, к которым привязана анимация (время начала следующего слова).
Длительность сцены = max(минимум, вступление + реплика + хвост), округлено до 0.25 с.
"""
import argparse, base64, glob, hashlib, json, time, math, os, re, subprocess, sys, urllib.request
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))

# (минимальная длительность сцены, задержка голоса от начала сцены, текст)
CUES = [
    (3.5, 0.05, "Игрок за неделю бэты переписал |a|9150 персонажей. Смотрим, |b|кем играет Альянс."),
    (4.0, 0.12, "Топ-1 — |a|паладин, охотник отстал всего на 25. А |b|разбойник — последний."),
    (4.0, 0.12, "Люди — |a|почти треть Альянса. А новые |b|небеснорожденные лишь третьи."),
    (4.5, 0.12, "Лучшая связка — |a|человек-паладин, 1018. Больше половины дворфов — |b|шаманы. А дворфов-разбойников |c|всего 22."),
    (4.5, 0.12, "Но есть нюанс: |a|70% данных — у банка и аукциона в столицах. А |b|разбойников и друидов в скрытности не видно."),
    (3.5, 0.12, "А ты кем играешь? Пиши в комменты и |a|заглядывай в мой телеграм-бот."),
]
TAIL = float(os.environ.get('TAIL', '0.2'))            # воздух после реплики до смены сцены
STEP = 0.05
PAUSE_MAX = float(os.environ.get('PAUSE_MAX', '0.15'))  # паузы внутри фразы длиннее этого — укорачиваются

ap = argparse.ArgumentParser()
ap.add_argument('work'); ap.add_argument('out')
ap.add_argument('--engine', default='auto')
a = ap.parse_args()
os.makedirs(a.work, exist_ok=True)

def load_env():
    p = os.path.join(HERE, '.env')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
load_env()
KEY = os.environ.get('ELEVENLABS_API_KEY', '')
VOICE = os.environ.get('ELEVENLABS_VOICE_ID', 'pNInz6obpgDQGcFmaJgB')   # Adam (премейд, мультиязычный)
MODEL = os.environ.get('ELEVENLABS_MODEL', 'eleven_multilingual_v2')

def find_piper_model():
    p = os.environ.get('PIPER_MODEL', '')
    if p and not os.path.isabs(p): p = os.path.join(HERE, p)
    if p and os.path.exists(p): return p
    for pat in ('voices/*.onnx', '*.onnx', 'piper/*.onnx', 'voices/**/*.onnx'):
        found = sorted(glob.glob(os.path.join(HERE, pat), recursive=True))
        ru = [f for f in found if 'ru_RU' in os.path.basename(f)]
        if ru or found: return (ru or found)[0]
    return ''
PIPER_MODEL = find_piper_model()
PIPER_SPEED = float(os.environ.get('PIPER_SPEED', '1.1'))
EDGE_VOICE = os.environ.get('EDGE_VOICE', 'ru-RU-DmitryNeural')
EDGE_RATE = os.environ.get('EDGE_RATE', '+15%')
EDGE_PITCH = os.environ.get('EDGE_PITCH', '+0Hz')
def has_edge():
    try:
        import edge_tts  # noqa
        return True
    except ImportError:
        return False
if a.engine != 'auto': engine = a.engine
elif KEY: engine = 'elevenlabs'
elif has_edge(): engine = 'edge'
elif PIPER_MODEL: engine = 'piper'
elif sys.platform == 'darwin': engine = 'say'
else: raise SystemExit('Нет голоса: положи модель Piper (*.onnx) в папку voices/ или запусти с --engine rec')

def parse(text):
    """'…|a|слово…' → чистый текст и {метка: индекс символа}."""
    clean, marks, i = '', {}, 0
    for part in re.split(r'(\|\w+\|)', text):
        if re.fullmatch(r'\|\w+\|', part): marks[part.strip('|')] = len(clean)
        else: clean += part
    return clean, marks

def to_wav48(src, dst):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-ac', '1', '-ar', str(SR), dst], check=True)
    return wavfile.read(dst)[1].astype(np.float64) / 32768

def tts_eleven(i, text, prev, nxt):
    body = {'text': text, 'model_id': MODEL, 'previous_text': prev, 'next_text': nxt,
            'voice_settings': {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.35, 'use_speaker_boost': True, 'speed': 1.12}}
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128',
        data=json.dumps(body).encode(), headers={'xi-api-key': KEY, 'Content-Type': 'application/json'})
    r = json.load(urllib.request.urlopen(req, timeout=120))
    mp3 = os.path.join(a.work, f'cue{i}.mp3'); open(mp3, 'wb').write(base64.b64decode(r['audio_base64']))
    x = to_wav48(mp3, os.path.join(a.work, f'cue{i}.wav'))
    al = r['alignment']
    return x, (lambda idx: al['character_start_times_seconds'][min(idx, len(al['characters']) - 1)])

def tts_say(i, text, prev, nxt):
    p = os.path.join(a.work, f'cue{i}.aiff')
    subprocess.run(['say', '-v', 'Milena', '-o', p, text], check=True)
    x = to_wav48(p, os.path.join(a.work, f'cue{i}.wav'))
    return x, None

def tts_edge(i, text, prev, nxt):
    """edge-tts: mp3 + время начала каждого слова → метки анимации ставятся точно на слова."""
    try:
        import asyncio, edge_tts
    except ImportError:
        raise SystemExit('Нет edge-tts: .\\.venv\\scripts\\python.exe -m pip install edge-tts')
    global EDGE_VOICE
    # кэш: уже озвученная реплика с тем же текстом/голосом/темпом берётся с диска, без запроса к Microsoft
    cdir = os.path.join(HERE, 'voice_cache'); os.makedirs(cdir, exist_ok=True)
    key = hashlib.sha1(f'{text}|{EDGE_VOICE.lower()}|{EDGE_RATE}|{EDGE_PITCH}'.encode('utf-8')).hexdigest()[:16]
    cmp3, cjs = os.path.join(cdir, key + '.mp3'), os.path.join(cdir, key + '.json')
    if os.path.exists(cmp3) and os.path.exists(cjs) and os.path.getsize(cmp3) > 1000:
        print(f'  реплика {i + 1}: из кэша')
        words = [tuple(w) for w in json.load(open(cjs, encoding='utf-8'))]
        return edge_finish(i, text, open(cmp3, 'rb').read(), words)
    if i == 0 or not getattr(tts_edge, 'checked', False):   # имя голоса без учёта регистра: ru-ru-dmitryneural → ru-RU-DmitryNeural
        try:
            names = [x['ShortName'] for x in asyncio.run(edge_tts.list_voices())]
            fix = {n.lower(): n for n in names}
            if EDGE_VOICE.lower() in fix: EDGE_VOICE = fix[EDGE_VOICE.lower()]
            else: print(f'Голоса {EDGE_VOICE} нет. Русские: {[n for n in names if n.startswith("ru-")]}')
        except Exception as e:
            print('Не получил список голосов:', e)
        tts_edge.checked = True
    words = []
    def simple(s):   # запасной вариант текста: без тире и символов, которые иногда ломают синтез
        s = s.replace('—', ',').replace('–', ',').replace('%', ' процентов').replace('Топ-1', 'Топ один')
        return re.sub(r'\s+,', ',', s)
    async def run(kw, txt):
        try:
            c = edge_tts.Communicate(txt, EDGE_VOICE, boundary='WordBoundary', **kw)
        except TypeError:                      # старые версии edge-tts: слова приходят и так
            c = edge_tts.Communicate(txt, EDGE_VOICE, **kw)
        audio = bytearray()
        async for ch in c.stream():
            if ch['type'] == 'audio': audio += ch['data']
            elif ch['type'] == 'WordBoundary': words.append((ch['offset'] / 1e7, ch['text']))
        return bytes(audio)
    data, err = None, ''
    if getattr(tts_edge, 'asked', False): time.sleep(1.5)   # пауза между репликами — реже упираемся в лимит сервера
    tts_edge.asked = True
    plans = [dict(rate=EDGE_RATE, pitch=EDGE_PITCH), dict(rate=EDGE_RATE), {}, dict(rate=EDGE_RATE), {}, {}, dict(rate=EDGE_RATE), {}]
    waits = [0, 3, 6, 10, 15, 20, 30, 45]
    texts_try = [text, text, text, simple(text), simple(text), text, simple(text), simple(text)]
    for n, (kw, w, txt) in enumerate(zip(plans, waits, texts_try)):
        if w:
            print(f'  реплика {i + 1}: сервер не отдал звук, жду {w} с и пробую ещё раз ({n + 1}/{len(plans)})…')
            time.sleep(w)
        words.clear()
        try:
            data = asyncio.run(run(kw, txt))
            if data: break
        except Exception as e:
            err = f'{type(e).__name__}: {e}'
    if not data:
        raise SystemExit(f'edge-tts не вернул звук ({EDGE_VOICE}): {err}\n'
                         'Похоже, Microsoft временно ограничил запросы. Подожди 10–15 минут и запусти снова:\n'
                         'уже готовые реплики возьмутся из кэша (папка voice_cache) и повторно не запрашиваются.\n'
                         'Если не помогает и через час — запусти .\\.venv\\scripts\\python.exe edge_test.py и пришли вывод.')
    open(cmp3, 'wb').write(data); json.dump(words, open(cjs, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'  реплика {i + 1}: готово')
    return edge_finish(i, text, data, words)

def edge_finish(i, text, data, words):
    mp3 = os.path.join(a.work, f'cue{i}.mp3'); open(mp3, 'wb').write(data)
    x = to_wav48(mp3, os.path.join(a.work, f'cue{i}.wav'))
    # позиции слов в тексте → время метки = начало первого слова, стоящего на месте метки или после неё
    pos, spans = 0, []
    for t, w in words:
        k = text.find(w, pos)
        if k < 0: continue
        spans.append((k, t)); pos = k + len(w)
    def at(idx):
        for k, t in spans:
            if k >= idx: return t
        return spans[-1][1] if spans else None
    return x, (at if spans else None)

def tts_piper(i, text, prev, nxt):
    """Piper: текст подаётся через stdin в UTF-8 (иначе на Windows кириллица ломается)."""
    if not PIPER_MODEL:
        raise SystemExit('Не нашёл модель Piper: положи ru_RU-ruslan-medium.onnx и .onnx.json в папку voices/')
    out = os.path.join(a.work, f'cue{i}_piper.wav')
    env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
    ls = f'{1 / PIPER_SPEED:.3f}'
    tries = [[sys.executable, '-m', 'piper', '-m', PIPER_MODEL, '-f', out, '--length-scale', ls],
             [sys.executable, '-m', 'piper', '-m', PIPER_MODEL, '-f', out, '--length_scale', ls],
             [sys.executable, '-m', 'piper', '-m', PIPER_MODEL, '-f', out],
             ['piper', '-m', PIPER_MODEL, '-f', out]]
    err = ''
    for cmd in tries:
        try:
            r = subprocess.run(cmd, input=(text + '\n').encode('utf-8'), capture_output=True, env=env)
        except FileNotFoundError as e:
            err = str(e); continue
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 1000:
            return to_wav48(out, os.path.join(a.work, f'cue{i}.wav')), None
        err = r.stderr.decode('utf-8', 'replace')[-800:]
    raise SystemExit(f'Piper не сработал.\nМодель: {PIPER_MODEL}\nОшибка:\n{err}\nПроверь: python -m pip install piper-tts')

def tts_rec(i, text, prev, nxt):
    """Своя запись: recordings/cue1.wav … cue6.wav (подойдёт и .mp3/.m4a/.ogg)."""
    d = os.path.join(HERE, 'recordings')
    for ext in ('wav', 'mp3', 'm4a', 'ogg', 'flac'):
        p = os.path.join(d, f'cue{i + 1}.{ext}')
        if os.path.exists(p):
            return to_wav48(p, os.path.join(a.work, f'cue{i}.wav')), None
    raise SystemExit(f'Нет файла recordings/cue{i + 1}.wav — запиши реплику: «{text}»')

def squeeze(x, maxgap=None):
    """Укорачивает паузы внутри реплики до maxgap секунд. Возвращает звук и функцию старое время → новое."""
    maxgap = PAUSE_MAX if maxgap is None else maxgap
    win = int(.01 * SR)
    env = np.convolve(np.abs(x), np.ones(win) / win, 'same')
    quiet = env < 0.03 * env.max()
    keep = int(maxgap * SR)
    cuts, i, n = [], 0, len(x)          # (начало вырезанного куска, длина) в отсчётах
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            if j - i > keep and i > 0 and j < n:
                cuts.append((i + keep // 2, j - i - keep))
            i = j
        else:
            i += 1
    if not cuts: return x, (lambda t: t)
    parts, prev = [], 0
    for s, L in cuts:
        parts.append(x[prev:s]); prev = s + L
    y = np.concatenate(parts + [x[prev:]])
    def remap(t):
        k = int(t * SR); d = 0
        for s, L in cuts:
            if k >= s + L: d += L
            elif k > s: d += k - s
        return (k - d) / SR
    return y, remap

def trim(x):
    idx = np.where(np.abs(x) > 0.02 * np.max(np.abs(x)))[0]
    s = max(0, idx[0] - 240)
    return x[s: idx[-1] + 2400], s / SR

def process(x):
    x = sosfilt(butter(2, 70, 'high', fs=SR, output='sos'), x)
    env = np.sqrt(sosfilt(butter(1, 12, 'low', fs=SR, output='sos'), x ** 2) + 1e-9)
    thr = np.percentile(env, 80) * .8
    x = x * np.where(env > thr, (thr / env) ** 0.4, 1.0)      # мягкая компрессия
    return x / np.max(np.abs(x)) * .75

texts = [parse(t) for _, _, t in CUES]
clips, marks, words_all = [], [], []
for i, (clean, mk) in enumerate(texts):
    prev = texts[i - 1][0] if i else ''
    nxt = texts[i + 1][0] if i + 1 < len(texts) else ''
    x, at = {'elevenlabs': tts_eleven, 'rec': tts_rec, 'piper': tts_piper, 'edge': tts_edge}.get(engine, tts_say)(i, clean, prev, nxt)
    x, off = trim(x)
    x, remap = squeeze(x)
    L = len(x) / SR
    # время метки внутри клипа: по выравниванию ElevenLabs, иначе — пропорционально позиции символа
    tm = lambda idx: max(0.0, remap(at(idx) - off)) if at else L * idx / len(clean)
    m = {k: tm(idx) for k, idx in mk.items()}
    # слова для субтитров: каждое слово (с прилипшей пунктуацией) и время его начала
    ws = [(tm(mt.start()), mt.group()) for mt in re.finditer(r'\S+', clean) if re.search(r'\w', mt.group())]
    clips.append(process(x)); marks.append(m); words_all.append(ws)

scenes, t = [], 0.0
for (mind, lead, _), c, m, ws in zip(CUES, clips, marks, words_all):
    L = len(c) / SR
    dur = max(mind, math.ceil((lead + L + TAIL) / STEP) * STEP)
    scenes.append({'start': round(t, 3), 'dur': dur, 'vo': [round(t + lead, 3), round(t + lead + L, 3)],
                   'marks': {k: round(t + lead + max(0, v), 3) for k, v in m.items()},
                   'words': [[round(t + lead + w_t, 3), w] for w_t, w in ws]})
    t += dur
total = t

track = np.zeros(int(SR * total) + SR)
for s, c in zip(scenes, clips):
    i0 = int(s['vo'][0] * SR); track[i0:i0 + len(c)] += c
track = track[:int(SR * total)]
wavfile.write(a.out, SR, (np.clip(track, -1, 1) * 32767).astype(np.int16))
open(os.path.join(HERE, 'assets', 'timeline.js'), 'w').write(
    f"window.SCENES = {json.dumps(scenes, ensure_ascii=False)};\nwindow.VOICE_ENGINE = {json.dumps(engine)};\n")

print(f'engine={engine}' + (f' voice={VOICE} model={MODEL}' if engine == 'elevenlabs' else '') + (f' model={PIPER_MODEL}' if engine == 'piper' else '') + (f' voice={EDGE_VOICE} rate={EDGE_RATE}' if engine == 'edge' else ''))
for s, (clean, _) in zip(scenes, texts):
    print(f"{s['start']:6.2f} +{s['dur']:.2f}  голос {s['vo'][0]:.2f}–{s['vo'][1]:.2f}  {clean}")
print(f'длительность {total:.2f} с')
