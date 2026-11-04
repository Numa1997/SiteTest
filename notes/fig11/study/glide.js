// lean during a glide (26): balancer with the 10 ms gains about the gliding reference, real equations, 60 N
const S=require('./sim.js'); const K=require('./gains.json').K10; const W=0.5;
function glide(e0,v,x0){let s=[x0,0,0,v,0,0],u=0,mx1=0,mx2=0,um=0,tgt=x0-e0,tin=null;const b=v+W*e0;
 for(let k=0;k<40000;k++){const t=k/1000;if(k%10===0){const ex=Math.exp(-W*t),xr=tgt+(e0+b*t)*ex,vr=(b-W*(e0+b*t))*ex;const e=[s[0]-xr,s[1],s[2],s[3]-vr,s[4],s[5]];u=0;for(let i=0;i<6;i++)u-=K[i]*e[i];u=Math.max(-60,Math.min(60,u));
   if(tin===null&&Math.abs(xr-tgt)<0.01)tin=t;}
  s=S.rk4(s,u,0.001);mx1=Math.max(mx1,Math.abs(s[1]));mx2=Math.max(mx2,Math.abs(s[2]));um=Math.max(um,Math.abs(u));}
 return `e0=${e0} m, v=${v} m/s: largest lean lower ${(mx1*180/Math.PI).toFixed(2)}°, upper ${(mx2*180/Math.PI).toFixed(2)}°, largest force ${um.toFixed(1)} N, reference within 1 cm after ${tin} s, end x ${s[0].toFixed(4)} m`;}
console.log(glide(-1,0,0)); console.log(glide(-1,-1,0)); console.log(glide(-1,1,0));
