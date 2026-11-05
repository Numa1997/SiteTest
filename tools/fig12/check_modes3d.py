"""Gate for modes3d.py.
1. Cylinder R = 40 mm, D = 100 mm: eigenvalues against the exact lam = k tanh(kD), k = xi_mn / R, and Q_x against
   2R/((xi^2 - 1) J1(xi)) for (1,1); Green's identity E = lam N; the Stokes-Joukowski inertia converges with the mesh.
2. The glass with its panels switched off (A_PANEL = 0) against the axisymmetric solver modes.py on the same profile.
Run: python3 tools/fig12/check_modes3d.py
"""
import sys, os, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modes3d, modes, geom as G
from scipy.special import jn_zeros, jvp, jv
from scipy.optimize import brentq

def xi_mn(m, n):   # n-th nonzero zero of J_m'
    if m == 0: return jn_zeros(1, n)[n - 1]
    zs = []; x = 1e-3
    while len(zs) < n:
        a, b = x, x + 0.2
        if jvp(m, a) * jvp(m, b) < 0: zs.append(brentq(lambda t: jvp(m, t), a, b))
        x = b
    return zs[n - 1]

ok = True
R, D = 0.040, 0.100
t0 = time.time()
cyl = lambda z, th: np.full_like(np.asarray(th, float), R) if np.ndim(th) else R
Mc, mdc, _, rigc = modes3d.solve(cyl, 0.0, D, nmodes=12, Ns=6, Nt=24, Nz=16)
t1 = time.time(); M, md, chis, rig = modes3d.solve(cyl, 0.0, D, nmodes=12, Ns=8, Nt=28, Nz=18)
print(f'coarse mesh ({Mc.n} nodes) {t1-t0:.1f} s; production mesh ({M.n} nodes) {time.time()-t1:.1f} s')
print(f'cylinder: {M.n} nodes, {len(M.E)} elements, {time.time()-t0:.1f} s; volume {rig["V"]*1e6:.3f} mL (exact {np.pi*R*R*D*1e6:.3f})')
exact = []
for m in range(0, 9):
    for n in range(1, 5):
        xi = xi_mn(m, n); k = xi / R
        for _ in range(1 if m == 0 else 2): exact.append((m, n, k * np.tanh(k * D), xi))   # m >= 1: a cos and a sin copy
exact.sort(key=lambda t: t[2])
print('  mode   lam FEM      lam exact    rel.err   E/(lam N)')
worst = 0
for md_, (m, n, lam_ex, xi) in zip(md, exact[:len(md)]):
    rel = abs(md_['lam'] - lam_ex) / lam_ex
    if m <= 3: worst = max(worst, rel)                        # the page keeps m <= 3
    print(f'  ({m},{n})  {md_["lam"]:10.4f}  {lam_ex:10.4f}  {rel:9.2e}  {md_["E"]/(md_["lam"]*md_["N"]):.6f}' + ('' if m <= 3 else '   (not kept)'))
    if m <= 3 and abs(md_['E'] / (md_['lam'] * md_['N']) - 1) > 1e-3: ok = False
if worst > 3e-4: ok = False
# Q_x of the (1,1) pair: with max psi = 1 on the rim, Q_x = int psi x dS / int psi^2 dS = 2R/((xi^2-1)J1(xi)) for psi = J1(kr)cos th / J1(xi)
xi = xi_mn(1, 1); Qex = 2 * R / (xi * xi - 1)     # Q_x = int psi x dS / int psi^2 dS with psi = J1(kr) cos th / J1(xi): the wall-normalised value
pair = [x for x in md if abs(x['lam'] - exact[0][2]) / exact[0][2] < 1e-2]
Qs = sorted([np.hypot(x['Qx'], x['Qy']) for x in pair])
print(f'  (1,1) pair: |Q| = {Qs}, exact {Qex:.6f}; rel.err {abs(Qs[-1]-Qex)/Qex:.2e}')
if abs(Qs[-1] - Qex) / Qex > 5e-4: ok = False
# rigid parts
Jr = np.pi * R * R * D * (R * R / 4 + D * D / 12)            # rigid-body inertia of the liquid about a transverse axis through its centre, per rho
print(f'  Stokes-Joukowski J/rho about y through the foot: {rig["Jsj"]["ry"]:.4e} m^5; rigid about the centre {Jr:.4e}, rigid about the foot {Jr + np.pi*R*R*D*(D/2)**2:.4e}')
print(f'  coarse mesh: J_sj {rigc["Jsj"]["ry"]:.4e} (change to production {abs(rigc["Jsj"]["ry"]-rig["Jsj"]["ry"])/rig["Jsj"]["ry"]:.1e}); lam11 rel.err {abs(mdc[0]["lam"]-exact[0][2])/exact[0][2]:.1e}, lam of mode 9 rel.err {abs(mdc[8]["lam"]-exact[8][2])/exact[8][2]:.1e} against {abs(md[8]["lam"]-exact[8][2])/exact[8][2]:.1e}')
if abs(rigc["Jsj"]["ry"]-rig["Jsj"]["ry"])/rig["Jsj"]["ry"] > 1e-3: ok = False
# wall integral for (1,1): exact int_wall |grad_t Phi|^2 dS with Phi = J1(kr) cosh k z / (J1(xi) cosh kD) cos th
k = xi / R; zz = np.linspace(0, D, 4001); ch = np.cosh(k * zz) / np.cosh(k * D); sh = np.sinh(k * zz) / np.cosh(k * D)
# on the wall grad_t = (1/R) d/dth, d/dz: |.|^2 = (sin^2 th /R^2) ch^2 + k^2 sh^2 cos^2 th -> integrate over th: pi/R^2 ch^2 + pi k^2 sh^2, times R dz
Iw_ex = np.trapezoid((np.pi / R ** 2 * ch ** 2 + np.pi * k * k * sh ** 2) * R, zz)
m11 = [x for x in pair if abs(x['Qx']) > abs(x['Qy'])][0]
print(f'  (1,1) along x: Iw FEM {m11["Iw"]:.5f}, exact {Iw_ex:.5f}, rel.err {abs(m11["Iw"]-Iw_ex)/Iw_ex:.1e}; Q_ry {m11["Qry"]:.5f} m')
if abs(m11['Iw'] - Iw_ex) / Iw_ex > 1e-3: ok = False

# ---- 2. the glass without panels against the axisymmetric solver ----
G.A_PANEL = 0.0
zf = G.Z_F / 1000; Rfun3 = lambda z, th: G.R_inner(z * 1000, th) / 1000
Rfun2 = lambda z: np.interp(z, np.arange(zf, G.H / 1000, 1e-4), G.R_inner(np.arange(zf, G.H / 1000, 1e-4) * 1000, np.pi / 2) / 1000)
zs = 0.1441   # about 500 mL
t0 = time.time(); M3, md3, _, _ = modes3d.solve(Rfun3, zf, zs, nmodes=12, Ns=8, Nt=28, Nz=18)
print(f'glass, panels off: {time.time()-t0:.1f} s')
ref = []
for m, nk in {0: 2, 1: 3, 2: 2, 3: 2, 4: 1, 5: 1}.items():
    X, T, idx, res = modes.solve(Rfun2, zf, zs, m, nk, 16, 40)
    for n, r in enumerate(res, 1):
        I = modes.integrals(X, T, idx, r, Rfun2, zf, zs); c = 1 / r['f'][-1]
        for _ in range(1 if m == 0 else 2): ref.append((m, n, r['lam'], (I['Px'] * c) / (c * c) if m == 1 else 0.0))
ref.sort(key=lambda t: t[2])
print('  mode   lam 3D       lam axisym   rel.err')
worst2 = 0
for x, (m, n, lam2, Q2) in zip(md3, ref[:len(md3)]):
    rel = abs(x['lam'] - lam2) / lam2
    if m <= 3: worst2 = max(worst2, rel)
    print(f'  ({m},{n})  {x["lam"]:10.4f}  {lam2:10.4f}  {rel:9.2e}' + (f'   Q {np.hypot(x["Qx"], x["Qy"]):.5f} vs {Q2:.5f}' if m == 1 else ''))
if worst2 > 3e-4: ok = False
print('PASS' if ok else 'FAIL', f'cylinder worst {worst:.1e}, glass worst {worst2:.1e}')
sys.exit(0 if ok else 1)
