import numpy as np, sys
from PIL import Image
d = np.load(sys.argv[1]); md = d['mean_dist']
c = np.log10(np.maximum(md, 1e-12))
lo, hi = np.percentile(c, 2), np.percentile(c, 99.5)
u = np.clip((c - lo) / (hi - lo), 0, 1)
rose = np.array([226, 162, 170.]); wine = np.array([122, 31, 43.])
rgb = rose[None, None, :] * (1 - u[..., None]) + wine[None, None, :] * u[..., None]
a = (u ** 1.6) * 0.62 * 255
img = np.dstack([rgb, a]).astype(np.uint8)
Image.fromarray(img, 'RGBA').save(sys.argv[2])
print('log10 mean distance: 2%% %.2f, 99.5%% %.2f, min %.2f, max %.2f' % (lo, hi, c.min(), c.max()))
