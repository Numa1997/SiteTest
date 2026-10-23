"""Gate 2, L2: start-distance convergence of E_S(40 um, 8 um) with the independent integrator, at two integration tolerances."""
import sys
src = open('L2_route2_numeric.py').read().split("print('== (3.5)(a)")[0]
St, S, p = 3.5974290473262687, 0.04496363069298862, 0.2
for label, (rt, at) in {'rtol 1e-10': (1e-10, 1e-12), 'rtol 1e-13': (1e-13, 1e-15)}.items():
    g = {}
    exec(src.replace('rtol=1e-10, atol=1e-12', 'rtol=%g, atol=%g' % (rt, at)), g)
    for Z in ([50, 100, 200, 400, 800] if rt == 1e-10 else [100, 200, 400]):
        Epsi, Eb, bc = g['E_of']('creeping', St, S, p, Z)
        print('own integrator (%s), creeping Z = %4d : E_flux = %.6f  b_c = %.6f' % (label, Z, Epsi, bc), flush=True)
