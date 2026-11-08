"""Export one closed butterfly orbit for the 3-D film (butterfly3d.html).

Reads the full-precision kick from butterflies.json (written by tools/fig13/butterfly.py), integrates one period with DOP853
(rtol 1e-11) and writes samples every 1/3000 s: theta1, theta2, p1, p2, and the petal times and directions.
Checks before writing: closure after N petals, and that tip = r e^{i psi} with r = 2 l cos(D/2) (to 1e-12).

Usage: python3 tools/fig13/gift/orbit.py HUNT_DIR N OUT.json
"""
import sys, json, math
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, __file__.rsplit('/', 2)[0])
from chaos_map import coefficients
from hunt import rhs, turns, energy, BASE, RTOL, ATOL

hunt_dir, N, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
b = [x for x in json.load(open(hunt_dir + '/butterflies.json'))['butterflies'] if x['k'] == N][0]
p1, p2 = b['p1'], b['p2']
coef = coefficients(dict(BASE, g=9.8))
t_tip, s_tip, sgn = turns(coef, p1, p2, N, 60.0)
T = float(t_tip[-1])
closure = math.hypot(math.remainder(s_tip[-1, 1], 2 * math.pi), math.hypot(s_tip[-1, 2] - p1, s_tip[-1, 3] - p2))
assert closure < 1e-8, closure
RATE = 3000
n = int(round(T * RATE)) + 1
tt = np.linspace(0, T, n)
sol = solve_ivp(rhs(coef), (0, T), [0, 0, p1, p2], method='DOP853', rtol=RTOL, atol=ATOL, t_eval=tt)
th1, th2 = sol.y[0], sol.y[1]
D, psi = th1 - th2, (th1 + th2) / 2
r = 2 * np.cos(D / 2)
X, Y = np.sin(th1) + np.sin(th2), np.cos(th1) + np.cos(th2)
err = max(np.max(np.abs(r * np.sin(psi) - X)), np.max(np.abs(r * np.cos(psi) - Y)))
assert err < 1e-12, err
phi = [0.0] + [float(a) for a in s_tip[:, 1]]
tp = [0.0] + [float(t) for t in t_tip]
wing = max(abs(math.remainder(a, 2 * math.pi)) for a in phi)
data = dict(N=N, T=T, rate=RATE, p1=p1, p2=p2, E=energy(coef, [0, 0, p1, p2]), closure=closure, map_error=float(err), wing_deg=math.degrees(wing),
            th1=[round(float(v), 7) for v in th1], th2=[round(float(v), 7) for v in th2],
            tp=tp, phi=[round(a, 7) for a in phi])
json.dump(data, open(out, 'w'), separators=(',', ':'))
print('N=%d  T=%.5f s  kick (%.9f, %.9f)  E=%.2f J  closure %.1e  map error %.1e  wings +-%.2f deg  samples %d'
      % (N, T, p1, p2, data['E'], closure, err, data['wing_deg'], n))
