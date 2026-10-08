# Таймкоды глав по настоящей озвучке: python tools/chapters.py  (после build.ps1, читает build/frames/timeline.json)
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['Вступление', 'Привет, голдфармеры', 'Секрет: шаман-хил', 'Где я фармлю', 'Аукцион не работает',
         'Редкий дроп: сабля', 'Огромные пуллы', 'Запретные методы голдфарма (Бусти)', 'Снежная буря и 29 уровень',
         'Обратно на Тайную магию', 'Дзинь, 30 уровень', 'Лучшая ферма до 30 (Орда)']
sc = json.load(open(os.path.join(ROOT, 'build', 'frames', 'timeline.json'), encoding='utf-8'))['scenes']
for n, s in zip(NAMES, sc):
    t = 0 if s is sc[0] else round(s['start'])
    print(f'{t // 60}:{t % 60:02d} {n}')
