"""L2 inputs: IEC 61400-1 ed. 3 turbulence at hub height, its rotor-effective average, and the one-state rotor of the NREL 5-MW.

Wind (TurbSim user's guide 1.50, Eqs. 21-23, 47, 49, the IEC Kaimal model; I_ref from IEC 61400-1 ed. 3 Table 1 as printed in
EMD windPRO 4.1 LOADS manual): sigma_1 = I_ref (0.75 V + 5.6 m/s); Lambda_1 = 42 m above 60 m; L_u = 8.1 Lambda_1;
  S_u(f) = 4 sigma_1^2 (L_u/V) / (1 + 6 f L_u/V)^(5/3)   (one-sided, m^2/s^2 per Hz)
  Coh(r, f) = exp(-12 sqrt((f r/V)^2 + (0.12 r/L_c)^2)),  L_c = 8.1 Lambda_1.
Records: 600 s, periodic (FFT synthesis without the zero frequency, as TurbSim), mean exactly V.  The spectrum is scaled so a
record's expected hub-point variance is sigma_1^2 (TurbSim's ScaleIEC = 1 scales each record to it exactly).
Rotor-effective wind: the uniform average of u over the rotor disc, spectrum S_u(f) chi(f), chi(f) = int p(r) Coh(r, f) dr with
p(r) the distribution of the distance between two random points of a disc of radius R (disk line picking).
Rotor (one state): J Omega' = Q_aero(v, Omega) - Q_gen(Omega), Q_aero = rho pi R^3 v^2 C_p(lambda)/(2 lambda), lambda = Omega R/v,
C_p(lambda) at pitch 0 from the ROSCO table; Q_gen the NREL baseline torque law (regions 1-3) on the low-speed shaft.  Above
rated speed an ideal pitch controller holds Omega at rated (modelling choice; its time fraction is reported).
"""
import math
import numpy as np
from scipy.interpolate import CubicSpline
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nrel5mw as T5

def iec_sigma(V, Iref=0.16):
    return Iref*(0.75*V + 5.6)

LAMBDA1 = 42.0
L_U = 8.1*LAMBDA1
L_C = 8.1*LAMBDA1

def kaimal(f, V, sigma):
    return 4*sigma**2*(L_U/V)/(1 + 6*f*L_U/V)**(5/3)

def disc_pair_pdf(r, R):
    s = r/(2*R)
    return 4*r/(math.pi*R**2)*(np.arccos(s) - s*np.sqrt(1 - s*s))

def chi(f, V, R=T5.R_TIP, n=2000):
    """rotor-disc averaging factor of the u-spectrum (0 < chi <= 1)"""
    r = (np.arange(n) + 0.5)*(2*R/n)
    p = disc_pair_pdf(r, R)*(2*R/n)
    f = np.atleast_1d(f)
    coh = np.exp(-12*np.sqrt((f[:, None]*r[None, :]/V)**2 + (0.12*r[None, :]/L_C)**2))
    return coh @ p

def synth(V, sigma, T=600.0, dt=0.1, nrec=1, seed=0, rotor_eff=True):
    """nrec periodic records of length T, step dt: (nrec, K) array of wind speed (m/s); spectrum scaled so the expected
    hub-point record variance is sigma^2.  rotor_eff: apply the disc-average factor chi(f)."""
    K = int(round(T/dt)); f = np.fft.rfftfreq(K, dt)[1:]
    df = 1.0/T
    S = kaimal(f, V, sigma)
    S *= sigma**2/np.sum(S*df)                                  # expected record variance at the hub = sigma^2
    if rotor_eff:
        S = S*chi(f, V)
    rng = np.random.default_rng(seed)
    amp = np.sqrt(S*df/4)                                        # Re, Im variance S df/4: x = 2 Re(X e^{i theta}) has variance S df
    X = np.zeros((nrec, K//2 + 1), complex)
    X[:, 1:] = (rng.standard_normal((nrec, f.size)) + 1j*rng.standard_normal((nrec, f.size)))*amp
    if K % 2 == 0:
        X[:, -1] = X[:, -1].real*np.sqrt(2)                      # Nyquist bin is real
    u = np.fft.irfft(X, n=K, axis=1)*K
    return V + u

_tsr, _pitch, _cp = T5.cp_table()
_cps = CubicSpline(_tsr, _cp[:, int(np.where(_pitch == 0.0)[0][0])])
OM_RATED = T5.OM_RATED*2*math.pi/60
J_TOTAL = (3*(math.cos(math.radians(T5.PRECONE))**2*T5.I_ROOT + 2*T5.R_HUB*math.cos(math.radians(T5.PRECONE))*T5.S_ROOT
             + T5.R_HUB**2*T5.M_BLADE) + T5.I_HUB + T5.N_GEAR**2*T5.I_GEN)

def cp(lam):
    lam = np.clip(lam, _tsr[0], _tsr[-1])
    return np.maximum(_cps(lam), 0.0)

def q_aero(v, Om):
    lam = Om*T5.R_TIP/v
    return 0.5*T5.RHO_AIR*math.pi*T5.R_TIP**3*v**2*cp(lam)/lam

def rotor_accel(v, Om):
    """Omega' (rad/s^2) of the one-state rotor, with the ideal-pitch speed limit at rated."""
    acc = (q_aero(v, Om) - T5.gen_torque_lss(Om)[0])/J_TOTAL
    return np.where((Om >= OM_RATED) & (acc > 0), 0.0, acc)

class WindInterp:
    """Catmull-Rom interpolation in time of per-member periodic wind records (nrec, K), step dt."""
    def __init__(self, V, dt):
        self.V = V; self.dt = dt; self.K = V.shape[1]
    def __call__(self, t):
        x = t/self.dt; i = int(math.floor(x)); s = x - i
        K = self.K
        p0, p1, p2, p3 = (self.V[:, (i - 1) % K], self.V[:, i % K], self.V[:, (i + 1) % K], self.V[:, (i + 2) % K])
        return 0.5*((2*p1) + (-p0 + p2)*s + (2*p0 - 5*p1 + 4*p2 - p3)*s*s + (-p0 + 3*p1 - 3*p2 + p3)*s**3)

def rotor_only(V, dt, Om0, T, h=0.05):
    """integrate the rotor alone (RK4) over records V (nrec, K): returns times, Omega (nrec, n), Omega' (nrec, n)"""
    w = WindInterp(V, dt)
    n = int(round(T/h)); Om = np.full(V.shape[0], Om0, float)
    ts = np.arange(n + 1)*h; out = np.empty((V.shape[0], n + 1)); acc = np.empty_like(out)
    out[:, 0] = Om; acc[:, 0] = rotor_accel(w(0.0), Om)
    for k in range(n):
        t = k*h
        k1 = rotor_accel(w(t), Om); k2 = rotor_accel(w(t + h/2), Om + h/2*k1)
        k3 = rotor_accel(w(t + h/2), Om + h/2*k2); k4 = rotor_accel(w(t + h), Om + h*k3)
        Om = np.minimum(Om + h/6*(k1 + 2*k2 + 2*k3 + k4), OM_RATED)
        out[:, k + 1] = Om; acc[:, k + 1] = rotor_accel(w(t + h), Om)
    return ts, out, acc
