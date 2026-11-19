# Fig. 16, rerun of the stored kerb ride on CPU, step 0: how long one step of the stored ride's solver takes on Kaggle's CPU.
# The solver exactly as the stored ride ran it: tools/fig12/kaggle/stout_jax.py at commit 7bb19a7 (run 5, notebook v8), 1.5 mm grid,
# model "full", K_frac 0.62 (run16 default then). 20 steps of the pint with the glass still, dt = 1 ms (the ride's steps are shorter
# when the stout moves fast; the ride's own step count is read from the stored ride: steps per picture).
import os, sys, time, json, re, urllib.request, glob
import numpy as np
C = '7bb19a7'; B = f'https://raw.githubusercontent.com/Numa1997/SiteTest/{C}/'
open('/tmp/stout_jax.py', 'wb').write(urllib.request.urlopen(B + 'tools/fig12/kaggle/stout_jax.py').read())
js = urllib.request.urlopen(B + 'public/scripts/guinness-glass.js').read().decode()
R = json.loads(re.search(r'R:\s*(\[[^\]]*\])', js).group(1))
sys.path.insert(0, '/tmp'); os.environ['JAX_PLATFORMS'] = 'cpu'
import jax; import stout_jax as SJ
print('device', jax.devices(), 'cpus', os.cpu_count(), flush=True)
t0 = time.time(); G = SJ.Geometry(R, 0.0005, 0.125, 0.0015); S = SJ.Stout(G, model='full', rho=1007.0, head_mass=True, seed=1, K_frac=0.62); s = S.init_state()
print(f'built in {time.time() - t0:.1f} s; particles {S.N:,}; cells {G.n}x{G.n}x{G.nz}', flush=True)
step = jax.jit(lambda s, dt: S.step(s, dt, 0.0, -9.81))
t0 = time.time(); s, d = step(s, 0.001); jax.block_until_ready(s['xp']); print(f'compile + first step {time.time() - t0:.1f} s', flush=True)
ts = []
for i in range(20):
    t0 = time.time(); s, d = step(s, 0.001); jax.block_until_ready(s['xp']); ts.append(time.time() - t0)
print(f'20 steps: median {np.median(ts):.2f} s, max {np.max(ts):.2f} s, iterations {int(d["it"])}', flush=True)
st = glob.glob('/kaggle/input/**/v8/output/2026-11-15/kerb_off.npz', recursive=True)
if st:
    Z = np.load(st[0]); steps = Z['steps']; t = Z['t']; k = np.searchsorted(t, 1.1)
    n = float(np.sum(steps[1:k + 1])); print(f'stored ride: {n:,.0f} steps up to t = {t[k]:.2f} s (rest of 2 s before it not included)', flush=True)
    print(f'ESTIMATE CPU time for the first {t[k]:.2f} s of the kerb ride: {n * np.median(ts) / 3600:.1f} h (plus the 2 s rest guard: about {2000 * np.median(ts) / 3600:.1f} h at dt = 1 ms)', flush=True)
