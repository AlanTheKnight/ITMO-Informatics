import re


samples = (
    "20 + 22 = 42",
    "30 - 12 != 1412",
    "12412",
    "Жило-было 3 крокодила",
    "2023 год совсем не весёлый",
    "8 * 12",
    "81 / 9 = 27 / 3",
    "5 / 0",
)


def calc(x):
    try:
        return str(eval(x.group(1)))
    except ZeroDivisionError:
        return "∞"


for sample_n, sample in enumerate(samples):
    print(f"Sample #{sample_n + 1}: {sample}")
    print(re.sub(r"(\d+)", lambda x: str(4 * int(x.group(1)) ** 2 - 7), sample))
    print(re.sub(r"(\d+\s[+/\-*]\s\d+)", calc, sample))
    print()
