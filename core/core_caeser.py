from core.utils import ascii_to_text, text_to_ascii


def core_caesar(in_prime, in_aux) -> str:
    C1 = [1, -1, 1, -1, 1, -1, 1]
    C2 = [1, -1, 1, -1, 1]
    aux = text_to_ascii(in_aux)
    prime = text_to_ascii(in_prime)
    tmp = 0
    t1 = 0
    for i in range(16):
        t1 += aux[i]
    c1 = t1 % 7
    c2 = prime[2 * c1 + 1] % 5
    c3 = (prime[2 * c2] + prime[2 * c1]) % 16
    arr = [0] * 16
    for i in range(16):
        q = (c1 + i) % 7
        j = (c2 + i) % 5
        p = (c3 + i) % 16
        l = i % 16
        tmp = (tmp + 64 + prime[p] + C1[q] * C2[j] * aux[l]) % 32
        arr[l] = tmp
    return ascii_to_text(arr)
