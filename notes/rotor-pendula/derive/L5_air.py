"""A first estimate of the air on the second blade (chapter 7). Quasi-steady aerofoil forces on a 1 m second blade at the
63 m tip, 8 m/s, rotor at lambda*. The rotor turns anticlockwise seen from upwind; phi is the mother blade's angle from the
horizontal; theta is positive in the direction of rotation.
Forces per blade, with U_t the head wind along the path (the blade's own speed, less any in-plane wind) and U_a the wind
along the shaft at the tip (v(1 - a), a between 1/3, the disc's average, and 0, air outside the disc):
  W = sqrt(U_t^2 + U_a^2);   in-plane force along the path, + forwards:  F_t = q S (C_L U_a/W - C_D U_t/W),  q = rho W^2/2
  C_L = C_L0 + a0 (gamma - gamma0): the section keeps its pitch, so the lift follows the inflow angle gamma = atan(U_a/U_t).
Steady lean: the torque F_t (l/2) cos(theta) balances the centrifugal (m l/2) Omega^2 r_p sin(theta): tan(theta_s) = F_t/(m Omega^2 r_p).
The steady force and the outward pull add to a field Omega^2 r_p / cos(theta_s): the centrifugal stiffness becomes R/cos(theta_s).
Once per turn (torques about the hinge, at the lean):
  gravity  -(m l/2) g cos(phi + theta_s) = -(m l/2) g [cos(theta_s) cos(phi) - sin(theta_s) sin(phi)]
  shear    the axial wind at height 90 + r_p sin(phi), u = v (z/90)^0.2, first sine harmonic du (times 1 - a):  dF_t/dU_a du sin(phi)
  tilt     the shaft points 5 deg up, so the wind has v sin 5 deg pointing up the rotor plane; along the path that is
           v sin 5 deg cos(phi), and it lowers the head wind: dU_t = -v sin 5 deg cos(phi)
  each air torque is (l/2) cos(theta_s) times the force change.
Small-swing best power goes as |push|^2 / (R_eff - 1); against gravity alone on a straight blade:
  ratio = (c^2 + s^2)/G^2 * (R - 1)/(R/cos(theta_s) - 1), with c and s the cos(phi) and sin(phi) amplitudes.
Air damping of the swing: a swing at theta' raises the head wind on the piece at s by s theta', so c_air = -(dF_t/dU_t) l^2/3.
Inputs: rho 1.225, mu 1.81e-5; tilt 5 deg, hub 90 m (Jonkman et al. 2009); shear exponent 0.2 (IEC normal wind profile);
C_D 0.01 (smooth wing section) and 1.2 (round rod near Re 5e4), textbook values; lift slope 2 pi (thin-aerofoil theory);
chord 0.1 m and C_L0 1 are illustrations, not a design.  Run: python3 -I L5_air.py   (writes L5_air.json)
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup as S
rho, mu, g = S.RHO, 1.81e-5, S.G0
rp, m, l = S.R_ROT, S.M_B, S.L_B
v = 8.0; Om = S.omega(v); ut0 = Om*rp
G = m*l/2*g; R = (m*l/2)*rp/(m*l*l/3); cstar = (R - 1)*(m*l*l/3)*Om
tilt, hub, alpha_sh = math.radians(5.0), 90.0, 0.2
ph = np.linspace(0, 2*math.pi, 4001)[:-1]
du_free = 2*np.mean(v*((hub + rp*np.sin(ph))/hub)**alpha_sh*np.sin(ph))
d_rod = 2*math.sqrt(m/l/7850/math.pi)
shapes = [('rod', 'bare steel rod', d_rod, 0.0, 1.2, 0.0), ('sym', 'streamlined, no lift', 0.1, 0.0, 0.01, 2*math.pi),
          ('wing', 'small wing', 0.1, 1.0, 0.01, 2*math.pi)]
out = dict(v=v, G_torque=G, cstar=cstar, du_free=du_free, dW_tilt=v*math.sin(tilt), d_rod=d_rod, runs={})
for akey, a in (('a3', 1/3), ('a0', 0.0)):
    ua0 = v*(1 - a); g0 = math.atan2(ua0, ut0); W0 = math.hypot(ut0, ua0)
    out['runs'][akey] = dict(a=a, W=W0, gam_deg=math.degrees(g0), q=0.5*rho*W0**2, du=du_free*(1 - a),
                             dgam_deg=math.degrees(du_free*(1 - a)*math.cos(g0)/W0), Re_rod=rho*W0*d_rod/mu, Re_wing=rho*W0*0.1/mu, cases={})
    for key, name, chord, CL0, CD, a0 in shapes:
        Sa = chord*l
        def Ft(Ut, Ua):
            W = math.hypot(Ut, Ua); gm = math.atan2(Ua, Ut); CL = CL0 + a0*(gm - g0)
            return 0.5*rho*W**2*Sa*(CL*Ua/W - CD*Ut/W)
        F0 = Ft(ut0, ua0); h = 1e-4
        dU_t = (Ft(ut0 + h, ua0) - Ft(ut0 - h, ua0))/(2*h); dU_a = (Ft(ut0, ua0 + h) - Ft(ut0, ua0 - h))/(2*h)
        ths = math.atan(F0/(m*Om**2*rp)); cs = math.cos(ths)
        A_shear = (l/2)*cs*dU_a*du_free*(1 - a)                # sin(phi) amplitude, + forwards
        A_tilt = (l/2)*cs*dU_t*(-v*math.sin(tilt))             # cos(phi) amplitude
        c_amp = -G*math.cos(ths) + A_tilt; s_amp = G*math.sin(ths) + A_shear
        Reff = R/cs
        ratio = (c_amp**2 + s_amp**2)/G**2*(R - 1)/(Reff - 1)
        ratio_push = (c_amp**2 + s_amp**2)/G**2
        c_air = -dU_t*l**2/3
        out['runs'][akey]['cases'][key] = dict(name=name, Ft=F0, lean_deg=math.degrees(ths), P_rotor=F0*ut0, A_shear=A_shear, A_tilt=A_tilt,
                                               ratio=ratio, ratio_push=ratio_push, c_air=c_air, F_over_G=F0*l/2/G)
        print(f"a={a:.2f} {name}: F_t {F0:+.1f} N ({F0*l/2/G:+.2f} of gravity's torque), lean {math.degrees(ths):+.1f} deg, rotor {F0*ut0:+.0f} W; "
              f"shear {A_shear:+.2f}, tilt {A_tilt:+.2f} N m; power x{ratio:.2f} (push alone x{ratio_push:.2f}); c_air {c_air:+.3f} N m s")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'L5_air.json'), 'w'), indent=1)
