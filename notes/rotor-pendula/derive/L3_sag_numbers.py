"""L3: size of the blade-sag effect on the pendulum's power at the NREL 5-MW pivots (linear theory from L3_sag.py).
Run: python3 -I L3_sag_numbers.py
Blade-angle form: theta'' + kappa theta' + R theta = -(G + 2 w/L) cos(phi) + kappa beta',  beta = -w' cos(phi);
the generator takes c <(thetadot - betadot)^2>.  Sag w(r) = Phi(x) * x_tip, x_tip = (int mu Phi dr) g / k_e (static, first
edgewise mode, nrel5mw.py), slope w' = Phi'(x) x_tip / L_b; dynamic amplification at 1P, 1/(1 - (Omega/omega_e)^2).
"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup as S
import nrel5mw as T5
g = 9.80665*math.cos(math.radians(5.0)); m, L = S.M, S.L
tab = T5.blade_table(); Lb = T5.R_TIP - T5.R_HUB; x = tab[:, 0]; mu = tab[:, 2]*T5.ADJ_BL_MS
phi = T5.edge_shape(x)
m_e = np.trapezoid(mu*phi**2, x*Lb); g_e = np.trapezoid(mu*phi, x*Lb)
om_e = 2*math.pi*T5.F_EDGE_SYS; k_e = m_e*om_e**2
Om = 0.9494
amp = 1/(1 - (Om/om_e)**2)
x_tip = g_e*9.80665*math.cos(math.radians(5.0))/k_e*amp
print(f'modal mass {m_e:.0f} kg, f_e {T5.F_EDGE_SYS} Hz, 1P amplification {amp:.4f}: 1P tip sag {x_tip:.3f} m')
dshape = lambda xx: sum(cc*(k + 2)*xx**(k + 1) for k, cc in enumerate(T5.EDGE_SHAPE))
for frac in (0.3, 0.6, 0.9):
    rp = frac*T5.R_TIP; xs = (rp - T5.R_HUB)/Lb
    w = T5.edge_shape(xs)*x_tip; wp = dshape(xs)*x_tip/Lb
    R = rp/L; G = g/(Om**2*L); k = R - 1
    def P(Gf, beta_amp):
        # theta = Re[A e^{i phi}]: (R - 1 + i k) A = -Gf + k * (i beta_amp)  [beta' = Re(i*(-beta_amp) e^{i phi})... see below]
        # beta = -wp cos(phi) = Re[-wp e^{i phi}] -> beta' = Re[-i wp e^{i phi}]; generator power ~ k |i(A - B)|^2 / 2
        B = -beta_amp
        A = (-Gf + k*1j*B)/(R - 1 + 1j*k)
        return k*abs(A - B)**2/2
    P0 = P(G, 0.0); P1 = P(G + 2*w/L, 0.0); P2 = P(G + 2*w/L, wp)
    print(f'pivot {frac*100:.0f} % (r_p {rp:.1f} m): sag w = {w*1e3:.1f} mm, slope {wp*1e3:.2f} mrad; drive +{2*w/L/G*100:.2f} %; '
          f'power: sag in the drive {(P1/P0 - 1)*100:+.2f} %, with the section rotation {(P2/P0 - 1)*100:+.2f} %')
