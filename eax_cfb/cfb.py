from core.feistel import frw as frw_Feistel
from core.utils import bin_to_dec, block_to_num, dec_to_bin, num_to_block


class CFBCipher:
    """CFB режим шифрования"""

    def _textxor(self, a_in: str, b_in: str) -> str:
        out = ""
        for i in range(4):
            a = a_in[i * 4 : i * 4 + 4]
            b = b_in[i * 4 : i * 4 + 4]
            A = dec_to_bin(block_to_num(a))
            B = dec_to_bin(block_to_num(b))
            C = [(A[j] + B[j]) % 2 for j in range(20)]
            c = bin_to_dec(C)
            out += num_to_block(c)
        return out

    def frw_cfb(self, msg_in: str, iv_in: str, key_in: str, mac_in: int) -> str:
        R = 6
        m = len(msg_in) // 16
        feedback = iv_in
        out = ""
        cont = "________________"

        for i in range(m):
            inp = msg_in[i * 16 : (i + 1) * 16]
            cont = self._textxor(inp, cont)
            keystream = frw_Feistel(feedback, key_in, R)
            feedback = self._textxor(inp, keystream)
            out += feedback

        keystream = frw_Feistel(feedback, key_in, R)
        mac = self._textxor(cont, keystream)

        if mac_in == 1:
            out += mac
        elif mac_in == -1:
            out = mac

        return out

    def inv_cfb(self, msg_in: str, iv_in: str, key_in: str, mac_in: int) -> str:
        R = 6
        m = len(msg_in) // 16
        feedback = iv_in
        out = ""
        cont = "________________"

        for i in range(m - mac_in):
            inp = msg_in[i * 16 : (i + 1) * 16]
            keystream = frw_Feistel(feedback, key_in, R)
            feedback = inp
            text = self._textxor(inp, keystream)
            cont = self._textxor(cont, text)
            out += text

        if mac_in != 0:
            mac = msg_in[(m - 1) * 16 : (m - 1) * 16 + 16]
            keystream = frw_Feistel(feedback, key_in, R)
            text = self._textxor(mac, keystream)
            cont = self._textxor(cont, text)

            if mac_in == 1:
                out += cont
            else:
                out = cont

        return out
