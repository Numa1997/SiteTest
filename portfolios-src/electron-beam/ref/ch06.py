"""Chapter 6 reference: single-scattering Monte Carlo of electrons in a solid; mirrors physics/ch06.js line by line (see its header for the
physics and the sources). Same random numbers: mulberry32 with one generator per electron."""
import math

from .core import C

INPUTS = ['V_land', 'material']
OUTPUTS = ['E_land', 'delta_SE', 'eta_BSE', 'R', 'V_int', 'sigma_sig', 'sig_core', 'f_core', 'sig_halo', 'u_eta', 'u_delta', 'r90', 'mc_paths']
NA = C['N_A']
SEED, NEL, EMIN, NPATH, NBIN, NH = 20261109, 2000, 0.05, 40, 4000, 400
MAT = {
    'Si': dict(Z=14, A=28.0855, rho=2.33, eps=90, ls=2.7),
    'Al': dict(Z=13, A=26.9815, rho=2.6989, eps=32, ls=1.7),
    'Cu': dict(Z=29, A=63.546, rho=8.96, eps=35, ls=0.6),
    'Au': dict(Z=79, A=196.967, rho=19.32, eps=35, ls=0.5),
}


def rng(seed):
    """mulberry32, as core.rng in physics/core.js (32-bit unsigned arithmetic)."""
    a = [seed & 0xFFFFFFFF]

    def imul(x, y):
        return (x * y) & 0xFFFFFFFF

    def nxt():
        a[0] = (a[0] + 0x6D2B79F5) & 0xFFFFFFFF
        t = a[0]
        t = imul(t ^ (t >> 15), t | 1)
        t ^= (t + imul(t ^ (t >> 7), t | 61)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt


def Jkev(Z):
    return (9.76 * Z + 58.5 * Z ** -0.19) * 1e-3


def screen(Z, E):
    return 3.4e-3 * Z ** 0.67 / E


def mfp(m, E):
    a = screen(m['Z'], E)
    r = (E + 511) / (E + 1024)
    sig = 5.21e-21 * (m['Z'] * m['Z']) / (E * E) * 4 * math.pi / (a * (1 + a)) * r * r
    return m['A'] / (NA * m['rho'] * sig) * 1e7


def stop(m, E, J):
    return 78500 * m['rho'] * m['Z'] / (m['A'] * E) * math.log(1.166 * (E + 0.85 * J) / J) * 1e-7


def rangeKO(m, E):
    return 27.6 * m['A'] * E ** 1.67 / (m['Z'] ** 0.89 * m['rho'])


def escInt(zA, zB, s, ls):
    dz = zB - zA
    if abs(dz) < 1e-6 * ls:
        return s * math.exp(-0.5 * (zA + zB) / ls)
    return s * ls / dz * (math.exp(-zA / ls) - math.exp(-zB / ls))


def turn(c, phi, psi):
    cp, sp, cs, ss = math.cos(phi), math.sin(phi), math.cos(psi), math.sin(psi)
    cx, cy, cz = c
    e1 = [0.0, cz, -cy] if abs(cx) < 0.6 else [-cz, 0.0, cx]
    l1 = math.sqrt(e1[0] * e1[0] + e1[1] * e1[1] + e1[2] * e1[2])
    e1 = [e1[0] / l1, e1[1] / l1, e1[2] / l1]
    e2 = [cy * e1[2] - cz * e1[1], cz * e1[0] - cx * e1[2], cx * e1[1] - cy * e1[0]]
    n = [c[k] * cp + sp * (e1[k] * cs + e2[k] * ss) for k in range(3)]
    l = math.sqrt(n[0] * n[0] + n[1] * n[1] + n[2] * n[2])
    return [n[0] / l, n[1] / l, n[2] / l]


def run(p, N=None):
    m = MAT[p['material']]
    E0 = p['V_land'] * 1e-3
    J = Jkev(m['Z'])
    R = rangeKO(m, E0)
    N = N or NEL
    binW = 3 * R / NBIN
    hist = [0.0] * NBIN
    nBS, seSum, seSq, wx2, wTot, depTot = 0, 0.0, 0.0, 0.0, 0.0, 0.0
    paths = []
    hW, hQ = [0.0] * NH, [0.0] * NH

    def hbin(ax):
        return 0 if ax <= 1e-3 else min(NH - 1, math.floor((math.log10(ax) + 3) / 8 * NH))
    for i in range(N):
        rnd = rng(SEED + 7919 * i)
        x = y = z = 0.0
        c = [0.0, 0.0, 1.0]
        E, se, bs = E0, 0.0, False
        rec = [0, 0] if i < NPATH else None
        guard = 0
        while guard < 200000:
            guard += 1
            lam, S = mfp(m, E), stop(m, E, J)
            s = -lam * math.log(1 - rnd())
            zn = z + c[2] * s
            ext = False
            if zn < 0:
                s = -z / c[2]
                zn = 0.0
                ext = True
            dead = False
            if S * s >= E - EMIN:
                s = (E - EMIN) / S
                zn = z + c[2] * s
                dead, ext = True, False
            xn, yn = x + c[0] * s, y + c[1] * s
            if min(z, zn) < 12 * m['ls']:
                n_p = min(200, max(1, math.ceil(s / (0.5 * m['ls']))))
                for k in range(n_p):
                    u0, u1 = s * k / n_p, s * (k + 1) / n_p
                    um = 0.5 * (u0 + u1)
                    wk = 0.5 * S / (m['eps'] * 1e-3) * escInt(z + c[2] * u0, z + c[2] * u1, u1 - u0, m['ls'])
                    xm = x + c[0] * um
                    se += wk
                    wx2 += wk * xm * xm
                    wTot += wk
                    hb = hbin(abs(xm))
                    hW[hb] += wk
                    hQ[hb] += wk * xm * xm
            dE = S * s
            mx, my, mz = 0.5 * (x + xn), 0.5 * (y + yn), 0.5 * (z + zn)
            rm = math.sqrt(mx * mx + my * my + mz * mz)
            hist[min(NBIN - 1, math.floor(rm / binW))] += dE
            depTot += dE
            x, y, z = xn, yn, zn
            E -= dE
            if rec is not None:
                rec += [x, z]
            if ext:
                bs = E > EMIN
                break
            if dead:
                break
            a = screen(m['Z'], E)
            r2 = rnd()
            cphi = 1 - 2 * a * r2 / (1 + a - r2)
            c = turn(c, math.acos(max(-1.0, min(1.0, cphi))), 2 * math.pi * rnd())
        if bs:
            nBS += 1
        seSum += se
        seSq += se * se
        if rec is not None:
            rec[0] = (len(rec) - 2) // 2
            rec[1] = 1 if bs else 0
            paths += rec
    eta, delta = nBS / N, seSum / N
    uDelta = math.sqrt(max(0.0, seSq / N - delta * delta) / N)
    def edge(b):
        return 10 ** (b * 8 / NH - 3)
    cw, x50 = 0.0, 0.0
    for b in range(NH):
        if cw + hW[b] >= 0.5 * wTot:
            f = (0.5 * wTot - cw) / hW[b]
            x50 = edge(b) * (edge(b + 1) / edge(b)) ** f
            break
        cw += hW[b]
    sCore = x50 / 0.67449
    cut = 3 * sCore
    wIn = qIn = 0.0
    for b in range(NH):
        lo, hi = edge(b), edge(b + 1)
        fr = 1.0 if hi <= cut else (0.0 if lo >= cut else math.log(cut / lo) / math.log(hi / lo))
        wIn += fr * hW[b]
        qIn += fr * hQ[b]
    fCore = wIn / wTot
    sHalo = math.sqrt((wx2 - qIn) / (wTot - wIn)) if wTot - wIn > 0 else sCore
    acc, r90 = 0.0, 3 * R
    for b in range(NBIN):
        if acc + hist[b] >= 0.9 * depTot:
            r90 = (b + (0.9 * depTot - acc) / hist[b]) * binW
            break
        acc += hist[b]
    return dict(E_land=p['V_land'] * C['e'], delta_SE=delta, eta_BSE=eta, R=R * 1e-9, V_int=2 / 3 * math.pi * (r90 * 1e-9) ** 3,
                sigma_sig=math.sqrt(wx2 / wTot) * 1e-9, sig_core=sCore * 1e-9, f_core=fCore, sig_halo=max(sHalo, sCore) * 1e-9, u_eta=math.sqrt(eta * (1 - eta) / N), u_delta=uDelta, r90=r90 * 1e-9, mc_paths=paths)


def compute(p):
    return run(p)
