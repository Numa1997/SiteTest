"""L0 population checks (capture only, Stokes, E = 1, coalescence = 1, finite r).
(a) Monodisperse start: master equation for one collector's capture count n with self-consistent depletion
    dP_n/dt = lam_{n-1} P_{n-1} - lam_n P_n,  lam_n = pi (R_n + r)^2 (v(R_n) - v(r)) n_d(t),  n_d = n_d0 - N_c <n>.
(b) Lognormal thesis modes, capture only (the thesis's collector-and-pool bookkeeping): deterministic mean field."""
import math, numpy as np
from scipy.integrate import solve_ivp
g=9.81; rw=1000.0; Rd=287.05; T=283.15; p=85000.0
rho=p/(Rd*T); mu=1.72e-5*(T/273)**1.5*393/(T+120); k=2*(rw-rho)*g/(9*mu); v=lambda a:k*a*a
m=lambda a:4/3*math.pi*rw*a**3; rad=lambda M:(3*M/(4*math.pi*rw))**(1/3)
r=8e-6; nd0=300e6; Nc=1e6; R0=40e-6; md=m(r); M0=m(R0)
Wtot=nd0*md+Nc*M0; Rm=rad(M0+nd0/Nc*md)
nmax=900
Rn=np.array([rad(M0+n*md) for n in range(nmax)])
Kn=math.pi*(Rn+r)**2*(v(Rn)-v(r))
def rhs(t,P):
    mean=np.dot(np.arange(nmax),P); nd=max(nd0-Nc*mean,0.0)
    lam=Kn*nd; d=-lam*P; d[1:]+=lam[:-1]*P[:-1]; return d
P0=np.zeros(nmax); P0[0]=1
ts=np.linspace(0,3600,3601)
sol=solve_ivp(rhs,[0,3600],P0,t_eval=ts,method='LSODA',rtol=1e-9,atol=1e-14)
Mn=M0+np.arange(nmax)*md
Fc=Nc*(sol.y.T@Mn)/Wtot
t50=np.interp(0.5,Fc,ts); t90=np.interp(0.9,Fc,ts)
i90=int(round(t90)); Pt=sol.y[:,i90]
above=(Rn>Rm)
print(f"(a) master eq.: t50={t50/60:.3f} min, t90={t90/60:.3f} min (L0 finite r: 2.927, 9.192)")
print(f"    at t90: fraction of collector mass above Rm={Rm*1e6:.2f} um: {np.dot(Pt[above],Mn[above])/np.dot(Pt,Mn)*100:.1f} %, mean captures {np.dot(np.arange(nmax),Pt):.1f}")
Pe=sol.y[:,-1]; mean=np.dot(np.arange(nmax),Pe); sd=math.sqrt(np.dot(np.arange(nmax)**2,Pe)-mean**2)
print(f"    at 60 min: mean captures {mean:.1f} +- {sd:.1f}; mass above Rm {np.dot(Pe[above],Mn[above])/np.dot(Pe,Mn)*100:.1f} %; P(R>=65um)={Pe[Rn>=65e-6].sum():.2e}, P(R>=68um)={Pe[Rn>=68e-6].sum():.2e}")
# (b) lognormal modes, capture only, deterministic
def lognorm_bins(N,rg,sg,edges):
    # number per bin from a lognormal in r
    from scipy.stats import norm
    z=(np.log(edges)-math.log(rg))/math.log(sg); return N*np.diff(norm.cdf(z))
s=8; x0=m(1e-6); xs=x0*2**(np.arange(0,400)/s); xs=xs[:np.searchsorted(xs,m(2e-3))+1]
rb=rad(xs); edges=np.sqrt(rb[1:]*rb[:-1]); edges=np.concatenate([[rb[0]**2/edges[0]],edges,[rb[-1]**2/edges[-1]]])
for label,sigc in [('thesis widths',1.2),('collector width 1.1',1.1),('collector width 1.3',1.3)]:
    nd=lognorm_bins(nd0,8e-6,1.25,edges); nc=lognorm_bins(Nc,40e-6,sigc,edges)
    # mass of the modes as on the grid (particles at bin centres)
    keep=nc>1e-12*nc.max(); nc=np.where(keep,nc,0.0)   # populated collector bins only (Stokes collectors beyond 1/Phi blow up)
    def rhs2(t,y):
        Mc=np.minimum(y[:len(rb)],m(1e-3)); ndr=y[len(rb):]
        Rc=rad(np.maximum(Mc,1e-30))
        K=math.pi*(Rc[:,None]+rb[None,:])**2*np.clip(v(Rc)[:,None]-v(rb)[None,:],0,None)*keep[:,None]
        dMc=K@(ndr*xs); dnd=-ndr*(nc@K)
        return np.concatenate([dMc,dnd])
    y0=np.concatenate([xs.copy(),nd])
    sol2=solve_ivp(rhs2,[0,3600],y0,t_eval=ts,rtol=1e-8,atol=1e-20,method='LSODA')
    Wt=np.dot(nd,xs)+np.dot(nc,xs)
    Mc=sol2.y[:len(rb)].T; ndr=sol2.y[len(rb):].T
    Rc=rad(Mc)
    F40=(np.sum(nc*Mc*(Rc>=40e-6),axis=1)+ndr@(xs*(rb>=40e-6)))/Wt
    Fcol=np.sum(nc*Mc,axis=1)/Wt
    tt=lambda F,q: ts[np.argmax(F>=q)]/60
    print(f"(b) {label}: water {Wt*1e3:.4f} g/m3 (droplets {np.dot(nd,xs)*1e3:.4f}, collectors {np.dot(nc,xs)*1e3:.4f}); F40(0)={F40[0]:.4f}")
    print(f"    F40: t50={tt(F40,0.5):.2f} t90={tt(F40,0.9):.2f} min (first recorded minute {math.ceil(tt(F40,0.5))}/{math.ceil(tt(F40,0.9))}); Fc: t50={tt(Fcol,0.5):.2f} t90={tt(Fcol,0.9):.2f} min")
    print(f"    largest collector after 60 min: {Rc[-1][nc>1e-3*nc.max()].max()*1e6:.1f} um (started {rb[nc>1e-3*nc.max()].max()*1e6:.1f} um)")
# (c) closed box, finite r, by quadrature of t(R) = integral dR / (dR/dt): the second numerical route beside solve_ivp
from scipy.integrate import quad
def dRdt(R):   # dM/dt = pi (R+r)^2 (v(R)-v(r)) W(R),  W(R) = N_c (4 pi/3) rho_w (Rm^3 - R^3)
    W=Nc*4/3*math.pi*rw*(Rm**3-R**3)
    return math.pi*(R+r)**2*(v(R)-v(r))*W/(4*math.pi*R*R*rw)
Rq=lambda F:(F*Wtot/(Nc*4/3*math.pi*rw))**(1/3)
for F in (0.5,0.9):
    tq,err=quad(lambda R:1/dRdt(R),R0,Rq(F),epsabs=0,epsrel=1e-12,limit=200)
    print(f"(c) closed box by quad: t{int(F*100)} = {tq/60:.5f} min (error estimate {err:.1e} s)")
# spread of collector radius at t90 in the master equation: a statistic free of any bin grid
mR=np.dot(Pt,Rn); sR=math.sqrt(np.dot(Pt,Rn**2)-mR**2)
print(f"    at t90 = {t90:.1f} s: mean collector radius {mR*1e6:.3f} um, s.d. {sR*1e6:.3f} um")
