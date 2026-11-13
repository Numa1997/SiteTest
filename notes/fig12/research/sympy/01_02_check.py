"""SymPy check of Wolfram derivations 01 (Stokes layer, wall damping of mode (1,1)) and 02 (bubble slip).
Run: python3 01_02_check.py > 01_02_check.out.txt"""
import sympy as sp

y, t, U, d, w, mu, rho, nu = sp.symbols('y t U delta omega mu rho nu', positive=True)
# (a) Stokes layer dissipation, time-averaged, per unit area
u = U*sp.exp(-y/d)*sp.cos(w*t - y/d)
D = sp.simplify(mu*w/(2*sp.pi)*sp.integrate(sp.integrate(sp.diff(u, y)**2, (y, 0, sp.oo)), (t, 0, 2*sp.pi/w)))
print('Stokes dissipation per area:', D, '=', sp.simplify(D.subs({d: sp.sqrt(2*nu/w), mu: rho*nu})))

# (b) deep-water closed form for the side-wall decay of mode (1,1) in a cylinder. Done here with the theta and z
# integrals exact (SymPy) and the r integral by mpmath quadrature; compare with Wolfram 01 (full 3D NIntegrate, finite depth).
import mpmath as mp
x, r, th, z = sp.symbols('x r theta z', real=True)
j = sp.nsolve(sp.diff(sp.besselj(1, x), x), x, 1.84)
Rv = 0.0391; kk = float(j)/Rv; g = 9.81; nuv = 2.06e-3/1007; wv = (g*kk)**0.5
# energy: 2E/rho = Int |grad phi|^2 dV = k * Int_top phi^2 dA (deep water, no flux through the wall)
E2 = kk*mp.pi*mp.quad(lambda rr: mp.besselj(1, kk*rr)**2*rr, [0, Rv])
# side wall: Int_0^2pi Int_-inf^0 [(J1(kR)/R)^2 sin^2 + k^2 J1(kR)^2 cos^2] e^{2kz} R dz dtheta
th_int = sp.integrate(sp.sin(th)**2, (th, 0, 2*sp.pi)); z_int = sp.integrate(sp.exp(2*sp.Symbol('k', positive=True)*z), (z, -sp.oo, 0))
print('theta integral =', th_int, '; z integral =', z_int)
J = mp.besselj(1, kk*Rv)
side = mp.pi*Rv*J**2*(1/Rv**2 + kk**2)/(2*kk)
gam_num = 0.5*mp.sqrt(nuv*wv/2)*side/E2
gam_cf = 0.5*mp.sqrt(nuv*wv/2)/Rv*(1 + 1/float(j)**2)/(1 - 1/float(j)**2)
print("j11' =", j, " omega(deep) =", wv, " gamma side (quadrature) =", gam_num, " closed form =", gam_cf)
C = (1 + 1/float(j)**2)/(1 - 1/float(j)**2)/(2*mp.sqrt(2))/float(j)**0.25
print('coefficient C in zeta = C sqrt(nu/(R^1.5 g^0.5)), deep water:', C)

# (c) bubble slip: 0 = rho V (A - G) + 6 pi mu a (u - v)
a, A, G, v, uu = sp.symbols('a A G v u', real=True)
V = sp.Rational(4, 3)*sp.pi*a**3
vs = sp.solve(sp.Eq(0, rho*V*(A - G) + 6*sp.pi*mu*a*(uu - v)), v)[0]
print('slip v - u =', sp.simplify(vs - uu))
print('relaxation time =', sp.simplify((rho*V/2)/(6*sp.pi*mu*a)))
for av in (45e-6, 50e-6, 61e-6):
    print('a = %.0f um: U = %.3f mm/s' % (av*1e6, 2*av**2*1007*9.81/(9*2.06e-3)*1e3))
