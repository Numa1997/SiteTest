"""NREL 5-MW reference turbine: constants (cited) and the derived numbers L2 and L3 need (computed here).

Run: python3 -I nrel5mw.py   (prints the table; PASS/FAIL against the cited values; exit 1 on any FAIL)
Sources (dossier-turbine.md has page and line for each):
  S1 Jonkman, Butterfield, Musial, Scott (2009) NREL/TP-500-38060: Tables 1-1, 2-2, 4-1, 5-1, 7-2, 9-1.
  S2 OpenFAST r-test, 5MW_Baseline/NRELOffshrBsline5MW_Blade.dat: distributed blade properties, edgewise mode shape.
  ROSCO Examples/Test_Cases/NREL-5MW/Cp_Ct_Cq.NREL5MW.txt (NREL/ROSCO on GitHub, written 13 Jan 2022): C_p(lambda, beta).
"""
import math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R_TIP, R_HUB, Z_HUB = 63.0, 1.5, 90.0                     # m (S1 Table 1-1)
OM_RATED, OM_MIN = 12.1, 6.9                               # rpm (S1 Table 1-1)
N_GEAR = 97.0                                              # (S1 Table 5-1)
I_HUB, I_GEN = 115926.0, 534.116                           # kg m^2 (S1 Tables 4-1, 5-1; generator on the high-speed shaft)
M_BLADE, S_ROOT, I_ROOT = 17740.0, 363231.0, 11776047.0    # kg, kg m, kg m^2 about the blade root (S1 Table 2-2)
PRECONE, TILT = 2.5, 5.0                                   # deg (S1 Table 1-1)
ZETA_BLADE = 0.477465e-2                                   # structural damping, all blade modes (S1 Table 2-2; S2)
F_EDGE_SYS = 1.0793                                        # Hz, 1st blade asymmetric edgewise, full system, FAST (S1 Table 9-1)
K_RGN2 = 0.0255764                                         # N m / rpm^2 on the generator shaft (S1 Table 7-2)
GEN_R1, GEN_R2, GEN_RATED = 670.0, 871.0, 1161.963         # generator rpm: region 1/1.5, 1.5/2, rated (S1 Table 7-2)
SLIP_25 = 0.10                                             # region 2.5 slip (S1 Table 7-2)
TQ_RATED = 43093.55                                        # N m, generator (S1 Table 7-2)
P_RATED_MECH = 5296610.0                                   # W (S1 Table 7-2)
EDGE_SHAPE = [0.3627, 2.5337, -3.5772, 2.376, -0.6952]     # coefficients of x^2..x^6 (S2 lines 77-81)
ADJ_BL_MS = 1.04536                                        # blade mass factor (S2 line 11)
RHO_AIR = 1.225                                            # kg/m^3 (S1)

def blade_table():
    rows = []
    for line in open(os.path.join(HERE, 'data', 'NRELOffshrBsline5MW_Blade.dat')):
        p = line.split()
        if len(p) == 5:
            try:
                rows.append([float(x) for x in p])
            except ValueError:
                pass
    return np.array(rows)            # BlFract, StrcTwst, BMassDen, FlpStff, EdgStff

def edge_shape(x):
    return sum(c*x**(k + 2) for k, c in enumerate(EDGE_SHAPE))
def edge_shape_xx(x):
    return sum(c*(k + 2)*(k + 1)*x**k for k, c in enumerate(EDGE_SHAPE))

def cp_table():
    L = open(os.path.join(HERE, 'data', 'Cp_Ct_Cq.NREL5MW.txt')).read().split('\n')
    pitch = np.array(L[4].split(), float); tsr = np.array(L[6].split(), float)
    rows = [l for l in L[12:12 + 40] if l.strip() and not l.startswith('#')][:len(tsr)]
    cp = np.array([r.split() for r in rows], float)
    return tsr, pitch, cp

def gen_torque_lss(Om):
    """baseline variable-speed torque law (S1 section 7.2), returned on the low-speed shaft (N m), Om in rad/s"""
    wg = np.asarray(Om)*N_GEAR*60/(2*math.pi)                 # generator rpm
    q2 = K_RGN2*wg**2
    w_sync = GEN_RATED/(1 + SLIP_25)
    slope25 = TQ_RATED/(GEN_RATED - w_sync)
    # region 2 / 2.5 boundary: where k w^2 meets slope25 (w - w_sync)
    a, b, c = K_RGN2, -slope25, slope25*w_sync
    w_tr = (-b - math.sqrt(b*b - 4*a*c))/(2*a)
    q15 = K_RGN2*GEN_R2**2*(wg - GEN_R1)/(GEN_R2 - GEN_R1)
    q25 = slope25*(wg - w_sync)
    qg = np.where(wg < GEN_R1, 0.0, np.where(wg < GEN_R2, q15, np.where(wg < w_tr, q2,
                  np.where(wg < GEN_RATED, q25, P_RATED_MECH/(wg*2*math.pi/60)))))
    return qg*N_GEAR, w_tr

if __name__ == '__main__':
    fails = 0
    def check(name, ok):
        global fails
        fails += (not ok); print(('PASS ' if ok else 'FAIL ') + name)
    tab = blade_table()
    Lb = R_TIP - R_HUB
    x = tab[:, 0]; mu = tab[:, 2]; EIe = tab[:, 4]
    mb = np.trapezoid(mu, x*Lb)
    print(f'blade mass from the table: {mb:.0f} kg; x AdjBlMs {ADJ_BL_MS}: {mb*ADJ_BL_MS:.0f} kg (S1: {M_BLADE:.0f} kg)')
    # rotor inertia about the shaft from S1 Table 2-2 (blade about its root), the hub radius and the precone
    cpc = math.cos(math.radians(PRECONE))
    I_blade_axis = cpc**2*I_ROOT + 2*R_HUB*cpc*S_ROOT + R_HUB**2*M_BLADE
    J_rotor = 3*I_blade_axis + I_HUB
    J_total = J_rotor + N_GEAR**2*I_GEN
    print(f'rotor inertia about the shaft {J_rotor:.4e} kg m^2; with the generator cast to the low-speed shaft (N^2 I_gen = '
          f'{N_GEAR**2*I_GEN:.4e}) J = {J_total:.4e} kg m^2')
    check('rotor inertia within 0.1 % of the value 38 759 236 kg m^2 reported for the model (scout lead)',
          abs(J_rotor/38759236 - 1) < 1e-3)
    # edgewise mode: modal mass (tip-normalised shape), Rayleigh frequency (non-rotating, isolated blade)
    phi = edge_shape(x); phixx = edge_shape_xx(x)/Lb**2
    for adj, lab in ((1.0, 'table'), (ADJ_BL_MS, 'x AdjBlMs')):
        m_e = np.trapezoid(adj*mu*phi**2, x*Lb)
        k_e = np.trapezoid(EIe*phixx**2, x*Lb)
        print(f'edgewise modal mass ({lab}): {m_e:.1f} kg; modal stiffness {k_e:.4e} N/m; Rayleigh frequency '
              f'{math.sqrt(k_e/m_e)/(2*math.pi):.4f} Hz (full system, FAST: {F_EDGE_SYS} Hz)')
    m_e = np.trapezoid(ADJ_BL_MS*mu*phi**2, x*Lb)
    g_e = np.trapezoid(ADJ_BL_MS*mu*phi, x*Lb)
    print(f'modal gravity factor int mu Phi dr = {g_e:.1f} kg (gravity modal force amplitude {g_e*9.80665/1e3:.1f} kN)')
    for frac in (0.3, 0.6, 0.9):
        xs = (frac*R_TIP - R_HUB)/Lb
        print(f'  pivot at {frac*100:.0f} % of the rotor radius (r = {frac*R_TIP:.1f} m, x = {xs:.4f}): Phi = {edge_shape(xs):.4f}, '
              f'mass ratio of a 0.1 kg bob mu = m Phi^2/m_e = {0.1*edge_shape(xs)**2/m_e:.2e}')
    # steady operating point at 8 m/s, pitch 0
    tsr, pitch, cp = cp_table()
    j0 = int(np.where(pitch == 0.0)[0][0])
    from scipy.interpolate import CubicSpline
    cps = CubicSpline(tsr, cp[:, j0])
    def q_aero(v, Om):
        lam = Om*R_TIP/v
        return 0.5*RHO_AIR*math.pi*R_TIP**3*v**2*cps(lam)/lam
    from scipy.optimize import brentq
    v = 8.0
    Om8 = brentq(lambda O: q_aero(v, O) - gen_torque_lss(O)[0], 0.5, 1.5)
    lam8 = Om8*R_TIP/v
    P8 = q_aero(v, Om8)*Om8
    _, w_tr = gen_torque_lss(1.0)
    dO = 1e-5
    dQ = (q_aero(v, Om8 + dO) - gen_torque_lss(Om8 + dO)[0] - q_aero(v, Om8 - dO) + gen_torque_lss(Om8 - dO)[0])/(2*dO)
    tau = J_total/(-dQ)
    print(f'region 2/2.5 boundary at generator {w_tr:.1f} rpm = rotor {w_tr/N_GEAR:.2f} rpm')
    print(f'steady state at 8 m/s: Omega = {Om8:.4f} rad/s = {Om8*60/2/math.pi:.3f} rpm, lambda = {lam8:.3f}, '
          f'C_p = {float(cps(lam8)):.4f}, aerodynamic power {P8/1e6:.3f} MW')
    print(f'rotor time constant J/(-d(Q_aero - Q_gen)/dOmega) = {tau:.2f} s')
    check('peak C_p of the ROSCO table at pitch 0 is near 7.5 (lambda grid 0.5)', abs(tsr[np.argmax(cp[:, j0])] - 7.5) < 0.26)
    print('ALL PASS' if fails == 0 else f'{fails} FAIL'); sys.exit(1 if fails else 0)
