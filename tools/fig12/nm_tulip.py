#!/usr/bin/env python3
"""Lukovsky's five-mode Narimanov–Moiseev sloshing equations for the real tulip glass, with the finite-element modes in
place of a cylinder's Bessel functions.

    python3 tools/fig12/nm_tulip.py check             # on a cylinder: must reproduce tools/fig12/nm_coeffs.py (FLT Table 1)
    python3 tools/fig12/nm_tulip.py tulip [h_mm ...]  # the tulip (default 125 mm); OUT=file.json saves the equations

Why surface data suffice. tools/fig12/nm_coeffs.py builds the system from Faltinsen, Lukovsky & Timokha (J. Fluid Mech. 804,
2016), eqs. (2.2)-(2.14): the kinematic functions A^p_k = int phi_k over the liquid up to the surface zeta, and the kinetic
matrix A^pp_kl = int grad phi_k . grad phi_l over the same volume, expanded in zeta about the mean surface to second order.
For a wall that is vertical where the surface meets it, every term of those expansions is an integral over the mean surface
of quantities known there:
    phi_k,   d phi_k/dz = kappa_k phi_k,   d2 phi_k/dz2 = -Lap_h phi_k   (Laplace's equation),   grad_h phi_k,
    d/dz (grad_h phi_k) = kappa_k grad_h phi_k   (tangential derivative of the surface condition along the flat surface),
and the zeroth-order kinetic matrix is A0_kk = kappa_k int phi_k^2 dS (Green's first identity). With the cylinder's Bessel
modes these are exactly nm_coeffs.py's integrals (checked below). The tulip's wall leans by dR/dz = -0.04 at 125 mm; the
terms that lean adds are left out here (stated; measured against whole-glass 3D runs).

Lengths in units of the surface radius R(h), time in sqrt(R/g), as in FLT. The surface is
    zeta = R0(r) p0 + R1(r) (p1 cos th + r1 sin th) + R2(r) (p2 cos 2th + r2 sin 2th),   int_0^1 r R_M^2 dr = 1,
R_M the first finite-element surface shape of harmonic M, written r^M P_M(r^2) with P_M a Chebyshev fit in r^2.
"""
import json, sys, os
import numpy as np
import sympy as sp
from numpy.polynomial import chebyshev as C
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modes_fem as FE

NAMES = ['p0', 'p1', 'r1', 'p2', 'r2']
MODES = [('p0', 0, 'c'), ('p1', 1, 'c'), ('r1', 1, 's'), ('p2', 2, 'c'), ('r2', 2, 's')]


def surface_mode(Rf, h, m, deg=16):
    """The first mode of harmonic m: kappa R(h) (dimensionless) and functions R, R', -Lap_h R of r/R(h), with int r R^2 = 1.
    Returns also the fit's largest residual relative to the shape's largest value."""
    out = FE.solve(Rf, h, m, 48, 96, 2, nmodes=1)
    Rs = out['r'][-1]; rr = out['r'] / Rs; e = out['shapes'][0]
    s = rr ** 2; keep = rr > 1e-9 if m > 0 else np.ones_like(rr, bool)
    y = e[keep] / rr[keep] ** m                     # P(s) = R / r^m
    cf = C.chebfit(2 * s[keep] - 1, y, deg)
    fit = rr ** m * C.chebval(2 * s - 1, cf)
    res = np.abs(fit - e).max() / np.abs(e).max()
    d1 = C.chebder(cf); d2 = C.chebder(d1)
    P = lambda s: C.chebval(2 * s - 1, cf); dP = lambda s: 2 * C.chebval(2 * s - 1, d1); ddP = lambda s: 4 * C.chebval(2 * s - 1, d2)
    xg, wg = np.polynomial.legendre.leggauss(400); rg = 0.5 * (xg + 1); wgr = 0.5 * wg
    norm = 1 / np.sqrt(np.sum(wgr * rg * (rg ** m * P(rg ** 2)) ** 2))
    R = lambda r: norm * r ** m * P(r * r)
    dR = lambda r: norm * (m * r ** (m - 1) * P(r * r) + 2 * r ** (m + 1) * dP(r * r)) if m > 0 else norm * 2 * r * dP(r * r)
    nlap = lambda r: -norm * r ** m * (4 * r * r * ddP(r * r) + 4 * (m + 1) * dP(r * r))      # -Lap_h of R e^{i m th}, radial part
    return dict(kappa=out['kappa'][0] * Rs, f=out['f'][0], R=R, dR=dR, nlap=nlap, fit_res=res, Rs=Rs)


def lagrange_numeric(J0, J1, J2, A0, A1, A2, Lam, fx, prov):
    """The same equations without symbolic algebra. M(b) = M0 + M1_i b_i + M2_ij b_i b_j (second order, as derive builds it),
    T = 1/2 b'^T M b', V = 1/2 sum Lam b^2, L_a = -a_x sum f b. Lagrange's equation of coordinate c:
        sum_b M_cb b''_b + sum_{b,i} d_i M_cb b'_i b'_b - 1/2 sum_{a,b} d_c M_ab b'_a b'_b + Lam_c b_c + f_c a_x = 0,
    every monomial kept or dropped by the Narimanov-Moiseev order, as in derive."""
    n = len(MODES); Ai = np.linalg.inv(A0)
    M0 = J0.T @ Ai @ J0
    # first order: M1[a,b,i]
    J1i = np.transpose(J1, (2, 0, 1)); A1i = np.transpose(A1, (2, 0, 1))        # [i][k][l]
    M1 = np.zeros((n, n, n)); M2 = np.zeros((n, n, n, n))
    for i in range(n):
        M1[:, :, i] = J1i[i].T @ Ai @ J0 + J0.T @ Ai @ J1i[i] - J0.T @ Ai @ A1i[i] @ Ai @ J0
    for i in range(n):
        for j in range(n):
            J2ij, A2ij = J2[:, :, i, j], A2[:, :, i, j]
            M2[:, :, i, j] = (J2ij.T @ Ai @ J0 + J0.T @ Ai @ J2ij + J1i[i].T @ Ai @ J1i[j] - J1i[i].T @ Ai @ A1i[j] @ Ai @ J0
                              - J0.T @ Ai @ A1i[i] @ Ai @ J1i[j] - J0.T @ Ai @ A2ij @ Ai @ J0 + J0.T @ Ai @ A1i[i] @ Ai @ A1i[j] @ Ai @ J0)
    order = [2, 1, 1, 2, 2]
    def name(fs):          # factors (var index, kind 0 b, 1 b', 2 b'') -> sympy's printed monomial
        cnt = {}
        for v, k in fs:
            nm = NAMES[v] + ['', 'd', 'dd'][k]; cnt[nm] = cnt.get(nm, 0) + 1
        return '*'.join(f'{k}**{c}' if c > 1 else k for k, c in sorted(cnt.items()))
    out = []
    for c in range(n):
        keep = 3 if c in (1, 2) else 2; terms = {}
        def add(coef, fs):
            if sum(order[v] for v, _ in fs) <= keep and abs(coef) > 0: terms[name(fs)] = terms.get(name(fs), 0) + coef
        for b in range(n):                           # M_cb b''_b, M to second order
            add(M0[c, b], [(b, 2)])
            for i in range(n):
                add(M1[c, b, i], [(b, 2), (i, 0)])
                for j in range(n): add(M2[c, b, i, j], [(b, 2), (i, 0), (j, 0)])
        for b in range(n):                           # d_i M_cb b'_i b'_b ;  d_i M = M1[..i] + (M2[..i,j] + M2[..j,i]) b_j
            for i in range(n):
                add(M1[c, b, i], [(i, 1), (b, 1)])
                for j in range(n): add(M2[c, b, i, j] + M2[c, b, j, i], [(i, 1), (b, 1), (j, 0)])
        for a in range(n):                           # -1/2 d_c M_ab b'_a b'_b
            for b in range(n):
                add(-0.5 * M1[a, b, c], [(a, 1), (b, 1)])
                for j in range(n): add(-0.5 * (M2[a, b, c, j] + M2[a, b, j, c]), [(a, 1), (b, 1), (j, 0)])
        add(Lam[c], [(c, 0)])
        terms = {k: v for k, v in terms.items() if abs(v) > 1e-10}
        if abs(fx[c]) > 1e-10: terms['a_x'] = fx[c]
        lead = terms[NAMES[c] + 'dd']; out.append({k: v / lead for k, v in terms.items()})
    mu = [float(M0[i, i]) for i in range(n)]
    return {'sigma2': dict(zip(NAMES, [Lam[i] / mu[i] for i in range(n)])), 'mu': dict(zip(NAMES, mu)), 'Lambda': dict(zip(NAMES, Lam)),
            'forcing': dict(zip(NAMES, fx)), 'R0': float(prov[0]['R'](np.array([1.0]))[0]), 'R1': float(prov[1]['R'](np.array([1.0]))[0]),
            'R2': float(prov[2]['R'](np.array([1.0]))[0]), 'd': {'d1': out[1].get('p1**2*p1dd', 0), 'd2': out[1].get('p1dd*r1**2', 0)},
            'equations': dict(zip(NAMES, out))}


def derive(prov, nr=200, nth=64, numeric=False):
    """prov[M] = surface_mode(...) for M = 0, 1, 2. The FLT construction of nm_coeffs.derive with surface integrals."""
    n = len(MODES)
    xg, wg = np.polynomial.legendre.leggauss(nr); r = 0.5 * (xg + 1); wr = 0.5 * wg
    th = 2 * np.pi * np.arange(nth) / nth; wth = 2 * np.pi / nth
    Rf = [prov[M]['R'](r) for _, M, _ in MODES]; dRf = [prov[M]['dR'](r) for _, M, _ in MODES]; nL = [prov[M]['nlap'](r) for _, M, _ in MODES]
    Tf = [np.cos(M * th) if t == 'c' else np.sin(M * th) for _, M, t in MODES]
    dTf = [-M * np.sin(M * th) if t == 'c' else M * np.cos(M * th) for _, M, t in MODES]
    kap = [prov[M]['kappa'] for _, M, _ in MODES]
    F = [np.outer(Rf[i], Tf[i]) for i in range(n)]
    NL = [np.outer(nL[i], Tf[i]) for i in range(n)]                              # -Lap_h phi_k = d2 phi_k / dz2 at the surface
    W = np.outer(wr * r, np.full(nth, wth))
    integ = lambda f: float(np.sum(W * f))
    # kinematic functions: phi_k(zeta) = phi_k + kappa_k phi_k zeta + (1/2) d2phi_k zeta^2
    J0 = np.array([[integ(F[k] * F[i]) for i in range(n)] for k in range(n)])
    J1 = np.array([[[kap[k] * integ(F[k] * F[i] * F[j]) for j in range(n)] for i in range(n)] for k in range(n)])
    J2 = np.array([[[[0.5 * integ(NL[k] * F[i] * F[j] * F[l]) for l in range(n)] for j in range(n)] for i in range(n)] for k in range(n)])
    # kinetic matrix: G1 = grad_h phi_a . grad_h phi_b ; vertical part kappa_a kappa_b phi_a phi_b at the surface
    G1 = [[np.outer(dRf[a] * dRf[b], Tf[a] * Tf[b]) + np.outer(Rf[a] * Rf[b] / r ** 2, dTf[a] * dTf[b]) for b in range(n)] for a in range(n)]
    A0 = np.diag([kap[a] * integ(F[a] * F[a]) for a in range(n)])                 # Green: int |grad phi|^2 dV = kappa int phi^2 dS
    A1 = np.array([[[integ((G1[a][b] + kap[a] * kap[b] * F[a] * F[b]) * F[i]) for i in range(n)] for b in range(n)] for a in range(n)])
    # d/dz of (grad_h phi_a . grad_h phi_b + phi_az phi_bz) = (kap_a + kap_b) G1 + kap_b phi_b d2phi_a + kap_a phi_a d2phi_b
    A2 = np.array([[[[0.5 * integ(((kap[a] + kap[b]) * G1[a][b] + kap[b] * F[b] * NL[a] + kap[a] * F[a] * NL[b]) * F[i] * F[j])
                      for j in range(n)] for i in range(n)] for b in range(n)] for a in range(n)])
    Lam = [integ(F[i] * F[i]) for i in range(n)]
    fx = [integ(np.outer(r, np.cos(th)) * F[i]) for i in range(n)]
    if numeric:
        return lagrange_numeric(J0, J1, J2, A0, A1, A2, Lam, fx, prov)
    B = sp.symbols('p0 p1 r1 p2 r2'); Bd = sp.symbols('p0d p1d r1d p2d r2d'); Bdd = sp.symbols('p0dd p1dd r1dd p2dd r2dd'); ax = sp.Symbol('a_x')
    lin = lambda T3: sp.Matrix(n, n, lambda a, b: sum(sp.Float(T3[a, b, i], 15) * B[i] for i in range(n)))
    quad = lambda T4: sp.Matrix(n, n, lambda a, b: sum(sp.Float(T4[a, b, i, j], 15) * B[i] * B[j] for i in range(n) for j in range(n)))
    J0m, A0i = sp.Matrix(J0), sp.Matrix(np.linalg.inv(A0))
    J1m, J2m, A1m, A2m = lin(J1), quad(J2), lin(A1), quad(A2)
    M = (J0m.T * A0i * J0m
         + J1m.T * A0i * J0m + J0m.T * A0i * J1m - J0m.T * A0i * A1m * A0i * J0m
         + J2m.T * A0i * J0m + J0m.T * A0i * J2m + J1m.T * A0i * J1m - J1m.T * A0i * A1m * A0i * J0m - J0m.T * A0i * A1m * A0i * J1m
         - J0m.T * A0i * A2m * A0i * J0m + J0m.T * A0i * A1m * A0i * A1m * A0i * J0m)
    bd = sp.Matrix(Bd); T = (bd.T * M * bd)[0] / 2; V = sum(Lam[i] * B[i] ** 2 for i in range(n)) / 2
    order = {B[0]: 2, B[1]: 1, B[2]: 1, B[3]: 2, B[4]: 2, Bd[0]: 2, Bd[1]: 1, Bd[2]: 1, Bd[3]: 2, Bd[4]: 2,
             Bdd[0]: 2, Bdd[1]: 1, Bdd[2]: 1, Bdd[3]: 2, Bdd[4]: 2, ax: 3}
    out = []
    for i in range(n):
        dT = sp.diff(T, Bd[i])
        e = sp.expand(sum(sp.diff(dT, B[j]) * Bd[j] + sp.diff(dT, Bd[j]) * Bdd[j] for j in range(n)) - sp.diff(T, B[i]) + sp.diff(V, B[i]) + ax * fx[i])
        keep = 3 if i in (1, 2) else 2; terms = {}
        for term in sp.Add.make_args(e):
            c, mon = term.as_coeff_Mul()
            o = sum(order[s] * d for s, d in mon.as_powers_dict().items() if s in order)
            if o <= keep and abs(float(c)) > 1e-10: terms[mon] = terms.get(mon, 0) + float(c)
        lead = terms[Bdd[i]]; out.append({str(k): v / lead for k, v in terms.items()})
    e1 = out[1]
    mu = [float(sp.Matrix(J0m.T * A0i * J0m)[i, i]) for i in range(n)]
    return {'sigma2': dict(zip(NAMES, [Lam[i] / mu[i] for i in range(n)])), 'mu': dict(zip(NAMES, mu)), 'Lambda': dict(zip(NAMES, Lam)),
            'forcing': dict(zip(NAMES, fx)), 'R0': float(prov[0]['R'](np.array([1.0]))[0]), 'R1': float(prov[1]['R'](np.array([1.0]))[0]),
            'R2': float(prov[2]['R'](np.array([1.0]))[0]), 'd': {'d1': e1.get('p1**2*p1dd', 0), 'd2': e1.get('p1dd*r1**2', 0)},
            'equations': dict(zip(NAMES, out))}


def check():
    import nm_coeffs as NM
    fails = []
    for hR in (1.0, 3.2):
        R = 0.04; h = hR * R; Rf = lambda z: np.full_like(z, R)
        prov = {m: surface_mode(Rf, h, m) for m in (0, 1, 2)}
        a = derive(prov); b = NM.derive(hR)
        print(f'cylinder h/R = {hR}: d1 {a["d"]["d1"]:.6f} (Bessel {b["FLT_d"]["d1"]:.6f}), d2 {a["d"]["d2"]:.6f} (Bessel {b["FLT_d"]["d2"]:.6f}); '
              f'sigma1^2 {a["sigma2"]["p1"]:.6f} ({b["sigma2"]["p1"]:.6f}); shape fits within ' + ', '.join(f'{prov[m]["fit_res"]:.1e}' for m in (0, 1, 2)))
        # the finite-element shapes are +1 at the wall, the Bessel ones have the sign of J_M(k): coordinate i of one is s_i times
        # that of the other, so a coefficient of monomial prod x_j in the equation of x_i changes by s_i prod s_j
        sg = {'p0': np.sign(a['R0'] * b['R0']), 'p1': np.sign(a['R1'] * b['R1']), 'r1': np.sign(a['R1'] * b['R1']),
              'p2': np.sign(a['R2'] * b['R2']), 'r2': np.sign(a['R2'] * b['R2'])}
        def flip(eq, i):
            out = {}
            for k, v in eq.items():
                f = sg[i]
                for fac in k.split('*'):
                    if fac == '' or fac[0].isdigit(): continue
                    nm_, _, pw = fac.partition('**'); base = nm_.rstrip('d')
                    f *= sg.get(base, 1) ** (int(pw) if pw else 1)
                out[k] = v * f
            return out
        worst = 0.0; where = None
        for name in NAMES:
            ea, eb = a['equations'][name], flip(b['equations'][name], name)
            for k in set(ea) | set(eb):
                d = abs(ea.get(k, 0) - eb.get(k, 0))
                if d > worst: worst, where = d, (name, k, ea.get(k, 0), eb.get(k, 0))
        print(f'  every coefficient of the five equations (signs aligned {sg}): largest difference {worst:.1e} at {where}')
        if worst > 1e-3 or abs(a['d']['d1'] / b['FLT_d']['d1'] - 1) > 1e-4: fails.append(f'h/R {hR}')
    if abs(NM.derive(1.0)['FLT_d']['d1'] - 1.758023) > 1e-5: fails.append('FLT Table 1')
    return fails


def tulip(hs):
    dz, Rarr = FE.glass(); Rf = FE.profile_fn(dz, Rarr); res = {}
    for hmm in hs:
        h = hmm / 1000
        prov = {m: surface_mode(Rf, h, m) for m in (0, 1, 2)}
        a = derive(prov); a['h_mm'] = hmm; a['R_surface'] = prov[1]['Rs']; a['f'] = {m: prov[m]['f'] for m in (0, 1, 2)}
        a['wall_slope'] = float((Rf(np.array([h + 1e-4]))[0] - Rf(np.array([h - 1e-4]))[0]) / 2e-4)
        print(f'tulip h {hmm} mm (R {prov[1]["Rs"] * 1000:.2f} mm, wall slope {a["wall_slope"]:+.3f}): d1 {a["d"]["d1"]:.6f}, d2 {a["d"]["d2"]:.6f}, '
              f'sigma^2 ' + ', '.join(f'{k} {v:.5f}' for k, v in a['sigma2'].items()) + '; fits ' + ', '.join(f'{prov[m]["fit_res"]:.1e}' for m in (0, 1, 2)))
        res[str(hmm)] = a
    return res


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if what == 'check':
        f = check(); print('CHECK ' + ('PASSED' if not f else 'FAILED: ' + '; '.join(f))); sys.exit(1 if f else 0)
    out = tulip([float(x) for x in sys.argv[2:]] or [125.0])
    if os.environ.get('OUT'): json.dump(out, open(os.environ['OUT'], 'w'), indent=1)
