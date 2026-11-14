"""Fig. 15, generation-1 running example (walls, E = 0.735): the stored 1D twin profile against the exact 1D packet built from
tm.psi_x. Written by the round-2 derivation check (14 Nov 2026); quoted in section 11 of the note. Prints per frame the largest
difference relative to the frame peak (raw) and relative to the run peak, see the variant at the end."""
import sys,numpy as np
sys.path.insert(0,'/home/user/SiteTest/tools/kaggle/resonant-tunnelling')
import read_rt3d,tm
b=open('/home/user/SiteTest/public/data/resonant-tunnelling/2026-11-13/kaggle/runs/dflat_R0_E0.735.bin','rb').read()
h,amp,ph,prof,p1=read_rt3d.read(b)
x=h['prof_x_first']+np.arange(h['prof_nx'])*h['step']
segs=tm.double(2.0,1.0,2.5)
k0=np.sqrt(2*0.735); sx=3.0; sk=1/(2*sx); x0=-20.0
ks=np.linspace(k0-7*sk,k0+7*sk,1401); dk=ks[1]-ks[0]
# initial packet chi0 = N exp(-(x-x0)^2/4sx^2 + i k0 x); Fourier amplitude ~ exp(-(k-k0)^2 sx^2) e^{-i(k-k0)x0}
amp_k=np.exp(-(k-k0)**2*sx**2) if False else None
A=np.exp(-(ks-k0)**2*sx**2)*np.exp(-1j*(ks-k0)*x0)*np.exp(-1j*k0*x0)*0+np.exp(-(ks-k0)**2*sx**2)*np.exp(-1j*ks*x0)
PSI=np.array([tm.psi_x(kk**2/2,segs,x)[0] for kk in ks])  # stationary states, incident e^{ikx}
t=np.arange(h['n'])*h['frame_dt']
inner=(h['prof_nx']//2-max(4,h['prof_nx']//10))*h['step']; m=np.abs(x)<inner
res=[]
c0=None
for f in range(h['n']):
    chi=(A[:,None]*np.exp(-1j*ks[:,None]**2/2*t[f])*PSI).sum(0)*dk
    pe=np.abs(chi)**2
    if c0 is None: c0=1/(pe.sum()*0.5)
    pe=pe*c0
    pt=p1[f]
    d_abs=np.abs(pe[m]-pt[m]).max()/pe[m].max()
    pen=pe[m]/pe[m].sum(); ptn=pt[m]/pt[m].sum()
    d_n=np.abs(pen-ptn).max()/pen.max()
    res.append((t[f],d_abs,d_n,pt.sum()*0.5))
res=np.array(res)
for f in range(0,200,10): print('t %.1f  raw %.3f  normalised %.3f  norm %.3f'%tuple(res[f]))
# variant: relative to global peak; and normalised-by-total relative to frame peak
PE=[];PT=[]
for f in range(h['n']):
    chi=(A[:,None]*np.exp(-1j*ks[:,None]**2/2*t[f])*PSI).sum(0)*dk; PE.append(np.abs(chi)**2*c0); PT.append(p1[f])
PE=np.array(PE)[:,m];PT=np.array(PT)[:,m]; G=PE.max()
d_glob=np.abs(PE-PT).max(1)/G
for f in range(0,200,10): print('t %.1f glob %.4f'%(t[f],d_glob[f]))
print('max glob after t=40:',d_glob[t>40].max(),' during 10-35:',d_glob[(t>10)&(t<35)].max())
fr=np.abs(PE-PT).max(1)/PE.max(1); print('frame-rel max during 10-35',fr[(t>10)&(t<35)].max(),' 35-45',fr[(t>35)&(t<45)].max(),' >45',fr[t>45].max(), 'tend',t[-1])
