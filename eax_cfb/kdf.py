from core.merdam_hash import merdam_hash
from core.utils import ascii_to_symbol


def kdf(mat_in: str, salt_in: str, con_in: list, size_in: list, iter_in: int) -> list:
    tmp = mat_in + salt_in

    for i in range(iter_in + 1):
        ext = merdam_hash(tmp)
        tmp = ext + tmp

    prk = tmp
    out = []

    for i in range(len(size_in)):
        q = (size_in[i] - (size_in[i] % 64)) // 64
        rem = i
        res = ""

        while rem > 0:
            h = rem % 32
            res = res + ascii_to_symbol(h)
            rem = (rem - h) // 32

        if q > 0:
            hash_val = prk
            for j in range(q + 1):
                tmp2 = hash_val + con_in[i] + prk
                hash_val = merdam_hash(tmp2)
                res = hash_val + res
        else:
            tmp2 = prk + con_in[i] + prk
            res = merdam_hash(tmp2)

        out.append(res[: size_in[i]])

    return out


# salt1 = "СЕАНС"
# pass1 = "ЧЕЧЕТКА"
# context = ["СЕАНСОВЫЙ_КЛЮЧ", "КЛЮЧ_РАСПРЕДЕЛЕНИЯ_КЛЮЧЕЙ"]
# size = [32, 16]

# print(kdf(pass1, salt1, context, size, 2))
