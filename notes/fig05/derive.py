"""Fig. 5 note: check every derivation step and every number of the note (water-wave.html, Sections 02-10).
Run: python3 notes/fig05/derive.py"""
import sympy as sp, math

x, z, t, a, k, w, g, x0, z0, dk, dw = sp.symbols('x z t a k omega g x0 z0 delta_k delta_omega', real=True)
th = k*x - w*t
phi = a*w/k*sp.exp(k*z)*sp.sin(th)                                  # (12)
print('Laplace (4) on (12):', sp.simplify(sp.diff(phi, x, 2) + sp.diff(phi, z, 2)))
eta = a*sp.cos(th)                                                    # (10)
print('kinematic (6):', sp.simplify(sp.diff(eta, t) - sp.diff(phi, z).subs(z, 0)))
print('dynamic (8) / (a cos):', sp.simplify((sp.diff(phi, t).subs(z, 0) + g*eta)/(a*sp.cos(th))))
u, ww = sp.diff(phi, x), sp.diff(phi, z)
print('(16) u:', sp.simplify(u - a*w*sp.exp(k*z)*sp.cos(th)), ' w:', sp.simplify(ww - a*w*sp.exp(k*z)*sp.sin(th)))
X = x0 - a*sp.exp(k*z0)*sp.sin(k*x0 - w*t); Z = z0 + a*sp.exp(k*z0)*sp.cos(k*x0 - w*t)   # (17)
print('(17) dX/dt - u(x0,z0):', sp.simplify(sp.diff(X, t) - u.subs({x: x0, z: z0})), ' dZ/dt - w:', sp.simplify(sp.diff(Z, t) - ww.subs({x: x0, z: z0})))
print('(18) circle:', sp.simplify((X-x0)**2 + (Z-z0)**2 - a**2*sp.exp(2*k*z0)))
# (20)-(21) Stokes drift: first-order Taylor term averaged over a period
r = a*sp.exp(k*z0); TH = sp.symbols('theta')
xi, ze = -r*sp.sin(TH), r*sp.cos(TH)
ux = sp.diff(u, x).subs({x: x0, z: z0}).subs(k*x0 - w*t, TH); uz = sp.diff(u, z).subs({x: x0, z: z0}).subs(k*x0 - w*t, TH)
print('(20)-(21) xi u_x + zeta u_z =', sp.simplify(xi*ux + ze*uz))
# (15) group velocity, and the two-wave group used for it
om = sp.sqrt(g*k)
print('(15) d omega/dk / (c/2):', sp.simplify(sp.diff(om, k)/(om/k/2)))
A_, B_ = k*x - w*t, dk*x - dw*t
two = a*sp.cos((k+dk)*x - (w+dw)*t) + a*sp.cos((k-dk)*x - (w-dw)*t)
print('two-wave group - 2a cos(dk x - dw t) cos(kx - wt):', sp.simplify(sp.expand_trig(two - 2*a*sp.cos(B_)*sp.cos(A_))))
# 6.2 trochoid: crest fraction and mean surface height
T_ = sp.symbols('T_', real=True)
xs = (TH)/k - a*sp.sin(TH)   # x along the surface at t = 0, theta = k x0
frac = sp.simplify((xs.subs(TH, sp.pi/2) - xs.subs(TH, -sp.pi/2))/(2*sp.pi/k))
mean = sp.simplify(sp.integrate(a*sp.cos(TH)*sp.diff(xs, TH), (TH, 0, 2*sp.pi))/(2*sp.pi/k))
print('crest fraction:', frac, '  mean surface height:', mean, '  dx/dx0:', sp.simplify(sp.diff(xs, TH)*k))

G = 9.81; lam = 2.6; km = 2*math.pi/lam; A = 0.24
wd = math.sqrt(G*km)
print('\n--- numbers at the defaults (lambda = 260 px = 2.6 m, A = 24 px) ---')
print('k_m = %.4f rad/m, a = %.2f m, ak = %.4f' % (km, A, A*km))
print('omega = %.4f rad/s, f = %.4f Hz, c = %.4f m/s, T = %.4f s, a*omega = %.4f m/s, cg = %.4f' % (wd, wd/2/math.pi, wd/km, 2*math.pi/wd, A*wd, wd/km/2))
for L in [1.2, 2.6, 4.0, 10, 100, 400]:
    kk = 2*math.pi/L; c = math.sqrt(G/kk); print('table lambda=%g: T=%.3f c=%.3f cg=%.3f k=%.3f' % (L, 2*math.pi/math.sqrt(G*kk), c, c/2, kk))
for T in [16, 8]:
    cg = G*T/(4*math.pi); print('storm T=%d s: lambda=%.1f m, cg=%.3f m/s, 2000 km in %.1f h' % (T, G*T*T/2/math.pi, cg, 2e6/cg/3600))
q = math.exp(-km*0.56); print('layer ratio %.4f; radii px:' % q, [round(24*q**j, 3) for j in range(5)], ' %%:', [round(100*q**j, 3) for j in range(5)])
print('e^-pi = %.4f, e^-2pi = %.5f (1 in %.0f), e^(pi/3) = %.3f' % (math.exp(-math.pi), math.exp(-2*math.pi), math.exp(2*math.pi), math.exp(math.pi/3)))
print('diver: 100 m swell at 5 m: %.3f' % math.exp(-2*math.pi*5/100))
print('Ex 6.1: 400 px -> %.4f, 120 px -> %.2e' % (math.exp(-2*math.pi/4.0*2.24), math.exp(-2*math.pi/1.2*2.24)))
print('6.2: crest fraction %.4f, mean drop %.2f px; cap 0.9/k = %.2f px; A=50 -> ak = %.3f' % (0.5 - 0.58/math.pi, 0.5*24**2*2*math.pi/260, 0.9*260/2/math.pi, 50*2*math.pi/260))
print('Michell H/lambda = 0.142 -> ak = %.3f' % (math.pi*0.142))
c0 = wd/km; a2 = 0.2/km
print('Stokes ak=0.2: a = %.4f m, U_S = %.4f m/s, U_S T = %.4f m; at z0=-0.56: %.3f mm/s; default U_S = %.4f m/s (c/U = %.2f)' % (a2, c0*0.04, 0.04*lam, 1e3*c0*0.04*math.exp(-2*km*0.56), wd*km*A*A, c0/(wd*km*A*A)))
print('tanh(pi) = %.5f, speed ratio %.5f' % (math.tanh(math.pi), math.sqrt(math.tanh(math.pi))))
sig, rho = 0.0728, 1000.0
print('capillary: lambda_m = %.4f cm, c_min = %.4f m/s' % (100*2*math.pi*math.sqrt(sig/rho/G), (4*G*sig/rho)**0.25))
print('viscous e-folding time: %.2f h' % (1/(2*1e-6*km*km)/3600))
