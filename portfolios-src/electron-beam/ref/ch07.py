"""Chapter 7 reference: line profile, shot noise, edge algorithm, CD precision and throughput; mirrors physics/ch07.js line by line
(see its header for the model)."""
import math

from .core import C
from .ch06 import rng

INPUTS = ['d_p', 'I_p', 't_d', 'N_px', 'eta_c', 'cd', 'pitch', 'height', 'sidewall', 'px', 't_ov', 'delta_SE', 'eta_BSE', 'sigma_sig']
OUTPUTS = ['SNR', 'sigma_CD', 'MPH', 'CD_meas', 'sigma_CD_mc', 'dose', 'n_pe', 'prof_curve']
SEED, NMC = 7072026, 4000


def erf(x):
    s = -1 if x < 0 else 1
    a = abs(x)
    t = 1 / (1 + 0.3275911 * a)
    y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * math.exp(-a * a)
    return s * y


def Phi(u):
    return 0.5 * (1 + erf(u / math.sqrt(2)))


def yieldAt(x, p, sb):
    w = p['height'] * math.tan(p['sidewall'])
    dens = p['delta_SE'] * p['height'] * (1 / math.cos(p['sidewall']) - math.tan(p['sidewall']))
    Y = p['delta_SE'] + p['eta_BSE']
    K = min(50, 2 + math.ceil(5 * sb / p['pitch']))
    for k in range(-K, K + 1):
        c = k * p['pitch']
        for a, b in ((c - (p['cd'] + w) / 2, c - (p['cd'] - w) / 2), (c + (p['cd'] - w) / 2, c + (p['cd'] + w) / 2)):
            if b - a < 1e-6 * sb:
                Y += dens * math.exp(-0.5 * ((x - 0.5 * (a + b)) / sb) ** 2) / (sb * math.sqrt(2 * math.pi))
            else:
                Y += dens / (b - a) * (Phi((x - a) / sb) - Phi((x - b) / sb))
    return Y


def setup(p):
    n = max(8, math.floor(p['pitch'] / p['px'] + 0.5))           # Math.round: halves go up
    dx = p['pitch'] / n
    sp = p['d_p'] / (2 * math.sqrt(2 * math.log(2)))
    sb = math.sqrt(sp * sp + p['sigma_sig'] * p['sigma_sig'])
    nbar = p['I_p'] * p['t_d'] / C['e']
    x, mean, var = [], [], []
    for i in range(n):
        xi = -p['pitch'] / 2 + (i + 0.5) * dx
        m = p['eta_c'] * yieldAt(xi, p, sb)
        x.append(xi)
        mean.append(nbar * m)
        var.append(nbar * (m + m * m))
    return dict(n=n, dx=dx, sb=sb, nbar=nbar, x=x, mean=mean, varLine=var)


def edges(S, x, p):
    n = len(S)
    q = (p['pitch'] - p['cd']) / 4
    bs, nb = 0.0, 0
    for i in range(n):
        if abs(x[i]) >= p['pitch'] / 2 - q:
            bs += S[i]
            nb += 1
    if not nb:
        return None
    b = bs / nb
    half = n // 2

    def side(lo, hi, d):
        im = lo
        for i in range(lo, hi):
            if S[i] > S[im]:
                im = i
        pk = (S[max(im - 1, 0)] + S[im] + S[min(im + 1, n - 1)]) / 3
        T = 0.5 * (b + pk)
        i = im
        while 0 <= i + d < n:
            j = i + d
            if S[j] < T:
                f = (S[i] - T) / (S[i] - S[j])
                return x[i] + f * (x[j] - x[i])
            i += d
        return None
    xL, xR = side(0, half, -1), side(half, n, 1)
    return None if xL is None or xR is None else [xL, xR]


def compute(p):
    if not p['height'] > 0:
        raise ValueError('a line of zero height has no walls')
    st = setup(p)
    N = p['N_px']
    e0 = edges(st['mean'], st['x'], p)
    if not e0:
        raise ValueError('the edge algorithm finds no edges')
    if max(st['mean']) - min(st['mean']) < 0.05 * min(st['mean']):
        raise ValueError('the edges are blurred away')
    cd0 = e0[1] - e0[0]
    v = 0.0
    S = list(st['mean'])
    for i in range(st['n']):
        h = 1e-6 * max(1e-30, abs(S[i])) + 1e-12
        S[i] += h
        e1 = edges(S, st['x'], p)
        S[i] -= h
        g = ((e1[1] - e1[0]) - cd0) / h if e1 else 0.0
        v += g * g * st['varLine'][i] / N
    rnd = rng(SEED)
    sd = [math.sqrt(z / N) for z in st['varLine']]
    s1 = s2 = 0.0
    ok = 0
    noisy = [0.0] * st['n']
    avgShown, lineShown = [], []
    for r in range(NMC):
        for i in range(st['n']):
            u1 = 1 - rnd()
            u2 = rnd()
            noisy[i] = st['mean'][i] + sd[i] * math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        if r == 0:
            avgShown = list(noisy)
        e = edges(noisy, st['x'], p)
        if e:
            c = e[1] - e[0]
            s1 += c
            s2 += c * c
            ok += 1
    mc = math.sqrt(max(0.0, (s2 - s1 * s1 / ok) / (ok - 1))) if ok > 1 else float('nan')
    for i in range(st['n']):
        u1 = 1 - rnd()
        u2 = rnd()
        lineShown.append(st['mean'][i] + math.sqrt(st['varLine'][i]) * math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2))
    ib = 0
    for i in range(st['n']):
        if abs(st['x'][i]) > abs(st['x'][ib]):
            ib = i
    ip = 0
    for i in range(st['n']):
        if st['mean'][i] > st['mean'][ip]:
            ip = i
    snr = (st['mean'][ip] - st['mean'][ib]) / math.sqrt(st['varLine'][ib])
    curve = []
    for i in range(st['n']):
        curve += [st['x'][i], st['mean'][i], lineShown[i], avgShown[i]]
    tSite = N * N * p['t_d'] + p['t_ov']
    return dict(SNR=snr, sigma_CD=math.sqrt(v), MPH=1 / tSite, CD_meas=cd0, sigma_CD_mc=mc, dose=p['I_p'] * p['t_d'] / (p['px'] * p['px']),
                n_pe=st['nbar'], prof_curve=curve)
