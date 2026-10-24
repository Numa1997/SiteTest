"""L10: the drift of the stochastic element that keeps evenly spread air evenly spread (the well-mixed condition), in two dimensions
with a mean flow. Stationary Fokker-Planck equation for (x, z, u, w): the density p = Gaussian(u, w; sigma^2(x, z)) times a constant
air density must be stationary. With dX = (U + u') dt and du'_i = a_i dt - (C0 eps/2)(u'_i/sigma^2)... dt + sqrt(C0 eps) dW_i, the
fluctuation-dissipation pair balances by itself, and the drift a_i must satisfy
    d_t p = 0 = -div_x[(U + u') p] - div_u[a p] + (C0 eps/2) lap_u p + div_u[(C0 eps/2)(u'/sigma^2) p].
   python3 derive/L10_drift.py
"""
import sympy as sp
x, z, u, w = sp.symbols('x z u w', real=True)
s2 = sp.Function('s2', positive=True)(x, z)          # sigma^2(x, z)
psi = sp.Function('psi')(x, z)                       # mean flow U = (psi_z, -psi_x)
Ux, Uz = sp.diff(psi, z), -sp.diff(psi, x)
p = sp.exp(-(u**2 + w**2) / (2 * s2)) / (2 * sp.pi * s2)
def residual(ax, az):
    adv = -sp.diff((Ux + u) * p, x) - sp.diff((Uz + w) * p, z)
    drift = -sp.diff(ax * p, u) - sp.diff(az * p, w)
    return sp.simplify((adv + drift) / p)          # the damping and the noise cancel each other for this p (checked below)
proj = ((u + Ux) * sp.diff(s2, x) + (w + Uz) * sp.diff(s2, z)) / (2 * s2)
full = residual(sp.diff(s2, x) / 2 + u * proj, sp.diff(s2, z) / 2 + w * proj)
oned = residual(sp.diff(s2, x) / 2 * (1 + u**2 / s2), sp.diff(s2, z) / 2 * (1 + w**2 / s2))
C0e = sp.symbols('C0eps', positive=True)
ou = sp.simplify((C0e / 2 * (sp.diff(p, u, 2) + sp.diff(p, w, 2)) + sp.diff(C0e / 2 * u / s2 * p, u) + sp.diff(C0e / 2 * w / s2 * p, w)) / p)
print('damping and noise together:', ou)
print('full 2-D drift a_i = (1/2) d_i s2 + u_i ((u + U) . grad s2)/(2 s2): residual =', sp.simplify(full))
print('one-dimensional drift applied per component: residual =', sp.factor(sp.simplify(oned)))
