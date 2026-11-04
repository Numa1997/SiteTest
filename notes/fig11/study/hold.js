// Long hold at the page's defaults: LQR with zero-order hold every Ts, RK4 at 1 ms, force clipped at 60 N
const S=require('./sim.js');const K=S.K;
for (const Ts of [0.010,0.030,0.035,0.040]) {
 let s=[0,2*Math.PI/180,-1*Math.PI/180,0,0,0],u=0,maxth=0,lostAt=null;const n=Math.round(Ts/0.001);
 for(let k=0;k<600000;k++){ if(k%n===0){u=0;for(let i=0;i<6;i++)u-=K[i]*s[i];u=Math.max(-60,Math.min(60,u));}
  s=S.rk4(s,u,0.001); const th=Math.max(Math.abs(s[1]),Math.abs(s[2])); if(k>5000)maxth=Math.max(maxth,th); if(lostAt===null&&th>1){lostAt=k/1000;break;} }
 console.log(`Ts=${Ts*1000} ms: ${lostAt===null?'held 600 s, largest angle after 5 s '+(maxth*180/Math.PI).toExponential(1)+'°':'lost at t = '+lostAt+' s'}`);}
