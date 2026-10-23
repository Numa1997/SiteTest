"""L3 sag, second shape model (Gate-1 skeptic objection M1): the static gravity deflection integrated directly from the
OpenFAST blade table (shear, moment, curvature M/EI, slope, deflection), with the same 1P factor and g cos 5 deg, once with the
edgewise stiffness alone and once with the in-plane compliance projected through the structural twist; then the same linear
power formula as L3_sag_numbers.py.  First written by the Gate-1 skeptic (skeptic-G1-L3-r1.md); adopted and rerun here.
Run: python3 -I L3_sag_static.py   (writes L3_sag_static.json)"""
import math, sys, json
import numpy as np
import os; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
import nrel5mw as T5
tab=T5.blade_table(); Lb=T5.R_TIP-T5.R_HUB
x=tab[:,0]; tw=np.radians(tab[:,1]); mu=tab[:,2]*T5.ADJ_BL_MS; EIf=tab[:,3]; EIe=tab[:,4]
r=T5.R_HUB+x*Lb
g=9.80665*math.cos(math.radians(5)); Om=0.9494
def cumint_from_tip(f):
    out=np.zeros_like(f)
    for i in range(len(f)-2,-1,-1): out[i]=out[i+1]+0.5*(f[i]+f[i+1])*(r[i+1]-r[i])
    return out
def cumint_from_root(f):
    out=np.zeros_like(f)
    for i in range(1,len(f)): out[i]=out[i-1]+0.5*(f[i]+f[i-1])*(r[i]-r[i-1])
    return out
amp=1/(1-(Om/(2*math.pi*T5.F_EDGE_SYS))**2)
q=mu*g
V=cumint_from_tip(q); M=cumint_from_tip(V)
res=[]
for lab,comp in (('edge only',1/EIe),('twist-projected',np.cos(tw)**2/EIe+np.sin(tw)**2/EIf)):
    slope=cumint_from_root(M*comp); w=cumint_from_root(slope)
    w*=amp; slope*=amp
    print(lab,'tip',round(w[-1],4))
    for frac in (0.3,0.6,0.9):
        rp=frac*T5.R_TIP; wi=np.interp(rp,r,w); si=np.interp(rp,r,slope)
        L=0.2; R=rp/L; G=g/(Om**2*L); k=R-1
        def P(Gf,b):
            B=-b; A=(-Gf+k*1j*B)/(R-1+1j*k); return k*abs(A-B)**2/2
        P0=P(G,0); P1=P(G+2*wi/L,0); P2=P(G+2*wi/L,si)
        res.append(dict(model=lab, frac=frac, w=float(wi), wp=float(si), sag_only=float(P1/P0-1), total=float(P2/P0-1)))
        print(f'  {frac}: w {wi*1e3:.1f} mm slope {si*1e3:.2f} mrad  w\'r/w {si*rp/wi:.2f}; sag only {(P1/P0-1)*100:+.2f} %, total {(P2/P0-1)*100:+.2f} %')
j=json.load(open(D+'/L3_sag.json'))
for e in j: print('modal', e['frac'], round(e['w']*1e3,1),'mm', round(e['wp']*1e3,2),'mrad', 'w\'r/w', round(e['wp']*e['frac']*63/e['w'],2))
json.dump(res, open(os.path.join(D, 'L3_sag_static.json'), 'w'), indent=1)
