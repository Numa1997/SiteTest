"""Scales and dimensionless groups of the 18 mountings.

Run: python3 -I scales.py
Mounting: tip-speed ratio 7 at wind 8 m/s fixes the rotor radius R_rot = 56 m/s / Omega; the pivot sits at 30, 60, 90 %
of the blade; pendulum M = 0.1 kg on L = 0.2 m. Everything printed here is computed, nothing is typed in.
"""
import math
g, M, L, lam, v = 9.81, 0.1, 0.2, 7.0, 8.0
rpms = [400, 200, 100, 20, 14, 8]
rows = []
print(f"{'rpm':>4} {'R_rot':>7} {'frac':>4} {'r_p':>7} {'R':>7} {'G':>8} {'Gamma':>7} {'1/Gam':>6} {'f_pend':>6} {'f_1P':>6} "
      f"{'ratio':>6} {'P*_mW':>7} {'MgLOm_mW':>8} {'v_piv':>6}")
for rpm in rpms:
    Om = rpm*2*math.pi/60
    Rrot = lam*v/Om
    for frac in (0.3, 0.6, 0.9):
        rp = frac*Rrot
        R = rp/L; G = g/(Om**2*L); Gam = rp*Om**2/g
        f_p = Om*math.sqrt(R)/(2*math.pi); f1 = Om/(2*math.pi)
        Pstar = M*L*g**2/(4*Om*abs(rp - L))
        Pub = M*g*L*Om
        rows.append((rpm, Rrot, frac, rp, R, G, Gam, f_p, f1, Pstar, Pub, rp*Om))
        print(f"{rpm:4d} {Rrot:7.3f} {frac:4.1f} {rp:7.3f} {R:7.2f} {G:8.3f} {Gam:7.2f} {1/Gam:6.3f} {f_p:6.2f} {f1:6.3f} "
              f"{f_p/f1:6.2f} {Pstar*1e3:7.2f} {Pub*1e3:8.1f} {rp*Om:6.1f}")
large = [r for r in rows if r[0] <= 20]
print()
print(f"R over all 18: {min(r[4] for r in rows):.2f} .. {max(r[4] for r in rows):.1f}")
print(f"pendulum frequency, all: {min(r[7] for r in rows):.2f} .. {max(r[7] for r in rows):.2f} Hz; large rotors: "
      f"{min(r[7] for r in large):.2f} .. {max(r[7] for r in large):.2f} Hz")
print(f"once-per-turn push: {min(r[8] for r in rows):.3f} .. {max(r[8] for r in rows):.3f} Hz")
print(f"own frequency / push: {min(r[7]/r[8] for r in rows):.2f} .. {max(r[7]/r[8] for r in rows):.2f}")
print(f"Gamma: {min(r[6] for r in rows):.2f} .. {max(r[6] for r in rows):.1f}")
print(f"P* (linear optimum): {min(r[9] for r in rows)*1e3:.2f} .. {max(r[9] for r in rows)*1e3:.2f} mW")
print(f"upper bound M g L Omega on the large rotors: {min(r[10] for r in large)*1e3:.0f} .. {max(r[10] for r in large)*1e3:.0f} mW")
print(f"pivot speed through the air r_p Omega, large rotors: {min(r[11] for r in large):.1f} .. {max(r[11] for r in large):.1f} m/s")
# exposed bob: steel sphere of 0.1 kg, drag coefficient 0.47 (subcritical sphere), air 1.225 kg/m3
rho_s, Cd, rho_a = 7850.0, 0.47, 1.225
rb = (3*M/(4*math.pi*rho_s))**(1/3); A = math.pi*rb**2
for r in large:
    pass
vmax = max(r[11] for r in large); vmin = min(r[11] for r in large)
for vv in (vmin, vmax):
    D = 0.5*rho_a*Cd*A*vv**2
    Re = rho_a*vv*2*rb/1.8e-5
    print(f"exposed steel bob (radius {rb*1e3:.1f} mm) at {vv:.1f} m/s: drag {D:.3f} N = {D/(M*g):.2f} weights, "
          f"drag power {D*vv:.2f} W, Re = {Re:.2e}")
