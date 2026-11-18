# Independent 1D stationary scattering (hbar=m=1): piecewise-constant V, transfer of (psi, psi') across each segment, vectorised over E.
import numpy as np
def T_of_E(E, segs, VL=0.0, VR=0.0):
    """segs: list of (x_left, x_right, V) in increasing x, contiguous or not (gaps are V=VL? no: gaps take value 'gapV')."""
    E=np.asarray(E,complex)
    # state vector (psi, dpsi) propagated from right to left; start with transmitted wave e^{i kR x} at x = x_end
    kR=np.sqrt(2*(E-VR)); kL=np.sqrt(2*(E-VL))
    xs=segs[-1][1]
    psi=np.exp(1j*kR*xs); dpsi=1j*kR*psi
    for (a,b,V) in reversed(segs):
        q=np.sqrt(2*(E-V)+0j); L=b-a
        # propagate backwards from b to a: psi(a) = cos(qL) psi(b) - sin(qL)/q dpsi(b); dpsi(a) = q sin(qL) psi(b) + cos(qL) dpsi(b)
        c=np.cos(q*L); s=np.where(abs(q)>1e-12, np.sin(q*L)/np.where(abs(q)>1e-12,q,1), L)
        qs=q*np.sin(q*L)
        psi, dpsi = c*psi - s*dpsi, qs*psi + c*dpsi
    xa=segs[0][0]
    # at xa: psi = A e^{ikL x} + B e^{-ikL x}
    A=(psi + dpsi/(1j*kL))/2*np.exp(-1j*kL*xa)
    t=1/A
    return (kR.real/kL.real)*abs(t)**2
def build(sp, nramp=4000):
    D,P,N,V0,b=sp['D'],sp['P'],sp['N'],sp['V0'],sp.get('bias',0.0)
    # centres as in the solver (c=0 or 0.25 shifts only the origin; T is shift invariant)
    cs=[(k-(N-1)/2)*P for k in range(N)]
    xl,xr=cs[0]-D/2,cs[-1]+D/2
    if not b:
        segs=[]
        for i,c in enumerate(cs):
            segs.append((c-D/2,c+D/2,V0))
            if i<N-1: segs.append((c+D/2,cs[i+1]-D/2,0.0))
        return segs,0.0
    faces=sorted([c-D/2 for c in cs]+[c+D/2 for c in cs]); segs=[]
    for a0,b0 in zip(faces[:-1],faces[1:]):
        m0=(a0+b0)/2; Vb=V0 if any(abs(m0-c)<D/2 for c in cs) else 0.0
        n=max(4,int(round(nramp*(b0-a0)/(xr-xl)))); xg=np.linspace(a0,b0,n+1)
        for a,bb in zip(xg[:-1],xg[1:]):
            m=(a+bb)/2; segs.append((a,bb,Vb-b*(m-xl)/(xr-xl)))
    return segs,-b
def packet_T(sp, nk=4001, nramp=4000):
    segs,VR=build(sp,nramp); k0=np.sqrt(2*sp['E']); sk=1/(2*sp['sx'])
    k=np.linspace(max(1e-4,k0-8*sk),k0+8*sk,nk); w=np.exp(-(k-k0)**2/(2*sk**2)); w/=w.sum()
    return float((w*T_of_E(k**2/2,segs,0.0,VR)).sum())
if __name__=='__main__':
    # check: single barrier analytic
    E=np.array([0.5,1.0,2.5]); V0=2.0; d=1.0
    kap=np.sqrt(2*(V0-E)+0j); k=np.sqrt(2*E)
    Ta=1/(1+ (V0**2*np.sinh(kap*d)**2)/(4*E*(V0-E)))
    print('analytic',Ta.real,' mine',T_of_E(E,[(0,d,V0)]))
