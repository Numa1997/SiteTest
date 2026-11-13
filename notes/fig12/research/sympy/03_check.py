"""SymPy/float check of Wolfram 03 (head as a soft solid). Run: python3 03_check.py > 03_check.out.txt"""
import sympy as sp
gam, R, Phi, Phic, ay, rho, a, h = sp.symbols('gamma R Phi Phi_c a_y rho_l a h', positive=True)
G0 = sp.Rational(14, 10)*gam/R*Phi*(Phi - Phic)
ty = ay*gam/R*(Phi - Phic)**2
phil = 1 - Phi
Bi = sp.simplify(ty/(rho*phil*a*h))
print('Bingham number tau_y/(rho_f a h) =', Bi)
print('lump size L* = tau_y/(rho_f a) =', sp.simplify(ty/(rho*phil*a)))
vals = {gam: 0.045, Phic: 0.64, rho: 1007, h: 0.019}
for Rv in (50e-6, 100e-6):
    for pl in (0.05, 0.1, 0.2, 0.3):
        s = dict(vals, R=Rv)
        s = {**vals, R: Rv, Phi: 1 - pl}
        print('R=%3.0f um phi_l=%.2f  G0=%6.1f Pa  tau_y(ay=.5,1)=%5.1f,%5.1f Pa  Bi(10 m/s2, ay=.5)=%.2f' % (
            Rv*1e6, pl, float(G0.subs(s)), float(ty.subs({**s, ay: 0.5})), float(ty.subs({**s, ay: 1})),
            float(Bi.subs({**s, ay: 0.5, a: 10}))))
mu = 2.06e-3
for V in (0.01, 0.1):
    Ca = mu*V/0.045
    print('V=%.2f m/s Ca=%.3e  f=6.82 gam Ca^(2/3)=%.3e N/m' % (V, Ca, 6.82*0.045*Ca**(2/3)))
