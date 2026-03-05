from utils import bin_to_dec, dec_to_bin


def compose_num(num1_in, num2_in, cont_in) -> int:
    arr1 = dec_to_bin(num1_in)
    arr2 = dec_to_bin(num2_in)
    arr3 = dec_to_bin(cont_in)
    result = []
    for i in range(20):
        result.append((arr1[i] * arr3[i]) + (arr2[i] * ((1 + arr3[i]) % 2)))
    return bin_to_dec(result)
