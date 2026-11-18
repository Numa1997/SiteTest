# My own 1D twin of rt3d2 (same rules: Strang split-step, spectral kinetic, V sampled on grid points strictly inside, sin^(1/8)
# border on outer tenth, packet start x0 = first face - max(14, 4 sx)); box length fixed at 96 a; dx free.
# Faces must fall between grid points: the structure is shifted by s so that every face sits on a half-cell.
import numpy as np
def twin(sp, t_end, dx=0.5, dt=0.01, L=96.0):
    n=int(round(L/dx)); x=(np.arange(n)-n//2)*dx; k=2*np.pi*np.fft.fftfreq(n,dx)
    W=max(4,n//10); m=np.ones(n); e=np.arange(W); m[:W]=np.sin(0.5*np.pi*e/W)**0.125; m[-W:]=m[:W][::-1]
    N,P,D,V0,b=sp['N'],sp['P'],sp['D'],sp['V0'],sp.get('bias',0.0)
    cs=np.array([(j-(N-1)/2)*P for j in range(N)]); f0=cs[0]-D/2
    s=(np.floor(f0/dx)+0.5)*dx-f0; cs=cs+s          # first face on a half-cell; all faces then are (D, P multiples of dx assumed)
    faces=np.concatenate([cs-D/2,cs+D/2]); assert np.all(abs(((faces/dx)-0.5)-np.round((faces/dx)-0.5))<1e-9), 'face on grid point'
    xl,xr=cs[0]-D/2,cs[-1]+D/2
    V=np.zeros(n)
    for c in cs: V+=np.where(abs(x-c)<D/2,V0,0.0)
    if b: V+=-b*np.clip((x-xl)/(xr-xl),0,1)
    k0=np.sqrt(2*sp['E']); x0=xl-max(14.0,4*sp['sx'])
    chi=np.exp(-(x-x0)**2/(4*sp['sx']**2)+1j*k0*x); chi/=np.sqrt((abs(chi)**2).sum()*dx)
    hv=np.exp(-0.5j*V*dt); kin=np.exp(-0.5j*k**2*dt); lost_r=0.0
    for _ in range(int(round(t_end/dt))):
        chi=hv*np.fft.ifft(kin*np.fft.fft(hv*chi)); before=abs(chi)**2; chi=chi*m
        lost_r+=((before-abs(chi)**2)*dx)[x>0].sum()
    return float((abs(chi[x>xr])**2).sum()*dx+lost_r)
