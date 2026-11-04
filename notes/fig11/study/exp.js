// Arrival experiment: A = plan must end with the cart at rest (current), B = plan ends at a moving equilibrium (free cart speed)
const S=require('./sim.js');const C=require('./colloc2.js');const R=require('./replay.js');const {Ep,Pp,uFor,f}=require('./calmlib.js');
const variant=process.argv[2], set=process.argv[3], i0=+process.argv[4], i1=+process.argv[5];
let seed=2026;const rnd=()=>{seed=(seed*1664525+1013904223)%4294967296;return seed/4294967296;};
const raw=[];for(let i=0;i<40;i++)raw.push([(rnd()-.5)*1.0,(rnd()*2-1)*Math.PI,(rnd()*2-1)*Math.PI,(rnd()-.5)*1.0,(rnd()-.5)*6,(rnd()-.5)*6]);
function calm(s0){let s=s0.slice(),t=0;const Emin=-(f[0]+f[1]);while(Ep(s)-Emin>0.05&&t<40){let a=2*Pp(s)-4*s[0]-4*s[3];a=Math.max(-8,Math.min(8,a));let u=Math.max(-60,Math.min(60,uFor(s,a)));s=S.rk4(s,u,0.001);t+=0.001;}return s;}
function Vred(w){const e=[0,w[1],w[2],0,w[4],w[5]];return S.V(e);}
function run(plan,tv,moving){ // track the plan, hand over at W<0.9c*, then balance (moving: about the moving equilibrium reached)
 const cstar=30.6,h=0.001;let s=plan.Z[0].slice(),u=0,mode='P',xh=0,vh=0,th=0,tvar=0,prevV=s[3],xmax=0;const T=plan.T+6;
 for(let i=0;i<Math.round(T/h);i++){ if(i%10===0){const k=i/10,t=i*h,w=S.wrapA(s);
   if(mode==='P'){ const ok= moving? Vred(w)<0.9*cstar : S.V(w)<0.9*cstar; if((ok&&k>5)||k>=tv.n){mode='L';xh=s[0];vh=s[3];th=t;} }
   if(mode==='P'){let v=tv.un[k];for(let j=0;j<6;j++)v-=tv.Kt[k][j]*(s[j]-tv.nom[k][j]);u=v;}
   else {const e=w.slice(); if(moving){e[0]=s[0]-(xh+vh*(t-th));e[3]=s[3]-vh;} u=0;for(let j=0;j<6;j++)u-=S.K[j]*e[j];}
   u=Math.max(-60,Math.min(60,u));}
  s=S.rk4(s,u,h);tvar+=Math.abs(s[3]-prevV);prevV=s[3];xmax=Math.max(xmax,Math.abs(s[0]));}
 const w=S.wrapA(s);return {caught:Math.abs(w[1])<0.02&&Math.abs(w[2])<0.02&&Math.abs(w[4])<0.05&&Math.abs(w[5])<0.05,tvar,xmax,vend:s[3]};}
const out=[];
for(let i=i0;i<i1;i++){const s0= set==='raw'? raw[i] : (i===0? [0,Math.PI,Math.PI,0,0,0] : calm(raw[i]));
 const Ts= set==='raw'? [4,6]:[4]; let rec={i,set,variant,found:false};const t0=Date.now();
 for(const T of Ts){const plan=C.planCol(s0,T,{M:Math.round(T*10),nsub:8,wd:100,wT:30,wl:20,wu:1,wr:0.02,ws:0.02,xlim:1.5,ulim:60,maxIt:150,vw:variant==='B'?0:0.3});
  const um=Math.max(...plan.U.map(Math.abs)),xm=Math.max(...plan.Z.map(z=>Math.abs(z[0])));
  if(plan.dmax<3e-3&&um<=63&&xm<=1.6){const tv=R.tvlqr(plan);const r=run(plan,tv,variant==='B');
   const u2=plan.U.reduce((a,u)=>a+u*u*plan.dt,0);const vM=plan.Z[plan.M][3];
   rec={i,set,variant,found:true,T,umax:+um.toFixed(1),u2:+u2.toFixed(0),vM:+vM.toFixed(3),...r,ms:Date.now()-t0};break;}}
 console.log(JSON.stringify(rec));}
