"""Curves of closed orbits on the Fig. 13 sheet.
Usage: python3 tools/fig13/closed_map.py W H TMAX OUT.npz [p1a p1b p2a p2b]   (1920 1080 3.0: 452 s on 4 cores)
A strike from hanging still closes (symmetric periodic orbit) exactly when, at some time t*, both rods are straight up or down together.
For each strike, at each of the first J times the upper rod passes straight (theta1 = m pi), record s = theta2 - n pi (signed distance of
the lower rod from straight, n the nearest whole number) and the labels (m, n). Where s changes sign between two neighbouring strikes with
the same labels, a closed orbit lies between them: a curve of closed orbits, with n1 = m and n2 = n turns per lap (lap = 2 t*)."""
import sys, time, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from numba import njit, prange
from chaos_map import rk4, coefficients, CONFIG
A, B, C, U1, U2 = coefficients(CONFIG)
J = 12

@njit(parallel=True)
def crossings(P1, P2, steps, h, J, A, B, C, U1, U2):
    n = P1.size; S = np.full((n, J), np.nan); M = np.zeros((n, J), np.int64); N = np.zeros((n, J), np.int64)
    for i in prange(n):
        q1 = 0.0; q2 = 0.0; p1 = P1[i]; p2 = P2[i]; j = 0
        for k in range(1, steps + 1):
            a1, a2 = q1, q2
            q1, q2, p1, p2 = rk4(q1, q2, p1, p2, h, A, B, C, U1, U2)
            if k * h < 0.02: continue
            fa = np.floor(a1 / np.pi); fb = np.floor(q1 / np.pi)
            if fa != fb:                                   # theta1 passed a multiple of pi during this step
                m = max(fa, fb); u = (m * np.pi - a1) / (q1 - a1); t2 = a2 + u * (q2 - a2)
                nn = np.round(t2 / np.pi); S[i, j] = t2 - nn * np.pi; M[i, j] = int(m); N[i, j] = int(nn); j += 1
                if j >= J: break
    return S, M, N

if __name__ == '__main__':
    W, H, TMAX = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
    PW, PH = 20 * 16 / 9, 20.0
    B1a, B1b, B2a, B2b = (float(x) for x in sys.argv[5:9]) if len(sys.argv) > 8 else (-PW, PW, -PH, PH)
    p1 = B1a + (np.arange(W) + .5) / W * (B1b - B1a); p2 = B2b - (np.arange(H) + .5) / H * (B2b - B2a)
    P1, P2 = np.meshgrid(p1, p2); h = CONFIG['h']; t0 = time.time()
    S, M, N = crossings(P1.ravel(), P2.ravel(), int(TMAX / h), h, J, A, B, C, U1, U2)
    np.savez_compressed(sys.argv[4], S=S.reshape(H, W, J), M=M.reshape(H, W, J), N=N.reshape(H, W, J), box=np.array([p1[0] - (p1[1]-p1[0])/2, p1[-1] + (p1[1]-p1[0])/2, p2[-1] - (p2[0]-p2[1])/2, p2[0] + (p2[0]-p2[1])/2]))
    print(f'{W}x{H}: {time.time() - t0:.0f} s')
