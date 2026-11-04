const S=require('./sim.js');
for (const [name,uf] of [['u=0',t=>0],['u=20sin5t',t=>20*Math.sin(5*t)]]) for (const h of [1e-3,5e-4]) {
 let s=[0,0.1,-0.05,0,0,0],t=0;const out=[];const n=Math.round(2/h);
 for(let k=1;k<=n;k++){ // RK4 with u evaluated at stage times
  const f=(st,tt)=>S.rhs(st,uf(tt));
  const k1=f(s,t),a=s.map((v,i)=>v+h/2*k1[i]),k2=f(a,t+h/2),b=s.map((v,i)=>v+h/2*k2[i]),k3=f(b,t+h/2),c=s.map((v,i)=>v+h*k3[i]),k4=f(c,t+h);
  s=s.map((v,i)=>v+h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]));t=k*h;
  if(k%Math.round(0.5/h)==0)out.push(s.map(v=>v.toPrecision(10)).join(' '));}
 console.log(name,'h='+h);console.log(out.join('\n'));}
