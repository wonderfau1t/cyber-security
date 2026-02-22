from typing import Literal

from core_caeser import core_caesar
from utils import add_txt, compress, confuse


def c_block(in_arr: list[str], out_size: Literal[16, 8, 4]) -> str:
    result = ""
    C = [
        "_" * 16,
        "ПРОЖЕКТОР_ЧЕПУХИ",
        "КОЛЫХАТЬ_ПАРОДИЮ",
        "КАРМАННЫЙ_АТАМАН",
    ]
    flag = True
    for i in range(len(in_arr)):
        if len(in_arr[i]) == 16:
            C[i] = add_txt(C[i], in_arr[i])
        else:
            flag = False
    if flag:
        C[1] = add_txt(C[1], in_arr[0])
        tmp1 = core_caesar(C[0], C[2])
        tmp2 = core_caesar(C[3], C[1])
        tmp3 = confuse(tmp1, tmp2)
        result = core_caesar(tmp3, tmp1)
        result = compress(result, out_size)
    return result
