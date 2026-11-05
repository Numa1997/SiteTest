"""Every number the Fig. 12 note quotes, recomputed (notes/fig12/numbers.json, from tools/fig12/note_numbers.py) and found in the page.
Usage: python3 tools/fig12/check_note_numbers.py  -> one line per number, PASS/FAIL at the end."""
import json, re, html, sys
N = json.load(open('notes/fig12/numbers.json'))
s = open('public/simulations/beer-slosh.html').read(); a = s.index('<article class="paper"'); b = s.index('</article>', a)
t = html.unescape(re.sub(r'<svg.*?</svg>', ' ', s[a:b], flags=re.S))
fv = {int(r[0]): r for r in N['f_vs_V']}
rows = [  # (what, formatted computed value, text that must contain it)
    ('delta Stokes, mm', f"{N['delta_stokes_mm']:.2f}", 'this is \\(\\delta = 0.45\\) mm'),
    ('omega_11 rad/s', f"{2*3.141592653589793*N['f11']:.1f}", '\\(\\omega = 20.4\\) rad/s'),
    ('kD', f"{N['kD']:.1f}", 'in our pint \\(kD = 6.1\\)'),
    ('z_s mm', f"{N['zs_mm']:.1f}", '\\(z_s = 137.5\\) mm'),
    ('a mm', f"{N['a_mm']:.1f}", '\\(a = 39.4\\) mm'),
    ('D mm', f"{N['D_mm']:.1f}", '\\(D = 129.5\\) mm'),
    ('lambda_11', f"{N['lam11']:.2f}", '\\(\\lambda_{11} = 47.27\\)'),
    ('f bare', f"{N['f11_bare']:.3f}", '= 3.427\\) Hz'),
    ('f with capillarity', f"{N['f11_cap']:.3f}", 'raises it to 3.445 Hz'),
    ('f with head', f"{N['f11']:.3f}", 'lowers it to 3.244 Hz'),
    ('mu_f,11', f"{N['muf11']:.3f}", '\\(\\mu_{f,11} = 0.128\\)'),
    ('capillary fraction %', f"{100*N['cap_ratio']:.1f}", 'that is 1.0 % in'),
    ('M_f', f"{N['Mf']:.2f}", '\\(M_f = \\varepsilon_f\\rho h_f = 2.72\\)'),
    ('nu', f"{N['nu']*1e6:.2f}", '2.05\\times10^{-6}'),
    ('f tulip 300', f"{fv[300][1]:.2f}", '(3.14 against 3.25 Hz at 300 mL)'),
    ('f cyl 300', f"{fv[300][2]:.2f}", '(3.14 against 3.25 Hz at 300 mL)'),
    ('f tulip 590', f"{fv[590][1]:.2f}", '(3.37 against 3.30 Hz at 590 mL)'),
    ('f cyl 590', f"{fv[590][2]:.2f}", '(3.37 against 3.30 Hz at 590 mL)'),
    ('acc at resonance', f"{N['acc_res']:.3f}", '\\(A\\omega^2 = 0.083\\)'),
    ('resonant amplitude', f"{N['A_res_mm']:.1f}", 'the steady wave at the wall is 5.6 mm'),
    ('Faraday threshold', f"{N['faraday_amin_mm']:.2f}", 'the threshold is \\(A = 0.58\\) mm'),
    ('Faraday predicted gain', f"{N['faraday_A2mm_gain']:.1f}", 'predicts a net growth rate of 1.2 per second'),
    ('theory coefficient', f"{N['delta_theory_coef']:.2f}", '3.50\\,\\nu^{1/2}'),
    ('ratio 4.98/3.50', f"{4.98/N['delta_theory_coef']:.2f}", '1.42 times the clean-wall theory'),
    ('gamma_b', f"{N['gb11']:.3f}", 'it is 0.009 per second'),
    ('gamma total', f"{N['gam11']:.2f}", '\\(\\gamma = 0.50\\)'),
    ('tau', f"{N['tau11']:.1f}", 'falls to 1/e in 2.0 s'),
    ('t 5%', f"{N['t5pct']:.1f}", 'to 5 % in 6.0 s'),
    ('no head gamma', f"{N['nohead']['gam']:.2f}", 'the rate is 0.27'),
    ('no head tau', f"{N['nohead']['tau']:.1f}", 'takes 3.7 s and 11.1 s'),
    ('no head 5%', f"{N['nohead']['t5pct']:.1f}", 'takes 3.7 s and 11.1 s'),
    ('clean tau', f"{N['clean']['tau']:.1f}", 'it would be 8.9 s'),
    ('brim volume', f"{N['V_brim']:.1f}", 'holds 603.7 mL'),
    ('Faraday measured', '1.21', 'grows at 1.21 per second'),
    ('decay length', f"{N['decay_len_mm']:.0f}", '\\(1/\\lambda = 21\\) mm'),
]
bad = 0
for what, val, ctx in rows:
    ok = ctx in t and val in ctx
    bad += not ok; print(f"{'ok  ' if ok else 'FAIL'} {what:24s} computed {val:>8s}   text: {ctx}")
print('PASS' if not bad else f'FAIL ({bad})', f'{len(rows) - bad}/{len(rows)} quoted numbers match the computation'); sys.exit(1 if bad else 0)
