// Certificate with climbs started from the weakest directions of the linear decrease (generalized eigenvectors), plus a few random tops
const S=require('./sim.js');const SA=require('./samp.js');
const m0=1.5,m1=.5,m2=.75,L1=.5,L2=.75,g=9.81,d=[m0+m1+m2,(m1/2+m2)*L1,m2*L2/2,(m1/3+m2)*L1*L1,m2*L1*L2/2,m2*L2*L2/3],f=[(m1/2+m2)*L1*g,m2*L2*g/2];
function inv(A){const n=A.length,W=A.map((row,i)=>{const e=new Array(n).fill(0);e[i]=1;return row.concat(e);});for(let c=0;c<n;c++){let p=c;for(let r=c+1;r<n;r++)if(Math.abs(W[r][c])>Math.abs(W[p][c]))p=r;const t=W[c];W[c]=W[p];W[p]=t;const dd=W[c][c];for(let j=0;j<2*n;j++)W[c][j]/=dd;for(let r=0;r<n;r++)if(r!==c){const ff=W[r][c];if(ff)for(let j=0;j<2*n;j++)W[r][j]-=ff*W[c][j];}}return W.map(r=>r.slice(n));}
const Di=inv([[d[0],d[1],d[2]],[d[1],d[3],d[4]],[d[2],d[4],d[5]]]);const A=[...Array(6)].map(()=>Array(6).fill(0)),B=[...Array(6)].map(()=>[0]);for(let i=0;i<3;i++){A[i][i+3]=1;A[i+3][1]=Di[i][1]*f[0];A[i+3][2]=Di[i][2]*f[1];B[i+3][0]=Di[i][0];}
const Ts=+process.argv[2]/1000,F=+process.argv[3]||60,ND=+process.argv[4]||1500,TOP=+process.argv[5]||6,IT=+process.argv[6]||60;
const r=SA.dlqr(A,B,[50,50,50,20,700,700],1,Ts),K=r.K,P=r.P,n=Math.max(1,Math.ceil(Ts/0.01)),h=Ts/n;
const L=(()=>{const L=[...Array(6)].map(()=>Array(6).fill(0));for(let i=0;i<6;i++)for(let j=0;j<=i;j++){let s=P[i][j];for(let k=0;k<j;k++)s-=L[i][k]*L[j][k];L[i][j]=i===j?Math.sqrt(s):s/L[j][j];}return L;})();
function back(v){const x=Array(6).fill(0);for(let i=5;i>=0;i--){let s=v[i];for(let k=i+1;k<6;k++)s-=L[k][i]*x[k];x[i]=s/L[i][i];}return x;}
function W(x){let t=0;for(let i=0;i<6;i++)for(let j=0;j<6;j++)t+=x[i]*P[i][j]*x[j];return t;}
let evals=0;function dW(dir,c){evals++;const x=back(dir.map(a=>a*Math.sqrt(c)));let u=0;for(let i=0;i<6;i++)u-=K[i]*x[i];u=Math.max(-F,Math.min(F,u));let y=x;for(let k=0;k<n;k++)y=S.rk4(y,u,h);return W(y)-W(x);}
// linear decrease: M = P - AclᵀPAcl in z-coordinates: N = Lᵀ⁻¹… we form Nz_ij = ΔW_lin(e_i, e_j) numerically from the linear map
const Acl=r.Phi.map((row,i)=>row.map((v,j)=>v-r.Gam[i][0]*K[j]));
const Z=[...Array(6)].map((_,i)=>back([...Array(6)].map((_,j)=>i===j?1:0)));   // x = L^{-T} e_i
function quad(Mx,a,b){let t=0;for(let i=0;i<6;i++)for(let j=0;j<6;j++)t+=a[i]*Mx[i][j]*b[j];return t;}
const AtPA=[...Array(6)].map((_,i)=>[...Array(6)].map((_,j)=>{let t=0;for(let k=0;k<6;k++)for(let l=0;l<6;l++)t+=Acl[k][i]*P[k][l]*Acl[l][j];return t;}));
const Mz=[...Array(6)].map((_,i)=>[...Array(6)].map((_,j)=>quad(P,Z[i],Z[j])-quad(AtPA,Z[i],Z[j])));
function jacobi(S){const n=6,a=S.map(r=>r.slice()),V=[...Array(n)].map((_,i)=>[...Array(n)].map((_,j)=>i===j?1:0));for(let sw=0;sw<50;sw++){let off=0;for(let p=0;p<n;p++)for(let q=p+1;q<n;q++)off+=a[p][q]*a[p][q];if(off<1e-22)break;
 for(let p=0;p<n;p++)for(let q=p+1;q<n;q++){if(Math.abs(a[p][q])<1e-300)continue;const th=(a[q][q]-a[p][p])/(2*a[p][q]),t=Math.sign(th||1)/(Math.abs(th)+Math.sqrt(th*th+1)),c=1/Math.sqrt(t*t+1),s=t*c;
  for(let k=0;k<n;k++){const akp=a[k][p],akq=a[k][q];a[k][p]=c*akp-s*akq;a[k][q]=s*akp+c*akq;}for(let k=0;k<n;k++){const apk=a[p][k],aqk=a[q][k];a[p][k]=c*apk-s*aqk;a[q][k]=s*apk+c*aqk;}
  for(let k=0;k<n;k++){const vkp=V[k][p],vkq=V[k][q];V[k][p]=c*vkp-s*vkq;V[k][q]=s*vkp+c*vkq;}}}return {vals:a.map((r,i)=>r[i]),vecs:[...Array(n)].map((_,j)=>V.map(r=>r[j]))};}
const eg=jacobi(Mz);const order=eg.vals.map((v,i)=>i).sort((a,b)=>eg.vals[a]-eg.vals[b]);
const nrm=v=>{const q=Math.hypot(...v);return v.map(a=>a/q);};
let seed=12345;const rnd=()=>{seed=(seed*1664525+1013904223)%4294967296;return seed/4294967296;};
const dirs=[];for(let k=0;k<ND;k++){const v=[];for(let i=0;i<6;i++)v.push(Math.sqrt(-2*Math.log(rnd()+1e-12))*Math.cos(2*Math.PI*rnd()));dirs.push(nrm(v));}
const SH=[1,0.7,0.4,0.15];
function climb(d,cl){let w0=dW(d,cl),hh=0.05;for(let it=0;it<IT&&hh>1e-6;it++){const gr=[];for(let j=0;j<6;j++){const dd=d.slice();dd[j]+=1e-5;gr.push((dW(nrm(dd),cl)-w0)/1e-5);}const gn=Math.hypot(...gr)||1;const dn=nrm(d.map((v,q)=>v+hh*gr[q]/gn));const w1=dW(dn,cl);if(w1>w0){d=dn;w0=w1;hh*=1.5;if(w0>=0)return w0;}else hh/=2;}return w0;}
function safe(c){const top=[];for(let k=0;k<ND;k++){const cl=c*SH[k%SH.length],w=dW(dirs[k],cl);if(w>=0)return false;const sc=w/cl;if(top.length<TOP||sc>top[top.length-1].sc){top.push({sc,d:dirs[k],cl});top.sort((a,b)=>b.sc-a.sc);if(top.length>TOP)top.pop();}}
 for(const i of order.slice(0,3))for(const sg of [1,-1])for(const sh of SH){if(climb(eg.vecs[i].map(v=>sg*v),c*sh)>=0)return false;}
 for(const t of top)if(climb(t.d,t.cl)>=0)return false;return true;}
const t0=Date.now();let lo=1,hi=1e4;if(!safe(lo)){console.log('c*=0');process.exit();}for(let it=0;it<13;it++){const mid=Math.sqrt(lo*hi);if(safe(mid))lo=mid;else hi=mid;}
console.log(`Ts=${Ts*1000} ms, ${F} N, ND=${ND}: c* = ${lo.toFixed(2)} (${evals} maps, ${Date.now()-t0} ms); weakest linear decrease rates per sample ${order.slice(0,3).map(i=>eg.vals[i].toExponential(2)).join(', ')}`);
