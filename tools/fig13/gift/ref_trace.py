"""Vector outlines of the ink in a photographed calligraphy plate (here: the reference Numa supplied, a Naskh/Thuluth رِيمْ),
so that the pen's own shapes can be re-coloured, composed and written by the phasor chain in reem2.html.

Steps: crop the word's box, upscale 4x (Lanczos), subtract the paper (a heavily blurred copy), threshold the difference, drop
specks, smooth, trace the boundary of the ink at sub-pixel accuracy (marching squares), simplify. Contours are written in the
crop's pixel units (y down) as lists of [x, y]; orientation follows the ink, so holes (the loop of the mim) run the other way.

    python3 tools/fig13/gift/ref_trace.py IMAGE.jpg OUT.json [x0 y0 x1 y1]     box as fractions of the screenshot width (923-wide view)
"""
import sys, json
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, label
from skimage.measure import find_contours, approximate_polygon

UP = 4
img = Image.open(sys.argv[1]).convert('RGB'); W, H = img.size; s = W / 923
x0, y0, x1, y1 = (float(v) for v in (sys.argv[3:7] if len(sys.argv) > 6 else (270, 1170, 690, 1370)))
crop = img.crop((int(x0 * s), int(y0 * s), int(x1 * s), int(y1 * s)))
crop = crop.resize((crop.width * UP, crop.height * UP), Image.LANCZOS)
g = np.asarray(crop.convert('L'), float)
paper = gaussian_filter(g, 60)                               # the paper's own brightness, slowly varying
diff = paper - g                                             # positive where darker than the paper: ink
from skimage.filters import apply_hysteresis_threshold
from scipy.ndimage import binary_closing, binary_opening, generate_binary_structure, iterate_structure
mask = apply_hysteresis_threshold(gaussian_filter(diff, 1.5), 20, 46)     # strong ink, plus the pale gold-flecked parts joined to it
mask = binary_closing(mask, iterate_structure(generate_binary_structure(2, 1), 5))   # close the gaps in the gold-flecked stroke
mask = binary_opening(mask, generate_binary_structure(2, 1))
mask[:, 1700:] = False; mask[:, :120] = False                          # the plate's frame lines (columns 0-69 and 1779-) are not part of the word
lab, n = label(mask); sizes = np.bincount(lab.ravel())
keep = np.isin(lab, [i for i in range(1, n + 1) if sizes[i] > 1500])      # drop paper grain
DROP = (1238, 645)   # crop pixels at 4x                                                       # the third dot of the photographed plate (wrong for ya): removed
lab2, n2 = label(keep)
for i in range(1, n2 + 1):
    yy, xx = np.nonzero(lab2 == i)
    if np.hypot(xx.mean() - DROP[0], yy.mean() - DROP[1]) < 90 and len(xx) < 9000: keep[lab2 == i] = False
sm = gaussian_filter(keep.astype(float), 2.0)
cs = []
for c in find_contours(sm, 0.5):
    c = approximate_polygon(c, 0.8)[:, ::-1]                 # (x, y), simplified within 0.8 px of the upscaled image
    area = 0.5 * abs(np.dot(c[:, 0], np.roll(c[:, 1], 1)) - np.dot(c[:, 1], np.roll(c[:, 0], 1)))
    if len(c) > 5 and area > 700: cs.append(c.round(2).tolist())   # specks (paper grain, flecks of gold) are not ink
json.dump(dict(width=crop.width, height=crop.height, contours=cs), open(sys.argv[2], 'w'), separators=(',', ':'))
print('crop %dx%d, %d contours, %d points' % (crop.width, crop.height, len(cs), sum(len(c) for c in cs)))
