"""Figure 5 of the Fig. 12 note: a 20 cm carry, the waiter against a hand moving along the same smooth path (rate 3 rad/s).
Writes notes/fig12/figs/waiter.svg from tools/fig12/controller.py."""
import sys, numpy as np; sys.path.insert(0, 'tools/fig12'); import controller as C
A, B, md, info = C.model(); K, Ad, Bd = C.lqr(A, B)
tw, ew, xw, Fw = C.carry(A, B, K, Ad, Bd, info, 0.20, T=4.0, series=True)
th, eh, xh, _ = C.carry(A, B, K, Ad, Bd, info, 0.20, T=4.0, mode='hand', Om=3.0, series=True)
INK, WINE, MUTED, RULE = '#1c1518', '#7a1f2b', '#8b8079', '#cdc1ae'; MONO = 'font-family="IBM Plex Mono, monospace"'
W, H = 720, 400; L, R = 70, 30
def panel(y0, h, ylo, yhi, ticks, lab):
    y = lambda v: y0 + h * (yhi - v) / (yhi - ylo); x = lambda t: L + (W - L - R) * t / 4.0
    b = [f'<rect x="{L}" y="{y0}" width="{W-L-R}" height="{h}" fill="none" stroke="{RULE}"/>']
    for v in ticks: b.append(f'<line x1="{L}" y1="{y(v):.1f}" x2="{W-R}" y2="{y(v):.1f}" stroke="#f0ebe3"/><text x="{L-6}" y="{y(v)+4:.1f}" {MONO} font-size="10" text-anchor="end" fill="{MUTED}">{v:g}</text>')
    b.append(f'<text x="16" y="{y0+h/2:.1f}" {MONO} font-size="10" text-anchor="middle" fill="{MUTED}" transform="rotate(-90 16 {y0+h/2:.1f})">{lab}</text>')
    return b, x, y
b1, x, y1 = panel(16, 150, -10, 10, [-8, -4, 0, 4, 8], 'η at the wall, mm')
fb = 160 - 137.539 - 18
b1.append(f'<line x1="{L}" y1="{y1(fb):.1f}" x2="{W-R}" y2="{y1(fb):.1f}" stroke="{WINE}" stroke-dasharray="5 4"/><text x="{W-R-4}" y="{y1(fb)-5:.1f}" {MONO} font-size="10" text-anchor="end" fill="{WINE}">head reaches the rim, {fb:.1f} mm</text>')
pl = lambda t, v, yf, col, dash='': f'<polyline fill="none" stroke="{col}" stroke-width="1.6" {"stroke-dasharray=%s" % chr(34)+dash+chr(34) if dash else ""} points="' + ' '.join(f'{x(a):.1f},{yf(c):.1f}' for a, c in zip(t[::10], v[::10])) + '"/>'
b1 += [pl(th, eh * 1000, y1, INK, '5 3'), pl(tw, ew * 1000, y1, WINE)]
b2, _, y2 = panel(196, 150, 0, 22, [0, 10, 20], 'position, cm')
b2 += [pl(th, xh * 100, y2, INK, '5 3'), pl(tw, xw * 100, y2, WINE)]
for t in range(0, 5): b2.append(f'<text x="{x(t):.1f}" y="{196+150+16}" {MONO} font-size="10" text-anchor="middle" fill="{MUTED}">{t}</text>')
b2.append(f'<text x="{(L+W-R)/2}" y="{H-8}" {MONO} font-size="10" text-anchor="middle" fill="{MUTED}">time after the command, s</text>')
leg = [f'<line x1="{L+12}" y1="30" x2="{L+36}" y2="30" stroke="{WINE}" stroke-width="1.6"/><text x="{L+42}" y="34" {MONO} font-size="10" fill="{WINE}">waiter: peak {np.abs(ew).max()*1000:.1f} mm</text>',
       f'<line x1="{L+12}" y1="46" x2="{L+36}" y2="46" stroke="{INK}" stroke-width="1.6" stroke-dasharray="5 3"/><text x="{L+42}" y="50" {MONO} font-size="10" fill="{INK}">hand on the same path: peak {np.abs(eh).max()*1000:.1f} mm</text>']
svg = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="A 20 centimetre carry: the waiter keeps the wave at the wall under the rim, a hand moving along the same smooth path does not."><rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>' + ''.join(b1 + b2 + leg) + '</svg>'
open('notes/fig12/figs/waiter.svg', 'w').write(svg); print('wrote notes/fig12/figs/waiter.svg; waiter peak %.2f mm, hand %.2f mm, freeboard %.1f mm' % (np.abs(ew).max()*1e3, np.abs(eh).max()*1e3, fb))
