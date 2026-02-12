import random
from s_caeser_mod import SCaeserMod
from utils import add_txt

ALPHABET = list("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯ_")

def random_text(length):
    return "".join(random.choice(ALPHABET) for _ in range(length))


def mutate_one_symbol(text):
    pos = random.randint(0, len(text) - 1)
    new_char = random.choice([c for c in ALPHABET if c != text[pos]])
    return text[:pos] + new_char + text[pos + 1:]


def hamming_distance(s1, s2):
    return sum(1 for a, b in zip(s1, s2) if a != b)


def test_small_input_change():
    base_inputs = [random_text(4) for _ in range(30)]
    mutated_inputs = [mutate_one_symbol(t) for t in base_inputs]

    stats = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    total_tests = 0

    for key_index in range(20):  # 20 ключей
        key = random_text(16)

        # print(f"\n\n------------ {key_index} ключ {key} ------------")

        for text, text_mod in zip(base_inputs, mutated_inputs):  # 30 входов

            out1 = SCaeserMod.encrypt(text, key)
            out2 = SCaeserMod.encrypt(text_mod, key)

            diff = hamming_distance(out1, out2)
            stats[diff] += 1
            total_tests += 1

            if diff <= 2:
                print(f"{diff} отл. | входы {text} и {text_mod}, выходы {out1} и {out2}, ключ {key}")

            # print(f"входы {text} и {text_mod}, выходы {out1} и {out2}")

    print("\nРаспределение отличий (малое изменение входа):")
    for k in sorted(stats.keys(), reverse=True):
        percent = (stats[k] / total_tests) * 100
        print(f"{k} символ(а): {stats[k]} случаев ({percent:.1f}%)")

    avg = sum(k * v for k, v in stats.items()) / total_tests
    print(f"\nСреднее число отличий: {avg:.2f} из 4")



def test_key_linearity():
    inputs = [random_text(4) for _ in range(30)]
    key_pairs = [(random_text(16), random_text(16)) for _ in range(20)]

    stats = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    total_tests = 0

    for i, text in enumerate(inputs, start=1):
        # print(f"\n\n------------ {i} вход {text} ------------")

        for k1, k2 in key_pairs:
            k_sum = add_txt(k1, k2)

            e1 = SCaeserMod.encrypt(text, k1)
            e2 = SCaeserMod.encrypt(text, k2)

            left = add_txt(e1, e2) # сумма выходов
            right = SCaeserMod.encrypt(text, k_sum) # выход суммы

            diff = hamming_distance(left, right)
            stats[diff] += 1
            total_tests += 1

            if diff <= 2:
                print(f"{diff} отл. | ключи {k1} и {k2}, сумма выходов: {left}; выход суммы: {right}, вход: {text}")

            # print(f"ключи {k1} и {k2}, сумма выходов: {left}; выход суммы: {right}")

    print("\nРаспределение отличий (линейность преобразований по ключу):")
    for k in sorted(stats.keys(), reverse=True):
        percent = (stats[k] / total_tests) * 100
        print(f"{k} символ(а): {stats[k]} случаев ({percent:.1f}%)")

    avg = sum(k * v for k, v in stats.items()) / total_tests
    print(f"\nСреднее число отличий: {avg:.2f} из 4")
