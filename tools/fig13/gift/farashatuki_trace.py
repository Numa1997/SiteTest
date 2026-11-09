"""Vector outlines of فراشتك from the Diwani plate Numa chose (9 November 2026: "Diwani, upper right most", panel 03 of a
nine-style sheet of the word, a screenshot of an image made by an image generator), traced like the رِيمْ plate (ref_trace.py).

The plate is gold ink on a dark board, so the ink is where the image is brighter than the board. Steps: crop panel 03,
upscale 4x (Lanczos), subtract the board (a heavily blurred copy), hysteresis threshold, close small gaps, keep only the
word's box (the panel's frame, its two labels "03. Diwani" and "ديواني" and the faint guide lines are not part of the word),
drop specks, smooth, trace the ink's boundary at sub-pixel accuracy, simplify. Output in the crop's pixels, y down.

    python3 tools/fig13/gift/farashatuki_trace.py IMAGE.jpg OUT.json [PREVIEW.png]
"""
import sys, json
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, label, binary_closing, binary_opening, generate_binary_structure, iterate_structure
from skimage.filters import apply_hysteresis_threshold
from skimage.measure import find_contours, approximate_polygon

UP = 4
BOX = (605, 775, 862, 918)          # panel 03 in the 923-px-wide view of the screenshot
WORD = (180, 100, 1012, 578)        # the word inside the 4x crop: x0, y0, x1, y1
LABELS = ((0, 0, 495, 150), (880, 0, 1204, 152))   # "03. Diwani" (left) and "ديواني" (right), 4x crop pixels

img = Image.open(sys.argv[1]).convert('RGB'); s = img.size[0] / 923
crop = img.crop(tuple(int(v * s) for v in BOX))
crop = crop.resize((crop.width * UP, crop.height * UP), Image.LANCZOS)
g = np.asarray(crop.convert('L'), float)
diff = g - gaussian_filter(g, 60)                       # brighter than the board: gold ink
mask = apply_hysteresis_threshold(gaussian_filter(diff, 1.5), 30, 60)
mask = binary_closing(mask, iterate_structure(generate_binary_structure(2, 1), 3))
mask = binary_opening(mask, generate_binary_structure(2, 1))
keep = np.zeros_like(mask); x0, y0, x1, y1 = WORD; keep[y0:y1, x0:x1] = True
for a, b, c, d in LABELS: keep[b:d, a:c] = False
mask &= keep
lab, n = label(mask); sizes = np.bincount(lab.ravel())
mask = np.isin(lab, [i for i in range(1, n + 1) if sizes[i] > 250])
sm = gaussian_filter(mask.astype(float), 1.5)
cs = []
for c in find_contours(sm, 0.5):
    c = approximate_polygon(c, 0.6)[:, ::-1]
    area = 0.5 * abs(np.dot(c[:, 0], np.roll(c[:, 1], 1)) - np.dot(c[:, 1], np.roll(c[:, 0], 1)))
    if len(c) > 5 and area > 200: cs.append(c.round(2).tolist())
json.dump(dict(width=crop.width, height=crop.height, contours=cs), open(sys.argv[2], 'w'), separators=(',', ':'))
print('crop %dx%d, %d contours, %d points' % (crop.width, crop.height, len(cs), sum(len(c) for c in cs)))
if len(sys.argv) > 3:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib.path import Path; from matplotlib.patches import PathPatch
    v, cd = [], []
    for q in cs: v += q + [q[0]]; cd += [Path.MOVETO] + [Path.LINETO] * (len(q) - 1) + [Path.CLOSEPOLY]
    fig, ax = plt.subplots(1, 2, figsize=(16, 5), dpi=90); fig.patch.set_facecolor('#f5f1ea')
    ax[0].imshow(np.asarray(crop)); ax[0].axis('off')
    ax[1].add_patch(PathPatch(Path(v, cd), fc='#7a1f2b', ec='none', fill=True)); ax[1].set_xlim(0, crop.width); ax[1].set_ylim(crop.height, 0)
    ax[1].set_aspect('equal'); ax[1].axis('off')
    fig.tight_layout(); fig.savefig(sys.argv[3], facecolor=fig.get_facecolor())
