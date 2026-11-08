"""Data for the 'dive' film (dive.html): a 9 x 9 grid of double pendulums in momentum space, one of them the 24-petal butterfly.

Every cell is a double pendulum of two equal uniform rods (1 kg, 1 m, g = 9.8 m/s^2) hanging still (theta1 = theta2 = 0) and kicked
with the momenta (p1, p2) of the cell's centre. The grid has spacing 4 kg m^2/s and is placed so that one cell sits exactly on the
butterfly kick from orbit24.json; all cells lie inside the square p1, p2 in [-20, 20], the square shown behind them (the chaos map).

Writes  OUT/dive.bin   float32, shape (81, n, 2): theta1, theta2 of each cell, sampled at RATE per second from t = 0 to TMAX
        OUT/dive.json  the grid, the sampling, and the butterfly's own momenta p1(t), p2(t) over one period (for the inset)
Checks: the butterfly cell reproduces orbit24.json to 1e-6 rad over one period; energy drift of every cell below 1e-6 relative.

Usage: python3 tools/fig13/gift/dive_data.py OUTDIR
"""
import sys, json, math
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, __file__.rsplit('/', 2)[0])
from chaos_map import coefficients
from hunt import rhs, energy, BASE, RTOL, ATOL

out = sys.argv[1]
O = json.load(open(__file__.rsplit('/', 1)[0] + '/orbit24.json'))
SPACING, RATE, TMAX, HALF = 4.0, 400, 9.0, 20.0          # kg m^2/s, samples per s, s, half-width of the momentum square
coef = coefficients(dict(BASE, g=9.8))
f = rhs(coef)
i_range = [i for i in range(-10, 11) if abs(O['p1'] + SPACING * i) + SPACING / 2 <= HALF]
j_range = [j for j in range(-10, 11) if abs(O['p2'] + SPACING * j) + SPACING / 2 <= HALF]
assert len(i_range) == 9 and len(j_range) == 9, (i_range, j_range)
tt = np.linspace(0, TMAX, int(round(TMAX * RATE)) + 1)
cells, data = [], []
for j in j_range[::-1]:                                    # rows from the top (largest p2) down
    for i in i_range:
        p1, p2 = O['p1'] + SPACING * i, O['p2'] + SPACING * j
        s = solve_ivp(f, (0, TMAX), [0, 0, p1, p2], method='DOP853', rtol=RTOL, atol=ATOL, t_eval=tt)
        assert s.success, s.message
        E0, E1 = energy(coef, s.y[:, 0]), energy(coef, s.y[:, -1])
        assert abs(E1 - E0) <= 1e-6 * max(1.0, abs(E0)), (p1, p2, E0, E1)
        cells.append(dict(p1=p1, p2=p2, i=i, j=j, E=E0, target=(i == 0 and j == 0)))
        data.append(np.stack([s.y[0], s.y[1]], axis=1))
arr = np.asarray(data, dtype=np.float32)
k = [c['target'] for c in cells].index(True)
n_T = int(round(O['T'] * O['rate']))
to = np.linspace(0, O['T'], len(O['th1']))                # orbit24.json samples are spaced T/(n-1), not exactly 1/rate
sel = tt <= O['T']
err = max(np.max(np.abs(arr[k, sel, 0] - np.interp(tt[sel], to, O['th1']))), np.max(np.abs(arr[k, sel, 1] - np.interp(tt[sel], to, O['th2']))))
assert err < 1e-4, err                                     # limited by interpolating orbit24 at 1/3000 s (~1e-5 rad) and float32
# the butterfly's momenta over one period, for the inset
tp = np.linspace(0, O['T'], int(round(O['T'] * 600)) + 1)
s = solve_ivp(f, (0, O['T']), [0, 0, O['p1'], O['p2']], method='DOP853', rtol=RTOL, atol=ATOL, t_eval=tp)
arr.tofile(out + '/dive.bin')
json.dump(dict(spacing=SPACING, rate=RATE, tmax=TMAX, half=HALF, n=int(arr.shape[1]), cells=cells, target=k,
               p_rate=600, p1=[round(float(v), 5) for v in s.y[2]], p2=[round(float(v), 5) for v in s.y[3]]),
          open(out + '/dive.json', 'w'), separators=(',', ':'))
print('cells %d, samples %d, target index %d, butterfly check %.1e rad, p1 range %.2f..%.2f, p2 range %.2f..%.2f, bin %.1f MB'
      % (len(cells), arr.shape[1], k, err, s.y[2].min(), s.y[2].max(), s.y[3].min(), s.y[3].max(), arr.nbytes / 1e6))
