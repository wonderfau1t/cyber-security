def make_coeffs(BPR_IN, SPR_IN, pow_in):
    ss = min(SPR_IN)
    bs = min(BPR_IN)
    bb = max(BPR_IN)
    sb = max(SPR_IN)
    max_ = 2**pow_in - 1
    tmp = bs * ss
    a = ss * bs * sb + 1
    c = bb
    for i in range(pow_in + 1):
        if tmp * ss >= max_:
            break
        else:
            tmp = tmp * ss
    m = tmp
    if (a < m) and (c < m):
        out = [a, c, m]
    else:
        out = "wrong_guess"
    return out
