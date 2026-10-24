"""Monte Carlo check of the power theorem (brief 4.3): mean dissipated power = (S/2) <m_eff> for white-noise shaking.

Run: python3 -I power_theorem_mc.py [--quick]     (prints PASS/FAIL; exit 1 on any FAIL)

The single pendulum of setup.py (0.5 kg on 0.1 m) and its double (two halves of the mass on two halves of the reach)
hang in gravity (damping ratio 0.2 of the lowest mode); the pivot is shaken horizontally (e = x) with white-noise acceleration a(t) of two-sided intensity S,
<a(t) a(t')> = S delta(t - t').  Generators brake the pivot joint (and the hinge) viscously.

Scheme: Euler-Maruyama in the noise, with the semi-implicit (symplectic) Euler update for the deterministic part
(velocity first, then angle with the new velocity), so that the conservative part has no secular energy drift.  Weak order 1;
run at dt and dt/2 to see the discretisation error.  Ensembles of N independent trajectories, seeds fixed below.
Per trajectory, time averages over a window after a transient of several damping times:
  P_diss = c1 psi1dot^2 + c2 (psi2dot - psi1dot)^2,   P_inj = (S/2) m_eff(q),   dE/T = energy change over the window / T.
Energy book: P_inj - P_diss - dE/T = 0 up to O(dt) and statistics.  The test asked by the brief: |P_diss/P_inj - 1| < 3 %.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup as SU
import numpy as np

g = 9.81
QUICK = '--quick' in sys.argv

def run_single(S, c, N, T_tr, T_win, dt, seed, m=0.1, L=0.2):
    rng = np.random.default_rng(seed)
    th = np.zeros(N); w = np.zeros(N)
    I = m*L**2
    n_tr, n_win = int(T_tr/dt), int(T_win/dt)
    Pd = np.zeros(N); Pi = np.zeros(N)
    sq = np.sqrt(S*dt)
    def energy(th, w): return 0.5*I*w**2 - m*g*L*np.cos(th)
    for k in range(n_tr + n_win):
        if k == n_tr: E0 = energy(th, w)
        b = m*L*np.cos(th)                     # b = m e.dx/dtheta, x = L(sin th, -cos th), e = (1, 0)
        if k >= n_tr:
            Pd += c*w**2
            Pi += 0.5*S*b**2/I
        acc = (-m*g*L*np.sin(th) - c*w)/I
        w = w + acc*dt - (b/I)*sq*rng.standard_normal(N)
        th = th + w*dt
    E1 = energy(th, w)
    return Pd/n_win, Pi/n_win, (E1 - E0)/T_win, np.sqrt(np.mean(np.sin(th/2)**2))*2

def run_double(S, c1, c2, N, T_tr, T_win, dt, seed, m1=0.05, m2=0.05, L1=0.1, L2=0.1):
    rng = np.random.default_rng(seed)
    p1 = np.zeros(N); p2 = np.zeros(N); w1 = np.zeros(N); w2 = np.zeros(N)
    n_tr, n_win = int(T_tr/dt), int(T_win/dt)
    Pd = np.zeros(N); Pi = np.zeros(N); flips = np.zeros(N)
    sq = np.sqrt(S*dt)
    def energy(p1, p2, w1, w2):
        T = 0.5*(m1 + m2)*L1**2*w1**2 + 0.5*m2*L2**2*w2**2 + m2*L1*L2*w1*w2*np.cos(p1 - p2)
        V = -(m1 + m2)*g*L1*np.cos(p1) - m2*g*L2*np.cos(p2)
        return T + V
    for k in range(n_tr + n_win):
        if k == n_tr: E0 = energy(p1, p2, w1, w2)
        d = p1 - p2; cd, sd = np.cos(d), np.sin(d)
        M11 = (m1 + m2)*L1**2; M22 = m2*L2**2; M12 = m2*L1*L2*cd
        det = M11*M22 - M12**2
        b1 = (m1 + m2)*L1*np.cos(p1); b2 = m2*L2*np.cos(p2)
        # generalised forces without the shaking: gyroscopic, gravity, generators (pivot c1, hinge c2 on psi2 - psi1)
        f1 = -m2*L1*L2*sd*w2**2 - (m1 + m2)*g*L1*np.sin(p1) - c1*w1 + c2*(w2 - w1)
        f2 = m2*L1*L2*sd*w1**2 - m2*g*L2*np.sin(p2) - c2*(w2 - w1)
        a1 = (M22*f1 - M12*f2)/det; a2 = (M11*f2 - M12*f1)/det
        n1 = (M22*b1 - M12*b2)/det; n2 = (M11*b2 - M12*b1)/det      # M^-1 b
        if k >= n_tr:
            Pd += c1*w1**2 + c2*(w2 - w1)**2
            Pi += 0.5*S*(b1*n1 + b2*n2)
        xi = rng.standard_normal(N)*sq
        w1 = w1 + a1*dt - n1*xi
        w2 = w2 + a2*dt - n2*xi
        p1o = p1
        p1 = p1 + w1*dt; p2 = p2 + w2*dt
        flips += (np.floor((p1 + np.pi)/(2*np.pi)) != np.floor((p1o + np.pi)/(2*np.pi)))
    E1 = energy(p1, p2, w1, w2)
    return Pd/n_win, Pi/n_win, (E1 - E0)/T_win, flips

def report(name, Pd, Pi, dE, Mtot, S, extra=''):
    N = len(Pd)
    mPd, sPd = Pd.mean(), Pd.std(ddof=1)/np.sqrt(N)
    mPi, sPi = Pi.mean(), Pi.std(ddof=1)/np.sqrt(N)
    r = Pd/Pi
    ratio, sr = r.mean(), r.std(ddof=1)/np.sqrt(N)
    close = (Pi - Pd - dE).mean()
    print(f'  {name}: P_diss = {mPd*1e3:.4f} +- {sPd*1e3:.4f} mW; (S/2)<m_eff> = {mPi*1e3:.4f} +- {sPi*1e3:.4f} mW; '
          f'ratio {ratio:.4f} +- {sr:.4f}; <m_eff>/M = {mPi/(0.5*S*Mtot):.4f}; book residual {close/mPi*100:+.2f} %{extra}')
    return ratio, sr

fails = 0
def verdict(name, ok):
    global fails
    fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name)

N = 300 if QUICK else 1000
t0 = time.time()
print(f'ensemble N = {N} trajectories per case; seeds 11, 12, 21, 22 (dt), 13, 14, 23, 24 (dt/2)')
# single: c = 2 zeta omega0 m L^2, omega0 = sqrt(g/L)
m, L = SU.M, SU.L
ZETA = 0.2                      # damping ratio: short correlation time, many independent samples per second
om0 = np.sqrt(g/L); c = 2*ZETA*om0*m*L**2
Ttr = 5/(ZETA*om0)
for label, S, dts, seeds in (('single, small swings', 2.0e-2, (2e-4, 1e-4), (11, 13)),
                             ('single, large swings', 34.0, (1e-4, 5e-5), (12, 14))):
    res = []
    for dt, sd in zip(dts, seeds):
        Pd, Pi, dE, rms = run_single(S, c, N, Ttr, 20 if QUICK else 40, dt, sd, m=m, L=L)
        res.append(report(f'{label}, dt = {dt:.0e} s, S = {S} m^2/s^3', Pd, Pi, dE, m, S,
                          f'; rms angle {rms:.3f} rad'))
    ratio, sr = res[-1]
    verdict(f'{label}: P_diss = (S/2)<m_eff> within 3 % (finest dt): {abs(ratio - 1)*100:.2f} %', abs(ratio - 1) < 0.03)
# double: equal masses and rods, the same total mass and reach; generators at pivot and hinge
m1 = m2 = SU.M/2; L1 = L2 = SU.L/2
c1 = c2 = 2*ZETA*np.sqrt(g/L1)*m2*L2**2
Ttr2 = 5/(ZETA*np.sqrt(g/L1)*0.6)
for label, S, dts, seeds in (('double, small swings', 2.0e-2, (1e-4, 5e-5), (21, 23)),
                             ('double, large chaotic swings', 34.0, (5e-5, 2.5e-5), (22, 24))):
    res = []
    for dt, sd in zip(dts, seeds):
        Pd, Pi, dE, flips = run_double(S, c1, c2, N, Ttr2, 20 if QUICK else 40, dt, sd, m1=m1, m2=m2, L1=L1, L2=L2)
        res.append(report(f'{label}, dt = {dt:.1e} s, S = {S} m^2/s^3', Pd, Pi, dE, m1 + m2, S,
                          f'; top-rod turns over per trajectory {flips.mean():.1f}'))
    ratio, sr = res[-1]
    verdict(f'{label}: P_diss = (S/2)<m_eff> within 3 % (finest dt): {abs(ratio - 1)*100:.2f} %', abs(ratio - 1) < 0.03)
print(f'({time.time() - t0:.0f} s)')
print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
