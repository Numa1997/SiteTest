"""Render the GPU chaos maps: v = log(1000 d)/log(1000) as in map_png.py, painted with a richer ramp
(night -> wine -> rose -> cream), plus a mild unsharp mask; no resampling of the computed pixels other than the final downscale."""
import numpy as np, json, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D='/tmp/claude-0/-home-user-SiteTest/1c12404a-a910-5155-b389-b69ad4e58af2/scratchpad/kgout/'
R=json.load(open(D+'results.json'))
stops=np.array([[0.00,20,13,16],[0.25,46,18,28],[0.50,122,31,43],[0.72,196,96,112],[0.88,226,162,170],[1.00,255,240,226]])
def paint(v):
    out=np.zeros(v.shape+(3,))
    for c in range(3): out[...,c]=np.interp(v,stops[:,0],stops[:,c+1])
    return out
def bright(d): return np.clip(np.log(1000*np.maximum(d,1e-12))/np.log(1000),0,1)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',30)
ims={}
for k,m in R.items():
    d=np.load(D+k+'.npy').astype(float); v=bright(d)
    im=Image.fromarray(paint(v).round().astype(np.uint8)).filter(ImageFilter.UnsharpMask(1.2,60,2))
    ims[k]=im; im.save(D+k+'_r.png')
# zoom sequence: each frame with a box where the next one is
names=[f'zoom{i}' for i in range(6)]
tiles=[]
for i,n in enumerate(names):
    m=R[n]; im=ims[n].copy(); dr=ImageDraw.Draw(im); W,H=im.size
    if i+1<len(names):
        nm=R[names[i+1]]; cx=(nm['centre'][0]-m['centre'][0])/(2*m['half'][0])*W+W/2; cy=H/2-(nm['centre'][1]-m['centre'][1])/(2*m['half'][1])*H
        bw=nm['half'][0]/m['half'][0]*W/2; bh=nm['half'][1]/m['half'][1]*H/2
        dr.rectangle([cx-bw,cy-bh,cx+bw,cy+bh],outline=(255,210,122),width=4)
    mag=8**i; dr.rectangle([0,0,W,54],fill=(20,13,16)); dr.text((18,10),f'zoom {i}: width {2*m["half"][0]:.6g} kg m2/s  ·  {mag:,}x  ·  {100*m["chaotic_share"]:.0f} % chaotic',font=f,fill=(255,246,234))
    tiles.append(im)
W,H=tiles[0].size; mont=Image.new('RGB',(2*W+12,3*H+24),(245,241,234))
for i,t in enumerate(tiles): mont.paste(t,((i%2)*(W+12),(i//2)*(H+12)))
mont.save(D+'zooms_montage.png')
for k in ['sheet','eye']: ims[k].convert('RGB').save(D+k+'_r.jpg',quality=93)
mont.convert('RGB').resize((mont.width//2,mont.height//2),Image.LANCZOS).save(D+'zooms_montage.jpg',quality=92)
for i,t in enumerate(tiles): t.convert('RGB').save(D+f'zoom{i}_r.jpg',quality=93)
print('done')
