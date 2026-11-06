# Added mass of a 2D body moving along x in unbounded potential flow, by a constant-strength source panel method.
# m11 = rho * ∮ phi n_x ds per metre of depth, phi the potential for unit velocity (dphi/dn = n_x on the body; n outward).
# Check: circle of radius a -> rho pi a^2.
import numpy as np, sys
def panels_rect(W, H, n):   # graded panels on a rectangle (cosine spacing on each side, fine at the corners)
    pts = []
    def side(p, q, m):
        s = 0.5 * (1 - np.cos(np.linspace(0, np.pi, m + 1)))
        return [p + (q - p) * t for t in s[:-1]]
    c = [np.array([W/2, -H/2]), np.array([W/2, H/2]), np.array([-W/2, H/2]), np.array([-W/2, -H/2])]
    m = [int(n * H / (2 * (W + H))), int(n * W / (2 * (W + H)))] * 2
    for k in range(4): pts += side(c[k], c[(k + 1) % 4], max(m[k], 4))
    return np.array(pts)
def panels_circle(a, n):
    t = np.linspace(0, 2 * np.pi, n + 1)[:-1]; return np.c_[a * np.cos(t), a * np.sin(t)]
def added_mass(P):
    A = P; B = np.roll(P, -1, axis=0); mid = (A + B) / 2; L = np.linalg.norm(B - A, axis=1); t = (B - A) / L[:, None]; nrm = np.c_[t[:, 1], -t[:, 0]]   # counter-clockwise -> outward normal (t_y, -t_x)
    N = len(P); # influence of a unit source panel j on point i: phi = (1/2pi) ∫ ln r ds ; dphi/dn by Gauss quadrature (self term 1/2)
    g, gw = np.polynomial.legendre.leggauss(16); g = (g + 1) / 2; gw = gw / 2
    An = np.zeros((N, N)); Ap = np.zeros((N, N))
    for j in range(N):
        q = A[j][None, :] + np.outer(g, B[j] - A[j])   # quadrature points on panel j
        d = mid[:, None, :] - q[None, :, :]; r2 = (d ** 2).sum(-1)
        An[:, j] = (L[j] / (2 * np.pi)) * ((d * nrm[:, None, :]).sum(-1) / r2 * gw).sum(1)
        Ap[:, j] = (L[j] / (2 * np.pi)) * (0.5 * np.log(r2) * gw).sum(1)
        An[j, j] = 0.5
        # exact self-integral of ln r over a straight panel from its midpoint: L (ln(L/2) - 1)
        Ap[j, j] = (L[j] * (np.log(L[j] / 2) - 1)) / (2 * np.pi)
    sig = np.linalg.solve(An, nrm[:, 0]); phi = Ap @ sig
    return (phi * nrm[:, 0] * L).sum() * -1   # m11/rho with the sign of the outward-normal convention used here
for n in (200, 400, 800): print('circle a=0.1, n', n, 'm/(rho pi a^2) =', added_mass(panels_circle(0.1, n)) / (np.pi * 0.01))
for n in (400, 800, 1600, 3200): m = added_mass(panels_rect(0.36, 0.12, n)); print('rect 0.36 x 0.12 along x, n', n, 'm/rho =', m, ' in units of rho pi (h/2)^2:', m / (np.pi * 0.06 ** 2))
