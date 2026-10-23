"""Numbers for contract L0, round 2 (answers to skeptic-G1-L0-r1)."""
import math, numpy as np
from scipy.integrate import solve_ivp
g=9.81; rw=1000.0; Rd=287.05; kB=1.380649e-23
T=283.15; p=85000.0
rho=p/(Rd*T); mu=1.72e-5*(T/273)**1.5*393/(T+120); nu=mu/rho
k=2*(rw-rho)*g/(9*mu); v=lambda a:k*a*a; tau=lambda a:2*rw*a*a/(9*mu)
r=8e-6; nd0=300e6; Nc=1e6; R0=40e-6
md=4/3*math.pi*rw*r**3; W=nd0*md
print(f"mu(20C)={1.72e-5*(293.15/273)**1.5*393/(293.15+120):.4e} vs Beard mu0=1.818e-5")
# 1 impaction Stokes number tau_p(r) dv / R
for R in [40e-6,60e-6,100e-6]:
    print(f"impaction St(r=8um, R={R*1e6:.0f}um) = {tau(r)*(v(R)-v(r))/R:.2f}")
# 2 growth time R/Rdot at 40 um, open cloud, finite r, E=1
Rdot=k*W/(4*rw)*(R0+r)**3*(R0-r)/R0**2
print(f"R/Rdot(40um)={R0/Rdot/60:.2f} min; tau_p(40)/(R/Rdot)={tau(R0)/(R0/Rdot):.2e}")
# 3 Poisson CV of the growth time 40 -> 100 um, open cloud (rate per capture lambda = K(R) nd)
M=4/3*math.pi*rw*R0**3; mean=0; var=0; n=0
while True:
    R=(3*M/(4*math.pi*rw))**(1/3)
    if R>=100e-6: break
    lam=math.pi*(R+r)**2*(v(R)-v(r))*nd0
    mean+=1/lam; var+=1/lam**2; M+=md; n+=1
print(f"captures 40->100: {n}, mean time {mean/60:.3f} min, CV {math.sqrt(var)/mean*100:.2f} %")
# 4 bottleneck: share of t* spent 40->60 and 40->100 (r<<R), and with finite r
from math import log
F=lambda R: log((R-r)/(R+r))/(8*r)-(3*R+2*r)/(4*(R+r)**2)
tstar=-F(R0)
for R1 in [60e-6,100e-6]:
    print(f"share of blow-up time spent 40->{R1*1e6:.0f}um: r<<R {1-R0/R1:.3f}, finite r {(F(R1)-F(R0))/tstar:.3f}")
# 5 open-cloud validity: Nc << W/((4pi/3) rho_w R^3) at 100 um
print(f"open-cloud condition: Nc << {W/(4/3*math.pi*rw*(100e-6)**3)/1e6:.3f} cm^-3")
# 6 Brownian Peclet number of the droplet near the collector
D=kB*T/(6*math.pi*mu*r); print(f"D={D:.3e} m2/s, Pe = dv (R+r)/D = {(v(R0)-v(r))*(R0+r)/D:.2e}")
# 7 condensation supply in a saturated updraft vs collection drain (Clausius-Clapeyron with constant L; moist adiabat)
L=2.5e6; Rv=461.5; cp=1005.0; eps=Rd/Rv
es=lambda T: 611.2*math.exp(L/Rv*(1/273.15-1/T))
rs=eps*es(T)/(p-es(T))
Gm=g*(1+L*rs/(Rd*T))/(cp+L*L*rs*eps/(Rd*T*T))
# d rs/dz along the moist adiabat: rs = eps es/(p - es); dp/dz = -rho g; dT/dz = -Gm
dz=1.0; T2=T-Gm*dz; p2=p-rho*g*dz; rs2=eps*es(T2)/(p2-es(T2))
dWdz=-rho*(rs2-rs)/dz
print(f"rs={rs*1e3:.3f} g/kg, moist lapse {Gm*1e3:.2f} K/km, condensation dW/dz={dWdz*1e6:.3f} g/m3/km")
for w in [0.5,1,2]: print(f"  updraft {w} m/s: supply {dWdz*w*60*1e3:.3f} g/m3/min")
drain=Nc*math.pi*(R0+r)**2*(v(R0)-v(r))*W
print(f"collection drain at t=0 (L0 kernel): {drain*60*1e3:.4f} g/m3/min")
rho_moist=(p-es(T))/(Rd*T)+es(T)/(Rv*T); print(f"moist air density {rho_moist:.4f} vs dry {rho:.4f} ({(rho_moist/rho-1)*100:+.2f} %)")
# 8 turbulence ratios for the pair (40, 8) over eps
for e in [1e-3,1e-2,1e-1]:
    tk=math.sqrt(nu/e); aeta=e**0.75*nu**-0.25
    shear=(R0+r)*math.sqrt(e/nu)          # velocity difference across the collision radius at the Kolmogorov shear rate
    inert=abs(tau(R0)-tau(r))*aeta
    print(f"eps={e}: tau_K={tk*1e3:.1f} ms, St(collector)={tau(R0)/tk:.2f}, St(droplet)={tau(r)/tk:.3f}, shear/dv={shear/(v(R0)-v(r)):.4f}, inertial/dv={inert/(v(R0)-v(r)):.3f}")
# 9 fall distance by t90 and swept fraction
print(f"collector fall distance in 9.19 min at 0.197..0.44 m/s: {0.197*9.19*60:.0f} to {0.44*9.19*60:.0f} m; swept volume fraction rate {Nc*math.pi*(R0+r)**2*(v(R0)-v(r))*1e3:.3f}e-3 /s")
