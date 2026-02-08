from utils import add_s, sub_s


class PolyCaeser:
    @staticmethod
    def encode(text_to_encode: str, secret_key: str) -> str:
        encoded_str = ""
        t_k = "_"
        k = len(secret_key)

        for i in range(len(text_to_encode)):
            t_i = text_to_encode[i]
            q = i % k
            print(q)
            t_k = add_s(t_k, secret_key[q])
            encoded_str += add_s(t_i, t_k)

        return encoded_str

    @staticmethod
    def decode(text_to_decode: str, secret_key: str) -> str:
        decoded_str = ""
        t_k = "_"
        k = len(secret_key)

        for i in range(len(text_to_decode)):
            t_i = text_to_decode[i]
            q = i % k
            t_k = add_s(t_k, secret_key[q])
            decoded_str += sub_s(t_i, t_k)

        return decoded_str
