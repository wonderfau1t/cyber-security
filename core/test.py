import math
import matplotlib.pyplot as plt
from utils import symbol_to_ascii
from c_ct_lcg_next import c_ct_lcg_next

set1 = [[252564, 9109, 961193], [252564, 9109, 961193], [723482, 8677, 983609]]
set2 = [[51190, 7927, 990711], [51190, 7927, 990711], [549234, 6949, 939683]]
set3 = [[227796, 5107, 981875], [227796, 5107, 981875], [167490, 9871, 809137]]
set4 = [[357630, 8971, 948209], [357630, 8971, 948209], [73335, 6779, 1014784]]
SET = [set1, set2, set3, set4]

seed = "АБВГДЕЖЗИЙКЛМНОП"
set_ = [
    [723482, 8677, 983609],
    [252564, 9109, 961193],
    [357630, 8971, 948209],
]

out, intern = c_ct_lcg_next("up", -1, seed, SET)
print(out)
print(intern)

# проверка влияния seed на генерируемую последовательность
def test_seed_influences(seed1, seed2, settings=SET, num_blocks=5):
    
    _, state1 = c_ct_lcg_next("up", -1, seed1, settings)
    _, state2 = c_ct_lcg_next("up", -1, seed2, settings)

    out1 = []
    out2 = []

    for _ in range(num_blocks):
        stream1, state1 = c_ct_lcg_next("down", state1, "", settings)
        stream2, state2 = c_ct_lcg_next("down", state2, "", settings)
        out1.append(stream1)
        out2.append(stream2)

    print(f"seed1 = {seed1}")
    for i, block in enumerate(out1):
        print(f"  блок {i+1}: {block}")

    print(f"\nseed2 = {seed2}")
    for i, block in enumerate(out2):
        print(f"  блок {i+1}: {block}")

    if out1 == out2:
        print("Последовательности одинаковые, seed не влияет")
    else:
        print("Seed влияет, последовательности разные")


# проверка, что seed воспроизодится
def test_reproducibility(seed, settings=SET, num_blocks=5):
    # первый запуск
    _, state1 = c_ct_lcg_next("up", -1, seed, settings)
    out1 = []
    for _ in range(num_blocks):
        stream, state1 = c_ct_lcg_next("down", state1, "", settings)
        out1.append(stream)

    # второй запуск (с тем же seed)
    _, state2 = c_ct_lcg_next("up", -1, seed, settings)
    out2 = []
    for _ in range(num_blocks):
        stream, state2 = c_ct_lcg_next("down", state2, "", settings)
        out2.append(stream)

    print(f"seed = {seed}")
    print("\nПервый запуск:")
    for i, block in enumerate(out1):
        print(f"  блок {i+1}: {block}")

    print("\nВторой запуск:")
    for i, block in enumerate(out2):
        print(f"  блок {i+1}: {block}")

    if out1 == out2:
        print("Выходы совпадают при одинаковом seed")
    else:
        print("Выходы различаются при одинаковом seed")


# частотный монобитный тест
def monobit_test(bits):
    n0 = bits.count(0)
    n1 = bits.count(1)
    n = n0 + n1
    p0 = n0 / n
    p1 = n1 / n
    s = math.sqrt(n * p0 * p1) / n
    if s == 0:
        return float('inf'), False
    x = abs(p0 - p1) / s
    return x, x < 3


# тест на длину серии единиц
def max_run_of_ones_test(bits):
    max_run = 0
    current_run = 0
    for bit in bits:
        if bit == 1:
            current_run += 1
            if current_run > max_run:
                max_run = current_run
        else:
            current_run = 0
    return max_run, (10 <= max_run <= 15)


# обертка над частотным тестом и на длину
def nist_tests(seed= "АБВГДЕЖЗИЙКЛМНОП"):
    num_replications = 200
    blocks_per_rep = 50  # 50 блоков * 80 бит = 4000 бит

    x_vals = []
    m_vals = []
    monobit_pass = 0
    maxrun_pass = 0

    _, state = c_ct_lcg_next("up", -1, seed, SET)

    for rep in range(num_replications):
        bits = []
        for _ in range(blocks_per_rep):
            stream, state = c_ct_lcg_next("down", state, "", SET)
            for ch in stream:
                num = symbol_to_ascii(ch)
                for shift in range(4, -1, -1):
                    bits.append((num >> shift) & 1)

        x, ok1 = monobit_test(bits)
        x_vals.append(x)
        if ok1:
            monobit_pass += 1

        m, ok2 = max_run_of_ones_test(bits)
        m_vals.append(m)
        if ok2:
            maxrun_pass += 1
    
    print(f"\nЧастотный монобитный тест")
    print(f"   Прошли: {monobit_pass}/{num_replications} ({monobit_pass/num_replications:.2%})")
    print(f"\nТест на длину серии единиц")
    print(f"   Прошли: {maxrun_pass}/{num_replications} ({maxrun_pass/num_replications:.2%})")


    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.hist(x_vals, bins=30, edgecolor='black')
    plt.axvline(x=3, color='red', linestyle='--')
    plt.xlabel('x')
    plt.ylabel('Частота')
    plt.title('Монобитный тест')

    plt.subplot(1, 2, 2)
    plt.hist(m_vals, bins=range(0, 21), edgecolor='black', align='left')
    plt.axvline(x=10, color='red', linestyle='--')
    plt.axvline(x=15, color='red', linestyle='--')
    plt.xlabel('Макс. длина серии единиц m')
    plt.ylabel('Частота')
    plt.title('Тест на длину серии')

    plt.tight_layout()
    plt.show()