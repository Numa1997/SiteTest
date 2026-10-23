"""L0 numbers from the exact solutions, cross-checked by SciPy integration of the ODE."""
import math
from scipy.integrate import solve_ivp
g=9.81; rw=1000.0; Rd=287.05
T=283.15; p=85000.0
rho_a=p/(Rd*T); mu=1.72e-5*(T/273)**1.5*(273+120)/(T+120)
k=2*(rw-rho_a)*g/(9*mu)
def F(R,r):  # antiderivative of R^2/((R+r)^3 (R-r))
    return math.log((R-r)/(R+r))/(8*r)-(3*R+2*r)/(4*(R+r)**2)
def t_exact(R0,R1,r,W,E=1.0):
    return 4*rw/(E*k*W)*(F(R1,r)-F(R0,r))
def t_small(R0,R1,W,E=1.0):
    c=E*k*W/(4*rw); return (1/R0-1/R1)/c
print(f"k = {k:.4e} 1/(m s)")
for W in [0.3e-3, 300e6*4/3*math.pi*rw*(8e-6)**3]:
    c=k*W/(4*rw)
    print(f"W={W*1e3:.3f} g/m3: t*(r->0)={1/(c*40e-6)/60:.2f} min; 40->100 um: r->0 {t_small(40e-6,100e-6,W)/60:.2f} min, r=8um exact {t_exact(40e-6,100e-6,8e-6,W)/60:.2f} min; t*(r=8um)={4*rw/(k*W)*(0-F(40e-6,8e-6))/60:.2f} min")
    sol=solve_ivp(lambda t,y:[k*W/(4*rw)*(y[0]+8e-6)**3*(y[0]-8e-6)/y[0]**2],[0,3000],[40e-6],events=lambda t,y:y[0]-100e-6,rtol=1e-11,atol=1e-16)
    print(f"   SciPy r=8um 40->100: {sol.t_events[0][0]/60:.4f} min vs exact {t_exact(40e-6,100e-6,8e-6,W)/60:.4f}")
# closed box (thesis cloud, monodisperse), r << R
Nc=1e6; Nd=300e6; r=8e-6; R0=40e-6
md=4/3*math.pi*rw*r**3; M0=4/3*math.pi*rw*R0**3
Wtot=Nd*md+Nc*M0
Rm=((Nd*md+Nc*M0)/(Nc*4/3*math.pi*rw))**(1/3)
def G(R):  # antiderivative of 1/(R^2 (Rm^3-R^3)), real form
    return (R*(-2*math.log(Rm-R)+math.log(R*R+R*Rm+Rm*Rm)-2*math.sqrt(3)*math.atan(math.sqrt(3)*(2*R+Rm)/(3*Rm)))/6-Rm)/(R*Rm**4)
A=k*Nc*math.pi/3   # dR/dt = A R^2 (Rm^3 - R^3)
print(f"closed box: Rm={Rm*1e6:.2f} um, F_c(0)={Nc*M0/Wtot:.4f}")
for Fq in [0.5,0.9]:
    RF=(Fq*Wtot/(Nc*4/3*math.pi*rw))**(1/3)
    te=(G(RF)-G(R0))/A
    sol=solve_ivp(lambda t,y:[A*y[0]**2*(Rm**3-y[0]**3)],[0,1e5],[R0],events=lambda t,y:y[0]-RF,rtol=1e-11,atol=1e-16)
    # finite r with depletion (Delta v = k(R^2-r^2), area (R+r)^2): SciPy only
    sol2=solve_ivp(lambda t,y:[k*(y[0]+r)**2*(y[0]**2-r**2)*(Nc*4/3*math.pi*rw*(Rm**3-y[0]**3))/(4*rw*y[0]**2)],[0,1e5],[R0],events=lambda t,y:y[0]-RF,rtol=1e-11,atol=1e-16)
    print(f"  F_c={Fq}: R={RF*1e6:.2f} um, t exact(r<<R)={te/60:.3f} min, SciPy={sol.t_events[0][0]/60:.3f} min, finite r={sol2.t_events[0][0]/60:.3f} min")
