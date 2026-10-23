"""L4 sensitivity (Gate-1 skeptic objection M1, the gearhead drag the catalogue does not give, and A1, the backdriven
efficiency): the formula (7.6)-(7.7) of L4_generator.py with the friction torque x1, x2, x3 and the efficiency at the sheet
value or 0.5, best catalogue ratio and load each time; also the load voltage peak.  First written by the Gate-1 skeptic
(skeptic-G1-L4-r1.md); adopted and rerun here, extended to all large-rotor mountings.  Run: python3 -I L4_sensitivity.py
(writes L4_sensitivity.json)"""
import math, sys
import os, json; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
import L4_generator as Gm
from scipy.optimize import minimize_scalar
base_T0=Gm.T0
def best(rpm,fr,T0mult,etab=None):
    Gm.T0=base_T0*T0mult
    Om=rpm*2*math.pi/60; rp=fr*56.0/Om; out=[]
    for N,eta,Jg in Gm.RATIOS:
        e=etab if etab else eta
        c_sc=N**2*Gm.KT*Gm.KE/Gm.RC
        r=minimize_scalar(lambda lc:-Gm.powers(Om,rp,N,e,Jg,math.exp(lc))['P_load'],bounds=(math.log(c_sc)-16,math.log(c_sc)-1e-9),method='bounded')
        p=Gm.powers(Om,rp,N,e,Jg,math.exp(r.x)); p['N']=N; p['ce']=math.exp(r.x); p['csc']=c_sc
        if p['Theta']<=0.5: out.append(p)
    b=max(out,key=lambda p:p['P_load'])
    RL=Gm.KT*Gm.KE*b['N']**2/b['ce']-Gm.RC
    V=Gm.KE*b['N']*b['Theta']*Om*RL/(RL+Gm.RC)
    return b['P_load'],b['N'],b['Theta'],b['f']/b['G'],V
res=[]
for rpm,fr in [(r,f) for r in (20,14,8) for f in (0.3,0.6,0.9)]:
    for mult,eb in ((1,None),(2,None),(3,None),(1,0.5),(2,0.5)):
        P,N,Th,fg,V=best(rpm,fr,mult,eb)
        res.append(dict(rpm=rpm,frac=fr,fric=mult,eta=eb,P_load=P,N=N,Theta=Th,V=V))
        print(f'{rpm} rpm {fr}: friction x{mult}, eta {eb or "sheet"}: load {P*1e3:.2f} mW (x{P/37.6e-6:.0f} sensor), N {N}, swing {Th:.3f}, f/G {fg:.2f}, load V peak {V*1e3:.0f} mV')
json.dump(res, open(os.path.join(D, 'L4_sensitivity.json'), 'w'), indent=1)
