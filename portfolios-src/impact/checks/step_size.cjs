const ph=require('../physics.cjs');
for(const dt of [2e-4,1e-4]){ph.P.dt=dt;for(const k of ['makeIron','makeCotton']){const t0=Date.now();const b=ph[k]();const n=Math.round(ph.P.tmax/dt);for(let i=0;i<n;i++)ph.step(b);console.log(dt,k,'Fmax',b.Fmax.toFixed(1),'cpu per sim-s',((Date.now()-t0)/1000/ph.P.tmax).toFixed(2))}}
