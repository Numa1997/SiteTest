const S=require('./sim.js');const C=require('./colloc.js');const R=require('./replay.js');const {Ep,Pp,uFor,f}=require('./calmlib.js');
const lines=require('fs').readFileSync('./random.out','utf8').split('\n').filter(l=>l.includes('NO FEASIBLE'));
const cases=lines.map(l=>JSON.parse(l.match(/s0=(\[[^\]]+\])/)[1]));
const Emin=-(f[0]+f[1]);let ok=0,tmax=0,tsum=0,xm=0,um=0;
for(const s0 of cases){let s=s0.slice(),t=0;
 while(Ep(s)-Emin>0.05&&t<40){let a=2*Pp(s)-4*s[0]-4*s[3];a=Math.max(-8,Math.min(8,a));let u=Math.max(-60,Math.min(60,uFor(s,a)));um=Math.max(um,Math.abs(u));s=S.rk4(s,u,0.001);t+=0.001;xm=Math.max(xm,Math.abs(s[0]));}
 tmax=Math.max(tmax,t);tsum+=t;let res='NO PLAN';
 for(const T of [4,5,6]){const plan=C.planCol(s,T,{M:Math.round(T*10),nsub:8,wd:100,wT:30,wl:20,wu:1,wr:0.02,ws:0.02,xlim:1.5,ulim:60,maxIt:150});
  const pu=Math.max(...plan.U.map(Math.abs)),px=Math.max(...plan.Z.map(z=>Math.abs(z[0])));
  if(plan.dmax<3e-3&&pu<=63&&px<=1.6){const r=R.replay(plan,R.tvlqr(plan),{Fm:60,cc:100,Tx:5});const good=Math.abs(r.end[1])<.05&&Math.abs(r.end[2])<.05;res=`T=${T} ${good?'CAUGHT':'replay failed'}`;if(good)ok++;break;}}
 console.log(`s0=[${s0}] calm ${t.toFixed(1)} s -> ${res}`);}
console.log(`SUMMARY calm-then-swing: ${ok}/${cases.length} caught; calming time mean ${(tsum/cases.length).toFixed(1)} s, max ${tmax.toFixed(1)} s; cart |x| max ${xm.toFixed(2)} m; |u| max ${um.toFixed(0)} N`);
