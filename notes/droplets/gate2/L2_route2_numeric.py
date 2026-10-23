"""Gate 2, level L2 (chapter 3), route 2 (numerical, SciPy): own trajectory integrator, written from (3.2) and the two model flows only.
Does not use physics.cjs trajectory code. The fall speeds U, v(r) of the one realistic case come from physics.cjs vBeard (an input, not under test here)."""
import numpy as np, subprocess, json
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

def air_vel(flow, x, z):
    q = np.hypot(x, z); c, s = z / q, x / q
    if flow == 'creeping': ur = c * (1 - 1.5 / q + 0.5 / q**3); ut = -s * (1 - 0.75 / q - 0.25 / q**3)
    else:                  ur = c * (1 - 1 / q**3);            ut = -s * (1 + 0.5 / q**3)
    return ur * s + ut * c, ur * c - ut * s
def psi(flow, x, z):
    q = np.hypot(x, z); g = (1 - 1.5 / q + 0.5 / q**3) if flow == 'creeping' else (1 - 1 / q**3)
    return 0.5 * x * x * g

def hits(flow, St, S, p, b, Z, free=False):
    rc = 1 + p
    if St == 0:                       # inertialess: follow the air minus settling
        f = lambda s_, y: [air_vel(flow, y[0], y[1])[0], air_vel(flow, y[0], y[1])[1] - S]
        y0 = [b, -Z]
    else:
        def f(s_, y):
            ax, az = air_vel(flow, y[0], y[1])
            return [y[2], y[3], (ax - y[2]) / St, (az - y[3] - S) / St]
        ax, az = air_vel(flow, b, -Z); y0 = [b, -Z, (0.0 if free else ax), (1.0 if free else az) - S]
    contact = lambda s_, y: np.hypot(y[0], y[1]) - rc; contact.terminal = True; contact.direction = -1
    gone = lambda s_, y: y[1] - (rc + 2.0); gone.terminal = True
    smax = 20 * Z + 200
    sol = solve_ivp(f, [0, smax], y0, method='DOP853', rtol=1e-13, atol=1e-15, events=[contact, gone])
    return len(sol.t_events[0]) > 0

def critical_b(flow, St, S, p, Z):
    rc = 1 + p
    if not hits(flow, St, S, p, 1e-6, Z): return 0.0
    hi = 1.5 * rc
    while hits(flow, St, S, p, hi, Z): hi *= 1.5
    lo = 0.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if hits(flow, St, S, p, mid, Z): lo = mid
        else: hi = mid
        if hi - lo < 1e-9 * rc: break
    return 0.5 * (lo + hi)

def E_of(flow, St, S, p, Z):
    bc = critical_b(flow, St, S, p, Z); rc = 1 + p
    Epsi = 2 * (psi(flow, bc, -Z) - 0.5 * S * bc**2) / ((1 - S) * rc**2)
    return Epsi, bc**2 / rc**2, bc

print('== (3.5)(a) zero-inertia limit, S = 0: grazing streamline gives E = psi-based closed form')
for flow, fE in [('creeping', lambda q: 1 - 1.5 / q + 0.5 / q**3), ('potential', lambda q: 1 - 1 / q**3)]:
    for p in [0.05, 0.2, 1.0]:
        Z = 60 if flow == 'creeping' else 15
        Epsi, Eb, bc = E_of(flow, 0, 0.0, p, Z)
        print('   %-9s p = %.2f : E (trajectories, flux form) = %.6f ; b_c^2/(1+p)^2 at start Z=%d : %.6f ; closed form %.6f' % (flow, p, Epsi, Z, Eb, fE(1 + p)))
print('== (3.5)(b) large Stokes number: straight paths, E -> 1 (partners start with the free-stream velocity, Z = 30)')
for flow in ['creeping', 'potential']:
    for St_big in [1e2, 1e4]:
        rc = 1.2; lo, hi = 0.0, 1.5 * rc
        for _ in range(45):
            mid = 0.5 * (lo + hi)
            if hits(flow, St_big, 0.0, 0.2, mid, 30, free=True): lo = mid
            else: hi = mid
        bc = 0.5 * (lo + hi); print('   %-9s St = %g, p = 0.2 : b_c = %.5f (1+p = 1.2), E = b_c^2/(1+p)^2 = %.5f' % (flow, St_big, bc, bc**2 / rc**2))

# physics.cjs inputs for the realistic pair (40 um collector, 8 um partner), cloud air 10 C 850 hPa
out = subprocess.run(['node', '-e', "const P=require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');const A=P.air(283.15,85000);console.log(JSON.stringify({U:P.vBeard(40e-6,A),vr:P.vBeard(8e-6,A),rho:A.rho,mu:A.mu,nu:A.nu}))"], capture_output=True, text=True).stdout
A = json.loads(out); g, rho_w = 9.81, 1000.0
R, r = 40e-6, 8e-6; U, vr = A['U'], A['vr']
gstar = g * (1 - A['rho'] / rho_w); tau = vr / gstar
St = tau * U / R; S = vr / U; p = r / R; Re = 2 * R * A['rho'] * U / A['mu']
print('== realistic pair 8 um on 40 um (cloud air): U = %.5f m/s, v(r) = %.6f m/s, tau = %.4e s, St = %.4f (text 3.60), S = %.4f (text 0.045), p = %.2f, Re = %.3f (text 0.84)' % (U, vr, tau, St, S, p, Re))
print('   2R/Re = %.2f collector radii (text 2.4)' % (2 / Re))

print('== (3.5)(c) start distance: E(flux form), b_c^2/(1+p)^2, for creeping flow')
for Z in [50, 200, 400]:
    Epsi, Eb, bc = E_of('creeping', St, S, p, Z)
    print('   Z = %3d : E_flux = %.6f   b_c^2/(1+p)^2 = %.6f   b_c = %.5f' % (Z, Epsi, Eb, bc))
ES = E_of('creeping', St, S, p, 200)[0]; EP = E_of('potential', St, S, p, 30)[0]
print('   E_S = %.5f (creeping, Z=200), E_P = %.5f (potential, Z=30)' % (ES, EP))
for c in [60, 20, 6, 2]:
    print('   Langmuir weight Re/%2d : E = %.4f  (text: %s)' % (c, (ES + EP * Re / c) / (1 + Re / c), {60: 0.344, 20: 0.358, 6: 0.399, 2: 0.485}[c]))

print('== (3.1) dimensional integration vs (3.2) non-dimensional: same path?')
b_nd = 0.8
def rhs_dim(t, Y):    # SI: x, z, vx, vz ; air u = U a(x/R, z/R)
    ax, az = air_vel('creeping', Y[0] / R, Y[1] / R)
    return [Y[2], Y[3], (U * ax - Y[2]) / tau, (U * az - Y[3] - tau * gstar) / tau]
ax0, az0 = air_vel('creeping', b_nd, -50.0)
sol_d = solve_ivp(rhs_dim, [0, 60 * R / U], [b_nd * R, -50 * R, U * ax0, U * az0 - vr], method='DOP853', rtol=1e-11, atol=1e-16, dense_output=True)
def rhs_nd(s_, y):
    ax, az = air_vel('creeping', y[0], y[1]); return [y[2], y[3], (ax - y[2]) / St, (az - y[3] - S) / St]
sol_n = solve_ivp(rhs_nd, [0, 60], [b_nd, -50.0, ax0, az0 - S], method='DOP853', rtol=1e-11, atol=1e-14, dense_output=True)
ss = np.linspace(0, 60, 13)
dev = max(np.abs(sol_d.sol(s_ * R / U)[0] / R - sol_n.sol(s_)[0]).max() for s_ in ss), max(np.abs(sol_d.sol(s_ * R / U)[1] / R - sol_n.sol(s_)[1]).max() for s_ in ss)
print('   b = 0.8: max |y_dimensional/R - y_nondim| over 13 times: x %.2e, z %.2e (path through z from -50 to %.2f)' % (dev[0], dev[1], sol_n.sol(60)[1]))

print('== (3.3)/(3.4) full nonlinear axis equation, p = 0, S = 0: St eta\'\' = a(eta) - eta\' ; log variables xi = ln(eta), u = eta\'/eta (u -> -infinity at a hit)')
def axis_reaches(flow, St_, Z):
    air_in = (lambda e: -(1 - 1 / (1 + e)**3)) if flow == 'potential' else (lambda e: -(1 - 1.5 / (1 + e) + 0.5 / (1 + e)**3))
    def f(s_, Y):
        e = np.exp(Y[0]); a_over_e = air_in(e) / e if e > 1e-6 else (-3 + 6 * e if flow == 'potential' else -1.5 * e)
        return [Y[1], (a_over_e - Y[1]) / St_ - Y[1]**2]
    Z0 = Z - 1.0
    Y0 = [np.log(Z0), air_in(Z0) / Z0]
    blow = lambda s_, Y: Y[1] + 1e3; blow.terminal = True
    sol = solve_ivp(f, [0, 400 * max(1, Z)], Y0, method='LSODA', rtol=1e-12, atol=1e-13, events=blow)
    return len(sol.t_events[0]) > 0
def axis_reaches_y(St_, Z):
    # creeping flow: the gap closes only algebraically (air speed ~ 1.5 eta^2), so plain Cartesian variables are fine: event gap < 1e-9
    inward = lambda y: -(1 - 1.5 / y + 0.5 / y**3)
    f = lambda s_, Y: [Y[1], (inward(Y[0]) - Y[1]) / St_]
    ev = lambda s_, Y: Y[0] - 1.0 - 1e-9; ev.terminal = True
    sol = solve_ivp(f, [0, 60 * Z], [Z, inward(Z)], method='LSODA', rtol=1e-12, atol=1e-14, events=ev)
    return len(sol.t_events[0]) > 0
lo, hi = 0.02, 0.3
for _ in range(40):
    mid = 0.5 * (lo + hi)
    if axis_reaches('potential', mid, 30.0): hi = mid
    else: lo = mid
print('   potential St_c = %.6f  (start 29 radii from the surface)   1/12 = %.6f' % (0.5 * (lo + hi), 1 / 12))
lo, hi = 0.5, 3.0
for _ in range(40):
    mid = 0.5 * (lo + hi)
    if axis_reaches_y(mid, 200.0): hi = mid
    else: lo = mid
print('   creeping  St_c = %.6f  (start at 200 radii)   text (Michael and Norey 1970) 1.21194' % (0.5 * (lo + hi)))
