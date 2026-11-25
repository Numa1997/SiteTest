"""Usage: python3 tools/fig13/closed_stability.py check | MAP.npz OUT.npy JSHOW
Stability of the closed orbits along every family line of closed_map.py.
For each sign change between neighbouring strikes: bisect along the segment to the exact strike (s = 0 at crossing j, same labels), take
T = 2 t*, and compute the monodromy matrix of one lap by central differences (8 trajectories). Its eigenvalues are 1, 1, lam, 1/lam;
the index s = trace - 2 = lam + 1/lam: |s| < 2 stable (a push stays small), s > 2 unstable, s < -2 unstable with a flip each lap."""
import sys, time, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from numba import njit, prange
from chaos_map import rk4, coefficients, CONFIG
A, B, C, U1, U2 = coefficients(CONFIG); h = CONFIG['h']

@njit
def cross(p1, p2, j, h, A, B, C, U1, U2):
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

@njit
def flow(s0, T, A, B, C, U1, U2):
    n = int(np.ceil(T / 2.0e-4)); hh = T / n; q1, q2, a, b = s0[0], s0[1], s0[2], s0[3]
    for _ in range(n): q1, q2, a, b = rk4(q1, q2, a, b, hh, A, B, C, U1, U2)
    return np.array([q1, q2, a, b])

@njit
def index(p1, p2, T, A, B, C, U1, U2):
    eps = 1e-6; tr = 0.0
    for i in range(4):
        sp = np.array([0.0, 0.0, p1, p2]); sm = sp.copy(); sp[i] += eps; sm[i] -= eps
        fp = flow(sp, T, A, B, C, U1, U2); fm = flow(sm, T, A, B, C, U1, U2); tr += (fp[i] - fm[i]) / (2 * eps)
    return tr - 2.0

@njit(parallel=True)
def run(XA, YA, XB, YB, JJ, h, A, B, C, U1, U2):
    n = XA.size; out = np.full((n, 5), np.nan)
    for i in prange(n):
        j = JJ[i]; ax, ay, bx, by = XA[i], YA[i], XB[i], YB[i]
        sa, ma, na, ta = cross(ax, ay, j, h, A, B, C, U1, U2); sb, mb, nb, tb = cross(bx, by, j, h, A, B, C, U1, U2)
        if not (np.isfinite(sa) and np.isfinite(sb)) or ma != mb or na != nb or np.sign(sa) == np.sign(sb): continue
        ok = True; ts = 0.0
        for _ in range(40):
            cx = .5 * (ax + bx); cy = .5 * (ay + by); sc, mc, nc, ts = cross(cx, cy, j, h, A, B, C, U1, U2)
            if not np.isfinite(sc) or mc != ma or nc != na: ok = False; break
            if np.sign(sc) == np.sign(sa): ax, ay, sa = cx, cy, sc
            else: bx, by, sb = cx, cy, sc
        if not ok: continue
        p1 = .5 * (ax + bx); p2 = .5 * (ay + by); T = 2 * ts
        out[i, 0] = p1; out[i, 1] = p2; out[i, 2] = T; out[i, 3] = index(p1, p2, T, A, B, C, U1, U2); out[i, 4] = ma * 1000 + na
    return out

if __name__ == '__main__':
    import json
    if sys.argv[1] == 'check':
        t = open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../public/scripts/fig13-hunt-data.js')).read(); G = json.loads(t[t.index('{'):t.rindex('}') + 1])['garden']
        for g in G: print(f"{g['kind']:9} {g['k']:2}: index here {index(g['p1'], g['p2'], g['period'], A, B, C, U1, U2):9.4f}   flower hunt's trace {g['trace']:9.4f}   ({g['stability']})")
        sys.exit()
    d = np.load(sys.argv[1]); S = d['S']; M = d['M']; N = d['N']; H, W, J = S.shape; JS = int(sys.argv[3])
    PW, PH = 20 * 16 / 9, 20.0; BOX = list(d['box']) if 'box' in d.files else [-PW, PW, -PH, PH]
    P1 = lambda x: BOX[0] + (x + .5) / W * (BOX[1] - BOX[0]); P2 = lambda y: BOX[3] - (y + .5) / H * (BOX[3] - BOX[2])
    XA, YA, XB, YB, JJ = [], [], [], [], []
    for j in range(JS):
        s, m, n = S[..., j], M[..., j], N[..., j]
        for axis in (0, 1):
            if axis == 1: sa, sb, ma, mb, na, nb = s[:, :-1], s[:, 1:], m[:, :-1], m[:, 1:], n[:, :-1], n[:, 1:]
            else: sa, sb, ma, mb, na, nb = s[:-1, :], s[1:, :], m[:-1, :], m[1:, :], n[:-1, :], n[1:, :]
            with np.errstate(invalid='ignore'):
                ok = (ma == mb) & (na == nb) & np.isfinite(sa) & np.isfinite(sb) & (np.sign(sa) != np.sign(sb)) & (np.abs(sa) < .6) & (np.abs(sb) < .6)
            yy, xx = np.nonzero(ok)
            XA.append(P1(xx)); YA.append(P2(yy)); XB.append(P1(xx + (axis == 1))); YB.append(P2(yy + (axis == 0))); JJ.append(np.full(len(yy), j))
    XA, YA, XB, YB, JJ = (np.concatenate(v) for v in (XA, YA, XB, YB, JJ)); print('segments', len(XA), flush=True)
    t0 = time.time(); out = run(XA, YA, XB, YB, JJ.astype(np.int64), h, A, B, C, U1, U2)
    np.save(sys.argv[2], out); ok = np.isfinite(out[:, 3]); s = out[ok, 3]
    print(f'{time.time()-t0:.0f} s; orbits pinned {ok.sum()}; stable {np.mean(np.abs(s) < 2):.3f}, unstable (s>2) {np.mean(s >= 2):.3f}, unstable with flip (s<-2) {np.mean(s <= -2):.3f}')
