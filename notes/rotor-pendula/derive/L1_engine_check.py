"""Checks of engine.py, then L1 at the 18 mountings (uniform rotation, single and double at equal mass and reach).

Run: python3 -I L1_engine_check.py   (PASS/FAIL; exit 1 on any FAIL; writes L1_mountings.json)
1. engine accelerations (+ generator torques) = Newton in the blade frame at random states (independent route).
2. observed order of the Radau IIA engine: successive differences at h, h/2, h/4, h/8, p = log2(d1/d2) -> 5.
3. SciPy DOP853 (rtol 1e-11) on the same equations, written again here from Newton's route: mean power agrees.
4. The 18 mountings at the best brakes: single and double powers.
"""
import json, math, os, sys, time
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Double, Single, pendulum_rhs, integrate

g = 9.80665
fails = 0
def check(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name, flush=True)

def newton_acc(p, ph, Om, Omd, ae, a1, a2, w1, w2):
    """Independent route: fictitious forces in the blade frame, projected (d'Alembert). p = (m1, m2, l1, l2, rp, c0, c1)."""
    m1, m2, l1, l2, rp, c0, c1 = p
    e1 = np.array([np.cos(a1), np.sin(a1)]); n1 = np.array([-np.sin(a1), np.cos(a1)])
    e2 = np.array([np.cos(a2), np.sin(a2)]); n2 = np.array([-np.sin(a2), np.cos(a2)])
    r1 = np.array([rp, 0.0]) + l1*e1; r2 = r1 + l2*e2
    v1 = l1*w1*n1; v2 = v1 + l2*w2*n2
    J1 = np.array([l1*n1, [0, 0]]).T; J2 = np.array([l1*n1, l2*n2]).T
    Jd1 = -l1*w1**2*e1; Jd2 = Jd1 - l2*w2**2*e2
    zx = lambda v: np.array([-v[1], v[0]])
    gb = g*np.array([-np.sin(ph), -np.cos(ph)]) - ae*np.array([0.0, 1.0])   # gravity and the pivot's edgewise shaking
    f = lambda m, r, v: m*(Om**2*r - 2*Om*zx(v) - Omd*zx(r) + gb)
    M = m1*J1.T@J1 + m2*J2.T@J2
    rhs = J1.T@(f(m1, r1, v1) - m1*Jd1) + J2.T@(f(m2, r2, v2) - m2*Jd2) - np.array([c0*w1 - c1*(w2 - w1), c1*(w2 - w1)])
    return np.linalg.solve(M, rhs)

# 1 ------------------------------------------------------------------------------------------------------------------
rng = np.random.default_rng(5); worst = 0
for _ in range(400):
    p = rng.uniform(0.05, 2, 7); ph, Om, Omd, ae, a1, a2, w1, w2 = rng.uniform(-3, 3, 8)
    acc, _ = Double(*p).acc(np.array([a1, a2]), np.array([w1, w2]), ph, Om, Omd, ae)
    ref = newton_acc(p, ph, Om, Omd, ae, a1, a2, w1, w2)
    worst = max(worst, np.max(np.abs(acc - ref))/(1 + np.max(np.abs(ref))))
check(f'1. engine accelerations = Newton in the blade frame (Coriolis, Euler, edgewise shaking) at 400 random states '
      f'(max rel diff {worst:.1e})', worst < 1e-12)

def mean_power(sysobj, Om, n, N_dis, N_avg, Y0=None):
    """mean generator power over turns N_dis..N_dis+N_avg, n steps per turn; returns power (N,) and final state"""
    Tt = 2*math.pi/Om; h = Tt/n; F = pendulum_rhs(sysobj, Om=Om)
    if Y0 is None:
        Y0 = np.zeros((np.broadcast(sysobj.rp).shape[0] if np.ndim(sysobj.rp) else 1, 2*sysobj.n + 1))
    r1 = integrate(F, Y0, 0, N_dis*Tt, h)
    r2 = integrate(F, r1['Y'], N_dis*Tt, (N_dis + N_avg)*Tt, h)
    return (r2['Y'][:, -1] - r1['Y'][:, -1])/(N_avg*Tt), r2['Y']

# 2, 3: a case that is not trivially periodic: the chaos group, R = 1, G = 3.0646, regular branch c = 0.022 N m s
Om = 4.0; p = (0.05, 0.05, 0.1, 0.1, 0.2, 0.022, 0.022)
sysd = Double(*p); Tturn = 2*math.pi/Om; T = 20*Tturn
F = pendulum_rhs(sysd, Om=Om)
finals = []
for n in (25, 50, 100, 200, 400):
    finals.append(integrate(F, np.zeros((1, 5)), 0, T, Tturn/n)['Y'][0])
dd = [np.max(np.abs(finals[i + 1][:4] - finals[i][:4])) for i in range(4)]
ps = [math.log2(dd[i]/dd[i + 1]) for i in range(3)]
print('   successive differences of the final state: ' + ', '.join(f'{x:.2e}' for x in dd) + '; orders ' + ', '.join(f'{x:.2f}' for x in ps))
check(f'2. observed order of the Radau IIA engine near 5 in the asymptotic range (got {ps[1]:.2f}, {ps[2]:.2f})',
      min(ps[1:]) > 4.0)
def rhs(t, y):
    a = newton_acc(p, Om*t, Om, 0.0, 0.0, y[0], y[1], y[2], y[3])
    harvest = p[5]*y[2]**2 + p[6]*(y[3] - y[2])**2
    return [y[2], y[3], a[0], a[1], harvest]
t_sc = time.time()
sol = solve_ivp(rhs, (0, T), [0, 0, 0, 0, 0], method='DOP853', rtol=1e-11, atol=1e-12, dense_output=True)
Pscipy = (sol.y[4, -1] - sol.sol(T/2)[4])/(T/2)
r1 = integrate(F, np.zeros((1, 5)), 0, T/2, Tturn/200); r2 = integrate(F, r1['Y'], T/2, T, Tturn/200)
Peng = (r2['Y'][0, -1] - r1['Y'][0, -1])/(T/2)
print(f'   mean power over turns 10-20: engine {Peng*1e3:.6f} mW, SciPy DOP853 {Pscipy*1e3:.6f} mW ({time.time()-t_sc:.0f} s)')
check(f'3. engine mean power = SciPy DOP853 on the Newton route (rel diff {abs(Peng/Pscipy - 1):.1e} < 1e-6)', abs(Peng/Pscipy - 1) < 1e-6)

# 4 ------------------------------------------------------------------------------------------------------------------
# The 18 mountings at our own brakes: single kappa* = R - 1 (2.4); double kappa* from its small-swing theory (L1_map.py).
from L1_map import kappa_star as kappa_star_double
import setup as S
M, L = S.M, S.L
results = []
t_all = time.time()
N_dis, N_avg = 60, 40
def run_wind(v, nturn):
    Om = S.omega(v)
    rps = np.array(S.FRACS)*S.R_ROT
    cs = np.array([(rp/L - 1)*M*L**2*Om for rp in rps])
    cd = np.array([kappa_star_double(rp/L)*M*L**2*Om for rp in rps])
    Ps_, Ys = mean_power(Single(M, L, rps, cs), Om, nturn, N_dis, N_avg, np.zeros((3, 3)))
    Pd_, Yd = mean_power(Double(M/2, M/2, L/2, L/2, rps, cd, cd), Om, nturn, N_dis, N_avg, np.zeros((3, 5)))
    return Om, rps, cs, cd, Ps_, Pd_
worst_conv = 0.0
for v in S.WINDS:
    Om, rps, cs, cd, Ps_, Pd_ = run_wind(v, 50)              # steps per turn
    _, _, _, _, Ps2, Pd2 = run_wind(v, 100)
    worst_conv = max(worst_conv, float(np.max(np.abs(Ps2/Ps_ - 1))), float(np.max(np.abs(Pd2/Pd_ - 1))))
    for i, f in enumerate(S.FRACS):
        Ps, Pd = Ps_[i], Pd_[i]; pct = round(f*100); rpm = S.rpm(v)
        results.append(dict(wind=v, rpm=rpm, pct=pct, Om=Om, rp=rps[i], c_single=cs[i], c_double=cd[i], P_single=Ps, P_double=Pd,
                            steps_per_turn=50))
        print(f'   {v:.0f} m/s ({rpm:.2f} rpm) {pct} %: single {Ps*1e3:8.4f} mW, double {Pd*1e3:8.4f} mW, ratio {Pd/Ps:.4f}', flush=True)
check(f'4. 50 against 100 steps per turn agree (worst {worst_conv:.1e} < 1e-4)', worst_conv < 1e-4)
print(f'   ({time.time() - t_all:.0f} s)')
json.dump(results, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L1_mountings.json'), 'w'), indent=1)
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
