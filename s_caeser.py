from poly_caeser import PolyCaeser
from utils import add_txt, ascii_to_text, text_to_ascii

C = [1, -1, 1, 2, -2, 1, 1, 3, -1, 2]


class SCaeser:
    @staticmethod
    def encode(text_to_encode: str, secret_key: str) -> str:
        """
        Функиця для кодировки шифром Цезаря

        :param message_in: Текст для кодировки (длина = 4)
        :type message_in: str
        :param key_in: Ключ для шфирования (длина = 16)
        :type key_in: str
        :return: Зашифрованное сообщение
        :rtype: str
        """
        encoded_str = text_to_encode
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

        encoded_str = PolyCaeser.encode(text_to_encode, key_tmp)

        return encoded_str

    @staticmethod
    def decode(text_to_decode: str, secret_key: str) -> str:
        """
        Docstring for decode

        :param text_to_decode: Description
        :type text_to_decode: str
        :param secret_key: Description
        :type secret_key: str
        :return: Description
        :rtype: str
        """
        decoded_str = text_to_decode
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

        decoded_str = PolyCaeser.decode(decoded_str, key_tmp)

        return decoded_str
