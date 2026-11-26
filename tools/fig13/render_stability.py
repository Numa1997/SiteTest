"""Usage: python3 tools/fig13/render_stability.py STAB.npy OUT.png WIDTH EXPOSURE [p1a p1b p2a p2b]
The families of closed orbits, coloured by stability. Input: stab.py's array (p1, p2, T, s, label) per line point.
s = trace of one lap's monodromy - 2 = lam + 1/lam. |s| < 2: stable, shown green, brighter the faster a push circles round;
near +-2: neutral, gold; s > 2: unstable, red; s < -2: unstable with a flip each lap, magenta; brighter the faster the push grows per second."""
import numpy as np, sys, json
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter

D=np.load(sys.argv[1]); D=D[np.isfinite(D[:,3])]; OW=int(sys.argv[3]); OH=OW*9//16; EXP=float(sys.argv[4])
PW,PH=20*16/9,20.0; box=[float(x) for x in sys.argv[5:9]] if len(sys.argv)>8 else [-PW,PW,-PH,PH]
px=(D[:,0]-box[0])/(box[1]-box[0])*OW; py=(box[3]-D[:,1])/(box[3]-box[2])*OH; s=D[:,3]; T=D[:,2]
col=np.zeros((len(s),3)); w=np.ones(len(s))
st=np.abs(s)<1.99; ne=np.abs(np.abs(s)-2)<=0.01; up=s>2.01; um=s<-2.01
phi=np.arccos(np.clip(s[st]/2,-1,1))/np.pi
col[st]=np.array([0.36,0.95,0.78]); w[st]=0.55+0.9*phi
col[ne]=np.array([1.0,0.80,0.42]); w[ne]=0.42
lam=np.log((np.abs(s)+np.sqrt(np.maximum(s*s-4,0)))/2)/np.maximum(T,1e-6)
col[up]=np.array([1.0,0.30,0.30]); w[up]=0.6+0.5*np.clip(lam[up]/3,0,1.5)
col[um]=np.array([0.95,0.35,0.95]); w[um]=0.6+0.5*np.clip(lam[um]/3,0,1.5)
inb=(px>=0)&(px<OW-1)&(py>=0)&(py<OH-1); px,py,col,w=px[inb],py[inb],col[inb],w[inb]
acc=np.zeros((OH,OW,3)); yi=py.astype(int); xi=px.astype(int); fy=py-yi; fx=px-xi
for dy,wy in ((0,1-fy),(1,fy)):
    for dx,wx in ((0,1-fx),(1,fx)): np.add.at(acc,(yi+dy,xi+dx),col*(w*wy*wx)[:,None])
sc=OW/1920*(2*PW)/(box[1]-box[0])
glow=acc+np.dstack([gaussian_filter(acc[...,i],1.5*max(sc,1)) for i in range(3)])*1.8+np.dstack([gaussian_filter(acc[...,i],6*max(sc,1)) for i in range(3)])*1.3
img=1-np.exp(-glow*EXP/max(sc,1)**0.5)
ch=Image.open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../public/images/fig13/chaos-map-rods-P20.png'))
bx=((box[0]/(2*PW)+.5)*1280,(.5-box[3]/40)*720,(box[1]/(2*PW)+.5)*1280,(.5-box[2]/40)*720)
ch=np.array(ch.resize((OW,OH),Image.BICUBIC,box=bx)).astype(float)/255; bg=np.array([20,13,16])/255.; a=0.3*ch[...,3:4]
base=bg*(1-a)+ch[...,:3]*a; out=base+(1-base)*img
im=Image.fromarray((np.clip(out,0,1)*255).astype(np.uint8)); dr=ImageDraw.Draw(im)
fs=max(14,OW//110); f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',fs)
x0,y0=fs,fs; dr.rectangle([x0-fs*.5,y0-fs*.5,x0+fs*26,y0+fs*7.6],fill=(20,13,16)); dr.text((x0,y0),'closed orbits, by what a small push does',font=f,fill=(245,241,234))
for i,(c,t) in enumerate([((92,242,199),'stable: the push stays small'),((255,204,107),'neutral: the push drifts'),((255,77,77),'unstable: the push grows'),((242,89,242),'unstable, flipping sides each lap')]):
    yy=y0+fs*1.45*(i+1); dr.line([x0,yy+fs*.6,x0+fs*2,yy+fs*.6],fill=c,width=max(2,fs//5)); dr.text((x0+fs*2.6,yy),t,font=f,fill=c)
im.save(sys.argv[2]); print('wrote',sys.argv[2],'points',len(px),'| stable %.3f neutral %.3f unstable %.3f flip-unstable %.3f'%(st.mean(),ne.mean(),up.mean(),um.mean()))
