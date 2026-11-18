"""Background ornaments of the Lucretius page: three vertically tiling SVGs of fractal curves in the house wine.

Run from the repository root: python3 notes/lucretius/make_bg.py
Writes public/images/lucretius/bg-a.svg, bg-b.svg, bg-c.svg (one left margin strip each; the page mirrors it for the right).
Every tile is H px tall and joins its own top and bottom seamlessly, so CSS can repeat it down the whole page.

  a  branches: a slow stem wandering down the strip, and from it recursive curved branches (depth 5, each branch 0.68 of
     its parent, turned by 22 to 38 degrees), like the roots and veins that run through the site's mark.
  b  Weierstrass lines: seven lines down the strip, each x(y) = x0 + sum_k a^k cos(2 pi b^k y / H + phase), a = 0.55, b = 2,
     eight octaves. Every term has a whole number of periods per tile, so the line is periodic; with a b > 1 the curve is
     nowhere smooth at the finest scales, the classic fractal of Weierstrass (1872), truncated at 2^7 waves per tile.
  c  tendrils: a sine vine with curls; every curl is a logarithmic spiral that sprouts two smaller curls, three levels deep.
"""
import math, random, os

H = 1600          # tile height, px
W = 360           # strip width, px
WINE = '#7a1f2b'
OUT = 'public/images/lucretius'


def svg(body, opacity):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<g fill="none" stroke="{WINE}" stroke-linecap="round" stroke-opacity="{opacity}">{body}</g></svg>\n')


def path(pts, w):
    d = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
    return f'<path d="{d}" stroke-width="{w:.2f}"/>'


# ---------- a: branches ----------
def make_a():
    rnd = random.Random(146)
    stem = lambda y: 120 + 46 * math.sin(2 * math.pi * y / H) + 18 * math.sin(6 * math.pi * y / H + 1.1)
    out = [path([(stem(y), y) for y in range(0, H + 1, 4)], 1.4)]

    def branch(x, y, ang, L, depth, w):
        if depth == 0 or L < 7:
            return
        bend = rnd.uniform(-.35, .35)
        x2, y2 = x + L * math.cos(ang), y + L * math.sin(ang)
        cx, cy = x + L * .5 * math.cos(ang + bend), y + L * .5 * math.sin(ang + bend)
        if not (4 < x2 < W - 4 and 30 < y2 < H - 30):
            return
        out.append(f'<path d="M{x:.1f} {y:.1f} Q{cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}" stroke-width="{w:.2f}"/>')
        for s in (-1, 1):
            if rnd.random() < .86:
                branch(x2, y2, ang + s * math.radians(rnd.uniform(22, 38)), L * .68, depth - 1, w * .74)
    for k in range(9):
        y = 90 + k * (H - 180) / 8 + rnd.uniform(-30, 30)
        side = 1 if k % 2 else -1
        ang = math.pi / 2 + side * math.radians(rnd.uniform(50, 70))
        branch(stem(y), y, ang, rnd.uniform(70, 95), 5, 1.1)
    return svg(''.join(out), .34)


# ---------- b: Weierstrass lines ----------
def make_b():
    rnd = random.Random(169)
    out = []
    for i in range(7):
        x0 = 40 + i * 42
        ph = [rnd.uniform(0, 2 * math.pi) for _ in range(8)]
        amp = 22 * (1 - .07 * i)
        pts = []
        for j in range(0, H + 1, 2):
            y = j
            x = x0 + amp * sum(.55 ** k * math.cos(2 * math.pi * 2 ** k * y / H + ph[k]) for k in range(8))
            pts.append((x, y))
        out.append(path(pts, 1.25 - .12 * i))
    return svg(''.join(out), .3)


# ---------- c: tendrils ----------
def make_c():
    rnd = random.Random(205)
    vine = lambda y: 110 + 60 * math.sin(4 * math.pi * y / H)
    out = [path([(vine(y), y) for y in range(0, H + 1, 4)], 1.3)]

    def curl(x, y, ang, r, turn, depth, w):
        pts, a, rr = [], 0.0, r
        while a < 2.6 * math.pi and rr > 1.2:
            pts.append((x + rr * math.cos(ang + turn * a) - r * math.cos(ang), y + rr * math.sin(ang + turn * a) - r * math.sin(ang)))
            a += .08; rr = r * math.exp(-.28 * a)
        if all(4 < px < W - 4 and 20 < py < H - 20 for px, py in pts):
            out.append(path(pts, w))
            if depth > 1:
                for frac in (.25, .55):
                    px, py = pts[int(len(pts) * frac)]
                    curl(px, py, ang + turn * 2 * math.pi * frac + math.pi / 2, r * .45, -turn, depth - 1, w * .75)
    for k in range(10):
        y = 80 + k * (H - 160) / 9
        side = 1 if k % 2 else -1
        curl(vine(y) + side * 4, y, 0 if side > 0 else math.pi, rnd.uniform(34, 46), side, 3, 1.0)
    return svg(''.join(out), .32)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, f in (('a', make_a), ('b', make_b), ('c', make_c)):
        s = f()
        open(f'{OUT}/bg-{name}.svg', 'w').write(s)
        print(name, len(s), 'bytes')


# ---------- d: currents and atoms (the default since 18 November 2026) ----------
# A full-width tile (WD x H). Sixty-six lines run down the page in six braided currents. Each line is
#   x(y) = X_c(y) + spread * u + sum_k 0.5^k A cos(2 pi m_k y / H + phase)
# with whole numbers m_k, so every line closes on itself from tile to tile; X_c(y), the current's own course, wanders
# the same way. Along the lines sit the "atoms": dots of random size, mostly small, a few large and solid,
# falling with the currents (the page moves this layer down slowly). Lucretius' atoms falling through the void and swerving.
WD = 2400


def fbm(y, ph, amp, ms):
    return sum(amp * .5 ** k * math.cos(2 * math.pi * m * y / H + ph[k]) for k, m in enumerate(ms))


def make_d():
    rnd = random.Random(1916)
    lines, atoms = [], []
    centres = [150, 420, 760, 1640, 1980, 2250]
    for ci, cx in enumerate(centres):
        cph = [rnd.uniform(0, 6.3) for _ in range(4)]
        n = 11
        for j in range(n):
            u = (j - (n - 1) / 2) / ((n - 1) / 2)
            ph = [rnd.uniform(0, 6.3) for _ in range(6)]
            width = rnd.uniform(.5, 1.7) * (1.3 if abs(u) < .35 else 1)
            pts = []
            for y in range(0, H + 1, 5):
                spread = 70 + 50 * math.sin(2 * math.pi * y / H * (ci % 3 + 1) + cph[3])
                x = cx + fbm(y, cph, 120, (1, 2, 3)) + spread * u + fbm(y, ph, 26, (2, 4, 7, 11, 17, 29))
                pts.append((x, y))
            lines.append(path(pts, width))
            for _ in range(rnd.randint(9, 16)):
                x, y = pts[rnd.randrange(len(pts))]
                r = rnd.choice((.9, 1.1, 1.3, 1.6, 2, 2.6, 3.4)) if rnd.random() > .06 else rnd.uniform(4.5, 7)
                solid = r > 3 or rnd.random() < .5
                atoms.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"' + (' fill="#7a1f2b" stroke="none"/>' if solid else ' stroke-width=".8"/>'))
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{WD}" height="{H}" viewBox="0 0 {WD} {H}">'
    tail = '</svg>\n'
    a = head + f'<g fill="none" stroke="{WINE}" stroke-linecap="round" stroke-opacity=".42">' + ''.join(lines) + '</g>' + tail
    b = head + f'<g fill="none" stroke="{WINE}" fill-opacity=".7" stroke-opacity=".7">' + ''.join(atoms) + '</g>' + tail
    return a, b


if __name__ == '__main__':
    a, b = make_d()
    open(f'{OUT}/bg-d-lines.svg', 'w').write(a)
    open(f'{OUT}/bg-d-atoms.svg', 'w').write(b)
    print('d', len(a), len(b), 'bytes')
