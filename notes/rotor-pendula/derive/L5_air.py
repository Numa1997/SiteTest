"""A first estimate of the air on the second blade (chapter 8). Quasi-steady thin-aerofoil forces on a 1 m second blade at
the 63 m tip, at 8 m/s, rotor at lambda*, wind slowed by a third at the rotor (section 0.2).
  steady in-plane force   F_t = q S (C_L sin g - C_D cos g),  q = rho W^2/2, S = chord x length, g the inflow angle (0.4)
  steady lean             sin theta_s = F_t / (m Omega^2 r_p)  (its torque F_t l/2 against the centrifugal spring)
  rotor's gain            F_t Omega r_p
  once per turn           wind shear: axial wind u(z) = v (z/z_hub)^alpha at the tip's height z = z_hub + r_p sin phi, first
                          sine harmonic, times (1 - a); it turns the inflow angle by cos(g) du/W
                          shaft tilt: the in-plane wind v sin(tilt) adds cos(phi) of itself to the blade's own speed
                          dF_t = 2 F_t dW/W + q S (a0 sin g + C_L cos g + C_D sin g) dg, with dW and dg from each source
  small-swing power       goes as the push squared: [(G +- A_tilt)^2 + A_shear^2]/G^2 (tilt in step with gravity's push,
                          shear a quarter turn out of step), G = (m l/2) g
  air damping of the swing  c_air <= rho W S l^2/3 (C_D + |C_L| sin g + pi sin^2 g), against c* (2.6)
Inputs: rho 1.225, mu 1.81e-5; tilt 5 deg and hub height 90 m (Jonkman et al. 2009); alpha 0.2 (the IEC normal wind
profile); C_D 0.01 for a smooth wing section and 1.2 for a round rod near Re 5e4 (textbook values); lift slope 2 pi per
radian (thin-aerofoil theory); chord 0.1 m and C_L 1 are illustrative choices, not a design.
Run: python3 -I L5_air.py   (writes L5_air.json)
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup as S
rho, mu, g = S.RHO, 1.81e-5, S.G0
rp, m, l = S.R_ROT, S.M_B, S.L_B
v = 8.0; Om = S.omega(v); a = 1/3
ut = Om*rp; ua = v*(1 - a); W = math.hypot(ut, ua); gam = math.atan2(ua, ut); q = 0.5*rho*W**2
Gt = m*l/2*g; cstar = (m*l/2*rp - m*l*l/3)*Om
tilt, hub, alpha_sh = math.radians(5.0), 90.0, 0.2
ph = np.linspace(0, 2*math.pi, 4001)[:-1]
u = v*((hub + rp*np.sin(ph))/hub)**alpha_sh
du = 2*np.mean(u*np.sin(ph))*(1 - a)                    # first sine harmonic of the axial wind at the rotor
dW_t = v*math.sin(tilt)
d_rod = 2*math.sqrt(m/l/7850/math.pi)
cases = [('rod', 'bare steel rod', d_rod, 0.0, 1.2, 0.0), ('sym', 'streamlined, no lift', 0.1, 0.0, 0.01, 2*math.pi),
         ('wing', 'small wing', 0.1, 1.0, 0.01, 2*math.pi)]
out = dict(v=v, W=W, gam_deg=math.degrees(gam), q=q, G_torque=Gt, cstar=cstar, du_shear=du, dW_tilt=dW_t,
           dgam_shear_deg=math.degrees(du*math.cos(gam)/W), Re_rod=rho*W*d_rod/mu, Re_wing=rho*W*0.1/mu, d_rod=d_rod, cases={})
for key, name, chord, CL, CD, a0 in cases:
    Sa = chord*l
    Ft = q*Sa*(CL*math.sin(gam) - CD*math.cos(gam))
    lean = math.degrees(math.asin(max(-1, min(1, Ft/(m*Om**2*rp)))))
    k_g = q*Sa*(a0*math.sin(gam) + CL*math.cos(gam) + CD*math.sin(gam))      # dF_t / d(inflow angle) at fixed W
    dg_s, dW_s = du*math.cos(gam)/W, du*math.sin(gam)
    dg_t, dW_tt = -dW_t*math.sin(gam)/W, dW_t*math.cos(gam)
    A_s = abs(2*Ft*dW_s/W + k_g*dg_s)*l/2
    A_t = abs(2*Ft*dW_tt/W + k_g*dg_t)*l/2
    lo = ((Gt - A_t)**2 + A_s**2)/Gt**2; hi = ((Gt + A_t)**2 + A_s**2)/Gt**2
    c_air = rho*W*Sa*l**2/3*(CD + abs(CL)*math.sin(gam) + math.pi*math.sin(gam)**2)
    out['cases'][key] = dict(name=name, chord=chord, CL=CL, CD=CD, Ft=Ft, lean_deg=lean, P_rotor=Ft*ut, A_shear=A_s, A_tilt=A_t,
                             ratio_lo=lo, ratio_hi=hi, c_air=c_air)
    print(f"{name}: F_t {Ft:+.1f} N, lean {lean:+.1f} deg, rotor {Ft*ut:+.0f} W; once per turn shear {A_s:.2f} N m, tilt {A_t:.2f} N m "
          f"(gravity {Gt:.2f}); power x{lo:.2f} to x{hi:.2f}; air damping {c_air:.3f} N m s against c* {cstar:.1f}")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L5_air.json'), 'w'), indent=1)
