# Таймкоды глав по настоящей озвучке: python tools/chapters.py  (после build.ps1, читает build/frames/timeline.json)
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['Вступление', 'Кто я и что покажу', 'Гиперспавн: 7 гуманоидов', 'Скорость респавна', 'Что падает: лут',
         '2 нюанса: здоровье, сумки, Деджанк', 'Запретные методы голдфарма (Бусти)', 'Фарм с 12 уровня: тактика',
         'Таланты и шмот', 'Где точка: карта', 'Что меня удивило', 'Итог']
sc = json.load(open(os.path.join(ROOT, 'build', 'frames', 'timeline.json'), encoding='utf-8'))['scenes']
for n, s in zip(NAMES, sc):
    t = 0 if s is sc[0] else round(s['start'])
    print(f'{t // 60}:{t % 60:02d} {n}')
