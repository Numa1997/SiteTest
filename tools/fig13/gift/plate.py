"""A plate of the traced word: dark (gold ink on deep navy) and paper (black ink on aged paper), with a ruled frame.

    python3 tools/fig13/gift/plate.py TRACE.json OUT.png
"""
import sys, json
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.path import Path; from matplotlib.patches import PathPatch, Rectangle

d = json.load(open(sys.argv[1])); v, c = [], []
for q in d['contours']:
    q = np.array(q); v += list(q) + [q[0]]; c += [Path.MOVETO] + [Path.LINETO] * (len(q) - 1) + [Path.CLOSEPOLY]
word = Path(v, c); allp = np.array(v); x0, y0 = allp.min(0); x1, y1 = allp.max(0); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; ww, hh = x1 - x0, y1 - y0

def plate(ax, ground, ink, rule, glow=None):
    W = ww * 1.4; H = hh * 1.8
    ax.set_xlim(cx - W / 2, cx + W / 2); ax.set_ylim(cy + H / 2, cy - H / 2); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((cx - W / 2, cy - H / 2), W, H, fc=ground, ec='none', zorder=-5))
    for k, (m, lw) in enumerate(((0.0, 3.0), (0.035, 1.2))):
        ax.add_patch(Rectangle((cx - W / 2 + W * (0.03 + m), cy - H / 2 + H * (0.035 + m)), W * (0.94 - 2 * m), H * (0.93 - 2 * m), fc='none', ec=rule, lw=lw))
    if glow is not None:
        for w_, a_ in ((14, 0.05), (7, 0.08)): ax.add_patch(PathPatch(word, fc='none', ec=glow, lw=w_, alpha=a_))
    ax.add_patch(PathPatch(word, fc=ink, ec=ink, lw=0.6))

fig, ax = plt.subplots(1, 2, figsize=(16, 6.2), dpi=110); fig.patch.set_facecolor('#140d10')
plate(ax[0], '#0c1424', '#e3bd6e', '#b8924a', glow='#e3bd6e')
plate(ax[1], '#efe8d8', '#1c1518', '#9b7b3d')
fig.subplots_adjust(0, 0, 1, 1, 0.01); fig.savefig(sys.argv[2], facecolor=fig.get_facecolor())
