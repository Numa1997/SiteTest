"""Fig. 12, gate 1.2: the free swing after the tilt, from an OpenFOAM run's stoutMonitor.dat.

python tools/fig12/of/analyse_swing.py <stoutMonitor.dat[.gz]> [<another> ...]
Per run: the swing's frequency (zero crossings of the lean, front minus back wall height, after the release at 1 s), the
swing's energy E = KE + (PE - PE_rest) (PE_rest the potential energy at t = 0, the stout at rest), its mean over 0.5 s
windows from 1.5 s, and the damping ratio from a least-squares fit of ln E = c - 2 zeta omega t; the mass change.
With a slip run and a no-slip run of the same mesh given as a pair (--pair slip.dat noslip.dat), the gate: the solver's
own damping (slip, negligible viscosity) against the real friction's (no-slip minus slip); pass if below one tenth.
"""
import gzip, math, sys
import numpy as np

def load(path):
    op = gzip.open if path.endswith('.gz') else open
    with op(path, 'rt') as f: rows = [list(map(float, l.split())) for l in f if l.strip() and not l.startswith('#')]
    return np.array(rows)

def analyse(path, t0=1.5):
    d = load(path); t, m, ke, pe, hf, hb = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 8], d[:, 9]
    E = ke + (pe - pe[0]); lean = (hf - hb) * 1000
    sel = t >= 1.05
    ts, ls = t[sel], lean[sel] - np.mean(lean[sel])
    cross = [ts[i] - ls[i] * (ts[i + 1] - ts[i]) / (ls[i + 1] - ls[i]) for i in range(len(ls) - 1) if ls[i] * ls[i + 1] < 0]
    f = (len(cross) - 1) / (2 * (cross[-1] - cross[0])) if len(cross) > 2 else float('nan')
    w = 2 * math.pi * f
    edges = np.arange(t0, t[-1] - 0.25, 0.5); tw, Ew = [], []
    for a in edges:
        s = (t >= a) & (t < a + 0.5)
        if s.sum() > 5: tw.append(a + 0.25); Ew.append(np.mean(E[s]))
    tw, Ew = np.array(tw), np.array(Ew)
    slope = np.polyfit(tw, np.log(Ew), 1)[0] if len(tw) >= 3 else float('nan')
    zeta = -slope / (2 * w)
    return dict(path=path, f=f, zeta=zeta, E0=Ew[0] if len(Ew) else float('nan'), E1=Ew[-1] if len(Ew) else float('nan'),
                t_end=t[-1], dmass=(m[-1] - m[0]) / m[0], lean_max=np.max(np.abs(lean[t > 1.05])) if np.any(t > 1.05) else float('nan'))

def show(r):
    print('%s: to %.2f s; swing %.4f Hz; swing energy %.1f -> %.1f uJ (window means); damping ratio %.5f; largest lean %.2f mm; mass change %.2e'
          % (r['path'], r['t_end'], r['f'], 1e6 * r['E0'], 1e6 * r['E1'], r['zeta'], r['lean_max'], r['dmass']))

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--pair':
        s, n = analyse(a[1]), analyse(a[2]); show(s); show(n)
        phys = n['zeta'] - s['zeta']
        ok = s['zeta'] < 0.1 * phys
        print('gate 1.2: solver\'s own damping %.5f, real friction\'s %.5f (no-slip minus slip): ratio %.3f (limit 0.1): %s'
              % (s['zeta'], phys, s['zeta'] / phys, 'PASS' if ok else 'FAIL'))
        sys.exit(0 if ok else 1)
    for p in a: show(analyse(p))
