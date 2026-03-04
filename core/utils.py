alphabet_to_ascii = {
    "А": 1,
    "Б": 2,
    "В": 3,
    "Г": 4,
    "Д": 5,
    "Е": 6,
    "Ж": 7,
    "З": 8,
    "И": 9,
    "Й": 10,
    "К": 11,
    "Л": 12,
    "М": 13,
    "Н": 14,
    "О": 15,
    "П": 16,
    "Р": 17,
    "С": 18,
    "Т": 19,
    "У": 20,
    "Ф": 21,
    "Х": 22,
    "Ц": 23,
    "Ч": 24,
    "Ш": 25,
    "Щ": 26,
    "Ы": 27,
    "Ь": 28,
    "Э": 29,
    "Ю": 30,
    "Я": 31,
    "_": 0,
}
ascii_to_alphabet = {v: k for k, v in alphabet_to_ascii.items()}


def symbol_to_ascii(symbol: str) -> int:
    return alphabet_to_ascii[symbol]


def text_to_ascii(text: str) -> list[int]:
    return [alphabet_to_ascii[symbol] for symbol in text]


def ascii_to_symbol(ascii_num: int) -> str:
    return ascii_to_alphabet[ascii_num]


def ascii_to_text(array: list[int]) -> str:
    return "".join([ascii_to_alphabet[num] for num in array])


def add_s(s1_in: str, s2_in: str) -> str:
    tmp = symbol_to_ascii(s1_in) + symbol_to_ascii(s2_in)
    return ascii_to_symbol(tmp % 32)


def sub_s(s1_in: str, s2_in: str) -> str:
    tmp = symbol_to_ascii(s1_in) - symbol_to_ascii(s2_in) + 32
    return ascii_to_symbol(tmp % 32)


def add_txt(t1_in: str, t2_in: str) -> str:
    result = ""

    m = min(len(t1_in), len(t2_in))
    t_in = t1_in if len(t1_in) > len(t2_in) else t2_in

    M = len(t_in)

    for i in range(m):
        t1 = t1_in[i : i + 1]
        t2 = t2_in[i : i + 1]
        result += add_s(t1, t2)

    if M > m:
        for i in range(m, M):
            t = t_in[i : i + 1]
            result += t

    return result


def sub_txt(t1_in: str, t2_in: str) -> str:
    result = ""

    m = min(len(t1_in), len(t2_in))

    if len(t1_in) > len(t2_in):
        t_in = t1_in
        flag = False
    else:
        t_in = t2_in
        flag = True

    M = len(t_in)

    for i in range(m):
        t1 = t1_in[i : i + 1]
        t2 = t2_in[i : i + 1]
        result += sub_s(t1, t2)

    if M > m:
        for i in range(m, M):
            t = t_in[i : i + 1]
            if flag:
                result += sub_s("_", t)
            else:
                result += sub_s(t, "_")

    return result


def block_to_num(block_in: str) -> int:
    result = 0
    pos = 1
    tmp = text_to_ascii(block_in)
    for i in range(3, -1, -1):
        result += pos * tmp[i]
        pos *= 32
    return result


def num_to_block(num_in: int) -> str:
    rem = num_in
    tmp = [0] * 4
    for i in range(4):
        print(rem)
        tmp[3 - i] = rem % 32
        rem = rem // 32
    return ascii_to_text(tmp)


def dec_to_bin(num_in: int) -> list[int]:
    return [int(bit) for bit in bin(num_in)[2:].zfill(20)]


def bin_to_dec(num_in: str) -> int:
    return int(num_in, 2)
