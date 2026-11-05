"""Gate for modes.py: an upright cylinder, where the exact answer is known.
lam = k tanh(k h), k = xi_mn / R with J_m'(xi_mn) = 0; forcing ratio (m=1) Px = 2R/((xi^2-1) J1(xi)) * N."""
import numpy as np, sys
from scipy.special import jnp_zeros, jv
sys.path.insert(0, 'tools/fig12'); import modes
R, h = 0.040, 0.100
ok = True
for ns, nz in [(8, 20), (16, 40)]:
    print(f'mesh ns={ns}, nz={nz}')
    for m in (0, 1, 2):
        X, T, idx, out = modes.solve(lambda z: R + 0*z, 0.0, h, m, 3, ns, nz)
        xis = jnp_zeros(m, 3)  # zeros of J_m' (for m = 0 scipy already leaves out x = 0)
        for k, md in enumerate(out):
            ex = xis[k]/R*np.tanh(xis[k]*h/R); err = md['lam']/ex - 1
            line = f'  m={m} n={k+1}: lam FEM {md["lam"]:.6f}  exact {ex:.6f} 1/m  rel.err {err:+.2e}'
            if m == 1 and ns == 16:
                I = modes.integrals(X, T, idx, md, lambda z: R + 0*z, 0.0, h)
                xi = xis[k]; beta = 2*R/((xi**2-1)*jv(1, xi))
                # exact normalisation: f = c J1(k r) with int f^2 r dr = 1
                kk = xi/R; Nn = R**2/2*(1-1/xi**2)*jv(1, xi)**2; c = 1/np.sqrt(Nn)
                line += f' | Px/(c*N) {I["Px"]/(c*Nn):.6f} vs beta {beta:.6f} | E/lam {I["E"]/md["lam"]:.6f}'
            print(line)
            if ns == 16 and abs(err) > (1e-4 if k < 2 else 3e-4): ok = False
print('PASS' if ok else 'FAIL', 'cylinder eigenvalues on the fine mesh within 1e-4 (n = 1, 2) and 3e-4 (n = 3)')
