/*PHYSICS-BEGIN*/
// Every number of the animation lives in P. Scaled units: length in drawing units, mass 1 per ball, time in seconds.
const P={
  g:9.81, h:10.0, M:1.0, dt:2e-4, tmax:9.0,
  iron:{R:0.5, a:0.10, k:1e5, ar0:3.95, c:2, rad:0.035, sub:5},
  cot:{R:1.3, nf:18, nb:34, s:0.08, turn:0.35, kax:300, kb:0.25, cb:0.004, c:0.3,
       jr:0.07, kj:40, Fj:4, drep:0.06, krep:20, crep:0.4, rad:0.03, seed:5, sub:2},
  head:{mp:0.2, kh:6000, ch:62, wc:1350, zc:0.5}
};
function rng(seed){return()=>{seed=(seed*16807)%2147483647;return(seed-1)/2147483646}}
function gauss(r){let u=0;while(!u)u=r();const v=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v)}

// A body: particles (positions x,y; velocities u,v; forces fx,fy), bonds, bending triplets.
function newBody(kind,pts,fibre){
  const N=pts.length;
  let ymin=Infinity;for(const p of pts)ymin=Math.min(ymin,p.y);
  const rad=P[kind==='iron'?'iron':'cot'].rad,lift=P.h-ymin+rad; // lowest point starts exactly h above the plate
  const b={kind,N,m:P.M/N,rad,
    x:new Float64Array(N),y:new Float64Array(N),u:new Float64Array(N),v:new Float64Array(N),
    fx:new Float64Array(N),fy:new Float64Array(N),fib:new Int32Array(N),
    bonds:[],tri:[],yp:0,vp:0,t:0,Fmax:0,tImpact:null,heat:0,heatBall:0,heatHead:0,Pd:0,Pdh:0,Ebond:0,Ebend:0,Erep:0,y00:0};
  b.kc=b.m*P.head.wc*P.head.wc;b.cc=2*P.head.zc*b.m*P.head.wc;   // skin contact: every particle rebounds in the same time 2π/wc, damping ratio zc
  pts.forEach((p,i)=>{b.x[i]=p.x;b.y[i]=p.y+lift;b.fib[i]=fibre?fibre[i]:0});
  let yc=0;for(let i=0;i<N;i++)yc+=b.y[i];b.y00=yc/N-P.h;  // height energy measured so that it starts at exactly M g h
  return b;
}
function packBonds(b,list){
  const n=list.length;b.nb=n;
  b.bi=new Int32Array(n);b.bj=new Int32Array(n);b.l0=new Float64Array(n);b.type=new Uint8Array(n); // 0 Morse metal, 1 fibre axial, 2 junction
  b.D=new Float64Array(n);b.al=new Float64Array(n);b.k=new Float64Array(n);b.brk=new Float64Array(n);b.alive=new Uint8Array(n);b.strain=new Float64Array(n);
  list.forEach((s,q)=>{b.bi[q]=s.i;b.bj[q]=s.j;b.l0[q]=s.l0;b.type[q]=s.type;b.D[q]=s.D||0;b.al[q]=s.al||0;b.k[q]=s.k||0;b.brk[q]=s.brk||1e9;b.alive[q]=1});
}
function makeIron(){
  const q=P.iron,pts=[],n=8;
  for(let j=-n;j<=n;j++)for(let i=-n;i<=n;i++){
    const x=(i+(j&1)*0.5)*q.a,y=j*q.a*Math.sqrt(3)/2;
    if(x*x+y*y<=q.R*q.R+1e-9)pts.push({x,y});
  }
  const b=newBody('iron',pts);
  const al=q.ar0/q.a,D=q.k/(2*al*al),L=[];   // Morse: bond stiffness at the minimum is 2 D al^2 = k
  for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){
    const d=Math.hypot(pts[i].x-pts[j].x,pts[i].y-pts[j].y);
    if(d<q.a*1.05)L.push({i,j,l0:d,type:0,D,al});
  }
  packBonds(b,L);b.c=q.c;b.Dm=D;b.alm=al;
  b.ntri=0;return b;
}
function turnAngle(ax,ay,bx,by,cx,cy){const ux=bx-ax,uy=by-ay,vx=cx-bx,vy=cy-by;return Math.atan2(ux*vy-uy*vx,ux*vx+uy*vy)}
function makeCotton(){
  const q=P.cot,r=rng(q.seed),pts=[],fibre=[],fibIdx=[];
  for(let f=0;f<q.nf;f++){             // each fibre: a persistent random walk that turns back at the ball's edge
    let x,y;do{x=(r()*2-1)*q.R;y=(r()*2-1)*q.R}while(x*x+y*y>(0.8*q.R)**2);
    let th=r()*2*Math.PI;const idx=[];
    for(let k=0;k<q.nb;k++){
      idx.push(pts.length);pts.push({x,y});fibre.push(f);
      th+=q.turn*gauss(r);
      let nx=x+q.s*Math.cos(th),ny=y+q.s*Math.sin(th);
      if(nx*nx+ny*ny>(0.95*q.R)**2){th=Math.atan2(-y,-x)+0.8*gauss(r);nx=x+q.s*Math.cos(th);ny=y+q.s*Math.sin(th)}
      x=nx;y=ny;
    }
    fibIdx.push(idx);
  }
  const b=newBody('cot',pts,fibre),L=[],T=[];
  for(const idx of fibIdx){
    for(let k=0;k+1<idx.length;k++){const i=idx[k],j=idx[k+1];L.push({i,j,l0:Math.hypot(pts[i].x-pts[j].x,pts[i].y-pts[j].y),type:1,k:q.kax})}
    for(let k=1;k+1<idx.length;k++){const i=idx[k-1],j=idx[k],l=idx[k+1];T.push([i,j,l,turnAngle(pts[i].x,pts[i].y,pts[j].x,pts[j].y,pts[l].x,pts[l].y)])}
  }
  // junctions: wherever two fibres (or two far-apart parts of one fibre) start within jr of each other
  const a=q.kj/(4*q.Fj),D=2*q.Fj/a;   // Morse with stiffness 2Da^2 = kj and largest pull Da/2 = Fj
  for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){
    if(fibre[i]===fibre[j]&&j-i<4)continue;
    const d=Math.hypot(pts[i].x-pts[j].x,pts[i].y-pts[j].y);
    if(d<q.jr)L.push({i,j,l0:d,type:2,D,al:a,brk:d+3*Math.log(2)/a});
  }
  packBonds(b,L);b.c=q.c;b.nj=L.filter(s=>s.type===2).length;
  b.ntri=T.length;b.ti=new Int32Array(T.map(t=>t[0]));b.tj=new Int32Array(T.map(t=>t[1]));b.tk=new Int32Array(T.map(t=>t[2]));b.th0=new Float64Array(T.map(t=>t[3]));
  b.cell=new Int32Array(pts.length);b.next=new Int32Array(pts.length);b.fibIdx=fibIdx;
  relax(b);
  return b;
}
function relax(b){          // let the freshly made tangle settle without gravity, then call that shape 'unstressed'
  const g=P.g;P.g=0;const y0=Array.from(b.y),x0=Array.from(b.x);
  for(let round=0;round<3;round++){
    for(let k=0;k<400;k++){sub(b,P.dt);for(let i=0;i<b.N;i++){b.u[i]*=0.9;b.v[i]*=0.9}}
    for(let q=0;q<b.nb;q++){const i=b.bi[q],j=b.bj[q];b.l0[q]=Math.hypot(b.x[j]-b.x[i],b.y[j]-b.y[i]);if(b.type[q]===2)b.brk[q]=b.l0[q]+3*Math.log(2)/b.al[q]}
    for(let q=0;q<b.ntri;q++){const I=b.ti[q],J=b.tj[q],K=b.tk[q];b.th0[q]=turnAngle(b.x[I],b.y[I],b.x[J],b.y[J],b.x[K],b.y[K])}
  }
  P.g=g;
  // put it back at the drop height, at rest, and start the energy books from zero
  let ymin=Infinity;for(let i=0;i<b.N;i++)ymin=Math.min(ymin,b.y[i]);
  const shift=P.h+b.rad-ymin;let yc=0;
  for(let i=0;i<b.N;i++){b.y[i]+=shift;b.u[i]=0;b.v[i]=0;yc+=b.y[i]}
  b.y00=yc/b.N-P.h;b.heat=0;b.heatBall=0;b.heatHead=0;b.yp=0;b.vp=0;b.t=0;b.tImpact=null;
}
function bondForces(b){
  const {x,y,u,v,fx,fy}=b;let Eb=0;
  for(let q=0;q<b.nb;q++){
    if(!b.alive[q])continue;
    const i=b.bi[q],j=b.bj[q],dx=x[j]-x[i],dy=y[j]-y[i],l=Math.sqrt(dx*dx+dy*dy)||1e-12,ex=dx/l,ey=dy/l;
    if(l>b.brk[q]){b.alive[q]=0;continue}
    let f;
    if(b.type[q]===1)f=b.k[q]*(l-b.l0[q]);                                  // fibre axis: Hooke
    else{const e=Math.exp(-b.al[q]*(l-b.l0[q]));f=2*b.D[q]*b.al[q]*e*(1-e)}  // Morse: f = dU/dr
    const vr=(u[j]-u[i])*ex+(v[j]-v[i])*ey;
    const fd=(b.type[q]===2?0.2:1)*b.c*vr;f+=fd;b.Pd+=fd*vr;   // damper power -> heat
    if(b.type[q]===1)Eb+=0.5*b.k[q]*(l-b.l0[q])**2;else{const e=Math.exp(-b.al[q]*(l-b.l0[q]));Eb+=b.D[q]*(1-e)*(1-e)}
    b.strain[q]=(l-b.l0[q])/b.l0[q];
    fx[i]+=f*ex;fy[i]+=f*ey;fx[j]-=f*ex;fy[j]-=f*ey;
  }
  b.Ebond=Eb;
}
function bendForces(b){
  const {x,y,u,v,fx,fy}=b,kb=P.cot.kb,cb=P.cot.cb;let Ebend=0;
  for(let q=0;q<b.ntri;q++){
    const I=b.ti[q],J=b.tj[q],K=b.tk[q];
    const ux=x[J]-x[I],uy=y[J]-y[I],vx=x[K]-x[J],vy=y[K]-y[J],u2=ux*ux+uy*uy,v2=vx*vx+vy*vy;
    let d=Math.atan2(ux*vy-uy*vx,ux*vx+uy*vy)-b.th0[q];d=Math.atan2(Math.sin(d),Math.cos(d));
    const gix=-uy/u2,giy=ux/u2,gkx=-vy/v2,gky=vx/v2;               // gradient of the turning angle
    const om=gix*u[I]+giy*v[I]+gkx*u[K]+gky*v[K]-(gix+gkx)*u[J]-(giy+gky)*v[J];
    const T=-kb*d-cb*om;                                            // elastic + frictional bending moment
    Ebend+=0.5*kb*d*d;b.Pd+=cb*om*om;
    fx[I]+=T*gix;fy[I]+=T*giy;fx[K]+=T*gkx;fy[K]+=T*gky;fx[J]-=T*(gix+gkx);fy[J]-=T*(giy+gky);
  }
  b.Ebend=Ebend;
}
function contactForces(b){                 // fibres touching fibres: soft repulsion with friction
  const q=P.cot,h=q.drep,{x,y,u,v,fx,fy,fib}=b,N=b.N;
  let GX0=Infinity,GY0=Infinity,x1=-Infinity,y1=-Infinity;   // grid around the ball, cell size = contact range
  for(let i=0;i<N;i++){if(x[i]<GX0)GX0=x[i];if(x[i]>x1)x1=x[i];if(y[i]<GY0)GY0=y[i];if(y[i]>y1)y1=y[i]}
  const nx=Math.floor((x1-GX0)/h)+1,ny=Math.floor((y1-GY0)/h)+1;
  if(!b.headArr||b.headArr.length<nx*ny)b.headArr=new Int32Array(nx*ny*2);
  const head=b.headArr;head.fill(-1,0,nx*ny);
  for(let i=0;i<N;i++){
    const cx=Math.min(nx-1,Math.max(0,Math.floor((x[i]-GX0)/h))),cy=Math.min(ny-1,Math.max(0,Math.floor((y[i]-GY0)/h)));
    const c=cx*ny+cy;b.cell[i]=c;b.next[i]=head[c];head[c]=i;
  }
  let Erep=0;
  for(let i=0;i<N;i++){
    const c=b.cell[i],cx=(c/ny)|0,cy=c-cx*ny;
    for(let ox=-1;ox<=1;ox++){const X=cx+ox;if(X<0||X>=nx)continue;
      for(let oy=-1;oy<=1;oy++){const Y=cy+oy;if(Y<0||Y>=ny)continue;
        for(let j=head[X*ny+Y];j!==-1;j=b.next[j]){
          if(j<=i||(fib[i]===fib[j]&&j-i<3))continue;
          const dx=x[j]-x[i],dy=y[j]-y[i],r2=dx*dx+dy*dy;
          if(r2>=h*h)continue;
          const r=Math.sqrt(r2)||1e-12,ex=dx/r,ey=dy/r,vr=(u[j]-u[i])*ex+(v[j]-v[i])*ey;
          const fe=-q.krep*(h-r),f=Math.min(0,fe+q.crep*vr);
          Erep+=0.5*q.krep*(h-r)*(h-r);
          b.Pd+=(f-fe)*vr;                  // power lost to contact friction (f-fe is the friction part)
          fx[i]+=f*ex;fy[i]+=f*ey;fx[j]-=f*ex;fy[j]-=f*ey;
        }}}
  }
  b.Erep=Erep;
}
function sub(b,dt){
  const H=P.head,{x,y,u,v,fx,fy}=b,N=b.N,m=b.m;
  for(let i=0;i<N;i++){fx[i]=0;fy[i]=-m*P.g}                      // Newton: weight on every particle
  b.Pd=0;b.Pdh=0;b.Ebend=0;b.Erep=0;
  bondForces(b);
  if(b.kind==='cot'){bendForces(b);contactForces(b)}
  let Fc=0,Ec=0;
  for(let i=0;i<N;i++){                                              // particle on plate: stiff spring, damped, never pulls
    const pen=b.yp-(y[i]-b.rad);
    if(pen>0){const fe=b.kc*pen,f=Math.max(0,fe-b.cc*(v[i]-b.vp));fy[i]+=f;Fc+=f;Ec+=0.5*b.kc*pen*pen;b.Pdh+=(fe-f)*(b.vp-v[i])*-1}
  }
  b.Pdh+=H.ch*b.vp*b.vp;                                             // head damper (soft tissue)
  for(let i=0;i<N;i++){u[i]+=fx[i]/m*dt;v[i]+=fy[i]/m*dt;x[i]+=u[i]*dt;y[i]+=v[i]*dt} // semi-implicit Euler
  const ap=(-Fc-H.kh*b.yp-H.ch*b.vp)/H.mp;b.vp+=ap*dt;b.yp+=b.vp*dt;  // plate: m_p a = -F_contact - k_h y - c_h v
  b.heatBall+=b.Pd*dt;b.heatHead+=b.Pdh*dt;b.heat=b.heatBall+b.heatHead;
  b.t+=dt;
  let KE=0,PE=0;for(let i=0;i<N;i++){KE+=0.5*m*(u[i]*u[i]+v[i]*v[i]);PE+=m*P.g*(y[i]-b.y00)}
  b.E={KE,PE,heatBall:b.heatBall,heatHead:b.heatHead,elastic:b.Ebond+b.Ebend+b.Erep+Ec,head:0.5*H.kh*b.yp*b.yp+0.5*H.mp*b.vp*b.vp,heat:b.heat};
  if(b.tImpact===null&&Fc>0)b.tImpact=b.t;
}
function step(b){                                                    // one frame step of length P.dt (iron: in 'sub' smaller steps, its bonds are stiff)
  const n=b.kind==='iron'?P.iron.sub:P.cot.sub;
  for(let s=0;s<n;s++)sub(b,P.dt/n);
  const Fs=-P.head.kh*b.yp;                                          // the scale reads its spring: F = k_h * compression
  if(Fs>b.Fmax)b.Fmax=Fs;
  return Fs;
}
/*PHYSICS-END*/
if(typeof module!=='undefined')module.exports={P,makeIron,makeCotton,step};
