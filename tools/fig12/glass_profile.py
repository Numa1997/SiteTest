"""Fig. 12: the inner profile of the tulip pint, measured from a dimensioned drawing.

Source: dimensions.com, "Irish Imperial Pint Glass" (the tulip, or Guinness, glass), dimensioned elevation and section, SVG:
https://cdn.prod.website-files.com/5b44edefca321a1e2d0c2aa6/61aac02a3ae60613b9073f5e_Dimensions-Objects-Beer-Glasses-Irish-Imperial-Pint-Glass-Dimensions.svg
(saved as tools/fig12/irish-imperial-pint.svg). It states: height 5.875 in (149 mm), diameter 3 in (76 mm), base 2.375 in, 16 oz.
The Guinness imperial pint is listed by retailers at 160 mm tall, 85 mm across at the widest, 568 ml.

Method: the SVG is rendered at 4x (4000 x 2300 px) in Chromium:
  node -e "require('playwright').chromium.launch().then(async b=>{const p=await b.newPage({viewport:{width:1000,height:575},deviceScaleFactor:4});
           await p.goto('file://'+process.argv[1]);await p.screenshot({path:process.argv[2]});await b.close()})" irish-imperial-pint.svg drawing.png
then, in the middle drawing (the section), every pixel row between the rim and the cavity floor is scanned outward from the axis
to the first red pixel on each side: that is the inner wall. The outer wall is the last red pixel. Lines are 3 px wide at 1x
(12 px here); the inner edge of the inner line is the cavity wall.
Usage: python3 tools/fig12/glass_profile.py drawing.png  -> prints the measurements and writes tools/fig12/glass_profile.json
"""
import sys, json, os
import numpy as np
from PIL import Image

img = np.asarray(Image.open(sys.argv[1]).convert('RGBA')).astype(int)
red = (img[:, :, 3] > 0) & (img[:, :, 0] > 150) & (img[:, :, 1] < 120) & (img[:, :, 2] < 140)
H, W = red.shape
x0, x1 = 1560, 2560                       # the section drawing lies between these columns (4x px)
xc = (x0 + x1) // 2
col = red[:, x0:x1]
# rim: the top line of the section; foot: the dashed base line at the bottom; floor: the inner bottom of the cavity at the axis
rows = np.where(red[:, x0:x0 + 300].any(axis=1))[0]   # the left wall only: the height label reaches into the middle
rim_y = rows.min()
axis_hits = np.where(red[:, xc - 2:xc + 3].any(axis=1))[0]
foot_y = axis_hits.max()                  # outer base line, under the axis
floor_y = max(y for y in axis_hits if y < foot_y - 40)    # the cavity floor line above it
# the inner floor surface is the top edge of that line
while red[floor_y - 1, xc - 2:xc + 3].any(): floor_y -= 1
px_per_mm = (foot_y - rim_y) / 149.2      # 5.875 in = 149.2 mm, rim line to foot line
prof = []
for y in range(rim_y + 40, floor_y):     # 40 px (3 mm) under the rim line: below the rounded lip
    left = right = None
    for x in range(xc, x0, -1):
        if red[y, x]: left = x; break
    for x in range(xc, x1):
        if red[y, x]: right = x; break
    if left is None or right is None: continue
    # the outer wall: last red pixel on each side
    oL = x0 + np.where(red[y, x0:xc])[0].min(); oR = xc + np.where(red[y, xc:x1])[0].max()
    prof.append(((floor_y - y) / px_per_mm, (right - left) / 2 / px_per_mm, (oR - oL) / 2 / px_per_mm))
prof.reverse()                            # z increasing
prof = np.array(prof)
# rows just under the rim cross the rounded lip: keep the rows below 3 mm under the rim, then continue the wall's last 10 mm slope
keep = prof[:, 0] < prof[:, 0].max() - 3.0
tail = prof[keep][-int(10 * px_per_mm):]
slope = np.polyfit(tail[:, 0], tail[:, 1], 1)[0]
zt = np.arange(prof[keep][:, 0].max(), prof[:, 0].max() + 1e-9, 1 / px_per_mm)
ext = np.array([(zz, prof[keep][-1, 1] + slope * (zz - prof[keep][-1, 0]), prof[keep][-1, 2]) for zz in zt[1:]]).reshape(-1, 3)
prof = np.vstack([prof[keep], ext])
z, ri, ro = prof[:, 0], prof[:, 1], prof[:, 2]
print('rim row %d, cavity floor row %d, foot row %d; %.3f px/mm' % (rim_y, floor_y, foot_y, px_per_mm))
print('drawing: cavity depth %.1f mm, floor %.1f mm above the foot; inner radius min %.1f at z=%.1f, max %.1f at z=%.1f, at the rim %.1f mm; outer max diameter %.1f mm (stated 76.2)'
      % (z.max(), (foot_y - floor_y) / px_per_mm, ri.min(), z[ri.argmin()], ri.max(), z[ri.argmax()], ri[z.argmax()], 2 * ro.max()))
# scale to the Guinness imperial pint: 160 mm tall (149.2 drawn), 85 mm widest outer diameter
sz, sr = 160.0 / 149.2, 85.0 / (2 * ro.max())
Z = z * sz / 1000; R = ri * sr / 1000           # metres
# resample on a 0.5 mm grid in z, smoothing the pixel steps (moving average over 2 mm)
zg = np.arange(0, Z.max(), 0.0005)
Rg = np.interp(zg, Z, R)
k = 4; Rs = np.convolve(np.pad(Rg, k, mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), mode='valid')
vol = np.sum(np.pi * Rs ** 2) * 0.0005
print('Guinness scaling: z x%.4f, r x%.4f; cavity depth %.1f mm, inner radius %.1f (foot) .. %.1f (widest) .. %.1f mm (rim); brim-full volume %.0f ml'
      % (sz, sr, zg[-1] * 1000, Rs[0] * 1000, Rs.max() * 1000, Rs[-1] * 1000, vol * 1e6))
out = {'source': 'dimensions.com Irish Imperial Pint Glass section (tools/fig12/irish-imperial-pint.svg), scaled to 160 mm x 85 mm',
       'scale_z': sz, 'scale_r': sr, 'dz': 0.0005, 'z0': 0.0, 'R': [round(float(r), 6) for r in Rs], 'volume_brim_m3': vol}
for hf in (0.110, 0.120, 0.125, 0.130):
    n = int(hf / 0.0005); print('stout filled to %.0f mm: %.0f ml' % (hf * 1000, np.sum(np.pi * Rs[:n] ** 2) * 0.0005 * 1e6))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'glass_profile.json'), 'w'))
print('wrote glass_profile.json with', len(Rs), 'radii')
js = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'public', 'scripts', 'guinness-glass.js')
open(js, 'w').write('/* Fig. 12: inner radius of the Guinness tulip pint, every 0.5 mm from the cavity floor (m). Written by\n'
    '   tools/fig12/glass_profile.py from the section of dimensions.com\u2019s Irish Imperial Pint Glass, scaled to 160 mm x 85 mm.\n'
    '   Do not edit. */\n(function (root) { var P = { dz: 0.0005, R: [' + ','.join('%.6f' % r for r in Rs) + '] };\n'
    '  if (typeof module === \'object\' && module.exports) module.exports = P; else root.GUINNESS_GLASS = P; })(typeof self !== \'undefined\' ? self : this);\n')
print('wrote public/scripts/guinness-glass.js')
