from ct_lcg_next import ct_lcg_next
from init_prng import init_prng
from utils import num_to_block, seed_to_nums


def c_ct_lcg_next(init_flag, STATE_IN, SEED_IN, SET_IN):
    result = "something wrong"
    stream = ""
    state = []
    check = False
    if init_flag == "up":
        INIT = init_prng(SEED_IN)
        for i in range(4):
            state.append(
                seed_to_nums(
                    [
                        INIT[i][:4],
                        INIT[i][4 : 4 + 4],
                        INIT[i][8 : 8 + 4],
                    ]
                )
            )
        check = True
    elif init_flag == "down":
        state = STATE_IN
        check = True
    if check:
        for j in range(4):
            tmp = 0
            sign = 1
            for i in range(4):
                T = ct_lcg_next(state[i], SET_IN[j])
                state[i] = T[1]
                tmp = (1048576 + sign * T[0] + tmp) % 1048576
                sign = -sign
            stream += num_to_block(tmp)
        result = [stream, state]
    return result
