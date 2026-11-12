import sys, json, zlib, struct, numpy as np, jax, jax.numpy as jnp, time
sys.path.insert(0, "/home/user/SiteTest/tools/kaggle/schrodinger-sphere")
from solver import setup
N=128; L=64.0; g=setup(N,L); x=g["x"]; dt=0.01; E,V0,R=2.0,3.0,4.0; k0=np.sqrt(2*E)
X,Y,Z=np.meshgrid(x,x,x,indexing="ij")
psi=jnp.asarray((2*np.pi*9)**-0.75*np.exp(-((X+14)**2+Y**2+Z**2)/36+1j*k0*X),jnp.complex64)
hv=jnp.asarray(np.exp(-0.5j*np.where(X**2+Y**2+Z**2<R*R,V0,0)*dt),jnp.complex64); kin=jnp.asarray(np.exp(-0.5j*g["K2"]*dt),jnp.complex64); mk=jnp.asarray(g["mask"],jnp.float32)
NF=32; steps=round(30/k0/dt); per=steps//(NF-1)
step=jax.jit(lambda p: jax.lax.fori_loop(0,per,lambda i,p: mk*(hv*jnp.fft.ifftn(kin*jnp.fft.fftn(hv*p))),p))
sl=(slice(16,112),slice(32,96),slice(32,96))   # x -24..24, y and z -16..16 (0.5 a steps)
fr=[]; peak=None; t=time.time()
for f in range(NF):
    if f: psi=step(psi)
    c=np.asarray(psi)[sl]
    if peak is None: peak=np.abs(c).max()
    fr.append(np.clip(np.round(127*c.real/peak),-127,127).astype(np.int8))
v=np.array(fr); raw=(v.astype(np.int16)+128).astype(np.uint8)
z=zlib.compress(raw.tobytes(),9)
print("frames",v.shape,"time",round(time.time()-t,1),"s; compressed per frame",len(z)/NF/1e3,"kB; per run",len(z)/1e6,"MB")
head=dict(E=E,V0=V0,R=R,n=NF,shape=list(v.shape[1:]),x0=-24.0,y0=-16.0,step=0.5,kind="re",dt=dt,steps=per*(NF-1))
hb=json.dumps(head).encode(); open("wave3d.bin","wb").write(b"SPHW"+struct.pack("<I",len(hb))+hb+z)
