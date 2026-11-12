"""Fig. 14: reads the stored Kaggle runs (public/data/schrodinger-sphere/*.bin) and prints the numbers the note quotes.
Usage: python3 notes/fig14/runs.py [E V0 R ...]"""
import json, struct, zlib, sys, os, numpy as np
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public', 'data', 'schrodinger-sphere', '2026-11-12')   # the first generation (generations.json)
IDX = json.load(open(os.path.join(D, 'index.json')))
def read(r, frames=False):
    b = open(os.path.join(D, r['file']), 'rb').read()
    assert b[:4] == b'SPH1'
    H = struct.unpack('<I', b[4:8])[0]; head = json.loads(b[8:8 + H])
    if frames:
        raw = np.frombuffer(zlib.decompress(b[8 + H:]), np.uint8); n, o = head['n'], head['out']
        head['amp'] = raw[:n * o * o].reshape(n, o, o)   # amplitude only on the website since 12 November 2026
    head['c'] = np.array(head['curves']); return head
def find(E, V, R):
    for r in IDX['runs']:
        if abs(r['E'] - E) < 1e-9 and abs(r['V0'] - V) < 1e-9 and abs(r['R'] - R) < 1e-9: return r
if __name__ == '__main__':
    print('runs', len(IDX['runs']), 'N', IDX['N'], 'L', IDX['L'], 'dt', IDX['dt'], 'sweep', IDX['sweep_s'])
    walls = [r['wall'] for r in IDX['runs']]; print('wall sum %.1f s, min %.2f max %.2f' % (sum(walls), min(walls), max(walls)))
    print('bytes total %.1f MB' % (sum(r['bytes'] for r in IDX['runs']) / 1e6))
    # norm in the first quarter of every run
    worst = 0; worst_at = None; s0 = IDX['sigma0']; free_worst = 0
    for r in IDX['runs']:
        h = read(r); c = h['c']; q = len(c) // 4
        d = np.max(np.abs(c[:q + 1, 1] - 1))
        if d > worst: worst, worst_at = d, (r['E'], r['V0'], r['R'])
        if r['V0'] == 0:
            fl = s0 * np.sqrt(1 + (c[:, 0] / (2 * s0 * s0)) ** 2)
            e = np.max(np.abs(c[:q + 1, 4] - fl[:q + 1])); free_worst = max(free_worst, e)
    print('norm first quarter (frames 0..12): max |norm-1| = %.2e at' % worst, worst_at)
    print('free runs (V0=0): max |sigma_y - law| in first quarter = %.2e' % free_worst)
    args = [float(a) for a in sys.argv[1:]]
    for i in range(0, len(args), 3):
        r = find(*args[i:i + 3]); h = read(r); c = h['c']
        print('\nE=%g V0=%g R=%g file %s steps %d wall %.2f dt_frame %.2f' % (r['E'], r['V0'], r['R'], r['file'], h['steps'], h['wall'], c[1, 0]))
        for f in [0, 6, 12, 18, 24, 30, 36, 42, 47]:
            t, n, b, a, sy = c[f]; print('  f%2d t=%6.2f norm=%.6f behind=%.5f ahead=%.5f inside=%.5f lost=%.5f sy=%.4f free=%.4f' % (f, t, n, b, a, n - b - a, 1 - n, sy, s0 * np.sqrt(1 + (t / 18) ** 2)))
