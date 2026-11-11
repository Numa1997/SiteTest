"""Fig. 13, the catch: how long a pendulum the motor has released stays on the butterfly, checked with an integrator other than the page's.

    node tools/fig13/catch_stats.cjs starts 1 100 16 900 runs.json     # 100 random starts; each run's state just after the release
    python3 tools/fig13/release_check.py runs.json [N=40]

For the first N released states: the free motion by DOP853 (rtol 1e-11) for 800 s, its distance to the butterfly (or its mirror) every
sixteenth of a lap; the distance is the note's eq. (11), weights (1, 1, 0.05, 0.05), nearest of 4800 orbit points computed here by DOP853.
Result of 11 November 2026 (seed 1, 16 sub-steps, N = 40): at release median 1e-4, worst 9e-4; largest within four laps: median 0.0023,
worst 0.040; time until the distance first exceeds 0.1: median 403 s, shortest 41 s, one run still within after 800 s.
"""
import sys, json
import numpy as np
from scipy.integrate import solve_ivp

A, B, C, U1, U2 = 4 / 3, 1 / 3, 0.5, 14.7, 4.9
P1, P2, T = 3.557312977100609, 12.211005483946245, 2.659405430607505
QD = np.array([1, 1, .05, .05])


def rhs(t, y):
    c = np.cos(y[0] - y[1]); s = np.sin(y[0] - y[1]); det = A * B - C * C * c * c
    w1 = (B * y[2] - C * c * y[3]) / det; w2 = (A * y[3] - C * c * y[2]) / det
    return [w1, w2, -C * w1 * w2 * s - U1 * np.sin(y[0]), C * w1 * w2 * s - U2 * np.sin(y[1])]


ORBIT = solve_ivp(rhs, (0, T), [0, 0, P1, P2], method='DOP853', rtol=1e-12, atol=1e-12, t_eval=np.linspace(0, T, 4801)[:-1]).y.T


def dist(y):
    best = 9.0
    for sg in (1, -1):
        d = y[None, :] - sg * ORBIT; d[:, :2] -= 2 * np.pi * np.round(d[:, :2] / (2 * np.pi)); best = min(best, np.sqrt((QD * d * d).sum(1).min()))
    return best


def main(path, n=40):
    runs = [r for r in json.load(open(path)) if r['caught']][:n]; res = []
    te = np.arange(0, 800, T / 16)
    for r in runs:
        sol = solve_ivp(rhs, (0, 800), r['sRel'], method='DOP853', rtol=1e-11, atol=1e-11, t_eval=te)
        dd = np.array([dist(sol.y[:, i]) for i in range(len(te))]); over = np.where(dd > 0.1)[0]
        res.append((dd[0], dd[te <= 4 * T].max(), te[over[0]] if len(over) else np.inf))
    res = np.array(res); t = res[:, 2]
    print('%d released runs: distance at release median %.4f, worst %.4f; largest within four laps: median %.4f, worst %.4f'
          % (len(res), np.median(res[:, 0]), res[:, 0].max(), np.median(res[:, 1]), res[:, 1].max()))
    print('time until the distance first exceeds 0.1: median %.0f s, shortest %.0f s, never within 800 s: %d' % (np.median(t), t.min(), np.isinf(t).sum()))


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 40)
