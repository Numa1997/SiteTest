"""Gate 2, level L6 (chapter 7), route 2 (numerical, NumPy/SciPy): own implementation of the weak-inertia relative speed from the paper's equations
(81, 26, Table 2, corrigendum), compared with physics.cjs ayalaFactor; the corrigendum's claim that the closed form is within 2.5 % of the exact
form; the epsilon -> 0 limit; the share of each term; the Stokes numbers."""
import json, numpy as np
from scipy.integrate import quad
from scipy.special import erf
D = json.load(open('L6_model_dump.json')); nu = D['nu']; g = 9.81
Rl = 2e4; a0 = (11 + 7 * Rl) / (205 + Rl)

def parts(a1, a2, eps, v):   # returns (shear, acceleration, coupling, gravity-part) contributions to sigma^2 and d g
    v1, v2 = v(a1), v(a2); t1, t2 = v1 / g, v2 / g; R = a1 + a2
    tk = np.sqrt(nu / eps); vk = (nu * eps) ** 0.25
    d = t1 - t2
    shear = R**2 * eps / (15 * nu); acc = d**2 * a0 * (vk / tk)**2; coup = (v1 * t1 - v2 * t2)**2 * 2 * eps / (15 * nu)
    return shear, acc, coup, d, t1, t2, tk
def ratio(a1, a2, eps, v):
    sh, ac, co, d, t1, t2, tk = parts(a1, a2, eps, v)
    wr = np.sqrt(2 / np.pi) * np.sqrt(sh + ac + co + np.pi / 8 * d**2 * g**2)
    return wr / (0.5 * abs(d) * g)
vtab = {int(k): v for k, v in D['v'].items()}
import subprocess
def vB(a):   # Beard fall speed of the model (input), radius in m
    return float(subprocess.run(['node', '-e', "const P=require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');const A=P.air(283.15,85000);console.log(P.vBeard(%r,A))" % a], capture_output=True, text=True).stdout)
cache = {}
def v(a):
    if a not in cache: cache[a] = vB(a)
    return cache[a]

print('== own implementation against physics.cjs ayalaFactor (model), 40 um on 8 um')
for r in D['factor']:
    mine = ratio(40e-6, 8e-6, r['eps'], v)
    print('   eps = %.0e m2/s3 : own %.9f ; model %.9f ; (own-1)/eps = %.4g' % (r['eps'], mine, r['f'], (mine - 1) / r['eps']))
print('   text: +0.4 %%, +5.6 %%, +28 %% at 10, 100, 400 cm2/s3:  own %+.2f %%, %+.2f %%, %+.2f %%' % tuple(100 * (ratio(40e-6, 8e-6, e, v) - 1) for e in (1e-3, 1e-2, 4e-2)))
print('   other pairs (own vs model):')
for r in D['pairs']:
    print('      %2d on %2d um, eps = %.0e : own %.6f  model %.6f' % (r['a1'], r['a2'], r['eps'], ratio(r['a1'] * 1e-6, r['a2'] * 1e-6, r['eps'], v), r['f']))
print('== limit eps -> 0 (gravity alone): ratio - 1 divided by eps tends to the constant 4 (R^2 + 2 A^2)/(15 pi nu d^2 g^2)')
a1, a2 = 40e-6, 8e-6; sh, ac, co, d, t1, t2, tk = parts(a1, a2, 1.0, v)
A2 = (v(a1) * t1 - v(a2) * t2)**2
lim = 4 * ((a1 + a2)**2 + 2 * A2) / (15 * np.pi * nu * d**2 * g**2)
for e in (1e-12, 1e-9, 1e-6):
    print('   eps = %.0e : (ratio-1)/eps = %.6g ; predicted limit %.6g' % (e, (ratio(a1, a2, e, v) - 1) / e, lim))
print('== share of each term at eps = 10, 100, 400 cm2/s3 (40 um on 8 um): increase of the kernel caused by shear / acceleration / coupling, alone')
for e in (1e-3, 1e-2, 4e-2):
    sh, ac, co, d, t1, t2, tk = parts(a1, a2, e, v); base = np.pi / 8 * d**2 * g**2
    f = lambda extra: np.sqrt(1 + extra / base) - 1
    print('   eps = %.0e : shear alone %+.2f %% ; acceleration alone %+.2f %% ; coupling alone %+.2f %% ; all together %+.2f %%' % (e, 100 * f(sh), 100 * f(ac), 100 * f(co), 100 * (ratio(a1, a2, e, v) - 1)))
print('== corrigendum: closed form |w_r| = sqrt(2/pi) sqrt(sigma^2 + pi/8 (dv)^2) against the exact direction average of E|dv cos(th) + sigma xi|')
def exact(sig, dv):
    # radial component along direction mu = cos(th): mean dv*mu (gravity), standard deviation sigma ; average over mu uniform on [-1,1]
    def inner(mu):
        m = dv * mu; c = m / (sig * np.sqrt(2))
        return sig * np.sqrt(2 / np.pi) * (np.exp(-c * c) + np.sqrt(np.pi) * c * erf(c))
    return 0.5 * quad(inner, -1, 1, epsabs=0, epsrel=1e-12)[0]
worst = 0; at = None
for b in np.logspace(-2, 2, 400):
    sig = 1.0; dv = b * sig * np.sqrt(2)
    apx = np.sqrt(2 / np.pi) * np.sqrt(sig**2 + np.pi / 8 * dv**2); ex = exact(sig, dv)
    if abs(apx / ex - 1) > worst: worst, at = abs(apx / ex - 1), b
print('   max relative difference of the closed form from the exact average over b in [0.01, 100]: %.2f %% at b = %.2f (corrigendum: about 2.5 %%); closed form is the larger' % (100 * worst, at))
print('== Stokes numbers (tau_p = v_Beard/g, tau_K = sqrt(nu/eps), nu = %.4e m2/s)' % nu)
for e, lab in ((1e-3, '10'), (1e-2, '100'), (4e-2, '400')):
    tk = np.sqrt(nu / e)
    print('   eps = %s cm2/s3 : tau_K = %.2f ms ; St(8 um) = %.4f ; St(40 um) = %.3f ; St(43 um) = %.3f ; St(50 um) = %.3f' % (lab, tk * 1e3, v(8e-6) / g / tk, v(40e-6) / g / tk, v(43e-6) / g / tk, v(50e-6) / g / tk))
print('   tau_p(8 um) = %.3f ms (text 0.8), tau_p(40 um) = %.2f ms (text 18)' % (v(8e-6) / g * 1e3, v(40e-6) / g * 1e3))
print('   radius where St passes 1 at eps = 400 cm2/s3: %.2f um (text 43)' % D['cut']['a1'])
