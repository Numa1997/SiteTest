# Fig. 16, kerb ride with control off, rerun on Kaggle's CPU to record where and how fast the stout leaves the rim (19 Nov 2026).
# The solver and the cart exactly as the stored ride (run 5, GPU notebook v8) ran them: commit 7bb19a7 of github.com/Numa1997/SiteTest.
# Only the RUNNER is changed, by text, below: (1) the rest guard is not rerun (the stored ride passed it; the ride starts from a fresh
# pint, not from the rest run); (2) the ride ends at 1.1 s (90 % of the stored spill has left by 1.02 s); (3) at every picture, every
# particle that has newly left the stout (fly, landed or stuck since the last picture) is saved with its position and velocity;
# (4) the stored ride's own settings, read from its summary.json (v8): k_frac 1.0, m_drops 131072, rot true, vol_corr 0.5 (the
# volume correction ON; version 1 of this rerun had it off, a different ride, and is ignored). Control is off, so the probe type plays no part.
# The check: the spilled mass against time must follow the stored ride's curve (75.6 g at 4 s; 492 g/s peak at 0.85 s).
import os, sys, json, re, urllib.request, runpy, glob
C = '7bb19a7'; B = f'https://raw.githubusercontent.com/Numa1997/SiteTest/{C}/'; ROOT = '/tmp/repo'
FILES = ['tools/fig12/kaggle/stout_jax.py', 'tools/fig12/kaggle/run_b.py', 'tools/fig12/glass_profile.json', 'tools/fig16/slosh_model.py',
         'tools/fig16/spill.py', 'tools/fig16/fit.json', 'tools/fig16/validation.json', 'tools/fig16/kaggle/cart4.py', 'tools/fig16/kaggle/modal4.py',
         'tools/fig16/kaggle/run16.py']
for f in FILES:
    p = os.path.join(ROOT, f); os.makedirs(os.path.dirname(p), exist_ok=True)
    try: open(p, 'wb').write(urllib.request.urlopen(B + f).read())
    except Exception as e: print('fetch failed', f, e, flush=True)
js = urllib.request.urlopen(B + 'public/scripts/guinness-glass.js').read().decode()
R = json.loads(re.search(r'R:\s*(\[[^\]]*\])', js).group(1)); json.dump({'R': R}, open('/tmp/glass.json', 'w'))
src = open(os.path.join(ROOT, 'tools/fig16/kaggle/run16.py')).read()
def rep(a, b):
    global src
    assert src.count(a) == 1, ('patch target not found once', a); src = src.replace(a, b)
rep('+ ["rest", "design"]]', '+ ["design"]]')
rep('dict(name="kerb_off", kind="ride", road=KERB, v0=1.5, ctrl="off", end=end_(4.0))', 'dict(name="kerb_off", kind="ride", road=KERB, v0=1.5, ctrl="off", end=1.1)')
rep('    def record(s, t, ex, st, wall):\n        o = obs(s); P = pol(o["H"])',
    '    LEFT = dict(t=[], x=[], v=[], k=[]); prevout = [None]\n'
    '    def record(s, t, ex, st, wall):\n'
    '        out_ = ~np.asarray(s["act"])\n'
    '        new = out_ if prevout[0] is None else (out_ & ~prevout[0]); prevout[0] = out_\n'
    '        if new.any():\n'
    '            LEFT["x"].append(np.asarray(s["xp"])[new].astype(np.float32)); LEFT["v"].append(np.asarray(s["vp"])[new].astype(np.float32))\n'
    '            LEFT["t"].append(np.full(int(new.sum()), float(t), np.float32)); LEFT["k"].append(np.full(int(new.sum()), len(rec["t"]), np.int32))\n'
    '        o = obs(s); P = pol(o["H"])')
rep('    np.savez_compressed(WORK / f"{name}.npz",',
    '    if LEFT["t"]: np.savez_compressed(WORK / f"{name}_left_rim.npz", t=np.concatenate(LEFT["t"]), x=np.concatenate(LEFT["x"]), v=np.concatenate(LEFT["v"]), picture=np.concatenate(LEFT["k"]), mp=S.mp, N=S.N)\n'
    '    np.savez_compressed(WORK / f"{name}.npz",')
open(os.path.join(ROOT, 'tools/fig16/kaggle/run16.py'), 'w').write(src)
os.environ.update(GLASS_JSON='/tmp/glass.json', BUDGET_S='40000', ONLY='kerb_off', K_FRAC='1.0', M_DROPS='131072', VOL_CORR='0.5', ROT='1', JAX_PLATFORMS='cpu', NB_WORK='/kaggle/working')
for d in ('tools/fig16/kaggle', 'tools/fig16', 'tools/fig12/kaggle'): sys.path.insert(0, os.path.join(ROOT, d))
runpy.run_path(os.path.join(ROOT, 'tools/fig16/kaggle/run16.py'), run_name='__main__')

# ---------------------------------------------------------------- the check, with its pass marks fixed BEFORE the run (19 Nov 2026)
# CPU and GPU round differently and the spray is chaotic: the curve must agree in shape and total, not drop for drop.
# PASS when all three hold: spilled mass at 1.1 s within 15 % of the stored ride's; time of the peak flux within 0.05 s (3 pictures);
# peak flux within 25 %.
import numpy as np, json as _j
new = glob.glob('/kaggle/working/**/kerb_off.npz', recursive=True); old = glob.glob('/kaggle/input/**/v8/output/2026-11-15/kerb_off.npz', recursive=True)
if new and old:
    A, Bz = np.load(new[0]), np.load(old[0]); mp = float(Bz['mp']); N = int(Bz['N'])
    def curve(Z): t = Z['t'].astype(float); s = (N - Z['nact'].astype(float)) * mp * 1e3; return t, s, np.gradient(s, t)
    ta, sa, fa = curve(A); tb, sb, fb = curve(Bz); k = np.searchsorted(tb, ta[-1])
    r = dict(t_end=float(ta[-1]), spilled_new_g=float(sa[-1]), spilled_stored_g=float(sb[k]), peak_t_new=float(ta[np.argmax(fa)]), peak_t_stored=float(tb[np.argmax(fb[:k + 1])]),
             peak_new_gps=float(fa.max()), peak_stored_gps=float(fb[:k + 1].max()))
    r['pass_total'] = abs(r['spilled_new_g'] / r['spilled_stored_g'] - 1) < 0.15; r['pass_peak_time'] = abs(r['peak_t_new'] - r['peak_t_stored']) < 0.05
    r['pass_peak_flux'] = abs(r['peak_new_gps'] / r['peak_stored_gps'] - 1) < 0.25; r['PASS'] = r['pass_total'] and r['pass_peak_time'] and r['pass_peak_flux']
    print('CHECK', _j.dumps(r), flush=True); _j.dump(r, open('/kaggle/working/check.json', 'w'), indent=1)
else: print('CHECK not done: files', new, old, flush=True)
