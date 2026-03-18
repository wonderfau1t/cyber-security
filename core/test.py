from feistel import frw, inv
from produce_round_keys import produce_round_keys

set1 = [[252564, 9109, 961193], [252564, 9109, 961193], [723482, 8677, 983609]]
set2 = [[51190, 7927, 990711], [51190, 7927, 990711], [549234, 6949, 939683]]
set3 = [[227796, 5107, 981875], [227796, 5107, 981875], [167490, 9871, 809137]]
set4 = [[357630, 8971, 948209], [357630, 8971, 948209], [73335, 6779, 1014784]]
LCG_SET = [set1, set2, set3, set4]

in1 = "КОРЫСТЬ_СЛОНА_ЭХ"
in2 = "НУЖНО_БОЛЬШЕ_ПЫЩ"
key = "МТВ_ВСЕ_ЕЩЕ_ТЛЕН"


keys = produce_round_keys(key, 6)

out1 = frw(in1, keys, 1)
lout1 = inv(out1, keys, 1)

out2 = frw(in2, keys, 4)
lout2 = inv(out2, keys, 4)

print(lout1, lout2)

print(keys)
