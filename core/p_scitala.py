from math import floor


def frw_P_scitala(block_in: str) -> str:
    q = floor(len(block_in) / 2)
    f = len(block_in) % 2
    tmp_a = block_in[: q + f]
    tmp_b = block_in[q + f : q + f + q]
    result = ""
    for i in range(q):
        if i % 2 == 0:
            result += tmp_a[i : i + 1]
            result += tmp_b[i : i + 1]
        else:
            result += tmp_b[i : i + 1]
            result += tmp_a[i : i + 1]
    if f == 1:
        result += tmp_a[q + f : q + f + 1]
    return result


def inv_P_scitala(block_in: str) -> str:
    q = floor(len(block_in) / 2)
    f = len(block_in) % 2
    tmp_a = ""
    tmp_b = ""
    for i in range(q):
        if i % 2 == 0:
            tmp_a += block_in[2 * i : 2 * i + 1]
            tmp_b += block_in[2 * i + 1 : 2 * i + 1 + 1]
        else:
            tmp_b += block_in[2 * i : 2 * i + 1]
            tmp_a += block_in[2 * i + 1 : 2 * i + 1 + 1]
    if f == 1:
        tmp_a += block_in[2 * q : 2 * q + 1]

    return tmp_a + tmp_b
