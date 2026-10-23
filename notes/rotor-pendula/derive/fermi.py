"""Fermi estimates of observable 1 (mean mechanical power at the generator) for each energy source, before any model.

Run: python3 -I fermi.py.  PROVISIONAL values (to be replaced from the scouts' dossiers) are marked (prov).
"""
import math
g, m, L = 9.81, 0.1, 0.2
# --- E0: gravity at uniform rotation, linear optimum (L0):  P* = m L g^2 / (4 Omega (r_p - L)) -------------------------
# representative large-rotor mounting: NREL-5MW-like rotor at 8 m/s (prov: radius 63 m, lambda* 7.55)
Rrot, lam, v = 63.0, 7.55, 8.0                      # (prov)
Om = lam*v/Rrot
rp = 0.3*Rrot; R = rp/L
Pg = m*L*g**2/(4*Om*(rp - L))
print(f"E0 gravity: Omega = {Om:.3f} rad/s ({Om*60/2/math.pi:.2f} rpm), r_p = {rp:.1f} m, R = {R:.0f}: P* = {Pg*1e3:.1f} mW;"
      f" bound m g L Omega = {m*g*L*Om*1e3:.0f} mW")
# --- E1: rotor-speed wandering --------------------------------------------------------------------------------------
# rotor time constant tau = J Omega^2 / (3 P) for a region-2 rotor (k Omega^2 torque law, at the C_p peak)
J, P_aero = 4.0e7, 1.9e6                            # (prov) rotor+generator inertia kg m^2, aerodynamic power W at 8 m/s
tau = J*Om**2/(3*P_aero)
s = 0.15                                            # (prov) sigma_Omega / Omega over 10 min
# dynamic Euler part: quasi-static response theta ~ -eps, eps = Omegadot/Omega^2; power c <thetadot^2>, thetadot ~ deps/dt
eps_rms = s*Om/tau/Om**2
depsdt = s*Om/tau**2/Om**2
c = m*L**2*Om*(R - 1)
P_dyn = c*depsdt**2
print(f"E1 rotor speed: tau_rotor = {tau:.1f} s; eps_rms ~ {eps_rms:.3f} (vs G = {g/(Om**2*L):.0f}, R = {R:.0f});"
      f" dynamic Euler power ~ {P_dyn*1e6:.1f} uW = {P_dyn/Pg:.1e} of E0")
print(f"   quasi-static (Jensen) part at fixed c: P(Omega)/P(Omega0) = 2/(1+(Omega/Omega0)^2), mean shift ~ +s^2/2 = {s**2/2*100:.1f} %")
# --- E2: blade edgewise vibration at the pivot, acceleration amplitude A, resonant with the pendulum ----------------
# at the gravity-optimal damping c* the resonant harmonic power is P_e = m A^2 / (2 Omega (R-1)) = 2 (A/g)^2 P*
for A in (0.1, 0.3, 1.0, 3.0):
    Pe = m*A**2/(2*Om*(R - 1))
    print(f"E2 edgewise, A = {A:4.1f} m/s^2 at the pivot: P_e = {Pe*1e3:.4f} mW = {Pe/Pg*100:.3f} % of E0")
# white-noise bound (power theorem): P <= (S/2) m for two-sided intensity S of the pivot acceleration
# --- E3: turbulence on an exposed bob: drag 0.05-0.49 weights at 17-50 m/s, costing 0.9-24 W of rotor power (scales.py)
print("E3 exposed bob: drag 0.054-0.482 N, rotor pays 0.90-24.3 W (scales.py) -> bob inside the blade shell, E3 = 0")
# --- observable 3, blade vibration: an optimally tuned absorber of mass ratio mu adds damping ~ sqrt(mu/8) (Den Hartog)
m_modal = 1000.0                                    # (prov) edgewise modal mass, tip-normalised, kg
for frac, phi in ((0.3, 0.08), (0.9, 0.8)):         # (prov) edgewise mode shape at 30 % and 90 % span
    mu = m*phi**2/m_modal
    print(f"obs 3 at {int(frac*100)} % span: mu = {mu:.1e}, best-tuned absorber damping ~ {math.sqrt(mu/8)*100:.3f} % "
          f"(blade structural 0.477 %); at the gravity-optimal damping the bob is nearly locked: far less")
