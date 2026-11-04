const S=require('./sim.js');const d=S.p.d,f=S.p.f;
function Ep(s){const D=S.Dm(s[1],s[2]);const w=[s[4],s[5]];return 0.5*(w[0]*(D[1][1]*w[0]+D[1][2]*w[1])+w[1]*(D[2][1]*w[0]+D[2][2]*w[1]))+f[0]*Math.cos(s[1])+f[1]*Math.cos(s[2]);}
function Pp(s){return d[1]*Math.cos(s[1])*s[4]+d[2]*Math.cos(s[2])*s[5];}
// force that produces cart acceleration a: rows 2,3 give angular accels for given a, row 1 gives u
function uFor(s,a){const D=S.Dm(s[1],s[2]),s1=Math.sin(s[1]),s2=Math.sin(s[2]),s12=Math.sin(s[1]-s[2]);
 const r2=-D[1][0]*a-d[4]*s12*s[5]*s[5]+f[0]*s1, r3=-D[2][0]*a+d[4]*s12*s[4]*s[4]+f[1]*s2;
 const det=D[1][1]*D[2][2]-D[1][2]*D[2][1], b1=(r2*D[2][2]-D[1][2]*r3)/det, b2=(D[1][1]*r3-D[2][1]*r2)/det;
 return D[0][0]*a+D[0][1]*b1+D[0][2]*b2-d[1]*s1*s[4]*s[4]-d[2]*s2*s[5]*s[5];}
const cases=[[0.12,1.67,-2.11,0.47,-2.73,-2.00],[-0.18,-1.49,1.05,0.33,-1.25,0.18],[0.36,-0.79,-1.76,0.21,-1.71,1.85],[0.33,-1.26,-2.88,0.43,-2.57,-2.31],[-0.19,-0.48,0.93,-0.14,-0.63,0.70],[-0.37,0.60,2.23,-0.27,2.98,0.37],[0.49,1.65,-1.50,-0.32,-2.32,2.32],[0.07,-0.57,-1.33,-0.32,1.50,-0.56],[-0.35,-1.59,0.80,0.31,0.21,2.69],[-0.26,0.76,0.65,0.02,0.31,1.35],[0.20,0.94,2.02,-0.05,2.94,0.26]];
module.exports={Ep,Pp,uFor,d,f};
