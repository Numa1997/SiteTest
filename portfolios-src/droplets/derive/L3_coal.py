"""L3: collision kinetic energy, surface energy, the Weber number We = CKE / (pi sigma d_c^2), and the coalescence laws."""
import math
from L1_beard import beard, stokes, air, sigma
rw=1000.0
T,p=283.15,85000.0; s=sigma(T)
def pair(a1,a2,law):
    d1,d2=2*a1,2*a2; v=(lambda d: beard(d,T,p)) if law=='beard' else (lambda d: stokes(d,T,p))
    dv=abs(v(d1)-v(d2)); m1=math.pi*rw*d1**3/6; m2=math.pi*rw*d2**3/6
    cke=0.5*m1*m2/(m1+m2)*dv*dv; dc=(d1**3+d2**3)**(1/3); Sc=math.pi*s*dc*dc; St=math.pi*s*(d1*d1+d2*d2)
    We=cke/Sc; Es=math.exp(-1.15*We)
    ET=cke+(St-Sc); dl,ds=max(d1,d2),min(d1,d2)
    ELL=0.778*(1+ds/dl)**-2*math.exp(-2.61e6*s*ET*ET/Sc)
    return dv,cke,Sc,We,Es,ELL,(St-Sc)
print(f"sigma(10 C) = {s:.5f} N/m")
print(" a1/a2 (um)     law     dv(m/s)   CKE(J)     S_c(J)     We        exp(-1.15We)  freed surface/CKE   Low-List(secondary)")
for a1,a2 in [(40,8),(60,8),(100,8),(60,50),(100,50),(200,100),(500,250),(1000,500),(2000,1000)]:
    for law in ['beard','stokes']:
        dv,cke,Sc,We,Es,ELL,dS=pair(a1*1e-6,a2*1e-6,law)
        print(f"{a1:5d}/{a2:<5d} {law:7s} {dv:8.4f}  {cke:.3e}  {Sc:.3e}  {We:.3e}  {Es:.6f}      {dS/cke:10.3g}        {ELL:.3f}")
