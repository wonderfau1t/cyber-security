from utils import text_to_ascii, ascii_to_text


class SBlockEnchanser:
    @staticmethod
    def merge_block(block: str, key: str) -> str:
        M = [0, 1, 2, 3]
        key_array = text_to_ascii(key)
        _sum = 0

        for i, num in enumerate(key_array):
            _sum = (24 + _sum + (-1) ** i * num) % 24

        for k in range(3):
            t = _sum % (4 - k)
            _sum = (_sum - t) / (4 - k)
            M[k], M[k + int(t)] = M[k + int(t)], M[k]

        block_array = text_to_ascii(block)

        for i in range(4):
            b = M[(1 + i) % 4]
            a = M[i % 4]
            block_array[b] = (block_array[b] + block_array[a]) % 32

        return ascii_to_text(block_array)

    @staticmethod
    def inverse_merge_block(block: str, key: str) -> str:
        M = [0, 1, 2, 3]
        key_array = text_to_ascii(key)
        _sum = 0

        for i, num in enumerate(key_array):
            _sum = (24 + _sum + (-1) ** i * num) % 24

        for k in range(3):
            t = _sum % (4 - k)
            _sum = (_sum - t) / (4 - k)
            M[k], M[k + int(t)] = M[k + int(t)], M[k]

        block_array = text_to_ascii(block)

        for i in range(3, -1, -1):
            b = M[(1 + i) % 4]
            a = M[i % 4]
            block_array[b] = (32 + block_array[b] - block_array[a]) % 32

        return ascii_to_text(block_array)
