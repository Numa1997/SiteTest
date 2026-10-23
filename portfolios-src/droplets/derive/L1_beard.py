"""L1: Beard (1976) three-regime fall speed, independent Python version; comparison with Gunn and Kinzer (1949)."""
import math
g=9.81; rw=1000.0; Rd=287.05
def air(T,p):
    rho=p/(Rd*T); mu=1.72e-5*(T/273)**1.5*393/(T+120); return rho,mu
def sigma(T):
    tau=1-T/647.096; return 0.2358*tau**1.256*(1-0.625*tau)
B2=[-3.18657,0.992696,-1.53193e-3,-9.87059e-4,-5.78878e-4,8.55176e-5,-3.27815e-6]
B3=[-5.00015,5.23778,-2.04914,0.475294,-0.0542819,0.00238449]
def beard(d,T,p,rhop=rw):
    rho,mu=air(T,p); dr=rhop-rho
    l=6.62e-8*(mu/1.818e-5)*(101325/p)*math.sqrt(T/293.15)
    csc=1+2.51*l/d
    if d<19e-6:
        return dr*g/(18*mu)*csc*d*d
    if d<1.07e-3 or rhop!=rw:
        X=math.log(4*rho*dr*g/(3*mu**2)*d**3)
        Re=csc*math.exp(sum(b*X**k for k,b in enumerate(B2)))
        return mu*Re/(rho*d)
    s=sigma(T); Bo=4*dr*g*d*d/(3*s); NP=s**3*rho**2/(mu**4*dr*g)
    X=math.log(Bo*NP**(1/6))
    Re=NP**(1/6)*math.exp(sum(b*X**k for k,b in enumerate(B3)))
    return mu*Re/(rho*d)
def stokes(d,T,p):
    rho,mu=air(T,p); return (rw-rho)*g*d*d/(18*mu)
GK=[(0.1,27),(0.2,72),(0.3,117),(0.4,162),(0.5,206),(0.6,247),(0.7,287),(0.8,327),(0.9,367),(1.0,403),(1.2,464),(1.4,517),(1.6,565),(1.8,609),(2.0,649),(2.2,690),(2.4,727),(2.6,757),(2.8,782),(3.0,806),(3.2,826),(3.4,844),(3.6,860),(3.8,872),(4.0,883),(4.2,892),(4.4,898),(4.6,903),(4.8,907),(5.0,909),(5.2,912),(5.4,914),(5.6,916),(5.8,917)]
T,p=293.15,101325
worst=0; print(" d(mm)  GK(m/s)  Beard   err%   Stokes")
for dmm,v in GK:
    d=dmm*1e-3; vb=beard(d,T,p); e=(vb/(v/100)-1)*100
    if dmm>=0.3: worst=max(worst,abs(e))
    print(f"{dmm:5.1f}  {v/100:6.2f}  {vb:6.3f}  {e:+6.2f}  {stokes(d,T,p):8.3f}")
print(f"largest |error| for d >= 0.3 mm: {worst:.2f} %")
# joints
for dj in [19e-6,1.07e-3]:
    for TT,pp in [(283.15,85000),(293.15,101325)]:
        rho,mu=air(TT,pp); dr=rw-rho; l=6.62e-8*(mu/1.818e-5)*(101325/pp)*math.sqrt(TT/293.15); csc=1+2.51*l/dj
        if dj<1e-4:
            a=dr*g/(18*mu)*csc*dj*dj; X=math.log(4*rho*dr*g/(3*mu**2)*dj**3); b=mu*csc*math.exp(sum(c*X**k for k,c in enumerate(B2)))/(rho*dj)
        else:
            X=math.log(4*rho*dr*g/(3*mu**2)*dj**3); a=mu*csc*math.exp(sum(c*X**k for k,c in enumerate(B2)))/(rho*dj)
            s=sigma(TT); Bo=4*dr*g*dj*dj/(3*s); NP=s**3*rho**2/(mu**4*dr*g); Y=math.log(Bo*NP**(1/6)); b=mu*NP**(1/6)*math.exp(sum(c*Y**k for k,c in enumerate(B3)))/(rho*dj)
        print(f"joint d={dj*1e6:.0f} um at {TT-273.15:.0f} C {pp/100:.0f} hPa: below {a:.5f}, above {b:.5f} m/s, jump {(b/a-1)*100:+.3f} %")
print("10 C, 850 hPa:")
for r in [8e-6,10e-6,20e-6,40e-6,41e-6,50e-6,60e-6,100e-6,200e-6,500e-6,1e-3]:
    d=2*r; vb=beard(d,283.15,85000); vs=stokes(d,283.15,85000); rho,mu=air(283.15,85000)
    print(f"r={r*1e6:6.0f} um  Beard {vb:.4f} m/s  Stokes {vs:.4f}  ratio S/B {vs/vb:.3f}  Re {2*r*rho*vb/mu:.3f}")
