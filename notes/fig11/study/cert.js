// Certified catch level for the SAMPLED loop: largest c with W(F(s)) < W(s) for all 0 < W(s) <= c, F = one loop period of the true equations with u = sat(-K s) held
const S=require('./sim.js');const SA=require('./samp.js');
const m0=1.5,m1=.5,m2=.75,L1=.5,L2=.75,g=9.81,d=[m0+m1+m2,(m1/2+m2)*L1,m2*L2/2,(m1/3+m2)*L1*L1,m2*L1*L2/2,m2*L2*L2/3],f=[(m1/2+m2)*L1*g,m2*L2*g/2];
function inv3(M){const a=M;const det=a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]);
 return [[(a[1][1]*a[2][2]-a[1][2]*a[2][1])/det,(a[0][2]*a[2][1]-a[0][1]*a[2][2])/det,(a[0][1]*a[1][2]-a[0][2]*a[1][1])/det],[(a[1][2]*a[2][0]-a[1][0]*a[2][2])/det,(a[0][0]*a[2][2]-a[0][2]*a[2][0])/det,(a[0][2]*a[1][0]-a[0][0]*a[1][2])/det],[(a[1][0]*a[2][1]-a[1][1]*a[2][0])/det,(a[0][1]*a[2][0]-a[0][0]*a[2][1])/det,(a[0][0]*a[1][1]-a[0][1]*a[1][0])/det]];}
const Di=inv3([[d[0],d[1],d[2]],[d[1],d[3],d[4]],[d[2],d[4],d[5]]]);const A=[...Array(6)].map(()=>Array(6).fill(0)),B=[...Array(6)].map(()=>[0]);for(let i=0;i<3;i++){A[i][i+3]=1;A[i+3][1]=Di[i][1]*f[0];A[i+3][2]=Di[i][2]*f[1];B[i+3][0]=Di[i][0];}
const Ts=+process.argv[2]/1000, which=process.argv[3]||'designed', F=+process.argv[4]||60;
const r=SA.dlqr(A,B,[50,50,50,20,700,700],1,Ts);const K= which==='designed'? r.K : S.K, P= which==='designed'? r.P : r.P;
const n=Math.max(1,Math.ceil(Ts/0.005)),h=Ts/n;
function W(x){let t=0;for(let i=0;i<6;i++)for(let j=0;j<6;j++)t+=x[i]*P[i][j]*x[j];return t;}
const Lc=(()=>{const L=[...Array(6)].map(()=>Array(6).fill(0));for(let i=0;i<6;i++)for(let j=0;j<=i;j++){let s=P[i][j];for(let k=0;k<j;k++)s-=L[i][k]*L[j][k];L[i][j]=i===j?Math.sqrt(s):s/L[j][j];}return L;})();
function back(v){const x=Array(6).fill(0);for(let i=5;i>=0;i--){let s=v[i];for(let k=i+1;k<6;k++)s-=Lc[k][i]*x[k];x[i]=s/Lc[i][i];}return x;}
let evals=0;
function dW(dir,c){evals++;const x=back(dir.map(a=>a*Math.sqrt(c)));let u=0;for(let i=0;i<6;i++)u-=K[i]*x[i];u=Math.max(-F,Math.min(F,u));let y=x;for(let k=0;k<n;k++)y=S.rk4(y,u,h);return W(y)-W(x);}
let seed=12345;const rnd=()=>{seed=(seed*1664525+1013904223)%4294967296;return seed/4294967296;};
const nrm=v=>{const q=Math.hypot(...v);return v.map(a=>a/q);};
const dirs=[];for(let k=0;k<8000;k++){const v=[];for(let i=0;i<6;i++)v.push(Math.sqrt(-2*Math.log(rnd()+1e-12))*Math.cos(2*Math.PI*rnd()));dirs.push(nrm(v));}
const SH=[1,0.8,0.6,0.4,0.2,0.08];
function safe(c){const worst=[];for(let k=0;k<dirs.length;k++)for(let sh=0;sh<(k%4===0?SH.length:1);sh++){const cl=c*SH[sh],w=dW(dirs[k],cl);if(w>=0)return false;const sc=w/cl;if(worst.length<12||sc>worst[11].sc){worst.push({sc,w,d:dirs[k],cl});worst.sort((a,b)=>b.sc-a.sc);if(worst.length>12)worst.pop();}}
 for(const m of worst){let d=m.d.slice(),w0=m.w,hh=0.05;for(let it=0;it<100&&hh>1e-6;it++){const gr=[];for(let j=0;j<6;j++){const dd=d.slice();dd[j]+=1e-5;gr.push((dW(nrm(dd),m.cl)-w0)/1e-5);}const gn=Math.hypot(...gr)||1;const dn=nrm(d.map((v,q)=>v+hh*gr[q]/gn));const w1=dW(dn,m.cl);if(w1>w0){d=dn;w0=w1;hh*=1.5;if(w0>=0)return false;}else hh/=2;}}
 return true;}
const t0=Date.now();let lo=1,hi=1e5;if(!safe(lo)){console.log(`Ts=${Ts*1000} ms ${which}: no certified level (c*=0) ${Date.now()-t0} ms`);process.exit();}
for(let it=0;it<20;it++){const mid=Math.sqrt(lo*hi);if(safe(mid))lo=mid;else hi=mid;}
console.log(`Ts=${Ts*1000} ms, ${which} gains, ${F} N: c* = ${lo.toFixed(2)}  (${evals} one-sample maps, ${Date.now()-t0} ms)`);
