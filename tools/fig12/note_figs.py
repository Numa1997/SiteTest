"""SVG figures of the Fig. 12 lecture note, in the house chart style (white plate, IBM Plex Mono ticks, ink and wine),
drawn from public/scripts/slosh-modes.js and notes/fig12/numbers.json. Writes notes/fig12/figs/*.svg."""
import json, math, numpy as np
D_ = json.loads(open('public/scripts/slosh-modes.js').read().split('window.SLOSH_MODES = ', 1)[1].rstrip().rstrip(';'))
N = json.load(open('notes/fig12/numbers.json')); GL = D_['glass']
INK, WINE, ROSE, RULE, MUTED, STOUT, HEAD = '#1c1518', '#7a1f2b', '#e2a2aa', '#cdc1ae', '#8b8079', '#2b1210', '#efe2c6'
MONO = "font-family=\"IBM Plex Mono, monospace\""
def svg(w, h, body, label): return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}"><rect x="0" y="0" width="{w}" height="{h}" fill="#fff"/>{body}</svg>'
def text(x, y, s, size=11, anchor='start', fill=INK, extra=''): return f'<text x="{x:.1f}" y="{y:.1f}" {MONO} font-size="{size}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
z = np.array(GL['z_mm']); Ro = np.array(GL['R_outer_mm']); Ri = np.array([np.nan if v is None else v for v in GL['R_inner_mm']])

# Figure 1: the measured profile
W, H = 720, 440; sc = 2.4; cx = 190; by = 410
X = lambda r: cx + r * sc; Y = lambda zz: by - zz * sc
b = []
for sd in (-1, 1):
    pts = [(X(sd * r), Y(q)) for r, q in zip(Ro, z)] + [(X(sd * r), Y(q)) for r, q in zip(Ri[::-1], z[::-1]) if not np.isnan(r)] + [(X(0), Y(GL['floor_mm'])), (X(0), Y(0))]
    b.append('<path d="M' + ' L'.join(f'{p[0]:.1f},{p[1]:.1f}' for p in pts) + f'Z" fill="#e6eff1" stroke="{INK}" stroke-width="1.2"/>')
zs = N['zs_mm']; m = (~np.isnan(Ri)) & (z <= zs)
liq = [(X(-r), Y(q)) for r, q in zip(Ri[m], z[m])][::-1] + [(X(r), Y(q)) for r, q in zip(Ri[m], z[m])]
b.append('<path d="M' + ' L'.join(f'{p[0]:.1f},{p[1]:.1f}' for p in liq) + f'Z" fill="{STOUT}"/>')
hz = zs + 18; mh = (~np.isnan(Ri)) & (z >= zs) & (z <= hz)
hd = [(X(-r), Y(q)) for r, q in zip(Ri[mh], z[mh])][::-1] + [(X(r), Y(q)) for r, q in zip(Ri[mh], z[mh])]
b.append('<path d="M' + ' L'.join(f'{p[0]:.1f},{p[1]:.1f}' for p in hd) + f'Z" fill="{HEAD}" stroke="#b08a50" stroke-width="0.8"/>')
def hline(zz, lab, col=INK, dash='4 3', right=True):
    r = float(np.interp(zz, z, Ro)); return f'<line x1="{X(-r)-6:.1f}" y1="{Y(zz):.1f}" x2="{X(r)+60:.1f}" y2="{Y(zz):.1f}" stroke="{col}" stroke-dasharray="{dash}" stroke-width="1"/>' + text(X(r) + 64, Y(zz) + 4, lab, 11, 'start', col)
b.append(hline(160, 'rim, 160 mm (published height)', WINE, 'none'))
b.append(hline(152.0, '568 mL (one pint) reaches 151.9 mm', MUTED))
b.append(hline(zs, f'500 mL: surface {zs:.1f} mm, a = {N["a_mm"]:.1f} mm', INK))
b.append(hline(GL['floor_mm'], 'floor of the cavity, 8 mm of solid glass below', MUTED))
iw = int(np.nanargmax(Ro)); b.append(f'<line x1="{X(-Ro[iw]):.1f}" y1="{Y(z[iw]):.1f}" x2="{X(Ro[iw]):.1f}" y2="{Y(z[iw]):.1f}" stroke="{WINE}" stroke-width="1"/>' + text(X(0), Y(z[iw]) - 5, f'{2*Ro[iw]:.1f} mm', 10, 'middle', WINE))
b.append(text(X(0), Y(160) - 8, f'{2*Ro[-1]:.1f} mm', 10, 'middle', WINE))
for t in range(0, 161, 40): b.append(f'<line x1="{cx-128}" y1="{Y(t):.1f}" x2="{cx-122}" y2="{Y(t):.1f}" stroke="{MUTED}"/>' + text(cx - 132, Y(t) + 4, str(t), 10, 'end', MUTED))
b.append(text(cx - 160, Y(80), 'z, mm', 10, 'middle', MUTED, f'transform="rotate(-90 {cx-160} {Y(80)})"'))
b.append(text(12, by + 24, 'outer radius from the photograph; inner = outer − 2.0 mm normal to the wall', 10, 'start', MUTED))
open('notes/fig12/figs/profile.svg', 'w').write(svg(W, H + 10, ''.join(b), 'The measured profile of the Guinness tulip glass: outer and inner wall, 500 mL of stout under 18 mm of head, the pint line at 152 mm and the rim at 160 mm.'))

# Figure 2: f11 against fill
W, H = 720, 330; L, R, T, B = 70, 30, 20, 50
fv = np.array(N['f_vs_V']); V = fv[:, 0]
x = lambda v: L + (v - 300) / 290 * (W - L - R); flo, fhi = 3.1, 3.7; y = lambda f: T + (fhi - f) / (fhi - flo) * (H - T - B)
b = [f'<rect x="{L}" y="{T}" width="{W-L-R}" height="{H-T-B}" fill="none" stroke="{RULE}"/>']
for f in np.arange(3.1, 3.71, 0.1): b.append(f'<line x1="{L}" y1="{y(f):.1f}" x2="{W-R}" y2="{y(f):.1f}" stroke="#f0ebe3"/>' + text(L - 6, y(f) + 4, f'{f:.1f}', 10, 'end', MUTED))
for v in range(300, 591, 50): b.append(text(x(v), H - B + 16, str(v), 10, 'middle', MUTED))
b.append(text((L + W - R) / 2, H - 10, 'stout V, mL', 10, 'middle', MUTED)); b.append(text(16, (T + H - B) / 2, 'f₁, Hz', 10, 'middle', MUTED, f'transform="rotate(-90 16 {(T+H-B)/2})"'))
def curve(col, idx, dash=''):
    return f'<polyline fill="none" stroke="{col}" stroke-width="1.8" {"stroke-dasharray=%s" % chr(34)+dash+chr(34) if dash else ""} points="' + ' '.join(f'{x(a):.1f},{y(b_):.1f}' for a, b_ in zip(V, fv[:, idx])) + '"/>'
b += [curve(INK, 3), curve(WINE, 1), curve(WINE, 2, '5 4')]
lx = L + 14; b.append(f'<line x1="{lx}" y1="{T+16}" x2="{lx+24}" y2="{T+16}" stroke="{INK}" stroke-width="1.8"/>' + text(lx + 30, T + 20, 'tulip glass, no head', 10))
b.append(f'<line x1="{lx}" y1="{T+32}" x2="{lx+24}" y2="{T+32}" stroke="{WINE}" stroke-width="1.8"/>' + text(lx + 30, T + 36, 'tulip glass, 18 mm head', 10, fill=WINE))
b.append(f'<line x1="{lx}" y1="{T+48}" x2="{lx+24}" y2="{T+48}" stroke="{WINE}" stroke-width="1.8" stroke-dasharray="5 4"/>' + text(lx + 30, T + 52, 'straight glass of the same a and D, 18 mm head', 10, fill=WINE))
vi = list(V).index(420); b.append(f'<line x1="{x(420):.1f}" y1="{T}" x2="{x(420):.1f}" y2="{H-B}" stroke="{RULE}" stroke-dasharray="3 3"/>' + text(x(420) + 4, H - B - 8, 'widest point of the glass', 9, 'start', MUTED))
open('notes/fig12/figs/f_vs_V.svg', 'w').write(svg(W, H, ''.join(b), 'Frequency of the slowest mode against the volume of stout: tulip glass with and without head, and a straight glass of the same surface radius and depth.'))

# Figure 3: the (1,1) mode in the cut, from the FEM field (fill 480 mL)
F = D_['fills'][D_['vols_mL'].index(480)]; md = [mm for mm in F['modes'] if mm['m'] == 1 and mm['n'] == 1][0]
ns, nz = D_['field_grid']['ns'], D_['field_grid']['nz']; fld = np.array(md['field']).reshape(nz, ns, 3)
zs, a = F['zs'] * 1e3, F['a'] * 1e3; zf = GL['floor_mm']; Dp = zs - zf
W, H = 720, 400; sc = 2.25; cx = 360; by = 380; X = lambda r: cx + r * sc; Y = lambda zz: by - zz * sc
b = []
for sd in (-1, 1):
    pts = [(X(sd * r), Y(q)) for r, q in zip(Ri, z) if not np.isnan(r) and q <= 160]
    b.append('<polyline fill="none" stroke="' + INK + '" stroke-width="1.2" points="' + ' '.join(f'{p[0]:.1f},{p[1]:.1f}' for p in pts) + '"/>')
amp = 9.0   # mm at the wall, drawn
rr = np.linspace(-1, 1, 49); fr = np.interp(np.abs(rr), np.linspace(0, 1, len(md['f'])), md['f']) * np.sign(rr)
surf = [(X(u * a), Y(zs + amp * f)) for u, f in zip(rr, fr)]
mz = (~np.isnan(Ri)) & (z <= zs)
body = [(X(-r), Y(q)) for r, q in zip(Ri[mz], z[mz])][::-1] + surf + [(X(r), Y(q)) for r, q in zip(Ri[mz], z[mz])][::-1][::-1]
left = [(X(-r), Y(q)) for r, q in zip(Ri[mz], z[mz])]                 # up the left wall
right = [(X(r), Y(q)) for r, q in zip(Ri[mz][::-1], z[mz][::-1])]      # down the right wall
b.append('<path d="M' + ' L'.join(f'{p[0]:.1f},{p[1]:.1f}' for p in left + [(X(-a), Y(zs)), (X(a), Y(zs))] + right) + f'Z" fill="{STOUT}" opacity="0.92"/>')
b.append('<polyline fill="none" stroke="' + WINE + '" stroke-width="1.4" stroke-dasharray="5 3" points="' + ' '.join(f'{p[0]:.1f},{p[1]:.1f}' for p in surf) + '"/>')

smax = np.abs(fld[:, :, 1:]).max(); ascale = 20 / smax
for i in range(1, nz, 2):
    for j in range(0, ns):
        d = Dp * (i / (nz - 1)) ** 1.6; zz = zs - d; r = float(np.interp(zz, z[~np.isnan(Ri)], Ri[~np.isnan(Ri)])) * j / (ns - 1)
        for sd in ((1, -1) if j else (1,)):
            cm = 1 if sd > 0 else (-1) ** md['m']        # cos(m θ) at θ = 0 (right half) or π (left half)
            ur, uz = sd * cm * fld[i, j, 1] * ascale, cm * fld[i, j, 2] * ascale   # horizontal: u_r cos(mθ) times the side's outward sign
            x0, y0 = X(sd * r), Y(zz); L_ = math.hypot(ur, uz)
            if L_ < 1.2: b.append(f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="0.9" fill="#f5f1ea"/>'); continue
            x1, y1 = x0 + ur, y0 - uz; an = math.atan2(y1 - y0, x1 - x0); hh = min(5, 0.45 * L_)
            b.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#f5f1ea" stroke-width="1.1"/><path d="M{x1:.1f},{y1:.1f} L{x1-hh*math.cos(an-0.45):.1f},{y1-hh*math.sin(an-0.45):.1f} L{x1-hh*math.cos(an+0.45):.1f},{y1-hh*math.sin(an+0.45):.1f}Z" fill="#f5f1ea"/>')
b.append(text(X(a) + 12, Y(zs + amp) + 4, 'tilt, 9 mm at the wall', 10, 'start', WINE)); b.append(text(X(a) + 12, Y(zs - 21.2) + 4, f'1/λ = {1000/md["lam"]:.0f} mm below', 10, 'start', MUTED))
b.append(f'<line x1="{X(a)+4}" y1="{Y(zs-1000/md["lam"]):.1f}" x2="{X(a)+10}" y2="{Y(zs-1000/md["lam"]):.1f}" stroke="{MUTED}"/>')
b.append(text(cx, 18, 'mode (1,1), 480 mL: velocity as the surface passes level; dashed: the tilt a quarter period later', 10, 'middle', MUTED))
open('notes/fig12/figs/mode11.svg', 'w').write(svg(W, H, ''.join(b), 'The slowest sloshing mode in a vertical cut through the glass: the tilted surface, and the velocity arrows from the finite-element solution, strongest near the surface and fading with depth.'))

# Figure 4: damping budget of the (1,1) mode
W, H = 720, 230; L = 190; R = 90
rows = [('wall and floor layers γ_w', N['gw11']), ('surface skin γ_s', N['gs11']), ('bulk 2νλ² γ_b', N['gb11']), ('contact line γ_c', N['gc11']), ('head friction γ_f', N['gf11'])]
tot = N['gam11']; xs = lambda v: L + v / 0.26 * (W - L - R)
b = []
for k, (lab, v) in enumerate(rows):
    yy = 22 + k * 30; b.append(text(L - 10, yy + 13, lab, 11, 'end'))
    b.append(f'<rect x="{L}" y="{yy}" width="{xs(v)-L:.1f}" height="18" fill="{WINE if "head" in lab else INK}" opacity="{0.9 if "head" in lab else 0.75}"/>' + text(xs(v) + 6, yy + 13, f'{v:.3f} 1/s  ({100*v/tot:.0f} %)', 10))
yy = 22 + 5 * 30 + 8; b.append(text(L - 10, yy + 4, 'total γ₁₁', 11, 'end', WINE)); b.append(text(L, yy + 4, f'{tot:.3f} 1/s: amplitude falls to 1/e in {1/tot:.2f} s, to 5 % in {math.log(20)/tot:.1f} s', 11, 'start', WINE))
for v in (0, 0.05, 0.1, 0.15, 0.2, 0.25): b.append(f'<line x1="{xs(v):.1f}" y1="16" x2="{xs(v):.1f}" y2="{22+5*30-6}" stroke="#f0ebe3"/>' + text(xs(v), 12, f'{v:.2f}', 9, 'middle', MUTED))
open('notes/fig12/figs/budget.svg', 'w').write(svg(W, H + 6, ''.join(b), 'Damping rates of the slowest mode, term by term, at 6 °C with 500 mL of stout and 18 mm of head.'))
print('wrote notes/fig12/figs/{profile,f_vs_V,mode11,budget}.svg')
