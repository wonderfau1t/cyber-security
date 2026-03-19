from p_scitala import frw_P_scitala, inv_P_scitala
from s_caeser_mod import SCaeserMod
from utils import add_txt, block_xor, sub_txt, swap_blocks


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


def frw_inner(block_in, key_in, r_in):
    tmp = frw_P_scitala(block_in)
    for i in range(r_in):
        tmp = frw_routine(tmp, key_in)
    return frw_P_scitala(tmp)


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
    tmp = frw_inner(right, key_in, 3)
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
