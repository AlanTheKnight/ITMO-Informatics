import re


CODES = ["r1", "r2", "i1", "r3", "i2", "i3", "i4"]


def validate_input(inp: str):
    return re.match(r"^[01]{7}$", inp)


def analyse(inp: str):
    code = list(map(int, list(inp)))

    r_res = [
        code[2] ^ code[4] ^ code[6],
        code[2] ^ code[5] ^ code[6],
        code[4] ^ code[5] ^ code[6],
    ]

    syndromes = [
        code[0] ^ r_res[0],
        code[1] ^ r_res[1],
        code[3] ^ r_res[2],
    ]

    if sum(syndromes) == 0:
        print("No errors")
        return

    error_bit = int("".join(map(str, syndromes[::-1])), 2)
    code[error_bit - 1] ^= 1
    print(f"Error in bit {error_bit}, {CODES[error_bit - 1]}")
    corrected = [i[1] for i in enumerate(''.join(map(str, code))) if bin(i[0] + 1)[2:].count("1") != 1]
    print(f"Corrected code: {''.join(corrected)}")


if __name__ == "__main__":
    inp = input("Enter 7-bit code: ")
    if not validate_input(inp):
        print("Invalid input")
        exit(1)

    analyse(inp)
