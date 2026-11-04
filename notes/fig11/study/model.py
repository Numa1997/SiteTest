import numpy as np, json
from scipy.linalg import expm, solve_discrete_are, solve_continuous_are
m0,m1,m2,L1,L2,g=1.5,.5,.75,.5,.75,9.81
d=[m0+m1+m2,(m1/2+m2)*L1,m2*L2/2,(m1/3+m2)*L1**2,m2*L1*L2/2,m2*L2**2/3]; f=[(m1/2+m2)*L1*g,m2*L2*g/2]
D0=np.array([[d[0],d[1],d[2]],[d[1],d[3],d[4]],[d[2],d[4],d[5]]]); Di=np.linalg.inv(D0)
A=np.zeros((6,6)); A[:3,3:]=np.eye(3); A[3:,:3]=Di@np.diag([0,f[0],f[1]]); B=np.zeros((6,1)); B[3:,0]=Di[:,0]
Q=np.diag([50,50,50,20,700,700.]); rho=1.0
P=solve_continuous_are(A,B,Q,np.array([[rho]])); K=(B.T@P)/rho
def sampled(T):
    Ab=np.zeros((7,7)); Ab[:6,:6]=A; Ab[:6,6:]=B           # augmented state (s, u) with du/dt = 0
    E=expm(Ab*T); Phi,Gam=E[:6,:6],E[:6,6:]
    Qb=np.zeros((7,7)); Qb[:6,:6]=Q; Qb[6,6]=rho
    C=np.zeros((14,14)); C[:7,:7]=-Ab.T; C[:7,7:]=Qb; C[7:,7:]=Ab   # Van Loan 1978
    F=expm(C*T); M=F[7:,7:].T@F[:7,7:]; M=(M+M.T)/2
    return Phi,Gam,M[:6,:6],M[:6,6:],M[6:,6:]
def dlqr(T):
    Phi,Gam,Qd,Nd,Rd=sampled(T)
    Pd=solve_discrete_are(Phi,Gam,Qd,Rd,s=Nd); Kd=np.linalg.solve(Rd+Gam.T@Pd@Gam,Gam.T@Pd@Phi+Nd.T)
    return Phi,Gam,Pd,Kd
rows=[]
print("continuous K", np.round(K[0],3))
for Tms in [0.1,1,5,10,20,30,34,35,40,60,80,120]:
    T=Tms/1000; Phi,Gam,Pd,Kd=dlqr(T)
    rc=max(abs(np.linalg.eigvals(Phi-Gam@K))); rd=max(abs(np.linalg.eigvals(Phi-Gam@Kd)))
    rows.append(dict(T=Tms,rho_cont=rc,rho_disc=rd,Kd=Kd[0].tolist()))
    print(f"T={Tms:6.1f} ms  rho(cont gains)={rc:.4f}  rho(designed)={rd:.4f}  Kd={np.round(Kd[0],2)}  |Pd-P|/|P|={np.linalg.norm(Pd-P)/np.linalg.norm(P):.2e}")
json.dump(rows,open('table.json','w'),indent=1)
_,_,P10,K10=dlqr(0.010); _,_,P40,K40=dlqr(0.040)
json.dump({'K10':K10[0].tolist(),'K40':K40[0].tolist(),'P10':P10.tolist(),'P40':P40.tolist(),'Kc':K[0].tolist()},open('gains.json','w'))
