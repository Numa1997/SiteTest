#!/usr/bin/env python3
"""The Narimanov–Moiseev five-mode sloshing equations of an upright circular cylinder, derived here from the multimodal
integrals of Faltinsen, Lukovsky & Timokha, J. Fluid Mech. 804 (2016) 608–645, eqs. (2.2)–(2.14), and reduced to their
eq. (2.17)–(2.18) with Ir = 1, Iθ = 2, which is Lukovsky's five-dimensional system, their eq. (2.23).

    python3 tools/fig12/nm_coeffs.py [h ...]        (h = depth / radius; default: 1 and 3.2)

The route (lecture note, §4.8). Lengths are scaled by the radius R, time by sqrt(R/g). The surface is
    zeta = R01(r) p0 + R11(r) (p1 cos th + r1 sin th) + R21(r) (p2 cos 2th + r2 sin 2th),   R_Mi = alpha J_M(k_Mi r),
with int_0^1 r R_Mi^2 dr = 1 (FLT (2.4)), and the potential Phi = sum_k P_k R_k(r) Z_k(z) T_k(th) over the same five modes,
Z_k = cosh(k (z + h)) / cosh(k h). FLT (2.12)–(2.14) give, for a surface zeta,
    A^p_k  = int int r T_k R_k int_{-h}^{zeta} Z_k dz dth dr,                    (the kinematic functions)
    A^pp_kl = int int r [ (R_k' R_l' T_k T_l + R_k R_l T_k' T_l' / r^2) I1 + k_k k_l R_k R_l T_k T_l I2 ] dth dr,
    I1 = int_{-h}^{zeta} Z_k Z_l dz,   I2 = int_{-h}^{zeta} Zs_k Zs_l dz,   Zs = sinh(k (z + h)) / cosh(k h).
The kinematic subsystem (2.9) is J beta' = A^pp P with J_ki = dA^p_k / d beta_i, so the kinetic energy (per unit density)
    T = 1/2 P' A^pp P = 1/2 beta'' M(beta) beta',   M = J' (A^pp)^-1 J,
and the potential energy of the surface is exactly V = 1/2 int int zeta^2 r dr dth (upright walls). The tank's horizontal
acceleration a_x adds L_a = -a_x int int x zeta r dr dth (the inertial force's potential in the tank's frame; the volume is
conserved by every mode). Lagrange's equations of L = T - V + L_a are the fully nonlinear modal system of these five modes
(Miles 1976; FLT (2.9)–(2.10)). Expanding the integrals in zeta about the mean surface to second order gives M to second order
in beta; keeping, as Narimanov and Moiseev order it (FLT (2.16)), cubic terms in (p1, r1) and products (p1, r1) x (p0, p2, r2)
in the equations of p1 and r1, and quadratic terms in (p1, r1) in those of p0, p2, r2, gives (2.17)–(2.18) with Ir = 1.

Printed: the natural frequencies, mu (the mass coefficients), every coefficient of the five equations divided by the
leading one, and the coefficients in FLT's (2.17)–(2.18) notation, d1 ... d10 (Ir = 1), to compare with FLT Table 1
(h = 1, Ir = 1: d1 = 1.758023, d2 = -1.083355). Also written as JSON to notes/fig12/runs/nm_coeffs.json.
"""
import json, sys, os
import numpy as np
import sympy as sp
from scipy.special import jv, jvp
from scipy.optimize import brentq

def kroots():
    # k_Mi: the first positive zero of J_M' (FLT: R'_Mi(1) = 0)
    return {m: brentq(lambda x: jvp(m, x), a, b) for m, (a, b) in {0: (3.0, 4.5), 1: (1.0, 2.5), 2: (2.5, 3.5)}.items()}

def derive(h, nr=200, nth=64):
    K = kroots()
    # the five modes: (name, M, trig) ; trig 'c' cos M th, 's' sin M th
    modes = [('p0', 0, 'c'), ('p1', 1, 'c'), ('r1', 1, 's'), ('p2', 2, 'c'), ('r2', 2, 's')]
    n = len(modes)
    # radial quadrature (Gauss–Legendre on [0, 1]) and angular (uniform; exact for trigonometric polynomials of low degree)
    xg, wg = np.polynomial.legendre.leggauss(nr); r = 0.5 * (xg + 1); wr = 0.5 * wg
    th = 2 * np.pi * np.arange(nth) / nth; wth = 2 * np.pi / nth
    alpha = {}
    for m in (0, 1, 2):
        k = K[m]; alpha[m] = 1 / np.sqrt(np.sum(wr * r * jv(m, k * r) ** 2))
    Rf = [alpha[M] * jv(M, K[M] * r) for _, M, _ in modes]                       # R_k(r) at the nodes
    dRf = [alpha[M] * K[M] * jvp(M, K[M] * r) for _, M, _ in modes]             # R_k'(r)
    Tf = [np.cos(M * th) if t == 'c' else np.sin(M * th) for _, M, t in modes]  # T_k(th)
    dTf = [-M * np.sin(M * th) if t == 'c' else M * np.cos(M * th) for _, M, t in modes]
    kk = [K[M] for _, M, _ in modes]; tk = [np.tanh(k * h) for k in kk]; kap = [k * t for k, t in zip(kk, tk)]
    # field of mode i on the (r, th) grid
    F = [np.outer(Rf[i], Tf[i]) for i in range(n)]
    W = np.outer(wr * r, np.full(nth, wth))                                     # r dr dth weights
    def integ(f): return float(np.sum(W * f))
    # zeta-expansions of the z-integrals at zeta = 0 (to second order)
    def I1_0(a, b):   # int_{-h}^0 Z_a Z_b dz
        ka, kb = kk[a], kk[b]; c = np.cosh(ka * h) * np.cosh(kb * h)
        if abs(ka - kb) < 1e-12: return (np.sinh(2 * ka * h) / (4 * ka) + h / 2) / c
        return 0.5 * (np.sinh((ka + kb) * h) / (ka + kb) + np.sinh((ka - kb) * h) / (ka - kb)) / c
    def I2_0(a, b):   # int_{-h}^0 Zs_a Zs_b dz
        ka, kb = kk[a], kk[b]; c = np.cosh(ka * h) * np.cosh(kb * h)
        if abs(ka - kb) < 1e-12: return (np.sinh(2 * ka * h) / (4 * ka) - h / 2) / c
        return 0.5 * (np.sinh((ka + kb) * h) / (ka + kb) - np.sinh((ka - kb) * h) / (ka - kb)) / c
    # J_ki(beta) = int int r T_k R_k T_i R_i Z_k(zeta) ;  Z_k(zeta) = 1 + kap_k zeta + 1/2 k_k^2 zeta^2 + ...
    J0 = np.array([[integ(F[k] * F[i]) for i in range(n)] for k in range(n)])
    J1 = np.array([[[kap[k] * integ(F[k] * F[i] * F[j]) for j in range(n)] for i in range(n)] for k in range(n)])
    J2 = np.array([[[[0.5 * kk[k] ** 2 * integ(F[k] * F[i] * F[j] * F[l]) for l in range(n)] for j in range(n)] for i in range(n)] for k in range(n)])
    # A^pp_kl(beta): G1 = R'R'TT + RRT'T'/r^2 with I1 ; G2 = k k RRTT with I2
    G1 = [[np.outer(dRf[a] * dRf[b], Tf[a] * Tf[b]) + np.outer(Rf[a] * Rf[b] / r ** 2, dTf[a] * dTf[b]) for b in range(n)] for a in range(n)]
    G2 = [[kk[a] * kk[b] * np.outer(Rf[a] * Rf[b], Tf[a] * Tf[b]) for b in range(n)] for a in range(n)]
    A0 = np.array([[integ(G1[a][b]) * I1_0(a, b) + integ(G2[a][b]) * I2_0(a, b) for b in range(n)] for a in range(n)])
    # dI1/dzeta = Z_a Z_b = 1 at 0 ; d2 = kap_a + kap_b.  dI2/dzeta = Zs_a Zs_b = tanh_a tanh_b at 0 ; d2 = k_a tanh_b + k_b tanh_a
    A1 = np.array([[[integ(G1[a][b] * F[i]) + tk[a] * tk[b] * integ(G2[a][b] * F[i]) for i in range(n)] for b in range(n)] for a in range(n)])
    A2 = np.array([[[[0.5 * (kap[a] + kap[b]) * integ(G1[a][b] * F[i] * F[j]) + 0.5 * (kk[a] * tk[b] + kk[b] * tk[a]) * integ(G2[a][b] * F[i] * F[j])
                      for j in range(n)] for i in range(n)] for b in range(n)] for a in range(n)])
    # symbolic beta, M(beta) to second order
    B = sp.symbols('p0 p1 r1 p2 r2'); Bd = sp.symbols('p0d p1d r1d p2d r2d'); Bdd = sp.symbols('p0dd p1dd r1dd p2dd r2dd'); ax = sp.Symbol('a_x')
    def lin(T3): return sp.Matrix(n, n, lambda a, b: sum(sp.Float(T3[a, b, i], 15) * B[i] for i in range(n)))
    def quad(T4): return sp.Matrix(n, n, lambda a, b: sum(sp.Float(T4[a, b, i, j], 15) * B[i] * B[j] for i in range(n) for j in range(n)))
    J0m, A0i = sp.Matrix(J0), sp.Matrix(np.linalg.inv(A0))
    J1m, J2m, A1m, A2m = lin(J1), quad(J2), lin(A1), quad(A2)
    M0 = J0m.T * A0i * J0m
    M1 = J1m.T * A0i * J0m + J0m.T * A0i * J1m - J0m.T * A0i * A1m * A0i * J0m
    M2 = (J2m.T * A0i * J0m + J0m.T * A0i * J2m + J1m.T * A0i * J1m - J1m.T * A0i * A1m * A0i * J0m - J0m.T * A0i * A1m * A0i * J1m
          - J0m.T * A0i * A2m * A0i * J0m + J0m.T * A0i * A1m * A0i * A1m * A0i * J0m)
    M = M0 + M1 + M2
    Lam = [integ(F[i] * F[i]) for i in range(n)]
    fx = [integ(np.outer(r, np.cos(th)) * F[i]) for i in range(n)]               # int int x zeta_i r dr dth
    bd = sp.Matrix(Bd)
    T = (bd.T * M * bd)[0] / 2
    V = sum(Lam[i] * B[i] ** 2 for i in range(n)) / 2                             # g = 1
    eqs = []
    for i in range(n):
        dT_dqd = sp.diff(T, Bd[i])
        # d/dt of dT/dqd: chain rule over beta and betadot
        ddt = sum(sp.diff(dT_dqd, B[j]) * Bd[j] + sp.diff(dT_dqd, Bd[j]) * Bdd[j] for j in range(n))
        eqs.append(sp.expand(ddt - sp.diff(T, B[i]) + sp.diff(V, B[i]) + ax * fx[i]))
    # Narimanov–Moiseev ordering: eps^(1/3) for p1, r1; eps^(2/3) for p0, p2, r2; keep terms up to eps (first-order eqs) or
    # eps^(2/3) (second-order eqs), counting time derivatives as order 1 and a_x as order eps
    order = {B[0]: 2, B[1]: 1, B[2]: 1, B[3]: 2, B[4]: 2, Bd[0]: 2, Bd[1]: 1, Bd[2]: 1, Bd[3]: 2, Bd[4]: 2,
             Bdd[0]: 2, Bdd[1]: 1, Bdd[2]: 1, Bdd[3]: 2, Bdd[4]: 2, ax: 3}
    out = []
    for i, e in enumerate(eqs):
        keep = 3 if i in (1, 2) else 2
        terms = {}
        for term in sp.Add.make_args(e):
            c, mon = term.as_coeff_Mul()
            o = sum(order[s] * d for s, d in mon.as_powers_dict().items() if s in order)
            if o <= keep and abs(float(c)) > 1e-10: terms[mon] = terms.get(mon, 0) + float(c)
        lead = terms[Bdd[i]]
        out.append({str(k): v / lead for k, v in terms.items()})
    mu = [float(M0[i, i]) for i in range(n)]
    sig2 = [Lam[i] / mu[i] for i in range(n)]
    # FLT notation, Ir = 1 (equation of p1, divided by its leading coefficient):
    e1 = out[1]
    d = {'d1': e1.get('p1**2*p1dd', 0), 'd2': e1.get('p1dd*r1**2', 0),
         'check_d1_from_p1*p1d**2': e1.get('p1*p1d**2', 0), 'check_d1-2d2_from_p1*r1d**2': e1.get('p1*r1d**2', 0),
         'check_d1-d2_from_p1*r1*r1dd': e1.get('p1*r1*r1dd', 0), 'check_2d2_from_p1d*r1*r1d': e1.get('p1d*r1*r1d', 0)}
    return {'h': h, 'k': {m: K[m] for m in K}, 'sigma2': dict(zip(['p0', 'p1', 'r1', 'p2', 'r2'], sig2)),
            'mu': dict(zip(['p0', 'p1', 'r1', 'p2', 'r2'], mu)), 'forcing': dict(zip(['p0', 'p1', 'r1', 'p2', 'r2'], fx)),
            'Lambda': dict(zip(['p0', 'p1', 'r1', 'p2', 'r2'], Lam)), 'R1': float(alpha[1] * jv(1, K[1])), 'R0': float(alpha[0] * jv(0, K[0])),
            'R2': float(alpha[2] * jv(2, K[2])), 'FLT_d': d, 'equations': dict(zip(['p0', 'p1', 'r1', 'p2', 'r2'], out))}

if __name__ == '__main__':
    hs = [float(a) for a in sys.argv[1:]] or [1.0, 3.2]
    res = []
    for h in hs:
        R = derive(h); res.append(R)
        print(f"h = {h}: sigma^2 = " + ', '.join(f"{k} {v:.6f}" for k, v in R['sigma2'].items()))
        print('  FLT (2.17) with Ir = 1: ' + ', '.join(f"{k} {v:.6f}" for k, v in R['FLT_d'].items()))
        for name, eq in R['equations'].items():
            print(f"  eq {name}: " + '  '.join(f"{v:+.5f} {k}" for k, v in sorted(eq.items(), key=lambda kv: kv[0])))
    out = os.path.join(os.path.dirname(__file__), '../../notes/fig12/runs/nm_coeffs.json')
    with open(out, 'w') as f: json.dump(res, f, indent=1)
    # the page's coefficients: the deepest case asked for (the glass: h / R(h) = 125 / 39.1 = 3.197), as a script
    R = max(res, key=lambda q: q['h'])
    js = os.path.join(os.path.dirname(__file__), '../../public/scripts/stout-nm.js')
    with open(js, 'w') as f:
        f.write('/* Written by tools/fig12/nm_coeffs.py; do not edit. The Narimanov–Moiseev five-mode equations of an upright circular\n'
                '   cylinder, h/R = %.3f (Faltinsen, Lukovsky & Timokha 2016, eqs. 2.17–2.18 with Ir = 1 = Lukovsky\'s eq. 2.23), lengths\n'
                '   in units of R, time in sqrt(R/g). Each equation (of p0, p1, r1, p2, r2) is a list of [coefficient, monomial] with\n'
                '   "x", "xd", "xdd" a coordinate, its rate and its acceleration, "a_x" the horizontal acceleration / g; the sum is 0. */\n' % R['h'])
        f.write('(function (root) { root.STOUT_NM = ' + json.dumps({'h': R['h'], 'k': R['k'], 'R0': R['R0'], 'R1': R['R1'], 'R2': R['R2'],
                'sigma2': R['sigma2'], 'Lambda': R['Lambda'], 'forcing': R['forcing'], 'mu': R['mu'], 'd': R['FLT_d'],
                'eqs': {k: [[round(v, 10), m] for m, v in sorted(e.items())] for k, e in R['equations'].items()}}) +
                '; if (typeof module !== "undefined") module.exports = root.STOUT_NM; })(typeof self !== "undefined" ? self : globalThis);\n')
