// Sampled-data LQR for the browser: exact zero-order-hold model, exact sampled cost (Van Loan 1978), discrete Riccati by doubling (SDA)
function zeros(n,m){const A=[];for(let i=0;i<n;i++)A.push(new Array(m).fill(0));return A;}
function mul(A,B){const n=A.length,m=B[0].length,k=B.length,C=zeros(n,m);for(let i=0;i<n;i++)for(let l=0;l<k;l++){const a=A[i][l];if(a===0)continue;for(let j=0;j<m;j++)C[i][j]+=a*B[l][j];}return C;}
function addm(A,B,s){return A.map((r,i)=>r.map((v,j)=>v+(s===undefined?1:s)*B[i][j]));}
function tr(A){return A[0].map((_,j)=>A.map(r=>r[j]));}
function eye(n){const I=zeros(n,n);for(let i=0;i<n;i++)I[i][i]=1;return I;}
function inv(A){const n=A.length,W=A.map((row,i)=>{const e=new Array(n).fill(0);e[i]=1;return row.concat(e);});
 for(let c=0;c<n;c++){let p=c;for(let r=c+1;r<n;r++)if(Math.abs(W[r][c])>Math.abs(W[p][c]))p=r;const t=W[c];W[c]=W[p];W[p]=t;const d=W[c][c];for(let j=0;j<2*n;j++)W[c][j]/=d;
  for(let r=0;r<n;r++)if(r!==c){const f=W[r][c];if(f)for(let j=0;j<2*n;j++)W[r][j]-=f*W[c][j];}}return W.map(r=>r.slice(n));}
function expm(M){ // scaling and squaring with an 18-term Taylor series: e^M = (e^{M/2^s})^(2^s)
 const n=M.length;let nm=0;for(const r of M)nm=Math.max(nm,r.reduce((a,v)=>a+Math.abs(v),0));
 const s=Math.max(0,Math.ceil(Math.log2(nm/0.25)));const X=M.map(r=>r.map(v=>v/Math.pow(2,s)));
 let E=eye(n),term=eye(n);for(let k=1;k<=18;k++){term=mul(term,X).map(r=>r.map(v=>v/k));E=addm(E,term);}
 for(let i=0;i<s;i++)E=mul(E,E);return E;}
function sampled(A,B,Q,rho,T){ // Φ, Γ, Q_d, N_d, R_d for u held over [0, T]
 const Ab=zeros(7,7);for(let i=0;i<6;i++){for(let j=0;j<6;j++)Ab[i][j]=A[i][j];Ab[i][6]=B[i][0];}
 const E=expm(Ab.map(r=>r.map(v=>v*T)));const Phi=E.slice(0,6).map(r=>r.slice(0,6)),Gam=E.slice(0,6).map(r=>[r[6]]);
 const C=zeros(14,14);for(let i=0;i<7;i++)for(let j=0;j<7;j++){C[i][j]=-Ab[j][i]*T;C[7+i][7+j]=Ab[i][j]*T;}for(let i=0;i<6;i++)C[i][7+i]=Q[i]*T;C[6][13]=rho*T;
 const F=expm(C),F12=F.slice(0,7).map(r=>r.slice(7)),F22=F.slice(7).map(r=>r.slice(7));let Mi=mul(tr(F22),F12);Mi=Mi.map((r,i)=>r.map((v,j)=>(v+Mi[j][i])/2));
 return {Phi,Gam,Qd:Mi.slice(0,6).map(r=>r.slice(0,6)),Nd:Mi.slice(0,6).map(r=>[r[6]]),Rd:Mi[6][6]};}
function dlqr(A,B,Q,rho,T){ const S=sampled(A,B,Q,rho,T),{Phi,Gam,Qd,Nd,Rd}=S;
 // remove the cross term: Ā = Φ − Γ R⁻¹ Nᵀ, Q̄ = Q_d − N R⁻¹ Nᵀ, G = Γ R⁻¹ Γᵀ; then P = ĀᵀP(I+GP)⁻¹Ā + Q̄
 let Ak=addm(Phi,mul(Gam,tr(Nd)),-1/Rd),Gk=mul(Gam,tr(Gam)).map(r=>r.map(v=>v/Rd)),Hk=addm(Qd,mul(Nd,tr(Nd)),-1/Rd);
 for(let it=0;it<60;it++){const Wi=inv(addm(eye(6),mul(Gk,Hk)));const AW=mul(Ak,Wi);
  const An=mul(AW,Ak),Gn=addm(Gk,mul(mul(AW,Gk),tr(Ak))),Hn=addm(Hk,mul(mul(tr(Ak),Hk),mul(Wi,Ak)));
  let dh=0,hn=0;for(let i=0;i<6;i++)for(let j=0;j<6;j++){dh+=Math.abs(Hn[i][j]-Hk[i][j]);hn+=Math.abs(Hn[i][j]);}
  Ak=An;Gk=Gn;Hk=Hn.map((r,i)=>r.map((v,j)=>(v+Hn[j][i])/2));if(dh<1e-13*hn)break;}
 const P=Hk,GP=mul(tr(Gam),P),den=Rd+mul(GP,Gam)[0][0],num=addm(mul(GP,Phi),tr(Nd))[0];
 return {K:num.map(v=>v/den),P,Phi,Gam};}
module.exports={dlqr,sampled,expm};
if(require.main===module){
 const m0=1.5,m1=.5,m2=.75,L1=.5,L2=.75,g=9.81,d=[m0+m1+m2,(m1/2+m2)*L1,m2*L2/2,(m1/3+m2)*L1*L1,m2*L1*L2/2,m2*L2*L2/3],f=[(m1/2+m2)*L1*g,m2*L2*g/2];
 const Di=inv([[d[0],d[1],d[2]],[d[1],d[3],d[4]],[d[2],d[4],d[5]]]);const A=zeros(6,6),B=zeros(6,1);for(let i=0;i<3;i++){A[i][i+3]=1;A[i+3][1]=Di[i][1]*f[0];A[i+3][2]=Di[i][2]*f[1];B[i+3][0]=Di[i][0];}
 const ref=require('./gains.json'),Q=[50,50,50,20,700,700];
 for(const [T,key,pk] of [[0.01,'K10','P10'],[0.04,'K40','P40']]){const t0=Date.now();const r=dlqr(A,B,Q,1,T);
  const dk=Math.max(...r.K.map((v,i)=>Math.abs(v-ref[key][i])/Math.max(1,Math.abs(ref[key][i]))));let dp=0;for(let i=0;i<6;i++)for(let j=0;j<6;j++)dp=Math.max(dp,Math.abs(r.P[i][j]-ref[pk][i][j])/Math.max(1,Math.abs(ref[pk][i][j])));
  console.log(`T=${T*1000} ms: K=${r.K.map(v=>v.toFixed(3)).join(', ')}  max rel diff K ${dk.toExponential(1)}, P ${dp.toExponential(1)}, ${Date.now()-t0} ms`);}
 for(const T of [0.001,0.12]){const t0=Date.now();const r=dlqr(A,B,Q,1,T);console.log(`T=${T*1000} ms: K=${r.K.map(v=>v.toFixed(2)).join(', ')} (${Date.now()-t0} ms)`);}
}
