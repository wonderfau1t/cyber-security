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

#print(lout1, lout2)

#print(keys)

#print(f"Исходный текст: {in1}\nЗашифрованный: {out1}\nРасшифрованный: {lout1}\n")
#print(f"Исходный текст: {in2}\nЗашифрованный: {out2}\nРасшифрованный: {lout2}\n")
#print(f"Цепочка ключей: {keys}")

import random
from feistel import frw
from produce_round_keys import produce_round_keys
from utils import block_to_num, num_to_block
import matplotlib.pyplot as plt

# ---------------------------
# Настройки
# --------------------------
NUM_KEYS = 8                  # число раундовых ключей
BLOCK_SIZE = 16               # длина блока в символах

# Генерация раундовых ключей
round_keys = produce_round_keys(key, NUM_KEYS)

# ---------------------------
# 1. Строгий аваланш-тест
# ---------------------------
def strict_avalanche_test(blocks_count=100, rounds=1, plot=True):
    results = [[] for _ in range(BLOCK_SIZE * 5)]  # 80 бит
    
    for _ in range(blocks_count):
        pt = ''.join(random.choices("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ_", k=BLOCK_SIZE))
        ct = frw(pt, round_keys, rounds)
        
        # Превращаем открытый текст в битовую строку (80 бит)
        pt_bits = ''.join(format(block_to_num(pt[i*4:(i+1)*4]), "020b") for i in range(4))
        
        for bit_index in range(len(pt_bits)):
            # инвертируем бит
            flipped_bits = list(pt_bits)
            flipped_bits[bit_index] = "1" if flipped_bits[bit_index] == "0" else "0"
            
            # собираем обратно в текстовый блок
            new_pt_bits = ''.join(flipped_bits)
            new_block = ''.join(
                num_to_block(int(new_pt_bits[i*20:(i+1)*20], 2)) for i in range(4)
            )
            new_ct = frw(new_block, round_keys, rounds)
            
            # Превращаем шифротексты в битовые строки
            ct_bits = ''.join(format(block_to_num(ct[i*4:(i+1)*4]), "020b") for i in range(4))
            new_ct_bits = ''.join(format(block_to_num(new_ct[i*4:(i+1)*4]), "020b") for i in range(4))
            
            hamming = sum(c1 != c2 for c1, c2 in zip(ct_bits, new_ct_bits))
            results[bit_index].append(hamming)
    
    # Суммируем по каждому биту
    sum_j = [sum(col) for col in results]
    expected = blocks_count * 40  # 100 * 40 = 4000
    
    print(f"Строгий аваланш-тест (раундов {rounds})")
    print(f"Суммы по каждому биту (ожидание ≈ {expected}):")
    print(sum_j)
    
    # Гистограмма
    if plot:
        plt.figure(figsize=(12, 5))
        plt.bar(range(len(sum_j)), sum_j, color='skyblue', edgecolor='navy')
        plt.axhline(y=expected, color='red', linestyle='--', label=f'Ожидание = {expected}')
        plt.xlabel('Номер бита')
        plt.ylabel('Сумма расстояний Хэмминга')
        plt.title(f'Строгий аваланш-тест (раундов {rounds})')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    return sum_j

def random_block(length=16):
    """Генерирует случайный блок из length символов (80 бит)."""
    alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ_"
    return ''.join(random.choices(alphabet, k=length))

def generative_differential_test(length=1000, rounds=6, plot=True):
    # Начальные блоки (связанные цепочки)
    X_chain = [random_block()]
    Y_chain = [random_block()]
    
    # Строим цепочки блоков, каждый следующий блок слегка отличается от предыдущего
    for i in range(1, length):
        # Можно просто изменять один случайный символ предыдущего блока
        prev_x = list(X_chain[-1])
        prev_y = list(Y_chain[-1])
        
        idx_x = random.randint(0, 15)
        idx_y = random.randint(0, 15)
        
        alphabet = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ_"
        prev_x[idx_x] = random.choice(alphabet)
        prev_y[idx_y] = random.choice(alphabet)
        
        X_chain.append(''.join(prev_x))
        Y_chain.append(''.join(prev_y))
    
    di = []
    
    for xi, yi in zip(X_chain, Y_chain):
        # C[Xi], C[Yi] и C[Xi+Yi] (для блока Xi+Yi используем посимвольное суммирование по модулю длины алфавита)
        c_xi = frw(xi, round_keys, rounds)
        c_yi = frw(yi, round_keys, rounds)
        
        # Суммируем блоки по модулю длины алфавита, чтобы получить "Xi + Yi"
        sum_block = ''.join(
            alphabet[(alphabet.index(xi[j]) + alphabet.index(yi[j])) % len(alphabet)]
            for j in range(len(xi))
        )
        c_sum = frw(sum_block, round_keys, rounds)
        
        # Переводим в битовые строки
        bits_xi = ''.join(format(block_to_num(c_xi[j*4:(j+1)*4]), "020b") for j in range(4))
        bits_yi = ''.join(format(block_to_num(c_yi[j*4:(j+1)*4]), "020b") for j in range(4))
        bits_sum = ''.join(format(block_to_num(c_sum[j*4:(j+1)*4]), "020b") for j in range(4))
        
        # Qi = C[Xi] XOR C[Yi]
        bits_qi = ''.join('1' if bits_xi[k] != bits_yi[k] else '0' for k in range(len(bits_xi)))
        # Расстояние Хэмминга между Qi и Oi
        hamming = sum(bits_qi[k] != bits_sum[k] for k in range(len(bits_qi)))
        di.append(hamming)
    
    print(f"Генеративный дифференциальный тест (раундов {rounds})")
    print("Первые 20 d_i:", di[:20])
    
    if plot:
        plt.figure(figsize=(10, 5))
        plt.hist(di, bins=range(0, 81, 2), edgecolor='black', color='lightgreen')
        plt.axvline(x=40, color='red', linestyle='--', label='Идеал (40)')
        plt.xlabel('Расстояние Хэмминга')
        plt.ylabel('Частота')
        plt.title(f'Генеративный дифференциальный тест (раундов {rounds})')
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    return di


# 1. Аваланш-тест для 6 раундов
sum_2_rounds = strict_avalanche_test(rounds=6)


# 3. Аваланш-тест для 2 и 4 раундов
sum_4_rounds = strict_avalanche_test(rounds=4)
sum_2_rounds = strict_avalanche_test(rounds=2)


# 2. Генеративный тест
diff_test_results = generative_differential_test(rounds=6)
