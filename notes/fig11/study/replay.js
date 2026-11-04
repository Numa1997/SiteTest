const S=require('./sim.js'); const C=require('./colloc.js'); const {K,P}=S;
const Qd=[50,50,50,20,700,700];
function mm(A,B){const n=A.length,m=B[0].length,k=B.length;return Array.from({length:n},(_,i)=>Array.from({length:m},(_,j)=>{let s=0;for(let l=0;l<k;l++)s+=A[i][l]*B[l][j];return s;}));}
function tr(A){return A[0].map((_,j)=>A.map(r=>r[j]));}
function tvlqr(plan,Ts=0.01){ // nominal on Ts grid with ZOH u from the plan
 const {U,dt}=plan;const n=Math.round(plan.T/Ts);const per=Math.round(dt/Ts);const nom=[];const un=[];
 for(let k=0;k<n;k++){const iv=Math.min(plan.M-1,Math.floor(k/per)),j=k-iv*per;const u=U[iv];nom.push(j==0?plan.Z[iv].slice():C.stepZ(plan.Z[iv],u,j*Ts,10*j));un.push(u);}
 nom.push(plan.Z[plan.M].slice());
 // linearise each Ts step: F=dstep/ds, G=dstep/du
 const Fs=[],Gs=[];for(let k=0;k<n;k++){const z=nom[k],u=un[k];const b=C.stepZ(z,u,Ts,10);const F=Array.from({length:6},()=>Array(6).fill(0));for(let j=0;j<6;j++){const e=1e-6;const zz=z.slice();zz[j]+=e;const st=C.stepZ(zz,u,Ts,10);for(let i=0;i<6;i++)F[i][j]=(st[i]-b[i])/e;}const e=1e-6;const st=C.stepZ(z,u+e,Ts,10);Fs.push(F);Gs.push(st.map((v,i)=>(v-b[i])/e));}
 // backward Riccati, R=1, terminal P
 let Pn=P.map(r=>r.slice());const Kt=new Array(n);for(let k=n-1;k>=0;k--){const F=Fs[k],G=Gs[k];const PG=Pn.map(r=>r.reduce((a,v,j)=>a+v*G[j],0));const den=1+G.reduce((a,v,i)=>a+v*PG[i],0);const PF=mm(Pn,F);const GPF=Array.from({length:6},(_,j)=>G.reduce((a,v,i)=>a+v*PF[i][j],0));const Kk=GPF.map(v=>v/den);Kt[k]=Kk;
  const FtPF=mm(tr(F),PF);const Pk=Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>FtPF[i][j]+(i==j?Qd[i]:0)-GPF[i]*Kk[j]));Pn=Pk.map((r,i)=>r.map((v,j)=>(v+Pk[j][i])/2));}
 return {nom,un,Kt,Ts,n};}
function replay(plan,tv,o){const {Fm,cc,Tx=4}=o;let s=plan.Z[0].slice(),h=0.001,Ts=tv.Ts,nstep=Ts/h,mode='P',tc=null,xmax=0,umax=0,u=0,maxdev=0;const T=plan.T+Tx;
 for(let i=0;i<Math.round(T/h);i++){if(i%nstep==0){const k=i/nstep;const w=S.wrapA(s);
   if(mode=='P'&&S.V(w)<cc&&k>5){mode='L';tc=k*Ts;}
   if(mode=='P'){const kk=Math.min(k,tv.n-1);if(k>=tv.n){mode='L';tc=k*Ts;}else{let v=tv.un[kk];const e=s.map((q,j)=>q-tv.nom[kk][j]);maxdev=Math.max(maxdev,Math.hypot(...e));for(let j=0;j<6;j++)v-=tv.Kt[kk][j]*e[j];u=v;}}
   if(mode=='L'){let v=0;for(let j=0;j<6;j++)v-=K[j]*w[j];u=v;}
   u=Math.max(-Fm,Math.min(Fm,u));}
  s=S.rk4(s,u,h);xmax=Math.max(xmax,Math.abs(s[0]));umax=Math.max(umax,Math.abs(u));}
 const w=S.wrapA(s);return {ok:Math.abs(w[1])<2e-2&&Math.abs(w[2])<2e-2&&Math.abs(w[3])<.05,tc,xmax:+xmax.toFixed(2),umax:+umax.toFixed(0),maxdev:+maxdev.toFixed(3),end:w.map(v=>+v.toFixed(3))};}
module.exports={tvlqr,replay};
if(require.main===module){const s0=[0,Math.PI-0.02,Math.PI-0.02,0,0,0];const t0=Date.now();
 const plan=C.planCol(s0,4,{M:40,nsub:5,wd:100,wT:30,wl:20,wu:1,wr:0.02,ws:0.02,xlim:1.5,ulim:60,maxIt:150});console.log('plan cost',plan.cost.toExponential(2),'defect',plan.dmax.toExponential(1),'s',((Date.now()-t0)/1000).toFixed(1));
 const tv=tvlqr(plan);console.log('tvlqr ready',((Date.now()-t0)/1000).toFixed(1),'s; gain norm at start',Math.hypot(...tv.Kt[0]).toFixed(0),'at end',Math.hypot(...tv.Kt[tv.n-1]).toFixed(0));
 for(const cc of [100]){console.log('replay with TVLQR',JSON.stringify(replay(plan,tv,{Fm:60,cc})));}
 // open loop for comparison (zero gains)
 const tv0={...tv,Kt:tv.Kt.map(k=>k.map(()=>0))};console.log('replay open loop',JSON.stringify(replay(plan,tv0,{Fm:60,cc:100})));}
