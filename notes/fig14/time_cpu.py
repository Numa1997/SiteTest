import sys, time, numpy as np
sys.path.insert(0, '/home/user/SiteTest/tools/kaggle/schrodinger-sphere')
import jax, jax.numpy as jnp
from solver import setup
for N in (64, 128):
    g = setup(N, 64.0)
    p = jnp.asarray(np.random.rand(N, N, N) + 0j, jnp.complex64); kin = jnp.asarray(np.exp(-0.5j * g['K2'] * 0.01), jnp.complex64)
    f = jax.jit(lambda p: jnp.fft.ifftn(kin * jnp.fft.fftn(p)))
    f(p).block_until_ready(); t = time.time()
    for i in range(20): p = f(p)
    p.block_until_ready(); print(N, 'ms per kinetic step', (time.time() - t) / 20 * 1e3)
