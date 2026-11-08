"""The flower hunt: which kick makes a double pendulum draw a closed flower (or a butterfly)?

Picture. Equal arms of length l: the tip is l e^{i th1} + l e^{i th2} = 2 l cos(D/2) e^{i psi}, D = th1 - th2, psi = (th1 + th2)/2.
When the arms fold (D = pi) the tip passes through the pivot; when they line up (D = 0 mod 2 pi) it reaches the rim, in the
direction of th2. If D keeps turning ("fold-through"), every turn of D draws one petal through the centre, and the next petal
tip lies delta further round, where delta is the turn of the lower arm during one turn of D. The flower closes with k petals
when delta / 2 pi = q / k with q, k coprime.

Step 1, g = 0. Without gravity p1 + p2 is conserved and the motion is scale-free: doubling |p| runs the same curve twice as
fast. So delta depends only on the direction alpha of the kick p = |p| (cos alpha, sin alpha). We compute delta(alpha) by
integrating one turn of D and solve delta(alpha) = 2 pi q / k by bisection.

Step 2, g = 9.8 m/s^2. Gravity breaks the scale freedom and the rotational symmetry. A closed flower is now a periodic orbit:
started at th1 = th2 = 0 with (p1, p2), after k turns of D the pendulum must be back at th2 = 0 (mod 2 pi) with the same
momenta. We solve the two equations  th2_k = 2 pi n  and  p1_k = p1_0  for (p1, p2) by Newton's method (energy conservation
then returns p2), starting from the g = 0 flower at a chosen size |p|.

Usage: python3 tools/fig13/hunt.py OUTDIR
"""
import sys, json, math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, root
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from chaos_map import coefficients                     # the same family coefficients as the chaos map

BASE = dict(model='rods', m1=1.0, m2=1.0, l1=1.0, l2=1.0)   # 2swap's equal uniform rods, SI units
RTOL, ATOL = 1e-11, 1e-12


def rhs(coef):
    A, B, C, U1, U2 = coef
    def f(t, s):
        q1, q2, p1, p2 = s
        c, sn = math.cos(q1 - q2), math.sin(q1 - q2)
        det = A * B - C * C * c * c
        w1 = (B * p1 - C * c * p2) / det
        w2 = (A * p2 - C * c * p1) / det
        e = C * w1 * w2 * sn
        return [w1, w2, -e - U1 * math.sin(q1), e - U2 * math.sin(q2)]
    return f


def energy(coef, s):
    A, B, C, U1, U2 = coef
    q1, q2, p1, p2 = s
    c = math.cos(q1 - q2); det = A * B - C * C * c * c
    return 0.5 * (B * p1 * p1 - 2 * C * c * p1 * p2 + A * p2 * p2) / det - U1 * math.cos(q1) - U2 * math.cos(q2)


def turns(coef, p1, p2, k, tmax):
    """Integrate from th1 = th2 = 0 until D = th1 - th2 has turned k times (sign of the start). Returns state at each turn."""
    f = rhs(coef)
    s0 = [0.0, 0.0, p1, p2]
    w = f(0, s0)
    sgn = 1.0 if w[0] - w[1] > 0 else -1.0
    states, times = [], []
    t0, s = 0.0, np.array(s0)
    for n in range(1, k + 1):
        target = sgn * 2 * math.pi * n
        ev = lambda t, y, target=target: y[0] - y[1] - target
        ev.terminal = True; ev.direction = sgn
        back = lambda t, y, base=target - sgn * 2 * math.pi: (y[0] - y[1] - base) * sgn + 1.0   # D fell back a whole radian: no fold-through
        back.terminal = True
        sol = solve_ivp(f, (t0, tmax), s, method='DOP853', rtol=RTOL, atol=ATOL, events=[ev, back])
        if sol.t_events[0].size == 0:
            return None                                  # D did not turn: the arms do not fold through
        t0 = sol.t_events[0][0]; s = sol.y_events[0][0]
        states.append(s.copy()); times.append(t0)
    return np.array(times), np.array(states), sgn


def delta_g0(alpha):
    coef = coefficients(dict(BASE, g=0.0))
    r = turns(coef, math.cos(alpha), math.sin(alpha), 1, 200.0)
    if r is None:
        return None, None
    t, s, sgn = r
    return s[0, 1], t[0]                               # turn of the lower arm during one turn of D, and the time it took


def main(out):
    report = {}
    # ---- Step 1: delta(alpha) at g = 0 -------------------------------------------------------------------------------
    alphas = np.linspace(0, math.pi, 1801)[:-1]               # 0.1 degree steps
    d = np.full(alphas.size, np.nan); T = np.full(alphas.size, np.nan)
    for i, a in enumerate(alphas):
        q = 3 * math.cos(a) ** 2 - 114 * math.cos(a) * math.sin(a) + 75 * math.sin(a) ** 2   # > 0: fold-through (g = 0)
        if q <= 1e-9:
            continue
        di, ti = delta_g0(a)
        if di is not None:
            d[i], T[i] = di, ti
    fold = ~np.isnan(d)
    print('g = 0: %d of %d directions fold through; delta/2pi ranges over [%.4f, %.4f]'
          % (fold.sum(), alphas.size, np.nanmin(d) / (2 * math.pi), np.nanmax(d) / (2 * math.pi)))
    # cross-check: the fold-through boundary lines from the energy argument (p1/p2 = 19 -+ 4 sqrt 21)
    edges = alphas[np.where(np.diff(fold.astype(int)) != 0)[0]]
    print('  fold-through region edges (rad):', np.round(edges, 4), ' expected from p1/p2 = 19 -+ 4 sqrt21:',
          np.round(np.sort(np.mod(np.arctan2(1, np.array([19 - 4 * 21 ** .5, 19 + 4 * 21 ** .5])), math.pi)), 4))
    np.savez(out + '/delta_g0.npz', alpha=alphas, delta=d, period=T)

    # ---- roots: delta / 2 pi = q / k  (mod 1) --------------------------------------------------------------------------
    nu = np.mod(d / (2 * math.pi), 1.0)
    targets = []
    for k in range(2, 13):
        for q in range(1, k):
            if math.gcd(q, k) != 1:
                continue
            g_ = nu - q / k
            for i in range(alphas.size - 1):
                if fold[i] and fold[i + 1] and np.sign(g_[i]) != np.sign(g_[i + 1]) and abs(g_[i] - g_[i + 1]) < 0.5:
                    a = brentq(lambda x: math.fmod(delta_g0(x)[0] / (2 * math.pi) - q / k + 10.5, 1.0) - 0.5, alphas[i], alphas[i + 1], xtol=1e-13)
                    targets.append(dict(k=k, q=q, alpha=a, p1_over_p2=math.cos(a) / math.sin(a)))
    print('g = 0 flowers found (k petals, q): %d' % len(targets))
    for tg in targets:
        if tg['k'] <= 8:
            print('  k=%2d q=%d  alpha=%.6f rad  p1/p2=%+.5f' % (tg['k'], tg['q'], tg['alpha'], tg['p1_over_p2']))
    report['g0_flowers'] = targets

    # ---- Step 2: with gravity, find the exact periodic flower near each g = 0 flower -----------------------------------
    coef = coefficients(dict(BASE, g=9.8))
    found = []
    for tg in targets:
        if tg['k'] > 8:
            continue
        for R in (30.0, 18.0):
            a = tg['alpha']; k = tg['k']
            x0 = np.array([R * math.cos(a), R * math.sin(a)])
            # pick the momentum sign that keeps the grid's range |p1| <= 35.6, |p2| <= 20 if possible
            def F(x):
                r = turns(coef, x[0], x[1], k, 400.0)
                if r is None:
                    return [10.0, 10.0]
                t, s, sgn = r
                th2 = s[-1, 1]
                return [math.remainder(th2, 2 * math.pi), s[-1, 2] - x[0]]
            sol = root(F, x0, method='hybr', options=dict(xtol=1e-12))
            res = F(sol.x)
            ok = sol.success and max(abs(res[0]), abs(res[1])) < 1e-8
            if not ok:
                continue
            r = turns(coef, sol.x[0], sol.x[1], k, 400.0)
            t, s, sgn = r
            E0 = energy(coef, [0, 0, sol.x[0], sol.x[1]])
            closure = float(np.hypot(math.remainder(s[-1, 1], 2 * math.pi), np.hypot(s[-1, 2] - sol.x[0], s[-1, 3] - sol.x[1])))
            found.append(dict(k=k, q=tg['q'], R_start=R, p1=float(sol.x[0]), p2=float(sol.x[1]), period=float(t[-1]),
                              E=E0, E_over_top=E0 / (4 * 9.8 * 1.0), closure=closure,
                              petal_tip_angles_deg=[float(np.degrees(math.remainder(x, 2 * math.pi))) for x in s[:, 1]]))
            print('  g=9.8: k=%2d q=%d from |p|=%4.1f -> p=(%+8.4f, %+8.4f)  period %.4f s  E=%.1f J (%.1f x top)  closure %.1e'
                  % (k, tg['q'], R, sol.x[0], sol.x[1], t[-1], E0, E0 / 39.2, closure))
    report['gravity_flowers'] = found
    json.dump(report, open(out + '/hunt.json', 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
