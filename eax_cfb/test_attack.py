from eax_cfb.eax import EAXCFB
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(BASE_DIR, "test_data.txt")


def load_test_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Разделяем по секциям
    messages = []
    assocdata = []
    key = ""
    nonce = ""
    
    current_section = None
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line == '[MESSAGES]':
            current_section = 'messages'
            continue
        elif line == '[ASSOCDATA]':
            current_section = 'assocdata'
            continue
        elif line == '[KEY]':
            current_section = 'key'
            continue
        elif line == '[NONCE]':
            current_section = 'nonce'
            continue
        
        if current_section == 'messages':
            messages.append(line)
        elif current_section == 'assocdata':
            parts = line.split(',')
            assocdata.append(parts[:4])
        elif current_section == 'key':
            key = line
        elif current_section == 'nonce':
            nonce = line
    
    
    return messages, assocdata, key, nonce



class SingleOracle:
    """Оракул для одного пакета"""
    def __init__(self, assocdata, key, nonce):
        self.assocdata = assocdata
        self.key = key
        self.nonce = nonce
        self.eax = EAXCFB()
    
    def decrypt(self, packet_bits):
        """Отправляет один пакет на расшифрование"""
        try:
            # Пакет передаётся как список из одного элемента
            received = self.eax.eax_cfb(
                self.assocdata, [packet_bits], self.key, self.nonce, "receive"
            )
            if received and received[0][3] == "ОК":
                return True, received[0][2]
            else:
                return False, None
        except Exception as e:
            return False, None
        


# Нарушение целостности (изменить шифротекст так, чтобы MAC остался валидным)
def test_integrity_attack():
    print("\nАтака 1: Нарушение целостности")
    
    messages, assocdata, key, nonce = load_test_data(filepath)
    single_assocdata = assocdata[0]
    
    eax = EAXCFB()
    packets = eax.eax_cfb(single_assocdata, messages, key, nonce, "send")
    
    if not packets:
        print("Нет пакетов")
        return
    
    original = packets[0]
    print(f"Оригинальный пакет (первые 100 бит): {original[:100]}...")
    
    # Модифицируем бит в шифротексте
    corrupted = original[:]
    bit_pos = 300
    if bit_pos < len(corrupted):
        corrupted[bit_pos] ^= 1
        print(f"Бит {bit_pos} инвертирован")
    
    oracle = SingleOracle(single_assocdata, key, nonce)
    success, msg = oracle.decrypt(corrupted)
    
    if success:
        print(f"УЯЗВИМОСТЬ: подделка принята!")
    else:
        print("Защита сработала: пакет отвергнут")


def test_iv_attack():
    print("\nАтака 2: Изменение IV")
    
    messages, assocdata, key, nonce = load_test_data(filepath)
    single_assocdata = assocdata[0]
    
    eax = EAXCFB()
    packets = eax.eax_cfb(single_assocdata, messages, key, nonce, "send")
    
    if not packets:
        print("Нет пакетов")
        return
    
    original = packets[0]
    
    # Определяем позицию IV в пакете
    # Заголовок: тип(2) + отправитель(8) + получатель(8) + сеанс(9) + длина(4) = 31 символ
    # 31 символ * 5 = 155 бит, но в битовом массиве всё упаковано подряд
    # Проще: IV идёт после заголовка. Заголовок в битах ~ 160-200
    iv_start = 200
    iv_end = min(iv_start + 80, len(original))
    
    print(f"IV позиция: биты {iv_start}-{iv_end}")
    
    # Модифицируем IV
    corrupted = original[:]
    for i in range(iv_start, min(iv_start + 8, iv_end)):
        corrupted[i] ^= 1
    
    print("IV изменён")
    
    oracle = SingleOracle(single_assocdata, key, nonce)
    success, msg = oracle.decrypt(corrupted)
    
    if success:
        print(f"УЯЗВИМОСТЬ: пакет с изменённым IV принят!")
    else:
        print("Защита сработала: пакет отвергнут")



def test_replay_attack():
    print("\nАтака 3: Replay-атака")
    
    messages, assocdata, key, nonce = load_test_data(filepath)
    single_assocdata = assocdata[0]
    
    eax = EAXCFB()
    
    # Отправляем первое сообщение
    packets = eax.eax_cfb(single_assocdata, messages[:1], key, nonce, "send")
    
    if not packets:
        print("Нет пакетов")
        return
    
    first_packet = packets[0]
    oracle = SingleOracle(single_assocdata, key, nonce)
    
    # Первый раз — должно пройти
    success1, msg1 = oracle.decrypt(first_packet)
    print(f"Первая отправка: {'принято' if success1 else 'отклонено'}")
    
    # Второй раз — должно быть отклонено из-за счётчика
    success2, msg2 = oracle.decrypt(first_packet)
    print(f"Replay: {'УЯЗВИМОСТЬ (принято повторно)' if success2 else 'защита (отклонено)'}")