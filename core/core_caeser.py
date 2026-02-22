from utils import ascii_to_text, text_to_ascii


def core_caesar(in_prime, in_aux) -> str:
    C1 = [1, 1, -1]
    C2 = [4, 3, 2, 1, -1, -2, -3, -4]
    aux = text_to_ascii(in_aux)
    prime = text_to_ascii(in_prime)
    tmp = 0
    c1 = prime[2] % 3
    c2 = prime[10 + c1] % 8
    c3 = prime[c2 + 3] % 16
    arr = [0] * 16
    for i in range(31 + 1):
        q = (c1 + i) % 3
        j = (c2 + i) % 8
        p = (c3 + i) % 16
        l = i % 16
        tmp = (tmp + 64 + prime[p] + C1[q] * aux[l] + C2[j]) % 32
        arr[l] = tmp
    return ascii_to_text(arr)
