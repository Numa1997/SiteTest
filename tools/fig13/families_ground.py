"""Fig. 13: where each kind of closed orbit sits on the chaos map.
Usage: families_ground.py STABILITY.npy SHEET.npy
STABILITY.npy: rows (p1, p2, T, s, label) for every point of the family lines (closed_stability.py, map mode).
SHEET.npy: the fine chaos map of the whole sheet, mean capped twin distance d per strike (kaggle_fractal.py), p1 in +-35.56, p2 in +-20.
Prints, for each stability class, its share of the line points, the share that lies on chaotic ground (v > 0.5,
v = log(1000 d)/log(1000) as in map_png.py) and the median growth of a push per lap, exp(|ln lambda|) (1.00 where the class does not grow)."""
import sys
import numpy as np
D = np.load(sys.argv[1]); D = D[np.isfinite(D[:, 3])]
d = np.load(sys.argv[2]); H, W = d.shape
v = np.clip(np.log(1000 * np.maximum(d, 1e-12)) / np.log(1000), 0, 1)
PW, PH = 20 * 16 / 9, 20.0                                    # half-widths of the sheet, kg m^2/s
x = ((D[:, 0] + PW) / (2 * PW) * W).astype(int).clip(0, W - 1)
y = ((PH - D[:, 1]) / (2 * PH) * H).astype(int).clip(0, H - 1)
s = D[:, 3]; g = v[y, x]
lam = np.log((np.abs(s) + np.sqrt(np.maximum(s * s - 4, 0))) / 2)
print('points', len(s), '| chaotic share of the sheet %.4f' % (v > 0.5).mean())
for name, m in [('stable |s| < 1.99', np.abs(s) < 1.99), ('neutral, within 0.01 of +-2', np.abs(np.abs(s) - 2) <= 0.01),
                ('unstable s > 2.01', s > 2.01), ('unstable with flip s < -2.01', s < -2.01)]:
    print('%-30s share %.3f | on chaotic ground %.3f | median growth per lap %.2f' % (name, m.mean(), (g[m] > 0.5).mean(), np.exp(np.median(lam[m])) if np.median(np.abs(s[m])) > 2 else 1.0))
