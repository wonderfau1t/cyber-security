def lcg_next(state_in, COEFFS_IN):
    a, c, m = COEFFS_IN
    return (a * state_in + c) % m


SET1 = [723482, 867, 983609]

