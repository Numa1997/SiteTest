"""Chaos map -> PNG for the Fig. 13 page.

Brightness v = log(1000 d) / log(1000), clipped to [0, 1], where d is the mean capped twin distance (chaos_map.py). This is
the scale of 2swap's swaptube (PendulumGridScene.cpp, mode 3: log(coloration * distance) / log(coloration), coloration 1000).
Colour: transparent where v = 0 (regular), wine #7a1f2b rising to rose #e2a2aa at v = 1; alpha = v^0.8. The page lays it under
the tip paths at reduced opacity.

Usage: python3 tools/fig13/map_png.py MAP.npz OUT.png
"""
import sys, json
import numpy as np
from PIL import Image

d = np.load(sys.argv[1])
m = d['mean_capped_dist'].astype(np.float64)
meta = json.loads(str(d['meta']))
assert m.shape == (meta['height'], meta['width'])
v = np.clip(np.log(1000 * np.maximum(m, 1e-12)) / np.log(1000), 0, 1)
wine, rose = np.array([122, 31, 43]), np.array([226, 162, 170])
rgb = wine[None, None, :] * (1 - v[..., None]) + rose[None, None, :] * v[..., None]
a = 255 * v ** 0.8
img = np.dstack([rgb, a]).round().clip(0, 255).astype(np.uint8)
Image.fromarray(img, 'RGBA').save(sys.argv[2], optimize=True)
print('wrote', sys.argv[2], img.shape, 'share of pixels with v > 0.5:', round(float((v > 0.5).mean()), 4), 'meta:', meta)
