"""L4 sensitivity (the gearhead drag the catalogue does not give, and the backdriven
efficiency): the formula (7.6)-(7.7) of L4_generator.py with the friction torque x1, x2, x3 and the efficiency at the sheet
value or 0.5, best catalogue ratio and load each time; also the load voltage peak.
The nine mountings of setup.py.  Run: python3 -I L4_sensitivity.py
(writes L4_sensitivity.json)"""
import math, sys
import os, json; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
import L4_generator as Gm
import setup as S
NEED=json.load(open(os.path.join(D,'sensor.json')))['need_uW']*1e-6
base_T0=Gm.T0
def best(Om,rp,T0mult,etab=None):
    Gm.T0=base_T0*T0mult
    out=[]
    for N,eta,Jg in Gm.RATIOS:
        e=etab if etab else eta
        c_sc=N**2*Gm.KT*Gm.KE/Gm.RC
        ce=Gm.best_brake(Om,rp,N,e,Jg)
        if ce is None: continue
        p=Gm.powers(Om,rp,N,e,Jg,ce); p['N']=N; p['ce']=ce; p['csc']=c_sc; out.append(p)
    b=max(out,key=lambda p:p['P_load'])
    RL=Gm.KT*Gm.KE*b['N']**2/b['ce']-Gm.RC
    V=Gm.KE*b['N']*b['Theta']*Om*RL/(RL+Gm.RC)
    return b['P_load'],b['N'],b['Theta'],b['f']/b['G'],V
res=[]
for v,fr,Om,rp in S.mountings():
    for mult,eb in ((1,None),(2,None),(3,None),(1,0.5),(2,0.5)):
        P,N,Th,fg,V=best(Om,rp,mult,eb)
        res.append(dict(wind=v,rpm=S.rpm(v),frac=fr,fric=mult,eta=eb,P_load=P,N=N,Theta=Th,V=V))
        print(f'{v:.0f} m/s {fr}: friction x{mult}, eta {eb or "sheet"}: load {P*1e3:.2f} mW (x{P/NEED:.0f} sensor), N {N}, swing {Th:.3f}, f/G {fg:.2f}, load V peak {V*1e3:.0f} mV')
json.dump(res, open(os.path.join(D, 'L4_sensitivity.json'), 'w'), indent=1)
