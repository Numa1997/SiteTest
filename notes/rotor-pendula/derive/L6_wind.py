"""L6: a turbulent wind field over the rotor disc, and the second blade swimming in it (the reference for the Wind tab).

The field (IEC 61400-1 ed. 3 normal turbulence model, Kaimal form, as TurbSim implements it; TurbSim User's Guide 1.50,
Eqs. 21-23, 47, 49, 50, 52):
  mean     U(z) = U_hub (z / 90 m)^0.2                                           (power law, exponent 0.2)
  spectra  S_K(f) = 4 sigma_K^2 (L_K/U_hub) / (1 + 6 f L_K/U_hub)^(5/3),  K = u, v, w (one-sided, m^2/s^2 per Hz)
           sigma_u = I_ref (0.75 U_hub + 5.6 m/s), sigma_v = 0.8 sigma_u, sigma_w = 0.5 sigma_u
           L_u = 8.1 Lambda, L_v = 2.7 Lambda, L_w = 0.66 Lambda, Lambda = 42 m (hub above 60 m)
  coherence, u: exp(-12 sqrt((f r/U_hub)^2 + (0.12 r/L_c)^2)), L_c = 8.1 Lambda = 340.2 m        (IEC, ed. 3)
  coherence, v and w: IEC defines none and TurbSim uses none (Eq. 50); here TurbSim's own default for its SMOOTH model,
           the Davenport form exp(-a f r/U_hub) with a = 0.75 U_hub (Eq. 18 with b = 0, CohExp = 0), so that the crosswind
           gusts have a size too.  The three components are independent of each other.
Synthesis (Veers 1988, as TurbSim): on an 11 x 11 grid, 12.6 m apart, covering the disc; at each frequency f_k = k/T
(k = 1 .. M/2 - 1, T = 256 s, M = 512 samples, dt = 0.5 s) the coherence matrix is factored, C = H H^T (Cholesky), and the
Fourier amplitudes are X = sqrt(2 S Delta f) H xi with xi complex normal of unit variance (so the record's part at f_k has
the covariance S Delta f C); the record is periodic in T.  The
spectrum is scaled so that the expected variance over the kept band is sigma_K^2 exactly.  The random numbers come from
mulberry32 and Box-Muller, the same generator the page uses, so the page's field is this field to rounding.
Between grid points: bilinear in space, Catmull-Rom in time.  Upstream of the rotor (side view only): Taylor's frozen
turbulence, u(x, z, t) = u(0, z, t - x/U(z)) for x < 0.

The machine in it (the same equations the page integrates, RK4 at h = 0.005 s):
  rotor     J Omega' = Q_aero(v_eff, Omega) - Q_gen(Omega), v_eff = mean of U + u over the grid points on the disc,
            Q_aero = rho pi R^3 v^2 C_p(lambda)/(2 lambda) with C_p at pitch 0 from the ROSCO table (Catmull-Rom on its
            0.5 grid), Q_gen the NREL baseline torque law; above rated speed an ideal pitch holds Omega (as turbulence.py)
  blade     (1.5) of the notes with the Euler torque, the brake c fixed at the best brake of the steady rotor speed at the
            mean wind, and the air on the second blade at mid-span (chapter 8's quasi-steady model, local wind from the field,
            induction a = 1/3, shaft tilt 5 deg): shape 'none', 'streamlined' (C_L = 0, C_D = 0.01, chord 0.1 m) or
            'wing' (C_L = 1 + 2 pi (gamma - gamma_0), C_D = 0.01, chord 0.1 m)
  start     the rotor at the steady speed of the wind at t = 0, the second blade on the small-swing swing (2.2)
  energy    the rotor's work on the second blade from Newton's law for its centre of mass (hinge force times hinge
            velocity, less the brake torque times Omega), the air's work, and the harvest are integrated with the motion;
            the book  W_rot + W_air = Delta E + E_h  closes to the integrator's error.

Checks (PASS/FAIL; exit 1 on a failure): the generator against its published test values; the synthesis against the
spectra, variances and coherences it was built from (ensemble of 40 records); the disc average against the averaging
factor chi(f) of turbulence.py (L2); the steady case against P*; the energy book.  Writes L6_wind.json and
L6_wind_ref.json (a short reference record that tools/check_wind.js compares the page with).
Run: python3 -I L6_wind.py   (about 3 minutes)
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nrel5mw as T5

FAILS = 0
def check(name, ok, detail=''):
    global FAILS
    FAILS += (not ok)
    print(('PASS ' if ok else 'FAIL ') + name + (f'  ({detail})' if detail else ''))

# ---------------------------------------------------------------- the generator the page uses: mulberry32 + Box-Muller
M32 = 0xFFFFFFFF
def imul(a, b):
    return (a*b) & M32
class Rng:
    def __init__(self, seed):
        self.a = seed & M32; self.spare = None
    def next(self):
        self.a = (self.a + 0x6D2B79F5) & M32
        t = imul(self.a ^ (self.a >> 15), self.a | 1)
        t = ((t + imul(t ^ (t >> 7), t | 61)) & M32) ^ t
        return ((t ^ (t >> 14)) & M32)/4294967296.0
    def pair(self):
        u1 = 1.0 - self.next(); u2 = self.next()
        r = math.sqrt(-2.0*math.log(u1))
        return r*math.cos(2*math.pi*u2), r*math.sin(2*math.pi*u2)

# ---------------------------------------------------------------- the field
Z_HUB, R_ROT, ALPHA, LAMBDA1 = 90.0, 63.0, 0.2, 42.0
LK = (8.1*LAMBDA1, 2.7*LAMBDA1, 0.66*LAMBDA1)
SK = (1.0, 0.8, 0.5)
L_C = 8.1*LAMBDA1
IREF = {'A': 0.16, 'B': 0.14, 'C': 0.12, 'none': 0.0}
NG, HALF, TREC, DT = 11, 63.0, 256.0, 0.5

def grid():
    c = np.array([-HALF + 2*HALF*i/(NG - 1) for i in range(NG)])
    y, z = np.meshgrid(c, c)                  # point p = iz*NG + iy
    return c, y.ravel(), z.ravel()

def kaimal(f, U, sig, L):
    return 4*sig**2*(L/U)/(1 + 6*f*L/U)**(5/3)

def coherence(comp, f, r, U):
    if comp == 0:
        return np.exp(-12*np.sqrt((f*r/U)**2 + (0.12*r/L_C)**2))
    return np.exp(-0.75*U*f*r/U)

def synth(U, cls, seed):
    """the field's fluctuations: (3, M, P) array u, v, w at the grid points, M = TREC/DT samples"""
    c, y, z = grid(); P = y.size
    M = int(round(TREC/DT)); K = M//2; df = 1.0/TREC
    f = np.arange(1, K)*df
    s1 = IREF[cls]*(0.75*U + 5.6)
    r = np.hypot(y[:, None] - y[None, :], z[:, None] - z[None, :])
    rng = Rng(seed)
    out = np.zeros((3, M, P))
    for comp in range(3):
        sig = SK[comp]*s1
        S = kaimal(f, U, sig, LK[comp]) if sig > 0 else np.zeros_like(f)
        if sig > 0:
            S = S*sig**2/np.sum(S*df)
        Y = np.zeros((M, P), complex)
        for k in range(1, K):
            H = np.linalg.cholesky(coherence(comp, f[k - 1], r, U))
            xi = np.empty(P, complex)
            for mm in range(P):
                a, b = rng.pair()
                xi[mm] = (a + 1j*b)/math.sqrt(2)
            Y[k] = math.sqrt(2)*math.sqrt(S[k - 1]*df)*(H @ xi)
        out[comp] = np.real(np.fft.ifft(Y, axis=0))*M
    return out

def disc_points():
    _, y, z = grid()
    return np.hypot(y, z) <= R_ROT + 1e-9

def mean_U(U, zrel):
    return U*((Z_HUB + zrel)/Z_HUB)**ALPHA

# ---------------------------------------------------------------- the turbine and the second blade (the page's equations)
SETUP = json.load(open(os.path.join(HERE, 'setup.json')))
G0, RHO = SETUP['G0'], SETUP['RHO']
MB, LB, RP = SETUP['M_B'], SETUP['L_B'], SETUP['R_ROT']
IB, MLC = MB*LB*LB/3, MB*LB/2
_tsr, _pitch, _cp = T5.cp_table()
CP0 = _cp[:, int(np.where(_pitch == 0.0)[0][0])]
TSR0, DTSR = float(_tsr[0]), float(_tsr[1] - _tsr[0])
J_ROT = (3*(math.cos(math.radians(T5.PRECONE))**2*T5.I_ROOT + 2*T5.R_HUB*math.cos(math.radians(T5.PRECONE))*T5.S_ROOT
           + T5.R_HUB**2*T5.M_BLADE) + T5.I_HUB + T5.N_GEAR**2*T5.I_GEN)
OM_RATED = T5.OM_RATED*2*math.pi/60
TILT = math.radians(5.0); A_IND = 1/3
SHAPES = {'none': (0.0, 0.0, 0.0), 'streamlined': (0.1, 0.0, 0.01), 'wing': (0.1, 1.0, 0.01)}   # chord m, C_L0, C_D

def catrom(p0, p1, p2, p3, s):
    return 0.5*((2*p1) + (-p0 + p2)*s + (2*p0 - 5*p1 + 4*p2 - p3)*s*s + (-p0 + 3*p1 - 3*p2 + p3)*s**3)

def cp(lam):
    x = (lam - TSR0)/DTSR; n = CP0.size
    x = min(max(x, 0.0), n - 1 - 1e-12); i = int(math.floor(x)); s = x - i
    q = lambda j: CP0[min(max(j, 0), n - 1)]
    return max(catrom(q(i - 1), q(i), q(i + 1), q(i + 2), s), 0.0)

def q_aero(v, Om):
    lam = Om*R_ROT/v
    return 0.5*RHO*math.pi*R_ROT**3*v*v*cp(lam)/lam

def q_gen(Om):
    return float(T5.gen_torque_lss(Om)[0])

def steady_omega(v):
    lo, hi = 0.3, OM_RATED
    if q_aero(v, hi) - q_gen(hi) > 0:
        return hi
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if q_aero(v, mid) - q_gen(mid) > 0: lo = mid
        else: hi = mid
    return 0.5*(lo + hi)

class Field:
    def __init__(self, U, cls, seed):
        self.U, self.cls = U, cls
        self.f = synth(U, cls, seed)                       # (3, M, P)
        c, y, z = grid(); self.c = c; self.z = z
        on = disc_points()
        self.veff = np.mean(mean_U(U, z[on])[None, :] + self.f[0][:, on], axis=1)
        self.M = self.f.shape[1]
    def tindex(self, t):
        x = t/DT; i = math.floor(x); return i, x - i
    def veff_at(self, t):
        i, s = self.tindex(t); M = self.M; v = self.veff
        return catrom(v[(i - 1) % M], v[i % M], v[(i + 1) % M], v[(i + 2) % M], s)
    def at(self, t, y, z):
        """u, v, w fluctuations at (y, z) relative to the hub: bilinear in space, Catmull-Rom in time"""
        gx = (y + HALF)/(2*HALF)*(NG - 1); gz = (z + HALF)/(2*HALF)*(NG - 1)
        gx = min(max(gx, 0.0), NG - 1 - 1e-9); gz = min(max(gz, 0.0), NG - 1 - 1e-9)
        ix, iz = int(gx), int(gz); sx, sz = gx - ix, gz - iz
        ps = (iz*NG + ix, iz*NG + ix + 1, (iz + 1)*NG + ix, (iz + 1)*NG + ix + 1)
        wts = ((1 - sx)*(1 - sz), sx*(1 - sz), (1 - sx)*sz, sx*sz)
        i, s = self.tindex(t); M = self.M
        rows = [(i + d) % M for d in (-1, 0, 1, 2)]
        out = []
        for comp in range(3):
            F = self.f[comp]
            val = 0.0
            for p, wgt in zip(ps, wts):
                val += wgt*catrom(F[rows[0], p], F[rows[1], p], F[rows[2], p], F[rows[3], p], s)
            out.append(val)
        return out

def model(field, shape):
    U = field.U
    vbar = float(np.mean(field.veff))
    Om0 = steady_omega(vbar)
    c_brake = (MLC*RP - IB)*Om0
    chord, CL0, CD = SHAPES[shape]
    gam0 = math.atan2(U*math.cos(TILT)*(1 - A_IND), Om0*RP)
    return dict(Om0=Om0, c=c_brake, chord=chord, CL0=CL0, CD=CD, gam0=gam0, vbar=vbar)

def start(field, md):
    """the rotor at the steady speed of the wind at t = 0; the second blade on the small-swing solution (2.2) at the brake c"""
    Om = steady_omega(float(field.veff[0]))
    R = MLC*RP/IB; Gg = MLC*G0/(IB*Om*Om); k = md['c']/(IB*Om)
    A = -Gg/(R - 1 + 1j*k)
    return [0.0, Om, A.real, (1j*A).real*Om, 0.0, 0.0, 0.0]

def deriv(t, y, field, md):
    phi, Om, th, w, Wr, Wa, Eh = y
    acc = (q_aero(field.veff_at(t), Om) - q_gen(Om))/J_ROT
    if Om >= OM_RATED and acc > 0: acc = 0.0
    # the air at mid-span
    ex, ez = math.cos(phi + th), math.sin(phi + th)
    ym, zm = RP*math.cos(phi) + LB/2*ex, RP*math.sin(phi) + LB/2*ez
    Ft = 0.0
    vpath = Om*RP + (Om + w)*LB/2*math.cos(th)
    if md['chord'] > 0:
        uf, vf, wf = field.at(t, ym, zm)
        Uz = mean_U(field.U, zm)
        wtot = wf + Uz*math.sin(TILT)
        Ut = vpath - (vf*(-math.sin(phi)) + wtot*math.cos(phi))
        Ua = (Uz + uf)*math.cos(TILT)*(1 - A_IND)
        W2 = Ut*Ut + Ua*Ua; gam = math.atan2(Ua, Ut)
        CL = md['CL0'] + (2*math.pi*(gam - md['gam0']) if md['CL0'] != 0 else 0.0)
        Ft = 0.5*RHO*W2*md['chord']*LB*(CL*math.sin(gam) - md['CD']*math.cos(gam))
    tau_air = Ft*LB/2*math.cos(th)
    c = md['c']
    wd = (-MLC*(Om*Om*RP*math.sin(th) + G0*math.cos(phi + th)) - (IB + MLC*RP*math.cos(th))*acc - c*w + tau_air)/IB
    # Newton for the centre of mass: m a_cm = F_hinge + m g + F_air
    er, et = (math.cos(phi), math.sin(phi)), (-math.sin(phi), math.cos(phi))
    e2r, e2t = (ex, ez), (-ez, ex)
    a_cm = [RP*(acc*et[i] - Om*Om*er[i]) + LB/2*((acc + wd)*e2t[i] - (Om + w)**2*e2r[i]) for i in (0, 1)]
    Fh = [MB*a_cm[0] - Ft*et[0], MB*a_cm[1] + MB*G0 - Ft*et[1]]
    vh = (RP*Om*et[0], RP*Om*et[1])
    P_rot = Fh[0]*vh[0] + Fh[1]*vh[1] - c*w*Om
    P_air = Ft*vpath
    return [Om, acc, w, wd, P_rot, P_air, c*w*w]

def energy(y):
    phi, Om, th, w = y[:4]
    T = 0.5*IB*(Om + w)**2 + 0.5*MB*RP*RP*Om*Om + MLC*RP*Om*(Om + w)*math.cos(th)
    V = MB*G0*(RP*math.sin(phi) + LB/2*math.sin(phi + th))
    return T + V

def run(field, shape, T_end, h=0.005, every=100):
    md = model(field, shape)
    y = start(field, md)
    E0 = energy(y); t = 0.0; rec = []; worst = 0.0
    n = int(round(T_end/h))
    for k in range(n + 1):
        if k % every == 0:
            book = y[4] + y[5] - (energy(y) - E0) - y[6]
            worst = max(worst, abs(book)/max(1.0, abs(y[4]) + abs(y[5]) + y[6]))
            rec.append([t] + list(y) + [field.veff_at(t), book])
        if k == n: break
        k1 = deriv(t, y, field, md)
        k2 = deriv(t + h/2, [a + h/2*b for a, b in zip(y, k1)], field, md)
        k3 = deriv(t + h/2, [a + h/2*b for a, b in zip(y, k2)], field, md)
        k4 = deriv(t + h, [a + h*b for a, b in zip(y, k3)], field, md)
        y = [a + h/6*(b1 + 2*b2 + 2*b3 + b4) for a, b1, b2, b3, b4 in zip(y, k1, k2, k3, k4)]
        t += h
    return md, rec, worst

def mean_power(rec, t0):
    """the harvest over the whole turns of the rotor after t0: from the first record past t0 to the last one a whole number
    of turns later (the power swings twice per turn, so a window of whole turns does not bias the mean)"""
    tail = [r for r in rec if r[0] >= t0]
    turns = (tail[-1][1] - tail[0][1])/(2*math.pi)
    want = tail[0][1] + 2*math.pi*math.floor(turns)
    end = min(tail, key=lambda r: abs(r[1] - want))
    return (end[7] - tail[0][7])/(end[0] - tail[0][0])

def p_star(Om):
    return MLC**2*G0**2/(4*Om*(MLC*RP - IB))

if __name__ == '__main__':
    out = {}
    # 1. the torque law against NREL's published values (TP-500-38060 Table 7-2: region 2 constant)
    Om8 = 9.0*2*math.pi/60
    check('torque law in region 2 is k Omega^2', abs(q_gen(Om8)/(T5.K_RGN2*(9.0*97)**2*97) - 1) < 1e-12)
    # 2. the synthesis: an ensemble of 40 records at 8 m/s, class A
    U, cls = 8.0, 'A'; s1 = IREF[cls]*(0.75*U + 5.6)
    c, y, z = grid(); hub = (NG//2)*NG + NG//2; nb = hub + 1           # the hub point and its neighbour 12.6 m to the side
    fields = [synth(U, cls, 1000 + s) for s in range(40)]
    M = fields[0].shape[1]; df = 1/TREC; f = np.arange(1, M//2)*df
    for comp, name in enumerate('uvw'):
        var = np.mean([np.var(F[comp][:, hub]) for F in fields])
        se = np.std([np.var(F[comp][:, hub]) for F in fields])/math.sqrt(len(fields))
        check(f'{name}: hub variance {var:.3f} against sigma^2 {(SK[comp]*s1)**2:.3f}', abs(var - (SK[comp]*s1)**2) < 3*se + 1e-9, f'standard error {se:.3f}')
        out[f'sigma_{name}'] = SK[comp]*s1
        out[f'var_hub_{name}'] = float(var); out[f'var_hub_se_{name}'] = float(se)
    # spectrum and coherence at the hub and its neighbour, averaged over the ensemble, in octave bands
    bands = [(0.01, 0.02), (0.02, 0.04), (0.04, 0.08), (0.08, 0.16), (0.16, 0.32)]
    coh_rows = []
    for comp, name in enumerate('uv'):
        Sxx = np.zeros(M//2 - 1); Syy = np.zeros(M//2 - 1); Sxy = np.zeros(M//2 - 1, complex)
        for F in fields:
            X = np.fft.rfft(F[comp][:, hub])[1:M//2]; Yf = np.fft.rfft(F[comp][:, nb])[1:M//2]
            Sxx += np.abs(X)**2; Syy += np.abs(Yf)**2; Sxy += X*np.conj(Yf)
        for lo, hi in bands:
            m = (f >= lo) & (f < hi)
            est = float(np.real(np.sum(Sxy[m]))/math.sqrt(np.sum(Sxx[m])*np.sum(Syy[m])))
            mod = float(np.mean(coherence(comp, f[m], 2*HALF/(NG - 1), U)))
            coh_rows.append({'comp': name, 'band': [lo, hi], 'estimate': est, 'model': mod})
            check(f'{name}: coherence 12.6 m apart, {lo}-{hi} Hz: {est:.3f} against {mod:.3f}', abs(est - mod) < 0.08)
        if comp == 0:
            sk = kaimal(f, U, s1, LK[0]); sk = sk*s1**2/np.sum(sk*df)
            spec_dev = 0.0
            for lo, hi in bands:
                m = (f >= lo) & (f < hi)
                est = np.sum(Sxx[m])/len(fields)*2/(M*M)/df       # one-sided periodogram, m^2/s^2 per Hz, summed over the band
                spec_dev = max(spec_dev, abs(est/np.sum(sk[m]) - 1))
                out['spec_dev_max'] = spec_dev
                check(f'u: spectrum {lo}-{hi} Hz within 20 % of Kaimal', abs(est/np.sum(sk[m]) - 1) < 0.2, f'ratio {est/np.sum(sk[m]):.3f}')
    out['coherence'] = coh_rows
    # for the figure of the notes: ensemble coherence at 12.6 and 25.2 m, and the u spectrum, in finer log bands
    fb = np.logspace(math.log10(f[0]), math.log10(0.6), 13)
    curves = []
    for comp in (0, 1):
        for step in (1, 2):
            q2 = hub + step
            Sxx = np.zeros(M//2 - 1); Syy = np.zeros(M//2 - 1); Sxy = np.zeros(M//2 - 1, complex)
            for F in fields:
                X = np.fft.rfft(F[comp][:, hub])[1:M//2]; Yf = np.fft.rfft(F[comp][:, q2])[1:M//2]
                Sxx += np.abs(X)**2; Syy += np.abs(Yf)**2; Sxy += X*np.conj(Yf)
            pts = []
            for lo, hi in zip(fb[:-1], fb[1:]):
                m = (f >= lo) & (f < hi)
                if m.sum():
                    pts.append([float(math.sqrt(lo*hi)), float(np.real(np.sum(Sxy[m]))/math.sqrt(np.sum(Sxx[m])*np.sum(Syy[m])))])
            curves.append({'comp': 'uv'[comp], 'r': step*2*HALF/(NG - 1), 'points': pts})
    out['coh_curves'] = curves
    Su = np.zeros(M//2 - 1)
    for F in fields:
        Su += np.abs(np.fft.rfft(F[0][:, hub])[1:M//2])**2
    Su = Su/len(fields)*2/(M*M)/df
    spec = []
    for lo, hi in zip(fb[:-1], fb[1:]):
        m = (f >= lo) & (f < hi)
        if m.sum():
            spec.append([float(math.sqrt(lo*hi)), float(np.mean(Su[m]))])
    out['u_spectrum'] = spec
    out['f_band'] = [float(f[0]), float(f[-1])]
    # 3. the disc average against L2's averaging factor chi(f): the rotor-effective variance
    on = disc_points()
    var_eff = np.mean([np.var(np.mean(F[0][:, on], axis=1)) for F in fields])
    try:
        import turbulence as TB
        sk = kaimal(f, U, s1, LK[0]); sk = sk*s1**2/np.sum(sk*df)
        var_chi = float(np.sum(sk*TB.chi(f, U)*df))
        check(f'disc-average variance {var_eff:.3f} against L2 chi(f) {var_chi:.3f} (grid of {int(on.sum())} points vs a continuous disc)',
              abs(var_eff/var_chi - 1) < 0.25)
        out['var_eff_chi'] = var_chi
    except ImportError:
        print('turbulence.py needs SciPy: the chi(f) comparison is skipped')
    out['var_eff'] = float(var_eff); out['n_disc'] = int(on.sum()); out['grid_step'] = 2*HALF/(NG - 1)
    out['sig_eff_frac'] = math.sqrt(var_eff)/U
    out['L'] = list(LK); out['Lc'] = L_C; out['T'] = TREC; out['dt'] = DT; out['N'] = NG
    # 4. the steady case: no turbulence, no air -> the harvest is P* at the steady rotor speed of the disc-mean wind
    rows = []
    for Uw in (6.0, 8.0, 10.0):
        fld = Field(Uw, 'none', 1)
        md, rec, worst = run(fld, 'none', 120.0)
        Pm = mean_power(rec, 60.0)
        check(f'{Uw} m/s steady: harvest {Pm*1e3:.2f} mW against P* {p_star(md["Om0"])*1e3:.2f} mW', abs(Pm/p_star(md['Om0']) - 1) < 0.01)
        check(f'{Uw} m/s steady: energy book closes, worst {worst:.1e}', worst < 1e-6)
        rows.append({'U': Uw, 'Om0': md['Om0'], 'vbar': md['vbar'], 'P_steady': Pm, 'P_star': p_star(md['Om0'])})
    out['steady'] = rows
    # 5. gusty runs at 8 m/s, class A, record 1: the three shapes, two periods of the field (512 s), measured over the second
    runs = []
    fld = Field(8.0, 'A', 1)
    for shape in ('none', 'streamlined', 'wing'):
        md, rec, worst = run(fld, shape, 2*TREC)
        tail = [r for r in rec if r[0] >= TREC]
        Pm = mean_power(rec, TREC)
        om = np.array([r[2] for r in tail]); th = np.array([r[3] for r in tail])
        check(f'8 m/s class A, {shape}: energy book closes, worst {worst:.1e}', worst < 1e-6)
        runs.append({'shape': shape, 'P_mean': Pm, 'P_star_mean': p_star(md['Om0']), 'Om0': md['Om0'], 'Om_mean': float(om.mean()),
                     'Om_sd': float(om.std()), 'th_mean': float(th.mean()), 'th_sd': float(th.std()), 'book_worst': worst,
                     'vbar': md['vbar']})
        print(f'  {shape}: P {Pm*1e3:.1f} mW (P* at the mean {p_star(md["Om0"])*1e3:.1f}), Omega {om.mean():.4f} +- {om.std():.4f}, theta {th.mean():.4f} +- {th.std():.4f}')
    out['gusty_8A'] = runs
    # the same three shapes in the steady, sheared wind (no turbulence): chapter 8's once-per-turn push, solved in time
    calm = []
    fld0 = Field(8.0, 'none', 1)
    for shape in ('none', 'streamlined', 'wing'):
        md, rec, worst = run(fld0, shape, 120.0)
        Pm = mean_power(rec, 60.0)
        th = np.array([r[3] for r in rec if r[0] >= 60])
        calm.append({'shape': shape, 'P_mean': Pm, 'th_mean': float(th.mean()), 'P_star': p_star(md['Om0'])})
        print(f'  steady shear, {shape}: P {Pm*1e3:.1f} mW, mean lean {math.degrees(th.mean()):.2f} deg')
    out['calm_8'] = calm
    # a snapshot for the notes: record 1 at t = 0, 8 m/s, class A
    out['snapshot'] = {'u': fld.f[0][0].tolist(), 'v': fld.f[1][0].tolist(), 'w': fld.f[2][0].tolist(), 'y': grid()[1].tolist(), 'z': grid()[2].tolist()}
    # 6. the reference record for the page: field samples and a 60 s run with the wing (every term in use)
    fld1 = Field(8.0, 'A', 1)
    md, rec, worst = run(fld1, 'wing', 60.0, every=200)
    ref = {'U': 8.0, 'cls': 'A', 'seed': 1, 'shape': 'wing',
           'field_samples': [{'comp': cpn, 'k': k, 'p': p, 'value': float(fld1.f[cpn][k, p])}
                             for cpn in range(3) for k in (0, 1, 77, 300, 511) for p in (0, 17, 60, 120)],
           'veff': [float(v) for v in fld1.veff[:64]],
           'Om0': md['Om0'], 'c': md['c'], 'run': [[float(x) for x in r] for r in rec]}
    json.dump(ref, open(os.path.join(HERE, 'L6_wind_ref.json'), 'w'))
    json.dump(out, open(os.path.join(HERE, 'L6_wind.json'), 'w'), indent=1)
    print('FAILURES:', FAILS)
    sys.exit(1 if FAILS else 0)
