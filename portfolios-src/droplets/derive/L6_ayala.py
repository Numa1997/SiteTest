"""L6: Ayala, Rosa and Wang (2008, Part 2) weak-inertia estimate of the turbulent change of the geometric kernel, from the formulas
in dossier-coalescence-turbulence.md (eqs. 2-4, g12 = 1 for size ratio 5), with this study's air and Beard speeds."""
import math
from L1_beard import beard, air
T,p=283.15,85000.0; rho,mu=air(T,p); nu=mu/rho; g=9.81; rw=1000.0
def tau(a): return beard(2*a,T,p)/g      # drag-corrected response time: v = tau g
Rl=2e4; a0=(11+7*Rl)/(205+Rl)
for a1,a2 in [(40e-6,8e-6),(60e-6,8e-6)]:
    t1,t2=tau(a1),tau(a2); v1,v2=beard(2*a1,T,p),beard(2*a2,T,p); R=a1+a2
    wg=math.sqrt(2/math.pi)*math.sqrt(math.pi/8)*abs(t1-t2)*g   # gravity-only <|w_r|> = (1/2)|v1 - v2|
    for eps in [1e-3,1e-2,4e-2]:
        tk=math.sqrt(nu/eps); vk=(nu*eps)**0.25
        s2=R*R*eps/(15*nu)+(t1-t2)**2*a0*(vk/tk)**2+(v1*t1-v2*t2)**2*2*eps/(15*nu)
        w=math.sqrt(2/math.pi)*math.sqrt(s2+math.pi/8*(t1-t2)**2*g*g)
        print(f"{a1*1e6:.0f}/{a2*1e6:.0f} um, eps={eps:g} m2/s3 ({eps*1e4:.0f} cm2/s3): St(large)={t1/tk:.2f}, kernel factor {w/wg:.3f} ({(w/wg-1)*100:+.1f} %)")
