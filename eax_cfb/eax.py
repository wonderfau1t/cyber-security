from eax_cfb.cfb import CFBCipher
from eax_cfb.packet_handler import PacketHandler
from core.utils import add_txt, num_to_block, block_to_num
from core.produce_round_keys import produce_round_keys

class EAXCFB:
    """EAX-CFB режим"""

    def __init__(self):
        self.cfb = CFBCipher()
        self.packet_handler = PacketHandler()

    def eax_cfb_frw(
        self, packet_in: list, cmac_in: str, key_in: str, sec_in: str, onlymac: int
    ) -> list:
        """Прямой EAX-CFB"""
        assdata_in, iv_in, msg_in, tmp = packet_in
        tmp = assdata_in[0] + assdata_in[3] + assdata_in[4]
        civ = self.cfb.frw_cfb(sec_in + tmp, iv_in, key_in, -1)

        if onlymac == 1:
            tmp = self.cfb.frw_cfb(msg_in, civ, key_in, -1)
            mac = self.cfb._textxor(self.cfb._textxor(tmp, civ), cmac_in)
            msg = msg_in
        else:
            tmp = self.cfb.frw_cfb(msg_in, civ, key_in, 1)
            m = tmp[len(msg_in) : len(msg_in) + 16]
            mac = self.cfb._textxor(self.cfb._textxor(m, civ), cmac_in)
            msg = tmp[0 : len(msg_in)]

        return [assdata_in, iv_in, msg, mac]

    def eax_cfb_inv(self, packet_in: list, key_in: str, sec_in: str, onlymac: int) -> list:
        """Обратный EAX-CFB"""
        ad_in, iv_in, msg_in, mac_in = packet_in
        tmp = ad_in[0] + ad_in[3] + ad_in[4]
        data = ad_in[0] + ad_in[1] + ad_in[2] + ad_in[3] + "_____"
        cmac = self.cfb.frw_cfb(data, sec_in, key_in, -1)
        civ = self.cfb.frw_cfb(sec_in + tmp, iv_in, key_in, -1)

        if onlymac == 1:
            tmp = self.cfb.frw_cfb(msg_in, civ, key_in, -1)
            mac = self.cfb._textxor(mac_in, self.cfb._textxor(self.cfb._textxor(tmp, civ), cmac))
            msg = msg_in
        else:
            cont = self.cfb._textxor(self.cfb._textxor(mac_in, civ), cmac)
            tmp = self.cfb.inv_cfb(msg_in + cont, civ, key_in, 1)
            m = tmp[len(msg_in) : len(msg_in) + 16]
            mac = m
            msg = tmp[0 : len(msg_in)]

        return [ad_in, iv_in, msg, mac]

    def eax_cfb(
        self, ass_data: list, msg_array: list, key_in: str, nonce: str, type_val: str
    ) -> list:
        """Основная функция EAX-CFB"""
        mtype, sender, receiver, transmission = ass_data
        t1 = receiver + sender
        t2 = mtype + transmission + "_____"
        cad = add_txt(t1, t2)
        iv0 = add_txt(add_txt(t1, t2), nonce)[:12]

        if receiver < sender:
            t3 = t1
        else:
            t3 = sender + receiver

        msg_counter = -1
        keyset = produce_round_keys(key_in, 8)
        secret = self.cfb.frw_cfb(t3 + t2, key_in, keyset, -1)
        data = mtype + sender + receiver + transmission + "_____"
        data_mac = self.cfb.frw_cfb(data, secret, keyset, -1)

        out = []

        if type_val == "send":
            for i in range(len(msg_array)):
                msg_sec = mtype
                msg_counter += 1
                iv = iv0 + num_to_block(msg_counter)
                tmp_packet = self.packet_handler.prepare_packet(
                    [msg_sec, sender, receiver, transmission], iv, msg_array[i]
                )

                if msg_sec == "В_":
                    out.append(self.packet_handler.transmit(tmp_packet))
                elif msg_sec == "ВА":
                    sec_packet = self.eax_cfb_frw(tmp_packet, data_mac, keyset, secret, 1)
                    out.append(self.packet_handler.transmit(sec_packet))
                elif msg_sec == "ВБ":
                    sec_packet = self.eax_cfb_frw(tmp_packet, data_mac, keyset, secret, 0)
                    out.append(self.packet_handler.transmit(sec_packet))

        elif type_val == "receive":
            last = -1
            for i in range(len(msg_array)):
                tmp_packet = self.packet_handler.receive(msg_array[i])
                rdata = tmp_packet[0]
                current = block_to_num(tmp_packet[1][12:16])

                if current > last:
                    if rdata[0] == "ВБ":
                        rec_packet = self.eax_cfb_inv(tmp_packet, keyset, secret, 0)
                        rec_packet[2] = self.packet_handler.padder.unpad_message(rec_packet[2])
                        if rec_packet[3] == "________________":
                            last = current
                            rec_packet[3] = "ОК"
                    elif (rdata[0] == "ВА") and (mtype != "ВБ"):
                        rec_packet = self.eax_cfb_inv(tmp_packet, keyset, secret, 1)
                        rec_packet[2] = self.packet_handler.padder.unpad_message(rec_packet[2])
                        if rec_packet[3] == "________________":
                            last = current
                            rec_packet[3] = "ОК"
                    elif (rdata[0] == "В_") and (mtype == "В_"):
                        rec_packet = tmp_packet
                        rec_packet[2] = self.packet_handler.padder.unpad_message(rec_packet[2])
                        if rec_packet[3] == "":
                            last = current
                            rec_packet[3] = "N/A"
                    else:
                        rec_packet = tmp_packet

                    out.append(rec_packet)

        return out
