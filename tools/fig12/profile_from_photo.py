"""Outer profile of the Guinness tulip pint glass from a side-on product photograph.

Input: a 500 x 500 px JPEG on white (MBS Wholesale product photo, guiness_2.jpg).
Method: per pixel row, the outermost pixels darker than a threshold mark the glass edge; the
half-width is half their distance. The pixel scale is fixed by the published height, 160 mm
(retailer listings: Nisbets JA936, Carrolls, Conaty). Output: CSV of z (mm, from the foot)
and outer radius R(z) (mm), smoothed, plus a diagnostic image.
"""
import sys, numpy as np
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert('L')).astype(float)
H = 160.0                                   # mm, published overall height
dark = im < 225
rows = np.where(dark.sum(1) > 2)[0]
top, bot = rows.min(), rows.max()
zs, rs, cs = [], [], []
for y in range(top, bot + 1):
    xs = np.where(dark[y])[0]
    if len(xs) < 2: continue
    zs.append(bot - y); rs.append((xs.max() - xs.min()) / 2); cs.append((xs.max() + xs.min()) / 2)
zs, rs, cs = map(np.array, (zs, rs, cs))
s = H / (bot - top)                          # mm per px
print(f'glass spans rows {top}..{bot} = {bot-top} px -> {s:.4f} mm/px; axis at x = {np.median(cs):.1f} px (spread {cs.std():.2f} px)')
z_mm, r_mm = zs * s, rs * s
# median filter then moving average (5 px)
from scipy.ndimage import median_filter, uniform_filter1d
r_s = uniform_filter1d(median_filter(r_mm, 7), 5)
print(f'max outer diameter {2*r_s.max():.1f} mm at z = {z_mm[r_s.argmax()]:.1f} mm; rim {2*r_s[-3:].mean():.1f} mm; foot {2*r_s[:3].mean():.1f} mm')
np.savetxt(out, np.c_[z_mm, r_s], delimiter=',', header='z_mm,R_outer_mm', fmt='%.3f')
img = Image.open(src).convert('RGB'); d = ImageDraw.Draw(img)
cx = np.median(cs)
for z, r in zip(zs, r_s / s):
    y = bot - z; d.point((cx - r, y), fill=(200, 0, 0)); d.point((cx + r, y), fill=(200, 0, 0))
img.save(out.replace('.csv', '_check.png'))
