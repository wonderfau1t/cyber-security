from utils import add_s, sub_s


class PolyCaeser:
    @staticmethod
    def encrypt(text_to_encrypt: str, secret_key: str) -> str:
        encoded_str = ""
        t_k = "_"
        k = len(secret_key)

        for i in range(len(text_to_encrypt)):
            t_i = text_to_encrypt[i]
            q = i % k
            t_k = add_s(t_k, secret_key[q])
            encoded_str += add_s(t_i, t_k)

        return encoded_str

    @staticmethod
    def decrypt(text_to_decrypt: str, secret_key: str) -> str:
        decoded_str = ""
        t_k = "_"
        k = len(secret_key)

        for i in range(len(text_to_decrypt)):
            t_i = text_to_decrypt[i]
            q = i % k
            t_k = add_s(t_k, secret_key[q])
            decoded_str += sub_s(t_i, t_k)

        return decoded_str
