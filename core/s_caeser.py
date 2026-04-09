from core.poly_caeser import PolyCaeser
from core.utils import add_txt, ascii_to_text, text_to_ascii

C = [1, -1, 1, 2, -2, 1, 1, 3, -1, 2]


class SCaeser:
    @staticmethod
    def encrypt(text_to_encrypt: str, secret_key: str) -> str:
        encoded_str = text_to_encrypt
        key_tmp = "___"
        extended_key = secret_key * 2

        for i in range(7 + 1):
            s_tmp = extended_key[i * 2 : i * 2 + 4]
            b_tmp = text_to_ascii(s_tmp)

            a_tmp = [0 for i in range(4)]
            for k in range(3 + 1):
                x = (2 * i + k) % 10
                a_tmp[k] = (64 + k + C[x] * b_tmp[k]) % 32

            key_tmp = add_txt(key_tmp, ascii_to_text(a_tmp))

        encoded_str = PolyCaeser.encrypt(text_to_encrypt, key_tmp)

        return encoded_str

    @staticmethod
    def decrypt(text_to_decrypt: str, secret_key: str) -> str:
        decoded_str = text_to_decrypt
        key_tmp = "___"
        extended_key = secret_key * 2

        for i in range(7 + 1):
            s_tmp = extended_key[i * 2 : i * 2 + 4]
            b_tmp = text_to_ascii(s_tmp)

            a_tmp = [0 for i in range(4)]
            for k in range(3 + 1):
                x = (2 * i + k) % 10
                a_tmp[k] = (64 + k + C[x] * b_tmp[k]) % 32

            key_tmp = add_txt(key_tmp, ascii_to_text(a_tmp))

        decoded_str = PolyCaeser.decrypt(decoded_str, key_tmp)

        return decoded_str
