"""Fig. 5 note, Figure 4 and Section 07: path of a parcel in the full linear velocity field (16), RK4.
Checks: loop length 1.043 T, loop advance 11.2 cm, mean drift 0.0835 m/s (+3.6 % over (21)), excess at ak = 0.1 and 0.05,
drift at z0 = -0.56 m, step-halving change < 1e-12 m. Run: python3 notes/fig05/fig4_rk4.py"""
import math
G, lam = 9.81, 2.6
k = 2*math.pi/lam; om = math.sqrt(G*k); T = 2*math.pi/om; c = om/k

def run(ak, z0, nper=2000, periods=3.2):
    a = ak/k; r = a*math.exp(k*z0)
    def f(t, x, z):
        e = a*om*math.exp(k*z); th = k*x - om*t
        return e*math.cos(th), e*math.sin(th)
    dt = T/nper; x, z, t = 0.0, z0 + r, 0.0
    tops = [(0.0, x, z)]; prev = [None, None]
    n = int(round(periods*nper))
    for i in range(n):
        k1 = f(t, x, z); k2 = f(t+dt/2, x+dt/2*k1[0], z+dt/2*k1[1]); k3 = f(t+dt/2, x+dt/2*k2[0], z+dt/2*k2[1]); k4 = f(t+dt, x+dt*k3[0], z+dt*k3[1])
        xn = x + dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]); zn = z + dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        # a top: vertical velocity changes sign from + to -  (refine by linear interpolation of w)
        w0 = f(t, x, z)[1]; w1 = f(t+dt, xn, zn)[1]
        if i > 0 and w0 > 0 and w1 <= 0:
            s = w0/(w0 - w1); tops.append((t + s*dt, x + s*(xn-x), z + s*(zn-z)))
        x, z, t = xn, zn, t + dt
    return tops, (x, z)

for ak, z0 in [(0.2, 0.0), (0.1, 0.0), (0.05, 0.0), (0.2, -0.56)]:
    tops, end = run(ak, z0)
    (t0, x0_, _), (t1, x1, _) = tops[0], tops[1]
    US = c*ak*ak*math.exp(2*k*z0)
    drift = (x1 - x0_)/(t1 - t0)
    print('ak=%.2f z0=%5.2f: loop %.4f T, advance %.2f cm, drift %.5f m/s, (21) %.5f m/s, excess %.2f %%, tops x(cm) %s, top z %.4f m' %
          (ak, z0, (t1-t0)/T, 100*(x1-x0_), drift, US, 100*(drift/US-1), [round(100*p[1], 2) for p in tops], tops[0][2]))
# step halving
_, e1 = run(0.2, 0.0, 2000); _, e2 = run(0.2, 0.0, 4000)
print('halving the step: |dx| = %.2e m, |dz| = %.2e m' % (abs(e1[0]-e2[0]), abs(e1[1]-e2[1])))
