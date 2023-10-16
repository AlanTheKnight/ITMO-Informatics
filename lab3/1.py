"""
Лабораторная работа №3 «Регулярные выражения»

Номер в ИСУ: 408512

Глаза: X
Нос: -
Рот: P
"""


import re


def find_with_re(text: str):
    return len(re.findall(r"X-P", text))


samples = [
    ("Фу, какая гадость! X-P", 1),
    ("Ужас какой-то! X-P X-P X-P", 3),
    ("Вот это да! X-P X-P X-P X-P X-P", 5),
    ("Что это такое X-P? Ну и гадость же! X-PX-P", 3),
    ("Не люблю людей, которые не используют регулярные выражения X-PX-PX-PX-P", 3),
]

try:
    for test in samples:
        assert find_with_re(test[0]) == test[1]
    print("All tests passed")
except AssertionError:
    print("Tests failed")
