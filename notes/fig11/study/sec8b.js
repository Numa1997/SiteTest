// §8: longest T_s at which the rods come to rest (largest angle in the last 10 s of 60 s below 0.001 rad), from θ1 = 2°, θ2 = −1°; 60 N
const S=require('./sim.js'); const {dlqr}=require('./samp.js'); const Q=[50,50,50,20,700,700];
function zeros(n,m){const A=[];for(let i=0;i<n;i++)A.push(new Array(m).fill(0));return A;}
function inv3(D){const [[a,b,c],[d,e,f],[g2,h,i]]=D,A=e*i-f*h,B=-(d*i-f*g2),C=d*h-e*g2,det=a*A+b*B+c*C;return [[A/det,-(b*i-c*h)/det,(b*f-c*e)/det],[B/det,(a*i-c*g2)/det,-(a*f-c*d)/det],[C/det,-(a*h-b*g2)/det,(a*e-b*d)/det]];}
function lin(p){const d=p.d,Di=inv3([[d[0],d[1],d[2]],[d[1],d[3],d[4]],[d[2],d[4],d[5]]]),A=zeros(6,6),B=zeros(6,1);for(let i=0;i<3;i++){A[i][i+3]=1;A[i+3][1]=Di[i][1]*p.f[0];A[i+3][2]=Di[i][2]*p.f[1];B[i+3][0]=Di[i][0];}return {A,B};}
function run(K,Ts,T=60){let s=[0,2*Math.PI/180,-Math.PI/180,0,0,0],u=0,late=0,um=0;const n=Math.round(Ts/0.001);for(let k=0;k<T*1000;k++){if(k%n===0){u=0;for(let i=0;i<6;i++)u-=K[i]*s[i];u=Math.max(-60,Math.min(60,u));}s=S.rk4(s,u,0.001);const th=Math.max(Math.abs(s[1]),Math.abs(s[2]));if(th>1)return {lost:k/1000};if(k>(T-10)*1000){late=Math.max(late,th);um=Math.max(um,Math.abs(u));}}return {late,um};}
const mode=process.argv[2];
for(const [name,L1,L2] of [['default',.5,.75],['lengths doubled',1,1.5],['lengths halved',.25,.375]]){
 const p=S.par(1.5,.5,.75,L1,L2); S.setp(p); const {A,B}=lin(p); const Kc=dlqr(A,B,Q,1,0.00002).K; const out=[];
 const grid = mode==='cont' ? Array.from({length:120},(_,i)=>10+i*0.5) : Array.from({length:100},(_,i)=>150+i*2.5);
 let last=null,first=null;
 for(const Tms of grid){const Ts=Tms/1000;const K=mode==='cont'?Kc:dlqr(A,B,Q,1,Ts).K;const r=run(K,Ts);const rest=r.lost===undefined&&r.late<1e-3;
  if(rest&&first===null)last=Tms; if(!rest&&first===null){first=Tms;out.push(`first not at rest ${Tms} ms: ${JSON.stringify(r)}`);}
  if(first!==null&&Tms>first+6)break;}
 console.log(`${name} (${mode}): rests up to ${last} ms; ${out.join(' ')}`);}
if(mode==='cont'){S.setp(S.par());const {A,B}=lin(S.par());const Kc=dlqr(A,B,Q,1,0.00002).K;for(const Tms of [40,60,80]){const r=run(Kc,Tms/1000);console.log(`default, continuous gains at ${Tms} ms: ${JSON.stringify(r)}`);}
 for(const Tms of [80]){const r=run(dlqr(A,B,Q,1,Tms/1000).K,Tms/1000);console.log(`default, designed gains at ${Tms} ms: ${JSON.stringify(r)}`);}}
