"""Checks of engine.RigidBlade, then L1 at the three winds (uniform rotation, the second blade at its best brake and around it).

Run: python3 -I L1_blade.py   (PASS/FAIL; exit 1 on any FAIL; writes L1_blade.json)
1. engine accelerations = Newton in the blade frame, slice by slice along the second blade (centrifugal, Coriolis, Euler,
   gravity, the hinge's edgewise acceleration), at random states: an independent route.
2. observed order of the Radau IIA engine on this system: successive differences at h, h/2, h/4, h/8, p = log2(d1/d2) -> 5.
3. SciPy DOP853 (rtol 1e-12) on the equation written again here from Newton's route: the mean power agrees.
4. The three winds at kappa/kappa* = 0.5, 1, 2: mean power, swing, mean trail and <sin theta>; the trail identity
   P = -(m l/2) r_p Omega^3 <sin theta> must hold to the integrator's error; at kappa* the power sits within 1 % of P*.
"""
import json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import RigidBlade, pendulum_rhs, integrate
import setup as S

g = S.G0
fails = 0
def check(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name, flush=True)

NS = 8                                               # Gauss-Legendre nodes along the blade: exact for the polynomials (degree <= 2) in s
GX, GW = np.polynomial.legendre.leggauss(NS)
def newton_acc(m, l, rp, c, ph, Om, Omd, ae, q, w):
    """Independent route: in the frame turning with the mother blade, sum the torque about the hinge of the fictitious forces,
    gravity and the hinge's edgewise acceleration on each slice dm = m/l ds, and divide by I = sum ds dm s^2."""
    s = (GX + 1)*l/2; dm = (m/l)*GW*l/2                # slice positions and masses (Gauss-Legendre weights)
    e = np.array([np.cos(q), np.sin(q)]); n = np.array([-np.sin(q), np.cos(q)])
    r = np.array([rp, 0.0])[:, None] + e[:, None]*s                # slice positions in the turning frame
    v = n[:, None]*s*w
    zx = lambda u: np.array([-u[1], u[0]])
    gb = g*np.array([-np.sin(ph), -np.cos(ph)])[:, None]            # lab "down" seen from the frame turned by phi
    f = dm*(Om**2*r - 2*Om*zx(v) - Omd*zx(r) + gb - ae*np.array([0.0, 1.0])[:, None])
    arm = e[:, None]*s
    torque = np.sum(arm[0]*f[1] - arm[1]*f[0]) - c*w
    Inum = np.sum(dm*s**2)
    return torque/Inum, Inum

# 1 ------------------------------------------------------------------------------------------------------------------
rng = np.random.default_rng(7); worst = 0
for _ in range(400):
    m, l, rp, c = rng.uniform(0.1, 3, 4); ph, Om, Omd, ae, q, w = rng.uniform(-3, 3, 6)
    acc, _ = RigidBlade(m, l, rp, c).acc(np.array([q]), np.array([w]), ph, Om, Omd, ae)
    ref, Inum = newton_acc(m, l, rp, c, ph, Om, Omd, ae, q, w)
    worst = max(worst, abs(acc[0] - ref)/(1 + abs(ref)), abs(Inum/(m*l*l/3) - 1))
check(f'1. RigidBlade accelerations = Newton summed over the blade (Gauss-Legendre, exact) in the blade frame at 400 random states, and the summed inertia = m l^2/3 (max rel diff {worst:.1e})', worst < 1e-12)

# 2 ------------------------------------------------------------------------------------------------------------------
v0 = 8.0; Om = S.omega(v0); rp = S.R_ROT; m, l = S.M_B, S.L_B
I, mlc = m*l*l/3, m*l/2
R = mlc*rp/I; kstar = R - 1; cstar = kstar*I*Om
blade = RigidBlade(m, l, rp, cstar); F = pendulum_rhs(blade, Om=Om)
Tt = 2*math.pi/Om; Tend = 3*Tt
ends = []
for n in (8, 16, 32, 64, 128):                       # steps per turn: coarse enough that the error stays above round-off
    ends.append(integrate(F, np.zeros((1, 3)), 0, Tend, Tt/n)['Y'][0, 0])
d = np.abs(np.diff(ends))
orders = [math.log2(d[i]/d[i + 1]) for i in range(len(d) - 1) if d[i + 1] > 1e-14]
print('   successive differences of theta(3 turns):', ', '.join(f'{x:.2e}' for x in d), '; orders', ', '.join(f'{p:.2f}' for p in orders))
p_mean = math.log2(d[0]/d[-1])/(len(d) - 1)            # the mean order over the halvings (all differences above 1e-11)
check(f'2. observed order of Radau IIA on the second blade: mean over 8 to 128 steps per turn {p_mean:.2f}, within 4.5 to 5.5 (single halvings scatter before the asymptotic range)',
      4.5 < p_mean < 5.5 and d[-1] > 1e-12)

# 3 ------------------------------------------------------------------------------------------------------------------
def rhs_newton(t, y):
    a, _ = newton_acc(m, l, rp, cstar, Om*t, Om, 0.0, 0.0, y[0], y[1])
    return [y[1], a, cstar*y[1]**2]
nt = 20
sol = solve_ivp(rhs_newton, (0, nt*Tt), [0.0, 0.0, 0.0], method='DOP853', rtol=1e-12, atol=1e-14, dense_output=True)
eng10 = integrate(F, np.zeros((1, 3)), 0, 10*Tt, Tt/240)
eng20 = integrate(F, eng10['Y'], 10*Tt, nt*Tt, Tt/240)
E_eng = eng20['Y'][0, 2] - eng10['Y'][0, 2]; E_ref = sol.sol(nt*Tt)[2] - sol.sol(10*Tt)[2]
rel = abs(E_eng/E_ref - 1)
check(f'3. harvested energy over turns 10 to 20 at 240 steps per turn: engine {E_eng:.10f} J, SciPy DOP853 on Newton\'s route {E_ref:.10f} J (rel diff {rel:.1e})', rel < 1e-8)
# the start from rest: the brake relaxes in 1/(kappa* Omega), shorter than one step, so the first turns carry a start-up error
# that dies away; it is stated here and it does not reach the measured means (60 turns of settling).
eng_full = eng20['Y'][0, 2]; rel0 = abs(eng_full/sol.y[2, -1] - 1)
print(f'   from rest, turns 0 to 20: engine {eng_full:.9f} J against {sol.y[2, -1]:.9f} J (rel diff {rel0:.1e}): the start-up error, '
      f'relaxation time 1/(kappa* Omega) = {1/(kstar*Om):.4f} s against a step of {Tt/240:.4f} s')
relax8, step8, turn8 = 1/(kstar*Om), Tt/240, Tt                 # at 8 m/s, before the loop below reuses the names

# 4 ------------------------------------------------------------------------------------------------------------------
SETTLE, MEAS, STEPS = 60, 40, 240
out = []
for v, Om, rp in S.mountings():
    Tt = 2*math.pi/Om; h = Tt/STEPS
    R = mlc*rp/I; kstar = R - 1; Pst = S.pstar(Om)
    for mult in (0.5, 1.0, 2.0):
        c = mult*kstar*I*Om
        F = pendulum_rhs(RigidBlade(m, l, rp, c), Om=Om)
        r1 = integrate(F, np.zeros((1, 3)), 0, SETTLE*Tt, h)
        r2 = integrate(F, r1['Y'], SETTLE*Tt, (SETTLE + MEAS)*Tt, h, record_every=1)
        qs = np.array([y[0, 0] for _, y in r2['rec']])
        P = (r2['Y'][0, 2] - r1['Y'][0, 2])/(MEAS*Tt)
        trail, trailSin = qs.mean(), np.sin(qs).mean()
        bill = -mlc*rp*Om**3*trailSin
        out.append(dict(wind=v, Om=Om, rp=rp, mult=mult, c=c, P=P, Theta=0.5*(qs.max() - qs.min()), trail=trail, trailSin=trailSin,
                        bill=bill, Pstar=Pst, kstar=kstar, steps_per_turn=STEPS, settle=SETTLE, measure=MEAS, m=m, l=l))
        print(f'   {v:.0f} m/s, kappa = {mult} kappa*: P {P*1e3:9.4f} mW (P* {Pst*1e3:8.4f}), swing {0.5*(qs.max()-qs.min()):.5f} rad, '
              f'trail {trail:+.3e} rad, bill {bill*1e3:9.4f} mW')
check('4a. the trail identity P = -(m l/2) r_p Omega^3 <sin theta> holds at every run to 0.1 %',
      all(abs(r['bill']/r['P'] - 1) < 1e-3 for r in out))
check('4b. at kappa* the full equation gives P* within 1 % at every wind',
      all(abs(r['P']/r['Pstar'] - 1) < 0.01 for r in out if r['mult'] == 1.0))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L1_blade.json'), 'w'), indent=1)
json.dump(dict(newton_max_rel=worst, order_mean=p_mean, orders=orders, scipy_rel=rel, startup_rel=rel0,
               relax_s=relax8, step_s=step8, turn_s=turn8, bill_max_rel=max(abs(r['bill']/r['P'] - 1) for r in out)),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L1_blade_checks.json'), 'w'), indent=1)
print('ALL PASS' if not fails else f'{fails} FAIL')
raise SystemExit(1 if fails else 0)
