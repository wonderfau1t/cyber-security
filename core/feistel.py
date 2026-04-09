from core.p_scitala import frw_P_scitala, inv_P_scitala
from core.s_caeser_mod import SCaeserMod
from core.utils import add_txt, bin2block, block2bin, block_xor, sub_txt, swap_blocks


def frw_routine(block_in: str, key_in: str):
    left = block_in[:4]
    right = block_in[4 : 4 + 4]
    tmp = SCaeserMod.encrypt(right, key_in)
    left = add_txt(tmp, left)
    return right + left


# print(frw_routine("ЕГОР_КОТ", "ЗОЛОТУХА_ПИКЕТКА"))


def inv_routine(block_in: str, key_in: str):
    left = block_in[: int(len(block_in) / 2)]
    right = block_in[int(len(block_in) / 2) :]
    tmp = SCaeserMod.encrypt(left, key_in)
    right = sub_txt(right, tmp)
    return right + left


# print(inv_routine("СВЕТНДОЬ", "ЗОЛОТУХА_ПИКЕТКА"))


def bit_swap(block_in):
    b = block2bin(block_in[:4])
    for i in range(10):
        t = b[2 * i]
        b[2 * i] = b[2 * i + 1]
        b[2 * i + 1] = t
    return bin2block(b) + block_in[4 : 4 + 4]


def bit_shift(block_in):
    b = block2bin(block_in[:4])
    t = b[19]
    for i in range(19, 0, -1):
        b[i] = b[i - 1]
    b[0] = t
    return bin2block(b) + block_in[4:8]


def frw_inner(block_in, key_in, r_in):
    tmp = bit_swap(frw_P_scitala(block_in))
    for i in range(r_in):
        tmp = frw_routine(tmp, key_in)
        tmp = bit_shift(tmp)
    return frw_P_scitala(bit_swap(tmp))


# print(frw_inner("ГОР_СВЕТ", "ЗОЛОТУХА_ПИКЕТКА", 2))


def inv_inner(block_in, key_in, r_in):
    tmp = inv_P_scitala(block_in)
    for i in range(r_in):
        tmp = inv_routine(tmp, key_in)
    return inv_P_scitala(tmp)


# print(inv_inner("ОУСТМЫЙЫ", "ЗОЛОТУХА_ПИКЕТКА", 2))


def round(block_in, key_in):
    left = block_in[:8]
    right = block_in[8 : 8 + 8]
    tmp = frw_inner(right, key_in, 2)
    left = block_xor(tmp, left)
    return right + left


# print(round("КОРЫСТЬ_СЛОНА_ЭХ", "МТВ_ВСЕ_ЕЩЕ_ТЛЕН"))


def frw(block_in, keys_in, r_in):
    key_set = keys_in
    block = block_xor(block_in, key_set[0])
    for i in range(1, r_in + 1):
        block = round(block, key_set[i])
    return block_xor(block, key_set[r_in + 1])


def inv(block_in, keys_in, r_in):
    key_set = keys_in
    block = block_xor(block_in, key_set[r_in + 1])
    block = swap_blocks(block)
    for i in range(r_in, 0, -1):
        block = round(block, key_set[i])
    block = swap_blocks(block)
    return block_xor(block, key_set[0])
