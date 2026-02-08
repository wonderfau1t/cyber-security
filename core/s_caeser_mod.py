from s_block_enchancer import SBlockEnchanser
from s_caeser import SCaeser


class SCaeserMod:
    @staticmethod
    def encrypt(block: str, key: str):
        tmp = SBlockEnchanser.merge_block(block, key)
        tmp = SCaeser.encrypt(tmp, key)
        return SBlockEnchanser.merge_block(tmp, key)

    @staticmethod
    def decrypt(block: str, key: str):
        tmp = SBlockEnchanser.inverse_merge_block(block, key)
        tmp = SCaeser.decrypt(tmp, key)
        return SBlockEnchanser.inverse_merge_block(tmp, key)
