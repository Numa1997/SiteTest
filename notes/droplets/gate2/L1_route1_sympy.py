"""Gate 2, level L1 (chapter 2), route 1: SymPy. Equations (2.1)-(2.5). Own derivation, own operators."""
import sympy as sp
from dims import *
r, th, a, U, mu, rhoa, rhow, g, d = sp.symbols('r theta a U mu rho_a rho_w g d', positive=True)
A_, B_, C_, D_ = sp.symbols('A B C D')
f = sp.Function('f')

def E2(psi):   # Stokes operator on psi(r, theta)
    return sp.diff(psi, r, 2) + sp.sin(th) / r**2 * sp.diff(sp.diff(psi, th) / sp.sin(th), th)

print('== (2.1)  ansatz psi = sin^2(th) f(r)')
print('  E2[sin^2 f] / sin^2 - (f\'\' - 2f/r^2) =', sp.simplify(E2(sp.sin(th)**2 * f(r)) / sp.sin(th)**2 - (f(r).diff(r, 2) - 2 * f(r) / r**2)))
fgen = A_ * r**4 + B_ * r**2 + C_ * r + D_ / r
psi_gen = sp.sin(th)**2 * fgen
print('  general power solution: E4 psi =', sp.simplify(E2(E2(psi_gen))), '(zero for every A,B,C,D)')
# independent: solve the ODE (d2/dr2 - 2/r2)^2 f = 0 with dsolve (Euler-type, trying powers r^s)
s_ = sp.symbols('s')
op = lambda h: sp.diff(h, r, 2) - 2 * h / r**2
indicial = sp.simplify(op(op(r**s_)) / r**(s_ - 4))
print('  indicial polynomial of (d2 - 2/r2)^2 acting on r^s :', sp.factor(indicial), ' roots s = -1, 1, 2, 4  -> f = A r^4 + B r^2 + C r + D/r')
# boundary conditions
A_val, B_val = 0, U / 2
fb = fgen.subs({A_: A_val, B_: B_val})
sol = sp.solve([fb.subs(r, a), sp.diff(fb, r).subs(r, a)], [C_, D_], dict=True)[0]
print('  far field psi -> U r^2 sin^2/2 gives A=0, B=U/2; no slip f(a)=f\'(a)=0 gives', sol)
psi = sp.sin(th)**2 / 2 * U * (r**2 - sp.Rational(3, 2) * a * r + a**3 / (2 * r))   # printed (2.1)
print('  printed (2.1) minus derived:', sp.simplify(psi - sp.sin(th)**2 * fb.subs(sol)))
print('  E4 psi (printed) =', sp.simplify(E2(E2(psi))))
ur = sp.diff(psi, th) / (r**2 * sp.sin(th)); ut = -sp.diff(psi, r) / (r * sp.sin(th))
print('  u_r =', sp.simplify(ur), '\n  u_th =', sp.simplify(ut))
print('  no slip u_r(a), u_th(a) =', sp.simplify(ur.subs(r, a)), sp.simplify(ut.subs(r, a)))
print('  far field limit u_r/cos(th) , u_th/(-sin th) as r->oo :', sp.limit(ur / sp.cos(th), r, sp.oo), sp.limit(ut / (-sp.sin(th)), r, sp.oo))
print('  continuity (1/r2) d_r(r2 ur) + 1/(r sin) d_th(sin ut) =', sp.simplify(sp.diff(r**2 * ur, r) / r**2 + sp.diff(sp.sin(th) * ut, th) / (r * sp.sin(th))))
# momentum equation  grad p = mu lap u  in spherical components (axisymmetric, no swirl)
lap = lambda F: sp.diff(r**2 * sp.diff(F, r), r) / r**2 + sp.diff(sp.sin(th) * sp.diff(F, th), th) / (r**2 * sp.sin(th))
lap_r = lap(ur) - 2 * ur / r**2 - 2 / (r**2 * sp.sin(th)) * sp.diff(ut * sp.sin(th), th)
lap_t = lap(ut) + 2 / r**2 * sp.diff(ur, th) - ut / (r**2 * sp.sin(th)**2)
p = -sp.Rational(3, 2) * mu * U * a * sp.cos(th) / r**2          # printed p - p_inf
print('  momentum, r-component  dp/dr - mu lap_r =', sp.simplify(sp.diff(p, r) - mu * lap_r))
print('  momentum, theta-component (1/r) dp/dth - mu lap_th =', sp.simplify(sp.diff(p, th) / r - mu * lap_t))
# Cartesian cross-check of the same statement, exact rational points
x, y, z = sp.symbols('x y z', real=True)
R_ = sp.sqrt(x**2 + y**2 + z**2); rho_ = sp.sqrt(x**2 + y**2)
ct, st = z / R_, rho_ / R_
ux_sph = ur.subs({r: R_, th: sp.Symbol('T')}); 
urC = ur.subs(sp.sin(th), st).subs(sp.cos(th), ct)
URc = (U * ct * (1 - sp.Rational(3, 2) * a / R_ + a**3 / (2 * R_**3)))
UTc = -U * st * (1 - sp.Rational(3, 4) * a / R_ - a**3 / (4 * R_**3))
print('  u_r, u_th printed in closed form match derived:', sp.simplify(ur - U * sp.cos(th) * (1 - sp.Rational(3, 2) * a / r + a**3 / (2 * r**3))) == 0, sp.simplify(ut + U * sp.sin(th) * (1 - sp.Rational(3, 4) * a / r - a**3 / (4 * r**3))) == 0)
ux = URc * x / R_ + UTc * (ct * x / rho_); uy = URc * y / R_ + UTc * (ct * y / rho_); uz = URc * z / R_ - UTc * st
pC = -sp.Rational(3, 2) * mu * U * a * z / R_**3
lapC = lambda F: sum(sp.diff(F, v, 2) for v in (x, y, z))
pts = [{x: sp.Rational(3, 2), y: sp.Rational(1, 3), z: sp.Rational(-2, 1)}, {x: sp.Rational(-1, 2), y: sp.Rational(7, 5), z: sp.Rational(5, 3)}]
subsc = {a: 1, U: 1, mu: 1}
for P in pts:
    res = [sp.nsimplify(sp.simplify((sp.diff(pC, v) - mu * lapC(u)).subs(subsc).subs(P))) for v, u in ((x, ux), (y, uy), (z, uz))]
    div = sp.simplify((sp.diff(ux, x) + sp.diff(uy, y) + sp.diff(uz, z)).subs(subsc).subs(P))
    print('  Cartesian point', P, ': grad p - mu lap u =', res, ' div u =', div)
# surface quantities
sig_rr = -p + 2 * mu * sp.diff(ur, r)
tau = mu * (r * sp.diff(ut / r, r) + sp.diff(ur, th) / r)
print('  at r=a:  normal viscous stress 2 mu d_r u_r =', sp.simplify((2 * mu * sp.diff(ur, r)).subs(r, a)), ';  shear tau_r_th =', sp.simplify(tau.subs(r, a)), '  (printed -3/2 mu U sin/a)')
print('  p - p_inf at th = pi (upstream face) =', sp.simplify(p.subs({r: a, th: sp.pi})), ' > 0 : higher upstream, as printed')
Fp = sp.integrate(sp.simplify(-p.subs(r, a) * sp.cos(th) * a**2 * sp.sin(th)), (th, 0, sp.pi)) * 2 * sp.pi
Fs = sp.integrate(sp.simplify(-tau.subs(r, a) * sp.sin(th) * a**2 * sp.sin(th)), (th, 0, sp.pi)) * 2 * sp.pi
print('== (2.2)  F_z = integral (sig_rr cos - tau sin) dA :  pressure part =', sp.simplify(Fp), ' shear part =', sp.simplify(Fs), ' sum =', sp.simplify(Fp + Fs))
print('  p_inf contributes', sp.integrate(sp.cos(th) * sp.sin(th), (th, 0, sp.pi)), '(uniform pressure: zero net force)')
same('F = 6 pi mu a U', mass * 0 * ONE if False else (visc * m * speed), force)
print('  Dimensional analysis: variables (F, mu, a, U) in (M,L,T): nullspace of exponent matrix =')
Mx = sp.Matrix([[1, 1, 0, 0], [1, -1, 1, 1], [-2, -1, 0, -1]])   # columns F, mu, a, U ; rows M, L, T
print('   ', Mx.nullspace(), ' -> one group F/(mu a U): the factor 6 pi needs the solution')

print('\n== (2.3) terminal speed: weight less buoyancy = Stokes drag')
v = sp.symbols('v', positive=True)
vS = sp.solve(sp.Eq(6 * sp.pi * mu * a * v, sp.Rational(4, 3) * sp.pi * a**3 * (rhow - rhoa) * g), v)[0]
print('  v =', vS, ' ; printed difference =', sp.simplify(vS - 2 * (rhow - rhoa) * g / (9 * mu) * a**2))
same('v = k a^2', (dens * accel / visc) * m**2, speed)
print('  limit rho_a -> 0 :', sp.limit(vS, rhoa, 0), ' ; sign: positive for rho_w > rho_a, zero at rho_w = rho_a (neutral drop does not sink)')
rho_a_cloud, mu_cloud = sp.Rational(1045790, 1000000), sp.Float('1.7710678993609708e-05')
aRe1 = sp.solve(sp.Eq(4 * rhoa * (rhow - rhoa) * g * a**3 / (9 * mu**2), 1), a)
av = [sp.N(sol.subs({rhoa: 1.0457907797732868, rhow: 1000, g: 9.81, mu: 1.7710678993609708e-05})) for sol in aRe1 if sp.im(sp.N(sol.subs({rhoa: 1, rhow: 1000, g: 9.81, mu: 1.8e-5}))) == 0]
print('  Re_Stokes = 2 a rho_a v/mu = 4 rho_a drho g a^3/(9 mu^2): check by substitution:', sp.simplify(2 * a * rhoa * vS / mu - 4 * rhoa * (rhow - rhoa) * g * a**3 / (9 * mu**2)))
print('  Re = 1 at a =', av, 'm  (text: 41.0 um) in cloud air (10 C, 850 hPa)')

print('\n== (2.4)/(2.5) drag balance and Davies number')
vv, CD, Re = sp.symbols('v C_D Re', positive=True)
eq24 = sp.Eq(sp.Rational(4, 3) * sp.pi * a**3 * (rhow - rhoa) * g, sp.Rational(1, 2) * rhoa * vv**2 * sp.pi * a**2 * CD)
print('  (2.4) with C_D = F/(rho_a v^2 pi a^2 /2): C_D definition inserted -> F =', sp.simplify(sp.Rational(1, 2) * rhoa * vv**2 * sp.pi * a**2 * CD))
CD_sol = sp.solve(eq24, CD)[0]
ReDef = rhoa * vv * (2 * a) / mu
NDa = sp.simplify(CD_sol * ReDef**2)
print('  N_Da = C_D Re^2 =', NDa, ' (v cancelled:', not NDa.has(vv), ')')
print('  printed 4 rho_a drho g d^3/(3 mu^2) with d = 2a minus derived =', sp.simplify(NDa - 4 * rhoa * (rhow - rhoa) * g * (2 * a)**3 / (3 * mu**2)))
same('N_Da', dens * dens * accel * m**3 / visc**2, ONE)
same('C_D = F/(rho v^2 pi a^2/2)', force / (dens * speed**2 * m**2), ONE)
same('Re = rho v d/mu', dens * speed * m / visc, ONE)
print('  Buckingham: variables (F, a, v, rho_a, mu): 5 quantities, rank of dimension matrix and null space')
Mb = sp.Matrix([[1, 0, 0, 1, 1], [1, 1, 1, -3, -1], [-2, 0, -1, 0, -1]])   # M, L, T rows
print('    rank =', Mb.rank(), ' -> groups =', 5 - Mb.rank(), ' ; null space vectors:', [list(nv) for nv in Mb.nullspace()])
print('  Stokes drag C_D = 24/Re : N_Da =', sp.simplify((24 / Re) * Re**2), '= 24 Re ; v from Re = N_Da/24 :',
      sp.simplify(mu * (NDa / 24) / (rhoa * (2 * a)) - vS), '(difference with (2.3), 0 = identical)')
print('  limit check Stokes drag in (2.4):', sp.simplify((sp.Rational(1, 2) * rhoa * vv**2 * sp.pi * a**2 * 24 / ReDef) - 6 * sp.pi * mu * a * vv), '(=0: reduces to 6 pi mu a v)')
