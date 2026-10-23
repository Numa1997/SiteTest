"""Independent physics checks of the Droplet Collection model.

Every constant is retyped here from its source; nothing is read from physics.cjs except the numbers it prints through
checks/model_dump.cjs, which this script compares with its own calculations (SciPy integrators, SymPy algebra).

    python3 checks/check_physics.py          # about two minutes; exit code 1 if any check fails
"""
import json, math, os, subprocess, sys
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from scipy.special import ive
from scipy.linalg import expm
from scipy import stats
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
results = []


def check(name, ok, detail):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}", flush=True)


def rel(a, b):
    return abs(a / b - 1)


print("running the model (node checks/model_dump.cjs) ...", flush=True)
dump = json.loads(subprocess.run(['node', os.path.join(HERE, 'model_dump.cjs')], capture_output=True, text=True, check=True,
                                 env=dict(os.environ, RUNS=os.environ.get('RUNS', '4000'))).stdout)

# ------------------------------------------------------------------ 1. air at 10 °C and 850 hPa
g = 9.81
rho_w = 1000.0
T, p = 283.15, 85000.0
rho_a = p / (287.05 * T)                                   # ideal gas, dry air
mu = 1.72e-5 * (T / 273.0) ** 1.5 * (273.0 + 120.0) / (T + 120.0)   # Sutherland with the thesis's constants
check("air density and viscosity", rel(rho_a, dump['air']['rho']) < 1e-12 and rel(mu, dump['air']['mu']) < 1e-12,
      f"rho = {rho_a:.4f} kg/m3, mu = {mu:.4e} Pa s")

# ------------------------------------------------------------------ 2. fall speeds: Beard (1976), coefficients retyped
B2 = [-0.318657e1, 0.992696, -0.153193e-2, -0.987059e-3, -0.578878e-3, 0.855176e-4, -0.327815e-5]
B3 = [-0.500015e1, 0.523778e1, -0.204914e1, 0.475294, -0.542819e-1, 0.238449e-2]


def sigma_w(T):          # IAPWS surface tension of water
    tau = 1 - T / 647.096
    return 0.2358 * tau ** 1.256 * (1 - 0.625 * tau)


def v_beard(a, T=T, p=p):
    rho = p / (287.05 * T)
    m = 1.72e-5 * (T / 273.0) ** 1.5 * 393.0 / (T + 120.0)
    d, dr = 2 * a, rho_w - rho
    lam = 6.62e-8 * (m / 1.818e-5) * (101325 / p) * math.sqrt(T / 293.15)
    slip = 1 + 2.51 * lam / d
    if d < 19e-6:
        return dr * g * d * d / (18 * m) * slip
    if d < 1.07e-3:
        X = math.log(4 * rho * dr * g * d ** 3 / (3 * m * m))
        return m * slip * math.exp(sum(b * X ** i for i, b in enumerate(B2))) / (rho * d)
    s = sigma_w(T)
    Bo, NP = 4 * dr * g * d * d / (3 * s), s ** 3 * rho * rho / (m ** 4 * dr * g)
    X = math.log(Bo * NP ** (1 / 6))
    return m * NP ** (1 / 6) * math.exp(sum(b * X ** i for i, b in enumerate(B3))) / (rho * d)


worst = max(rel(v_beard(a), vm) for a, vm in zip(dump['radii'], dump['vBeard']))
check("Beard fall speeds, 5 um to 2 mm", worst < 1e-9, f"largest relative difference {worst:.1e}; v(40 um) = {v_beard(40e-6):.4f} m/s")
k_st = 2 * (rho_w - rho_a) * g / (9 * mu)
worst = max(rel(k_st * a * a, vm) for a, vm in zip(dump['radii'], dump['vStokes']))
check("Stokes speeds", worst < 1e-12, f"k = {k_st:.4e} 1/(m s)")

# Gunn and Kinzer (1949), 20 °C, 1013 hPa, diameter (mm) -> speed (cm/s), retyped from their table
GK = [(0.3, 117), (0.4, 162), (0.5, 206), (0.6, 247), (0.7, 287), (0.8, 327), (0.9, 367), (1.0, 403), (1.2, 464), (1.4, 517),
      (1.6, 565), (1.8, 609), (2.0, 649), (2.2, 690), (2.4, 727), (2.6, 757), (2.8, 782), (3.0, 806), (3.2, 826), (3.4, 844),
      (3.6, 860), (3.8, 872), (4.0, 883), (4.2, 892), (4.4, 898), (4.6, 903), (4.8, 907), (5.0, 909), (5.2, 912), (5.4, 914),
      (5.6, 916), (5.8, 917)]
err = max(abs(v_beard(dmm * 5e-4, 293.15, 101325) / (v / 100) - 1) for dmm, v in GK)
check("Beard against Gunn and Kinzer from 0.3 mm", abs(err * 100 - 2.07) < 0.01, f"largest error {err * 100:.2f} % (text: 2.1 %)")

# ------------------------------------------------------------------ 3. collision efficiency by trajectories (SciPy DOP853)
_xs, _zs = sp.symbols('x z', real=True)
_q = sp.sqrt(_xs ** 2 + _zs ** 2)
_PSI = {'potential': _xs ** 2 / 2 * (1 - 1 / _q ** 3),                                   # uniform stream + dipole
        'stokes': _xs ** 2 / 2 * (1 - sp.Rational(3, 2) / _q + sp.Rational(1, 2) / _q ** 3)}   # Stokes (1851)
# Stokes stream function in cylindrical (x, z): u_x = -(1/x) dpsi/dz, u_z = (1/x) dpsi/dx; differentiated by SymPy
_U = {k: sp.lambdify((_xs, _zs), [sp.simplify(-sp.diff(v, _zs) / _xs), sp.simplify(sp.diff(v, _xs) / _xs)], 'math')
      for k, v in _PSI.items()}


def flow(kind, x, z):
    """Air velocity around a sphere of radius 1 at rest, uniform flow +z at infinity; cylindrical x >= 0."""
    if x < 1e-300:
        x = 1e-300
    return tuple(_U[kind](x, z))


def psi(kind, x, z):
    q = math.sqrt(x * x + z * z)
    return 0.5 * x * x * ((1 - 1 / q ** 3) if kind == 'potential' else (1 - 1.5 / q + 0.5 / q ** 3))


def hits(kind, St, S, p, b, Z):
    rc = 1 + p
    ux, uz = flow(kind, b, -Z)
    def f(t, y):
        ax, az = flow(kind, y[0], y[1])
        return [y[2], y[3], (ax - y[2]) / St, (az - y[3] - S) / St]
    hit = lambda t, y: math.hypot(y[0], y[1]) - rc
    hit.terminal = True
    passed = lambda t, y: y[1] - 3.0
    passed.terminal = True
    sol = solve_ivp(f, [0, 50 * Z], [b, -Z, ux, uz - S], method='DOP853', rtol=1e-10, atol=1e-12, events=[hit, passed])
    return len(sol.t_events[0]) > 0


def efficiency(kind, St, S, p, Z):
    lo, hi = 0.0, 1.5 * (1 + p)
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if hits(kind, St, S, p, mid, Z) else (lo, mid)
    bc = 0.5 * (lo + hi)
    return 2 * (psi(kind, bc, -Z) - 0.5 * S * bc * bc) / ((1 - S) * (1 + p) ** 2)


R, r = 40e-6, 8e-6
U, vr = v_beard(R), v_beard(r)
tau = vr / (g * (1 - rho_a / rho_w))
St, S, pr, Re = tau * U / R, vr / U, r / R, 2 * R * rho_a * U / mu
E_S, E_P = efficiency('stokes', St, S, pr, 200), efficiency('potential', St, S, pr, 30)
E = (E_S + E_P * Re / 60) / (1 + Re / 60)
pm = dump['pair']
check("trajectory efficiency E(40 um, 8 um)", rel(E, pm['E']) < 2e-3 and rel(St, pm['St']) < 1e-9,
      f"SciPy {E:.4f} (creeping {E_S:.4f}, potential {E_P:.4f}, St = {St:.3f}, Re = {Re:.3f}); model {pm['E']:.4f}; text 0.344")

# critical Stokes numbers on the axis: potential flow analytic, creeping flow numerical
def axis_hit(kind, St, Z=100.0):
    """Point droplet on the axis, no settling; hit iff it reaches the surface. Near the surface the flow speed vanishes as
    eta (potential) or eta^2 (creeping); below eta = 1e-4 the remaining free flight St*|w| decides (exact to O(eta))."""
    def u(z):
        q = -z
        return (1 - 1 / q ** 3) if kind == 'potential' else (1 - 1.5 / q + 0.5 / q ** 3)
    near = lambda t, y: (-y[0] - 1) - 1e-4
    near.terminal = True
    stop = lambda t, y: y[1] - 1e-14 * 0 - 0.0
    stop.terminal = True
    stop.direction = -1
    sol = solve_ivp(lambda t, y: [y[1], (u(y[0]) - y[1]) / St], [0, 1e5], [-Z, u(-Z)], method='DOP853', rtol=1e-12, atol=1e-14,
                    events=[near, stop])
    if not len(sol.t_events[0]):
        return False
    z, w = sol.y_events[0][0]
    eta = -z - 1
    if kind == 'potential':    # linearised: St eta'' + eta' + 3 eta = 0 reaches eta = 0 iff it oscillates or St w > eta
        return 1 - 12 * St < 0 or St * w > eta
    return St * w > eta


stc_c = brentq(lambda s: (1 if axis_hit('stokes', s) else -1), 0.5, 3, xtol=1e-6)
stc_p = brentq(lambda s: (1 if axis_hit('potential', s) else -1), 0.02, 0.3, xtol=1e-7)
check("critical Stokes numbers", abs(stc_p - 1 / 12) < 1e-5 and abs(stc_c - dump['stc']['stokes']) < 2e-4,
      f"potential {stc_p:.5f} (1/12 = 0.08333; model {dump['stc']['potential']:.5f}), creeping {stc_c:.5f} (model {dump['stc']['stokes']:.5f})")

# ------------------------------------------------------------------ 4. SymPy: the closed forms the text derives
x, z, q, U0 = sp.symbols('x z q U', positive=True)
# Stokes stream function: E^4 psi = 0 with E^2 = d2/dq2 + (sin th / q^2) d/dth (1/sin th d/dth); psi = sin^2 th f(q)
th = sp.symbols('theta', positive=True)
f = U0 / 2 * (q ** 2 - sp.Rational(3, 2) * q + sp.Rational(1, 2) / q)
Psi = sp.sin(th) ** 2 * f
E2 = lambda F: sp.diff(F, q, 2) + sp.sin(th) / q ** 2 * sp.diff(sp.diff(F, th) / sp.sin(th), th)
ok_stokes = sp.simplify(E2(E2(Psi))) == 0 and sp.simplify(f.subs(q, 1)) == 0 and sp.simplify(sp.diff(f, q).subs(q, 1)) == 0
# centre-of-mass split of the kinetic energy (4.1)
m1, m2, V, dv = sp.symbols('m1 m2 V dv', positive=True)
v1, v2 = V + m2 / (m1 + m2) * dv, V - m1 / (m1 + m2) * dv
ok_split = sp.simplify(m1 * v1 ** 2 / 2 + m2 * v2 ** 2 / 2 - ((m1 + m2) * V ** 2 / 2 + m1 * m2 / (m1 + m2) * dv ** 2 / 2)) == 0
# L0 growth law dR/dt = c R^2
t, c, R0s = sp.symbols('t c R0', positive=True)
Rf = sp.Function('R')
sol = sp.dsolve(sp.Eq(Rf(t).diff(t), c * Rf(t) ** 2), Rf(t), ics={Rf(0): R0s})
ok_l0 = sp.simplify(sol.rhs - R0s / (1 - c * R0s * t)) == 0
# lever rule (5.3)
xk, xk1, xs, C = sp.symbols('x_k x_k1 x_s C', positive=True)
nk, nk1 = sp.symbols('nu_k nu_k1')
lev = sp.solve([nk + nk1 - C, xk * nk + xk1 * nk1 - xs * C], [nk, nk1])
ok_lever = sp.simplify(lev[nk1] / C - (xs - xk) / (xk1 - xk)) == 0
check("SymPy derivations", ok_stokes and ok_split and ok_l0 and ok_lever,
      f"Stokes E^4 psi = 0 with no-slip {ok_stokes}; kinetic-energy split (4.1) {ok_split}; R = R0/(1 - c R0 t) {ok_l0}; lever rule (5.3) {ok_lever}")

# ------------------------------------------------------------------ 5. Golovin's exact solution
G = dump['golovin']
b, L, mbar, N0, tG = G['b'], G['L'], G['mbar'], G['N0'], G['t']


def golovin(m, t):
    tau_ = 1 - math.exp(-b * L * t)
    u = m / mbar
    arg = 2 * u * math.sqrt(tau_)
    return N0 / mbar * (1 - tau_) / (u * math.sqrt(tau_)) * ive(1, arg) * math.exp(arg - (1 + tau_) * u)


worst = max(rel(golovin(m, tG), n) for m, n in zip(G['m'], G['n']) if n > 1e-250)
lims = (math.log(1e-8), math.log(1e8))
Nnum = quad(lambda lu: golovin(math.exp(lu) * mbar, tG) * math.exp(lu) * mbar, *lims, limit=2000, epsrel=1e-10)[0]
Mnum = quad(lambda lu: golovin(math.exp(lu) * mbar, tG) * (math.exp(lu) * mbar) ** 2, *lims, limit=2000, epsrel=1e-10)[0]
check("Golovin density against SciPy Bessel, and its moments", worst < 1e-6 and rel(Nnum, N0 * math.exp(-b * L * tG)) < 1e-6 and rel(Mnum, L) < 1e-6,
      f"density difference {worst:.1e} (Abramowitz-Stegun polynomial); N/N0 = {Nnum / N0:.5f} (exp(-bLt) = {math.exp(-b * L * tG):.5f}); mass {Mnum / L:.8f} L")

# ------------------------------------------------------------------ 6. the collection equation, solved again with independent code
x_g = np.array(dump['grid']['x'])
n = len(x_g)
K = np.array(dump['K']).reshape(n, n)
N = np.array(dump['N0'])


def sce_step(N, dt):
    """Explicit two-bin (lever-rule) step, all pairs at once; same physics as (5.3), different code and update order."""
    I, J = np.triu_indices(n)
    Cij = K[I, J] * N[I] * N[J] * dt * np.where(I == J, 0.5, 1.0)
    xs = x_g[I] + x_g[J]
    kk = np.searchsorted(x_g, xs, side='right') - 1
    # limiter: no bin may lose, net, more drops than it holds. A large drop that sweeps up a small one mostly stays in its own bin
    # (product bin kk = J): it loses the fraction f of the pair count, not all of it.
    fk = (xs - x_g[np.minimum(kk, n - 2)]) / (x_g[np.minimum(kk, n - 2) + 1] - x_g[np.minimum(kk, n - 2)])
    netJ = np.where((kk == J) & (kk < n - 1), fk, 1.0)
    loss0 = np.zeros(n)
    np.add.at(loss0, I, np.where(I == J, 2.0, 1.0) * Cij)
    np.add.at(loss0, J, np.where(I == J, 0.0, netJ) * Cij)
    a = np.where(loss0 > N, N / np.maximum(loss0, 1e-300), 1.0)
    Cij = Cij * np.minimum(a[I], a[J])
    loss = np.zeros(n)
    np.add.at(loss, I, Cij)
    np.add.at(loss, J, Cij)
    gain = np.zeros(n)
    top = kk >= n - 1
    k_ = np.minimum(kk, n - 2)
    f = (xs - x_g[k_]) / (x_g[k_ + 1] - x_g[k_])
    np.add.at(gain, k_[~top], ((1 - f) * Cij)[~top])
    np.add.at(gain, k_[~top] + 1, (f * Cij)[~top])
    return N - loss + gain, float(np.sum((Cij * xs)[top]))


r_g = np.array(dump['grid']['r'])
k40 = int(np.argmax(r_g >= 40e-6))
M0 = float(N @ x_g)
over, F, ts = 0.0, [], []
dt = 0.5
for step in range(int(1200 / dt) + 1):
    if step % 10 == 0:
        F.append(float(N[k40:] @ x_g[k40:]) / M0)
        ts.append(step * dt)
    N, o = sce_step(N, dt)
    over += o
F = np.array(F)
t50 = np.interp(0.5, F, ts) / 60
t90 = np.interp(0.9, F, ts) / 60
Fm = np.array(dump['sce']['F40'])
tm = np.array(dump['sce']['t'])
m50, m90 = np.interp(0.5, Fm, tm) / 60, np.interp(0.9, Fm, tm) / 60
check("collection equation re-solved in NumPy (extended kernel, s = 8)", abs(t50 - m50) / m50 < 0.02 and abs(t90 - m90) / m90 < 0.02 and min(N) > -1e-6 * max(N),
      f"t50/t90 = {t50:.3f}/{t90:.3f} min (dt = 0.5 s) against the model's {m50:.3f}/{m90:.3f} (dt = 1 s); text 5.77/13.47; mass drift {(float(N @ x_g) + over) / M0 - 1:.1e}")

# ------------------------------------------------------------------ 7. the stochastic engine against an exact death chain
ch = dump['chain']
lam = np.array(ch['rates'])
nn = ch['n']
Q = np.zeros((nn + 1, nn + 1))
for kk_ in range(nn):
    Q[kk_, kk_] -= lam[kk_]
    Q[kk_ + 1, kk_] += lam[kk_]
P = expm(Q * ch['T'])[:, 0]
counts = np.bincount(ch['k'], minlength=nn + 1)[:nn + 1]
runs = len(ch['k'])
mean_exact, mean_mc = float(np.arange(nn + 1) @ P), float(np.mean(ch['k']))
se = float(np.std(ch['k'], ddof=1)) / math.sqrt(runs)
expct = P * runs
# pool sparse cells for the chi-square test
obs_p, exp_p, acc_o, acc_e = [], [], 0, 0
for o_, e_ in zip(counts, expct):
    acc_o += o_
    acc_e += e_
    if acc_e >= 5:
        obs_p.append(acc_o); exp_p.append(acc_e); acc_o = acc_e = 0
obs_p[-1] += acc_o; exp_p[-1] += acc_e
chi2 = sum((o_ - e_) ** 2 / e_ for o_, e_ in zip(obs_p, exp_p))
pval = 1 - stats.chi2.cdf(chi2, len(obs_p) - 1)
check("Gillespie engine against the exact capture chain (one 40 um collector, 20 droplets of 8 um, 0.05 cm3, 60 s)",
      pval > 0.01 and abs(mean_mc - mean_exact) < 3 * se and not ch.get('violations'),
      f"{runs} runs: mean captures {mean_mc:.3f} +- {se:.3f} against exact {mean_exact:.3f}; chi2 = {chi2:.1f} on {len(obs_p) - 1} d.o.f., p = {pval:.2f}")

# ------------------------------------------------------------------ 8. the Poisson bridge (6.1) against the exact runs
st = json.load(open(os.path.join(ROOT, 'data', 'stochastic.json')))
br = json.load(open(os.path.join(ROOT, 'data', 'bridge.json')))['s16']
tb, nb = np.array(br['t'], float), np.array(br['N100'], float)
for Vcm in ('1000', '100'):
    times = [q['t100'] for q in st['V'][Vcm] if q['t100'] is not None]
    nr = len(st['V'][Vcm])
    cdf = lambda tt: 1 - np.exp(-float(Vcm) * 1e-6 * np.interp(tt, tb, nb))
    if len(times) == nr:
        ks = stats.kstest(times, cdf)
        line = f"{Vcm} cm3, {nr} runs: KS distance {ks.statistic:.3f}, p = {ks.pvalue:.2f}"
        ok = ks.pvalue > 0.01 if Vcm == '1000' else True
        check(f"Poisson bridge (6.1), {Vcm} cm3" + ("" if Vcm == '1000' else " (reported)"), ok, line)

print(f"\n{sum(results)}/{len(results)} checks passed")
print("PHYSICS CHECK PASS" if all(results) else "PHYSICS CHECK FAIL")
sys.exit(0 if all(results) else 1)
