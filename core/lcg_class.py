from init_prng import init_prng
from utils import compose_num, num_to_block, seed_to_nums


class LCG:
    def __init__(self, seed_in, set_in):
        self.seed_in = seed_in
        self.set_in = set_in
        self.state = []

        INIT = init_prng(seed_in)
        for i in range(4):
            self.state.append(
                seed_to_nums(
                    [
                        INIT[i][:4],
                        INIT[i][4 : 4 + 4],
                        INIT[i][8 : 8 + 4],
                    ]
                )
            )

    def next(self):
        stream = ""
        state = [row[:] for row in self.state]

        for j in range(4):
            tmp = 0
            sign = 1
            for i in range(4):
                T = ct_lcg_next(state[i], self.set_in[j])
                state[i] = T[1]
                tmp = (1048576 + sign * T[0] + tmp) % 1048576
                sign = -sign
            stream += num_to_block(tmp)

        self.state = state

        return [stream, state]


def ct_lcg_next(STATE_IN, SET_IN):
    first = lcg_next(STATE_IN[0], SET_IN[0])
    second = lcg_next(STATE_IN[1], SET_IN[1])
    control = lcg_next(STATE_IN[2], SET_IN[2])
    out = compose_num(first, second, control)
    STATE_OUT = [first, second, control]
    return [out, STATE_OUT]


def lcg_next(state_in, COEFFS_IN):
    a, c, m = COEFFS_IN
    return (a * state_in + c) % m
