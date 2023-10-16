import re


samples = ("20 + 22 = 42",)


for sample_n, sample in enumerate(samples):
    print(f"Sample #{sample_n + 1}: {sample}")
    print(re.sub(r"(\d+)", lambda x: str(4 * int(x.group(1)) ** 2 - 7), sample))
    print()
