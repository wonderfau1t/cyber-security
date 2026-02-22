from utils import add_txt, ascii_to_text, reverse_str, sub_txt, text_to_ascii


def blocks_mix(in1: str, in2: str) -> list[str]:
    in1 = reverse_str(in1)
    return [add_txt(in1, in2), sub_txt(in1, in2)]


def block_mask(IN: str, CONST: str) -> str:
    arr = text_to_ascii(IN)
    con = text_to_ascii(CONST)
    result = [0] * 16
    for i in range(16):
        if arr[i] < (con[i] + i):
            result[i] = (64 - (con[i] - i)) % 32
        else:
            result[i] = (arr[i] + i) % 32
    return ascii_to_text(result)
