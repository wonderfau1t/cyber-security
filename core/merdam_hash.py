from c_block import c_block
from macrocompression import macrocompression
from utils import pad_MD


def merdam_hash(msg: str) -> str:
    data = pad_MD(msg)
    n = len(data) / 64
    a, b, c, d, e = ["_" * 16 for i in range(5)]
    for i in range(int(n)):
        tmp = data[i * 64 : i * 64 + 64]
        a, b, c, d, e = macrocompression(tmp, a + b + c + d + e)
    p1 = c_block([a, e], 16)
    p2 = c_block([b, e], 16)
    p3 = c_block([c, e], 16)
    p4 = c_block([d, e], 16)
    return p1 + p2 + p3 + p4
