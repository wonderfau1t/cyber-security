from typing import Literal

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
        tmp[3 - i] = rem % 32
        rem = rem // 32
    return ascii_to_text(tmp)


def confuse(in1: str, in2: str) -> str:
    arr1 = text_to_ascii(in1)
    arr2 = text_to_ascii(in2)

    for i in range(16):
        if arr1[i] > arr2[i]:
            arr1[i] = (arr1[i] + i) % 32
        else:
            arr1[i] = (arr2[i] + i) % 32
    tmp = ascii_to_text(arr1)

    return add_txt(add_txt(tmp, in1), in2)


def compress(in_16: str, out_n: Literal[16, 8, 4]) -> str:
    out = "input_error"
    if out_n == 16:
        return in_16

    a1 = in_16[0:4]
    a2 = in_16[4:8]
    a3 = in_16[8:12]
    a4 = in_16[12:16]

    if out_n == 8:
        a13 = a1 + a3
        a24 = a2 + a4
        out = add_txt(a13, a24)

    elif out_n == 4:
        a13 = sub_txt(a1, a3)
        a24 = sub_txt(a2, a4)
        out = add_txt(a13, a24)

    return out


def mixinputs(input):
    in1, in2, in3, in4 = input
    out1 = add_txt(in1, in2)
    out2 = sub_txt(in1, in2)
    out3 = add_txt(out2, add_txt(in3, in4))
    out4 = add_txt(out1, sub_txt(in3, in4))
    return [out1, out2, out3, out4]


def dec_to_bin(num_in: int) -> list[int]:
    return [int(bit) for bit in bin(num_in)[2:].zfill(20)]


def bin_to_dec(num_in: list[int]) -> int:
    tmp = list(map(str, num_in))
    tmp = "".join(tmp)
    return int(tmp, 2)


def seed_to_nums(array_in: list):
    result = []
    for item in array_in:
        result.append(block_to_num(item))
    return result


def compose_num(num1_in, num2_in, cont_in) -> int:
    arr1 = dec_to_bin(num1_in)
    arr2 = dec_to_bin(num2_in)
    arr3 = dec_to_bin(cont_in)
    result = []
    for i in range(20):
        result.append((arr1[i] * arr3[i]) + (arr2[i] * ((1 + arr3[i]) % 2)))
    return bin_to_dec(result)


def subblocks_xor(blocka_in, blockb_in):
    dec_a = block_to_num(blocka_in)
    dec_b = block_to_num(blockb_in)
    bin_a = dec_to_bin(dec_a)
    bin_b = dec_to_bin(dec_b)
    result = []
    for i in range(len(bin_a)):
        result.append((bin_a[i] + bin_b[i]) % 2)
    dec_o = bin_to_dec(result)
    return num_to_block(dec_o)


def block_xor(blocka_in, blockb_in):
    nb = len(blocka_in) // 4
    result = ""
    for i in range(nb):
        tmp_a = blocka_in[i * 4 : i * 4 + 4]
        tmp_b = blockb_in[i * 4 : i * 4 + 4]
        result += subblocks_xor(tmp_a, tmp_b)
    return result


def swap_blocks(block_in):
    left = block_in[:8]
    right = block_in[8 : 8 + 8]
    return right + left


def reverse_str(s: str) -> str:
    return s[::-1]


def pad_MD(IN: str) -> str:
    result = IN
    rem = 64 - len(IN) % 64
    if rem != 64:
        for i in range(rem):
            result += "_"
    return result


def is_sym(s_in: str) -> int:
    return True if s_in in alphabet_to_ascii else False


def sym2bin(s_in: str) -> int:
    return ord(s_in) - 48


def msg2bin(msg_in: str) -> list:
    tmp = []
    i = 0
    M = len(msg_in)

    while i < M:
        ch = msg_in[i]
        if ch in alphabet_to_ascii:
            c = symbol_to_ascii(ch)
            for j in range(4, -1, -1):
                tmp.append((c >> j) & 1)
            i += 1
        else:
            if ch == "0" or ch == "1":
                tmp.append(int(ch))
                i += 1
            else:
                i += 1

    return tmp


# print(msg2bin("ГНОЛЛЫ_ПИЛИЛИ_ПЫЛЕСОС_ЛОСОСЕМ"))
# print(len(msg2bin("ГНОЛЛЫ_ПИЛИЛИ_ПЫЛЕСОС_ЛОСОСЕМ")))


def bin2msg(bin_in: list) -> str:
    if not bin_in:
        return ""

    out = ""
    i = 0
    B = len(bin_in)

    while i < B:
        if i + 5 <= B:
            t = 0
            for _ in range(5):
                t = (t << 1) | bin_in[i]
                i += 1

            if 0 <= t <= 32:
                out += ascii_to_symbol(t)
            else:
                i -= 5
                break
        else:
            break

    while i < B:
        out += str(bin_in[i])
        i += 1

    return out


# print(bin2msg(msg2bin("ГНОЛЛЫ_ПИЛИЛИ_ПЫЛЕСОС_ЛОСОСЕМ00111")))


def block2bin(block_in):
    return dec_to_bin(block_to_num(block_in))


def bin2block(bin_in):
    return num_to_block(bin_to_dec(bin_in))
