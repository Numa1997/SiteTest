"""Chapter 8 checks: the chained machine against the separate chapters. Runs derive/ch08_probe.cjs (the page's own modules in Node) and
writes data/ch08/derive_results.json; the page shows the table and the sensitivity table at the defaults.

    python3 portfolios-src/electron-beam/derive/ch08.py
"""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parents[1]
d = json.loads(subprocess.run(['node', str(HERE / 'derive' / 'ch08_probe.cjs')], capture_output=True, text=True, check=True).stdout)
o, h, p = d['o'], d['hand'], d['p']
checks, nums = [], {}


def check(cid, title, ok, detail, record=False):
    checks.append({'id': cid, 'title': title, 'ok': bool(ok), 'detail': detail, 'record': record})


check('W1', 'the chain reproduces the separate chapters: chapter 5’s best probe from chapter 2’s source and chapter 4’s lens, and chapter 7’s σ_CD and rate from it',
      abs(o['d_p'] / h['d_p'] - 1) < 1e-12 and abs(o['sigma_CD'] / h['sigma_CD'] - 1) < 1e-8 and abs(o['MPH'] / h['MPH'] - 1) < 1e-12,
      'd_p %.6g nm both ways; σ_CD %.8g against %.8g nm' % (o['d_p'] * 1e9, o['sigma_CD'] * 1e9, h['sigma_CD'] * 1e9))
ys = d['yields']
dev = [max(abs(y['delta_t'] - y['delta']) / y['udelta'], abs(y['eta_t'] - y['eta']) / y['ueta']) for y in ys]
check('W2', 'chapter 6 read from its stored runs (interpolated in log E) against fresh runs off the grid, silicon at 1.2, 4 and 12 kV: δ and η within 3 statistical errors',
      max(dev) < 3, '; '.join('%g kV: δ %.3f vs %.3f, η %.3f vs %.3f, core %.2f vs %.2f nm, halo %.1f vs %.1f nm' % (y['V'] / 1e3, y['delta_t'], y['delta'], y['eta_t'], y['eta'], y['core_t'] * 1e9, y['core'] * 1e9, y['halo_t'] * 1e9, y['halo'] * 1e9) for y in ys))
df = d['defocus']
check('W3', 'defocus: chapter 4’s axial ray with the excitation raised by ε crosses the axis earlier by Δz = 2C_cε (C_c referred to the image)',
      all(abs(x['dz'] / x['model'] - 1) < 1e-3 for x in df), '; '.join('ε = %g: traced %.4f nm, 2C_cε = %.4f nm' % (x['eps'], x['dz'] * 1e9, x['model'] * 1e9) for x in df))
check('W4', 'the tolerance Monte Carlo’s source: B_r interpolated in the 5 × 5 grid of chapter 2 runs against direct runs at the same random draws (5 samples)',
      d['grid_worst'] < 0.01, 'largest relative difference %.2g' % d['grid_worst'])
S = o['sens']
NIN = 10
row = lambda i: S[i * NIN:(i + 1) * NIN]
sCD, sMPH = row(2), row(3)
tframe = p['N_px'] ** 2 * p['t_d']
check('W5', 'sensitivities with a known answer: σ_CD to dwell time and to the number of lines −½ each; rate to dwell time −t_frame/(t_frame + t_ov)',
      abs(sCD[7] + 0.5) < 0.02 and abs(sCD[8] + 0.5) < 0.03 and abs(sMPH[7] + tframe / (tframe + 1.0)) < 1e-3,
      'σ_CD: %.3f, %.3f; rate: %.4f against %.4f' % (sCD[7], sCD[8], sMPH[7], -tframe / (tframe + 1.0)))
nums['sens'] = S
nums['o'] = {k: v for k, v in o.items() if k not in ('sens', 'pwin')}
pw = o['pwin']
nums['pwin'] = pw
nums['defocus'] = df
nums['hand'] = h
nums['tol_each'] = d['tol_each']
out = {'checks': checks, 'numbers': nums, 'summary': '%d of %d checks pass' % (sum(c['ok'] for c in checks), len(checks))}
(HERE / 'data' / 'ch08').mkdir(parents=True, exist_ok=True)
(HERE / 'data' / 'ch08' / 'derive_results.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
if __name__ == '__main__':
    for c in checks:
        print(('PASS ' if c['ok'] else 'FAIL ') + c['id'] + ' ' + c['title'] + ' :: ' + c['detail'])
    print(out['summary'])
    sys.exit(0 if all(c['ok'] for c in checks) else 1)
