"""SVG figures of the Fig. 12 lecture note, in the house chart style (white plate, IBM Plex Mono ticks, ink and wine),
drawn from the mode data, geom.py, notes/fig12/numbers.json and the controller reference. Writes notes/fig12/figs/*.svg.
    python3 tools/fig12/note_figs.py [slosh-modes.js]"""
import re, json, math, os, sys, numpy as np
sys.path.insert(0, 'tools/fig12')
import geom as G, plant, controller3 as C
MPATH = sys.argv[1] if len(sys.argv) > 1 else 'public/scripts/slosh-modes.js'
D_ = C.load_modes(MPATH); N = json.load(open('notes/fig12/numbers.json')); GL = D_['glass']
INK, WINE, ROSE, RULE, MUTED, STOUT, HEAD, LIGHT = '#1c1518', '#7a1f2b', '#e2a2aa', '#cdc1ae', '#8b8079', '#2b1210', '#efe2c6', '#f0ebe3'
MONO = "font-family=\"IBM Plex Mono, monospace\""
def svg(w, h, body, label): return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/>{body}</svg>'
def sub(s):   # a_b -> a<tspan sub>b</tspan> for the labels: one letter or a short group after the underscore
    return re.sub(r'([A-Za-zψβ])_([A-Za-z0-9]+)', lambda m: f'{m.group(1)}<tspan baseline-shift="sub" font-size="7">{m.group(2)}</tspan>', s)
def text(x, y, s, size=11, anchor='start', fill=INK, extra=''): return f'<text x="{x:.1f}" y="{y:.1f}" {MONO} font-size="{size}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
def path(pts, **kw): return '<path d="M' + ' L'.join(f'{p[0]:.1f},{p[1]:.1f}' for p in pts) + ('Z' if kw.pop('close', False) else '') + '" ' + ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items()) + '/>'
os.makedirs('notes/fig12/figs', exist_ok=True)

# ---- Figure 1: the glass to scale, and its cross-sections ----
W, H = 720, 440; sc = 2.4; cx = 170; by = 410
X = lambda r: cx + r * sc; Y = lambda zz: by - zz * sc
z = np.arange(0, G.H + 1e-9, 1.0); Ro = G.R0(z); Ri = G.R_inner(z, np.pi / 2); Rif = G.R_inner(z, 0.0)
b = []
for sd in (-1, 1):
    m = z >= G.Z_F
    pts = [(X(sd * r), Y(q)) for r, q in zip(Ro, z)] + [(X(sd * r), Y(q)) for r, q in zip(Ri[m][::-1], z[m][::-1])] + [(X(0), Y(G.Z_F)), (X(0), Y(0))]
    b.append(path(pts, close=True, fill='#e6eff1', stroke=INK, stroke_width=1.2))
zs = N['zs_mm']; m = (z >= G.Z_F) & (z <= zs)
b.append(path([(X(-r), Y(q)) for r, q in zip(Ri[m], z[m])][::-1] + [(X(r), Y(q)) for r, q in zip(Ri[m], z[m])], close=True, fill=STOUT))
hz = zs + 18; mh = (z >= zs) & (z <= hz)
b.append(path([(X(-r), Y(q)) for r, q in zip(Ri[mh], z[mh])][::-1] + [(X(r), Y(q)) for r, q in zip(Ri[mh], z[mh])], close=True, fill=HEAD, stroke='#b08a50', stroke_width=0.8))
mp = (z >= 10) & (z <= 105)
b.append(path([(X(-r), Y(q)) for r, q in zip(Rif[mp], z[mp])], fill='none', stroke=WINE, stroke_width=0.9, stroke_dasharray='3 2'))
b.append(path([(X(r), Y(q)) for r, q in zip(Rif[mp], z[mp])], fill='none', stroke=WINE, stroke_width=0.9, stroke_dasharray='3 2'))
def hline(zz, lab, col=INK, dash='4 3'):
    r = float(np.interp(zz, z, Ro)); return f'<line x1="{X(-r)-6:.1f}" y1="{Y(zz):.1f}" x2="{X(r)+40:.1f}" y2="{Y(zz):.1f}" stroke="{col}" stroke-dasharray="{dash}" stroke-width="1"/>' + text(X(r) + 46, Y(zz) + 4, lab, 10, 'start', col)
b.append(hline(160, 'rim, 160 mm; 80.7 mm across', WINE, 'none').replace(f'y="{Y(160)+4:.1f}"', f'y="{Y(160)-4:.1f}"'))
b.append(hline(N['glass']['z_568'], f"568 mL, one pint, at {N['glass']['z_568']:.1f} mm", MUTED).replace(f'y="{Y(N["glass"]["z_568"])+4:.1f}"', f'y="{Y(N["glass"]["z_568"])+12:.1f}"'))
b.append(hline(zs, f'500 mL: Z = {zs:.1f} mm, R = {N["a_mm"]:.1f} mm', INK))
b.append(hline(N['glass']['z_widest'], f"widest, {N['glass']['D_max']:.1f} mm across", WINE, '2 2'))
b.append(hline(N['glass']['z_waist'], f"waist, {N['glass']['D_waist']:.1f} mm across", MUTED, '2 2'))
b.append(hline(G.Z_F, 'floor of the cavity, 8 mm of glass below', MUTED))
b.append(text(X(-Ro[int(60)]) - 8, Y(60) + 4, 'panel', 9, 'end', WINE))
for t in range(0, 161, 40): b.append(f'<line x1="{cx-118}" y1="{Y(t):.1f}" x2="{cx-112}" y2="{Y(t):.1f}" stroke="{MUTED}"/>' + text(cx - 122, Y(t) + 4, str(t), 10, 'end', MUTED))
b.append(text(cx - 146, Y(80), 'Z, mm', 10, 'middle', MUTED, f'transform="rotate(-90 {cx-146} {Y(80)})"'))
# cross-sections at the right
sx, sy, ssc = 560, 300, 1.55
th = np.linspace(-np.pi, np.pi, 361)
for zz, col, lab in ((50, WINE, '50 mm'), (70, INK, '70 mm'), (90, MUTED, '90 mm')):
    r = G.R_inner(zz, th) * ssc; b.append(path([(sx + rr * math.cos(t), sy - rr * math.sin(t)) for rr, t in zip(r, th)], close=True, fill='none', stroke=col, stroke_width=1.1))
    b.append(f'<line x1="{sx+66}" y1="{sy-52+13*[50, 70, 90].index(zz):.1f}" x2="{sx+78}" y2="{sy-52+13*[50, 70, 90].index(zz):.1f}" stroke="{col}" stroke-width="1.1"/>' + text(sx + 82, sy - 49 + 13 * [50, 70, 90].index(zz), f'Z = {lab}', 9, 'start', col))
b.append(text(sx, sy + 78, 'cavity from above, two panels', 10, 'middle', MUTED)); b.append(text(sx, sy + 92, 'front', 9, 'middle', MUTED)); b.append(f'<line x1="{sx}" y1="{sy+60}" x2="{sx}" y2="{sy+68}" stroke="{MUTED}"/>')
b.append(text(12, by + 24, f'outline from the dimensioned drawing, scaled to 160 x 85 mm; wall 2.0 mm; panels {G.A_PANEL:.0f} mm deep (estimated)', 10, 'start', MUTED))
open('notes/fig12/figs/profile.svg', 'w').write(svg(W, H + 10, ''.join(b), 'The profile of the Guinness glass from its drawing: outer and inner wall, the sculpted panel, 500 mL of stout under 18 mm of head, the pint line and the rim; and three cross-sections of the cavity showing the two panels.'))

# ---- Figure 2: f11 against fill ----
W, H = 720, 330; L, R, T, B = 70, 30, 20, 50
fv = np.array(N['f_vs_V']); V = fv[:, 0]
ymin, ymax = 3.0, 3.6
xx = lambda v: L + (W - L - R) * (v - 300) / (580 - 300); yy = lambda f: T + (H - T - B) * (1 - (f - ymin) / (ymax - ymin))
b = [f'<rect x="{L}" y="{T}" width="{W-L-R}" height="{H-T-B}" fill="none" stroke="{RULE}"/>']
for f in np.arange(3.0, 3.61, 0.1): b.append(f'<line x1="{L}" y1="{yy(f):.1f}" x2="{W-R}" y2="{yy(f):.1f}" stroke="{LIGHT}"/>' + text(L - 6, yy(f) + 4, f'{f:.1f}', 10, 'end', MUTED))
for v in range(300, 581, 40): b.append(text(xx(v), H - B + 16, str(v), 10, 'middle', MUTED))
b.append(text((L + W - R) / 2, H - 6, 'stout, mL', 10, 'middle', MUTED)); b.append(text(16, (T + H - B) / 2, 'f₁, Hz', 10, 'middle', MUTED, f'transform="rotate(-90 16 {(T+H-B)/2})"'))
def curve(col, idx, dash=''): return path([(xx(v), yy(f)) for v, f in zip(V, fv[:, idx])], fill='none', stroke=col, stroke_width=1.6, **({'stroke_dasharray': dash} if dash else {}))
b.append(curve(INK, 3)); b.append(curve(WINE, 1)); b.append(curve(WINE, 4, '1 3')); b.append(curve(WINE, 2, '6 4'))
Vw = float(np.interp(N['glass']['z_widest'], fv[:, 6], V)); b.append(f'<line x1="{xx(Vw):.1f}" y1="{T}" x2="{xx(Vw):.1f}" y2="{H-B}" stroke="{MUTED}" stroke-dasharray="2 3"/>' + text(xx(Vw) + 4, T + 12, 'surface at the widest point', 9, 'start', MUTED))
for i2, (lab, col, dash) in enumerate((('no head', INK, ''), ('with 18 mm of head', WINE, ''), ('straight glass, with head', WINE, '5 4'))):
    ly = H - B - 46 + 14 * i2; b.append(f'<line x1="{W-R-150}" y1="{ly-3}" x2="{W-R-126}" y2="{ly-3}" stroke="{col}" stroke-width="1.6" {"stroke-dasharray=\"" + dash + "\"" if dash else ""}/>' + text(W - R - 120, ly, lab, 10, 'start', col))
open('notes/fig12/figs/f_vs_V.svg', 'w').write(svg(W, H, ''.join(b), 'Frequency of the slowest mode against the volume of stout: the Guinness glass with and without head, its sin copy, and a straight glass of the same surface radius and depth.'))

# ---- Figure 3: the damping budget ----
W, H = 720, 236; rows = [('wall and floor layers γ<tspan baseline-shift="sub" font-size="8">w</tspan>', N['gw11']), ('surface skin γ<tspan baseline-shift="sub" font-size="8">s</tspan>', N['gs11']), ('interior γ<tspan baseline-shift="sub" font-size="8">v</tspan>', N['gb11']), ('contact line γ<tspan baseline-shift="sub" font-size="8">c</tspan>', N['gc11']), ('head on the wall γ<tspan baseline-shift="sub" font-size="8">f</tspan>', N['gf11'])]
tot = N['gam11']; b = []; scale = 250 / tot
for i, (lab, v) in enumerate(rows):
    y0 = 22 + 30 * i; b.append(text(180, y0 + 13, lab, 11, 'end')); b.append(f'<rect x="190" y="{y0}" width="{v*scale:.1f}" height="18" fill="{WINE if i == 4 else INK}" opacity="0.75"/>'); b.append(text(196 + v * scale, y0 + 13, f'{v:.3f} s⁻¹  ({100*v/tot:.0f} %)', 10))
b.append(f'<line x1="190" y1="176" x2="{190+tot*scale:.1f}" y2="176" stroke="{INK}" stroke-width="2"/>' + text(180, 180, 'total γ', 11, 'end') + text(196 + tot * scale, 180, f'{tot:.3f} s⁻¹ → 1/e in {1/tot:.1f} s, 5 % in {math.log(20)/tot:.1f} s', 10))
b.append(text(12, 222, '500 mL of stout at 6 °C, 18 mm of head, ε_f = 0.15, c_s = 1, γ_c = 0.05 s⁻¹, c_f = 1', 10, 'start', MUTED))
open('notes/fig12/figs/budget.svg', 'w').write(svg(W, H + 6, ''.join(b), 'Damping rates of the slowest mode, term by term, at 6 °C with 500 mL of stout and 18 mm of head.'))

# ---- Figure 4: the slowest mode in the cut, from the stored three-dimensional field ----
F = [f for f in D_['fills'] if f['V_mL'] == 500][0]; md = [m for m in F['modes'] if m['m'] == 1 and m['o'] == 'c' and m['n'] == 1][0]
SN = np.array(D_['s_nodes']); FZ = np.array(F['field_z']); zf = GL['floor_mm'] / 1000; zs = F['zs']
W, H = 720, 400; sc = 2.4 * 1e3; cx = 360; by = 380
X = lambda r: cx + r * sc; Y = lambda zz: by - zz * sc
b = []
for sd in (-1, 1):
    th = 0.0 if sd > 0 else np.pi
    pts = [(X(sd * G.R0(q) / 1e3), Y(q / 1e3)) for q in z] + [(X(sd * G.R_inner(q, th) / 1e3), Y(q / 1e3)) for q in z[z >= G.Z_F][::-1]]
    b.append(path(pts, close=True, fill='#e6eff1', stroke=INK, stroke_width=1.0))
# the surface shape psi(s, theta) along the cut, scaled to 8 mm at the rim
amp = 0.008
def psi(s, th): return sum(np.interp(s, SN, md['psi'][k][0]) * math.cos(int(k) * th) + np.interp(s, SN, md['psi'][k][1]) * math.sin(int(k) * th) for k in md['psi'])
surf = [(X(-u * G.R_inner(zs * 1e3 + amp * psi(u, np.pi) * 1e3, np.pi) / 1e3), Y(zs + amp * psi(u, np.pi))) for u in np.linspace(1, 0, 25)] + [(X(u * G.R_inner(zs * 1e3, 0) / 1e3), Y(zs + amp * psi(u, 0))) for u in np.linspace(0, 1, 25)]
liq = [(X(-G.R_inner(q, np.pi) / 1e3), Y(q / 1e3)) for q in np.arange(G.Z_F, zs * 1e3, 1.0)]      # up the left wall, across the surface, down the right wall
b.append(path(liq + surf + [(X(G.R_inner(q, 0) / 1e3), Y(q / 1e3)) for q in np.arange(zs * 1e3, G.Z_F, -1.0)], close=True, fill=STOUT))
b.append(f'<line x1="{X(-0.045):.1f}" y1="{Y(zs):.1f}" x2="{X(0.045):.1f}" y2="{Y(zs):.1f}" stroke="{INK}" stroke-dasharray="4 3" stroke-width="0.8"/>')
# arrows: (d_r Phi, d_z Phi) at the stored grid, both halves of the cut; scale fixed
umax = 0; arr = []
for i in range(1, len(FZ), 1):
    for j in range(0, len(SN), 2):
        for sd, th in ((1, 0.0), (-1, np.pi)):
            if sd < 0 and j == 0: continue
            ur = sum(md['field'][k][i][j][1][0] * math.cos(int(k) * th) + md['field'][k][i][j][1][1] * math.sin(int(k) * th) for k in md['field'])
            uz = sum(md['field'][k][i][j][2][0] * math.cos(int(k) * th) + md['field'][k][i][j][2][1] * math.sin(int(k) * th) for k in md['field'])
            r = SN[j] * G.R_inner(FZ[i] * 1e3, th) / 1e3; arr.append((sd * r, FZ[i], sd * ur, uz)); umax = max(umax, math.hypot(ur, uz))
asc = 26 / umax
for (r, zz, ur, uz) in arr:
    x0, y0 = X(r), Y(zz); dx, dy = ur * asc, -uz * asc; L_ = math.hypot(dx, dy)
    if L_ < 1.5: b.append(f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="0.9" fill="{HEAD}"/>'); continue
    an = math.atan2(dy, dx); hh = min(4, 0.4 * L_)
    b.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0+dx:.1f}" y2="{y0+dy:.1f}" stroke="{HEAD}" stroke-width="1.1"/><path d="M{x0+dx:.1f},{y0+dy:.1f} L{x0+dx-hh*math.cos(an-0.45):.1f},{y0+dy-hh*math.sin(an-0.45):.1f} L{x0+dx-hh*math.cos(an+0.45):.1f},{y0+dy-hh*math.sin(an+0.45):.1f}Z" fill="{HEAD}"/>')
b.append(text(X(0.05), Y(zs - 1 / md['lam']) + 4, f'1/λ = {1e3/md["lam"]:.0f} mm below the surface', 10, 'start', MUTED)); b.append(f'<line x1="{X(0.042):.1f}" y1="{Y(zs-1/md["lam"]):.1f}" x2="{X(0.048):.1f}" y2="{Y(zs-1/md["lam"]):.1f}" stroke="{MUTED}"/>')
b.append(text(X(-0.05), Y(zs) + 4, 'calm level', 10, 'end', INK)); b.append(text(12, H - 8, 'mode (1,1) along x, 500 mL; surface drawn at 8 mm; arrows: velocity, one scale', 10, 'start', MUTED))
open('notes/fig12/figs/mode11.svg', 'w').write(svg(W, H, ''.join(b), 'The slowest sloshing mode in a vertical cut through the glass: the tilted surface, and the velocity arrows from the three-dimensional finite-element solution, strongest near the surface and fading with depth.'))

# ---- Figure 5: the one-wheel cart, side view, and the road's push on the wheel at a bump ----
W, H = 720, 440; b = []
gx, gr = 250, 366                                   # the wheel's centre x, the rest road line y
Rw = 34                                             # px: the wheel's radius in the drawing
# the road: flat, then a bump the wheel is climbing
road_pts = [(30, gr)] + [(x, gr - 30 * 0.5 * (1 - math.cos(2 * math.pi * (x - 210) / 160)) if 210 < x < 370 else gr) for x in range(200, 381, 4)] + [(700, gr)]
b.append(path([(30, H)] + road_pts + [(700, H)], close=True, fill='#efe8dc', stroke='none')); b.append(path(road_pts, fill='none', stroke=WINE, stroke_width=1.4))
# the contact point on the up-slope and the wheel resting on it
xc_ = 250; zc_ = 30 * 0.5 * (1 - math.cos(2 * math.pi * (xc_ - 210) / 160)); sl = 30 * 0.5 * math.sin(2 * math.pi * (xc_ - 210) / 160) * 2 * math.pi / 160
nx_, ny_ = -sl / math.hypot(1, sl), 1 / math.hypot(1, sl)            # unit normal, pointing up and back
cx_, cy_ = xc_ + Rw * nx_, gr - zc_ - Rw * ny_
b.append(f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="{Rw}" fill="#fff" stroke="{INK}" stroke-width="2"/><circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="3.5" fill="{WINE}"/>')
for k in range(6):
    an = k * math.pi / 3 + 0.3; b.append(f'<line x1="{cx_:.1f}" y1="{cy_:.1f}" x2="{cx_ + 0.85 * Rw * math.cos(an):.1f}" y2="{cy_ - 0.85 * Rw * math.sin(an):.1f}" stroke="{INK}" stroke-width="1"/>')
# the push N_vec from the contact point along the normal, and its two parts
L = 56; px_, py_ = xc_, gr - zc_
def arr(x0, y0, x1, y1, col, w=2):
    an = math.atan2(y1 - y0, x1 - x0); h = 8
    return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{col}" stroke-width="{w}"/>' +
            f'<path d="M{x1:.1f},{y1:.1f} L{x1 - h * math.cos(an - 0.4):.1f},{y1 - h * math.sin(an - 0.4):.1f} L{x1 - h * math.cos(an + 0.4):.1f},{y1 - h * math.sin(an + 0.4):.1f}Z" fill="{col}"/>')
# the push acts at the contact point, along the normal towards the axle: drawn with its tail in the road, its head at the contact point
tx_, ty_ = px_ - L * nx_, py_ + L * ny_
b.append(arr(tx_, ty_, px_, py_, WINE, 2.4))
b.append(arr(tx_, ty_, px_, ty_, ROSE, 1.6)); b.append(arr(px_, ty_, px_, py_, ROSE, 1.6))
b.append(f'<circle cx="{px_:.1f}" cy="{py_:.1f}" r="2.5" fill="{INK}"/>')
b.append(text(tx_ + (px_ - tx_) / 2, ty_ + 14, sub('kick −N z_a′ (back)'), 10, 'middle', WINE)); b.append(text(px_ + 6, (py_ + ty_) / 2 + 4, 'N', 11, 'start', WINE))
b.append(text(px_ + 14, py_ - 14, 'contact', 9, 'start', MUTED))
# the strut: spring and damper from the axle up to the body
bx, by_, bw, bh = cx_ - 95, cy_ - 140, 190, 22
b.append(f'<rect x="{bx:.1f}" y="{by_:.1f}" width="{bw}" height="{bh}" rx="4" fill="#3a2f2c" stroke="{INK}"/>' + text(bx + bw / 2, by_ + 15, sub('body M_b'), 10, 'middle', '#fff'))
yb_ = cy_ - Rw - 8                                  # the axle bar, just above the wheel, held by a fork from the axle
b.append(f'<line x1="{cx_:.1f}" y1="{cy_:.1f}" x2="{cx_:.1f}" y2="{yb_:.1f}" stroke="{INK}" stroke-width="1.6"/>')
sx_ = cx_ - 22; zig = ''.join(f' L{sx_ + (7 if k % 2 else -7):.1f},{yb_ - 4 - (yb_ - 4 - by_ - bh) * k / 9:.1f}' for k in range(1, 9))
b.append(f'<path d="M{sx_:.1f},{yb_:.1f} L{sx_:.1f},{yb_ - 4:.1f}{zig} L{sx_:.1f},{by_ + bh:.1f}" fill="none" stroke="#d99a3a" stroke-width="1.6"/>')
dx_ = cx_ + 22; ym = (yb_ + by_ + bh) / 2
b.append(f'<line x1="{dx_:.1f}" y1="{yb_:.1f}" x2="{dx_:.1f}" y2="{ym + 4:.1f}" stroke="{WINE}" stroke-width="1.6"/><rect x="{dx_ - 7:.1f}" y="{ym - 14:.1f}" width="14" height="24" fill="none" stroke="{WINE}" stroke-width="1.4"/><line x1="{dx_:.1f}" y1="{ym - 14:.1f}" x2="{dx_:.1f}" y2="{by_ + bh:.1f}" stroke="{WINE}" stroke-width="1.6"/>')
b.append(f'<line x1="{sx_:.1f}" y1="{yb_:.1f}" x2="{dx_:.1f}" y2="{yb_:.1f}" stroke="{INK}" stroke-width="1.4"/>')
b.append(text(sx_ - 12, ym + 4, sub('k_s'), 10, 'end', '#a8741f')); b.append(text(dx_ + 12, ym, sub('c, u_s'), 10, 'start', WINE))
b.append(text(cx_ + Rw + 8, cy_ - 14, sub('m_w, k_t, R_w'), 10, 'start', MUTED))
# posts, tray and the glass
tyy = by_ - 64
for xx in (cx_ - 50, cx_ + 50): b.append(f'<line x1="{xx:.1f}" y1="{by_:.1f}" x2="{xx:.1f}" y2="{tyy:.1f}" stroke="{INK}" stroke-width="2"/>')
b.append(f'<rect x="{cx_ - 72:.1f}" y="{tyy - 4:.1f}" width="144" height="4" fill="#fff" stroke="{WINE}"/>')
gz = tyy - 4; gp = [(cx_ - 11, gz), (cx_ - 13, gz - 20), (cx_ - 16, gz - 44), (cx_ - 13, gz - 56), (cx_ + 13, gz - 56), (cx_ + 16, gz - 44), (cx_ + 13, gz - 20), (cx_ + 11, gz)]
b.append(path(gp, close=True, fill='#e6eff1', stroke=INK, stroke_width=1)); b.append(f'<rect x="{cx_ - 13:.1f}" y="{gz - 48:.1f}" width="26" height="46" fill="{STOUT}"/><rect x="{cx_ - 15:.1f}" y="{gz - 54:.1f}" width="30" height="7" fill="{HEAD}"/>')
b.append(f'<circle cx="{cx_:.1f}" cy="{gz:.1f}" r="2.5" fill="{WINE}"/>' + text(cx_ + 80, gz + 2, sub('O, h_g above the body'), 9, 'start', WINE))
# the drive and its motor
b.append(arr(cx_ + 100, by_ + bh / 2, cx_ + 160, by_ + bh / 2, INK, 1.6) + text(cx_ + 166, by_ + bh / 2 + 4, 'drive: −c<tspan baseline-shift="sub" font-size="7">drive</tspan> ẋ<tspan baseline-shift="sub" font-size="7">c</tspan> + u<tspan baseline-shift="sub" font-size="7">m</tspan>', 10, 'start', INK))
b.append(text(cx_ - 120, by_ + 15, sub('z_b ↑'), 10, 'end', MUTED)); b.append(text(cx_ - 120, cy_ + 4, sub('z_w ↑'), 10, 'end', MUTED))
b.append(text(380, 26, sub('X = v t + x_c along the road →'), 10, 'start', MUTED))
b.append(text(560, gr + 22, sub('road z_r(X); the axle follows z_a(X)'), 10, 'end', MUTED))
open('notes/fig12/figs/cart.svg', 'w').write(svg(W, H, ''.join(b), 'The one-wheel cart on a bump: the wheel touches the road on the up-slope, the road pushes along the normal through the axle, and that push has a vertical part, the tyre load N, and a horizontal part, the kick, pointing back. Above the wheel the strut with its spring and damper carries the body, posts carry the tray and the glass, and the drive pulls along the road.'))

# ---- Figure 6: the bump runs ----
P = dict(plant.DEFAULT); rho = 1007.0
F500 = C.load_modes(MPATH)['fills']; F500 = [f for f in F500 if f['V_mL'] == 500][0]
def gamma_fn(mdx):
    lam = mdx['lam']; kappa = N['Mf'] * lam / rho; w = math.sqrt((9.81 * lam + 0.045 * lam ** 3 / rho) / (1 + kappa)); sq = 0.5 * math.sqrt(N['nu'] * w / 2)
    return sq * (mdx['Iw'] + mdx['Ib']) + sq * mdx['Is'] + 2 * N['nu'] * lam ** 2 + 0.05 + (0.016 / F500['a']) * (1 - math.exp(-lam * 0.018))
modes = plant.modal_params(F500, rho, 0.045, N['Mf'], gamma_fn)
for mdx, raw in zip(modes['x'], [m for m in F500['modes'] if m['m'] == 1 and m['o'] == 'c']): mdx['rim_front'] = sum(raw['psi'][k][0][-1] for k in raw['psi'])
Dd = C.design(P, F500, modes, rho, Ts=0.01, s_eta=0.0005, s_w=0.001, s_v=0.05, s_u=20.0, s_m=20.0)
runs = {law: C.simulate(Dd, P, 'bump', v=1.5, T=4.0, law=law, h_road=0.03) for law in ('passive', 'skyhook', 'lqr')}
W, H = 720, 460; L, R = 70, 30; panels = [(30, 150, 'stout at the front of the rim, mm', -10, 20), (190, 290, 'the road’s kick along the road, N', -30, 30), (330, 430, 'drive motor force, N', -30, 30)]
b = []
for (T, B, lab, lo, hi) in panels:
    b.append(f'<rect x="{L}" y="{T}" width="{W-L-R}" height="{B-T}" fill="none" stroke="{RULE}"/>'); b.append(text(L, T - 5, lab, 10, 'start', MUTED))
    for v in np.linspace(lo, hi, 7): yv = T + (B - T) * (1 - (v - lo) / (hi - lo)); b.append(f'<line x1="{L}" y1="{yv:.1f}" x2="{W-R}" y2="{yv:.1f}" stroke="{LIGHT}"/>' + text(L - 6, yv + 4, f'{v:g}', 10, 'end', MUTED))
xx = lambda t: L + (W - L - R) * t / 4.0
for t in range(0, 5): b.append(text(xx(t), H - 14, str(t), 10, 'middle', MUTED))
b.append(text((L + W - R) / 2, H - 2, 'time after the start, s', 10, 'middle', MUTED))
def clipped(col, T, B, lo, hi, ts, vs, dash=''):
    yv = lambda v: T + (B - T) * (1 - (min(max(v, lo), hi) - lo) / (hi - lo))
    return path([(xx(t), yv(v)) for t, v in zip(ts, vs)], fill='none', stroke=col, stroke_width=1.4, **({'stroke_dasharray': dash} if dash else {}))
lim = N['ctl']['dome_mm'] - N['ctl']['head_top_rest_mm']
T0, B0, _, lo0, hi0 = panels[0]; ylim = T0 + (B0 - T0) * (1 - (lim - lo0) / (hi0 - lo0)); b.append(f'<line x1="{L}" y1="{ylim:.1f}" x2="{W-R}" y2="{ylim:.1f}" stroke="{WINE}" stroke-dasharray="5 4"/>' + text(L + 6, ylim - 7, f'dome limit, {lim:.1f} mm', 9, 'start', WINE))
for law, col in (('passive', INK), ('skyhook', ROSE), ('lqr', WINE)):
    o = runs[law]; b.append(clipped(col, *panels[0][:2], panels[0][3], panels[0][4], o['t'], o['eta'] * 1e3)); b.append(clipped(col, *panels[1][:2], panels[1][3], panels[1][4], o['t'], o['kick'])); b.append(clipped(col, *panels[2][:2], panels[2][3], panels[2][4], o['t'], o['u'][:, 1]))
b.append(text(L + 6, 330 + 12, 'ink: passive · rose: skyhook · wine: LQR', 9, 'start', MUTED))
open('notes/fig12/figs/runs.svg', 'w').write(svg(W, H, ''.join(b), 'The pint over a 30 mm speed bump at 1.5 m/s: the stout at the front of the rim, the road’s kick along the road and the drive motor’s force, for the passive cart, the skyhook damper and the LQR.'))
print('wrote notes/fig12/figs/{profile,f_vs_V,budget,mode11,cart,runs}.svg')
