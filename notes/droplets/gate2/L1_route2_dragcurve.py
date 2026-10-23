"""Gate 2, L1, route 2 (numerical): (2.4)/(2.5) against an INDEPENDENT drag law (Schiller-Naumann C_D = 24/Re (1+0.15 Re^0.687), Re<1000),
solved by root finding on (2.4); and the text's quoted numbers (Stokes too fast by 11/27/69 %, doubling the speed multiplies the drag by 2.44)."""
import json, numpy as np
from scipy.optimize import brentq
D = json.load(open('L1_model_dump.json'))
rho_w, g = 1000.0, 9.81
def v_drag_balance(a, A, CD):
    d = 2 * a; dr = rho_w - A['rho']
    f = lambda v: 4 / 3 * np.pi * a**3 * dr * g - 0.5 * A['rho'] * v**2 * np.pi * a**2 * CD(A['rho'] * v * d / A['mu'])
    return brentq(f, 1e-9, 50.0, xtol=1e-14, rtol=1e-13)
SN = lambda Re: 24 / Re * (1 + 0.15 * Re**0.687)
for name in ['cloud', 'std20']:
    A = D[name]['air']; print('== air:', name, ' rho_a=%.4f mu=%.4e' % (A['rho'], A['mu']))
    print('  a(um)   v_Stokes   v_(2.4)+SchillerNaumann   v_model(Beard)   Beard/SN-1   Stokes/Beard-1   N_Da (2.5)    Re(Beard)  C_D(Beard)=N_Da/Re^2')
    for row in D[name]['rows']:
        a = row['a_um'] * 1e-6
        if row['a_um'] > 500: continue
        vsn = v_drag_balance(a, A, SN)
        d = 2 * a; NDa = 4 * A['rho'] * (rho_w - A['rho']) * g * d**3 / (3 * A['mu']**2)
        Re = A['rho'] * row['vB'] * d / A['mu']
        # (2.4) with C_D := N_Da/Re^2 must return the model's own weight=drag balance
        bal = 0.5 * A['rho'] * row['vB']**2 * np.pi * a**2 * NDa / Re**2 / (4 / 3 * np.pi * a**3 * (rho_w - A['rho']) * g)
        print('  %5.0f  %9.5f  %9.5f  %9.5f  %+7.3f%%  %+7.1f%%  %11.4g  %8.3f  %8.3f   balance ratio %.12f' % (row['a_um'], row['vS'], vsn, row['vB'], 100 * (row['vB'] / vsn - 1), 100 * (row['vS'] / row['vB'] - 1), NDa, Re, NDa / Re**2, bal))
# the 2.44: F(2v)/F(v) at a = 100 um in cloud air with the model's curve C_D(Re) (parametrised through the size) and with SN
A = D['cloud']['air']
import subprocess
rows = D['cloud']['rows']
a100 = 100e-6; d = 2 * a100
vB = [r for r in rows if r['a_um'] == 100][0]['vB']
Re1 = A['rho'] * vB * d / A['mu']
# C_D(Re) of the model's curve: need v_B at arbitrary sizes -> ask node
def vB_at(a_um):
    return float(subprocess.run(['node', '-e', "const P=require('/home/user/SiteTest/portfolios-src/droplets/physics.cjs');const A=P.air(283.15,85000);console.log(P.vBeard(%g*1e-6,A))" % a_um], capture_output=True, text=True).stdout)
def CD_model(Re_target):
    f = lambda a_um: A['rho'] * vB_at(a_um) * 2 * a_um * 1e-6 / A['mu'] - Re_target
    a_um = brentq(f, 20, 600, xtol=1e-6)
    dd = 2 * a_um * 1e-6; NDa = 4 * A['rho'] * (rho_w - A['rho']) * g * dd**3 / (3 * A['mu']**2)
    return NDa / Re_target**2
ratio_model = 4 * CD_model(2 * Re1) / CD_model(Re1)
ratio_SN = 4 * SN(2 * Re1) / SN(Re1)
print('doubling the speed of a 100 um drop (Re = %.2f): drag ratio = 4 C_D(2Re)/C_D(Re): model curve %.3f ; Schiller-Naumann %.3f ; (text 2.44)' % (Re1, ratio_model, ratio_SN))
print('   honey world 2^1 = 2, water world 2^2 = 4; position of %.2f between them = %.0f %%' % (ratio_model, 100 * (ratio_model - 2) / 2))
# local exponent n = d ln F / d ln v = 2 + d ln C_D / d ln Re (central difference over +-1 % in Re), and 2**n
h = 0.01
nloc_model = 2 + (np.log(CD_model(Re1 * (1 + h))) - np.log(CD_model(Re1 * (1 - h)))) / (np.log(1 + h) - np.log(1 - h))
nloc_SN = 2 + (np.log(SN(Re1 * (1 + h))) - np.log(SN(Re1 * (1 - h)))) / (np.log(1 + h) - np.log(1 - h))
print('local exponent n = dlnF/dlnv at 100 um: model curve %.3f (2^n = %.3f) ; Schiller-Naumann %.3f (2^n = %.3f)' % (nloc_model, 2**nloc_model, nloc_SN, 2**nloc_SN))
print('   so "2.44" is 2^n with the local exponent n; the exact factor for a finite doubling along the curve is %.3f' % ratio_model)
