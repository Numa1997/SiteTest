"""Fig. 12 reference model in NumPy/SciPy: the numbers of the note, and the page's numbers to compare against.

Run: python3 notes/fig12/physics.py
"""
import numpy as np
from scipy.linalg import solve_continuous_are
import json, sys

# ---------- the rig ----------
MA, RA = 0.10, 0.16            # arm: a uniform bar of 0.10 kg, 0.16 m from the axis to the hinge
JH = 2.0e-4                    # hub and motor rotor, kg m^2
MP, LP = 0.08, 0.30            # pendulum: a uniform rod of 0.08 kg and 0.30 m, hinged at one end
G0 = 9.81
BR, BP = 1.0e-4, 2.0e-5        # bearing friction of the arm and of the pendulum's hinge, N m s
KM, RM, LAM, VMAX = 0.10, 4.0, 2.0e-3, 12.0   # motor constant N m/A = V s, winding resistance, inductance, supply limit

JR = MA * RA**2 / 3 + JH
J0 = JR + MP * RA**2
JP = MP * LP**2 / 3
HH = MP * RA * LP / 2
GG = MP * G0 * LP / 2
DEL = J0 * JP - HH**2

def wrap(a):
    return (a + np.pi) % (2 * np.pi) - np.pi

def accel(y, V):
    ph, al, w, v = y
    I = (V - KM * w) / RM
    tau = KM * I
    s, c = np.sin(al), np.cos(al)
    M = np.array([[J0 + JP * s * s, HH * c], [HH * c, JP]])
    rhs = np.array([tau - BR * w - 2 * JP * s * c * w * v + HH * s * v * v,
                    JP * s * c * w * w + GG * s - BP * v])
    a = np.linalg.solve(M, rhs)
    return a, I, tau

def energy(y):
    ph, al, w, v = y
    s, c = np.sin(al), np.cos(al)
    return 0.5 * (J0 + JP * s * s) * w * w + HH * c * w * v + 0.5 * JP * v * v + GG * c

def Ep(y):
    return 0.5 * JP * y[3]**2 + GG * np.cos(y[1])

def linear():
    A = np.array([[0, 0, 1, 0], [0, 0, 0, 1],
                  [0, -HH * GG / DEL, -JP * (BR + KM**2 / RM) / DEL, HH * BP / DEL],
                  [0, J0 * GG / DEL, HH * (BR + KM**2 / RM) / DEL, -J0 * BP / DEL]])
    B = np.array([[0], [0], [JP * KM / (RM * DEL)], [-HH * KM / (RM * DEL)]])
    return A, B

def numlin(al0):
    e = 1e-6; y0 = np.array([0, al0, 0, 0.]); A = np.zeros((4, 4)); B = np.zeros((4, 1))
    def f(y, V): a, _, _ = accel(y, V); return np.array([y[2], y[3], a[0], a[1]])
    for j in range(4):
        d = np.zeros(4); d[j] = e; A[:, j] = (f(y0 + d, 0) - f(y0 - d, 0)) / (2 * e)
    B[:, 0] = (f(y0, e) - f(y0, -e)) / (2 * e)
    return A, B

def lqr(A, B, Q, rho):
    P = solve_continuous_are(A, B, np.diag(Q), np.array([[rho]]))
    K = (B.T @ P / rho).ravel()
    return K, P

class Ctl:
    def __init__(s, mode='swing', phistar=0.0, Q=(2, 40, 0.5, 2), rho=1.0, kE=40.0, amax=30.0, kphi=4.0, kw=3.0, cin=None, cout=None):
        s.mode, s.phistar, s.kE, s.amax, s.kphi, s.kw = mode, phistar, kE, amax, kphi, kw
        A, B = linear(); s.K, s.P = lqr(A, B, Q, rho)
        s.cin, s.cout = cin, cout
        s.caught = False
    def err(s, y):
        return np.array([wrap(y[0] - s.phistar), wrap(y[1]), y[2], y[3]])
    def lyap(s, y):
        e = s.err(y); return e @ s.P @ e
    def decide(s, y):
        # once per step: catch when the Lyapunov value of the LQR falls below cin, drop back above cout
        if s.mode == 'lqr': s.caught = True; return
        if s.mode == 'off': s.caught = False; return
        L = s.lyap(y)
        if not s.caught and L < s.cin: s.caught = True
        elif s.caught and L > s.cout: s.caught = False
    def volt(s, y):
        if s.mode == 'off': return 0.0
        if s.caught:
            V = -s.K @ s.err(y)
        else:
            ph, al, w, v = y
            uE = s.kE * (Ep(y) - GG) * v * np.cos(al)
            uE = np.clip(uE, -s.amax, s.amax)
            u = uE - s.kphi * wrap(ph - s.phistar) - s.kw * w
            # the torque that gives the arm the acceleration u (12), then the voltage that gives that torque
            sn, c = np.sin(al), np.cos(al)
            aldd = (-HH * c * u + JP * sn * c * w * w + GG * sn - BP * v) / JP
            tau = (J0 + JP * sn * sn) * u + HH * c * aldd + 2 * JP * sn * c * w * v - HH * sn * v * v + BR * w
            V = RM * tau / KM + KM * w
        return float(np.clip(V, -VMAX, VMAX))

def rk4(y, h, ctl, acc):
    def f(z):
        V = ctl.volt(z); a, I, tau = accel(z, V)
        return np.array([z[2], z[3], a[0], a[1], V * I, RM * I * I, BR * z[2]**2 + BP * z[3]**2])
    z = np.concatenate([y, [0, 0, 0]])
    k1 = f(z[:4]); k2 = f(z[:4] + h / 2 * k1[:4]); k3 = f(z[:4] + h / 2 * k2[:4]); k4 = f(z[:4] + h * k3[:4])
    d = h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    acc += d[4:]
    return y + d[:4]

def run(y0, ctl, T=20.0, h=5e-4, every=20, rec=True):
    y = np.array(y0, float); acc = np.zeros(3); out = []; E0 = energy(y); n = int(round(T / h)); tcatch = None
    for i in range(n + 1):
        if rec and i % every == 0:
            out.append([i * h, *y, ctl.volt(y), energy(y), *acc, ctl.caught])
        if i == n: break
        ctl.decide(y)
        if ctl.caught and tcatch is None: tcatch = i * h
        y = rk4(y, h, ctl, acc)
        if abs(y[2]) > 500: break
    bal = E0 + acc[0] - acc[1] - acc[2] - energy(y)
    return np.array(out) if rec else None, y, bal, tcatch

if __name__ == '__main__':
    A, B = linear(); An, Bn = numlin(0.0)
    print('J_r, J0, Jp, h, G, Delta =', JR, J0, JP, HH, GG, DEL)
    print('A analytic vs numeric max diff', np.abs(A - An).max(), np.abs(B - Bn).max())
    print('open-loop eigenvalues at the top', np.sort_complex(np.linalg.eigvals(A)))
    Ad, Bd = numlin(np.pi)
    print('open-loop eigenvalues at the bottom', np.sort_complex(np.linalg.eigvals(Ad)))
    print('bare pendulum on a fixed pivot: sqrt(G/Jp) =', np.sqrt(GG / JP), ' with the arm recoiling: sqrt(J0 G/Delta) =', np.sqrt(J0 * GG / DEL))
    print('electrical time Lambda/R =', LAM / RM, 's; pendulum time sqrt(Jp/G) =', np.sqrt(JP / GG))
    C = np.hstack([B, A @ B, A @ A @ B, A @ A @ A @ B]); print('rank C =', np.linalg.matrix_rank(C), ' cond', np.linalg.cond(C))
    c = Ctl(mode='lqr'); print('K =', c.K); print('closed-loop eig', np.sort_complex(np.linalg.eigvals(A - B @ c.K[None, :])))
