"""Inspect the flowers found by hunt.py: draw each one, and measure whether it is stable.

Stability. The arms line up (D = 0 mod 2 pi) once per petal. On those moments the state is (th2, p1, p2) with th1 = th2,
and energy fixes p2 from (th2, p1). So one petal is a map (th2, p1) -> (th2', p1') of the plane, and a k-petal flower is a
fixed point of its k-th power. Hamiltonian maps keep area, so the 2 x 2 Jacobian J of that k-th power has det J = 1 and
eigenvalues lambda, 1/lambda. If |trace J| < 2 they lie on the unit circle: nearby orbits circle the flower (stable, an
island, the picture survives). If |trace J| > 2 nearby orbits run away like e^{n ln|lambda|} (unstable, the picture smears).

Usage: python3 tools/fig13/hunt_inspect.py OUTDIR      (reads OUTDIR/hunt.json)
"""
import sys, json, math
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from chaos_map import coefficients
from hunt import rhs, turns, energy, BASE, RTOL, ATOL


def p2_from_energy(coef, th2, p1, E, near):
    """On the section th1 = th2: E = (B p1^2 - 2 C p1 p2 + A p2^2) / (2 (A B - C^2)) - (U1 + U2) cos th2. Branch nearest `near`."""
    A, B, C, U1, U2 = coef
    det = A * B - C * C
    disc = C * C * p1 * p1 - A * (B * p1 * p1 - 2 * det * (E + (U1 + U2) * math.cos(th2)))
    if disc < 0:
        raise ValueError('no real p2 on this energy surface')
    r = [(C * p1 + s * math.sqrt(disc)) / A for s in (1, -1)]
    return min(r, key=lambda x: abs(x - near))


def section_map_k(coef, th2, p1, p2, k):
    """Start on the section (th1 = th2), run k turns of D, return (th2, p1, p2) at the k-th turn."""
    f = rhs(coef)
    s = np.array([th2, th2, p1, p2])
    w = f(0, s); sgn = 1.0 if w[0] - w[1] > 0 else -1.0
    t0 = 0.0
    for n in range(1, k + 1):
        ev = lambda t, y, n=n: y[0] - y[1] - sgn * 2 * math.pi * n
        ev.terminal = True; ev.direction = sgn
        sol = solve_ivp(f, (t0, t0 + 50), s, method='DOP853', rtol=RTOL, atol=ATOL, events=ev)
        assert sol.t_events[0].size == 1, 'the arms stopped folding through near this flower'
        t0 = sol.t_events[0][0]; s = sol.y_events[0][0]
    return s[1], s[2], s[3]


def floquet_trace(coef, fl):
    p1, p2, k = fl['p1'], fl['p2'], fl['k']
    E = energy(coef, [0, 0, p1, p2])
    eps = 1e-6
    J = np.zeros((2, 2))
    for j, (dth, dp) in enumerate(((eps, 0.0), (0.0, eps))):
        cols = []
        for sgnv in (1, -1):
            th = sgnv * dth; q1 = p1 + sgnv * dp
            q2 = p2_from_energy(coef, th, q1, E, p2)
            a, b, _ = section_map_k(coef, th, q1, q2, k)
            cols.append((math.remainder(a, 2 * math.pi), b))
        J[0, j] = (cols[0][0] - cols[1][0]) / (2 * eps)
        J[1, j] = (cols[0][1] - cols[1][1]) / (2 * eps)
    return float(np.trace(J)), float(np.linalg.det(J))


def tip_path(coef, p1, p2, T, n):
    f = rhs(coef)
    t = np.linspace(0, T, n)
    sol = solve_ivp(f, (0, T), [0, 0, p1, p2], method='DOP853', rtol=RTOL, atol=ATOL, t_eval=t)
    q1, q2 = sol.y[0], sol.y[1]
    return np.sin(q1) + np.sin(q2), np.cos(q1) + np.cos(q2)       # metres, y pointing down (l = 1 m)


def main(out):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    rep = json.load(open(out + '/hunt.json'))
    coef = coefficients(dict(BASE, g=9.8))
    fl = rep['gravity_flowers']
    for f_ in fl:
        f_['trace'], f_['det'] = floquet_trace(coef, f_)
        f_['stable'] = abs(f_['trace']) < 2
        print('k=%d q=%d p=(%+8.3f,%+8.3f) T=%.3f s  E/top=%5.1f  trace=%+9.3f det=%.6f  %s'
              % (f_['k'], f_['q'], f_['p1'], f_['p2'], f_['period'], f_['E_over_top'], f_['trace'], f_['det'],
                 'STABLE' if f_['stable'] else 'unstable'))
    json.dump(rep, open(out + '/hunt.json', 'w'), indent=1)
    n = len(fl); cols = 6; rows = math.ceil(n / cols)
    fig, axs = plt.subplots(rows * 2, cols, figsize=(cols * 2.6, rows * 5.4), facecolor='#140d10')
    for i, f_ in enumerate(fl):
        r, c = divmod(i, cols)
        for row, nper, colr in ((2 * r, 1, '#f3d6da'), (2 * r + 1, 8, '#e2a2aa')):
            ax = axs[row, c]; ax.set_facecolor('#140d10')
            x, y = tip_path(coef, f_['p1'], f_['p2'], f_['period'] * nper, 4000 * nper)
            ax.plot(x, -y, color=colr, lw=0.5, alpha=0.9); ax.plot(0, 0, 'o', ms=2, color='#7a1f2b')
            ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.1, 2.1); ax.set_aspect('equal'); ax.axis('off')
            ax.set_title('%s k=%d p=(%.1f,%.1f)\n%s' % ('1 period' if nper == 1 else '8 periods', f_['k'], f_['p1'], f_['p2'],
                         'stable' if f_['stable'] else 'unstable'), color='#f5f1ea', fontsize=7)
    for j in range(n, rows * cols):
        r, c = divmod(j, cols); axs[2 * r, c].axis('off'); axs[2 * r + 1, c].axis('off')
    plt.tight_layout(); plt.savefig(out + '/hunt_gallery.png', dpi=110, facecolor='#140d10')


if __name__ == '__main__':
    main(sys.argv[1])
