const ph=require('../physics.cjs');
for(const dt of [2e-4]){ph.P.dt=dt;for(const kind of ['makeIron','makeCotton']){const t0=Date.now();const b=ph[kind]();const tb=(Date.now()-t0)/1000;
 // initial stored energy
 ph.step(b);const e1=b.E;
 const n=Math.round(ph.P.tmax/dt);let F,E0=e1.KE+e1.PE+e1.elastic+e1.head+e1.heat,maxErr=0,acc=0,cnt=0,minH=Infinity,keImp=0;
 for(let k=0;k<n;k++){F=ph.step(b);const e=b.E;const tot=e.KE+e.PE+e.elastic+e.head+e.heat;maxErr=Math.max(maxErr,Math.abs(tot-E0));if(b.t>4.0)acc+=F,cnt++;
   if(b.tImpact&&!keImp)keImp=e.KE;
   if(b.tImpact&&b.t<b.tImpact+0.5){let lo=Infinity,hi=-Infinity;for(let i=0;i<b.N;i++){lo=Math.min(lo,b.y[i]);hi=Math.max(hi,b.y[i])}minH=Math.min(minH,hi-lo)}}
 const e=b.E;console.log(dt,kind,'build s',tb,'E0',E0.toFixed(3),'stored at start',e1.elastic.toFixed(4),'KE at contact',keImp.toFixed(2),'end: KE',e.KE.toFixed(3),'PE',e.PE.toFixed(3),'elastic',e.elastic.toFixed(3),'heat',e.heat.toFixed(3),'max|err|',maxErr.toFixed(3),'Fmax',b.Fmax.toFixed(1),'weight',(acc/cnt).toFixed(3),'minH',minH.toFixed(2),'broken',b.alive.length-b.alive.reduce((s,a)=>s+a,0),'cpu',(Date.now()-t0)/1000)}}
