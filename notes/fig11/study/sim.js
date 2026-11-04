const PK=require('./PK.json'); const P=PK.P,K=PK.K;
const G=9.81; function par(m0=1.5,m1=.5,m2=.75,L1=.5,L2=.75){return {d:[m0+m1+m2,(m1/2+m2)*L1,m2*L2/2,(m1/3+m2)*L1*L1,m2*L1*L2/2,m2*L2*L2/3],f:[(m1/2+m2)*L1*G,m2*L2*G/2]};}
const p=par();
function solve3(A,b){const M=[A[0].concat(b[0]),A[1].concat(b[1]),A[2].concat(b[2])];for(let i=0;i<3;i++){let k=i;for(let r=i+1;r<3;r++)if(Math.abs(M[r][i])>Math.abs(M[k][i]))k=r;[M[i],M[k]]=[M[k],M[i]];for(let r=i+1;r<3;r++){const m=M[r][i]/M[i][i];for(let c=i;c<4;c++)M[r][c]-=m*M[i][c];}}const x=[0,0,0];for(let i=2;i>=0;i--){let s=M[i][3];for(let c=i+1;c<3;c++)s-=M[i][c]*x[c];x[i]=s/M[i][i];}return x;}
function Dm(a,b){const d=p.d,c1=Math.cos(a),c2=Math.cos(b),c12=Math.cos(a-b);return [[d[0],d[1]*c1,d[2]*c2],[d[1]*c1,d[3],d[4]*c12],[d[2]*c2,d[4]*c12,d[5]]];}
function rhs(s,u){const d=p.d,f=p.f,a=s[1],b=s[2],xd=s[3],ad=s[4],bd=s[5];const D=Dm(a,b);const s1=Math.sin(a),s2=Math.sin(b),s12=Math.sin(a-b);
 const Cq=[-d[1]*s1*ad*ad-d[2]*s2*bd*bd, d[4]*s12*bd*bd, -d[4]*s12*ad*ad]; // C*qd with C row1=[0,-d2 s1 ad,-d3 s2 bd]*qd -> uses ad,bd once; see below
 // C qd exactly: row1 = -d2 s1 ad*ad - d3 s2 bd*bd ; row2 = d5 s12 bd*bd ; row3 = -d5 s12 ad*ad
 const Gv=[0,-f[0]*s1,-f[1]*s2];const q=solve3(D,[u-Cq[0]-Gv[0],-Cq[1]-Gv[1],-Cq[2]-Gv[2]]);return [xd,ad,bd,q[0],q[1],q[2]];}
function rk4(s,u,h){const k1=rhs(s,u),a=s.map((v,i)=>v+h/2*k1[i]),k2=rhs(a,u),b=s.map((v,i)=>v+h/2*k2[i]),k3=rhs(b,u),c=s.map((v,i)=>v+h*k3[i]),k4=rhs(c,u);return s.map((v,i)=>v+h/6*(k1[i]+2*k2[i]+2*k3[i]+k4[i]));}
function wrapA(s){const w=s.slice();for(const i of [1,2])w[i]=((w[i]+Math.PI)%(2*Math.PI)+2*Math.PI)%(2*Math.PI)-Math.PI;return w;}
function V(w){let t=0;for(let i=0;i<6;i++)for(let j=0;j<6;j++)t+=w[i]*P[i][j]*w[j];return t;}
module.exports={p,par,rhs,rk4,K,P,wrapA,V,Dm,solve3,setp:(q)=>Object.assign(p,q)};
