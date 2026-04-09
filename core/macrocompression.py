from core.blocks_ops import block_mask, blocks_mix
from core.c_block import c_block
from core.utils import add_txt


def macrocompression(IN: str, STATE: str) -> list[str]:
    a = add_txt(IN[0:16], STATE[0:16])
    b = add_txt(IN[16 : 16 + 16], STATE[16 : 16 + 16])
    c = add_txt(IN[32 : 32 + 16], STATE[32 : 32 + 16])
    d = add_txt(IN[48 : 48 + 16], STATE[48 : 48 + 16])
    e = STATE[64 : 64 + 16]
    con = "ААААЯЯЯЯААЯЯААЯЯ"
    for i in range(12):
        e = add_txt(e, c_block([a, b, c, d], 16))
        tmp = blocks_mix(c, d)
        con = add_txt(con, "ААААЯЯЯЯААЯЯААЯЯ")
        c = tmp[0]
        d = tmp[1]
        b = block_mask(b, con)
        a, b, c, d, e = b, c, d, e, a
    return [a, b, c, d, e]
