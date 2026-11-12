"""Fig. 14 note: numbers for the figures and for section 9, from the stored runs."""
import numpy as np, json, sys
sys.path.insert(0, '/home/user/SiteTest/notes/fig14')
from runs import IDX, read, find
out = {}
h = read(find(2.5, 3.0, 4.0), frames=True); A = h['amp']; c = h['c']
sat = [(int(f), int((A[f] == 255).sum())) for f in range(48) if (A[f] == 255).sum() > 0]
out['saturated_frames'] = sat; out['peak_frame0_pixels255'] = int((A[0] == 255).sum())
out['level_max_by_frame'] = [int(A[f].max()) for f in range(48)]
out['curves_default'] = c.tolist()
# free runs: sigma_y against the law over the whole run
s0 = 3.0; worst = 0
for r in IDX['runs']:
    if r['V0'] == 0:
        cc = read(r)['c']; law = s0 * np.sqrt(1 + (cc[:, 0] / 18) ** 2); worst = max(worst, float(np.max(np.abs(cc[:, 4] - law))))
out['free_sigma_worst_whole_run'] = worst
# ahead at the end against V0, E = 2.5
out['ahead_vs_V0'] = {R: [(r['V0'], r['ahead'], r['behind'], round(1 - r['norm_end'], 5)) for r in sorted([q for q in IDX['runs'] if q['E'] == 2.5 and q['R'] == R], key=lambda q: q['V0'])] for R in (2.0, 4.0, 6.0)}
# a few end values over the grid
runs = IDX['runs']
ahead_EltV = [r for r in runs if r['E'] < r['V0']]
out['E<V0 ahead range'] = (min(r['ahead'] for r in ahead_EltV), max(r['ahead'] for r in ahead_EltV))
out['lost_end_range'] = (min(1 - r['norm_end'] for r in runs), max(1 - r['norm_end'] for r in runs), [ (r['E'], r['V0'], r['R']) for r in runs if 1 - r['norm_end'] == max(1 - q['norm_end'] for q in runs)])
print(json.dumps({k: v for k, v in out.items() if k != 'curves_default'}, indent=0)[:3000])
json.dump(out, open('/home/user/SiteTest/notes/fig14/figdata.json', 'w'))
