"""The butterfly hunt.

A butterfly is a flower caught in the one-petal resonance. Each petal tip lands close to the previous one (the lower arm turns
by nearly a whole turn between petals), so the petal direction moves slowly. Gravity pulls it towards straight down and it
swings about the bottom like a pendulum. Near the turning points it moves slowest, so petals pile up there: two dense fans,
left and right, which are the wings. (Measured at the video's cell p = (3.556, 10): petal directions run 57, 97, 119, 126,
121, 104, 74, 33, -14, ... degrees from straight down; the swing reaches +-126 degrees.)
When one swing takes a whole number N of petals the tip path closes: a periodic orbit with N turns of D, which Newton's
method (the same solver as hunt.py) finds exactly.

Measured per kick (p1, p2): theta2 at each alignment of the arms (D = 2 pi n), i.e. each petal tip direction.
  u_n = remainder(theta2_n, 2 pi)   petal direction from straight down
  caught: |u_n| never reaches pi (the swing never goes over the top); wing angle = max |u_n|;
  petals per swing from the zero crossings of u_n (two per swing).

Usage: python3 tools/fig13/butterfly.py OUTDIR
"""
import sys, json, math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from chaos_map import coefficients
from hunt import rhs, turns, energy, BASE, RTOL, ATOL
from hunt_inspect import floquet_trace

G = 9.8
P1_LINE = ((5 + .5) / 10 - .5) * 40 * 16 / 9              # p1 = +3.556 kg m^2/s: column i = 5 of the video's grid, its butterfly cells
NPET = 120


def petal_angles(coef, p1, p2, n):
    r = turns(coef, p1, p2, n, 60.0)
    if r is None:
        return None
    t, s, sgn = r
    return t, s[:, 1]


def rock(th2):
    n = np.arange(1, th2.size + 1)
    u = np.concatenate([[0.0], [math.remainder(a, 2 * math.pi) for a in th2]])     # u_0 = 0: the start is a petal tip straight down
    z = np.where(np.diff(np.sign(u)) != 0)[0]
    per = 2 * np.mean(np.diff(z)) if z.size >= 3 else np.nan             # petals per full rock
    return u, float(np.max(np.abs(u))), float(per)


def stability(tr):
    """|trace| < 2 stable, > 2 unstable; within 0.01 of 2 the finite-difference Jacobian cannot tell: neutral."""
    if abs(abs(tr) - 2) < 0.01:
        return 'neutral'
    return 'stable' if abs(tr) < 2 else 'unstable'


def main(out):
    coef = coefficients(dict(BASE, g=G))
    p2s = np.round(np.arange(4.0, 20.001, 0.1), 3)
    rows = []
    for p2 in p2s:
        r = petal_angles(coef, P1_LINE, p2, NPET)
        if r is None:
            rows.append((p2, np.nan, np.nan, np.nan)); continue
        t, th2 = r
        u, amp, per = rock(th2)
        trapped = amp < math.pi * 0.98                                      # the swing never goes over the top: caught in the resonance
        rows.append((p2, amp if trapped else np.nan, per if trapped else np.nan, t[-1] / NPET))
    rows = np.array(rows)
    print('line p1 = %.3f: kicks caught in the one-petal resonance (petal direction swings about straight down):' % P1_LINE)
    caught = ~np.isnan(rows[:, 1])
    print('  %d of %d values of p2, from %.1f to %.1f' % (caught.sum(), len(rows), rows[caught, 0].min(), rows[caught, 0].max()))
    for p2, amp, per, tp in rows[caught][::6]:
        print('  p2=%5.1f  wing angle %5.1f deg  petals per swing %6.2f  time per petal %.4f s' % (p2, math.degrees(amp), per, tp))
    np.save(out + '/butterfly_scan.npy', rows)

    # close butterflies: petals per rock = N (even, so the wings are mirror pairs); Newton on the periodic orbit with k = N
    found = []
    for N in (12, 14, 16, 18, 20, 24, 28, 32):
        sel = caught & (np.abs(rows[:, 2] - N) < 1.5)
        if not sel.any():
            continue
        p2g = rows[sel][np.argmin(np.abs(rows[sel, 2] - N)), 0]
        def F(x):
            r = turns(coef, x[0], x[1], N, 60.0)
            if r is None:
                return [10.0, 10.0]
            t, s, sgn = r
            return [math.remainder(s[-1, 1], 2 * math.pi), s[-1, 2] - x[0]]
        sol = root(F, [P1_LINE, p2g], method='hybr', options=dict(xtol=1e-12))
        res = F(sol.x)
        if not max(map(abs, res)) < 1e-8:                                  # closure judged by the residual itself
            print('  N=%d: Newton did not close (residual %.1e)' % (N, max(map(abs, res)))); continue
        t, s, sgn = turns(coef, sol.x[0], sol.x[1], N, 60.0)
        u, amp, _ = rock(s[:, 1])
        fl = dict(k=N, p1=float(sol.x[0]), p2=float(sol.x[1]), period=float(t[-1]), E=energy(coef, [0, 0, *sol.x]),
                  wing_half_angle_deg=math.degrees(amp), closure=max(map(abs, res)))
        fl['trace'], fl['det'] = floquet_trace(coef, fl)
        found.append(fl)
        print('  closed butterfly N=%2d: p=(%+.5f, %+.5f)  period %.3f s  E=%.1f J  wings +-%.1f deg  trace %+.3f  %s'
              % (N, fl['p1'], fl['p2'], fl['period'], fl['E'], fl['wing_half_angle_deg'], fl['trace'],
                 stability(fl['trace'])))
    json.dump(dict(line_p1=P1_LINE, butterflies=found), open(out + '/butterflies.json', 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
