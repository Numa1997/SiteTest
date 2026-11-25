"""Fig. 13 card picture: the eye of the chaos map, public/images/sims/momentum-spirographs.webp, 800 x 500 px.

Reads the map the page shows (public/images/fig13/chaos-map-rods-P20.png, from chaos_map.py and map_png.py) and crops it to
|p1| <= 14.4, |p2| <= 9 kg m^2/s around the eye. Drawn over it, from the equations of the lecture note: the pupil's edge
K = 2 U2 = 9.8 J (green), the iris K = 2 U1 = 29.4 J (dashed) and K = 2 (U1 + U2) = 39.2 J (gold), and the two fold lines
p1 = (19 -+ 4 sqrt 21) p2 (dashed, the lashes). No text: the card carries the title.

Usage: python3 tools/fig13/eye_thumb.py
"""
import pathlib, math
import numpy as np
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[2]
W, H, SS = 800, 500, 3                      # output size; drawn 3x larger and reduced, for smooth lines
PW_MAP, PH_MAP = 20 * 16 / 9, 20.0           # the map's extent, kg m^2/s
VW, VH = 14.4, 9.0                           # half-extent of the crop, kg m^2/s (16:10)
A, B, C, U1, U2 = 4 / 3, 1 / 3, 1 / 2, 14.7, 4.9

src = Image.open(ROOT / 'public/images/fig13/chaos-map-rods-P20.png').convert('RGBA')
mw, mh = src.size
box = ((-VW / (2 * PW_MAP) + .5) * mw, (.5 - VH / (2 * PH_MAP)) * mh, (VW / (2 * PW_MAP) + .5) * mw, (.5 + VH / (2 * PH_MAP)) * mh)
crop = src.resize((W * SS, H * SS), Image.LANCZOS, box=box)
bg = Image.new('RGBA', crop.size, (20, 13, 16, 255))
img = Image.alpha_composite(bg, crop)
d = ImageDraw.Draw(img)
S = W * SS / (2 * VW)
X = lambda p1: W * SS / 2 + p1 * S
Y = lambda p2: H * SS / 2 - p2 * S
K = lambda p1, p2: (B * p1 * p1 - 2 * C * p1 * p2 + A * p2 * p2) / (2 * (A * B - C * C))


def ellipse_pts(ke, n=400):
    pts = []
    for k in range(n + 1):
        a = 2 * math.pi * k / n
        r = math.sqrt(ke / K(math.cos(a), math.sin(a)))
        pts.append((X(r * math.cos(a)), Y(r * math.sin(a))))
    return pts


def dashed(pts, fill, width, on, off):
    acc, draw_on = 0.0, True
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0); s = 0.0
        while s < L:
            step = min((on if draw_on else off) - acc, L - s)
            if draw_on:
                d.line([(x0 + (x1 - x0) * s / L, y0 + (y1 - y0) * s / L), (x0 + (x1 - x0) * (s + step) / L, y0 + (y1 - y0) * (s + step) / L)], fill=fill, width=width)
            s += step; acc += step
            if acc >= (on if draw_on else off) - 1e-9:
                acc = 0.0; draw_on = not draw_on


# the pupil, filled faintly
pupil = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(pupil).polygon(ellipse_pts(2 * U2), fill=(143, 227, 208, 22))
img = Image.alpha_composite(img, pupil); d = ImageDraw.Draw(img)
for k in (19 - 4 * math.sqrt(21), 19 + 4 * math.sqrt(21)):          # the lashes
    n = math.hypot(k, 1); L = 40
    dashed([(X(-L * k / n), Y(-L / n)), (X(L * k / n), Y(L / n))], (255, 246, 234, 105), 2 * SS, 9 * SS, 8 * SS)
d.line(ellipse_pts(2 * U2), fill=(143, 227, 208, 200), width=2 * SS)
dashed(ellipse_pts(2 * U1), (255, 210, 122, 140), 2 * SS, 7 * SS, 7 * SS)
d.line(ellipse_pts(2 * (U1 + U2)), fill=(255, 210, 122, 190), width=2 * SS)
out = img.resize((W, H), Image.LANCZOS).convert('RGB')
dest = ROOT / 'public/images/sims/momentum-spirographs.webp'
out.save(dest, 'WEBP', quality=88, method=6)
print('wrote', dest, out.size, dest.stat().st_size, 'bytes')
