from core.c_block import c_block
from core.utils import add_txt


def init_prng(seed: str) -> list[str]:
    const = ["ПЕРВОЕ_АКТЕРСТВО", "ВТОРОЙ_ДАЛЬТОНИК", "ТРЕТЬЯ_САДОВНИЦА", "ЧЕТВЕРТЫЙ_ГОБЛИН"]
    values = []

    for item in const:
        values.append(c_block([item, seed], 16))
    secret = c_block(values, 16)

    result = []
    for i in range(4):
        tmp = values[i]
        TMP = ""
        for _ in range(4):
            tmp = add_txt(tmp, const[i])
            TMP += c_block([tmp, secret], 4)
            tmp = add_txt(tmp, TMP)
        result.append(TMP[4 : 4 + 12])
    return result
