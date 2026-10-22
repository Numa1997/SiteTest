const ph=require('../physics.cjs');ph.P.tmax=9;
for(const k of ['makeIron','makeCotton']){const b=ph[k]();const n=Math.round(ph.P.tmax/ph.P.dt);const F=[];for(let i=0;i<n;i++){F.push(ph.step(b))}
 const avg=(t0,t1)=>{let s=0,c=0;for(let i=Math.round(t0/ph.P.dt);i<Math.round(t1/ph.P.dt);i++){s+=F[i];c++}return (s/c).toFixed(3)};
 const mn=(t0,t1)=>{let lo=1e9,hi=-1e9;for(let i=Math.round(t0/ph.P.dt);i<Math.round(t1/ph.P.dt);i++){lo=Math.min(lo,F[i]);hi=Math.max(hi,F[i])}return lo.toFixed(2)+'..'+hi.toFixed(2)};
 console.log(k,[6,6.5,7,7.5,8,8.5,9].map(t=>t+':'+avg(4,t)).join(' '))}
