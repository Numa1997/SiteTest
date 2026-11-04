// Multiple-shooting / collocation swing-up planner (Levenberg-Marquardt on defects), then TVLQR for tracking.
const S=require('./sim.js');
function stepZ(s,u,dt,nsub){const h=dt/nsub;for(let i=0;i<nsub;i++)s=S.rk4(s,u,h);return s;}
function solveLin(A,b){const n=b.length;const M=A.map((r,i)=>r.slice().concat(b[i]));for(let i=0;i<n;i++){let k=i;for(let r=i+1;r<n;r++)if(Math.abs(M[r][i])>Math.abs(M[k][i]))k=r;[M[i],M[k]]=[M[k],M[i]];const piv=M[i][i];for(let r=i+1;r<n;r++){const m=M[r][i]/piv;if(m!==0)for(let c=i;c<=n;c++)M[r][c]-=m*M[i][c];}}const x=Array(n).fill(0);for(let i=n-1;i>=0;i--){let s=M[i][n];for(let c=i+1;c<n;c++)s-=M[i][c]*x[c];x[i]=s/M[i][i];}return x;}
function planCol(s0,T,o){const M=o.M||40,dt=T/M,nsub=o.nsub||5;const tgt=[0,2*Math.PI*Math.round(s0[1]/(2*Math.PI)),2*Math.PI*Math.round(s0[2]/(2*Math.PI))];
 const nz=6*M,nx=nz+M; let X=new Array(nx).fill(0);
 for(let k=1;k<=M;k++){const f=k/M;X[6*(k-1)+0]=s0[0];X[6*(k-1)+1]=s0[1]+(tgt[1]-s0[1])*f;X[6*(k-1)+2]=s0[2]+(tgt[2]-s0[2])*f;X[6*(k-1)+3]=0;X[6*(k-1)+4]=(tgt[1]-s0[1])/T;X[6*(k-1)+5]=(tgt[2]-s0[2])/T;}
 const zOf=(X,k)=>k==0?s0:X.slice(6*(k-1),6*k);
 function resid(X){const R=[];for(let k=0;k<M;k++){const z=zOf(X,k),zn=zOf(X,k+1),u=X[nz+k];const st=stepZ(z,u,dt,nsub);for(let i=0;i<6;i++)R.push(o.wd*(zn[i]-st[i]));}
  const zT=zOf(X,M);R.push(o.wT*(zT[1]-tgt[1]),o.wT*(zT[2]-tgt[2]),o.wT*zT[4],o.wT*zT[5],o.wT*0.3*zT[3]);
  for(let k=1;k<=M;k++){const z=zOf(X,k);R.push(o.wl*Math.max(0,Math.abs(z[0])-o.xlim));}
  for(let k=0;k<M;k++){R.push(o.wu*Math.max(0,Math.abs(X[nz+k])-o.ulim));R.push(o.wr*X[nz+k]);if(k>0)R.push(o.ws*(X[nz+k]-X[nz+k-1]));}
  return R;}
 function jac(X,R0){ // sparse structure but built dense by finite differences of local blocks
  const m=R0.length;const J=Array.from({length:m},()=>new Float64Array(nx));let row=0;
  for(let k=0;k<M;k++){const z=zOf(X,k),u=X[nz+k];const base=stepZ(z,u,dt,nsub);
   // d defect / d z_{k+1} = wd*I ; d/dz_k = -wd*dstep/dz ; d/du = -wd*dstep/du
   for(let i=0;i<6;i++){ if(k+1<=M){J[row+i][6*k+i]=o.wd;} }
   if(k>0){for(let j=0;j<6;j++){const e=1e-6*Math.max(1,Math.abs(z[j]));const zz=z.slice();zz[j]+=e;const st=stepZ(zz,u,dt,nsub);for(let i=0;i<6;i++)J[row+i][6*(k-1)+j]=-o.wd*(st[i]-base[i])/e;}}
   {const e=1e-6*Math.max(1,Math.abs(u));const st=stepZ(z,u+e,dt,nsub);for(let i=0;i<6;i++)J[row+i][nz+k]=-o.wd*(st[i]-base[i])/e;}
   row+=6;}
  // terminal
  J[row][6*(M-1)+1]=o.wT;J[row+1][6*(M-1)+2]=o.wT;J[row+2][6*(M-1)+4]=o.wT;J[row+3][6*(M-1)+5]=o.wT;J[row+4][6*(M-1)+3]=o.wT*0.3;row+=5;
  for(let k=1;k<=M;k++){const z=zOf(X,k);if(Math.abs(z[0])>o.xlim)J[row][6*(k-1)]=o.wl*Math.sign(z[0]);row++;}
  for(let k=0;k<M;k++){if(Math.abs(X[nz+k])>o.ulim)J[row][nz+k]=o.wu*Math.sign(X[nz+k]);row++;J[row][nz+k]=o.wr;row++;if(k>0){J[row][nz+k]=o.ws;J[row][nz+k-1]=-o.ws;row++;}}
  return J;}
 let R=resid(X),c=R.reduce((a,v)=>a+v*v,0),lam=1e-2,it=0;
 for(;it<(o.maxIt||80);it++){const J=jac(X,R);const m=R.length;const A=Array.from({length:nx},()=>new Float64Array(nx));const g=new Float64Array(nx);
  for(let r=0;r<m;r++){const Jr=J[r];const rr=R[r];for(let i=0;i<nx;i++){const a=Jr[i];if(a===0)continue;g[i]+=a*rr;const Ai=A[i];for(let j=i;j<nx;j++){const b=Jr[j];if(b!==0)Ai[j]+=a*b;}}}
  for(let i=0;i<nx;i++)for(let j=0;j<i;j++)A[i][j]=A[j][i];
  let ok=false;for(let tr=0;tr<10;tr++){const Al=A.map((r,i)=>{const q=Array.from(r);q[i]+=lam*(1e-6+A[i][i]);return q;});const d=solveLin(Al,Array.from(g).map(v=>-v));const Xn=X.map((v,i)=>v+d[i]);const Rn=resid(Xn);const cn=Rn.reduce((a,v)=>a+v*v,0);if(cn<c){X=Xn;R=Rn;const rel=(c-cn)/c;c=cn;lam=Math.max(lam/4,1e-9);ok=true;if(rel<1e-9)it=1e9;break;}lam*=4;}
  if(!ok)break;if(o.verbose)console.log(it,c.toExponential(2));}
 // defects only
 let dmax=0;for(let k=0;k<M;k++){const st=stepZ(zOf(X,k),X[nz+k],dt,nsub),zn=zOf(X,k+1);for(let i=0;i<6;i++)dmax=Math.max(dmax,Math.abs(zn[i]-st[i]));}
 const Z=[s0.slice()];for(let k=1;k<=M;k++)Z.push(zOf(X,k));const U=X.slice(nz);
 return {Z,U,dt,T,M,cost:c,dmax,tgt,iters:it};}
module.exports={planCol,stepZ,solveLin};
if(require.main===module){const s0=[0,Math.PI-0.02,Math.PI-0.02,0,0,0];const t0=Date.now();
 const r=planCol(s0,4,{M:40,nsub:5,wd:100,wT:30,wl:20,wu:1,wr:0.02,ws:0.02,xlim:1.5,ulim:60,verbose:true,maxIt:100});
 console.log('cost',r.cost.toExponential(2),'defect max',r.dmax.toExponential(2),'iters',r.iters,'umax',Math.max(...r.U.map(Math.abs)).toFixed(1),'xmax',Math.max(...r.Z.map(z=>Math.abs(z[0]))).toFixed(2),'end',r.Z[r.M].map(v=>+v.toFixed(3)).join(','),'s',((Date.now()-t0)/1000).toFixed(1));}
