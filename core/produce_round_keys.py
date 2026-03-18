from lcg_class import LCG


def produce_round_keys(key_in, num_in):
    set1 = [[252564, 9109, 961193], [252564, 9109, 961193], [723482, 8677, 983609]]
    set2 = [[51190, 7927, 990711], [51190, 7927, 990711], [549234, 6949, 939683]]
    set3 = [[227796, 5107, 981875], [227796, 5107, 981875], [167490, 9871, 809137]]
    set4 = [[357630, 8971, 948209], [357630, 8971, 948209], [73335, 6779, 1014784]]
    LCG_SET = [set1, set2, set3, set4]
    strings = []
    lcg = LCG(key_in, LCG_SET)
    if num_in > 1:
        for _ in range(num_in):
            strings.append(lcg.next()[0])
    return strings


# print(produce_round_keys("ПОЛИМАТ_ТЕХНОБОГ", 6))
