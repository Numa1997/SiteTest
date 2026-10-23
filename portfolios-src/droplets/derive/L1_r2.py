"""Every number of contract L1, round 2. Uses L1_beard.py's Beard implementation (independent of physics.cjs)."""
import math, numpy as np
from scipy.integrate import solve_ivp, quad
from L1_beard import beard, stokes, air, sigma, B2, GK
g=9.81; rw=1000.0
T,p=283.15,85000.0; rho,mu=air(T,p); nu=mu/rho
vS=lambda a: stokes(2*a,T,p); vB=lambda a: beard(2*a,T,p)
print(f"air: rho={rho:.4f} mu={mu:.4e}")
# Stokes' own Re = 1 and Beard's Re = 1
from scipy.optimize import brentq
aS=brentq(lambda a:2*a*rho*vS(a)/mu-1,1e-6,1e-4); aB=brentq(lambda a:2*a*rho*vB(a)/mu-1,1e-6,1e-4)
print(f"Re=1: Stokes speed at a={aS*1e6:.1f} um, Beard speed at a={aB*1e6:.1f} um")
for a in [20,30,40,60,100,146]:
    A=a*1e-6; print(f"a={a} um: vS/vB={vS(A)/vB(A):.3f}, Re_B={2*A*rho*vB(A)/mu:.2f}")
# local exponent d ln v / d ln a (Beard)
for a1,a2 in [(40,60),(60,100),(100,200),(200,500)]:
    print(f"exponent {a1}-{a2} um: {math.log(vB(a2*1e-6)/vB(a1*1e-6))/math.log(a2/a1):.2f}")
# Oseen at the fit's low end: ln Re = sum b X^k vs Stokes Re = N/24 and Oseen Re(1+3Re/16) = N/24
for X in [0.0,-1.1,-2,-4]:
    N=math.exp(X); Rfit=math.exp(sum(b*X**k for k,b in enumerate(B2))); RS=N/24
    Ros=brentq(lambda R:R*(1+3*R/16)-N/24,1e-12,10)
    print(f"X=ln N_Da={X}: Re_fit/Re_Stokes={Rfit/RS:.4f}, Oseen/Stokes={Ros/RS:.4f}")
# Open cloud 40 -> 100 um, E = 1, finite r = 8 um, W = 0.643 g/m3
r=8e-6; W=300e6*4/3*math.pi*rw*r**3
def topen(v):
    f=lambda R: 4*rw*R*R/(W*(R+r)**2*(v(R)-v(r)))
    return quad(f,40e-6,100e-6,epsrel=1e-11,limit=200)[0]
tS,tB=topen(vS),topen(vB)
print(f"open cloud 40->100 um: Stokes {tS:.1f} s ({tS/60:.2f} min), Beard {tB:.1f} s ({tB/60:.2f} min), ratio {tB/tS:.4f}")
rat=[(vS(a)-vS(r))/(vB(a)-vB(r)) for a in np.linspace(40e-6,100e-6,601)]
print(f"   bound: ratio of relative speeds over 40-100 um in [{min(rat):.3f}, {max(rat):.3f}]")
# Closed box: 1 cm-3 collectors of 40 um, 300 cm-3 droplets of 8 um; F_c = water in collectors / total
Nc=1e6; M0=4/3*math.pi*rw*(40e-6)**3; md=4/3*math.pi*rw*r**3; Wt=300e6*md+Nc*M0
Rm=((M0+300*md)/(4/3*math.pi*rw))**(1/3)
def tbox(v,F):
    RF=(F*Wt/(Nc*4/3*math.pi*rw))**(1/3)
    f=lambda R: 4*rw*R*R/((R+r)**2*(v(R)-v(r))*Nc*4/3*math.pi*rw*(Rm**3-R**3))
    return quad(f,40e-6,RF,epsrel=1e-11,limit=200)[0], RF
for F in [0.5,0.9]:
    (a,RF),(b,_)=tbox(vS,F),tbox(vB,F)
    rr=[(vS(x)-vS(r))/(vB(x)-vB(r)) for x in np.linspace(40e-6,RF,401)]
    print(f"closed box F_c={F} (R={RF*1e6:.2f} um): Stokes {a:.1f} s, Beard {b:.1f} s, ratio {b/a:.4f}; exact bound [{min(rr):.3f}, {max(rr):.3f}]")
# Gunn and Kinzer split
errs=[(d,(beard(d*1e-3,293.15,101325)/(v/100)-1)*100) for d,v in GK]
ins=[e for d,e in errs if d>=1.2]; out=[e for d,e in errs if 0.3<=d<=1.0]; low=[e for d,e in errs if d<0.3]
print(f"G&K in sample (1.2-5.8 mm, regime 3): max |err| {max(abs(e) for e in ins):.2f} %")
print(f"G&K out of sample (0.3-1.0 mm): errors {', '.join(f'{e:+.2f}' for e in out)} %")
print(f"G&K study range (0.1, 0.2 mm): {', '.join(f'{e:+.2f}' for e in low)} %")
print(f"Beard & Pruppacher 1969 (secondary) 25.6 cm/s at 0.10 mm vs Beard {beard(1e-4,293.15,101325)*100:.2f} cm/s: {(0.256/beard(1e-4,293.15,101325)-1)*100:+.1f} %")
# regime 2 range Beard checked: 20 um to 1 mm at 20 C, 1 atm -> N_Da range; same N_Da at 10 C, 850 hPa
r20,m20=air(293.15,101325); C20=4*r20*(rw-r20)*g/(3*m20**2); C10=4*rho*(rw-rho)*g/(3*mu**2)
print(f"N_Da range of Beard's check: {C20*(20e-6)**3:.3f} to {C20*(1e-3)**3:.0f}; at 10 C, 850 hPa: d = {(C20*(20e-6)**3/C10)**(1/3)*1e6:.1f} um to {(C20*(1e-3)**3/C10)**(1/3)*1e3:.3f} mm")
# rigid sphere at 3 mm with Langmuir's constant drag C0 = 0.40 vs Gunn-Kinzer C_D = 0.503 (their Table 2)
print(f"3 mm: rigid sphere with C_D = 0.40 would fall sqrt(0.503/0.40) = {math.sqrt(0.503/0.40):.3f} times faster than measured")
# internal circulation (Hadamard-Rybczynski), kappa = mu_w/mu_a with mu_w(10 C) ~ 1.306e-3 Pa s (standard value)
kap=1.306e-3/mu; print(f"Hadamard-Rybczynski: kappa={kap:.1f}, speed factor 1+1/(2+3 kappa) = {1+1/(2+3*kap):.4f}")
# saturated air effect on v
es=611.2*math.exp(2.5e6/461.5*(1/273.15-1/T)); rhom=(p-es)/(287.05*T)+es/(461.5*T)
def beard_rho(d,rh):
    dr=rw-rh; l=6.62e-8*(mu/1.818e-5)*(101325/p)*math.sqrt(T/293.15); csc=1+2.51*l/d
    X=math.log(4*rh*dr*g/(3*mu**2)*d**3); return mu*csc*math.exp(sum(b*X**k for k,b in enumerate(B2)))/(rh*d)
for a in [40e-6,100e-6]: print(f"saturated air: v({a*1e6:.0f} um) changes {(beard_rho(2*a,rhom)/beard_rho(2*a,rho)-1)*100:+.3f} %")
# slip at 40 um: C_sc - 1 on v
l=6.62e-8*(mu/1.818e-5)*(101325/p)*math.sqrt(T/293.15)
print(f"slip: C_sc(d=80 um)-1 = {2.51*l/80e-6*100:.3f} %, C_sc(d=16 um)-1 = {2.51*l/16e-6*100:.2f} %")
# Bond number at d = 200 um (deformation irrelevant below regime 3)
print(f"Bo(d=200 um) = {4*(rw-rho)*g*(200e-6)**2/(3*sigma(T)):.4f}, Bo(d=1.07 mm) = {4*(rw-rho)*g*(1.07e-3)**2/(3*sigma(T)):.3f}")
# standard Sutherland vs the thesis's constants at 10 C
mus=1.716e-5*(T/273.15)**1.5*(273.15+110.4)/(T+110.4); print(f"standard Sutherland mu={mus:.4e}, thesis constants {mu:.4e}: {(mu/mus-1)*100:+.2f} %")

print("\n--- round 3 additions: every remaining number of contract L1 ---")
print(f"mean free path l = {l*1e6:.4f} um; Knudsen 2l/d at d = 16 um: {2*l/16e-6:.4f}")
print(f"tau_p(40 um) = {2*rw*(40e-6)**2/(9*mu)*1e3:.2f} ms")
sp=(300e6)**(-1/3); print(f"droplet spacing n^-1/3 = {sp*1e3:.3f} mm = {sp/8e-6:.0f} droplet radii = {sp/40e-6:.0f} radii of a 40 um collector = {sp/100e-6:.0f} of a 100 um drop")
print(f"Oseen length nu/v at 40 um: {nu/vB(40e-6)*1e6:.0f} um")
r20,m20=air(293.15,101325)
print(f"Bo(d = 3 mm, 20 C) = {4*(rw-r20)*g*(3e-3)**2/(3*sigma(293.15)):.3f}")
X=math.log(4*rho*(rw-rho)*g/(3*mu**2)*(2e-4)**3); print(f"seven terms of the fit at d = 0.2 mm, 10 C, 850 hPa (ln N_Da = {X:.3f}): " + ", ".join(f"{b*X**k:.2f}" for k,b in enumerate(B2)))
# L0 blow-up (r << R, Stokes, E = 1, W = 0.643 g/m3) from 40 um
kS=2*(rw-rho)*g/(9*mu); W=300e6*4/3*math.pi*rw*(8e-6)**3; print(f"L0 blow-up time from 40 um (r << R): {4*rw/(kS*W*40e-6):.1f} s")
# drag exponent n in F ~ v^n at given Re from Beard's fit: n = 1/(d ln Re / d ln N_Da) ... computed numerically from v(a)
def dragexp(a):
    # at fixed size, F = weight; along the fit, N_Da ~ C_D Re^2 and F ~ C_D Re^2 at fixed a: n = d ln(C_D Re^2)/d ln Re = d ln N_Da / d ln Re
    X0=math.log(4*rho*(rw-rho)*g/(3*mu**2)*(2*a)**3); h=1e-4
    Y=lambda X: sum(b*X**k for k,b in enumerate(B2))
    return 1/((Y(X0+h)-Y(X0-h))/(2*h))
for a in [40e-6,100e-6]:
    n=dragexp(a); print(f"drag exponent at a = {a*1e6:.0f} um (Re = {2*a*rho*vB(a)/mu:.2f}): F ~ v^{n:.2f}; doubling v multiplies the drag by {2**n:.2f}")
for mh in [2,10,14]:
    print(f"spoon in honey (mu = {mh} Pa s, rho = 1400 kg/m3, 1 cm, 1 cm/s): Re = {1400*0.01*0.01/mh:.3f}; in water (1 mm^2/s... mu = 1e-3, 1 m/s): Re = {1000*1*0.01/1e-3:.0f}")
# open-cloud rate exponent of (R+r)^2 (v(R)-v(r))/R^2 with r = 8 um, Beard
rate=lambda R:(R+8e-6)**2*(vB(R)-vB(8e-6))/R**2
for a1,a2 in [(40,50),(40,60),(60,80),(80,100)]:
    print(f"growth-rate exponent d ln(dR/dt)/d ln R, {a1}-{a2} um: {math.log(rate(a2*1e-6)/rate(a1*1e-6))/math.log(a2/a1):.2f}")
# Gunn and Kinzer with their 50 % RH air (density from the partial pressure of vapour)
Tg,pg=293.15,101325; es20=611.2*math.exp(2.5e6/461.5*(1/273.15-1/Tg)); e=0.5*es20
rho50=(pg-e)/(287.05*Tg)+e/(461.5*Tg)
def beard_air(d,rh,mu_,T_,p_):
    dr=rw-rh; l_=6.62e-8*(mu_/1.818e-5)*(101325/p_)*math.sqrt(T_/293.15); csc=1+2.51*l_/d
    if d<19e-6: return dr*g/(18*mu_)*csc*d*d
    if d<1.07e-3:
        Xg=math.log(4*rh*dr*g/(3*mu_**2)*d**3); return mu_*csc*math.exp(sum(b*Xg**k for k,b in enumerate(B2)))/(rh*d)
    s=sigma(T_); Bo=4*dr*g*d*d/(3*s); NP=s**3*rh**2/(mu_**4*dr*g); Yg=math.log(Bo*NP**(1/6))
    from L1_beard import B3
    return mu_*NP**(1/6)*math.exp(sum(b*Yg**k for k,b in enumerate(B3)))/(rh*d)
mu20=air(293.15,101325)[1]
e50=[(dd,(beard_air(dd*1e-3,rho50,mu20,Tg,pg)/(vv/100)-1)*100) for dd,vv in GK]
print(f"G&K with 50 % RH air (rho = {rho50:.4f} vs dry {r20:.4f}, {(rho50/r20-1)*100:+.3f} %):")
print("   in sample (1.2-5.8 mm) max |err| = %.2f %%; 2.4 mm: %+.2f %%" % (max(abs(x) for d,x in e50 if d>=1.2), dict(e50)[2.4]))
print("   out of sample (0.3-1.0 mm): " + ", ".join(f"{x:+.2f}" for d,x in e50 if 0.3<=d<=1.0) + " %")
print("   study range (0.1, 0.2 mm): " + ", ".join(f"{x:+.2f}" for d,x in e50 if d<0.3) + " %")
vbp=beard_air(1e-4,(pg-es20)/(287.05*Tg)+es20/(461.5*Tg),mu20,Tg,pg)
print(f"Beard at 0.1 mm in saturated air (as Beard and Pruppacher measured): {vbp*100:.2f} cm/s; 25.6 cm/s (search excerpt) is {(0.256/vbp-1)*100:+.2f} % above")
