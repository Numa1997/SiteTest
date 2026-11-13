#!/usr/bin/env python3
"""Stage A of the controlled Guinness rides: the model and the controllers, derived and checked exactly.

    python3 tools/fig12/control/derive.py            # prints every number; exits 1 if a gate fails
    python3 tools/fig12/control/derive.py > tools/fig12/control/derive.out.txt

Nothing here simulates. It derives (SymPy, exact where possible; SciPy for the Riccati equations and matrix
exponentials) the numbers the controllers of public/scripts/stout-cart.js use, and compares them with what the
site's own code prints (node tools/fig12/observer.cjs 3d | modal). The same matrices are evaluated a second time
in Wolfram Language (tools/fig12/control/derive.wl, output in derive.wl.out.txt).

Sections
  1  the first sloshing mode: xi_11, omega_11, the higher modes, breaking amplitude
  2  the forced mode: the push x = r cos(theta) expanded in J1 modes; coupling beta; static share 2/(xi^2 - 1)
  3  damping numbers (wall boundary layer)
  4  the linear plant (speed, swing, integral) and its controllability from the motor current and from u_s
  5  the slosh LQR (continuous Riccati): gains and poles, for each plant frequency in use
  6  the suspension LQR with its cross term: gains and poles
  7  the Kalman filter: exact zero-order hold, Van Loan's Q_d, the settled gain with a probe every n samples
  8  the joint controller's cancellation current
"""
import sys
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.linalg import expm, solve_continuous_are

mp.mp.dps = 30
FAIL = []


def gate(name, got, want, tol):
    """Compare with the site's printed number: |got - want| <= tol (tol = half a unit of the last digit given)."""
    ok = abs(got - want) <= tol
    print(f"   {'ok  ' if ok else 'FAIL'} {name}: {got:.6g} (site {want:g}, tolerance {tol:g})")
    if not ok:
        FAIL.append(name)


g = 9.81
# ---------------------------------------------------------------------------------------------- 1. the first mode
print("1. First sloshing mode of an upright cylinder, radius R, depth h")
xi = [mp.findroot(lambda x: mp.besselj(0, x) - mp.besselj(1, x) / x, x0) for x0 in (1.84, 5.33, 8.54)]  # J1'(x) = 0
print("   zeros of J1': " + ", ".join(mp.nstr(v, 10) for v in xi))
# J1'(x) = J0(x) - J1(x)/x: SymPy confirms the identity used for the root search
x = sp.symbols('x', positive=True)
assert sp.simplify(sp.diff(sp.besselj(1, x), x).rewrite(sp.besselj) - (sp.besselj(0, x) - sp.besselj(1, x) / x)) == 0


def omega(n, R, h):
    return mp.sqrt(g * xi[n] / R * mp.tanh(xi[n] * h / R))


for label, R, h in (("site, R(h) = 39.1 mm", 0.0391, 0.125),):
    f = [float(omega(n, R, h) / (2 * mp.pi)) for n in range(3)]
    print(f"   {label}, h = 125 mm: f_11, f_12, f_13 = {f[0]:.3f}, {f[1]:.3f}, {f[2]:.3f} Hz; omega_11 = {float(omega(0, R, h)):.2f} rad/s")
    gate("f_11 (Hz)", f[0], 3.421, 0.0005)
    gate("f_12 (Hz)", f[1], 5.821, 0.0005)
    gate("f_13 (Hz)", f[2], 7.365, 0.0005)
    w11 = float(omega(0, R, h))
    print(f"   linear breaking amplitude g/omega^2 = {g / w11 ** 2 * 1e3:.1f} mm at the wall")
    gate("g/omega^2 (mm)", g / w11 ** 2 * 1e3, 21.2, 0.05)

# ---------------------------------------------------------------------------------------------- 2. the forced mode
print("2. The push expanded in the modes, and the coupling beta")
# In the glass's frame a push a_x adds the potential a_x x = a_x r cos(theta). Expand r on 0 <= r <= R in
# J1(xi_n r/R) (orthogonal with weight r because J1'(xi_n) = 0):  r = sum_n c_n J1(xi_n r/R),
#   c_n = int_0^R r^2 J1 dr / int_0^R r J1^2 dr.  Closed forms (checked numerically below):
#   int_0^R r^2 J1(xi r/R) dr = R^3 J2(xi)/xi = R^3 J1(xi)/xi^2   (J2(xi) = J1(xi)/xi when J1'(xi) = 0)
#   int_0^R r J1(xi r/R)^2 dr = R^2 (xi^2 - 1) J1(xi)^2 / (2 xi^2)
# so c_n = 2 R / ((xi_n^2 - 1) J1(xi_n)), and the wall height of mode n under a steady push is
#   q_n = -(R a_x/g) * 2/(xi_n^2 - 1):  the share 2/(xi_n^2 - 1) of the full tilt R a_x/g.
shares = []
for n in range(3):
    X = xi[n]
    num = mp.quad(lambda r: r ** 2 * mp.besselj(1, X * r), [0, 1])
    den = mp.quad(lambda r: r * mp.besselj(1, X * r) ** 2, [0, 1])
    c_num = num / den
    c_closed = 2 / ((X ** 2 - 1) * mp.besselj(1, X))
    assert abs(c_num - c_closed) < mp.mpf(10) ** -20, (c_num, c_closed)
    shares.append(float(2 / (X ** 2 - 1)))
print("   wall-height shares 2/(xi_n^2 - 1), n = 1..3: " + ", ".join(f"{s:.4f}" for s in shares))
# the shares of all modes add up to 1 (the full tilt): partial sum of the first 200
many = [mp.findroot(lambda x: mp.besselj(0, x) - mp.besselj(1, x) / x, 1.84 + mp.pi * k + (0.35 if k else 0)) for k in range(200)]
many = sorted(set(round(float(v), 9) for v in many))
print(f"   sum of 2/(xi_n^2 - 1) over the first {len(many)} modes = {sum(2 / (v * v - 1) for v in many):.5f} (-> 1)")
# Mode equation: q'' + 2 zeta w q' + w^2 (1 + a_z/g) q = -beta a_x. A steady push must give the static share:
#   w^2 q = -beta a_x = -(2/(xi^2 - 1)) (R a_x/g) w^2  =>  beta = 2 xi tanh(xi h/R) / (xi^2 - 1)
xs, hs, Rs, gs, ax_, w_ = sp.symbols('xi h R g a_x omega', positive=True)
beta_sym = sp.solve(sp.Eq(w_ ** 2 * (-(2 / (xs ** 2 - 1)) * Rs * ax_ / gs), -sp.Symbol('beta') * ax_), sp.Symbol('beta'))[0]
beta_sym = sp.simplify(beta_sym.subs(w_ ** 2, gs * xs / Rs * sp.tanh(xs * hs / Rs)))
print("   beta =", beta_sym)
beta = float(beta_sym.subs({xs: sp.Float(str(xi[0]), 25), hs: 0.125, Rs: 0.0391}))
print(f"   beta(first mode) = {beta:.4f}")
gate("beta", beta, 1.5407, 0.00005)
gate("first mode's share", shares[0], 0.837, 0.0005)

# ---------------------------------------------------------------------------------------------- 3. damping
print("3. Wall boundary-layer damping, Lambda = K nu^(1/2) R^(-3/4) g^(-1/4), zeta = Lambda / (2 pi)")
nu, R = 1.0e-6, 0.0391
for K_, src, want in ((3.52, "laminar theory", 0.0036), (5.23, "measured, NASA TN D-1367", 0.0053)):
    z = K_ * nu ** 0.5 * R ** -0.75 * g ** -0.25 / (2 * np.pi)
    print(f"   K = {K_} ({src}): zeta = {z:.5f}")
    gate(f"zeta, K = {K_}", z, want, 0.00005)
print(f"   Stokes layer sqrt(2 nu/omega) = {np.sqrt(2 * nu / w11) * 1e3:.3f} mm")

# ---------------------------------------------------------------------------------------------- 4. plant
print("4. The linear plant and what each actuator can reach")
Mb, mw, Rw, Iw, Ng, Km, Jm, cx, kS, cS, kt, ct, Imax, Ts = 1.5, 0.3, 0.04, 2.4e-4, 10, 0.02, 2e-6, 2.0, 600.0, 8.0, 2.0e4, 5.0, 3.0, 1e-3
b = Ng * Km / Rw


def massX(ml):
    return Mb + ml + mw + (Iw + Ng * Ng * Jm) / Rw ** 2


print(f"   b = N K_m / R_w = {b:g} N/A;  M_x = {massX(0.4266):.4f} kg (site, stout 426.6 g), {massX(0.4296):.4f} kg (Kaggle, 429.6 g)")
gate("M_x site (kg)", massX(0.4266), 2.5016, 0.00005)
wc = 2 * np.pi * 8
print(f"   PI speed loop: K_p = M_x w_c / b = {massX(0.4296) * wc / b:.4f} A/(m/s), K_i = K_p w_c / 4 = {massX(0.4296) * wc / b * wc / 4:.3f} A/m (Kaggle mass)")
gate("K_p Kaggle", massX(0.4296) * wc / b, 25.178818315223719, 1e-3)
gate("K_i Kaggle", massX(0.4296) * wc / b * wc / 4, 316.40636258071589, 2e-2)
gate("c_sky Kaggle", 2 * 0.7 * np.sqrt(kS * (Mb + 0.4296)), 47.636016270456992, 1e-3)

# symbolic: state (dv, q, q', xi_int), input di.  M_x dv' = b di - c_x dv;  q'' = -w^2 q - 2 z w q' - beta dv';  xi' = -dv
Mx_, b_, cx_, w, z, be = sp.symbols('M_x b c_x omega zeta beta', positive=True)
A4 = sp.Matrix([[-cx_ / Mx_, 0, 0, 0], [0, 0, 1, 0], [be * cx_ / Mx_, -w ** 2, -2 * z * w, 0], [-1, 0, 0, 0]])
B4 = sp.Matrix([b_ / Mx_, 0, -be * b_ / Mx_, 0])
C4 = sp.Matrix.hstack(*[A4 ** k * B4 for k in range(4)])
detC = sp.factor(C4.det())
print("   controllability determinant, motor current:", detC)
assert detC != 0 and sp.simplify(detC - be ** 2 * b_ ** 4 * w ** 4 / Mx_ ** 4) == 0
print("   = beta^2 b^4 omega^4 / M_x^4: non-zero whenever beta, b, omega are; the current reaches all four states.")
# the whole level-road linear plant with both actuators: (dv, q, q', s, v_b, v_w, d); u_s enters only the vertical block,
# and the heave a_z enters the swing as -w^2 (a_z/g) q: a product of two small quantities, zero in the linearisation.
Ms_, mw_, k_, c_, kt_, ct_ = sp.symbols('M_s m_w k c k_t c_t', positive=True)
Av = sp.Matrix([[0, 1, -1, 0], [-k_ / Ms_, -c_ / Ms_, c_ / Ms_, 0], [k_ / mw_, c_ / mw_, -(c_ + ct_) / mw_, kt_ / mw_], [0, 0, -1, 0]])
Bv = sp.Matrix([0, 1 / Ms_, -1 / mw_, 0])
A7 = sp.diag(A4[:3, :3], Av)
Bu = sp.Matrix.vstack(sp.zeros(3, 1), Bv)
C7 = sp.Matrix.hstack(*[A7 ** k * Bu for k in range(7)])
rank_us = C7.rank()
print(f"   rank of the controllability matrix from u_s on the 7 states (dv, q, q', s, v_b, v_w, d): {rank_us}; rows of (dv, q, q') all zero: {C7[:3, :] == sp.zeros(3, 7)}")
assert rank_us == 4 and C7[:3, :] == sp.zeros(3, 7)
print("   So the active force reaches the four vertical states and, linearly, nothing of the speed or the swing (note 8.6).")

# ---------------------------------------------------------------------------------------------- 5. slosh LQR
print("5. Slosh LQR: minimise int (x'Qx + r u^2) dt, Bryson weights 0.05 m/s, 2 mm, 2 mm x omega, 0.02 m, 3 A")


def slosh_lqr(wn, zeta, beta_, Mx):
    A = np.array([[-cx / Mx, 0, 0, 0], [0, 0, 1, 0], [beta_ * cx / Mx, -wn * wn, -2 * zeta * wn, 0], [-1, 0, 0, 0]])
    B = np.array([[b / Mx], [0], [-beta_ * b / Mx], [0]])
    Q = np.diag(1 / np.array([0.05, 0.002, 0.002 * wn, 0.02]) ** 2)
    Rr = np.array([[1 / Imax ** 2]])
    P = solve_continuous_are(A, B, Q, Rr)
    K = (B.T @ P / Rr[0, 0]).ravel()
    res = A.T @ P + P @ A - P @ B @ B.T @ P / Rr[0, 0] + Q
    poles = np.linalg.eigvals(A - B @ K[None, :])
    return K, poles, np.abs(res).max() / np.abs(Q).max()


def show_lqr(label, wn, zeta, beta_, Mx):
    K, poles, res = slosh_lqr(wn, zeta, beta_, Mx)
    sw = [p for p in poles if abs(p.imag) > 1e-6]
    zcl = -sw[0].real / abs(sw[0])
    print(f"   {label}: K = ({K[0]:.2f}, {K[1]:.1f}, {K[2]:.2f}, {K[3]:.1f});  poles " + ", ".join(f"{p.real:.2f}{p.imag:+.2f}j" if abs(p.imag) > 1e-6 else f"{p.real:.2f}" for p in sorted(poles, key=lambda p: p.real)) + f";  swing damping ratio {zcl:.3f};  Riccati residual {res:.1e}")
    return K, sw[0], zcl


K, sw, zcl = show_lqr("site 3D plant (4 mm grid: 3.214 Hz, zeta 0.008)", 2 * np.pi * 3.214, 0.008, beta, massX(0.4266))
for i, (want, tol) in enumerate(((76.69, 0.02), (-1934, 1.0), (-41.32, 0.02), (-150.0, 0.05))):
    gate(f"K[{i}]", K[i], want, tol)
gate("swing pole, real part (1/s)", sw.real, -11.33, 0.01)
gate("swing pole, |imaginary part| (1/s)", abs(sw.imag), 7.54, 0.01)
gate("swing damping ratio", zcl, 0.832, 0.001)
K, sw, zcl = show_lqr("site live model (3.421 Hz, zeta 0.005349)", w11, 0.005348992643617189, beta, massX(0.4266))
for i, (want, tol) in enumerate(((75.03, 0.02), (-1939, 1.0), (-38.81, 0.02), (-150.0, 0.05))):
    gate(f"K_live[{i}]", K[i], want, tol)
gate("live swing pole, real part", sw.real, -12.01, 0.01)
gate("live swing pole, |imaginary part|", abs(sw.imag), 8.82, 0.01)
print("   K[3] = -sqrt(Q_44 / r) = -(1/0.02) x 3 = -150 A/m exactly (the integral state's weight against the current's).")
# the plant of the Kaggle solver v2 at 1.5 mm, wall + foam (tools/fig12/kaggle/free_swing_fit.py: 3.29-3.33 Hz, zeta 0.018)
for fK, zK in ((3.31, 0.018),):
    show_lqr(f"Kaggle solver v2 plant ({fK} Hz, zeta {zK}, 429.6 g)", 2 * np.pi * fK, zK, beta, massX(0.4296))

# ---------------------------------------------------------------------------------------------- 6. suspension LQR
print("6. Suspension LQR on y = (stroke, v_b, v_w, tyre compression); cost: body acceleration 0.5 m/s^2, stroke 10 mm, tyre 0.2 mm, force 40 N")


def susp_lqr(ml):
    Ms = Mb + ml
    A = np.array([[0, 1, -1, 0], [-kS / Ms, -cS / Ms, cS / Ms, 0], [kS / mw, cS / mw, -(cS + ct) / mw, kt / mw], [0, 0, -1, 0]])
    B = np.array([[0], [1 / Ms], [-1 / mw], [0]])
    Ca = np.array([-kS / Ms, -cS / Ms, cS / Ms, 0]); Da = 1 / Ms; wa = 1 / 0.5 ** 2
    Q = wa * np.outer(Ca, Ca) + np.diag([1 / 0.010 ** 2, 0, 0, 1 / 0.0002 ** 2])
    N = (wa * Ca * Da)[:, None]
    Rr = np.array([[wa * Da * Da + 1 / 40.0 ** 2]])
    P = solve_continuous_are(A, B, Q, Rr, s=N)
    K = ((B.T @ P + N.T) / Rr[0, 0]).ravel()
    return K, np.linalg.eigvals(A - B @ K[None, :])


Ks, ps = susp_lqr(0.4266)
print(f"   site mass: K_s = ({Ks[0]:.1f}, {Ks[1]:.2f}, {Ks[2]:.2f}, {Ks[3]:.1f});  poles " + ", ".join(sorted({f"{p.real:.2f} +- {abs(p.imag):.2f}j" for p in ps})))
for i, (want, tol) in enumerate(((-502.6, 0.1), (11.6, 0.06), (-6.1, 0.06), (612.6, 0.1))):
    gate(f"K_s[{i}]", Ks[i], want, tol)
pr = sorted(ps, key=lambda p: -p.real)
gate("slow suspension pole, real part", pr[0].real, -4.94, 0.01)
gate("slow suspension pole, |imaginary part|", abs(pr[0].imag), 4.98, 0.01)
gate("fast suspension pole, real part", pr[-1].real, -32.0, 0.06)
gate("fast suspension pole, |imaginary part|", abs(pr[-1].imag), 259.9, 0.06)
Ks2, _ = susp_lqr(0.4296)
print(f"   Kaggle mass (429.6 g): K_s = ({Ks2[0]:.2f}, {Ks2[1]:.3f}, {Ks2[2]:.3f}, {Ks2[3]:.2f})")

# ---------------------------------------------------------------------------------------------- 7. Kalman filter
print("7. Kalman filter on z = (v, q, q'): exact zero-order hold over T_s = 1 ms, Van Loan's Q_d, Joseph form")


def kalman_design(wn, zeta, beta_, Mx, WF=0.5, Wa=0.002):
    A = np.array([[-cx / Mx, 0, 0], [0, 0, 1], [beta_ * cx / Mx, -wn * wn, -2 * zeta * wn]])
    B = np.array([b / Mx, 0, -beta_ * b / Mx])
    G = np.array([[1 / Mx, 0], [0, 0], [-beta_ / Mx, 1]])
    M4 = np.zeros((4, 4)); M4[:3, :3] = A * Ts; M4[:3, 3] = B * Ts
    E4 = expm(M4); Ad, Bd = E4[:3, :3], E4[:3, 3]
    GWG = G @ np.diag([WF, Wa]) @ G.T
    M6 = np.zeros((6, 6)); M6[:3, :3] = -A * Ts; M6[:3, 3:] = GWG * Ts; M6[3:, 3:] = A.T * Ts
    E6 = expm(M6)
    Qd = Ad @ E6[:3, 3:]; Qd = 0.5 * (Qd + Qd.T)
    return A, B, Ad, Bd, Qd


def kalman_settle(Ad, Qd, every, sigV=0.002, sigQ=0.0008, wn=1.0):
    """The covariance's cycle with the speed read every sample and the probes every `every` samples."""
    P = np.diag([sigV ** 2, sigQ ** 2, (sigQ * wn) ** 2])
    L = None
    for k in range(40000):
        Pp = Ad @ P @ Ad.T + Qd
        rows = [0, 1] if k % every == every - 1 else [0]
        H = np.eye(3)[rows]; Rm = np.diag([sigV ** 2, sigQ ** 2])[np.ix_(rows, rows)]
        S = H @ Pp @ H.T + Rm
        Lk = Pp @ H.T @ np.linalg.inv(S)
        I = np.eye(3) - Lk @ H
        P = I @ Pp @ I.T + Lk @ Rm @ Lk.T; P = 0.5 * (P + P.T)
        if len(rows) == 2:
            L = Lk; Pprobe = P
    return L, Pprobe


A, B, Ad, Bd, Qd = kalman_design(2 * np.pi * 3.214, 0.008, beta, massX(0.4266))
print("   site 3D plant: A_d =", np.array2string(Ad, precision=4, suppress_small=False).replace("\n", " "))
print("   B_d =", np.array2string(Bd, precision=4), " Q_d diag =", np.array2string(np.diag(Qd), precision=4))
gate("A_d[2,1]", Ad[2, 1], -0.4077, 0.00005)
gate("A_d[2,0]", Ad[2, 0], 0.001231, 5e-7)
gate("B_d[0]", Bd[0], 0.001998, 5e-7)
gate("B_d[2]", Bd[2], -0.003078, 5e-7)
gate("Q_d[0,0]", Qd[0, 0], 0.00007983, 5e-9)
gate("Q_d[1,1]", Qd[1, 1], 6.383e-11, 5e-15)
gate("Q_d[2,2]", Qd[2, 2], 0.0001914, 5e-8)
# Q_d against its definition, int_0^Ts e^{As} G W G' e^{A's} ds, by Gauss-Legendre quadrature (independent of Van Loan)
G_ = np.array([[1 / massX(0.4266), 0], [0, 0], [-beta / massX(0.4266), 1]]); GWG = G_ @ np.diag([0.5, 0.002]) @ G_.T
xg, wg = np.polynomial.legendre.leggauss(12)
Qq = sum(wq * Ts / 2 * expm(A * (Ts / 2 * (xq + 1))) @ GWG @ expm(A.T * (Ts / 2 * (xq + 1))) for xq, wq in zip(xg, wg))
print(f"   Van Loan against 12-point quadrature of the definition: largest relative difference {np.abs(Qd - Qq).max() / np.abs(Qd).max():.1e}")
assert np.abs(Qd - Qq).max() / np.abs(Qd).max() < 1e-10
L, P = kalman_settle(Ad, Qd, 5, wn=2 * np.pi * 3.214)
print(f"   probes every 5 samples (the site's 5 ms fluid step): gain on y_q = ({L[1, 1]:.4f}, {L[2, 1]:.3f} 1/s); sd of q after it {np.sqrt(P[1, 1]) * 1e3:.3f} mm")
gate("Kalman gain q", L[1, 1], 0.1429, 0.00005)
gate("Kalman gain q' (1/s)", L[2, 1], 2.187, 0.0005)
gate("Kalman gain v on speed", L[0, 0], 0.9544, 0.00005)
gate("estimate sd of q (mm)", np.sqrt(P[1, 1]) * 1e3, 0.302, 0.0005)
A, B, Ad, Bd, Qd = kalman_design(w11, 0.005348992643617189, beta, massX(0.4266))
L, P = kalman_settle(Ad, Qd, 5, wn=w11)
gate("live model: Kalman gain q", L[1, 1], 0.1394, 0.00005)
gate("live model: Kalman gain q' (1/s)", L[2, 1], 2.075, 0.0005)
A, B, Ad, Bd, Qd = kalman_design(2 * np.pi * 3.31, 0.018, beta, massX(0.4296))
L, P = kalman_settle(Ad, Qd, 2, wn=2 * np.pi * 3.31)
print(f"   Kaggle plant (3.31 Hz, zeta 0.018), probes every 2 samples (Kaggle's 2 ms fluid step): gain on y_q = ({L[1, 1]:.4f}, {L[2, 1]:.3f} 1/s); sd of q {np.sqrt(P[1, 1]) * 1e3:.3f} mm")

# ---------------------------------------------------------------------------------------------- 8. joint
print("8. The joint controller's cancellation current")
# swing: q'' = -w^2 (1 + a_z/g) q - 2 z w q' - beta dv'.  An extra current di gives dv' = b di / M_x, so the swing gets
# -beta b di / M_x. Asking that this cancels the parametric term -w^2 (a_z/g) q:
az, q_, di = sp.symbols('a_z q di', real=True)
sol = sp.solve(sp.Eq(-be * b_ * di / Mx_ - w ** 2 * (az / gs) * q_, 0), di)[0]
print("   i_par =", sol, "  (stout-cart.js line 1602: -M_x w^2 (a_z/g) q / (beta b))")
assert sp.simplify(sol + Mx_ * w ** 2 * az * q_ / (be * b_ * gs)) == 0
print(f"   example: a_z = 3 m/s^2, q = 5 mm, 3.31 Hz, Kaggle mass: i_par = {-massX(0.4296) * (2 * np.pi * 3.31) ** 2 * (3 / g) * 0.005 / (beta * b):.3f} A (limit 3 A)")

print()
print("GATE A:", "passed, every site number reproduced to the digits given" if not FAIL else "FAILED: " + "; ".join(FAIL))
sys.exit(1 if FAIL else 0)
