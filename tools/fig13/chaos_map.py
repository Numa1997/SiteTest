"""Fig. 13 chaos map: how fast twin pendulums part, over momentum space.

Every pixel is a double pendulum started at theta1 = theta2 = 0 with that pixel's momenta (p1, p2), plus a twin whose theta1
is 1e-4 rad larger. Both are stepped with RK4; after every step the four-dimensional distance between them,
sqrt(dtheta1^2 + dtheta2^2 + dp1^2 + dp2^2), is capped at 1 and added up. The map is the mean over all steps.
This is the measure of 2swap's swaptube (PendulumFractal.cu, double_pendulum_simulation_kernel: distance = min(distance, 1)),
over the same 6.67 s as his momentum-space scene (4000 steps of 0.05/30 s; DoublePendulum project file, line 431), but with a
step four times finer (see CONFIG).

Physics: the general double pendulum of Fig. 13 (link i: mass m_i, length l_i, centre of mass a_i, inertia I_i about its joint);
the defaults below are 2swap's equal uniform rods.

Usage:
  python3 tools/fig13/chaos_map.py --check map.npz    # kernel without the cap must reproduce the previous NumPy map
  python3 tools/fig13/chaos_map.py --out DIR          # compute the map and write DIR/chaos-map-rods-P20.npz
"""
import argparse, json, time, sys
import numpy as np
from numba import njit, prange

CONFIG = dict(model='rods', m1=1.0, m2=1.0, l1=1.0, l2=1.0, g=9.8,   # SI units: kg, m, m/s^2
              P=20.0, aspect=16 / 9,                                    # p2 in [-P, P], p1 in [-P*aspect, P*aspect], kg m^2/s
              width=1280, height=720,                                   # pixels; pixel centres
              steps=16000, h=0.05 / 30 / 4,                             # RK4 steps and step, s: the same 6.67 s as 2swap, step 4x finer
              # Why 4x finer: at 2swap's step (0.05/30 s) the high-energy corners show twin divergence that is integrator
              # error, not chaos. Corner pixel p = (-34, 19): 2.35e-2 at h, 9.13e-4 at h/4, 9.10e-4 at h/16 (8 Nov 2026).
              twin_dtheta1=1e-4, cap=1.0)


def coefficients(c):
    rods = c['model'] == 'rods'
    if not rods and c['model'] != 'points':
        raise ValueError(c['model'])
    a1 = c['l1'] / 2 if rods else c['l1']
    a2 = c['l2'] / 2 if rods else c['l2']
    I1 = c['m1'] * c['l1'] ** 2 / 12 if rods else 0.0
    I2 = c['m2'] * c['l2'] ** 2 / 12 if rods else 0.0
    A = c['m1'] * a1 ** 2 + I1 + c['m2'] * c['l1'] ** 2
    B = c['m2'] * a2 ** 2 + I2
    C = c['m2'] * c['l1'] * a2
    U1 = c['g'] * (c['m1'] * a1 + c['m2'] * c['l1'])
    U2 = c['g'] * c['m2'] * a2
    return A, B, C, U1, U2


@njit(inline='always')
def deriv(q1, q2, p1, p2, A, B, C, U1, U2):
    d = q1 - q2
    cs = np.cos(d); sn = np.sin(d)
    det = A * B - C * C * cs * cs
    w1 = (B * p1 - C * cs * p2) / det
    w2 = (A * p2 - C * cs * p1) / det
    e = C * w1 * w2 * sn
    return w1, w2, -e - U1 * np.sin(q1), e - U2 * np.sin(q2)


@njit(inline='always')
def rk4(q1, q2, p1, p2, h, A, B, C, U1, U2):
    a1, a2, a3, a4 = deriv(q1, q2, p1, p2, A, B, C, U1, U2)
    b1, b2, b3, b4 = deriv(q1 + .5 * h * a1, q2 + .5 * h * a2, p1 + .5 * h * a3, p2 + .5 * h * a4, A, B, C, U1, U2)
    c1, c2, c3, c4 = deriv(q1 + .5 * h * b1, q2 + .5 * h * b2, p1 + .5 * h * b3, p2 + .5 * h * b4, A, B, C, U1, U2)
    d1, d2, d3, d4 = deriv(q1 + h * c1, q2 + h * c2, p1 + h * c3, p2 + h * c4, A, B, C, U1, U2)
    return (q1 + h / 6 * (a1 + 2 * b1 + 2 * c1 + d1), q2 + h / 6 * (a2 + 2 * b2 + 2 * c2 + d2),
            p1 + h / 6 * (a3 + 2 * b3 + 2 * c3 + d3), p2 + h / 6 * (a4 + 2 * b4 + 2 * c4 + d4))


@njit(parallel=True)
def twin_map(P1, P2, steps, h, dth, cap, A, B, C, U1, U2):
    n = P1.size
    out = np.empty(n)
    for k in prange(n):
        q1 = 0.0; q2 = 0.0; p1 = P1[k]; p2 = P2[k]
        r1 = dth; r2 = 0.0; s1 = P1[k]; s2 = P2[k]
        acc = 0.0
        for i in range(steps):
            q1, q2, p1, p2 = rk4(q1, q2, p1, p2, h, A, B, C, U1, U2)
            r1, r2, s1, s2 = rk4(r1, r2, s1, s2, h, A, B, C, U1, U2)
            dist = np.sqrt((q1 - r1) ** 2 + (q2 - r2) ** 2 + (p1 - s1) ** 2 + (p2 - s2) ** 2)
            if cap > 0 and dist > cap:
                dist = cap
            acc += dist
        out[k] = acc / steps
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', metavar='MAP_NPZ')
    ap.add_argument('--out')
    a = ap.parse_args()
    c = dict(CONFIG)
    coef = coefficients(c)
    if a.check:
        prev = np.load(a.check)                              # the previous session's map.npz (fig13-study-bundle branch)
        gx, gy = prev['gx'], prev['gy']                      # the previous grid: linspace with end points
        G1, G2 = np.meshgrid(gx, gy)
        sel = (slice(None, None, 9), slice(None, None, 9))  # every 9th pixel each way: 24 x 43 = 1032 pendulums
        mine = twin_map(G1[sel].ravel(), G2[sel].ravel(), c['steps'], c['h'], c['twin_dtheta1'], 0.0, *coef)
        ref = prev['mean_dist'][sel].ravel()
        rel = np.abs(mine - ref) / ref
        # Regular pixels: twins stay close, round-off is not amplified, the two codes must agree to rounding.
        # Chaotic pixels: round-off grows like exp(lambda t); two correct codes agree only statistically.
        reg = ref < 0.05
        print('uncapped kernel vs previous NumPy map, %d pixels (%d regular: mean distance < 0.05)' % (ref.size, reg.sum()))
        print('  regular pixels: max relative difference %.2e, median %.2e' % (rel[reg].max(), np.median(rel[reg])))
        print('  chaotic pixels: median relative difference %.2e, max %.2e; mean log10 distance %.4f (mine) vs %.4f (previous)'
              % (np.median(rel[~reg]), rel[~reg].max(), np.log10(mine[~reg]).mean(), np.log10(ref[~reg]).mean()))
        assert rel[reg].max() < 1e-5, 'kernel does not reproduce the previous map on regular pixels'  # regular pixels next to the chaos edge still amplify round-off a little
        assert abs(np.log10(mine[~reg]).mean() - np.log10(ref[~reg]).mean()) < 0.01, 'chaotic pixels disagree on average'
        return
    if not a.out:
        raise SystemExit('give --out DIR or --check')
    W, H = c['width'], c['height']
    p1 = (np.arange(W) + .5) / W * 2 * c['P'] * c['aspect'] - c['P'] * c['aspect']
    p2 = c['P'] - (np.arange(H) + .5) / H * 2 * c['P']     # row 0 is the top: p2 = +P
    G1, G2 = np.meshgrid(p1, p2)
    t0 = time.time()
    m = twin_map(G1.ravel(), G2.ravel(), c['steps'], c['h'], c['twin_dtheta1'], c['cap'], *coef).reshape(H, W)
    dt = time.time() - t0
    meta = dict(c, seconds=round(dt, 1), numba=__import__('numba').__version__, numpy=np.__version__)
    np.savez_compressed(a.out + '/chaos-map-rods-P20.npz', mean_capped_dist=m.astype(np.float32), p1=p1, p2=p2,
                        meta=json.dumps(meta))
    print('map %dx%d done in %.0f s; mean distance min %.3g, median %.3g, max %.3g' % (W, H, dt, m.min(), np.median(m), m.max()))


if __name__ == '__main__':
    main()
