const S=require('./sim.js');const K40=require('./K40.json').K40;
function run(K,Ts,s0,T){let s=s0.slice(),u=0,late=0,lost=null,umax=0;const n=Math.round(Ts/0.001);
 for(let k=0;k<T*1000;k++){if(k%n===0){u=0;for(let i=0;i<6;i++)u-=K[i]*s[i];u=Math.max(-60,Math.min(60,u));}
  s=S.rk4(s,u,0.001);const th=Math.max(Math.abs(s[1]),Math.abs(s[2]));if(k>(T-60)*1000){late=Math.max(late,th);umax=Math.max(umax,Math.abs(u));}if(th>1.2){lost=k/1000;break;}}
 return lost!==null?`lost at ${lost} s`:`held ${T} s; in the last 60 s largest angle ${(late*180/Math.PI).toFixed(3)}°, largest force ${umax.toFixed(1)} N`;}
const s0=[0,2*Math.PI/180,-1*Math.PI/180,0,0,0];
console.log('continuous gains, Ts=10 ms:',run(S.K,0.010,s0,600));
console.log('continuous gains, Ts=40 ms:',run(S.K,0.040,s0,600));
console.log('gains designed for 40 ms:  ',run(K40,0.040,s0,600));
for(const lean of [5,10,15]){const s1=[0,lean*Math.PI/180,0,0,0,0];console.log(`lean ${lean}° , Ts=40 ms: continuous gains ${run(S.K,0.040,s1,60)} | designed for 40 ms ${run(K40,0.040,s1,60)}`);}
