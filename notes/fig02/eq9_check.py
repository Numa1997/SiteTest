# Fig. 2: eq. (9) against a direct numerical solve of (8), 10 000 random states and slider parameters. Run: python3 -I notes/fig02/eq9_check.py
import numpy as np
g=9.81; m1=1.0; l1=1.0
for seed in range(5):
    rng=np.random.default_rng(seed)
    worst_vec=0; worst_comp=0
    for _ in range(10000):
        t1,t2=rng.uniform(-np.pi,np.pi,2); o1,o2=rng.uniform(-5,5,2)
        m2=m1*np.exp(rng.uniform(-2.3,2.3)); l2=l1*np.exp(rng.uniform(-1.6,1.6))
        d=t1-t2
        den=2*m1+m2-m2*np.cos(2*d)
        a1=(-g*(2*m1+m2)*np.sin(t1)-m2*g*np.sin(t1-2*t2)-2*np.sin(d)*m2*(o2*o2*l2+o1*o1*l1*np.cos(d)))/(l1*den)
        a2=(2*np.sin(d)*(o1*o1*l1*(m1+m2)+g*(m1+m2)*np.cos(t1)+o2*o2*l2*m2*np.cos(d)))/(l2*den)
        M=np.array([[(m1+m2)*l1,m2*l2*np.cos(d)],[l1*np.cos(d),l2]])
        b=np.array([-m2*l2*o2**2*np.sin(d)-(m1+m2)*g*np.sin(t1), l1*o1**2*np.sin(d)-g*np.sin(t2)])
        x=np.linalg.solve(M,b)
        worst_vec=max(worst_vec,np.linalg.norm(x-[a1,a2])/np.linalg.norm(x))
        worst_comp=max(worst_comp,max(abs(x[0]-a1)/max(abs(x[0]),1e-300),abs(x[1]-a2)/max(abs(x[1]),1e-300)))
    print(f'seed {seed}: worst relative difference, vector norm {worst_vec:.2e}; per component {worst_comp:.2e}')
