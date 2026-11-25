"""Usage: python3 tools/fig13/closed_pin.py MAP.npz OUT.json
New closed drawings picked from the family map (closed_map.py): refine each crossing by bisection in p1, then integrate one full lap (T = 2 t*)
and check that the state returns (angles mod 2 pi, momenta)."""
import sys, json, math, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from numba import njit
from chaos_map import rk4, coefficients, CONFIG
from PIL import Image
A, B, C, U1, U2 = coefficients(CONFIG); h = CONFIG['h']

@njit
def cross(p1, p2, j, h, A, B, C, U1, U2):          # signed s at the j-th crossing, labels, and the crossing time
    q1 = 0.0; q2 = 0.0; a = p1; b = p2; c = 0; k = 0
    while k * h < 4.0:
        o1, o2 = q1, q2
        q1, q2, a, b = rk4(q1, q2, a, b, h, A, B, C, U1, U2); k += 1
        if k * h < 0.02: continue
        fa = np.floor(o1 / np.pi); fb = np.floor(q1 / np.pi)
        if fa != fb:
            m = max(fa, fb); u = (m * np.pi - o1) / (q1 - o1); t2 = o2 + u * (q2 - o2); n = np.round(t2 / np.pi)
            if c == j: return t2 - n * np.pi, m, n, (k - 1 + u) * h
            c += 1
    return np.nan, 0.0, 0.0, 0.0

d = np.load(sys.argv[1]); S = d['S']; M = d['M']; N = d['N']; H, W, J = S.shape
PW, PH = 20 * 16 / 9, 20.0
cm = np.array(Image.open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../public/images/fig13/chaos-map-rods-P20.png')).resize((W, H), Image.BILINEAR)).astype(float); v = (cm[..., 3] / 255) ** (1 / .8)
P1 = lambda x: ((x + .5) / W - .5) * 2 * PW; P2 = lambda y: (.5 - (y + .5) / H) * 2 * PH
cand = {}
rng = np.random.default_rng(3)
for j in range(3):
    s, m, n = S[..., j], M[..., j], N[..., j]
    sa, sb = s[:, :-1], s[:, 1:]
    with np.errstate(invalid='ignore'):
        ok = (m[:, :-1] == m[:, 1:]) & (n[:, :-1] == n[:, 1:]) & (np.sign(sa) != np.sign(sb)) & (np.abs(sa) < .3) & (np.abs(sb) < .3) & (v[:, :-1] < .05)
    yy, xx = np.nonzero(ok); order = rng.permutation(len(yy))
    for i in order:
        y, x = yy[i], xx[i]; key = (int(m[y, x]), int(n[y, x]))
        if key[0] == key[1] or key in cand: continue
        if math.hypot(P1(x), P2(y)) > 30: continue
        cand[key] = (j, P1(x), P1(x + 1), P2(y))
print(len(cand), 'classes found')
keys = sorted(cand, key=lambda k: (abs(k[0] - k[1]), abs(k[0]), k))
out = []
for key in keys:
    j, a, b, p2 = cand[key]
    sa = cross(a, p2, j, h, A, B, C, U1, U2); sb = cross(b, p2, j, h, A, B, C, U1, U2)
    if not (np.isfinite(sa[0]) and np.isfinite(sb[0])) or np.sign(sa[0]) == np.sign(sb[0]) or sa[1] != sb[1] or sa[2] != sb[2]: continue
    for _ in range(50):
        c = .5 * (a + b); sc = cross(c, p2, j, h, A, B, C, U1, U2)
        if sc[1] != sa[1] or sc[2] != sa[2] or not np.isfinite(sc[0]): break
        if np.sign(sc[0]) == np.sign(sa[0]): a, sa = c, sc
        else: b, sb = c, sc
    p1 = .5 * (a + b); s0, m0, n0, ts = cross(p1, p2, j, h, A, B, C, U1, U2)
    T = 2 * ts; steps = int(round(T / (h / 4))); hh = T / steps
    q = np.array([0.0, 0.0, p1, p2]); tip = []
    for k in range(steps):
        if k % 8 == 0: tip.append((math.sin(q[0]) + math.sin(q[1]), -(math.cos(q[0]) + math.cos(q[1]))))
        q = np.array(rk4(q[0], q[1], q[2], q[3], hh, A, B, C, U1, U2))
    w = lambda x: (x + math.pi) % (2 * math.pi) - math.pi
    err = max(abs(w(q[0])), abs(w(q[1])), abs(q[2] - p1), abs(q[3] - p2))
    n1, n2 = round(q[0] / (2 * math.pi)), round(q[1] / (2 * math.pi))
    E = (B * p1 * p1 - 2 * C * p1 * p2 + A * p2 * p2) / (2 * (A * B - C * C)) - U1 - U2
    out.append(dict(p1=p1, p2=p2, T=T, n1=n1, n2=n2, E=E, err=err, tip=tip))
    print(f'({n1:3d},{n2:3d})  p=({p1:8.4f},{p2:8.4f})  T={T:.3f} s  E={E:7.1f} J  closure {err:.1e}', flush=True)
json.dump(out, open(sys.argv[2], 'w'))
