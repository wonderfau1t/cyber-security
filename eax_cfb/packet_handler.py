from eax_cfb.message_padder import MessagePadder
from core.utils import add_txt, ascii_to_symbol, bin2msg, msg2bin, symbol_to_ascii


class PacketHandler:
    """Класс для обработки пакетов"""

    def __init__(self):
        self.padder = MessagePadder()

    def prepare_packet(self, data_in: list, iv_in: str, msg_in: str) -> list:
        data = data_in
        iv = add_txt("________________", iv_in)
        msg = self.padder.pad_message(msg_in)
        L = len(msg2bin(msg))
        a = ""
        for i in range(5):
            a = ascii_to_symbol(L % 32) + a
            L = L // 32
        data.append(a)
        mac = ""
        return [data, iv, msg, mac]

    def validate_packet(self, packet_in: list) -> int:
        [data, iv, msg, mac] = packet_in
        f = 1
        t = data[0][0:1]
        s = data[0][1:2]
        ml = len(mac)
        if t != "В":
            f = 0
        elif ((s == "А") or (s == "Б")) and (ml != 16):
            f = 0
        elif (s == "_") and (ml != 0):
            f = 0
        return f

    def transmit(self, packet_in: list) -> list:
        [data, iv, msg, mac] = packet_in
        out = data[0] + data[1] + data[2] + data[3] + data[4]
        out = msg2bin(out + iv + msg + mac)
        return out

    def receive(self, stream_in: list) -> list:
        p = bin2msg(stream_in)
        M = len(p)
        type = p[0:2]
        sender = p[2:10]
        reciever = p[10:18]
        session = p[18:27]
        length = p[27:32]
        iv = p[32:48]
        L = 0
        for i in range(5):
            t = length[i : i + 1]
            l = symbol_to_ascii(t)
            L = 32 * L + l
        L = L // 5
        message = p[48 : 48 + L]
        mac = p[48 + L : 48 + L + M - (48 + L)]
        return [[type, sender, reciever, session, length], iv, message, mac]
