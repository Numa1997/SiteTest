"""Fig. 14 note: writes the three inline SVG figures (house chart style) from the stored runs and the page's formulas."""
import json, numpy as np, sys
sys.path.insert(0, '/home/user/SiteTest/notes/fig14')
def Tpage(E_, V, a_):   # the page's T1D, copied from the page (and from derive.py)
    if V == 0: return 1
    if abs(E_ - V) < 1e-9: return 1 / (1 + a_ * a_ * V / 2)
    if E_ < V: k_ = np.sqrt(2 * (V - E_)); s_ = np.sinh(k_ * a_); return 1 / (1 + V * V * s_ * s_ / (4 * E_ * (V - E_)))
    k2 = np.sqrt(2 * (E_ - V)); s2 = np.sin(k2 * a_); return 1 / (1 + V * V * s2 * s2 / (4 * E_ * (E_ - V)))
F = json.load(open('/home/user/SiteTest/notes/fig14/figdata.json')); C = json.load(open('/home/user/SiteTest/notes/fig14/classical.json'))
def f(v): return ('%.1f' % v).rstrip('0').rstrip('.') if abs(v - round(v)) > 1e-9 else str(int(round(v)))
# ---------- Figure 1: the geometry, to scale ----------
s = 5.3125; X0, Y0 = 40, 26; cx, cy = X0 + 32 * s, Y0 + 32 * s
P = lambda x, y: (cx + x * s, cy - y * s)
o = ['<svg viewBox="0 0 720 392" role="img" aria-label="The computational box seen in the plane z = 0: the sphere of radius R at the centre, the starting packet at x = −14, the three slabs behind, inside and ahead, and the absorbing border." xmlns="http://www.w3.org/2000/svg">',
     '<rect x="0" y="0" width="720" height="392" fill="#fff"/>']
b = 6 * s
o.append(f'<path d="M{X0} {Y0} h{64*s:.1f} v{64*s:.1f} h{-64*s:.1f} Z M{X0+b:.1f} {Y0+b:.1f} v{(64-12)*s:.1f} h{(64-12)*s:.1f} v{-(64-12)*s:.1f} Z" fill="#efe6d8" fill-rule="evenodd"/>')
o.append(f'<rect x="{X0}" y="{Y0}" width="{64*s:.1f}" height="{64*s:.1f}" fill="none" stroke="#8b8079" stroke-width="1.2"/>')
for xs in (-4, 4):
    x, _ = P(xs, 0); o.append(f'<line x1="{x:.1f}" y1="{Y0}" x2="{x:.1f}" y2="{Y0+64*s:.1f}" stroke="#8b8079" stroke-width="1" stroke-dasharray="5 4"/>')
for r, op in ((2 * 3, 0.10), (1.5 * 3, 0.16), (3, 0.26), (1.5, 0.40)):
    x, y = P(-14, 0); o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*s:.1f}" fill="#7a1f2b" fill-opacity="{op}"/>')
x, y = P(0, 0); o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4*s:.1f}" fill="#d9c4c0" stroke="#1c1518" stroke-width="1.3" stroke-dasharray="6 5"/>')
x1, y1 = P(-14, 0); x2, _ = P(-14 + 9, 0)
o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y1:.1f}" stroke="#1c1518" stroke-width="1.6"/><path d="M{x2-1:.1f} {y1-5:.1f} L{x2+9:.1f} {y1:.1f} L{x2-1:.1f} {y1+5:.1f} Z" fill="#1c1518"/>')
o.append(f'<text class="m" x="{x2-14:.1f}" y="{y1-9:.1f}">k<tspan class="mu" font-size="12" dy="4">0</tspan></text>')
xl, _ = P(-14, 0); o.append(f'<text class="lbl" x="{xl:.1f}" y="{P(0,-9)[1]:.1f}" text-anchor="middle">packet at x₀ = −14</text>')
o.append(f'<line x1="{P(0,0)[0]:.1f}" y1="{P(0,0)[1]:.1f}" x2="{P(4*0.7071,4*0.7071)[0]:.1f}" y2="{P(4*0.7071,4*0.7071)[1]:.1f}" stroke="#1c1518" stroke-width="1"/>')
o.append(f'<text class="m" x="{P(1.2,3.6)[0]:.1f}" y="{P(1.2,3.6)[1]:.1f}">R</text>')
for xs, t in ((-18, 'behind'), (0, 'inside'), (18, 'ahead')):
    o.append(f'<text class="lbl" x="{P(xs,0)[0]:.1f}" y="{Y0-7:.1f}" text-anchor="middle">{t}</text>')
o.append(f'<text class="lbl" x="{P(0,0)[0]:.1f}" y="{Y0+64*s+16:.1f}" text-anchor="middle">x = −R and x = +R (dashed)</text>')
xa, ya = P(-29, -29)
o.append(f'<text class="lbl" x="{X0+4}" y="{Y0+12}">absorbing border, 6 a</text>')
# scale bar 10 a
xb, yb = P(14, -27); o.append(f'<line x1="{xb:.1f}" y1="{yb:.1f}" x2="{xb+10*s:.1f}" y2="{yb:.1f}" stroke="#1c1518" stroke-width="1.6"/><text class="tick" x="{xb+5*s:.1f}" y="{yb-6:.1f}" text-anchor="middle">10 a</text>')
# axes arrows
ax, ay = X0 + 64 * s + 14, cy
o.append(f'<text class="m" x="{X0+64*s+8:.1f}" y="{cy+5:.1f}">x</text><text class="m" x="{X0-16:.1f}" y="{Y0+14:.1f}">y</text>')
# side text
tx = 440
lines = [('m', 'Box: side 64 a, periodic'), ('lbl', '128³ points, Δx = 0.5 a'), ('lbl', ''), ('lbl', 'Sphere: radius R, V = V₀ inside'), ('lbl', 'Packet: width σ₀ = 3 a,'), ('lbl', 'centre x₀ = −14 a, wave number k₀'), ('lbl', ''),
         ('lbl', 'Slabs counted from the whole 3D ψ:'), ('lbl', 'behind  x < −R'), ('lbl', 'inside  −R ≤ x ≤ R'), ('lbl', 'ahead   x > R'), ('lbl', ''), ('lbl', 'Shaded frame: the outer 12 cells'), ('lbl', 'of each face, where the mask'), ('lbl', 'removes the wave')]
for i, (cl, t) in enumerate(lines):
    if t: o.append(f'<text class="lbl" x="{tx}" y="{46+i*20}">{t}</text>')
o.append('</svg>')
open('/home/user/SiteTest/notes/fig14/fig1.svg', 'w').write('\n'.join(o))
# ---------- chart helper ----------
def chart(W, H, L, R_, T, B, xr, yr, xt, yt, xlab, ylab, series, cid):
    pw, ph = W - L - R_, H - T - B
    X = lambda v: L + pw * (v - xr[0]) / (xr[1] - xr[0]); Y = lambda v: T + ph * (1 - (v - yr[0]) / (yr[1] - yr[0]))
    o = [f'<defs><clipPath id="{cid}"><rect x="{L}" y="{T}" width="{pw}" height="{ph}"/></clipPath></defs>', f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>']
    for v in yt:
        o.append(f'<line x1="{L}" x2="{L+pw}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#eee6d9" stroke-width="1"/><text class="tick" x="{L-8}" y="{Y(v)+4:.1f}" text-anchor="end">{v:.2f}</text>')
    for v in xt:
        o.append(f'<line x1="{X(v):.1f}" x2="{X(v):.1f}" y1="{T+ph}" y2="{T+ph+5}" stroke="#8b8079"/><text class="tick" x="{X(v):.1f}" y="{T+ph+19}" text-anchor="middle">{f(v)}</text>')
    o.append(f'<line x1="{L}" x2="{L+pw}" y1="{T+ph}" y2="{T+ph}" stroke="#8b8079"/><line x1="{L}" x2="{L}" y1="{T}" y2="{T+ph}" stroke="#8b8079"/>')
    o.append(f'<text class="lbl" x="{L+pw}" y="{T+ph+38}" text-anchor="end">{xlab}</text><text class="lbl" x="{L-8}" y="{T-14}">{ylab}</text>')
    for pts, col, dash, w, mk in series:
        d = ' '.join(('M' if i == 0 else 'L') + f'{X(a):.1f} {Y(b):.1f}' for i, (a, b) in enumerate(pts))
        o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else '') + f' clip-path="url(#{cid})"/>')
        if mk:
            for a, b in pts:
                o.append(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="3.2" fill="{col if mk == "f" else "#fff"}" stroke="{col}" stroke-width="1.4"/>')
    return o, X, Y
# ---------- Figure 2: the default run's four probabilities ----------
c = np.array(F['curves_default']); t = c[:, 0]
ser = [(list(zip(t, c[:, 2])), '#1c1518', None, 2, None), (list(zip(t, c[:, 1] - c[:, 2] - c[:, 3])), '#b07a6a', '6 4', 2, None),
       (list(zip(t, c[:, 3])), '#7a1f2b', None, 2, None), (list(zip(t, 1 - c[:, 1])), '#8b8079', '2 3', 2, None)]
W, H = 720, 330
body, X, Y = chart(W, H, 64, 22, 36, 52, (0, 13.16), (0, 1), [0, 2, 4, 6, 8, 10, 12], [0, 0.25, 0.5, 0.75, 1.0], 'time t (in m a²/ħ)', 'probability', ser, 'clip14b')
lg = [('behind', '#1c1518', None), ('inside', '#b07a6a', '6 4'), ('ahead', '#7a1f2b', None), ('lost', '#8b8079', '2 3')]
for i, (n, col, dash) in enumerate(lg):
    x0 = 470 + (i % 2) * 110; y0 = 120 + (i // 2) * 22
    body.append(f'<line x1="{x0}" x2="{x0+24}" y1="{y0}" y2="{y0}" stroke="{col}" stroke-width="2"' + (f' stroke-dasharray="{dash}"' if dash else '') + f'/><text class="lbl" x="{x0+30}" y="{y0+4}">{n}</text>')
open('/home/user/SiteTest/notes/fig14/fig2.svg', 'w').write('\n'.join(['<svg viewBox="0 0 720 330" role="img" aria-label="Probability behind, inside and ahead of the sphere and lost at the border against time, for E = 2.5, V0 = 3, R = 4, from the stored run." xmlns="http://www.w3.org/2000/svg">'] + body + ['</svg>']))
# ---------- Figure 3: probability ahead at the end against V0 (E = 2.5) ----------
cols = {2.0: '#c99a8f', 4.0: '#7a1f2b', 6.0: '#1c1518'}
ser = []
vv = np.linspace(0, 8, 321)
ser.append((list(zip(vv, [Tpage(2.5, v, 8.0) for v in vv])), '#8b8079', '2 3', 1.4, None))
for R in (2.0, 4.0, 6.0):
    q = F['ahead_vs_V0'][str(R)]; ser.append(([(a[0], a[1]) for a in q], cols[R], None, 2, 'f'))
    cl = [(v, C[f'2.5_{float(v)}_{int(R)}']['ahead']) for v in [a[0] for a in q]]
    ser.append((cl, cols[R], '5 4', 1.3, 'o'))
body, X, Y = chart(720, 350, 64, 22, 36, 52, (0, 8), (0, 1), [0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 0.25, 0.5, 0.75, 1.0], 'barrier height V₀ (E = 2.5)', 'probability ahead at the end of the run', ser, 'clip14c')
xE = X(2.5); body.append(f'<line x1="{xE:.1f}" x2="{xE:.1f}" y1="36" y2="{350-52}" stroke="#8b8079" stroke-width="1" stroke-dasharray="1 4"/><text class="tick" x="{xE+5:.1f}" y="{350-60}">V₀ = E</text>')
lg = [('R = 2', '#c99a8f'), ('R = 4', '#7a1f2b'), ('R = 6', '#1c1518')]
for i, (n, col) in enumerate(lg):
    x0 = 380 + i * 110; y0 = 182; body.append(f'<circle cx="{x0}" cy="{y0}" r="3.2" fill="{col}" stroke="{col}"/><text class="lbl" x="{x0+12}" y="{y0+4}">{n}</text>')
body.append(f'<line x1="368" x2="392" y1="160" y2="160" stroke="#1c1518" stroke-width="2"/><circle cx="380" cy="160" r="3.2" fill="#1c1518"/><text class="lbl" x="398" y="164">quantum (stored runs)</text>')
body.append(f'<line x1="590" x2="614" y1="160" y2="160" stroke="#1c1518" stroke-width="1.3" stroke-dasharray="5 4"/><circle cx="602" cy="160" r="3.2" fill="#fff" stroke="#1c1518" stroke-width="1.4"/><text class="lbl" x="620" y="164">classical</text>')
body.append(f'<line x1="368" x2="392" y1="204" y2="204" stroke="#8b8079" stroke-width="1.4" stroke-dasharray="2 3"/><text class="lbl" x="398" y="208">1D slab of thickness 2R = 8</text>')
open('/home/user/SiteTest/notes/fig14/fig3.svg', 'w').write('\n'.join(['<svg viewBox="0 0 720 350" role="img" aria-label="Probability ahead of the sphere at the end of the run against the barrier height, for E = 2.5 and R = 2, 4, 6: the stored quantum runs, a classical ensemble, and the 1D slab formula." xmlns="http://www.w3.org/2000/svg">'] + body + ['</svg>']))
print('written')
