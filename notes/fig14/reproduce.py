"""Fig. 14: re-runs the page's own solver (tools/kaggle/schrodinger-sphere/solver.py, imported unchanged) on this
workspace's CPU with JAX, and measures what the note quotes about the method.
Usage: python3 notes/fig14/reproduce.py <task>   tasks: stored, bits, order, unitary, energy"""
import sys, time, json, numpy as np
sys.path.insert(0, '/home/user/SiteTest/tools/kaggle/schrodinger-sphere')
import jax
jax.config.update('jax_enable_x64', True)
import jax.numpy as jnp
from solver import setup, run
sys.path.insert(0, '/home/user/SiteTest/notes/fig14')
from runs import read, find
task = sys.argv[1]
out = {}
def init(g, E, V0, R, s0=3.0, x0=-14.0):
    x = g['x']; X, Y, Z = np.meshgrid(x, x, x, indexing='ij'); k0 = np.sqrt(2 * E)
    psi = (2 * np.pi * s0**2) ** -0.75 * np.exp(-((X - x0)**2 + Y**2 + Z**2) / (4 * s0**2) + 1j * k0 * X)
    V = np.where(X**2 + Y**2 + Z**2 < R**2, V0, 0.0); return psi, V
def stepper(g, V, dt, dtype, use_mask=True):
    halfV = jnp.asarray(np.exp(-0.5j * V * dt), dtype); kin = jnp.asarray(np.exp(-0.5j * g['K2'] * dt), dtype)
    mask = jnp.asarray(g['mask'] if use_mask else np.ones_like(g['mask']), jnp.float64 if dtype == jnp.complex128 else jnp.float32)
    @jax.jit
    def many(p, n):
        def body(i, p):
            p = halfV * p; p = jnp.fft.ifftn(kin * jnp.fft.fftn(p)); p = halfV * p
            return p * mask
        return jax.lax.fori_loop(0, n, body, p)
    return many
def slabs(g, psi, R):
    rho = np.abs(np.asarray(psi))**2 * g['dx']**3; rx = rho.sum(axis=(1, 2)); x = g['x']
    return float(rx.sum()), float(rx[x < -R].sum()), float(rx[x > R].sum())
if task == 'stored':          # the stored default run and the E=2 test run, solver.run unchanged, 32-bit, CPU
    g = setup(128, 64.0)
    for (E, V0, R) in [(2.5, 3.0, 4.0), (2.0, 3.0, 4.0)]:
        t = time.time(); r = run(g, E, V0, R); c = r['curves'][-1]; s = read(find(E, V0, R))['c'][-1]
        out[f'{E}_{V0}_{R}'] = dict(cpu=[float(v) for v in c], kaggle=[float(v) for v in s], steps=int(r['steps']), wall=time.time() - t,
                                    maxdiff=float(np.max(np.abs(r['curves'] - read(find(E, V0, R))['c']))))
        print(out)
elif task == 'bits':          # 32-bit against 64-bit, same run, solver.run unchanged
    g = setup(128, 64.0, dtype=jnp.complex128); r = run(g, 2.0, 3.0, 4.0); out['c128'] = [float(v) for v in r['curves'][-1]]; print(out)
elif task == 'order':         # the time error: same end time, dt halved again and again, 64-bit, whole psi compared
    g = setup(128, 64.0, dtype=jnp.complex128); psi0, V = init(g, 2.0, 3.0, 4.0); T = 14.57
    res = {}
    for dt in [0.04, 0.02, 0.01, 0.005, 0.0025]:
        n = int(round(T / dt)); t = time.time(); p = stepper(g, V, dt, jnp.complex128)(jnp.asarray(psi0), n); p = np.asarray(p)
        res[dt] = p; nb, b, a = slabs(g, p, 4.0); out[dt] = dict(steps=n, norm=nb, behind=b, ahead=a, s=time.time() - t)
        print(dt, out[dt], flush=True)
    dts = sorted(res)[::-1]
    for i in range(len(dts) - 1):
        d = np.sqrt(np.sum(np.abs(res[dts[i]] - res[dts[i + 1]])**2) * g['dx']**3); out[f'diff_{dts[i]}_{dts[i+1]}'] = float(d); print(dts[i], dts[i + 1], d, flush=True)
elif task == 'unitary':       # norm without the absorbing border: each factor unitary
    for dtype in (jnp.complex64, jnp.complex128):
        g = setup(128, 64.0); psi0, V = init(g, 2.5, 3.0, 4.0)
        p = jnp.asarray(psi0, dtype); n0 = float(np.sum(np.abs(np.asarray(p, np.complex128))**2) * g['dx']**3)
        f = stepper(g, V, 0.01, dtype, use_mask=False); rows = []
        for k in range(5):
            p = f(p, 300); n = float(np.sum(np.abs(np.asarray(p, np.complex128))**2) * g['dx']**3); rows.append((300 * (k + 1), n - n0))
        out[str(dtype.__name__ if hasattr(dtype, '__name__') else dtype)] = dict(n0=n0, rows=rows); print(out, flush=True)
elif task == 'energy':        # mean energy of the starting packet, from its Fourier transform: k0^2/2 + 3/(8 sigma0^2)?
    g = setup(128, 64.0); psi0, V = init(g, 2.5, 0.0, 4.0); ph = np.fft.fftn(psi0); w = np.abs(ph)**2
    out['norm'] = float(np.sum(np.abs(psi0)**2) * g['dx']**3); out['mean_k2_over_2'] = float(np.sum(w * g['K2']) / np.sum(w) / 2)
    out['formula'] = 2.5 + 3 / (8 * 9); kx = 2 * np.pi * np.fft.fftfreq(128, g['dx']); out['kmax_grid'] = float(np.abs(kx).max())
    print(out)
json.dump(out, open(f'/home/user/SiteTest/notes/fig14/reproduce-{task}.json', 'w'), indent=1, default=str)
