"""Compose the four hardware figures with numbered balloons; the key goes in the HTML caption. Writes fig-*.webp."""
import json
from PIL import Image, ImageDraw, ImageFont
O = 'blender/out/'; FD = 'fonts/'
mono = lambda s: ImageFont.truetype(FD + 'ibm-plex-mono-500-latin.ttf', s)
ink = (28, 21, 24); wine = (122, 31, 43); grey = (110, 102, 98)

def load(n):
    im = Image.open(O + n + '.png').convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    return bg.convert('RGB'), json.load(open(O + n + '.json'))
def bbox(im, pad=20):
    g = im.convert('L').point(lambda v: 255 if v < 248 else 0); b = g.getbbox()
    return (max(0, b[0] - pad), max(0, b[1] - pad), min(im.width, b[2] + pad), min(im.height, b[3] + pad))

def place(name, crop=None, scale=1.0):
    im, pts = load(name); W0, H0 = im.size
    c = crop or bbox(im)
    im = im.crop(c); im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    P = {k: ((v[0] / 100 * W0 - c[0]) * scale, (v[1] / 100 * H0 - c[1]) * scale) for k, v in pts.items()}
    return im, P

def balloons(d, items, r=24, fs=29):
    """items: list of (n, (ax, ay), (bx, by)): anchor dot, leader, numbered circle"""
    for n, (ax, ay), (bx, by) in items:
        d.line((ax, ay, bx, by), fill=ink, width=3)
        d.ellipse((ax - 6, ay - 6, ax + 6, ay + 6), fill=wine)
    for n, (ax, ay), (bx, by) in items:
        d.ellipse((bx - r, by - r, bx + r, by + r), fill='white', outline=wine, width=3)
        d.text((bx, by + 1), str(n), font=mono(fs), fill=wine, anchor='mm')

def off(p, dx, dy): return (p[0] + dx, p[1] + dy)

# ---------- Figure 1: the machine ----------
im, P = place('rig', scale=1.25)
S = Image.new('RGB', (im.width + 160, im.height + 110), 'white'); S.paste(im, (80, 20)); d = ImageDraw.Draw(S)
Q = {k: (x + 80, y + 20) for k, (x, y) in P.items()}
seq = [('pivot', 120, 10), ('rod1', 90, 0), ('m1', 90, 0), ('rod2', 90, 0), ('m2', 100, -30), ('axle', -110, -20), ('strut', 100, 0),
       ('cart', -90, -110), ('magnet', 40, -100), ('rail', 0, 75)]
balloons(d, [(i + 1, Q[k], off(Q[k], dx * 1.3, dy * 1.3)) for i, (k, dx, dy) in enumerate(seq)], r=34, fs=40)
S.save(O + 'fig-machine.webp', quality=88); print('machine', S.size)

# ---------- Figure 2: the two pinned ends ----------
A, PA = place('ball-end', scale=1.0); B, PB = place('cart-end', scale=0.95)
h = max(A.height, B.height); gap = 230
S = Image.new('RGB', (A.width + gap + B.width + 40, h + 130), 'white'); d = ImageDraw.Draw(S)
ya = 60 + (h - A.height) // 2; yb = 60 + (h - B.height) // 2; xb = A.width + gap + 20
S.paste(A, (20, ya)); S.paste(B, (xb, yb))
d.text((24, 20), 'A', font=mono(32), fill=wine); d.text((62, 28), 'AT BALL 2', font=mono(19), fill=grey)
d.text((xb + 4, 20), 'B', font=mono(32), fill=wine); d.text((xb + 42, 28), 'AT THE CART', font=mono(19), fill=grey)
QA = {k: (x + 20, max(y, 30) + ya) for k, (x, y) in PA.items()}; QB = {k: (x + xb, y + yb) for k, (x, y) in PB.items()}
sa = [('rod2', 110, 30), ('ball', 120, -20), ('bore', 90, -95), ('axle', -40, -80), ('bush', -150, -60), ('cheek', -120, 60), ('bridge', 130, 20), ('boss', 120, 60), ('tube', 110, 0)]
sb = [('tube', 120, 0), ('shank', 120, 0), ('eye', -120, -10), ('bearing', 130, 0), ('pin', -40, -70), ('bore', 150, -40), ('clevis', 150, 30), ('screws', 60, -110), ('cart', -120, 40)]
balloons(d, [(i + 1, QA[k], off(QA[k], dx, dy)) for i, (k, dx, dy) in enumerate(sa)])
balloons(d, [(i + 1 + len(sa), QB[k], off(QB[k], dx, dy)) for i, (k, dx, dy) in enumerate(sb)])
# locator between the panels
cx = A.width + 20 + gap // 2; top = 120; bot = h - 40
bx, by = cx + 18, top + 40; hx, hy = cx - 22, bot - 80
d.line((bx - 30, by - 90, bx, by), fill=(60, 60, 60), width=6); d.ellipse((bx - 20, by - 20, bx + 20, by + 20), fill=(60, 12, 20))
d.line((bx, by, hx, hy), fill=(160, 160, 160), width=9)
d.rectangle((hx - 55, hy, hx + 55, hy + 32), fill=(228, 228, 228), outline=(120, 120, 120), width=2)
for wx in (hx - 34, hx + 34): d.ellipse((wx - 9, hy + 28, wx + 9, hy + 46), fill=(245, 245, 245), outline=(120, 120, 120), width=2)
d.line((cx - 95, hy + 48, cx + 95, hy + 48), fill=(90, 90, 90), width=4)
for (x, y, t, ox) in ((bx, by, 'A', 50), (hx, hy, 'B', 52)):
    d.line((x, y, x + ox - 20, y), fill=wine, width=2)
    d.ellipse((x + ox - 20, y - 20, x + ox + 20, y + 20), outline=wine, width=3, fill='white'); d.text((x + ox, y + 1), t, font=mono(22), fill=wine, anchor='mm')
S.save(O + 'fig-ends.webp', quality=88); print('ends', S.size)

# ---------- Figure 3: the strut cut open ----------
im, P = place('strut', scale=0.82)
S = Image.new('RGB', (im.width + 40, im.height + 190), 'white'); S.paste(im, (20, 85)); d = ImageDraw.Draw(S)
Q = {k: (x + 20, y + 85) for k, (x, y) in P.items()}
seq = [('eye1', 0, 90), ('plug', 0, -90), ('spring', 0, 90), ('collar', 0, -90), ('inner', 0, 90), ('outer', 0, -90), ('bush', 0, -90), ('iplug', 0, 90), ('fork', 0, 60), ('axle', 40, 60), ('ball', 0, -70)]
balloons(d, [(i + 1, Q[k], (Q[k][0] + dx, (85 - 46 if dy < 0 else 85 + im.height + 46))) for i, (k, dx, dy) in enumerate(seq)])
S.save(O + 'fig-strut.webp', quality=88); print('strut', S.size)

# ---------- Figure 4: magnet track and coil ----------
im, P = place('motor', scale=1.05)
S = Image.new('RGB', (im.width + 40, im.height + 60), 'white'); S.paste(im, (20, 10)); d = ImageDraw.Draw(S)
Q = {k: (x + 20, y + 10) for k, (x, y) in P.items()}
seq = [('cart', -90, -20), ('coil', -120, -40), ('B', 40, -110), ('magN', 150, 150), ('magS', -170, 120), ('channel', -40, 150), ('Ileft', -110, 60), ('Iright', 110, 70), ('F', 0, 60)]
balloons(d, [(i + 1, Q[k], off(Q[k], dx, dy)) for i, (k, dx, dy) in enumerate(seq)])
S.save(O + 'fig-motor.webp', quality=88); print('motor', S.size)
