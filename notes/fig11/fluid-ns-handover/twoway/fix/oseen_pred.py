# Linear steady Oseen prediction of the rods' self-induced velocity, point by point.
# rho U du/dx = -grad p + mu lap u - (1/b) sum_j F_j delta_h(x - X_j),  div u = 0  (unbounded plane approximated by a large periodic box)
# F_j = f_j * wq_j is the force (N) the water puts on rod point j; the water receives -F_j. Kernel: Peskin 4-point, read with the same kernel.
import json, sys, numpy as np
def phi4(r):
    r = np.abs(r); out = np.zeros_like(r)
    a = r < 1; out[a] = (3 - 2*r[a] + np.sqrt(1 + 4*r[a] - 4*r[a]**2))/8
    b = (r >= 1) & (r < 2); out[b] = (5 - 2*r[b] - np.sqrt(-7 + 12*r[b] - 4*r[b]**2))/8
    return out
def predict(d, Lbox=40.0, h=None, Uadv=None, ell=2.0):
    h = h or d['dx']; n = int(round(Lbox/h)); n += n % 2
    rho, nu, b, U = d['rho'], d['nu'], d['b'], (Uadv if Uadv is not None else d['U'])
    fx = np.zeros((n, n)); fy = np.zeros((n, n)); x0 = -Lbox/2
    P = d['pts']
    for q in P:
        gx = (q['X'] - x0)/h; gy = (q['Y'] - x0)/h; i0 = int(np.floor(gx)); j0 = int(np.floor(gy))
        I = np.arange(i0-1, i0+3); J = np.arange(j0-1, j0+3)
        w = np.outer(phi4(J - gy), phi4(I - gx))/(h*h)          # delta_h, area one
        fx[np.ix_(J % n, I % n)] += -q['fx']*q['wq']*w/b; fy[np.ix_(J % n, I % n)] += -q['fy']*q['wq']*w/b
    k = 2*np.pi*np.fft.fftfreq(n, h); KX, KY = np.meshgrid(k, k); K2 = KX**2 + KY**2; K2[0, 0] = 1
    Fx, Fy = np.fft.fft2(fx), np.fft.fft2(fy)
    dot = (KX*Fx + KY*Fy)/K2; Px, Py = Fx - KX*dot, Fy - KY*dot          # Leray projection
    den = rho*(nu*K2 + 1j*U*KX + abs(U)/ell); den[0, 0] = 1   # damping alpha = U/ell: the wake leaves the tank after about ell metres
    ux = np.real(np.fft.ifft2(Px/den)); uy = np.real(np.fft.ifft2(Py/den)); ux -= ux.mean(); uy -= uy.mean()
    res = []
    for q in P:
        gx = (q['X'] - x0)/h; gy = (q['Y'] - x0)/h; i0 = int(np.floor(gx)); j0 = int(np.floor(gy))
        I = np.arange(i0-1, i0+3); J = np.arange(j0-1, j0+3); w = np.outer(phi4(J - gy), phi4(I - gx))
        res.append((np.sum(w*ux[np.ix_(J % n, I % n)]), np.sum(w*uy[np.ix_(J % n, I % n)])))
    return np.array(res)
if __name__ == '__main__':
    for f in sys.argv[1:]:
        d = json.load(open(f)); U = d['U']; P = d['pts']
        meas = np.array([U - q['ux'] for q in P])            # measured slowing at each point
        for ell in (1.0, 2.0, 4.0):
            pr = predict(d, Lbox=40.0, ell=ell); pred = -pr[:, 0]
            print(f"{d['med']:8s} U={U:5} ell={ell:4}: mean slowing/U meas {meas.mean()/U:.4f} pred {pred.mean()/U:.4f}  ratio {pred.mean()/meas.mean():.3f}  pointwise rms(pred-meas)/U {np.sqrt(np.mean((pred-meas)**2))/U:.4f}")
