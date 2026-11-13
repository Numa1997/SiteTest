"""Independent check of Wolfram 05 with scipy-free Python: equilibrium liquid-fraction profile of the head (Princen column,
Pi = K (gam/R)(ec-e)^2/sqrt(e), dPi/dz = rho g (1-e)) by SymPy derivative + trapezoid integration; yield stress and modulus."""
import sympy as sp
e, K, ec = sp.symbols('e K e_c', positive=True)
gam, rho, g, R = 0.045, 1007, 9.81, 34e-6
Pi = K*gam/R*(ec - e)**2/sp.sqrt(e)
dz_de = sp.lambdify((e, K, ec), -sp.diff(Pi, e)/(rho*g*(1 - e)))
def height(e0, Kv, ecv, n=20000):
    h = (ecv - 1e-9 - e0)/n; s = 0.0
    for i in range(n + 1):
        x = e0 + i*h; w = 0.5 if i in (0, n) else 1.0; s += w*dz_de(x, Kv, ecv)
    return s*h
for Kv, ecv in ((3.2, 0.36), (7.3, 0.26)):
    lo, hi = 0.02, ecv - 1e-6
    for _ in range(60):
        mid = 0.5*(lo + hi)
        if height(mid, Kv, ecv, 4000) > 0.019: lo = mid
        else: hi = mid
    print('K=%.1f ec=%.2f: liquid fraction at the top of a 19 mm head = %.4f' % (Kv, ecv, mid))
for ev in (0.22, 0.27, 0.34):
    Phi = 1 - ev
    print('e=%.2f: G0(1.4)=%.1f Pa, tau_y=%.2f Pa' % (ev, 1.4*gam/R*Phi*(Phi - 0.64), 0.51*gam/R*(Phi - 0.62)**2))
