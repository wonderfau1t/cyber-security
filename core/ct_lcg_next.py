from compose_num import compose_num
from lcg_next import lcg_next


def ct_lcg_next(STATE_IN, SET_IN):
    first = lcg_next(STATE_IN[0], SET_IN[0])
    second = lcg_next(STATE_IN[1], SET_IN[1])
    control = lcg_next(STATE_IN[2], SET_IN[2])
    out = compose_num(first, second, control)
    STATE_OUT = [first, second, control]
    return [out, STATE_OUT]
