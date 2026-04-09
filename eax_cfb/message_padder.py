from core.utils import bin2msg, msg2bin


class MessagePadder:
    """Класс для дополнения сообщений"""

    def _check_padding(self, binmsg_in: list) -> list:
        bins = binmsg_in
        M = len(bins)

        if M % 80 != 0:
            return [0, [0, 0]]

        blocks = M // 80

        # последние 20 бит
        tb = bins[M - 20 : M]

        PL = tb[0:7]  # pad length (7 бит)
        NB = tb[7:17]  # num blocks (10 бит)
        ender = tb[17:20]  # последние 3 бита

        # проверка маркера конца
        if ender != [0, 0, 1]:
            return [0, [0, 0]]

        # декодируем числа
        padlength = 0
        for bit in PL:
            padlength = (padlength << 1) | bit

        numblocks = 0
        for bit in NB:
            numblocks = (numblocks << 1) | bit

        # проверки
        if numblocks != blocks or not (23 <= padlength < 103):
            return [0, [0, 0]]

        if padlength > M:
            return [0, [0, 0]]

        # проверка паддинга
        pad = bins[M - padlength : M - 20]

        if len(pad) == 0 or pad[0] != 1:
            return [0, [0, 0]]

        # все остальные должны быть 0
        for bit in pad[1:]:
            if bit != 0:
                return [0, [0, 0]]

        return [1, [numblocks, padlength]]

    def _produce_padding(self, rem_in: int, blocks_in: int) -> list:
        """Генерация дополнения"""
        if rem_in == 0:
            b = blocks_in + 1
            r = 80
        elif rem_in <= 57:
            r = 80 - rem_in
            b = blocks_in + 1
        else:
            b = blocks_in + 2
            r = 160 - rem_in

        pad = [0] * r
        pad[0] = 1

        rt = r
        for i in range(6, -1, -1):
            pad[r - 20 + i] = rt % 2
            rt = rt // 2

        for i in range(9, -1, -1):
            pad[r - 13 + i] = b % 2
            b = b // 2

        pad[r - 3] = 0
        pad[r - 2] = 0
        pad[r - 1] = 1

        return pad

    def pad_message(self, msg_in: str) -> str:
        """Дополнение сообщения"""
        bins = msg2bin(msg_in)
        M = len(bins)
        blocks = M // 80
        remainder = M % 80

        if remainder == 0:
            f = self._check_padding(bins)[0]
        else:
            f = 1

        if f == 1:
            pad = self._produce_padding(remainder, blocks)
            bins.extend(pad)

        return bin2msg(bins)

    def unpad_message(self, msg_in: str) -> str:
        """Удаление дополнения"""
        bins = msg2bin(msg_in)
        T = self._check_padding(bins)
        M = len(bins)
        if T[0] == 1:
            pl = T[1][1]
            tmp = bins[: M - pl] if M - pl > 0 else []
            out = bin2msg(tmp)
        else:
            out = msg_in

        return out
