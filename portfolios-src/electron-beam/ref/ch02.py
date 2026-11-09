"""Project 07 · The Electron Beam · chapter 2, the source: NumPy reference.

A readable second implementation of physics/ch02.js, written independently line by line from the formulas on the page
(same grids, same integrals), so that the two can be compared number by number (notes/electron-beam/ch02/check_parity.py).
SI units unless a name ends in _eV. Constants: CODATA 2018 exact values.

    python3 ref/ch02.py          prints the numbers that the text of the chapter quotes
"""
import math
import numpy as np

e = 1.602176634e-19
h = 6.62607015e-34
hbar = h / (2 * math.pi)
me = 9.1093837015e-31
eps0 = 8.8541878128e-12
kB = 1.380649e-23
u = 1.66053906660e-27
eV = e
Q0 = e * e / (16 * math.pi * eps0)                      # image-charge constant, J m
bFN = 4 * math.sqrt(2 * me) / (3 * hbar * e)            # J^-3/2 V/m
RD = 4 * math.pi * me * e * kB * kB / h ** 3            # Richardson constant, A m^-2 K^-2


# ------------------------------------------------------------------------------------------------ the barrier
def schottky_lowering(F):
    return math.sqrt(e ** 3 * F / (4 * math.pi * eps0))


def scaled_field(F, phi):
    return e ** 3 * F / (4 * math.pi * eps0 * phi ** 2)


def reference_field(phi):
    return 4 * math.pi * eps0 * phi ** 2 / e ** 3


_GL = {}


def _gl(n):
    if n not in _GL:
        _GL[n] = np.polynomial.legendre.leggauss(n)
    return _GL[n]


def barrier_G(F, phi, n=48):
    """WKB exponent G = (2/hbar) Int sqrt(2 m U) dx between the two roots of U = phi - eF x - Q0/x."""
    if phi <= 0:
        return 0.0
    f = scaled_field(F, phi)
    if f >= 1:
        return 0.0
    s = math.sqrt(1 - f)
    x1, x2 = phi * (1 - s) / (2 * e * F), phi * (1 + s) / (2 * e * F)
    D = x2 - x1
    x, wgt = _gl(n)
    th = math.pi / 4 * (x + 1)
    sn, cs = np.sin(th), np.cos(th)
    S = math.pi / 4 * np.sum(wgt * 2 * D * D * sn ** 2 * cs ** 2 / np.sqrt(x1 + D * sn ** 2))
    return 2 * math.sqrt(2 * me) / hbar * math.sqrt(e * F) * S


def v_exact(f):
    if f <= 0:
        return 1.0
    if f >= 1:
        return 0.0
    phi = 4.5 * eV
    F = f * reference_field(phi)
    return barrier_G(F, phi, 64) * F / (bFN * phi ** 1.5)


def v_forbes(f):
    return 1.0 if f <= 0 else 1 - f + f * math.log(f) / 6


def t_forbes(f):
    return 1.0 if f <= 0 else 1 + f / 9 - f * math.log(f) / 18


# ------------------------------------------------------------------------------------------------ analytic FN
def d_tunnel(F, phi):
    return hbar * e * F / (2 * math.sqrt(2 * me * phi) * t_forbes(min(scaled_field(F, phi), 1)))


def j_fn(F, phi, T=0.0):
    f = scaled_field(F, phi)
    if f >= 1:
        return float('nan')
    t, v = t_forbes(f), v_forbes(f)
    J = e ** 3 * F * F / (8 * math.pi * h * phi * t * t) * math.exp(-v * bFN * phi ** 1.5 / F)
    if T > 0:
        x = math.pi * kB * T / d_tunnel(F, phi)
        J *= x / math.sin(x) if x < 1.5 else float('nan')
    return J


def j_richardson(T, phi):
    return RD * T * T * math.exp(-phi / (kB * T))


def j_schottky(F, T, phi):
    return RD * T * T * math.exp(-(phi - schottky_lowering(F)) / (kB * T))


# ------------------------------------------------------------------------------------------------ the full model
def neg_li2(z):
    """-Li2(-z) for z > 0 (complete Fermi-Dirac integral of order 1), Landen and inversion formulas, series in y <= 1/2."""
    def li2(y):
        k = np.arange(1, 60)
        return float(np.sum(y ** k / k ** 2))

    def small(zz):
        y, l = zz / (1 + zz), math.log(1 + zz)
        return li2(y) + 0.5 * l * l
    if z <= 1:
        return small(z)
    l = math.log(z)
    return math.pi ** 2 / 6 + 0.5 * l * l - small(1 / z)


def emission_model(F, phi, T, max_points=2400):
    T = max(T, 1.0)
    kT = kB * T
    dphi = schottky_lowering(F)
    top = phi - dphi
    f0 = scaled_field(F, phi)
    d = d_tunnel(F, phi) if f0 < 1 else 0.1 * eV
    lo = -max(25 * d, 12 * kT)
    hi = max(14 * kT, top + 14 * kT)
    step = min(d, kT) / 14
    n = max(400, min(max_points, math.ceil((hi - lo) / step)))
    dw = (hi - lo) / (n - 1)
    w = lo + dw * np.arange(n)
    s_top = 0.0
    if top > 0:
        dl = min(0.02 * eV, 0.2 * top)
        s_top = barrier_G(F, phi - (top - dl), 24) / dl
    G = np.array([barrier_G(F, phi - wi, 24) if wi <= top else -(wi - top) * s_top for wi in w])
    Dv = np.where(G > 700, 0.0, 1 / (1 + np.exp(np.minimum(G, 700))))
    ferm = 1 / (1 + np.exp(np.minimum(w / kT, 700)))
    z = np.exp(-w / kT)
    lw = np.where(w / kT > 40, z, np.log1p(np.minimum(z, 1e300)))
    wt = np.ones(n)
    wt[0] = wt[-1] = 0.5
    pref = 4 * math.pi * me / h ** 3
    sJ = np.sum(wt * lw * Dv)
    sj0 = np.sum(wt * ferm * Dv)
    g0 = np.sum(wt * lw * Dv)
    g1 = np.sum(wt * np.array([neg_li2(min(zi, 1e300)) for zi in z]) * Dv)
    C = np.concatenate([[0.0], np.cumsum(0.5 * (Dv[1:] + Dv[:-1]) * dw)])
    P = ferm * C
    J = e * pref * kT * sJ * dw
    jt0 = e * pref * sj0 * dw
    mean_et = kT * g1 / g0 if g0 > 0 else 0.0
    ip = int(np.argmax(P))
    half = P[ip] / 2
    l = ip
    while l > 0 and P[l] > half:
        l -= 1
    r = ip
    while r < n - 1 and P[r] > half:
        r += 1
    xl = w[l] + (half - P[l]) / (P[l + 1] - P[l]) * dw if l < ip else w[l]
    xr = w[r - 1] + (P[r - 1] - half) / (P[r - 1] - P[r]) * dw if r > ip else w[r]
    J_check = e * pref * np.sum(wt * P) * dw
    return dict(J=J, J_check=J_check, jt0=jt0, B_r=eV * jt0 / math.pi, mean_et=mean_et, fwhm=xr - xl, peak=w[ip],
                top=top, d=d, f=f0, kT=kT, dphi=dphi, w=w, D=Dv, P=P, regime=_regime(f0, kT, w[ip], top))


def _regime(f, kT, peak, top):
    if f >= 1:
        return 'field above the barrier: no tunnelling barrier left'
    if peak < 0:
        return 'cold field emission'
    if top > 0 and peak < top - 3 * kT:
        return 'thermal-field emission'
    return 'thermionic (Schottky) emission'


# ------------------------------------------------------------------------------------------------ tip, hand-over
def tip_field(V, r, k):
    return V / (k * r)


def tip_current(V, r, k, phi, T, fast=False, u0=0.0, nodes=24):
    F0 = tip_field(V, r, k)
    x, wgt = _gl(nodes)
    a, b = (1 - u0) / 2, (1 + u0) / 2
    s = 0.0
    for xi, wi in zip(x, wgt):
        Fu = F0 * (a * xi + b)
        J = j_fn(Fu, phi, T) if fast else emission_model(Fu, phi, T, max_points=500)['J']
        s += wi * (J if math.isfinite(J) else 0.0)
    return 2 * math.pi * r * r * a * s


def handover(V, r, k, phi, T):
    F0 = tip_field(V, r, k)
    m = emission_model(F0, phi, T)
    I_e = tip_current(V, r, k, phi, T)
    d_v = 2 * r * math.sqrt(m['mean_et'] / (e * V))
    return dict(I_e=I_e, B_r=m['B_r'], dE=m['fwhm'], dE_eV=m['fwhm'] / eV, d_v=d_v, F0=F0, f=m['f'], J0=m['J'],
                meanEt_eV=m['mean_et'] / eV, regime=m['regime'])


# ------------------------------------------------------------------------------------------------ vacuum and contamination
def hk_flux(p_pa, Tg, mu):
    return p_pa / math.sqrt(2 * math.pi * mu * u * kB * Tg)


def k_des(Ed_eV, T, nu0=1e13):
    return nu0 * math.exp(-Ed_eV * eV / (kB * T))


def coverage_step(theta0, dt, a, kd):
    lam = a + kd
    th_inf = a / lam if lam > 0 else 0.0
    return th_inf + (theta0 - th_inf) * math.exp(-lam * dt)


def time_to_coverage(th, a, kd):
    lam = a + kd
    inf = a / lam
    return -math.log(1 - th / inf) / lam if th < inf else math.inf


def current_ratio(theta, rho):
    return (1 - theta) + theta * rho


def covered_ratio(F, phi, dphi_ads_eV):
    return j_fn(F, phi + dphi_ads_eV * eV, 0.0) / j_fn(F, phi, 0.0)


def cycle(pPa, Tg, mu, Ns, s, kappa, Ed, T, Tflash, tflash, thr, theta0, rho, tmax, dt):
    a = kappa * s * hk_flux(pPa, Tg, mu) / Ns
    kRT, kFl = k_des(Ed, T), k_des(Ed, Tflash)
    t, th = 0.0, theta0
    ts, ths, rs, flashes = [], [], [], []
    every = max(1, round(tmax / dt / 1200))
    i = 0
    while t <= tmax:
        if i % every == 0:
            ts.append(t); ths.append(th); rs.append(current_ratio(th, rho))
        i += 1
        if thr > 0 and current_ratio(th, rho) < thr:
            flashes.append(t)
            th = coverage_step(th, tflash, a, kFl)
            t += tflash
            ts.append(t); ths.append(th); rs.append(float('nan'))
            continue
        th = coverage_step(th, dt, a, kRT)
        t += dt
    return dict(t=ts, theta=ths, ratio=rs, flashes=flashes, a=a, kRT=kRT, kFl=kFl)


# ------------------------------------------------------------------------------------------------ published data (Ayari et al. 2023)
def load_ayari(path):
    rows = np.genfromtxt(path, delimiter=',', names=True, dtype=None, encoding='utf-8')
    return rows


def fit_tip(V, I_A, phi_eV=4.5, T=300.0):
    """Fit I = A J_FN(V / zeta) to measured (V, I): two parameters, the voltage conversion length zeta (m) and the emitting area A (m^2).
    ln A drops out in closed form for every zeta; zeta is found by golden-section search on the rms of ln I."""
    phi = phi_eV * eV
    lnI = np.log(I_A)

    def rms(zeta):
        J = np.array([j_fn(v / zeta, phi, T) for v in V])
        if not np.all(np.isfinite(J)):          # temperature correction outside its range: treat as a bad zeta, not as data
            return math.inf, math.nan
        lnJ = np.log(J)
        lnA = np.mean(lnI - lnJ)
        return math.sqrt(np.mean((lnI - lnJ - lnA) ** 2)), lnA
    a, b = 300e-9, 1500e-9
    gr = (math.sqrt(5) - 1) / 2
    c, d = b - gr * (b - a), a + gr * (b - a)
    for _ in range(80):
        if rms(c)[0] < rms(d)[0]:
            b = d
        else:
            a = c
        c, d = b - gr * (b - a), a + gr * (b - a)
    zeta = (a + b) / 2
    r, lnA = rms(zeta)
    return dict(zeta=zeta, A=math.exp(lnA), rms_lnI=r)


if __name__ == '__main__':
    print('v max error', max(abs(v_exact(f) - v_forbes(f)) for f in np.arange(0.01, 1, 0.01)))
    for Fnm in (3, 4, 5):
        m = emission_model(Fnm * 1e9, 4.5 * eV, 300)
        print(Fnm, 'V/nm', f"J={m['J']:.4e} FWHM={m['fwhm'] / eV:.4f} eV <Et>={m['mean_et'] / eV:.4f} eV B_r={m['B_r']:.4e}", m['regime'])


# ------------------------------------------------------------------------------------------------ the contract interface (stage ch02)
INPUTS = ['r_t', 'V_ex', 'phi', 'T', 'p', 't_clean', 'k_f']
OUTPUTS = ['I_e', 'B_r', 'dE', 'd_v', 'theta_cov']
ASSUME = dict(mu=2.016, Tg=300.0, ks=0.535, Ns=1e19, Ed=1.9, dads=1.0)


def compute(p):
    """Mirror of compute() in physics/ch02.js: hand-over of the clean tip, coverage after t_clean, patch-model mix."""
    r, k, phi, T, V = p['r_t'], p['k_f'], p['phi'], p['T'], p['V_ex']
    h = handover(V, r, k, phi, T)
    h['I_e'] = tip_current(V, r, k, phi, T, nodes=16)
    a = ASSUME['ks'] * hk_flux(p['p'], ASSUME['Tg'], ASSUME['mu']) / ASSUME['Ns']
    th = coverage_step(0.0, p['t_clean'], a, k_des(ASSUME['Ed'], T))
    phiV = phi + ASSUME['dads'] * eV
    Iv = tip_current(V, r, k, phiV, T, nodes=16)
    mv = emission_model(tip_field(V, r, k), phiV, T)
    return dict(I_e=(1 - th) * h['I_e'] + th * Iv, B_r=(1 - th) * h['B_r'] + th * mv['B_r'], dE=h['dE'], d_v=h['d_v'], theta_cov=th)
