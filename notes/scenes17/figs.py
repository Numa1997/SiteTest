# Fig. 17, section 2: the three SVG figures of the spinners note, plotted from the formulas and the stored checks.
# python3 notes/scenes17/figs.py <spinners.json>  ->  figs.json (three SVG strings, pasted into the page)
import json, numpy as np
import sys; d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'spinners.json'))   # the stored spinners.json of the run
X0, X1, Y0, Y1 = 64, 698, 36, 278
def ax(xmin, xmax, ymin, ymax, xt, yt, xl, yl, fmt=lambda v: ('%g' % v)):
    sx = lambda v: X0 + (v - xmin) / (xmax - xmin) * (X1 - X0)
    sy = lambda v: Y1 - (v - ymin) / (ymax - ymin) * (Y1 - Y0)
    o = ['<rect x="0" y="0" width="720" height="330" fill="#fff"/>']
    for v in yt: o.append('<line x1="64" x2="698" y1="%.1f" y2="%.1f" stroke="#eee6d9" stroke-width="1"/><text class="tick" x="56" y="%.1f" text-anchor="end">%s</text>' % (sy(v), sy(v), sy(v) + 4, fmt(v)))
    for v, lab in xt: o.append('<line x1="%.1f" x2="%.1f" y1="278" y2="283" stroke="#8b8079"/><text class="tick" x="%.1f" y="297" text-anchor="middle">%s</text>' % (sx(v), sx(v), sx(v), lab))
    o.append('<line x1="64" x2="698" y1="278" y2="278" stroke="#8b8079"/><line x1="64" x2="64" y1="36" y2="278" stroke="#8b8079"/>')
    o.append('<text class="lbl" x="698" y="316" text-anchor="end">%s</text><text class="lbl" x="56" y="22">%s</text>' % (xl, yl))
    return o, sx, sy
def path(sx, sy, xs, ys, st):
    return '<path d="%s" fill="none" %s/>' % (' '.join(('M' if i == 0 else 'L') + '%.1f %.1f' % (sx(a), sy(b)) for i, (a, b) in enumerate(zip(xs, ys))), st)
def svg(o, label):
    return '<svg viewBox="0 0 720 330" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">\n' % label + '\n'.join(o) + '\n</svg>'

# Figure 1: psi' = Delta - K sin psi, K = 4
K = 4; ps = np.linspace(-np.pi, np.pi, 241)
o, sx, sy = ax(-np.pi, np.pi, -12, 12, [(-np.pi, '−π'), (-np.pi/2, '−π/2'), (0, '0'), (np.pi/2, 'π/2'), (np.pi, 'π')], [-12, -8, -4, 0, 4, 8, 12],
               'angle ψ = θ − φ of the rotor behind or ahead of the field (rad)', 'ψ′ (rad/s), for K = 4 rad/s')
o.append('<line x1="64" x2="698" y1="%.1f" y2="%.1f" stroke="#8b8079" stroke-width="1"/>' % (sy(0), sy(0)))
for D, st, nm in [(2, 'stroke="#7a1f2b" stroke-width="2"', 'Δ = 2: locks'), (4, 'stroke="#b07a6a" stroke-width="2" stroke-dasharray="6 4"', 'Δ = K = 4: the edge'), (7, 'stroke="#1c1518" stroke-width="2" stroke-dasharray="2 3"', 'Δ = 7: slips')]:
    o.append(path(sx, sy, ps, D - K * np.sin(ps), st))
p1 = np.arcsin(2 / 4); p2 = np.pi - p1
o.append('<circle cx="%.1f" cy="%.1f" r="5" fill="#7a1f2b"/><circle cx="%.1f" cy="%.1f" r="5" fill="#fff" stroke="#7a1f2b" stroke-width="2"/>' % (sx(p1), sy(0), sx(p2), sy(0)))
o.append('<text class="lbl" x="%.1f" y="%.1f">stable</text><text class="lbl" x="%.1f" y="%.1f" text-anchor="end">unstable</text>' % (sx(p1) - 22, sy(0) + 22, sx(p2) + 18, sy(0) + 22))
for i, (st, nm) in enumerate([('stroke="#7a1f2b" stroke-width="2"', 'Δ = 2 rad/s: locks'), ('stroke="#b07a6a" stroke-width="2" stroke-dasharray="6 4"', 'Δ = K = 4 rad/s: the edge'), ('stroke="#1c1518" stroke-width="2" stroke-dasharray="2 3"', 'Δ = 7 rad/s: slips')]):
    o.append('<line x1="84" x2="108" y1="%d" y2="%d" %s/><text class="lbl" x="114" y="%d">%s</text>' % (222 + 20 * i, 222 + 20 * i, st, 226 + 20 * i, nm))
f1 = svg(o, 'The rate of the angle psi against psi for K = 4 rad/s and three mistunings: two crossings of zero for Delta = 2, a touching for Delta = 4, none for Delta = 7.')

# Figure 2: mean rate vs omega, K = 4, Omega = 3, with the stored check points
Om = 3; w = np.linspace(-6, 12, 721); D = w - Om
mr = np.where(np.abs(D) < K, Om, Om + np.sign(D) * np.sqrt(np.clip(D * D - K * K, 0, None)))
o, sx, sy = ax(-6, 12, -6, 12, [(v, str(v).replace('-', '−')) for v in range(-6, 13, 3)], [-6, -3, 0, 3, 6, 9, 12],
               'own rate ω of the rotor (rad/s)', 'mean rate ⟨θ′⟩ (rad/s), K = 4 rad/s, Ω = 3 rad/s', fmt=lambda v: ('%g' % v).replace('-', '−'))
o.append(path(sx, sy, w, w, 'stroke="#8b8079" stroke-width="1" stroke-dasharray="4 4"'))
o.append(path(sx, sy, w, mr, 'stroke="#7a1f2b" stroke-width="2"'))
for c in d['checks']['adler']:
    m = Om + np.sign(c['omega'] - Om) * 2 * np.pi / c['T_slip_measured'] if c['kind'] == 'slips' else c['rate_measured']
    o.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="#fff" stroke="#1c1518" stroke-width="1.6"/>' % (sx(c['omega']), sy(m)))
o.append('<line x1="%.1f" x2="%.1f" y1="%.1f" y2="%.1f" stroke="#b07a6a" stroke-width="1"/><line x1="%.1f" x2="%.1f" y1="%.1f" y2="%.1f" stroke="#b07a6a" stroke-width="1"/>' % (sx(-1), sx(-1), Y0, Y1, sx(7), sx(7), Y0, Y1))
o.append('<text class="lbl" x="%.1f" y="56" text-anchor="middle">locked: Ω − K &lt; ω &lt; Ω + K</text>' % sx(3))
o.append('<line x1="84" x2="108" y1="52" y2="52" stroke="#7a1f2b" stroke-width="2"/><text class="lbl" x="114" y="56">Adler, equation (8)</text>')
o.append('<circle cx="96" cy="72" r="4.5" fill="#fff" stroke="#1c1518" stroke-width="1.6"/><text class="lbl" x="114" y="76">one rotor on Kaggle</text>')
o.append('<line x1="84" x2="108" y1="92" y2="92" stroke="#8b8079" stroke-dasharray="4 4"/><text class="lbl" x="114" y="96">no field, ⟨θ′⟩ = ω</text>')
f2 = svg(o, 'Mean rate of one rotor against its own rate for K = 4 and Omega = 3: a flat step at Omega between omega = -1 and 7, square-root curves outside it, and the seven rotors computed on Kaggle lying on the curve.')

# Figure 3: locking radius vs |Delta|
Dd = np.linspace(0.05, 20, 800); s = 4
o, sx, sy = ax(0, 10, 0, 12, [(v, str(v)) for v in range(0, 11, 2)], [0, 2, 4, 6, 8, 10, 12], 'mistuning |Δ| = |ω − Ω| (rad/s)', 'locking radius r (lattice spacings), σ = 4')
o.append('<rect x="%.1f" y="36" width="%.1f" height="242" fill="#f6efe6"/><rect x="%.1f" y="36" width="%.1f" height="242" fill="#efe3e0"/>' % (sx(0), sx(2) - sx(0), sx(4.5), sx(8) - sx(4.5)))
o.append('<text class="lbl" x="%.1f" y="270" text-anchor="middle">turning with the field</text><text class="lbl" x="%.1f" y="270" text-anchor="middle">turning against it</text>' % (sx(1), sx(6.25)))
for K0, st in [(4, 'stroke="#b07a6a" stroke-width="2" stroke-dasharray="6 4"'), (10, 'stroke="#7a1f2b" stroke-width="2"'), (20, 'stroke="#1c1518" stroke-width="2" stroke-dasharray="2 3"')]:
    m = Dd < K0; r = s * np.sqrt(2 * np.log(K0 / Dd[m])); r = np.minimum(r, 12)
    o.append(path(sx, sy, Dd[m][(Dd[m] <= 10)], r[(Dd[m] <= 10)], st))
for i, (st, nm) in enumerate([('stroke="#b07a6a" stroke-width="2" stroke-dasharray="6 4"', 'K₀ = 4 rad/s'), ('stroke="#7a1f2b" stroke-width="2"', 'K₀ = 10 rad/s'), ('stroke="#1c1518" stroke-width="2" stroke-dasharray="2 3"', 'K₀ = 20 rad/s')]):
    o.append('<line x1="560" x2="584" y1="%d" y2="%d" %s/><text class="lbl" x="590" y="%d">%s</text>' % (52 + 20 * i, 52 + 20 * i, st, 56 + 20 * i, nm))
f3 = svg(o, 'Locking radius against mistuning for K0 = 4, 10 and 20; shaded bands mark the mistunings of the stored rotors that turn with the field (0 to 2) and against it (4.5 to 8).')
open('figs.json', 'w').write(json.dumps([f1, f2, f3]))
print(len(f1), len(f2), len(f3))
