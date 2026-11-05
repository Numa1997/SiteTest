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
    ('kD', f"{N['kD']:.1f}", 'in our pint \\(\\lambda D = 6.1\\)'),
    ('z_s mm', f"{N['zs_mm']:.1f}", '\\(Z_s = 137.5\\) mm'),
    ('a mm', f"{N['a_mm']:.1f}", '\\(R = 39.4\\) mm'),
    ('D mm', f"{N['D_mm']:.1f}", '\\(D = 129.5\\) mm'),
    ('lambda_11', f"{N['lam11']:.2f}", '\\(\\lambda_{11} = 47.27\\)'),
    ('f bare', f"{N['f11_bare']:.3f}", '= 3.427\\) Hz'),
    ('f with capillarity', f"{N['f11_cap']:.3f}", 'raises it to 3.445 Hz'),
    ('f with head', f"{N['f11']:.3f}", 'lowers it to 3.244 Hz'),
    ('mu_f,11', f"{N['muf11']:.3f}", '\\(\\kappa_{11} = 0.128\\)'),
    ('capillary fraction %', f"{100*N['cap_ratio']:.1f}", '1.0 % for our pint'),
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
    ('gamma_b', f"{N['gb11']:.3f}", '\\(\\gamma_v\\) is 0.009 per second'),
    ('gamma total', f"{N['gam11']:.2f}", '\\(\\gamma = 0.50\\)'),
    ('tau', f"{N['tau11']:.1f}", 'falls to 1/e in 2.0 s'),
    ('t 5%', f"{N['t5pct']:.1f}", 'to 5 % in 6.0 s'),
    ('no head gamma', f"{N['nohead']['gam']:.2f}", 'the rate is 0.27'),
    ('no head tau', f"{N['nohead']['tau']:.1f}", 'takes 3.7 s and 11.1 s'),
    ('no head 5%', f"{N['nohead']['t5pct']:.1f}", 'takes 3.7 s and 11.1 s'),
    ('clean tau', f"{N['clean']['tau']:.1f}", 'it would be 8.9 s to 1/e'),
    ('brim volume', f"{N['V_brim']:.1f}", 'holds 603.7 mL'),
    ('Faraday measured', '1.21', 'comes out at 1.21 per second'),
    ('hand gain', f"{100*N['hand_gain_f1']:.0f}", 'at \\(\\Omega_h^2/(\\Omega_h^2 + \\omega^2) = 54\\) %'),
    ('tilt share', f"{100*N['tilt_sum_at_wall_over_R']:.0f}", 'reproduce 93 % of the tilt'),
    ('waiter M', f"{N['w_M']:.3f}", '\\(M = 1.523\\) kg'),
    ('stout mass', f"{N['w_ml']:.3f}", 'the stout is 0.503 kg'),
    ('sloshing mass 1', f"{N['w_m1_g']:.0f}", 'sloshing mass is 79 g'),
    ('sloshing masses 2,3', f"{N['w_m2_g']:.1f} g and {N['w_m3_g']:.1f} g", 'the next two 2.2 g and 0.5 g'),
    ('M_e', f"{N['w_Me']:.3f}", '\\(M_e = 1.442\\) kg'),
    ('waiter peak', f"{N['w_peak_mm']:.1f}", 'only 2.6 mm with the waiter'),
    ('hand same path', f"{N['w_hand3_mm']:.1f}", 'the stout rises 8.0 mm'),
    ('waiter arrival', f"{N['w_settle']:.2f}", 'in 1.45 s'),
    ('waiter force', f"{N['w_Fmax']:.1f}", 'at most 2.7 N'),
    ('waiter current', f"{N['w_Imax']:.2f}", '(0.23 A)'),
    ('quick hand', f"{N['w_hand22_mm']:.0f}", 'a wave of 128 mm'),
    ('tau open', f"{N['w_tau_open']:.1f}", 'from 2.0 s to 1.0 s'),
    ('tau closed', f"{N['w_tau_cl']:.1f}", 'from 2.0 s to 1.0 s'),
    ('freeboard', f"{N['w_freeboard_mm']:.1f}", 'passes 4.5 mm'),
    ('m11 cylinder fraction', f"{100*N['m11_cyl_frac']:.0f}", '45 % of a cylinder'),
    ('decay length', f"{N['decay_len_mm']:.0f}", '\\(1/\\lambda = 21\\) mm'),
]
bad = 0
for what, val, ctx in rows:
    ok = ctx in t and val in ctx
    bad += not ok; print(f"{'ok  ' if ok else 'FAIL'} {what:24s} computed {val:>8s}   text: {ctx}")
print('PASS' if not bad else f'FAIL ({bad})', f'{len(rows) - bad}/{len(rows)} quoted numbers match the computation'); sys.exit(1 if bad else 0)
