"""Fig. 11, note §1.1 and Figure 2: where the energy of one swing goes.
Linear model (8) at the straight-hanging rest (target r = 0), LQR gains (12)-(14) with q = 5, rho = 0.02,
coil clamped at 30 N, RK4 with h = 0.5 ms for 8 s. Release: ball 2 moved 10 cm to the right (theta2 = 0.2), all else at rest.
Run: python3 notes/fig11/energy_path.py"""
import numpy as np
from scipy.linalg import solve_continuous_are as care
m1 = m2 = 0.5; l1 = l2 = 0.5; Mc = 1.0; g = 9.81; N0 = 3.0; H = 1.65; l0 = H - l1 - l2; Fmax = 30.0; h = 5e-4
M = np.array([[(m1 + m2) * l1**2, m2 * l1 * l2, 0], [m2 * l1 * l2, m2 * l2**2, 0], [0, 0, Mc]])
s = N0 / l0; c = np.array([l1, l2, -1.0])                      # string stiffness N0/l0 and offset x2 - X = c . q
Kc = np.diag([(m1 + m2) * g * l1 + N0 * l1, m2 * g * l2 + N0 * l2, 0]); K = Kc + s * np.outer(c, c)
Mi = np.linalg.inv(M)
A = np.block([[np.zeros((3, 3)), np.eye(3)], [-Mi @ K, np.zeros((3, 3))]]); B = np.r_[np.zeros(3), Mi @ [0, 0, 1]].reshape(6, 1)
P = care(A, B, np.diag([5.0] * 6), np.array([[0.02]])); Kg = (B.T @ P / 0.02).ravel()
E = lambda y: 0.5 * y[3:] @ M @ y[3:] + 0.5 * y[:3] @ K @ y[:3]
def f(y):
    F = np.clip(-Kg @ y, -Fmax, Fmax); return A @ y + B.ravel() * F, F
y = np.array([0, 0.2, 0, 0, 0, 0.0]); y0 = y.copy()
W = Win = Wout = Wchain = Wcart = tsat = 0.0; t = 0.0; marks = {}
while t < 8 - 1e-12:
    k1, F1 = f(y); k2, F2 = f(y + h / 2 * k1); k3, F3 = f(y + h / 2 * k2); k4, F4 = f(y + h * k3)
    for yy, FF, wt in ((y, F1, 1 / 6), (y + h / 2 * k1, F2, 1 / 3), (y + h / 2 * k2, F3, 1 / 3), (y + h * k3, F4, 1 / 6)):
        p = FF * yy[5]; W += wt * h * p; Win += wt * h * max(p, 0); Wout += wt * h * min(p, 0)
        x2 = l1 * yy[0] + l2 * yy[1]; x2d = l1 * yy[3] + l2 * yy[4]; fs = s * (yy[2] - x2)   # sideways pull on ball 2
        Wchain += wt * h * fs * x2d; Wcart += wt * h * (-fs) * yy[5]
    if abs(F1) >= Fmax - 1e-9: tsat += h
    y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4); t += h
    for tt in (0.1, 0.2):
        if abs(t - tt) < h / 2: marks[tt] = (Win, Wout, y[2], l1 * y[0] + l2 * y[1], s * (y[2] - l1 * y[0] - l2 * y[1]))
print(f"gains K = {np.round(Kg, 2)}; F(0) asked {-Kg @ y0:.2f} N, clamped for {tsat*1e3:.1f} ms")
print(f"swing energy {E(y0):.4f} J = chain {0.5 * y0[:3] @ Kc @ y0[:3]:.4f} J + string {0.5 * s * (l2 * 0.2)**2:.4f} J; ball 2 lifted {l2*(1-np.cos(0.2))*100:.2f} cm")
for tt, (wi, wo, X, x2, fs) in marks.items(): print(f"t = {tt} s: coil in {wi:.3f} J, out {wo:+.3f} J; X = {X*100:.1f} cm, x2 = {x2*100:.1f} cm, string pull on ball 2 {fs:+.3f} N")
print(f"after 8 s: coil in {Win:.3f} J, out {Wout:+.3f} J, net {W:+.4f} J; string on chain {Wchain:+.4f} J, on cart {Wcart:+.4f} J; energy left {E(y):.1e} J")
