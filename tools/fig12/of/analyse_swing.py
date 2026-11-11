"""Fig. 12, gates 1.2 and 1.5: the free swing after the tilt, from an OpenFOAM run's stoutMonitor.dat.

python tools/fig12/of/analyse_swing.py [--rho R] <stoutMonitor.dat[.gz]> [<another> ...]
python tools/fig12/of/analyse_swing.py [--rho R] --pair <slip run> <no-slip run>

Mass books (gate 1.5). m(t) is the stout in the domain, outVolume the stout volume that has left through the open
patches ('spill', 'atmosphere'). What is neither in the domain nor gone out has been lost by the numerics:
    leak(t) = m(t) - m(0) + rho * outVolume(t)      (negative: stout destroyed; positive: created)
rho is read from case.json next to the monitor (the workflow stores it there), else --rho (default 1000).

Swing energy. The swing's energy is what the stout has above its state of rest. The state of rest depends only on the
mass present (the surface flat at the height that holds it), so its potential energy is PE_rest(m), and
    dPE_rest/dm = g h(m),
h the height of the flat surface: adding dm at rest adds a layer dm/(rho A) thick at height h. Over a mass change dm
the surface moves by dm/(rho A); the second-order term g dm^2/(2 rho A) is printed and is far below a microjoule here.
So
    E(t) = KE + PE - PE(0) - g h0 (m(t) - m(0)),
h0 the mean of the four wall probes at t = 0 (the stout at rest before the tilt). This is exact whatever the stout's
shape, as long as m(0) is at rest. Where the lost stout came from is unknown, so its true share of the potential energy
lies between 0 and g h0 |leak|: that band is printed as the energy's uncertainty, and a damping ratio is reported only
while the swing energy stays well above it.

Per run: the swing's frequency (zero crossings of the lean, front minus back wall height, after the release at 1 s),
E averaged over 0.5 s windows from 1.5 s, and the damping ratio from a least-squares fit of ln E = c - 2 zeta omega t
over the windows whose energy exceeds 10 times the leak band; the time step (median and largest), with the damping
that first-order implicit (backward Euler) time stepping alone would cause, omega dt / 2 (derived with sympy: the
backward-Euler step of x'' = -omega^2 x multiplies the amplitude by 1/sqrt(1 + omega^2 dt^2)).
With a pair (slip walls and negligible viscosity, then no-slip and the stout's viscosity, same mesh) the gate 1.2: the
solver's own damping against the real friction's (no-slip minus slip); pass if below one tenth.
"""
import gzip, json, math, os, sys
import numpy as np

G = 9.81

def load(path):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt') as f: rows = [list(map(float, l.split())) for l in f if l.strip() and not l.startswith('#')]
    return np.array(rows)

def rho_for(path, rho_arg):
    cj = os.path.join(os.path.dirname(os.path.abspath(path)), 'case.json')
    if os.path.exists(cj):
        with open(cj) as f: c = json.load(f)
        if 'rho' in c: return float(c['rho']), 'case.json'
    return rho_arg, '--rho'

def analyse(path, rho_arg=1000.0, t0=1.5):
    d = load(path)
    t, m, ke, pe, outV, hf, hb, hl, hr = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 7], d[:, 8], d[:, 9], d[:, 10], d[:, 11]
    rho, rho_src = rho_for(path, rho_arg)
    h0 = float(np.mean([hf[0], hb[0], hl[0], hr[0]]))
    leak = (m - m[0]) + rho * outV
    E = ke + (pe - pe[0]) - G * h0 * (m - m[0])
    E_old = ke + (pe - pe[0])
    band = G * h0 * np.abs(leak)
    # second-order term of PE_rest: g dm^2 / (2 rho A), A the surface area at h0 from the tilt-free volume is unknown
    # here; bound it with the narrowest plausible surface (the glass's base radius 16.31 mm, guinness-glass.js)
    A_min = math.pi * 0.01631 ** 2
    second = G * np.max((m - m[0]) ** 2) / (2 * rho * A_min)
    lean = (hf - hb) * 1000
    sel = t >= 1.05
    ts, ls = t[sel], lean[sel] - np.mean(lean[sel])
    cross = [ts[i] - ls[i] * (ts[i + 1] - ts[i]) / (ls[i + 1] - ls[i]) for i in range(len(ls) - 1) if ls[i] * ls[i + 1] < 0]
    f = (len(cross) - 1) / (2 * (cross[-1] - cross[0])) if len(cross) > 2 else float('nan')
    w = 2 * math.pi * f
    edges = np.arange(t0, t[-1] - 0.25, 0.5); tw, Ew, Bw, Ow = [], [], [], []
    for a in edges:
        s = (t >= a) & (t < a + 0.5)
        if s.sum() > 5: tw.append(a + 0.25); Ew.append(np.mean(E[s])); Bw.append(np.max(band[s])); Ow.append(np.mean(E_old[s]))
    tw, Ew, Bw, Ow = map(np.array, (tw, Ew, Bw, Ow))
    good = (Ew > 10 * Bw) & (Ew > 0)
    zeta, n_fit = float('nan'), int(good.sum())
    if n_fit >= 3:
        zeta = -np.polyfit(tw[good], np.log(Ew[good]), 1)[0] / (2 * w)
    dts = np.diff(t[t >= 1.05])
    dt_med, dt_max = (float(np.median(dts)), float(np.max(dts))) if len(dts) else (float('nan'),) * 2
    return dict(path=path, rho=rho, rho_src=rho_src, h0=h0, f=f, zeta=zeta, n_fit=n_fit, n_win=len(tw),
                E0=Ew[0] if len(Ew) else float('nan'), E1=Ew[-1] if len(Ew) else float('nan'),
                Eo0=Ow[0] if len(Ow) else float('nan'), Eo1=Ow[-1] if len(Ow) else float('nan'),
                band_end=Bw[-1] if len(Bw) else float('nan'), t_end=t[-1], m0=m[0],
                dmass=(m[-1] - m[0]) / m[0], out_mass=rho * outV[-1], leak=leak[-1], leak_rel=leak[-1] / m[0],
                second=second, dt_med=dt_med, dt_max=dt_max, zeta_euler=w * dt_med / 2,
                lean_max=np.max(np.abs(lean[t > 1.05])) if np.any(t > 1.05) else float('nan'))

def show(r):
    print('%s (to %.2f s, rho %g from %s, rest height h0 %.2f mm)' % (r['path'], r['t_end'], r['rho'], r['rho_src'], 1e3 * r['h0']))
    print('  mass: %.6f kg at the start; change %.3e (relative); out through the open patches %.3e kg; lost by the numerics %.3e kg (%.2e relative)'
          % (r['m0'], r['dmass'], r['out_mass'], -r['leak'], -r['leak_rel']))
    print('  swing %.4f Hz; largest lean %.2f mm' % (r['f'], r['lean_max']))
    print('  swing energy %.1f -> %.1f uJ (window means; was %.1f -> %.1f uJ before the rest reference followed the mass);'
          ' leak band at the end +-%.1f uJ; second-order term below %.1e uJ'
          % (1e6 * r['E0'], 1e6 * r['E1'], 1e6 * r['Eo0'], 1e6 * r['Eo1'], 1e6 * r['band_end'], 1e6 * r['second']))
    print('  damping ratio %.5f (fitted on %d of %d windows above 10x the leak band)' % (r['zeta'], r['n_fit'], r['n_win']))
    print('  time step: median %.3e s, largest %.3e s; backward Euler alone would damp at omega dt/2 = %.5f'
          % (r['dt_med'], r['dt_max'], r['zeta_euler']))

if __name__ == '__main__':
    a = sys.argv[1:]
    rho = 1000.0
    if a and a[0] == '--rho': rho = float(a[1]); a = a[2:]
    if a and a[0] == '--pair':
        s, n = analyse(a[1], rho), analyse(a[2], rho); show(s); show(n)
        phys = n['zeta'] - s['zeta']
        if not (math.isfinite(s['zeta']) and math.isfinite(phys)) or phys <= 0:
            print('gate 1.2: no verdict (a damping ratio is missing or the friction adds none: solver %.5f, no-slip %.5f)' % (s['zeta'], n['zeta']))
            sys.exit(2)
        ok = s['zeta'] < 0.1 * phys
        print('gate 1.2: solver\'s own damping %.5f, real friction\'s %.5f (no-slip minus slip): ratio %.3f (limit 0.1): %s'
              % (s['zeta'], phys, s['zeta'] / phys, 'PASS' if ok else 'FAIL'))
        sys.exit(0 if ok else 1)
    for p in a: show(analyse(p, rho))
