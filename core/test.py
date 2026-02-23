import matplotlib.pyplot as plt
import numpy as np
from merdam_hash import merdam_hash

DEFAULT_NUM_HASHES = 10000
DEFAULT_HASH_LENGTH = 64
ALPHABET = list("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ_")


def generate_hash_chain(start: str, length: int):
    chain = []
    current = start
    for i in range(length):
        if i % 1000 == 0:
            print(f"Прогресс: {i}/{length}", end='\r')
        h = merdam_hash(current)
        chain.append(h)
        current = h
    print(f"Прогресс: {length}/{length}")

    return chain


# как часто символ встречается на каждой позиции
def test_symbol_by_position(chain, symbol: str):
    freq = [0] * 64
    for h in chain:
        for pos, ch in enumerate(h):
            if ch == symbol:
                freq[pos] += 1
    
    return freq


def print_symbol_test_result(freq, symbol: str, num_hashes: int):
    print(f"\nЧастота появления '{symbol}' по позициям:")
    
    # выводим по 8 позиций в строке
    for block in range(8):
        start = block * 8
        end = start + 8
        line = f"поз.{start:2}-{end-1:2}: "
        line += " ".join(f"{freq[p]:5d}" for p in range(start, end))
        print(line)
    
    avg_freq = sum(freq) / 64
    expected = num_hashes / len(ALPHABET)
    print(f"Среднее появление на каждой позиции: {avg_freq:.1f} (ожидание: {expected:.1f})")
    print(f"Всего появлений символа: {sum(freq)} (ожидание: {num_hashes * 64 / len(ALPHABET):.0f})")

    # гисторгамма распределения символа по позициям
    plt.figure(figsize=(10, 5))
    positions = range(64)
    plt.bar(positions, freq, color='skyblue', edgecolor='navy', alpha=0.7)
    plt.axhline(y=expected, color='red', linestyle='--', linewidth=2, 
                label=f'Ожидание = {expected:.1f}')
    
    # Подписываем все позиции, но поворачиваем для читаемости
    plt.xticks(positions, positions, fontsize=6)
    plt.xlabel('Позиция в хеше')
    plt.ylabel('Частота')
    plt.title(f"Распределение символа '{symbol}' по позициям")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

# как часто каждой символ встречается на этой позиции
def test_position_by_symbol(chain, position: int):
    freq = {ch: 0 for ch in ALPHABET}
    for h in chain:
        ch = h[position]
        if ch in freq:
            freq[ch] += 1
    
    return freq

def print_position_test_result(freq, position: int, num_hashes: int):
    print(f"\nЧастота символов в позиции {position}:")

    items = sorted(freq.items())
    chars = [item[0] for item in items]
    counts = [item[1] for item in items]
    
    # вывод по 8 символов в строке
    line = []
    for i, (ch, cnt) in enumerate(items):
        line.append(f"{ch}:{cnt:4d}")
        if (i + 1) % 8 == 0 or i == len(items)-1:
            print("  " + "  ".join(line))
            line = []

    expected = num_hashes / len(ALPHABET)
    
    # гистограмма распределения символов в конкретной позиции
    plt.figure(figsize=(10, 5))
    
    x_pos = range(len(chars))
    plt.bar(x_pos, counts, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
    plt.axhline(y=expected, color='red', linestyle='--', linewidth=2,
                label=f'Ожидание = {expected:.1f}')
    plt.xticks(x_pos, chars, rotation=0)
    plt.xlabel('Символ')
    plt.ylabel('Частота')
    plt.title(f"Распределение символов в позиции {position}")
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()


def run_generation_test(
    message: str = "ЭТО_НАЧАЛЬНОЕ_ЗНАЧЕНИЕ_ПО_УМОЛЧАНИЮ",
    target_symbol: str = None,      # буква для теста "по символам" (если None - не выполняется)
    target_position: int = None,    # позиция для теста "по позициям" (если None - не выполняется)
):
    print(f"\nНачало генерации цепочки из {DEFAULT_NUM_HASHES} хэшей")
    
    chain = generate_hash_chain(message, DEFAULT_NUM_HASHES)
    
    # тест для одной буквы по всем позициям
    if target_symbol is not None:
        freq = test_symbol_by_position(chain, target_symbol)
        print_symbol_test_result(freq, target_symbol, DEFAULT_NUM_HASHES)
    
    # тест для одной позиции по всем символам
    if target_position is not None:
        freq = test_position_by_symbol(chain, target_position)
        print_position_test_result(freq, target_position, DEFAULT_NUM_HASHES)
    
    return